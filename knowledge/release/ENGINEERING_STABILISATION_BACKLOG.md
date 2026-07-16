# Engineering Stabilisation Backlog

**Capability ID:** V1S-001  
**Sprint:** Version 1 Sprint 1  
**Title:** Engineering Stabilisation  
**Status:** SUBMITTED — awaiting Executive Review  
**Date:** 2026-07-15  
**Nature:** Classification and backlog only — no application code, educational behaviour, Constitution, Logic Registry, governance, evidence, Twin, or recommendation algorithms were modified  

---

## Authority

| Authority | Role |
|-----------|------|
| Release Protocol | Engineering STOP CONDITIONS (`docs/process/RELEASE_PROTOCOL.md`) |
| EGI-003 §7 | Engineering + Architecture + Educational Governance triad |
| V1R-001 | Version 1 Release Certification (`KWALITEC_VERSION1_RELEASE_CERTIFICATION.md`) |
| EIP-005 / Continuity Standard | Lawful delete flash / continuity messaging |
| `docs/TECHNICAL_DEBT_REGISTER.md` | Pre-existing engineering debt inventory |
| Architecture / capability status headers | Outstanding Architecture Review queue |

**Constraint (binding for this capability):** Educational architecture is locked. This backlog records **engineering stabilisation only**. Educational redesign is out of scope unless a constitutional defect is discovered.

---

## Executive Snapshot

| Observation | Result |
|-------------|--------|
| Full automated suite (`tests/` + `app/founder`) | **2 failed**, **2108 passed** (2026-07-15) |
| Founder subsystem alone | **165 passed** |
| EIP / IA educational regression subset | Previously certified green; not re-failed in this run |
| Educational Governance (EIP-007) | APPROVED — not reopened |
| Version 1 Release Candidate eligibility | **Blocked** (Engineering STOP + Architecture process gap + unclean candidate + Alpha trust criterion per V1R-001) |

---

## Task 1 — Failing Automated Tests (Inventory)

| # | Test node ID | File:line | Assertion | Observed behaviour |
|---|--------------|-----------|-----------|-------------------|
| F1 | `tests/test_routes.py::TestStudyPlanManagementRoutes::test_delete_plan_post` | `tests/test_routes.py:498` | `assert b"permanently deleted" in resp.data.lower()` | HTTP 200; flash: **“Study plan deleted. Your learning progress and study history are preserved.”** |
| F2 | `tests/test_smoke.py::TestSmokeStudyPlanLifecycle::test_complete_lifecycle` | `tests/test_smoke.py:974` (and identical expectation at `:984`) | `assert b"permanently deleted" in resp.data.lower()` | Same flash as F1 on both delete steps in the lifecycle |

**Suite scope executed**

```text
python -m pytest tests/ app/founder -q
# → 2 failed, 2108 passed
```

No other failing automated tests were observed under that collection.

---

## Task 1 — Classification

| Failure | Classification | Rationale |
|---------|----------------|-----------|
| **F1** | **Legacy expectation** | Implementation flash matches EIP-005 Educational Continuity (`app/study_plan/routes.py` ~1056–1059). Tests still assert pre-continuity copy (`"permanently deleted"`). Product path is intentional and educationally approved; the expectation is stale. |
| **F2** | **Legacy expectation** | Same root copy contract as F1; smoke lifecycle duplicates the obsolete substring check (two assert sites, one test). |

**Not classified as**

| Category | Why not |
|----------|---------|
| Broken implementation | Delete still removes the plan; continuity preservation works; EIP-005 regression suite passes. |
| Broken expectation | Expectation is not merely “wrong about current product by accident”; it is the **previous** product contract left behind after a lawful educational change. |
| Test debt (generic) | Not flaky harness debt, missing fixtures, or over-mocked suite structure — a precise legacy string lock. |

---

## Task 2 — Failure Review

### F1 — `test_delete_plan_post`

| Field | Assessment |
|-------|------------|
| **Root Cause** | EIP-005 changed delete flash from permanent-deletion language to continuity language. Route assertions were not updated. |
| **Affected Capability** | Study Plan delete UX verification; EIP-005 Educational Continuity messaging contract; Release Protocol “tests fail” STOP. |
| **Regression Risk** | **Low** if tests are updated to assert the continuity flash (and preferably plan row absence, already asserted). **High** if someone “fixes” by reverting flash to `"permanently deleted"` — that would regress EIP-005 GAP-001 closure and educational honesty. |
| **Recommended Fix** | Update assertion to the continuity substring (e.g. `learning progress` / `preserved`, or the exact flash). Keep `StudyPlan` row-absence check. Do **not** change educational flash copy. |

### F2 — `test_complete_lifecycle`

| Field | Assessment |
|-------|------------|
| **Root Cause** | Identical legacy flash substring as F1, asserted twice (delete active plan; delete archived plan). |
| **Affected Capability** | End-to-end Study Plan lifecycle smoke; same EIP-005 contract; Release Protocol STOP. |
| **Regression Risk** | Same as F1. Smoke is a Release Protocol journey — green suite is mandatory for RC. |
| **Recommended Fix** | Replace both `"permanently deleted"` asserts with continuity-aligned asserts; retain plan-absence and remaining-plan count checks. |

---

## Task 3 — Engineering Stabilisation Backlog

Only **objective engineering** work. Educational redesign, Twin, recommendation algorithms, Constitution, Registry, and governance content are excluded.

### Critical

| ID | Item | Why Critical | Suggested action |
|----|------|--------------|------------------|
| **ES-C-001** | Reconcile F1/F2 lifecycle & smoke assertions with EIP-005 delete flash | Release Protocol hard STOP while pytest fails | Update `tests/test_routes.py` and `tests/test_smoke.py` only; re-run full suite to green |
| **ES-C-002** | Produce a clean, intentional Integrity Programme commit (or RC branch) with fingerprinted working tree | V1R: dirty tree + untagged EIP delta; Protocol repository gate | Stage/commit EIP + IA engineering + tests + knowledge artefacts under release discipline; no drive-by educational redesign |
| **ES-C-003** | Confirm CI-parity green after ES-C-001 | CI runs `tests/` + founder packages; same F1/F2 would fail PR/`main` | `python -m pytest` matching `.github/workflows` collection; optional Ruff on release-touched paths per Protocol |

### High

| ID | Item | Why High | Suggested action |
|----|------|----------|------------------|
| **ES-H-001** | Close Engineering Review pillar for Version 1 candidate | EGI-003 §7 requires Engineering APPROVED; currently Fail on STOP CONDITIONS | After ES-C-001…003, record Engineering Review APPROVED against the candidate commit |
| **ES-H-002** | Quarantine latent `MissionOptimizer` from accidental student rewire (hygiene) | Accepted V1-TD-003 / V1R-R-005 — prophylactic, not educational redesign | Ensure no student route imports/renders optimizer; document guard in engineering checklist |
| **ES-H-003** | Release-touched Ruff hygiene on Integrity Programme modules | Protocol: Ruff on modified modules; residual E501 on `app/study_plan/routes.py` etc. | Fix only release-touched lint that Protocol treats as required for the ship; do not expand into historical repo-wide reformatting |

### Medium

| ID | Item | Why Medium | Suggested action |
|----|------|------------|------------------|
| **ES-M-001** | SQLAlchemy `Query.get()` → `Session.get()` migration (TD-001 / TD-005) | Large warning volume; future SA 2.0 breakage; not current functional fail | Maintenance sweep; prefer `db.session.get` patterns already used elsewhere |
| **ES-M-002** | Replace `datetime.utcnow()` (e.g. settings export, recommendation metadata) | Python 3.14 DeprecationWarning; future removal | `datetime.now(UTC)` / timezone-aware UTC |
| **ES-M-003** | Study Plan route module size (TD-002) | Maintainability risk for RC support velocity | Split only when touching adjacent edit boundaries; not a gate for green tests |

### Low

| ID | Item | Why Low | Suggested action |
|----|------|---------|------------------|
| **ES-L-001** | Curriculum disk miss log noise (`IFoA/CM1 Revised/2026.json`) during some suite paths | Logged `CurriculumLoadError` then graceful skip; tests still pass | Confirm fixture/path expectations or tone down ERROR→DEBUG for intentional absence; do not invent curriculum files |
| **ES-L-002** | Broader historical Ruff / Architecture Guardian file-size findings (TD-004 / TD-006) | Explicitly non-blocking for Protocol unless instructed | Incremental maintenance after RC |
| **ES-L-003** | Curriculum query performance polish (TD-007) | Correctness prioritised; no suite fail | Post-RC performance sprint |

**Explicitly out of this engineering backlog (not engineering stabilisation)**

- Educational Constitution / Logic Registry / Evidence / Twin / recommendation algorithm changes  
- Product features (coaching Accept/Later, multi-subject remind-me, Version 2 Estimated Mastery exposure)  
- Internal Alpha trust re-test week (process / research evidence — see Release Blockers)  
- Architecture Review **decisions** themselves (listed under Task 4)

---

## Task 4 — Architecture Review Backlog

Outstanding Architecture actions, separated by work type. Source: capability status headers + V1R-001 Architecture Readiness.

### Administrative

| ID | Action | Artefact(s) |
|----|--------|-------------|
| **AR-A-001** | Record Architecture Review outcome for Educational Governance Certification V1 | `EDUCATIONAL_GOVERNANCE_CERTIFICATION_V1.md` (SUBMITTED — awaiting Architecture Review) |
| **AR-A-002** | Record Architecture Review outcomes for IA stabilization capabilities | IA-001, IA-002, IA-003, IA-004 capability docs (`Implemented — pending Architecture Review`) |
| **AR-A-003** | Record Architecture Review for EIP implemented / submitted design artefacts still open | EIP-002 Evidence Authority (implemented); EIP-006 Version 1 State Refinement (implemented); EPA / Philosophy Audit V1 & V2; EIP-004 Recertification; EIP-006-DESIGN / Evidence Model design docs still marked awaiting Architecture Review |
| **AR-A-004** | Clear Architecture pillar for Version 1 Release Candidate under EGI-003 §7 | Composite APPROVED record for Integrity Programme + IA + V1 candidate structure |
| **AR-A-005** | Architecture Office countersignature / return on Founder ops certification if still required | `FSI-005_OPERATIONAL_CERTIFICATION.md` posture |
| **AR-A-006** | Close or supersede IA-001 follow-up RCA as Architecture disposition | `IA-001_FOLLOWUP_TOPIC_SELECTION_RCA.md` — Learning Mode (IA-004) now owns mission topic selection; confirm RCA residual vs closed |

### Engineering

| ID | Action | Notes |
|----|--------|-------|
| **AR-E-001** | Verify layering invariants on Integrity Programme delta (Blueprints → Services → Models; no educational math in routes) | Architecture compliance check, not educational redesign |
| **AR-E-002** | Verify curriculum V1/V2 dual load/traversal preserved after EIP/IA land | Structural invariant from `ARCHITECTURE.md` |
| **AR-E-003** | Confirm Learning Mode remains sole Version 1 mission topic authority on live product path; document any residual Adaptive P1/P2 dead code policy | Aligns with AR-A-006; **do not** reopen recommendation/Twin redesign in V1S |
| **AR-E-004** | Accept / reaffirm interim `TopicProgress` estimate store and latent MissionOptimizer as Version 1 technical architecture debt (already educationally accepted) | Structural acknowledgement for RC; quarantine engineering under ES-H-002 |

### Documentation

| ID | Action | Notes |
|----|--------|-------|
| **AR-D-001** | Update capability status headers from “awaiting / pending Architecture Review” to recorded outcome | Prevents stale “process gap” after AR-A-* closes |
| **AR-D-002** | Sync Architecture Review report(s) into `knowledge/release/` or Architecture records location per ENG-005 | Permanent engineering/architecture record |
| **AR-D-003** | Mark IA-001 follow-up RCA disposition in product/internal_alpha README | Documentation closure for Alpha chain |
| **AR-D-004** | Product roadmap folder remains draft — documentation gap for operators (V1R Product Readiness observation) | Not a student-feature hole; optional RC doc polish |

---

## Task 5 — Release Blockers (Version 1 Release Candidate)

Anything preventing a lawful **Version 1 Release Candidate** under existing authorities (not new criteria):

| Blocker | Severity | Gate | Evidence |
|---------|----------|------|----------|
| **RB-001** Full pytest FAIL (F1, F2) | **Critical** | Release Protocol STOP — “Tests fail” | 2 failed / 2108 passed |
| **RB-002** Working tree unclean; Integrity Programme not on tagged candidate | **Critical** | Protocol repository / fingerprint gates; V1R-R-002 | ~59 dirty paths; latest tag `v0.9.2` |
| **RB-003** Engineering pillar not APPROVED | **Critical** | EGI-003 §7 | Follows RB-001 / RB-002 |
| **RB-004** Architecture Review backlog unresolved (no APPROVED record for IA + EIP + EIP-007 process artefacts / V1 candidate) | **High** | EGI-003 §7 Architecture | V1R-R-004; Task 4 inventory |
| **RB-005** Internal Alpha trust re-confirmation unmet | **High** | Educational Integrity Programme Blueprint §8 Exit Criterion 3; V1R Category 5 | week_001 trust collapse; no post-repair week artefact |
| **RB-006** No fingerprinted `v1.0.0` (or RC) deploy candidate | **High** | Release Protocol §8–§9 | Cannot start lawful Production Release operation |
| **RB-007** Release-touched lint residual (Protocol hygiene) | **Medium** | Protocol Ruff on modified modules | E501 on study-plan routes; not equal to pytest STOP but required before ship discipline claims “clean” |
| **Non-blockers (accepted debt / V2)** | — | — | V1-TD-001…007; Product Blueprint Epics 2–4; coaching Accept/Later polish; thin high-stage density; registration closed by design |

**Educational Governance is not a release blocker** for the triad’s educational pillar (EIP-007 APPROVED). Composite release remains unlawful until Engineering + Architecture (+ Protocol/Alpha conditions) clear.

---

## Recommended Order

1. **ES-C-001** — Green the suite (test assertion reconciliation only).  
2. **ES-C-002 / ES-C-003** — Land clean candidate; prove CI-parity green.  
3. **ES-H-001** — Engineering Review APPROVED on that commit.  
4. **AR-A-*** / **AR-E-*** / **AR-D-*** — Architecture Review returns and records (parallelisable with step 3 once code is frozen).  
5. **RB-005** — Post-repair Internal Alpha trust confirmation (or Architecture-accepted equivalent).  
6. **ES-H-002 / ES-H-003** — Quarantine + release-touched lint as part of RC hygiene.  
7. Release Protocol Production path → fingerprint → smoke → Release Report.  
8. **ES-M-*** / **ES-L-*** — After RC baseline, not as educational programme work.

---

## Verification Evidence (this capability)

| Check | Command / Artefact | Outcome |
|-------|--------------------|---------|
| Product + certification tests | `python -m pytest tests/ -q` | 2 failed, 1943 passed |
| Founder tests | `python -m pytest app/founder -q` | 165 passed |
| Combined | `python -m pytest tests/ app/founder -q` | 2 failed, 2108 passed |
| Failure detail | F1/F2 verbose rerun | Legacy `"permanently deleted"` vs continuity flash |
| Prior certification | `KWALITEC_VERSION1_RELEASE_CERTIFICATION.md` | NOT READY; same two failures identified |

---

## Constraints Honoured

- No educational behaviour changes  
- No Constitution / Logic Registry / Educational Governance / Evidence amendments  
- No Twin or recommendation algorithm changes  
- No automated-test or application fixes performed under V1S-001  

---

## Closing

Engineering stabilisation work required for a Version 1 Release Candidate is **narrow and objective**: reconcile two legacy delete-flash assertions, land a clean Integrity Programme candidate, clear Engineering and Architecture process gates, and satisfy Internal Alpha trust confirmation under existing authorities.

**Stop.**  
**Return for Executive Review.**  
**Do not implement fixes from this backlog until directed.**

**End of V1S-001 — Engineering Stabilisation Backlog**
