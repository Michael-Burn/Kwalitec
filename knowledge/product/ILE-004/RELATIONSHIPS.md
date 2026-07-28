# Relationship Map — Daily Mission Intelligence

**Programme:** ILE-004  

---

## Upstream (read-only authority)

| System | Relationship |
|---|---|
| Decision Engine / Runtime A recommendation | Owns *what* is next; Mission Intelligence does not re-select |
| Recommendation / MES explanation | Supplies why, evidence, benefit, confidence, timeliness |
| ILE-001C0 / ILE-001C | Study Sensei voice and explainability arc |
| ILE-010 / ILE-011 | Sensei identity and decision responsibility |

## Downstream / siblings

| System | Relationship |
|---|---|
| Decision Journal (ILE-002) | Writes significant present / accept / defer / complete / reflect moments |
| Educational Timeline (ILE-003) | Reads journal memories; Mission Intelligence does not narrate history itself |
| Unified Journey / Home | Consumes the mission brief as centre of daily interaction |
| Capability 2.10 Mission Intelligence | Structural task operationalisation — distinct from this learner brief |
| Educational Feedback Loop (ILE-005) | Reviews mission/journal recommendation outcomes after completion; does not recompose or re-select the Mission |

## Non-duplication rule

No educational authority may be duplicated. Composition never invents a second reasoner, Twin store, or readiness score.

## Distinct from

| System | Distinction |
|---|---|
| `mission_engine` / `mission_engine_v2` | Scheduling / session wrapper lifecycle |
| Adaptive Assessment | Evidence gathering sessions — not daily primary Mission |
| Tutor | Explains authorised decisions; out of scope for ILE-004 UI |
