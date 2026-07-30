# Private Beta Guide

**Version:** `2.0.0-beta.1`  
**Programme:** RC-001  
**Status:** Official Private Beta baseline

---

## Purpose

Run a controlled Private Beta with approximately **10–20 invite-only students** on a frozen, production-deployed build. Collect evidence of study usefulness — not feature requests for new educational architecture.

---

## Who is in scope

| Role | Responsibility |
|---|---|
| Founder / operator | Provision accounts, publish certified curriculum, enrol cohort, observe, triage feedback |
| Student | Sign in, onboard, study with Daily Mission / Session, use Tutor / Knowledge Map as needed, submit feedback |

Public self-registration remains **disabled**.

---

## Student journey (expected)

1. Receive invite credentials from Founder.
2. Sign in → complete onboarding / subject selection as prompted.
3. Land on Student Home → start **Today’s Mission** / session.
4. Complete at least one study session.
5. Optionally open **Tutor** and **Knowledge Map**.
6. Check **Journey / Progress**.
7. Submit feedback via **Report issue** (Private Beta feedback).

If any step fails with a platform error, report immediately with screen name and subject code.

---

## Founder journey (expected)

1. Sign in to Kwalitec Console (Founder).
2. Curriculum Studio: create/select subject → upload syllabus + CMP → run certification → publish.
3. Confirm Curriculum Health shows certified / published readiness.
4. Enrol participants on **Private Beta** dashboard.
5. Monitor feedback and record observations during sessions.
6. Generate end-of-beta report when the cohort window closes (PB-001 emitter).

---

## Feedback categories (PB-001)

Students should prefer concrete reports:

- Cannot start / continue studying
- Wrong or confusing recommendation
- Broken page or error
- Curriculum content mismatch
- Suggestion (non-blocking)

Founders triage severity from the Beta Dashboard. Critical defects that block studying are deployment blockers for continued beta; educational-quality wishes are deferred.

---

## Success signals (after real usage)

Tracked by PB-001 metrics (not claimed by RC-001 alone):

- Create study plans / begin learning
- Start a mission
- Complete a session
- Return within a week
- Zero critical platform bugs / data loss / certification corruption

---

## Explicit non-goals

Do **not** expand during Private Beta:

- New subjects beyond the certified publish set
- Tutor / mission / KG “smarter” redesigns
- Public marketing launch
- Commercial packaging

---

## Related

- `RELEASE_NOTES.md`
- `FOUNDER_DEPLOYMENT_GUIDE.md`
- `knowledge/product/private_beta/` (onboarding, support, privacy)
- `knowledge/engineering/pb001_private_beta_validation/`
