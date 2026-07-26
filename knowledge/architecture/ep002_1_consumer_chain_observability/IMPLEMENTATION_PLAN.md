# EP-002.1 — Implementation Plan

**Milestone:** EP-002.1 — Consumer-Chain Observability & Twin Quarantine  
**Date:** 2026-07-26  
**Status:** Executed (see COMPLETION_REPORT)

---

## Approach

1. Reuse `StructuredLogger` + `CorrelationContext` + `EventRegistry` (no second framework).  
2. Add thin `consumer_chain` package with observer wrapper around existing `build_*` bodies.  
3. Extract bodies to `_build_*_body` so business logic is unchanged and public APIs only add observation.  
4. Optional dual-run fingerprint helper gated by Twin ON + non-production `APP_ENV`.  
5. Document Twin quarantine + correct Shadow / Adaptive TwinInput flag drift.

## Non-goals (enforced)

- No HTTP cutover, no algorithm changes, no schema/migrations, no new feature flags, no new Twin.

## Sequence

1. Discovery report  
2. Event types + telemetry + observer + dual_run  
3. Wrap three Runtime A services  
4. Unit / observability / flag / regression tests  
5. Quarantine + doc alignment  
6. Completion report  
