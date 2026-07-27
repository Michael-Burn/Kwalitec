# PRD-001A — Readiness Audit

Surfaces evaluated: Estimated Knowledge, Readiness, Confidence, Journey — and whether they **influence recommendations** or **merely report**.

---

## Estimated Knowledge

| Aspect | Finding | Evidence |
|---|---|---|
| Storage | `TopicProgress.mastery_score` | ORM learning progress |
| Evidence gate | `has_estimated_knowledge` true only when `average_accuracy is not None` | Model helper — wizard declarations do not mint EK |
| Student visibility (EOS) | **Weak** — not on Home/Journey/History templates | Grep empty under `templates/student/` |
| Student visibility (other) | Study Plan roadmap shows `%` | `study_plan/view.html` |
| Influences Learning Mode mission topic? | **No** | `_select_topic_for_today` |
| Influences recommendations? | **Yes** — weak-topic bucket uses mastery thresholds (&lt;30 Critical, &lt;60 High) | `RecommendationService._weak_topic_recommendations` |
| Influences Twin daily plan (flagged)? | **Yes** — weak/recovery slots | `DailyStudyPlanAssembler` |
| Production Twin plan cutover? | **Off** | `render.yaml` / `v2_flags` defaults |

**Verdict:** EK is a **real backend estimate** that **partially drives recommendation rules** and **does not drive default missions**. On the EOS Home decision surface it mostly **fails to appear**, so students cannot see it influencing anything.

---

## Readiness

| Aspect | Finding | Evidence |
|---|---|---|
| Computation | Composite ~50% coverage + 30% avg mastery + 20% review discipline | `ReadinessService.get_overall_readiness` |
| Student visibility | Home panel + disclosure | `home.html` |
| Influences mission topic? | **No** | Learning Mode selector |
| Influences planning packaging? | **Labels / workload notes only** | `planning_quality.py` header comments |
| Influences recommendations? | Indirect — readiness surfaces, weakest topics, packaging | Recommendation + readiness services |
| Decision value today | Helps student **judge** exam posture; does **not** choose today’s syllabus leaf | Experience audit |

**Verdict:** Readiness is a **genuine reporting + coaching signal** with partial recommendation coupling. It is **not** the mission authority.

---

## Confidence

| Aspect | Finding |
|---|---|
| Presentation | Confidence labels on readiness disclosure and explanation trust/refusal paths |
| Influence | Softens trust UX; does not select topics |
| Honesty | Improves when thin evidence → low confidence / honest refusal |

---

## Journey

| Aspect | Finding |
|---|---|
| Role | Structural syllabus progress narrative |
| Influence on mission | Reflects same progress backbone (`completed` topics) but is not a separate selector |
| Home panel | Story text — low decision density vs `/student/journey` page |

---

## Influence summary

```
                    Mission topic (Learning Mode)    Recommendations / labels
Estimated Knowledge          No                              Yes (weak topics)
Readiness                    No                              Partial (packaging, related recs)
Confidence                   No                              Trust presentation
Journey progress             Same completed flags            Progression framing
```

---

## Student impact

Founder observation “Estimated Knowledge is not obviously influencing recommendations” is:

- **Correct** for the primary Daily Mission.  
- **Incomplete** for the RecommendationService weak-topic path.  
- **Correct as experience** because EOS does not show EK beside the primary CTA.

Classification: **Category A** (EK/readiness influence under-exposed) + **intentional V1 selection law** (not a bug that Learning Mode ignores EK).
