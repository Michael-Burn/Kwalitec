# Recommended Action

**Programme:** EV-002  
**Constraint:** No implementation authorised in EV-002. Actions below are sequencing recommendations only.

---

## Immediate

1. **Do not treat EV-001 and FV-001B Final as contradictory proof about one runtime.**  
   Record Case D (environment mismatch) as the reconciliation.

2. **Invalidate FV-001B Final as a verdict against the EV-001-verified code image.**  
   Keep its UX findings as *symptoms observed on a stale/polluted environment*, useful as regression probes after a clean re-run — not as proof that post–PI-002R Ready is unreachable.

3. **Do not start FV-001C** until a clean Founder re-validation issues GO or GO WITH CONDITIONS (unchanged from FV-001B Final exit).

---

## Required re-run protocol (Founder Studio)

Before the next FV-001B Final (or equivalent) judgement:

| Control | Requirement |
|---|---|
| Process | Start a **new** Flask process from the intended commit/tree; **do not** reuse long-lived `:5130`/orphan listeners |
| Reload | Prefer `--no-reload` only after confirming start time ≥ last relevant code edit |
| Database | Dedicated empty SQLite (`DATABASE_URL` set); do not reuse `instance/kwalitec.sqlite3` with prior CS1* debris |
| Migrations | Confirm Alembic revision matches intended head (today: `202607280080` or newer if advanced) |
| Fixtures | Document PDF paths + SHA-256; prefer the EV-001 CS1V fixture set **or** an explicitly approved Founder pack — do not silently change chapter/LO density mid-comparison |
| Evidence | Capture `base` URL, `DATABASE_URL`, process start timestamp, and `git rev-parse HEAD` in the walk JSON |

---

## Optional confirmation (engineering, still no product redesign)

- Repeat the EV-001 happy path on the **same** fresh process/DB recipe used for the Founder re-run (sanity that Ready still holds).  
- If that fails, open a new defect programme (possible Case E / residual PI-002).  
- If that passes and Founder re-run still fails on identical env+fixtures, then reclassify (likely Case E or product UX blockers independent of environment).

---

## Product follow-ups (out of EV-002 scope)

Already known from EV-001 / FV surfaces; schedule separately:

- Student Choose Exam `_format_release` datetime/string handling  
- Stale NEXT STEP after documents Ready  
- CIP syllabus `missing_learning_objective` warning vs Founder “blocking” language clarity  
- Ensure Approve failures never surface Publish verbs on the intended code image  

---

## Exit for EV-002

EV-002 is complete: first divergence identified (Validate), evidence reconciled under **Case D**, recommendation issued. No application changes were made.
