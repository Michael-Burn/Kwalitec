"""Question-type strategy contracts for delivery validation and mapping."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from application.assessment.delivery.exceptions import InvalidResponseFormatError
from application.assessment.delivery.question_content import QuestionContent
from domain.assessment.enums import ItemType


@dataclass(frozen=True, slots=True)
class QuestionPresentationModel:
    """Neutral presentation model consumed by templates / renderers."""

    question_id: str
    item_type: str
    stem: str
    version: str
    options: tuple[dict[str, str], ...] = ()
    hints: tuple[str, ...] = ()
    placeholder: str | None = None
    unit_label: str | None = None
    accessibility_note: str | None = None
    input_name: str = "response"
    allows_multiple: bool = False
    is_numeric: bool = False
    is_text: bool = False
    is_confidence_only: bool = False
    attributes: dict[str, Any] = field(default_factory=dict)


class QuestionTypeStrategy(ABC):
    """Strategy for one ItemType: present, validate, map — no educational scoring."""

    item_type: ItemType

    @abstractmethod
    def presentation_model(self, content: QuestionContent) -> QuestionPresentationModel:
        """Build a presentation model from catalogue content."""

    @abstractmethod
    def validate(self, raw: Mapping[str, Any], content: QuestionContent) -> None:
        """Validate response format (required fields / shapes only)."""

    @abstractmethod
    def map_response(
        self, raw: Mapping[str, Any], content: QuestionContent
    ) -> dict[str, Any]:
        """Map raw form/API input to an observation response_payload."""


def _require_non_empty_str(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidResponseFormatError(f"{field_name} is required")
    return value.strip()


class MultipleChoiceStrategy(QuestionTypeStrategy):
    item_type = ItemType.MULTIPLE_CHOICE

    def presentation_model(self, content: QuestionContent) -> QuestionPresentationModel:
        return QuestionPresentationModel(
            question_id=content.question_id,
            item_type=content.item_type.value,
            stem=content.stem,
            version=content.version,
            options=tuple(
                {"option_id": o.option_id, "label": o.label} for o in content.options
            ),
            hints=content.hints,
            accessibility_note=content.accessibility_note,
            input_name="selected_option",
        )

    def validate(self, raw: Mapping[str, Any], content: QuestionContent) -> None:
        selected = _require_non_empty_str(raw.get("selected_option"), "selected_option")
        allowed = {o.option_id for o in content.options}
        if selected not in allowed:
            raise InvalidResponseFormatError("selected_option is not a valid choice")

    def map_response(
        self, raw: Mapping[str, Any], content: QuestionContent
    ) -> dict[str, Any]:
        self.validate(raw, content)
        return {
            "selected_option": str(raw["selected_option"]).strip(),
            "item_type": self.item_type.value,
        }


class MultipleResponseStrategy(QuestionTypeStrategy):
    item_type = ItemType.MULTIPLE_RESPONSE

    def presentation_model(self, content: QuestionContent) -> QuestionPresentationModel:
        return QuestionPresentationModel(
            question_id=content.question_id,
            item_type=content.item_type.value,
            stem=content.stem,
            version=content.version,
            options=tuple(
                {"option_id": o.option_id, "label": o.label} for o in content.options
            ),
            hints=content.hints,
            accessibility_note=content.accessibility_note,
            input_name="selected_options",
            allows_multiple=True,
        )

    def validate(self, raw: Mapping[str, Any], content: QuestionContent) -> None:
        selected = raw.get("selected_options")
        if isinstance(selected, str):
            selected = [selected] if selected.strip() else []
        if not isinstance(selected, list | tuple) or not selected:
            raise InvalidResponseFormatError("selected_options is required")
        allowed = {o.option_id for o in content.options}
        cleaned = [str(item).strip() for item in selected if str(item).strip()]
        if not cleaned:
            raise InvalidResponseFormatError("selected_options is required")
        if any(item not in allowed for item in cleaned):
            raise InvalidResponseFormatError(
                "selected_options contains an invalid choice"
            )

    def map_response(
        self, raw: Mapping[str, Any], content: QuestionContent
    ) -> dict[str, Any]:
        self.validate(raw, content)
        selected = raw.get("selected_options")
        if isinstance(selected, str):
            selected = [selected]
        cleaned = sorted({str(item).strip() for item in selected if str(item).strip()})
        return {
            "selected_options": cleaned,
            "item_type": self.item_type.value,
        }


class NumericStrategy(QuestionTypeStrategy):
    item_type = ItemType.NUMERIC

    def presentation_model(self, content: QuestionContent) -> QuestionPresentationModel:
        return QuestionPresentationModel(
            question_id=content.question_id,
            item_type=content.item_type.value,
            stem=content.stem,
            version=content.version,
            hints=content.hints,
            placeholder=content.placeholder or "Enter a number",
            unit_label=content.unit_label,
            accessibility_note=content.accessibility_note,
            input_name="entered_value",
            is_numeric=True,
        )

    def validate(self, raw: Mapping[str, Any], content: QuestionContent) -> None:
        value = raw.get("entered_value")
        if value is None or (isinstance(value, str) and not value.strip()):
            raise InvalidResponseFormatError("entered_value is required")
        try:
            float(str(value).strip())
        except (TypeError, ValueError) as exc:
            raise InvalidResponseFormatError(
                "entered_value must be a number"
            ) from exc

    def map_response(
        self, raw: Mapping[str, Any], content: QuestionContent
    ) -> dict[str, Any]:
        self.validate(raw, content)
        return {
            "entered_value": str(raw["entered_value"]).strip(),
            "item_type": self.item_type.value,
        }


class FormulaStrategy(QuestionTypeStrategy):
    item_type = ItemType.FORMULA

    def presentation_model(self, content: QuestionContent) -> QuestionPresentationModel:
        return QuestionPresentationModel(
            question_id=content.question_id,
            item_type=content.item_type.value,
            stem=content.stem,
            version=content.version,
            hints=content.hints,
            placeholder=content.placeholder or "Enter an expression",
            accessibility_note=content.accessibility_note,
            input_name="entered_expression",
            is_text=True,
        )

    def validate(self, raw: Mapping[str, Any], content: QuestionContent) -> None:
        _require_non_empty_str(raw.get("entered_expression"), "entered_expression")

    def map_response(
        self, raw: Mapping[str, Any], content: QuestionContent
    ) -> dict[str, Any]:
        self.validate(raw, content)
        return {
            "entered_expression": str(raw["entered_expression"]).strip(),
            "item_type": self.item_type.value,
        }


class FreeTextStrategy(QuestionTypeStrategy):
    item_type = ItemType.FREE_TEXT

    def presentation_model(self, content: QuestionContent) -> QuestionPresentationModel:
        return QuestionPresentationModel(
            question_id=content.question_id,
            item_type=content.item_type.value,
            stem=content.stem,
            version=content.version,
            hints=content.hints,
            placeholder=content.placeholder or "Write a short answer",
            accessibility_note=content.accessibility_note,
            input_name="entered_text",
            is_text=True,
        )

    def validate(self, raw: Mapping[str, Any], content: QuestionContent) -> None:
        _require_non_empty_str(raw.get("entered_text"), "entered_text")

    def map_response(
        self, raw: Mapping[str, Any], content: QuestionContent
    ) -> dict[str, Any]:
        self.validate(raw, content)
        return {
            "entered_text": str(raw["entered_text"]).strip(),
            "item_type": self.item_type.value,
        }


class WorkedSolutionStrategy(QuestionTypeStrategy):
    item_type = ItemType.WORKED_SOLUTION

    def presentation_model(self, content: QuestionContent) -> QuestionPresentationModel:
        return QuestionPresentationModel(
            question_id=content.question_id,
            item_type=content.item_type.value,
            stem=content.stem,
            version=content.version,
            hints=content.hints,
            placeholder=content.placeholder or "Describe your steps",
            accessibility_note=content.accessibility_note,
            input_name="entered_steps",
            is_text=True,
        )

    def validate(self, raw: Mapping[str, Any], content: QuestionContent) -> None:
        _require_non_empty_str(raw.get("entered_steps"), "entered_steps")

    def map_response(
        self, raw: Mapping[str, Any], content: QuestionContent
    ) -> dict[str, Any]:
        self.validate(raw, content)
        return {
            "entered_steps": str(raw["entered_steps"]).strip(),
            "item_type": self.item_type.value,
        }


class ConfidenceRatingStrategy(QuestionTypeStrategy):
    item_type = ItemType.CONFIDENCE_RATING

    def presentation_model(self, content: QuestionContent) -> QuestionPresentationModel:
        return QuestionPresentationModel(
            question_id=content.question_id,
            item_type=content.item_type.value,
            stem=content.stem,
            version=content.version,
            hints=content.hints,
            accessibility_note=content.accessibility_note,
            input_name="confidence",
            is_confidence_only=True,
        )

    def validate(self, raw: Mapping[str, Any], content: QuestionContent) -> None:
        value = raw.get("confidence")
        try:
            level = int(value)
        except (TypeError, ValueError) as exc:
            raise InvalidResponseFormatError(
                "confidence must be an integer from 1 to 5"
            ) from exc
        if level < 1 or level > 5:
            raise InvalidResponseFormatError(
                "confidence must be an integer from 1 to 5"
            )

    def map_response(
        self, raw: Mapping[str, Any], content: QuestionContent
    ) -> dict[str, Any]:
        self.validate(raw, content)
        return {
            "confidence": int(raw["confidence"]),
            "item_type": self.item_type.value,
        }


class ReflectionStrategy(QuestionTypeStrategy):
    item_type = ItemType.REFLECTION

    def presentation_model(self, content: QuestionContent) -> QuestionPresentationModel:
        return QuestionPresentationModel(
            question_id=content.question_id,
            item_type=content.item_type.value,
            stem=content.stem,
            version=content.version,
            hints=content.hints,
            placeholder=content.placeholder or "Share a brief reflection",
            accessibility_note=content.accessibility_note,
            input_name="reflection_text",
            is_text=True,
        )

    def validate(self, raw: Mapping[str, Any], content: QuestionContent) -> None:
        _require_non_empty_str(raw.get("reflection_text"), "reflection_text")

    def map_response(
        self, raw: Mapping[str, Any], content: QuestionContent
    ) -> dict[str, Any]:
        self.validate(raw, content)
        return {
            "reflection_text": str(raw["reflection_text"]).strip(),
            "item_type": self.item_type.value,
        }


class ConceptLinkingStrategy(QuestionTypeStrategy):
    item_type = ItemType.CONCEPT_LINKING

    def presentation_model(self, content: QuestionContent) -> QuestionPresentationModel:
        return QuestionPresentationModel(
            question_id=content.question_id,
            item_type=content.item_type.value,
            stem=content.stem,
            version=content.version,
            options=tuple(
                {"option_id": o.option_id, "label": o.label} for o in content.options
            ),
            hints=content.hints,
            accessibility_note=content.accessibility_note,
            input_name="linked_concepts",
            allows_multiple=True,
        )

    def validate(self, raw: Mapping[str, Any], content: QuestionContent) -> None:
        selected = raw.get("linked_concepts")
        if isinstance(selected, str):
            selected = [selected] if selected.strip() else []
        if not isinstance(selected, list | tuple) or not selected:
            raise InvalidResponseFormatError("linked_concepts is required")
        allowed = {o.option_id for o in content.options}
        cleaned = [str(item).strip() for item in selected if str(item).strip()]
        if not cleaned:
            raise InvalidResponseFormatError("linked_concepts is required")
        if any(item not in allowed for item in cleaned):
            raise InvalidResponseFormatError(
                "linked_concepts contains an invalid concept"
            )

    def map_response(
        self, raw: Mapping[str, Any], content: QuestionContent
    ) -> dict[str, Any]:
        self.validate(raw, content)
        selected = raw.get("linked_concepts")
        if isinstance(selected, str):
            selected = [selected]
        cleaned = sorted({str(item).strip() for item in selected if str(item).strip()})
        return {
            "linked_concepts": cleaned,
            "item_type": self.item_type.value,
        }


_STRATEGIES: dict[ItemType, QuestionTypeStrategy] = {
    ItemType.MULTIPLE_CHOICE: MultipleChoiceStrategy(),
    ItemType.MULTIPLE_RESPONSE: MultipleResponseStrategy(),
    ItemType.NUMERIC: NumericStrategy(),
    ItemType.FORMULA: FormulaStrategy(),
    ItemType.FREE_TEXT: FreeTextStrategy(),
    ItemType.WORKED_SOLUTION: WorkedSolutionStrategy(),
    ItemType.CONFIDENCE_RATING: ConfidenceRatingStrategy(),
    ItemType.REFLECTION: ReflectionStrategy(),
    ItemType.CONCEPT_LINKING: ConceptLinkingStrategy(),
}


def get_strategy(item_type: ItemType | str) -> QuestionTypeStrategy:
    """Resolve the strategy for an item type."""
    key = ItemType(item_type) if isinstance(item_type, str) else item_type
    try:
        return _STRATEGIES[key]
    except KeyError as exc:
        raise InvalidResponseFormatError(
            f"unsupported item type: {item_type}"
        ) from exc


def all_strategies() -> tuple[QuestionTypeStrategy, ...]:
    return tuple(_STRATEGIES.values())
