# PX-001 — Redundancy Audit

**Programme:** PX-001 Product Experience Elevation  
**Date:** 2026-07-31

---

## Principle

Every piece of information appears exactly once on a given view (or once per progressive disclosure layer).

---

## Hotspots found

| Element | Where it repeated | Resolution |
|---------|-------------------|------------|
| Subject name | Home mission hero + Progress signals | Progress hides subject when mission shows it |
| Duration | Mission hero + signals | Already omitted from signals (UX-001) |
| Learning objective | Home + Overview context + briefing wall | Briefing collapsed under “Session details” |
| Mission / topic title | Home, Overview H1, Tutor, Revision | Acceptable across routes; removed intra-page duplicates |
| “Revision supports Mission…” | Revision body + empty context + Help | Removed from Revision body/empty; Help may teach once |
| Epistemology bridge | History intro linking Journal/Timeline/Journey | Removed; optional Journey teaser retained once |
| Empty-state context lines | `ds_empty_operational` context on many pages | Context parameter no longer rendered |
| “Why this is empty” | Legacy `educational_empty` | Removed from macro render path |
| Feedback Hub essay | H1 + long description of hub behaviour | Shortened to one guiding sentence |
| Students vs Participants | Nav label vs page H1 | Aligned to **Students** |
| Footer philosophy | “Reduce decisions. Increase learning.” | Replaced with quiet “Study with focus.” |
| Settings intro | Explained where progress lives | Short preferences line only |

---

## Still acceptable cross-surface repeats

- Topic title on Home and again on Session (different screens, continuity).
- Subject on Syllabus page (that page’s job).
- Version strings on Console Settings and Releases (operator identity).

---

## Follow-ups (no new features)

- Sitting Report: audit objective / insight repeats within the complete surface.
- Platform Intelligence: section labels still engineering-dense (nested tool).
- Help glossary vs FAQ: some terms defined twice — slim in a later PX pass if dogfood confirms friction.
