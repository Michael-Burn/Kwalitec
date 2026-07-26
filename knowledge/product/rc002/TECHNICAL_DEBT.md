# RC-002 — Technical Debt (Category C)

**Programme:** RC-002  
**Date:** 2026-07-27  
**Count:** **8**

---

## Definition (charter)

Architecture purity, internal structure, performance budget, maintainability. **Safe for deployment.**

---

## C1 — Student-experience application imports

| Field | Evidence |
|-------|----------|
| **Test** | `tests/application/student_experience/test_independence.py::test_application_no_forbidden_imports` |
| **Purpose** | Hexagonal boundary: application layer must not import Flask/SQLAlchemy/models/services/infrastructure |
| **Expected** | `_offenders(APP_ROOT) == []` |
| **Actual** | 11 offenders — e.g. `recommendation_commitment.py` → `app.extensions`, `app.models.recommendation_commitment`, `app.services.recommendation_service`, `app.infrastructure.adapters.learning_feedback`; explanation modules → readiness/recommendation quality services |
| **Root cause** | EP-008.3 commitment + explainability services wired persistence directly into application package |
| **Category** | **C** |
| **Deployment impact** | None observed for Stage 1 runtime; coupling debt |
| **Recommendation** | Introduce ports; move ORM/service calls to infrastructure adapters |
| **Evidence** | Pytest offender list (first item: `recommendation_commitment.py: from app.extensions`) |

---

## C2 — Reflection route line budget

| Field | Evidence |
|-------|----------|
| **Test** | `tests/education_os/adapters/flask/test_architecture_purity.py::test_route_handlers_stay_thin[reflection/routes.py]` |
| **Purpose** | EOS Flask handlers ≤ 45 lines |
| **Expected** | `submit_reflection` ≤ 45 |
| **Actual** | 50 lines |
| **Root cause** | Experience context wiring duplicated in POST handler |
| **Category** | **C** |
| **Deployment impact** | None — handler functions; EOS not Stage 1 prod mount |
| **Recommendation** | Extract helper / push assembly into controller |
| **Evidence** | `AssertionError: submit_reflection is 50 lines (max 45)` |

---

## C3 — `prioritise` on adaptive mission generator

| Field | Evidence |
|-------|----------|
| **Test** | `tests/education_os/application/test_architecture_purity.py::test_no_educational_intelligence_methods[education/mission_generation/adaptive_mission_generator.py]` |
| **Purpose** | Forbid educational-intelligence method names in application mission generation |
| **Expected** | No method named `prioritise` |
| **Actual** | `AdaptiveMissionGenerator.prioritise` delegates to ordering rules (execution order, not Runtime A ranking) |
| **Root cause** | Vocabulary collision with purity allowlist |
| **Category** | **C** |
| **Deployment impact** | None |
| **Recommendation** | Rename to `order_missions_for_execution` or document allowlist |
| **Evidence** | Assert `'prioritise' not in methods` fails |

---

## C4 — `prioritise` on ordering rules

| Field | Evidence |
|-------|----------|
| **Test** | `…::test_no_educational_intelligence_methods[education/mission_generation/rules/ordering_rules.py]` |
| **Purpose** | Same purity gate |
| **Expected** | No `prioritise` |
| **Actual** | `OrderingRules.prioritise` sorts by priority magnitude / type / id |
| **Root cause** | Same as C3 |
| **Category** | **C** |
| **Deployment impact** | None |
| **Recommendation** | Same as C3 |
| **Evidence** | Assert failure naming `prioritise` |

---

## C5 — Digital Twin imports student experience (T4)

| Field | Evidence |
|-------|----------|
| **Test** | `tests/infrastructure/adapters/adaptive_engine/test_twin_input_integration.py::test_digital_twin_does_not_import_experience_for_t4` |
| **Purpose** | Twin package must not import student_experience adapters |
| **Expected** | No `app.infrastructure.adapters.student_experience` in twin `*.py` |
| **Actual** | `shadow_rollback.py` lazily imports `build_production_experience` |
| **Root cause** | Rollback verification drill embeds experience composition import |
| **Category** | **C** |
| **Deployment impact** | None — observational/rollback tooling; Twin OFF in production defaults |
| **Recommendation** | Inject composition factory; remove hard import from twin package text |
| **Evidence** | Assert fails on `shadow_rollback.py` import string |

---

## C6 — Application must not import infrastructure (authority)

| Field | Evidence |
|-------|----------|
| **Test** | `tests/infrastructure/authority/test_authority.py::test_adapters_do_not_import_flask_into_application_ports` |
| **Purpose** | `app/application/` must not import `app.infrastructure.*` |
| **Expected** | `offenders == []` |
| **Actual** | 6 files — analytics dispatcher/events from `educational_state`, `journey_observation`, `reflection_manager`, `twin_repository/observation`; learning_feedback from `recommendation_commitment` |
| **Root cause** | Analytics emit hooks + EP-008.3 feedback adapter in application layer |
| **Category** | **C** |
| **Deployment impact** | None for Stage 1 function |
| **Recommendation** | Event publisher port in application |
| **Evidence** | First offender: `educational_state/__init__.py` |

---

## C7 — Application independence (duplicate gate)

| Field | Evidence |
|-------|----------|
| **Test** | `tests/infrastructure/test_independence.py::test_application_does_not_import_infrastructure` |
| **Purpose** | Same boundary as C6 with path:import reporting |
| **Expected** | No infrastructure imports under `app/application` |
| **Actual** | Same six import paths as C6 |
| **Root cause** | Same as C6 |
| **Category** | **C** |
| **Deployment impact** | None |
| **Recommendation** | Same as C6 |
| **Evidence** | Pytest offender list mirrors C6 |

---

## C8 — First-party CSS soft budget

| Field | Evidence |
|-------|----------|
| **Test** | `tests/test_v1sp003_performance.py::TestStaticAssetsOptimised::test_first_party_css_js_under_budget` |
| **Purpose** | V1SP-003 static CSS budget `< 70_000` bytes |
| **Expected** | `css_bytes < 70_000` |
| **Actual** | `70362` (+362) |
| **Root cause** | CSS growth from subsequent PX/RC accessibility and shell work without budget revision |
| **Category** | **C** |
| **Deployment impact** | Negligible for Stage 1 pilot; soft governance budget |
| **Recommendation** | Trim unused CSS or raise budget with documented rationale after measuring LCP |
| **Evidence** | `assert 70362 < 70000` |

---

## Post-release notes

These items improve long-term maintainability and CI hygiene. They do not change the RC-002 release decision.
