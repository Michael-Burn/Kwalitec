# EA-003 — Mission Schema

**Programme:** Educational Excellence Programme EA-003  
**Status:** Binding — permanent Mission authoring-pack schema  
**Effective:** 2026-08-01  
**Parent:** `EA003_MISSION_BLUEPRINT.md`  
**Related:** `EA001_MISSION_PHILOSOPHY.md` · Gate MG · AF-MS · `EA002_CERTIFICATION_WORKFLOW.md`  
**Nature:** Structural specification for Mission packs — not live content, not application code  

---

## 1. Purpose

Define the complete field schema every Mission authoring pack must satisfy so authors, reviewers, and certifiers share one structure.

This schema is the **contract** between:

- Educational authors  
- Educational / Tutor reviewers  
- Quality Gate / Publication Approvers  
- Future composition engines (when built — out of scope for EA-003)

Schema validity is **necessary but not sufficient**. Educational PASS still requires Gate MG, Tutor Intent quality, and rubric threshold (`EA003_MISSION_SCORING_RUBRIC.md`).

---

## 2. Schema identity

| Property | Value |
|----------|-------|
| Schema name | `kwalitec.mission.blueprint` |
| Schema version | `1.0.0` |
| Programme | EA-003 |
| Artefact class | Mission (AF-MS) |
| Encoding | Logical fields (YAML/JSON/markdown pack equivalent) — storage format not mandated by EA-003 |

---

## 3. Pack structure

```text
MissionAuthoringPack
├── identity          (publication + topic identity)
├── blueprint         (educational specification fields)
├── continuity        (yesterday / today / tomorrow)
├── execution         (Session link, time, load)
├── evidence_hooks    (revision signals, Twin assumptions)
├── quality           (self-checks, prohibited-pattern denials)
└── certification     (review outcomes — filled during certification)
```

---

## 4. Field catalogue

### 4.1 Identity block

| Field ID | Type | Required | Constraint |
|----------|------|----------|------------|
| `mission_id` | string | Yes | Stable unique ID within subject package |
| `schema_version` | string | Yes | Must be `1.0.0` for EA-003 packs |
| `subject_id` | string | Yes | e.g. CS1 |
| `package_version` | string | Yes | Curriculum / educational package version |
| `topic_code` | string | Yes | Official syllabus node; no contaminants |
| `topic_title` | string | Yes | Accurate human title |
| `mode` | enum | Yes | `learning` \| `revision` |
| `display_title` | string | Yes | Student-facing Mission title; **≠** syllabus heading alone preferred; must not equal `learning_objective` |
| `author_id` | string | Yes | Author identity |
| `created_at` | datetime | Yes | ISO-8601 |
| `updated_at` | datetime | Yes | ISO-8601 |
| `cmp_edition` | string | Yes | Pinned CMP edition/version for loci |
| `status` | enum | Yes | `draft` \| `in_review` \| `certified` \| `published` \| `retired` \| `hold` |

### 4.2 Blueprint block (permanent specification)

| Field ID | Type | Required | Notes |
|----------|------|----------|-------|
| `mission_purpose` | text | Yes | ≤280 chars preferred |
| `educational_intent` | text | Yes | Cognitive move + intended learning change |
| `tutor_intent` | text | Yes | **Mandatory.** Tutor coaching move; must be Mission-unique |
| `learning_objective` | text | Yes | Actionable verb; ≤160 chars preferred; ≠ syllabus heading; ≠ `display_title` |
| `cmp_reading_scope` | object | Yes | See §5.1 |
| `syllabus_coverage` | object | Yes | See §5.2 |
| `prerequisite_knowledge` | list[text] | Yes | ≥1 item or explicit cold-start statement |
| `concept_focus` | text | Yes | Single-day conceptual centre |
| `common_misconceptions` | list[object] | Yes | 1–3 items; see §5.3 |
| `study_strategy` | object | Yes | See §5.4 |
| `reflection_goal` | text | Yes | Topic-specific residual harvest |
| `success_criteria` | list[text] | Yes | 1–3 assessable criteria |
| `tomorrow_bridge` | object | Yes | See §5.5 |
| `estimated_cognitive_load` | enum | Yes | `light` \| `moderate` \| `heavy` \| `very_heavy` |
| `cognitive_load_rationale` | text | Yes | One-line justification |
| `estimated_study_time_minutes` | object | Yes | `{min, max}` positive integers; max ≥ min |
| `revision_signals` | list[object] | Yes | May be empty list only with `revision_signals_note` |
| `revision_signals_note` | text | Conditional | Required if `revision_signals` empty |
| `why_now` | text | Yes | Specific educational reason; must not be reusable boilerplate |
| `expected_benefit` | text | Yes | Plain educational benefit (skill / coverage step / evidence) |
| `explainability` | text | Yes | Specific prior topic, prerequisite, or exam-skill gap; Mission-unique |

### 4.3 Continuity block

| Field ID | Type | Required | Notes |
|----------|------|----------|-------|
| `prior_bridge` | text | Yes | “Yesterday… Today…” or lawful cold-start bridge |
| `prior_mission_id` | string | Conditional | Required when prior Mission exists |
| `prior_topic_code` | string | Conditional | Required when prior topic exists |
| `cold_start` | boolean | Yes | `true` if no prior Mission history |
| `continuity_bundle_complete` | boolean | Yes | Author assertion; reviewer verifies |

### 4.4 Execution / dependencies block

| Field ID | Type | Required | Notes |
|----------|------|----------|-------|
| `session_intent` | list[string] | Yes | Ordered stage names matching real Episodes |
| `linked_session_id` | string | Yes* | *Required before certification/publication; may be draft-linked during early authoring |
| `linked_episode_ids` | list[string] | Yes* | Same rule as session |
| `dependencies` | object | Yes | See §5.6 |
| `unavailable_state` | object | Conditional | If Mission shown without Session: honest unavailable copy + reason |

### 4.5 Quality self-check block

| Field ID | Type | Required | Notes |
|----------|------|----------|-------|
| `voice_self_check` | boolean | Yes | Conforms to Tutor Voice Guide |
| `style_self_check` | boolean | Yes | Conforms to Educational Style Guide |
| `prohibited_patterns_denied` | list[string] | Yes | Explicit denial of P1–P12 IDs |
| `principle_citations` | list[string] | Yes | EP-01–EP-10 IDs designed to satisfy |
| `ev001_regression_denied` | list[string] | Yes | TB classes checked (e.g. TB-002, TB-004) |

### 4.6 Certification block (filled in review)

| Field ID | Type | Required at publish | Notes |
|----------|------|---------------------|-------|
| `educational_review` | object | Yes | Result, reviewer_id, date, notes |
| `tutor_review` | object | Yes | Result, reviewer_id, date, notes |
| `gate_mg` | object | Yes | Per-criterion PASS/FAIL |
| `rubric_scores` | object | Yes | Dimension scores + overall |
| `certification_status` | enum | Yes | `pass` \| `fail` \| `hold` |
| `publication_approval` | object | Conditional | Required for `status=published` |
| `certification_evidence_uri` | string | Yes | Path/ref to evidence pack |

---

## 5. Nested object shapes

### 5.1 `cmp_reading_scope`

```text
cmp_reading_scope:
  open_point: string          # e.g. "CMP §4.2 GLM setup"
  stop_condition: string      # e.g. "through first worked example"
  out_of_scope_today: string  # what not to read
  materials_authority: enum   # cmp | authorised_notes | past_paper
```

### 5.2 `syllabus_coverage`

```text
syllabus_coverage:
  topic_code: string
  topic_title: string
  coverage_claim: string      # honest progress language
  first_pass: boolean
  weight_cue: string | null   # exam weight note when known
```

### 5.3 `common_misconceptions[]`

```text
common_misconceptions[]:
  statement: string
  corrective_move: string     # how study strategy addresses it
```

### 5.4 `study_strategy`

```text
study_strategy:
  method_summary: string      # leverage move in tutor language
  session_structure: list[string]
  active_demands: list[string]  # note | recall | solve | justify
```

### 5.5 `tomorrow_bridge`

```text
tomorrow_bridge:
  known: boolean
  next_topic_code: string | null
  next_topic_title: string | null
  continuity_line: string     # educational bridge or honest absence
  light_prep_cue: string | null
```

### 5.6 `dependencies`

```text
dependencies:
  prior_topic_or_cold_start: string
  linked_session_id: string | null
  linked_episode_ids: list[string]
  curriculum_package_version: string
  cmp_edition: string
  twin_inputs_assumed: list[string]  # may be empty
```

### 5.7 Review result object

```text
*_review / gate_mg / publication_approval:
  result: pass | fail | hold
  reviewer_id: string
  reviewed_at: datetime
  notes: string
  hold_expiry: datetime | null
```

---

## 6. Validation rules (machine-assistable)

These rules may be automated as pre-fail detectors later; human PASS remains mandatory for Tutor Intent and voice.

| ID | Rule | Severity |
|----|------|----------|
| SV-01 | All Required fields present and non-empty | Block |
| SV-02 | `learning_objective` ≠ `topic_title` and ≠ syllabus heading string | Block |
| SV-03 | `learning_objective` ≠ `display_title` | Block |
| SV-04 | No placeholder lexicon (`Today’s topic`, TODO, TBD, lorem, `{{`) | Block |
| SV-05 | `tutor_intent` length ≥ 40 characters | Block |
| SV-06 | `why_now` and `explainability` not identical to another Mission in same package (similarity threshold — human confirms) | Block if identical |
| SV-07 | `cmp_reading_scope.open_point` present | Block |
| SV-08 | `session_intent` non-empty; matches `linked_episode_ids` count at certification | Block at certify |
| SV-09 | `estimated_study_time_minutes.max` ≥ `min` > 0 | Block |
| SV-10 | If `tomorrow_bridge.known=true`, next topic fields present and lawful | Block |
| SV-11 | If `revision_signals` empty, `revision_signals_note` present | Block |
| SV-12 | `status=published` requires `certification_status=pass` and publication approval | Block |
| SV-13 | `mode=revision` requires revision labelling in purpose/intent | Block |
| SV-14 | Topic code resolves to syllabus node (no address/metadata contaminants) | Block |

---

## 7. Continuity invariants

| ID | Invariant |
|----|-----------|
| CI-01 | `prior_bridge` must mention prior topic/skill **or** explicit cold-start enrolment/chapter purpose |
| CI-02 | `tomorrow_bridge.continuity_line` must agree with Mission handoff used on Summary / Home |
| CI-03 | `concept_focus` must appear coherently in purpose, objective, or strategy (same day story) |
| CI-04 | `reflection_goal` must relate to `concept_focus` or `common_misconceptions` |
| CI-05 | One Educational Truth: pack must not assert coverage/completion facts that contradict twin/history assumptions listed |

---

## 8. Mapping to student-facing surfaces

| Schema field | Typical student surface |
|--------------|-------------------------|
| `display_title` | Home Mission hero title |
| `learning_objective` | Mission / Overview objective |
| `prior_bridge` + `why_now` | Narrative / educational context |
| `concept_focus` | Session focus line |
| `cmp_reading_scope` | Materials cue |
| `study_strategy.session_structure` | Stage list |
| `success_criteria` | “Done when…” |
| `expected_benefit` | Benefit line (not readiness ±% alone) |
| `explainability` | “Why this guidance?” |
| `tomorrow_bridge` | Tomorrow Preview |
| `reflection_goal` | Reflection framing |
| `tutor_intent` | **Internal** — not required on hero; informs all student copy |

Tutor Intent may remain authoring-internal. All student-visible fields must still pass Tutor Voice.

---

## 9. Minimal complete pack checklist

A pack is schema-complete only when:

1. Identity block valid  
2. All blueprint fields populated to Blueprint standards  
3. Continuity block complete (`continuity_bundle_complete` verifiable)  
4. Execution dependencies declared (Session/Episodes linked before certify)  
5. Quality self-checks recorded  
6. No SV-* block violations  

Certification outcomes (§4.6) are required for publication, not for draft authoring start.

---

## 10. Non-goals

- Does not define database tables or Flask models  
- Does not generate CS1 Missions  
- Does not replace Gate MG or EA-002 certification stages  
- Does not authorise placeholder publication  

---

## 11. Closing

This schema is the permanent Mission pack contract.

> If a field in the Blueprint has no home in the pack, the pack is incomplete.  
> If the pack is complete but Tutor Intent is generic, the Mission is still unfit.
