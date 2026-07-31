# PX-003 — Founder Walkthrough

**Programme:** Product Experience Programme PX-003 — Workflow Transparency & Confidence  
**Date:** 2026-07-31  
**Method:** Manual code-backed walkthrough of implemented Founder workflows only.

---

## Walkthrough 1 — Create Subject → Upload → Preview → Approve → Publish

| Step | Purpose | Visible outcome | Confidence before | Confidence after PX-003 | Next action |
|------|---------|-----------------|-------------------|-------------------------|-------------|
| Create Subject | Register syllabus subject | Form → workspace | Flash vague | Flash → upload next | Upload documents |
| Upload | Provide CMP + Syllabus | Upload cards + processing | Processing felt silent | Plain processing copy; Step 1 of 4 | Continue when ready |
| Preview | Inspect structure | Hierarchy tree when built | Empty felt dead; CTA mismatch | Empty explains; Generate preview CTA | Approve structure |
| Approve | Commit structure | Was copy-only | “What am I approving?” | Tree + counts visible | Assign version / Publish |
| Publish | Release to students | Thin status | Unclear outcome | Summary + ready line; flash on Home | Enrol from Subjects |

**Confidence drops closed:** CTA mismatch, invisible processing, Approve without preview, generic flashes, backend stage words on Studio index.

**Intentionally unchanged:** Gate logic, auto-advance, publish redirect to Home, no new Archive/Delete.

---

## Walkthrough 2 — Login → Dashboard → Subjects → Curriculum Studio → Settings

| Step | Purpose | Confidence notes | PX-003 change |
|------|---------|------------------|---------------|
| Login → Home | Current work | Supporting text empty; lifecycle queue labels | Supporting text + user progress labels (“Processing”, “Ready to publish”) |
| Subjects | Catalogue | Already founder-stage aware | Unchanged (already strong) |
| Curriculum Studio | Workspace index | Domain stage leak (`content_sources`) | Founder stage labels; next-step hint; empty guidance |
| Settings | Account + shortcuts | Lifecycle filters secondary | Documented as remaining debt; no new actions |

**Confidence drops closed:** Current Work “what should I do?”; Studio list stage vocabulary.

---

### Remaining Founder experience debt

1. Settings remains the home of lifecycle filter shortcuts.
2. Recent Publications still link to Subjects hub (not deep workspace).
3. Gate-blocked messages remain dense single flashes.
