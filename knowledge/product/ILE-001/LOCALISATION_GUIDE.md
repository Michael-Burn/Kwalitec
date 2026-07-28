# ILE-001A — Localisation Guide

**Programme:** ILE-001 — Adaptive Assessment Experience  
**Milestone:** ILE-001A  
**Status:** Readiness only (English defaults; no translations)  
**Effective:** 2026-07-28  
**Implementation:** `app/application/adaptive_assessment/localisation.py`

---

## Purpose

Prepare Adaptive Assessment product resources for future localisation: externalised strings, pluralisation, and variable interpolation — without translating in this milestone.

---

## Catalogue

- Default locale: `en`  
- Built from the copy registry via `build_catalogue_from_copy_registry` / `get_default_catalogue`  
- Each entry: key, default string, optional plural forms, translator description  

---

## Interpolation

Use `{name}` placeholders:

```python
from app.application.adaptive_assessment import format_message, resolve_copy

format_message("Learning check: {session_name}", session_name="Quick Check")
resolve_copy("a11y.session_region", session_name="Quick Check")
```

Missing variables are left as `{name}` (tolerant) so incomplete wiring does not crash.

---

## Pluralisation

English subset: `one` vs `other`.

```python
from app.application.adaptive_assessment.localisation import format_pluralizable

format_pluralizable("duration.about_minutes", count=1)  # About 1 minute
format_pluralizable("duration.about_minutes", count=5)  # About 5 minutes
```

Mark copy entries with `pluralizable=True` when count-sensitive. Future locales can supply full CLDR categories without changing call sites.

---

## Rules

1. Do **not** hard-code learner-facing AA strings outside the registry.  
2. Do **not** translate in ILE-001A — English defaults only.  
3. Keep translator `description` notes non-student-facing.  
4. Terminology validation still applies to default English strings.

---

**End of LOCALISATION_GUIDE**
