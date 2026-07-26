# Blind Review Execution Guide

**Purpose:** Execute any registered reviewer from a short operator instruction — without recreating prompts.  
**Framework root:** `knowledge/product/ep004_private_beta/reviewer_framework/`

---

## Automatic run contract

When the operator says any of:

- `Run reviewer SV-011`
- `Run SV-004`
- `Repeat SV-007`
- `Run all reviewers`
- `Run only CM1 reviewers`
- `Run only workflow reviewers`
- `Run only trust reviewers`

the agent must:

1. Load [`REVIEW_PROTOCOL.md`](REVIEW_PROTOCOL.md)
2. Load [`REVIEW_TEMPLATE.md`](REVIEW_TEMPLATE.md)
3. Load the matching persona YAML under [`personas/`](personas/)
4. Verify the latest student review package + baseline
5. Perform the review as that student only
6. Write `knowledge/product/ep004_private_beta/blind_reviews/SV-XXX.md`

No separate mega-prompt is required.

---

## Load sequence (every single-reviewer run)

```
REVIEW_PROTOCOL.md
        ↓
REVIEW_TEMPLATE.md
        ↓
personas/SV-XXX.yaml
        ↓
knowledge/reviews/V1_REVIEW_PACKAGE/   (verify)
../REVIEW_BASELINE_AUDIT.md            (verify when present)
        ↓
Live student-facing application experience
        ↓
blind_reviews/SV-XXX.md                (write)
```

Optional scoring reference: [`REVIEW_SCORING_GUIDE.md`](REVIEW_SCORING_GUIDE.md).

---

## Examples

### Run SV-004

1. Load protocol + template.
2. Load `personas/SV-004.yaml` (Michael Dube — restart after missed days).
3. Verify package/baseline.
4. Complete one realistic Monday-evening return session under the persona task.
5. Answer all YAML questions; score YAML dimensions.
6. Write `../blind_reviews/SV-004.md`.

### Run SV-011

1. Load protocol + template.
2. Load `personas/SV-011.yaml` (Oliver Hughes — educational feedback after consistent study).
3. Simulate the YAML task frame (three weeks of consistent use) while judging the **current** student experience.
4. Focus on improvement awareness / feedback surfaces (Journey, Readiness, Coach, practice outcomes, progress honesty).
5. Write `../blind_reviews/SV-011.md`.

### Run SV-020

1. Load protocol + template.
2. Load `personas/SV-020.yaml` (Michael Edwards — bounded commitment).
3. Explore thoroughly enough to decide commitment; complete several representative sessions if needed.
4. End with an explicit commit / do-not-commit judgement as required by the persona task and central question.
5. Write `../blind_reviews/SV-020.md`.

### Repeat SV-007

Same as Run SV-007:

- Reload YAML (do not reuse memory of the previous transcript as evidence).
- Re-verify package/baseline against today’s build.
- Overwrite `../blind_reviews/SV-007.md` unless the operator asked to archive.
- Still no comparison with other reviewers.

### Repeat all reviews

1. Resolve the full set SV-001 … SV-020 from [`REVIEWER_REGISTRY.md`](REVIEWER_REGISTRY.md).
2. Execute **sequentially**, one reviewer at a time.
3. Between reviewers: clear persona context; do not carry findings forward.
4. Produce/overwrite all twenty review files.
5. Do **not** run meta-analysis unless separately requested.

### Run only CM1 reviewers

Select personas where `exam: CM1`:

`SV-002, SV-005, SV-006, SV-008, SV-011, SV-012, SV-013, SV-015, SV-017, SV-019`

Execute sequentially.

### Run only workflow reviewers

Select personas with `workflow` in `filter_tags` (and/or `primary_dimension: Workflow`):

Typically: `SV-002, SV-007, SV-009, SV-016, SV-018`

(Habit-retention SV-007 is included as workflow/habit infrastructure.)

### Run only trust reviewers

Select personas with `trust` in `filter_tags` (and/or trust-centred hypotheses):

Typically: `SV-003, SV-005, SV-008, SV-010, SV-013, SV-014`

### Run reviewers by exam

Operator form:

- `Run all CS1 reviewers`
- `Run all CM1 reviewers`
- `Run all CS2 reviewers`

Filter: YAML `exam`.

### Run reviewers by hypothesis

Operator form:

- `Run reviewers for hypothesis Calibration`
- `Run deliberate practice reviewer`

Match against `educational_hypothesis` and/or `primary_dimension` in the registry.

### Run reviewers by educational dimension

Operator form:

- `Run all Decision Support reviewers`
- `Run Adaptation reviewers`

Filter: YAML `primary_dimension`.

### Generate a new reviewer

1. Choose next ID (`SV-021`…).
2. Copy an existing YAML as structural template.
3. Change demographics, hypothesis, dimension, questions, and scoring to a **new** research question.
4. Register the row in [`REVIEWER_REGISTRY.md`](REVIEWER_REGISTRY.md).
5. Run with `Run reviewer SV-021`.

---

## Expected outputs

| Request | Output |
|---|---|
| Single reviewer | One Markdown file at persona `output` |
| Filtered batch | One Markdown file per selected ID |
| Full cohort | Twenty files `SV-001.md` … `SV-020.md` |
| New reviewer | New YAML + registry row + review file on first run |

Each review file must contain:

- Persona header
- Package/baseline confirmation
- First-person usage narrative
- Full answers section
- Scoring table (1–10)
- Explicit central-question answer

Not expected unless separately requested:

- Meta-analysis
- Product recommendations
- Engineering tickets
- Score averages across reviewers

---

## Selection cheat sheet

| Intent | Filter |
|---|---|
| One known student | `id` |
| Paper family | `exam` |
| Sitting | `attempt` |
| Research theme | `primary_dimension` / `educational_hypothesis` |
| Workflow programme slice | `filter_tags` contains `workflow` |
| Trust programme slice | `filter_tags` contains `trust` |
| CM1 programme slice | `exam: CM1` |

Registry master table: [`REVIEWER_REGISTRY.md`](REVIEWER_REGISTRY.md).

---

## Failure conditions (do not write a review)

Stop and report to the operator if:

- Persona YAML is missing or malformed
- Review package path is missing
- Live student app is unreachable when the task requires interactive verification
- Operator asked for synthesis/recommendations inside a persona run

---

## Operator phrases (canonical)

```
Run reviewer SV-011
Run SV-004
Repeat SV-007
Repeat all reviews
Run all reviewers
Run only CM1 reviewers
Run only workflow reviewers
Run only trust reviewers
Run all CS1 reviewers
Run reviewers by dimension Calibration
Generate new reviewer based on SV-014 for [new hypothesis]
```
