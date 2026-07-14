# FOS-003 — Internal Alpha Processing Pipeline

**Document ID:** FOS-003  
**Title:** Internal Alpha Processing Pipeline  
**Owner:** Founder Operating System  
**Status:** Version 1.0 Implemented  
**Classification:** Founder Infrastructure

---

## Purpose

Transform raw Internal Alpha text feedback into structured engineering artefacts.

Version 1 is **filesystem-based infrastructure only**:

- No UI
- No Flask routes
- No Dashboard
- No LLMs / AI summaries
- No founder recommendations
- No database persistence

The pipeline is deterministic and fully unit-tested.

---

## Architecture

Package root: `app/founder/internal_alpha/`

```text
app/founder/internal_alpha/
├── config.py              # Single configuration location
├── models/                # Immutable domain objects
├── dto/                   # Serialisation helpers + DuplicateRelation
├── validators/            # Folder + file validation
├── processors/            # Discover + read FeedbackItem
├── classifiers/           # RuleBasedClassifier + DuplicateDetector
├── aggregators/           # WeeklyAggregator (counts only)
├── exporters/             # JSON + Markdown writers
├── services/              # InternalAlphaPipelineService (coordinator)
└── tests/                 # Unit tests (temp directories)
```

### Dependency direction

```text
services  →  validators, processors, classifiers, aggregators, exporters
exporters →  models, dto, config
aggregators / classifiers / processors / validators → models, config, dto
```

No Flask, no SQLAlchemy, no curriculum engine imports.

---

## Pipeline Flow

`InternalAlphaPipelineService.run(week_dir)` executes:

1. **Discover week** — treat `week_dir` as the week root (label = directory name unless overridden)
2. **Validate** — `FeedbackFolderValidator` (folder, `raw_feedback/`, `.txt` presence)
3. **Read files** — `FeedbackProcessor` (+ `FeedbackFileValidator` encoding/emptiness)
4. **Classify** — `RuleBasedClassifier` (configurable keyword rules)
5. **Detect duplicates** — `DuplicateDetector` (relationships only; items retained)
6. **Aggregate** — `WeeklyAggregator` (category / contributor / duplicate counts)
7. **Export** — write JSON + Markdown under `processed/` (or custom `output_dir`)
8. **Return** — `PipelineResult`

---

## Folder Structure (week input)

```text
<week_dir>/
├── raw_feedback/
│   ├── alice.txt
│   └── bob.txt
└── processed/          # created by the pipeline
    ├── classified_feedback.json
    ├── feedback_statistics.json
    ├── duplicate_report.json
    ├── WEEK_SUMMARY.md
    ├── architecture.md
    ├── engineering.md
    ├── product.md
    ├── educational.md
    ├── ux.md
    ├── proposed_actions.md
    └── release_readiness.md
```

Contributor identity Version 1: filename stem (e.g. `alice.txt` → `alice`).

---

## Core Domain Objects

| Object | Role |
|--------|------|
| `FeedbackItem` | Immutable raw observation |
| `ClassifiedFeedback` | Category + confidence + optional `duplicate_of` |
| `WeeklySummary` | Counts for one week |
| `PipelineResult` | Success flag, items, warnings, output paths |

---

## Configuration

All configurable values live in `app/founder/internal_alpha/config.py`:

- categories
- keyword rules
- folder names (`raw_feedback`, `processed`)
- feedback extension
- similarity threshold
- output filenames
- default category (`Other`)

Construct overrides with `InternalAlphaPipelineConfig(...)` for tests or future weeks without changing the coordinator.

Adding a category in a future version: extend `categories` + `keyword_rules` (+ optional markdown export mapping). The pipeline service does not hardcode category lists.

---

## Classification (V1)

`RuleBasedClassifier` scans configured keyword rules (case-insensitive substring). Highest hit count wins; ties break by configured category order. Zero hits → `Other` with confidence `0.0`.

---

## Duplicate Detection (V1)

`DuplicateDetector` returns `DuplicateRelation` records for:

1. Identical raw text
2. Normalised-identical text (case / whitespace / punctuation)
3. Similarity ≥ configured threshold (`difflib.SequenceMatcher` on normalised text)

Duplicates are **never** deleted automatically. The pipeline annotates `ClassifiedFeedback.duplicate_of`.

---

## Exporters

Exporters write files only. They do not classify, aggregate, or recommend.

JSON: `classified_feedback.json`, `feedback_statistics.json`, `duplicate_report.json`  
Markdown: `WEEK_SUMMARY.md`, category files, `proposed_actions.md`, `release_readiness.md`

---

## Future Extensions

- Pluggable classifiers (still deterministic; no LLMs in core path without ADR)
- Cross-week trend aggregation
- Contributor identity beyond filename stem
- Founder recommendation layer (FOS-004+)
- Dashboard presentation of processed artefacts
- Optional DB persistence — out of scope for V1

Do not begin FOS-004 from this document alone; architecture review gates the next capability.

---

## Related Paths

| Path | Role |
|------|------|
| `research/internal_alpha/` | Research week templates (human process) |
| `knowledge/founder/FOS-003_INTERNAL_ALPHA_PIPELINE.md` | This specification |
| `app/founder/internal_alpha/` | Implementation |
