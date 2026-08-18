"""
FRED data acquisition — macro context for the bank distress early-warning project (MSDS 696).

Downloads a small set of macroeconomic series from the official FRED API
(https://fred.stlouisfed.org/docs/api/fred/) and saves one quarter-end-aligned
table to data/raw/fred.parquet, ready to join to the FDIC panel on REPDTE.

Series (chosen for relevance to bank distress; see project data-fit notes):
  FEDFUNDS  policy rate               DGS10    10-year Treasury yield
  T10Y3M    yield-curve slope         UNRATE   unemployment rate
  GDPC1     real GDP (quarterly)      CPIAUCSL CPI (inflation)
  USSTHPI   FHFA house price index    BAA10Y   corporate credit spread
  USREC     NBER recession indicator   DRTSCILM SLOOS lending standards (1990+)
  NFCI      financial conditions index BOGZ1FL075035503Q  CRE price index

Aggregation to quarters: monthly/daily series are averaged within each calendar
quarter and stamped to the quarter-end date (matching FDIC REPDTE). GDPC1 and
USSTHPI are already quarterly. USREC is taken as "any recession month in quarter".

The API key is read from the FRED_API_KEY environment variable, or a key.txt
file next to this script (gitignore it), so no secret lives in the code.

Usage:
  FRED_API_KEY=... python fred_download.py
"""

import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

BASE = "https://api.stlouisfed.org/fred/series/observations"
HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "data" / "raw"
START = "1983-01-01"  # one year before the FDIC panel starts, for lag features

SERIES = {
    "FEDFUNDS": "mean",   # monthly
    "DGS10": "mean",      # daily
    "T10Y3M": "mean",     # daily
    "UNRATE": "mean",     # monthly
    "GDPC1": "last",      # quarterly
    "CPIAUCSL": "mean",   # monthly
    "USSTHPI": "last",    # quarterly
    "BAA10Y": "mean",     # daily (starts 1986)
    "USREC": "max",       # monthly recession flag -> any month in quarter
    "DRTSCILM": "last",   # SLOOS: % banks tightening C&I standards (quarterly, 1990+)
    "NFCI": "mean",       # Chicago Fed financial conditions index (weekly, full sample)
    "BOGZ1FL075035503Q": "last",  # commercial real estate price index (quarterly)
}


def api_key() -> str:
    key = os.environ.get("FRED_API_KEY")
    if not key:
        keyfile = HERE / "key.txt"
        if keyfile.exists():
            key = keyfile.read_text().strip()
    if not key:
        raise SystemExit("no API key: set FRED_API_KEY or create scripts/key.txt")
    return key


def fetch_series(series_id: str, key: str) -> pd.Series:
    params = {
        "series_id": series_id,
        "api_key": key,
        "file_type": "json",
        "observation_start": START,
        "limit": 100000,
    }
    url = f"{BASE}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=60) as r:
        j = json.load(r)
    obs = j["observations"]
    if not obs:
        raise RuntimeError(f"{series_id}: no observations returned")
    s = pd.Series(
        [float(o["value"]) if o["value"] != "." else None for o in obs],
        index=pd.to_datetime([o["date"] for o in obs]),
        name=series_id,
    ).dropna()
    print(f"  {series_id}: {len(s):,} observations, {s.index.min():%Y-%m} to {s.index.max():%Y-%m}")
    return s


def main() -> None:
    key = api_key()
    RAW.mkdir(parents=True, exist_ok=True)

    quarterly = {}
    for sid, how in SERIES.items():
        s = fetch_series(sid, key)
        q = s.resample("Q").agg(how)
        quarterly[sid] = q
        time.sleep(0.5)

    fred = pd.DataFrame(quarterly)
    fred.index.name = "REPDTE"
    fred = fred.reset_index()

    # sanity checks
    assert fred["REPDTE"].is_unique, "duplicate quarters"
    assert fred["REPDTE"].min().year <= 1984, "series should reach back to the panel start"

    out = RAW / "fred.parquet"
    tmp = out.with_suffix(".parquet.tmp")
    fred.to_parquet(tmp, index=False)
    tmp.rename(out)
    print(f"fred: {fred.shape[0]} quarters x {fred.shape[1]} cols -> {out.name}")


if __name__ == "__main__":
    main()
