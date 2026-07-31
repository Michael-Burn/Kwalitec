# RF-002 — Release Recommendation

**Programme:** Release Verification Programme RF-002  
**Phase:** Educational System Acceptance — Release Recommendation  
**Date:** 2026-07-31  
**Authority:** RF-001 · BF-001 · RF-001A · SB-001A · RF-002 verification evidence

---

## Recommendation

# GO FOR G1 FOUNDER VALIDATION

**(Candidate educational system — with deployment preconditions)**

The RF-002 candidate demonstrates a coherent educational lifecycle after Student Baseline integration. A learner can begin from a truthful declared position, receive Twin initialisation and Runtime entry without a second intake, continue across sessions, and keep history intact. That is sufficient educational grounds to open **G1 Founder Validation**.

---

## Why GO

Judged as Head of Education — not as a software ledger:

1. **One origin.** Baseline replaces Calibration theatre. The student is asked once where they are and where they want to go.
2. **Memory.** Twin birth + Study Plan / enrolment retain that origin; logout and interruption do not erase it.
3. **Continuity.** Missions do not duplicate; plans deactivate rather than fork; Baseline restart never destroys attempts.
4. **Both runtimes share the conversation.** Runtime A and Runtime C start from the same Baseline; engines themselves were not redesigned.
5. **No Category A educational defects** remain on the candidate for the verified lifecycle.
6. **Founder can inspect and safely reset** Baseline without annihilating learning history; Studio lifecycle remains operable post BF-001.

Evidence: `RF002_SYSTEM_VERIFICATION_REPORT.md` and companion RF-002 artefacts; 271+ green focused verification tests; mission/Twin/bridge suites.

---

## Why not unconditional live GO

Production still runs RF-001 tip `e4d5a1b`:

- `/baseline` is **404** on live — Baseline continuity is not yet what students experience in production.
- Alembic has **two heads** (`202607300005` and `202607310001`) — migrate is unsafe until merged.
- BF-001 Studio Expand/Collapse JS is still pending Manual Deploy (RF-001A R1).

Therefore: **recommend G1 on the candidate / post-cutover build**, not on today's live tip for Baseline claims.

---

## Deployment preconditions (must complete before live G1 Baseline dogfood)

1. Commit SB-001A + BF-001 + RF-002 reports (and related working-tree educational work).
2. Add Alembic **merge revision** for heads `202607300005` × `202607310001`.
3. Push `main` and **Manual Deploy** on Render.
4. Verify live:
   - Migrations at merge / SB-001A head
   - Authenticated `/baseline/` reachable
   - Studio JS `var byId = {}`
   - Availability → Baseline → Home smoke

---

## Accepted limitations (carry forward)

| Item | Status |
|------|--------|
| Thin Runtime C SCI seed (no Baseline→SCI overrides) | Accepted SB-001A debt |
| Runtime C Twin birth may honestly skip | Disclose; monitor TwinAbsent |
| Narrow Baseline gate (Home-centric) | Accept for G1 |
| Session finish → Sitting Report test drift | RF-001A Category D |
| Full-tree pytest residual (~159) | RF-001A accepted debt |
| No dedicated per-student Twin viewer | Inspect via Baseline `twin_snapshot_id` |
| Public `/health/details` | Prior accepted ops posture |

---

## What G1 should validate (Founder)

G1 is **Founder Validation**, not another engineering redesign. Ask:

1. Does Baseline feel like a tutor intake (not a form wall)?
2. After Baseline, does Home / Mission feel continuous with what was declared?
3. After leaving mid-session and returning, does the platform still feel like it remembers?
4. Does Founder Baseline inspect/reset behave safely (history intact)?
5. On production post-cutover: can a real subject be studied for several days without educational inconsistency?

If those hold in Founder hands, Version 1 G1 evidence collection may proceed under the Product Success / Release Frameworks.

---

## What not to open next

Per verification discipline:

- Do **not** redesign Runtime C, SCI, recommendations, Study Plans, or Twin architecture as a follow-on to RF-002.
- Do **not** open a full-tree pytest-zero programme as a substitute for G1.
- Do **complete** the deployment preconditions above before claiming live Baseline continuity.

---

## Final educational statement

Kwalitec’s educational system, on the RF-002 candidate, now behaves like a tutor who has taken notes: it knows where the student began, does not ask again, and continues from retained progress. That principle holds across the verified lifecycle. **Recommend the system for G1 Founder Validation** once the deployment cutover places that same behaviour in the Founder’s live daily path.
