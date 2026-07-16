# V1S-002 — Engineering Stabilisation Corrections

**Capability ID:** V1S-002  
**Sprint:** Version 1 Sprint 1  
**Title:** Engineering Stabilisation Corrections  
**Status:** SUBMITTED — awaiting Executive Review  
**Date:** 2026-07-15  
**Nature:** Engineering corrections only — obsolete pytest expectations aligned to EIP-005 Educational Continuity wording. No educational behaviour, Constitution, Logic Registry, governance, or messaging-semantics changes.

---

## Executive Summary

V1S-001 Critical pytest blockers **ES-C-001** and **ES-C-003** are resolved. Legacy delete-flash assertions (`"permanently deleted"`) in route and smoke tests were replaced with stronger Educational Continuity assertions matching the live EIP-005 flash. Full default pytest suite is **2139 passed / 0 failed**. V1S-002 introduced **no new Ruff findings** on edited lines.

**Critical ES-C-002 remains open:** the working tree on `main` is still dirty with Integrity Programme / Internal Alpha artefacts and is not a clean release candidate fingerprint. Therefore full **Engineering APPROVED** for the Version 1 Release Candidate pillar is **not** claimed. Engineering recommendation for the pytest Release Protocol STOP: **CLEARED**.

---

## Tests Updated

| File | Change |
|------|--------|
| `tests/test_routes.py` | `test_delete_plan_post` — replaced `permanently deleted` with Continuity asserts (`study plan deleted`, `learning progress`, `study history`, `preserved`); retained plan-row absence |
| `tests/test_smoke.py` | `test_complete_lifecycle` — same Continuity asserts on both delete steps; retained plan absence and remaining-plan count |

Assertions were **not weakened**: successful deletion, Continuity messaging, and preserved-history wording are all locked. Learner-history preservation behaviour remains covered by `tests/test_eip005_educational_continuity.py` (unchanged).

**Application / educational implementation:** untouched under this capability.

---

## Pytest Results

| Check | Command | Outcome |
|-------|---------|---------|
| Default suite (`pyproject.toml` testpaths) | `.venv/bin/python -m pytest -q --tb=line` | **2139 passed**, 0 failed (56.15s) |
| F1 isolated | `tests/test_routes.py::…::test_delete_plan_post` | **passed** |
| F2 isolated | `tests/test_smoke.py::…::test_complete_lifecycle` | **passed** |

Obsolete substring `"permanently deleted"` is absent from both updated files.

---

## Engineering Review

### Critical backlog status (from V1S-001)

| ID | Item | Status |
|----|------|--------|
| **ES-C-001** | Reconcile F1/F2 assertions with EIP-005 delete flash | **RESOLVED** |
| **ES-C-003** | Confirm CI-parity green after ES-C-001 | **RESOLVED** (default suite 100% green) |
| **ES-C-002** | Clean intentional Integrity Programme / RC commit | **OPEN** |

### Ruff (release-touched paths)

- Edited V1S-002 lines in `tests/test_routes.py` / `tests/test_smoke.py`: **no Ruff hits**.
- Pre-existing findings remain on those files and broader Integrity Programme modules (E501, I001, historical F401 ignored in CI). **No newly introduced issues** attributable to this capability.
- Broader release-touched sweep still reports historical debt (ES-H-003 / ES-M-\* territory) — not opened by V1S-002 edits.

### Working-tree review (Task 4)

| Check | Result |
|-------|--------|
| Branch | `main` |
| Clean working tree | **No** — modified + untracked Integrity Programme / EIP / IA / knowledge / scripts |
| Accidental research files | `research/internal_alpha/week_001/` is intentional Internal Alpha week packaging, **not** a random dump — but it is **not** yet an intentional RC commit; must not be mistaken for a released fingerprint |
| Unintended artefacts | `.ruff_cache/` local cache (should stay uncommitted); do not stage |

---

## Remaining Release Blockers

| ID | Blocker | Owner |
|----|---------|-------|
| **ES-C-002** | Dirty tree / no fingerprinted Integrity Programme RC commit | Engineering (release discipline) |
| **ES-H-001** | Engineering Review pillar fully closed for Version 1 candidate | Blocked on ES-C-002 |
| **AR-*** | Architecture Review returns (administrative / educational — out of V1S-002) | Architecture |
| **RB-005** (V1S-001) | Internal Alpha trust confirmation | Product / process |
| **ES-H-002 / ES-H-003** | Optimizer quarantine hygiene; residual release-touched lint | Engineering (High, post-green-suite) |

Pytest Release Protocol STOP from F1/F2: **cleared**.

---

## Architecture Impact

| Concern | Assessment |
|---------|------------|
| Layering | Unchanged — test expectation alignment only |
| Curriculum V1/V2 | Unaffected |
| Educational Continuity (EIP-005) | Messaging contract **confirmed** by tests; implementation not modified |
| Migrations | None |
| Constitution / Registry / Governance | Not modified |

---

## Release Recommendation

| Gate | Recommendation |
|------|----------------|
| Pytest / ES-C-001 / ES-C-003 | **PASS — Engineering CLEARED** for the Critical test STOP |
| Version 1 RC Engineering pillar (EGI-003 §7) | **NOT YET APPROVED** — residual Critical **ES-C-002** (clean commit / fingerprint) |
| Proceed to V1S-003 | **Do not begin** until Executive Review directs |

**Summary recommendation to Executive Review:** accept V1S-002 as complete for Critical **test** stabilisation; withhold full **Engineering APPROVED** for the Version 1 Release Candidate until ES-C-002 lands a clean intentional commit.

---

## Constraints Honoured

- No educational behaviour changes  
- No Constitution / Logic Registry / Educational Governance changes  
- No Educational messaging semantics changes in application code  
- Implementation not modified to satisfy obsolete tests — tests aligned to Continuity standard  

---

## Closing

**Stop.**  
**Return for Executive Review.**  
**Do not begin V1S-003.**

**End of V1S-002 — Engineering Stabilisation Corrections**
