# EP-003.4 — Risk Assessment

**Programme:** EP-003.4 — Learning Feedback Loop  
**Date:** 2026-07-26  

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Feedback treated as mastery evidence | Medium | High | Claim boundaries; forbidden inference keys; docs |
| Fourth educational brain creep | Medium | High | Recorder has no decision API; STOP criteria documented |
| Student-path breakage from recorder failures | Low | High | Fail-open emitters; tests |
| Conflating Experience Feedback / Advisory Outcome / Learning Feedback | Medium | Medium | Distinct packages + architecture docs |
| PII / over-retention | Low | Medium | Process-local buffer; no email; capped deque |
| Over-claiming KSI from event availability | Medium | Medium | Under-claim ΔKSI; K6 gated on observation only |
| Revision adherence false positives from titles | Medium | Low | Title heuristic documented as limitation; prefer future explicit kind |
| Production accidental ON | Low | Medium | Default OFF; independent flag |

**Overall residual risk:** Acceptable for an observation-only milestone.
