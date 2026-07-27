"""Persistence orchestration for Student Digital Twin (SDT-001)."""

from __future__ import annotations

import json
from typing import Any

from app.domain.student_digital_twin.confidence import (
    ConfidenceState,
    confidence_band_from_score,
)
from app.domain.student_digital_twin.knowledge_gap import GapSeverity, KnowledgeGap
from app.domain.student_digital_twin.learning_state import LearningState
from app.domain.student_digital_twin.mastery import (
    MasteryMap,
    MasteryRecord,
    MasteryTrend,
)
from app.domain.student_digital_twin.observation import Observation, ObservationKind
from app.domain.student_digital_twin.prediction import Prediction, PredictionKind
from app.domain.student_digital_twin.reasoning import ReasoningRecord, ReasoningStep
from app.domain.student_digital_twin.recommendation import (
    Recommendation,
    RecommendationPriority,
)
from app.domain.student_digital_twin.student import Student
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin
from app.domain.student_digital_twin.timeline import Timeline
from app.extensions import db
from app.models.student_digital_twin import (
    SdtKnowledgeGap,
    SdtLearningStateSnapshot,
    SdtMasteryRecord,
    SdtObservation,
    SdtPrediction,
    SdtReasoningHistory,
    SdtRecommendation,
    SdtStudentDigitalTwin,
)


def _dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)


def _loads(raw: str | None, default: Any) -> Any:
    if not raw:
        return default
    return json.loads(raw)


class TwinPersistenceService:
    """Map between domain Twin aggregates and SDT ORM tables."""

    def save_twin_root(self, twin: StudentDigitalTwin) -> SdtStudentDigitalTwin:
        row = SdtStudentDigitalTwin.query.filter_by(twin_id=twin.twin_id).first()
        if row is None:
            row = SdtStudentDigitalTwin(twin_id=twin.twin_id)
            db.session.add(row)
        row.student_id = twin.student.student_id
        row.display_name = twin.student.display_name
        row.subject_code = twin.student.subject_code
        row.workspace_id = twin.student.workspace_id
        row.external_user_id = twin.student.external_user_id
        row.version = twin.version
        row.created_at = twin.created_at or row.created_at
        row.updated_at = twin.updated_at or row.updated_at
        return row

    def append_observation(self, observation: Observation) -> SdtObservation:
        existing = SdtObservation.query.filter_by(
            observation_id=observation.observation_id
        ).first()
        if existing is not None:
            raise ValueError(
                f"observation {observation.observation_id!r} already "
                "persisted (immutable)"
            )
        row = SdtObservation(
            observation_id=observation.observation_id,
            twin_id=observation.twin_id,
            student_id=observation.student_id,
            kind=observation.kind.value,
            recorded_at=observation.recorded_at,
            curriculum_entity_id=observation.curriculum_entity_id,
            curriculum_entity_kind=observation.curriculum_entity_kind,
            evidence_reference=observation.evidence_reference,
            provenance=observation.provenance,
            metadata_json=_dumps(dict(observation.metadata)),
        )
        db.session.add(row)
        return row

    def replace_inferences(self, twin: StudentDigitalTwin) -> None:
        """Replace current inference rows; append learning-state + reasoning history."""
        twin_id = twin.twin_id

        SdtMasteryRecord.query.filter_by(twin_id=twin_id).delete()
        SdtKnowledgeGap.query.filter_by(twin_id=twin_id).delete()
        SdtRecommendation.query.filter_by(twin_id=twin_id).delete()
        SdtPrediction.query.filter_by(twin_id=twin_id).delete()
        db.session.flush()

        for record in twin.mastery.records:
            db.session.add(
                SdtMasteryRecord(
                    mastery_id=record.mastery_id,
                    twin_id=twin_id,
                    concept_id=record.concept_id,
                    concept_title=record.concept_title,
                    mastery_score=record.mastery_score,
                    confidence=record.confidence,
                    trend=record.trend.value,
                    evidence_count=record.evidence_count,
                    supporting_evidence_json=_dumps(list(record.supporting_evidence)),
                    reason=record.reason,
                    last_updated=record.last_updated,
                )
            )

        for gap in twin.knowledge_gaps:
            db.session.add(
                SdtKnowledgeGap(
                    gap_id=gap.gap_id,
                    twin_id=twin_id,
                    concept_id=gap.concept_id,
                    concept_title=gap.concept_title,
                    severity=gap.severity.value,
                    confidence=gap.confidence,
                    likely_prerequisite_id=gap.likely_prerequisite_id,
                    likely_prerequisite_title=gap.likely_prerequisite_title,
                    supporting_evidence_json=_dumps(list(gap.supporting_evidence)),
                    retrieval_log_id=gap.retrieval_log_id,
                    estimated_recovery_effort=gap.estimated_recovery_effort,
                    reason=gap.reason,
                    identified_at=gap.identified_at,
                    is_active=True,
                )
            )

        for rec in twin.recommendations:
            db.session.add(
                SdtRecommendation(
                    recommendation_id=rec.recommendation_id,
                    twin_id=twin_id,
                    title=rec.title,
                    reason=rec.reason,
                    priority=rec.priority.value,
                    confidence=rec.confidence,
                    curriculum_entity_id=rec.curriculum_entity_id,
                    supporting_evidence_json=_dumps(list(rec.supporting_evidence)),
                    related_gap_id=rec.related_gap_id,
                    status=rec.status,
                    created_at=rec.created_at,
                    is_active=True,
                )
            )

        for pred in twin.predictions:
            db.session.add(
                SdtPrediction(
                    prediction_id=pred.prediction_id,
                    twin_id=twin_id,
                    kind=pred.kind.value,
                    value=pred.value,
                    confidence=pred.confidence,
                    horizon_days=pred.horizon_days,
                    supporting_evidence_json=_dumps(list(pred.supporting_evidence)),
                    reason=pred.reason,
                    algorithm_version=pred.algorithm_version,
                    created_at=pred.created_at,
                    is_active=True,
                )
            )

        state = twin.learning_state
        if state.snapshot_id:
            existing_snap = SdtLearningStateSnapshot.query.filter_by(
                snapshot_id=state.snapshot_id
            ).first()
            if existing_snap is None:
                db.session.add(
                    SdtLearningStateSnapshot(
                        snapshot_id=state.snapshot_id,
                        twin_id=twin_id,
                        knowledge=state.knowledge,
                        confidence=state.confidence,
                        retention=state.retention,
                        consistency=state.consistency,
                        momentum=state.momentum,
                        exam_readiness=state.exam_readiness,
                        evidence_count=state.evidence_count,
                        reason=state.reason,
                        computed_at=state.computed_at,
                    )
                )

        if twin.reasoning_history:
            latest = twin.reasoning_history[-1]
            existing_reason = SdtReasoningHistory.query.filter_by(
                reasoning_id=latest.reasoning_id
            ).first()
            if existing_reason is None:
                db.session.add(
                    SdtReasoningHistory(
                        reasoning_id=latest.reasoning_id,
                        twin_id=twin_id,
                        triggered_by=latest.triggered_by,
                        observation_ids_json=_dumps(list(latest.observation_ids)),
                        steps_json=_dumps(
                            [
                                {
                                    "code": s.code,
                                    "detail": s.detail,
                                    "inputs": dict(s.inputs),
                                    "outputs": dict(s.outputs),
                                }
                                for s in latest.steps
                            ]
                        ),
                        summary=latest.summary,
                        reasoning_version=latest.reasoning_version,
                        created_at=latest.created_at,
                    )
                )

        self.save_twin_root(twin)

    def load_twin(self, twin_id: str) -> StudentDigitalTwin | None:
        root = SdtStudentDigitalTwin.query.filter_by(twin_id=twin_id).first()
        if root is None:
            return None

        student = Student(
            student_id=root.student_id,
            display_name=root.display_name,
            subject_code=root.subject_code,
            workspace_id=root.workspace_id,
            external_user_id=root.external_user_id,
        )

        observations = tuple(
            Observation(
                observation_id=row.observation_id,
                kind=ObservationKind(row.kind),
                twin_id=row.twin_id,
                student_id=row.student_id,
                recorded_at=row.recorded_at,
                curriculum_entity_id=row.curriculum_entity_id,
                curriculum_entity_kind=row.curriculum_entity_kind,
                evidence_reference=row.evidence_reference,
                provenance=row.provenance,
                metadata=_loads(row.metadata_json, {}),
            )
            for row in SdtObservation.query.filter_by(twin_id=twin_id)
            .order_by(SdtObservation.recorded_at.asc(), SdtObservation.id.asc())
            .all()
        )

        mastery_rows = SdtMasteryRecord.query.filter_by(twin_id=twin_id).all()
        mastery = MasteryMap(
            records=tuple(
                MasteryRecord(
                    mastery_id=r.mastery_id,
                    twin_id=r.twin_id,
                    concept_id=r.concept_id,
                    concept_title=r.concept_title,
                    mastery_score=r.mastery_score,
                    confidence=r.confidence,
                    trend=MasteryTrend(r.trend),
                    evidence_count=r.evidence_count,
                    supporting_evidence=tuple(_loads(r.supporting_evidence_json, [])),
                    last_updated=r.last_updated,
                    reason=r.reason,
                )
                for r in mastery_rows
            )
        )

        gaps = tuple(
            KnowledgeGap(
                gap_id=r.gap_id,
                twin_id=r.twin_id,
                concept_id=r.concept_id,
                concept_title=r.concept_title,
                severity=GapSeverity(r.severity),
                confidence=r.confidence,
                likely_prerequisite_id=r.likely_prerequisite_id,
                likely_prerequisite_title=r.likely_prerequisite_title,
                supporting_evidence=tuple(_loads(r.supporting_evidence_json, [])),
                retrieval_log_id=r.retrieval_log_id,
                estimated_recovery_effort=r.estimated_recovery_effort,
                reason=r.reason,
                identified_at=r.identified_at,
            )
            for r in SdtKnowledgeGap.query.filter_by(
                twin_id=twin_id, is_active=True
            ).all()
            if _loads(r.supporting_evidence_json, [])
        )

        recommendations = tuple(
            Recommendation(
                recommendation_id=r.recommendation_id,
                twin_id=r.twin_id,
                title=r.title,
                reason=r.reason,
                priority=RecommendationPriority(r.priority),
                confidence=r.confidence,
                curriculum_entity_id=r.curriculum_entity_id,
                supporting_evidence=tuple(_loads(r.supporting_evidence_json, [])),
                related_gap_id=r.related_gap_id,
                created_at=r.created_at,
                status=r.status,
            )
            for r in SdtRecommendation.query.filter_by(
                twin_id=twin_id, is_active=True
            ).all()
        )

        predictions = tuple(
            Prediction(
                prediction_id=r.prediction_id,
                twin_id=r.twin_id,
                kind=PredictionKind(r.kind),
                value=r.value,
                confidence=r.confidence,
                horizon_days=r.horizon_days,
                supporting_evidence=tuple(_loads(r.supporting_evidence_json, [])),
                reason=r.reason,
                created_at=r.created_at,
                algorithm_version=r.algorithm_version,
            )
            for r in SdtPrediction.query.filter_by(
                twin_id=twin_id, is_active=True
            ).all()
        )

        latest_state_row = (
            SdtLearningStateSnapshot.query.filter_by(twin_id=twin_id)
            .order_by(
                SdtLearningStateSnapshot.computed_at.desc(),
                SdtLearningStateSnapshot.id.desc(),
            )
            .first()
        )
        if latest_state_row is None:
            learning_state = LearningState.empty()
        else:
            learning_state = LearningState(
                knowledge=latest_state_row.knowledge,
                confidence=latest_state_row.confidence,
                retention=latest_state_row.retention,
                consistency=latest_state_row.consistency,
                momentum=latest_state_row.momentum,
                exam_readiness=latest_state_row.exam_readiness,
                snapshot_id=latest_state_row.snapshot_id,
                computed_at=latest_state_row.computed_at,
                evidence_count=latest_state_row.evidence_count,
                reason=latest_state_row.reason,
            )

        confidence = ConfidenceState(
            score=learning_state.confidence,
            band=confidence_band_from_score(learning_state.confidence),
            evidence_count=learning_state.evidence_count,
            reason="loaded_from_learning_state",
            updated_at=learning_state.computed_at,
        )

        reasoning_history = tuple(
            ReasoningRecord(
                reasoning_id=r.reasoning_id,
                twin_id=r.twin_id,
                triggered_by=r.triggered_by,
                observation_ids=tuple(_loads(r.observation_ids_json, [])),
                steps=tuple(
                    ReasoningStep(
                        code=s["code"],
                        detail=s["detail"],
                        inputs=s.get("inputs") or {},
                        outputs=s.get("outputs") or {},
                    )
                    for s in _loads(r.steps_json, [])
                ),
                summary=r.summary,
                created_at=r.created_at,
                reasoning_version=r.reasoning_version,
            )
            for r in (
                SdtReasoningHistory.query.filter_by(twin_id=twin_id)
                .order_by(
                    SdtReasoningHistory.created_at.asc(),
                    SdtReasoningHistory.id.asc(),
                )
                .all()
            )
        )

        return StudentDigitalTwin(
            twin_id=root.twin_id,
            student=student,
            observations=observations,
            learning_state=learning_state,
            mastery=mastery,
            knowledge_gaps=gaps,
            confidence=confidence,
            recommendations=recommendations,
            predictions=predictions,
            timeline=Timeline(),
            reasoning_history=reasoning_history,
            created_at=root.created_at,
            updated_at=root.updated_at,
            version=root.version,
        )

    def list_state_snapshots(self, twin_id: str) -> list[LearningState]:
        rows = (
            SdtLearningStateSnapshot.query.filter_by(twin_id=twin_id)
            .order_by(
                SdtLearningStateSnapshot.computed_at.asc(),
                SdtLearningStateSnapshot.id.asc(),
            )
            .all()
        )
        return [
            LearningState(
                knowledge=r.knowledge,
                confidence=r.confidence,
                retention=r.retention,
                consistency=r.consistency,
                momentum=r.momentum,
                exam_readiness=r.exam_readiness,
                snapshot_id=r.snapshot_id,
                computed_at=r.computed_at,
                evidence_count=r.evidence_count,
                reason=r.reason,
            )
            for r in rows
        ]
