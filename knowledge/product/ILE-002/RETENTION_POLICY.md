# Decision Journal Retention Policy

**Programme:** ILE-002 — Decision Journal  
**Version:** 1.0  
**Status:** Active  
**Companion:** [`DECISION_JOURNAL_PHILOSOPHY.md`](DECISION_JOURNAL_PHILOSOPHY.md)  

---

## Retention principle

Educational memory is retained so continuity and trust can survive across sessions, plan refreshes, and soft archives.

**Default:** Journal entries and appended evidence events are retained for the life of the learner account.

---

## Soft archive

- `archived` status hides nothing destructive.  
- Entries remain readable in the timeline (`include_archived=True` by default).  
- Archive must never delete rows.

---

## Plan deletion / continuity

Decision Journal preference history and educational narrative survive study-plan deletion (Educational Continuity Standard). Journal rows are keyed by `user_id`, not by plan id.

---

## Backup / export

`DecisionJournalEntry` is included in settings backup model list (`decision_journal_entries`) so learners can export their educational memory alongside preference `decisions` rows.

Evidence event rows are retained with the parent entry via foreign key; a future export enhancement may serialise them explicitly.

---

## Erasure

Account-level erasure (when productised) must treat journal rows as personal educational data. Until an explicit privacy programme defines erasure UX, do not silently purge journal history for “storage hygiene.”

---

## Not retained here

Clickstream, performance telemetry, and Adaptive Assessment item-level traces are **out of scope** for this journal and follow their own retention rules.
