# Relationship to Decision Journal

**Programme:** ILE-003 — Educational Timeline  

---

## Division of responsibility

```
Decision Journal          Educational Timeline
─────────────────         ────────────────────
record / accept           read journal evidence
defer / reflect           detect patterns
append evidence           write narrative moments
outcome / archive         invite reflection
student chronology        educational story
```

Do **not** duplicate:

- Entry lifecycle transitions  
- Evidence append-only store  
- Commitment mirroring  
- Preference / mastery writes  

---

## Data flow

1. Student Experience / Mission surfaces write significant guidance via `DecisionJournalService` (ILE-002).  
2. ILE-004 Daily Mission Intelligence also records present / complete (and related) mission moments into the same journal.  
3. ILE-005 Educational Feedback Loop appends optional student reflection and internal Sensei reviews; Timeline still reads journal rows only (never Sensei governance tables).  
4. Educational Timeline loads owned journal rows for the current learner.  
5. Domain narrative builders emit sections only when evidence supports moments.  
6. Presentation renders `/student/educational-timeline` under History chrome.

---

## Related systems (distinct)

| System | Distinction |
|---|---|
| Decision Journal | Memory store — not interpreter |
| History recommendation narrative | Short recent-choice list — not full reflective timeline |
| Journey runtime timeline events | Runtime A mission/attempt projection — not ILE-003 journal narrative |
| Analytics | Observability — out of scope |
| Twin / readiness / Tutor | Unchanged by ILE-003 |

---

## Cross-links in UI

- History → Decision Journal and Educational Timeline  
- Decision Journal → Educational Timeline  
- Educational Timeline → Decision Journal (source entries)
