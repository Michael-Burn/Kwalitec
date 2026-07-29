# FV-001B Re-run — UX Defect Register

Severity: **Critical** (blocks publish), **Major** (trust / wrong path), **Minor** (polish).

| ID | Severity | Surface | Defect | Evidence |
|---|---|---|---|---|
| D-01 | Critical | Workspace · Validate | Validation fails with “blocking findings” while documents are Ready, overview shows 0 validation errors, and **no findings list** is shown | `phase5_validate_blocked.png`, `complete.json` C2 |
| D-02 | Critical | Workspace · Preview | Green success (“preview successfully — N topics”) coexists with “Preview needs attention · not_ready · N topics” | `phase6_preview_contradiction.png`, `phase6_preview_success_vs_not_ready.png` |
| D-03 | Critical | Workspace · Approve | **Approve Curriculum** returns a **Publish** refusal flash; approval never confirms | `phase7_approve_confused.png` |
| D-04 | Critical | Workspace · Publish | Publish never succeeds on dual-Ready subject; Founder cannot finish journey | `phase8_publish_refused.png` |
| D-05 | Critical | Subjects | Subject never reaches **Ready**; no published date after attempted publish | `phase9_subjects_not_ready.png` |
| D-06 | Major | Workspace · Status | Overview Topics (23) disagree with Preview line (2); Structure shows many topics | `phase6_structure_topics.png`, C3 captures |
| D-07 | Major | Workspace · NEXT STEP | NEXT STEP remains “upload / run validation after upload” after both docs Ready | `complete.json` C0–C5 |
| D-08 | Major | Workspace · Validate copy | Flash says “fix CMP/syllabus issues” when both slots already Ready | `phase5_validate_blocked.png` |
| D-09 | Major | Actions | Approve/Publish/Validate remain fully clickable while gates fail — learning-by-error | probe/complete controls |
| D-10 | Major | Incomplete Approve | Approve on empty workspace also shows Publish refusal wording | `complete.json` C7_incomplete_approve |
| D-11 | Minor | Document meta | “Uploaded by 38” | `phase4_both_docs_ready.png` |
| D-12 | Minor | Structure tab | “23 entities · 99 relationships” | `phase6_structure_topics.png` |
| D-13 | Minor | Studio activity | Machine event keys in recent activity | `phases.json` Studio captures |
| D-14 | Minor | Console Home | Curriculum CTA not first-viewport hero | `phase1_console_home.png` |
| D-15 | Minor | Upload UX | No explicit Upload button; auto-bind may surprise | Phase 4 notes |

---

## Counts

- Critical: 5  
- Major: 5  
- Minor: 5
