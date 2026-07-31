# PX-001 — Information Architecture Audit

**Programme:** PX-001 Product Experience Elevation  
**Date:** 2026-07-31  
**Basis:** UX-001 PASS · RC-002 · V1S-008 PASS

---

## Method

For every primary screen: User · Primary Question · Primary Action · Secondary Information.  
Surfaces that answered multiple questions were flagged for split or demotion.  
Sections that did not support the screen purpose were flagged for removal.

---

## Student surfaces

| Screen | User | Primary question | Primary action | Secondary | Verdict |
|--------|------|------------------|----------------|-----------|---------|
| Home | Student | What should I do now? | Start / Continue Session | Progress, Tomorrow, Quick Actions | **PASS** after UX-001; Progress subject demoted when mission shows subject |
| Session Overview | Student | Am I ready to begin? | Begin Session | Context, task, details | **Elevate** — briefing collapsed (progressive disclosure) |
| Session Activity | Student | What do I practice now? | Submit Answer | Feedback, stages | Keep |
| Reflection | Student | What do I take away? | Finish Session | Optional note | Keep |
| Summary | Student | Did I complete planned study? | Finish review | Notes | Keep |
| Sitting Report | Student | What happened in this sitting? | Return Home | Insights, links | Keep; watch density |
| Revision | Student | What should I strengthen? | Begin Revision | Alternatives, why-detail | **Elevate** — philosophy removed; detail collapsed |
| Syllabus (Journey) | Student | Where am I? | Return Home / Map | Progress, up next | Keep; empty guided |
| History | Student | What have I practiced? | Return Home | Trends, sessions | **Elevate** — epistemology bridge removed |
| My Learning Journey | Student | How has learning developed? | Back to History | Story, forecast, reports | **Elevate** — essay framing shortened |
| Tutor | Student | Why this Session? | Return / ask | Sources | Empty guided |
| Curriculum Map | Student | Where does today’s topic sit? | Explore map | Tree | Empty guided |
| Decision Journal | Student | What guidance did I receive? | Back to Home | Entries | Empty → one action |
| Educational Timeline | Student | How does guidance tell a story? | Open Journal | Sections | Empty → one action |
| Settings (profile) | Student | How do I adjust my account? | Edit groups | Account cards | **Elevate** — intro rewritten |
| Help | Student | How do I get unstuck? | Search / FAQ | Glossary | Keep as teaching surface; still dense |
| Choose Exam | Student | Which exam do I study for? | Select exam | Filters | Empty guided |

---

## Founder surfaces (primary nav)

| Screen | User | Primary question | Primary action | Secondary | Verdict |
|--------|------|------------------|----------------|-----------|---------|
| Home | Founder | What needs attention today? | Open current work | Queue, recent | Empty philosophy removed |
| Subjects | Founder | Which subject do I open or create? | Create / open | Filters | Keep |
| Curriculum Studio | Founder | Which workspace do I advance? | Open workspace | List | Support shortened |
| Workspace | Founder | How do I complete this publication? | Stage primary | Health, supporting, technical | Keep staged model |
| Students | Founder | Who is studying? | Feedback / award | Roster | **Elevate** — label aligned to Students |
| Feedback | Founder | What feedback needs triage? | Open row / specialist | Filters | **Elevate** — Hub essay shortened |
| Settings | Founder | Where do I configure or go next? | Open destination | Ops links | Description shortened |

---

## Secondary Founder destinations (Settings)

Many secondary pages still mix programme vocabulary (Runtime Health, Evidence Gates, Dual-run).  
**IA rule:** keep them nested under Settings; do not promote to primary nav; copy cleanup is progressive, not a feature expansion.

---

## Splits already enforced

- Home vs Session Overview (UX-001) — decision vs briefing.
- Feedback Hub vs Product Check-in — browse vs triage.
- Subjects vs Curriculum Studio — catalogue vs execution.

---

## Residual IA risks

1. Help still teaches multiple conceptual models on one page.
2. Sitting Report remains dense (report surface by nature).
3. Secondary Console pages retain engineering labels — acceptable only as nested operator tools until Founder Validation.
