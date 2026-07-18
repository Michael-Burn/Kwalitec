"""Select an Instructional Blueprint from structural signals.

Never uses student identity, mastery scores, or curriculum content.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.instructional_blueprint.blueprint_registry import (
    BlueprintRegistry,
)
from app.application.instructional_blueprint.exceptions import (
    BlueprintNotFound,
    BlueprintSelectionError,
)
from app.application.instructional_blueprint.policies.selection_policy import (
    SelectionPolicy,
)
from app.domain.instructional_blueprint.blueprint import InstructionalBlueprint
from app.domain.instructional_blueprint.blueprint_type import BlueprintType


@dataclass(frozen=True)
class SelectionResult:
    """Outcome of selecting an Instructional Blueprint."""

    blueprint: InstructionalBlueprint
    blueprint_type: BlueprintType
    rationale_tags: tuple[str, ...]


class BlueprintSelector:
    """Select a registered Instructional Blueprint deterministically."""

    def __init__(self, registry: BlueprintRegistry | None = None) -> None:
        self._registry = registry or BlueprintRegistry()

    @property
    def registry(self) -> BlueprintRegistry:
        return self._registry

    def select(
        self,
        *,
        blueprint_type: BlueprintType | str | None = None,
        blueprint_id: str | None = None,
        intent_tags: list[str] | tuple[str, ...] | None = None,
        objective_kinds: list[str] | tuple[str, ...] | None = None,
    ) -> SelectionResult:
        """Select a blueprint from structural signals.

        Precedence: explicit blueprint_id → explicit type → intent tags →
        objective kinds → default type.

        Raises:
            BlueprintSelectionError: When selection inputs are unusable.
            BlueprintNotFound: When the resolved blueprint is not registered.
        """
        if blueprint_id is not None:
            bid = blueprint_id.strip()
            if not bid:
                raise BlueprintSelectionError("blueprint_id must be non-empty")
            blueprint = self._registry.get(bid)
            rationale = (
                "source=explicit_id",
                f"selected={blueprint.blueprint_type.value}",
                "no_student_state",
                "no_curriculum_content",
                "no_ai",
            )
            return SelectionResult(
                blueprint=blueprint,
                blueprint_type=blueprint.blueprint_type,
                rationale_tags=rationale,
            )

        resolved = SelectionPolicy.resolve_type(
            blueprint_type=blueprint_type,
            intent_tags=intent_tags,
            objective_kinds=objective_kinds,
        )
        try:
            blueprint = self._registry.get_by_type(resolved)
        except BlueprintNotFound as exc:
            raise BlueprintSelectionError(
                f"No registered blueprint for selected type {resolved.value!r}"
            ) from exc

        rationale = SelectionPolicy.rationale_tags(
            resolved=resolved,
            blueprint_type=blueprint_type,
            intent_tags=intent_tags,
            objective_kinds=objective_kinds,
        )
        return SelectionResult(
            blueprint=blueprint,
            blueprint_type=resolved,
            rationale_tags=rationale,
        )

    def resolve_type(
        self,
        *,
        blueprint_type: BlueprintType | str | None = None,
        intent_tags: list[str] | tuple[str, ...] | None = None,
        objective_kinds: list[str] | tuple[str, ...] | None = None,
    ) -> BlueprintType:
        """Resolve type without fetching a blueprint instance."""
        return SelectionPolicy.resolve_type(
            blueprint_type=blueprint_type,
            intent_tags=intent_tags,
            objective_kinds=objective_kinds,
        )
