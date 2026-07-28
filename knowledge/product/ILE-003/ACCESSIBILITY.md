# Accessibility

**Programme:** ILE-003 — Educational Timeline  

---

## Requirements

| Requirement | Implementation |
|---|---|
| Screen-reader compatible | Semantic `<nav>`, `<section>`, `<h2>`/`<h3>`, `<dl>` arc labels |
| Keyboard accessible | In-page section links; focusable section targets (`tabindex="-1"`); visible `:focus-visible` |
| Chronological navigation | Ordered lists per section; skip-nav list of section anchors |
| Readable typography | Existing student design tokens; calm line-height; italic only for reflection questions |

---

## Meaning not colour-only

Section labels, Observation / Pattern / Meaning / Reflection terms, and certainty status are textual. Timeline markers are decorative (`aria-hidden="true"`).

---

## Empty state

Empty Timeline uses `role="status"` with a clear title, description, and primary CTA to the Decision Journal.

---

## Tests

Presentation accessibility coverage lives in `tests/presentation/student/test_educational_timeline.py` (`TestEducationalTimelineAccessibility`).
