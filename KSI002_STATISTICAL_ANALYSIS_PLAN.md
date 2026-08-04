# KSI-002 — Statistical Analysis Plan (SAP)

**Programme:** KSI-002 — Educational Effectiveness Validation Protocol  
**Version:** 1.0  
**Status:** PROTOCOL COMPLETE — AWAITING FOUNDER REVIEW  
**Effective:** 2026-08-04  
**Authority:** `KSI002_VALIDATION_PROTOCOL.md` · `KSI002_STUDY_DESIGN.md` · `EDUCATIONAL_METRICS.md` · PSF §5  

**This SAP defines analysis rules only.** It contains **no statistical calculations**, no cohort results, and no new validated KSI.

---

## 1. Purpose

Pre-specify how future executors must analyse educational-effectiveness and validated-KSI evidence so that results cannot be reshaped after seeing favourable or unfavourable outcomes.

---

## 2. Estimands (what we estimate)

| Estimand ID | Description | Population |
|-------------|-------------|------------|
| E1 | Mean rolling 4-week study consistency (M6) | Active external participants meeting analysis inclusion |
| E2 | Session completion rate (M4 primary or secondary formula as available) | Same |
| E3 | Proportion of interviewed participants with Final Test = Yes (usefulness over time) | Interview completers with consent |
| E4 | Proportion with perceived multi-week preparedness = Yes or Partial-with-Why | Interview completers |
| E5 | Observational recommendation follow-through rate within TTL | Participants with ≥1 eligible recommendation exposure |
| E6 | Validated KSI composite and K1–K8 category scores | Claim-window evidence package (judgemental scoring under PSF + protocol) |

E6 is **structured expert scoring**, not a frequentist estimator from a single formula. The SAP still constrains inputs, prefer-lower, and confidence labelling.

---

## 3. Analysis sets

| Set | Definition |
|-----|------------|
| **ITT-Accepted** | All invite-accepted external participants |
| **Activated** | Accepted with ≥1 productive Session completion |
| **Active-Evaluable** | Activated and observed ≥ minimum study length (4 weeks) unless dropout rules exclude |
| **Interview** | Activated with completed structured interview + interview consent |
| **Per-protocol** | Active-Evaluable with measurement consent retained throughout window |

**Primary effectiveness board:** Active-Evaluable + Interview set for qualitative endpoints.  
**Sensitivity:** Always also report ITT-Accepted denominators for drop-off honesty.

---

## 4. Confidence intervals

| Rule | Spec |
|------|------|
| Default interval | **95%** two-sided for proportions and means when N permits |
| Proportion method | Wilson score interval preferred; Clopper–Pearson acceptable; document choice pre-analysis |
| Mean method | t-interval if approximate normality plausible; otherwise bootstrap percentile (declare seed) |
| Small N | If cell N &lt; 10, report **exact counts** + interval, and label confidence **Low** for Strong-band claims |
| KSI composite | Not a sampling CI; publish **assessment confidence** High/Medium/Low + G1.7 ±3 tolerance instead |

---

## 5. Effect sizes

| Contrast | Effect size | Notes |
|----------|-------------|-------|
| Pre-specified directional targets vs observed | Absolute difference (observed − target) | Targets from Educational Metrics / Study Design |
| Subgroup exploratory | Risk difference or mean difference | Explicitly exploratory; no G1 claim from subgroup alone |
| Category score movement | Integer Δ on 0–100 scale with prefer-lower | Require linked evidence paths |

**Do not** convert Progressive Confidence means or Premium scores into KSI effect sizes.

---

## 6. Minimum detectable effect (MDE) — planning assumptions

These are **protocol planning assumptions**, not computed power results.

| Endpoint | Assumed MDE (planning) | Notes |
|----------|------------------------|-------|
| M6 consistency | **0.10** absolute on [0,1] mean | Below this, treat as noise for GO rhetoric |
| M4 completion | **5** percentage points | |
| Interview Final Test Yes rate | **15** percentage points vs 70% target framing | With N_interviews≈8, power is limited — prefer descriptive + prefer-lower |
| K2 follow-through | **10** percentage points | Observational; no causal ranking claim |

If observed precision cannot support MDE, **do not** claim Strong-band lifts; hold prior validated scores.

---

## 7. Power assumptions (declarative)

| Assumption | Value |
|------------|------:|
| Stage 1 external N (design) | 5–10 |
| Stage 2 active N (GO floor) | ≥20 |
| Interview N (GO path) | ≥8 |
| Type I error (exploratory tests) | α = 0.05 two-sided |
| Power target for Stage 2 confirmatory language | 80% for MDE above — **aspirational**; if unmet, remain descriptive |

**Rule:** Insufficient power → descriptive statistics + qualitative synthesis; **not** “no effect proven” marketing, and **not** “effect proven” from underpowered p-values.

---

## 8. Statistical tests

| Use | Test | When |
|-----|------|------|
| Single proportion vs target | Exact binomial or one-sample proportion test | Stage 2+ only for confirmatory tone |
| Before/after within participant | Sign test or Wilcoxon signed-rank | Only if pre-registered paired measures exist |
| Two independent groups | Not primary — no randomised arms under this protocol | |
| Trend across weeks | Descriptive spaghetti + mean trajectory | Primary; formal mixed models optional Stage 2+ if pre-registered |

**Default posture:** Prefer **estimation + CIs + counts** over dichotomous significance theatre.

---

## 9. Multiple comparisons

| Rule | Spec |
|------|------|
| Primary family | E1–E4 only for effectiveness GO narrative |
| Secondary / exploratory | All other metrics — label **exploratory**; no α-spending required, but **no G1 cherry-pick** |
| K1–K8 scoring | Not a multiplicity-adjusted battery; constrained by prefer-lower and evidence rules |
| Forbidden | Running many cuts until a green GO appears |

---

## 10. Missing data

| Situation | Handling |
|-----------|----------|
| Measurement consent withdrawn | Exclude from numerators **and** note denominator change; do not impute educational outcomes |
| Interview declined | Remain in behavioural sets; missing qualitative → do not impute Yes |
| Partial weeks | Compute M6 on observed weeks; report number of weeks contributing |
| Missing events (telemetry gap) | Prefer manual ops tally if pre-specified; else mark metric **Unavailable** — do not invent |
| Lost to follow-up | Count as drop-off in ITT; exclude from Active-Evaluable if &lt; minimum length |

**Primary:** Available-case for Active-Evaluable.  
**Sensitivity:** Worst-case for binary interview endpoints (missing = not-Yes) when claiming GO.

---

## 11. Outlier rules

| Rule | Spec |
|------|------|
| Session duration extremes | Do not drop completions solely for short/long duration if educational completion status is authoritative |
| Hyper-active users | Winsorise M2 contribution at pre-declared percentile (e.g. 95th) for **mean** summaries; always report median |
| Duplicate accounts | Remove per Participant Protocol before analysis lock |
| Staff contamination | Remove from external sets |

Document every exclusion with pseudonymous ID and reason.

---

## 12. Recommendation rates (K2)

| Rate | Definition skeleton |
|------|---------------------|
| Acceptance / commitment | Eligible primary next-action marked commit / start within TTL |
| Deferral | Explicit defer within TTL |
| Completion reflection | Completed Session attributable to that commitment |
| Follow-through | Commitment → completion within TTL |

**Analysis rules:** Pre-declare TTL (e.g. 24h / 7d); report denominators; marketing freeze held; Strong-band K2 requires rates **and** prefer-lower vs perception-only packs.

---

## 13. Validated KSI scoring procedure (E6)

1. Assemble Evidence Register (paths, claim window, flag matrix).  
2. Score each K1–K8 with rationale, confidence, limitations.  
3. Apply prefer-lower on conflicts.  
4. Compute composite per PSF §5.2; round to nearest integer.  
5. Independent re-score (G1.7); resolve disputes per PSF §5.5.  
6. Refuse to publish if confidence Low for composite claim.

**No** blending of estimated ΔKSI, Premium PASS, or Progressive Confidence into E6 inputs.

---

## 14. Reporting format (mandatory)

Future analysis reports must include:

1. Protocol / SAP version IDs  
2. Claim window and flag matrix  
3. Analysis sets with N flow (Accepted → Activated → Evaluable → Interview)  
4. Primary endpoints with counts, point estimates, 95% CIs where applicable  
5. Secondary / exploratory clearly labelled  
6. Missingness table  
7. Exclusions log  
8. Effectiveness Q1–Q5 worksheet with linked paths  
9. KSI category table + composite + confidence  
10. Non-claims section (pass-rate, marketing, commercial)  
11. Prefer-lower decisions explicitly listed  

---

## 15. Software and reproducibility

| Rule | Spec |
|------|------|
| Computation | Spreadsheet or scripted pipeline acceptable; archive inputs in `knowledge/evidence/releases/<PROGRAMME>/` |
| Seeds | Declare for any bootstrap |
| PII | Pseudonymous IDs only in git artefacts |

---

## 16. Amendments

SAP amendments after seeing outcome data require Founder approval, version bump, and explicit bias note. Silent post-hoc target changes are honesty incidents (G1.10 risk).

---

## 17. Exit

**STOP.** No calculations under KSI-002. Await Founder review.
