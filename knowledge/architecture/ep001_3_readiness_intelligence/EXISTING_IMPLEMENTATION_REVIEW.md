# EP-001.3 — Existing Implementation Review

**Milestone:** EP-001.3 — Readiness Intelligence  
**Phase:** 2 — Existing Implementation Review  
**Date:** 2026-07-26

---

## 1. Review dimensions

| Dimension | Current behaviour | Category |
|---|---|---|
| Readiness score (composite %) | `get_overall_readiness`: Coverage 50% + Avg mastery 30% + Review discipline 20% | **Already implemented** |
| Weighted syllabus readiness | `calculate_readiness` from `StudentCurriculumSummary` (progress only) | **Already implemented** |
| Confidence level | No explicit confidence band on Runtime A readiness dicts; warrant exists only on Epic structural stack / V2 estimator | **Missing** (Runtime A) |
| Strongest areas | `get_strongest_topics` via ORM TopicProgress | **Already implemented** |
| Weakest areas | `get_weakest_topics` via ORM TopicProgress | **Already implemented** |
| Readiness drivers | Implicit in score components; not surfaced as named drivers with CLS provenance | **Partially implemented** |
| Recommended next actions | `RecommendationService` adjacent; readiness itself does not emit action list from Planner | **Partially implemented** (adjacent) / **Missing** on readiness surface |
| Mission influence | Review discipline uses Mission completion rates | **Already implemented** |
| Mastery influence | 30% of composite + weak/strong topics | **Already implemented** |
| Study behaviour influence | Burnout monitor / facets exist; not in readiness composite | **Missing** (Runtime A readiness) |
| Consistency / streaks influence | Streaks exposed separately; not in composite drivers package | **Partially implemented** |
| Evidence sources | TopicProgress, Mission, StudyAttempt, Curriculum leaves; Twin CLS available but unused by readiness enrichment | **Partially implemented** |
| Dashboard consumers | dashboard / analytics / settings call ReadinessService directly | **Already implemented** |
| Consume Canonical Learner State | Foundation embeds readiness_overall; readiness does not consume CLS for enrichment | **Missing** |
| Consume Planner outputs | Planner daily plan unused by readiness | **Missing** |

---

## 2. Current readiness calculations (detail)

### 2.1 Overall composite (`get_overall_readiness`)

```
score = coverage_pct * 0.50
      + avg_mastery_score * 0.30
      + review_discipline * 0.20
```

- Coverage: started leaf topics / total leaf topics (`revision_count > 0`)
- Mastery: mean `TopicProgress.mastery_score` over started topics
- Review discipline: Mission `Completed` / total missions

### 2.2 Weighted progress readiness (`calculate_readiness`)

- Pure syllabus weighting completion — explicitly **not** mastery/confidence
- Used on dashboard curriculum summary card

### 2.3 Topic ranking

- Weakest / strongest require attempt-derived `average_accuracy` (IA-004)
- Ordered by `mastery_score`

---

## 3. Confidence calculations

| Stack | Status |
|---|---|
| Runtime A `ReadinessService` | No confidence field on returned dicts |
| Epic `ReadinessAggregation` | `WarrantPosture` / overall posture (structural; no %) |
| V2 `ReadinessEstimator` | `ConfidenceBand` from Twin confidence state |
| Education OS readiness composer | Evidence-quality cards from OS artefacts |

**Verdict:** Runtime A confidence for readiness intelligence is **Missing**.

---

## 4. Mission / mastery / behaviour influence

| Influence | Path today |
|---|---|
| Mission | Review completion rate + backlog due counts |
| Mastery | Composite weight + topic lists |
| Study behaviour | Not in readiness math (facets live on Foundation / Behaviour twin) |
| Consistency | Not packaged as a readiness driver |
| Streaks | Exposed via separate getters; also Twin pass-through |

---

## 5. Evidence sources

| Source | Used by Runtime A readiness? | On Canonical Learner State? |
|---|---|---|
| TopicProgress | Yes | Yes (`topic_progress` / `topic_mastery`) |
| Mission | Yes (completion / review) | Yes (`mission_completion`) |
| StudyAttempt | Streaks / topic detail | Yes (`learning_evidence` / practice) |
| Curriculum leaves | Yes (denominator) | Via study goals / curriculum collector |
| Behaviour facets | No | Yes (`study_behaviour` / `study_consistency`) |
| Planner daily plan | No | Via EP-001.2 when Twin ON |
| Mock exams | No | Unavailable (honest) |

---

## 6. Dashboard / HTTP consumers

| Consumer | Methods used |
|---|---|
| `app/dashboard/routes.py` | overall, backlog, weakest, strongest, `calculate_readiness` |
| `app/analytics/routes.py` | overall, coverage, backlog, review, streaks, weak/strong |
| `app/settings/routes.py` | overall, coverage |
| `app/mission/routes.py` | `calculate_readiness` |
| `AnalyticsService` | overall, streaks, weak/strong |
| `RecommendationService` | backlog, weak, coverage, overall |
| `ExamTimeline` | coverage, overall |
| `ReadinessCollector` | overall, coverage, backlog, streaks |

---

## 7. Categorisation summary

### Already implemented

- Deterministic overall readiness score
- Coverage, review completion, backlog, streaks
- Weakest / strongest topics (ORM)
- Weighted syllabus progress readiness
- Dashboard / analytics wiring
- Twin pass-through of readiness aggregates via `ReadinessCollector`

### Partially implemented

- Named readiness drivers (components exist, not packaged with CLS provenance)
- Recommended next actions (RecommendationService exists; readiness surface does not emit Planner-grounded actions)
- Streaks / mission as first-class intelligence drivers (available but not composed into one assessment object)
- Strongest / weakest when Twin ON still re-query ORM instead of CLS mastery

### Missing

1. Explicit **confidence level** on Runtime A readiness intelligence
2. **Consume Canonical Learner State** for enrichment (behaviour, consistency, evidence density, CLS mastery areas)
3. **Consume Planner outputs** for recommended next actions
4. Single **`build_readiness_intelligence`** assessment packaging score + confidence + areas + drivers + actions
5. Fail-open Twin-gated API without changing legacy getters (avoid collector recursion)

---

## 8. What must remain untouched in this review’s conclusion

- Do not delete or rewrite Epic / V2 / OS readiness stacks
- Do not change `ReadinessCollector` to invent formulae
- Do not make `get_overall_readiness` call Foundation (circular with collector)
- Do not invent mock performance
