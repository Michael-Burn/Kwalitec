# MISSION-001 — Student Mission Engine & Presentation Audit

**Programme:** MISSION-001 · Student Mission Engine & Presentation Audit  
**Date:** 2026-07-30  
**Scope:** Evidence-only investigation (no fixes, no redesign, no code changes)  
**Method:** Static pipeline trace + live reproduction against the post–RCV-002 CS1 certified package (5 / 15 / 73)  
**Predecessor:** RCV-002 production curriculum recovery (Begin Learning now works)

---

## Executive Summary

Begin Learning succeeds against the certified published package. The first Daily Mission is **not** a coherent V2 educational presentation. Four independent defects compose the observed student experience:

| Observed symptom | Exact cause |
|---|---|
| Mission title shows `node-…` IDs | Publication projects Educational Intelligence `node_id` into package `code`; mission title template is `Study {code} — {title}` |
| Mission topic ≠ “Why this mission” topic | **Two selectors:** `CertifiedMissionEngine` picks **4.2** (max uncovered LOs); progress/journey explanation uses **1.1** (first incomplete). Home `why_now` prefers journey timeliness over mission rationale |
| “Next incomplete topic” with no declared progress | Correct for empty event stream — but the **mission** is not that topic; rationale text **claims** syllabus-order selection while EI-002B scored by LO count |
| Runtime objects leak into UI | Node IDs in titles, rationale, supporting evidence, learning-objective labels; presentation projects raw runtime DTOs |

**Verdict:** Runtime C curriculum authority and artefact derivation are active and load the certified package. The mission engine is **not** fully coherent V2 Educational Intelligence for students: selection, explanation, and presentation diverge, and legacy Runtime A remains the coexistence default for non-enrolled / Preferred-Authority paths.

**Production evidence (RCV-002 STEP 6):**

```text
mission_instance_id: msn_fc1413d58f8441a8b258e07549a44695
topic_id:            node-1f3e467797c40a23
title:               Study node-1f3e467797c40a23 — 4.2 Understand and use generalised linear models
```

Source: `knowledge/evidence/releases/RCV002/step6_begin_learning.json`

**Live reproduction (local post-recovery package, empty progress):** same pattern — mission = **4.2 GLM** (`node-8185f5267169ea7d`, 10 LOs); curriculum position / journey “why today” = **1.1 Data Analysis** (`node-f6efa6549c1cb033`); Home `why_now` winner = journey timeliness (1.1).

---

## Mission Generation Pipeline

```
PublishedCurriculumPackage (DB, is_active)
  → PublishedCurriculumAuthority.get_active("CS1")
  → EducationalArtefactDeriver.derive(package)
  → EducationalRuntimeEngineService.enrol_student / _instantiate_study_plan
  → derive_progress(events=∅) → current_topic = first incomplete (1.1)
  → generate_daily_mission()
       ├─ _select_certified_mission() → CertifiedMissionEngine.generate()
       │     score = uncovered_LOs×10 − display_order×0.01
       │     → selects 4.2 (10 LOs) over 1.1 (5 LOs)
       │     because structure.topics[*].prerequisite_ids = [] always
       └─ else fallback: progress.current_topic_id (1.1)
  → RuntimeMissionInstance(title=template.title, topic_code=template.topic_code)
  → EducationalExperienceService.load_for_user(ensure_mission=True)
  → presentation VMs → StudentHomeService → ds_mission_panel
```

### Key decision points

1. **Curriculum authority** — certified package only when `certification.authority` / status accepted (`authority.py` `_runtime_accepts`).
2. **Topic for mission** — EI-002B certified selector **overrides** progress current topic when certification block present.
3. **Topic for “position / why today”** — always from `derive_progress().current_topic_id` (syllabus order + empty prereqs ⇒ first topic).
4. **Home “Why this mission”** — `StudentHomeService._why_now` prefers `explanation.timeliness_line` (= journey why-today = **1.1**) over mission `why_recommended` (= **4.2**).

---

## Presentation Pipeline

```
EducationalExperienceService._project()
  → CurriculumPositionSnapshot  ← progress.current_topic_id  (1.1)
  → MissionEducationSnapshot    ← mission instance + quality envelope (4.2)
  → JourneyEducationSnapshot    ← get_journey_explanation → build_journey_explanation (1.1)

educational_vm()
  → today_topic_title = position (1.1)
  → mission_title     = mission.title (4.2 + node id)
  → why_this_mission  = mission explanation (4.2 + node ids)
  → why_today         = journey (1.1 + node id)

_home_from_educational()
  → ExplanationViewModel.timeliness_line = edu.why_today (1.1)
  → ExplanationViewModel.why_recommended = mission why (4.2)
  → recommendation.title = mission title (4.2)

StudentHomeService._why_now()
  → prefers timeliness_line → student sees 1.1 under “Why this mission”

student/home.html → ds_mission_panel(title, objective, why_now, …)
```

---

## Progress Engine Analysis

### Runtime C (active for enrolled Begin Learning students)

| Question | Evidence |
|---|---|
| How is study position established? | Event-sourced `derive_progress(progress_model, events)` in `app/domain/educational_runtime_engine/progress.py` |
| What exists for a brand-new student? | No `TOPIC_COMPLETED` events → `completed_topic_ids=()`, `incomplete_topic_ids=all 15 topics`, `coverage_ratio=0.0` |
| How is “next incomplete” calculated? | First topic in published `progress_model.topic_ids` whose `prerequisite_ids` are all in completed; if none, first incomplete |
| Assumption | **Zero completion** ⇒ start at syllabus head. **Also:** published package ships `prerequisite_ids: []` for every topic (`structure_preparation_service.py` lines 198–209), so every topic is “prereq-ready” |

### Critical inconsistency

Progress correctly concludes **1.1** is current.  
`generate_daily_mission` then **ignores** that conclusion when CertifiedMissionEngine returns a different topic.  
Rationale strings still say *“because it is the next incomplete topic in syllabus order”* — which is **false** for the selected 4.2 mission.

### Runtime A (legacy, still present)

`CurriculumService.get_next_incomplete_topic` walks DB leaf topics via `TopicProgress`. Used by `PlanningService.generate_today_mission` for students **not** on Runtime C. Not the path that produced the RCV-002 mission, but still active in coexistence.

---

## Legacy Runtime Analysis

| Component | Status for Begin Learning / Runtime C enrollee | Still in codebase / student paths? |
|---|---|---|
| `PublishedCurriculumAuthority` + Runtime C | **Active authority** for enrolled CS1 after RCV-002 | Yes |
| `EducationalArtefactDeriver` | Active | Yes |
| `CertifiedMissionEngine` (EI-002B) | Active override on certified packages | Yes |
| `PlanningService.generate_today_mission` | Not used when Runtime C page succeeds | Yes — Runtime A default / fallback |
| `CurriculumService.get_next_incomplete_topic` | Not used on Runtime C mission path | Yes — Runtime A missions + recommendations |
| `RecommendationService` / ILE-004 Daily Mission Intelligence | Bypassed when Runtime C educational page loads | Yes — Home overlay when RI-001 Preferred Authority available or no Runtime C enrolment |
| Bundled JSON V1/V2 import (`CurriculumService.import_curricula`) | Parallel syllabus store; not the certified package | Yes — startup still imports IFoA CS1/CM1/CB2 JSON |
| `RuntimeCoexistencePolicy.json_runtime_remains_default()` | Returns **True** — Runtime A remains default until cutover | Yes |
| RI-001 Preferred Authority gate | If SCI/educational decisions exist, `_try_runtime_c_page` returns `None` → Runtime A Home | Yes (`views.py`) |

**Conclusion:** Legacy Runtime A is **not deleted** and remains the **default** student path. Runtime C is an enrolment-gated overlay. For the observed Begin Learning mission, generation was Runtime C + EI-002B — but presentation still mixes journey (progress) and mission (certified selector), and coexistence policy still treats JSON Runtime A as default.

**Is the mission engine fully V2?**  
**No.** Certified package counts are V2-shaped (5/15/73), but:

- Student-facing codes are EI node IDs, not syllabus codes  
- Prerequisites are stripped at publication  
- Selection is LO-count scoring, not Constitution / Registry Learning Mode (next incomplete unit)  
- Dual runtimes remain active  

---

## Mission Consistency Matrix

Live reproduction (empty progress, certified CS1 package):

| Displayed field | Educational artefact referenced | Same as mission topic? |
|---|---|---|
| Mission title | 4.2 GLM + `node-8185…` as “code” | — (mission) |
| Mission `topic_id` / `topic_code` | 4.2 node | Yes |
| Curriculum position / “Today’s topic” | **1.1** Data Analysis | **No** |
| Why this mission (mission envelope) | 4.2 + node IDs in text + LO node IDs | Same topic, wrong *reason text* (“syllabus order”) |
| Why this mission (Home `why_now`) | **1.1** via journey timeliness | **No** |
| Supporting evidence | Topic + objective **node IDs** | Same topic, internal IDs |
| Expected outcome / benefit | 4.2 first-pass wording | Same topic |
| Estimated duration | Template minutes for 4.2 (e.g. 250) | Same topic |
| Progress / coverage | 0% / position on **1.1** | Progress artefact ≠ mission |
| Journey “what unlocks next” | Relative to **1.1** current | **No** |

**Rule violated:** “No field may come from an unrelated lookup.” Mission card aggregates **at least two** educational artefacts (mission topic vs progress current topic).

---

## Educational Artefact Trace

### STEP 1 — Curriculum Authority

| Check | Result | Evidence |
|---|---|---|
| Active package only | Pass | `PublishedCurriculumAuthority.get_active` filters `is_active=True` |
| Certified | Pass | `authority=certified_snapshot`, `CERTIFIED_WITH_WARNINGS` |
| 5 / 15 / 73 | Pass | Live package + RCV-002 `after_active_package.json` / `step6_begin_learning.json` |
| No legacy V1 traversal in this load | Pass for authority path | Deriver reads published `structure`; does not call `CurriculumService` |
| Draft unreachable | Pass | `is_draft_reachable` always False |

**Gap:** Authority does not validate educational *presentation* quality (human codes, prerequisites). Counts-only gate lives in the deriver (non-empty sections/topics/objectives).

### STEP 2 — Progress (new student)

```
events = []
→ completed = ∅
→ incomplete = all progress_model.topic_ids (published order)
→ current = first with prereqs ⊆ completed
→ package prereqs all [] ⇒ current = first topic = 1.1
```

No diagnostic, no declared prior study, no TopicProgress rows on this path. “Next incomplete” is an **assumption of syllabus start**, not student-declared progress.

### STEP 3 — Mission generator (`generate_daily_mission`)

| Field | Value (live reproduction) |
|---|---|
| Section | Parent of 4.2 (section node id) |
| Topic | `node-8185f5267169ea7d` — title `4.2 Understand and use generalised linear models` |
| Objectives | 10 certified LO node ids |
| Snapshot / generation | Package cert `snap-b8a3d3ea939763d5` / chain `ei-chain-ws-cs1` (RCV-002); selection reasons include `next_uncovered_objective`, `prerequisite_ready`, `progress_advance` |
| Why 4.2 wins | `score += len(uncovered)*10`; 4.2 has 10 LOs vs 1.1’s 5; all topics prereq-empty |

RCV-002 production used a prior snap’s equivalent 4.2 node (`node-1f3e467797c40a23`) — same selection class.

### STEP 4 — Mission explanation

| Layer | Source artefact | Text |
|---|---|---|
| Template `educational_rationale` | Mission topic at derivation | “Today focuses on {code} — {title} because it is the **next incomplete topic in syllabus order**” |
| EQ-001 `build_mission_explanation` | Same | Embeds `topic_id` in supporting evidence |
| Journey `build_journey_explanation` | **Progress current topic** | Independent lookup → 1.1 |
| Home `why_now` | Prefers journey timeliness | Surfaces 1.1 to student |

**Divergence:** Explanation pipeline performs an **independent journey lookup** and the presentation layer **promotes it over** the mission envelope for the mission card’s “Why this mission” line.

### STEP 5 — Presentation fields (mission card)

| UI field | Source | Transformation | Purpose | Student value | Leakage |
|---|---|---|---|---|---|
| Title | `mission.title` ← `Study {code} — {title}` | Direct | Name today’s work | High if human code | **EI node id as code** |
| Subject line | `examination_label` / fallbacks | Concat subject | Context | Medium | Low |
| Learning objective | Often mission/recommendation title | Fallback chain | Objective clarity | High when real LO text | Often duplicates title; LO codes are node ids in evidence |
| Why this mission | `_why_now` → timeliness first | Truncate 140 | Motivate selection | High | **Wrong topic** + node id |
| Expected outcome | `expected_benefit` / suggested next | Truncate 140 | Motivation | Medium | Weak / generic |
| Duration | Quality / template minutes | Label | Timebox | Medium | Can be inflated (e.g. 250 min) |
| Difficulty | Often empty / feasibility misuse | Optional | Calibration | Low when missing | — |
| Progress signals | Coverage from progress | % | Orientation | High | Anchored to 1.1 while mission is 4.2 |
| Supporting evidence (details) | EQ-001 evidence list | Raw strings | Explainability | Low as shipped | **Node IDs everywhere** |

---

## UI Leakage Analysis

| Leak | Where introduced | Where shown |
|---|---|---|
| `node-{hex}` as topic **code** | `StructurePreparationService.structure_dict`: `"code": tid` | Mission title, rationale, evidence |
| `node-{hex}` as objective **code** | Same: `"code": oid` | Rationale objective clause; evidence list; LO labels when text missing |
| Topic id duplicated in evidence | `build_mission_explanation`: `Published topic {code} ({topic_id})` | Explainability details |
| Journey text embeds node id | `build_journey_explanation`: `code = current_topic_code or current_topic_id` | Why today / why_now |
| Internal mission instance ids | Runtime persistence | Not primary card title; present in forms (`mission_id`) |
| False educational claim | Rationale always says “syllabus order” | Mission why / envelope even when EI-002B scored by LO density |

Students should never see Educational Intelligence identifiers. They currently do in the primary mission title.

Root publication line:

```198:209:app/application/curriculum_studio/structure_preparation_service.py
        topics = [
            {
                "topic_id": tid,
                "code": tid,
                "title": title,
                ...
                "prerequisite_ids": [],
            }
            for idx, (tid, title) in enumerate(prepared.topic_titles)
        ]
```

---

## Architecture Assessment

### Boundaries (intended)

```
Templates → Blueprints → Services/Application → Domain → Models/DB/JSON
Educational Intelligence (Founder)  ≠  Student Runtime  ≠  Presentation
```

### Violations / coupling

| Issue | Detail |
|---|---|
| EI identifiers in student package | Publication structure uses node ids as student-facing `code` |
| Dual educational authorities on one card | Mission generator (CertifiedMissionEngine) vs progress/journey explanation without a single Mission Presentation Model |
| Presentation mixes layers | Home `why_now` priority encodes product policy over educational consistency |
| Coexistence incomplete | Runtime A services remain default; RI-001 can silently skip Runtime C UI |
| Prerequisites discarded | Domain graph / EI prereqs not projected into published structure → EQ-M07 gate and “prereq ready” are vacuously true |
| Explanation lies about policy | EQ-001 rationale hard-codes Learning Mode syllabus-order language while EI-002B uses coverage scoring |

Presentation is not a pure projection of one educational artefact; it recombines independent runtime objects.

---

## Premium UX Assessment

Evaluated against product vision (student should know what to study, why, and what “done” means — without developer concepts).

| Criterion | Assessment |
|---|---|
| Helps a student learn | Partially — names a real syllabus topic (4.2) but undermines trust by contradicting “why” |
| Technical language | Fail — `node-…` identifiers |
| Developer / EI terminology | Fail — node ids, objective id lists |
| Weak explanations | Fail — claims “next incomplete” while jumping to §4; Home why points at §1.1 |
| Missing educational guidance | Fail — no human syllabus codes (e.g. `4.2`); LO text often displaced by ids in evidence |
| Missing motivation / context | Weak — generic first-pass benefit; duration may be unrealistic |
| Missing study personalisation | Fail for first mission — no use of diagnostic, availability calendar, or prior mastery beyond empty events |
| Premium trust | Fail — inconsistent card reads as unfinished internal tooling |

---

## Personalisation (STEP 7)

| Signal | Known on first mission? | Used in selection? |
|---|---|---|
| Exam date | Optional on `enrol_student`; may be set via study-plan wizard / bridge | Pacing projection only — **not** CertifiedMissionEngine score |
| Study schedule / availability | Wizard exists on Runtime A study-plan path | **Not** consumed by Runtime C mission selector |
| Previous progress | Empty event stream for new enrollee | Treated as zero coverage |
| Diagnostic assessment | Not on this path | No |
| Curriculum position | Inferred as first incomplete (1.1) | Used for plan pointer / journey; **overridden** for mission topic |
| Difficulty preference | Empty string default | Optional; calibration bias only if embedded in package |
| Calibration | May be embedded in package structure | Affects score if present; does not restore syllabus order |

**Assumptions flagged:**

1. Student starts at syllabus beginning (no declaration).  
2. Empty prerequisites ⇒ every topic eligible.  
3. More uncovered LOs ⇒ better first mission (contradicts Learning Mode registry).  
4. “Next incomplete in syllabus order” is an acceptable explanation even when selection was not that.  
5. Journey current topic may safely differ from today’s mission on the same card.

---

## Recommended Corrective Programmes

Evidence-only recommendations — **do not implement under MISSION-001**.

| ID | Programme | Purpose | Addresses |
|---|---|---|---|
| **MP-001** | Mission Presentation Model | Single educational artefact → student card fields; forbid mixed lookups | Dual-topic card, UI leakage |
| **MP-002** | Human Syllabus Identity Projection | Publish stable syllabus `code`/`number` (e.g. `4.2`), never EI `node_id`, as student-facing code; map node ids only internally | Node IDs in titles |
| **MP-003** | Prerequisite Projection Repair | Materialise real prerequisite edges into published structure (stop hard-coding `[]`) | Illegal early §4 missions; vacuous EQ-M07 |
| **MP-004** | Learning Mode Selection Alignment | First-pass Daily Mission = next incomplete eligible topic (Constitution / Registry); LO-density scoring only where product law allows (or rename/explain honestly) | False “syllabus order” claim; 4.2-first |
| **MP-005** | Explanation Consistency Gate | Mission why / evidence / journey why_today must reference `mission.topic_id`; fail quality cert if mismatch | Why-this-mission divergence |
| **MP-006** | Student Runtime Cutover / Sole Authority | Retire or hard-gate Runtime A Home for subjects with active published packages; clarify RI-001 vs Runtime C | Legacy coexistence risk |
| **MP-007** | New-Student Onboarding Honesty | Explicit starting position, optional progress declaration / diagnostic before claiming “next incomplete” | Progress assumption |
| **MP-008** | Premium Mission UX Pass | Duration realism, LO human text, motivation, done-when, no internal ids in any student string | Premium standard |

Suggested sequence: **MP-002 + MP-003** (data truth) → **MP-004 + MP-005** (selection + explanation) → **MP-001 + MP-008** (presentation) → **MP-006 / MP-007** (runtime & onboarding).

---

## Trace Evidence Index

| Claim | Artefact / location |
|---|---|
| RCV-002 first mission title with node id + 4.2 | `knowledge/evidence/releases/RCV002/step6_begin_learning.json` |
| Package 5/15/73 certified | `knowledge/evidence/releases/RCV002/after_active_package.json` |
| `code: tid`, empty prereqs at publish | `app/application/curriculum_studio/structure_preparation_service.py` ~198–209 |
| Title template uses code | `app/domain/educational_engine_foundation/derivation.py` `_mission_template_for_topic` |
| Certified override in generate | `app/application/educational_runtime_engine/service.py` `generate_daily_mission` + `_select_certified_mission` |
| LO-count scoring | `app/application/curriculum_intelligence/certified_mission_engine.py` |
| Progress first incomplete | `app/domain/educational_runtime_engine/progress.py` |
| “Syllabus order” rationale | `app/domain/educational_quality/rules.py` `build_mission_educational_rationale` |
| Journey independent why-today | `app/domain/educational_quality/rules.py` `build_journey_explanation` |
| Home prefers timeliness | `app/presentation/student/services/student_home_service.py` `_why_now` |
| Position vs mission in VM | `app/presentation/student/educational_view_models.py` `educational_vm` / `_home_from_educational` |
| Runtime A remains default | `app/application/educational_runtime_engine/coexistence.py` |
| Live dual-topic reproduction | Local certified package: mission 4.2 vs position/why_now 1.1 (`DIVERGENCE? True`) |

---

## Success Criteria Checklist

| Criterion | Answer |
|---|---|
| Why node IDs appear | Publication sets `code = node_id`; mission title / rationale interpolate `code` |
| Why two different topics appear | CertifiedMissionEngine selects 4.2; progress/journey + Home `why_now` surface 1.1 |
| How progress was inferred | Empty event stream ⇒ first incomplete in published order (prereqs empty) |
| Whether legacy runtime remains active | Yes — Runtime A is still default coexistence path; Runtime C is enrolment-gated |
| Whether mission engine is fully V2 | No — certified package load is V2-shaped, but selection/explanation/presentation are not a coherent V2 student system |
| Programmes required for premium standard | MP-001 … MP-008 above |

---

## Migration Impact

None (audit only — no schema or application changes).

## Architecture Compliance

Audit only. Documents that Runtime C respects PublishedCurriculumAuthority for package load, but student presentation and EI-002B selection currently violate educational consistency invariants expected of a production Student Runtime.

## Technical Debt (observed, not introduced by this audit)

- Dual mission authorities without a unifying presentation contract  
- Stripped prerequisites at structure projection  
- Hard-coded syllabus-order copy over LO-scoring selection  
- Coexistence default still Runtime A  

## Known Limitations

- Production node id for 4.2 in RCV-002 evidence (`node-1f3e467797c40a23`) differs from the local package’s 4.2 id (`node-8185f5267169ea7d`) after recertification — same defect class, not the same snap bytes.  
- This audit did not capture live production HTML screenshots; card field mapping is from code + local reproduction.  
- No application code was modified.
