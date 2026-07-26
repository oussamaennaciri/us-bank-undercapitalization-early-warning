# Data Concerns — to revisit during cleaning/prep

Running list from EDA (`02_eda.ipynb`). Not acted on yet — parking here so nothing gets lost before the cleaning pass.

## 1. PCA ratios don't exist before 1990
- Missing rate for `RBC1AAJ`/`RBC1RWAJ`/`RBCRWAJ` is ~100% for 1984–89, drops to ~0.3% from 1990 on. Not random — PCA didn't exist as a regulatory framework before then.
- **Decision needed:** restrict the modeling window to 1990Q1 forward rather than imputing/backfilling six years the label was never built to support.

## 2. RESOLVED — Small tail of failed banks look "well"/"adequate" right before failing
- Of 1,360 failed banks with a pre-failure filing, 88 (6.5%) looked healthy at the last one. Verified **real, not a date artifact**: gap from last filing to failure is a normal ~2-month reporting lag (median 62 days, max 125), and capital genuinely looked fine (median 11.6%). The 2023 marquee cases are here: SVB (16.0%), Signature (12.3%), First Republic (12.7%) — deposit-run failures.
- **The label is correct** — these banks were genuinely well-capitalized on paper. This is a feature gap (concern #5), not a label error.
- **Warning WAS in the data, in the funding columns:** SVB into failure showed capital rising 11.5%->16% (useless) but uninsured deposits ~86% (standing red flag), deposit growth flipping from +21% to sustained outflows (-5%,-6%,-2%), and cash buffer CHBALR falling 15%->6%. The signal was the deposit-flow *trend*, not any single-quarter level — direct support for building trend features and for concern #5's funding/liquidity features.
- **Fixed in `cleaning.ipynb` (flag only):** added `fast_failure` boolean marking all rows of the 88 healthy-at-last-filing failures (5,227 rows). Lets evaluation report performance on these hard cases separately. No label changed.

## 3. RESOLVED — Label stops at the charter (`CERT`)
- A bank that merges away isn't tracked as "distress" under the current onset label — it just disappears from the panel, so its last few healthy quarters get a confident `onset_4q = 0` when the forward window was never observable (censored).
- **Scope:** of ~19,300 panel banks, 13,423 exited (merged/absorbed), 1,582 failed, 4,255 still active. The label problem is confined to the 48,671 rows (3.97% of healthy negatives) within 4 quarters of a non-failure exit.
- **Fixed in `cleaning.ipynb`:** added a boolean `near_merge_exit` flag (fate from `institutions` ACTIVE/ENDEFYMD + `failures`). Rows are kept, not dropped — modeling can drop, keep, or use the flag, and report sensitivity both ways. Failures are deliberately not flagged (real distress, not censoring).

## 4. RESOLVED — the 2020 capital-ratio drop was CBLR placeholder zeros
- Confirmed mechanism (subtler than first suspected): for CBLR opt-in banks (2020+), the FDIC fills `RBCRWAJ` with **0.0** — not null — while `RBC1RWAJ` stays null. ~44K placeholder zeros were dragging the median down ~3 points.
- **Fixed in `feature_selection.ipynb`:** zeros with missing Tier 1 are set to missing before the panel is saved. The label was never affected (those rows already routed through the CBLR rule). A small residual step remains post-2020 — real composition change, since the banks that left the reporting pool were small, high-capital ones.
- **Lesson:** zero and null are different lies. Check both when a level shift appears.

## 5. Capital ratios alone missed SVB entirely
- Case study (SVB vs. First-Citizens, both ~$200-235B peak assets): SVB's total RBC ratio was ~16% ("well capitalized") the quarter before it failed, and its NPA ratio stayed flat near zero the whole time. Classic CAMELS ratios gave no warning — the failure mode was a liquidity/duration-driven deposit run, which quarterly Call Report ratios can't see.
- **Implication:** the model needs a funding/liquidity-stability signal (uninsured-deposit share, deposit growth rate, deposit concentration) in addition to CAMELS ratios, or it will systematically miss SVB-style failures.

## 6. RESOLVED — M&A accounting artifacts (and tiny denominators) in ROA
- Two causes of the heavy positive tail: (a) M&A bargain-purchase gains (First-Citizens' ROA spiked 1.2% -> 23.6% the quarter it acquired SVB), and (b) tiny/de-novo banks with near-zero asset denominators (52% of ROA>15% rows have assets <$25M). Both are non-organic; 99% of these rows are currently healthy.
- Extreme negatives are the opposite — real distress (33% currently distressed at ROA<-20%), so the negative signal is preserved.
- Matching merger events from `history` caught only ~0.4% of the positive spikes, so gating on detected acquisitions is unreliable; the fix keys on implausible magnitude instead.
- **Fixed in `cleaning.ipynb` (flag only, no numbers changed):** added a boolean `roa_artifact` flag = ROA > 15% (4,381 rows, 0.35%; 99% currently healthy, confirming artifact not distress). Raw `ROA` left untouched. Negatives are not flagged (real losses). Modeling can drop the flagged rows or cap them later if a linear model needs it.
- **Follow-up:** ROE has the same denominator vulnerability (equity can be tiny/negative) and likely warrants the same treatment when it enters the feature set.

## 7. Data leakage risk (flagged by outside reviewer feedback, not yet checked)
- The target is an event in time (bank crosses into distress at quarter *t*). Any feature or validation setup that lets training data see across that boundary leaks the answer.
- **Specific risks:** (a) engineered features that look forward (e.g. "ratio dropped over the next N quarters") instead of only backward from the prediction quarter; (b) standard random k-fold CV, which shuffles across time and mixes past/future; (c) rolling stats computed over a window that spans the distress quarter itself.
- **Fix needed:** time-based train/test split (train ≤ year X, test > year X) or CV grouped by year, and an explicit audit that every feature is computed using only data available *as of* the prediction quarter.

## 8. RESOLVED — the last quarters had no outcome window to check against
- `onset_4q` asks whether a bank falls to undercapitalized within the next 4 quarters, which requires those 4 quarters to exist. The panel ends 2026-03, so the last fully checkable filing date is **2025-03**.
- Rows from 2025-06 onward were labeled `0` ("stayed safe") when the honest answer is *unknown*: 17,488 rows, all negatives. Left alone they silently inflate any score computed on the recent period (~9.5% of the 2017+ test set).
- Positives in that window are still valid — the bank already crossed inside the visible part of its window, so the missing tail cannot change the answer. Counts confirm this: 5 / 4 / 3 / 0 positives survive for 2025-06 through 2026-03.
- **Fixed in `cleaning.ipynb`:** unobservable negatives set to blank (`NaN`) in `onset_4q`. No new flag column — the panel already uses blank for "cannot be labeled" (already-distressed rows), so this reuses the existing convention. No rows deleted, no feature values changed.
- **Effect:** `onset_4q` now has 1,217,288 labeled rows (9,010 positives) and 41,600 blank.
- **Follow-up:** the 4 unlabeled quarters keep every predictor, so they are the natural "who looks risky right now" scoring set for the final presentation — a demo output, not a validated score.
