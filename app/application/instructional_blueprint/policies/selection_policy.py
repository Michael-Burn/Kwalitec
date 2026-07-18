"""Stateless selection rules for Instructional Blueprints.

Selects pedagogical strategies from structural intent / objective tags only.
Never uses student identity, mastery scores, or curriculum content.
"""

from __future__ import annotations

from app.domain.instructional_blueprint.blueprint_type import BlueprintType

# Deterministic intent-tag → blueprint type mapping (structural only).
_INTENT_TO_TYPE: dict[str, BlueprintType] = {
    "concept": BlueprintType.CONCEPT_MASTERY,
    "concept_mastery": BlueprintType.CONCEPT_MASTERY,
    "mastery": BlueprintType.CONCEPT_MASTERY,
    "understand": BlueprintType.CONCEPT_MASTERY,
    "calculation": BlueprintType.CALCULATION_INTENSIVE,
    "calculation_intensive": BlueprintType.CALCULATION_INTENSIVE,
    "compute": BlueprintType.CALCULATION_INTENSIVE,
    "apply": BlueprintType.CALCULATION_INTENSIVE,
    "theory": BlueprintType.THEORY_HEAVY,
    "theory_heavy": BlueprintType.THEORY_HEAVY,
    "explain": BlueprintType.THEORY_HEAVY,
    "revision": BlueprintType.REVISION,
    "revise": BlueprintType.REVISION,
    "review": BlueprintType.REVISION,
    "spaced": BlueprintType.REVISION,
    "mixed": BlueprintType.MIXED_PRACTICE,
    "mixed_practice": BlueprintType.MIXED_PRACTICE,
    "practice": BlueprintType.MIXED_PRACTICE,
    "exam": BlueprintType.EXAM_PRACTICE,
    "exam_practice": BlueprintType.EXAM_PRACTICE,
    "assessment": BlueprintType.EXAM_PRACTICE,
    "test": BlueprintType.EXAM_PRACTICE,
    "case": BlueprintType.CASE_STUDY,
    "case_study": BlueprintType.CASE_STUDY,
    "analyse": BlueprintType.CASE_STUDY,
    "analyze": BlueprintType.CASE_STUDY,
    "custom": BlueprintType.CUSTOM,
}

# Objective-kind tokens → blueprint type (structural bridge only).
_OBJECTIVE_KIND_TO_TYPE: dict[str, BlueprintType] = {
    "understand": BlueprintType.CONCEPT_MASTERY,
    "apply": BlueprintType.CALCULATION_INTENSIVE,
    "analyse": BlueprintType.CASE_STUDY,
    "analyze": BlueprintType.CASE_STUDY,
    "review": BlueprintType.REVISION,
    "revise": BlueprintType.REVISION,
}


class SelectionPolicy:
    """Instructional blueprint selection rules (stateless, deterministic)."""

    @staticmethod
    def default_type() -> BlueprintType:
        """Default blueprint when no structural signal is supplied."""
        return BlueprintType.CONCEPT_MASTERY

    @staticmethod
    def normalise_tag(tag: str) -> str:
        """Normalise a structural selection tag."""
        return (tag or "").strip().lower().replace("-", "_").replace(" ", "_")

    @staticmethod
    def type_from_intent(tag: str) -> BlueprintType | None:
        """Map a structural intent tag to a BlueprintType, if known."""
        token = SelectionPolicy.normalise_tag(tag)
        if not token:
            return None
        return _INTENT_TO_TYPE.get(token)

    @staticmethod
    def type_from_objective_kind(kind: str) -> BlueprintType | None:
        """Map an objective-kind token to a BlueprintType, if known."""
        token = SelectionPolicy.normalise_tag(kind)
        if not token:
            return None
        return _OBJECTIVE_KIND_TO_TYPE.get(token)

    @staticmethod
    def resolve_type(
        *,
        blueprint_type: BlueprintType | str | None = None,
        intent_tags: list[str] | tuple[str, ...] | None = None,
        objective_kinds: list[str] | tuple[str, ...] | None = None,
    ) -> BlueprintType:
        """Resolve a BlueprintType from structural signals.

        Precedence: explicit type → first matching intent tag → first matching
        objective kind → default. Never inspects student state.
        """
        if blueprint_type is not None:
            return BlueprintType.resolve(blueprint_type)

        for tag in intent_tags or ():
            resolved = SelectionPolicy.type_from_intent(tag)
            if resolved is not None:
                return resolved

        for kind in objective_kinds or ():
            resolved = SelectionPolicy.type_from_objective_kind(kind)
            if resolved is not None:
                return resolved

        return SelectionPolicy.default_type()

    @staticmethod
    def rationale_tags(
        *,
        resolved: BlueprintType,
        blueprint_type: BlueprintType | str | None = None,
        intent_tags: list[str] | tuple[str, ...] | None = None,
        objective_kinds: list[str] | tuple[str, ...] | None = None,
    ) -> tuple[str, ...]:
        """Explainable selection rationale (no mastery claims)."""
        tags: list[str] = [f"selected={resolved.value}"]
        if blueprint_type is not None:
            tags.append("source=explicit_type")
        elif intent_tags:
            tags.append("source=intent_tags")
            tags.append(f"intent_count={len(tuple(intent_tags))}")
        elif objective_kinds:
            tags.append("source=objective_kinds")
            tags.append(f"objective_kind_count={len(tuple(objective_kinds))}")
        else:
            tags.append("source=default")
        tags.append("no_student_state")
        tags.append("no_curriculum_content")
        tags.append("no_ai")
        return tuple(tags)

    @staticmethod
    def rejects_student_state() -> bool:
        """Selection never uses student-specific state."""
        return True

    @staticmethod
    def rejects_content_generation() -> bool:
        """Selection never generates study content."""
        return True

    @staticmethod
    def rejects_ai() -> bool:
        """Selection never uses AI."""
        return True
