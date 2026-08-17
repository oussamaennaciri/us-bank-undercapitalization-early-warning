# Predicting U.S. Bank Distress

A model that flags which U.S. banks are heading for undercapitalization, using the quarterly
reports every bank files with the FDIC.

**The recommendation:** supervisors should rank the review queue with the model instead of
ranking on the capital ratio alone. At the same workload it finds 30% more troubled banks.

MSDS 696 Data Science Practicum II · Regis University · Oussama Ennaciri

---

## The problem

About 4,900 banks file every quarter. Roughly 5 of them are heading for trouble. Every bank
gets examined eventually, but only every 12 to 18 months, so the order matters: a bank
reviewed sooner has more options left.

The obvious way to order that queue is by capital against assets, which is the measure the
regulation itself uses. That finds half of them.

## The target

A healthy bank falls to undercapitalized or worse within the next four quarters.

The capital tiers come from [12 CFR 324.403](https://www.law.cornell.edu/cfr/text/12/324.403).
The thresholds switch with the rules in force at each date: original FDICIA before 2015,
Basel III after, and a Community Bank Leverage Ratio overlay from 2020.

## The data

| Source | What |
|---|---|
| [FDIC BankFind API](https://banks.data.fdic.gov/docs/) | Quarterly filings for every insured bank |
| [FRED](https://fred.stlouisfed.org/) | Rates, unemployment, GDP, housing, stress indices |

109 inputs per bank-quarter: 98 from the bank's own filing, 11 national economic series.

Split by time, with a gap year, because the label looks four quarters ahead:

| | Period | Rows | Cases |
|---|---|---|---|
| Train | 1990Q1 to 2015Q4 | 1,026,797 | 8,414 |
| Gap | all of 2016 | dropped | |
| Test | 2017Q1 to 2025Q1 | 161,117 scored | 160 |

The data files are not in this repo (16 GB). They are pulled straight from the two public
APIs above.

## The method

Four candidates on the same rows, no tuning, so the comparison is even. Gradient boosting
won and is the model in the results.

| Model | PR-AUC |
|---|---|
| **Gradient boosting** | **0.219** |
| Capital ratio (benchmark) | 0.128 |
| GRU | 0.122 |
| MLP | 0.086 |
| Logistic regression | 0.031 |

## The result

Reading the riskiest 1% of filings, the model finds 65% of troubled banks against 50% for
the capital ratio. It leads at every depth, not just that one.

Of the banks it caught, about 60% were flagged a full year before they crossed. All ten
banks in the test window that became undercapitalized and later failed were flagged first.

## What it cannot do

Most of what it flags is a false alarm: at the 1% depth, 93 in 100 never cross. The capital
ratio is 95 in 100 at the same depth.

It cannot detect a sudden bank run. It reads quarterly filings, and a run happens between
them.

## Repo layout

```
notebooks/
  feature_selection.ipynb   Build the panel, capital tiers, the label
  cleaning.ipynb            Feature dictionary, data-quality flags
  feature_engineering.ipynb Trend and funding features
  eda.ipynb                 Exploratory charts
  modeling.ipynb            Leakage guardrail, split, models, results
reports/          Written deliverables (PDF)
presentations/    Slide decks (PDF)
```

Run the notebooks in order: `feature_selection`, `cleaning`, `feature_engineering`, `eda`,
`modeling`.

## A note on leakage

A label that looks four quarters ahead is easy to leak. `modeling.ipynb` opens with a
guardrail that is enforced rather than described: a drop list covering identifiers and label
components, the time split with its gap year, and assertions that fail loudly on overlapping
windows, leaked columns, or a rare-event rate that has been quietly rebalanced.

## Note on LLM use

LaTeX typesetting, code review, and wording polish were done with Claude Code. All content,
research, and decisions are my own, and every suggested edit was reviewed and approved.
