# RC2_POST_HYGIENE_REPORT.md

**Programme:** VERSION1-RC2 — Sprint A  
**Date:** 2026-08-01  
**Role:** Post-hygiene integrity verification  
**Tagged tip:** `v2.0.0-beta.1-rc2` → `75c29d2b0017d7df44a0767ae0e428605151cd90`

---

## Verdict

**LOCAL RELEASE-CANDIDATE INTEGRITY: PASS**  
**UNCONDITIONAL GO: NO** (deploy, smoke, EV-001 trust remain)

Repository hygiene and an immutable local fingerprint now exist. LIVE still runs `613722c`.

---

## 1. Clean repository

| Check | Result | Evidence |
|-------|--------|----------|
| Working tree clean at tag | **PASS** | `git status` clean after `75c29d2` / tag cut |
| EV-001 dumps excluded | **PASS** | Deleted + `.gitignore` patterns |
| Inventory in Git | **PASS** | `educational_packages` module + campaign/package JSON tracked |
| Evidence corpus committed | **PASS** | EA→EF / PR / EV / FV / RR001 / RC2 docs |

---

## 2. Migration chain unchanged

| Check | Result | Evidence |
|-------|--------|----------|
| `flask db heads` | Single head `202607310002` | CLI |
| New migrations in tip | None | Diff vs pre-sprint |
| LIVE head (RR-001) | `202607310002` | Unchanged expectation |

---

## 3. Version consistency

| Source | Value |
|--------|-------|
| `VERSION` | `2.0.0-beta.1` |
| `pyproject.toml` | `2.0.0-beta.1` |
| `app.version.APP_VERSION` | `2.0.0-beta.1` |
| RC tag (distinct) | `v2.0.0-beta.1-rc2` |
| Historical collision avoided | Did **not** reuse `v1.0.0-rc2` / `VERSION1-RC2` |

---

## 4. Reproducible release candidate

| Artefact | Value |
|----------|-------|
| Branch | `main` |
| Commit | `75c29d2b0017d7df44a0767ae0e428605151cd90` |
| Tag | `v2.0.0-beta.1-rc2` (annotated) |
| Timestamp (tag UTC) | `2026-08-01T08:25:15Z` |
| Build fingerprint | `2.0.0-beta.1` + tag + SHA + migration `202607310002` |

Checkout recipe: `git checkout v2.0.0-beta.1-rc2`

---

## 5. Tests / architecture (Sprint A)

| Suite | Result |
|-------|--------|
| `tests/application/educational_packages/` | **7 passed** |
| `tests/curriculum/test_curriculum_parity.py` + discover curricula | **PASS** (after excluding non-syllabus data dirs) |
| `tests/architecture/` | **2137 passed** |
| Focused RC regression (packages + parity + architecture + curriculum v2) | **2267 passed** |
| Architecture Guardian | **40/100** — pre-existing debt; Blueprint Separation **PASS**; not introduced by Sprint A |
| Full `pytest` (46k+) | **206 failed / 45853 passed** — sample failures (smoke FK, snapshot drift, stale migration assertions) reproduce **without** inventory dirs; treated as pre-existing workstation/suite debt, not Sprint A regressions |

Compatibility fix in tip: `discover_curricula()` skips `educational_packages` / `educational_campaigns` so inventory JSON is not registered as syllabi.

---

## 6. Blocker status after Sprint A

| Blocker | Status |
|---------|--------|
| **C1 / KI-C1** Repository hygiene | **CLOSED** |
| **C2** Local release fingerprint (commit + tag + manifest) | **CLOSED** |
| KI-C2 LIVE `/health.commit` match | **OPEN** — requires push + Render deploy (Priority 3; out of Sprint A) |
| KI-C3 EV-001 trust | **OPEN** |
| KI-C4 Smoke completion | **OPEN** |

---

## Conclusion

Sprint A success criteria for **repository clean + RC commit + RC tag + manifest + C1/C2 local closure** are met. Do not begin EV-001 or deploy work from this report; follow `RC2_RELEASE_ACTION_PLAN.md` Priority 3 next.
