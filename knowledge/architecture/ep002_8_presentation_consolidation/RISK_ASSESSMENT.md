# EP-002.8 — Risk Assessment

**Milestone:** EP-002.8  
**Date:** 2026-07-26

| ID | Risk | Likelihood | Impact | Mitigation | Residual |
|---|---|---|---|---|---|
| R1 | Twin readiness mapping omits nuance vs EIP-003 prose | M | L | Map drivers + confidence + estimate labels; tests | Copy tone may differ — acceptable |
| R2 | Template AttributeError if narrative shape drifts | L | H | Always emit `ReadinessNarrative` / `MissionNarrative` | Low |
| R3 | Accidental third narrator | L | H | Facade selects only; no new speech engine | None if design held |
| R4 | EI + Insight both visible | L | M | Preserve mutual exclusion | TD-CO-02 accepted |
| R5 | Ownership drift into templates | L | H | No business logic in templates; tests | None |
| R6 | Production activation by mistake | L | H | Defaults OFF; no flag change in this milestone | Operational |
| R7 | Session routes inconsistently Twin | L | L | Intentional ORM-only; documented | Accepted |
| R8 | EP-002.7A artefact missing misread as incomplete soak | M | L | Document surrogate constitutional pack | Process |

**Overall presentation risk:** Low — presentation-only change with fail-open preserved.
