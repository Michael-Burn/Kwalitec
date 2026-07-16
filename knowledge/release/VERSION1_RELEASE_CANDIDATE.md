# Version 1 Release Candidate Preparation

**Capability ID:** V1S-003  
**Sprint:** Version 1 Sprint 1  
**Title:** Release Candidate Preparation  
**Status:** SUBMITTED — awaiting Executive Review  
**Date:** 2026-07-15  
**Nature:** Release engineering / operational only — no application features implemented under this capability  

---

## Authority

| Authority | Role |
|-----------|------|
| Release Protocol | Clean intentional release commit; working-tree discipline (`docs/process/RELEASE_PROTOCOL.md`) |
| EGI-003 §7 | Engineering + Architecture + Educational Governance triad |
| V1R-001 | Version 1 Release Certification (`KWALITEC_VERSION1_RELEASE_CERTIFICATION.md`) |
| V1S-001 / V1S-002 | Engineering stabilisation backlog and Critical test closures |
| EIP-007 | Educational Governance **APPROVED** / Educationally Ready |
| ES-C-002 | Clean Integrity Programme / RC fingerprint (still open until commit) |

**Constraints honoured under V1S-003**

- No application features implemented  
- No commits created  
- No push  
- No tag  
- No deploy  
- Release Candidate **not** created — preparation and classification only  

---

## Executive Summary

Engineering Critical test STOP from V1S-002 is cleared (**2139 passed / 0 failed**). Educational Governance remains **APPROVED**. The working tree on `main` still contains the full uncommitted Educational Integrity Programme, IA-004, release-engineering artefacts, Internal Alpha week_001 research, and research tooling.

This capability classifies every dirty path, defines the staging plan for an intentional Version 1 Release Candidate fingerprint, and confirms that the **candidate content set** can be kept free of research, temporary, and generated noise — **without** creating the commit.

**Logical Release Candidate identifier:** `VERSION1-RC1`  
**Commit target:** one intentional Integrity Programme + IA-004 + V1S stabilisation commit on `main` (not created under V1S-003)  
**Baseline HEAD (pre-RC):** `2f99e6b` — `docs(release): add v0.9.2 Internal Alpha stabilization notes`  
**Latest shipped Internal Alpha tag:** `v0.9.2`

---

## Task 1 — Working Tree Review

### Repository snapshot

| Item | Value |
|------|-------|
| Branch | `main` |
| HEAD | `2f99e6b453a231b85c7067cb67ff258e54752f94` |
| Working tree | **Dirty** — 30 modified paths; 61+ untracked paths (status `-uall`) |
| Cache / generated in `git status` | **None** |
| Ignored local noise (not in status) | `.DS_Store` (e.g. under `research/internal_alpha/week_001/`), `.ruff_cache/`, `.pytest_cache/`, `__pycache__/` |

### Classification legend

| Category | Meaning |
|----------|---------|
| **Release Candidate** | Belongs in the intentional Version 1 RC commit fingerprint |
| **Research** | Internal Alpha research / week packaging / research tooling — not product RC |
| **Documentation** | Programme / product docs that support the RC but are governance or product narrative (still stage with RC when listed under RC) |
| **Temporary** | Local or transient artefacts that must not ship |
| **Ignore** | Already gitignored or must never be staged |

*Note:* Governance and Integrity Programme knowledge files are product authorities for Version 1. They are classified **Release Candidate** (not optional commentary).

---

### Modified tracked files

| Path | Category | Rationale |
|------|----------|-----------|
| `app/analytics/routes.py` | Release Candidate | EIP explainability / truthful progress surface wiring |
| `app/application/dashboard/recommendation_card_builder.py` | Release Candidate | IA/EIP student messaging + explainability card contract |
| `app/dashboard/routes.py` | Release Candidate | EIP explainability / guidance surfaces |
| `app/mission/routes.py` | Release Candidate | EIP explainability / mission guidance surfaces |
| `app/models/topic_progress.py` | Release Candidate | State / continuity support for Integrity Programme |
| `app/services/adaptive_learning_service.py` | Release Candidate | Evidence-gated estimate pathway (EIP-002) |
| `app/services/learning_service.py` | Release Candidate | Progress / estimate honesty alignment |
| `app/services/planning_service.py` | Release Candidate | Learning Mode / plan-bound topic selection (IA-004 lineage) |
| `app/services/readiness_service.py` | Release Candidate | Readiness claims aligned to educational authority |
| `app/services/recommendation_service.py` | Release Candidate | Recommendation honesty / explainability |
| `app/services/study_plan_service.py` | Release Candidate | Continuity / plan lifecycle alignment (EIP-005) |
| `app/settings/routes.py` | Release Candidate | Minor Integrity Programme alignment |
| `app/study_plan/routes.py` | Release Candidate | Continuity delete flash / plan lifecycle (EIP-005) |
| `app/templates/analytics/index.html` | Release Candidate | Student surfaces + explainability partial |
| `app/templates/dashboard/index.html` | Release Candidate | Student surfaces + explainability partial |
| `app/templates/mission/index.html` | Release Candidate | Student surfaces + explainability partial |
| `app/templates/study_plan/edit.html` | Release Candidate | EIP-006 terminology / honesty copy |
| `app/templates/study_plan/list.html` | Release Candidate | EIP-006 terminology / honesty copy |
| `app/templates/study_plan/view.html` | Release Candidate | EIP-006 terminology / honesty copy |
| `app/templates/study_plan/wizard_step_4.html` | Release Candidate | EIP-006 terminology / honesty copy |
| `knowledge/product/internal_alpha/IA-001_MISSION_RECOMMENDATION_INTEGRITY.md` | Release Candidate | Product capability record update |
| `knowledge/product/internal_alpha/README.md` | Release Candidate | Index update (IA-004 / related) |
| `tests/application/test_recommendation_card_builder.py` | Release Candidate | Regression for messaging / explainability |
| `tests/conftest.py` | Release Candidate | Test harness support for EIP/IA suite |
| `tests/test_curriculum_integration.py` | Release Candidate | Curriculum + educational behaviour alignment |
| `tests/test_ia003_student_centred_educational_messaging.py` | Release Candidate | IA-003 regression maintained against EIP copy |
| `tests/test_routes.py` | Release Candidate | V1S-002 Continuity flash assertions (ES-C-001) |
| `tests/test_services.py` | Release Candidate | Service contract updates for EIP/IA |
| `tests/test_smoke.py` | Release Candidate | V1S-002 Continuity flash assertions (ES-C-001) |
| `tests/test_study_plan_service.py` | Release Candidate | Continuity / plan service regression |

---

### Untracked application / test artefacts

| Path | Category | Rationale |
|------|----------|-----------|
| `app/services/educational_continuity_service.py` | Release Candidate | EIP-005 implementation |
| `app/services/educational_evidence_authority.py` | Release Candidate | EIP-002 implementation |
| `app/services/educational_explainability_service.py` | Release Candidate | EIP-003 implementation |
| `app/templates/partials/educational_explainability.html` | Release Candidate | EIP-003 What / Why / Next partial |
| `tests/test_eip001_educational_state_ownership.py` | Release Candidate | EIP-001 regression |
| `tests/test_eip002_educational_evidence_authority.py` | Release Candidate | EIP-002 regression |
| `tests/test_eip003_educational_explainability.py` | Release Candidate | EIP-003 regression |
| `tests/test_eip005_educational_continuity.py` | Release Candidate | EIP-005 regression |
| `tests/test_eip006_version1_educational_state_refinement.py` | Release Candidate | EIP-006 regression |
| `tests/test_ia004_truthful_learning_progress.py` | Release Candidate | IA-004 regression |

---

### Untracked educational / product / release knowledge

| Path | Category | Rationale |
|------|----------|-----------|
| `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` | Release Candidate | Constitutional authority |
| `knowledge/educational/EDUCATIONAL_LOGIC_REGISTRY.md` | Release Candidate | Logic Registry authority |
| `knowledge/educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md` | Release Candidate | EIP-001 |
| `knowledge/educational/EDUCATIONAL_EVIDENCE_AUTHORITY.md` | Release Candidate | EIP-002 |
| `knowledge/educational/EDUCATIONAL_EVIDENCE_MODEL.md` | Release Candidate | EIP-002-DESIGN |
| `knowledge/educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md` | Release Candidate | EIP-003 |
| `knowledge/educational/EDUCATIONAL_GOVERNANCE_RECERTIFICATION.md` | Release Candidate | EIP-004 |
| `knowledge/educational/EDUCATIONAL_CONTINUITY_STANDARD.md` | Release Candidate | EIP-005 |
| `knowledge/educational/EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md` | Release Candidate | EIP-005-DESIGN |
| `knowledge/educational/VERSION1_EDUCATIONAL_STATE_REFINEMENT.md` | Release Candidate | EIP-006 |
| `knowledge/educational/KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md` | Release Candidate | EIP-006-DESIGN |
| `knowledge/educational/EDUCATIONAL_GOVERNANCE_CERTIFICATION_V1.md` | Release Candidate | EIP-007 |
| `knowledge/educational/EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md` | Release Candidate | EGI review standard |
| `knowledge/educational/EDUCATIONAL_INTEGRITY_PROGRAMME_BLUEPRINT.md` | Release Candidate | Programme blueprint |
| `knowledge/educational/EDUCATIONAL_PHILOSOPHY_AUDIT_V2.md` | Release Candidate | Educational philosophy audit V2 |
| `knowledge/product/EDUCATIONAL_PHILOSOPHY_AUDIT.md` | Release Candidate | Product philosophy audit (programme input) |
| `knowledge/product/internal_alpha/IA-001_FOLLOWUP_TOPIC_SELECTION_RCA.md` | Release Candidate | IA-001 follow-up disposition record |
| `knowledge/product/internal_alpha/IA-004_TRUTHFUL_LEARNING_PROGRESS.md` | Release Candidate | IA-004 capability record |
| `knowledge/release/ENGINEERING_STABILISATION_BACKLOG.md` | Release Candidate | V1S-001 release engineering trail |
| `knowledge/release/V1S002_ENGINEERING_REVIEW.md` | Release Candidate | V1S-002 engineering clearance record |
| `knowledge/release/KWALITEC_VERSION1_RELEASE_CERTIFICATION.md` | Release Candidate | V1R-001 certification artefact |
| `knowledge/release/VERSION1_RELEASE_CANDIDATE.md` | Release Candidate | This V1S-003 preparation artefact |

---

### Untracked research / tooling

| Path | Category | Rationale |
|------|----------|-----------|
| `research/internal_alpha/week_001/**` (all week artefacts listed in git status) | Research | Week_001 raw feedback, processed findings, decisions, archive, weekly review, release notes for research process |
| `scripts/run_internal_alpha.py` | Research | Internal Alpha research workflow runner — not Version 1 product runtime |
| `scripts/README.md` | Research | Documents research runner |

---

### Temporary / Ignore

| Path | Category | Action |
|------|----------|--------|
| `research/internal_alpha/week_001/.DS_Store` | Ignore / Temporary | Gitignored; must never be staged |
| `.ruff_cache/`, `.pytest_cache/`, `__pycache__/` | Ignore | Local caches; already ignored; not in status |

**No Temporary application artefacts** appear in the dirty tree.

---

## Task 2 — Staging Plan

### Files to stage (Release Candidate fingerprint)

Stage **exactly** the Release Candidate set from Task 1:

1. **Application (modified)** — all 20 `app/**` paths listed above  
2. **Application (new)** — three educational services + explainability partial  
3. **Tests (modified)** — all eight modified test/harness paths  
4. **Tests (new)** — all six `test_eip00*` / `test_ia004*` modules  
5. **Knowledge educational** — all fifteen `knowledge/educational/*` files listed above  
6. **Knowledge product** — philosophy audit + IA-001 follow-up RCA + IA-004 + IA-001 doc delta + README  
7. **Knowledge release** — V1S-001, V1S-002, V1R-001, and this V1S-003 document  

Suggested path-scoped add (illustrative; execute only after Executive authorization):

```bash
git add \
  app/analytics/routes.py \
  app/application/dashboard/recommendation_card_builder.py \
  app/dashboard/routes.py \
  app/mission/routes.py \
  app/models/topic_progress.py \
  app/services/adaptive_learning_service.py \
  app/services/educational_continuity_service.py \
  app/services/educational_evidence_authority.py \
  app/services/educational_explainability_service.py \
  app/services/learning_service.py \
  app/services/planning_service.py \
  app/services/readiness_service.py \
  app/services/recommendation_service.py \
  app/services/study_plan_service.py \
  app/settings/routes.py \
  app/study_plan/routes.py \
  app/templates/analytics/index.html \
  app/templates/dashboard/index.html \
  app/templates/mission/index.html \
  app/templates/partials/educational_explainability.html \
  app/templates/study_plan/edit.html \
  app/templates/study_plan/list.html \
  app/templates/study_plan/view.html \
  app/templates/study_plan/wizard_step_4.html \
  knowledge/educational/ \
  knowledge/product/EDUCATIONAL_PHILOSOPHY_AUDIT.md \
  knowledge/product/internal_alpha/ \
  knowledge/release/ \
  tests/application/test_recommendation_card_builder.py \
  tests/conftest.py \
  tests/test_curriculum_integration.py \
  tests/test_eip001_educational_state_ownership.py \
  tests/test_eip002_educational_evidence_authority.py \
  tests/test_eip003_educational_explainability.py \
  tests/test_eip005_educational_continuity.py \
  tests/test_eip006_version1_educational_state_refinement.py \
  tests/test_ia003_student_centred_educational_messaging.py \
  tests/test_ia004_truthful_learning_progress.py \
  tests/test_routes.py \
  tests/test_services.py \
  tests/test_smoke.py \
  tests/test_study_plan_service.py
```

### Files to exclude (do not stage for VERSION1-RC1)

| Path / tree | Reason |
|-------------|--------|
| `research/internal_alpha/week_001/` | Research week packaging — not product RC |
| `scripts/run_internal_alpha.py` | Research tooling |
| `scripts/README.md` | Research tooling docs |
| Any `.DS_Store`, caches, `__pycache__`, `.env`, credentials | Temporary / secrets / noise |

### Files to archive later

| Artefact | Deferred action |
|----------|-----------------|
| `research/internal_alpha/week_001/` | Commit or archive under research programme when Executive authorizes research persistence (separate from Version 1 RC) |
| `scripts/run_internal_alpha.py` + `scripts/README.md` | Commit with research tooling tranche, or relocate per research ops standard |
| Historical local caches | Remain ignored; no archive required |

---

## Task 3 — Release Candidate Cleanliness

Verification of the **proposed RC content set** (not of a created commit):

| Check | Result |
|-------|--------|
| Accidental research in RC stage set | **None** — week_001 and research scripts explicitly excluded |
| Temporary artefacts in stage set | **None** |
| Cache / generated noise in `git status` | **None** |
| Secrets (`.env`, credentials) in dirty tree | **None observed** |
| Alembic / migration noise in dirty tree | **None** — no migration files pending |
| RC mix with research | **Avoided** by staging plan |

**Working tree cleanliness after preparation:** still **dirty** (expected). ES-C-002 closes only when the intentional RC commit is created and the tree is re-verified clean of *unintended* residue (research may remain unstaged).

---

## Task 4 — Release Candidate Fingerprint

| Field | Value |
|-------|--------|
| **Commit target** | One intentional commit on `main` containing the staged Release Candidate set above; closes **ES-C-002**. **Not created under V1S-003.** |
| **Pre-commit baseline (HEAD)** | `2f99e6b453a231b85c7067cb67ff258e54752f94` (`v0.9.2` release notes commit) |
| **Release Candidate identifier** | `VERSION1-RC1` |
| **Proposed commit message (illustrative)** | `feat(release): land Version 1 Integrity Programme release candidate (VERSION1-RC1)` |
| **Release scope** | Educational Integrity Programme (EIP-001–EIP-007 artefacts + implementation), Internal Alpha IA-004 + related surface/test alignment, V1S-001/002 engineering stabilisation records, V1R-001 certification artefact, this preparation doc |
| **Out of scope for this RC** | Research week_001 packaging; Internal Alpha research runner scripts; tagging; push; deploy; new product features beyond already-implemented EIP/IA work |
| **Included capabilities** | See below |
| **Tag** | **Deferred.** Do not tag under V1S-003. Historical tags `v1.0.0` / `v1.2.0` / `v1.3.0` / `v1.4.0-beta` already exist on ancestry; Executive must assign the Version 1 public tag strategy separately (cannot silently reuse `v1.0.0`). Latest Internal Alpha ship remains `v0.9.2`. |
| **Migrations** | None in this candidate set |
| **Pytest (declared engineering state)** | **2139 passed / 0 failed** (V1S-002 evidence) — re-run required after any future RC commit before ship |
| **Educational Governance** | **APPROVED** (EIP-007) — not reopened |
| **Engineering RC pillar** | **Prepared, not APPROVED** until commit lands and post-commit clean-tree + pytest re-verification |

### Included capabilities

| ID | Title | In RC |
|----|-------|-------|
| EIP-001 | Educational State Ownership | Yes |
| EIP-002 | Educational Evidence Authority | Yes |
| EIP-003 | Educational Explainability | Yes |
| EIP-004 | Educational Governance Re-certification | Yes (knowledge baseline) |
| EIP-005 | Educational Continuity | Yes |
| EIP-006 | Version 1 Educational State Refinement | Yes |
| EIP-007 | Educational Governance Certification V1 | Yes (knowledge certificate) |
| IA-001 | Mission Recommendation Integrity | Already on `v0.9.2`; doc delta staged |
| IA-002 | Study Plan State Synchronization | Already on `v0.9.2` |
| IA-003 | Student-Centred Educational Messaging | Already on `v0.9.2`; tests/docs kept aligned |
| IA-004 | Truthful Learning Progress | Yes (new in dirty tree) |
| V1S-001 | Engineering Stabilisation Backlog | Yes (knowledge) |
| V1S-002 | Engineering Stabilisation Corrections | Yes (test continuity asserts + review doc) |
| V1S-003 | Release Candidate Preparation | Yes (this document only; no commit) |
| V1R-001 | Version 1 Release Certification | Yes (knowledge; historically NOT READY pending Engineering/Architecture/Alpha gates) |

### Explicitly not included

- Creating/pushing the RC commit  
- Creating/pushing any git tag  
- Deploying to any environment  
- Internal Alpha week_001 research commit  
- Architecture APPROVED paperwork (still Process gate)  
- Internal Alpha trust re-confirmation evidence (Product / process)

---

## Release Candidate Readiness

| Dimension | Status |
|-----------|--------|
| Staging plan complete | **Yes** |
| Content classification complete | **Yes** |
| Candidate set free of research/temp/cache | **Yes (by plan)** |
| Intentional commit created | **No** — stopped for Executive Review |
| Fingerprint hash (post-commit) | **N/A** until commit exists |
| ES-C-002 | **OPEN** until commit |
| EGI-003 composite Version 1 ship | **Not cleared** — Engineering RC commit pending; Architecture / Alpha trust remain separate |

**Verdict:** Release Candidate is **PREPARED FOR EXECUTIVE REVIEW**. It is **not** created.

---

## Engineering Recommendation

1. **Accept V1S-003** as complete for operational RC preparation.  
2. **Authorize** (separate Executive instruction) one intentional `VERSION1-RC1` commit using the staging plan above.  
3. **Exclude** `research/internal_alpha/week_001/` and `scripts/` from that commit.  
4. After commit: re-run full pytest, confirm tree has only intentional research residue (or is clean if research also committed separately), then proceed under Release Protocol — still **no tag/deploy** until subsequent Executive authorization.  
5. **Do not** treat historical `v1.0.0` as this Version 1 programme’s ship tag without an explicit versioning decision.

---

## Constraints Honoured

- No application features implemented under V1S-003  
- No commits / push / tag / deploy  
- Release Candidate not created  

---

## Closing

**Stop.**  
**Return for Executive Review.**  
**Do not create the Release Candidate.**

**End of V1S-003 — Release Candidate Preparation**
