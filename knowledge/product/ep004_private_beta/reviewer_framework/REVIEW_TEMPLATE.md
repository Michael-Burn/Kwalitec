# Blind Review Template

**Authority:** Canonical structure for every Kwalitec blind review  
**Filled from:** `personas/SV-XXX.yaml` + live student experience  
**Governed by:** [`REVIEW_PROTOCOL.md`](REVIEW_PROTOCOL.md)

Do not invent a new outline per run. Instantiate this template from the persona YAML.

---

## Instantiation rules

| Template block | Source |
|---|---|
| Persona header | YAML: `id`, `name`, `age`, `country`, `exam`, `attempt`, `weeks_to_exam`, `occupation` |
| Background | YAML: `background` (internalise; paraphrase into first person — do not paste as a checklist dump) |
| Task | YAML: `task` |
| Evaluation focus | YAML: `evaluation_focus` + protocol §5–9 |
| Questions | YAML: `questions` (answer every item) |
| Scoring | YAML: `scoring` (1–10 integer per dimension) |
| Output path | YAML: `output` |

Central research question: YAML `central_question` (also `educational_hypothesis` / `primary_dimension` for framing).

---

## Output document skeleton

```markdown
# Blind Review {{id}}

**Reviewer:** {{name}}
**Age:** {{age}}
**Country:** {{country}}
**Exam:** IFoA {{exam}} ({{attempt}})
**Weeks until exam:** {{weeks_to_exam}}
**Occupation:** {{occupation}}
**Date:** {{review_date}}
**Context:** {{one_or_two_sentences_from_background_and_task}}

**Package confirmed:** {{student_package_and_build_label}}. Reviewed student-facing experience only.
**Baseline:** {{brief_baseline_check}}. Ignored engineering documentation.

---

## How I used it

{{First-person narrative of the session(s) performed under {{task}}.
Name concrete screens, topics, durations, and actions.
Do not test every feature — stay inside the persona’s realistic study behaviour.}}

---

## Answers

### 1. {{questions[0]}}

{{answer}}

### 2. {{questions[1]}}

{{answer}}

… continue until every `questions[]` item is answered …

---

## Scoring

| Dimension | Score (1–10) | Notes |
|---|---|---|
| {{scoring[0]}} | {{n}} | {{short evidence note}} |
| {{scoring[1]}} | {{n}} | {{short evidence note}} |
| … | … | … |
| Overall | {{n}} | {{one-sentence overall judgement against central_question}} |

---

## Central question

**{{central_question}}**

{{Direct answer. Then 2–6 sentences of evidence. No programme synthesis.}}
```

---

## Placeholders (canonical)

### Persona

`id` · `name` · `age` · `country` · `exam` · `attempt` · `weeks_to_exam` · `occupation`

### Background

Structured facts the reviewer brings into the session (study habits, life constraints, prior failure, mature tool stack, simulated weeks of use, etc.). Convert into lived first-person context; do not dump YAML keys into the transcript.

### Task

What the reviewer must do tonight (first visit, weeknight hour, day-14 habit check, results-day return, multi-week simulation, etc.).

### Questions

Ordered list. Every item becomes a numbered `###` answer section.

### Scoring

Ordered dimension list. Always include an Overall row. Scores are integers 1–10. See [`REVIEW_SCORING_GUIDE.md`](REVIEW_SCORING_GUIDE.md) for definitions.

### Output

Write exactly one Markdown file at `output`. On repeat runs, overwrite unless archive was requested.

---

## Quality bar

- Specific observations beat generic praise or blame.
- Cite what was seen (topic names, durations, empty states, Coach wording, dual homes, practice outcome form, etc.).
- Answer the persona’s hypothesis — not a different reviewer’s.
- No comparison with other SV-IDs.
- No engineering recommendations disguised as student commentary.
