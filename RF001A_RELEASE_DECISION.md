# RF-001A — Release Decision

**Programme:** Release Acceptance Programme RF-001A  
**Phase:** Founder Validation Release Decision  
**Date:** 2026-07-31  
**Authority:** RF-001 · BF-001 PASS · RC-002 · PX-004 PASS

---

## Recommendation

# GO WITH ACCEPTED DEBT

The RF-001A candidate build (RF-001 Founder Validation Build **plus** BF-001 Studio blocker remediation) is suitable for the Founder to use as a primary daily study system. Known residual issues do not prevent effective learning on the Student path. No unresolved Category A product defects remain in the candidate.

---

## Why not plain GO

Accepted debt remains material enough to name explicitly:

1. **159 full-tree pytest failures** — identical to RF-001; classified B/C/D only.
2. **BF-001 is verified in the working tree but not yet sealed on `main` / live** — production still serves broken Expand/Collapse JS until Manual Deploy (Risk R1).
3. Presentation polish debt from PX-003/004 (Pause duplication, History labels, Bootstrap islands).

These do not justify **NO GO** for daily study once BF-001 is cut over for any production Studio authoring the Founder needs.

---

## Why not NO GO

| Success criterion | Evidence |
|-------------------|----------|
| Complete regression executed | 45654 passed / 159 failed / 9 skipped in 321.67 s |
| Remaining failures classified | `RF001A_TEST_CLASSIFICATION.md` — **0 Category A** in candidate |
| Founder walkthrough succeeds | BF-001 + founder workflow/ops gates **PASS** |
| Student walkthrough succeeds | Student workflow + alpha smoke + V1S-008 **PASS** |
| Deployment verified | Live healthy at `e4d5a1b`; DB connected; migrations head; static 200 |
| No unresolved Category A in candidate | BF-001 PASS closes prior Studio blockers |
| Recommendation evidence-based | Comparison shows **zero new failures** vs RF-001 |

---

## Operational precondition (not a new programme)

Before the Founder relies on **production Curriculum Studio** authoring:

1. Commit BF-001 remediation + reports.
2. Push `main` and **Manual Deploy** on Render.
3. Confirm live `/static/js/curriculum_preview_tree.js` contains `var byId = {}` (not `Object`).

Student daily study on the already-deployed RF-001 tip is not blocked by R1; Studio Expand/Collapse on live is.

---

## Accepted limitations

Carried forward from `FOUNDER_VALIDATION_BUILD.md` / RF-001, plus RF-001A notes:

- Full pytest residual debt (unchanged 159).
- Public `/health/details`.
- Legacy Bootstrap Founder islands.
- Soft CSS/JS budget overrun.
- Manual Deploy process dependency.
- BF-001 restart retains upload facts (by design).
- Interactive browser console capture not available in this RF-001A agent environment (HTTP/static/Flask evidence used).

---

## Next programme

Per RF-001A final instruction — engineering pauses after this **GO WITH ACCEPTED DEBT**.

**Next:** **SB-001 — Student Baseline & Continuity**, then targeted verification **RF-002**, before G1 Founder Validation evidence collection.

Do **not** open additional engineering programmes beyond RF-001A for polish or full-tree zero.
