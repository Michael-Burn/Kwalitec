# Kwalitec Governance

**Version:** 1.0  
**Status:** Active  
**Effective:** July 2026  
**Programme:** Post-Consolidation Product Governance  

This document defines permanent governance for product, architecture, and engineering decisions after Architecture Consolidation.

It does **not** redesign the application or change educational algorithms.

---

## 1. Document hierarchy

Authority flows **downward**. Lower documents must not contradict higher ones. When conflict appears: **STOP**, document, recommend amendment of the higher authority first.

| Rank | Document | Canonical path | Owns |
|---:|---|---|---|
| 1 | Product Vision 2030 | `knowledge/product/vision/PRODUCT_VISION_2030.md` | Why; north star; philosophies; never-build; Final Test |
| 2 | Product Blueprint | `PRODUCT_BLUEPRINT.md` (repo root) | Strategy; audiences; model; roadmap; promise |
| 2a | Product Success Framework (KSI) | `knowledge/product/p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md` | Educational usefulness measurement; Version 1 KSI ≥ 80; roadmap prioritisation by student value |
| 2b | Explainability Standard | `knowledge/product/p001_2_explainability_standard/EXPLAINABILITY_STANDARD.md` | Product explainability levels, mandatory schema, patterns, quality; review gate for student-facing intelligence |
| 2c | Recommendation Quality Standard | `knowledge/product/p001_3_recommendation_quality_standard/RECOMMENDATION_QUALITY_STANDARD.md` | Product recommendation quality principles, dimensions, decision framework, scorecard; review gate for student-facing recommendations |
| 2d | Version 1 Release Framework | `knowledge/product/p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md` | When Version 1 may be declared production-ready; gates G1–G12; evidence package; go / no-go |
| 2e | Version 1 Release Dossier | `knowledge/product/p003_1_version1_release_dossier/Version_1_RELEASE_DOSSIER.md` | Board-level evidence synthesis for release decisions (does not amend gates or declare Version 1) |
| 2f | Commercial Readiness Framework (CRI) | `knowledge/product/cq001_commercial_readiness/COMMERCIAL_READINESS_FRAMEWORK.md` | Version 1 commercial-quality index; CRI prioritisation; living Commercial Readiness Board |
| 3 | Educational Constitution | `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` | Educational law and truth |
| 4 | Educational Validation Framework (EVF) | `knowledge/educational_validation/` | Educational quality / trust; Educational Release Gate |
| 5 | Architecture Constitution + System Architecture | `docs/ARCHITECTURE_CONSTITUTION.md`, `docs/architecture/SYSTEM_ARCHITECTURE.md`, `ARCHITECTURE.md` | Structural law; one runtime; layering |
| 6 | ADRs | `docs/adr/` (primary EOS); historical trees indexed there | Accepted architectural decisions |
| 7 | Engineering Standards + Quality Manual | `knowledge/ENGINEERING_STANDARDS.md`, `knowledge/QUALITY_MANUAL.md` | How we build and verify |
| 8 | PRDs | `knowledge/prd/` | Feature proposals |
| 9 | Release Playbook + Release Protocol | `knowledge/RELEASE_PLAYBOOK.md`, `docs/process/RELEASE_PROTOCOL.md` | How we ship |
| 10 | Version 1 Readiness | `knowledge/VERSION_1_READINESS.md` | Readiness tracking (statuses must reflect P-002.1 evidence) |

**KSI note:** The Product Success Framework does not replace Vision 2030. KSI is the operational educational-usefulness index that serves the north star. Version 1 product-success claims require **KSI ≥ 80** per that framework.

**Version 1 release note:** The Version 1 Release Framework (P-002.1) does not replace Vision 2030, KSI, or the EVF Educational Release Gate. It defines objective gates (validated KSI, constitutional compliance, explainability / recommendation / planning / readiness quality, performance, reliability, telemetry, security, tests, feature flags) and the evidence / go-no-go process for declaring Version 1 **production-ready**. Estimated programme ΔKSI alone is insufficient. The Version 1 Release Dossier (P-003.1) synthesises board evidence for release decisions; it does not amend gates and does not itself declare Version 1.

**Explainability note:** The Explainability Standard does not replace EIP-003 Educational Explainability Standard or Architecture Constitution Article IV. It specialises product levels, schema, patterns, and the review gate for student-facing intelligence. Version 1 criterion **V1-K3** (K8 ≥ 70) depends on conformance to this standard in implementation programmes.

**Recommendation quality note:** The Recommendation Quality Standard does not replace the Educational Recommendation Model or Recommendation Objectives. It specialises product quality principles, prioritisation, scorecard metrics, and the review gate for student-facing recommendations. Version 1 criterion **V1-K2** (no category below 50) is met on the validated board (K2 **68** per EP-008.1B / EP-008.3B hold) — Partial upper, not Strong-band. Strong-band K2 and effectiveness claims still require observational commitment / acceptance rates (Stage 0/1) after EP-008.3A instrumentation. Complementary to the Explainability Standard (selection/priority vs speech).

**Commercial Readiness note:** The Commercial Readiness Framework (CQ-001) does not replace Vision 2030, KSI, or P-002.1. CRI is the operational commercial-quality index for Version 1 prioritisation (founder-trusted premium daily study OS). From CQ-001 onwards, Version 1 work must optimise CRI; tasks without measurable CRI improvement defer to the Version 2 backlog. Milestone tags `cri-45`…`cri-90` and `v1.0.0` must not be created prematurely; `v1.0.0` additionally requires P-002.1 production-ready declaration. Living board: `knowledge/product/cq001_commercial_readiness/COMMERCIAL_READINESS_BOARD.md` (baseline CRI **43%**, provisional).

**Validated KSI note:** Estimated programme ΔKSI does not satisfy Gate G1. The current validated assessment is `knowledge/product/ep005_1_ksi_validation_evidence/` (baseline KSI **59**) updated by `knowledge/product/ep006_3_mes_perception_validation/` (K8 then **70**, Gate **G1.5 PASS**), `knowledge/product/ep006_5_readiness_perception_validation/` (K3 **65**), `knowledge/product/ep007_2_canonical_journey_perception_validation/` (K1 **72**; KSI then **62**), `knowledge/product/ep008_1b_recommendation_trust_validation/` (K2 **68**; K8 **72**; KSI **64**), and `knowledge/product/ep008_3b_recommendation_commitment_validation/` (K2 **68** hold; K7 **60**; K8 **72** hold; KSI **64**; overall Gate G1 **FAIL** as of 2026-07-26). Experience-gap root causes and G1 remediation priorities are in `knowledge/product/ep005_2_educational_experience_validation/` (EP-005.2). MES delivery path audit, student-visible delivery contract, and K8 / G1.5 remediation design are in `knowledge/product/ep006_1_mes_end_to_end_delivery/` (EP-006.1). MES delivery implementation (presentation pass-through for Home/Coach) is in `knowledge/product/ep006_2_mes_delivery_implementation/` (EP-006.2). MES Tier B perception validation is in `knowledge/product/ep006_3_mes_perception_validation/` (EP-006.3). Home readiness experience completion (drivers / confidence / review / next) is in `knowledge/product/ep006_4_readiness_experience_completion/` (EP-006.4). Readiness Tier B perception validation is in `knowledge/product/ep006_5_readiness_perception_validation/` (EP-006.5). Student journey consolidation (single Home / duration fact; REM-02 / REM-03) is in `knowledge/product/ep007_1_student_journey_consolidation/` (EP-007.1). Canonical journey Tier B perception validation is in `knowledge/product/ep007_2_canonical_journey_perception_validation/` (EP-007.2). Educational effectiveness Stage 1 cohort design / assessment and Gate G1.9 review are in `knowledge/product/ep007_3_educational_effectiveness_validation_stage1/` (EP-007.3 — effectiveness **NO-GO / PENDING EVIDENCE**; G1.9 **FAIL**; external N = 0). KSI gap analysis and improvement roadmap are in `knowledge/product/p004_1_ksi_gap_analysis/` (P-004.1). Recommendation Trust presentation design and delivery are in `knowledge/product/ep008_1_recommendation_trust/` (EP-008.1 / EP-008.1A). Recommendation Trust Tier B validation is in `knowledge/product/ep008_1b_recommendation_trust_validation/` (EP-008.1B — K2 **68**; permanence recommended). Recommendation Commitment & Follow-through design and delivery are in `knowledge/product/ep008_3_recommendation_commitment_followthrough/` (EP-008.3 / EP-008.3A — IMP-02; no ranking change). Recommendation Commitment Tier B validation is in `knowledge/product/ep008_3b_recommendation_commitment_validation/` (EP-008.3B — K2 hold **68**; K7 **60**; permanence recommended for presentation; Strong-band / follow-through rates still open). Stage 1 operational readiness assessment is in `knowledge/product/ep008_2a_stage1_operational_readiness/` (EP-008.2A — enrollment **HOLD**; Critical privacy / Pilot analytics gates; ΔKSI **0**). Stage 1 pilot readiness closure packages are in `knowledge/product/ep008_2b_stage1_pilot_readiness_closure/` (EP-008.2B — OR-01/OR-02 docs complete; signatures/evidence **OPEN**; enrollment **HOLD**; ΔKSI **0**). Product Board release synthesis and recommendation (**NO GO**) are in `knowledge/product/p003_1_version1_release_dossier/` (P-003.1).

**Educational authority split:** EGI Educational Constitution / Governance Review own *lawful educational meaning and integrity*. EVF owns *whether educational quality is sufficient to release to students*. EVF consumes Blind Review; it does not replace it.

**Educational Framework Freeze (EF-001):** The Educational Framework corpus — Educational Excellence (EA-001…EA-008), Educational Operations (EO-001), Educational Trust (TV-001), Educational Justification (EJ-001), and Editorial Workspace (EW-001) — is **FROZEN** as Version 1 Educational Law under operational stewardship (`EF001_EDUCATIONAL_FRAMEWORK_FREEZE.md`). No further Educational Framework design programmes unless a genuine Founder Validation / Private Beta failure cannot be explained by existing law and evidence shows framework deficiency (not content or execution). Post-freeze engineering prioritises Volume production, Founder study, Private Beta, evidence-driven improvement, and author tooling that does not lower frozen quality exits.

### Path note (resolved)

The post-consolidation directive referenced `knowledge/PRODUCT_BLUEPRINT.md`. The authoritative Blueprint remains at **repository root** `PRODUCT_BLUEPRINT.md` to avoid duplication. Do not create a second Blueprint under `knowledge/`.

### Supporting indexes

| Index | Path |
|---|---|
| Vision folder | `knowledge/product/vision/README.md` |
| Knowledge base | `knowledge/README.md` |
| Version 1 Release Dossier | `knowledge/product/p003_1_version1_release_dossier/` |
| ADR index (EOS) | `docs/adr/README.md` |
| Ubiquitous language | `UBIQUITOUS_LANGUAGE.md` |
| Product language (UI) | `knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md` |

---

## 1a. Founder-operated approval authority (GP-001)

Kwalitec is **founder-operated**. A single Founder currently holds the governance **capacities** Product Owner, Engineering Owner, Operations Owner, Privacy Owner, and Product Board Chair. Multi-person role names elsewhere in this corpus describe capacities, not separate staff.

| Artefact | Path |
|---|---|
| Founder Governance Model | `knowledge/product/gp001_founder_governance_model/FOUNDER_GOVERNANCE_MODEL.md` |
| Role mapping | `knowledge/product/gp001_founder_governance_model/ROLE_MAPPING.md` |
| Approval matrix | `knowledge/product/gp001_founder_governance_model/UPDATED_APPROVAL_MATRIX.md` |

**Hard rules:** Evidence Hierarchy, claim standards, dry-runs, Privacy Review, kill-switch rehearsal, and P-002.1 gate evidence are **not** weakened. Product Board remains the sole Version 1 GO / NO GO recommendation authority (Founder acts as Chair and records capacity Founder Reviews). Independent second-assessor duties (e.g. G1.7) are **not** satisfied by capacity concentration alone. Independent separation of duties is deferred until organisational scale — Decision **DR-054**; residual **PR-027**.

Material approvals use **Founder Review** records: Reviewer · Date · Decision · Notes (capacity exercised).

---

## 2. Decision hierarchy

| Decision type | Primary authorities | Approver (default) |
|---|---|---|
| Product philosophy / never-build | Vision 2030 | Founder — Product Owner capacity |
| Roadmap / audience / promise | Blueprint | Founder — Product Owner capacity |
| Educational usefulness / Version 1 KSI bar / prioritisation by student value | Product Success Framework (KSI) | Founder — Product Owner capacity |
| Version 1 commercial-quality prioritisation / CRI bar / V2 deferral | Commercial Readiness Framework (CRI) | Founder — Product Owner capacity |
| Version 1 production-ready declaration (gates G1–G12) | Version 1 Release Framework (P-002.1) + EVF educational outcome | Founder as Product Board Chair after capacity Founder Reviews (Educational / Architecture / Engineering / Privacy / Operations lenses) |
| Version 1 board evidence synthesis / release dossier | Version 1 Release Dossier (P-003.1) | Founder — Product Owner capacity (does not replace P-002.1 gates) |
| Student-facing explanation levels / schema / Runtime A consistency | Explainability Standard (P-001.2) + EIP-003 | Founder — Product Owner + Educational Gate Owner capacities |
| Student-facing recommendation quality / prioritisation / K2 usefulness | Recommendation Quality Standard (P-001.3) + Educational Recommendation Model | Founder — Product Owner + Educational Gate Owner capacities |
| Educational meaning / mastery / evidence | Educational Constitution | Founder — Educational Gate Owner capacity |
| Educational quality / student trust to release | Educational Validation Framework (Release Gate) | Founder — Educational Gate Owner capacity |
| Runtime, layering, Twin boundaries | Architecture Constitution + ADRs | Founder — Engineering Owner (architecture lens) |
| Feature scope | PRD → Vision + Blueprint + KSI alignment | Founder — Product Owner (+ Engineering Owner as needed) |
| Implementation pattern | Engineering Standards + ADRs | Founder — Engineering Owner capacity |
| Ship / rollback | Release Playbook + Protocol (+ EVF educational outcome) | Founder — Operations Owner (release lens) |

**Final Test (mandatory for features):**

> Does this help students become better professionals?

If no → do not build.

**KSI contribution (mandatory for material EP / P programmes):**

> What is the estimated KSI contribution, and which baseline gaps does this close?

If none can be articulated → do not start as a student-value programme (infra / security / docs exceptions must state ΔKSI = 0 explicitly).

**CRI contribution (mandatory for Version 1 material programmes from CQ-001 onwards):**

> Which CRI domains does this improve, what is the expected CRI increase, what is the founder benefit, and what is the release risk?

If no measurable CRI improvement → defer to `knowledge/product/cq001_commercial_readiness/VERSION_2_BACKLOG.md` (infra / security / docs exceptions must state ΔCRI = 0 explicitly and justify Version 1 capacity).

---

## 3. Review process

### 3.1 Document review

| Trigger | Action |
|---|---|
| End of major release | Review Vision (philosophy drift), Blueprint (roadmap), Readiness tracker |
| End of Epic | Review Technical Debt Register, ADR currency, Quality Manual budgets |
| Educational capability change | Educational Governance Review Standard (EGI-003) |
| Educational version release / trust claims | Educational Validation Framework Release Gate (`knowledge/educational_validation/`) |
| Architecture boundary change | New or amended ADR before merge |

### 3.2 Pull Request review

Every PR must satisfy (see Engineering Standards):

- Tests
- Documentation
- Accessibility (if UI)
- Security
- Performance (budgets / no regress without justification)
- Architecture (layering, no duplicate educational logic)

### 3.3 When uncertain

1. **STOP**
2. **Document** the uncertainty
3. **Recommend** options with Vision / Blueprint / Educational Constitution citations
4. **Never guess** into educational algorithms, Twin, or EducationalStateService

---

## 4. Feature proposal process

1. Author a PRD using `knowledge/prd/PRD_TEMPLATE.md`.
2. Complete Vision Alignment and Architecture Impact sections honestly.
3. Product reviews student/educational benefit, Final Test, and estimated KSI contribution (categories K1–K8).
4. Architecture reviews Educational State / Twin / runtime impact.
5. If educational law may be affected → Educational Governance review before implementation.
6. Implementation follows Engineering Standards; PR uses Definition of Done.
7. Completion report per project reporting rules when required by milestone.

**No PRD → no significant feature work.**

Exceptions (still require review notes): hotfixes, pure docs, pure chore with no behaviour change.

### 4.1 EP / P programme completion (mandatory student-value sections)

Every future **EP** or **P** programme completion report must include:

| Section | Requirement |
|---|---|
| **Student Impact Assessment** | Completed assessment using `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md` (or equivalent sections + link) |
| **Estimated KSI contribution** | Category deltas (K1–K8) and net ΔKSI; may be 0 with rationale |
| **Evidence collected** | Paths to tests, reviews, metrics, dogfood, interviews |
| **Lessons learned for student value** | What the programme taught about educational usefulness |

Architectural blast-radius tables (flag/cohort visibility) may supplement the Student Impact Assessment; they do not replace student-problem / benefit / KSI sections.

Standard engineering completion sections (Summary, Files Created/Modified, Tests, Migration, Architecture Compliance, Technical Debt, Known Limitations) remain required when the milestone uses the project reporting template.

### 4.2 Explainability review (mandatory for student-facing intelligence)

Every future **EP** or **P** programme that affects **student-facing intelligence** (recommendations, predictions, planning decisions, readiness assessments, Coach/Insights narration, or related Runtime A guidance speech) must complete the Explainability Review Checklist:

| Artefact | Path |
|---|---|
| **Explainability Standard** | `knowledge/product/p001_2_explainability_standard/EXPLAINABILITY_STANDARD.md` |
| **Explanation Patterns** | `knowledge/product/p001_2_explainability_standard/EXPLANATION_PATTERNS.md` |
| **Explainability Review Checklist** | `knowledge/product/p001_2_explainability_standard/EXPLAINABILITY_REVIEW_CHECKLIST.md` |

Mandatory verification themes (see checklist for full items):

1. Explanations are evidence-backed.
2. Confidence is communicated appropriately.
3. Student action is clear.
4. Explanations avoid unnecessary technical detail.
5. Explanations remain consistent across Runtime A.

Docs-only / infra-only programmes with no student-facing intelligence speech may record **N/A** with a one-line rationale. K8 Explainability score claims require a checklist **Pass** (or an explicit Product + Educational waiver).

### 4.3 Recommendation quality review (mandatory for student-facing recommendations)

Every future **EP** or **P** programme that affects **student-facing recommendations** (ranking, selection, RecommendationService prioritisation, Coach/Insights/Mission “what to do next” tips, revision/recovery/workload recommendations, or Runtime A primary-recommendation consolidation) must complete the Recommendation Review Checklist:

| Artefact | Path |
|---|---|
| **Recommendation Quality Standard** | `knowledge/product/p001_3_recommendation_quality_standard/RECOMMENDATION_QUALITY_STANDARD.md` |
| **Recommendation Decision Framework** | `knowledge/product/p001_3_recommendation_quality_standard/RECOMMENDATION_DECISION_FRAMEWORK.md` |
| **Recommendation Quality Scorecard** | `knowledge/product/p001_3_recommendation_quality_standard/RECOMMENDATION_QUALITY_SCORECARD.md` |
| **Recommendation Review Checklist** | `knowledge/product/p001_3_recommendation_quality_standard/RECOMMENDATION_REVIEW_CHECKLIST.md` |

Mandatory verification themes (see checklist for full items):

1. Recommendation solves a real student problem.
2. Recommendation is evidence-backed.
3. Recommendation is proportionate.
4. Recommendation has clear expected benefit.
5. Recommendation aligns with Product Constitution.
6. Recommendation complies with Explainability Standard.

When recommendation *speech* also changes, complete §4.2 Explainability Review as well. Docs-only / infra-only programmes with no recommendation behaviour or speech may record **N/A** with a one-line rationale. K2 Recommendation usefulness score claims require a checklist **Pass** (or an explicit Product + Educational waiver).

### 4.4 Version 1 production-ready declaration (mandatory gates)

Declaring **Kwalitec Version 1 production-ready** requires the Version 1 Release Framework — not estimated KSI alone, not GA certification alone, and not architecture cutover alone.

| Artefact | Path |
|---|---|
| **Version 1 Release Framework** | `knowledge/product/p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md` |
| **Acceptance Checklist** | `knowledge/product/p002_1_version_1_release_framework/VERSION_1_ACCEPTANCE_CHECKLIST.md` |
| **Go / No-Go Guide** | `knowledge/product/p002_1_version_1_release_framework/VERSION_1_GO_NO_GO_GUIDE.md` |
| **Evidence Requirements** | `knowledge/product/p002_1_version_1_release_framework/VERSION_1_EVIDENCE_REQUIREMENTS.md` |
| **Validated KSI (EP-005.1)** | `knowledge/product/ep005_1_ksi_validation_evidence/VALIDATED_KSI_REPORT.md` (updated by EP-006.3 / EP-006.5 / EP-007.2 / EP-008.1B / EP-008.3B to KSI **64**; K7 **60**) |
| **Gate G1 status** | `knowledge/product/ep005_1_ksi_validation_evidence/VERSION_1_G1_STATUS.md` (overall **FAIL**; G1.5 see EP-006.3; K3 see EP-006.5; K1 see EP-007.2; K2/KSI see EP-008.1B; K7 see EP-008.3B; G1.9 see EP-007.3) |
| **Version 1 Release Dossier (P-003.1)** | `knowledge/product/p003_1_version1_release_dossier/` (board synthesis; recommendation **NO GO**) |
| **G1 remediation strategy (EP-005.2)** | `knowledge/product/ep005_2_educational_experience_validation/PRIORITISED_REMEDIATION_PLAN.md` |
| **MES delivery / K8 G1.5 path (EP-006.1)** | `knowledge/product/ep006_1_mes_end_to_end_delivery/K8_REMEDIATION_PLAN.md` |
| **MES delivery implementation (EP-006.2)** | `knowledge/product/ep006_2_mes_delivery_implementation/` |
| **MES perception validation / G1.5 (EP-006.3)** | `knowledge/product/ep006_3_mes_perception_validation/` (K8 **70**; G1.5 **PASS**) |
| **Readiness experience completion (EP-006.4)** | `knowledge/product/ep006_4_readiness_experience_completion/` |
| **Readiness perception validation / K3 (EP-006.5)** | `knowledge/product/ep006_5_readiness_perception_validation/` (K3 **65**; KSI **61**) |

Mandatory themes:

1. Validated KSI ≥ 80 (and V1-K2…V1-K7) under Product Success Framework.  
2. Constitutional compliance (Vision / Educational / Architecture) including EVF Gate outcome.  
3. Explainability, Recommendation, Planning, and Readiness quality compliance.  
4. Performance, reliability, production telemetry, security/data integrity, tests, feature-flag readiness.  
5. Complete Version 1 Evidence Package + signed go / no-go decision.

EP/P programme completion reports that claim progress toward Version 1 readiness should cite residual open gates when relevant. Docs/governance programmes that only define law may record N/A for a live declaration.

### 4.5 Commercial Readiness (CRI) — mandatory for Version 1 programmes

From **CQ-001** onwards, every material **Version 1** programme completion report must include:

| Section | Requirement |
|---|---|
| **CRI domains improved** | Which of CR1–CR9 (or none with rationale) |
| **Estimated CRI delta** | Net points; may be 0 with rationale |
| **Evidence supporting the increase** | Paths / artefacts |
| **Remaining blockers** | What still caps affected domains |
| **Provisional or validated** | Label the delta; tags require validated thresholds |

| Artefact | Path |
|---|---|
| **Commercial Readiness Framework** | `knowledge/product/cq001_commercial_readiness/COMMERCIAL_READINESS_FRAMEWORK.md` |
| **Living Board** | `knowledge/product/cq001_commercial_readiness/COMMERCIAL_READINESS_BOARD.md` |
| **Task intake** | `knowledge/product/cq001_commercial_readiness/TASK_INTAKE_TEMPLATE.md` |
| **Version 2 backlog** | `knowledge/product/cq001_commercial_readiness/VERSION_2_BACKLOG.md` |

**Priority order (normative):** CR1 → CR2 → CR4 → CR3 → CR5 → CR6 → CR8 → CR7 (maintain) → CR9.

Do not introduce Version 2 capabilities unless they directly improve current CRI. Do not create `cri-45`…`cri-90` or `v1.0.0` tags prematurely.

---

## 5. Architecture proposal process

1. Confirm Vision / Blueprint / Educational Constitution do not forbid the change.
2. Write or amend an ADR under the correct tree (`docs/adr/` for EOS boundaries).
3. ADR must reference Vision 2030, Blueprint, and Educational Principles (Constitution).
4. Update `docs/adr/README.md` (and secondary indexes if historical trees change).
5. Prefer additive changes with compatibility shims over breaking rewrites.
6. Document migration impact and V1/V2 curriculum effects.
7. Do not bypass StartupService safety or introduce a second educational brain.

**Forbidden without explicit programme authority:**

- Redesigning the Student Digital Twin
- Changing EducationalStateService contracts casually
- Changing educational algorithms under “governance” or “docs” cover
- Introducing duplicate educational logic

---

## 6. Post-consolidation posture

Architecture Consolidation is **COMPLETE**. The Education Operating System is the canonical runtime.

Development focus: product excellence, governance, quality, documentation, engineering maturity, release readiness — not parallel educational architectures.

---

## 7. Related programmes

| Programme | Artefact |
|---|---|
| KSI Baseline & Version 1 Success Framework (P-001.1) | `knowledge/product/p001_1_ksi_baseline/` |
| Commercial Readiness First (CQ-001) | `knowledge/product/cq001_commercial_readiness/` |
| Explainability Standard (P-001.2) | `knowledge/product/p001_2_explainability_standard/` |
| Recommendation Quality Standard (P-001.3) | `knowledge/product/p001_3_recommendation_quality_standard/` |
| Version 1 Release Framework (P-002.1) | `knowledge/product/p002_1_version_1_release_framework/` |
| KSI Validation & Evidence Collection (EP-005.1) | `knowledge/product/ep005_1_ksi_validation_evidence/` |
| Educational Experience Validation (EP-005.2) | `knowledge/product/ep005_2_educational_experience_validation/` |
| MES End-to-End Delivery (EP-006.1) | `knowledge/product/ep006_1_mes_end_to_end_delivery/` |
| MES Delivery Implementation (EP-006.2) | `knowledge/product/ep006_2_mes_delivery_implementation/` |
| MES Perception Validation (EP-006.3) | `knowledge/product/ep006_3_mes_perception_validation/` |
| Readiness Experience Completion (EP-006.4) | `knowledge/product/ep006_4_readiness_experience_completion/` |
| Readiness Perception Validation (EP-006.5) | `knowledge/product/ep006_5_readiness_perception_validation/` |
| Engineering governance | `knowledge/ENGINEERING_STANDARDS.md` |
| Quality platform | `knowledge/QUALITY_MANUAL.md` |
| Product requirements | `knowledge/prd/` |
| Product analytics (design only) | `knowledge/product/analytics/PRODUCT_ANALYTICS_ARCHITECTURE.md` |
| Private beta prep | `knowledge/product/private_beta/README.md` |
| Founder Governance Model (GP-001) | `knowledge/product/gp001_founder_governance_model/` |
| Blind Review (research subsystem) | `knowledge/product/ep004_private_beta/reviewer_framework/` |
| Educational Validation Framework (Programme V) | `knowledge/educational_validation/` |
| Technical debt | `docs/TECHNICAL_DEBT_REGISTER.md` |
| Release management | `knowledge/RELEASE_PLAYBOOK.md` |
| V1 readiness | `knowledge/VERSION_1_READINESS.md` |
| Founder Governance Model (GP-001) | `knowledge/product/gp001_founder_governance_model/` |

---

**Status:** Active  
**Next review:** End of next major release
