# Literature Notes — Bank Distress Early-Warning Model
*MSDS 696 Practicum II · Oussama Ennaciri · working notes, one section per paper*

---

## Paper 1 — Cole & White (2012), "Déjà Vu All Over Again"

**Citation:** Cole, Rebel A., and Lawrence J. White. 2012. "Déjà Vu All Over Again: The Causes of U.S. Commercial Bank Failures This Time Around." *Journal of Financial Services Research* 42, 5–29. (SSRN 1644983)

**Question & target**
- Why did US commercial banks fail in 2009? Which balance-sheet characteristics, measured 1–5 years earlier, predict failure?
- Label: FAIL = 1 if (a) closed by FDIC during 2009 (117 banks), OR (b) "technically failed" at year-end 2009: **(Equity + Loan Loss Reserves − 0.5 × NPA) < 0** (148 banks). Total 265 (263 usable).
- NPA = loans past due 30–89 days + past due 90+ + nonaccrual loans + other real estate owned (OREO).
- Horizon: separate models using year-end data from 2008, 2007, 2006, 2005, 2004 → prediction 1 to 5 years ahead.

**Data**
- FDIC Call Reports, commercial banks only (thrifts and savings banks excluded).
- Cross-sections per year: ~7,146–7,629 banks; failures 232–263 (≈3.4% positive rate).

**Methodology**
- Multivariate logistic regression, one cross-section per lag year; marginal effects at means.
- No resampling or reweighting for class imbalance (raw logit on ~3.4% positives).
- Out-of-sample test: 2008-data model applied to Q4-2009 call reports to predict failures in the first 3 quarters of 2010.
- Metrics: McFadden pseudo-R²; Type I (missed failure) vs Type II (false alarm) error tradeoff (ROC-style curve). Explicitly argues Type I errors cost orders of magnitude more than Type II.

**ALL features (Table 1; every variable a fraction of total assets except LNSIZE)**
| Var | Definition | Predictive? |
|---|---|---|
| TE | Total equity / assets | Significant (−) only ≤2 yrs before failure; loses power earlier — capital is a LATE signal |
| LLR | Loan loss reserves / assets | (−) significant 3+ yrs out, fades near failure |
| ROA | Net income / assets | (−) significant all 5 years — consistent early signal |
| NPA | Nonperforming assets / assets | (+) significant all 5 years — strongest single signal |
| SEC | Securities (HTM + AFS) / assets | (−) protective; sig. most years |
| BD | Brokered deposits / assets | (+) significant 4 of 5 years — rapid-growth/hot-money flag |
| LNSIZE | log(total assets) | Mostly insignificant |
| CASHDUE | Cash & due from banks / assets | (−) protective, intermittent |
| GOODWILL | Goodwill / assets | (+) near failure, sign flips earlier; unstable |
| RER14 | 1–4 family residential mortgages / assets | (−) or neutral — residential lending is SAFE |
| REMUL | Multifamily mortgages / assets | (+) significant yrs 2–5 — early signal |
| RECON | Construction & development loans / assets | (+) significant ALL years, biggest early effect — the star predictor |
| RECOM | Nonfarm nonresidential (CRE) mortgages / assets | (+) significant yrs 2–5 |
| CI | Commercial & industrial loans / assets | Weak/mixed |
| CONS | Consumer loans / assets | (−) protective, intermittent |
- Tried and found insignificant: trading assets, premises, restructured loans, insider loans, home equity loans, MBS holdings, asset growth rate, FHLB advances/assets, concentration dummies (RECOM>300% of equity, RECON>100%), squared CRE terms, charge-off components.

**Results**
- Pseudo-R²: 0.62 (1 yr ahead) → 0.35 → 0.28 → 0.24 → 0.21 (5 yrs ahead).
- Out-of-sample (predicting 2010 failures): at 2% false-alarm rate ≈ Type I 17.8%; at 5% false alarms, only 4 of 107 failures missed (Type I 3.7%); at 10%, 2.8% — far better than Cole & Gunther (1998) benchmark (9.8% @ 10%).
- Six variables consistently significant 4+ of 5 years: NPA(+), ROA(−), BD(+), RECON(+), RECOM(+), REMUL(+).

**Limitations they admit**
- Commercial banks only; one crisis episode (2009–10 failures); "technical failure" label is authors' construct; write-downs mechanically shrink risky-asset categories near failure (attenuates late-year loan-mix coefficients); RECOM/RER14 multicollinearity.

**Lessons for my project**
1. **Signals rotate with horizon**: capital predicts late, loan-portfolio mix predicts early → direct support for my "at risk, and how soon?" multi-horizon framing.
2. **Loan-mix features are mandatory**: construction & development, CRE, multifamily concentrations are the strongest early predictors — must add these to my feature list (not in my starter 27).
3. NPA composition (incl. OREO and past-due buckets) and brokered deposits confirmed as core features.
4. Their asymmetric-cost ROC framing (miss vs false alarm) is the right evaluation story for a regulator/risk-officer audience.
5. Their "technical failure" construct is a cousin of my undercapitalized label — both catch distress before the FDIC acts.

---

# Methods Synthesis — How Every Paper Modeled

*Added after a full methodology pass over all 10 PDFs (July 2026). Paper 1 above is the
only full write-up; this section covers what each paper **did**, not what it found.*

## The table

| Paper | Method | Validation | Metric |
|---|---|---|---|
| Cole & White 2012 | Logit, one cross-section per lag year (1–5 yrs) | 2008 model applied to 2010 failures | Type I / Type II tradeoff |
| SCOR (Collier 2003) | Ordinal logit on **CAMELS downgrade** | **None** — sample too small for a holdout | Type I / Type II at a probability cutoff |
| Nuxoll 2003 | Logit, with and without state economic data | Out-of-sample | Type I / Type II |
| Curry et al. 2004 | Logit + hazard, adds equity-market variables | In- and out-of-sample, bootstrapped | Accuracy at 50% cutoff (matched sample) |
| Oshinsky & Olin 2005 | **Multinomial logit — 4 outcomes** | Cohort observed 2 years forward | Accuracy by predicted state |
| Maechler & McDill 2003 | Simultaneous-equation panel regression | Robustness across variable groupings | Coefficients |
| Martin/Puri/Ufier 2018 | LPM baseline; probit and **Cox proportional hazard** as robustness | Placebo period (2006) | Coefficients, hazard ratios |
| Petropoulos et al. 2020 | **Random Forest** vs logit, LDA, SVM, neural net, CRF | **Out-of-sample AND out-of-time** (2013–14) | AUROC, G-mean, balanced accuracy, Youden, weighted BA |
| Correia/Luck/Verner 2024 | Logit / LPM, 5 terms incl. **one interaction** | **Expanding window**, retrained each year | AUC + **PR-AUC as a multiple of the base rate** |
| Carmona/Climent/Momparler 2018 | **XGBoost** on a matched 50/50 sample | Random 75/25 holdout + k-fold CV | AUC (0.98) |
| Chu et al. (FDIC 2026) | Descriptive + regression on account-level run data | — | Run rates by depositor type |

## What this changes for my project

**1. Nuxoll's conclusion is the opposite of what I had written.**
He tested exactly the question I assumed he supported — does adding economic data improve
Call-Report-only failure forecasts — and found *"economic data do not improve these
forecasts despite the fact that the data are statistically significant."* Oshinsky & Olin
independently excluded economic variables by choice. My 11 FRED columns are therefore
**not literature-backed**. They need their own with/without test, or they should go.
(`features_by_dataset.md` has been corrected.)

**2. A plain logit can capture "together" — if you name the pair.**
Correia et al. reach out-of-sample AUC 0.94 on the modern sample with five terms:
insolvency (net income/assets), noncore funding (time deposits + other borrowed money),
**their interaction**, asset growth, and aggregate conditions. So the claim "only a complex
model sees combinations" is wrong as stated. The defensible claim: a logit sees only the
combinations specified in advance — with 54 features that is >1,400 candidate pairs, and
tree ensembles find them without guessing. My logistic baseline must include a comparable
interaction or the comparison is a strawman.

**3. Lagged observations are standard; I have none.**
Petropoulos feeds up to **2 years of lagged observations** per feature. My panel is one
quarter per row — a still frame. My own EDA finding is a two-year decline, which a single
snapshot cannot see by construction. Asset growth (Cole & White, Correia) is the minimum
version of this.

**4. Nobody uses accuracy.** Two live options: Type I / Type II at a chosen cutoff (the FDIC
lineage — SCOR, Nuxoll, Cole & White), or PR-AUC reported against the base rate (Correia).
Decision: PR-AUC to compare models, Type I / Type II to present the chosen one, since the
audience is a risk committee that needs "how many do we miss."

**5. Merger can be an outcome, not missing data.**
Oshinsky & Olin predict four futures — recover, merge, stay a problem, fail — rather than
yes/no. That is a real answer to my `near_merge_exit` censoring problem. Caveat: 69% of my
panel banks merged, so merger as a class would be dominated by healthy consolidation.

**6. Hazard models are the standard answer to "how soon."**
Martin uses Cox; Curry references them. That is the unused half of my Week 1 question and
the unused `quarters_to_onset` column.

## Validation designs worth copying

- **Petropoulos**: separates *out-of-sample* (different banks, same period) from
  *out-of-time* (future period). Logit did fine out-of-sample and **worst in 6 of 8
  criteria out-of-time** — a concrete precedent for a simple model degrading across eras.
- **Correia**: expanding window — train on the first 10 years, predict year *t+1*, refit,
  repeat. More realistic than one fixed split, and closer to how a supervisor would run it.
- **Petropoulos on imbalance**: downsampled the majority to build a "short in-sample" set
  (10% of good cases + all bad cases → ~12% positives), tuned there, then evaluated on the
  full, untouched distribution. Rebalancing on the training data only — the same rule as
  the Week 4 lecture.


---

## Paper 11 — Carmona, Climent & Momparler (2018), XGBoost for U.S. bank failure

**Citation:** Carmona, Pedro, Francisco Climent, and Alexandre Momparler. 2018. "Predicting
failure in the U.S. banking sector: An extreme gradient boosting approach." *International
Review of Economics and Finance*. DOI 10.1016/j.iref.2018.03.008

Added after the first modeling run. It matters because it is the **only paper in the folder
that uses the method I chose**, on the same population.

**Design**
- Extreme gradient boosting (XGBoost) predicting failure of U.S. national commercial banks.
- 2001–2015, **annual** series, 30 financial ratios (17 "performance", 13 "condition").
- **156 banks**, built as a matched sample: every failed bank paired with a solvent bank of
  similar total assets — so roughly 50/50, not a rare event.
- Random 75/25 train/test holdout, with k-fold cross-validation for parameter tuning.
- Reported AUC ≈ **0.98**; optimal tree count 149.

**Their top predictors**
- Retained earnings to average equity (low → higher failure risk)
- Pretax return on assets (low → higher risk)
- Total risk-based capital ratio (low → higher risk)
- **Yield on earning assets (high → higher risk)** — reaching for yield as a distress signal.
  This is the one candidate here that is *not* in my current 87 features.

**What it gives me**

1. **A citable precedent for the champion.** Gradient boosting on U.S. bank distress is now
   peer-reviewed prior work, not an unsupported choice. Fills the gap in the Week 4 defense.

2. **A rigour contrast, not a score to chase.** Their 0.98 comes from 156 banks, a balanced
   50/50 sample, and a *random* split — no time separation at all, so a bank's 2009 and 2010
   rows can sit on opposite sides of the boundary. My setup is 1.26M bank-quarters at a 0.34%
   base rate, split by time with a four-quarter gap. The numbers are not comparable, and the
   harder setup is mine. Worth stating explicitly rather than letting a reader assume I
   underperformed.

3. **The SCOR operational benchmark, quoted.** They cite Collier et al. (2003): the FDIC's own
   off-site system misses **roughly two-thirds of actual downgrades**, and roughly two-thirds
   of the banks it flags are never downgraded. That is the closest real-world bar for a
   tier-drop model like mine, and a far more meaningful comparison than an AUC from a matched
   sample.

**Limitation worth noting when citing it:** the matched design answers "given a failed bank
and a healthy one of the same size, can you tell them apart?" — not "which of 19,000 banks
should a supervisor look at on Monday?" The second question is mine, and it is the harder one.
