# Lifecycle Verification

**Programme:** EV-001  
**Subject under test:** CS1V — Actuarial Statistics (EV-001 Verification)  
**Workspace:** `ws-cs1v`  
**Version:** 2026.1  
**Server:** `http://127.0.0.1:5141` (dedicated EV-001 SQLite DB)  
**Operator account:** `founder.studio@kwalitec.example`  
**Walk script:** `_evidence/ev001_lifecycle_walk.py`  
**Raw capture:** `_evidence/lifecycle.json`  
**Engineering correction:** `_evidence/engineering_analysis.json`

---

## Lifecycle matrix

| Transition | Required | Observed | Pass |
|---|---|---|---|
| Draft | Subject + workspace created | Created 2026-07-28 22:34:48 UTC; Stage Subject → Content Sources | ✓ |
| Validated | `validation_passed` / successful validate | UI: Validation completed successfully · passed; blocking = 0 | ✓ |
| Preview Ready | `ready_for_review` + validated | Preview ready · ready_for_review · 23 topics | ✓ |
| Approved | Approval success + preview approved | We've approved…; Preview ready · approved · 23 topics | ✓ |
| Published | Publish success + Management/Foundation published | We've published…; Status: Published · Version 2026.1 | ✓ |
| Ready | Subjects hub Ready + version + date | CS1V Ready · Current Version 2026.1 · Published 2026-07-28 | ✓ |
| Student Subject Catalogue | Discoverable Ready subject | Package active; Choose Exam 500 (`_format_release`) | ✗ UI |

---

## Stage notes

### Draft
Create Subject + Open Workspace succeeded without seeded state. Initial lifecycle presented as Subject / Content Sources Draft path with version assignment on upload (`2026.1`).

### Validated
Validate Curriculum succeeded on first attempt after documents Ready. Findings panel showed no blocking issues. Status line: `Validation completed successfully · passed`.

### Preview Ready
Build Preview succeeded with honest success flash and matching readiness: `ready_for_review` and 23 topics. PI-002R success semantics held (success only when ready + validated).

### Approved
Approve Curriculum succeeded; checklist advanced (6 of 8); preview readiness moved to `approved`.

### Published
Publish Verified Curriculum succeeded; workspace status became `Published`; Foundation package row created.

### Ready
Subjects catalogue row for CS1V showed Ready, Current Version, and Published date.

### Student Subject Catalogue
Engineering confirms active Ready package for CS1V. Visible Choose Exam path failed with:

```text
AttributeError: 'str' object has no attribute 'strftime'
  at SubjectCatalogueService._format_release
  via /study-plan/wizard/1
```

---

## Manual intervention check

| Constraint | Observed |
|---|---|
| No application code modified during verification | Held |
| No workflow gate bypass | Held |
| No manual DB publication edits | Held |
| No seeded publication facts | Held — package created only by Publish action |

---

## Overall lifecycle judgment

**Studio publication lifecycle:** PASS  
**Student visible catalogue:** FAIL (presentation bug)  
**Programme outcome:** see [`ENGINEERING_SIGNOFF.md`](ENGINEERING_SIGNOFF.md)
