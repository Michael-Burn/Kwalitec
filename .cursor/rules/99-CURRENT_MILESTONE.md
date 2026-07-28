# Current Milestone

**RI-001** — Educational Runtime Integration (**Active delivery**)

## Objective

Integrate the Educational Intelligence Core into the live runtime with Preferred Authority cutover: EI-007 → EX-001 Experience Models whenever an active SCI has Educational Decisions; instrumented Runtime A Temporary compatibility otherwise.

## Allowed modifications

- `app/application/runtime_integration/`
- Wiring into Recommendation Bridge, Dashboard, Mission/Session, Tutor, Student Home Runtime C fork
- `app/application/config/v2_flags.py` (`ENABLE_RUNTIME_INTEGRATION`)
- `tests/application/runtime_integration/`
- `knowledge/runtime_integration/ri001_educational_runtime_integration/`
- Programme dashboard / milestone pointers for RI-001

## Forbidden

- Modifying EI-007 reasoning, Twin beliefs, Learning Evidence, or CKG
- Introducing new educational reasoning or bypassing EX-001
- Adding educational logic to controllers or Runtime C
- New educational features on Runtime A

## Parallel note

FV-001 Founder Validation remains the commercial dogfood track. RI-001 does not reopen CQ engineering or Founder Validated CRI claims.

## Authoritative artefacts

- Architecture: `knowledge/runtime_integration/ri001_educational_runtime_integration/ARCHITECTURE.md`
- Audit: `knowledge/runtime_integration/ri001_educational_runtime_integration/RUNTIME_AUDIT.md`
- Completion: `knowledge/runtime_integration/ri001_educational_runtime_integration/RI001_COMPLETION_REPORT.md`
- Upstream: EI-007 · EX-001

---

*This file is intentionally overwritten when the active milestone changes.*
