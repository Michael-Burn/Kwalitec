# RC2_SPRINT_A_COMPLETION_REPORT.md

**Programme:** VERSION1-RC2 — Sprint A (Repository Hygiene & Release Fingerprint)  
**Date:** 2026-08-01  
**Commit (tagged tip):** `75c29d2b0017d7df44a0767ae0e428605151cd90`  
**Tag:** `v2.0.0-beta.1-rc2`  
**Follow-up docs commit:** see `git log` after this report is committed

---

## Summary

Sprint A cut a clean, tagged Release Candidate tip on `main`: educational inventory and overlays are in Git, EV-001 dumps are removed/ignored, the VERSION triad is unchanged at `2.0.0-beta.1`, Alembic head remains `202607310002`, and the manifest records the fingerprint. Critical blocker **C1 is CLOSED**. **C2 local release fingerprint is CLOSED** (commit + distinct tag + manifest); LIVE `/health.commit` match remains Pending because deployment was explicitly out of scope.

---

## Files Created

- `REPOSITORY_HYGIENE_REPORT.md`
- `RC2_POST_HYGIENE_REPORT.md`
- `RC2_SPRINT_A_COMPLETION_REPORT.md` (this file)
- Full keep-set inventory/docs from `REPOSITORY_AUDIT.md` (educational packages module, campaigns, programme markdown, RC2 gate docs) — see hygiene report for exhaustive lists

---

## Files Modified

- `.gitignore` — ignore `.ev001_evidence*`
- `CHANGELOG.md` — `[2.0.0-beta.1-rc2]` section
- `VERSION1_RELEASE_MANIFEST.md` — fingerprint filled
- `KNOWN_ISSUES_RC2.md` — C1/C2/M3/M4 status
- Audit keep-set overlays + EF docs (pre-existing WIP committed as a set)
- `app/curriculum/loader.py` — exclude non-syllabus inventory dirs from `discover_curricula()`
- `tests/test_curriculum_engine.py` — discovery exclusion assertion
- `tests/application/educational_packages/test_ea006_publication.py` — ruff E501 wrap only

---

## Files Removed

- `.ev001_evidence/` (entire dump tree)
- `.ev001_evidence.html`

---

## What was intentionally not changed

- No EV-001 educational trust remediation  
- No UI redesign  
- No readiness / analytics / recommendation engine redesign  
- No database schema / Alembic revisions  
- No Render deployment or push to `origin`  
- No `v1.0.0` tag  
- Application version string left at `2.0.0-beta.1`  
- Educational Framework remains FROZEN (EF-001)

---

## Tests Executed

| Command | Outcome |
|---------|---------|
| `ruff check` on educational_packages + touched overlay paths | Pass |
| `pytest tests/application/educational_packages/` | 7 passed |
| `pytest tests/curriculum/test_curriculum_parity.py` + discover tests | Pass |
| `pytest tests/architecture/` | 2137 passed |
| Focused RC set (+ curriculum v2) | 2267 passed |
| `python tools/architecture_guardian.py` | Score 40/100 (pre-existing); Blueprint Separation PASS |
| Full `pytest` | 45853 passed, 206 failed — failures sample as pre-existing (reproduced without inventory dirs) |

---

## Migration Impact

**None.** Alembic head remains `202607310002`.

---

## Architecture Compliance

- Layering preserved: package loader under `app/application/`; curriculum JSON under `app/curriculum/data/`; presentation/services call loader via existing seams.  
- Curriculum V1/V2 discovery preserved by excluding `educational_packages` / `educational_campaigns` from syllabus walk — inventory co-location does not register false exams.  
- Traversal/import compatibility for IFoA CS1/CM1/CB2 unchanged.  
- Architecture Guardian debt unchanged (pre-existing).

---

## Evidence for closing C1 and C2

| Blocker | Evidence |
|---------|----------|
| **C1 CLOSED** | Clean `git status` on tip; inventory tracked; dumps deleted/ignored — `REPOSITORY_HYGIENE_REPORT.md` |
| **C2 local CLOSED** | Annotated tag `v2.0.0-beta.1-rc2` → `75c29d2…`; manifest fingerprint block filled — `VERSION1_RELEASE_MANIFEST.md`, `RC2_POST_HYGIENE_REPORT.md` |
| **C2 LIVE open** | Deploy not performed; `/health.commit` still `613722c` |

**Report:** C1 **can be marked CLOSED**. C2 Release Fingerprint (Sprint A scope: authoritative commit + tag + manifest) **can be marked CLOSED**. KI-C2 LIVE equality **cannot** be fully CLOSED until Priority 3 deploy.

---

## Remaining blockers

- KI-C2 LIVE match (push + Render deploy)  
- KI-C3 EV-001 educational trust  
- KI-C4 Session completion smoke  
- KI-H1 / KI-H4 volume `released` + activation (if GO = released Pilot Arc)  
- KI-H3 cleared locally once tip includes `f066bcf` ancestor; remote push still needed  

---

## Technical Debt

- Full pytest suite has substantial pre-existing failures on this workstation (smoke FK, snapshot drift, stale head assertions). Not introduced by Sprint A keep-set; still a Release Protocol follow-up before unconditional GO.  
- Architecture Guardian 40/100 pre-existing.

---

## Known Limitations

- Tip is local (+ ahead of `origin/main`); not on LIVE.  
- Certified inventory committed does not by itself clear EV-001 trust failures.  
- Volumes remain `publication_ready`, not `released`.

---

## Student Impact Assessment

N/A for Sprint A docs/hygiene scope relative to new student-facing features. Inventory commit enables future certified substance on deploy; no LIVE student change until Priority 3.

Template: `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md` — deferred to deploy/validation sprint.

---

## Estimated KSI contribution

**ΔKSI = 0** (release hygiene / fingerprint; no validated student-outcome change on LIVE).

---

## Evidence collected

- `REPOSITORY_HYGIENE_REPORT.md`  
- `RC2_POST_HYGIENE_REPORT.md`  
- `VERSION1_RELEASE_MANIFEST.md`  
- Tag `v2.0.0-beta.1-rc2`  
- Pytest/ruff/guardian outputs as above  

---

## Lessons learned for student value

Shipping inventory into Git is necessary but not sufficient for student trust: EV-001 class failures and LIVE fingerprint match remain the educational GO path.

---

## Explainability Review

N/A — Sprint A did not change recommendation/explainability surfaces beyond committing pre-authored package prefer-path wiring already on disk; no new opaque scores.

---

## Recommendation Quality Review

N/A — no ranking/recommendation redesign.

---

## Version 1 readiness residual

Gates G1–G12 remain open for unconditional production-ready declaration; Sprint A only clears repository hygiene / local RC fingerprint inputs to RR-001.

---

## CRI domains improved

None validated (docs/hygiene). **ΔCRI = 0**.

---

## Stop

Sprint A complete. **Do not begin EV-001 or subsequent sprints from this agent turn.**
