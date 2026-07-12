"""Twin snapshot JSON codec — Application persistence mapping only.

Serialises / deserialises complete Digital Twin aggregates for durable storage.
Never invents Mid beliefs, never fills empty domains, never reinterprets
provenance. Reconstructs via domain ``create()`` factories.

Framework-free: no Flask / ORM / SQLAlchemy.
"""

from __future__ import annotations

import json
from datetime import date, datetime
from typing import Any

from app.domain.twin.behaviour_state import BehaviourState
from app.domain.twin.digital_twin import DigitalTwin
from app.domain.twin.goal_state import GoalState
from app.domain.twin.identity_state import IdentityState
from app.domain.twin.knowledge_state import KnowledgeState, TopicMasteryRecord
from app.domain.twin.memory_state import MemoryState, RetentionRecord
from app.domain.twin.performance_state import PerformanceState, PerformanceSummary
from app.domain.twin.prediction_state import PredictionState

CODEC_FORMAT_VERSION = "1.0"


class TwinCodecError(ValueError):
    """Raised when snapshot payload cannot be mapped to a lawful Digital Twin."""


def encode_twin(twin: DigitalTwin) -> str:
    """Encode a complete Digital Twin to a JSON string."""
    payload = {
        "format_version": CODEC_FORMAT_VERSION,
        "twin": {
            "identity": _encode_identity(twin.identity),
            "goals": _encode_goals(twin.goals),
            "knowledge": _encode_knowledge(twin.knowledge),
            "memory": _encode_memory(twin.memory),
            "behaviour": _encode_behaviour(twin.behaviour),
            "performance": _encode_performance(twin.performance),
            "predictions": _encode_predictions(twin.predictions),
        },
    }
    return json.dumps(payload, separators=(",", ":"), sort_keys=True)


def decode_twin(payload: str | dict[str, Any]) -> DigitalTwin:
    """Decode a JSON Twin payload to a Digital Twin via ``create()`` factories.

    Raises:
        TwinCodecError: Corrupt, unreadable, or contract-violating cargo.
    """
    try:
        data = json.loads(payload) if isinstance(payload, str) else payload
    except (TypeError, json.JSONDecodeError) as exc:
        raise TwinCodecError(f"unreadable Twin payload: {exc}") from exc

    if not isinstance(data, dict):
        raise TwinCodecError("Twin payload must be a JSON object")

    version = data.get("format_version")
    if version not in (None, CODEC_FORMAT_VERSION, "1.0"):
        raise TwinCodecError(f"unsupported Twin format_version: {version!r}")

    twin_data = data.get("twin")
    if not isinstance(twin_data, dict):
        raise TwinCodecError("Twin payload missing twin object")

    try:
        identity = _decode_identity(twin_data.get("identity"))
        return DigitalTwin.create(
            identity,
            goals=_decode_goals(twin_data.get("goals")),
            knowledge=_decode_knowledge(twin_data.get("knowledge")),
            memory=_decode_memory(twin_data.get("memory")),
            behaviour=_decode_behaviour(twin_data.get("behaviour")),
            performance=_decode_performance(twin_data.get("performance")),
            predictions=_decode_predictions(twin_data.get("predictions")),
        )
    except TwinCodecError:
        raise
    except (TypeError, ValueError, KeyError, AttributeError) as exc:
        raise TwinCodecError(f"corrupt Twin payload: {exc}") from exc


def encode_provenance(provenance: dict[str, Any] | None) -> str | None:
    """Encode opaque provenance bag without reinterpretation."""
    if provenance is None:
        return None
    return json.dumps(dict(provenance), separators=(",", ":"), sort_keys=True)


def decode_provenance(payload: str | None) -> dict[str, Any] | None:
    """Decode opaque provenance bag; None stays None."""
    if payload is None:
        return None
    try:
        data = json.loads(payload)
    except (TypeError, json.JSONDecodeError) as exc:
        raise TwinCodecError(f"unreadable provenance payload: {exc}") from exc
    if not isinstance(data, dict):
        raise TwinCodecError("provenance payload must be a JSON object")
    return dict(data)


# ── Domain encode / decode ───────────────────────────────────────────────────


def _encode_date(value: date | None) -> str | None:
    return value.isoformat() if value is not None else None


def _encode_datetime(value: datetime | None) -> str | None:
    return value.isoformat() if value is not None else None


def _decode_date(value: object) -> date | None:
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return date.fromisoformat(value)
    raise TwinCodecError(f"invalid date value: {value!r}")


def _decode_datetime(value: object) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    raise TwinCodecError(f"invalid datetime value: {value!r}")


def _encode_identity(identity: IdentityState) -> dict[str, Any]:
    return {
        "student_id": identity.student_id,
        "curriculum_id": identity.curriculum_id,
        "current_exam": identity.current_exam,
        "target_sitting": _encode_date(identity.target_sitting),
    }


def _decode_identity(data: object) -> IdentityState:
    if not isinstance(data, dict):
        raise TwinCodecError("identity must be an object")
    return IdentityState.create(
        data["student_id"],
        curriculum_id=data.get("curriculum_id"),
        current_exam=data.get("current_exam"),
        target_sitting=_decode_date(data.get("target_sitting")),
    )


def _encode_goals(goals: GoalState) -> dict[str, Any]:
    return {
        "target_pass_probability": goals.target_pass_probability,
        "target_completion_date": _encode_date(goals.target_completion_date),
        "planned_study_hours_per_week": goals.planned_study_hours_per_week,
    }


def _decode_goals(data: object) -> GoalState:
    if data is None:
        return GoalState.create()
    if not isinstance(data, dict):
        raise TwinCodecError("goals must be an object")
    return GoalState.create(
        target_pass_probability=data.get("target_pass_probability"),
        target_completion_date=_decode_date(data.get("target_completion_date")),
        planned_study_hours_per_week=data.get("planned_study_hours_per_week"),
    )


def _encode_knowledge(knowledge: KnowledgeState) -> dict[str, Any]:
    return {
        "topic_mastery": [
            {
                "topic_id": record.topic_id,
                "mastery_belief": record.mastery_belief,
                "evidence_ids": list(record.evidence_ids),
            }
            for record in knowledge.topic_mastery
        ],
        "evidence_ids": list(knowledge.evidence_ids),
        "last_updated": _encode_datetime(knowledge.last_updated),
    }


def _decode_knowledge(data: object) -> KnowledgeState:
    if data is None:
        return KnowledgeState.create()
    if not isinstance(data, dict):
        raise TwinCodecError("knowledge must be an object")
    mastery_raw = data.get("topic_mastery") or []
    if not isinstance(mastery_raw, list):
        raise TwinCodecError("topic_mastery must be a list")
    mastery = [
        TopicMasteryRecord.create(
            item["topic_id"],
            mastery_belief=item.get("mastery_belief"),
            evidence_ids=item.get("evidence_ids"),
        )
        for item in mastery_raw
    ]
    return KnowledgeState.create(
        topic_mastery=mastery,
        evidence_ids=data.get("evidence_ids"),
        last_updated=_decode_datetime(data.get("last_updated")),
    )


def _encode_memory(memory: MemoryState) -> dict[str, Any]:
    return {
        "retention": [
            {
                "topic_id": record.topic_id,
                "retention_belief": record.retention_belief,
                "last_reinforced": _encode_datetime(record.last_reinforced),
            }
            for record in memory.retention
        ],
        "revision_ids": list(memory.revision_ids),
        "last_updated": _encode_datetime(memory.last_updated),
    }


def _decode_memory(data: object) -> MemoryState:
    if data is None:
        return MemoryState.create()
    if not isinstance(data, dict):
        raise TwinCodecError("memory must be an object")
    retention_raw = data.get("retention") or []
    if not isinstance(retention_raw, list):
        raise TwinCodecError("retention must be a list")
    retention = [
        RetentionRecord.create(
            item["topic_id"],
            retention_belief=item.get("retention_belief"),
            last_reinforced=_decode_datetime(item.get("last_reinforced")),
        )
        for item in retention_raw
    ]
    return MemoryState.create(
        retention=retention,
        revision_ids=data.get("revision_ids"),
        last_updated=_decode_datetime(data.get("last_updated")),
    )


def _encode_behaviour(behaviour: BehaviourState) -> dict[str, Any]:
    return {
        "consistency_metrics": dict(behaviour.consistency_metrics),
        "session_history_ids": list(behaviour.session_history_ids),
        "study_pattern_ids": list(behaviour.study_pattern_ids),
        "evidence_ids": list(behaviour.evidence_ids),
        "last_updated": _encode_datetime(behaviour.last_updated),
    }


def _decode_behaviour(data: object) -> BehaviourState:
    if data is None:
        return BehaviourState.create()
    if not isinstance(data, dict):
        raise TwinCodecError("behaviour must be an object")
    return BehaviourState.create(
        consistency_metrics=data.get("consistency_metrics"),
        session_history_ids=data.get("session_history_ids"),
        study_pattern_ids=data.get("study_pattern_ids"),
        evidence_ids=data.get("evidence_ids"),
        last_updated=_decode_datetime(data.get("last_updated")),
    )


def _encode_performance(performance: PerformanceState) -> dict[str, Any]:
    return {
        "assessment_ids": list(performance.assessment_ids),
        "performance_summaries": [
            {
                "scope_id": summary.scope_id,
                "summary": dict(summary.summary),
            }
            for summary in performance.performance_summaries
        ],
        "evidence_ids": list(performance.evidence_ids),
        "last_updated": _encode_datetime(performance.last_updated),
    }


def _decode_performance(data: object) -> PerformanceState:
    if data is None:
        return PerformanceState.create()
    if not isinstance(data, dict):
        raise TwinCodecError("performance must be an object")
    summaries_raw = data.get("performance_summaries") or []
    if not isinstance(summaries_raw, list):
        raise TwinCodecError("performance_summaries must be a list")
    summaries = [
        PerformanceSummary.create(
            item["scope_id"],
            summary=item.get("summary"),
        )
        for item in summaries_raw
    ]
    return PerformanceState.create(
        assessment_ids=data.get("assessment_ids"),
        performance_summaries=summaries,
        evidence_ids=data.get("evidence_ids"),
        last_updated=_decode_datetime(data.get("last_updated")),
    )


def _encode_predictions(predictions: PredictionState) -> dict[str, Any]:
    return {
        "readiness_snapshot": predictions.readiness_snapshot,
        "pass_probability_snapshot": predictions.pass_probability_snapshot,
        "as_of": _encode_datetime(predictions.as_of),
        "metadata": dict(predictions.metadata),
    }


def _decode_predictions(data: object) -> PredictionState:
    if data is None:
        return PredictionState.create()
    if not isinstance(data, dict):
        raise TwinCodecError("predictions must be an object")
    return PredictionState.create(
        readiness_snapshot=data.get("readiness_snapshot"),
        pass_probability_snapshot=data.get("pass_probability_snapshot"),
        as_of=_decode_datetime(data.get("as_of")),
        metadata=data.get("metadata"),
    )
