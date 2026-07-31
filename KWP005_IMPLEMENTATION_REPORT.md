# KWP-005 — Assessment Mode & Sitting Reports

**Programme:** KWP-005 · Assessment Mode & Sitting Reports  
**Phase:** Commercialisation Phase 5  
**Date:** 2026-07-30  
**Nature:** Presentation / product experience — **no runtime authority redesign**  
**Authority:** KWP-004 · KWP-003 · KWP-002 · SR-001A · EV-001A · EV-001B · SDT-004 · SR-003 · `PRODUCT_BLUEPRINT.md`

---

## 1. Executive Summary

KWP-005 surfaces Educational+ evidence already captured by the commercial Session loop into a premium student-facing **Sitting Report**, reached immediately after Finish Review. The report answers what was studied, which exercises were assigned and completed, how practice went, what was learned, what strengthened, what needs reinforcement, why Progress changed, and what happens tomorrow — in plain language, without Twin / Evidence Authority / Educational+ / Runtime / FSM jargon.

**Assessment Mode** is implemented as a presentation section inside the Sitting Report over scored practice outcomes — not a new educational engine. Learning Insights quality was improved from evidence-backed observations. Journey **Needs Attention** is wired as a Weak Topic Centre from existing Revision / History facts. Session History discoverability and founder sitting metrics were extended on existing surfaces.

**Verdict:** Presentation consumes existing evidence, Progress, and Twin outputs. LearningSessionRuntime, EducationalEvidenceAuthority, StudentTwinEngine, ProgressEngine, Mission Runtime, Commercial Loop, Session FSM, curriculum traversal, and evidence mathematics were **not** redesigned.

---

## 2. Implementation Audit

| Capability | Verdict | Classification | Notes |
|---|---|---|---|
| **1. Assessment Mode** | Partial → productised | **NEW** (presentation) · reuses scored practice | `/assessment/` Learning Check and adaptive Quick Check existed; no Session Sitting Assessment Mode. Added Assessment Mode section on Sitting Report over EV-RT-07/08/40 outcomes. |
| **2. Session Completion / Sitting Report** | Partial → production path | **NEW** Sitting Report · **MODIFIED** Complete surface + Finish redirect | Complete UI existed but Finish Review redirected to Home. Now redirects to Sitting Report (`session.complete`). |
| **3. Learning Insights** | Partial | **MODIFIED** | Templates existed; runtime strings were hollow. Insights now derived from practice outcomes, reflection, and finish honesty. Journey insights wired from History / Revision. |
| **4. Weak Topic presentation** | Partial | **MODIFIED** | Journey Needs Attention was always empty. Now projects Revision options + recent History practice as Weak Topic Centre. Sitting Report lists needs-reinforcement from incorrect practice + syllabus refs. |
| **5. Progress explanations** | Missing / thin | **NEW** (presentation) | Students now see why Journey moved or stayed (honest finish, accepted study, partial/no). |
| **6. Founder analytics** | Partial | **MODIFIED** | Reused Platform Intelligence Educational+ yield; added Finish Review breakdown, reflection rate, evidence density. |
| **7. Session History** | Exists | **MODIFIED** | History page + cards existed. Improved discoverability, outcome copy, and links from Sitting Report. |

### EXISTING (reused)

- Finish Review (Yes / Partially / No) — LXP-003 / KWP-002  
- Evidence Package + Authority validation — EV-001A / EV-001B  
- Scoreable practice + Correct/Incorrect feedback — KWP-004  
- CompletionSnapshot / Complete surface shell — LXP-003  
- Journey Needs Attention / Learning Insights template slots — SOP / KWP-002  
- HistoryService + history cards — Student OS  
- `EducationalYieldMetrics` — KWP-004  
- Product Language Guide + forbidden-term scrub  

### NEW

- `app/presentation/session/sitting_report.py` — Sitting Report / Assessment Mode projector  
- Sitting Report UI blocks on Complete surface  
- Progress explanation + tomorrow preview copy  
- `tests/test_kwp005_sitting_reports.py`  
- Persistence helper `save_sitting_outcome` for Sitting Report GET  

### MODIFIED

- Finish Review POST → `session.complete` (Sitting Report) instead of Home  
- `get_completion_summary_opaque` — opaque sitting facts for presentation  
- CompletionService metadata carry-through  
- Completion / StudySession view models + `session_body.html`  
- Journey VM Weak Topic Centre + Learning Insights population  
- History card / header discoverability  
- Founder Platform Intelligence yield metrics  
- Product language approved terms (`Sitting Report`, `Assessment Mode`)  
- Complete surface labels (`Sitting Report`)  

---

## 3. Assessment Mode

**Nature:** Presentation layer over existing Educational+ scored practice.

After Finish Review, the Sitting Report includes an **Assessment Mode** section when practice was assigned or scored. It shows:

- Performance summary (correct / to revisit)  
- Exercises assigned and completed (titles + stages — **never** CMP question text)  
- Assessment summary in plain language  

It does **not** introduce quiz engines, mock exams, new evidence types, or grading math. Scoring remains KWP-004 deterministic practice scoring; evidence remains EV-001B Authority.

Separate `/assessment/` Learning Check and `/adaptive-assessment/` Quick Check remain available legacy/adjacent paths and were not replaced.

---

## 4. Sitting Reports

**Happy path:** Summary (Finish Review) → **Sitting Report** → Return Home / Journey / History.

The Sitting Report answers:

| Question | Source (opaque, student-safe) |
|---|---|
| What did I study? | Topic + learning objectives + stage presence |
| Which exercises assigned / completed? | Activity sequence titles / stages |
| How did I perform? | Practice correct / incorrect observations |
| What did I learn? | Learning Insights from outcomes |
| Strengthened / needs reinforcement? | Correct vs incorrect practice + objectives |
| Why did Progress change? | Finish verdict + progress/mission flags + disposition |
| What happens tomorrow? | Next recommendation / reinforcement preview |

Internal IDs, Twin, Evidence Authority, Educational+, Runtime, and FSM never appear in learner copy.

---

## 5. Learning Insights

**Before:** Generic runtime strings (“Finish review closes today’s session — it does not claim mastery.”) and empty Journey insights.

**After:** Plain-language insights such as:

- “You consistently answered … practice correctly.”  
- “You struggled with … practice today.”  
- “You left a reflection — that helps shape tomorrow’s Session.”  
- “Tomorrow’s Session has been adjusted toward reinforcement.”  

Journey Learning Insights populate from History (recent Session, strengthened topics, readiness trend) and Revision suggestions when available.

---

## 6. Weak Topic Centre

**Audit:** Journey Needs Attention UI existed but was hard-wired empty; ProgressEngine weak annotations stayed internal; Revision already carried dynamic weak framing.

**Implementation:** Journey Needs Attention is the Weak Topic Centre:

- Revision primary + alternatives (topic, priority, why / benefit)  
- Recent History revision topics as soft reinforcement hints  
- Link to Revision for guided reinforcement  
- Sitting Report lists needs-reinforcement + syllabus references (chapter / question refs only — no CMP content reproduction)  

No ProgressEngine or Mission selection redesign.

---

## 7. Session History

**Existing:** History route, study time, readiness trends, completed Session cards.

**Improvements:**

- Clearer page support copy (past Sessions, reflections, trends)  
- Card insight / progress lines for discoverability  
- Sitting Report links to History and Journey  

Full per-sitting replay of Assessment Mode from History remains a follow-up (packages are persisted; dedicated History drill-down not built).

---

## 8. Founder Analytics

**Reused:** Platform Intelligence Educational+ yield panel.

**Extended metrics (additive):**

- Finish Review Yes / Partially / No counts  
- Reflection completion rate  
- Average observation density (evidence density proxy)  

Educational+ rate, Learning Yield, Twin-updated sittings retained. No parallel founder dashboard.

---

## 9. Student Impact Assessment

| Dimension | Assessment |
|---|---|
| **Student problem** | After Finish Review, students were sent Home without a clear report of what they learned, what still needs work, or why tomorrow differs. |
| **Student benefit** | Sitting Report + Assessment Mode close the Session with calm, premium clarity. |
| **Learning benefit** | Insights and reinforcement signals connect scored practice to Journey / tomorrow without overclaiming mastery. |
| **Success metrics** | Finish → Sitting Report reach; insight non-emptiness after scored sittings; Needs Attention population when Revision exists; zero forbidden internal terms on Complete. |
| **Risks** | Overclaiming progress; hollow insights when unscored; syllabus refs sparse until package artefacts carry them. |
| **Assumptions** | Commercial Loop flags ON; KWP-004 scored practice present for Educational+ denser sittings. |

---

## 10. Commercial Readiness Assessment

| Domain | Effect |
|---|---|
| **CR1 Student experience** | Improved — premium close ritual |
| **CR2 Trust / honesty** | Improved — progress why + partial/no honesty |
| **CR3 Personalisation perception** | Improved — Insights / Weak Topic Centre / tomorrow preview |
| **CR4–CR9** | Unchanged or incidental |

**Estimated CRI delta:** Provisional **+1 to +2** on student-experience / trust perception (presentation only; not validated cohort measurement).

**Remaining blockers:** Content density (KWP-004 seed still thin vs full CMP bank); History drill-down; validated KSI / dogfood still required for Version 1 declaration.

---

## 11. Architecture Compliance

| Constraint | Status |
|---|---|
| LearningSessionRuntime redesign | **No** — additive opaque summary + sitting outcome persistence only |
| EducationalEvidenceAuthority | **Unchanged** |
| StudentTwinEngine | **Unchanged** |
| ProgressEngine | **Unchanged** |
| Mission Runtime / Commercial Loop / Session FSM | **Unchanged** |
| Curriculum traversal / evidence mathematics | **Unchanged** |
| Layering | Presentation projects Sitting Report; application carries opaque metadata; infrastructure exposes sitting facts without authority math |
| Curriculum V1/V2 | **N/A** — no curriculum engine changes |

---

## 12. Files Modified

### Created

- `app/presentation/session/sitting_report.py`  
- `tests/test_kwp005_sitting_reports.py`  
- `KWP005_IMPLEMENTATION_REPORT.md`  

### Modified

- `app/presentation/session/routes.py`  
- `app/presentation/session/view_models.py`  
- `app/presentation/session/dto/study_session.py`  
- `app/presentation/session/services/study_session_service.py`  
- `app/presentation/session/navigation.py`  
- `app/templates/session/partials/session_body.html`  
- `app/application/session_experience/completion_service.py`  
- `app/infrastructure/adapters/learning_session/runtime_engine.py`  
- `app/infrastructure/adapters/learning_session/persistence.py`  
- `app/domain/session_experience/session_workspace.py`  
- `app/domain/session_experience/session_navigation.py`  
- `app/presentation/product_language.py`  
- `app/presentation/student/view_models.py`  
- `app/templates/student/journey.html`  
- `app/templates/student/history.html`  
- `app/templates/student/components/history_card.html`  
- `app/services/educational_yield_metrics.py`  
- `app/founder/dashboard/templates/founder_dashboard/alpha_observability.html`  

### Migration Impact

**None.**

---

## 13. Tests Added

```bash
python3 -m pytest tests/test_kwp005_sitting_reports.py -q
```

**Outcome:** 8 passed.

Also green with related suites: `tests/test_kwp004_assessable_practice.py`, `tests/test_kwp002_student_value_activation.py`, `tests/test_lxp003_session_product.py`, `tests/presentation/student/test_templates.py`, `tests/test_dx006b_student_home.py`.

Coverage includes Sitting Report projection, Assessment Mode activation, progress-why for partial finish, Finish → Complete redirect, Journey Weak Topic Centre markers, and founder Finish/Reflection metrics.

---

## 14. Known Limitations

1. Sitting Report richness depends on KWP-004 scored practice density and syllabus_refs on activity items.  
2. History does not yet open a stored Sitting Report per past Session (discoverability only).  
3. Weak Topic Centre uses Revision / History — not a live ProgressEngine weak-topic feed (by design: no Progress redesign).  
4. Assessment Mode is Session sitting presentation, not a timed mock exam product.  
5. Founder metrics remain aggregate; no per-student Sitting Report inspector.  

---

## 15. Recommendation for KWP-006

**Working title:** KWP-006 — Exam Week Briefing & Retention Loop

**Mandate:** Aggregate Sitting Reports + Journey Weak Topic Centre + Exam Readiness into a weekly student briefing and retention-oriented Home moment — still presentation-only over existing Progress / Twin / Evidence authorities.

**Suggested outcomes:**

1. Weekly Exam Briefing surface (what strengthened, what to reinforce, pace honesty).  
2. History drill-down to stored Sitting Reports.  
3. Optional founder per-sitting inspector atop Evidence Packages.  
4. Dogfood / provisional KSI validation of KWP-002→005 commercial loop.  

**Non-goals:** New evidence grades, Twin math, Progress Engine redesign, CMP content reproduction.

---

## Success Criteria Check

> A student completing a Session should feel: “I know exactly what I learned, what still needs work, and why tomorrow’s Session will be different.” — without exposing internal architecture.

**Status:** Met for the commercial Finish → Sitting Report path when substance + scored practice are present. Unscored / partial sittings remain honest and calm rather than empty or technical.
