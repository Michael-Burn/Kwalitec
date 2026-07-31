# SDT-004 — Student Digital Twin Activation

**Programme:** SDT-004 · SR-001A Phase P5  
**Date:** 2026-07-30  
**Nature:** P5 implementation — Twin as consumer of Accepted Educational+ evidence  
**Authority:** SR-001 · SR-001A · EIP-002 · EV-001A · EV-001B  
**Predecessor:** EV-001B (Evidence Before Completion)  
**Successor:** SR-003 / P6 Progress singularity  

---

## Executive Summary

SDT-004 activates the Student Digital Twin as an **observer** of Educational Evidence Authority decisions. After a sitting Evidence Package is Accepted with Educational+ grade, and only when `SR_TWIN_DAILY_LOOP` is ON, the Twin ingests authorised scored observations and recalculates **Estimated Knowledge** and **Estimated Mastery** deterministically via `StudentTwinEngine`.

The Twin never evaluates evidence. Rejected, Behavioural-only, Informational, reading-only, and reflection-only packages are ignored. Mission Runtime and Progress advancement remain Authority-driven and independent of Twin writes. Flag default: **OFF**.

```
Mission → Study Session → Evidence Package
        → EducationalEvidenceAuthority (Accept / Reject)
        → Mission Complete + Progress (when authorised)
        → Student Digital Twin (Educational+ only; P5 flag ON)
```

---

## Twin Architecture

| Concern | Owner |
|---|---|
| Evidence Accept / Reject | `EducationalEvidenceAuthority` (sole Evidence Authority) |
| Twin consumption gate | `validation.may_update_twin` + `SR_TWIN_DAILY_LOOP` |
| Evidence → Twin mapping | `SessionTwinEvidenceConsumer` |
| Knowledge / Mastery math | `StudentTwinEngine` (deterministic recalculation) |
| Twin persistence | `DailyLoopTwinPersistence` (`sdt.daily_loop_twin`) |
| Session completion wiring | `LearningSessionRuntimeEngine` (adapter; FSM unchanged) |
| Mission / Progress | Unchanged EV-001B path |

**Invariant:** Twin observes; EducationalEvidenceAuthority remains the sole authority on educational evidence.

```
Accepted Educational+ package
        │
        ▼
SessionTwinEvidenceConsumer.consume
        │  trusts may_update_twin (no re-evaluation)
        │  maps only Educational+ EV-RT-* → EvidenceEvent
        ▼
StudentTwinEngine.ingest_evidence → recalculate
        │
        ▼
DailyLoopTwinPersistence (Initialised → Active)
```

Twin status:

| Status | Meaning |
|---|---|
| **Initialised** | Birth Twin created for learner/subject scope |
| **Active** | At least one Educational+ event ingested |

Gate **G-Twin:** Twin Active (or Initialised then Active) after first lawful Educational+ session evidence when the flag is ON.

---

## Evidence Consumption

### What updates the Twin

| Package shape | Authority | `may_update_twin` | Twin |
|---|---|---|---|
| Practice correct / incorrect / structured question | Accepted | **True** | Updates (flag ON) |
| Practice attempted (unscored) | Accepted with Restrictions | False | Ignored |
| Reading-only / reflection-only / duration-only | Rejected | False | Ignored |
| Finish Review Partially / No | Accepted with Restrictions | False | Ignored |
| Finish Review Yes alone | Rejected | False | Ignored |

### Mapping (Educational+ only)

| Runtime type | Twin `EvidenceType` | Outcome / score |
|---|---|---|
| `EV-RT-07` Practice correct | `practice_result` | correct / 1.0 |
| `EV-RT-08` Practice incorrect | `practice_result` | incorrect / 0.0 |
| `EV-RT-40` Structured question results | `assessment_outcome` | from payload |
| `EV-RT-41`…`44` Quiz / assessment / mock / official | `assessment_outcome` | from payload |

Behavioural and Informational observations co-present in an Accepted Educational+ package are **not** ingested.

### What the Twin must never do

- Revalidate or regrade packages (no second Evidence Authority)
- Update from Mark-complete, reading-only, reflection-only, duration, Finish Review alone
- Complete missions or advance Progress
- Teach or select tomorrow’s mission (observation-only)

---

## Knowledge Model

Estimated Knowledge and Estimated Mastery are Twin-owned beliefs derived solely from ingested EvidenceEvents:

| Estimate | Owner | Derivation |
|---|---|---|
| **Estimated Mastery** | `MasteryCalculator` + `MasteryPolicy` | Deterministic deltas from practice / assessment polarity |
| **Estimated Knowledge** | `StudentTwinEngine._knowledge_from_mastery` | Slightly lagged transform of mastery (+ soft signals only from Twin-admissible events) |

Same Educational+ event sequence → same Twin conclusions (reproducible). Persistence stores event history and reloads by replay so estimates remain deterministic after restart within the store.

Silence is preferred: when no Educational+ evidence exists, Twin-owned educational states stay unchanged.

---

## Files Created

- `app/application/student_twin/session_evidence_consumer.py` — Twin evidence consumer
- `app/application/student_twin/daily_loop_codec.py` — opaque Twin encode / replay decode
- `app/application/student_twin/dto/twin_consumption_result.py` — consumption result DTO
- `app/infrastructure/adapters/student_twin/daily_loop_persistence.py` — Twin document store
- `tests/test_sdt004_twin_activation.py` — P5 unit / integration / acceptance suite
- `SDT004_IMPLEMENTATION_REPORT.md` — this report

## Files Modified

- `app/application/config/v2_flags.py` — `SR_TWIN_DAILY_LOOP` (default OFF)
- `app/services/educational_evidence_authority.py` — `may_update_twin=True` for Educational+ Accepted packages
- `app/infrastructure/adapters/learning_session/runtime_engine.py` — Twin consume after Authority decision (fail-open)
- `tests/test_ev001b_evidence_gate.py` — scored practice asserts `may_update_twin=True`

**Not modified (by design):** Mission Runtime completion semantics, Progress Engine redesign, LearningSessionRuntime FSM, adaptive mission composition, evidence evaluation rules beyond Twin column activation.

---

## Tests Added

`tests/test_sdt004_twin_activation.py` (19 tests):

| Layer | Coverage |
|---|---|
| **Unit** | Accepted Educational+ updates Twin; Rejected / Behavioural / reading / reflection / informational ignored; flag OFF silence; incorrect practice; reproducible estimates; Twin does not revalidate |
| **Authority** | Educational+ `may_update_twin=True`; behavioural False; structured questions True |
| **Integration** | Scored practice → Twin + Progress; behavioural practice → Progress without Twin; reading-only blocked, no Twin; Twin flag OFF preserves Progress |
| **Acceptance** | `SR_TWIN_DAILY_LOOP` default OFF; enables with env |

### Tests Executed

```bash
python3 -m pytest tests/test_sdt004_twin_activation.py \
  tests/test_ev001b_evidence_gate.py -q
# 42 passed

python3 -m ruff check app/application/student_twin/session_evidence_consumer.py \
  app/application/student_twin/daily_loop_codec.py \
  app/application/student_twin/dto/twin_consumption_result.py \
  app/infrastructure/adapters/student_twin/daily_loop_persistence.py \
  app/infrastructure/adapters/learning_session/runtime_engine.py \
  app/services/educational_evidence_authority.py \
  app/application/config/v2_flags.py \
  tests/test_sdt004_twin_activation.py
# All checks passed
```

---

## Twin Examples

### Accepted Educational+ (Twin updates)

```
Observations: EV-RT-07 (practice correct), Finish Review Yes
Disposition: accepted
may_complete_mission=True, may_advance_progress=True, may_update_twin=True
SR_TWIN_DAILY_LOOP=ON
→ Mission Completed + TOPIC_COMPLETED
→ Twin Active; Estimated Mastery / Knowledge for topic updated
→ Package lifecycle → consumed; twin_updated=True
```

### Behavioural practice (Progress yes, Twin no)

```
Observations: EV-RT-06 (practice attempted), Finish Review Yes
Disposition: accepted_with_restrictions
may_update_twin=False
→ Mission + Progress may advance
→ Twin unchanged (behavioural_package_ignored)
```

### Rejected reading-only

```
Observations: EV-RT-03 (reading completed), Finish Review Yes
Disposition: rejected / reading_only_package
→ Session close blocked; Twin untouched
```

### Flag OFF rollback

```
Educational+ Accepted package; SR_TWIN_DAILY_LOOP=OFF
→ Mission + Progress unchanged from EV-001B behaviour
→ Twin write skipped (twin_daily_loop_flag_off); prior Twin state retained
```

---

## Migration Impact

**None.** Twin daily-loop documents persist via SessionDocumentStore (`sdt.daily_loop_twin`). No Alembic revision. Flag rollback OFF stops new Twin writes and retains existing Twin documents (C10 retention posture).

---

## Architecture Compliance

- Curriculum V1/V2 loadability unchanged.  
- EducationalEvidenceAuthority remains sole Evidence Authority (C4).  
- Twin after evidence (C3); Study ≠ understanding (C2).  
- Twin does not teach or select missions (observation-only).  
- Mission Runtime / Progress writers unchanged in semantics; Twin consumption is additive and fail-open.  
- LearningSessionRuntime FSM unchanged; adapter wires Twin after Authority decision only.  
- EIP-002 V1.0 Twin catalogue respected (scored practice / structured question / reserved assessment types).

---

## Technical Debt

- Production session path still typically emits Behavioural `EV-RT-06` (attempted) until scored practice / LXP-005 assessment wiring yields Educational-grade outcomes on the default loop. Twin activation is ready; Educational+ density depends on scoring.  
- Daily-loop Twin store is opaque document persistence (same pattern as EV-001B evidence packages), not the calibration SQLAlchemy TwinRepository — intentional isolation for P5.  
- Enrolment-time Twin birth for all published curricula is soft / deferred; P5 births Twin on first lawful Educational+ consume (satisfies G-Twin Initialised→Active).

---

## Known Limitations

- Adaptive mission composition does not yet consume Twin estimates (P6+ / SR-003 soft).  
- Readiness formula and Home Twin theatre unchanged.  
- Session Experience twin port remains read-oriented; no new student-facing Twin chrome.  
- Flag default OFF — enable only after EV-001B dogfood with Educational+ packages available.

---

## P5 Exit Criteria

| Criterion | Status |
|---|---|
| Twin consumes only Accepted Educational+ evidence | **Met** |
| Rejected / Behavioural / Informational ignored | **Met** |
| Twin never becomes Evidence Authority | **Met** |
| Estimated Knowledge / Mastery update only after authorised evidence | **Met** |
| Mission Runtime unchanged | **Met** |
| Progress unaffected by Twin consumption | **Met** |
| Twin estimates reproducible | **Met** |
| Gate G-Twin (Active/Initialised after lawful Educational+ evidence, flag ON) | **Met** |
| `SR_TWIN_DAILY_LOOP` default OFF with retain-on-rollback | **Met** |

---

## Recommendation for P6 Readiness

**Proceed to P6 (Progress singularity) when:**

1. `SR_EVIDENCE_GATE` remains ON in dogfood with `SR_SESSION_SUBSTANCE` ON.  
2. At least one daily-loop path routinely produces Educational+ Accepted packages (scored practice or structured questions) so Twin updates are educationally meaningful — or Board records residual Behavioural-coverage risk.  
3. `SR_TWIN_DAILY_LOOP` dogfooded ON for published CS1 without Twin theatre or mission-selection claims.  
4. Progress Engine work treats Twin estimates as **optional inputs**, never as a second Progress writer or substitute for Evidence Before Completion.

Prefer rolling Twin OFF (`SR_TWIN_DAILY_LOOP=0`) over disabling the evidence gate if Twin behaviour needs rollback.

---

**End of SDT-004.**
