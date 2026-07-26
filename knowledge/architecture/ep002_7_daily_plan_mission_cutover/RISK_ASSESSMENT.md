# EP-002.7 — Risk Assessment

**Milestone:** EP-002.7  
**Date:** 2026-07-26

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Accidental production cutover | Low | High | Env hard-exclude + flags default OFF |
| R2 | Display topic ≠ session ORM topic (TD-DP-01) | Medium | Medium | Documented; alignment metrics; session still legacy ORM |
| R3 | Twin latency on dashboard/missions | Medium | Medium | P95 metrics; kill switch |
| R4 | MissionOptimizer accidentally re-wired | Low | High | Quarantine tests; source guards |
| R5 | Ownership drift / parallel mission engine | Low | High | Facade-only; no new engine |
| R6 | Double Twin assemble with Insights/Readiness | Medium | Low | Shared Foundation DI; independent ContextVars |
| R7 | Scope creep to Experience bridge | Medium | High | Explicit out-of-scope |

**Conclusion:** Residual risk dominated by display/persistence split (R2), acceptable for gated non-prod activation.
