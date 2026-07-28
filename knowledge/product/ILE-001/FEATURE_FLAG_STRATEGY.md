# ILE-001A — Feature Flag Strategy

**Programme:** ILE-001 — Adaptive Assessment Experience  
**Milestone:** ILE-001A  
**Status:** Active  
**Effective:** 2026-07-28  
**Implementation:** `app/application/adaptive_assessment/feature_flags.py`

---

## Purpose

Progressive, reversible enablement of Adaptive Assessment product surfaces without educational logic changes.

---

## Flags

| Flag | Env key | Default | Meaning |
|---|---|---|---|
| Adaptive Assessment (master) | `KWALITEC_ADAPTIVE_ASSESSMENT` | OFF | Master product switch |
| Quick Check | `KWALITEC_QUICK_CHECK` | OFF | Session type |
| Deep Check | `KWALITEC_DEEP_CHECK` | OFF | Session type |
| Recovery Check | `KWALITEC_RECOVERY_CHECK` | OFF | Session type |
| Confidence Check | `KWALITEC_CONFIDENCE_CHECK` | OFF | Session type |
| Readiness Check | `KWALITEC_READINESS_CHECK` | OFF | Session type |

Truthy values: `1`, `true`, `yes`, `on` (case-insensitive).

Session types require the **master switch** plus their own flag.

---

## Subject-level enablement

| Env key | Behaviour |
|---|---|
| `KWALITEC_ADAPTIVE_ASSESSMENT_SUBJECTS` | Comma-separated subject codes allow-list |

- Empty (default): no subject restriction when master is ON.  
- Non-empty: only listed subject codes are eligible.

---

## Cohort rollout (future)

| Env key | Behaviour |
|---|---|
| `KWALITEC_ADAPTIVE_ASSESSMENT_COHORTS` | Comma-separated cohort ids allow-list |

- Empty (default): no cohort restriction when master is ON.  
- Non-empty: only listed cohorts are eligible (dogfood / alpha first).

Combined gate: `flags.is_available(session_type_id, subject_code=..., cohort_id=...)`.

---

## Rollout posture

1. **ILE-001A** — infrastructure only; all flags OFF in production.  
2. **ILE-001B** — enable master + Quick Check for dogfood cohort / selected subjects.  
3. Later types — enable independently after perception safety for Quick Check.  
4. Rollback — set master (or session flag) OFF; no schema dependency.

---

## Non-goals

Flags do not select items, update Twin belief, or change Mission planning math. They gate product surfaces only.

---

**End of FEATURE_FLAG_STRATEGY**
