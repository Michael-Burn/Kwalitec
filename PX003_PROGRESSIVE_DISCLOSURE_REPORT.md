# PX-003 — Progressive Disclosure Report

**Programme:** Product Experience Programme PX-003 — Workflow Transparency & Confidence  
**Date:** 2026-07-31

---

### Principle applied

Primary workflow content first → review summary → warnings → technical details last. Never the reverse.

### Founder Publication Workspace

| Layer | Content |
|-------|---------|
| L0 | Step X of Y strip, next-step sentence, single Primary |
| L1 | Stage content (upload / preview tree / approve review / publish summary) |
| Supporting | Validation/preview count lines (user language) |
| Disclosure | Document jobs (collapsed when present) |
| L3 Technical details | Workspace id, subject code, publication step, version history |

**Changes**

- Document jobs moved behind `<details>` so processing pipeline stays primary.
- Domain stage token removed from Technical details; shows Founder step label.
- Approve shows hierarchy before commitment (primary content, not buried).

### Student Session

| Layer | Content |
|-------|---------|
| Header | Eyebrow (Step N of M) + title + timer/estimate |
| Journey | Stage indicator (Overview → Activity → Reflection → Summary) |
| L0 | Learning task + primary |
| Overview briefing | Open by default — educational preview first |
| Complete | Headline, what studied, finish outcome, up next, History link |
| Complete disclosure | Assessment, strategy, reinforcement, journey links |

**Home (UX-001 preserved)**

- Why-now remains on Overview (not restored to Home MES stack).
- Home adds only “After this · …” for next-step confidence.

### Empty workflow states

| Empty | Guidance |
|-------|----------|
| No preview yet | What happened + generate next |
| No preview on Approve | Return to Preview |
| No workspaces | Create Subject + journey strip |
| History empty | Unchanged PX-001 pattern |

### Remaining disclosure debt

- Curriculum Health strip still light placeholder for Certification.
- Gate-blocked checklist still flash-only (not proactive L1 list).
