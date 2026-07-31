# EV-001B — Evidence Before Completion

**Programme:** EV-001B · SR-001A Phase P4  
**Date:** 2026-07-30  
**Nature:** P4 implementation — Evidence Before Completion gate  
**Authority:** SR-001 · SR-001A · EV-001A · LXP-003 · LXP-004A  
**Predecessor:** EV-001A (Educational Evidence Contract)  
**Successor:** SDT-004 / P5 Twin activation  

---

## Executive Summary

EV-001B wires the EV-001A Educational Evidence Contract into the Student Runtime. LearningSessionRuntime emits **candidate** educational observations throughout a sitting. On Finish Review, the runtime assembles one **Evidence Package**, and **EducationalEvidenceAuthority** alone returns **Accepted**, **Accepted with Restrictions**, or **Rejected**.

Mission completion and Progress advancement occur only when Authority authorises them. Explicit Finish Review Partially / No closes the session honestly without mission or coverage advancement. Twin remains read-only — no Twin mutation in this programme.

Flag: `SR_EVIDENCE_GATE` (default **OFF**).

---

## Architecture Changes

```
Mission → Study Session → Read → Example → Practice → Reflect
        → Finish Review
        → Evidence Package (Generated)
        → EducationalEvidenceAuthority (Validate → Accept / Reject)
        → Persisted package
        → Mission Complete + Progress (only when authorised)
        → Twin (deferred to P5)
```

| Concern | Owner |
|---|---|
| Candidate emission | LearningSessionRuntime / RuntimeEngine |
| Package assembly | `EvidencePackageBuilder` + `EvidenceBeforeCompletionGate` |
| Accept / Reject | `EducationalEvidenceAuthority` (sole Evidence Authority) |
| Session FSM | `LearningSessionRuntime` (Session Authority) |
| HTTP | Session Experience `/session/*` (ADAPTER) |
| Mission / TOPIC_COMPLETED | `EducationalRuntimeEngineService.complete_mission` |
| Product flag | `SR_EVIDENCE_GATE` |

Authorities preserved:

- **LearningSessionRuntime** — Session Authority  
- **EducationalEvidenceAuthority** — Evidence Authority  
- **Session Experience** — HTTP Adapter only  

---

## Evidence Package Model

`SessionEvidencePackage` carries one sitting:

| Field | Role |
|---|---|
| Mission / topic / curriculum identity | Attribution (C11) |
| Learning objectives | Sitting context |
| Candidate observations | EV-RT-* catalogue types |
| Finish Review | Yes / Partially / No |
| Session metadata | Duration estimates, phase |
| Provenance | `learning_session_runtime` |
| Validation result | Disposition + authority columns |
| Lifecycle state | Generated → Validated → Accepted/Rejected → Persisted |

Candidate types follow EV-001A exactly (`EV-RT-01` … `EV-RT-93`). Grade ceilings are assigned at Validation; consumers may not inflate them.

---

## Authority Integration

`EducationalEvidenceAuthority.validate_session_evidence_package`:

| Package shape | Disposition | Session | Mission | Progress | Twin |
|---|---|---|---|---|---|
| Practice (scored correct/incorrect) | Accepted | Yes | Yes | Yes | **No** (P4) |
| Practice attempted (unscored) | Accepted with Restrictions | Yes | Yes | Yes | **No** |
| Reading-only / reflection-only / duration-only / checklist-only | Rejected | No | No | No | No |
| Finish Review Yes alone | Rejected | No | No | No | No |
| Finish Review Partially / No | Accepted with Restrictions | Yes | No | No | No |

Twin catalogue methods (EIP-002 V1.0) are unchanged. EV-001B never calls Twin writers.

---

## Lifecycle

```
Generated → Validated → Accepted / Rejected → Persisted → Consumed
```

- **Generated:** candidates appended during begin / response / reflection / finish  
- **Validated / Accepted / Rejected:** Authority decision at session complete  
- **Persisted:** `lsr.evidence_package` document (C10 — not deleted on flag rollback)  
- **Consumed:** mission completion + optional `TOPIC_COMPLETED` when authorised  

---

## Files Created

- `app/application/learning_session/dto/candidate_observation.py`
- `app/application/learning_session/dto/evidence_package.py`
- `app/application/learning_session/evidence_package_builder.py`
- `app/application/learning_session/evidence_gate.py`
- `tests/test_ev001b_evidence_gate.py`
- `EV001B_IMPLEMENTATION_REPORT.md` — this report

## Files Modified

### Flags / Authority

- `app/application/config/v2_flags.py` — `SR_EVIDENCE_GATE`
- `app/services/educational_evidence_authority.py` — session package validation (EV-001A)

### LearningSessionRuntime (Session Authority)

- `app/application/learning_session/runtime.py` — `emit_candidate_observation`
- `app/application/learning_session/exceptions.py` — `EvidenceGateRejected`
- `app/application/learning_session/dto/__init__.py` — export package / candidate types

### Persistence / opaque engine

- `app/infrastructure/adapters/learning_session/persistence.py` — candidates + package docs
- `app/infrastructure/adapters/learning_session/runtime_engine.py` — emit + gate on complete

### Mission / Progress / Experience

- `app/application/educational_runtime_engine/service.py` — `advance_progress` / `evidence_package_id`
- `app/application/educational_experience/service.py` — gate blocks Mark-complete without package
- `app/application/session_experience/completion_service.py` — evidence rejection + mission metadata
- `app/presentation/student/routes.py` — Mark-complete blocked when gate ON
- `app/presentation/session/routes.py` — honest evidence rejection flash
- `app/presentation/session/messages.py` — `evidence_rejected` copy

---

## Tests Added

`tests/test_ev001b_evidence_gate.py` (23 tests):

| Layer | Coverage |
|---|---|
| **Unit** | Authority accept/reject; reading/reflection/duration/checklist-only; Partial/No; builder stage mapping; runtime emit |
| **Integration** | Practice package → mission + progress; reading-only blocked; Partial/No session close without mission |
| **Regression** | Twin never updated; gate OFF preserves P2/P3; persisted package survives conceptual rollback |
| **Acceptance** | Flag default OFF; G-Evidence enable; Home Mark-complete blocked when gate ON |

### Tests Executed

```bash
python3 -m pytest tests/test_ev001b_evidence_gate.py \
  tests/test_lxp003_session_product.py \
  tests/test_lxp004a_session_substance.py \
  tests/test_eip002_educational_evidence_authority.py -q
# 70 passed (EV-001B + LXP-003 + LXP-004A + EIP-002 regression)

python3 -m ruff check app/application/learning_session/ \
  app/services/educational_evidence_authority.py \
  app/infrastructure/adapters/learning_session/ \
  # …touched presentation/config modules…
# All checks passed
```

---

## Evidence Examples

### Accepted practice package (restrictions: Twin off)

```
Observations: EV-RT-03 (read), EV-RT-06 (practice attempted), EV-RT-23 (Yes)
Disposition: accepted_with_restrictions
may_complete_mission=True, may_advance_progress=True, may_update_twin=False
→ Mission Completed + TOPIC_COMPLETED; Twin unchanged
```

### Rejected reading-only

```
Observations: EV-RT-03 (read), EV-RT-23 (Yes)
Disposition: rejected / reading_only_package
may_complete_session=False
→ Session remains open; honest explanation to student
```

### Explicit Partial

```
Finish Review: Partially
Disposition: accepted_with_restrictions
may_complete_session=True, may_complete_mission=False, may_advance_progress=False
→ Session closes; mission remains educationally incomplete
```

---

## Migration Impact

**None.** Evidence candidates and packages persist via SessionDocumentStore opaque documents (`lsr.evidence_candidates`, `lsr.evidence_package`). No Alembic revision.

---

## Architecture Compliance

- Curriculum V1/V2 loadability unchanged.  
- LearningSessionRuntime remains Session Authority; Session Experience remains HTTP Adapter.  
- EducationalEvidenceAuthority remains sole Evidence Authority (C4).  
- Study ≠ understanding preserved (C2).  
- Twin after evidence deferred to P5 (C3 / C7 silence).  
- Non-authoritative packages rejected for Progress / Twin / understanding (C8).  
- Explicit Partial/No lawful honesty (C9).  
- Idempotent persistence — no delete on flag rollback (C10).

---

## Technical Debt

- Practice outcomes are typically Behavioural (attempted) until scored practice / LXP-005 assessment wiring yields Educational-grade EV-RT-07/08.  
- Mission completer fail-open logs when student_id is non-numeric (unit fakes); production spine uses numeric user ids.  
- Completion summary projection still understates evidence disposition until a follow-up surface polish.

## Known Limitations

- Twin birth/update intentionally out of scope (P5 / SDT-004).  
- Readiness formula unchanged.  
- Mission composition / assessment redesign unchanged.  
- Adaptive intelligence unchanged.  
- Gate default OFF — production enablement requires dogfood with `SR_SESSION_SUBSTANCE` ON so Accepted packages are educationally meaningful.

---

## P4 Exit Criteria

| Criterion | Status |
|---|---|
| G-Evidence — session → mission blocked unless Accept or explicit Partial/No | **Met** (when `SR_EVIDENCE_GATE` ON) |
| Automated accept / reject / Partial / No tests | **Met** |
| Home Mark-complete cannot emit unscoped TOPIC_COMPLETED without evidence | **Met** (blocked when gate ON) |
| Twin writes OFF | **Met** |
| Persisted rows survive conceptual rollback | **Met** |

---

## Recommendation for P5 Readiness

**Do not start SDT-004 Twin activation until:**

1. `SR_EVIDENCE_GATE` is dogfooded ON with `SR_SESSION_SUBSTANCE` ON for published CS1.  
2. At least one daily-loop path produces Educational-grade (scored practice / structured question) Accepted packages — or Board records residual Behavioural-coverage risk in writing.  
3. Twin writers consume only Authority-Accepted Educational+ observations on EIP-002 authorised sources.  

Prefer keeping the evidence gate ON and rolling back Twin (P5) rather than deleting evidence rows.

---

**End of EV-001B.**
