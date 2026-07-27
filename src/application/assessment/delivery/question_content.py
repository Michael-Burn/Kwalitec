"""Delivery-facing question content (stems, options) — not educational scoring."""

from __future__ import annotations

from dataclasses import dataclass, field

from domain.assessment.enums import ItemType


@dataclass(frozen=True, slots=True)
class ChoiceOption:
    """A single selectable option for MC / multi-response items."""

    option_id: str
    label: str


@dataclass(frozen=True, slots=True)
class QuestionContent:
    """Renderable content for one published assessment item version."""

    question_id: str
    item_type: ItemType
    stem: str
    version: str = "1"
    options: tuple[ChoiceOption, ...] = ()
    hints: tuple[str, ...] = ()
    placeholder: str | None = None
    unit_label: str | None = None
    accessibility_note: str | None = None
    attributes: dict[str, object] = field(default_factory=dict)
