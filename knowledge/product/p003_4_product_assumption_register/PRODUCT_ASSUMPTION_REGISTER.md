# Product Assumption Register

**Programme:** P-003.4 — Product Assumption Register  
**Document:** Canonical Product Assumption Register (full cards)  
**Date:** 2026-07-26  
**Status:** Complete — documentation only  
**Does not:** Amend runtime, services, UI, governance law, architecture, release gates, decisions, or risks  

**Purpose:** Permanent Product Board reference for every material assumption that underpins Version 1 product, educational, release, and validation posture — distinguishing what is known, believed, disproved, and still requires evidence.

**Companions:** [`VALIDATED_ASSUMPTIONS.md`](VALIDATED_ASSUMPTIONS.md) · [`UNVALIDATED_ASSUMPTIONS.md`](UNVALIDATED_ASSUMPTIONS.md) · [`REJECTED_ASSUMPTIONS.md`](REJECTED_ASSUMPTIONS.md) · [`ASSUMPTION_TRACEABILITY.md`](ASSUMPTION_TRACEABILITY.md) · [`ASSUMPTION_REVIEW_PROCESS.md`](ASSUMPTION_REVIEW_PROCESS.md)

**Evidence standard:** Every assumption cites existing artefacts. Unsupported assumptions are not invented. Posture and confidence freeze at 2026-07-26 evidence (aligned with P-003.1 dossier, P-003.2 Decision Register, P-003.3 Risk Register).

**How to use:** A Product Board member should answer *what assumptions underpin Kwalitec today, and what evidence supports or challenges them?* from the status indexes plus this register.

**Related registers:** Decisions (`DR-NNN`) · Risks (`PR-NNN`) · Assumptions (`PA-NNN`)

---

## Register conventions

| Field | Meaning |
|---|---|
| **Assumption ID** | Stable `PA-NNN` identifier (never reuse) |
| **Category** | Educational · Behavioural · Product · Operational · Governance · Architecture · Release · Research |
| **Status** | `Hypothesis` · `Supported` · `Validated` · `Rejected` · `Superseded` |
| **Current Confidence** | High · Medium · Low (in the *status claim*, not in product success) |
| **Owner** | Accountable role for review / validation work |

### Status meanings

| Status | Meaning |
|---|---|
| **Hypothesis** | Believed or designed; insufficient evidence to treat as product knowledge |
| **Supported** | Credible supporting evidence exists (often Tier B / structural / law-adjacent); not yet outcome-validated for the claim class |
| **Validated** | Evidence-bound as true for the stated claim window (methodology, invariant, Universal theme, or gate law as applicable) |
| **Rejected** | Falsified or explicitly unsupported as a claim; must not drive release or marketing language |
| **Superseded** | Once held; replaced by a later assumption or decision (see card) |

Indexes: [`VALIDATED_ASSUMPTIONS.md`](VALIDATED_ASSUMPTIONS.md) · [`UNVALIDATED_ASSUMPTIONS.md`](UNVALIDATED_ASSUMPTIONS.md) · [`REJECTED_ASSUMPTIONS.md`](REJECTED_ASSUMPTIONS.md) · Traceability: [`ASSUMPTION_TRACEABILITY.md`](ASSUMPTION_TRACEABILITY.md)

---

## Board control statement

> Version 1 is governed by a mix of **validated law and invariants**, **supported perception/structure evidence**, and **untested behavioural hypotheses**. External educational effectiveness remains **unproven** (external N = 0). Several historically convenient shortcuts — estimate stacking, checklist-as-KSI, perception-as-effectiveness, GA-as-ready — are **Rejected**. Under P-002.1 / P-003.1, this posture forces **NO GO** on Version 1 production-ready declaration until evidence programmes close the gaps.

---

# Part A — Explainability, MES, and trust

---

## PA-001 — Better explanations improve student trust

| Field | Content |
|---|---|
| **Title** | Better explanations improve student trust |
| **Category** | Educational |
| **Status** | Supported |
| **Statement** | When students can see why a recommendation, plan, or readiness signal was produced (evidence-bound, syllabus-linked, falsifiable), they trust guidance more than when speech is opaque or generic. |
| **Origin** | P-001.2 Explainability Standard; EP-006.3 MES perception |
| **Supporting Evidence** | `knowledge/product/p001_2_explainability_standard/EXPLAINABILITY_STANDARD.md` (Trust outcome); `knowledge/product/ep006_3_mes_perception_validation/MES_PERCEPTION_REPORT.md` (Conditional Pass; schema-complete speech earned cautious trust); K8 validated floor **70** (G1.5) |
| **Contradicting Evidence** | Pre-MES Coach opacity near-universal (EP-005.2); cold-start generic speech still distrusted (SV-005 in EP-006.3); trust ≠ effectiveness (DR-033) |
| **Current Confidence** | Medium |
| **Related Decisions** | DR-028, DR-019, DR-042 |
| **Related Risks** | PR-018 |
| **Related Programmes** | P-001.2, EP-005.2, EP-006.1–EP-006.3 |
| **Validation Trigger** | External cohort interviews measuring trust + uptake; re-run Tier B after further MES changes |
| **Retirement Criteria** | Replaced by outcome-validated trust↔behaviour link (new PA), or evidence shows explanations do not move trust under production defaults |

---

## PA-002 — Schema-complete MES at service layer is insufficient without render pass-through

| Field | Content |
|---|---|
| **Title** | Service-layer MES completeness does not guarantee student-visible explainability |
| **Category** | Product |
| **Status** | Validated |
| **Statement** | Attaching a complete Mandatory Explanation Schema in services does not raise student-perceived explainability if adapters compress fields and templates omit them. Students only trust what is rendered. |
| **Origin** | EP-005.2 KSI Gap Analysis RC-01 |
| **Supporting Evidence** | `knowledge/product/ep005_2_educational_experience_validation/KSI_GAP_ANALYSIS.md` (“Services attach complete schemas; adapters compress; templates omit…”); EP-006.1 delivery specification; EP-006.2 implementation (“No educational math in presentation”) |
| **Contradicting Evidence** | None — accepted root cause; remediation path EP-006.* |
| **Current Confidence** | High |
| **Related Decisions** | DR-019, DR-005 |
| **Related Risks** | PR-011, PR-018 |
| **Related Programmes** | EP-005.2, EP-006.1, EP-006.2 |
| **Validation Trigger** | Regression if templates again omit MES fields under W-PROD |
| **Retirement Criteria** | Superseded only if MES delivery architecture is replaced with an equally evidenced student-visible contract |

---

## PA-003 — Checklist Pass alone raises validated K8 ≥ 70

| Field | Content |
|---|---|
| **Title** | Explainability checklist Pass alone raises validated K8 ≥ 70 |
| **Category** | Governance |
| **Status** | Rejected |
| **Statement** | Passing P-001.2 explainability checklists (or related quality contracts) automatically produces validated K8 ≥ 70 without student-facing perception evidence. |
| **Origin** | EP-005.1 methodology; EP-006.3 unsupported-claims log |
| **Supporting Evidence** | *(for rejection)* `knowledge/product/ep006_3_mes_perception_validation/MES_PERCEPTION_REPORT.md` (“Validated K8 ≥ 70 from checklist Pass alone \| **Unsupported**”); `knowledge/product/ep005_1_ksi_validation_evidence/VALIDATION_METHODOLOGY.md` (“Do not treat checklist Pass as automatic +10 category points”) |
| **Contradicting Evidence** | N/A — claim falsified for scoring law |
| **Current Confidence** | High (confidence in rejection) |
| **Related Decisions** | DR-026, DR-027, DR-042 |
| **Related Risks** | PR-002, PR-008 |
| **Related Programmes** | EP-005.1, EP-006.3, P-001.2 |
| **Validation Trigger** | None — do not revive without new methodology that explicitly allows it |
| **Retirement Criteria** | Remains Rejected; archival only |

---

## PA-004 — Students trust falsifiable syllabus rules more than composite intelligence speech

| Field | Content |
|---|---|
| **Title** | Falsifiable syllabus rules beat composite “intelligence” speech for trust |
| **Category** | Behavioural |
| **Status** | Supported |
| **Statement** | Students trust concrete, falsifiable syllabus rules (e.g. Learning Mode next unfinished topic) more than composite or opaque “intelligence” speech. |
| **Origin** | EP-005.2 Educational Experience Review |
| **Supporting Evidence** | `knowledge/product/ep005_2_educational_experience_validation/EDUCATIONAL_EXPERIENCE_REVIEW.md` (SV-014); Learning Mode primacy (DR-017) |
| **Contradicting Evidence** | Schema-complete MES partially restores trust for evidence-backed speech (EP-006.3 Conditional Pass) |
| **Current Confidence** | Medium |
| **Related Decisions** | DR-017, DR-028 |
| **Related Risks** | PR-018, PR-025 |
| **Related Programmes** | EP-004 private beta, EP-005.2, EP-006.3 |
| **Validation Trigger** | Stage 1 interviews comparing rule-based vs composite explanation trust |
| **Retirement Criteria** | Evidence shows composite speech trusted equally when MES-complete under production defaults |

---

## PA-005 — Opaque LLM Coach copy raises explainability and trust

| Field | Content |
|---|---|
| **Title** | Opaque LLM Coach copy raises explainability / trust |
| **Category** | Educational |
| **Status** | Rejected |
| **Statement** | Using opaque LLM-generated Coach copy (without deterministic educational truth) would raise explainability and student trust. |
| **Origin** | EP-006.1 K8 Remediation Plan non-remediations; EP-007.3 Prioritised Remediation |
| **Supporting Evidence** | *(for rejection)* `knowledge/product/ep006_1_mes_end_to_end_delivery/K8_REMEDIATION_PLAN.md` (“Opaque LLM Coach to raise trust \| Conflicts with Vision / P9”); P-001.2 P9 (“No AI-authored educational truth”) |
| **Contradicting Evidence** | N/A — constitutionally forbidden path |
| **Current Confidence** | High (confidence in rejection) |
| **Related Decisions** | DR-013, DR-028, DR-005 |
| **Related Risks** | PR-025 |
| **Related Programmes** | EP-006.1, EP-007.3, P-001.2 |
| **Validation Trigger** | None under current Educational Constitution |
| **Retirement Criteria** | Remains Rejected unless Constitution / P9 amended (out of scope here) |

---

# Part B — Canonical Home, journey, cognitive load

---

## PA-006 — Dual-home increases decision burden and caps planning trust

| Field | Content |
|---|---|
| **Title** | Dual-home (Dashboard vs Student Home) increases cognitive / decision burden |
| **Category** | Product |
| **Status** | Validated |
| **Statement** | Competing “today” homes (Dashboard vs Student Home) force weeknight reconciliation, raise decision burden, and cap planning trust (K1/K5). MES alone does not cure dual-home trust. |
| **Origin** | EP-005.2 Student Journey Review / KSI Gap Analysis RC-02 |
| **Supporting Evidence** | `knowledge/product/ep005_2_educational_experience_validation/KSI_GAP_ANALYSIS.md` RC-02; Near-Universal blind theme; `knowledge/product/ep006_3_mes_perception_validation/MES_PERCEPTION_REPORT.md` (“Dual-home trust cured by MES \| **Unsupported**”) |
| **Contradicting Evidence** | Dual-home retained when `SOLE_RUNTIME` OFF (soak/Alpha) — residual by design |
| **Current Confidence** | High |
| **Related Decisions** | DR-007, DR-020 |
| **Related Risks** | PR-017 |
| **Related Programmes** | EP-005.2, EP-006.3, EP-007.1 |
| **Validation Trigger** | Re-introduce dual-home as W-PROD default → expect regression themes |
| **Retirement Criteria** | Only if a validated alternative multi-home design proves lower burden with evidence |

---

## PA-007 — Canonical Home under sole runtime reduces organisational friction

| Field | Content |
|---|---|
| **Title** | Canonical Home reduces cognitive load / organisational friction |
| **Category** | Behavioural |
| **Status** | Supported |
| **Statement** | Consolidating to a single canonical Student Home under sole runtime reduces organisational friction (“where do I start tonight?”) and improves planning-usefulness perception. |
| **Origin** | EP-007.1 consolidation; EP-007.2 journey perception |
| **Supporting Evidence** | `knowledge/product/ep007_2_canonical_journey_perception_validation/JOURNEY_PERCEPTION_REPORT.md` (SV-016 cleared; SV-002 “weeknight reconciliation tax gone”); K1 revalidation to **72** |
| **Contradicting Evidence** | SV-009 Conditional Pass — companion only, not tool absorption; topic selection quality unchanged (PA-009); not effectiveness evidence |
| **Current Confidence** | Medium |
| **Related Decisions** | DR-007, DR-008, DR-020 |
| **Related Risks** | PR-017, PR-021 |
| **Related Programmes** | EP-007.1, EP-007.2, EP-005.2 (REM-02) |
| **Validation Trigger** | External cohort M-series on orientation / start clarity; Alpha dual-run OFF residual watch |
| **Retirement Criteria** | Evidence shows sole-runtime Home does not reduce burden, or SOLE_RUNTIME OFF becomes W-PROD default |

---

## PA-008 — Same-day duration mismatch undermines planning usefulness

| Field | Content |
|---|---|
| **Title** | Conflicting same-day session durations undermine planning usefulness |
| **Category** | Educational |
| **Status** | Validated |
| **Statement** | Showing conflicting planned session durations on the same day (e.g. preferred minutes vs weekday/weekend clock) erodes planning usefulness, trust, and completion likelihood. |
| **Origin** | EP-005.2 RC-03 (REM-03) |
| **Supporting Evidence** | `knowledge/product/ep005_2_educational_experience_validation/KSI_GAP_ANALYSIS.md` (14+ reviewers); EP-007.1 shared `resolve_planned_session_minutes()`; DR-008 |
| **Contradicting Evidence** | Residual when sole runtime OFF or surfaces bypass shared resolver |
| **Current Confidence** | High |
| **Related Decisions** | DR-008, DR-003 |
| **Related Risks** | PR-005 |
| **Related Programmes** | EP-005.2, EP-007.1, EP-003.3 |
| **Validation Trigger** | Spot-check W-PROD surfaces for dual clocks; Tier B regression |
| **Retirement Criteria** | Evidence that dual clocks no longer appear and no longer harm trust — then may move to Watch/closed operational control |

---

## PA-009 — Journey consolidation alone improves planning topic selection quality

| Field | Content |
|---|---|
| **Title** | Journey consolidation alone improves PlanningService topic selection quality |
| **Category** | Product |
| **Status** | Rejected |
| **Statement** | Consolidating the student journey / canonical Home improves PlanningService topic selection quality. |
| **Origin** | EP-007.2 unsupported-claims log |
| **Supporting Evidence** | *(for rejection)* `knowledge/product/ep007_2_canonical_journey_perception_validation/JOURNEY_PERCEPTION_REPORT.md` (“PlanningService topic selection improved \| **Unsupported** (not measured; unchanged)”) |
| **Contradicting Evidence** | N/A — not measured; must not be claimed |
| **Current Confidence** | High (confidence in rejection of the claim) |
| **Related Decisions** | DR-003, DR-007 |
| **Related Risks** | PR-002 |
| **Related Programmes** | EP-007.1, EP-007.2 |
| **Validation Trigger** | Dedicated topic-quality measurement programme |
| **Retirement Criteria** | Remains Rejected until a new measured programme validates a revised statement |

---

## PA-010 — Linear session stages aid clear progression perception

| Field | Content |
|---|---|
| **Title** | Linear session stages aid clear progression |
| **Category** | Product |
| **Status** | Hypothesis |
| **Statement** | A linear session path (overview → activity → reflection → summary → complete) helps students perceive clear progression through a study session. |
| **Origin** | EP-007.1 Student Journey Consolidation design |
| **Supporting Evidence** | `knowledge/product/ep007_1_student_journey_consolidation/STUDENT_JOURNEY_CONSOLIDATION.md` (design intent); limited Tier B stage-clarity themes |
| **Contradicting Evidence** | External behavioural completion (M4) not measured (EP-007.3) |
| **Current Confidence** | Low |
| **Related Decisions** | DR-007 |
| **Related Risks** | PR-017 |
| **Related Programmes** | EP-007.1, EP-007.3 |
| **Validation Trigger** | Stage 1 interviews + completion telemetry under privacy clearance |
| **Retirement Criteria** | Tier B/external evidence Supports or Rejects; update status accordingly |

---

# Part C — Personalisation, recommendations, feedback

---

## PA-011 — Personalisation improves educational usefulness when tertiary and visible

| Field | Content |
|---|---|
| **Title** | Personalisation improves educational usefulness |
| **Category** | Educational |
| **Status** | Hypothesis |
| **Statement** | Bounded, evidence-bound personalisation (tertiary to syllabus Decision Framework; ranks 1–3 immutable) improves educational usefulness when flags are ON and provenance is visible. |
| **Origin** | P-001.1 K4; EP-004.1–EP-004.3; DR-006 |
| **Supporting Evidence** | PSF K4 definition; EP-004 SIAs (substrate / constitutional fit); PERSONALISATION_RULES.md |
| **Contradicting Evidence** | W-PROD flags OFF → validated ΔK4 = **0** (`VALIDATED_KSI_REPORT.md`); EP-005.2 RC-06; marketing-while-OFF risk (PR-016) |
| **Current Confidence** | Low (for student benefit under current defaults) |
| **Related Decisions** | DR-006, DR-039 |
| **Related Risks** | PR-016, PR-012 |
| **Related Programmes** | EP-004.1–EP-004.3, EP-005.1, EP-005.2 |
| **Validation Trigger** | Personalisation ON in claim window + dogfood + cohort evidence + G12 matrix |
| **Retirement Criteria** | Validated K4 movement under ON defaults, or evidence of no usefulness lift → Rejected/Supported update |

---

## PA-012 — Turning personalisation/feedback flags ON immediately raises validated KSI

| Field | Content |
|---|---|
| **Title** | Flip personalisation/feedback flags ON now to raise validated KSI |
| **Category** | Operational |
| **Status** | Rejected |
| **Statement** | Turning personalisation and learning-feedback flags ON immediately (without dogfood, visible provenance, and G12 discipline) would raise validated KSI safely. |
| **Origin** | EP-005.2 KSI Gap Analysis §6 rejected remediations |
| **Supporting Evidence** | *(for rejection)* `knowledge/product/ep005_2_educational_experience_validation/KSI_GAP_ANALYSIS.md` §6; honesty / G12 risks |
| **Contradicting Evidence** | N/A |
| **Current Confidence** | High (confidence in rejection) |
| **Related Decisions** | DR-039, DR-043, DR-038 |
| **Related Risks** | PR-012, PR-016 |
| **Related Programmes** | EP-005.2, EP-004.* |
| **Validation Trigger** | Board-approved ON programme with evidence package (then new PA for measured lift) |
| **Retirement Criteria** | Remains Rejected as an immediate shortcut |

---

## PA-013 — Record-only learning feedback enables trustworthy future adaptation

| Field | Content |
|---|---|
| **Title** | Record-only feedback loop enables trustworthy future adaptation |
| **Category** | Architecture |
| **Status** | Supported |
| **Statement** | A record-only learning feedback loop (events without inventing mastery) creates substrate for future adaptation without pretending current learning already improved. |
| **Origin** | EP-003.4 Learning Feedback Loop |
| **Supporting Evidence** | `knowledge/product/ep003_4_learning_feedback_loop/STUDENT_IMPACT_ASSESSMENT.md`; DR-038 (flag OFF in W-PROD) |
| **Contradicting Evidence** | K6 floor residual; Journey emit deferred (DR-047); no validated K6 lift under W-PROD |
| **Current Confidence** | Medium (structural); Low (for K6 outcome) |
| **Related Decisions** | DR-038, DR-047 |
| **Related Risks** | PR-011 |
| **Related Programmes** | EP-003.4 |
| **Validation Trigger** | Emit path ON with privacy + telemetry honesty; K6 revalidation |
| **Retirement Criteria** | Adaptation programmes consume events with measured honesty, or architecture replaced |

---

## PA-014 — Runtime A recommendations improve study behaviour when accepted

| Field | Content |
|---|---|
| **Title** | Runtime A recommendations improve study behaviour |
| **Category** | Behavioural |
| **Status** | Hypothesis |
| **Statement** | When students accept and follow Runtime A primary recommendations, study behaviour improves (coverage, weak-topic repair, consistency) versus unguided study. |
| **Origin** | P-001.3 Recommendation Quality Standard; EP-003.1; EP-007.3 |
| **Supporting Evidence** | Design intent in `RECOMMENDATION_QUALITY_STANDARD.md`; Decision Framework (DR-029, DR-050) |
| **Contradicting Evidence** | EP-007.3 — recommendation uptake “Not instrumented / excluded”; external N = 0; DR-036 marketing freeze |
| **Current Confidence** | Low |
| **Related Decisions** | DR-002, DR-029, DR-036, DR-050 |
| **Related Risks** | PR-001, PR-024 |
| **Related Programmes** | EP-003.1, EP-007.3, P-001.3 |
| **Validation Trigger** | Stage 1 scorecards + interviews measuring uptake and M-series |
| **Retirement Criteria** | Effectiveness Go/No-Go updates; Supported or Rejected with cohort evidence |

---

## PA-015 — Recommendation ranking quality is the primary K2 gap

| Field | Content |
|---|---|
| **Title** | Recommendation ranking/decision quality is the primary K2 gap |
| **Category** | Product |
| **Status** | Rejected |
| **Statement** | The primary barrier to recommendation usefulness (K2) is ranking/algorithm quality rather than inspectability, trust, or presentation of explanations. |
| **Origin** | EP-005.2 KSI Gap Analysis §6 |
| **Supporting Evidence** | *(for rejection)* EP-005.2: “Contracts Pass; perception fails on inspectability”; EP-003.1 automated quality tests Pass |
| **Contradicting Evidence** | Future evidence could re-open ranking as a *secondary* gap after inspectability closes |
| **Current Confidence** | High (as primary-gap claim under 2026-07-26 evidence) |
| **Related Decisions** | DR-002, DR-029 |
| **Related Risks** | PR-018 |
| **Related Programmes** | EP-003.1, EP-005.2 |
| **Validation Trigger** | Post-MES K2 revalidation still fails with inspectability Pass |
| **Retirement Criteria** | Remains Rejected as *primary* gap until new evidence reorders root causes |

---

## PA-016 — Single primary recommendation CTA reduces decision burden

| Field | Content |
|---|---|
| **Title** | Single primary recommendation CTA reduces decision burden |
| **Category** | Product |
| **Status** | Supported |
| **Statement** | Presenting one primary recommendation CTA (Decision Framework) reduces decision burden versus competing next-action directors. |
| **Origin** | DR-050; P-001.3 Decision Framework |
| **Supporting Evidence** | `PRODUCT_DECISION_REGISTER.md` DR-050; EP-003.1 consolidation intent; dual-home historically competed CTAs (EP-005.2) |
| **Contradicting Evidence** | Limited dedicated Tier B isolating CTA singularity from Home consolidation |
| **Current Confidence** | Medium |
| **Related Decisions** | DR-050, DR-002, DR-029 |
| **Related Risks** | PR-017 |
| **Related Programmes** | EP-003.1, P-001.3, EP-007.1 |
| **Validation Trigger** | Perception pack isolating multi-CTA vs single-CTA |
| **Retirement Criteria** | Evidence of no burden difference, or Decision Framework change |

---

# Part D — Readiness, confidence, honesty

---

## PA-017 — Students understand readiness drivers and provisional confidence when MES-rendered on Home

| Field | Content |
|---|---|
| **Title** | Students understand readiness confidence / drivers when rendered |
| **Category** | Educational |
| **Status** | Supported |
| **Statement** | Students can understand readiness drivers and that confidence is provisional when schema-complete MES is rendered on Home (not merely computed). |
| **Origin** | EP-006.4 readiness experience; EP-006.5 perception |
| **Supporting Evidence** | `knowledge/product/ep006_5_readiness_perception_validation/STUDENT_IMPACT_ASSESSMENT.md`; SV-013 “Drivers falsify overclaim”; validated K3 **65** |
| **Contradicting Evidence** | EP-006.3 PERC-01 — Home readiness drivers Unsupported before EP-006.4; cold-start / sparse-evidence overconfidence residual (PR-005) |
| **Current Confidence** | Medium |
| **Related Decisions** | DR-004, DR-018 |
| **Related Risks** | PR-005 |
| **Related Programmes** | EP-006.4, EP-006.5, EP-003.2 |
| **Validation Trigger** | Stage 1 interviews on confidence calibration; readiness cutover ON watch |
| **Retirement Criteria** | External corroboration → Validated; or regression → Supported→Hypothesis |

---

## PA-018 — Bare readiness percentage without drivers risks false precision

| Field | Content |
|---|---|
| **Title** | Bare readiness percentage risks false precision / overconfidence |
| **Category** | Educational |
| **Status** | Supported |
| **Statement** | Showing a readiness percentage without named drivers and honesty context risks false precision and overconfidence, especially for cold-start / sparse-evidence students. |
| **Origin** | EP-006.4 SIA; EP-005.2 RC-04; Educational Constitution |
| **Supporting Evidence** | EP-006.4 SIA; blind SV-013 calibration-safety persona; PR-005 |
| **Contradicting Evidence** | Partial mitigation via drivers pass-through on Home (EP-006.4/006.5) |
| **Current Confidence** | Medium–High |
| **Related Decisions** | DR-018, DR-035 |
| **Related Risks** | PR-005 |
| **Related Programmes** | EP-003.2, EP-006.4, EP-006.5 |
| **Validation Trigger** | Spot-checks that % never appears without drivers on claim surfaces |
| **Retirement Criteria** | Controls proven durable under production defaults + no overconfidence themes |

---

## PA-019 — Recalibrating readiness weights “to feel clearer” fixes unpackability

| Field | Content |
|---|---|
| **Title** | Recalibrating readiness weights fixes unpackability |
| **Category** | Educational |
| **Status** | Rejected |
| **Statement** | Changing readiness weight calibration to make scores “feel clearer” is an appropriate fix for unpackability / explainability gaps. |
| **Origin** | EP-006.1 K8 Remediation Plan non-remediations |
| **Supporting Evidence** | *(for rejection)* EP-006.1: “Changes educational reasoning — out of scope”; ownership remains ReadinessService (DR-004) |
| **Contradicting Evidence** | N/A |
| **Current Confidence** | High (confidence in rejection as remediation path) |
| **Related Decisions** | DR-004, DR-013 |
| **Related Risks** | PR-005, PR-025 |
| **Related Programmes** | EP-006.1 |
| **Validation Trigger** | Separate educational-reasoning programme with EVF/Constitution review |
| **Retirement Criteria** | Remains Rejected as a presentation/explainability shortcut |

---

## PA-020 — Absence of evidence must remain unknown (no mastery / Exam Ready theatre)

| Field | Content |
|---|---|
| **Title** | Absence of evidence must remain “unknown” |
| **Category** | Governance |
| **Status** | Validated |
| **Statement** | Where evidence is absent or sparse, readiness and related signals must remain unknown / provisional — no mastery theatre, Exam Ready marketing, or exam-sit advice from readiness alone. |
| **Origin** | Educational Constitution; DR-024, DR-035; EP-006.5 sit-advice refusal |
| **Supporting Evidence** | P-003.1 Executive Summary; EP-006.5 perception (lawful refusal); DR-024 / DR-035 |
| **Contradicting Evidence** | PR-005 residual cold-start overconfidence risk remains watched |
| **Current Confidence** | High |
| **Related Decisions** | DR-024, DR-035, DR-018 |
| **Related Risks** | PR-005, PR-020 |
| **Related Programmes** | P-003.1, EP-006.5, EGI-001 |
| **Validation Trigger** | Exam Ready marketing request; readiness cutover ON |
| **Retirement Criteria** | Only if Constitution amended (out of scope); else permanent law |

---

# Part E — KSI, release, external validation

---

## PA-021 — KSI ≥ 80 is the binding usefulness bar for Version 1 product-success claims

| Field | Content |
|---|---|
| **Title** | KSI ≥ 80 is required for Version 1 product-success claims |
| **Category** | Release |
| **Status** | Validated |
| **Statement** | Version 1 product-success claims require validated KSI ≥ 80 under production defaults (Gate G1.1). Current validated KSI **62** does not meet the bar. |
| **Origin** | P-001.1 PSF; P-002.1 G1; DR-025, DR-051 |
| **Supporting Evidence** | `PRODUCT_SUCCESS_FRAMEWORK.md` §2.1; `VERSION_1_RELEASE_FRAMEWORK.md` G1; `Release_Gates.md` G1.1 FAIL; DR-051 |
| **Contradicting Evidence** | None on the bar; PR-002 tracks sub-bar state |
| **Current Confidence** | High |
| **Related Decisions** | DR-025, DR-051, DR-041 |
| **Related Risks** | PR-002 |
| **Related Programmes** | P-001.1, P-002.1, EP-005.1, EP-007.2, P-003.1 |
| **Validation Trigger** | New validated KSI board ≥ 80 |
| **Retirement Criteria** | PSF / G1.1 amended by governance programme (not this register) |

---

## PA-022 — KSI is a usefulness index, not Vision 2030’s north star

| Field | Content |
|---|---|
| **Title** | KSI does not replace Vision 2030 pass-rate north star |
| **Category** | Governance |
| **Status** | Validated |
| **Statement** | KSI measures operational educational usefulness categories; it is not a second north star and does not prove exam pass-rate outcomes. |
| **Origin** | P-001.1; DR-046; GOVERNANCE.md |
| **Supporting Evidence** | PSF / GOVERNANCE: “KSI is not a second north star”; G1.8 / V1-K7 distinguish usefulness from pass-rate proof; PR-024 |
| **Contradicting Evidence** | None |
| **Current Confidence** | High |
| **Related Decisions** | DR-046, DR-021 |
| **Related Risks** | PR-024 |
| **Related Programmes** | P-001.1, P-002.1 |
| **Validation Trigger** | Pass-rate methodology definition programme |
| **Retirement Criteria** | Governance amendment only |

---

## PA-023 — Estimated programme ΔKSI can be summed to infer validated KSI

| Field | Content |
|---|---|
| **Title** | Naive stacking of estimated ΔKSI yields claimable validated KSI |
| **Category** | Governance |
| **Status** | Rejected |
| **Statement** | Summing estimated programme ΔKSI contributions (e.g. ~+12 → ~70) yields a claimable validated KSI without W-PROD re-score. |
| **Origin** | EP-005.1 Validated KSI Report |
| **Supporting Evidence** | *(for rejection)* `VALIDATED_KSI_REPORT.md` (“Naive sum… **≈ +12.0 → ~70 (not claimable — double-count + gated flags)**”); EP-005.2 “EP-005.1 falsified naive stacking”; DR-026, DR-027 |
| **Contradicting Evidence** | N/A |
| **Current Confidence** | High (confidence in rejection) |
| **Related Decisions** | DR-026, DR-027 |
| **Related Risks** | PR-002, PR-008 |
| **Related Programmes** | EP-005.1, EP-005.2 |
| **Validation Trigger** | None — methodology forbids |
| **Retirement Criteria** | Remains Rejected |

---

## PA-024 — Structural / quality-contract Pass equals validated student educational value

| Field | Content |
|---|---|
| **Title** | Tier A structural Pass equals validated educational value |
| **Category** | Research |
| **Status** | Rejected |
| **Statement** | Passing structural / quality contracts (Tier A) equals validated educational value to students. |
| **Origin** | EP-005.1 methodology; EP-005.2 gap statement |
| **Supporting Evidence** | *(for rejection)* EP-005.2: “**implemented capability ≠ validated educational value** until students can see, trust, and act on it”; EP-005.1 ≤50% credit rule when Tier C conflicts; DR-021 |
| **Contradicting Evidence** | N/A |
| **Current Confidence** | High (confidence in rejection) |
| **Related Decisions** | DR-021, DR-033 |
| **Related Risks** | PR-001 |
| **Related Programmes** | EP-005.1, EP-005.2 |
| **Validation Trigger** | None under current EVF / validation methodology |
| **Retirement Criteria** | Remains Rejected |

---

## PA-025 — Perception validation confirms educational effectiveness (G1.9)

| Field | Content |
|---|---|
| **Title** | Tier B perception Pass confirms educational effectiveness / G1.9 |
| **Category** | Research |
| **Status** | Rejected |
| **Statement** | Passing Tier B perception packs (MES / readiness / journey) confirms educational effectiveness and clears Gate G1.9. |
| **Origin** | DR-033; EP-007.3 |
| **Supporting Evidence** | *(for rejection)* `EDUCATIONAL_EFFECTIVENESS_REPORT.md` (“Do not treat perception Pass as confirmation”; G1.9 **FAIL**); DR-033 “Perception is not effectiveness” |
| **Contradicting Evidence** | Perception is necessary supporting context (Medium confidence) — not sufficient |
| **Current Confidence** | High (confidence in rejection) |
| **Related Decisions** | DR-033, DR-022 |
| **Related Risks** | PR-001, PR-006 |
| **Related Programmes** | EP-006.3, EP-006.5, EP-007.2, EP-007.3 |
| **Validation Trigger** | None — law forbids substitution |
| **Retirement Criteria** | Remains Rejected |

---

## PA-026 — External cohort evidence is required for educational-effectiveness clearance

| Field | Content |
|---|---|
| **Title** | External validation is required for educational effectiveness |
| **Category** | Release |
| **Status** | Validated |
| **Statement** | External cohort evidence (Stage 1+) is required before educational-effectiveness GO or Gate G1.9 clearance. Perception and dogfood are insufficient substitutes. |
| **Origin** | P-002.1 G1.9; EP-004; EP-007.3; DR-022 |
| **Supporting Evidence** | `Release_Gates.md` G1.9; EP-007.3 COHORT_DESIGN / COHORT_EVIDENCE_REGISTER (ABSENT floors); P-003.3 board control statement (external N = 0) |
| **Contradicting Evidence** | PR-007 — privacy HOLD is not recruitment failure; Stage 0 dogfood may continue |
| **Current Confidence** | High |
| **Related Decisions** | DR-022, DR-040, DR-033 |
| **Related Risks** | PR-001, PR-003, PR-006, PR-007 |
| **Related Programmes** | EP-004, EP-007.3, P-002.1, P-003.1 |
| **Validation Trigger** | Privacy Review signed; Stage 1 ops complete; effectiveness re-verdict |
| **Retirement Criteria** | Governance amendment of G1.9 only |

---

## PA-027 — Operational GA / architecture cutover implies Version 1 educational readiness

| Field | Content |
|---|---|
| **Title** | GA or architecture cutover implies Version 1 production-ready |
| **Category** | Release |
| **Status** | Rejected |
| **Statement** | Completing operational GA, shipping a build, or finishing architecture cutover programmes implies Version 1 educational / production-ready declaration. |
| **Origin** | P-002.1 §1; EP-005.2; DR-030–DR-032 |
| **Supporting Evidence** | *(for rejection)* “Version 1 production-ready ≠ operational GA alone”; “Architecture cutover alone \| **Insufficient**”; DR-041 NO GO |
| **Contradicting Evidence** | N/A |
| **Current Confidence** | High (confidence in rejection) |
| **Related Decisions** | DR-030, DR-031, DR-032, DR-041 |
| **Related Risks** | PR-004, PR-014 |
| **Related Programmes** | P-002.1, EP-005.2, P-003.1 |
| **Validation Trigger** | None — three separable verdicts remain law |
| **Retirement Criteria** | Remains Rejected |

---

# Part F — Architecture, determinism, flags, curriculum

---

## PA-028 — Planning, readiness, and recommendations must be deterministic

| Field | Content |
|---|---|
| **Title** | Deterministic cores for planning / readiness / recommendations |
| **Category** | Architecture |
| **Status** | Validated |
| **Statement** | Planning, readiness, and recommendations must be reproducible from the same inputs (deterministic cores); opaque non-deterministic educational truth is forbidden on the production path. |
| **Origin** | DR-013; Engineering Philosophy; Educational Constitution |
| **Supporting Evidence** | `PRODUCT_DECISION_REGISTER.md` DR-013; P-003.1 Executive Summary; `.cursor/rules/00-engineering.mdc` |
| **Contradicting Evidence** | None as law |
| **Current Confidence** | High |
| **Related Decisions** | DR-013, DR-005 |
| **Related Risks** | PR-025 |
| **Related Programmes** | EP-002.9, EP-003.*, P-001.2 |
| **Validation Trigger** | Proposal to introduce non-deterministic educational authority |
| **Retirement Criteria** | Architecture / Constitution amendment only |

---

## PA-029 — Runtime A is sole student-visible educational authority under W-PROD

| Field | Content |
|---|---|
| **Title** | Runtime A is sole W-PROD educational authority |
| **Category** | Architecture |
| **Status** | Validated |
| **Statement** | Under production defaults, Runtime A (RecommendationService, PlanningService, ReadinessService) is the sole student-visible educational authority. Twin/cutover paths do not replace it while flags remain OFF. |
| **Origin** | DR-001; EP-002.9 baseline |
| **Supporting Evidence** | EP-002.9 `AUTHORITATIVE_ARCHITECTURE_BASELINE.md`; P-003.1 Architecture Summary; DR-001 |
| **Contradicting Evidence** | V2 Adaptive Decision Engine design exists but does not supersede defaults (DR-053) |
| **Current Confidence** | High |
| **Related Decisions** | DR-001, DR-002, DR-003, DR-004, DR-053 |
| **Related Risks** | PR-025, PR-012 |
| **Related Programmes** | EP-002.9, P-003.1, P-003.2 |
| **Validation Trigger** | Twin/cutover production-default ON with dual-run exit criteria |
| **Retirement Criteria** | Ownership re-certification when cutover becomes W-PROD truth |

---

## PA-030 — Twin / cutover flags default OFF; fail-open to legacy

| Field | Content |
|---|---|
| **Title** | Flag-gated Twin/cutover protects students during soak |
| **Category** | Operational |
| **Status** | Validated |
| **Statement** | Production defaults keep Digital Twin, Authority, and HTTP cutover flags OFF; student-visible payloads fail-open to legacy Runtime A; production hard-gate blocks HTTP cutovers in prod. |
| **Origin** | DR-009, DR-010; EP-002 cutover programmes |
| **Supporting Evidence** | EP-002.9 baseline §3, §6, §7; DR-009, DR-010; P-003.1 Architecture Summary |
| **Contradicting Evidence** | PR-016 marketing-vs-flag mismatch risk if claims outrun flags |
| **Current Confidence** | High |
| **Related Decisions** | DR-009, DR-010, DR-016 |
| **Related Risks** | PR-012, PR-016 |
| **Related Programmes** | EP-002.5–EP-002.9 |
| **Validation Trigger** | Board-approved production-default ON for any Twin/cutover flag |
| **Retirement Criteria** | Explicit lift programme with G12 evidence package |

---

## PA-031 — Sole runtime unifies chrome/journey, not Twin educational truth

| Field | Content |
|---|---|
| **Title** | Sole runtime ≠ Twin educational cutover |
| **Category** | Architecture |
| **Status** | Validated |
| **Statement** | `KWALITEC_V2_SOLE_RUNTIME` unifies student chrome/journey (canonical Home) and does not mean Twin educational cutover or a second educational brain is live. |
| **Origin** | DR-020 (supersedes misconception) |
| **Supporting Evidence** | DR-020 decision statement; EP-007.1 / EP-002.9 separation of concerns |
| **Contradicting Evidence** | Alpha dual-run still shows legacy shells when OFF (EP-007.2) |
| **Current Confidence** | High |
| **Related Decisions** | DR-020, DR-007, DR-001 |
| **Related Risks** | PR-016, PR-025 |
| **Related Programmes** | EP-007.1, EP-002.9 |
| **Validation Trigger** | Messaging that equates sole runtime with Twin ON |
| **Retirement Criteria** | Flag semantics redefined by architecture programme |

---

## PA-032 — Curriculum V1 and V2 must both remain loadable

| Field | Content |
|---|---|
| **Title** | Curriculum V1/V2 dual-loadability invariant |
| **Category** | Architecture |
| **Status** | Validated |
| **Statement** | Flat (V1) and hierarchical (V2) syllabus formats must both remain loadable and traversable; feature work must not silently break flat curricula. |
| **Origin** | DR-011; ADR-003; P-002.1 G2.6 |
| **Supporting Evidence** | `ARCHITECTURE.md`; ADR-003; `VERSION_1_RELEASE_FRAMEWORK.md` G2.6; DR-011, DR-012 |
| **Contradicting Evidence** | None as invariant |
| **Current Confidence** | High |
| **Related Decisions** | DR-011, DR-012 |
| **Related Risks** | (architecture compliance; no dedicated PR) |
| **Related Programmes** | P-002.1, architecture baseline |
| **Validation Trigger** | Explicit V1 retirement milestone |
| **Retirement Criteria** | Migration programme with evidence retires V1 |

---

## PA-033 — Feature-flag matrix discipline (G12) is required before educational flags ON

| Field | Content |
|---|---|
| **Title** | G12 flag-matrix discipline before educational flags ON |
| **Category** | Operational |
| **Status** | Supported |
| **Statement** | A complete, reviewed feature-flag matrix and rollback readiness (G12) is required before flipping educational flags ON as production defaults. |
| **Origin** | DR-043; P-002.1 G12; PR-012 |
| **Supporting Evidence** | DR-043; PR-012 “Feature-flag matrix / rollback unreadiness”; EP-004 flag-OFF defaults |
| **Contradicting Evidence** | Matrix completeness itself remains a residual (Hypothesis that current packaging is complete) |
| **Current Confidence** | Medium |
| **Related Decisions** | DR-043, DR-009, DR-039 |
| **Related Risks** | PR-012, PR-013 |
| **Related Programmes** | P-002.1, EP-004.*, P-003.1 |
| **Validation Trigger** | G12 PASS package published; any educational flag ON proposal |
| **Retirement Criteria** | G12 PASS sustained; then may become Validated operational control |

---

## PA-034 — Presentation must not generate educational reasoning

| Field | Content |
|---|---|
| **Title** | Presentation pass-through only (no educational reasoning) |
| **Category** | Architecture |
| **Status** | Validated |
| **Statement** | Presentation delivers authored explanations and journey chrome; it must not invent evaluation, planning, readiness scores, or a third educational narrator. |
| **Origin** | DR-005, DR-019; EP-006.2 |
| **Supporting Evidence** | EP-006.2 MES delivery implementation; P-001.2 P9; Architecture Constitution Art V–VI |
| **Contradicting Evidence** | Experience `/student` ExplanationService residual parallel stack (deferred TD in DR-005) |
| **Current Confidence** | High |
| **Related Decisions** | DR-005, DR-019 |
| **Related Risks** | PR-025 |
| **Related Programmes** | EP-002.8, EP-006.1, EP-006.2, P-001.2 |
| **Validation Trigger** | Narrator consolidation / residual stack removal |
| **Retirement Criteria** | Ownership re-certification after residual consolidation |

---

# Part G — Research methodology and behavioural links

---

## PA-035 — Blind student-only reviews yield credible qualitative evidence

| Field | Content |
|---|---|
| **Title** | Blind SV reviews are credible qualitative evidence |
| **Category** | Research |
| **Status** | Validated |
| **Statement** | Blind student-only reviews (SV-001–SV-020) with one hypothesis per persona yield credible Tier C/B qualitative evidence when protocol is followed — and do not by themselves validate post-change lifts without Tier B re-review. |
| **Origin** | EP-004 reviewer framework; EP-005.1 validation methodology |
| **Supporting Evidence** | `ep004_private_beta/reviewer_framework/REVIEW_PROTOCOL.md`; EP-005.1 §3 C-BLIND; used as falsifier and support across EP-005.2–EP-007.2 |
| **Contradicting Evidence** | Pre-change corpus does not validate post EP-003/004 perception lifts without re-review |
| **Current Confidence** | High (methodology); Medium (any single theme) |
| **Related Decisions** | DR-027 |
| **Related Risks** | PR-008 |
| **Related Programmes** | EP-004, EP-005.1, EP-006.3, EP-007.2 |
| **Validation Trigger** | Protocol change; new reviewer cohort |
| **Retirement Criteria** | Methodology superseded by board-approved replacement |

---

## PA-036 — Tier B perception packs can raise specific KSI categories without clearing G1

| Field | Content |
|---|---|
| **Title** | Perception packs can move category scores without clearing G1 |
| **Category** | Research |
| **Status** | Supported |
| **Statement** | Post-change Tier B perception packs can raise specific validated category scores (e.g. K8→70, K1→72) and composite KSI (59→62) without clearing Gate G1 (still &lt; 80) or G1.9. |
| **Origin** | EP-006.3, EP-006.5, EP-007.2 revalidations |
| **Supporting Evidence** | GOVERNANCE.md validated KSI synthesis; EP-007.2 `K1_REVALIDATION.md`; EP-006.3 MES report |
| **Contradicting Evidence** | Mid-Strong 75+ optimism Rejected without external corroboration (PR-008 Medium ceiling) |
| **Current Confidence** | Medium |
| **Related Decisions** | DR-042, DR-051, DR-027 |
| **Related Risks** | PR-002, PR-008, PR-009 |
| **Related Programmes** | EP-006.3, EP-006.5, EP-007.2 |
| **Validation Trigger** | Next validated KSI board; G1.7 independent re-score |
| **Retirement Criteria** | Replaced by newer validated board numbers |

---

## PA-037 — Planning usefulness requires one coherent tonight-plan without conflicts

| Field | Content |
|---|---|
| **Title** | Planning usefulness needs one coherent “tonight” plan |
| **Category** | Educational |
| **Status** | Supported |
| **Statement** | Planning usefulness (K1) requires one coherent “what to study tonight” plan without conflicting durations or competing today-directors. |
| **Origin** | P-001.1 K1; EP-005.2 RC-02/RC-03; EP-007.2 |
| **Supporting Evidence** | PSF K1; EP-007.2 journey pack Pass; K1 = **72**; DR-003, DR-008 |
| **Contradicting Evidence** | Topic ranking quality not measured (PA-009); external N = 0 |
| **Current Confidence** | Medium |
| **Related Decisions** | DR-003, DR-008, DR-007 |
| **Related Risks** | PR-005, PR-017 |
| **Related Programmes** | EP-003.3, EP-007.1, EP-007.2 |
| **Validation Trigger** | Stage 1 planning-usefulness interviews; topic-quality measurement |
| **Retirement Criteria** | External corroboration → Validated; or regression themes |

---

## PA-038 — Readiness usefulness depends on unpackable drivers and honest refusal

| Field | Content |
|---|---|
| **Title** | Readiness usefulness needs drivers + honesty, not percentage theatre |
| **Category** | Educational |
| **Status** | Supported |
| **Statement** | Readiness intelligence usefulness (K3) depends on unpackable drivers, honest confidence, and lawful refusal — not bare percentage theatre. |
| **Origin** | P-001.1 K3; EP-003.2; EP-006.4/006.5 |
| **Supporting Evidence** | PSF K3; EP-006.5 perception themes; validated K3 **65**; DR-004, DR-018 |
| **Contradicting Evidence** | EP-003.2 SIA historically emphasised Dashboard/Analytics path — Home path now central (see PA-041) |
| **Current Confidence** | Medium |
| **Related Decisions** | DR-004, DR-018 |
| **Related Risks** | PR-005 |
| **Related Programmes** | EP-003.2, EP-006.4, EP-006.5 |
| **Validation Trigger** | Stage 1 readiness calibration interviews |
| **Retirement Criteria** | External corroboration → Validated |

---

## PA-039 — Perception gains cause better study behaviour over time

| Field | Content |
|---|---|
| **Title** | Perception gains → better study behaviour / preparedness |
| **Category** | Behavioural |
| **Status** | Hypothesis |
| **Statement** | Runtime A perception improvements (explanations, readiness communication, coherent journey) cause better study behaviour and preparedness feeling over weeks. |
| **Origin** | EP-007.3 Educational Effectiveness Stage 1 |
| **Supporting Evidence** | Design hypothesis in `EDUCATIONAL_EFFECTIVENESS_REPORT.md` §2; COHORT_DESIGN |
| **Contradicting Evidence** | “Ops Stage 1 absent”; M1–M9 external insufficient; perception→behaviour link **Unsupported** (`CONFIDENCE_UPDATE.md`) |
| **Current Confidence** | Low |
| **Related Decisions** | DR-033, DR-022 |
| **Related Risks** | PR-001 |
| **Related Programmes** | EP-007.3 |
| **Validation Trigger** | Stage 1 privacy clearance + scorecards + interviews → effectiveness re-verdict |
| **Retirement Criteria** | Supported / Rejected / Validated after Stage 1 evidence; never claim from perception alone |

---

## PA-040 — Invite-only private beta with Privacy Review protects students while evidence is incomplete

| Field | Content |
|---|---|
| **Title** | Invite-only + Privacy Review protects students during incomplete evidence |
| **Category** | Operational |
| **Status** | Validated |
| **Statement** | Invite-only private beta with Privacy Review gate protects students from premature public expansion while educational effectiveness and KSI remain below declaration bars. |
| **Origin** | DR-034, DR-040; EP-004 Go/No-Go |
| **Supporting Evidence** | P-003.1 Executive Summary; EP-004 `GO_NO_GO_DECISION.md`; PR-003 / PR-006 / PR-007 |
| **Contradicting Evidence** | PR-015 support/commercial unreadiness if public launch forced; unsigned Privacy Review stalls evidence (trade-off accepted) |
| **Current Confidence** | High |
| **Related Decisions** | DR-034, DR-040, DR-041 |
| **Related Risks** | PR-003, PR-006, PR-007, PR-015 |
| **Related Programmes** | EP-004, P-003.1 |
| **Validation Trigger** | Public registration proposal; Privacy Review signatures |
| **Retirement Criteria** | Public launch approved under cleared privacy + evidence gates |

---

# Part H — Superseded historical assumptions

---

## PA-041 — Dashboard / Analytics is the primary readiness surface for student value

| Field | Content |
|---|---|
| **Title** | Dashboard/Analytics is the primary readiness surface |
| **Category** | Product |
| **Status** | Superseded |
| **Statement** | Student readiness value is primarily delivered via Dashboard / Analytics surfaces rather than Student Home. |
| **Origin** | EP-003.2 programme framing / SIA path assumptions |
| **Supporting Evidence** | Historical EP-003.2 SIA emphasis on Dashboard/Analytics path |
| **Contradicting Evidence** | EP-006.4/006.5 Home readiness experience; EP-007.1 canonical Home; DR-007 |
| **Current Confidence** | High (confidence that Home path is now central for W-PROD sole-runtime claim window) |
| **Related Decisions** | DR-007, DR-004, DR-018 |
| **Related Risks** | PR-017 |
| **Related Programmes** | EP-003.2, EP-006.4, EP-006.5, EP-007.1 |
| **Validation Trigger** | N/A — superseded |
| **Retirement Criteria** | Superseded by PA-017 / PA-038 + DR-007 Home-centric delivery |

---

## PA-042 — Sole runtime means Twin educational cutover is live

| Field | Content |
|---|---|
| **Title** | Sole runtime = Twin educational cutover live |
| **Category** | Architecture |
| **Status** | Superseded |
| **Statement** | Enabling sole runtime means Twin / consumer-chain educational cutover is the student-visible educational truth. |
| **Origin** | Informal cutover messaging risk during EP-002 / EP-007 |
| **Supporting Evidence** | *(historical misconception)* |
| **Contradicting Evidence** | DR-020 explicitly separates sole runtime (chrome/journey) from Twin educational authority (DR-001/DR-009) |
| **Current Confidence** | High (confidence in supersession) |
| **Related Decisions** | DR-020, DR-001, DR-009 |
| **Related Risks** | PR-016, PR-025 |
| **Related Programmes** | EP-002.9, EP-007.1, P-003.2 |
| **Validation Trigger** | N/A — superseded |
| **Retirement Criteria** | Superseded by PA-031 / DR-020 |

---

## Inventory summary

| Status | Count | IDs |
|---|---:|---|
| Validated | 15 | PA-002, PA-006, PA-008, PA-020, PA-021, PA-022, PA-026, PA-028, PA-029, PA-030, PA-031, PA-032, PA-034, PA-035, PA-040 |
| Supported | 11 | PA-001, PA-004, PA-007, PA-013, PA-016, PA-017, PA-018, PA-033, PA-036, PA-037, PA-038 |
| Hypothesis | 4 | PA-010, PA-011, PA-014, PA-039 |
| Rejected | 10 | PA-003, PA-005, PA-009, PA-012, PA-015, PA-019, PA-023, PA-024, PA-025, PA-027 |
| Superseded | 2 | PA-041, PA-042 |
| **Total** | **42** | PA-001…PA-042 |

Indexes: [`VALIDATED_ASSUMPTIONS.md`](VALIDATED_ASSUMPTIONS.md) · [`UNVALIDATED_ASSUMPTIONS.md`](UNVALIDATED_ASSUMPTIONS.md) · [`REJECTED_ASSUMPTIONS.md`](REJECTED_ASSUMPTIONS.md)