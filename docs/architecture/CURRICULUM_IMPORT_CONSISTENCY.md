# Curriculum Import Consistency

**Status:** Active  
**Scope:** Official syllabus JSON under `app/curriculum/data/`  
**Related:** `app/curriculum/README.md`, ADR-001, Capability 4.2 Internal Alpha Enablement

## Purpose

Keep multi-paper syllabi (CS1, CB2, CM1, …) importable through one V2 path so
`CurriculumService`, `CurriculumContextBuilder`, Study Plan wizard,
`PlanningService`, Time Engine, and the Educational Orchestrator stay compatible
without per-paper special cases.

## Canonical layout

```
app/curriculum/data/{organisation}/{paper}/{year}.json
```

Example:

- `app/curriculum/data/ifoa/cs1/2026.json`
- `app/curriculum/data/ifoa/cb2/2026.json`
- `app/curriculum/data/ifoa/cm1/2026.json`

Organisation and paper directory names are lowercase. Discovery is automatic via
`CurriculumRepository.discover_curricula` / `load_auto`.

## V2 hierarchy (required for IFoA Core Principles papers)

```
Subject (exam_code / exam_name)
  └─ Major Topic / Section  (exam_weight on section only)
       └─ Subtopic / Topic
            └─ Learning Objective
```

Rules:

1. Preserve official numbering in `code` fields (`1`, `1.1`, `1.1.1`, …).
2. Preserve official titles and descriptions from the published syllabus.
3. Put exam weights on **sections only**. Topic rows import with
   `syllabus_weight=0.0` in the database.
4. Section `exam_weight` values must sum to 100 ± 5.
5. Do not invent weights for subtopics.
6. Do not flatten or simplify the official hierarchy for convenience.

## Import path

1. Place JSON at the canonical path.
2. Startup / `CurriculumService.import_curricula()` discovers and imports
   idempotently.
3. V2 import creates `Section` rows, links `Topic.section_id`, and stores learning
   objectives.
4. No `seed.py` change is required for additional V2 papers.

## Product surface consistency

| Consumer | Expectation |
|---|---|
| Study Plan wizard | Paper appears via examination catalogue (`IFoA` + paper code) |
| Roadmap UI | Show section weight on section headers; omit blank topic weights |
| Planning / missions | Traverse topics via `CurriculumService.get_all_topics_ordered` |
| CurriculumContextBuilder | Detects V2 when sections exist; uses section weights |
| Time Engine / Orchestrator | Receive curriculum context through existing builders |

## Adding a paper checklist

1. Obtain the official syllabus PDF for the target exam year.
2. Encode full Section → Topic → Learning Objective structure in V2 JSON.
3. Run curriculum validation (`validate_curriculum_v2`).
4. Confirm discovery: `CurriculumRepository().load_auto(org, paper, year)`.
5. Confirm DB import creates sections + topics.
6. Confirm a study plan can be created for `IFoA {PAPER}`.

## Non-goals

- Evidence Loop / Twin / Recommendation redesign
- Inventing unofficial topic weights
- Public self-registration of curricula or users
