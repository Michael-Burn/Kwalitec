# KWP-004 — Assessable Practice Activation

**Programme:** KWP-004 · Assessable Practice Activation  
**Phase:** Commercialisation Phase 4  
**Date:** 2026-07-30  
**Nature:** Content & activity enrichment — **no runtime authority redesign**  
**Authority:** KWP-003 · SR-001A · EV-001A · EV-001B · SDT-004 · SR-003  

---

## Executive Summary

KWP-004 activates scoreable Educational+ practice inside the existing commercial Session. Package-derived practice activities now carry authorised answer keys, mark schemes, explanations, and model answers. The activity layer scores deterministically and passes `scored_correct` into the existing Evidence Package Builder, which emits **EV-RT-07** / **EV-RT-08** (and **EV-RT-40** for structured MCQ/numeric items).

A normal Finish Review **Yes** sitting with scored practice now yields **Accepted** Educational+ evidence — Progress may advance, Twin may update when `SR_TWIN_DAILY_LOOP` is ON — without redesigning LearningSessionRuntime, EducationalEvidenceAuthority, StudentTwinEngine, ProgressEngine, or Mission Runtime.

Students see calm Correct / Incorrect feedback with Why, Model Answer, Common Mistake, and Next Action. Founders see Educational+ rate, Behavioural vs Educational observations, Twin activation signals, and Learning Yield on Platform Intelligence.

**Verdict:** Content in → Educational+ out. Architecture unchanged. Commercial Loop finally has assessable fuel.

---

## Content Schema

| Artefact | Role |
|---|---|
| `ScoreablePracticeItem` | Prompt, response type, answer key, mark scheme, explanation, model answer, common mistake, next action, LO / syllabus binding |
| `AnswerKey` | Accepted variants, MCQ choice id, numeric tolerance |
| `MarkScheme` | Mark points + max marks (learner-facing) |
| `PracticeResponseType` | `mcq` · `numeric` · `short_structured` · `free_text` |
| `PracticeScoreResult` | Deterministic outcome + feedback payload |

CS1 commercial seed (`scoreable_seed.py`) covers high-traffic topics (cash flows, discounting / present value, equity method) plus a general fallback. `EducationalSubstancePlanner` attaches up to three scoreable practice items per sitting when planning package / mission-fact substance.

Answer keys remain **server-side only**. Learner opaque activity payloads never expose keys.

---

## Scoring Flow

```
Practice response
  → PackageActivityEngine.submit_response_opaque
  → score_practice_response(item, response)   # deterministic
  → feedback (Correct/Incorrect + artefacts)
  → ActivityService passes scored_correct / structured / score_payload
  → LearningSessionRuntimeEngine.record_response_opaque
  → EvidencePackageBuilder.observation_for_stage_response
```

| Response shape | Match rule | Evidence type |
|---|---|---|
| MCQ | Choice id or accepted label | EV-RT-40 (structured) or EV-RT-07/08 |
| Numeric | Float within tolerance | EV-RT-40 (structured) or EV-RT-07/08 |
| Short structured | Normalised exact / containment vs accepted variants | EV-RT-07 / EV-RT-08 |
| No key / empty | Unscored | EV-RT-06 / EV-RT-09 (unchanged Behavioural path) |

No opaque LLM grading on the core Educational+ path.

---

## Evidence Flow

```
Scored practice observation(s)
  → sitting Evidence Package (Generated)
  → EducationalEvidenceAuthority.validate_session_evidence_package
  → Accepted (Educational+) when EV-RT-07 / 08 / 40 present + Finish Yes
  → ProgressEngine (authorised columns) · StudentTwinEngine (Educational+ only)
```

| Change | Location |
|---|---|
| `scored_correct` / `structured` / `score_payload` | Additive kwargs on record path |
| EV-RT-07 / EV-RT-08 mapping | Existing builder (now fed by activity scoring) |
| EV-RT-40 | Builder when `structured=True` and scored |
| Authority / Twin / Progress math | **Unchanged** |

Demonstration (tests): scored commercial sitting → disposition **Accepted**, `may_update_twin=True`, mission completion + progress advancement authorised.

---

## Student Experience

After a scored practice attempt the Session activity surface shows:

| Element | Copy |
|---|---|
| Outcome | **Correct** / **Incorrect** |
| Why | Item explanation |
| Model answer | Authorised model answer |
| Common mistake | Shown on incorrect only |
| Next action | Calm continue guidance |

Presentation remains professional Session language (no Twin / Evidence Authority jargon). Unscored stages (Read / Worked example) keep behavioural coaching copy.

---

## Founder Metrics

Platform Intelligence (`/console/alpha-observability`) now includes **Educational+ yield**:

| Metric | Meaning |
|---|---|
| Educational+ rate | Share of sittings Accepted with Educational+ observations |
| Behavioural-only | Sittings without Educational+ practice outcomes |
| Learning Yield | Educational+ observations per Session |
| Educational vs Behavioural practice | Observation counts |
| Twin-updated / first Twin activation | Signals from package validation / twin status |
| Restricted / Rejected | Gate dispositions |

Computed by `EducationalYieldMetrics` from persisted Evidence Packages — read-only observability.

---

## Files Created

- `app/application/learning_session/scoreable_practice.py`
- `app/application/learning_session/scoreable_seed.py`
- `app/services/educational_yield_metrics.py`
- `tests/test_kwp004_assessable_practice.py`
- `KWP004_IMPLEMENTATION_REPORT.md`

## Files Modified

- `app/application/learning_session/educational_flow.py`
- `app/application/learning_session/substance_planner.py`
- `app/application/learning_session/evidence_package_builder.py`
- `app/infrastructure/adapters/learning_session/package_activity_engine.py`
- `app/infrastructure/adapters/learning_session/runtime_engine.py`
- `app/infrastructure/session/runtime_adapter.py`
- `app/infrastructure/session/store.py`
- `app/infrastructure/engines/opaque_bridges.py`
- `app/application/session_experience/ports/session_runtime_port.py`
- `app/application/session_experience/activity_service.py`
- `app/application/session_experience/dto/activity_snapshot.py`
- `app/application/session_experience/_snapshots.py`
- `app/domain/session_experience/activity_projection.py`
- `app/presentation/session/dto/study_session.py`
- `app/presentation/session/services/study_session_service.py`
- `app/presentation/session/view_models.py`
- `app/templates/session/partials/session_body.html`
- `app/founder/dashboard/routes.py`
- `app/founder/dashboard/templates/founder_dashboard/alpha_observability.html`
- `tests/application/session_experience/helpers.py`
- `tests/infrastructure/session/helpers.py`

**Not redesigned:** LearningSessionRuntime (additive kwargs only), EducationalEvidenceAuthority, StudentTwinEngine, ProgressEngine, Mission Runtime.

---

## Tests Added

`tests/test_kwp004_assessable_practice.py` — 13 tests covering:

- MCQ / numeric / short-structured deterministic scoring  
- Seed + planner scoreable practice emission  
- Builder EV-RT-07 / EV-RT-08 / EV-RT-40  
- Activity engine feedback payload  
- Commercial Session → **Accepted Educational+**  
- Student template feedback surface  
- Founder Learning Yield metrics  

### Tests Executed

```bash
python3 -m pytest tests/test_kwp004_assessable_practice.py \
  tests/test_lxp004a_session_substance.py \
  tests/test_ev001b_evidence_gate.py \
  tests/application/session_experience/test_services.py -q
```

**Result:** 58 passed.

```bash
python3 -m ruff check <changed modules>
```

**Result:** All checks passed.

---

## Student Impact Assessment

| Dimension | Assessment |
|---|---|
| **Student problem** | Sessions felt like checklists — practice without knowing if the answer was right; Insights stayed “building.” |
| **Student benefit** | Immediate Correct/Incorrect + model answer; Journey/Insights can thicken after real scored practice. |
| **Learning benefit** | Syllabus-bound assessable items; common-mistake guidance; deterministic, explainable scoring. |
| **Success metrics** | Educational+ accept rate; Learning Yield ≥ 1 scored observation per commercial sitting on seeded topics; Twin Active after first scored sitting (when Twin flag ON). |
| **Risks** | Thin seed corpus outside cash/discount/equity keywords falls back to general short item; free-text matching is bounded containment — not full open marking. |
| **Assumptions** | Commercial Loop + Evidence Gate remain ON; students complete practice and Finish Review Yes. |

---

## Commercial Readiness Assessment

| Domain | Effect |
|---|---|
| **CR3 Study loop reliability** | Daily Session can lawfully produce Accepted Educational+ — loop completes with understanding signals, not only participation. |
| **CR4 Explainability** | Correct/Incorrect + Why + Model Answer without engine jargon. |
| **Willingness-to-pay** | Correctness feedback and model answers — Phase 3/4 monetisation fuel from KWP-003. |
| **Residual** | Full CS1 L2+ coverage and Assessment Mode surfaces remain for later programmes; seed depth is pilot, not full syllabus bank. |

**Estimated CRI delta (provisional):** Positive on CR3/CR4 from Educational+ density; not a validated board update in this programme.

**Architecture compliance:** Curriculum V1/V2 traversal unchanged. Content remains syllabus-faithful. Evidence grades not inflated for Reading / Reflection / Finish Review.

---

## Migration Impact

**None** — no Alembic / schema changes. Scoring and evidence use existing session document store namespaces.

---

## Architecture Compliance

| Invariant | Stance |
|---|---|
| LearningSessionRuntime sole Session AUTHORITY | Preserved — additive scored kwargs only |
| EducationalEvidenceAuthority sole Evidence AUTHORITY | Unchanged — richer candidates |
| StudentTwinEngine | Unchanged — more Educational+ to observe |
| ProgressEngine | Unchanged — same authorisation columns |
| Mission Runtime | Unchanged |
| Blueprint | Outcomes before engagement; deterministic cores; not a question-bank identity |

---

## Technical Debt

- Seed matching is keyword-based; package artefact binding for certified item banks is the durable path.  
- Short-text scoring uses normalised containment — adequate for seed items, not full open-response marking.  
- Founder metrics scan in-process Evidence Packages; durable warehouse rollups may follow.  

## Known Limitations

- Not Assessment Mode chrome or Exam Briefing.  
- Not full CS1 L2+ corpus coverage.  
- Not mission assessment / mock (EV-RT-42/43).  
- Reading and worked examples remain Behavioural by EV-001A law.  

---

## Recommendation for KWP-005

### Name

**KWP-005 — Assessment Mode & Sitting Reports**

### Mandate

With Educational+ daily practice active, surface Stage B assessment pathways and student-facing Sitting Reports:

1. Topic Quick Check packs (5–8 scored items) composed via existing Mission / Session path.  
2. Sitting Report presentation over Accepted Educational+ history (plain language strengths / weaknesses).  
3. Expand CS1 seed → certified package artefact item banks.  
4. Keep authorities unchanged — consume denser Educational+ fuel.

### What KWP-005 is not

Not Exam Briefing marketing (candidate for KWP-006). Not Twin/Progress/Evidence redesign.

---

## Closing

KWP-003 diagnosed content starvation. KWP-004 feeds the loop: scoreable practice → deterministic scoring → EV-RT-07/08/40 → Accepted Educational+ → Progress / Twin / Insights finally receive understanding observations.

> Architecture complete. Assessable practice active. Feed Learning Insights.

---

**Document status:** Complete — KWP-004 implementation deliverable  
**Next programme:** KWP-005 Assessment Mode & Sitting Reports (recommended)  
**Architecture stance:** SR-001A authorities unchanged; Educational+ inputs enriched only  
