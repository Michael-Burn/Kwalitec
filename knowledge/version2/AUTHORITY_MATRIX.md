# Version 2 Authority Matrix

**Document ID:** V2-017-AUTHORITY  
**Status:** Architectural  
**Milestone:** V2-017 — Production Integration Foundation  
**Related:** [`ARCHITECTURE_DECISIONS/ADR-005-Single-Next-Action-Authority.md`](ARCHITECTURE_DECISIONS/ADR-005-Single-Next-Action-Authority.md) · [`ARCHITECTURE_DECISIONS/ADR-006-Authority-Boundaries.md`](ARCHITECTURE_DECISIONS/ADR-006-Authority-Boundaries.md) · [`PRODUCTION_INTEGRATION.md`](PRODUCTION_INTEGRATION.md)

This matrix names **authority** (who may lawfully decide or mutate) versus **consumers** (who may read or request via ports). Upstream / downstream list integration dependencies only.

---

## Learner State

| | |
|--|--|
| **Authority** | Student Digital Twin |
| **Consumers** | Adaptive Decision Engine, Learning Orchestrator, Student UI, Education Platform (read), Mission Engine (read) |
| **Upstream** | Evidence spine (session / activity / mission outcomes) |
| **Downstream** | Adaptive decisions, explainability surfaces, readiness projections |

---

## Learner-Facing Next Action

| | |
|--|--|
| **Authority** | Adaptive Decision Engine (sole) |
| **Consumers** | Student UI, Learning Orchestrator, Mission Engine (delivery), Education Platform (compose) |
| **Upstream** | Twin snapshots, Journey position, curriculum context |
| **Downstream** | Mission delivery, session planning surfaces |

---

## Curriculum Structure (Syllabus Truth)

| | |
|--|--|
| **Authority** | Curriculum Graph |
| **Consumers** | Instructional Blueprint, Journey, Session, Activity, Mission, Education Platform, Studio (display) |
| **Upstream** | Published Management releases / official JSON |
| **Downstream** | Pedagogy compilation, traversal, sequencing |

---

## Curriculum Publication Lifecycle

| | |
|--|--|
| **Authority** | Curriculum Management |
| **Consumers** | Curriculum Studio, Curriculum Ingestion (feeds), Education Platform (consume published), Founder UI |
| **Upstream** | Ingestion normalised packages, Founder approvals |
| **Downstream** | Active subject versions available to Educational Core |

---

## Curriculum Ingestion Pipeline

| | |
|--|--|
| **Authority** | Curriculum Ingestion |
| **Consumers** | Curriculum Studio (status/display), Curriculum Management (import candidates) |
| **Upstream** | Abstract document sources |
| **Downstream** | Normalised structures / validation reports |

---

## Founder Curriculum Readiness (Studio)

| | |
|--|--|
| **Authority** | Curriculum Studio (orchestration / projection only) |
| **Consumers** | Founder UI (future), Founder automation |
| **Upstream** | Management, Ingestion, Education Platform ports |
| **Downstream** | Founder dashboards, checklists, diffs (no second publication ontology) |

---

## Pedagogy (Instructional Design)

| | |
|--|--|
| **Authority** | Instructional Blueprint Engine |
| **Consumers** | Journey / Session / Activity composition, Education Platform |
| **Upstream** | Curriculum Graph sections |
| **Downstream** | Learning activities and session structures |

---

## Learning Journey

| | |
|--|--|
| **Authority** | Learning Journey Engine / domain |
| **Consumers** | Session Runtime, Mission Engine, Education Platform, Adaptive Decision (context) |
| **Upstream** | Curriculum + Blueprint + Twin readiness inputs |
| **Downstream** | Sessions, reflections, journey progress |

---

## Learning Session Execution

| | |
|--|--|
| **Authority** | Learning Session Runtime |
| **Consumers** | Activity Engine, Mission delivery, Orchestrator (events) |
| **Upstream** | Journey recommendation / intent |
| **Downstream** | Evidence events, session completion |

---

## Learning Activity Execution

| | |
|--|--|
| **Authority** | Learning Activity Engine |
| **Consumers** | Session Runtime, Twin evidence intake |
| **Upstream** | Blueprint / session plan |
| **Downstream** | Activity outcomes → evidence |

---

## Mission Delivery

| | |
|--|--|
| **Authority** | Mission Engine 2.0 (delivery lifecycle) |
| **Consumers** | Student UI, Learning Orchestrator, Mission Adapter (cutover) |
| **Upstream** | Adaptive Decision (next action), Journey context |
| **Downstream** | Daily commitments, mission state transitions |

**Constraint:** Mission does not independently recommend learner next actions (ADR-005).

---

## Educational Core Composition

| | |
|--|--|
| **Authority** | Education Platform (facade composition — no educational law) |
| **Consumers** | Product ingress paths, Studio health/surface probes, CLI/automation |
| **Upstream** | Bound engine ports |
| **Downstream** | Workflow results / platform health |

---

## Live Event Coordination

| | |
|--|--|
| **Authority** | Learning Orchestrator (pipeline order only) |
| **Consumers** | Infrastructure adapters, analytics observation |
| **Upstream** | Evidence events |
| **Downstream** | Twin update → Adaptive Decision → Mission apply → Analytics |

---

## Persistence / Events / Observability

| | |
|--|--|
| **Authority** | Infrastructure (`app/infrastructure`) |
| **Consumers** | All adapters; never educational engines directly for business rules |
| **Upstream** | Application ports |
| **Downstream** | Durable stores, integration events, operational metrics |

**Constraint:** Repositories and stores hold **no** educational algorithms.

---

## Explicit Non-Authorities

| Capability | Must not claim authority |
|------------|--------------------------|
| UI / templates | Mastery, Topic Complete, publication law, next action |
| Analytics adapters | Educational decisions |
| Founder tools | Student Learning Mode mutation |
| AI / LLM | Twin truth, next-action law, curriculum publication |

---

## Closing

When a new surface wants to “recommend” or “publish”, check this matrix first. If authority is unclear, stop and amend ADR-005 / ADR-006 — do not invent a parallel owner.
