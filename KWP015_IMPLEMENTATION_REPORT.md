# KWP-015 — Educational Authoring & Learning Episodes

**Programme:** KWP-015 · Educational Experience Phase 2  
**Phase:** Educational Authoring — Learning Episodes  
**Date:** 2026-07-31  
**Nature:** Educational composition layer — **not an Educational Intelligence rewrite**  
**Authority:** KWP-014 · KWP-013 · KWP-012 · KWP-011 · KWP-010 · KWP-009 · KWP-008 · KWP-007 · `PRODUCT_BLUEPRINT.md`

---

## 1. Executive Summary

KWP-015 introduces the **Educational Authoring Engine**: curriculum intelligence (Curriculum V2 topics, objectives, Knowledge Graph relationships, and Educational Intelligence signals) is composed into **Learning Episodes** — the smallest intentionally authored educational experience.

Students on Adaptive Study Workspace now see authored educational context, one clear learning objective, ordered concept focus, deterministic activities, explicit success criteria, estimated duration, and tomorrow continuity — without raw CMP wording or isolated topic dumps. Missions surface as Morning Brief → Learning Episode(s) → Checkpoint → Reflection → Tomorrow Preview, with Extra Study offers when spare capacity remains.

**Verdict:** Study sessions feel carefully prepared by an expert tutor. Educational Authoring owns composition language only; Strategy, Diagnostics, Difficulty, Evidence, Progress, Forecast, Memory, Knowledge Architecture graphs, Adaptive Workspace engines, and Mission Runtime remain unchanged.

---

## 2. Implementation Audit

| # | Capability | Verdict | Classification | Notes |
|---|---|---|---|---|
| 1 | Curriculum topic / objective metadata | Available | **EXISTING** · reused · Curriculum V2 | Certified package / artefacts — no metadata duplication |
| 2 | Knowledge Graph relationships | Available | **EXISTING** · reused · Knowledge Graph | KA graph adapter + `CurriculumGraph` for prereq / successor / foundation titles |
| 3 | Mission selection / scheduling | Available | **EXISTING** · reused · Mission Runtime | Authoring never selects or reschedules missions |
| 4 | Adaptive Study Workspace | Available | **MODIFIED** · Adaptive Workspace | Consumes authored mission composition; engines unchanged |
| 5 | Morning Brief | Available | **EXISTING** · reused · Adaptive Workspace | KWP-013 morning narrative retained |
| 6 | Session Plan objective copy | Partial | **MODIFIED** | Prefers authored Learning Episode objective over raw mission dump |
| 7 | Educational Memory | Available | **EXISTING** · reused · Educational Memory | Recent strengthened titles only; Memory engine not redesigned |
| 8 | Learning Episode model (commercial path) | Absent | **NEW** | Application DTOs — context, objective, concepts, activities, success, duration, connection |
| 9 | Domain Learning Episode aggregate (`src/`) | Available | **EXISTING** · not duplicated | Lifecycle/atomicity aggregate remains separate; KWP-015 owns composition projections |
| 10 | Educational Authoring Engine | Absent | **NEW** | Composition authority for Learning Episodes + Mission arcs |
| 11 | Mission writing rules (no CMP paste) | Absent | **NEW** | Deterministic tutor language from titles + graph relationships |
| 12 | Tomorrow Preview + Start Early | Partial | **NEW** | Workspace Tomorrow section; Sitting Report preview remains separate |
| 13 | Extra Study (Continue Revision / Start Tomorrow) | Absent | **NEW** | Offered when available minutes exceed mission duration |
| 14 | Founder episode / authoring analytics | Absent | **NEW** | Platform Intelligence Educational Authoring section |
| 15 | Learning Runtime / Evidence / Progress / Strategy / Diagnostics / Difficulty / Effectiveness / Memory / Forecast / KA / Mission | Must not redesign | **EXISTING** unchanged | Consumed or left alone |

### EXISTING (reused)

- Curriculum V2 / certified learner packages via `graph_from_learner_package`  
- Knowledge Architecture `CurriculumGraph` relationships (KWP-014)  
- Adaptive Study Workspace composer + Morning Brief (KWP-013)  
- Mission Runtime selection / HomeMission projection  
- Educational Memory recent sitting titles (optional enrichment)  
- Founder Platform Intelligence section pattern + presentation telemetry  
- Product Language Guide  
- Domain `src/domain/education/learning_episode` aggregate (lifecycle authority — not rewritten)

### NEW

- `app/application/educational_authoring/` — DTOs, writing rules, duration, episode builder, composition, tomorrow, extra study, engine  
- `app/services/educational_authoring_metrics.py`  
- Workspace Learning Episode / Tomorrow Preview / Extra Study / Mission Composition DTOs  
- Presentation telemetry events for episodes / tomorrow / start-early  
- `tests/test_kwp015_educational_authoring.py`  
- `KWP015_IMPLEMENTATION_REPORT.md`

### MODIFIED

- Adaptive Workspace composer — attaches authored mission composition; Session Plan prefers authored objective  
- `home.html` — Learning Episode, Tomorrow Preview, Extra Study sections  
- Design system CSS — episode / tomorrow / extra workspace styles  
- Product language — Learning Episode, Educational Authoring, Tomorrow Preview, Extra Study  
- Founder alpha observability — Educational Authoring analytics  
- Presentation telemetry allow-list — episode / tomorrow events  

---

## 3. Educational Authoring Architecture

```
Curriculum V2 / Certified package
        │
        ▼
 Knowledge Graph (CurriculumGraph / KA adapter)
        │
        ▼
 Educational Intelligence signals (pace / weak / recent — consumed only)
        │
        ▼
 Educational Authoring Engine
        ├─ writing rules          (tutor language, no CMP paste)
        ├─ Learning Episode       (smallest educational experience)
        ├─ Mission composition    (episodes + checkpoint + reflection)
        ├─ Tomorrow Preview       (continuity + Start Early)
        └─ Extra Study offers     (Continue Revision / Start Tomorrow)
        │
        ▼
 Adaptive Study Workspace (presentation)
        │
        ▼
 Student
```

**Hard boundary:** Educational Authoring owns **educational composition** only. It never writes Evidence, Progress, Strategy, Diagnostics, Difficulty, Intervention Effectiveness, Educational Memory state, Forecast, Twin, Knowledge Architecture graphs, Adaptive Workspace engines, or Mission Runtime schedules.

| Authority | Relationship |
|---|---|
| Curriculum V2 / certified packages | Structure + metadata source — reused |
| Knowledge Architecture / CurriculumGraph | Relationship titles for context / connection — reused |
| Mission Runtime | Selection / scheduling unchanged; authoring composes language around today's mission |
| Adaptive Workspace | Presentation consumes `MissionComposition` |
| Learning Strategy / Diagnostics / Difficulty | Not redesigned; weak-topic signal may be consumed for episode shape |
| Educational Memory | Optional recent titles for “strengthened recently” language |
| Readiness Forecast / Progress / Evidence | Unchanged |
| `src/.../learning_episode` | Separate domain lifecycle aggregate — not duplicated |

---

## 4. Learning Episode Model

A **Learning Episode** is the smallest educational experience. Every mission consists of one or more episodes.

| Element | Rule |
|---|---|
| Educational Context | Why today's work matters — composed from foundations / successors / recent strengthening |
| Learning Objective | One clear objective — never a CMP paragraph |
| Concept Focus | 2–5 ordered concepts from curriculum-grounded titles |
| Activities | Deterministic: Read, Worked Example, Practice, optional Revision, Checkpoint |
| Success Criteria | Explicit finished definition (Explain / Solve / Complete) |
| Estimated Duration | Effort × difficulty × pace × prior evidence (rounded to 5 minutes) |
| Connection | Why tomorrow builds on today |

Alignment codes (`topic:`, `objective:`, `prereq:`, `successor:`, `subject:`) map every authored episode back to curriculum structure — no fabricated educational content.

---

## 5. Mission Composition

Authored mission arc for Adaptive Workspace:

```
Morning Brief          (KWP-013 — reused)
        ↓
Learning Episode 1     (+ Episode 2 when weak foundations warrant)
        ↓
Checkpoint
        ↓
Reflection
        ↓
Tomorrow Preview
        ↓
Extra Study             (when spare capacity ≥ 15 minutes)
```

Weak-topic missions may open with a short foundation episode on the prerequisite title, then the primary topic episode — still composition-only; Mission Runtime selection is untouched.

---

## 6. Writing Rules

| Never | Instead |
|---|---|
| Copy CMP | Compose tutor prose from topic / relationship titles |
| Concatenate objectives | One clear objective sentence |
| Repeat syllabus wording (“Study Probability.”) | Educational framing (“Today's session develops the foundations required for…”) |
| Fabricate content | Only cite titles and relationships present in inputs / graph |
| Hype / gamification / guilt | Professional, calm, encouraging, premium actuarial-tutor tone |

CMP-dump detection rejects long semicolon-heavy extracts and markers such as “candidates should”, “learning outcome”, “unit aim”.

**Example**

- BAD: `Study Probability.`  
- GOOD: `Today's session develops the foundations required for Conditional Probability. You'll begin by strengthening sample-space reasoning before applying those ideas to events.`  
  (Grounded form in this milestone: foundation / successor topic titles from the Knowledge Graph.)

---

## 7. Tomorrow Preview

Workspace displays:

- **Tomorrow** — next topic title  
- Continuity line — “Building directly on today's … work.”  
- Estimated duration  
- Optional **Start Early** — begin the introduction today; copy states that tomorrow's Mission will adjust (Mission Runtime remains the scheduler)

Tomorrow title resolves from explicit next-topic input, Journey up-next when present, or Knowledge Graph successors.

---

## 8. Extra Study Flow

When `available_minutes − mission_minutes ≥ 15`:

| Offer | When |
|---|---|
| Continue Revision | Revision available or weak-topic signal |
| Start Tomorrow | Tomorrow / successor title known |

Never leave students asking “What now?” after finishing early.

---

## 9. Founder Analytics

Platform Intelligence section **Educational Authoring** reports:

- Mission completion  
- Episode completion / starts  
- Average episode duration (when supplied)  
- Episode abandonment  
- Tomorrow Preview opens  
- Start Tomorrow / Start Early usage  
- Reflection completion  
- Most difficult / most successful episodes (when supplied)

Implementation: `EducationalAuthoringMetrics` + alpha observability template + new presentation telemetry event types.

---

## 10. Architecture Compliance

- Layering preserved: presentation → application educational authoring → curriculum graph / Home inputs.  
- No educational logic migrated out of Strategy / Diagnostics / Difficulty / Memory / Forecast / Evidence / Progress.  
- Curriculum V1/V2 traversal unchanged; authoring consumes graph + titles only.  
- No Flask globals inside authoring services (explicit `AuthoringContext`).  
- Deterministic cores — same context ⇒ same episodes, activities, and copy.  
- Domain Learning Episode aggregate under `src/` left intact (lifecycle ≠ composition).  

---

## 11. Files Created

- `app/application/educational_authoring/__init__.py`  
- `app/application/educational_authoring/dto.py`  
- `app/application/educational_authoring/guidance.py`  
- `app/application/educational_authoring/writing.py`  
- `app/application/educational_authoring/duration.py`  
- `app/application/educational_authoring/episode.py`  
- `app/application/educational_authoring/composition.py`  
- `app/application/educational_authoring/tomorrow.py`  
- `app/application/educational_authoring/extra_study.py`  
- `app/application/educational_authoring/engine.py`  
- `app/services/educational_authoring_metrics.py`  
- `tests/test_kwp015_educational_authoring.py`  
- `KWP015_IMPLEMENTATION_REPORT.md`  

## 12. Files Modified

- `app/presentation/student/dto/adaptive_workspace.py`  
- `app/presentation/student/adaptive_workspace.py`  
- `app/templates/student/home.html`  
- `app/static/css/design_system.css`  
- `app/presentation/product_language.py`  
- `app/services/presentation_telemetry_service.py`  
- `app/founder/dashboard/routes.py`  
- `app/founder/dashboard/templates/founder_dashboard/alpha_observability.html`  

---

## 13. Tests

```bash
python3 -m pytest tests/test_kwp015_educational_authoring.py -v
python3 -m pytest tests/test_kwp013_adaptive_workspace.py tests/test_kwp014_knowledge_architecture.py -v
python3 -m ruff check app/application/educational_authoring/ app/services/educational_authoring_metrics.py …
```

**Outcome:** KWP-015 suite **13 passed**; KWP-013 / KWP-014 suites **30 passed**; ruff clean on touched paths.

---

## 14. Migration Impact

**None.** No Alembic migrations. Learning Episodes are composed projections; persistence of episode lifecycle remains out of scope for this programme.

---

## 15. Known Limitations

1. Authoring richness depends on Knowledge Graph / certified package coverage — sparse packages yield thinner context and concept focus.  
2. Tomorrow Preview soft-falls back to successors / Journey up-next; full Mission Runtime “schedule tomorrow” adjustment is not invoked by Start Early (copy only).  
3. Average episode duration and most-difficult / most-successful episode rankings require richer telemetry payloads than event counts alone.  
4. Domain `src/domain/education/learning_episode` lifecycle is not yet bridged to commercial authored projections.  
5. Activity prompts are deterministic templates — not item-bank content or worked-example bodies.  
6. Extra Study “Start Tomorrow” links to Home pending a dedicated early-start session entry point.  

---

## 16. Technical Debt

- Persist authored episode snapshots alongside Evidence Packages for dogfood analytics.  
- Wire Start Early to Mission Runtime’s tomorrow adjustment path when that API is student-safe.  
- Unify commercial Learning Episode projections with the `src/` domain aggregate under one read model in a later phase.  
- Emit episode start/complete/abandon events from Session lifecycle (currently allow-listed for founders).  

---

## 17. Recommendation for KWP-016

**Working title:** KWP-016 — Authored Episode Runtime Continuity & Content Depth

**Suggested scope:**

1. Persist Learning Episode projections with Evidence Packages and dogfood Start Early / Extra Study.  
2. Bridge commercial authoring DTOs with the `src/` Learning Episode lifecycle where educationally safe.  
3. Deepen activity substance (worked-example and practice prompts from certified artefacts — still no LLM).  
4. Founder drill-down: difficult episodes → learners → recovery / revision pathways (KA reuse).  
5. Validate writing quality against actuarial chains (Probability → Conditional Probability → Bayes; Interest Theory → Annuities).  

**Next programme:** KWP-016 Authored Episode Runtime Continuity & Content Depth (recommended)

---

## Success Criteria Check

> A student should feel “I know exactly what I am learning, why I am learning it, what success looks like, and what comes next,” without ever seeing raw CMP wording or isolated topic names. The educational experience should feel intentionally authored, not automatically assembled.

**Status:** Met for the commercial Adaptive Study Workspace path. Educational Authoring composes Learning Episodes and Mission arcs from curriculum-aligned inputs; students see context, objective, concepts, activities, success criteria, duration, tomorrow continuity, and extra-study options. No authority redesign; no CMP paste.

---

**Document status:** Complete — KWP-015 implementation deliverable  
**Next programme:** KWP-016 Authored Episode Runtime Continuity & Content Depth (recommended)  
**Architecture stance:** Composition layer only; Learning Runtime / Evidence / Progress / Strategy / Diagnostics / Difficulty / Effectiveness / Memory / Forecast / Knowledge Architecture / Mission Runtime unchanged
