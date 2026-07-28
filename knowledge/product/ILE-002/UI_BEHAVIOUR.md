# Decision Journal UI Behaviour

**Programme:** ILE-002 — Decision Journal  
**Version:** 1.0  
**Status:** Active  
**Companion:** [`DECISION_JOURNAL_PHILOSOPHY.md`](DECISION_JOURNAL_PHILOSOPHY.md)  

---

## Surface

| Item | Value |
|---|---|
| Route | `GET /student/decision-journal` |
| Endpoint | `student.decision_journal` |
| Template | `app/templates/student/decision_journal.html` |
| Nav chrome | History (active) — journal is a History sibling, not a new primary nav item |
| Discovery | Link from History (“Open your Decision Journal”) |

---

## Timeline behaviour

- Newest first chronology.  
- Each entry answers: What happened? Why? What did I choose? What happened afterwards? What should I learn from this?  
- Expanded “Why this guidance” details expose evidence, expected benefit, uncertainty, and appended evidence updates.  
- Empty state is calm and invitational — never guilt.  
- Archived entries remain visible with muted treatment.

---

## Accessibility

- Page `lang`, viewport, and colour-scheme from the student shell.  
- One clear `h1` (shell title); timeline section has `h2`; entries use `h3`.  
- Timeline is an ordered list with `aria-label`.  
- Empty state uses `role="status"`.  
- Provenance uses native `<details>` / `<summary>` (keyboard operable).  
- Lifecycle and confidence are **text** labels — never colour alone.  
- Focus-visible styles on provenance summary.

---

## Copy tone (ILE-001C0)

- Calm, precise, warm.  
- Evidence-first; no hype, streak guilt, or comparative ranking as identity.  
- No engineering jargon on the page.

---

## Non-goals for this UI

- No accept/defer controls on the journal page itself (those remain on Home / commitment chrome).  
- No analytics charts or acceptance-rate dashboards for students.  
- No AI chat.
