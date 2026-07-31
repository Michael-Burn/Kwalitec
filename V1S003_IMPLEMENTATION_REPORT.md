# V1S-003 — Engineering Quality & Repository Simplification

**Programme:** V1S-003 · Version 1 Stabilisation  
**Phase:** Engineering quality + repository health  
**Date:** 2026-07-31  
**Nature:** Maintainability, clarity, consistency — **no new educational capabilities**  
**Authority:** V1S-002 · V1S-001 · KWP-015 · `PRODUCT_BLUEPRINT.md` · `V1_RELEASE_CRITERIA.md`

---

## Executive Summary

V1S-003 audited the full repository and published a **package lifecycle matrix** so every audited package has one responsibility, one owner, and one lifecycle (`ACTIVE` | `MAINTENANCE` | `DEPRECATED` | `ARCHIVED` | `REMOVE`). Engineering standards for repository layout, naming, modules, app dependency direction, and package lifecycle now live under `docs/engineering/`. The Founder Version 1 Readiness dashboard gained **Repository Health**, **Package Lifecycle**, **Engineering Quality**, and **Code Debt** sections.

**Verdict:** **DOGFOOD GO WITH CONDITIONS** (unchanged educationally). Repository navigability is improved by ownership and standards; physical simplification (deletes, report relocation, `src/` archive) remains gated follow-up work. No student product behaviour changed.

---

## Repository Audit

### Shape (measured)

| Tree | Approx Python LOC | Role |
|---|---|---|
| `app/application` | ~124k / 849 files | Product application engines |
| `app/domain` | ~52k | Product domain |
| `app/infrastructure` | ~88k | Adapters |
| `app/services` | ~29k | Flask-era orchestration |
| `app/presentation` | ~19k | Student / session HTTP |
| `src/` (Education OS) | ~120k+ | Parallel OS — **not** dogfood runtime |
| `tests/` | ~1100 test modules | Behaviour + architecture |

### Dual-tree finding

`app/` and `src/` do not import each other on the product path (`pythonpath` includes `src` for tests only). Dogfood authority remains under `app/`. `src/` is classified **MAINTENANCE / ARCHIVED** relative to commercial dogfood until an adopt-or-archive programme decides.

### Root clutter

50+ programme reports at repository root (`KWP*`, `MISSION*`, `SR*`, …). Standards now direct completed reports to `docs/reports/` — relocation not executed in this programme (docs-only risk to git history / links).

### Mandatory classification

Canonical registry: `app/services/package_lifecycle.py`.

| Lifecycle | Count (registry) | Meaning |
|---|---|---|
| ACTIVE | 46 | Live product / founder growth surface |
| MAINTENANCE | 52 | Needed; not the growth surface |
| DEPRECATED | 10 | Superseded; no new callers |
| ARCHIVED | 6 | Unwired; tests/history only |
| REMOVE | 1 | Deletion gated (`domain/learning_events`) |

All **69** `app/application/*` packages are registered (enforced by test).

---

## Package Lifecycle Matrix

### Dogfood ACTIVE spine (grow here)

| Package | Owner | Notes |
|---|---|---|
| `educational_runtime_engine` | Educational Runtime | Mission instance authority |
| `learning_session` | Learning Session Runtime | Sitting FSM |
| `student_runtime` | Student Runtime Coordinator | Spine glue |
| `educational_experience` | Educational Experience | Runtime C snapshots |
| `curriculum_intelligence` | Curriculum Intelligence | CertifiedMissionEngine |
| `curriculum_studio` / `_foundation` | Curriculum Studio | Publish + authority |
| `progress_engine` | Progress Engine | Progress writes |
| `learning_strategy` … `educational_authoring` | KWP-007…015 | CLEAN authorities |
| `session_experience` | Session Experience | HTTP adapter |
| `platform_integration` / `config` | Platform | Routing + flags |

### DEPRECATED / ARCHIVED / REMOVE (do not grow)

| Package | Lifecycle | Recommendation | Gate |
|---|---|---|---|
| `mission_engine` | DEPRECATED | extract planning/ | Then archive shell |
| `mission_engine_v2` | ARCHIVED | remove | Independence-test migration |
| `mission_adapter` | ARCHIVED | remove | With MEV2 |
| `learning_orchestrator` | DEPRECATED | archive | Orchestrator flag OFF |
| `learning_loop` | ARCHIVED | remove | Zero consumers |
| `instructional_blueprint` | ARCHIVED | remove | Tests-only |
| `app/mission`, `dashboard`, `analytics` | DEPRECATED | archive | RI-002 sole-runtime |
| `domain/learning_events` | REMOVE | remove | Confirm no dynamic import |
| `src/web`, `src/adapters` | ARCHIVED | remove | Not create_app |

### Twin / naming debt (MAINTENANCE + merge)

`twin` / `student_twin` / `student_digital_twin` (application + domain) — pick one canonical name in a twin consolidation follow-up; do not add a fourth package.

Full matrix (top-level, application, notable domain, src/, docs clutter) is code-backed in `package_lifecycle.py` and rendered on `/founder/v1-readiness`.

---

## Dependency Review

| Rule | Finding |
|---|---|
| Presentation → application/services → domain | Holds for dogfood path |
| `app` ↔ `src` runtime coupling | **None** (AST guard) |
| Student presentation → archived mission packages | **None** (guard retained) |
| Curriculum format detection | Still `load_auto` only |
| Cross-application hotspots | `curriculum` facade (~128 importers), `twin` (~23), `mission_engine` (~25 — mostly EI / adaptive mission) |
| `src/` dependency law | Existing `docs/DEPENDENCY_RULES.md` + `tests/architecture/` |
| `app/` dependency law | **New** `docs/engineering/DEPENDENCY_RULES_APP.md` |

Circular risk: no hard import cycles found at package level for the dogfood spine; oversized packages (`curriculum_intelligence`, ERE service) remain cognitive — not circular — debt.

---

## Code Quality Review

| Area | Assessment | Action |
|---|---|---|
| Naming | HOLD — triple twin; dual reasoning/experience engines | Naming Standards + merge recommendations |
| Documentation | Mixed — strong package docs on KWP engines; root report noise | Repository Standards root hygiene |
| Comments | Acceptable on new KWP code; avoid engine nouns in UI | Unchanged |
| Type hints | Generally present on new application modules | Module Standards |
| Logging | Module loggers common; no change | Module Standards |
| Error handling | Specific exceptions on session/runtime paths | Retain |
| Configuration | Flags concentrated in platform_integration / config | Retain |
| Consistency | Layering OK; dual-tree is the consistency tax | Freeze dogfood work in `src/` |
| God modules | planning (~1658), recommendation (~1460), research_insight (~1530), ERE service (~1390), student view_models (~2365), evidence contracts (~2457) | Split guidance in Module Standards — **not split this programme** |

---

## Test Quality Review

| Signal | Assessment |
|---|---|
| Coverage shape | Strong programme suites (`test_kwp*`, `test_v1s*`) + architecture purity under `tests/architecture/` and `src` domain |
| Behaviour tests | Prefer these for ACTIVE packages — pattern is healthy on KWP/V1S |
| Regression | Curriculum V1/V2 and independence suites retained |
| Architecture tests | Excellent for `src/`; app now gains lifecycle + import guards |
| Risk | Archived packages still carry large independence suites (~MEV2/adapter) — delete with REMOVE gates |
| Avoided this programme | No implementation-only tests; no duplicate suite explosion |

New suite: `tests/test_v1s003_repository_health.py` (registry integrity, full application registration, archived alignment, presentation import guard, app↛src guard, standards presence, readiness sections).

---

## Technical Debt

### Removed / closed by V1S-003

| Item | Action |
|---|---|
| Unowned application packages | **Closed** — all 69 registered |
| Undocumented engineering standards for `app/` | **Closed** — `docs/engineering/` |
| Founder readiness missing repo health | **Closed** — dashboard sections |
| Silent dual-tree status | **Documented** — src/ MAINTENANCE/ARCHIVED vs dogfood |

### Remaining (owned)

| Item | Severity | Owner | Gate |
|---|---|---|---|
| Physical delete MissionEngineV2 + MissionAdapter | High | Mission consolidation | Test migration |
| Extract MissionPlanningService; retire ME shell | High | Mission consolidation | New `mission_planning/` |
| Adopt-or-archive `src/` Education OS | High | Architecture | Programme decision |
| God services / view_models splits | Medium | Platform | Module Standards plan |
| Twin package consolidation | Medium | Twin consolidation | Canonical name |
| Root report relocation | Low | Docs hygiene | Move to `docs/reports/` |
| `domain/learning_events` delete | Low | Domain housekeeping | Dynamic-import check |
| Progress singularity / RI-002 | High | Prior programmes | Out of V1S-003 |

---

## Recommendations

1. **Grow only ACTIVE** packages on the dogfood spine; treat MAINTENANCE as bugfix-only.
2. **Freeze** new dogfood features under `src/`.
3. **Next delete programme:** MissionEngineV2 + MissionAdapter after independence-test migration.
4. **Extract** `mission_engine.planning` → `mission_planning/` before deleting ME shell.
5. **Decide** adopt-or-archive for `src/` within the next stabilisation train.
6. **Relocate** completed root reports to `docs/reports/` in a docs-only commit.
7. **Do not** redesign Adaptive Workspace, KWP engines, or curriculum cutover in engineering programmes.
8. Use `/founder/v1-readiness` as the living package/runtime board.

---

## Engineering Standards

Published:

| Document | Path |
|---|---|
| Repository Standards | `docs/engineering/REPOSITORY_STANDARDS.md` |
| Naming Standards | `docs/engineering/NAMING_STANDARDS.md` |
| Module Standards | `docs/engineering/MODULE_STANDARDS.md` |
| Dependency Rules (app/) | `docs/engineering/DEPENDENCY_RULES_APP.md` |
| Package Lifecycle Policy | `docs/engineering/PACKAGE_LIFECYCLE_POLICY.md` |

Companion (pre-existing, `src/`): `docs/DEPENDENCY_RULES.md`, `docs/ENGINEERING_CHARTER.md`, `docs/ARCHITECTURE_CONSTITUTION.md`.

Release criteria extended: **T9** (lifecycle owner), **T10** (standards), **T11** (no `src` imports into `app`).

---

## Architecture Compliance

- Layering preserved: registry + Founder observability + docs only.
- **No** redesign of Learning Runtime, Evidence, Progress, Strategy, Diagnostics, Difficulty, Intervention Effectiveness, Educational Memory, Forecast, Knowledge Architecture, Educational Authoring, or Adaptive Workspace.
- Curriculum V1/V2 loader singularity unchanged (`load_auto`).
- V1S-002 dogfood curriculum cutover and mission spine unchanged.
- Runtime A not hard-deleted.
- Application code intentionally limited to ownership/observability; educational algorithms untouched.

---

## Known Limitations

1. Physical package deletion not executed (gates required).
2. Root programme reports not yet moved (link/history risk).
3. Domain matrix lists notable packages, not every `app/domain/*` directory as exhaustively as application (application is complete; domain highlights debt + ACTIVE pairs).
4. `src/` adopt-or-archive decision deferred.
5. God-module splits deferred (standards only).
6. Does not claim P-002.1 production-ready / Gate G1.
7. Does not add educational intelligence or UI redesign beyond Founder readiness sections.

---

## Student Impact Assessment

Completed using the spirit of `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`.

| Lens | Assessment |
|---|---|
| Student problem | Indirect — engineering debt slows trustworthy delivery |
| Student benefit | No direct UI change; reduces risk of dual truths / accidental archived-package wiring |
| Learning benefit | None this programme (by design) |
| Success metrics | T9–T11 PASS; zero new educational regressions |
| Risks | Over-eager deletes could break independence suites — mitigated by gates |
| Assumptions | Dogfood continues on V1S-002 cutover path |

---

## Estimated KSI contribution

**ΔKSI = 0** (provisional). Infra/docs/ownership programme; no validated student-value measurement. K1–K8 unchanged.

---

## Evidence collected

- `tests/test_v1s003_repository_health.py` — 7 passed  
- `tests/test_v1s002_curriculum_authority_cutover.py` — 11 passed (ownership sections compatible with V1S-003)  
- Ruff clean on touched Python modules  
- Registries: `app/services/package_lifecycle.py`, `app/services/runtime_ownership.py`  
- Standards: `docs/engineering/*`  
- Founder: `/founder/v1-readiness` template + `v1_readiness_dashboard.py`

---

## Lessons learned for student value

Repository complexity (dual `app/`/`src/` trees, 70 application packages, root report noise) is itself a student-value risk: it invites accidental dual authorities. Explicit lifecycle ownership is a precondition for safe simplification; deleting without gates would trade engineering clarity for outages.

---

## Explainability Review

**N/A** — no student-facing intelligence, recommendations, or guidance copy changed.

---

## Recommendation Quality Review

**N/A** — no recommendation ranking/selection changes.

---

## Version 1 readiness residual

Open relative to P-002.1 / dogfood board:

- Gate G1 validated KSI  
- Progress singularity  
- RI-002 Runtime A hard removal  
- Mission package physical REMOVE  
- `src/` adopt-or-archive  
- Published packages required before dogfood enrol (V1S-002 condition)

---

## CRI domains improved

None material (engineering hygiene). **ΔCRI = 0** provisional — no `COMMERCIAL_READINESS_BOARD.md` update required.

---

## Estimated CRI delta

**0** — docs/registry/observability only.

---

## Evidence supporting the increase

N/A (no CRI increase claimed).

---

## Remaining blockers

See Executive Summary / Technical Debt Remaining / Founder readiness remaining blockers.

---

## Provisional or validated

All engineering scores and ΔKSI / ΔCRI claims are **provisional**.

---

## Tests Executed

```
python3 -m pytest tests/test_v1s003_repository_health.py \
  tests/test_v1s002_curriculum_authority_cutover.py -q
```

Outcome: **18 passed**.

```
ruff check app/services/package_lifecycle.py \
  app/services/v1_readiness_dashboard.py \
  tests/test_v1s003_repository_health.py
```

Outcome: clean.

---

## Migration Impact

**None** — no Alembic / schema changes.

---

## Files Created

- `app/services/package_lifecycle.py`
- `docs/engineering/REPOSITORY_STANDARDS.md`
- `docs/engineering/NAMING_STANDARDS.md`
- `docs/engineering/MODULE_STANDARDS.md`
- `docs/engineering/DEPENDENCY_RULES_APP.md`
- `docs/engineering/PACKAGE_LIFECYCLE_POLICY.md`
- `tests/test_v1s003_repository_health.py`
- `V1S003_IMPLEMENTATION_REPORT.md`
- `docs/reports/` (directory reserved for relocated reports)

## Files Modified

- `app/services/v1_readiness_dashboard.py`
- `app/founder/dashboard/templates/founder_dashboard/v1_readiness.html`
- `tests/test_v1s002_curriculum_authority_cutover.py`
- `V1_RELEASE_CRITERIA.md`

## Success criteria

| Criterion | Result |
|---|---|
| Complete repository audit with lifecycle classification | **PASS** |
| Every application package owned | **PASS** |
| Engineering standards produced | **PASS** |
| Founder V1 Readiness extended (Repo Health / Lifecycle / Quality / Code Debt) | **PASS** |
| No new educational capabilities | **PASS** |
| No UI redesign (student) | **PASS** |
| Repository easier to navigate via explicit map | **PASS** (map); physical simplification **HOLD** |
