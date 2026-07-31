# KWP-013 — Adaptive Study Workspace

**Programme:** KWP-013 · Adaptive Study Workspace  
**Phase:** Student Experience Phase 1  
**Date:** 2026-07-30  
**Nature:** Presentation composition layer — **not an Educational Intelligence rewrite**  
**Authority:** KWP-012 · KWP-011 · KWP-010 · KWP-009 · KWP-008 · KWP-007 · `PRODUCT_BLUEPRINT.md`

---

## 1. Executive Summary

KWP-013 transforms Student Home into a unified **Adaptive Study Workspace**: one coherent study environment that answers *Where am I? What should I do? Why? How long? Am I improving? Where am I heading?* without requiring navigation between independent feature cards.

The workspace composes Mission, Readiness, Forecast (KWP-012), Learning Journey (KWP-011), Recent Progress, Current Focus (Strategy / Diagnostics / Difficulty), and Today's Session into a single adaptive layout. Educational Intelligence engines remain unchanged — the workspace is presentation-only.

**Verdict:** Students experience Kwalitec as one study companion that understands their path, without needing to understand Strategy, Diagnostics, Difficulty, Memory, or Forecast internals.

---

## 2. Implementation Audit

| # | Capability | Verdict | Classification | Notes |
|---|---|---|---|---|
| 1 | Today's Mission / Session CTAs | Available | **EXISTING** · reused | `HomeMission` + DX-005A selection unchanged |
| 2 | Study signals / readiness strip | Available | **EXISTING** · reused | `HomeStudySignals` + readiness card |
| 3 | Exam Week Briefing (KWP-006) | Available | **MODIFIED** · folded | Data still computed; surfaced via Morning Brief / Current Focus |
| 4 | Home Insights (fragmented cards) | Available | **MODIFIED** · superseded | Replaced by narrative workspace sections |
| 5 | Readiness Forecast (KWP-012) | Available | **EXISTING** · consumed | One concise forecast on workspace |
| 6 | Educational Memory / Journey (KWP-011) | Available | **EXISTING** · consumed | One milestone, one pattern, one improvement |
| 7 | Strategy / Diagnostics / Difficulty | Available | **EXISTING** · consumed | Combined into Current Focus explanation |
| 8 | Sitting Report / Session Complete | Available | **EXISTING** · linked | Review Yesterday → Sitting Report |
| 9 | Revision surface | Available | **EXISTING** · linked | Resume Revision quick action |
| 10 | Morning Brief adaptive summary | Absent | **NEW** | Greeting + momentum + yesterday + today + duration |
| 11 | Session Plan section | Absent | **NEW** | Objective / duration / status projection |
| 12 | Progress narrative (vs metrics) | Partial | **NEW** | Memory patterns → educational story |
| 13 | Workspace quick-action set | Partial | **NEW** | Begin / Review / Resume / Journey / Forecast |
| 14 | Founder workspace analytics | Absent | **NEW** | Engagement, mission, journey, forecast usage |
| 15 | Learning Runtime / Evidence / Progress / Strategy / Diagnostics / Difficulty / Effectiveness / Memory / Forecast / Mission | Must not redesign | **EXISTING** unchanged | Presentation consumption only |

### EXISTING (reused)

- `StudentHomeService` mission selection (DX-005A)  
- Exam Week Briefing projector + Home Insights builders (inputs still used)  
- `get_readiness_forecast_engine()` (KWP-012)  
- `get_educational_memory_service().journey_for_student()` (KWP-011)  
- Learning Strategy / Diagnostics / Difficulty engines (live or frozen snapshot)  
- Design-system mission panel + study signals macros  
- Presentation telemetry + Founder Platform Intelligence pattern  
- Product Language Guide  

### NEW

- `app/presentation/student/dto/adaptive_workspace.py` — workspace section DTOs  
- `app/presentation/student/adaptive_workspace.py` — presentation composer  
- `app/services/study_workspace_metrics.py` — founder analytics  
- `tests/test_kwp013_adaptive_workspace.py`  
- `KWP013_IMPLEMENTATION_REPORT.md`  

### MODIFIED

- Student Home DTO / service — attach `AdaptiveStudyWorkspace`  
- `home.html` — adaptive layout (Morning Brief → … → Quick Actions)  
- Design system CSS — workspace section styles  
- Presentation telemetry — workspace / journey / forecast events  
- Founder alpha observability — Adaptive Study Workspace section  
- Product language — Adaptive Study Workspace terms  
- KWP-006 Home template assertions — aligned to workspace composition  

---

## 3. Workspace Architecture

```
Experience VMs (Home / History / Revision / Journey / Profile)
+ Evidence Packages (via store)
        │
        ▼
 StudentHomeService.build_home(...)     # existing mission / signals / briefing
        │
        ▼
 compose_adaptive_workspace(page, home) # KWP-013 presentation only
        │
        ├─ Educational Memory narrative     (KWP-011 — consumed)
        ├─ Readiness Forecast               (KWP-012 — consumed)
        ├─ Strategy / Diagnostics / Difficulty (live or frozen snapshot)
        └─ Mission / signals / briefing     (existing Home projection)
        │
        ▼
 AdaptiveStudyWorkspace
        └─ Student Home template (one coherent layout)
```

**Hard boundary:** Workspace is **presentation only**. It never writes Evidence, Progress, Strategy, Diagnostics, Difficulty, Effectiveness, Educational Memory, Forecast state, Twin, or Mission Runtime.

| Authority | Relationship |
|---|---|
| Learning Strategy | Consumed for Current Focus — not redesigned |
| Learning Diagnostics | Consumed for Current Focus — not redesigned |
| Learning Difficulty | Consumed for Current Focus — not redesigned |
| Intervention Effectiveness | Unchanged (Sitting Report / Memory) |
| Educational Memory | Journey highlights — consumed only |
| Readiness Forecast | One concise forecast — consumed only |
| Progress Engine | Unchanged |
| EducationalEvidenceAuthority | Unchanged |
| LearningSessionRuntime / Mission Runtime | Unchanged |

---

## 4. Adaptive Layout

Student Home (`/student/`) renders in this order when the workspace is enabled:

1. **Morning Brief** — greeting, momentum, yesterday, today, estimated time  
2. **Today's Mission** — existing mission panel + primary CTA  
3. **Session Plan** — objective, duration, status  
4. **Current Focus** — combined Strategy / Diagnostics / Difficulty explanation  
5. **Study Signals** — existing orientation strip  
6. **Recent Progress** — educational narrative (not KPI wall)  
7. **Forecast** — one KWP-012 guidance line  
8. **Learning Journey Highlights** — one milestone, one pattern, one improvement  
9. **Quick Actions** — Begin Session · Review Yesterday · Resume Revision · View Journey · View Forecast  

Empty state (no exam) remains Choose Exam. Quiet / day-complete states keep calm operational messaging while still showing available workspace sections.

---

## 5. Morning Brief

Single adaptive summary. Examples of projected language:

> Good evening.  
> You are maintaining steady progress.  
> Yesterday's reinforcement improved your understanding of Discount Factors.  
> Today's session continues that momentum with Annuities.  
> Estimated study time — 70 minutes.

Sources (presentation projection only):

- Time-of-day greeting  
- Study Health tone / Memory consistency patterns → momentum  
- History latest sitting / Memory timeline → yesterday  
- Mission title / day-complete → today  
- Mission duration label → estimated study time  
- Exam Week Briefing reinforcement folded in when History is thin  

---

## 6. Student Experience

### Current Focus

Combines Strategy, Diagnostics, and Difficulty into one explanation:

> Today's focus is Annuities.  
> Strengthen prerequisite foundations first, then continue with Annuities.

Prefers the latest frozen Educational Memory snapshot for the topic; otherwise projects live engines for the current focus topic only. Never exposes category labels, load bands, or internal verdicts.

### Recent Progress

Replaces isolated metrics with narrative:

> You have recovered from your previous difficulties with probability distributions.

or

> Recent sessions suggest stronger consistency.

### Forecast

Reuses KWP-012 exclusively. Surfaces one concise guidance line with optional link to My Learning Journey for the full trajectory explanation.

### Journey Highlights

Reuses Educational Memory. Surfaces at most:

- one meaningful milestone  
- one longitudinal pattern  
- one recent improvement  

### Quick Actions

| Action | Behaviour |
|---|---|
| Begin Session | Mission start / continue CTA |
| Review Yesterday | Latest Sitting Report or History |
| Resume Revision | Revision surface when due |
| View Journey | `/student/learning-journey` |
| View Forecast | Same journey page (forecast section) |

---

## 7. Founder Analytics

Platform Intelligence (`/founder/alpha-observability`) — **Adaptive Study Workspace**:

- Workspace opens  
- Workspace interactions  
- Mission starts / completions / completion rate  
- Insight usefulness signals  
- Journey usage (opens + rate of workspace opens)  
- Forecast usage (views + rate of workspace opens)  
- Unique learners engaged / engagement rate  

Computed from presentation telemetry — no mutation of Educational Intelligence authorities.

New telemetry events (additive): `workspace_opened`, `workspace_interaction`, `learning_journey_opened`, `forecast_viewed`, `insight_useful`.

---

## 8. Architecture Compliance

| Constraint | Status |
|---|---|
| Learning Runtime redesign | **No** |
| Educational Evidence redesign | **No** |
| Progress Engine redesign | **No** |
| Learning Strategy / Diagnostics / Difficulty / Effectiveness redesign | **No** |
| Educational Memory redesign | **No** — consumed only |
| Readiness Forecast redesign | **No** — consumed only |
| Mission Runtime redesign | **No** |
| Workspace is presentation only | **Met** |
| No duplicate educational logic | **Met** |
| Reuse presentation components | **Met** (mission panel, signals, readiness card) |
| Curriculum V1/V2 | **N/A** — no curriculum engine changes |
| Migration Impact | **None** — no schema migrations |

---

## 9. Files Modified

### Created

- `app/presentation/student/dto/adaptive_workspace.py`  
- `app/presentation/student/adaptive_workspace.py`  
- `app/services/study_workspace_metrics.py`  
- `tests/test_kwp013_adaptive_workspace.py`  
- `KWP013_IMPLEMENTATION_REPORT.md`  

### Modified

- `app/presentation/student/dto/student_home.py`  
- `app/presentation/student/services/student_home_service.py`  
- `app/templates/student/home.html`  
- `app/static/css/design_system.css`  
- `app/presentation/student/routes.py`  
- `app/presentation/product_language.py`  
- `app/services/presentation_telemetry_service.py`  
- `app/founder/dashboard/routes.py`  
- `app/founder/dashboard/templates/founder_dashboard/alpha_observability.html`  
- `tests/test_kwp006_home_exam_briefing.py`  

### Migration Impact

**None.**

---

## 10. Tests Executed

```bash
python3 -m pytest tests/test_kwp013_adaptive_workspace.py \
  tests/test_kwp006_home_exam_briefing.py \
  tests/test_kwp012_readiness_forecast.py \
  tests/test_kwp011_educational_memory.py -q
```

**Outcome:** 49 passed (12 KWP-013 + regressions).

Coverage includes empty/disabled workspace, Morning Brief greeting + duration, Current Focus composition, progress narrative from Memory, Forecast reuse (no fabricated certainty), Journey highlights (milestone / pattern / improvement), mandated Quick Actions, Home service attachment, template layout markers, founder metrics, approved product terms, and forbidden-vocabulary scrub.

Ruff clean on new / touched modules.

---

## 11. Known Limitations

1. Workspace composition depends on session-store package visibility for Memory / Forecast enrichment (`ENABLE_DURABLE_STORE` for multi-process durability).  
2. Live Strategy / Diagnostics / Difficulty projection for Current Focus uses thin synthetic evidence when no frozen snapshot exists for the topic — lawful but less personalised than Sitting Report.  
3. Exam Week Briefing is no longer a separate Home card; its signals are folded into Morning Brief / Current Focus. Full weekly briefing detail remains available via `home.briefing` for future surfaces.  
4. Forecast and Journey full detail still live on My Learning Journey — workspace shows highlights only by design.  
5. Founder workspace engagement rates are presentation-telemetry proxies, not calibrated educational outcome metrics.  
6. Parallel Education OS XP-004 workspace under `src/` remains a separate stack and is intentionally not duplicated.

---

## 12. Recommendation for KWP-014

**Working title:** KWP-014 — Adaptive Workspace Continuity & Authority Dogfood

**Mandate:**

1. Dogfood the Adaptive Study Workspace across reinforce / consolidate / recover / advance paths with frozen Sitting Report history.  
2. Publish an explicit **authority matrix** for when Strategy vs Diagnostics vs Difficulty vs Effectiveness vs Forecast each win inside Current Focus (no silent re-ranking).  
3. Optional “what changes if I study one more sitting this week” sensitivity on Forecast (still deterministic, still non-certain).  
4. Founder alert when workspace engagement falls while mission completion stays high (or the inverse) — detect presentation / value mismatches.  
5. Align History archive vocabulary with workspace Morning Brief / Progress narrative (single student language for “am I improving?”).

**Non-goals:** Pass-probability product claims, LLM narrative generation, Progress / Twin / Mission redesign, second workspace database, psychological profiling, redesign of Educational Intelligence engines.

---

## Success Criteria Check

> Students should feel that Kwalitec understands them without ever needing to understand how Kwalitec works internally.

**Status:** Met for the commercial Home path. Adaptive Study Workspace unifies Mission, Focus, Progress, Forecast, and Journey into one calm study environment; Educational Intelligence remains unchanged behind the presentation boundary.

---

**Document status:** Complete — KWP-013 implementation deliverable  
**Next programme:** KWP-014 Adaptive Workspace Continuity & Authority Dogfood (recommended)  
**Architecture stance:** Presentation composition only; SR-001A / EI Phase 1–6 authorities unchanged
