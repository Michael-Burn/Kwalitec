# EP-004.1 — Discovery Report

**Programme:** EP-004.1 — Personal Learning Profile  
**Date:** 2026-07-26  
**Phase:** Discovery  

---

## 1. Sources reviewed

| Authority | Path | Relevance |
|---|---|---|
| Product Constitution | `knowledge/product/vision/PRODUCT_VISION_2030.md` | Evidence-based guidance; Final Test; no opaque optimisation |
| Educational Constitution | `knowledge/educational/` | Evidence immutable; inference ≠ inventing evidence; accept ≠ mastery |
| P-001.1 KSI Framework | `knowledge/product/p001_1_ksi_baseline/` | K4 Personalisation primary gap; K6 analytics substrate from EP-003.4 |
| EP-003.1 | `knowledge/product/ep003_1_recommendation_engine_enhancement/` | Quality contract; deferred long-term preference profile |
| EP-003.2 | `knowledge/product/ep003_2_readiness_intelligence_enhancement/` | Consistency signals without durable habit profile |
| EP-003.3 | `knowledge/product/ep003_3_adaptive_planning_enhancement/` | Recovery / completion without long-term planning behaviour summary |
| EP-003.4 | `knowledge/product/ep003_4_learning_feedback_loop/` | Observed event stream — does not close personalisation loop |
| EP-002.9 baseline | `knowledge/architecture/ep002_9_programme_exit_certification/` | Rec / Readiness / Planning / presentation ownership |
| Student Digital Twin | `STUDENT_DIGITAL_TWIN.md`, `STUDENT_DIGITAL_TWIN_ARCHITECTURE.md` | Twin facets ≠ Personal Learning Profile; Twin must not gain write authority |
| Learning Feedback architecture | `LEARNING_FEEDBACK_ARCHITECTURE.md` | Lawful evidence inputs for profile aggregation |

---

## 2. Current behaviour (pre-EP-004.1)

1. Learning Feedback records plan / recommendation / study interaction events (process-local).
2. Twin Foundation exposes learner-state facets (rhythm, consistency, …) as a separate read model.
3. Experience `ProfileProjection` holds settings/preferences for presentation — not educational evidence summary.
4. Recommendation / Readiness / Planning quality contracts improve explainability but do not maintain a long-term observed behavioural profile.
5. No unified, provenance-backed Personal Learning Profile contract for optional Runtime A consumption.

---

## 3. Discovery conclusions

| Finding | Implication |
|---|---|
| EP-003.4 supplies events but not a stable profile | Add aggregator + immutable profile snapshot |
| Twin already has behavioural facets | Keep profile separate — do not merge authorities or invent a fourth brain |
| Accept ≠ mastery is settled law | Preference attributes must remain `preference_summary` |
| Some candidate attributes lack evidence today | Explicitly mark unsupported (duration without declaration; study windows) |
| Services need optional inputs without coupling | Expose `PersonalLearningProfilePort` + fail-open consumer helpers |

---

## 4. Recommended implementation shape

1. Add `app/infrastructure/adapters/personal_learning_profile/` with contracts, aggregator, store, consumer Port.
2. Derive attributes only from Learning Feedback (+ optional declared session minutes).
3. Feature flag `KWALITEC_PERSONAL_LEARNING_PROFILE` default OFF.
4. Wire fail-open consume helpers on Recommendation / Readiness / Planning without changing decisions.
5. Document observed / derived / unsupported explicitly; reject forbidden inference keys.

---

## 5. Out of scope (explicit)

- Automatic optimisation / ranking / readiness / plan changes from profile values.
- Twin Ready / HTTP cutover declarations.
- Durable cross-process profile persistence.
- Treating preference or completion rates as mastery.
- Creating `PersonalLearningProfileService` as educational decision authority.
- Inferring preferred study windows from emit wall-clock timestamps.
