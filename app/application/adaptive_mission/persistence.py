"""Persistence for Adaptive Mission Engine (AME-001).

Does not store Twin mastery/gap/recommendation rows — those remain in SDT-001.
"""

from __future__ import annotations

import json
import uuid
from datetime import date
from typing import Any

from app.domain.adaptive_mission.adaptive_mission import AdaptiveMission
from app.domain.adaptive_mission.mission import Mission, MissionStatus
from app.domain.adaptive_mission.mission_completion import MissionCompletion
from app.domain.adaptive_mission.mission_objective import MissionObjective
from app.domain.adaptive_mission.mission_outcome import MissionOutcome
from app.domain.adaptive_mission.mission_plan import MissionPlan
from app.domain.adaptive_mission.mission_priority import MissionPriority
from app.domain.adaptive_mission.mission_progress import MissionProgress
from app.domain.adaptive_mission.mission_reason import MissionReason
from app.domain.adaptive_mission.mission_schedule import MissionSchedule
from app.domain.adaptive_mission.mission_step import (
    ActivityType,
    MissionActivity,
    MissionStep,
)
from app.extensions import db
from app.models.adaptive_mission import (
    AmeAdaptiveMission,
    AmeMissionCompletion,
    AmeMissionFeedback,
    AmeMissionHistory,
    AmeMissionProgress,
    AmeMissionStep,
)


def _dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)


def _loads(raw: str | None, default: Any) -> Any:
    if not raw:
        return default
    return json.loads(raw)


class AdaptiveMissionPersistenceService:
    """Load and persist AdaptiveMission aggregates."""

    def save_mission(self, mission: AdaptiveMission) -> AmeAdaptiveMission:
        row = AmeAdaptiveMission.query.filter_by(mission_id=mission.mission_id).first()
        payload = self._mission_row_payload(mission)
        if row is None:
            row = AmeAdaptiveMission(**payload)
            db.session.add(row)
        else:
            for key, value in payload.items():
                setattr(row, key, value)

        AmeMissionStep.query.filter_by(mission_id=mission.mission_id).delete()
        for step in mission.steps:
            db.session.add(
                AmeMissionStep(
                    step_id=step.step_id,
                    mission_id=mission.mission_id,
                    step_order=step.order,
                    activity_type=step.activity.activity_type.value,
                    concept_id=step.activity.concept_id,
                    title=step.activity.title,
                    estimated_minutes=step.activity.estimated_minutes,
                    reason=step.activity.reason or "",
                    success_criterion=step.success_criterion or "",
                    evidence_json=_dumps(list(step.activity.evidence_references)),
                    completed=bool(step.completed),
                )
            )

        progress_row = AmeMissionProgress.query.filter_by(
            mission_id=mission.mission_id
        ).first()
        progress_payload = {
            "progress_id": mission.progress.progress_id,
            "mission_id": mission.mission_id,
            "steps_total": mission.progress.steps_total,
            "steps_completed": mission.progress.steps_completed,
            "percent_complete": mission.progress.percent_complete,
            "last_step_id": mission.progress.last_step_id or "",
            "note": mission.progress.note or "",
            "updated_at": mission.progress.updated_at or mission.updated_at,
        }
        if progress_row is None:
            db.session.add(AmeMissionProgress(**progress_payload))
        else:
            for key, value in progress_payload.items():
                setattr(progress_row, key, value)

        if mission.completion is not None:
            self.save_completion(mission.completion)

        return row

    def save_completion(self, completion: MissionCompletion) -> AmeMissionCompletion:
        row = AmeMissionCompletion.query.filter_by(
            mission_id=completion.mission_id
        ).first()
        payload = {
            "completion_id": completion.completion_id,
            "mission_id": completion.mission_id,
            "twin_id": completion.twin_id,
            "completed_at": completion.completed_at,
            "steps_completed": completion.steps_completed,
            "steps_total": completion.steps_total,
            "outcome_achieved": completion.outcome_achieved,
            "reflection_response": completion.reflection_response or "",
            "feedback_summary": completion.feedback_summary or "",
        }
        if row is None:
            row = AmeMissionCompletion(**payload)
            db.session.add(row)
        else:
            for key, value in payload.items():
                setattr(row, key, value)
        return row

    def append_history(
        self,
        *,
        mission_id: str,
        twin_id: str,
        event_type: str,
        summary: str,
        payload: dict[str, Any] | None = None,
        history_id: str | None = None,
        created_at=None,
    ) -> AmeMissionHistory:
        row = AmeMissionHistory(
            history_id=history_id or f"amh-{uuid.uuid4().hex[:16]}",
            mission_id=mission_id,
            twin_id=twin_id,
            event_type=event_type,
            summary=summary,
            payload_json=_dumps(payload or {}),
            created_at=created_at,
        )
        db.session.add(row)
        return row

    def append_feedback(
        self,
        *,
        mission_id: str,
        twin_id: str,
        comment: str = "",
        rating: int | None = None,
        feedback_id: str | None = None,
    ) -> AmeMissionFeedback:
        row = AmeMissionFeedback(
            feedback_id=feedback_id or f"amf-{uuid.uuid4().hex[:16]}",
            mission_id=mission_id,
            twin_id=twin_id,
            rating=rating,
            comment=comment or "",
        )
        db.session.add(row)
        return row

    def load_mission(self, mission_id: str) -> AdaptiveMission | None:
        row = AmeAdaptiveMission.query.filter_by(mission_id=mission_id).first()
        if row is None:
            return None
        return self._hydrate(row)

    def load_active_for_twin(self, twin_id: str) -> AdaptiveMission | None:
        row = (
            AmeAdaptiveMission.query.filter_by(
                twin_id=twin_id, status=MissionStatus.ACTIVE.value
            )
            .order_by(AmeAdaptiveMission.updated_at.desc())
            .first()
        )
        if row is None:
            return None
        return self._hydrate(row)

    def list_for_twin(
        self,
        twin_id: str,
        *,
        limit: int = 50,
    ) -> list[AdaptiveMission]:
        rows = (
            AmeAdaptiveMission.query.filter_by(twin_id=twin_id)
            .order_by(
                AmeAdaptiveMission.mission_date.desc(),
                AmeAdaptiveMission.created_at.desc(),
            )
            .limit(limit)
            .all()
        )
        return [self._hydrate(row) for row in rows]

    def list_history_for_twin(
        self,
        twin_id: str,
        *,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        rows = (
            AmeMissionHistory.query.filter_by(twin_id=twin_id)
            .order_by(AmeMissionHistory.created_at.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "history_id": r.history_id,
                "mission_id": r.mission_id,
                "twin_id": r.twin_id,
                "event_type": r.event_type,
                "summary": r.summary,
                "payload": _loads(r.payload_json, {}),
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]

    def supersede_active(
        self,
        twin_id: str,
        *,
        except_mission_id: str | None = None,
        updated_at=None,
    ) -> list[str]:
        """Mark other ACTIVE missions for the twin as SUPERSEDED."""
        query = AmeAdaptiveMission.query.filter_by(
            twin_id=twin_id, status=MissionStatus.ACTIVE.value
        )
        superseded: list[str] = []
        for row in query.all():
            if except_mission_id and row.mission_id == except_mission_id:
                continue
            row.status = MissionStatus.SUPERSEDED.value
            row.updated_at = updated_at or row.updated_at
            superseded.append(row.mission_id)
            self.append_history(
                mission_id=row.mission_id,
                twin_id=twin_id,
                event_type="superseded",
                summary="Superseded by a newer adaptive mission.",
                created_at=updated_at,
            )
        return superseded

    def mission_as_dict(self, mission: AdaptiveMission) -> dict[str, Any]:
        return {
            "mission_id": mission.mission_id,
            "twin_id": mission.twin_id,
            "student_id": mission.student_id,
            "mission_date": mission.mission_date.isoformat(),
            "status": mission.status.value,
            "goal": mission.goal,
            "priority": mission.priority.value,
            "educational_objective": mission.objective.statement,
            "primary_concept_id": mission.objective.primary_concept_id,
            "concepts_covered": list(mission.concepts_covered),
            "estimated_duration_minutes": mission.estimated_duration_minutes,
            "reason": {
                "summary": mission.reason.summary,
                "educational_explanation": mission.reason.educational_explanation,
                "recommendation_ids": list(mission.reason.recommendation_ids),
                "gap_ids": list(mission.reason.gap_ids),
                "recovery_path_concept_ids": list(
                    mission.reason.recovery_path_concept_ids
                ),
                "evidence_ids": list(mission.reason.evidence_ids),
                "graph_influence": mission.reason.graph_influence,
            },
            "expected_outcome": mission.expected_outcome.statement,
            "success_criteria": list(mission.success_criteria),
            "reflection_prompt": mission.reflection_prompt,
            "evidence_references": list(mission.evidence_references),
            "source_recommendation_ids": list(mission.source_recommendation_ids),
            "source_gap_ids": list(mission.source_gap_ids),
            "reasoning_run_id": mission.reasoning_run_id,
            "validation_passed": mission.validation_passed,
            "validation_summary": mission.validation_summary,
            "schedule": {
                "total_minutes": mission.schedule.total_minutes,
                "focus_block_minutes": mission.schedule.focus_block_minutes,
                "reflection_minutes": mission.schedule.reflection_minutes,
                "allocation_note": mission.schedule.allocation_note,
            },
            "steps": [
                {
                    "step_id": step.step_id,
                    "order": step.order,
                    "activity_type": step.activity.activity_type.value,
                    "concept_id": step.activity.concept_id,
                    "title": step.activity.title,
                    "estimated_minutes": step.activity.estimated_minutes,
                    "reason": step.activity.reason,
                    "success_criterion": step.success_criterion,
                    "completed": step.completed,
                    "evidence_references": list(step.activity.evidence_references),
                }
                for step in mission.steps
            ],
            "progress": {
                "progress_id": mission.progress.progress_id,
                "steps_total": mission.progress.steps_total,
                "steps_completed": mission.progress.steps_completed,
                "percent_complete": mission.progress.percent_complete,
                "last_step_id": mission.progress.last_step_id,
                "note": mission.progress.note,
            },
            "mission_card": mission.as_mission_card(),
            "version": mission.version,
            "created_at": (
                mission.created_at.isoformat()
                if mission.created_at
                else None
            ),
            "updated_at": (
                mission.updated_at.isoformat()
                if mission.updated_at
                else None
            ),
        }

    def _mission_row_payload(self, mission: AdaptiveMission) -> dict[str, Any]:
        return {
            "mission_id": mission.mission_id,
            "twin_id": mission.twin_id,
            "student_id": mission.student_id,
            "mission_date": mission.mission_date,
            "status": mission.status.value,
            "goal": mission.goal,
            "priority": mission.priority.value,
            "educational_objective": mission.objective.statement,
            "primary_concept_id": mission.objective.primary_concept_id,
            "concepts_json": _dumps(list(mission.concepts_covered)),
            "estimated_duration_minutes": mission.estimated_duration_minutes,
            "reason_summary": mission.reason.summary,
            "educational_explanation": mission.reason.educational_explanation,
            "expected_outcome": mission.expected_outcome.statement,
            "success_criteria_json": _dumps(list(mission.success_criteria)),
            "reflection_prompt": mission.reflection_prompt,
            "evidence_json": _dumps(list(mission.evidence_references)),
            "source_recommendation_ids_json": _dumps(
                list(mission.source_recommendation_ids)
            ),
            "source_gap_ids_json": _dumps(list(mission.source_gap_ids)),
            "recovery_path_json": _dumps(
                list(mission.reason.recovery_path_concept_ids)
            ),
            "reasoning_run_id": mission.reasoning_run_id or "",
            "schedule_json": _dumps(
                {
                    "total_minutes": mission.schedule.total_minutes,
                    "focus_block_minutes": mission.schedule.focus_block_minutes,
                    "reflection_minutes": mission.schedule.reflection_minutes,
                    "allocation_note": mission.schedule.allocation_note,
                }
            ),
            "plan_json": _dumps(
                {
                    "plan_id": mission.plan.plan_id,
                    "objective_id": mission.objective.objective_id,
                    "supporting_concept_ids": list(
                        mission.objective.supporting_concept_ids
                    ),
                }
            ),
            "reason_json": _dumps(
                {
                    "summary": mission.reason.summary,
                    "educational_explanation": mission.reason.educational_explanation,
                    "decision_references": list(mission.reason.decision_references),
                    "graph_influence": mission.reason.graph_influence,
                }
            ),
            "outcome_json": _dumps(
                {
                    "outcome_id": mission.expected_outcome.outcome_id,
                    "statement": mission.expected_outcome.statement,
                    "target_concept_id": mission.expected_outcome.target_concept_id,
                    "expected_mastery_delta": (
                        mission.expected_outcome.expected_mastery_delta
                    ),
                    "success_signals": list(mission.expected_outcome.success_signals),
                }
            ),
            "validation_passed": bool(mission.validation_passed),
            "validation_summary": mission.validation_summary or "",
            "version": mission.version,
            "created_at": mission.created_at,
            "updated_at": mission.updated_at,
        }

    def _hydrate(self, row: AmeAdaptiveMission) -> AdaptiveMission:
        step_rows = (
            AmeMissionStep.query.filter_by(mission_id=row.mission_id)
            .order_by(AmeMissionStep.step_order.asc())
            .all()
        )
        steps = tuple(
            MissionStep(
                step_id=s.step_id,
                order=s.step_order,
                activity=MissionActivity(
                    activity_type=ActivityType(s.activity_type),
                    concept_id=s.concept_id,
                    title=s.title,
                    estimated_minutes=s.estimated_minutes,
                    reason=s.reason or "",
                    evidence_references=tuple(_loads(s.evidence_json, [])),
                ),
                success_criterion=s.success_criterion or "",
                completed=bool(s.completed),
            )
            for s in step_rows
        )
        progress_row = AmeMissionProgress.query.filter_by(
            mission_id=row.mission_id
        ).first()
        if progress_row is None:
            progress = MissionProgress.empty(
                mission_id=row.mission_id,
                progress_id=f"prog-{row.mission_id}",
            )
        else:
            progress = MissionProgress(
                progress_id=progress_row.progress_id,
                mission_id=row.mission_id,
                steps_total=progress_row.steps_total,
                steps_completed=progress_row.steps_completed,
                percent_complete=progress_row.percent_complete,
                last_step_id=progress_row.last_step_id or "",
                updated_at=progress_row.updated_at,
                note=progress_row.note or "",
            )

        completion_row = AmeMissionCompletion.query.filter_by(
            mission_id=row.mission_id
        ).first()
        completion = None
        if completion_row is not None:
            completion = MissionCompletion(
                completion_id=completion_row.completion_id,
                mission_id=completion_row.mission_id,
                twin_id=completion_row.twin_id,
                completed_at=completion_row.completed_at,
                steps_completed=completion_row.steps_completed,
                steps_total=completion_row.steps_total,
                outcome_achieved=bool(completion_row.outcome_achieved),
                reflection_response=completion_row.reflection_response or "",
                feedback_summary=completion_row.feedback_summary or "",
            )

        schedule_data = _loads(row.schedule_json, {})
        outcome_data = _loads(row.outcome_json, {})
        plan_data = _loads(row.plan_json, {})
        reason_data = _loads(row.reason_json, {})
        concepts = tuple(_loads(row.concepts_json, []))
        supporting = tuple(plan_data.get("supporting_concept_ids") or [])

        objective = MissionObjective(
            objective_id=str(plan_data.get("objective_id") or f"obj-{row.mission_id}"),
            statement=row.educational_objective,
            primary_concept_id=row.primary_concept_id,
            supporting_concept_ids=supporting,
            source_recommendation_id=(
                (_loads(row.source_recommendation_ids_json, []) or [""])[0]
            ),
            source_gap_id=(_loads(row.source_gap_ids_json, []) or [""])[0],
        )
        plan = MissionPlan(
            plan_id=str(plan_data.get("plan_id") or f"plan-{row.mission_id}"),
            objective=objective,
            steps=steps,
            concepts_covered=concepts,
            estimated_duration_minutes=row.estimated_duration_minutes,
        )
        schedule = MissionSchedule(
            total_minutes=int(
                schedule_data.get("total_minutes") or row.estimated_duration_minutes
            ),
            focus_block_minutes=int(
                schedule_data.get("focus_block_minutes")
                or max(1, row.estimated_duration_minutes - 5)
            ),
            reflection_minutes=int(schedule_data.get("reflection_minutes") or 5),
            allocation_note=str(schedule_data.get("allocation_note") or ""),
        )
        reason = MissionReason(
            summary=row.reason_summary,
            educational_explanation=row.educational_explanation,
            decision_references=tuple(reason_data.get("decision_references") or []),
            recommendation_ids=tuple(
                _loads(row.source_recommendation_ids_json, [])
            ),
            gap_ids=tuple(_loads(row.source_gap_ids_json, [])),
            recovery_path_concept_ids=tuple(_loads(row.recovery_path_json, [])),
            evidence_ids=tuple(_loads(row.evidence_json, [])),
            graph_influence=str(reason_data.get("graph_influence") or ""),
        )
        outcome = MissionOutcome(
            outcome_id=str(outcome_data.get("outcome_id") or f"out-{row.mission_id}"),
            statement=row.expected_outcome,
            target_concept_id=str(
                outcome_data.get("target_concept_id") or row.primary_concept_id
            ),
            expected_mastery_delta=float(
                outcome_data.get("expected_mastery_delta") or 0.0
            ),
            success_signals=tuple(outcome_data.get("success_signals") or []),
        )
        mission_date = row.mission_date
        if isinstance(mission_date, str):
            mission_date = date.fromisoformat(mission_date)

        return AdaptiveMission(
            identity=Mission(
                mission_id=row.mission_id,
                twin_id=row.twin_id,
                student_id=row.student_id,
                mission_date=mission_date,
                status=MissionStatus(row.status),
                goal=row.goal,
            ),
            objective=objective,
            plan=plan,
            schedule=schedule,
            reason=reason,
            expected_outcome=outcome,
            priority=MissionPriority(row.priority),
            success_criteria=tuple(_loads(row.success_criteria_json, [])),
            reflection_prompt=row.reflection_prompt or "",
            progress=progress,
            evidence_references=tuple(_loads(row.evidence_json, [])),
            concepts_covered=concepts,
            estimated_duration_minutes=row.estimated_duration_minutes,
            source_recommendation_ids=tuple(
                _loads(row.source_recommendation_ids_json, [])
            ),
            source_gap_ids=tuple(_loads(row.source_gap_ids_json, [])),
            reasoning_run_id=row.reasoning_run_id or "",
            validation_passed=bool(row.validation_passed),
            validation_summary=row.validation_summary or "",
            completion=completion,
            created_at=row.created_at,
            updated_at=row.updated_at,
            version=row.version,
        )
