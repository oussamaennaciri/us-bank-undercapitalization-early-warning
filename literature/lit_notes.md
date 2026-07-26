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
