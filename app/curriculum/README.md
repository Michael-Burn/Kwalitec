# Curriculum Intelligence Engine

The **Curriculum Engine** is the central source of truth for every educational feature in Kwalitec — Study Planning, Adaptive Learning, Mission Generation, Exam Readiness, Recommendations, Analytics, and Dashboard.

Supports both **V1 (flat topics)** and **V2 (hierarchical: Section → Topic → Learning Objective)** formats with automatic detection.

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
├── models.py            # V1 + V2 dataclasses
├── exceptions.py        # Typed exceptions
├── schemas.py           # JSON Schema + detect_format()
├── loader.py            # File I/O, JSON parsing, discovery
├── validator.py         # Business-rule validation
├── repository.py        # Cache + query API (load_auto canonical entry point)
├── seed.py              # Bootstrap bundled curricula at startup
├── README.md            # This file
└── data/
    └── ifoa/
        └── cs1/
            └── 2026.json   # IFoA CS1 2026 syllabus (V1 format)
```

### Data Flow

```
JSON file  →  schemas.detect_format()  →  loader (V1 or V2 builder)
           →  schemas.validate_instance()
           →  validator.validate_curriculum[_v2]()
           →  repository._cache
           →  load_auto() / load() / load_v2()
```

---

## Two Curriculum Formats

| | V1 (legacy) | V2 (canonical) |
|---|---|---|
| Engine types | `Curriculum`, `Topic`, `LearningOutcome` | `CurriculumDefinition`, `SectionDefinition`, `TopicDefinition`, `LearningObjectiveDefinition` |
| Hierarchy | Flat topics list | Section → Topic → Learning Objective |
| Weights | Per-topic `weighting` (sums to 100%) | Per-section `exam_weight` |
| Difficulty | On `Topic` | On `SectionDefinition` and `TopicDefinition` |
| Hours | `estimated_hours` on `Topic` | `estimated_minutes` on `TopicDefinition`; `estimated_hours` on `SectionDefinition` |
| DB sections | None (`topic.section_id` NULL) | `Section` + `topic.section_id` set |
| Format key | `organisation` + `topics` present | `exam_code` + `sections` present |

Both formats coexist permanently. V1 study plans and progress rows must not break when V2 features are added.

---

## V1 JSON Schema

```json
{
  "organisation": "IFoA",
  "examination": "Actuarial Statistics",
  "paper": "CS1",
  "syllabus_version": "2026",
  "effective_from": "2026-01-01",
  "effective_to": null,
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
          "description": "Define and distinguish ...",
          "suggested_revision_days": 7
        }
      ]
    }
  ]
}
```

## V2 JSON Schema

```json
{
  "exam_code": "CS1",
  "exam_name": "Actuarial Statistics",
  "provider": "IFoA",
  "version": "2026",
  "effective_date": "2026-01-01",
  "sections": [
    {
      "id": "CS1-A",
      "code": "CS1-A",
      "title": "Random Variables and Distributions",
      "description": "...",
      "exam_weight": 25.0,
      "estimated_hours": 45.0,
      "difficulty": "foundational",
      "display_order": 1,
      "topics": [
        {
          "id": "CS1-A-T01",
          "section_id": "CS1-A",
          "code": "CS1-A.1",
          "title": "Discrete and Continuous Random Variables",
          "description": "...",
          "estimated_minutes": 90,
          "difficulty": "foundational",
          "display_order": 1,
          "learning_objectives": [
            {
              "id": "CS1-A-T01-LO01",
              "topic_id": "CS1-A-T01",
              "code": "CS1-A.1.a",
              "description": "...",
              "cognitive_level": "understand",
              "estimated_minutes": 20,
              "learning_type": "conceptual",
              "display_order": 1
            }
          ]
        }
      ]
    }
  ]
}
```

---

## Canonical Loader — `load_auto()`

All application code that needs to load a curriculum **without knowing its format** must use the canonical loader:

```python
from app.curriculum.repository import CurriculumRepository

repo = CurriculumRepository()
curriculum = repo.load_auto("ifoa", "cs1", "2026")
# → Curriculum (V1) or CurriculumDefinition (V2)
```

Or via `CurriculumEngineService` (preferred from service/route layer):

```python
from app.services.curriculum_engine_service import CurriculumEngineService

engine = CurriculumEngineService()
curriculum = engine.load_auto("IFoA", "CS1", "2026")
```

`load_auto()` tries V1 first, then falls back to V2. **Never** duplicate this logic elsewhere.

Detect the format after loading:

```python
from app.curriculum.models import CurriculumDefinition
is_v2 = isinstance(curriculum, CurriculumDefinition)
```

---

## Canonical Flattening — `get_topics_flat()`

To obtain a flat, canonically ordered list of topics from either a V1 or V2 engine curriculum:

```python
from app.services.curriculum_engine_service import CurriculumEngineService

topics = CurriculumEngineService.get_topics_flat(curriculum)
# V1: list[Topic] unchanged
# V2: list[TopicDefinition] sorted by section.display_order then topic.display_order
```

**Never** copy the `sorted(curriculum.sections, ...) for topic in sorted(...)` pattern outside this helper.

---

## Repository API

```python
from app.curriculum.repository import CurriculumRepository

repo = CurriculumRepository()

# Canonical auto-detect (recommended)
curriculum  = repo.load_auto("ifoa", "cs1", "2026")

# V1-specific
v1          = repo.load("ifoa", "cs1", "2026")
topics      = repo.get_topics("ifoa", "cs1", "2026")
topic       = repo.get_topic("ifoa", "cs1", "2026", "cs1-2026-1")
lo          = repo.get_learning_outcome("ifoa", "cs1", "2026", "cs1-2026-1-2")

# V2-specific
v2          = repo.load_v2("ifoa", "cs1", "2026")
sections    = repo.get_sections("ifoa", "cs1", "2026")
section     = repo.get_section("ifoa", "cs1", "2026", "CS1-A")
topic_v2    = repo.get_topic_v2("ifoa", "cs1", "2026", "CS1-A-T01")
los         = repo.get_learning_objectives("ifoa", "cs1", "2026", "CS1-A-T01")

# Discovery
exams       = repo.list_exams()           # [("IFoA", "CS1", ["2026"])]
versions    = repo.list_versions("ifoa", "cs1")  # ["2026"]
repo.exists("ifoa", "cs1", "2026")       # True
```

---

## Canonical DB Hierarchy (V2)

```
Curriculum (exam_name, version)
  └─ Section (display_order, exam_weight)
       └─ Topic (order, section_id → Section.id)
            └─ LearningObjective (order)
```

V1 DB layout (no sections):

```
Curriculum (exam_name, version)
  └─ Topic (order, section_id = NULL, parent_topic_id optional)
       └─ LearningObjective (order)
```

Use `CurriculumService` helpers for DB traversal — never query topics directly.

---

## Versioning Strategy

- Each syllabus year is a separate JSON file: `data/{org}/{paper}/{year}.json`
- Multiple versions coexist — a 2025 and 2026 syllabus can both be loaded
- V1 and V2 formats can coexist within the same paper across years
- No version migration is needed; each version is self-contained

---

## Adding a New Syllabus

### V1 format
1. Create `data/{organisation}/{paper}/{version}.json` following the V1 schema
2. Ensure `weighting` fields sum to ~100%
3. Ensure all `prerequisites` IDs reference valid topic IDs
4. Add `repo.load(org, paper, version)` in `seed.py`

### V2 format
1. Create `data/{organisation}/{paper}/{version}.json` following the V2 schema
2. Ensure `exam_weight` fields on sections sum to ~100%
3. Use `display_order` on both sections and topics
4. No `seed.py` change needed (V2 is discovered and imported automatically)

---

## Validation Rules

### V1

| Rule | Error |
|---|---|
| Required fields present | `CurriculumLoadError` |
| Topics array non-empty | `CurriculumLoadError` |
| Unique topic IDs and codes | `CurriculumValidationError` |
| Weightings sum to 100 ± 5% | `InvalidWeightingError` |
| All `estimated_hours` > 0 | `CurriculumValidationError` |
| Prerequisites reference valid IDs | `InvalidPrerequisiteError` |

### V2

| Rule | Error |
|---|---|
| Required fields present | `CurriculumLoadError` |
| Sections array non-empty | `CurriculumLoadError` |
| Unique section/topic/LO codes | `CurriculumValidationError` |
| Section `exam_weight` sum 100 ± 5% | `InvalidWeightingError` |
| All `estimated_minutes` > 0 | `CurriculumValidationError` |
| `display_order` unique within parent | `CurriculumValidationError` |
