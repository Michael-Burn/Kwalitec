# Decision Traceability

**Programme:** P-003.2 — Product Decision Register  
**Date:** 2026-07-26  
**Purpose:** Map every registered decision to programme(s), primary evidence, and current status.

**Rule:** No decision appears here without an evidence path. Unsupported decisions are omitted.

Full cards: [`PRODUCT_DECISION_REGISTER.md`](PRODUCT_DECISION_REGISTER.md)

---

## 1. Decision → programme → evidence → status

| Decision ID | Title | Primary programme(s) | Primary evidence | Status |
|---|---|---|---|---|
| DR-001 | Runtime A sole educational authority | EP-002.9, EP-002.*, P-003.1 | `ep002_9_.../AUTHORITATIVE_ARCHITECTURE_BASELINE.md`; P-003.1 Architecture Summary | ACTIVE |
| DR-002 | RecommendationService owns recommendations | EP-001.4/001.5, EP-002.9, EP-003.1, P-001.3 | Authority matrix; EP-003.1 completion | ACTIVE |
| DR-003 | PlanningService owns planning | EP-001.2, EP-002.7/002.9, EP-003.3 | Baseline §4; Planning Quality Contract | ACTIVE |
| DR-004 | ReadinessService owns readiness | EP-001.3, EP-002.6/002.9, EP-003.2, EP-006.4 | Baseline; EP-003.2; EP-006.4 | ACTIVE |
| DR-005 | Presentation non-authority | EP-002.8/002.9, EP-006.1/006.2, P-001.2 | Presentation consolidation; MES specs; Explainability Standard | ACTIVE |
| DR-006 | Personalisation tertiary | EP-004.1–004.3, P-001.3 | Constitutional verifications; Decision Framework §5 | ACTIVE |
| DR-007 | Canonical Home | EP-007.1, EP-007.2, EP-005.2, V2-023 | `STUDENT_JOURNEY_CONSOLIDATION.md`; K1 revalidation | ACTIVE |
| DR-008 | Single planned session duration | EP-007.1, EP-003.3, EP-005.2 | Journey consolidation; planning contract | ACTIVE |
| DR-009 | Twin/cutover default OFF; fail-open | EP-002.5–002.9 | Baseline §3, §6, §7 | ACTIVE |
| DR-010 | Production hard-gate blocks cutovers | EP-002.5–002.9 | Baseline §3 | ACTIVE |
| DR-011 | Curriculum V1/V2 coexistence | ADR-003 | `ADR-003-curriculum-v1-v2.md`; ARCHITECTURE.md | ACTIVE |
| DR-012 | Canonical topic traversal | ADR-004, EGI-001 | ADR-004; Educational Constitution Art II | ACTIVE |
| DR-013 | Deterministic cores; no black-box LLM | EGI-001, APP-003, P-001.2 | Educational Constitution; Architecture Constitution; P-001.2 P9 | ACTIVE |
| DR-014 | Service layer; thin blueprints | ADR-001, ADR-002 | ADR-001; ADR-002; ARCHITECTURE.md | ACTIVE |
| DR-015 | Twin/Insight no educational writes | EP-001.5, EP-002.9, Twin Constitution, EGI-001 | Baseline §4; Twin Constitution | ACTIVE |
| DR-016 | Twin stack quarantine | EP-002.1, EP-002.9 | `TWIN_STACK_QUARANTINE.md` | ACTIVE |
| DR-017 | Learning Mode V1 mission authority | EGI-001 | Educational Constitution Art VI | ACTIVE |
| DR-018 | Readiness ≠ Next Action; Rec ≠ Evidence | EGI-001 | Educational Constitution Art IV, VIII | ACTIVE |
| DR-019 | MES authoring + pass-through | EP-006.1–006.3, P-001.2 | MES Delivery Specification; G1_5_STATUS | ACTIVE |
| DR-020 | Sole runtime = chrome only | V2-023, EP-007.1, EP-002.* | ARCHITECTURE.md; Educational Runtime Bridge | ACTIVE |
| DR-021 | Educational claims need educational evidence | EP-005.1, EP-007.3, EP-003, P-001.1 | VALIDATED_KSI_REPORT; G1_9_STATUS; GO_NO_GO_REPORT | ACTIVE |
| DR-022 | G1.9 external effectiveness evidence | P-001.1, P-002.1, EP-003/004/007.3, P-003.1 | Release Framework G1.9; G1_9_STATUS | ACTIVE |
| DR-023 | Document authority hierarchy | GOVERNANCE | `knowledge/GOVERNANCE.md` §1 | ACTIVE |
| DR-024 | Educational Constitution highest law | EGI-001, GOVERNANCE | Educational Constitution; GOVERNANCE split | ACTIVE |
| DR-025 | KSI ≥ 80 for V1 success claims | P-001.1, P-002.1 | PRODUCT_SUCCESS_FRAMEWORK; G1 | ACTIVE |
| DR-026 | Estimated ≠ validated KSI | P-001.1, EP-005.1 | PSF §5.6; VALIDATED_KSI_REPORT | ACTIVE |
| DR-027 | Prefer-lower scoring | P-001.1, EP-006.3, EP-005.1 | PSF §5.1; perception methodology | ACTIVE |
| DR-028 | Explainability mandatory | P-001.2, EP-003.*, EP-006.* | EXPLAINABILITY_STANDARD; GOVERNANCE §4.2 | ACTIVE |
| DR-029 | Recommendation Quality + Framework | P-001.3, EP-003.1 | Quality Standard; Decision Framework | ACTIVE |
| DR-030 | V1 requires G1–G12 | P-002.1, P-003.1, GOVERNANCE | VERSION_1_RELEASE_FRAMEWORK; GOVERNANCE §4.4 | ACTIVE |
| DR-031 | Hard-gate FAIL → NO-GO | P-002.1 | VERSION_1_GO_NO_GO_GUIDE | ACTIVE |
| DR-032 | Three separable verdicts | EP-004, EP-003, EP-007.3, P-002.1, P-003.1 | GO_NO_GO artefacts; dossier §11 | ACTIVE |
| DR-033 | Perception ≠ effectiveness | EP-007.3 (+ EP-006/007.2 context) | G1_9_STATUS; dossier lessons | ACTIVE |
| DR-034 | Invite-only; no public registration | EP-003, EP-004, security baseline | Private Beta Protocol; GO_NO_GO; PROJECT_CONTEXT | ACTIVE |
| DR-035 | Exam Ready marketing ban | P-002.1, EP-004, Vision, EP-003.2/006.4 | Release Framework G6.3; Vision Never-Build | ACTIVE |
| DR-036 | Recommendation-effectiveness freeze | EP-001, EP-003, EP-004, P-002.1 | G4.5; EP-003 G9; EP-004 forbidden claims | ACTIVE |
| DR-037 | SIA mandate | P-001.1, GOVERNANCE | SIA template; GOVERNANCE §4; reporting rule 07 | ACTIVE |
| DR-038 | Learning feedback record-only OFF | EP-003.4 | EP-003.4 completion + constitutional verification | ACTIVE |
| DR-039 | Personalisation flags OFF in W-PROD | EP-004.*, EP-005.1, P-002.1 | Completions; EP-005.1; G12 | ACTIVE |
| DR-040 | Private beta GO WITH CONDITIONS | EP-004 | `ep004_private_beta/GO_NO_GO_DECISION.md` | ACTIVE (posture) |
| DR-041 | V1 production-ready NO GO | P-003.1, P-002.1, EP-007.2/007.3 | Version_1_RELEASE_DOSSIER §11; Release_Gates | ACTIVE (posture) |
| DR-042 | K8 ≥ 70 / G1.5 PASS | EP-006.3, P-001.1, P-002.1 | G1_5_STATUS; K8_REVALIDATION | ACTIVE (posture) |
| DR-043 | Flag matrix discipline (G12) | P-002.1, EP-004, EP-002.* | Release Framework G12; dossier | ACTIVE |
| DR-044 | Final Test mandatory | GOVERNANCE, Vision | GOVERNANCE §2; Vision 2030 | ACTIVE |
| DR-045 | EVF outside decision path | EVF | EDUCATIONAL_VALIDATION_CONSTITUTION | ACTIVE |
| DR-046 | KSI ≠ north star | P-001.1, P-002.1, Vision | PSF; G1.8; Vision 2030 | ACTIVE |
| DR-047 | Analytics Journey emit deferred | Analytics EP-002, P-003.1 | VERSION_1_READINESS; Release_Gates G9 | ACTIVE |
| DR-048 | Idempotent bootstrap | Engineering baseline | ARCHITECTURE.md; PROJECT_CONTEXT | ACTIVE |
| DR-049 | MissionOptimizer quarantined | EP-002.*, EP-001.2 | Baseline §4/§8; OWNERSHIP_CERTIFICATION | ACTIVE |
| DR-050 | Single primary recommendation CTA | P-001.3, EP-003.1 | Decision Framework §§2,6; EP-003.1 | ACTIVE |
| DR-051 | Current validated KSI = 62 | EP-007.2 (+ chain), P-003.1 | K1_REVALIDATION; KSI_Evolution | ACTIVE (posture) |
| DR-052 | EP-003 contracts bind Runtime A | EP-003.1–003.3, EP-005.1 | Completions; dossier §2 | ACTIVE |
| DR-053 | V2 Adaptive Decision ≠ Runtime A defaults | V2-017, EP-002.9 | ADR-005; ADR-007; EP-002.9 | ACTIVE |

---

## 2. Programme → decisions

| Programme | Decisions established or confirmed |
|---|---|
| **Vision 2030 / GOVERNANCE** | DR-023, DR-044, DR-046 (partial), DR-035 (Never-Build) |
| **EGI-001 Educational Constitution** | DR-013, DR-017, DR-018, DR-024, DR-012 (curriculum primacy) |
| **ADR-001 / ADR-002** | DR-014 |
| **ADR-003 / ADR-004** | DR-011, DR-012 |
| **EP-001.*** | DR-002–DR-004 (ownership seeds), DR-036 (freeze), DR-015 |
| **EP-002.*** / **EP-002.9** | DR-001, DR-005, DR-009, DR-010, DR-015, DR-016, DR-020, DR-049, DR-053 |
| **P-001.1** | DR-025, DR-026, DR-027, DR-037, DR-046 |
| **P-001.2** | DR-028, DR-005, DR-019 (schema law) |
| **P-001.3** | DR-029, DR-006, DR-050 |
| **P-002.1** | DR-022, DR-030, DR-031, DR-035, DR-036, DR-043 |
| **EP-003 (umbrella)** | DR-021, DR-032, DR-034, DR-036 |
| **EP-003.1–.3** | DR-002–DR-004, DR-050, DR-052, DR-028/029 structural |
| **EP-003.4** | DR-038 |
| **EP-004 (umbrella)** | DR-040, DR-032, DR-034, DR-035 |
| **EP-004.1–.3** | DR-006, DR-039 |
| **EP-005.1** | DR-026, DR-021, SD-001/SD-002 |
| **EP-005.2** | REM-02/03 → DR-007, DR-008 |
| **EP-006.1–.3** | DR-019, DR-042, SD-012 |
| **EP-006.4–.5** | DR-004 (Home delivery), DR-051 chain |
| **EP-007.1–.2** | DR-007, DR-008, DR-051 |
| **EP-007.3** | DR-022, DR-033, DR-021 |
| **P-003.1** | DR-041, DR-032, DR-051 (synthesis), Architecture restatement of DR-001–DR-005 |
| **P-003.2 (this programme)** | Register packaging only — does not create new product law |
| **V2-023** | DR-007, DR-020 |
| **V2 ADR-005/007** | DR-053 (coexistence clarification) |
| **EVF** | DR-045 |
| **Analytics EP-002** | DR-047 |
| **APP-003 / Twin Constitution** | DR-005, DR-013, DR-015 |

---

## 3. Evidence class → decisions

| Evidence class | Example paths | Decisions |
|---|---|---|
| Authoritative architecture | `ep002_9_.../AUTHORITATIVE_ARCHITECTURE_BASELINE.md` | DR-001–DR-005, DR-009–DR-010, DR-015–DR-016, DR-049 |
| Educational law | `KWALITEC_EDUCATIONAL_CONSTITUTION.md` | DR-017, DR-018, DR-024, DR-013 |
| Product standards | `p001_1_*`, `p001_2_*`, `p001_3_*` | DR-025–DR-029, DR-037, DR-050 |
| Release law | `p002_1_*` | DR-022, DR-030, DR-031, DR-043 |
| Board synthesis | `p003_1_*` | DR-041, DR-051, Architecture restatement |
| Go/No-Go artefacts | EP-003/004 GO_NO_GO; EP-007.3 G1.9 | DR-032, DR-040, DR-022, DR-033 |
| Perception / KSI boards | EP-005.1; EP-006.3/006.5; EP-007.2 | DR-042, DR-051, DR-027 |
| Journey consolidation | EP-007.1 | DR-007, DR-008 |
| MES delivery | EP-006.1–006.2 | DR-019 |
| Personalisation | EP-004.* constitutional verifications | DR-006, DR-039 |
| ADRs | curriculum / service / blueprint ADRs | DR-011, DR-012, DR-014, DR-053 |

---

## 4. Supersession traceability

| Superseded ID | Successor decision(s) | Evidence of supersession |
|---|---|---|
| SD-001 | DR-026, DR-027 | EP-005.1 VALIDATED_KSI_REPORT |
| SD-002 | DR-051 | EP-006.3 → EP-006.5 → EP-007.2 chain |
| SD-003 | DR-007, DR-020 | EP-007.1 / EP-007.2 |
| SD-004 | DR-008 | EP-007.1 |
| SD-005 | DR-005, DR-019 | EP-002.8 / EP-006.* |
| SD-006 | DR-021, DR-025, DR-026, DR-052 | EP-005.1; P-003.1 lessons |
| SD-007 | DR-039, DR-006, DR-043 | EP-005.1 |
| SD-008 | DR-033, DR-022, DR-021 | EP-007.3 |
| SD-009 | DR-030, DR-031, DR-041 | P-002.1; P-003.1 |
| SD-010 | DR-001, DR-009, DR-010 | EP-002.9 |
| SD-011 | DR-053, DR-001, DR-002 | ADR-005 coexistence clarification |
| SD-012 | DR-019, DR-042 | EP-006.1–006.3 |

Detail: [`SUPERSEDED_DECISIONS.md`](SUPERSEDED_DECISIONS.md)

---

## 5. Current board posture snapshot (traceable)

| Posture | Decision | Evidence date | Status |
|---|---|---|---|
| Private beta execution | DR-040 GO WITH CONDITIONS | 2026-07-24 | ACTIVE (posture) |
| Educational effectiveness | DR-022 / DR-033 → NO-GO / PENDING EVIDENCE | 2026-07-26 | ACTIVE (law + posture) |
| Version 1 production-ready | DR-041 NO GO | 2026-07-26 | ACTIVE (posture) |
| Validated KSI | DR-051 = 62 | 2026-07-26 | ACTIVE (posture) |
| G1.5 explainability floor | DR-042 PASS (K8=70) | 2026-07-26 | ACTIVE (posture) |

---

## 6. Intentionally not registered

The following were reviewed and **not** elevated to DR entries because they are meta-models, deferred residuals, or lack Product Board governing force as Version 1 behaviour law:

- Constitutional decision *lifecycle/completion models* under `knowledge/decision/**` (meta-law for decision objects, not product behaviour).  
- Open residuals without binding product rule (e.g. Experience narrator consolidation TD; G1.7 HOLD as incomplete evidence rather than a standing behavioural law).  
- Forward V2 roadmap items that do not yet govern W-PROD student behaviour (except coexistence clarifications such as DR-053).  
- Individual Tier B persona findings without programme-level decision force.

Lifecycle for adding future decisions: [`DECISION_LIFECYCLE.md`](DECISION_LIFECYCLE.md).
