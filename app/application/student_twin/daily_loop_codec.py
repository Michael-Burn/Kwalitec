"""Opaque codec for Student Twin daily-loop persistence (SDT-004).

Serialises EvidenceEvent history + Estimated Knowledge / Mastery so Twin
updates remain reproducible after reload. Does not invent educational state.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.application.student_twin.twin_engine import StudentTwinEngine
from app.domain.student_twin.digital_twin import DigitalTwin
from app.domain.student_twin.evidence_event import EvidenceEvent
from app.domain.student_twin.learner import Learner

CODEC_FORMAT = "sdt004_daily_loop/1.0"


def encode_daily_loop_twin(
    twin: DigitalTwin, *, status: str = "active"
) -> dict[str, Any]:
    """Project a Twin to an opaque daily-loop document."""
    knowledge = {
        record.topic_id: round(record.knowledge_score, 6)
        for record in twin.knowledge.topic_records
    }
    mastery = {
        record.topic_id: round(record.mastery_score, 6)
        for record in twin.mastery.topic_records
    }
    return {
        "format": CODEC_FORMAT,
        "status": status,
        "twin_id": twin.twin_id,
        "learner_id": twin.learner_id,
        "subject_code": twin.identity.subject_code,
        "created_at": _iso(twin.created_at),
        "updated_at": _iso(twin.updated_at),
        "events": [_encode_event(event) for event in twin.history.events],
        "estimated_knowledge": knowledge,
        "estimated_mastery": mastery,
        "overall_knowledge": round(twin.knowledge.overall_score, 6),
        "overall_mastery": round(twin.mastery.overall_score, 6),
        "event_count": twin.event_count,
        "authority": "student_digital_twin",
    }


def decode_daily_loop_twin(
    document: dict[str, Any] | None,
    *,
    engine: StudentTwinEngine | None = None,
) -> tuple[DigitalTwin, str] | None:
    """Rebuild a Twin from a daily-loop document by replaying events.

    Returns ``(twin, status)`` or ``None`` when cargo is missing/corrupt.
    Replay keeps estimates deterministic and reproducible.
    """
    if not isinstance(document, dict) or not document.get("twin_id"):
        return None
    twin_id = str(document["twin_id"]).strip()
    learner_id = str(document.get("learner_id") or "").strip()
    if not twin_id or not learner_id:
        return None
    subject = document.get("subject_code")
    subject_code = str(subject).strip() if subject else None
    status = str(document.get("status") or "initialised").strip() or "initialised"
    created = _parse_dt(document.get("created_at"))
    eng = engine or StudentTwinEngine()
    twin = eng.create_twin(
        Learner.create(learner_id),
        twin_id=twin_id,
        subject_code=subject_code,
    )
    if created is not None:
        twin = DigitalTwin(
            identity=twin.identity,
            learner=twin.learner,
            version=twin.version,
            history=twin.history,
            knowledge=twin.knowledge,
            mastery=twin.mastery,
            confidence=twin.confidence,
            retention=twin.retention,
            readiness=twin.readiness,
            velocity=twin.velocity,
            weaknesses=twin.weaknesses,
            recommendations=twin.recommendations,
            evidence_profile=twin.evidence_profile,
            created_at=created,
            updated_at=created,
        )
    events: list[EvidenceEvent] = []
    for raw in document.get("events") or ():
        if isinstance(raw, dict):
            event = _decode_event(raw)
            if event is not None:
                events.append(event)
    if events:
        twin = eng.ingest_many(twin, events)
    return twin, status


def _encode_event(event: EvidenceEvent) -> dict[str, Any]:
    return {
        "event_id": event.event_id,
        "evidence_type": event.evidence_type.value,
        "occurred_at": event.occurred_at.isoformat(),
        "topic_id": event.topic_id,
        "outcome": event.outcome,
        "score": event.score,
        "confidence_rating": event.confidence_rating,
        "duration_seconds": event.duration_seconds,
        "source_ref": event.source_ref,
        "metadata": [list(pair) for pair in event.metadata],
    }


def _decode_event(raw: dict[str, Any]) -> EvidenceEvent | None:
    try:
        occurred = _parse_dt(raw.get("occurred_at"))
        if occurred is None:
            return None
        metadata_raw = raw.get("metadata") or ()
        metadata = tuple(
            (str(pair[0]), str(pair[1]))
            for pair in metadata_raw
            if isinstance(pair, list | tuple) and len(pair) == 2
        )
        return EvidenceEvent.create(
            str(raw["event_id"]),
            str(raw["evidence_type"]),
            occurred,
            topic_id=raw.get("topic_id"),
            outcome=raw.get("outcome"),
            score=raw.get("score"),
            confidence_rating=raw.get("confidence_rating"),
            duration_seconds=raw.get("duration_seconds"),
            source_ref=raw.get("source_ref"),
            metadata=metadata,
        )
    except (KeyError, TypeError, ValueError):
        return None


def _iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    when = value if value.tzinfo else value.replace(tzinfo=UTC)
    return when.isoformat()


def _parse_dt(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=UTC)
    if isinstance(value, str) and value.strip():
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError:
            return None
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
    return None
