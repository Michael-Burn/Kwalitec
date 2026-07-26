# EP-001.1 — Student Digital Twin Foundation

**Milestone:** EP-001.1 — Student Digital Twin Foundation (Implementation)  
**Status:** Implemented  
**Authority:** Extends constitutional Twin specs; does not redesign them  
**Package:** `app/infrastructure/adapters/digital_twin/` (`foundation.py`, `authority.py`)

---

## Deliverables

| Artefact | Path |
|---|---|
| Architecture Discovery | [`ARCHITECTURE_DISCOVERY.md`](ARCHITECTURE_DISCOVERY.md) |
| Existing Implementation Review | [`EXISTING_IMPLEMENTATION_REVIEW.md`](EXISTING_IMPLEMENTATION_REVIEW.md) |
| Gap Analysis | [`GAP_ANALYSIS.md`](GAP_ANALYSIS.md) |
| Implementation Plan | [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md) |
| Completion Report | [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) |

---

## Canonical decision (binding)

| Concern | Canonical owner |
|---|---|
| Syllabus structure | Curriculum Engine / `CurriculumService` |
| Educational **transaction facts** (attempts, missions, TopicProgress writes) | Runtime A SQL + services |
| Constitutional **learner-state aggregate** (belief structure) | `app/domain/twin.DigitalTwin` |
| Runtime-A-grounded **synthesis + foundation read model** | MS-004 `app/infrastructure/adapters/digital_twin` + EP-001.1 Foundation |
| Experience TwinPort UX | `ExperienceTwinAdapter` until `KWALITEC_DIGITAL_TWIN_AUTHORITY=1` |
| V2 `app/domain/student_twin` | Parallel bounded context — **not** production authority |
| EOS `src/domain/education/digital_twin` | Education OS stack — **not** Flask Runtime A authority |

**Rule:** Prefer extend / integrate / consolidate. Never introduce a fourth Twin stack.

---

## Feature flags

| Env | Flag | Default | Effect |
|---|---|---|---|
| `KWALITEC_DIGITAL_TWIN` | `ENABLE_DIGITAL_TWIN` | OFF | MS-004 pipeline + Foundation DI |
| `KWALITEC_DIGITAL_TWIN_AUTHORITY` | `ENABLE_DIGITAL_TWIN_AUTHORITY` | OFF | Experience `StudentTwinPort` serves Foundation (requires Twin ON) |

---

## Governing documents

- [`STUDENT_DIGITAL_TWIN.md`](../../../STUDENT_DIGITAL_TWIN.md)
- [`docs/architecture/DIGITAL_TWIN_CONSTITUTION.md`](../../../docs/architecture/DIGITAL_TWIN_CONSTITUTION.md)
- [`STUDENT_DIGITAL_TWIN_ARCHITECTURE.md`](../STUDENT_DIGITAL_TWIN_ARCHITECTURE.md)
- [`DIGITAL_TWIN_DATA_MODEL.md`](../DIGITAL_TWIN_DATA_MODEL.md)
- ADR-004 Digital Twin ([`knowledge/version2/ARCHITECTURE_DECISIONS/ADR-004-Digital-Twin.md`](../../version2/ARCHITECTURE_DECISIONS/ADR-004-Digital-Twin.md))
