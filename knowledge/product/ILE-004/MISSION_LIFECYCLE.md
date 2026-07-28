# Mission Lifecycle

**Programme:** ILE-004 — Daily Mission Intelligence  
**Companion:** [`MISSION_PHILOSOPHY.md`](MISSION_PHILOSOPHY.md)  
**Related:** ILE-002 [`ENTRY_LIFECYCLE.md`](../ILE-002/ENTRY_LIFECYCLE.md); ILE-011 Decision Lifecycle  

---

## Product lifecycle

```
Created
  ↓
Presented
  ↓
Accepted
  ↓
Completed  or  Deferred
  ↓
Journal
  ↓
Timeline
  ↓
Next mission
```

| Phase | Meaning | System behaviour |
|---|---|---|
| Created | Brief composed from authorised evidence | Domain composition only |
| Presented | Learner sees today's Mission on Home | Idempotent Decision Journal `recommended` row |
| Accepted | Learner starts / commits | Existing commitment path + journal accept |
| Completed | Learner finishes the Mission | Journal outcome (Runtime C complete mirrors) |
| Deferred | Learner chooses not today | Commitment defer + journal deferred |
| Journal | Educational memory persisted | ILE-002 Decision Journal sole store |
| Timeline | Reflective story updates | ILE-003 reads journal; no duplicate store |
| Next mission | New day / new authorised tip | Fresh composition; no stale private model |

---

## Reflection after completion

Prompts invite:

- Was the mission appropriate?  
- What changed?  
- Should tomorrow be different?  

Answers belong in the Decision Journal when the learner records reflection — never as Twin mutation or ranking change.
