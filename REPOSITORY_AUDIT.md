# REPOSITORY_AUDIT.md

**Programme:** VERSION1-RC2 — Release Stabilization Sprint  
**Date:** 2026-08-01  
**Scope:** Local `main` working tree vs `HEAD` `f066bcf` / `origin/main` `613722c`  
**Method:** `git status --porcelain`, path inspection, diff sampling  
**Constraint:** **No deletions performed** — cleanup plan only

---

## Executive summary

| Metric | Evidence |
|--------|----------|
| Branch | `main` ahead of `origin/main` by **1** commit (`f066bcf` EF-001) |
| Modified tracked files | **10** |
| Untracked status entries | **117** |
| Untracked files (expanded) | **263** (includes `__pycache__` + `.ev001_evidence/`) |
| Alembic script head (`flask db heads`) | Single head `202607310002` |
| LIVE tip (RR-001) | `613722c` — does **not** include untracked inventory |

Nothing in this audit was deleted automatically.

---

## Category legend

| Category | Meaning |
|----------|---------|
| **intended release** | Required for a coherent RC tip that can clear RR-001 inventory / EF fingerprint goals |
| **experimental** | Behavioural change not yet release-gated; review before commit |
| **obsolete** | Superseded or not needed for RC |
| **generated** | Build/test/cache artefacts |
| **temporary** | Operator/debug/evidence dumps not part of product source |

| Action | Meaning |
|--------|---------|
| **keep** | Include in intended RC commit set (or already committed) |
| **remove** | Do **not** commit; delete or gitignore later (manual) |
| **defer** | Park outside RC tip; decide in a later programme |

---

## 1. Modified tracked files (10)

| File | Category | Reason | Action |
|------|----------|--------|--------|
| `.cursor/rules/11-educational-framework-freeze.mdc` | intended release | EF-001 operational-review rule addition (unstaged follow-up to `f066bcf`) | **keep** |
| `EF001_EDUCATIONAL_FRAMEWORK_FREEZE.md` | intended release | Adds mandatory `EF001_OPERATIONAL_REVIEW_TEMPLATE.md` stewardship rule | **keep** |
| `app/application/educational_authoring/composition.py` | intended release* | EA-006 package composition overlay hook | **keep** (with package module) |
| `app/application/educational_engine_foundation/service.py` | intended release* | Mission template overlay for certified packages | **keep** |
| `app/application/educational_runtime_engine/service.py` | intended release* | Prefer certified display title over syllabus-paste chrome | **keep** |
| `app/application/learning_session/substance_planner.py` | intended release* | Prefer certified package session substance | **keep** |
| `app/application/student_runtime/coordinator.py` | intended release* | Package why_now / substance source wiring | **keep** |
| `app/infrastructure/adapters/learning_session/runtime_engine.py` | intended release* | Runtime adapter support for package path | **keep** |
| `app/presentation/session/sitting_report.py` | intended release* | Tomorrow/continuity from certified package | **keep** |
| `app/presentation/student/services/student_home_service.py` | intended release* | Home title/why_now from certified package | **keep** |

\*These modify product behaviour. They are **in scope for RR-001 inventory activation**, not net-new features. They must ship **together** with `app/application/educational_packages/` and package JSON, or be deferred as a set. Shipping overlays without JSON is incomplete; shipping JSON without overlays leaves inventory inert.

---

## 2. Untracked application / curriculum / tests

| Path | Category | Reason | Action |
|------|----------|--------|--------|
| `app/application/educational_packages/` (`.py` sources) | intended release | EA-006 loader/models/overlay — required for certified substance | **keep** |
| `app/application/educational_packages/__pycache__/` | generated | Bytecode | **remove** (do not commit; already gitignored pattern) |
| `app/curriculum/data/educational_campaigns/cs1/campaign-alpha-ep001/` | intended release | Campaign Alpha inventory (CS1-001) — RR-001 blocker | **keep** |
| `app/curriculum/data/educational_campaigns/cs1/campaign-beta-cs1002/` | intended release | Campaign Beta inventory (CS1-002) | **keep** |
| `app/curriculum/data/educational_packages/cs1/4.2-glm-structure-ea006.json` | intended release | EA-006 4.2 grandfather package | **keep** |
| `tests/application/educational_packages/test_ea006_publication.py` | intended release | Package publication tests | **keep** |
| `tests/application/educational_packages/__pycache__/` | generated | Bytecode | **remove** |

---

## 3. Untracked programme documentation (root `*.md`)

These are Educational Framework / operations / validation artefacts produced during EA→EF / PR / EV / FV programmes. They are **not** runtime code. For RC2 hygiene they should be committed as the release evidence corpus **or** moved under `knowledge/` in a later docs-only chore — but must not remain as indefinite dirty tree.

### 3.1 Educational law & freeze (keep)

| File pattern / files | Category | Action |
|----------------------|----------|--------|
| `EF001_OPERATIONAL_REVIEW_TEMPLATE.md` | intended release | **keep** |
| `EA001_*` … `EA008_*` (law + reports) | intended release | **keep** |
| `EO001_*` | intended release | **keep** |
| `TV001_*` | intended release | **keep** |
| `EJ001_*` | intended release | **keep** |
| `EW001_*` | intended release | **keep** |

### 3.2 Production / volume / campaign evidence (keep)

| File pattern | Category | Action |
|--------------|----------|--------|
| `EP001_*` | intended release | **keep** |
| `PR001_*` | intended release | **keep** |
| `CS1002_*` | intended release | **keep** |
| `CE001_*` | intended release | **keep** |
| `DSH001_*` | intended release | **keep** |
| `DX001_*` | intended release | **keep** |
| `SV001_*` | intended release | **keep** |

### 3.3 Validation evidence (keep as evidence; not runtime)

| File pattern | Category | Action |
|--------------|----------|--------|
| `EV001_*` | intended release (evidence) | **keep** |
| `FV002_*` | intended release (evidence) | **keep** |

### 3.4 RR-001 gate artefacts (keep)

| File | Category | Action |
|------|----------|--------|
| `RR001_RELEASE_READINESS_REPORT.md` | intended release | **keep** |
| `RR001_DEPLOYMENT_VERIFICATION.md` | intended release | **keep** |
| `RR001_LIVE_SMOKE_REPORT.md` | intended release | **keep** |
| `RR001_RELEASE_DECISION.md` | intended release | **keep** |

**Count:** 111 root-level untracked `*.md` status entries (includes RR001 + programmes above).

---

## 4. Temporary / generated evidence dumps

| Path | Category | Reason | Action |
|------|----------|--------|--------|
| `.ev001_evidence/` (~128 files HTML/TXT/HDR) | temporary / generated | Live walkthrough capture dumps from EV-001 | **remove** from release set (do not commit) |
| `.ev001_evidence.html` | temporary | Aggregate evidence HTML | **remove** from release set |

**Cleanup plan (manual, later):** delete or archive outside the repo; optionally add explicit ignore rules if dumps recur. **Not deleted in this sprint.**

---

## 5. Already committed but unpushed

| Item | Category | Reason | Action |
|------|----------|--------|--------|
| Commit `f066bcf` — EF-001 freeze (+ rule + `knowledge/GOVERNANCE.md`) | intended release | Required EF fingerprint; not on `origin/main` / LIVE | **keep** + **push** with RC tip |

---

## 6. Migrations / obsolete docs / abandoned artefacts

| Item | Finding | Category | Action |
|------|---------|----------|--------|
| Alembic head | `flask db heads` → single `202607310002` | n/a | **keep** (no new migration in dirty tree) |
| Files `202609*`, `202610*`, `202611*` under `migrations/versions/` | **In chain** (ancestors via history); odd date prefixes but not abandoned | obsolete naming only | **defer** rename (do not touch in RC) |
| Untracked abandoned migrations | **None found** in dirty tree | — | — |
| Historical tag `v1.0.0-rc2` (`f2cbdc5`) | Older Internal Alpha RC2 — **not** this sprint tip | obsolete label collision risk | **defer** — choose distinct new tag name for this RC |
| Architecture Guardian score 40/100 | Pre-existing debt (`tools/architecture_guardian.py`) | experimental/debt | **defer** (not introduced by dirty tree) |

---

## 7. Release-set recommendation (plan only)

### Commit set A — “RC tip minimum for RR-001 inventory path”

1. Unpushed `f066bcf` + unstaged EF-001 doc/rule deltas  
2. `app/application/educational_packages/` (sources only)  
3. `app/curriculum/data/educational_campaigns/`  
4. `app/curriculum/data/educational_packages/`  
5. Eight modified app overlay files listed in §1  
6. `tests/application/educational_packages/` (sources only)  
7. RR-001 + EF/EA/EO/TV/EJ/EW/EP/PR (+ related) programme markdown if releasing with full evidence corpus  

### Explicitly exclude from commit

- `.ev001_evidence/` and `.ev001_evidence.html`  
- All `__pycache__/` / `*.pyc`  

### Do not delete in this sprint

Per mission constraint: prepare plan only. Operator executes cleanup after approval.

---

## 8. Audit conclusion

The repository is **not release-clean**. The dominant RR-001 hygiene failure is a large **intended but uncommitted** educational corpus plus **temporary EV-001 dumps**, on top of an **unpushed** EF-001 commit. Cleanup is primarily **selective commit + exclude dumps**, not mass deletion of programme docs.
