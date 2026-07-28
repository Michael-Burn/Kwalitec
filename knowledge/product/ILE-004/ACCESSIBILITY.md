# Accessibility — Daily Mission Intelligence

**Programme:** ILE-004  

---

## Requirements

| Requirement | Implementation |
|---|---|
| Landmark / labelled panel | `aside.student-mission-intelligence` with `aria-labelledby` |
| Heading hierarchy | Home hero `h2` remains primary; intelligence panel uses `h3` |
| Labels before content | Purpose, Why today, Evidence, Confidence, etc. use `.student-label` |
| Disclosure | Mission explanation in native `<details>` / `<summary>` |
| No colour-only meaning | Status and labels use text |
| Forbidden terms | Domain invariants reject engineering / engagement theatre leakage |
| Keyboard | Details/summary and existing Home CTAs remain operable |

## Tests

`tests/presentation/student/test_daily_mission_intelligence.py` asserts labelled headings and forbidden-term absence when the panel renders.
