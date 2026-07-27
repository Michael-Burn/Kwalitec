"""Serialisers for Founder Twin diagnostics (JSON only)."""

from __future__ import annotations

from typing import Any

from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin


def twin_public(twin: StudentDigitalTwin) -> dict[str, Any]:
    return {
        "twin_id": twin.twin_id,
        "version": twin.version,
        "student": {
            "student_id": twin.student.student_id,
            "display_name": twin.student.display_name,
            "subject_code": twin.student.subject_code,
            "workspace_id": twin.student.workspace_id,
            "external_user_id": twin.student.external_user_id,
        },
        "observation_count": twin.observation_count,
        "learning_state": {
            "snapshot_id": twin.learning_state.snapshot_id,
            "knowledge": twin.learning_state.knowledge,
            "confidence": twin.learning_state.confidence,
            "retention": twin.learning_state.retention,
            "consistency": twin.learning_state.consistency,
            "momentum": twin.learning_state.momentum,
            "exam_readiness": twin.learning_state.exam_readiness,
            "evidence_count": twin.learning_state.evidence_count,
            "reason": twin.learning_state.reason,
            "computed_at": _dt(twin.learning_state.computed_at),
        },
        "confidence": {
            "score": twin.confidence.score,
            "band": twin.confidence.band.value,
            "evidence_count": twin.confidence.evidence_count,
            "reason": twin.confidence.reason,
        },
        "mastery_count": len(twin.mastery.records),
        "gap_count": len(twin.knowledge_gaps),
        "recommendation_count": len(twin.recommendations),
        "prediction_count": len(twin.predictions),
        "reasoning_count": len(twin.reasoning_history),
        "created_at": _dt(twin.created_at),
        "updated_at": _dt(twin.updated_at),
    }


def observation_public(obs: Any) -> dict[str, Any]:
    return {
        "observation_id": obs.observation_id,
        "kind": obs.kind.value if hasattr(obs.kind, "value") else obs.kind,
        "recorded_at": _dt(obs.recorded_at),
        "curriculum_entity_id": obs.curriculum_entity_id,
        "curriculum_entity_kind": obs.curriculum_entity_kind,
        "evidence_reference": obs.evidence_reference,
        "provenance": obs.provenance,
        "metadata": dict(obs.metadata),
    }


def mastery_public(record: Any) -> dict[str, Any]:
    return {
        "mastery_id": record.mastery_id,
        "concept_id": record.concept_id,
        "concept_title": record.concept_title,
        "mastery_score": record.mastery_score,
        "confidence": record.confidence,
        "trend": record.trend.value if hasattr(record.trend, "value") else record.trend,
        "evidence_count": record.evidence_count,
        "supporting_evidence": list(record.supporting_evidence),
        "reason": record.reason,
        "last_updated": _dt(record.last_updated),
    }


def gap_public(gap: Any) -> dict[str, Any]:
    return {
        "gap_id": gap.gap_id,
        "concept_id": gap.concept_id,
        "concept_title": gap.concept_title,
        "severity": (
            gap.severity.value if hasattr(gap.severity, "value") else gap.severity
        ),
        "confidence": gap.confidence,
        "likely_prerequisite_id": gap.likely_prerequisite_id,
        "likely_prerequisite_title": gap.likely_prerequisite_title,
        "supporting_evidence": list(gap.supporting_evidence),
        "retrieval_log_id": gap.retrieval_log_id,
        "estimated_recovery_effort": gap.estimated_recovery_effort,
        "reason": gap.reason,
        "identified_at": _dt(gap.identified_at),
    }


def recommendation_public(rec: Any) -> dict[str, Any]:
    return {
        "recommendation_id": rec.recommendation_id,
        "title": rec.title,
        "reason": rec.reason,
        "priority": (
            rec.priority.value if hasattr(rec.priority, "value") else rec.priority
        ),
        "confidence": rec.confidence,
        "curriculum_entity_id": rec.curriculum_entity_id,
        "supporting_evidence": list(rec.supporting_evidence),
        "related_gap_id": rec.related_gap_id,
        "status": rec.status,
        "created_at": _dt(rec.created_at),
    }


def prediction_public(pred: Any) -> dict[str, Any]:
    return {
        "prediction_id": pred.prediction_id,
        "kind": pred.kind.value if hasattr(pred.kind, "value") else pred.kind,
        "value": pred.value,
        "confidence": pred.confidence,
        "horizon_days": pred.horizon_days,
        "supporting_evidence": list(pred.supporting_evidence),
        "reason": pred.reason,
        "algorithm_version": pred.algorithm_version,
        "created_at": _dt(pred.created_at),
    }


def reasoning_public(record: Any) -> dict[str, Any]:
    return {
        "reasoning_id": record.reasoning_id,
        "triggered_by": record.triggered_by,
        "observation_ids": list(record.observation_ids),
        "summary": record.summary,
        "reasoning_version": record.reasoning_version,
        "created_at": _dt(record.created_at),
        "steps": [
            {
                "code": s.code,
                "detail": s.detail,
                "inputs": dict(s.inputs),
                "outputs": dict(s.outputs),
            }
            for s in record.steps
        ],
    }


def _dt(value: Any) -> str | None:
    if value is None:
        return None
    return value.isoformat()
