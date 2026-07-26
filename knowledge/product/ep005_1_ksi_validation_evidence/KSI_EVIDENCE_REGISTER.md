# EP-005.1 — KSI Evidence Register

**Programme:** EP-005.1 — KSI Validation & Evidence Collection  
**Version:** 1.0  
**Assessment date:** 2026-07-26  
**Claim window:** W-PROD (production defaults) unless noted  
**Method:** [`VALIDATION_METHODOLOGY.md`](VALIDATION_METHODOLOGY.md)  
**Does not:** Change runtime behaviour, Twin algorithms, UI, or APIs  

---

## 1. Purpose

Traceable register of evidence used to validate (or refuse) estimated KSI improvements from EP-003.1–EP-004.3. Every validated category score in [`VALIDATED_KSI_REPORT.md`](VALIDATED_KSI_REPORT.md) cites IDs from this register.

---

## 2. Evidence catalogue

### 2.1 Baseline and frameworks (Tier C / authority)

| ID | Tier | Artefact | Supports |
|---|---|---|---|
| EV-BASE-001 | C / Auth | `../p001_1_ksi_baseline/BASELINE_KSI_ASSESSMENT.md` | Baseline category scores; gap to 80 |
| EV-BASE-002 | Auth | `../p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md` | Scoring law; V1-K1…V1-K7 |
| EV-BASE-003 | Auth | `../p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md` | Gate G1 criteria |
| EV-BASE-004 | Auth | `../p002_1_version_1_release_framework/VERSION_1_EVIDENCE_REQUIREMENTS.md` | Evidence package rules |

### 2.2 Blind-review / private-beta perception (Tier C)

| ID | Tier | Artefact | Supports |
|---|---|---|---|
| EV-PERC-001 | C | `../ep004_private_beta/blind_reviews/SV-001.md` … `SV-020.md` | Pre-change student perception corpus |
| EV-PERC-002 | C | `../ep004_private_beta/BLIND_REVIEW_META_ANALYSIS_V2.md` | Coach opacity, dual-home, duration mismatch, readiness unpackability themes |
| EV-PERC-003 | C | `../ep004_private_beta/WEEKLY_SCORECARD.md` (Week 0) | External N=0; M1–M9 exploratory / insufficient |
| EV-PERC-004 | C | `../ep004_private_beta/GO_NO_GO_DECISION.md` | Programme GO WITH CONDITIONS; effectiveness claim NO-GO |
| EV-PERC-005 | C | `../ep003_educational_effectiveness/GO_NO_GO_REPORT.md` | Educational effectiveness PENDING EVIDENCE |
| EV-PERC-006 | C | `../ep003_educational_effectiveness/VERSION_1_EDUCATIONAL_REVIEW.md` | Surface readiness qualitative baseline |

### 2.3 Recommendation usefulness (K2) — Tier A / D

| ID | Tier | Artefact | Supports |
|---|---|---|---|
| EV-REC-001 | A | `../ep003_1_recommendation_engine_enhancement/RECOMMENDATION_REVIEW.md` | P-001.3 checklist Pass |
| EV-REC-002 | A | `../ep003_1_recommendation_engine_enhancement/EXPLAINABILITY_REVIEW.md` | P-001.2 checklist Pass (rec surfaces) |
| EV-REC-003 | A | `../ep003_1_recommendation_engine_enhancement/COMPLETION_REPORT.md` + `tests/services/test_recommendation_quality_ep003_1.py` | Schema, Decision Framework, refusal tests |
| EV-REC-004 | A | `knowledge/architecture/RECOMMENDATION_SERVICE_QUALITY_CONTRACT.md` | Contract authority |
| EV-REC-005 | D | `../ep003_1_recommendation_engine_enhancement/KSI_IMPACT_ASSESSMENT.md` | Estimated K2 +6 |
| EV-REC-006 | A / D | `../ep004_2_adaptive_recommendation_personalisation/RECOMMENDATION_REVIEW.md` + `KSI_IMPACT_ASSESSMENT.md` | Personalisation checklist Pass; estimated K2 +4 (**W-GATED**) |
| EV-REC-007 | A | `../ep004_2_adaptive_recommendation_personalisation/COMPLETION_REPORT.md` | Flag OFF default; fail-open personalisation |

### 2.4 Planning usefulness (K1) — Tier A / D

| ID | Tier | Artefact | Supports |
|---|---|---|---|
| EV-PLAN-001 | A | `../ep003_3_adaptive_planning_enhancement/EXPLAINABILITY_REVIEW.md` | P-001.2 Pass |
| EV-PLAN-002 | A | `../ep003_3_adaptive_planning_enhancement/COMPLETION_REPORT.md` + `tests/services/test_planning_quality_ep003_3.py` | Planning quality contract tests |
| EV-PLAN-003 | A | `knowledge/architecture/PLANNING_SERVICE_QUALITY_CONTRACT.md` | Contract authority |
| EV-PLAN-004 | D | `../ep003_3_adaptive_planning_enhancement/KSI_IMPACT_ASSESSMENT.md` | Estimated K1 +7 |
| EV-PLAN-005 | A / D | `../ep004_3_adaptive_planning_personalisation/COMPLETION_REPORT.md` + `KSI_IMPACT_ASSESSMENT.md` | Estimated K1 +5 (**W-GATED**) |
| EV-PLAN-006 | C | EV-PERC-002 duration mismatch / dual-home themes | Caps K1 optimism until re-tested |

### 2.5 Readiness usefulness (K3) — Tier A / D

| ID | Tier | Artefact | Supports |
|---|---|---|---|
| EV-RDY-001 | A | `../ep003_2_readiness_intelligence_enhancement/EXPLAINABILITY_REVIEW.md` | P-001.2 Pass |
| EV-RDY-002 | A | `../ep003_2_readiness_intelligence_enhancement/COMPLETION_REPORT.md` + `tests/services/test_readiness_quality_ep003_2.py` | Drivers, confidence, refusal path |
| EV-RDY-003 | A | `knowledge/architecture/READINESS_SERVICE_QUALITY_CONTRACT.md` | Contract authority |
| EV-RDY-004 | D | `../ep003_2_readiness_intelligence_enhancement/KSI_IMPACT_ASSESSMENT.md` | Estimated K3 +8 |
| EV-RDY-005 | C | EV-PERC-002 readiness unpackability / overconfidence themes | Caps K3 optimism |

### 2.6 Explainability (K8) — Tier A / C / D

| ID | Tier | Artefact | Supports |
|---|---|---|---|
| EV-EXP-001 | A | EP-003.1 / .2 / .3 Explainability Reviews (Pass) | MES on Rec / Plan / Readiness |
| EV-EXP-002 | A | `../p001_2_explainability_standard/EXPLAINABILITY_STANDARD.md` | Explanation law |
| EV-EXP-003 | C | EV-PERC-002 Coach “highest-value without working” (Near Universal) | Student-perceived explainability still weak pre-re-review |
| EV-EXP-004 | D | Sum of programme K8 estimates (overlapping) | Must be de-duplicated; not G1 input alone |

### 2.7 Personalisation (K4) — Tier A / D (W-GATED)

| ID | Tier | Artefact | Supports |
|---|---|---|---|
| EV-PERS-001 | A | `../ep004_1_personal_learning_profile/COMPLETION_REPORT.md` + profile tests | Substrate exists; flag OFF |
| EV-PERS-002 | A | `../ep004_2_adaptive_recommendation_personalisation/PERSONALISATION_RULES.md` | Bounded rec personalisation |
| EV-PERS-003 | A | `../ep004_3_adaptive_planning_personalisation/PERSONALISATION_RULES.md` | Bounded plan personalisation |
| EV-PERS-004 | D | EP-004.1–.3 `KSI_IMPACT_ASSESSMENT.md` | Estimated K4 lifts (**W-GATED**) |
| EV-PERS-005 | Auth | `app/application/config/v2_flags.py` (`ENABLE_PERSONAL_LEARNING_PROFILE = False`) | W-PROD Δ = 0 for perceived personalisation |

### 2.8 Learning feedback / analytics (K6) — Tier A / D (W-GATED)

| ID | Tier | Artefact | Supports |
|---|---|---|---|
| EV-FB-001 | A | `../ep003_4_learning_feedback_loop/COMPLETION_REPORT.md` + feedback adapter tests | Record-only loop; flag OFF |
| EV-FB-002 | D | `../ep003_4_learning_feedback_loop/KSI_IMPACT_ASSESSMENT.md` | Estimated K6 +6 (**W-GATED**) |
| EV-FB-003 | C | Journey emit deferred (ADR-026 referenced in readiness tracker) | Caps analytics usefulness claims |
| EV-FB-004 | Auth | `ENABLE_LEARNING_FEEDBACK = False` default | W-PROD Δ = 0 for feedback-driven analytics |

### 2.9 Motivation / revision (K5 / K7)

| ID | Tier | Artefact | Supports |
|---|---|---|---|
| EV-MOT-001 | C | EV-BASE-001 + EV-PERC-002 habit / friction themes | K5 retained at baseline pending consequence evidence |
| EV-REV-001 | A / D | EP-003.3 / EP-004.2 / EP-004.3 revision-adjacent estimates | Insufficient student evidence for validated lift in W-PROD |

### 2.10 Honesty / effectiveness posture

| ID | Tier | Artefact | Supports |
|---|---|---|---|
| EV-HON-001 | C | EV-PERC-004 / EV-PERC-005 | No educational-effectiveness GO; freeze on recommendation marketing |
| EV-HON-002 | A | Constitutional verification files under each EP-003.x / EP-004.x folder | No second educational brain claimed in programme exits |

---

## 3. Coverage matrix (W-PROD)

| Dimension | Estimated source | Validating evidence IDs | Outcome class |
|---|---|---|---|
| Recommendation usefulness | EP-003.1 (+ EP-004.2 gated) | EV-REC-001…005; EV-PERC-002 | Partially validated |
| Planning usefulness | EP-003.3 (+ EP-004.3 gated) | EV-PLAN-001…004, EV-PLAN-006 | Partially validated |
| Readiness usefulness | EP-003.2 | EV-RDY-001…005 | Partially validated |
| Explainability | EP-003.1–.3 K8 estimates | EV-EXP-001…003 | Partially validated (below V1 floor) |
| Personalisation usefulness | EP-004.1–.3 | EV-PERS-005 | Unsupported in W-PROD (flag OFF) |
| Learning feedback quality | EP-003.4 | EV-FB-004 | Unsupported in W-PROD (flag OFF) |

---

## 4. Missing evidence (blocks Strong-band / G1 pass)

| Gap ID | Missing item | Blocks |
|---|---|---|
| GAP-01 | Post-change blind re-review or interview sample after EP-003.1–.3 | Tier B for K1/K2/K3/K8 |
| GAP-02 | External cohort N≥10 directional / N≥20 product-decision + ≥4 weeks | M1–M9; educational GO; KSI ≥ 70–80 claims |
| GAP-03 | Privacy Stage 1 signatures + analytics pilot activation | C-EXT formation |
| GAP-04 | Flag-ON dogfood pack for profile / personalisation / feedback | W-GATED → validated |
| GAP-05 | Independent second assessor re-score note | G1.7 formal closure (tolerance procedure documented; second pass optional until declaration) |
| GAP-06 | Recommendation acceptance KPI under approved PRD | K2 Strong-band |

---

## 5. Chain-of-custody

| Field | Value |
|---|---|
| Assembled by | Product measurement validation (EP-005.1) |
| Assembly date | 2026-07-26 |
| Immutable rule | Cite paths; do not alter source programme scores silently |
| Next refresh | After Stage 1 scorecard fill **or** post-change blind re-review — whichever first |

---

**End of KSI_EVIDENCE_REGISTER**
