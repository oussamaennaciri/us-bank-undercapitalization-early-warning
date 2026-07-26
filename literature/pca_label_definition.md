# PCA Capital Categories — Verified Definitions and Sources

Authoritative basis for the target label. Verified July 2026 against the regulation text, not secondary summaries.

## Statutory basis

- **12 U.S.C. § 1831o** (FDIC Act Section 38), created by FDICIA (Dec 1991). Requires regulators to classify insured banks into five capital categories and take mandatory corrective action as capital falls.
- Implementing rule for FDIC-supervised banks: originally **12 CFR 325.103** (effective Dec 19, 1992; published 57 FR 44866, Sept 29, 1992), replaced by **12 CFR 324.403** (Basel III revision, effective Jan 1, 2015).

## Timeline of changes (all four, so far)

| Date | Change |
|---|---|
| 1992-12-19 | Original PCA rule takes effect — 3 ratios (Total RBC, Tier 1 RBC, Leverage) |
| 2015-01-01 | Basel III rule takes effect — adds CET1 as a 4th ratio, raises Tier 1 thresholds |
| 2020-01-01 | Community Bank Leverage Ratio (CBLR) framework **created** — new opt-in path to "well capitalized" for qualifying small banks, bypassing the ratio table entirely |
| 2026-07-01 | CBLR threshold lowered from 9% to 8% |

Treat this list as provisional, not final — it's what two rounds of checking turned up, not a guarantee nothing else changed.

## Regime 1 — Original FDICIA rule (1992-12-19 to 2014-12-31)

Three ratios + tangible equity trigger. Source: 12 CFR 325.103 (1992); FDIC Prompt Corrective Action manual, Ch. 5.

| Tier | Total RBC | Tier 1 RBC | Leverage |
|---|---|---|---|
| Well capitalized | ≥ 10% | ≥ 6% | ≥ 5% |
| Adequately capitalized | ≥ 8% | ≥ 4% | ≥ 4% |
| Undercapitalized | < 8% | < 4% | < 4% |
| Significantly undercapitalized | < 6% | < 3% | < 3% |
| Critically undercapitalized | tangible equity / total assets ≤ 2% | | |

## Regime 2 — Basel III rule (2015-01-01 to present)

Adds CET1 as a fourth ratio and raises the Tier 1 thresholds. Source: 12 CFR 324.403 (current, via Cornell LII).

| Tier | Total RBC | Tier 1 RBC | CET1 | Leverage |
|---|---|---|---|---|
| Well capitalized | ≥ 10% | ≥ 8% | ≥ 6.5% | ≥ 5% |
| Adequately capitalized | ≥ 8% | ≥ 6% | ≥ 4.5% | ≥ 4% |
| Undercapitalized | < 8% | < 6% | < 4.5% | < 4% |
| Significantly undercapitalized | < 6% | < 4% | < 3% | < 3% |
| Critically undercapitalized | tangible equity / total assets ≤ 2% | | | |

Classification rule (both regimes): a bank must meet **all** ratio minimums to hold a tier; the **worst** ratio sets the category. "Well capitalized" additionally requires no capital directive in force (not observable in this data — known limitation).

## CBLR overlay (2020-01-01 to present, revised 2026-07-01)

- Community Bank Leverage Ratio framework (2019 final rule, effective Jan 1, 2020): qualifying banks (<$10B assets, limited trading/off-balance-sheet exposure) may **opt in** and are **deemed well capitalized** if leverage ratio > 9%, without reporting the risk-based ratios.
- CARES Act temporarily lowered it to 8% (2020), graduated back to 9% by 2022.
- **2026 revision**: the CBLR threshold was permanently lowered from 9% to 8%, effective **July 1, 2026**, with the grace period extended from 2 to 4 quarters. Source: FDIC/OCC/Fed joint final rule, April 2026.
- **Consequence for the label:** CBLR opt-in banks may have null risk-based ratios post-2020. This is the suspected cause of the 2020 level shift in median `RBCRWAJ` (concern #4 in `data_concerns.md`). These banks are well capitalized by rule, not missing data. For 2026Q3 onward, the CBLR cutoff is 8%, not 9%.

## Mapping to FDIC fields (`risview_properties.yaml`)

| Ratio | Field | FDIC title |
|---|---|---|
| Total RBC | `RBCRWAJ` | TOTAL RBC RATIO-PCA |
| Tier 1 RBC | `RBC1RWAJ` | TIER 1 RBC RATIO-PCA |
| Leverage | `RBC1AAJ` | LEVERAGE RATIO-PCA |
| CET1 | `RBCT1CER` | COMMON EQUITY TIER 1 RATIO |
| Tangible equity proxy | `EQV` | BANK EQUITY CAPITAL/ASSETS |

The `-PCA` suffix means the FDIC computes these to PCA spec (adjusted numerators/denominators per the rule) — no need to derive from raw components. `EQV` is equity/assets, a proxy for the rule's "tangible equity" (which deducts most intangibles); small upward bias for banks with large goodwill.

## Implications for the label build

1. **Regime-switch at 2015Q1**: classic 3-ratio table before, 4-ratio table (with CET1 `RBCT1CER` and raised Tier 1 cutoffs) after.
2. **Label start = 1990Q1 at the earliest** (ratios first populated ~1990; PCA legally effective Dec 1992 — decide whether to start the label at 1990 with "as-if" classification or at 1993Q1 strictly).
3. **Post-2020**: treat CBLR opt-in banks (null RBC ratios, leverage > 9%) as well capitalized, not missing.
4. Current `02_eda` label uses Regime 1 thresholds across the whole window — fine for the practice pass, must be fixed for the real build.

## Sources

- [12 CFR 324.403 — current PCA capital categories (Cornell LII)](https://www.law.cornell.edu/cfr/text/12/324.403)
- [FDIC Act Section 38 — Prompt Corrective Action (12 U.S.C. § 1831o)](https://www.fdic.gov/federal-deposit-insurance-act/section-38-prompt-corrective-action)
- [FDIC Formal and Informal Enforcement Actions Manual, Ch. 5: Prompt Corrective Action](https://www.fdic.gov/regulations/examinations/enforcement-actions/ch-05.pdf)
- [FDIC Community Bank Leverage Ratio Framework — Compliance Guide](https://www.fdic.gov/resources/community-banking/docs/cblr-guide.pdf)
- [OCC Bulletin 2020-89 — CBLR temporary 8% / transition rule](https://www.occ.gov/news-issuances/bulletins/2020/bulletin-2020-89.html)
- [FDIC press release — CBLR lowered to 8%, effective July 1, 2026](https://www.fdic.gov/news/press-releases/2026/agencies-finalize-changes-community-bank-leverage-ratio)
- Original rule: 57 FR 44866 (Sept 29, 1992), codified at 12 CFR 325.103 (1992–2014)
