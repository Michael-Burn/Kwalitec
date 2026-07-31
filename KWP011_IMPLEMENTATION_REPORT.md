# KWP-011 — Educational Memory & Learning Timeline

**Programme:** KWP-011 · Educational Memory & Learning Timeline  
**Phase:** Educational Intelligence Phase 5  
**Date:** 2026-07-30  
**Nature:** Persistence layer for educational intelligence outcomes — **not a reasoning engine**  
**Authority:** KWP-010 · KWP-009 · KWP-008 · KWP-007 · SR-001A · `PRODUCT_BLUEPRINT.md`

---

## 1. Executive Summary

KWP-011 introduces **Educational Memory**: a persistence and projection layer that freezes Learning Strategy, Diagnostics, Difficulty, and Intervention Effectiveness outputs onto Evidence Packages at sitting close, then derives a chronological Learning Timeline, longitudinal patterns, and educational milestones from that evidence.

Students gain **My Learning Journey** — an educational story across months of sittings — and can reopen historical Sitting Reports with Strategy / Diagnostics / Difficulty / Effectiveness **as they existed at the time**. Founders see longitudinal memory metrics (snapshot coverage, recovery/mastery duration, retention recovery, timeline completeness, growth trajectories).

**Verdict:** The platform can now answer *“What kind of learner have I become?”* from years of educational evidence, without redesigning Learning Runtime, Evidence, Progress, Twin, Strategy, Diagnostics, Difficulty, Effectiveness, Mission Runtime, or the Commercial Loop.

---

## 2. Implementation Audit

| # | Capability | Verdict | Classification | Notes |
|---|---|---|---|---|
| 1 | Evidence Package persistence | Available | **EXISTING** | Reused `lsr.evidence_package`; no second store |
| 2 | Decision Journal / Educational Timeline | Available | **EXISTING** | Guidance memory retained; not duplicated |
| 3 | Strategy / Diagnostics / Difficulty / Effectiveness engines | Available | **EXISTING** · consumed | Reasoning unchanged; outputs snapshotted |
| 4 | Sitting Report live projection | Available | **MODIFIED** | Prefers frozen snapshot when present |
| 5 | Intelligence output persistence | Absent | **NEW** | `intelligence_snapshot` on package |
| 6 | Auto `prior_intervention` chain | Absent | **NEW** | Last same-topic outgoing → next sitting |
| 7 | Learning Timeline from evidence | Partial (Journal only) | **NEW** (package-derived) | Never fabricates events |
| 8 | Longitudinal patterns (student) | Absent | **NEW** | Prerequisite, mismatch, recovery, … |
| 9 | Educational milestones (no gamification) | Partial (schema only) | **NEW** | Growth milestones from evidence |
| 10 | My Learning Journey | Absent | **NEW** | `/student/learning-journey` |
| 11 | Historical Sitting Report drill-down | Absent | **NEW** | History + archive links to Complete |
| 12 | Founder longitudinal memory metrics | Absent | **NEW** | Platform Intelligence section |
| 13 | Learning Runtime / Evidence / Progress / Twin / Mission / Commercial | Must not redesign | **EXISTING** unchanged | Additive persist hook only |

### EXISTING (reused)

- Session Evidence Packages + `SessionDocumentStore` / `list_evidence_packages`  
- Learning Strategy / Diagnostics / Difficulty / Intervention Effectiveness engines  
- Sitting Report projector + Complete surface  
- Decision Journal + Educational Timeline (guidance memory — complementary)  
- History archive surface + Founder Platform Intelligence pattern  
- Product Language Guide  

### NEW

- `app/application/educational_memory/` — DTOs, snapshot, timeline, patterns, milestones, narrative, service  
- `app/services/educational_memory_metrics.py`  
- `app/templates/student/learning_journey.html`  
- `tests/test_kwp011_educational_memory.py`  
- `KWP011_IMPLEMENTATION_REPORT.md`  

### MODIFIED

- Runtime complete — additive Educational Memory persist after sitting outcome  
- Completion service — flattens frozen Sitting Report fields into metadata  
- Sitting Report — prefers frozen snapshot; never rebuilds historical advice with current rules  
- History cards / History bridge — Sitting Report links + My Learning Journey  
- Founder alpha observability — Educational Memory metrics  
- Product language — Educational Memory / My Learning Journey / Learning Timeline  

---

## 3. Educational Memory Architecture

```
Evidence Package (existing persistence)
        │
        ▼  on Session complete (additive)
 EducationalMemoryService.persist_on_store
   ├─ resolve prior same-topic outgoing intervention
   ├─ Strategy / Diagnostics / Difficulty / Effectiveness  (evaluate once)
   └─ freeze intelligence_snapshot + outgoing_intervention
        │
        ├─ Sitting Report / Complete  → frozen student fields when present
        ├─ My Learning Journey        → timeline + patterns + milestones + story
        └─ Founder EducationalMemoryMetrics
```

**Hard boundary:** Educational Memory **stores outcomes**. It does not decide WHAT / WHY / Pace / Progress feedback — those remain Strategy, Diagnostics, Difficulty, and Effectiveness.

| Authority | Relationship |
|---|---|
| Learning Strategy | Consumed at capture; not redesigned |
| Learning Diagnostics | Consumed at capture; not redesigned |
| Learning Difficulty | Consumed at capture; not redesigned |
| Intervention Effectiveness | Consumed at capture; prior auto-attached |
| EducationalEvidenceAuthority | Unchanged; packages remain the sitting spine |
| Progress Engine / Student Twin | Unchanged |
| LearningSessionRuntime / Session FSM | Additive persist only |
| Mission Runtime / Commercial Loop | Unchanged |
| Decision Journal / Educational Timeline | Complementary guidance memory — not replaced |

---

## 4. Persistence Design

### Intelligence snapshot (`intelligence_snapshot` on Evidence Package)

Schema `kwp011.1` includes:

| Block | Purpose |
|---|---|
| `strategy` / `diagnostics` / `difficulty` / `effectiveness` | Full opaques for founder / continuity |
| `prior_intervention` | What this sitting evaluated against |
| `outgoing_intervention` | What the next same-topic sitting should inherit |
| `student_sitting_report` | Frozen student-facing Sitting Report fields |

### Continuity

1. On complete, memory looks up the learner’s latest same-topic package.  
2. Its `outgoing_intervention` becomes `prior_intervention` for Effectiveness.  
3. Snapshot is written once; re-complete is **idempotent** (existing snapshot kept).  

### No duplicate persistence

- Observations remain only on the Evidence Package.  
- Decision Journal remains the guidance-commitment memory.  
- Longitudinal Evidence Repository (P4-MS002) is **not** used as a parallel sitting store.

---

## 5. Timeline Model

Chronological entries derived **only** from Evidence Packages (+ snapshots):

| Event | Evidence basis |
|---|---|
| Started topic | First sitting for a topic |
| Repeated reinforcement | Weak follow-up / reinforcement strategy |
| Consolidated | Consolidate strategy |
| Understanding improved | Accuracy improved vs prior same-topic sitting |
| Advanced | Progress advanced / advance strategy |
| Knowledge decayed | Retention risk / recover strategy |
| Recovered | Successful recovery evidence |
| Mastered | Sustained strong + advance signals |
| Reflected | Reflection observation present |
| Study sitting | Spine entry for every package |

**Never fabricate.** Thin history lawfully yields fewer meaningful events; completeness is measured honestly for founders.

---

## 6. Student Experience

### My Learning Journey (`/student/learning-journey`)

Students see:

- A natural-language **story** (e.g. earlier reinforcement → recent consistency)  
- **Educational milestones** (growth — no points, badges, or leaderboards)  
- **Patterns over time**  
- A **Learning Timeline**  
- An archive of **Sitting Reports** with frozen Strategy / Diagnostics / Difficulty / Effectiveness  

### History

- Bridge links to Decision Journal, Educational Timeline, and My Learning Journey.  
- Session cards link to `/session/<id>/complete` to reopen the Sitting Report.  

### Historical Sitting Reports

When `intelligence_snapshot` (or flattened metadata) is present, `build_sitting_report` **prefers frozen fields** and does not re-run engines with current rules.

---

## 7. Founder Analytics

Platform Intelligence (`/founder/alpha-observability`) — **Educational Memory**:

- Snapshot coverage / recommendation persistence  
- Timeline entry count / completeness  
- Average recovery duration (sittings)  
- Average mastery duration (sittings)  
- Retention recovery rate  
- Learners with journey narrative  
- Growth trajectory labels  
- Pattern / milestone distributions  
- Repeated misconception categories  

Computed by scanning Evidence Packages — no mutation of EI authorities.

---

## 8. Architecture Compliance

| Constraint | Status |
|---|---|
| Learning Runtime redesign | **No** — additive persist hook only |
| Educational Evidence redesign | **No** |
| Progress Engine redesign | **No** |
| Student Twin redesign | **No** |
| Learning Strategy / Diagnostics / Difficulty / Effectiveness redesign | **No** — consumed at capture |
| Mission Runtime / Commercial Loop | **Unchanged** |
| Memory is persistence, not reasoning | **Met** |
| No fabricated timeline events | **Met** |
| No gamification (points / badges / leaderboards) | **Met** |
| Historical advice not rebuilt with current rules | **Met** when snapshot present |
| Curriculum V1/V2 | **N/A** — no curriculum engine changes |
| Migration Impact | **None** — opaque document fields only |

---

## 9. Files Modified

### Created

- `app/application/educational_memory/__init__.py`  
- `app/application/educational_memory/dto.py`  
- `app/application/educational_memory/snapshot.py`  
- `app/application/educational_memory/timeline.py`  
- `app/application/educational_memory/patterns.py`  
- `app/application/educational_memory/milestones.py`  
- `app/application/educational_memory/narrative.py`  
- `app/application/educational_memory/service.py`  
- `app/services/educational_memory_metrics.py`  
- `app/templates/student/learning_journey.html`  
- `tests/test_kwp011_educational_memory.py`  
- `KWP011_IMPLEMENTATION_REPORT.md`  

### Modified

- `app/infrastructure/adapters/learning_session/runtime_engine.py`  
- `app/application/session_experience/completion_service.py`  
- `app/presentation/session/sitting_report.py`  
- `app/presentation/session/view_models.py`  
- `app/presentation/student/routes.py`  
- `app/presentation/student/view_models.py`  
- `app/templates/student/history.html`  
- `app/templates/student/components/history_card.html`  
- `app/presentation/product_language.py`  
- `app/founder/dashboard/routes.py`  
- `app/founder/dashboard/templates/founder_dashboard/alpha_observability.html`  

### Migration Impact

**None.**

---

## 10. Tests Added

```bash
python3 -m pytest tests/test_kwp011_educational_memory.py \
  tests/test_kwp010_intervention_effectiveness.py \
  tests/test_kwp009_learning_difficulty.py \
  tests/test_kwp005_sitting_reports.py -q
```

**Outcome:** 56 passed (12 KWP-011 + regressions).

Coverage includes snapshot capture / restore, prior-intervention continuity, store idempotence, frozen Sitting Report preference, timeline from evidence, patterns/milestones (no gamification language), journey narrative safety, founder metrics, and template / approved-term markers.

Ruff clean on new / touched modules.

---

## 11. Known Limitations

1. Sittings completed **before** KWP-011 lack snapshots — History may still reopen Complete, but live engines may run until a snapshot exists.  
2. Learning Journey filters Evidence Packages by `student_id` on the session store; durable multi-process coverage depends on `ENABLE_DURABLE_STORE`.  
3. Timeline / pattern / milestone heuristics are deterministic and evidence-gated — sparse history lawfully yields thin narratives.  
4. Decision Journal Educational Timeline remains journal-derived; package Learning Timeline is a complementary sitting narrative, not a merge.  
5. My Learning Journey is linked from History (not a primary nav item) to avoid crowding the OS chrome.  
6. Founder recovery/mastery durations are sitting-count spans, not calendar-day claims.

---

## 12. Recommendation for KWP-012

**Working title:** KWP-012 — Educational Intelligence Continuity Authority Matrix & Dogfood

**Mandate:**

1. Publish an explicit **authority matrix**: when Strategy vs Diagnostics vs Difficulty vs Effectiveness vs Runtime A Decision each win (no silent re-ranking).  
2. Dogfood My Learning Journey + frozen Sitting Report history across reinforce / consolidate / recover / advance paths.  
3. Optional backfill: capture snapshots for recent packages missing `intelligence_snapshot` using stored evidence only (still never invent).  
4. Founder alert when recommendation persistence or timeline completeness falls below a deterministic threshold.  
5. Unify History session cards with journey archive rows (single student-facing sitting archive vocabulary).

**Non-goals:** Evidence grade redesign, Progress Engine rewrite, Mission Runtime redesign, LLM narrative generation, gamification, psychological profiling, second memory database.

---

## Success Criteria Check

> The platform should answer “What kind of learner have I become?” using years of educational evidence, not only today's session.

**Status:** Met for the commercial path. Educational intelligence outputs persist on Evidence Packages; Learning Timeline / patterns / milestones derive only from that evidence; students receive My Learning Journey and frozen Sitting Report history; founders see longitudinal memory metrics. Reasoning remains inside Strategy, Diagnostics, Difficulty, and Effectiveness.

---

**Document status:** Complete — KWP-011 implementation deliverable  
**Next programme:** KWP-012 Educational Intelligence Continuity Authority Matrix & Dogfood (recommended)  
**Architecture stance:** SR-001A authorities unchanged; Educational Memory persists and projects outcomes only
