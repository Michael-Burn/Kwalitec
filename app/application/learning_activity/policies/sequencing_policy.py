"""Stateless sequencing rules for Learning Activities.

Orders structural activity types into an educational sequence. Never generates
study content or uses AI.
"""

from __future__ import annotations

from app.domain.learning_activity.value_objects.activity_type import ActivityType

# Deterministic default educational arc (structural types only).
DEFAULT_SEQUENCE: tuple[ActivityType, ...] = (
    ActivityType.INTRODUCTION,
    ActivityType.CONCEPT_LEARNING,
    ActivityType.WORKED_EXAMPLE,
    ActivityType.GUIDED_PRACTICE,
    ActivityType.INDEPENDENT_PRACTICE,
    ActivityType.KNOWLEDGE_CHECK,
    ActivityType.REFLECTION,
    ActivityType.SUMMARY,
    ActivityType.NEXT_INTENTION,
)

# Relative educational priority for stable sort when reordering known types.
_TYPE_PRIORITY: dict[ActivityType, int] = {
    ActivityType.INTRODUCTION: 10,
    ActivityType.CONCEPT_LEARNING: 20,
    ActivityType.WORKED_EXAMPLE: 30,
    ActivityType.GUIDED_PRACTICE: 40,
    ActivityType.INDEPENDENT_PRACTICE: 50,
    ActivityType.KNOWLEDGE_CHECK: 60,
    ActivityType.SPACED_RECALL: 65,
    ActivityType.REVIEW: 70,
    ActivityType.REFLECTION: 80,
    ActivityType.SUMMARY: 90,
    ActivityType.NEXT_INTENTION: 100,
    ActivityType.CUSTOM: 55,
}

# Map common session planner tags → ActivityType (structural bridge only).
_TAG_TO_TYPE: dict[str, ActivityType] = {
    "read_core_notes": ActivityType.CONCEPT_LEARNING,
    "check_definitions": ActivityType.CONCEPT_LEARNING,
    "self_explain": ActivityType.REFLECTION,
    "worked_example": ActivityType.WORKED_EXAMPLE,
    "guided_practice": ActivityType.GUIDED_PRACTICE,
    "independent_attempt": ActivityType.INDEPENDENT_PRACTICE,
    "compare_approaches": ActivityType.GUIDED_PRACTICE,
    "diagnose_errors": ActivityType.KNOWLEDGE_CHECK,
    "structure_solution": ActivityType.INDEPENDENT_PRACTICE,
    "spaced_review": ActivityType.SPACED_RECALL,
    "concept_check": ActivityType.KNOWLEDGE_CHECK,
    "summary_recall": ActivityType.SUMMARY,
    "targeted_revision": ActivityType.REVIEW,
    "evidence_review": ActivityType.REVIEW,
    "weak_spot_drill": ActivityType.INDEPENDENT_PRACTICE,
    "focused_study": ActivityType.CONCEPT_LEARNING,
    "practice_check": ActivityType.KNOWLEDGE_CHECK,
    "brief_reflection_prep": ActivityType.REFLECTION,
}


class SequencingPolicy:
    """Educational activity sequencing rules (stateless, deterministic)."""

    @staticmethod
    def default_types() -> tuple[ActivityType, ...]:
        """Return the default educational activity arc."""
        return DEFAULT_SEQUENCE

    @staticmethod
    def type_from_tag(tag: str) -> ActivityType:
        """Map a structural planner tag to an ActivityType."""
        token = (tag or "").strip().lower().replace("-", "_").replace(" ", "_")
        if not token:
            return ActivityType.CUSTOM
        if token in _TAG_TO_TYPE:
            return _TAG_TO_TYPE[token]
        return ActivityType.resolve(token)

    @staticmethod
    def types_from_tags(
        tags: list[str] | tuple[str, ...] | None,
    ) -> tuple[ActivityType, ...]:
        """Map planner tags to ActivityTypes, preserving first-seen order."""
        if not tags:
            return SequencingPolicy.default_types()
        collected: list[ActivityType] = []
        seen: set[ActivityType] = set()
        for tag in tags:
            activity_type = SequencingPolicy.type_from_tag(tag)
            if activity_type not in seen:
                seen.add(activity_type)
                collected.append(activity_type)
        return tuple(collected) if collected else SequencingPolicy.default_types()

    @staticmethod
    def order_types(
        types: list[ActivityType] | tuple[ActivityType, ...] | None,
        *,
        preserve_input_order: bool = True,
    ) -> tuple[ActivityType, ...]:
        """Order activity types deterministically.

        When ``preserve_input_order`` is True (default), input order is kept.
        When False, types are sorted by educational priority then catalogue order.
        """
        items = tuple(types or ())
        if not items:
            return SequencingPolicy.default_types()
        if preserve_input_order:
            return items
        return tuple(
            sorted(
                items,
                key=lambda t: (
                    _TYPE_PRIORITY.get(t, 55),
                    ActivityType.known_values().index(t.value)
                    if t.value in ActivityType.known_values()
                    else 999,
                ),
            )
        )

    @staticmethod
    def ensure_bookends(
        types: list[ActivityType] | tuple[ActivityType, ...] | None,
        *,
        require_introduction: bool = False,
        require_summary: bool = False,
        require_reflection: bool = False,
    ) -> tuple[ActivityType, ...]:
        """Optionally prepend/append educational bookend types.

        Additive only — never removes caller-supplied types.
        """
        items = list(types or ())
        if require_introduction and ActivityType.INTRODUCTION not in items:
            items.insert(0, ActivityType.INTRODUCTION)
        if require_reflection and ActivityType.REFLECTION not in items:
            items.append(ActivityType.REFLECTION)
        if require_summary and ActivityType.SUMMARY not in items:
            items.append(ActivityType.SUMMARY)
        return tuple(items) if items else SequencingPolicy.default_types()

    @staticmethod
    def priority(activity_type: ActivityType) -> int:
        """Return educational priority rank for a type."""
        return _TYPE_PRIORITY.get(activity_type, 55)

    @staticmethod
    def rejects_content_generation() -> bool:
        """Sequencing never generates study content."""
        return True

    @staticmethod
    def rejects_ai() -> bool:
        """Sequencing never uses AI."""
        return True
