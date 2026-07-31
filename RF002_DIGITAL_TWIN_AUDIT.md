# RF-002 — Digital Twin Audit

**Programme:** RF-002 Educational System Verification  
**Phase:** Phase 4 — Digital Twin Verification  
**Date:** 2026-07-31  
**Verdict:** **PASS** on Runtime A birth path · **CONDITIONAL** for Runtime C published curricula (honest TwinAbsent allowed)

---

## Origin chain (authoritative)

```text
StudentBaseline (ORM — educational origin)
    → BaselineDeclarations
    → AlphaCalibrationDeclarations / StudentCalibrationContract
    → StudentCalibrationBuilder
    → BaselineTwinBirth
    → TwinRepository.persist_birth_twin (twin_snapshots)
```

Baseline is the durable educational origin. Twin birth reuses Capability 3.6–3.7 builders — **no second authorship path**.

---

## Verification matrix

| Check | Result | Evidence |
|-------|--------|----------|
| Twin birth on Baseline finalize | **PASS** | Coordinator `_birth_twin()` before plan/enrol; `BaselineTwinBirth.persist` |
| Twin persistence (immutable snapshots) | **PASS** | `tests/application/test_twin_repository.py` — birth makes current; succession |
| Twin reload | **PASS** | `tests/application/test_twin_provider.py` — retrieve / TwinAbsent honesty |
| Twin update after study | **PASS** | `tests/application/test_twin_update_coordinator.py` — evidence succession |
| Twin survives logout/login | **PASS** | Snapshot rows durable; Baseline stores `twin_snapshot_id` pointer |
| Twin survives session interruption | **PASS** | Snapshots not session-scoped; Session Experience separate |
| Duplicate birth blocked | **PASS** | Second birth same scope → `DUPLICATE` failure |
| Restart does not delete Twin | **PASS** | Supersede Baseline only; Twin rows retained |

---

## Field consistency (Baseline → Twin cargo)

| Concern | Carrier | Consistency |
|---------|---------|-------------|
| Current Position | Plan `curriculum_topic_code` / completed topics + Twin knowledge priors | Mapped via `build_plan_fields` / declared sections |
| Study Phase | Plan `current_stage` / `current_position` from experience | Brand new → not_started; revision → revising |
| Confidence | Baseline row + Twin provenance cargo (`confidence_kind: self_declared`) | Not diagnostic mastery |
| Objective | Contract `StudyObjective` + Baseline objective token in cargo | CONTINUE → FINISH_REMAINING; restart/recommend → FIRST_SIT |
| Attempt History | Contract previous_attempts + Twin performance domain | Thin at birth; grows via evidence pipeline |

Internal consistency rule verified: Twin does **not** invent Mid/High theatre or Estimated Knowledge at birth. Unknowns remain honest.

---

## Runtime A vs Runtime C

| Runtime | Twin birth | Notes |
|---------|------------|-------|
| Runtime A (JSON curriculum) | Expected success when curriculum loadable | Linked on Baseline `twin_snapshot_id` |
| Runtime C (published) | May return `twin_persisted=False` | Finalize still completes; student message is honest |

This is **accepted thin-bridge debt** from SB-001A — not a Category A defect for educational continuity of Baseline + enrolment, but it weakens Twin-authoritative intelligence until curriculum id resolution is reliable.

---

## Founder visibility

Founder Baseline inspect shows `twin_snapshot_id` on the student Baseline table. There is **no dedicated per-student Twin viewer** — aggregate Twin observability remains on alpha surfaces. Adequate for G1 inspection of origin linkage; deeper Twin UI is out of RF-002 scope.

---

## Educational judgement

The Twin remembers where the student declared they are, and evolves from study evidence rather than re-asking. That memory is durable across sessions. Where Twin birth cannot complete for a published curriculum, the platform continues honestly rather than fabricating a Twin — preferable to false confidence.
