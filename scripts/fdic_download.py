"""
FDIC data acquisition — bank distress early-warning project (MSDS 696).

Downloads four datasets from the FDIC BankFind Suite API (https://api.fdic.gov/banks):
  1. financials        - quarterly call-report data, all fields, one file per quarter
  2. institutions      - bank directory (identity, charter, status)
  3. failures          - failed-bank list (ground truth)
  4. history           - structure changes (mergers, acquisitions, closures)

Design constraints validated against the official OpenAPI spec (docs/swagger.yaml):
  - fields param: requests with >250 fields are capped at limit=500, so fields are
    pulled in chunks of <=250 and merged on the API's ID key (CERT_REPDTE).
  - limit: max 10,000 records per request; quarters with more banks are paginated
    with offset, sorted by CERT so page order is deterministic.
  - every page is verified: rows received == rows expected, total across pages ==
    the API's meta.total, and no duplicate CERTs. A quarter is saved only if every
    check passes.

Usage:
  python fdic_download.py --smoke        # 2022-2023 only (8 quarters)
  python fdic_download.py                # full 1984-present run (resumes if interrupted)
"""

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd
import yaml

BASE = "https://api.fdic.gov/banks"
HERE = Path(__file__).resolve().parent
REF = HERE.parent / "data_reference"
DATA = HERE.parent / "data"
RAW = DATA / "raw"

CHUNK_SIZE = 250          # documented: >250 fields caps limit at 500
PAGE_LIMIT = 10_000       # documented max records per request
PAUSE = 0.25              # seconds between requests (politeness)
RETRIES = 3


def get_json(url: str) -> dict:
    """GET a URL with retries; raise after RETRIES failures."""
    last_err = None
    for attempt in range(1, RETRIES + 1):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001 - retry any transport error
            last_err = e
            time.sleep(2 * attempt)
    raise RuntimeError(f"failed after {RETRIES} attempts: {url[:120]}... ({last_err})")


def load_fields(properties_file: str) -> list[str]:
    """All field names from an FDIC properties YAML (the official data dictionary)."""
    d = yaml.safe_load(open(REF / properties_file))
    return list(d["properties"]["data"]["properties"].keys())


def fetch_all(endpoint: str, filters: str | None, fields: list[str], sort_by: str) -> pd.DataFrame:
    """Fetch every record for one endpoint+filter, one field-chunk at a time,
    paginating inside each chunk. Returns one wide DataFrame keyed by ID."""
    chunks = [fields[i : i + CHUNK_SIZE] for i in range(0, len(fields), CHUNK_SIZE)]
    merged: pd.DataFrame | None = None
    expected_total: int | None = None

    for ci, chunk in enumerate(chunks):
        params = {
            "fields": ",".join(chunk),
            "limit": PAGE_LIMIT,
            "sort_by": sort_by,
            "sort_order": "ASC",
        }
        if filters:
            params["filters"] = filters

        rows: list[dict] = []
        offset = 0
        while True:
            params["offset"] = offset
            url = f"{BASE}/{endpoint}?{urllib.parse.urlencode(params)}"
            j = get_json(url)
            total = j["meta"]["total"]
            page = [rec["data"] for rec in j["data"]]
            expected_page = min(PAGE_LIMIT, total - offset)
            if len(page) != expected_page:
                raise RuntimeError(
                    f"{endpoint} chunk {ci} offset {offset}: got {len(page)} rows, expected {expected_page}"
                )
            rows.extend(page)
            offset += len(page)
            time.sleep(PAUSE)
            if offset >= total:
                break

        if len(rows) != total:
            raise RuntimeError(f"{endpoint} chunk {ci}: {len(rows)} rows != meta.total {total}")
        if expected_total is None:
            expected_total = total
        elif total != expected_total:
            raise RuntimeError(f"{endpoint} chunk {ci}: total {total} != first chunk's {expected_total}")

        df = pd.DataFrame(rows).set_index("ID")
        if df.index.duplicated().any():
            raise RuntimeError(f"{endpoint} chunk {ci}: duplicate ID keys")
        if merged is None:
            merged = df
        else:
            new_cols = df.columns.difference(merged.columns)
            merged = merged.join(df[new_cols], how="outer", validate="one_to_one")
            if len(merged) != expected_total:
                raise RuntimeError(f"{endpoint}: row count changed after joining chunk {ci}")

    return merged.reset_index() if merged is not None else pd.DataFrame()


def quarters(start_year: int, end_year: int) -> list[str]:
    return [f"{y}{md}" for y in range(start_year, end_year + 1) for md in ("0331", "0630", "0930", "1231")]


def download_financials(start_year: int, end_year: int) -> None:
    fields = load_fields("risview_properties.yaml")
    print(f"financials: {len(fields)} fields -> {-(-len(fields) // CHUNK_SIZE)} chunks per quarter")
    for q in quarters(start_year, end_year):
        out = RAW / f"financials_{q}.parquet"
        if out.exists():
            print(f"  {q}: exists, skipping")
            continue
        probe = get_json(f"{BASE}/financials?filters=REPDTE:{q}&fields=CERT&limit=1")
        total = probe["meta"]["total"]
        if total == 0:
            print(f"  {q}: no data (future or unpublished quarter), skipping")
            continue
        t0 = time.time()
        df = fetch_all("financials", f"REPDTE:{q}", fields, sort_by="CERT")
        if df["CERT"].duplicated().any():
            raise RuntimeError(f"{q}: duplicate CERT within quarter")
        if len(df) != total:
            raise RuntimeError(f"{q}: final rows {len(df)} != probe total {total}")
        tmp = out.with_suffix(".parquet.tmp")
        df.to_parquet(tmp, index=False)
        tmp.rename(out)  # atomic: file appears only when complete
        print(f"  {q}: {len(df):,} banks x {df.shape[1]:,} cols in {time.time()-t0:.0f}s -> {out.name}")


def download_support() -> None:
    jobs = [
        ("institutions", "institution_properties.yaml", None, "CERT"),
        ("failures", "failure_properties.yaml", None, "CERT"),
        ("history", "history_properties.yaml", None, "CERT"),
    ]
    for endpoint, props, filters, sort_by in jobs:
        out = RAW / f"{endpoint}.parquet"
        if out.exists():
            print(f"{endpoint}: exists, skipping")
            continue
        fields = load_fields(props)
        t0 = time.time()
        df = fetch_all(endpoint, filters, fields, sort_by=sort_by)
        tmp = out.with_suffix(".parquet.tmp")
        df.to_parquet(tmp, index=False)
        tmp.rename(out)
        print(f"{endpoint}: {len(df):,} rows x {df.shape[1]:,} cols in {time.time()-t0:.0f}s -> {out.name}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true", help="2022-2023 financials only")
    args = ap.parse_args()

    RAW.mkdir(parents=True, exist_ok=True)
    if args.smoke:
        download_financials(2022, 2023)
    else:
        download_financials(1984, 2026)
        download_support()
    print("done.")


if __name__ == "__main__":
    main()
