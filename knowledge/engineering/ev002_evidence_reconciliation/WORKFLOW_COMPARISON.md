# Workflow Comparison

**Programme:** EV-002  
**Sources:** EV-001 `lifecycle.json` + `STAGE_BY_STAGE_EVIDENCE.md`; FV-001B Final `phases.json` + `FOUNDER_STUDIO_REVIEW.md`.

---

## Stage table

| Stage | EV-001 (CS1V / :5141) | FV-001B Final (CS1F / :5130) |
|---|---|---|
| Create | Pass — subject + `ws-cs1v` Draft/Subject | Pass — subject + `ws-cs1f` Draft/Subject |
| Upload | Pass — CMP+Syllabus Ready; CIP extracted; preview cue ~23 topics | Pass — CMP+Syllabus Ready; CIP extracted; preview cue ~26 topics |
| Validate | **Pass** — “We've completed validation successfully”; `passed`; blocking 0 | **Fail** — “blocking findings remain”; `Validation needs attention · in_progress` |
| Preview | **Pass** — success + `ready_for_review · 23 topics` | **Fail / contradictory** — success “2 topics” + card `not_ready · 2 topics`; version label `preview_ready` |
| Approve | **Pass** — “We've approved…”; preview `approved` | **Fail** — Publish refusal flash; no approval confirmation |
| Publish | **Pass** — “We've published…”; Status Published | **Fail** — same Publish refusal; stage remains Content Sources |
| Ready | **Pass** — Subjects: Ready · Current Version 2026.1 · Published 2026-07-28 | **Fail** — `2026.1 · Content Sources`; no Ready / Published Date |

---

## User actions (aligned)

Both walks:

1. Login as `founder.studio@kwalitec.example`
2. Open Curriculum Studio / Subjects
3. Create subject (code + title)
4. Open workspace
5. Upload Official CMP then Official Syllabus via labelled file inputs
6. Wait until document STATUS Ready
7. Advance to Content Sources
8. Click Validate Curriculum
9. Click Build Preview
10. Click Approve Curriculum
11. Click Publish Verified Curriculum
12. Return to Subjects hub

FV additionally browsed Console nav (Review Queue, Publishing, Versions, Quality) before create — exploration only; no curriculum mutation.

---

## First divergence

**Stage: Validate.**

Prior stages (Create, Upload, structure visible) both Pass with Ready documents. From Validate onward the paths diverge and never reconverge.

---

## Notes

- EV-001 auto-heuristics in `lifecycle.json` marked publication `ok: false` despite UI/DB success; engineering correction in `engineering_analysis.json` is authoritative for EV Ready.
- FV automated checklist marked some preview/acceptance flags true while founder review correctly scored Validate/Preview/Approve/Publish/Ready as Fail — UI contradiction, not Ready achievement.
