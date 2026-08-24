# Product Decision Register

**Programme:** P-003.2 — Product Decision Register  
**Document:** Canonical Decision Register (full cards)  
**Date:** 2026-07-26  
**Status:** Complete — documentation only  
**Does not:** Amend runtime, services, UI, governance law, architecture, or release gates  

**Purpose:** Permanent Product Board reference for every major product, governance, architectural, educational, release, presentation, validation, and operational decision that continues to govern Version 1.

**Companions:** [`ACTIVE_DECISIONS.md`](ACTIVE_DECISIONS.md) · [`SUPERSEDED_DECISIONS.md`](SUPERSEDED_DECISIONS.md) · [`DECISION_TRACEABILITY.md`](DECISION_TRACEABILITY.md) · [`DECISION_LIFECYCLE.md`](DECISION_LIFECYCLE.md)

**Evidence standard:** Every decision cites existing artefacts. Unsupported decisions are not invented. Current board posture numbers freeze at 2026-07-26 evidence (P-003.1 dossier).

**How to use:** A Product Board member should be able to answer *why does Kwalitec behave this way?* by reading this register and the active index. Full programme history remains in programme folders and the Version 1 Release Dossier.

---

## Register conventions

| Field | Meaning |
|---|---|
| **Decision ID** | Stable `DR-NNN` identifier |
| **Category** | Architecture · Educational · Governance · Release · Runtime · Presentation · Validation · Operational |
| **Status** | `ACTIVE` (governs Version 1) · `SUPERSEDED` (see [`SUPERSEDED_DECISIONS.md`](SUPERSEDED_DECISIONS.md)) · `ACTIVE (posture)` (binding current board state; review when evidence changes) |
| **Supersedes** | Prior decision IDs or named historical postures, if any |
| **Future Review Trigger** | Condition that requires re-evaluation |

Indexes: [`ACTIVE_DECISIONS.md`](ACTIVE_DECISIONS.md) · Traceability: [`DECISION_TRACEABILITY.md`](DECISION_TRACEABILITY.md)

---

# Part A — Runtime educational authority

---

## DR-001 — Runtime A is the sole educational authority (production defaults)

| Field | Content |
|---|---|
| **Category** | Runtime · Architecture |
| **Status** | ACTIVE |
| **Decision Statement** | Under production defaults, Runtime A (legacy RecommendationService, PlanningService, ReadinessService) is the sole student-visible educational authority. Twin-gated consumer-chain paths may soak or dual-run but do not replace Runtime A as Version 1 student truth while Twin/Authority/Cutover flags remain OFF. |
| **Background** | EP-001/EP-002 built a Twin-gated Student Intelligence Surface. Students must not be exposed to a second educational brain during soak. |
| **Rationale** | One Education OS; fail-open legacy protects students; production defaults keep Twin/cutover OFF. |
| **Evidence** | `knowledge/architecture/ep002_9_programme_exit_certification/AUTHORITATIVE_ARCHITECTURE_BASELINE.md`; `knowledge/product/p003_1_version1_release_dossier/Architecture_Summary.md`; `Version_1_RELEASE_DOSSIER.md` §3 |
| **Programmes** | EP-002.9, EP-001.*, EP-002.*, P-003.1 |
| **Dependencies** | DR-009, DR-010, DR-015 |
| **Supersedes** | None (coexists with V2 Adaptive Decision Engine design law for non–Runtime-A paths) |
| **Risks** | Premature Twin cutover ON as production default without evidence; dual messaging if presentation invents authority |
| **Future Review Trigger** | Twin/cutover production-default ON with dual-run exit criteria met and G12 matrix published |

---

## DR-002 — RecommendationService owns recommendations

| Field | Content |
|---|---|
| **Category** | Runtime · Educational |
| **Status** | ACTIVE |
| **Decision Statement** | RecommendationService (Runtime A), with EP-001.4 Insight as communication owner on Twin path, owns ranking and student next-action guidance. It must not invent learner state, plan missions, or recalculate readiness. |
| **Background** | Recommendation ownership must be unambiguous so Home/Coach/Mission do not invent competing tips. |
| **Rationale** | Separates advice from planning and readiness evaluation; binds P-001.3 Decision Framework to one owner. |
| **Evidence** | EP-002.9 `AUTHORITATIVE_ARCHITECTURE_BASELINE.md` §4; `knowledge/architecture/ep001_5_architectural_integration_review/AUTHORITY_MATRIX.md`; EP-003.1 `COMPLETION_REPORT.md` |
| **Programmes** | EP-001.4, EP-001.5, EP-002.9, EP-003.1, P-001.3 |
| **Dependencies** | DR-001, DR-029, DR-050 |
| **Supersedes** | None |
| **Risks** | Presentation re-ranking; personalisation overriding ladder ranks 1–3 |
| **Future Review Trigger** | Change of recommendation ownership in authoritative architecture baseline |

---

## DR-003 — PlanningService owns planning

| Field | Content |
|---|---|
| **Category** | Runtime · Educational |
| **Status** | ACTIVE |
| **Decision Statement** | PlanningService owns today’s mission / daily plan and ORM mission persistence (`generate_today_mission`). Twin must not write missions; Insight must not invent plans; MissionOptimizer is not a second planning authority. |
| **Background** | Multiple planners historically risked conflicting “today” directives and durations. |
| **Rationale** | Single plan authority preserves curriculum-first Learning Mode and duration honesty. |
| **Evidence** | EP-002.9 baseline §4; EP-003.3 completion; `knowledge/architecture/PLANNING_SERVICE_QUALITY_CONTRACT.md`; EP-002.9 `OWNERSHIP_CERTIFICATION.md` |
| **Programmes** | EP-001.2, EP-002.7, EP-002.9, EP-003.3 |
| **Dependencies** | DR-001, DR-008, DR-017, DR-049 |
| **Supersedes** | Informal multi-planner heuristics |
| **Risks** | Cutover display proxying Twin plan while ORM remains legacy — must not become dual write |
| **Future Review Trigger** | Planning cutover ON as production default with ownership re-certification |

---

## DR-004 — ReadinessService owns readiness

| Field | Content |
|---|---|
| **Category** | Runtime · Educational |
| **Status** | ACTIVE |
| **Decision Statement** | ReadinessService owns readiness estimate, drivers, confidence honesty, and honest refusal. Collectors must use legacy getters safely; Intelligence must not invent readiness when Twin is OFF. Readiness is not a next-action engine. |
| **Background** | Readiness was at risk of becoming a composite marketing score or a second recommender. |
| **Rationale** | Preparedness judgement must stay evidence-bound and separable from recommendations (Educational Constitution). |
| **Evidence** | EP-002.9 baseline §2–4; EP-003.2 completion; EP-006.4 Home readiness experience; Educational Constitution Art IV |
| **Programmes** | EP-001.3, EP-002.6, EP-002.9, EP-003.2, EP-006.4, EGI-001 |
| **Dependencies** | DR-001, DR-018, DR-035 |
| **Supersedes** | None |
| **Risks** | “Exam Ready” theatre; soothing composites hiding sparse evidence |
| **Future Review Trigger** | Readiness cutover ON as production default; or Exam Ready marketing gate clearance |

---

## DR-005 — Presentation cannot generate educational reasoning

| Field | Content |
|---|---|
| **Category** | Presentation · Architecture |
| **Status** | ACTIVE |
| **Decision Statement** | Presentation (including `RuntimeAPresentationAdapter`, templates, Student Experience) delivers authored explanations and journey chrome. It must not invent evaluation, planning, readiness scores, or a third educational narrator. AI may enrich wording of decided explanations only. |
| **Background** | EP-006 found MES authored in services was lost before templates; the fix was pass-through, not new reasoning. |
| **Rationale** | Prevents dual messaging and false confidence; upholds P-001.2 and Architecture Constitution. |
| **Evidence** | EP-002.8 presentation consolidation; EP-006.1/006.2 MES specs; P-001.2 Explainability Standard §2 P9; `docs/ARCHITECTURE_CONSTITUTION.md` Art V–VI; P-003.1 Architecture Summary |
| **Programmes** | EP-002.8, EP-002.9, EP-006.1, EP-006.2, P-001.2, APP-003 |
| **Dependencies** | DR-002, DR-003, DR-004, DR-019 |
| **Supersedes** | Pre-EP-002.8 route-local presentation narration as peer authority |
| **Risks** | Experience `/student` ExplanationService residual parallel stack (deferred TD) |
| **Future Review Trigger** | Experience narrator consolidation under SOLE_RUNTIME completes with ownership re-certification |

---

## DR-006 — Personalisation is tertiary only

| Field | Content |
|---|---|
| **Category** | Educational · Runtime |
| **Status** | ACTIVE |
| **Decision Statement** | Personal Learning Profile supplies behavioural attributes only (no educational authority APIs). Recommendation personalisation may reorder only within the same Decision Framework ladder rank/priority band; ranks 1–3 are immutable. Planning personalisation must not change educational slot order or invent missions. Production defaults keep personalisation flags OFF. |
| **Background** | EP-004.* implemented bounded personalisation without transferring educational authority to profile. |
| **Rationale** | Curriculum-first Decision Framework remains primary; personalisation is tie-break, not override. |
| **Evidence** | EP-004.1/004.2/004.3 constitutional verifications; P-001.3 Decision Framework §5; PERSONALISATION_RULES.md |
| **Programmes** | EP-004.1, EP-004.2, EP-004.3, P-001.3 |
| **Dependencies** | DR-002, DR-003, DR-029, DR-039 |
| **Supersedes** | None |
| **Risks** | Marketing personalisation while flags OFF; claiming K4 lift without ON defaults + cohort evidence |
| **Future Review Trigger** | Personalisation flags ON in W-PROD with G12 matrix and effectiveness evidence |

---

## DR-007 — Canonical Home

| Field | Content |
|---|---|
| **Category** | Presentation · Runtime |
| **Status** | ACTIVE |
| **Decision Statement** | When `KWALITEC_V2_SOLE_RUNTIME` is ON, Student Home (`student.home`) is the single authoritative home. Login, onboarding, calibration, plan activation, completion, and errors route via canonical home helpers. Dual-home (Dashboard vs Student Home) is retained only when sole runtime is OFF (soak/Alpha). |
| **Background** | EP-005.2 REM-02: dual-home friction blocked student value (K1/K5). |
| **Rationale** | Students need one coherent “where do I start tonight?” surface. |
| **Evidence** | EP-007.1 `STUDENT_JOURNEY_CONSOLIDATION.md`; EP-007.2 Tier B K1 revalidation; P-003.1 dossier §4 |
| **Programmes** | EP-007.1, EP-007.2, EP-005.2 (REM-02), V2-023 |
| **Dependencies** | DR-020 |
| **Supersedes** | Dual-home as W-PROD canonical journey when SOLE_RUNTIME ON (see SUPERSEDED) |
| **Risks** | Alpha dual-run residual outside W-PROD claim window |
| **Future Review Trigger** | SOLE_RUNTIME OFF becomes production default; or dual-home intentionally restored |

---

## DR-008 — Single planned session duration

| Field | Content |
|---|---|
| **Category** | Presentation · Runtime |
| **Status** | ACTIVE |
| **Decision Statement** | One planned session duration fact is resolved via shared resolver (`resolve_planned_session_minutes()`), preferring `preferred_session_minutes`, across Home, Mission, bridges, and StudySessionService. Conflicting weekday/weekend vs preferred-minutes clocks must not appear on the same day on W-PROD sole-runtime surfaces. |
| **Background** | EP-005.2 REM-03: conflicting duration clocks eroded trust. |
| **Rationale** | Duration honesty is part of planning quality (G5) and journey coherence (K1/K5). |
| **Evidence** | EP-007.1 consolidation; EP-003.3 planning quality contract; EP-007.2 perception |
| **Programmes** | EP-007.1, EP-003.3, EP-005.2 (REM-03) |
| **Dependencies** | DR-003, DR-007 |
| **Supersedes** | Competing duration clocks on W-PROD sole-runtime path |
| **Risks** | Surfaces bypassing shared resolver |
| **Future Review Trigger** | Duration resolver ownership or preference rule change |

---

## DR-009 — Twin and cutover flags default OFF; fail-open to legacy

| Field | Content |
|---|---|
| **Category** | Runtime · Operational |
| **Status** | ACTIVE |
| **Decision Statement** | Production defaults keep Digital Twin, Authority, and HTTP cutover flags OFF. Student-visible payloads fail-open to legacy Runtime A. Surface rollback = cutover flag OFF + restart; global Twin kill = Twin flag OFF. |
| **Background** | EP-002 cutovers are soak-ready but not Version 1 production-default truth. |
| **Rationale** | Protect students during dual-run; enable instant rollback without schema rollback. |
| **Evidence** | EP-002.9 baseline §3, §6, §7; P-003.1 Architecture Summary §9–10 |
| **Programmes** | EP-002.5–EP-002.9 |
| **Dependencies** | DR-001, DR-010 |
| **Supersedes** | None |
| **Risks** | Marketing Twin capabilities while OFF; incomplete G12 matrix |
| **Future Review Trigger** | Board-approved production-default ON for any Twin/cutover flag |

---

## DR-010 — Production hard-gate blocks HTTP cutovers

| Field | Content |
|---|---|
| **Category** | Operational · Release |
| **Status** | ACTIVE |
| **Decision Statement** | HTTP cutover flags (`STUDY_INSIGHTS`, `READINESS_INTELLIGENCE`, `DAILY_PLAN`) are ineligible when environment is `production`/`prod`, regardless of flag values. |
| **Background** | Hard-gate prevents accidental student exposure to cutover surfaces in production. |
| **Rationale** | Defence in depth beyond default-OFF flags. |
| **Evidence** | EP-002.9 baseline §3; EP-002.5–002.7 cutover programmes |
| **Programmes** | EP-002.5, EP-002.6, EP-002.7, EP-002.9 |
| **Dependencies** | DR-009 |
| **Supersedes** | Soft reliance on flags alone |
| **Risks** | Environment misclassification bypassing hard-gate |
| **Future Review Trigger** | Explicit programme to lift production hard-gate with evidence package |

---

## DR-011 — Curriculum V1 and V2 must both remain loadable

| Field | Content |
|---|---|
| **Category** | Architecture · Educational |
| **Status** | ACTIVE |
| **Decision Statement** | Flat (V1) and hierarchical (V2) syllabus formats remain loadable and traversable indefinitely until an explicit migration milestone removes V1. Feature work must not silently break flat curricula. |
| **Background** | Product serves multiple curriculum shapes; V1 loaders must not be deleted casually. |
| **Rationale** | Curriculum-first product; continuity for existing cohorts. |
| **Evidence** | `knowledge/architecture/ADR-003-curriculum-v1-v2.md`; `ARCHITECTURE.md`; `PROJECT_CONTEXT.md` |
| **Programmes** | ADR-003, curriculum milestones |
| **Dependencies** | DR-012 |
| **Supersedes** | None |
| **Risks** | V2-only assumptions in planning/presentation |
| **Future Review Trigger** | Explicit curriculum V1 retirement milestone with migration evidence |

---

## DR-012 — Canonical topic traversal via CurriculumService

| Field | Content |
|---|---|
| **Category** | Architecture |
| **Status** | ACTIVE |
| **Decision Statement** | All product feature ordering uses `CurriculumService` helpers (and engine `load_auto()` / `get_topics_flat()`). Reimplementing V1/V2 ordering in planning, missions, readiness, routes, or presentation is forbidden. |
| **Background** | Duplicated ordering caused syllabus drift. |
| **Rationale** | Single traversal authority preserves curriculum primacy. |
| **Evidence** | ADR-004; `ARCHITECTURE.md`; Educational Constitution Art II §2 |
| **Programmes** | ADR-004, EGI-001 |
| **Dependencies** | DR-011 |
| **Supersedes** | Ad-hoc ordering in feature services |
| **Risks** | Bridge/cutover code copying order logic |
| **Future Review Trigger** | CurriculumService API redesign with migration ADR |

---

## DR-013 — Deterministic educational cores; no black-box LLM in core path

| Field | Content |
|---|---|
| **Category** | Educational · Runtime |
| **Status** | ACTIVE |
| **Decision Statement** | Planning, readiness, and recommendations must be reproducible from the same inputs. External LLM APIs must not own educational truth or sit in the core recommendation/planning/readiness path. AI may enrich presentation wording of decided explanations only. |
| **Background** | Vision and Educational Constitution require explainable, evidence-based AI. |
| **Rationale** | Determinism enables audit, dual-run comparison, and student trust. |
| **Evidence** | Educational Constitution Art II §3; `PROJECT_CONTEXT.md`; Architecture Constitution Art II; P-001.2 P9 |
| **Programmes** | EGI-001, APP-003, P-001.2 |
| **Dependencies** | DR-005 |
| **Supersedes** | None |
| **Risks** | Covert LLM introduction into ranking/scoring |
| **Future Review Trigger** | Explicit programme authorizing LLM in a bounded, explainable role with constitutional amendment if required |

---

## DR-014 — Service layer owns business logic; thin blueprints

| Field | Content |
|---|---|
| **Category** | Architecture |
| **Status** | ACTIVE |
| **Decision Statement** | Domain rules live in `app/services/` (and documented application adapters). Blueprints authenticate, validate, call services, and render. Routes must not contain planning/mastery/recommendation math. Services must not depend on `flask.request` / session globals. |
| **Background** | Layering invariant of the Flask Runtime A application. |
| **Rationale** | Testability, reuse, and prevention of god routes. |
| **Evidence** | ADR-001, ADR-002; `ARCHITECTURE.md`; `.cursor/rules/01-architecture.mdc` |
| **Programmes** | ADR-001, ADR-002 |
| **Dependencies** | None |
| **Supersedes** | God-route patterns |
| **Risks** | Application-layer services reinventing educational authority outside Runtime A contracts |
| **Future Review Trigger** | Architecture Constitution amendment of layering |

---

## DR-015 — Twin and Insight do not write educational state

| Field | Content |
|---|---|
| **Category** | Runtime · Architecture |
| **Status** | ACTIVE |
| **Decision Statement** | Runtime A SQL + services own educational fact writes. Twin packages, Insight, and bridges must not write educational state. Twin is a provisional evidence-driven read model, not the student. |
| **Background** | Twin Constitution and EP-002 authority matrix. |
| **Rationale** | Prevent silent dual writes and Twin-as-student confusion. |
| **Evidence** | EP-002.9 baseline §4; Digital Twin Constitution; Educational Constitution Art III–IV |
| **Programmes** | EP-001.5, EP-002.9, Twin Constitution, EGI-001 |
| **Dependencies** | DR-001, DR-016 |
| **Supersedes** | None |
| **Risks** | Bridge adapters writing missions/progress |
| **Future Review Trigger** | Certified write-path redesign with dual-run exit criteria |

---

## DR-016 — Twin stack quarantine

| Field | Content |
|---|---|
| **Category** | Architecture · Runtime |
| **Status** | ACTIVE |
| **Decision Statement** | Only MS-004 + EP-001.1 Foundation is authoritative for Runtime A Twin/EP-001–EP-002 paths. Epic Twin, V2 `student_twin`, and EOS Twin remain reference/isolated. Do not introduce a fourth Twin stack. Authority ON is not implied by Twin ON. |
| **Background** | Multiple historical Twin stacks risked parallel brains. |
| **Rationale** | Quarantine preserves one Runtime A Twin read-model lineage. |
| **Evidence** | `knowledge/architecture/TWIN_STACK_QUARANTINE.md`; EP-002.9 baseline §5 |
| **Programmes** | EP-002.1, EP-002.9 |
| **Dependencies** | DR-015 |
| **Supersedes** | Ad-hoc use of non-Foundation Twin stacks for Runtime A |
| **Risks** | Accidental cross-import of V2/EOS Twin into Runtime A |
| **Future Review Trigger** | Explicit Twin-stack consolidation programme |

---

## DR-017 — Learning Mode is Version 1 mission authority

| Field | Content |
|---|---|
| **Category** | Educational |
| **Status** | ACTIVE |
| **Decision Statement** | In Version 1, Today’s Mission follows Current Learning Topic in official syllabus order by default. Disclosed Learning Mode consolidation checkpoints may pause forward progress at exam-proximity cadence when weak covered topics exist (Founder-authorized deliberate amendment, 2026-08-24 architecture session — motivated by activating real mastery data to emulate tutor-like consolidation). Advisory review/weak-topic signals may appear but must not silently or off-cadence replace Learning Mode mission authority. Broader Adaptive Mode interruption remains deferred. Distinct from Revision Mode post-syllabus rotation. |
| **Background** | Educational Constitution Art VI. Amended 2026-08-24 to authorise disclosed Learning Mode consolidation checkpoints; not a silent/undocumented behaviour change. |
| **Rationale** | Curriculum primacy over opportunistic adaptation in V1, with honest tutor-like consolidation when mastery evidence warrants it at a disclosed cadence. |
| **Evidence** | `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` Art VI §§1–3; `knowledge/educational/EDUCATIONAL_LOGIC_REGISTRY.md` EL-002 / EL-003 / EL-009 |
| **Programmes** | EGI-001 |
| **Dependencies** | DR-003, DR-012 |
| **Supersedes** | Prior DR-017 wording that deferred all weak-topic mission interruption without a disclosed-checkpoint exception |
| **Risks** | Personalisation or recommendations silently rewriting mission topic; conflating Learning Mode checkpoints with Revision Mode |
| **Future Review Trigger** | Broader constitutional Adaptive Mode activation beyond Learning Mode consolidation checkpoints |

---

## DR-018 — Readiness ≠ Next Action; Recommendation ≠ Evidence

| Field | Content |
|---|---|
| **Category** | Educational |
| **Status** | ACTIVE |
| **Decision Statement** | Readiness is a preparedness judgement, not a next-action engine. Recommendations are advice, not observational evidence. Surfaces must preserve this integrity split. |
| **Background** | Constitutional integrity rules prevent category collapse. |
| **Rationale** | Students and validators must distinguish preparedness from advice and evidence. |
| **Evidence** | Educational Constitution Art IV; Art VIII rules 7–8 |
| **Programmes** | EGI-001 |
| **Dependencies** | DR-002, DR-004 |
| **Supersedes** | None |
| **Risks** | UI copy collapsing readiness into “do this next” without recommendation ownership |
| **Future Review Trigger** | Educational Constitution amendment |

---

## DR-019 — MES authored by services; presentation pass-through

| Field | Content |
|---|---|
| **Category** | Presentation · Validation |
| **Status** | ACTIVE |
| **Decision Statement** | Mandatory Explanation Schema (MES) fields are authored by Recommendation/Planning/Readiness services. Presentation maps authored fields 1:1 when schema-complete; layout/terminology translation is allowed; inventing why/evidence/confidence/next is forbidden. Re-narration is fallback only for incomplete/cold-start payloads. |
| **Background** | EP-006.1 audited field loss; EP-006.2 delivered pass-through; EP-006.3 cleared K8 floor (70). |
| **Rationale** | Explainability requires visible *why + next* without a second narrator. |
| **Evidence** | EP-006.1 MES Delivery Specification; EP-006.2 implementation + Explainability Pass; EP-006.3 `G1_5_STATUS.md`; P-001.2 |
| **Programmes** | EP-006.1, EP-006.2, EP-006.3, P-001.2 |
| **Dependencies** | DR-005, DR-028 |
| **Supersedes** | Silent MES drop before templates |
| **Risks** | Future template changes reintroducing field loss |
| **Future Review Trigger** | MES schema version change; K8 revalidation failure |

---

## DR-020 — Sole runtime unifies chrome, not educational truth

| Field | Content |
|---|---|
| **Category** | Architecture · Presentation |
| **Status** | ACTIVE |
| **Decision Statement** | `KWALITEC_V2_SOLE_RUNTIME` unifies navigation and templates (`/student/*`, `/session/*`). It does not replace Runtime A service authority or unify educational truth by itself. Bridges remain required for Home to reflect real curriculum/plan state. |
| **Background** | V2-023 sole runtime vs EP-002 educational authority frequently confused. |
| **Rationale** | Prevent treating chrome cutover as educational cutover. |
| **Evidence** | `ARCHITECTURE.md`; Educational Runtime Bridge docs; EP-007.1; EP-002.9 |
| **Programmes** | V2-023, EP-007.1, EP-002.* |
| **Dependencies** | DR-001, DR-007 |
| **Supersedes** | “Sole runtime = Twin educational cutover” misconception |
| **Risks** | Claiming educational consolidation from chrome-only flags |
| **Future Review Trigger** | Programme that intentionally binds chrome and educational cutover together |

---

## DR-049 — MissionOptimizer is quarantined

| Field | Content |
|---|---|
| **Category** | Runtime · Architecture |
| **Status** | ACTIVE |
| **Decision Statement** | MissionOptimizer is soft-deprecated/quarantined. Planning authority remains with PlanningService. Cutover display may proxy Twin plan but ORM persistence remains legacy Runtime A. |
| **Background** | Historical optimizer risked becoming a second planner. |
| **Rationale** | One planning authority (DR-003). |
| **Evidence** | EP-002.9 baseline §4, §8; OWNERSHIP_CERTIFICATION; MissionOptimizer decision notes |
| **Programmes** | EP-002.*, EP-001.2 |
| **Dependencies** | DR-003 |
| **Supersedes** | MissionOptimizer as peer planning authority |
| **Risks** | Re-enabling optimizer writes without ownership review |
| **Future Review Trigger** | Explicit retirement or re-authorization programme |

---

## DR-050 — Single primary recommendation CTA

| Field | Content |
|---|---|
| **Category** | Presentation · Educational |
| **Status** | ACTIVE |
| **Decision Statement** | Dashboard / mission-start / Home primary surfaces show exactly one primary recommendation. Secondary tips must not override “today.” Hard gates (lawful warrant, plan coherence, explainability readiness, proportionality, honest refusal) apply before ranking. |
| **Background** | P-001.3 Decision Framework; EP-003.1 Runtime A contract. |
| **Rationale** | Students need one highest-value next action (Vision daily expression). |
| **Evidence** | `RECOMMENDATION_DECISION_FRAMEWORK.md` §§2, 6; EP-003.1 completion |
| **Programmes** | P-001.3, EP-003.1 |
| **Dependencies** | DR-002, DR-029 |
| **Supersedes** | Multi-primary competing CTAs on same surface |
| **Risks** | UI stacking multiple “do this now” equal-weight CTAs |
| **Future Review Trigger** | Decision Framework amendment of primary CTA rule |

---

# Part B — Governance, validation, and release

---

## DR-021 — Educational claims require educational evidence

| Field | Content |
|---|---|
| **Category** | Validation · Governance |
| **Status** | ACTIVE |
| **Decision Statement** | Claims that Kwalitec improves learning outcomes, recommendation effectiveness, or exam pass rates require educational evidence (cohort KPIs, scorecards, interviews) — not structural completeness, schema Pass, or Tier B perception alone. |
| **Background** | EP-005.1 and EP-007.3 rejected substituting engineering completeness for effectiveness. |
| **Rationale** | Honesty protects students and Final Test; Vision north star remains unproven until measured. |
| **Evidence** | EP-005.1 `VALIDATED_KSI_REPORT.md`; EP-007.3 `G1_9_STATUS.md`; EP-003 `GO_NO_GO_REPORT.md`; Vision 2030 |
| **Programmes** | EP-005.1, EP-007.3, EP-003, P-001.1 |
| **Dependencies** | DR-022, DR-033 |
| **Supersedes** | “Ship quality contracts → claim effectiveness” |
| **Risks** | Marketing language drift |
| **Future Review Trigger** | Educational effectiveness GO under EP-003 Q1–Q5 with C5–C6 floors |

---

## DR-022 — Version 1 release requires external effectiveness evidence (G1.9)

| Field | Content |
|---|---|
| **Category** | Release · Validation |
| **Status** | ACTIVE |
| **Decision Statement** | Gate G1.9 requires that educational effectiveness Go/No-Go is not NO-GO for the claim window. External cohort evidence is required (current external N = 0). Tier B N=9 perception does not clear G1.9. |
| **Background** | P-001.1 V1-K5 / P-002.1 G1.9; EP-007.3 reaffirmed FAIL. |
| **Rationale** | Production-ready declaration without effectiveness evidence overclaims student value. |
| **Evidence** | P-002.1 Release Framework G1.9; EP-007.3 `G1_9_STATUS.md`; P-003.1 dossier §7, §11 |
| **Programmes** | P-001.1, P-002.1, EP-003, EP-004, EP-007.3, P-003.1 |
| **Dependencies** | DR-021, DR-030, DR-033, DR-040 |
| **Supersedes** | None |
| **Risks** | Pressure to waive G1.9 without written HOLD path |
| **Future Review Trigger** | Effectiveness verdict update after Stage 1 ops + M1–M9 + interviews |

---

## DR-023 — Document authority hierarchy

| Field | Content |
|---|---|
| **Category** | Governance |
| **Status** | ACTIVE |
| **Decision Statement** | Authority flows downward: Vision 2030 → Blueprint / KSI / Explainability / Recommendation / Release Framework / Release Dossier → Educational Constitution → EVF → Architecture → ADRs → Engineering Standards → PRDs → Release playbooks. Lower documents must not contradict higher ones; conflicts require amending the higher authority first. |
| **Background** | Post-consolidation Product Governance (July 2026). |
| **Rationale** | Prevents local programmes inventing conflicting law. |
| **Evidence** | `knowledge/GOVERNANCE.md` §1 |
| **Programmes** | GOVERNANCE |
| **Dependencies** | None |
| **Supersedes** | Informal document peer equality |
| **Risks** | Shadow constitutions in programme folders |
| **Future Review Trigger** | Governance hierarchy amendment |

---

## DR-024 — Educational Constitution is highest educational law

| Field | Content |
|---|---|
| **Category** | Educational · Governance |
| **Status** | ACTIVE |
| **Decision Statement** | `KWALITEC_EDUCATIONAL_CONSTITUTION.md` (EGI-001) is the highest educational authority. Implementation never governs the Constitution. Amendments require Article X process. EVF owns whether quality is sufficient to release; it does not replace educational law. |
| **Background** | Educational Governance Initiative. |
| **Rationale** | Lawful educational meaning must outrank convenience. |
| **Evidence** | Educational Constitution; `GOVERNANCE.md` educational authority split |
| **Programmes** | EGI-001, GOVERNANCE |
| **Dependencies** | DR-023 |
| **Supersedes** | None |
| **Risks** | Feature programmes bypassing constitutional verification |
| **Future Review Trigger** | Article X amendment |

---

## DR-025 — KSI ≥ 80 for Version 1 product-success claims

| Field | Content |
|---|---|
| **Category** | Validation · Release |
| **Status** | ACTIVE |
| **Decision Statement** | Version 1 product-success claims require validated Kwalitec Student Index ≥ 80 (weighted K1–K8). Additional floors: no category below 50 (G1.4); K8 ≥ 70 (G1.5). KSI does not replace Vision 2030’s north star. |
| **Background** | P-001.1 Product Success Framework. |
| **Rationale** | Objective usefulness bar for Version 1 claims. |
| **Evidence** | `PRODUCT_SUCCESS_FRAMEWORK.md` §§2, 6, 7; P-002.1 G1; P-003.1 KSI Evolution |
| **Programmes** | P-001.1, P-002.1 |
| **Dependencies** | DR-026, DR-046 |
| **Supersedes** | Informal “good enough” usefulness claims |
| **Risks** | Treating estimated ΔKSI as validated (forbidden by DR-026) |
| **Future Review Trigger** | PSF amendment of Version 1 bar |

---

## DR-026 — Estimated ΔKSI is not validated KSI

| Field | Content |
|---|---|
| **Category** | Validation · Governance |
| **Status** | ACTIVE |
| **Decision Statement** | Programme estimated ΔKSI must not satisfy Gate G1 / V1-K1. Only evidence-bound validated KSI assessments (≤ 90 days for declaration) count. Do not sum overlapping programme estimates. Docs/infra programmes record ΔKSI = 0. |
| **Background** | EP-005.1 proved naive estimate stacks (~+12) are not claimable. |
| **Rationale** | Prefer-lower honesty; prevent claim inflation. |
| **Evidence** | PSF §5.6, §7.1; EP-005.1 `VALIDATED_KSI_REPORT.md`; `GOVERNANCE.md` |
| **Programmes** | P-001.1, EP-005.1 |
| **Dependencies** | DR-025, DR-027 |
| **Supersedes** | Naive ΔKSI stack as G1 input (see SUPERSEDED) |
| **Risks** | Roadmap slides treating estimates as validated |
| **Future Review Trigger** | PSF methodology amendment |

---

## DR-027 — Prefer-lower scoring discipline

| Field | Content |
|---|---|
| **Category** | Validation |
| **Status** | ACTIVE |
| **Decision Statement** | When evidence conflicts, assign the lower category score. Honesty before optimism. |
| **Background** | PSF scoring rules; applied in Tier B revalidations (e.g. K8 held at floor 70). |
| **Rationale** | Protects students from overclaimed usefulness. |
| **Evidence** | PSF §5.1; EP-006.3 perception methodology; P-003.1 lessons |
| **Programmes** | P-001.1, EP-006.3, EP-005.1 |
| **Dependencies** | DR-026 |
| **Supersedes** | Optimistic averaging of conflicting evidence |
| **Risks** | Board pressure to round up |
| **Future Review Trigger** | PSF scoring-rule amendment |

---

## DR-028 — Explainability mandatory; silent steering forbidden

| Field | Content |
|---|---|
| **Category** | Governance · Presentation |
| **Status** | ACTIVE |
| **Decision Statement** | If guidance cannot be explained, it must not be shown on student surfaces. Recommendation, Planning, and Readiness production-default surfaces must attach schema-complete explanations. K8 claims require Explainability Review Checklist Pass (or waiver). |
| **Background** | P-001.2 Explainability Standard; V1-K3 / G1.5 / G3. |
| **Rationale** | Trust and Final Test require visible reasons. |
| **Evidence** | `EXPLAINABILITY_STANDARD.md`; `GOVERNANCE.md` §4.2; EP-003.1–.3 reviews; EP-006.3 G1.5 PASS |
| **Programmes** | P-001.2, EP-003.*, EP-006.* |
| **Dependencies** | DR-019, DR-005 |
| **Supersedes** | Silent tips without schema |
| **Risks** | Incomplete declaration spot-check pack for full G3 |
| **Future Review Trigger** | Explainability Standard version change; K8 < 70 on revalidation |

---

## DR-029 — Recommendation Quality Standard and Decision Framework

| Field | Content |
|---|---|
| **Category** | Governance · Educational |
| **Status** | ACTIVE |
| **Decision Statement** | Student-facing recommendations follow P-001.3 quality principles and the Decision Framework priority ladder (hard gates before ranking; motivation last). Complements explainability (selection vs speech). K2 claims require Recommendation Review Checklist Pass (or waiver). |
| **Background** | P-001.3 law; EP-003.1 Runtime A contract. |
| **Rationale** | One lawful selection ladder across Runtime A. |
| **Evidence** | Recommendation Quality Standard; Decision Framework; `GOVERNANCE.md` §4.3; EP-003.1 |
| **Programmes** | P-001.3, EP-003.1 |
| **Dependencies** | DR-002, DR-006, DR-050 |
| **Supersedes** | Ad-hoc tip ordering |
| **Risks** | Scorecard instrumentation gaps for full G4 declaration |
| **Future Review Trigger** | Decision Framework ladder amendment |

---

## DR-030 — Version 1 production-ready requires gates G1–G12

| Field | Content |
|---|---|
| **Category** | Release · Governance |
| **Status** | ACTIVE |
| **Decision Statement** | Declaring Version 1 production-ready requires P-002.1 gates G1–G12 with evidence package and signed go/no-go. Operational GA alone, architecture cutover alone, tracker greens alone, or estimated ΔKSI alone are insufficient. The Release Dossier (P-003.1) synthesises evidence but does not amend gates or declare Version 1. |
| **Background** | P-002.1 Release Framework; clarified in GOVERNANCE and P-003.1. |
| **Rationale** | Objective declaration authority. |
| **Evidence** | `VERSION_1_RELEASE_FRAMEWORK.md`; `VERSION_1_GO_NO_GO_GUIDE.md`; `GOVERNANCE.md` §4.4; P-003.1 |
| **Programmes** | P-002.1, P-003.1, GOVERNANCE |
| **Dependencies** | DR-022, DR-025, DR-031, DR-041 |
| **Supersedes** | “Architecture COMPLETE = production-ready” |
| **Risks** | Incomplete evidence package pressure |
| **Future Review Trigger** | P-002.1 framework amendment |

---

## DR-031 — Hard-gate FAIL yields overall NO-GO

| Field | Content |
|---|---|
| **Category** | Release |
| **Status** | ACTIVE |
| **Decision Statement** | Any hard-gate FAIL (including validated KSI < 80, category < 50, K8 < 70, EVF REJECTED, honesty incident) yields overall **NO-GO** for Version 1 production-ready declaration. GO WITH CONDITIONS must not claim unconditional readiness. |
| **Background** | P-002.1 go/no-go guide. |
| **Rationale** | Prevent soft-launch of failed gates. |
| **Evidence** | `VERSION_1_GO_NO_GO_GUIDE.md` §§2–4 |
| **Programmes** | P-002.1 |
| **Dependencies** | DR-030 |
| **Supersedes** | Informal conditional launch without HOLD language |
| **Risks** | Relabeling FAIL as HOLD without criteria |
| **Future Review Trigger** | Go/No-Go guide amendment |

---

## DR-032 — Three separable verdicts

| Field | Content |
|---|---|
| **Category** | Release · Governance |
| **Status** | ACTIVE |
| **Decision Statement** | Private-beta execution GO WITH CONDITIONS, educational effectiveness NO-GO/PENDING EVIDENCE, and Version 1 production-ready NO-GO are intentionally separable. One may continue Stage 0 beta without claiming effectiveness or production-ready status. |
| **Background** | EP-004 sign-off vs EP-003/007.3 vs P-002.1/P-003.1. |
| **Rationale** | Allows continued learning under claim freezes. |
| **Evidence** | EP-004 `GO_NO_GO_DECISION.md`; EP-003 `GO_NO_GO_REPORT.md`; P-003.1 §11; P-002.1 §3.2 |
| **Programmes** | EP-004, EP-003, EP-007.3, P-002.1, P-003.1 |
| **Dependencies** | DR-040, DR-041, DR-022 |
| **Supersedes** | Collapsing all GO/NO-GO into one binary |
| **Risks** | Stakeholders confusing beta GO with V1 declaration |
| **Future Review Trigger** | Any of the three verdicts changes |

---

## DR-033 — Perception is not effectiveness

| Field | Content |
|---|---|
| **Category** | Validation |
| **Status** | ACTIVE |
| **Decision Statement** | Tier B perception validation (N=9 packs) may revalidate KSI category scores but does not satisfy educational effectiveness GO or Gate G1.9. |
| **Background** | EP-006.3/006.5/007.2 moved KSI 59→62; EP-007.3 correctly refused substitution. |
| **Rationale** | Perceived unpackability ≠ measured learning improvement. |
| **Evidence** | EP-007.3 `G1_9_STATUS.md`; P-003.1 lessons learned |
| **Programmes** | EP-006.3, EP-006.5, EP-007.2, EP-007.3 |
| **Dependencies** | DR-021, DR-022 |
| **Supersedes** | “Tier B clears effectiveness” |
| **Risks** | Using perception wins in effectiveness marketing |
| **Future Review Trigger** | Methodology that formally equates perception to a defined effectiveness slice (would require law change) |

---

## DR-034 — Invite-only; no public registration

| Field | Content |
|---|---|
| **Category** | Operational · Governance |
| **Status** | ACTIVE |
| **Decision Statement** | Public self-service registration is disabled. Accounts are invite-only / admin-provisioned. Public marketing launch is forbidden while private-beta and V1 production-ready constraints apply. |
| **Background** | Security posture + EP-003/004 private beta protocol. |
| **Rationale** | Controlled cohort; privacy/support readiness incomplete for public launch. |
| **Evidence** | `PROJECT_CONTEXT.md`; EP-003 Private Beta Protocol; EP-004 GO_NO_GO; P-003.1 risks R10 |
| **Programmes** | EP-003, EP-004, security baseline |
| **Dependencies** | DR-040, DR-041 |
| **Supersedes** | Public registration |
| **Risks** | Accidental exposure of registration routes |
| **Future Review Trigger** | Explicit public-launch programme after V1 declaration path and privacy readiness |

---

## DR-035 — Exam Ready marketing ban

| Field | Content |
|---|---|
| **Category** | Governance · Educational |
| **Status** | ACTIVE |
| **Decision Statement** | No “Exam Ready” marketing without readiness gates (G6.3 / Never-Build alignment). Readiness honesty path (drivers, confidence, refusal) must not be replaced by soothing composites. |
| **Background** | Vision Never-Build; P-002.1 G6.3; EP-004 forbidden claims. |
| **Rationale** | False readiness harms students more than silence. |
| **Evidence** | P-002.1 Release Framework; Vision 2030 Never-Build; EP-004 GO_NO_GO; EP-003.2/006.4 |
| **Programmes** | P-002.1, EP-004, EP-003.2, EP-006.4, Vision |
| **Dependencies** | DR-004, DR-018 |
| **Supersedes** | Exam Ready theatre copy |
| **Risks** | Sales language drift |
| **Future Review Trigger** | Readiness gates explicitly cleared for marketing claim class |

---

## DR-036 — Recommendation-effectiveness marketing freeze

| Field | Content |
|---|---|
| **Category** | Governance |
| **Status** | ACTIVE |
| **Decision Statement** | Recommendation-effectiveness marketing remains frozen unless EP-001 O8 / approved PRD evidence lifts the freeze (G4.5 / EP-003 G9). |
| **Background** | EP-001 product validation freeze rules retained through EP-003/004. |
| **Rationale** | Effectiveness unproven (N_external = 0). |
| **Evidence** | P-002.1 G4.5; EP-003 GO_NO_GO G9; EP-004 forbidden claims |
| **Programmes** | EP-001, EP-003, EP-004, P-002.1 |
| **Dependencies** | DR-021, DR-022 |
| **Supersedes** | Effectiveness marketing without evidence |
| **Risks** | Soft claims in Coach copy |
| **Future Review Trigger** | Approved evidence package lifts freeze |

---

## DR-037 — Student Impact Assessment mandate

| Field | Content |
|---|---|
| **Category** | Governance |
| **Status** | ACTIVE |
| **Decision Statement** | Every EP/P programme completion must include Student Impact Assessment (template or equivalent), estimated ΔKSI (or 0 with rationale), evidence collected, and lessons learned for student value. Material programmes affecting intelligence/recommendations must complete explainability/recommendation reviews when in scope. |
| **Background** | P-001.1 + GOVERNANCE §4 + reporting rule 07. |
| **Rationale** | Forces student-value discipline even for docs programmes. |
| **Evidence** | `STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`; `GOVERNANCE.md` §4; `.cursor/rules/07-reporting.mdc` |
| **Programmes** | P-001.1, GOVERNANCE |
| **Dependencies** | DR-026 |
| **Supersedes** | Completions without student-value sections |
| **Risks** | Template theatre without honest evidence |
| **Future Review Trigger** | Governance §4 amendment |

---

## DR-038 — Learning feedback is record-only; flag OFF in W-PROD

| Field | Content |
|---|---|
| **Category** | Runtime · Operational |
| **Status** | ACTIVE |
| **Decision Statement** | EP-003.4 learning feedback records observed behavioural evidence events only — no mastery/readiness/recommendation-quality inference loop. Production default flag OFF; no validated K4/K6 lift while OFF. |
| **Background** | Closed-loop optimisation deferred for honesty and soak. |
| **Rationale** | Evidence capture without silent educational mutation. |
| **Evidence** | EP-003.4 completion + constitutional verification; P-003.1 dossier |
| **Programmes** | EP-003.4 |
| **Dependencies** | DR-015, DR-039 |
| **Supersedes** | None |
| **Risks** | Marketing feedback loop as live adaptation |
| **Future Review Trigger** | Flag ON with constitutional verification and cohort evidence |

---

## DR-039 — Personalisation and profile flags OFF in W-PROD

| Field | Content |
|---|---|
| **Category** | Operational · Runtime |
| **Status** | ACTIVE |
| **Decision Statement** | Personal Learning Profile and recommendation/planning personalisation capabilities are complete but unsupported in W-PROD while flags OFF. Claim language and KSI credit must exclude OFF capabilities. Fail-open to EP-003 baselines when profile missing or flag OFF. |
| **Background** | EP-004.*; EP-005.1 rejected gated Δ while OFF. |
| **Rationale** | G12 flag discipline; no phantom student-value claims. |
| **Evidence** | EP-004.* completions; EP-005.1; P-003.1 Version1_State; P-002.1 G12 |
| **Programmes** | EP-004.1–004.3, EP-005.1, P-002.1 |
| **Dependencies** | DR-006, DR-043 |
| **Supersedes** | Claiming personalisation Δ while OFF |
| **Risks** | UI copy implying live personalisation |
| **Future Review Trigger** | Flags ON in production defaults with G12 matrix and evidence |

---

## DR-040 — Private beta GO WITH CONDITIONS

| Field | Content |
|---|---|
| **Category** | Release · Operational |
| **Status** | ACTIVE (posture) |
| **Decision Statement** | EP-004 execution verdict remains **GO WITH CONDITIONS** for Stage 0 internal private beta. Stage 1 external expansion HOLD until Privacy Review signed (C1). Effectiveness claims remain NO-GO until C5–C6 floors. |
| **Background** | Controlled private beta programme. |
| **Rationale** | Continue learning under constraints without overclaim. |
| **Evidence** | `knowledge/product/ep004_private_beta/GO_NO_GO_DECISION.md` |
| **Programmes** | EP-004 |
| **Dependencies** | DR-032, DR-034, DR-022 |
| **Supersedes** | Unconditional beta expansion |
| **Risks** | Inviting Stage 1 before privacy signatures |
| **Future Review Trigger** | Privacy Review signed; C5–C6 met; or programme NO-GO |

---

## DR-041 — Version 1 production-ready declaration: NO GO

| Field | Content |
|---|---|
| **Category** | Release |
| **Status** | ACTIVE (posture) |
| **Decision Statement** | As of 2026-07-26, Product Board recommendation is **NO GO** on declaring Version 1 production-ready. Blocking: Gate G1 FAIL (G1.1 validated KSI 62 < 80; G1.9 effectiveness NO-GO); incomplete G1–G12 evidence package. |
| **Background** | P-003.1 Release Dossier synthesis under P-002.1 rules. |
| **Rationale** | Hard-gate FAIL → NO-GO (DR-031). |
| **Evidence** | P-003.1 `Version_1_RELEASE_DOSSIER.md` §11; `Release_Gates.md`; EP-007.2 K1 revalidation; EP-007.3 G1.9 |
| **Programmes** | P-003.1, P-002.1, EP-005.1, EP-007.2, EP-007.3 |
| **Dependencies** | DR-030, DR-031, DR-022, DR-025 |
| **Supersedes** | Any informal “we’re ready” posture |
| **Risks** | Premature declaration pressure (R4) |
| **Future Review Trigger** | New validated KSI ≥ 80 + effectiveness non-NO-GO + complete evidence package + signed board |

---

## DR-042 — Explainability floor K8 ≥ 70 (G1.5 PASS)

| Field | Content |
|---|---|
| **Category** | Validation · Release |
| **Status** | ACTIVE (posture) |
| **Decision Statement** | Version 1 requires K8 ≥ 70 (G1.5). After MES delivery + Tier B perception, validated K8 = 70 and G1.5 is PASS. Prefer-lower kept score at the floor. |
| **Background** | EP-006.1–006.3 remediation of invisible MES. |
| **Rationale** | Explainability floor is necessary but not sufficient for G1 overall. |
| **Evidence** | EP-006.3 `G1_5_STATUS.md`; `K8_REVALIDATION.md`; P-003.1 |
| **Programmes** | P-001.1, P-002.1, EP-006.3 |
| **Dependencies** | DR-019, DR-028, DR-025 |
| **Supersedes** | Pre-EP-006.3 K8 < 70 board slice |
| **Risks** | Regression of MES pass-through dropping K8 below floor |
| **Future Review Trigger** | K8 revalidation < 70 or Standard amendment of floor |

---

## DR-043 — Feature-flag matrix discipline (G12)

| Field | Content |
|---|---|
| **Category** | Operational · Release |
| **Status** | ACTIVE |
| **Decision Statement** | Version 1 declaration requires a published flag matrix: every student-visible educational flag with production default ON/OFF and kill-switch notes. Flags OFF must not be marketed as live. G12 declaration board not yet complete. |
| **Background** | P-002.1 G12; dossier notes unscored declaration board. |
| **Rationale** | Prevent phantom capabilities and unsafe rollouts. |
| **Evidence** | P-002.1 G12; P-003.1 Architecture Summary §9; Risk R5/R9 |
| **Programmes** | P-002.1, EP-004, EP-002.* |
| **Dependencies** | DR-009, DR-039, DR-038 |
| **Supersedes** | Informal flag folklore |
| **Risks** | Declaration without matrix |
| **Future Review Trigger** | Published V1 flag matrix + G12 scoring |

---

## DR-044 — Final Test is mandatory

| Field | Content |
|---|---|
| **Category** | Educational · Governance |
| **Status** | ACTIVE |
| **Decision Statement** | Every feature must answer: *Does this help students become better professionals?* If no → do not build. |
| **Background** | Vision 2030 / GOVERNANCE §2. |
| **Rationale** | Product philosophy gate above convenience. |
| **Evidence** | `GOVERNANCE.md` §2; Vision 2030 |
| **Programmes** | GOVERNANCE, Vision |
| **Dependencies** | DR-023 |
| **Supersedes** | Feature shipping without Final Test |
| **Risks** | Infra programmes mislabeled as student-value without ΔKSI = 0 honesty |
| **Future Review Trigger** | Vision amendment of Final Test |

---

## DR-045 — EVF must not execute inside educational decision path

| Field | Content |
|---|---|
| **Category** | Validation · Governance |
| **Status** | ACTIVE |
| **Decision Statement** | Educational Validation Framework artefacts may inspect student-visible behaviour but must not execute inside the educational decision path or mutate recommendations/plans/readiness. |
| **Background** | Educational Validation Constitution. |
| **Rationale** | Validators must not become a second brain. |
| **Evidence** | `knowledge/educational_validation/EDUCATIONAL_VALIDATION_CONSTITUTION.md`; `GOVERNANCE.md` |
| **Programmes** | EVF |
| **Dependencies** | DR-001, DR-024 |
| **Supersedes** | None |
| **Risks** | Inline validation hooks mutating tips |
| **Future Review Trigger** | EVF constitution amendment |

---

## DR-046 — KSI does not replace Vision 2030 north star

| Field | Content |
|---|---|
| **Category** | Educational · Governance |
| **Status** | ACTIVE |
| **Decision Statement** | KSI is the operational educational-usefulness index. Vision 2030’s north star remains materially higher exam pass probability for consistent users. Claim language must distinguish KSI usefulness from exam pass-rate proof (G1.8). |
| **Background** | PSF §1, §3.3; P-002.1 G1.8. |
| **Rationale** | Prevent declaring “success” on KSI alone while north star unmeasured. |
| **Evidence** | `PRODUCT_SUCCESS_FRAMEWORK.md`; Vision 2030; P-002.1 G1.8 |
| **Programmes** | P-001.1, P-002.1, Vision |
| **Dependencies** | DR-025, DR-021 |
| **Supersedes** | Treating KSI as north star |
| **Risks** | Pass-rate methodology still open (EP-001 O9) |
| **Future Review Trigger** | Approved pass-rate measurement methodology + evidence |

---

## DR-047 — Analytics Journey emit deferred; flag OFF

| Field | Content |
|---|---|
| **Category** | Operational · Validation |
| **Status** | ACTIVE |
| **Decision Statement** | Analytics instrumentation is ops-ready but production Journey emit remains deferred/gated (flag OFF). Do not claim live Journey KPIs as production-active without checklist. G9 posture: COMPLETE (flag OFF). |
| **Background** | Analytics EP-002; ADR-026 emit deferral. |
| **Rationale** | Avoid vanity/live-metric overclaim. |
| **Evidence** | `VERSION_1_READINESS.md` Analytics; P-003.1 Release Gates G9 |
| **Programmes** | Analytics EP-002, P-003.1 |
| **Dependencies** | DR-043 |
| **Supersedes** | Claiming live Journey KPIs while emit deferred |
| **Risks** | Dashboarding deferred metrics as live |
| **Future Review Trigger** | Journey emit ON with privacy/ops checklist |

---

## DR-048 — Idempotent bootstrap; no production data drops

| Field | Content |
|---|---|
| **Category** | Operational · Architecture |
| **Status** | ACTIVE |
| **Decision Statement** | Startup import/migrate/admin paths must be safe to re-run. Never drop production data in startup paths. Schema changes go through Alembic. |
| **Background** | Engineering/architecture baseline; StartupService safety. |
| **Rationale** | Production safety and re-deployability. |
| **Evidence** | `ARCHITECTURE.md`; `PROJECT_CONTEXT.md`; engineering rules |
| **Programmes** | Engineering baseline |
| **Dependencies** | None |
| **Supersedes** | Destructive bootstrap scripts |
| **Risks** | One-off ops scripts bypassing invariant |
| **Future Review Trigger** | StartupService redesign with safety review |

---

## DR-051 — Current validated KSI board is 62

| Field | Content |
|---|---|
| **Category** | Validation |
| **Status** | ACTIVE (posture) |
| **Decision Statement** | Latest validated W-PROD KSI is **62** (Medium confidence): K1 72, K2 55, K3 65, K4 55, K5 63, K6 50, K7 58, K8 70. Gap to ≥ 80 is 18 points. Do not invent category scores beyond published boards. |
| **Background** | Chain: EP-005.1 (59) → EP-006.3 (60) → EP-006.5 (61) → EP-007.2 (62). |
| **Rationale** | Single current board for G1.1 tracking. |
| **Evidence** | EP-007.2 `K1_REVALIDATION.md`; P-003.1 `KSI_Evolution.md`; `GOVERNANCE.md` validated KSI note |
| **Programmes** | EP-005.1, EP-006.3, EP-006.5, EP-007.2, P-003.1 |
| **Dependencies** | DR-026, DR-027, DR-025 |
| **Supersedes** | Validated KSI 59/60/61 as *current* board (historical boards remain evidence) |
| **Risks** | Mixing estimated and validated numbers |
| **Future Review Trigger** | Next validated re-score programme |

---

## DR-052 — EP-003 quality contracts bind Runtime A production path

| Field | Content |
|---|---|
| **Category** | Runtime · Validation |
| **Status** | ACTIVE |
| **Decision Statement** | EP-003.1–.3 quality contracts (schema-complete recommendations, readiness explainability, planning duration honesty) bind Runtime A production-default educational outputs and feed structural G3–G6 inputs. They do not by themselves prove KSI ≥ 80 or effectiveness GO. |
| **Background** | EP-003 umbrella + EP-005.1 honesty. |
| **Rationale** | Structural quality is necessary; perception and cohort evidence remain separate. |
| **Evidence** | EP-003.1–.3 completions; P-003.1 dossier §2; EP-005.1 |
| **Programmes** | EP-003.1, EP-003.2, EP-003.3, EP-005.1 |
| **Dependencies** | DR-002, DR-003, DR-004, DR-028, DR-029 |
| **Supersedes** | Uncontracted Runtime A educational outputs |
| **Risks** | Treating contract Pass as G1 Pass |
| **Future Review Trigger** | Contract version bump |

---

## DR-053 — V2 Adaptive Decision Engine does not supersede Runtime A defaults

| Field | Content |
|---|---|
| **Category** | Architecture · Runtime |
| **Status** | ACTIVE |
| **Decision Statement** | V2 ADR-005 (Adaptive Decision Engine as sole next-action authority) governs V2/EOS product paths. It does **not** supersede EP-002.9 Runtime A production-default authority (RecommendationService/PlanningService) until dual-run exit criteria and explicit cutover. Legacy V1 services remain until V2-020-style exit criteria. |
| **Background** | V2 ADRs coexist with Flask Runtime A baseline. |
| **Rationale** | Prevent applying future-path ADRs as current student truth. |
| **Evidence** | `knowledge/version2/ARCHITECTURE_DECISIONS/ADR-005-Single-Next-Action-Authority.md`; ADR-007; EP-002.9 baseline |
| **Programmes** | V2-017, V2-013, EP-002.9 |
| **Dependencies** | DR-001, DR-002 |
| **Supersedes** | Misreading ADR-005 as current W-PROD law |
| **Risks** | Dual next-action authorities in production defaults |
| **Future Review Trigger** | V2 exit criteria met + production-default cutover programme |

---

## DR-054 — Founder Governance Model is current approval authority

| Field | Content |
|---|---|
| **Category** | Governance · Operational |
| **Status** | ACTIVE |
| **Decision Statement** | Kwalitec is founder-operated. Approval authority for product, engineering, operations, privacy, and Product Board procedure is exercised by the Founder through named **capacities** (Product Owner, Engineering Owner, Operations Owner, Privacy Owner, Product Board Chair, and related Board lenses). Material approvals use Founder Review records. Evidence Hierarchy, claim standards, P-002.1 gate evidence, dry-runs, Privacy Review, kill-switch rehearsal, and Product Board sole Version 1 GO/NO GO recommendation authority are unchanged. Independent second-assessor duties (e.g. G1.7) are not satisfied by capacity concentration alone. Independent separation of duties is deferred until organisational scale. |
| **Background** | Prior governance text assumed multi-person Product / Security / Operations / Board staffing that does not currently exist. |
| **Rationale** | Truthful operating model without weakening evidence or release standards. |
| **Evidence** | `knowledge/product/gp001_founder_governance_model/FOUNDER_GOVERNANCE_MODEL.md`; `ROLE_MAPPING.md`; `UPDATED_APPROVAL_MATRIX.md`; `GOVERNANCE_UPDATE_REPORT.md`; `knowledge/GOVERNANCE.md` §1a |
| **Programmes** | GP-001 |
| **Dependencies** | DR-023, DR-030, DR-031, DR-032; P-003.7 Charter |
| **Supersedes** | Interpretation of multi-person sign-off tables as implying separate staffed departments |
| **Risks** | Capacity concentration (PR-027); skipping capacity-labelled reviews |
| **Future Review Trigger** | Second operator/engineer hired; external Board member; public launch; multi-jurisdiction privacy expansion |

---

# Part C — Quick board map

| Question | Decision IDs |
|---|---|
| Who decides what to study next? | DR-001, DR-002, DR-050, DR-029 |
| Who owns today’s plan/duration? | DR-003, DR-008, DR-017 |
| Who owns readiness? | DR-004, DR-018, DR-035 |
| Why can’t UI invent reasons? | DR-005, DR-019, DR-028 |
| Why is personalisation weak/OFF? | DR-006, DR-039, DR-038 |
| Why one Home? | DR-007, DR-020 |
| Why Twin OFF? | DR-009, DR-010, DR-015, DR-016 |
| Why no effectiveness claims? | DR-021, DR-022, DR-033, DR-036 |
| Why not production-ready? | DR-030, DR-031, DR-041, DR-051 |
| Why invite-only? | DR-034, DR-040 |
| Who approves under founder operation? | DR-054 |

---

**End of Product Decision Register**
