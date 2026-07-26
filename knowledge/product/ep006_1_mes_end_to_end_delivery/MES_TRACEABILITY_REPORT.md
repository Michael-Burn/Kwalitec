# EP-006.1 — MES Traceability Report (Delivery Audit)

**Programme:** EP-006.1 — MES End-to-End Delivery  
**Version:** 1.0  
**Date:** 2026-07-26  
**Status:** Evidence audit (no runtime / UI / API changes)  
**Authority:** Subordinate to P-001.2 Explainability Standard  
**Validated baseline:** K8 **65** (EP-005.1); Gate G1.5 **FAIL**

---

## 1. Executive verdict

Runtime A services generate **schema-complete** Meaningful Explanation Schema (MES) payloads for recommendations, planning judgements, and readiness assessments. Downstream presentation **compresses, re-narrates, or omits** those fields before the student sees them.

| Path | MES fidelity at student surface |
|---|---|
| Legacy Dashboard / Mission (`RuntimeAPresentationAdapter`) | **Partial** — evidence + next action via `learn_more`; drivers / review_point dropped |
| Canonical Student Home / Coach | **Poor** — ~4 fields; no evidence list; next action & review_point absent; Coach clipped to 3 sentences |
| Analytics readiness | **Partial** — narrative + `evidence_basis`; drivers unbound |
| Session outcome | **None** — hardcoded completion strings only |

**Critical inversion:** The surface designated as the canonical daily home delivers **less** MES than the legacy Dashboard it is meant to replace. This is the primary mechanism keeping validated K8 below the Version 1 floor of 70.

---

## 2. Scope and method

| Reviewed | Sources |
|---|---|
| Service generation | `app/services/recommendation_quality.py`, `planning_quality.py`, `readiness_quality.py` |
| Bridge / adaptive | `app/infrastructure/adapters/educational_runtime_bridge/recommendation_mapper.py`, `adaptive/adapter.py` |
| Student Experience | `explanation_service.py`, `dto/explanation_snapshot.py`, `home_service.py` |
| Presentation | `app/presentation/intelligence_surface/adapter.py`, `app/presentation/student/view_models.py` |
| Unified Journey | `app/application/unified_journey/contracts.py`, `daily_mission_assembler.py` |
| Templates | `student/home.html`, `dashboard/index.html`, `mission/index.html`, `analytics/index.html`, `student/components/explanation_card.html` |
| Prior evidence | EP-005.2 experience review; EP-003.1–.3 explainability Pass at service layer |

**Does not:** Change code; re-score validated KSI; amend constitutions.

---

## 3. Two delivery paths (structural finding)

There is **no single MES delivery pipeline**. Two independent, unequally lossy paths exist:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Runtime A services (schema-complete MES)                                │
│ RecommendationService / PlanningService / ReadinessService              │
└────────────────────────────┬───────────────────────────┬────────────────┘
                             │                           │
              Legacy path    │                           │  Canonical path
                             ▼                           ▼
              RuntimeAPresentationAdapter      recommendation_mapper (6 keys)
              MissionNarrative /               ExplanationService.from_opaque
              ReadinessNarrative               (re-narrates from reason codes)
                             │                           │
                             ▼                           ▼
              Dashboard / Mission templates    ExplanationSnapshot (5 fields)
              + learn_more disclosure          → Home VM coach_insight (3 sent.)
                             │                           │
                             ▼                           ▼
              Partial MES visible              Poor MES / no evidence card
```

| Dimension | Legacy | Canonical Home |
|---|---|---|
| Entry | `app/dashboard/routes.py` | `app/application/student_experience/home_service.py` |
| Compressor | `RuntimeAPresentationAdapter` | `ExplanationService` → `ExplanationSnapshot` |
| Renders evidence list? | Yes (`explainability_block`) | **No** |
| Progressive disclosure? | Yes (`learn_more`) | **No** |
| Renders next action? | Yes | **No** |
| Renders review_point? | **No** | **No** |

---

## 4. Service generation (intact)

### 4.1 Recommendation

**Owner:** `RecommendationService` via `recommendation_quality.apply_quality_contract()` / `_attach_explanation_schema()`.

`SCHEMA_REQUIRED_KEYS` (`app/services/recommendation_quality.py`):

| Field | Present at service boundary |
|---|---|
| `title`, `reason`, `why_recommended` | Yes |
| `supporting_evidence` | Yes (capped `[:4]`) |
| `confidence_level` | Yes |
| `expected_benefit` | Yes |
| `next_action`, `suggested_next_action` | Yes |
| `review_point` | Yes |
| `decision_ladder_rank`, `plan_coherence` | Yes |
| `explanation_schema_version`, `explanation_level` | Yes |
| EIP-003: `observed_facts`, `estimates`, `educational_advice` | Yes |
| EP-004.2 (flag-gated): `personalisation_factors` | When ON |

**First truncation (acceptable):** evidence list capped at 4 points — still Level-2 compliant if rendered.

### 4.2 Planning

**Owner:** `PlanningService` via `planning_quality.apply_planning_quality_contract()`.

Required: `judgement`, `why_this_plan`, `supporting_evidence`, `confidence_level`, `expected_benefit`, `suggested_next_action`, `review_point`, `plan_drivers`, schema version/level. Also: `change_reasoning`, `readiness_alignment`, `recommendation_alignment`, `plan_coherence`, personalisation_* when gated. Evidence capped `[:6]`. Daily-plan cutover mirrors ~22 keys onto nested payload.

### 4.3 Readiness

**Owner:** `ReadinessService` via `readiness_quality.apply_readiness_quality_contract()`.

Required: `judgement`, `why_this_estimate`, `supporting_evidence`, `confidence_level`, `expected_benefit`, `suggested_next_action`, `review_point`, `readiness_drivers`, schema version/level. Drivers include `curriculum_coverage`, `knowledge_strength`, `mission_discipline`, `evidence_density` with influence + rationale. `change_reasoning` compares vs previous score. Evidence capped `[:5]`.

**Verdict:** All three classes are **schema-complete at the service boundary**. Loss begins downstream. Educational reasoning must not be changed to “fix” presentation.

---

## 5. Adapter / presentation transforms

### 5.1 Legacy — `RuntimeAPresentationAdapter`

**File:** `app/presentation/intelligence_surface/adapter.py`

| Transform | Kept | Dropped / compressed |
|---|---|---|
| `_schema_readiness_narrative` → `ReadinessNarrative` | label, %, explanation, evidence_basis blob, can_estimate | Structured `supporting_evidence` list → joined string; **`readiness_drivers` not read on schema path**; `review_point`, `expected_benefit`, `judgement` text dropped as first-class fields |
| `_schema_mission_narrative` → `MissionNarrative` | observed_facts[:6], estimates pairing confidence+change_reasoning | **`plan_drivers`**, **`review_point`**, expected_benefit (as field), plan_coherence, alignments, personalisation_factors |
| `enrich_recommendations_if_needed` | Schema-complete rows **pass through** as dicts | — |

### 5.2 Bridge mapper (canonical entry)

**File:** `app/infrastructure/adapters/educational_runtime_bridge/recommendation_mapper.py`

Constructs explanation with only:

```text
summary, authority, category, priority, expected_benefit, reason
```

`_narrative_summary()` reduces to `reason` or `title`. ~20 MES fields → **6 keys**. Alternatives receive the same reduction.

### 5.3 ExplanationService (re-narration)

**File:** `app/application/student_experience/explanation_service.py` → `from_opaque()`

Reads: topic/title, reason_codes/reasons, evidence_points/evidence_considered/evidence_phrases, expected_benefit, priority, confidence.

**Does not read** Runtime A authored names: `why_recommended`, `supporting_evidence`, `suggested_next_action`, `review_point`, `change_reasoning`, `personalisation_factors`, `decision_ladder_rank`, `plan_coherence`.

`build_explanation()` in `app/domain/student_experience/recommendation_explanation.py` **re-synthesises** `why_recommended` from reason codes. The Coach prose a student reads is **not** the explanation RecommendationService authored.

### 5.4 ExplanationSnapshot bottleneck

**File:** `app/application/student_experience/dto/explanation_snapshot.py`

Five payload fields only: `summary`, `why_recommended`, `evidence_points`, `expected_benefit`, `confidence_label` (+ `is_complete`).

No slots for next action, review point, drivers, change reasoning, or personalisation. **Anything absent here cannot reach Home regardless of template work.**

### 5.5 View-model compression

**File:** `app/presentation/student/view_models.py`

| Step | Effect |
|---|---|
| `explanation_vm()` | `evidence_points[:3]` — second truncation |
| `_compose_coach_insight()` | Concatenates summary + why + benefit; **`_clip_sentences(text, 3)`** hard cap |
| Home readiness card | Confidence label only; no why / drivers / review |

### 5.6 Unified Journey

**Files:** `contracts.py` (`JourneyContext`), `daily_mission_assembler.py`

`JourneyContext` has no fields for evidence, confidence, review_point, drivers, or change_reasoning. `supporting_insights` is capped and fed from maps that are empty on the Home path → reliably empty. `_mission_summary()` applies `_first_sentence` with ~160-char ellipsis. Session outcome assembler emits hardcoded completion strings — **no MES**.

---

## 6. Template / UI render inventory

| Template | MES fields bound | Gap |
|---|---|---|
| `student/home.html` | `why_it_matters`, `expected_outcome` / `expected_benefit_label`, `mission_summary`, recommendation summary/reason, readiness `confidence_label`, `coach_insight` | **Never calls `explanation_card`**; no evidence, next action, review_point, drivers |
| `student/components/explanation_card.html` | summary, why_recommended, evidence_points[:3], expected_benefit | Exists; used only from `revision.html` |
| `dashboard/index.html` | next_action, observed_facts, estimates, educational_advice/reason, expected_benefit, readiness explanation + evidence_basis | Best daily MES surface today |
| `mission/index.html` | next_action, reason_for_selection, educational_purpose, observed_facts, estimates, coverage evidence_basis | Partial planning MES |
| `analytics/index.html` | label, explanation, evidence_basis | Drivers unbound |
| Session outcome templates | Completion copy | No recommendation/plan/readiness MES |

### Highest-impact template defect

`HomePageViewModel.explanation` is populated and `explanation_vm()` runs, but **`home.html` never imports or renders `explanation_card`**. Evidence exists in memory at render time and is silently discarded. Only `revision.html` calls the macro.

---

## 7. Omission inventory (complete)

### 7.1 Recommendation

| Field | Legacy Dashboard | Canonical Home | Where lost (Home path) |
|---|---|---|---|
| `why_recommended` | As advice/reason | Rendered but **re-synthesised** | `explanation_service.from_opaque` never reads authored field |
| `supporting_evidence` | Via explainability_block | **Never rendered** | Mapper drop + home omits card |
| `confidence_level` | Not on rec card | Readiness panel only (bare) | Dropped at mapper for rec |
| `expected_benefit` | Yes | Yes | — |
| `suggested_next_action` / `next_action` | Yes | **Never** | Absent from `ExplanationSnapshot` |
| `review_point` | **Never** | **Never** | Absent from all downstream DTOs |
| `decision_ladder_rank` | No | No | Mapper |
| `plan_coherence` | No | No | Mapper |
| `personalisation_factors` | No | No | Mapper (also flag-OFF) |

### 7.2 Planning

| Field | Legacy | Canonical | Where lost |
|---|---|---|---|
| `why_this_plan` | Yes | As `why_it_matters`, first-sentence clipped | `_first_sentence` |
| `supporting_evidence` | Yes [:6] | **No** | `JourneyContext` |
| `confidence_level` | Folded into estimates | **No** | `JourneyContext` |
| `expected_benefit` | Dropped by adapter as field | As `expected_outcome` | Adapter / Journey |
| `suggested_next_action` | Yes | **No** | No VM field |
| `review_point` | **Dropped by adapter** | **No** | `_schema_mission_narrative` |
| `plan_drivers` | **Dropped by adapter** | **No** | `_schema_mission_narrative` |
| `change_reasoning` | Folded into estimates | **No** | Journey |

### 7.3 Readiness

| Field | Legacy | Canonical | Where lost |
|---|---|---|---|
| `why_this_estimate` | As `explanation` | **No** | Never reaches HomeSnapshot |
| `supporting_evidence` | Flattened to `evidence_basis` | **No** | Schema narrative join; Home never loads |
| `confidence_level` | Inside blob | Bare label | Basis missing |
| `expected_benefit` | Dropped | Dropped | `_schema_readiness_narrative` |
| `suggested_next_action` | Appended to prose | **No** | — |
| `review_point` | **Dropped** | **Dropped** | Adapter |
| `readiness_drivers` | **Dropped on schema path** | **Dropped** | `_schema_readiness_narrative` never calls `_driver_evidence` |
| `change_reasoning` | Appended to evidence_basis | **Dropped** | — |

### 7.4 Fields reaching no student surface anywhere

`review_point` · `readiness_drivers` (schema path) · `plan_drivers` · `personalisation_factors` · `decision_ladder_rank` · `plan_coherence` (as student control) · `explanation_schema_version` / `explanation_level` (meta — OK to omit from student chrome)

**Most material for K8 / G1.5:** `review_point`, structured evidence, `suggested_next_action` on Home, and `readiness_drivers` / `plan_drivers`.

---

## 8. Progressive disclosure patterns found

| Pattern | Location | Used on default daily path? |
|---|---|---|
| `learn_more` (`contextual_help.html`) | Dashboard, Mission | Legacy only |
| `explanation_card` (`student/components/…`) | Revision only | **No** on Home |
| `explainability_block` (EIP-003 Observed / Estimates / Advice / Next) | Nested in `learn_more` | Legacy only |

Canonical `home.html` has **zero** `<details>` disclosures. Compression is forced into always-visible flat copy.

---

## 9. Compression cascade (canonical path)

Five stacked reductions (none individually catastrophic; jointly destructive):

1. Service evidence cap `[:4]` — `recommendation_quality.py`
2. Mapper ~20 → 6 keys — `recommendation_mapper.py`
3. DTO admits 5 fields — `ExplanationSnapshot`
4. VM evidence cap `[:3]` — `explanation_vm`
5. Coach insight `_clip_sentences(..., 3)` — `view_models.py`

Plus Journey `_first_sentence` (~160 chars) on mission summary.

---

## 10. Consistency with P-001.2

| Principle | Assessment |
|---|---|
| P1 Every guidance explains itself | **Fail on Home** — silent drop of evidence / next / review |
| P2 Evidence before opinion | **Fail on Home** — no identifiable evidence list |
| P3 Confidence speakable | **Partial** — label without basis |
| P4 One clear next action | **Fail on Home** — next action not rendered |
| P7 Consistent across Runtime A | **Fail** — Dashboard richer than Home for same decision class |
| P8 Length fits level | Misapplied — clips instead of progressive disclosure |
| Service checklist Pass | **True** — overstates student-visible explainability |

---

## 11. Conclusions for remediation design

1. **Do not change educational services** — they already produce MES.  
2. **Widen DTOs first** (`ExplanationSnapshot`, `JourneyContext`, readiness Home cards) — template fixes alone cannot restore dropped fields.  
3. **Pass through authored Runtime A fields** — stop re-narrating from reason codes when schema-complete payloads exist.  
4. **Wire `explanation_card` + Level-2 disclosure on Home** — match or exceed legacy Dashboard fidelity.  
5. **Restore drivers on schema readiness/planning paths** — REM-05 dependency.  
6. **Treat presentation completeness as a hard quality gate** equal to service schema completeness (EP-005.2 lesson).

Detailed contract and implementation design: [`MES_DELIVERY_SPECIFICATION.md`](MES_DELIVERY_SPECIFICATION.md).  
Prioritised K8 plan: [`K8_REMEDIATION_PLAN.md`](K8_REMEDIATION_PLAN.md).

---

## References

- `../ep005_2_educational_experience_validation/EDUCATIONAL_EXPERIENCE_REVIEW.md`  
- `../ep005_2_educational_experience_validation/PRIORITISED_REMEDIATION_PLAN.md` (REM-01, REM-05)  
- `../p001_2_explainability_standard/EXPLAINABILITY_STANDARD.md` §6–§9  
- `../ep005_1_ksi_validation_evidence/VERSION_1_G1_STATUS.md`  

---

**End of MES_TRACEABILITY_REPORT**
