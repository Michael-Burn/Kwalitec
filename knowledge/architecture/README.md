# Architecture

## Purpose

Architecture governance artefacts for Kwalitec: Design Principles, Founder Information Architecture, Architecture Decision Records (ADRs), and related specifications.

## Owner

Architecture Governance / Product Operations Programme (for POP artefacts)

## Status

Active — Version 2 closed (APP-004 production readiness); architecture governance (APP-003) remains binding

## Contents

### Version 2 Educational OS governance (release artefacts)

| Document | Role |
|---|---|
| [`docs/ARCHITECTURE_CONSTITUTION.md`](../../docs/ARCHITECTURE_CONSTITUTION.md) | Version 2 architectural law |
| [`docs/ARCHITECTURE_OVERVIEW.md`](../../docs/ARCHITECTURE_OVERVIEW.md) | Layer and subsystem map |
| [`docs/SYSTEM_CONTEXT.md`](../../docs/SYSTEM_CONTEXT.md) | Actors and trust boundaries |
| [`docs/DEPENDENCY_RULES.md`](../../docs/DEPENDENCY_RULES.md) | Dependency direction law |
| [`docs/adr/`](../../docs/adr/) | ADR-001 … ADR-010 (Educational OS) |
| `tests/architecture/` | Mandatory CI architecture gates |

### Design principles and historical ADRs

| Document | Role |
|---|---|
| [DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md) | Governing product-design philosophy (ARCH-001) |
| [POP-002_FOUNDER_INFORMATION_ARCHITECTURE.md](POP-002_FOUNDER_INFORMATION_ARCHITECTURE.md) | Founder Command Centre IA specification |
| [ADR-001-service-layer.md](ADR-001-service-layer.md) | Service-layer decision |
| [ADR-002-blueprint-architecture.md](ADR-002-blueprint-architecture.md) | Thin blueprints |
| [ADR-003-curriculum-v1-v2.md](ADR-003-curriculum-v1-v2.md) | Curriculum V1 + V2 coexistence |
| [ADR-004-canonical-topic-traversal.md](ADR-004-canonical-topic-traversal.md) | Canonical topic ordering |
| [ADR-005-testing-strategy.md](ADR-005-testing-strategy.md) | Testing strategy |

Structural map of the running application: [`ARCHITECTURE.md`](../../ARCHITECTURE.md) at the repository root.

As-built Founder / brand implementation reports: [`knowledge/releases/`](../releases/) (IAHF-003, IAHF-004A/B, V1SP-*).

### MS-001 — Foundational Trust (navigation investigation)

Read-only architecture investigation of study navigation, session lifecycle, and sources of truth. **No implementation.**

| Document | Role |
|---|---|
| [NAVIGATION_AUDIT.md](NAVIGATION_AUDIT.md) | Every study entry point (route → service → destination) |
| [NAVIGATION_GRAPH.md](NAVIGATION_GRAPH.md) | Route graph: guards, redirects, required state |
| [SESSION_LIFECYCLE.md](SESSION_LIFECYCLE.md) | Legacy and canonical session lifecycles |
| [SOURCE_OF_TRUTH_ANALYSIS.md](SOURCE_OF_TRUTH_ANALYSIS.md) | Ownership / duplication / single-SoT verdict |
| [SERVICE_DEPENDENCY_MAP.md](SERVICE_DEPENDENCY_MAP.md) | Navigation services, cycles, recommendation pipeline |
| [UI_INVENTORY.md](UI_INVENTORY.md) | Navigation-related templates, JS, remain/remove |
| [REFACTORING_RECOMMENDATIONS.md](REFACTORING_RECOMMENDATIONS.md) | Strengths, risks, safest order, complexity |

### MS-001 — Foundational Trust (Engineering Directive 002 / 003 / 004 — Educational Runtime Bridge)

Architecture design for bridging Experience ports to canonical SQL educational services. **Mission Read Adapter** and **Mission Start Bridge** implemented; Resume and remaining bridges not started.

| Document | Role |
|---|---|
| [EDUCATIONAL_RUNTIME_BRIDGE.md](EDUCATIONAL_RUNTIME_BRIDGE.md) | Authority matrix, Experience consumption map, ADR, Bridge Complete, Mission Read / Start status |
| [BRIDGE_INTERFACE_SPECIFICATION.md](BRIDGE_INTERFACE_SPECIFICATION.md) | Bridge interfaces: inputs, outputs, failures, fallbacks, telemetry |
| [BRIDGE_SEQUENCE_DIAGRAM.md](BRIDGE_SEQUENCE_DIAGRAM.md) | Sequences: Start, Resume, Load Home, Complete, Recommendation |
| [MIGRATION_PLAN.md](MIGRATION_PLAN.md) | Incremental releasable phases |
| [ROLLBACK_PLAN.md](ROLLBACK_PLAN.md) | Per-phase and emergency rollback |
| [RISK_ANALYSIS.md](RISK_ANALYSIS.md) | Technical + educational risk per phase |
| [TEST_STRATEGY.md](TEST_STRATEGY.md) | Unit → E2E + Internal Alpha (design only) |

### MS-002 — Educational Continuity (Engineering Directive 001 — Journey / History architecture)

Architecture design for Educational Journey and History read bridges sourced exclusively from Runtime A. **No implementation.**

| Document | Role |
|---|---|
| [EDUCATIONAL_JOURNEY_ARCHITECTURE.md](EDUCATIONAL_JOURNEY_ARCHITECTURE.md) | Canonical timeline, Journey/History projection, ADR, Journey Bridge Complete, final report |
| [JOURNEY_SEQUENCE_DIAGRAM.md](JOURNEY_SEQUENCE_DIAGRAM.md) | Sequences: Load Journey, View Recommendation Change |
| [HISTORY_SEQUENCE_DIAGRAM.md](HISTORY_SEQUENCE_DIAGRAM.md) | Sequences: Load History, Inspect Evidence |
| [JOURNEY_INTERFACE_SPECIFICATION.md](JOURNEY_INTERFACE_SPECIFICATION.md) | JourneyBridge / HistoryBridge contracts, pagination, TraceRef |
| [JOURNEY_DATA_MODEL.md](JOURNEY_DATA_MODEL.md) | Logical projection model over existing SQL (no schema changes) |
| [JOURNEY_TRACEABILITY_MATRIX.md](JOURNEY_TRACEABILITY_MATRIX.md) | What / Why / Evidence / Recommendation delta per event type |
| [MIGRATION_PLAN_MS002.md](MIGRATION_PLAN_MS002.md) | Incremental releasable phases J0–J7 |
| [RISK_ANALYSIS_MS002.md](RISK_ANALYSIS_MS002.md) | Technical + educational risk per phase |

### MS-003 — Adaptive Learning Intelligence (Engineering Directive 001–008)

Architecture and implementation for the Adaptive Learning Engine that converts authoritative Runtime A evidence into explainable future learning decisions. **A0–A6 Implemented** (contracts through Shadow Soak). Engine remains read-only relative to educational history; Authority / Experience cutover remains flag-gated OFF by default. Await architecture review before Adaptive Engine Ready (A7) / MS-003 complete.

| Document | Role |
|---|---|
| [ADAPTIVE_ENGINE_ARCHITECTURE.md](ADAPTIVE_ENGINE_ARCHITECTURE.md) | Engine placement, inputs/outputs, ADR, Adaptive Engine Ready, **A0–A6 status**, soak operational readiness |
| [ADAPTIVE_ENGINE_READINESS_REPORT.md](ADAPTIVE_ENGINE_READINESS_REPORT.md) | Directive 008 readiness assessment, risks, rollout recommendation, activation checklist |
| [ADAPTIVE_DECISION_PIPELINE.md](ADAPTIVE_DECISION_PIPELINE.md) | Runtime A → Evidence → Engine → Recommendation → Experience |
| [ADAPTIVE_INTERFACE_SPECIFICATION.md](ADAPTIVE_INTERFACE_SPECIFICATION.md) | AdaptiveEngineBridge / AdaptiveDecisionRecord contracts |
| [ADAPTIVE_DATA_FLOW.md](ADAPTIVE_DATA_FLOW.md) | Read-only input flows; advice-only outputs; forbidden writes |
| [ADAPTIVE_TRACEABILITY.md](ADAPTIVE_TRACEABILITY.md) | Evidence → Decision → Recommendation → Student Outcome |
| [ADAPTIVE_EXPLAINABILITY.md](ADAPTIVE_EXPLAINABILITY.md) | Six-question ExplanationBundle contract |
| [MIGRATION_PLAN_MS003.md](MIGRATION_PLAN_MS003.md) | Incremental releasable phases A0–A7 |
| [RISK_ANALYSIS_MS003.md](RISK_ANALYSIS_MS003.md) | Feedback loops, over-adaptation, stale evidence, bias, performance |

### EP-001 / EP-002 — Canonical learner intelligence (Runtime A)

Constitutional Twin-consuming chain on MS-004 substrate, then student-surface activation. **EP-001.1–4 Implemented** (Foundation → Planner → Readiness → Insight); **EP-001.5 Integration Review Complete**; **EP-002 Student Intelligence Surface — Complete** (EP-002.1–9; constitutionally certified; production defaults Twin / Authority / Cutover OFF; **Ready for Controlled Pilot**; Twin Ready (T7) not declared). Distinct from product [`../product/analytics/ep002/`](../product/analytics/ep002/) (Analytics Operational Readiness).

| Document | Role |
|---|---|
| [`ep001_1_student_digital_twin_foundation/`](ep001_1_student_digital_twin_foundation/) | Canonical learner-state Foundation |
| [`ep001_2_adaptive_study_planner/`](ep001_2_adaptive_study_planner/) | Adaptive Study Planner consumer |
| [`ep001_3_readiness_intelligence/`](ep001_3_readiness_intelligence/) | Readiness Intelligence consumer |
| [`ep001_4_insight_recommendation_layer/`](ep001_4_insight_recommendation_layer/) | Insight & Recommendation Layer |
| [`ep001_5_architectural_integration_review/`](ep001_5_architectural_integration_review/) | EP-001 assurance / integration review |
| [`ep002_student_intelligence_surface/`](ep002_student_intelligence_surface/) | EP-002 planning: cutover programme brief |
| [`ep002_1_consumer_chain_observability/`](ep002_1_consumer_chain_observability/) | EP-002.1: `build_*` observability + dual-run diagnostics |
| [`ep002_2_shared_foundation_di/`](ep002_2_shared_foundation_di/) | EP-002.2: shared Foundation/CLS DI + MissionOptimizer decision |
| [`ep002_3_twin_authority_soak/`](ep002_3_twin_authority_soak/) | EP-002.3: Twin + Authority non-prod soak |
| [`ep002_4_study_insights_dual_run/`](ep002_4_study_insights_dual_run/) | EP-002.4: Study Insights dual-run (legacy authoritative) |
| [`ep002_5_study_insights_gated_http_cutover/`](ep002_5_study_insights_gated_http_cutover/) | EP-002.5: Study Insights gated HTTP cutover (legacy fail-open) |
| [`ep002_6_readiness_intelligence_cutover/`](ep002_6_readiness_intelligence_cutover/) | EP-002.6: Readiness Intelligence dual-run → gated cutover |
| [`ep002_7_daily_plan_mission_cutover/`](ep002_7_daily_plan_mission_cutover/) | EP-002.7: Daily Plan / mission dual-run → gated cutover |
| [`ep002_8_presentation_consolidation/`](ep002_8_presentation_consolidation/) | EP-002.8: Runtime A presentation consolidation |
| [`ep002_9_programme_exit_certification/`](ep002_9_programme_exit_certification/) | EP-002.9: programme exit + authoritative architecture baseline |
| [`TWIN_STACK_QUARANTINE.md`](TWIN_STACK_QUARANTINE.md) | Operator quarantine: MS-004 vs Epic / V2 / EOS Twin |

### MS-004 — Student Digital Twin (Engineering Directive 001 — architecture; Directive 002–008 — T0–T6)

Architecture design for the Student Digital Twin as a Runtime-A-grounded longitudinal learner profile. Twin consumes authoritative evidence; Adaptive Engine may consume Twin but does not own it. **T0–T5 Implemented** (`app/infrastructure/adapters/digital_twin/`); **T4 Adaptive Twin-input Implemented** (`adaptive_engine.twin_input`); **T6 Shadow Validation Implemented**; Experience UX authority cutover / Twin Ready (T7) not started.

| Document | Role |
|---|---|
| [STUDENT_DIGITAL_TWIN_ARCHITECTURE.md](STUDENT_DIGITAL_TWIN_ARCHITECTURE.md) | Twin placement, responsibilities, Runtime A / Adaptive / Experience relationships, ADR, Twin Ready; **T0–T6 status** |
| [DIGITAL_TWIN_READINESS_REPORT.md](DIGITAL_TWIN_READINESS_REPORT.md) | Directive 008 readiness assessment, risks, rollout recommendation, activation checklist |
| [DIGITAL_TWIN_DATA_MODEL.md](DIGITAL_TWIN_DATA_MODEL.md) | Logical LearnerProfileSnapshot facets over existing SQL (no schema changes) |
| [DIGITAL_TWIN_LIFECYCLE.md](DIGITAL_TWIN_LIFECYCLE.md) | States, update triggers, freshness, post-evidence sequencing |
| [DIGITAL_TWIN_INTERFACE_SPECIFICATION.md](DIGITAL_TWIN_INTERFACE_SPECIFICATION.md) | DigitalTwinBridge / StudentTwinPort / Adaptive attach contracts |
| [DIGITAL_TWIN_TRACEABILITY.md](DIGITAL_TWIN_TRACEABILITY.md) | Evidence → Twin Update → Claim → Projection → optional Adaptive |
| [DIGITAL_TWIN_EXPLAINABILITY.md](DIGITAL_TWIN_EXPLAINABILITY.md) | Twin six-question ExplanationBundle + gate |
| [MIGRATION_PLAN_MS004.md](MIGRATION_PLAN_MS004.md) | Incremental releasable phases T0–T7 |
| [RISK_ANALYSIS_MS004.md](RISK_ANALYSIS_MS004.md) | Authority inversion, invented mastery, Adaptive ownership, privacy, stale insights |

### MS-005 — Learning Strategy & Intervention Engine (Engineering Directive 001 — architecture; Directive 002–005 — S0–S3)

Architecture design for the Learning Strategy & Intervention Engine as a deterministic orchestration layer over Runtime A evidence, Twin interpretation, and Adaptive recommendations. **S0 Contracts Implemented**; **S1 Core Strategy Engine Implemented**; **S2 Explainability & Projection Implemented**; **S3 Shadow Validation Implemented** (`app/infrastructure/adapters/strategy_engine/`). Experience authority cutover / Strategy Ready not started.

| Document | Role |
|---|---|
| [LEARNING_STRATEGY_ENGINE_ARCHITECTURE.md](LEARNING_STRATEGY_ENGINE_ARCHITECTURE.md) | Engine placement, responsibilities, dependency law, ADR, feature-flag rollout; **S0–S3 status** |
| [STRATEGY_ENGINE_READINESS_REPORT.md](STRATEGY_ENGINE_READINESS_REPORT.md) | Directive 005 readiness assessment, risks, rollout recommendation, activation checklist |
| [INTERVENTION_MODEL.md](INTERVENTION_MODEL.md) | Intervention kinds, lifecycle, study/session/revision/recovery/fatigue/confidence models |
| [STRATEGY_PIPELINE.md](STRATEGY_PIPELINE.md) | Runtime A → Twin → Adaptive → Strategy → Experience pipeline |
| [STRATEGY_EXPLAINABILITY.md](STRATEGY_EXPLAINABILITY.md) | Five mandatory questions + StrategyExplanationBundle + gate |
| [STRATEGY_TRACEABILITY.md](STRATEGY_TRACEABILITY.md) | Evidence → Twin → Adaptive → Intervention → Delivery → Outcome |
| [STRATEGY_INTERFACE_SPECIFICATION.md](STRATEGY_INTERFACE_SPECIFICATION.md) | StrategyEngineBridge / StrategyInterventionPort contracts |
| [MIGRATION_PLAN_MS005.md](MIGRATION_PLAN_MS005.md) | Incremental releasable phases S0–S7 |
| [RISK_ANALYSIS_MS005.md](RISK_ANALYSIS_MS005.md) | Authority inversion, Adaptive re-rank, over-orchestration, mission conflict, poly-authority |

### MS-006 — Learning Evidence & Experimentation Platform (E0–E5 Implemented)

Observational measurement and policy-evaluation platform that sits **after** Experience in the dependency chain. Observes outcomes, supports controlled flag-mediated experiments, and enables governed policy evolution — without educational write authority. **E0–E4 Implemented**; **E5 Shadow Validation & Operational Readiness Implemented** (`app/infrastructure/adapters/evidence_platform/`). Policy deployment / Evidence Platform Ready not declared — await architecture review.

| Document | Role |
|---|---|
| [LEARNING_EVIDENCE_PLATFORM_ARCHITECTURE.md](LEARNING_EVIDENCE_PLATFORM_ARCHITECTURE.md) | Platform placement, dependency law, ADR draft, flags, **E0–E5 Implemented** |
| [EVIDENCE_PLATFORM_READINESS_REPORT.md](EVIDENCE_PLATFORM_READINESS_REPORT.md) | E5 operational readiness / MS-006 architecture review gate |
| [EVIDENCE_MODEL.md](EVIDENCE_MODEL.md) | Evidence lifecycle, artefacts, claim boundaries, quality gates |
| [EXPERIMENT_FRAMEWORK.md](EXPERIMENT_FRAMEWORK.md) | Experiment protocol, assignment, measurement, analysis |
| [POLICY_EVALUATION.md](POLICY_EVALUATION.md) | Policy versions, evaluation workflow, five-answer explainability |
| [OUTCOME_ANALYTICS.md](OUTCOME_ANALYTICS.md) | Analytics responsibilities, metric families, anti-patterns |
| [GOVERNANCE_MODEL.md](GOVERNANCE_MODEL.md) | Propose → review → decide → apply → verify process |
| [EVIDENCE_TRACEABILITY.md](EVIDENCE_TRACEABILITY.md) | Facts → delivery → outcome → evaluation → governance chain |
| [MIGRATION_PLAN_MS006.md](MIGRATION_PLAN_MS006.md) | Incremental releasable phases E0–E7 |
| [RISK_ANALYSIS_MS006.md](RISK_ANALYSIS_MS006.md) | Authority inversion, false causation, SP8 collapse, auto-promote, privacy |
