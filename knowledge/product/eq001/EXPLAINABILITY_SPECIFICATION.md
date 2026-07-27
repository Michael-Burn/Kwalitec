# EQ-001 — Explainability Specification (Runtime C generation)

**Programme:** EQ-001  
**Status:** Active  
**Companion:** [`../p001_2_explainability_standard/EXPLAINABILITY_STANDARD.md`](../p001_2_explainability_standard/EXPLAINABILITY_STANDARD.md)

---

## 1. Purpose

Every automatically generated mission and journey decision on Runtime C must expose **structured reasoning suitable for student display**, without requiring a UI redesign in this programme.

This specification maps Runtime C generation outputs onto the P-001.2 Mandatory Explanation Schema so future surfaces can consume one contract.

---

## 2. Schema version

| Field | Value |
|---|---|
| `explanation_schema_version` | `eq001/p001.2/v1` |
| Default level | `level_1` for daily mission; `level_2` for journey / pacing judgements |

---

## 3. Mission explanation envelope

Each mission quality envelope includes an `explanation` object:

| Key | Content |
|---|---|
| `judgement` | Short statement of today’s learning focus |
| `why_this_plan` / `why_this_mission` | Educational rationale (syllabus position + objectives) |
| `supporting_evidence` | List of identifiable facts (topic code, LO codes, prerequisite status, recommended minutes) |
| `confidence_level` | `High confidence` when curriculum-bound with satisfied prerequisites; otherwise humble |
| `expected_benefit` | Coverage / first-pass progress on named topic — never mastery claims from mission alone |
| `suggested_next_action` | Complete today’s mission tasks for the named topic |
| `review_point` | After mission completion / next study day |
| `plan_drivers` | Structured drivers: `syllabus_order`, `learning_objectives`, `prerequisites`, `estimated_duration` |
| `explanation_schema_complete` | `true` when all mandatory keys present |

---

## 4. Journey explanation envelope

| Key | Content |
|---|---|
| `why_today` | Why current topic is selected |
| `why_previous_complete` | Why previous topic is treated complete |
| `unlocks_next` | What completing today unlocks |
| `supporting_evidence` | Progress facts (coverage ratio, completed count, journey stage) |
| `explanation_schema_version` | `eq001/p001.2/v1` |

---

## 5. Forbidden speech

- Twin / Adaptive / warrant / pipeline / internal enum leakage
- Mastery or Exam Ready claims from mission completion alone
- Vague “because learning evidence says so” without syllabus facts
- Silent prerequisite skips

---

## 6. Certification ids

| Id | Check |
|---|---|
| EQ-X01 | Mission explanation has complete mandatory schema |
| EQ-X02 | Supporting evidence cites topic and at least one objective |
| EQ-X03 | Confidence matches prerequisite satisfaction |
| EQ-X04 | Journey explanation answers the three mandatory questions |
| EQ-X05 | No forbidden technical jargon in student-facing rationale fields |
