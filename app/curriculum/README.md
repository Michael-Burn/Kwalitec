# Curriculum Intelligence Engine

The **Curriculum Engine** is the central source of truth for every educational feature in Kwalitec — Study Planning, Adaptive Learning, Mission Generation, Exam Readiness, Recommendations, Analytics, and Dashboard.

---

## Purpose

Every feature in Kwalitec that needs to know *what* a student should study gets that information from the Curriculum Engine. The engine loads official examination syllabuses (IFoA, and in the future CAA, SOA, etc.) and exposes them through a clean, in-memory repository API.

---

## Design Principles

1. **Curriculum First.** Everything begins with the official syllabus — not with ML models, heuristics, or user preferences.
2. **Deterministic.** No AI. No randomness. No external API calls. Given the same JSON, the engine always produces the same curriculum.
3. **Versioned.** Multiple syllabus years coexist. A 2025 syllabus and a 2026 syllabus for the same paper are independently loadable.
4. **Explainable.** Every topic, learning outcome, weighting, and prerequisite is traceable back to the source JSON.
5. **Extensible.** Adding a new paper (e.g. CM1) or a new examining body (e.g. CAA) requires only a JSON file — zero code changes.

---

## Architecture

```
app/curriculum/
├── __init__.py          # Public API exports
├── models.py            # Dataclasses: Curriculum, Topic, LearningOutcome
├── exceptions.py        # Typed exceptions for every failure mode
├── schemas.py           # JSON Schema definition + lightweight validator
├── loader.py            # File I/O, JSON parsing, curriculum discovery
├── validator.py         # Business-rule validation (weightings, codes, etc.)
├── repository.py        # In-memory cache + query API
├── seed.py              # Bootstrap bundled curricula at startup
├── README.md            # This file
└── data/
    └── ifoa/
        └── cs1/
            └── 2026.json   # IFoA CS1 2026 syllabus
```

### Data Flow

```
JSON file  →  loader  →  schemas.validate_instance()
                        →  loader.build dataclasses
                        →  validator.validate_curriculum()
                        →  repository.cache
                        →  repository API (get_curriculum, get_topics, ...)
```

---

## JSON Schema

Each curriculum file is a JSON document with this structure:

```json
{
  "organisation": "IFoA",
  "examination": "Actuarial Statistics",
  "paper": "CS1",
  "syllabus_version": "2026",
  "effective_from": "2026-01-01",
  "effective_to": null,
  "metadata": {
    "description": "...",
    "source_url": "..."
  },
  "topics": [
    {
      "id": "cs1-2026-1",
      "code": "CS1-A",
      "title": "Random Variables and Distributions",
      "description": "...",
      "weighting": 25.0,
      "estimated_hours": 45.0,
      "difficulty": "foundational",
      "prerequisites": [],
      "learning_outcomes": [
        {
          "id": "cs1-2026-1-1",
          "code": "CS1-A-1",
          "description": "Define and distinguish between discrete and continuous random variables.",
          "suggested_revision_days": 7
        }
      ]
    }
  ]
}
```

### Field Reference

| Field | Type | Required | Notes |
|---|---|---|---|
| `organisation` | string | Yes | e.g. `IFoA`, `CAA`, `SOA` |
| `examination` | string | Yes | Full qualification name |
| `paper` | string | Yes | Paper code, e.g. `CS1`, `CM1` |
| `syllabus_version` | string | Yes | 4-digit year |
| `effective_from` | string | Yes | ISO date |
| `effective_to` | string\|null | No | ISO date or null |
| `metadata` | object | No | Arbitrary key-value pairs |
| `topics[].id` | string | Yes | Unique within the curriculum |
| `topics[].code` | string | Yes | Human-readable, unique |
| `topics[].weighting` | number | Yes | 0–100; all must sum to ~100 |
| `topics[].estimated_hours` | number | Yes | Must be > 0 |
| `topics[].difficulty` | enum | Yes | `foundational`, `intermediate`, `advanced` |
| `topics[].prerequisites` | string[] | Yes | Topic IDs that should be studied first |
| `topics[].learning_outcomes[].suggested_revision_days` | int | No | Defaults to 14 |

---

## Repository API

```python
from app.curriculum import CurriculumRepository, seed_curricula

repo = seed_curricula()

curriculum  = repo.get_curriculum("ifoa", "cs1", "2026")
topics      = repo.get_topics("ifoa", "cs1", "2026")
topic       = repo.get_topic("ifoa", "cs1", "2026", "cs1-2026-1")
lo          = repo.get_learning_outcome("ifoa", "cs1", "2026", "cs1-2026-1-2")

exams       = repo.list_exams()       # [("IFoA", "CS1", ["2026"])]
versions    = repo.list_versions("ifoa", "cs1")  # ["2026"]

repo.exists("ifoa", "cs1", "2026")    # True
repo.exists("ifoa", "cm2", "2025")    # False
```

---

## Versioning Strategy

- Each syllabus year is a separate JSON file: `data/{org}/{paper}/{year}.json`
- Multiple versions coexist — a 2025 and 2026 syllabus can both be loaded
- `Curriculum.effective_from` / `effective_to` encode the active date range
- No version migration is needed; each version is self-contained

---

## Adding a New Syllabus

1. Create the JSON file at `data/{organisation}/{paper}/{version}.json`
2. Follow the JSON schema documented above
3. Ensure weightings sum to ~100%
4. Ensure all prerequisite IDs reference valid topic IDs
5. Add a `repo.load(...)` call in `seed.py`
6. No code changes needed

---

## Adding a New Examination Board

1. Create a new directory under `data/` (e.g. `data/caa/`)
2. Create paper subdirectories and JSON files following the same convention
3. Update `seed.py` if the board should be pre-loaded at startup
4. No code changes needed

---

## Validation Rules

The engine enforces these rules on every load:

| Rule | Error |
|---|---|
| Required fields present | `CurriculumLoadError` |
| `syllabus_version` is a 4-digit year | `CurriculumLoadError` |
| Topics array is non-empty | `CurriculumLoadError` |
| Unique topic IDs | `CurriculumValidationError` |
| Unique topic codes | `DuplicateTopicCodeError` |
| Unique learning outcome codes | `DuplicateLearningOutcomeCodeError` |
| Weightings sum to 100 ± 5% | `InvalidWeightingError` |
| All `estimated_hours` > 0 | `CurriculumValidationError` |
| Prerequisites reference valid topic IDs | `InvalidPrerequisiteError` |
| Difficulty is one of the three enum values | `CurriculumValidationError` |
| All `suggested_revision_days` > 0 | `CurriculumValidationError` |
