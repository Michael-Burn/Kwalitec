# EA-006 — Regression Report

**Programme:** Educational Excellence Programme EA-006 — Educational Package Publication  
**Date:** 2026-08-01  
**Question:** Did publishing one certified educational package change Runtime A, Runtime C selection, SCI, Twin, or recommendation logic?

---

## 1. Verdict

**No architectural regressions.** Educational content for CS1 topic **4.2** is replaced via a content-layer package; authorities and selection engines remain intact.

---

## 2. Constraint checklist

| Constraint | Status | Evidence |
|------------|--------|----------|
| Do NOT redesign Runtime A | Met | No changes under Runtime A ownership / decision assembly beyond educational copy overlays |
| Do NOT redesign Runtime C | Met | Topic selection / mission generation algorithm unchanged; only prefers overlaid certified `display_title` when foundation supplies one |
| Do NOT redesign SCI | Met | `sci_lifecycle.py` untouched |
| Do NOT redesign recommendations | Met | `recommendation_service.py` untouched |
| Do NOT redesign Student Digital Twin | Met | Twin application packages untouched |
| Do NOT introduce new UI features | Met | Existing Home / Session shells; no new routes or templates |
| Do NOT perform subject-wide rewrite | Met | One package: CS1 4.2 only |
| Only educational content changes | Met | Pack JSON + content consumption hooks |

---

## 3. Files changed (application)

### New (educational content layer)

| Path | Role |
|------|------|
| `app/curriculum/data/educational_packages/cs1/4.2-glm-structure-ea006.json` | Certified package artefact |
| `app/application/educational_packages/*` | Loader, models, substance map, composition overlay |
| `tests/application/educational_packages/test_ea006_publication.py` | Publication / substance / composition tests |

### Modified (content consumption only)

| Path | Nature of change |
|------|------------------|
| `app/application/learning_session/substance_planner.py` | Prefer certified pack substance when topic matches |
| `app/application/educational_authoring/composition.py` | Prefer pack Mission composition when topic matches |
| `app/application/educational_engine_foundation/service.py` | Overlay pack title/rationale/tasks onto derived mission templates |
| `app/application/educational_runtime_engine/service.py` | Use non-`Study …` template title when pack overlaid (content chrome) |
| `app/application/student_runtime/coordinator.py` | Overview why/objective from substance rationale |
| `app/infrastructure/adapters/learning_session/runtime_engine.py` | Reflection prompt from pack when topic matches |
| `app/presentation/student/services/student_home_service.py` | Display title / why_now / expected benefit from pack |
| `app/presentation/session/sitting_report.py` | Tomorrow line from pack when topic matches |

### Explicitly unchanged (spot-checked)

| Path / area | Status |
|-------------|--------|
| `app/application/curriculum_intelligence/certified_mission_engine.py` | Unchanged |
| `app/application/educational_runtime_engine/sci_lifecycle.py` | Unchanged |
| `app/services/recommendation_service.py` | Unchanged |
| `app/application/student_digital_twin` / Twin packages | Unchanged |
| `app/services/runtime_ownership.py` | Unchanged |
| Curriculum JSON `app/curriculum/data/ifoa/cs1/2026.json` | Unchanged |
| Templates / new UI routes | Unchanged |

---

## 4. Behavioural regression notes

| Behaviour | Expected | Result |
|-----------|----------|--------|
| Topic selection order | Unchanged (syllabus / Runtime C) | Unchanged |
| SCI lifecycle transitions | Unchanged | Unchanged |
| Twin update math | Unchanged | Unchanged |
| Recommendation ranking | Unchanged | Unchanged |
| Non-4.2 topics | Continue templated substance | Confirmed by negative resolution test |
| Session FSM / shell | Same Read → Example → Practice | Same shell; richer content |

---

## 5. Tests executed

```text
python3 -m pytest tests/application/educational_packages/test_ea006_publication.py \
  tests/test_lxp004a_session_substance.py tests/test_kwp004_assessable_practice.py -q
```

**Outcome:** 34 passed.

```text
python3 -m ruff check app/application/educational_packages \
  app/application/educational_authoring/composition.py \
  app/application/learning_session/substance_planner.py \
  app/application/educational_engine_foundation/service.py \
  app/application/educational_runtime_engine/service.py \
  app/presentation/student/services/student_home_service.py \
  app/application/student_runtime/coordinator.py \
  app/infrastructure/adapters/learning_session/runtime_engine.py \
  app/presentation/session/sitting_report.py
```

**Outcome:** All checks passed.

---

## 6. Residual risks (not regressions introduced)

1. Existing open `RuntimeMissionInstance` rows may still store pre-publish syllabus-paste titles until regenerated; Home overlays correct display for matching topics.  
2. Curriculum contaminant topic (EV-001 TB-003) remains until a separate curriculum republish.  
3. Production dogfood pending deploy.

---

## 7. Closing

EA-006 changes **what educational content** students see for one certified package. It does not change **how** the product selects topics, scores readiness, updates the Twin, or ranks recommendations.
