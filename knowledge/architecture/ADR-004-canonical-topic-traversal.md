# ADR-004: Canonical Topic Traversal

# Status

Accepted

# Date

2026-07-10

# Context

Almost every learning feature needs an ordered list of topics: study-plan distribution, “next incomplete topic,” daily missions, readiness coverage, recommendations, and analytics.

V1 and V2 use **different** ordering rules:

| Format | Order |
|---|---|
| V2 | `Section.display_order`, then `Topic.order` within each section |
| V1 | Depth-first walk of `parent_topic_id` + `order` via `curriculum.get_all_topics_ordered()` |

If planning, missions, and readiness each implement their own “get topics in order” query, Kwalitec will silently diverge: one feature walks sections, another sorts by primary key, another ignores inactive topics. That breaks determinism and V1/V2 compatibility ([ADR-003](ADR-003-curriculum-v1-v2.md)).

# Decision

**All curriculum topic traversal for product features must go through `CurriculumService` helpers.** The primary entry point is:

```python
CurriculumService.get_all_topics_ordered(curriculum)
```

Related helpers (same ownership, same branching):

| Method | Behaviour |
|---|---|
| `get_sections(curriculum)` | Sections by `display_order`; `[]` for V1 |
| `get_topics_for_section(section)` | Active topics by `Topic.order` |
| `get_all_topics_ordered(curriculum)` | V2: section then topic; V1: parent-tree DFS |
| `get_ordered_topics(curriculum)` | Alias → `get_all_topics_ordered` |
| `get_next_incomplete_topic(...)` | First incomplete leaf in canonical order |

Branching lives **only** inside these helpers:

```
if get_sections(curriculum):
    # V2: sections → topics
else:
    # V1: parent-tree DFS
```

### Forbidden

- Reimplementing V1/V2 ordering in `PlanningService`, `MissionService`, `ReadinessService`, `RecommendationService`, or routes.
- Ad-hoc `Topic.query.filter_by(curriculum_id=...).order_by(...)` for syllabus order.
- Assuming `Topic.order` alone is globally meaningful for V2 (order is per section).

`get_ordered_topics` exists as a compatibility alias; new code should prefer `get_all_topics_ordered` for clarity.

# Consequences

### Positive consequences

- One ordering story for the whole product → reproducible plans and missions.
- V1 flat curricula and V2 sectioned curricula stay correct without callers knowing the format.
- Code review has a clear red flag: duplicate traversal logic.
- Matches [`ARCHITECTURE.md`](../../ARCHITECTURE.md) “Curriculum Traversal” and `.cursor/rules/08-curriculum-v2.mdc`.

### Trade-offs

- Callers must depend on `CurriculumService` even for “simple” lists — intentional coupling to the right abstraction.
- Performance-sensitive paths still go through the helper; optimise inside the helper, not by bypassing it.
- Engine in-memory ordering APIs remain separate; DB product features use the service, not raw engine walks, after import.

### Future considerations

- If ordering rules change (e.g. new hierarchy level), update **only** `CurriculumService` and expand regression tests.
- Keep `get_next_incomplete_topic` and similar derived helpers on the same service so “next” always means “next in canonical order.”
- Document any intentional non-canonical sort (e.g. urgency ranking of mission *tasks*) as ranking **after** canonical topic identity is resolved — not as a replacement for syllabus order.

**See also:** [curriculum-engine.md](../subsystems/curriculum-engine.md), [study-planning.md](../subsystems/study-planning.md), [missions.md](../subsystems/missions.md).

## Governance Alignment

This decision must remain consistent with:

- [Product Vision 2030](../product/vision/PRODUCT_VISION_2030.md) — product constitution
- [Product Blueprint](../../PRODUCT_BLUEPRINT.md) — product strategy and operating model
- [Educational Constitution](../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) — educational principles

If a future change would conflict with those authorities, amend the governing documents first (see [`knowledge/GOVERNANCE.md`](../GOVERNANCE.md)).
