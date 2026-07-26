# EP-003.4 — Discovery Report

**Programme:** EP-003.4 — Learning Feedback Loop  
**Date:** 2026-07-26  
**Phase:** Discovery  

---

## 1. Sources reviewed

| Authority | Path | Relevance |
|---|---|---|
| Product Constitution | `knowledge/product/vision/PRODUCT_VISION_2030.md` | Evidence-based guidance; Final Test; no opaque optimisation |
| Educational Constitution | `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` / `EDUCATIONAL_CONSTITUTION.md` | Evidence immutable; inference ≠ inventing evidence; accept ≠ mastery |
| P-001.1 KSI Framework | `knowledge/product/p001_1_ksi_baseline/` | K6 analytics weak; need behavioural evidence for future usefulness claims |
| EP-003.1 | `knowledge/product/ep003_1_recommendation_engine_enhancement/` | Deferred acceptance/completion instrumentation |
| EP-003.2 | `knowledge/product/ep003_2_readiness_intelligence_enhancement/` | No readiness history / consistency feedback stream |
| EP-003.3 | `knowledge/product/ep003_3_adaptive_planning_enhancement/` | Recovery/missed signals unused for outcome attribution |
| EP-002.9 baseline | `knowledge/architecture/ep002_9_programme_exit_certification/` | Ownership: Rec / Readiness / Planning / presentation |
| Student Digital Twin | `knowledge/architecture/STUDENT_DIGITAL_TWIN_ARCHITECTURE.md`, `DIGITAL_TWIN_LIFECYCLE.md` | Optional RecommendationResponse; no Twin write-back |
| Sibling observation stacks | Experience Feedback, Advisory Outcome, Longitudinal Evidence | Overlap without unified Runtime A loop |

---

## 2. Current behaviour (pre-EP-003.4)

1. Recommendation Decision Journal can persist accept/complete but is not wired into a coherent learning-feedback stream.
2. Advisory Outcome Measurement records operational advisory rollout actions (no personal educational loop).
3. Experience Feedback displays factual Evidence summaries on Home (display-only).
4. Planning recovery uses `mission_missed_count` for plan assembly but does not emit durable feedback events.
5. Readiness streak helpers exist but do not emit observational feedback.
6. Twin lifecycle documents `RecommendationResponse` as optional Behaviour preference trigger — not implemented as a product feedback loop.

---

## 3. Discovery conclusions

| Finding | Implication |
|---|---|
| Multiple observation stacks, no EP-003 loop | Add Runtime A learning-feedback recorder, do not merge stacks |
| EP-003.1–3 deferred instrumentation | Emit from existing service ownership boundaries |
| Accept ≠ mastery is settled law | Preference-journal claim boundary required |
| Twin must not become write authority | Feedback is observational input for future analytics only |
| Presentation must stay speech-only | Forbidden as feedback source authority |

---

## 4. Recommended implementation shape

1. Add `app/infrastructure/adapters/learning_feedback/` with immutable events + process-local recorder.
2. Fail-open emitters callable only from Recommendation / Readiness / Planning.
3. Feature flag `KWALITEC_LEARNING_FEEDBACK` default OFF.
4. Document observed vs inferred explicitly; reject forbidden inference payload keys.
5. Do not change ranking, readiness formulae, planning policy, or presentation behaviour.

---

## 5. Out of scope (explicit)

- Automatic optimisation / ranking changes from feedback.
- Twin Ready / production HTTP cutover declarations.
- Durable cross-process persistence (future Longitudinal Evidence publish).
- Treating clicks, acceptance, or completion as mastery evidence.
- Creating a fourth educational brain (`LearningFeedbackService` as decision authority).
