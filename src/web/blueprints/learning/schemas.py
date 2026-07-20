"""Request validation and command/query construction for the Learning API."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import Any

from application.commands.complete_learning_episode import CompleteLearningEpisode
from application.commands.record_evidence import EvidenceItemSpec, RecordEvidence
from application.commands.start_learning_session import StartLearningSession
from application.errors import ApplicationError
from application.queries.get_learner_state import GetLearnerState
from application.queries.get_learning_trajectory import GetLearningTrajectory


def serialize_dto(dto: Any) -> dict[str, Any]:
    """Convert an application DTO dataclass into a JSON-ready mapping."""
    return asdict(dto)


def parse_start_learning_session(payload: Any) -> StartLearningSession:
    data = _require_object(payload)
    return StartLearningSession(episode_id=_require_str(data, "episode_id"))


def parse_complete_learning_episode(payload: Any) -> CompleteLearningEpisode:
    data = _require_object(payload)
    return CompleteLearningEpisode(
        episode_id=_require_str(data, "episode_id"),
        reflection_id=_require_str(data, "reflection_id"),
        reflection_type=_require_str(data, "reflection_type"),
        reflection_content=_require_str(data, "reflection_content"),
        outcome_id=_require_str(data, "outcome_id"),
        outcome_kind=_require_str(data, "outcome_kind"),
        outcome_summary=_require_str(data, "outcome_summary"),
        perceived_difficulty=_optional_str(data, "perceived_difficulty"),
        perceived_understanding=_optional_str(data, "perceived_understanding"),
    )


def parse_record_evidence(payload: Any) -> RecordEvidence:
    data = _require_object(payload)
    items_raw = data.get("items")
    if not isinstance(items_raw, list) or not items_raw:
        raise ApplicationError("items must be a non-empty list")
    items = tuple(
        _parse_evidence_item(item, index) for index, item in enumerate(items_raw)
    )
    return RecordEvidence(
        evidence_id=_require_str(data, "evidence_id"),
        student_id=_require_str(data, "student_id"),
        source_id=_require_str(data, "source_id"),
        source_kind=_require_str(data, "source_kind"),
        source_label=_require_str(data, "source_label"),
        context_id=_require_str(data, "context_id"),
        context_dimension=_require_str(data, "context_dimension"),
        context_summary=_require_str(data, "context_summary"),
        confidence_level=_require_str(data, "confidence_level"),
        strength_level=_require_str(data, "strength_level"),
        occurred_at=_require_datetime(data, "occurred_at"),
        items=items,
        concept_ids=_optional_str_tuple(data, "concept_ids"),
        learning_episode_ids=_optional_str_tuple(data, "learning_episode_ids"),
        confidence_ratio=_optional_float(data, "confidence_ratio"),
        twin_id=_optional_str(data, "twin_id"),
        evidence_type_for_twin=_optional_str(data, "evidence_type_for_twin"),
    )


def parse_get_learner_state(student_id: str) -> GetLearnerState:
    cleaned = (student_id or "").strip()
    if not cleaned:
        raise ApplicationError("student_id is required")
    return GetLearnerState(student_id=cleaned)


def parse_get_learning_trajectory(student_id: str) -> GetLearningTrajectory:
    cleaned = (student_id or "").strip()
    if not cleaned:
        raise ApplicationError("student_id is required")
    return GetLearningTrajectory(student_id=cleaned)


def _require_object(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ApplicationError("request body must be a JSON object")
    return payload


def _require_str(data: dict[str, Any], field: str) -> str:
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ApplicationError(f"missing or invalid field: {field}")
    return value.strip()


def _optional_str(data: dict[str, Any], field: str) -> str | None:
    if field not in data or data[field] is None:
        return None
    value = data[field]
    if not isinstance(value, str):
        raise ApplicationError(f"invalid field: {field}")
    cleaned = value.strip()
    return cleaned or None


def _optional_float(data: dict[str, Any], field: str) -> float | None:
    if field not in data or data[field] is None:
        return None
    value = data[field]
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ApplicationError(f"invalid field: {field}")
    return float(value)


def _optional_str_tuple(data: dict[str, Any], field: str) -> tuple[str, ...]:
    if field not in data or data[field] is None:
        return ()
    value = data[field]
    if not isinstance(value, list):
        raise ApplicationError(f"invalid field: {field}")
    items: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise ApplicationError(f"invalid field: {field}[{index}]")
        items.append(item.strip())
    return tuple(items)


def _require_datetime(data: dict[str, Any], field: str) -> datetime:
    value = data.get(field)
    if isinstance(value, datetime):
        return value
    if not isinstance(value, str) or not value.strip():
        raise ApplicationError(f"missing or invalid field: {field}")
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text)
    except ValueError as exc:
        raise ApplicationError(f"invalid field: {field}") from exc


def _parse_evidence_item(raw: Any, index: int) -> EvidenceItemSpec:
    if not isinstance(raw, dict):
        raise ApplicationError(f"items[{index}] must be an object")
    return EvidenceItemSpec(
        item_id=_require_str(raw, "item_id"),
        kind=_require_str(raw, "kind"),
        summary=_require_str(raw, "summary"),
        concept_id=_optional_str(raw, "concept_id"),
        learning_episode_id=_optional_str(raw, "learning_episode_id"),
    )
