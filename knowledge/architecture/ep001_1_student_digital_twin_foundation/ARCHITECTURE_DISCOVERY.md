# EP-001.1 — Architecture Discovery Report

**Milestone:** EP-001.1 — Student Digital Twin Foundation  
**Phase:** 1 — Architecture Discovery (read-only)  
**Date:** 2026-07-26

---

## 1. Constitutional sources read

| Document | Role |
|---|---|
| `STUDENT_DIGITAL_TWIN.md` | Canonical domain architecture — Twin as learner-state SoT (10 domains) |
| `docs/architecture/DIGITAL_TWIN_CONSTITUTION.md` | Normative law — five educational domains; evidence → Twin → guidance |
| `DIGITAL_TWIN_PHILOSOPHY.md` / `knowledge/version2/DIGITAL_TWIN_PHILOSOPHY.md` | Why the Twin exists |
| `knowledge/version2/STUDENT_DIGITAL_TWIN.md` | V2-013 engine package contract (`app/domain/student_twin`) |
| `knowledge/version2/ARCHITECTURE_DECISIONS/ADR-004-Digital-Twin.md` | Evidence-driven Twin decision |
| `knowledge/architecture/STUDENT_DIGITAL_TWIN_ARCHITECTURE.md` | MS-004 synthesis architecture (T0–T6 Implemented) |
| `knowledge/architecture/DIGITAL_TWIN_DATA_MODEL.md` | Logical LearnerProfileSnapshot over Runtime A |
| `knowledge/architecture/MIGRATION_PLAN_MS004.md` | Phased cutover; Authority flag documented |
| `knowledge/architecture/DIGITAL_TWIN_READINESS_REPORT.md` | T6 ready; hold Authority / T7 |
| `app/domain/twin/README.md` | Epic Twin package — authoritative domain aggregate |

---

## 2. Constitutional model (summary)

The Student Digital Twin is Kwalitec’s living, evidence-backed model of a learner relative to a syllabus and sitting.

**Binding principles**

1. Twin is the single source of truth for *learner state* (beliefs / synthesis).
2. Curriculum remains syllabus structure SoT.
3. Evidence is append-only; Twin evolves by accumulation.
4. Core updates are deterministic and explainable.
5. Plans / missions are *derived*, not competing learner-state stores.
6. AI must not own Twin mutations.

**MS-004 refinement (accepted):** Runtime A remains the SoT for *transaction facts* (attempts, missions, TopicProgress writes). Twin **consumes** those facts and synthesises a longitudinal profile — it must not invent mastery or write Runtime A.

These are complementary: facts live in Runtime A; learner-state *claims for consumers* should go through Twin so subsystems do not fork independent copies.

---

## 3. Components that already contribute to the Twin

### 3.1 Domain aggregates

| Stack | Path | Contribution |
|---|---|---|
| Epic Twin | `app/domain/twin/` | Identity, Goals, Knowledge, Memory, Behaviour, Performance, Predictions + update strategies |
| Learning Evidence | `app/domain/evidence/` | Canonical evidence input to Twin update pipeline |
| V2 Student Twin | `app/domain/student_twin/` | Computed mastery / readiness / recommendations engine (framework-free) |
| EOS Digital Twin | `src/domain/education/digital_twin/` | Separate Education OS DDD aggregate |

### 3.2 Application orchestration

| Path | Contribution |
|---|---|
| `app/application/twin_update/` | Evidence → Epic Twin write coordination |
| `app/application/twin_repository/` | Durable `twin_snapshots` persistence |
| `app/application/twin/twin_provider.py` | Twin retrieval for orchestrator |
| `app/application/student_twin/` | V2 `StudentTwinEngine` |
| `app/application/student_experience/ports/student_twin_port.py` | Experience read port |

### 3.3 Infrastructure / synthesis

| Path | Contribution |
|---|---|
| `app/infrastructure/adapters/digital_twin/` | MS-004 T0–T6: facets, snapshot, explainability, Experience projection, shadow |
| `app/infrastructure/adapters/student_twin/` | ExperienceTwinAdapter + TwinPort adapter |
| `app/infrastructure/adapters/adaptive_engine/collectors.py` | Runtime A collectors reused by Twin assembler |
| `app/infrastructure/adapters/adaptive_engine/twin_input.py` | Adaptive consumes Twin read-only |

### 3.4 Runtime A fact sources (Twin inputs)

| Path | Contribution |
|---|---|
| `app/models/topic_progress.py` | Topic mastery / stage / accuracy |
| `app/models/learning.py` | StudyAttempt evidence |
| `app/models/mission.py` | Mission completion |
| `app/services/adaptive_learning_service.py` | Mastery writes |
| `app/services/learning_service.py` | Attempt writes |
| `app/services/mission_service.py` | Mission lifecycle |
| `app/services/readiness_service.py` | Readiness + streaks |

### 3.5 Persistence

| Table / model | Role |
|---|---|
| `twin_snapshots` (`app/models/twin_snapshot.py`) | Epic Twin durable snapshots |
| `eos_digital_twins` | EOS Twin persistence |
| `topic_progress`, `study_attempts`, `missions` | Runtime A educational facts |

---

## 4. Discovery conclusion

Kwalitec already has a **rich Twin architecture** (domain + MS-004 synthesis + V2 engine + EOS). What is missing for Foundation is not another Twin model — it is:

1. A **single canonical foundation read contract** covering the learner-state dimensions consumers need.
2. Explicit **consolidation rules** naming which stack is production authority.
3. An optional, flag-gated **Experience authority seam** so future subsystems can obtain state from Twin without independent copies.
4. Pass-through packaging of mastery, progress, evidence, practice, streaks, and mission completion into that foundation (already available via Runtime A collectors).

**No code was modified during Phase 1.**
