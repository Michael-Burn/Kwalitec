# PX-004 — Error Experience Report

**Programme:** Product Experience Programme PX-004 — Premium Craft & Release Polish  
**Date:** 2026-07-31

---

### Principle

Every recoverable error answers: What happened? What should I do next? No blame. No engineering vocabulary on primary surfaces.

### Notifications audited

| Category | Treatment |
|----------|-----------|
| Success | What happened + next step (retained PX-003 continuity pattern) |
| Warning | Recovery path; “try again” preserved for contracts |
| Error / danger | Token styling via `.ds-flash--danger` |
| Information | `.ds-flash--info` / `--message` |

### Copy corrections

| Before | After |
|--------|-------|
| “educational calibration, not engagement scoring” | “helps us improve how we guide your study” |
| `str(exc)` on curriculum readiness | Fixed friendly curriculum-not-ready copy |
| “gate publication” / “blocking findings” / “immutable publication history” | Plain next-step language |
| “Curriculum Management and Ingestion” / “platform support” | “Studio service… contact support” |
| “publication readiness gates are incomplete” | “required steps are incomplete” |
| “Plan checklist updated.” | “Updated your session plan.” |
| “Advancement blocked — cannot enter {target} yet. Remaining tasks: …” | “Advancement blocked — finish N step(s) before {target}.” + marks + Next |
| Version field “immutable label for history and rollback” | “track published versions” |
| Session “Entering your study environment” | Calm continue tone |

### Forms

| Form area | Polish |
|-----------|--------|
| Feedback hub filters | Calmer placeholders; console primary Apply |
| Version assign | Softer DataRequired message |
| Disclosure focus | Restored visible focus for keyboard users |

### Empty states

| Page | Fix |
|------|-----|
| History | Single guiding sentence (no duplicate explanation) |
| Feedback hub | Intact guide empties (No matches / No feedback) |
| Students | Intact |

### Remaining error debt

1. Gate-blocked checklist still travels in the flash string (shortened; workspace panel remains the readable source).
2. Some Studio warning paths still mention CMP/syllabus by product necessity.
3. Raw domain exceptions elsewhere may still surface if uncaught — existing fail-open paths unchanged.

### No feature additions

Message strings and flash presentation only. Exception types and recovery routes unchanged.
