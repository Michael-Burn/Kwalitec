# EP-005.1 — Validation Methodology

**Programme:** EP-005.1 — KSI Validation & Evidence Collection  
**Version:** 1.0  
**Status:** Active for this validation window  
**Assessment date:** 2026-07-26  
**Authority:** Executes [`PRODUCT_SUCCESS_FRAMEWORK.md`](../p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md) §5 and Version 1 Release Framework Gate **G1**  
**Does not:** Change runtime behaviour, Twin algorithms, UI, or APIs  

---

## 1. Purpose

Define how estimated programme ΔKSI from EP-003.1–EP-004.3 is reconciled into a **validated** KSI assessment suitable for Gate G1 — without inflating scores or treating programme estimates as proof.

---

## 2. Claim windows

Two claim windows are scored separately. Mixing them is forbidden.

| Window ID | Definition | What may be credited |
|---|---|---|
| **W-PROD** | Production defaults as of 2026-07-26 | Student-visible Runtime A quality contracts from EP-003.1 / .2 / .3 (no new production flag). Capabilities gated **OFF** by default are **not** credited as student-perceived usefulness. |
| **W-GATED** | Flag-ON posture (`ENABLE_LEARNING_FEEDBACK`, `ENABLE_PERSONAL_LEARNING_PROFILE`) | Substrate + closed-loop personalisation **only as estimated / structural eligibility** until Stage 1+ dogfood and post-change perception evidence exist. |

**G1 declaration uses W-PROD only.** W-GATED informs roadmap residual, not Version 1 production-ready usefulness.

---

## 3. Evaluation cohort

| Cohort | N | Role | Claim level |
|---|---:|---|---|
| **C-STRUCT** — Structural / quality-contract | N/A (artefact pack) | Automated tests, architecture contracts, Explainability / Recommendation review checklists, constitutional verifications | Structural eligibility — necessary, not sufficient for Strong-band student usefulness |
| **C-BLIND** — EP-004 blind reviews SV-001–SV-020 | 20 personas | Pre-enhancement student-only qualitative corpus (baseline input) | **Baseline perception only** — does **not** validate post EP-003.1–004.3 perception lifts |
| **C-BETA0** — Stage 0 internal private beta | 3 internal (N_external = 0) | Week 0 scorecard exploratory | Exploratory / insufficient N — no product-decision KPI claims |
| **C-EXT** — External private beta Stage 1–2 | 0 | Required for Strong-band + educational effectiveness GO | **Absent** this window |

**Primary validation cohort for W-PROD:** C-STRUCT + C-BLIND (as baseline counterweight) + C-BETA0 honesty constraints.  
**Insufficient for G1 Strong claims:** C-EXT absent; no post-change blind re-review.

---

## 4. Observation period

| Period | Scope |
|---|---|
| Qualitative corpus | EP-004 Stage 0 blind reviews filed through 2026-07-24 |
| Scorecard | Week 0 (2026-07-24) — exploratory |
| Programme implementation evidence | EP-003.1–EP-004.3 completion artefacts dated 2026-07-26 |
| Validation assembly | 2026-07-26 (this programme) |
| Freshness for G1 | Assessment ≤ 90 days at any future declaration (PSF §5.4) |

No multi-week external WAL window exists for this validation.

---

## 5. Evidence sources and tiers

| Tier | Name | Acceptable sources | May support |
|---|---|---|---|
| **A** | Structural / contract | Pytest quality suites; P-001.2 / P-001.3 checklist Pass; architecture contracts; constitutional verification | Floor movement eligibility; schema completeness; honesty paths |
| **B** | Student perception (current) | Post-change blind re-reviews; interviews (≥8 or 25% active); filled M1–M9 at directional/product-decision N | Category score lifts into Partial→Strong; KSI ≥ 70 claims |
| **C** | Exploratory / pre-change | C-BLIND baseline themes; Stage 0 Week 0 scorecard; dogfood notes | Caps optimism; falsifies over-claim; **cannot alone raise** post-change scores |
| **D** | Programme estimates | EP/P `KSI_IMPACT_ASSESSMENT.md` estimated Δ | Planning / reconciliation only — **never** G1 alone |

### Evidence ID convention

`EV-<DOMAIN>-<NNN>` registered in [`KSI_EVIDENCE_REGISTER.md`](KSI_EVIDENCE_REGISTER.md). Every validated category score cites ≥1 Tier A or B ID (or explicitly records “no lift — baseline retained”).

---

## 6. Confidence levels

Per PSF §5.3, each category records **High / Medium / Low**.

| Level | Rule |
|---|---|
| **High** | Tier A **and** Tier B agree within ±5 category points; sample floors met (Metrics §4 / interview targets); no material honesty incident |
| **Medium** | Tier A complete with checklist Pass **or** Tier B directional with disclosed insufficient N; limitations explicit; no unresolved honesty P1 |
| **Low** | Tier D only; Tier A missing for claimed lift; conflicting evidence unresolved; gated-OFF capability claimed as student-visible |

**Composite confidence** = lowest material category confidence among K1, K2, K3, K8 (Version 1 pillars), unless Product owner documents a waiver with claim restriction.  
**G1.2:** composite Low → Gate G1 **FAIL**.

---

## 7. Acceptance thresholds

| Threshold | Rule |
|---|---|
| Category score validity | Evidence paths + rationale + confidence + limitations (PSF §5.3) |
| Prefer lower on conflict | When Tier A suggests lift and Tier C (pre-change perception) shows unresolved harm themes without Tier B re-test → credit **≤50%** of estimated category Δ, rounded down |
| Gated-OFF rule | Flag default OFF → validated Δ = **0** for student-perceived usefulness in W-PROD |
| Double-count rule | Stack overlapping programmes by **max non-overlapping primary lift** per category; do not sum K8 from every programme |
| V1-K floors (inform G1) | No category &lt; 50; K8 ≥ 70; composite KSI ≥ 80 — evaluated in [`VERSION_1_G1_STATUS.md`](VERSION_1_G1_STATUS.md) |
| Review tolerance | Independent re-score of same package within ±3 KSI (PSF §5.5) |
| Under-claim | Estimated programme bands that exceed validated evidence are marked **unsupported** |

### Evaluation dimensions (task scope)

| Dimension | Primary KSI | Validation focus |
|---|---|---|
| Recommendation usefulness | K2 | Decision Framework, plan coherence, refusal, acceptance absence |
| Planning usefulness | K1 | Schema, recovery, duration/dual-home residual themes |
| Readiness usefulness | K3 | Drivers, confidence labels, honest refusal, unpackability residual |
| Explainability | K8 | Mandatory Explanation Schema coverage vs Coach opacity corpus |
| Personalisation usefulness | K4 | Profile + closed-loop only if flag ON + perception evidence |
| Learning feedback quality | K6 | Record-only events; analytics UX / Journey emit status |

---

## 8. Handling insufficient evidence

| Situation | Action |
|---|---|
| No Tier A for a claimed lift | Validated Δ = 0; estimate → **unsupported** |
| Tier A present, no Tier B | Allow **conservative structural credit** only (≤50% of de-duplicated estimated Δ, rounded down); confidence ≤ Medium |
| External N = 0 / scorecard exploratory | Forbid Strong-band (70+) lifts; forbid educational-effectiveness marketing |
| Blind corpus predates change | Use as **cap / falsifier**, not as proof of improvement |
| Conflicting programme estimates | Prefer baseline + lowest justified lift; document dispute |
| Honesty incident open | Freeze affected categories; G1.10 FAIL |
| Package incomplete for a G1 criterion | Outcome **DEFER** for that criterion — never silent PASS |

**Inflation ban:** Do not average optimistic estimates into validated scores. Do not treat checklist Pass as automatic +10 category points.

---

## 9. Reconciliation procedure

```
1. Freeze claim window (W-PROD for G1)
2. Inventory estimated Δ from EP-003.1 … EP-004.3
3. De-duplicate overlapping category lifts; separate W-GATED
4. Map each residual lift to Evidence IDs (Tier A/B/C/D)
5. Apply insufficient-evidence rules → validated category scores
6. Compute composite KSI; assign confidences
7. Classify each estimate as Validated / Partially validated / Unsupported
8. Score G1.1–G1.10 → PASS / FAIL / HOLD / DEFER
9. Publish artefacts; update Version 1 evidence package index + readiness tracker
```

---

## 10. Non-claims

This methodology does **not** authorise:

- Exam pass-rate proof  
- Recommendation-effectiveness marketing (freeze intact)  
- “Exam Ready” marketing  
- Equating estimated stacked ΔKSI with validated KSI  
- Crediting flag-OFF personalisation as production usefulness  

---

## References

- [`PRODUCT_SUCCESS_FRAMEWORK.md`](../p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md)
- [`VERSION_1_RELEASE_FRAMEWORK.md`](../p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md)
- [`VERSION_1_EVIDENCE_REQUIREMENTS.md`](../p002_1_version_1_release_framework/VERSION_1_EVIDENCE_REQUIREMENTS.md)
- [`../ep003_educational_effectiveness/EDUCATIONAL_METRICS.md`](../ep003_educational_effectiveness/EDUCATIONAL_METRICS.md)
- [`../ep004_private_beta/WEEKLY_SCORECARD.md`](../ep004_private_beta/WEEKLY_SCORECARD.md)

---

**End of VALIDATION_METHODOLOGY**
