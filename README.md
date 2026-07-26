# Predicting U.S. Bank Distress

An early-warning model that flags which U.S. banks are at risk of becoming
**undercapitalized**, and how soon — while the bank can still take corrective action.

MSDS 696 Data Science Practicum II · Regis University · Oussama Ennaciri

---

## The question

The 2023 failures of Silicon Valley Bank and First Republic were visible in public
regulatory data before they happened. This project asks: **which banks are at risk of a
capital-tier drop, and how soon?**

The answer changes what two groups do. A bank's risk committee can raise capital, cut
dividends, restructure its securities portfolio, or pursue a merger. A regulator (FDIC,
OCC, Federal Reserve, state examiners) can escalate examinations before options narrow.

## The target

A **Prompt Corrective Action** tier drop — the regulatory capital categories defined in
[12 CFR 324.403](https://www.law.cornell.edu/cfr/text/12/324.403) and its predecessors.

`onset_4q` = 1 if a currently healthy (well or adequately capitalized) bank falls to
undercapitalized-or-worse within the following four quarters.

The thresholds switch with the rules actually in force at each date:

| Period | Rule |
|---|---|
| 1990–2014 | Original FDICIA — 3 ratios |
| 2015+ | Basel III — adds common equity tier 1 (`CET1`), raises Tier 1 cutoffs |
| 2020+ | Community Bank Leverage Ratio (`CBLR`) overlay for qualifying small banks |

Full derivation and sources: [`literature/pca_label_definition.md`](literature/pca_label_definition.md)

## The data

| Source | What |
|---|---|
| [FDIC BankFind API](https://banks.data.fdic.gov/docs/) | Quarterly filings for every insured institution — financials, institutions, failures, history |
| [FRED](https://fred.stlouisfed.org/) | Macroeconomic context — rates, unemployment, GDP, housing, stress indices |

**Modeling panel:** 1,258,888 bank-quarter rows, 1990Q1–2026Q1, 66 columns.
The target is rare — **0.73%** of healthy bank-quarters cross into distress within a year.

Data files are not in this repo (16 GB). Rebuild them with the scripts below.

## Repo layout

```
scripts/          FDIC and FRED download scripts
notebooks/
  feature_selection.ipynb   Build the panel: joins, 1990 cutoff, PCA tier, onset_4q label
  cleaning.ipynb            Feature dictionary, data-quality concerns, flags
  eda.ipynb                 14 charts
  modeling.ipynb            Leakage guardrail, train/test split, models
  data_concerns.md          Running log of data issues, 5 of 8 resolved
literature/       Paper notes, feature synthesis, regulatory label definition
data_reference/   FDIC API schemas
Week 1-4/         Weekly deliverables (proposal, status reports, talk scripts)
```

## Rebuilding the data

```bash
export FDIC_API_KEY=...    # https://banks.data.fdic.gov/
export FRED_API_KEY=...    # https://fred.stlouisfed.org/docs/api/api_key.html

python scripts/fdic_download.py
python scripts/fred_download.py
```

Then run the notebooks in order: `feature_selection` → `cleaning` → `eda` → `modeling`.

## Two findings so far

**1. The road to trouble.** Banks that later became undercapitalized decline across all six
core vitals for roughly two years beforehand, while matched healthy banks tracked over the
same calendar quarters stay flat. The decline is bank-specific, not macro-driven.

**2. Capital ratios alone missed SVB.** Silicon Valley Bank's total risk-based capital ratio
was ~16% — comfortably "well capitalized" — the quarter before it failed. 88 of 1,360 failed
banks looked healthy at their last filing. The warning was there, but in the funding columns:
uninsured deposits near 86%, deposit growth flipping to sustained outflows, and (tested
against a same-size healthy peer) held-to-maturity losses at 7.5% of assets versus 1.4%.

That gap is what the current work addresses — trend and funding-stability features, not just
the classic capital ratios.

## A note on leakage

The label looks four quarters into the future, which makes this problem unusually easy to
leak. `modeling.ipynb` opens with a guardrail that is enforced, not documented:

- a drop list covering identifiers, label components, and two flags built from future outcomes
- a time-based split — train 1990Q1–2015Q4, a four-quarter gap, test 2017Q1–2025Q1
- assertions that fail loudly on overlapping windows, leaked columns, or a rare-event rate
  that has been quietly rebalanced

## Note on LLM use

LaTeX typesetting, code review, and wording polish were done with Claude Code. All content,
research, and decisions are my own; every suggested edit was reviewed and approved.
