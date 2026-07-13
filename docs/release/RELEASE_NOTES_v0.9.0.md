# Kwalitec v0.9.0

## Internal Alpha Baseline Reset and Educational Honesty

Version:

v0.9.0

Status:

Production

---

## Overview

Version 0.9.0 prepares Internal Alpha for a shared educational baseline after multi-version test data, and hardens curriculum binding and schedule-status honesty on the dashboard.

---

## Highlights

### Internal Alpha reset

`flask internal-alpha-reset` removes generated educational state (study plans, twins, progress, missions, attempts, decisions, subjects) while preserving users, password hashes, curricula, configuration, and Alembic history.

### Curriculum self-healing

Unbound study plans repair `curriculum_id` / `curriculum_version` transparently through `StudyPlanService` on dashboard and related accessors.

### Honest educational KPI status

Schedule / pace labels are derived only from owned evidence (calendar + TimeEngine hours balance). Reserved future slots remain unset until those algorithms exist.

### Dashboard and planning polish

KPI presentation, mission/study-plan path updates, and Internal Alpha enablement test coverage aligned with the healed curriculum journey.

---

## Operator notes

After deploy, run production reset once:

```bash
flask internal-alpha-reset --yes
```

Then confirm accounts still login, curricula remain imported, and educational history is empty before inviting participants to recreate Study Plans.

---

Thank you to everyone contributing to Kwalitec.
