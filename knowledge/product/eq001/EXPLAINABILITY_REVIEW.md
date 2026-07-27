# EQ-001 — Explainability Review

| Field | Value |
|---|---|
| **Programme / Milestone ID** | EQ-001 |
| **Title** | Educational Quality Certification |
| **Date** | 2026-07-27 |
| **Reviewer** | Engineering |
| **Surfaces / contracts in scope** | Runtime C mission quality envelope; journey explanation; pacing projection notes |
| **Default explanation level(s)** | L1 mission; L2 journey |
| **Runtime A surfaces touched** | None |

---

## Mandatory verification

| # | Requirement | Pass / Fail / N/A | Evidence |
|---|---|---|---|
| R1 | Explanations are evidence-backed | Pass | Topic code, LO codes, prerequisite status, minutes in `supporting_evidence` |
| R2 | Confidence communicated appropriately | Pass | High when prereqs satisfied; Low/Suggested otherwise (`EQ-X03`) |
| R3 | Student action is clear | Pass | `suggested_next_action` on mission envelope |
| R4 | Avoid unnecessary technical detail | Pass | Forbidden-jargon check (`EQ-X05`); no Twin/pipeline speech |
| R5 | Consistent across Runtime A | N/A | Runtime A surfaces not modified; contract aligned to P-001.2 keys for future consistency |

## Schema checks

| # | Check | Pass / Fail / N/A | Evidence |
|---|---|---|---|
| S1 | Mandatory schema fields present | Pass | `EQ-X01` |
| S2 | Default level matches surface job | Pass | level_1 mission / level_2 journey |
| S3 | Reading-time targets | Pass | Short rationale sentences; not diagnostic dumps |
| S4 | EIP-003 four questions | Pass | Know (topic/LOs), Estimate (duration/pacing), Why (rationale), Next (action/unlocks) |
| S5 | Facts ≠ estimates ≠ advice | Pass | Completion definition states study progress ≠ mastery |
| S6 | Advice does not replace Learning Mode | Pass | Envelope describes authorised syllabus-order mission |
| S7 | Pattern catalogue | Pass | Syllabus-order mission / journey transition patterns in EQ explainability spec |
| S8 | Accessibility | N/A | No UI chrome in this programme |

**Outcome:** Pass  

**Notes:** Explainability is certified at the generation contract layer. Student-visible trust (K8) remains gated on a future surface programme consuming these envelopes.
