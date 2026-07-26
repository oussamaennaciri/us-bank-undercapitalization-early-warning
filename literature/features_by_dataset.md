# Features by Dataset — Literature Synthesis

Consolidated from all 10 papers in the literature folder (Cole & White 2012; Collier et al. SCOR 2003; Maechler & McDill 2003; Nuxoll 2003; Curry et al. 2004; Oshinsky & Olin 2005; Petropoulos et al. 2020; Correia, Luck & Verner 2024; Martin, Puri & Ufier 2018; Chu et al. Depositor Flight 2026). Organized by which of the five source tables each feature would come from.

## FDIC Financials (Call Report, ~2,378 fields — main feature pool)

**Capital**
- Risk-based / total risk-based capital ratio — Cole & White, SCOR, Petropoulos, Oshinsky & Olin
- Tangible equity ratio — Oshinsky & Olin, Correia/Luck/Verner
- Leverage ratio / total equity to assets — Cole & White (TE, significant only ≤2 yrs before failure — a late signal), Petropoulos, Correia/Luck/Verner
- Tier 1 capital ratio — Petropoulos

**Asset quality**
- Nonperforming loan / nonperforming assets ratio — Cole & White (NPA: strongest single signal, significant all 5 years out), and nearly universal elsewhere
- Past-due 30–89 days, past-due 90+ days — Oshinsky & Olin, Nuxoll, Cole & White (components of NPA)
- Nonaccrual loans/leases — Oshinsky & Olin, Cole & White (component of NPA)
- Allowance / loan loss reserves ratio (ALLL, LLR) — Oshinsky & Olin, Cole & White (significant 3+ yrs out, fades near failure), Petropoulos
- Other real estate owned (OREO) — Oshinsky & Olin, Cole & White (component of NPA)
- Net charge-offs to loans — Cole & White, Petropoulos
- Goodwill / assets — Cole & White (sign unstable, weak/near-failure-only signal — low priority)

**Loan portfolio mix / concentration** *(new category, driven almost entirely by Cole & White)*
- Construction & land development loans / assets — Cole & White's single strongest, most consistent early predictor (significant all 5 years, biggest early effect)
- Nonfarm nonresidential (CRE) mortgages / assets — Cole & White, significant years 2–5; also flagged by SCOR/Petropoulos as a general concentration risk
- Multifamily mortgages / assets — Cole & White, significant years 2–5
- 1–4 family residential mortgages / assets — Cole & White (protective/neutral — residential lending was NOT a 2009 failure driver, contrary to the RMBS narrative)
- Commercial & industrial loans / assets — Cole & White (weak/mixed)
- Consumer loans / assets — Cole & White (protective, intermittent)
- Securities (HTM + AFS) / assets — Cole & White (protective, significant most years)
- Cash & due from banks / assets — Cole & White (protective, intermittent liquidity signal)

**Earnings**
- ROA — nearly universal
- ROE — Petropoulos, SCOR
- Net interest margin — Oshinsky & Olin, Petropoulos
- Net interest income (% avg assets) — Oshinsky & Olin
- Provision for loan losses — Oshinsky & Olin, Petropoulos
- Net noninterest income/expense — Oshinsky & Olin
- Efficiency ratio (noninterest expense / (NII + noninterest income)) — Oshinsky & Olin, SCOR

**Liquidity / funding structure**
- Volatile liabilities ratio — Oshinsky & Olin, SCOR
- Loans + securities with maturity ≥5yr (asset-liability mismatch) — Oshinsky & Olin
- Brokered deposits / brokered-to-total-deposits — Martin/Puri/Ufier, Cole & White (significant 4 of 5 years — rapid-growth/hot-money flag)
- Large time deposits >$250k (uninsured share) — Martin/Puri/Ufier
- Core deposit ratio / insured vs. uninsured deposit split — Martin/Puri/Ufier, Maechler & McDill
- Loan-to-deposit ratio — SCOR, Petropoulos

**Management (proxy only — no direct field)**
- Efficiency ratio doubles as management proxy — Oshinsky & Olin, SCOR
- Asset growth rate (rapid growth flagged as risk-appetite proxy) — Cole & White, Correia/Luck/Verner

**Sensitivity to market risk**
- Long-term asset/securities maturity mismatch — Oshinsky & Olin
- Uninsured deposit reliance as funding-shock sensitivity — Maechler & McDill, Martin/Puri/Ufier

## FDIC Institutions (static/reference table)

- Charter type / primary regulator (state vs. national, Fed member) — Cole & White
- Asset size class / log(total assets) — Cole & White (LNSIZE, mostly insignificant on its own but used as a control), and nearly all papers stratify by size
- Age / de novo status — Martin/Puri/Ufier
- State / geographic location — Cole & White (regional CRE concentration, e.g. GA, FL)

## FDIC Failures + History

- Failure date, resolution type, resolution cost — used for label construction, not as predictive features
- Prior formal enforcement actions (C&D orders, PCA status) — Martin/Puri/Ufier use enforcement-action date as a distress-regime marker; this data isn't in the current 5-table pull and may need a 6th source (FDIC enforcement actions) if I want it as a feature

## FRED Macro table

- GDP growth (current quarter) — Martin/Puri/Ufier, Nuxoll
- Unemployment rate — Nuxoll, Cole & White
- Interest rate level and changes — Nuxoll, Correia/Luck/Verner (rate-shock exposure was central to 2023 failures)
- Housing starts — Martin/Puri/Ufier
- Stock returns and VIX — Martin/Puri/Ufier
- OFR Financial Stress Index — Martin/Puri/Ufier
- State/regional economic conditions — Cole & White ties failures to regional real estate downturns; may need state-level FRED series, not just national

## Notes

- Nuxoll (2003) directly tests whether adding macro data improves on Call-Report-only prediction, and finds it **does not**: "economic data do not improve these forecasts despite the fact that the data are statistically significant." Oshinsky & Olin (2005) likewise excluded economic variables by choice. So the FRED join is *not* literature-backed — it needs its own test (train with and without the macro block, compare) or it should be dropped.
- Curry et al. (2004) find equity-market signals (stock price decline, volatility, distance-to-default) predict failure earlier than Call Report ratios, but that requires market data (e.g., CRSP) outside the FDIC/FRED scope — a known limitation, not a feature I can add without a new data source.
- Cole & White (2012) is the strongest single source for feature selection here: logit on ~3.4% positive rate, six variables significant 4+ of 5 years out (NPA+, ROA−, brokered deposits+, construction & development loans+, CRE mortgages+, multifamily mortgages+), and an explicit finding that residential mortgage exposure was NOT a 2009 failure driver — worth citing directly when justifying which features make the cut.
- CAMELS is the organizing frame across nearly every paper here; the financials table covers Capital, Asset quality, Earnings, and Liquidity directly, Management only by proxy, and Sensitivity partially (rate/maturity mismatch, funding concentration). Loan portfolio mix (construction, CRE, multifamily, residential, C&I, consumer) sits partly under Asset quality and partly under Sensitivity, but is broken out separately above since it's Cole & White's headline result.

## Coverage check

All 10 papers in the literature folder are now reflected here: Cole & White (`ssrn-1644983.pdf`), SCOR (`SCOR_Collier_2003.pdf`), Maechler & McDill (`Depositor_Discipline_Maechler_McDill_2003.pdf`), Nuxoll (`Economic_Data_BankFailure_Nuxoll_2003.pdf`), Curry et al. (`Equity_Markets_Predict_Failures_Curry_2004.pdf`), Oshinsky & Olin (`Troubled_Banks_Oshinsky_Olin_2005.pdf`), Petropoulos et al. (`Session 2 - Predicting bank insolvencies...pdf`), Correia/Luck/Verner (`Failing_Banks_Correia_Luck_Verner_NYFed.pdf`), Martin/Puri/Ufier (`Deposit_Flows_Failing_Banks_Martin_2018.pdf`), and Chu et al. (`Depositor_Flight_2023Failures_FDIC_2026.pdf`). `lit_notes.md` and this file are working notes, not source papers.
