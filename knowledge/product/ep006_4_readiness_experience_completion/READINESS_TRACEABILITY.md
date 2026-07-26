# EP-006.4 — Readiness Traceability

**Programme:** EP-006.4 — Readiness Experience Completion  
**Date:** 2026-07-26  
**Purpose:** Trace authored readiness MES fields from Runtime A to student-visible Home bindings after EP-006.4.

---

## 1. Problem restatement (pre-change)

| Layer | Status before EP-006.4 |
|---|---|
| ReadinessService + quality contract | Authored complete MES (EP-003.2) |
| Analytics | Drivers + review_point + next bound (EP-006.2 MES-05) |
| Canonical Home | Score / trend / borrowed recommendation cues; **`readiness_drivers=()` hardcoded** |
| Perception | EP-006.3 PERC-01 — Home drivers student-visible = **Unsupported** |

---

## 2. End-to-end field trace (Home path)

| MES field | Author | Transport | Home DTO | Home VM | Template binding |
|---|---|---|---|---|---|
| `why_this_estimate` | ReadinessService / quality | Dashboard surface → adapter narrative | `ReadinessExplanationSnapshot.why_this_estimate` | `ReadinessCardViewModel.why_this_estimate` | L1 body |
| `confidence_level` | ReadinessService / quality | surface → narrative | `confidence_label` | `confidence_label` | L1 cue / L2 `data-mes-field="confidence_level"` |
| `confidence_basis` | Surface optional; else lexical label | adapter pass-through | `confidence_basis` | `confidence_basis` | L2 with confidence |
| `suggested_next_action` | ReadinessService / quality | surface → narrative | `suggested_next_action` | `suggested_next_action` | L1 `data-mes-field="readiness_next_action"` |
| `review_point` | ReadinessService / quality | surface → narrative | `review_point` | `review_point` | L2 `data-mes-field="review_point"` |
| `readiness_drivers` | ReadinessService / quality | `_driver_evidence` ≤4 | `readiness_drivers` | `readiness_drivers` | L2 `data-mes-field="readiness_drivers"` |
| `supporting_evidence` | ReadinessService / quality | narrative tuple | `supporting_evidence` | `supporting_evidence` | L2 `data-mes-field="supporting_evidence"` |
| `expected_benefit` | ReadinessService / quality | narrative | `expected_benefit` | `expected_benefit` | Available on VM (optional render) |
| Score / band | Twin readiness summary | Educational State | `exam_readiness` / label | percent + label | L1 metric |

---

## 3. Ownership matrix

| Concern | Owner | EP-006.4 change? |
|---|---|---|
| Readiness score / weights | ReadinessService | **No** |
| Driver authorship | ReadinessService / quality contract | **No** |
| Narrative selection (schema / twin / legacy) | `RuntimeAPresentationAdapter` | Pass-through only (`confidence_basis`) |
| Home attachment | `HomeService` + `readiness_explanation` | **Yes** — fail-open load |
| Layout / disclosure | Templates + `home_vm` | **Yes** |

---

## 4. Omission inventory — closed by this programme

| ID | Omission | Status after EP-006.4 |
|---|---|---|
| PERC-01 | Home `readiness_drivers` empty | **Closed** on schema-complete path |
| MES-05 Home residual | Drivers + review on Home | **Closed** |
| REM-05 (presentation slice) | Level-2 unpackability on Home | **Closed** for delivery; Tier B re-perception pending |

---

## 5. Residual omissions (out of scope)

| ID | Residual | Owner |
|---|---|---|
| PERC-02 | Cold-start generic speech | Copy / incomplete-schema UX |
| PERC-04 | Dual-home / duration | EP-005.2 REM-02 / REM-03 |
| — | Tier B readiness-focused re-review | Successor perception pack |
| — | Validated K3 lift claim | Requires Tier B + re-score |

---

## 6. Test evidence

| Intent | Test |
|---|---|
| Driver delivery | `test_readiness_driver_delivery_from_schema_surface` |
| Completeness | `test_explanation_completeness_requires_drivers_why_confidence_next` |
| Home VM bind | `test_home_vm_binds_authored_readiness_mes` |
| Home render | `test_home_template_renders_readiness_drivers_and_review` |
| Fallback | `test_fallback_when_readiness_explanation_absent`, `test_fallback_when_load_fails_open` |
| Loader pass-through | `test_load_home_readiness_explanation_pass_through` |

Path: `tests/presentation/student/test_readiness_experience_delivery.py`

---

## References

- [`READINESS_EXPERIENCE_IMPLEMENTATION.md`](READINESS_EXPERIENCE_IMPLEMENTATION.md)  
- `../ep006_1_mes_end_to_end_delivery/MES_TRACEABILITY_REPORT.md`  
- `../ep006_3_mes_perception_validation/MES_PERCEPTION_REPORT.md`  

---

**End of READINESS_TRACEABILITY**
