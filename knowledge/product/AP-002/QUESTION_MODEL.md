# AP-002 — Question Model

**Programme:** AP-002 — Educational Assessment Engine  
**Status:** Design  

---

## 1. Purpose

Define the taxonomy and metadata contract for Assessment Engine items (“questions” broadly includes reflective and linking prompts).

Questions are **evidence instruments**, not exam items. Metadata must make selection, delivery, observation emission, and explainability deterministic.

---

## 2. Item types

| Type | Learner action | Primary evidence | Notes |
|---|---|---|---|
| **Multiple choice** | Select one option | Correctness, distractor/misconception tag | Prefer misconception-tagged distractors |
| **Multiple response** | Select all that apply | Partial correctness pattern | Record which subset chosen |
| **Numeric** | Enter number / range | Correctness with tolerance | Tolerance is educational metadata, not “marks scheme” |
| **Formula** | Enter symbolic expression | Equivalence / form match | Aligns with `formula_recall` event |
| **Free text** | Short written answer | Rubric-coded categories (deterministic) | No LLM scoring in V1 Engine |
| **Worked solution** | Study / complete steps | Step completion, error locus | Evidence of process, not only final answer |
| **Confidence rating** | Self-rate certainty | Calibration signal (soft) | Never alone upgrades mastery |
| **Reflection** | Metacognitive prompt | Reflection submission | Soft/educational narrative signal |
| **Concept linking** | Relate concepts / edges | Structural understanding vs Graph | Useful for Graph-informed recovery |

Types may compose (e.g. multiple choice + confidence rating on the same item).

---

## 3. Core metadata fields

Every item declares:

| Field | Meaning |
|---|---|
| `item_id` | Stable identifier |
| `type` | Taxonomy value above |
| `stem` | Prompt shown to learner |
| `learning_objective_id` | Educational objective advanced |
| `curriculum_entity_id` | Opaque curriculum id (resolved only via Retrieval) |
| `curriculum_entity_kind` | topic / concept / formula / … |
| `knowledge_level` | recall · understanding · application · analysis (curriculum-aligned band) |
| `difficulty` | ordered band (e.g. introductory · standard · stretch) — not a hidden IRT black box |
| `estimated_time_seconds` | Planning / mission budgeting |
| `prerequisites` | Curriculum / Graph prerequisite entity ids |
| `evidence_produced` | Declared evidence dimensions (see Scoring / Evidence models) |
| `misconception_tags` | Optional tags on distractors or error patterns |
| `hint_policy` | none · available · staged |
| `retry_policy` | none · limited · unlimited (with evidence of retries) |
| `feedback_keys` | Deterministic feedback template keys |
| `version` | Content version for audit |

### Optional fields

| Field | Meaning |
|---|---|
| `rubric` | Deterministic category map for free text / worked steps |
| `tolerance` | Numeric acceptance window |
| `equivalence_rules` | Formula normalisation rules (deterministic) |
| `graph_edge_targets` | Concept-linking expected relations |
| `accessibility` | Alt text, reading level notes |
| `locale` | Language variant |

---

## 4. Evidence produced (per item)

Each item must declare which educational evidence dimensions it can emit, for example:

- correctness
- partial_correctness_pattern
- misconception_category
- confidence
- response_time
- hint_usage
- retries
- process_step_errors
- concept_link_accuracy
- reflection_theme (coded)

Selection algorithms prefer items that fill Twin evidence gaps rather than maximising “hardness”.

---

## 5. Difficulty and knowledge level

Difficulty and knowledge level are **selection metadata**, not prestige labels shown as judgement.

Student-facing copy should prefer:

- “Quick check”
- “Practice this idea”
- “See if this still feels solid”

Avoid:

- “Hard exam question”
- “Only top students get this”

---

## 6. Prerequisites

Items with unmet prerequisites should not be selected for diagnostic depth beyond the learner’s lawful Learning Graph position — unless intent is explicitly diagnostic at the boundary, with explainable framing (“checking foundations”).

Prerequisite checks use Learning Graph + Twin state; Assessment does not invent ordering.

---

## 7. Content authority

| Source | Role |
|---|---|
| Curriculum Studio / published curriculum | Learning objectives & entity ids |
| Curriculum Retrieval | Evidence excerpts / grounding for item authoring & Tutor |
| Assessment instrument catalogue | Owned by Assessment Engine bounded context (future) |
| Founder authoring tools | Create/version items (future milestone) |

Items must not scrape VectorStore directly at runtime.

---

## 8. Versioning & immutability

- Published item versions are immutable.
- Edits create a new `version`.
- Historical sessions always reference the version answered.
- Soft-delete / retire items without rewriting past observations.

---

## 9. Anti-patterns

- Questions without learning objectives
- Distractors without educational meaning
- Free text scored by opaque LLM as mastery authority
- Difficulty as gamified shame
- Items that cannot map to an ObservationKind / AP-001 event
