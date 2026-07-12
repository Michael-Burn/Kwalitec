"""Actionable suggestion projected from Decision SelectedAction.

Projection only — never re-selects among candidates or invents topics.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.decision.action_types import (
    ActionFamily,
    ActionIntent,
    SelectedAction,
)


@dataclass(frozen=True)
class ActionableSuggestion:
    """Student-facing action surface projected from Decision selected action.

    Attributes:
        family: Action family from Decision — not re-chosen.
        curriculum_entity_id: Official syllabus identity when Decision scoped it.
        intent: Named educational tension from Decision.
        intent_tags: Structural tags derived from intent / Decision notes.
        presentation_tags: Structural communication tags — not marketing slogans.
    """

    family: ActionFamily
    curriculum_entity_id: str | None
    intent: ActionIntent
    intent_tags: tuple[str, ...] = ()
    presentation_tags: tuple[str, ...] = ()

    @classmethod
    def create(
        cls,
        family: ActionFamily | str,
        *,
        curriculum_entity_id: str | None = None,
        intent: ActionIntent | str = ActionIntent.EVIDENCE_CREATING,
        intent_tags: list[str] | tuple[str, ...] | None = None,
        presentation_tags: list[str] | tuple[str, ...] | None = None,
    ) -> ActionableSuggestion:
        """Construct an ActionableSuggestion."""
        fam = family if isinstance(family, ActionFamily) else ActionFamily(family)
        inten = intent if isinstance(intent, ActionIntent) else ActionIntent(intent)
        entity = None
        if curriculum_entity_id is not None:
            stripped = curriculum_entity_id.strip()
            entity = stripped or None
        return cls(
            family=fam,
            curriculum_entity_id=entity,
            intent=inten,
            intent_tags=tuple(intent_tags or ()),
            presentation_tags=tuple(presentation_tags or ()),
        )

    @classmethod
    def from_selected(
        cls,
        selected: SelectedAction,
        *,
        intent_tags: list[str] | tuple[str, ...] | None = None,
        presentation_tags: list[str] | tuple[str, ...] | None = None,
    ) -> ActionableSuggestion:
        """Project SelectedAction into an actionable suggestion surface."""
        tags = list(intent_tags or ())
        if selected.intent.value not in tags:
            tags.insert(0, selected.intent.value)
        return cls.create(
            selected.family,
            curriculum_entity_id=selected.curriculum_entity_id,
            intent=selected.intent,
            intent_tags=tags,
            presentation_tags=presentation_tags,
        )
