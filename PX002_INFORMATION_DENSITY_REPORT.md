# PX-002 — Information Density Report

**Programme:** PX-002 Founder Console Experience Elevation  
**Date:** 2026-07-31

---

## Redundancy removed

| Surface | Removed |
|---------|---------|
| Home | Empty-state essays; dual explanation when title present |
| Students | Page description paragraph; eyebrow chrome |
| Feedback Hub | Page description; always-visible filter grid |
| Product Check-in | Page description; always-open Insight engine wall; always-visible advanced filters; Findings/Research footer prompts |
| Settings | Flat undifferentiated link dump; header essay |
| Curriculum Studio | Header support sentence |

---

## Hierarchy improvements

1. **One H1 per primary page** — ds-page headers without competing eyebrows where possible.
2. **Home layers** — Current Work (primary) → Waiting → Recently published.
3. **Feedback** — Table first; Filters and Patterns disclosed.
4. **Settings** — Account (immediate) → Advanced (grouped) → Studio shortcuts.
5. **Nav** — Workflow groups reduce equal-weight scanning of six peers plus secondary actions.

---

## Spacing / visual rhythm

- Console main padding increased slightly
- Nav group labels + consistent gaps
- Table header uppercase meta, roomier row padding
- Settings meta as definition list grid (not stacked bold paragraphs)
- Empty states use shared `ds-empty-operational` pattern

---

## Density challenge results

| Element | Keep? | Rationale |
|---------|-------|-----------|
| Home Current Work | Keep | Answers the page question |
| Waiting queue | Keep | Secondary attention list |
| Recently published | Keep | Confirms safe-to-ignore published work |
| Feedback source counts | Keep | Operational triage signal |
| Specialist links (Beta/Alpha/Check-in) | Keep | Route to required workflows without new features |
| Insight / Patterns panels | Disclose | Required RIP-004; not default focus |
| Advanced Settings tools | Keep nested | Functionality preserved; not primary chrome |
| Studio status shortcuts | Keep | Operational jump links |

---

## Remaining density debt

- Product Check-in detail panel still lists many fields (needed for triage)
- Advanced nested pages not slimmed in this pass
- Topbar still shows Internal Alpha badge + Account + Sign out (useful; left intact)
