# SR-003 — Progress Singularity

**Programme:** SR-003 · SR-001A Phase P6  
**Date:** 2026-07-30  
**Nature:** P6 implementation — one Progress Engine as sole curriculum progression AUTHORITY  
**Authority:** SR-001 · SR-001A · EV-001A · EV-001B · SDT-004  
**Predecessor:** SDT-004 (P5 Twin activation)  
**Successor:** SR-003b (JSON curriculum adapter) / SR-004 / P7 legacy retirement  

---

## Executive Summary

SR-003 creates the singular **Progress Engine** that integrates Accepted educational evidence decisions, mission completion signals, curriculum structure, and optional Twin estimates into one Study Progress truth.

The Progress Engine is the sole AUTHORITY for curriculum progression: coverage, current topic, completed / remaining objectives, curriculum position, and progress projections. It does **not** evaluate evidence, update the Twin, run study sessions, teach, or generate evidence.

```
LearningSessionRuntime
        │
        ▼
EducationalEvidenceAuthority
        │
        ▼
Progress Engine  ──► Mission Composition
        │
        └──────────► Dashboard

StudentTwinEngine
        │  optional educational estimate
        ▼
Progress Engine   (no authority inversion)
```

Flag: `SR_PROGRESS_SINGULARITY` (default **OFF**). Event-sourced `TOPIC_COMPLETED` history is retained on rollback.

---

## Architecture

| Concern | Owner |
|---|---|
| Evidence Accept / Reject | `EducationalEvidenceAuthority` (sole Evidence Authority) |
| Coverage advance authorisation | `ProgressEngine.authorise_*` (trusts Authority columns) |
| Study Progress derivation | `ProgressEngine.derive_study_progress` → domain `derive_progress` |
| Event store (`TOPIC_COMPLETED`) | `EducationalRuntimeEngineService` (sole writer when singularity ON) |
| Twin estimates (optional) | `StudentTwinEngine` → `TwinEstimateInput` (read-only) |
| Session completion wiring | `LearningSessionRuntimeEngine` (adapter) |
| Session FSM | `LearningSessionRuntime` (unchanged) |

**One Educational State invariants preserved:**

| Authority | Remains sole for |
|---|---|
| LearningSessionRuntime | Study sessions |
| EducationalEvidenceAuthority | Evidence evaluation |
| StudentTwinEngine | Learner estimation |
| ProgressEngine | Curriculum progression |

### Pipeline (P6)

```
Mission → Study Session → Evidence Package
        → EducationalEvidenceAuthority (Accept / Reject)
        → Progress Engine (authorise coverage; derive Study Progress)
        → Mission Complete + TOPIC_COMPLETED (when authorised)
        → Twin (Educational+ only; independent; optional projection input)
        → Mission Composition / Dashboard (consume Study Progress)
```

---

## Progress Model

### Study Progress (`StudyProgress`)

| Field | Meaning |
|---|---|
| `coverage_ratio` | Completed topics / total topics (Study Progress — not understanding) |
| `current_topic_id` | Singular next eligible curriculum node |
| `completed_topic_ids` | Ordered coverage completions |
| `incomplete_topic_ids` | Remaining topics |
| `completed_objective_ids` / `remaining_objective_ids` | Objective roll-ups from topic specs |
| `position` | `CurriculumPosition` (index, stage, counts) |
| `projection` | `ProgressProjection` (remaining, next, optional Twin annotations) |

### Coverage math

Coverage remains deterministic event-sourced derivation (`derive_progress` over `TOPIC_COMPLETED` + published `ProgressModelSpec`). Twin estimates never invent or erase coverage.

### Progress projections

| Twin present? | Projection basis | Behaviour |
|---|---|---|
| No | `coverage_only` | Remaining topics + next topic; lawful silence on mastery |
| Yes | `coverage_plus_optional_twin` | Annotate remaining topics with Estimated Mastery / Knowledge; flag weak topics for mission composition inputs |

Weak-topic threshold for annotation: mastery &lt; 0.45 (projection only — not mission redesign).

### Mission composition inputs

`MissionCompositionInputs` exposes singular `current_topic_id`, coverage, remaining topics, and optional `weak_topic_ids`. Mission selection remains Mission AUTHORITY.

---

## Authority Matrix

| Actor | MAY | MUST NOT |
|---|---|---|
| **Progress Engine** | Advance coverage (when Authority allows); determine current topic; compute position; expose projections; provide tomorrow-mission inputs | Evaluate evidence; update Twin; run sessions; teach; generate evidence |
| **EducationalEvidenceAuthority** | Accept / Reject packages; set `may_advance_progress` | Derive Study Progress; invent coverage without Progress Engine |
| **StudentTwinEngine** | Supply optional estimates | Author coverage; invert Progress authority |
| **LearningSessionRuntime** | Emit candidates; close sessions | Advance Progress independently of Authority + Progress Engine |
| **EducationalRuntimeEngineService** | Persist `TOPIC_COMPLETED` as sole event writer under singularity | Parallel “current topic” disagreeing with Progress Engine |

### Advance decision table

| Evidence shape | Progress Engine decision |
|---|---|
| Accepted + `may_advance_progress=True` | Advance |
| Accepted with Restrictions + advance allowed | Advance |
| Finish Review Partially / No | Ignore (no advance) |
| Rejected (reading-only, reflection-only, …) | Ignore (`rejected_evidence_ignored`) |
| Missing validation | Ignore |

---

## Files Created

- `app/application/progress_engine/__init__.py`
- `app/application/progress_engine/engine.py` — `ProgressEngine`
- `app/application/progress_engine/dto.py` — Study Progress / position / projection / Twin input / advance decision
- `app/application/progress_engine/exceptions.py`
- `tests/test_sr003_progress_singularity.py`
- `SR003_PROGRESS_SINGULARITY_REPORT.md` — this report

## Files Modified

- `app/application/config/v2_flags.py` — `SR_PROGRESS_SINGULARITY` (default OFF)
- `app/application/educational_runtime_engine/service.py` — Progress Engine authorisation on `complete_mission`; `get_study_progress`; `get_mission_progress_inputs`
- `app/infrastructure/adapters/learning_session/runtime_engine.py` — Progress Engine advance gate; optional Study Progress attachment on session complete

**Not modified (by design):** Evidence evaluation rules, Twin estimation math, Mission redesign, Adaptive AI, Recommendation engine, LearningSessionRuntime FSM, JSON curriculum adapter (SR-003b).

---

## Tests

`tests/test_sr003_progress_singularity.py` (17 tests):

| Layer | Coverage |
|---|---|
| **Unit** | Accepted advances; Rejected ignored; Partial/No blocked; deterministic coverage; unique current topic; objectives roll-up; Twin absence; Twin optional annotations; no revalidation |
| **Authority** | Sole-writer registry rejects duplicates; Progress Engine authority id; opaque Study Progress contract |
| **Acceptance** | Flag default OFF; enables with env; rollback OFF retains derive capability |

### Tests Executed

```bash
python3 -m pytest tests/test_sr003_progress_singularity.py \
  tests/test_sdt004_twin_activation.py \
  tests/test_ev001b_evidence_gate.py \
  tests/domain/educational_runtime_engine/test_lifecycle.py -q
# 66 passed

python3 -m ruff check app/application/progress_engine/ \
  app/application/educational_runtime_engine/service.py \
  app/application/config/v2_flags.py \
  app/infrastructure/adapters/learning_session/runtime_engine.py \
  tests/test_sr003_progress_singularity.py
# All checks passed
```

---

## Examples

### Accepted Educational+ (Progress advances)

```
Observations: EV-RT-07 (practice correct), Finish Review Yes
Disposition: accepted
may_advance_progress=True
SR_PROGRESS_SINGULARITY=ON
→ ProgressEngine.authorise → may_advance=True
→ Mission Completed + TOPIC_COMPLETED
→ Study Progress: coverage↑; current topic advances uniquely
→ Twin may update independently (P5); optional estimate feeds projection only
```

### Rejected reading-only (Progress ignores)

```
Observations: EV-RT-03 (reading completed), Finish Review Yes
Disposition: rejected / reading_only_package
→ ProgressEngine → rejected_evidence_ignored
→ No TOPIC_COMPLETED; coverage unchanged
```

### Twin absence

```
Accepted practice package; no Twin / SR_TWIN_DAILY_LOOP=OFF
→ Coverage advances from evidence alone
→ projection_basis=coverage_only; twin_present=False
```

### Twin estimates optional

```
Coverage: t1 completed → current=t2
Twin: estimated_mastery t2=0.2, t3=0.8
→ Coverage still 1/3 (Twin does not invent completion)
→ projection weak_topic_ids=(t2,); mission inputs include weak hint
```

### Flag OFF rollback

```
SR_PROGRESS_SINGULARITY=OFF
→ Legacy complete_mission advance_progress path remains
→ Event history retained; ProgressEngine.derive still available for reads
```

---

## P6 Exit Criteria

| Criterion | Status |
|---|---|
| One Progress Engine | **Met** — `ProgressEngine` AUTHORITY |
| Consumes Accepted evidence / mission / curriculum / optional Twin | **Met** |
| Produces coverage, current topic, completed topics, position, projections | **Met** |
| No second educational state | **Met** — authorities not inverted; sole-writer registry |
| Accepted evidence advances progress | **Met** (tests) |
| Rejected evidence ignored | **Met** (tests) |
| Twin absence supported | **Met** (tests) |
| Twin estimates optional | **Met** (tests) |
| Coverage deterministic | **Met** (tests) |
| Current topic unique | **Met** (tests) |
| No duplicate progress writers | **Met** (registry + claim on singularity) |
| Rollback | **Met** — flag default OFF; events retained |
| Gate **G-Progress** (engine half) | **Met** for published path derivation + advance singularity |
| JSON subject smoke via Curriculum Source Adapter | **Deferred** to SR-003b |
| Coexistence cutover registry (dual-OS retirement) | **Deferred** to SR-003b / P7 |

---

## Recommendation for P7 Readiness

**Proceed to SR-003b (curriculum source adapter) before full P7 retirement.**

1. **SR-003b** — Feed JSON-bundled curricula into the same Progress Engine DTOs / Mission → Session → Evidence pipeline; shrink `RuntimeCoexistencePolicy` toward a subject cutover registry.  
2. **EducationalStateService audit** — Ensure Experience read models project from Progress Engine Study Progress when singularity is ON (no silent dual progress projections).  
3. **P7** — Retire legacy TopicProgress writers, Mark-complete Primary defaults, and coexistence dual-OS semantics only after G-Progress + subject cutover gates are green.  
4. **Do not** start Home continuity craft (SLJ-003 / DX-005 polish) until Progress singularity + adapter cutover are proven for published CS1.

Enable path for dogfood:

```
SR_SESSION_PRIMARY=1
SR_EVIDENCE_GATE=1
SR_TWIN_DAILY_LOOP=1   # optional; Progress does not require Twin
SR_PROGRESS_SINGULARITY=1
```

---

## Migration Impact

**None.** No Alembic revisions. Progress remains event-sourced; singularity is a behavioural flag over existing `TOPIC_COMPLETED` history.

---

## Architecture Compliance

- Layering preserved: Progress Engine is application AUTHORITY; domain `derive_progress` remains pure; Session Experience / runtime engine remain adapters.  
- Curriculum V1/V2 loadability untouched.  
- One Educational State: Progress does not become Evidence or Twin; Twin does not author coverage.  
- Traversal / import compatibility: N/A (no curriculum JSON mutation).

---

## Technical Debt

- Sole-writer registry is process-scoped (sufficient for singularity assertion in-app / tests; not a distributed lock).  
- Session-complete Study Progress attachment fail-opens when enrolment projection is unavailable (unit tests without DB).  
- Legacy TopicProgress / Runtime A dual-read paths still exist until SR-003b / P7.  
- `EducationalStateService` not yet forced to consume `StudyProgress` exclusively.

---

## Known Limitations

- JSON Curriculum Source Adapter (SR-003b) not implemented in this programme.  
- Mission Engine redesign / adaptive selection out of scope.  
- Progress projections annotate weak topics; they do not select tomorrow’s mission.  
- Full G-Progress subject cutover registry + coexistence dual-OS retirement remain P7 / SR-003b work.
