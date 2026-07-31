# MISSION-002 — Mission Briefing & Selection Coherence

**Programme:** MISSION-002 · SR-001A Phase P0  
**Date:** 2026-07-30  
**Nature:** P0 implementation — mission briefing trust  
**Authority:** SR-001 + SR-001A  
**Predecessor audits:** MISSION-001 · SLJ-001 · RCV-002  

---

## Executive Summary

MISSION-002 restores trust in the Mission Brief. Students now see **one coherent educational story**: mission title, explanation, curriculum position, why-today, and supporting evidence all reference the **same syllabus topic**, in **human educational language**, with **zero Educational Intelligence `node-…` identifiers** on student-facing surfaces.

Root causes closed from MISSION-001:

| Defect | Fix |
|---|---|
| CertifiedMissionEngine LO-density scoring jumped to §4.2 while progress stayed on §1.1 | Learning Mode selection: **next incomplete eligible topic in syllabus order**; LO density is a weak tie-break only; `preferred_topic_id` binds to progress current topic |
| Home “Why this mission” preferred journey timeliness (wrong topic) | `_why_now` prefers mission rationale; journey why-today aligned to mission topic |
| Publication used `code = node_id` in titles / rationale / evidence | Student-facing identity helpers + derivation / certifier / projection sanitisation |
| Rationale claimed “next incomplete” while selector used LO density | Selection now **is** syllabus-order; rationale is accurate |

**Out of scope (honoured):** Study Session, LearningSessionRuntime, Evidence pipeline, Student Digital Twin, Progress Engine architecture redesign, P1 Session binding, SR-002.

---

## Files Created

- `app/domain/educational_runtime_engine/student_facing_identity.py` — human syllabus codes + `node-` sanitisation
- `tests/test_mission002_briefing_coherence.py` — unit / integration / regression / acceptance suite
- `MISSION002_IMPLEMENTATION_REPORT.md` — this report

## Files Modified

### Selection & mission generation

- `app/application/curriculum_intelligence/certified_mission_engine.py`
- `app/application/educational_runtime_engine/service.py`

### Explanation & derivation

- `app/domain/educational_engine_foundation/derivation.py`
- `app/domain/educational_quality/rules.py`
- `app/application/educational_quality/certifier.py`

### Presentation / experience projection

- `app/application/educational_experience/service.py`
- `app/presentation/student/services/student_home_service.py`

### Publication (future packages)

- `app/application/curriculum_studio/structure_preparation_service.py`

### Config

- `app/application/config/v2_flags.py` — `SR_MISSION_BRIEF_COHERENCE` (default ON)

### Tests

- `tests/application/educational_experience/test_acceptance.py` — Home HTTP acceptance aligned to mission panel

---

## Architecture Compliance

- **Layering preserved:** selection remains in `curriculum_intelligence`; mission instantiation in `educational_runtime_engine`; presentation projection in `educational_experience` + student VMs; no routes contain selection math.
- **Curriculum V1/V2:** unchanged loadability; published CS1 path is the primary coherence surface.
- **Progress Engine architecture:** `derive_progress` logic untouched; presentation half of **G-Progress** satisfied (mission ≡ position ≡ why-now). Full engine singularity remains **P6**.
- **Not modified:** LearningSessionRuntime, Evidence Authority, Twin, Study Session HTTP spine.
- **No schema / Alembic migrations.**

---

## Tests Added

| Layer | Coverage |
|---|---|
| **Unit** | Syllabus-code extraction; sanitisation; CertifiedMissionEngine selects syllabus head (not LO-dense 4.2); preferred topic; post-completion advance; derivation human titles; explanation evidence excludes node ids; Home `_why_now` prefers mission rationale |
| **Integration** | enrol → `generate_daily_mission` → EducationalExperience → Home VM; mission ≡ progress ≡ why-now; mid-progress coherence |
| **Regression** | Empty-stream `derive_progress` unchanged; EI-002B human-code fixture still selects first topic; Runtime C / EQ-001 / CS04–CS08 suites green |
| **Acceptance** | Educational VM single-topic story; Home HTTP shows coherent mission language and no `node-` |

**Command (P0 regression slice):**

```bash
python3 -m pytest \
  tests/test_mission002_briefing_coherence.py \
  tests/application/curriculum_intelligence/test_ei002b_student_intelligence.py \
  tests/domain/educational_quality/test_rules.py \
  tests/application/educational_experience/test_acceptance.py \
  tests/application/educational_runtime_engine/test_integration.py \
  tests/certification/test_eq001_educational_quality.py \
  tests/certification/test_cs04_to_cs08_runtime.py \
  -q
```

**Result:** **63 passed** (2026-07-30).

---

## Evidence

### Before (MISSION-001 / RCV-002)

```text
title:     Study node-1f3e467797c40a23 — 4.2 Understand and use generalised linear models
position:  1.1 Data Analysis
why_now:   Today's topic is 1.1 … (journey timeliness)
rationale: "next incomplete topic in syllabus order"  ← false for LO-density pick
```

### After (MISSION-002 fixtures)

```text
title:     Study 1.1 — Data Analysis
position:  1.1 Data Analysis
why_now:   Today focuses on 1.1 — Data Analysis because it is the next incomplete…
rationale: accurate — selection IS syllabus-order Learning Mode
evidence:  no node-* substrings
```

Automated reproduction: `tests/test_mission002_briefing_coherence.py` (`_mission001_package` with 5 vs 10 LOs).

---

## Before/After Comparison

| Field | Before | After |
|---|---|---|
| Mission topic (empty progress) | 4.2 (LO density) | 1.1 (syllabus head) |
| Curriculum position | 1.1 | 1.1 (= mission) |
| Home why-now | 1.1 via journey (label: “Why this mission”) | Mission rationale for 1.1 |
| Mission title code | `node-…` | Human syllabus code (`1.1`) |
| Supporting evidence | Topic + objective node ids | Human codes / educational text only |
| Selection claim | False “syllabus order” | True syllabus-order Learning Mode |

---

## Remaining Risks

| ID | Risk | Mitigation |
|---|---|---|
| R-H2 residual | Existing in-flight mission rows may still store node-id titles until re-read | Snapshot / experience projection re-humanises on read |
| R-M1 residual | Empty published `prerequisite_ids` still make every topic “eligible” | Selection order fixed; full prerequisite projection remains MP-003 / later |
| P6 | Engine-level progress singularity not done | Presentation half of G-Progress only; P6 owns full merge |
| Flag | `SR_MISSION_BRIEF_COHERENCE` documents cutover; behaviour is unconditional correctness | Emergency rollback = revert PR (flag is soft documentation) |
| Home markers | Legacy `data-edu-field` strip no longer on Home (pre-existing DX drift) | Acceptance updated to mission panel; Journey strip may still vary |

---

## P0 Exit Criteria

| Criterion | Status |
|---|---|
| Mission topic ≡ progress current topic ≡ Home why-now (empty + mid progress) | **Met** (tests) |
| Zero `node-` in Home mission title, why-now, LO labels on production path | **Met** (tests + sanitisation) |
| MISSION-001 reproduction regression green | **Met** |
| G-Progress *presentation half* for published path | **Met** |
| No P1 Session binding / LSR / Evidence / Twin changes | **Met** |

---

## Recommendation for P1 Readiness

**P0 exit criteria are satisfied. P1 (SR-002 / SR-002a — Session spine binding) may proceed** behind `SR_SESSION_PRIMARY`, subject to:

1. LearningSessionRuntime persistence story ready (SR-001A R-D1 / R-L4).  
2. Do **not** enable production Start Session Primary until P0 remains green on dogfood with the live CS1 package.  
3. Keep Mark-complete as non-product Primary until G-Session.  
4. Do **not** begin SR-002 substance/evidence/Twin work in the same unflagged release.

**Authorised next programme:** SR-002 / SR-002a (P1) — bind Home Primary → `/session/*` → LearningSessionRuntime.

---

## Migration Impact

**None** (no Alembic revisions; additive presentation/selection behaviour only).

## Technical Debt

- Prerequisite edges still empty at publication (MP-003 deferred).  
- Full Progress singularity deferred to P6.  
- Soft flag does not dual-path old LO-density behaviour (intentional — defect, not feature).

## Known Limitations

- Does not bind Study Session or change completion Primary.  
- Does not restore real prerequisite graph into published packages.  
- Does not republish production packages; live packages benefit via derivation + presentation sanitisation without republish.

---

**End of MISSION-002.**
