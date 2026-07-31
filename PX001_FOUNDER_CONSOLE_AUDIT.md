# PX-001 — Founder Console Audit

**Programme:** PX-001 Product Experience Elevation  
**Date:** 2026-07-31

---

## Primary nav (managing workflows)

| Nav | Purpose | Remove / simplify |
|-----|---------|-------------------|
| Home | Today’s attention | Philosophy context on empty — **removed** |
| Subjects | Catalogue | Keep; empty already operational |
| Curriculum Studio | Execution index | Support shortened |
| Students | Roster | **Renamed from Participants**; empty guided |
| Feedback | Inbox | Hub essay shortened; Check-in description shortened |
| Settings | Destinations | Description shortened; keep nested ops links |

---

## Per-page findings

### Home
- **Keep:** Current Work (one primary), Publication Queue, Recent Publications.
- **Removed:** Curriculum philosophy under empty state.
- **Primary task:** Open or create the next curriculum step.

### Subjects
- **Keep:** Create, search, catalogue.
- **Low risk:** Help text for syllabus codes is operational guidance — retain.

### Curriculum Studio
- **Keep:** Workspace list → open.
- **Simplified:** Support line.
- **Workspace:** Stage strip + one primary remains correct IA.

### Students
- **Fixed:** H1/eyebrow “Participants” → **Students** (match nav).
- **Simplified:** Description and empty state.
- **Primary task:** Find a student and open feedback / recognition.

### Feedback
- **Simplified:** Hub and Check-in descriptions.
- **Keep:** Specialist links (browse vs triage split is useful).
- **Watch:** Insight engine disclaimer required by RIP-004 — retain for now.

### Settings
- **Simplified:** Header copy.
- **Keep:** Nested Operations & reports as progressive disclosure of secondary tools.
- **Distraction:** Dense secondary list — acceptable as a directory; do not elevate items to primary nav.

---

## Secondary pages (not elevated this pass)

Operations, Runtime Health, Platform Intelligence, Evidence Gates, Version 1 Readiness, Vision Journal, Findings, Search, Private Beta, Curriculum Health.

**Common issues:** engineering vocabulary, title/nav mismatches (Analytics/Research, Learning/Founder Intelligence), dual chrome (DS vs legacy founder-header).

**Rule:** leave nested; no new Founder functionality; language polish may continue post–Founder Validation.

---

## Navigation coherence

| Issue | Status |
|-------|--------|
| Students vs Participants | Fixed |
| Feedback vs Feedback Hub | H1 → Feedback |
| Support vs Feedback in `FOUNDER_PRIMARY_NAV_LABELS` | Constant still says Support — nav UI uses Feedback; align constant in follow-up if tests allow |
| Two “Operations” concepts | Documented; remain nested |

---

## What distracts from today’s work

Anything that explains Console architecture, dual-run readiness, or milestone programmes on primary pages. Primary pages now lead with the next curriculum or student action.
