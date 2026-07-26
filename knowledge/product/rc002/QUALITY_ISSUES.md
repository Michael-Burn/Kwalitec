# RC-002 — Quality Issues (Category B)

**Programme:** RC-002  
**Date:** 2026-07-27  
**Count:** **4**

---

## Definition (charter)

Application functions correctly but quality is reduced (copy inconsistency, explainability gaps, minor accessibility, incorrect messaging). Ideally fixed before pilot — **does not** block deployment when Category A = 0.

---

## Shared root cause

All four failures assert constitutional EIP-003 / EIP-006 / IA-004 vocabulary on **`GET /missions/`** after `PlanningService.generate_today_mission`.

When the Runtime A presentation adapter finds a complete plan-explanation schema, it renders **planning-schema narration** instead of the legacy template fallback that still contains `Learning Mode` / `Current Learning Topic` / `Estimated Knowledge` phrases:

- Adapter: `app/presentation/intelligence_surface/adapter.py` → `_schema_mission_narrative(...)`
- Fallback copy (only when `mission_narrative` absent): `app/templates/mission/index.html` (Learning Mode paragraph)

Live schema-path body still contains:

- `Why you are studying this` ✓  
- `Observed Facts` ✓  
- `Estimates` ✓  
- `Learning Mode` ✗  
- `Current Learning Topic` ✗  
- `Estimated Knowledge` ✗  

**Stage 1 deployment context:** production `KWALITEC_V2_SOLE_RUNTIME=1` routes students to `/student/*`. These tests do **not** set sole runtime and exercise the legacy mission surface. Impact on Stage 1 pilots is therefore **indirect** — standards drift and legacy-path quality — not a sole-runtime home crash.

---

## B1 — `test_mission_page_explains_itself`

| Field | Evidence |
|-------|----------|
| **Test** | `tests/test_eip003_educational_explainability.py::TestPositiveMissionExplainability::test_mission_page_explains_itself` |
| **Purpose** | EIP-003: mission HTML must explain selection with Learning Mode doctrine + Observed Facts / Estimates |
| **Expected** | Body contains `Learning Mode`, `Current Learning Topic`, `Observed Facts`, `Estimates`, `Why you are studying this` |
| **Actual** | Schema path omits Learning Mode / Current Learning Topic; retains Why / Observed Facts / Estimates |
| **Root cause** | Intentional EP-003.3 schema pass-through replaced legacy EIP vocabulary on the default path |
| **Category** | **B** |
| **Deployment impact** | Quality / standards gap on legacy `/missions/`; not Stage 1 sole-runtime primary path |
| **Recommendation** | Either restore Learning Mode phrases in `_schema_mission_narrative`, or update EIP-003 + tests to the new honest schema vocabulary and cover `/student/*` |
| **Evidence** | Pytest assert `'Learning Mode' in body` fails; adapter schema branch; template fallback still has Learning Mode |

---

## B2 — `test_dashboard_and_mission_share_learning_mode_story`

| Field | Evidence |
|-------|----------|
| **Test** | `tests/test_eip003_educational_explainability.py::TestPositiveCoherentStory::test_dashboard_and_mission_share_learning_mode_story` |
| **Purpose** | Coherent Learning Mode story across mission + dashboard |
| **Expected** | `Learning Mode` and `Current Learning Topic` in mission body |
| **Actual** | Same schema-path omission as B1 |
| **Root cause** | Same as B1 |
| **Category** | **B** |
| **Deployment impact** | Indirect (legacy surfaces) |
| **Recommendation** | Same as B1 |
| **Evidence** | Pytest asserts on `/missions/` body; same adapter path |

---

## B3 — `test_mission_page_explains_estimated_knowledge`

| Field | Evidence |
|-------|----------|
| **Test** | `tests/test_eip006_version1_educational_state_refinement.py::TestPositiveVersion1EducationalStates::test_mission_page_explains_estimated_knowledge` |
| **Purpose** | EIP-006 V1: mission distinguishes Estimated Knowledge vs Study Progress |
| **Expected** | `Estimated Knowledge` (and Study Progress) in body |
| **Actual** | Schema path uses Estimates block without the literal `Estimated Knowledge` label; legacy `EducationalExplainabilityService` still emits EK on non-schema path |
| **Root cause** | Schema narration omits V1 EK label |
| **Category** | **B** |
| **Deployment impact** | Labelling quality on legacy mission; not a false readiness claim |
| **Recommendation** | Add EK labelling to schema narrative or retarget EIP-006 tests to sole-runtime student surfaces |
| **Evidence** | Assert `'Estimated Knowledge' in body` fails; service still has EK string on legacy path |

---

## B4 — `test_mission_page_explains_learning_mode`

| Field | Evidence |
|-------|----------|
| **Test** | `tests/test_ia004_truthful_learning_progress.py::TestStudentFacingTerminology::test_mission_page_explains_learning_mode` |
| **Purpose** | IA-004 truthful progress terminology on mission |
| **Expected** | `Learning Mode`, `Current Learning Topic`, Study Progress |
| **Actual** | Same schema-path vocabulary gap as B1 |
| **Root cause** | Same as B1 |
| **Category** | **B** |
| **Deployment impact** | Indirect |
| **Recommendation** | Same as B1 |
| **Evidence** | Assert `'Learning Mode' in body` fails |

---

## Post-release priority

1. Decide source of truth: EIP-003/IA-004 labels **vs** Runtime A schema speech **vs** sole-runtime `/student` explainability (`Why this tip?` / `Why this estimate?`).
2. Implement one coherent student-facing story; update the losing side (product or tests/standards).
3. Add regression coverage under `SOLE_RUNTIME=1` so Stage 1 path is what CI guards.
