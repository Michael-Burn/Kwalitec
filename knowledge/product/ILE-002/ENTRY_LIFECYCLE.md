# Decision Journal Entry Lifecycle

**Programme:** ILE-002 — Decision Journal  
**Version:** 1.0  
**Status:** Active  
**Companion:** [`DECISION_JOURNAL_PHILOSOPHY.md`](DECISION_JOURNAL_PHILOSOPHY.md)  
**Related:** ILE-011 [`DECISION_LIFECYCLE.md`](../DECISION_LIFECYCLE.md)  

---

## Lifecycle

```
Recommended
    ↓
Accepted  or  Deferred
    ↓
Evidence evolves (append-only)
    ↓
Reflection
    ↓
Outcome
    ↓
Archived
```

Statuses are product vocabulary stored on each journal entry.

| Status | Meaning |
|---|---|
| `recommended` | Guidance offered; no learner choice yet |
| `accepted` | Learner accepted the guidance |
| `deferred` | Learner deferred (or set aside) the guidance |
| `evidence_evolving` | New evidence appended after the original snapshot |
| `reflected` | Reflection closed the educational loop |
| `outcome_recorded` | What happened afterwards is known |
| `archived` | Soft archive; entry remains readable |

---

## Append-only evidence

When evidence changes:

1. Leave the original observation, meaning, and recommendation untouched.  
2. Append a `decision_journal_evidence_events` row with a student-safe summary.  
3. Optionally move lifecycle status to `evidence_evolving` when lawful.

Editing historical recommendation text is **forbidden**.

---

## Mapping to ILE-011 decision lifecycle

ILE-011 describes the Sensei–learner loop:

`Observation → Understanding → Guidance → Student action → Reflection → Updated understanding`

The Decision Journal **persists** the learner-visible parts of that loop for significant interactions. It does not replace Twin / Educational State updates; those remain owned by certified Educational Intelligence.

---

## Student action values

| Value | Label |
|---|---|
| `none_yet` | No choice recorded yet |
| `accepted` | You accepted this guidance |
| `deferred` | You deferred this guidance |
| `dismissed` | You set this aside |

Dismissal maps to deferred lifecycle posture for retention (lawful non-acceptance without shame).

---

## Reflection status

| Value | Meaning |
|---|---|
| `pending` | Reflection not yet recorded |
| `reflected` | Reflection note present |
| `not_applicable` | Reflection not required for this kind |

---

## Archive policy

Archiving never deletes. Archived entries stay in the timeline (optionally filterable). Retention: keep for the life of the learner account unless a future privacy programme defines a lawful erasure path that preserves educational continuity obligations.
