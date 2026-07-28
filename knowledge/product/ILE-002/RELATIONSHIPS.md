# Decision Journal — Relationship Map

**Programme:** ILE-002 — Decision Journal  

---

## ILE-011 — Student Decision Framework

- Optional `catalogue_decision_id` stores catalogue IDs (e.g. `D-L01`).  
- Lifecycle respects learner agency: guidance is proposed; accept/defer are student actions.  
- Qualitative confidence bands match ILE-011 (Insufficient → High).  
- Journal does not invent a second decision engine.

## P-001.2 — Explainability Standard

- Entries permanently store Observation, Meaning, Recommendation, Evidence summary, Confidence, Expected benefit, Uncertainty, and later Outcome.  
- Student UI answers EIP-003-style questions without Level-3 internals.  
- See `ILE002_EXPLAINABILITY_REVIEW.md`.

## ILE-001C0 — Study Sensei Communication Framework

- Timeline copy and empty states follow Sensei voice: calm, evidence-first, no shame.  
- Forbidden engineering terms are enforced at write time (`assert_student_safe_text`).  
- Explanation arc mirrors ILE-001C0 default observation → meaning → action → benefit → uncertainty.

## EP-008.3 — Recommendation Commitment

- `RecommendationServiceDecisionJournalAdapter` continues to write legacy preference `decisions` rows and **mirrors** Mission tip commit/defer/complete into the educational journal (fail-open).

## Distinct from

| System | Distinction |
|---|---|
| Adaptive-engine `EducationalDecision` (`eos_decisions`) | Execution readiness aggregate — not student narrative |
| Decision Engine (`app/domain/decision/`) | Next-action selection — not journal |
| Product Decision Register | Board/product decisions — not learner memory |
| Analytics / telemetry | Observability — not educational continuity |
| Educational Timeline (ILE-003) | Interprets journal memories into a reflective story — does not store entries |

## Downstream

**ILE-003 — Educational Timeline** reads Decision Journal evidence to produce Observation → Pattern → Meaning → Reflection narratives. Journal remains the sole educational memory store.

**ILE-004 — Daily Mission Intelligence** composes today's primary Mission brief from authorised recommendations and records present / accept / defer / complete moments into the Decision Journal (fail-open). It does not invent a second journal.

**ILE-005 — Educational Feedback Loop** reviews recommendation outcomes using journal evidence, optional student reflection, and internal Sensei educational review records. It never rewrites journal history and never re-ranks tips.

