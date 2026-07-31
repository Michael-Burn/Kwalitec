# KWP-012 — Readiness Forecast & Study Trajectory

**Programme:** KWP-012 · Readiness Forecast & Study Trajectory  
**Phase:** Educational Intelligence Phase 6  
**Date:** 2026-07-30  
**Nature:** Projection layer for educational forecasting — **not a reasoning authority rewrite**  
**Authority:** KWP-011 · KWP-010 · KWP-009 · KWP-008 · KWP-007 · `PRODUCT_BLUEPRINT.md`

---

## 1. Executive Summary

KWP-012 introduces deterministic **Readiness Forecast & Study Trajectory**: a projection layer that estimates where a learner is heading from existing educational evidence — coverage, consistency, recovery history, difficulty trends, Learning Memory patterns, intervention effectiveness, cadence, confidence alignment, reflection, and target exam date.

Students see natural guidance such as *“If your recent study pattern continues, you are likely to reach Ready for Revision before your scheduled sitting.”* Founders see forecast accuracy, trajectory distribution, recovery projections, readiness progression, and forecast confidence on Platform Intelligence.

**Verdict:** The platform can now answer *“If the learner continues studying in this way, what is the likely readiness by the target exam date?”* without redesigning Learning Runtime, Evidence, Progress, Strategy, Diagnostics, Difficulty, Intervention Effectiveness, Educational Memory, Student Twin, or Mission Runtime.

---

## 2. Implementation Audit

| # | Capability | Verdict | Classification | Notes |
|---|---|---|---|---|
| 1 | Evidence Packages / sitting observations | Available | **EXISTING** · consumed | Sole evidence spine |
| 2 | Intelligence snapshots (Strategy / Diagnostics / Difficulty / Effectiveness) | Available | **EXISTING** · consumed | Via Educational Memory snapshots |
| 3 | Learning Memory patterns / milestones | Available | **EXISTING** · consumed | Growth / recovery patterns as factors |
| 4 | StrategyEvidenceInput field lift | Available | **EXISTING** · reused | Practice / finish / cadence / retention |
| 5 | KWP-006 readiness stage vocabulary | Available | **EXISTING** · reused | Building → Ready for Assessment |
| 6 | Exam countdown / Home readiness | Available | **EXISTING** · enriched | Days-to-exam + optional ratio |
| 7 | Twin PredictionState storage | Structural only | **EXISTING** · not duplicated | No forecasting algorithms there |
| 8 | Digital Twin learning trajectory (src/) | Parallel Education OS | **EXISTING** · not reused | Different stack; commercial path uses packages |
| 9 | Momentum postures (Strategy) | Available | **EXISTING** · complementary | Sitting momentum ≠ exam trajectory |
| 10 | Forecast label catalogue | Absent | **NEW** | On Track / Building Momentum / … |
| 11 | Trajectory projection + assumptions | Absent | **NEW** | Trend, projected stage, factors |
| 12 | Student natural forecast guidance | Absent | **NEW** | No pass % / no certainty theatre |
| 13 | My Learning Journey forecast section | Absent | **NEW** | Projection on journey page |
| 14 | Home Study Trajectory insight | Absent | **NEW** | Insight card when evidence warrants |
| 15 | Founder forecast analytics | Absent | **NEW** | Accuracy, distribution, confidence |
| 16 | Learning Runtime / Evidence / Progress / Strategy / Diagnostics / Difficulty / Effectiveness / Memory / Twin / Mission | Must not redesign | **EXISTING** unchanged | Projection only |

### EXISTING (reused)

- Session Evidence Packages + `list_evidence_packages`  
- Educational Memory intelligence snapshots + longitudinal patterns  
- `StrategyEvidenceInput.from_opaque`  
- KWP-006 readiness stage thresholds / titles  
- Home countdown + readiness presentation enrichments  
- Founder Platform Intelligence section pattern  
- Product Language Guide  

### NEW

- `app/application/readiness_forecast/` — DTOs, signals, projection, rules, guidance, engine  
- `app/services/readiness_forecast_metrics.py`  
- `tests/test_kwp012_readiness_forecast.py`  
- `KWP012_IMPLEMENTATION_REPORT.md`  

### MODIFIED

- My Learning Journey route / VM / template — Readiness Forecast section  
- Home Insights — optional Study Trajectory card  
- Founder alpha observability — Readiness Forecast metrics  
- Product language — `Readiness Forecast`, `Study Trajectory`  

---

## 3. Forecast Architecture

```
Evidence Packages (+ intelligence snapshots)
+ optional exam countdown / readiness ratio
        │
        ▼
 extract_forecast_signals(...)
        │
        ▼
 project_trajectory(...)  → trend, projected stage, assumptions, factors, confidence
        │
        ▼
 classify_forecast(...)   → ForecastLabel + rule_id
        │
        ▼
 guidance / explanation   → student-safe natural language
        │
        ▼
 ReadinessForecast
        ├─ My Learning Journey  → Readiness Forecast section
        ├─ Home Insights        → Study Trajectory card
        └─ Founder ReadinessForecastMetrics
```

**Hard boundary:** Forecasting is a **projection layer**. It never writes Evidence, Progress, Educational Intelligence engines, Educational Memory, Twin, or Mission state.

| Authority | Relationship |
|---|---|
| Learning Strategy | Consumed via snapshots / opaque facts — not redesigned |
| Learning Diagnostics | Consumed via snapshots — not redesigned |
| Learning Difficulty | Consumed via snapshots — not redesigned |
| Intervention Effectiveness | Consumed via snapshots — not redesigned |
| Educational Memory | Patterns consumed; Memory not mutated |
| Progress Engine | Advance flags consumed only |
| EducationalEvidenceAuthority | Unchanged |
| StudentTwinEngine | Optional readiness / countdown enrichments only |
| LearningSessionRuntime / Mission Runtime | Unchanged |

---

## 4. Forecast Vocabulary

### Labels (student-safe titles)

| Label | Meaning |
|---|---|
| On Track | Current pattern likely reaches Ready for Revision by sitting |
| Building Momentum | Improving trajectory; target not yet secured |
| Needs Greater Consistency | Cadence / consistency is the binding constraint |
| Recovery Required | Retention / recovery pressure must be addressed first |
| Ahead of Schedule | Comfortably clears Ready for Revision with time to spare |
| Below Target Pace | At current pace, projected stage falls short by exam |
| Not Enough Evidence Yet | Fewer than two sittings — no lawful forecast |

### Trajectory explanation fields

- Current trend (Improving / Stable / Declining / Recovering / Not yet clear)  
- Projected readiness stage (KWP-006 vocabulary)  
- Key assumptions (pattern continues; exam horizon; thin-evidence honesty)  
- Most influential factors (consistency, strength, recovery, time to exam, …)  
- Confidence (Limited / Emerging / Established) — never fabricated certainty  

### Target

Sitting preparation target remains **Ready for Revision** (ratio 0.80) — same stage system as Exam Week Briefing. No second readiness band inventing pass probability.

---

## 5. Student Experience

### My Learning Journey (`/student/learning-journey`)

When sittings exist, students see a **Readiness Forecast** section with:

- Forecast title + natural guidance  
- Current trend / projected readiness / confidence  
- Influential factors and key assumptions  

Example guidance:

> If your recent study pattern continues, you are likely to reach Ready for Revision before your scheduled sitting.

or

> Current progress suggests additional study consistency will be needed to stay on a healthy readiness trajectory.

### Home Insights

When store packages support a forecast, Home Learning Insights include a **Study Trajectory** card (kind `trajectory`) — calm, one line, no analytics wall.

---

## 6. Founder Analytics

Platform Intelligence (`/founder/alpha-observability`) — **Readiness Forecast**:

- Learners forecasted / sittings scanned  
- On-track rate / below-pace rate  
- Recovery projections  
- Average projected readiness  
- Forecast accuracy (retrospective first-half vs later proxy)  
- Established confidence rate  
- Trajectory / trend / confidence distributions  
- Readiness progression labels (current → projected)  

Computed by scanning Evidence Packages — no mutation of EI authorities.

---

## 7. Architecture Compliance

| Constraint | Status |
|---|---|
| Learning Runtime redesign | **No** |
| Educational Evidence redesign | **No** |
| Progress Engine redesign | **No** |
| Learning Strategy / Diagnostics / Difficulty / Effectiveness redesign | **No** |
| Educational Memory redesign | **No** — consumed only |
| Student Twin / Mission Runtime redesign | **No** |
| Forecasting is projection only | **Met** |
| No fabricated certainty / pass probability product claims | **Met** |
| Reuses KWP-006 stage vocabulary | **Met** |
| No duplicate forecasting engine in Twin PredictionState | **Met** |
| Curriculum V1/V2 | **N/A** — no curriculum engine changes |
| Migration Impact | **None** — no schema migrations |

---

## 8. Files Modified

### Created

- `app/application/readiness_forecast/__init__.py`  
- `app/application/readiness_forecast/dto.py`  
- `app/application/readiness_forecast/signals.py`  
- `app/application/readiness_forecast/projection.py`  
- `app/application/readiness_forecast/rules.py`  
- `app/application/readiness_forecast/guidance.py`  
- `app/application/readiness_forecast/engine.py`  
- `app/services/readiness_forecast_metrics.py`  
- `tests/test_kwp012_readiness_forecast.py`  
- `KWP012_IMPLEMENTATION_REPORT.md`  

### Modified

- `app/presentation/student/routes.py`  
- `app/presentation/student/view_models.py`  
- `app/presentation/student/exam_week_briefing.py`  
- `app/presentation/student/services/student_home_service.py`  
- `app/templates/student/learning_journey.html`  
- `app/presentation/product_language.py`  
- `app/founder/dashboard/routes.py`  
- `app/founder/dashboard/templates/founder_dashboard/alpha_observability.html`  

### Migration Impact

**None.**

---

## 9. Tests Executed

```bash
python3 -m pytest tests/test_kwp012_readiness_forecast.py \
  tests/test_kwp011_educational_memory.py \
  tests/test_kwp010_intervention_effectiveness.py \
  tests/test_kwp005_sitting_reports.py -q
```

**Outcome:** 53 passed (15 KWP-012 + regressions).

Coverage includes thin-history honesty, on-track / recovery / consistency / near-exam paths, deterministic replay, trajectory explanation fields, Learning Journey VM + template markers, Home trajectory insight, founder metrics, approved product terms, and forbidden-vocabulary scrub.

Ruff clean on new / touched modules.

---

## 10. Known Limitations

1. Forecast without an exam date uses a short four-week horizon — directional only.  
2. Current readiness may be a deterministic evidence proxy when Home readiness is unavailable.  
3. Founder “forecast accuracy” is a retrospective directional check (first-half projection vs later proxy), not a calibrated ML score.  
4. Learners with fewer than two Evidence Packages lawfully receive “Not Enough Evidence Yet.”  
5. Home trajectory insight depends on session-store package visibility (`ENABLE_DURABLE_STORE` for multi-process durability).  
6. Parallel Education OS Twin trajectory (`src/domain/.../learning_trajectory.py`) remains a separate stack and is intentionally not duplicated here.

---

## 11. Recommendation for KWP-013

**Working title:** KWP-013 — Educational Intelligence Continuity Authority Matrix & Dogfood

**Mandate:**

1. Publish an explicit **authority matrix**: when Strategy vs Diagnostics vs Difficulty vs Effectiveness vs Forecast vs Runtime A Decision each win (no silent re-ranking).  
2. Dogfood My Learning Journey forecast + frozen Sitting Report history across reinforce / consolidate / recover / advance paths.  
3. Optional exam-date sensitivity: show how +1 sitting/week changes projected stage (still deterministic, still non-certain).  
4. Founder alert when below-pace rate or recovery projections exceed a deterministic threshold.  
5. Align History archive vocabulary with Journey forecast language (single “where am I heading” student phrase).

**Non-goals:** Pass-probability product claims, LLM narrative generation, Progress / Twin / Mission redesign, second forecast database, psychological profiling.

---

## Success Criteria Check

> Students should understand not only where they are, but where their current learning journey is likely to take them, using deterministic educational evidence.

**Status:** Met for the commercial path. Readiness Forecast projects trajectory from Evidence Packages and existing EI / Memory signals; students receive natural guidance on My Learning Journey and Home Insights; founders see forecast analytics. No authority redesign; certainty is never fabricated.

---

**Document status:** Complete — KWP-012 implementation deliverable  
**Next programme:** KWP-013 Educational Intelligence Continuity Authority Matrix & Dogfood (recommended)  
**Architecture stance:** Projection layer only; SR-001A / EI Phase 1–5 authorities unchanged
