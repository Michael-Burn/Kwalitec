# REPOSITORY_HYGIENE_REPORT.md

**Programme:** VERSION1-RC2 — Sprint A (Repository Hygiene & Release Fingerprint)  
**Date:** 2026-08-01  
**Authority:** `REPOSITORY_AUDIT.md`  
**Constraint:** No application-behaviour redesign; selective commit + exclude dumps only

---

## Executive summary

Executed the audit keep / remove / ignore plan. Temporary EV-001 evidence dumps were deleted and gitignored. All **keep** paths (EF deltas, educational package module + campaigns/packages JSON, overlays, tests, programme evidence markdown, RC2 gate docs) are included in the release candidate commit set. Working tree target: **clean** after the RC commit.

---

## Actions applied

| Action | What |
|--------|------|
| **Keep** | Audit §§1–3 keep-set + RC2 stabilization artefacts produced for this programme |
| **Remove** | `.ev001_evidence/` (~128 HTML/TXT/HDR dumps) and `.ev001_evidence.html` deleted from disk |
| **Ignore** | `.gitignore` extended with `.ev001_evidence/`, `.ev001_evidence.html`, and `.ev*_evidence*` patterns |
| **Archive** | Not used — dumps removed rather than relocated (audit allowed delete or archive) |

---

## Files kept

### Modified tracked (10)

- `.cursor/rules/11-educational-framework-freeze.mdc`
- `EF001_EDUCATIONAL_FRAMEWORK_FREEZE.md`
- `app/application/educational_authoring/composition.py`
- `app/application/educational_engine_foundation/service.py`
- `app/application/educational_runtime_engine/service.py`
- `app/application/learning_session/substance_planner.py`
- `app/application/student_runtime/coordinator.py`
- `app/infrastructure/adapters/learning_session/runtime_engine.py`
- `app/presentation/session/sitting_report.py`
- `app/presentation/student/services/student_home_service.py`

### Application / curriculum / tests (sources only)

- `app/application/educational_packages/` (`__init__.py`, `composition_overlay.py`, `loader.py`, `models.py`, `substance.py`)
- `app/curriculum/data/educational_campaigns/cs1/campaign-alpha-ep001/`
- `app/curriculum/data/educational_campaigns/cs1/campaign-beta-cs1002/`
- `app/curriculum/data/educational_packages/cs1/4.2-glm-structure-ea006.json`
- `tests/application/educational_packages/test_ea006_publication.py`

### Programme evidence & law (root `*.md`)

- `EF001_OPERATIONAL_REVIEW_TEMPLATE.md`
- `EA001_*` … `EA008_*`
- `EO001_*`, `TV001_*`, `EJ001_*`, `EW001_*`
- `EP001_*`, `PR001_*`, `CS1002_*`, `CE001_*`, `DSH001_*`, `DX001_*`, `SV001_*`
- `EV001_*` (reports only — not live dumps), `FV002_*`
- `RR001_RELEASE_READINESS_REPORT.md`, `RR001_DEPLOYMENT_VERIFICATION.md`, `RR001_LIVE_SMOKE_REPORT.md`, `RR001_RELEASE_DECISION.md`

### RC2 stabilization corpus

- `REPOSITORY_AUDIT.md`, `RC2_INTEGRITY_REPORT.md`, `DEPLOYMENT_CHECKLIST.md`, `KNOWN_ISSUES_RC2.md`, `VERSION1_RELEASE_MANIFEST.md`, `RC2_RELEASE_ACTION_PLAN.md`
- `REPOSITORY_HYGIENE_REPORT.md` (this file)
- `.gitignore` (evidence-dump ignore rules)

### Already committed (unpushed lineage)

- `f066bcf` — EF-001 Educational Framework freeze (kept as ancestor of RC tip)

---

## Files removed

| Path | Justification |
|------|---------------|
| `.ev001_evidence/` (entire directory) | Audit §4 **temporary / generated** — live walkthrough dumps; **remove** from release set |
| `.ev001_evidence.html` | Audit §4 aggregate evidence HTML — **remove** |

`__pycache__/` under educational package paths was cleared locally; pattern already gitignored — not committed.

---

## Files ignored

| Pattern | Justification |
|---------|---------------|
| `.ev001_evidence/` | Prevent reintroduction of EV-001 dumps |
| `.ev001_evidence.html` | Same |
| `.ev*_evidence/` / `.ev*_evidence.html` | Forward-looking guard for similar dump names |
| `__pycache__/`, `*.py[cod]` | Pre-existing generated-artefact ignores |

---

## Remaining untracked files

**None** after tagged tip `75c29d2` / `v2.0.0-beta.1-rc2` (working tree clean). Follow-up docs commits may land after the tag without changing the tagged inventory tip.

---

## Justification

1. **KI-C1** requires a clean, reproducible tip containing educational inventory and evidence corpus — not mass deletion of programme docs.  
2. EV-001 dumps are operator captures, not product source; committing them would bloat the tree and risk accidental publication of transient HTML.  
3. Overlay + package module + campaign JSON must ship **together** (audit §1 footnote) for RR-001 inventory activation coherence.  
4. No schema / migration / business-logic redesign was introduced by this hygiene pass — only commit-set selection and ignore/delete of temporaries.

---

## C1 status recommendation

**KI-C1 (Repository Hygiene) → CLOSED** once `git status` reports a clean working tree on the tagged RC tip.
