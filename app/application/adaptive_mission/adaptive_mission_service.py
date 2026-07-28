"""AdaptiveMissionService — generate, validate, track daily adaptive missions.

Pipeline (deterministic):
  Student Digital Twin
    → Educational Reasoning decisions (already on Twin)
    → Learning Graph
    → Curriculum Retrieval (evidence enrichment)
    → Mission Prioritisation
    → Mission Construction
    → Mission Validation
    → Daily Mission

AP-002D5 planning path (decision-set explicit):
  Validated Twin belief + EducationalDecisionSet
    → MissionPlanningService
    → StudyMissionPlan
    → STOP (no Reasoning / Assessment / Tutor)
"""

from __future__ import annotations

import uuid
from datetime import UTC, date, datetime
from typing import Any

from app.application.adaptive_mission.persistence import (
    AdaptiveMissionPersistenceService,
)
from app.application.curriculum_retrieval.curriculum_retrieval_service import (
    CurriculumRetrievalService,
)
from app.application.learning_graph.learning_graph_service import LearningGraphService
from app.application.mission_engine.planning.mission_planning_service import (
    MissionPlanningService,
)
from app.application.mission_engine.planning.persistence import (
    PlanningPersistenceService,
)
from app.application.student_digital_twin.student_digital_twin_service import (
    StudentDigitalTwinService,
)
from app.domain.adaptive_mission.adaptive_mission import AdaptiveMission
from app.domain.adaptive_mission.construction import construct_mission
from app.domain.adaptive_mission.mission_completion import MissionCompletion
from app.domain.adaptive_mission.mission_progress import MissionProgress
from app.domain.adaptive_mission.prioritisation import (
    PrioritisationResult,
    prioritise_candidates,
)
from app.domain.adaptive_mission.validation import (
    MissionValidationResult,
    validate_mission,
)
from app.domain.curriculum_retrieval.profile import RetrievalProfile
from app.domain.curriculum_retrieval.query import RetrievalQuery
from app.domain.mission.planning.result import PlanningResult
from app.domain.reasoning.decisions.decision_set import EducationalDecisionSet
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin
from app.extensions import db


class AdaptiveMissionService:
    """Public facade for the Adaptive Mission Engine.

    Educational reasoning is never performed here. The engine consumes Twin
    recommendations / gaps / validated EducationalDecisionSet and Learning Graph
    recovery structure.
    """

    ENGINE_VERSION = "ame001.adaptive_mission_engine_v1"

    def __init__(
        self,
        *,
        twins: StudentDigitalTwinService | None = None,
        graphs: LearningGraphService | None = None,
        retrieval: CurriculumRetrievalService | None = None,
        persistence: AdaptiveMissionPersistenceService | None = None,
        planning: MissionPlanningService | None = None,
        planning_persistence: PlanningPersistenceService | None = None,
    ) -> None:
        self._twins = twins or StudentDigitalTwinService()
        self._graphs = graphs or LearningGraphService()
        self._retrieval = retrieval
        self._persistence = persistence or AdaptiveMissionPersistenceService()
        self._planning = planning or MissionPlanningService(
            persistence=planning_persistence or PlanningPersistenceService()
        )

    def generate_for_twin(
        self,
        twin_id: str,
        *,
        mission_date: date | None = None,
        available_minutes: int = 45,
        activate: bool = True,
        persist: bool = True,
        computed_at: datetime | None = None,
        enrich_evidence: bool = True,
    ) -> AdaptiveMission:
        """Generate today's adaptive mission from existing educational decisions."""
        twin = self._twins.get(twin_id)
        if twin is None:
            raise ValueError(f"Student Digital Twin {twin_id!r} not found")
        return self.generate_from_twin(
            twin,
            mission_date=mission_date,
            available_minutes=available_minutes,
            activate=activate,
            persist=persist,
            computed_at=computed_at,
            enrich_evidence=enrich_evidence,
        )

    def generate_from_twin(
        self,
        twin: StudentDigitalTwin,
        *,
        mission_date: date | None = None,
        available_minutes: int = 45,
        activate: bool = True,
        persist: bool = True,
        computed_at: datetime | None = None,
        enrich_evidence: bool = True,
    ) -> AdaptiveMission:
        """Full deterministic generation pipeline for one Twin."""
        when = computed_at or datetime.now(UTC).replace(tzinfo=None)
        day = mission_date or when.date()
        graph = self._graphs.get_for_twin(twin.twin_id)

        prioritisation = prioritise_candidates(
            recommendations=twin.recommendations,
            gaps=twin.knowledge_gaps,
            learning_state=twin.learning_state,
            observations=twin.observations,
            learning_graph=graph,
            computed_at=when,
        )
        if prioritisation.selected is None:
            raise ValueError(prioritisation.explanation)

        candidate = prioritisation.selected
        if enrich_evidence:
            candidate = self._enrich_candidate_evidence(twin, candidate)

        reasoning_run_id = ""
        if twin.reasoning_history:
            reasoning_run_id = twin.reasoning_history[-1].reasoning_id

        mission = construct_mission(
            twin_id=twin.twin_id,
            student_id=twin.student.student_id,
            mission_date=day,
            candidate=candidate,
            reasoning_run_id=reasoning_run_id,
            created_at=when,
            available_minutes=available_minutes,
        )

        validation = validate_mission(
            mission,
            twin=twin,
            learning_graph=graph,
            existing_active_mission_id=None,
            require_evidence=True,
        )
        mission = mission.with_validation(
            passed=validation.passed,
            summary=validation.summary,
            updated_at=when,
        )
        if not validation.passed:
            if persist:
                self._persistence.save_mission(mission)
                self._persistence.append_history(
                    mission_id=mission.mission_id,
                    twin_id=mission.twin_id,
                    event_type="rejected",
                    summary=validation.summary,
                    payload={"issues": [i.code for i in validation.issues]},
                    created_at=when,
                )
                db.session.commit()
            raise ValueError(validation.summary)

        if activate:
            if persist:
                self._persistence.supersede_active(
                    twin.twin_id,
                    except_mission_id=mission.mission_id,
                    updated_at=when,
                )
            mission = mission.activate(updated_at=when)

        if persist:
            self._persistence.save_mission(mission)
            self._persistence.append_history(
                mission_id=mission.mission_id,
                twin_id=mission.twin_id,
                event_type="generated",
                summary=prioritisation.explanation,
                payload={
                    "priority": mission.priority.value,
                    "concept_id": mission.objective.primary_concept_id,
                    "engine_version": self.ENGINE_VERSION,
                },
                created_at=when,
            )
            if activate:
                self._persistence.append_history(
                    mission_id=mission.mission_id,
                    twin_id=mission.twin_id,
                    event_type="activated",
                    summary="Adaptive mission activated for today.",
                    created_at=when,
                )
            db.session.commit()
        return mission

    def plan_from_decisions(
        self,
        twin: StudentDigitalTwin,
        decision_set: EducationalDecisionSet,
        *,
        available_minutes: int = 45,
        curriculum_position: str = "",
        planned_at: datetime | None = None,
        persist: bool = True,
        allow_idempotent_skip: bool = True,
    ) -> PlanningResult:
        """AP-002D5: plan a study mission from validated Twin decisions only.

        Consumes EducationalDecisionSet + Twin belief. Uses Learning Graph for
        recovery-path structure. Does not reason, does not interpret assessment
        evidence, and does not notify Tutor.
        """
        graph = self._graphs.get_for_twin(twin.twin_id)
        return self._planning.plan(
            twin,
            decision_set,
            learning_graph=graph,
            available_minutes=available_minutes,
            curriculum_position=curriculum_position,
            planned_at=planned_at,
            persist=persist,
            allow_idempotent_skip=allow_idempotent_skip,
        )

    @property
    def planning(self) -> MissionPlanningService:
        """AP-002D5 Mission planning service (Twin decisions → StudyMissionPlan)."""
        return self._planning

    def prioritise_for_twin(
        self,
        twin_id: str,
        *,
        computed_at: datetime | None = None,
    ) -> PrioritisationResult:
        twin = self._twins.get(twin_id)
        if twin is None:
            raise ValueError(f"Student Digital Twin {twin_id!r} not found")
        graph = self._graphs.get_for_twin(twin_id)
        return prioritise_candidates(
            recommendations=twin.recommendations,
            gaps=twin.knowledge_gaps,
            learning_state=twin.learning_state,
            observations=twin.observations,
            learning_graph=graph,
            computed_at=computed_at,
        )

    def validate(
        self,
        mission: AdaptiveMission,
        *,
        twin: StudentDigitalTwin | None = None,
        check_active_duplicate: bool = True,
    ) -> MissionValidationResult:
        twin = twin or self._twins.get(mission.twin_id)
        graph = self._graphs.get_for_twin(mission.twin_id)
        active = (
            self._persistence.load_active_for_twin(mission.twin_id)
            if check_active_duplicate
            else None
        )
        return validate_mission(
            mission,
            twin=twin,
            learning_graph=graph,
            existing_active_mission_id=(
                active.mission_id
                if active and active.mission_id != mission.mission_id
                else None
            ),
        )

    def get(self, mission_id: str) -> AdaptiveMission | None:
        return self._persistence.load_mission(mission_id)

    def get_active(self, twin_id: str) -> AdaptiveMission | None:
        return self._persistence.load_active_for_twin(twin_id)

    def list_for_twin(self, twin_id: str, *, limit: int = 50) -> list[AdaptiveMission]:
        return self._persistence.list_for_twin(twin_id, limit=limit)

    def history_for_twin(
        self, twin_id: str, *, limit: int = 100
    ) -> list[dict[str, Any]]:
        return self._persistence.list_history_for_twin(twin_id, limit=limit)

    def update_progress(
        self,
        mission_id: str,
        *,
        steps_completed: int,
        last_step_id: str = "",
        note: str = "",
        persist: bool = True,
        updated_at: datetime | None = None,
        emit_assessment: bool = True,
    ) -> AdaptiveMission:
        mission = self._persistence.load_mission(mission_id)
        if mission is None:
            raise ValueError(f"Adaptive mission {mission_id!r} not found")
        when = updated_at or datetime.now(UTC).replace(tzinfo=None)
        progress = MissionProgress.from_steps(
            progress_id=mission.progress.progress_id,
            mission_id=mission.mission_id,
            steps_total=len(mission.steps),
            steps_completed=steps_completed,
            last_step_id=last_step_id,
            updated_at=when,
            note=note,
        )
        updated = mission.with_progress(progress, updated_at=when)
        if persist:
            self._persistence.save_mission(updated)
            self._persistence.append_history(
                mission_id=updated.mission_id,
                twin_id=updated.twin_id,
                event_type="progress",
                summary=(
                    f"Progress {updated.progress.steps_completed}/"
                    f"{updated.progress.steps_total}"
                ),
                payload={
                    "percent_complete": updated.progress.percent_complete,
                    "last_step_id": last_step_id,
                },
                created_at=when,
            )
            db.session.commit()
        if emit_assessment and last_step_id and persist:
            self._emit_step_assessment(updated, last_step_id=last_step_id, when=when)
        return updated

    def complete(
        self,
        mission_id: str,
        *,
        reflection_response: str = "",
        feedback_summary: str = "",
        outcome_achieved: bool = True,
        persist: bool = True,
        completed_at: datetime | None = None,
        emit_assessment: bool = True,
        refresh_mission: bool = True,
    ) -> AdaptiveMission:
        mission = self._persistence.load_mission(mission_id)
        if mission is None:
            raise ValueError(f"Adaptive mission {mission_id!r} not found")
        when = completed_at or datetime.now(UTC).replace(tzinfo=None)
        completion = MissionCompletion(
            completion_id=f"amc-{uuid.uuid4().hex[:16]}",
            mission_id=mission.mission_id,
            twin_id=mission.twin_id,
            completed_at=when,
            steps_completed=mission.progress.steps_total,
            steps_total=mission.progress.steps_total,
            outcome_achieved=outcome_achieved,
            reflection_response=reflection_response,
            feedback_summary=feedback_summary,
        )
        progress = MissionProgress.from_steps(
            progress_id=mission.progress.progress_id,
            mission_id=mission.mission_id,
            steps_total=mission.progress.steps_total,
            steps_completed=mission.progress.steps_total,
            last_step_id=(
                mission.steps[-1].step_id if mission.steps else ""
            ),
            updated_at=when,
            note="completed",
        )
        updated = mission.with_progress(progress, updated_at=when).with_completion(
            completion, updated_at=when
        )
        if persist:
            self._persistence.save_mission(updated)
            self._persistence.append_history(
                mission_id=updated.mission_id,
                twin_id=updated.twin_id,
                event_type="completed",
                summary="Adaptive mission completed.",
                payload={"outcome_achieved": outcome_achieved},
                created_at=when,
            )
            if feedback_summary or reflection_response:
                self._persistence.append_feedback(
                    mission_id=updated.mission_id,
                    twin_id=updated.twin_id,
                    comment=feedback_summary or reflection_response,
                )
            db.session.commit()
        if emit_assessment and persist:
            self._emit_completion_assessment(
                updated,
                outcome_achieved=outcome_achieved,
                reflection_response=reflection_response,
                feedback_summary=feedback_summary,
                when=when,
                refresh_mission=refresh_mission,
            )
        return updated

    def _emit_step_assessment(
        self,
        mission: AdaptiveMission,
        *,
        last_step_id: str,
        when: datetime,
    ) -> None:
        """AP-001: mission step progress becomes structured educational evidence."""
        try:
            from app.application.assessment_pipeline import (
                assessment_pipeline_service as ap_svc,
            )

            concept_ids = [
                mission.objective.primary_concept_id,
                *mission.objective.supporting_concept_ids,
            ]
            ap_svc.AssessmentPipelineService().record_mission_step_completion(
                twin_id=mission.twin_id,
                mission_id=mission.mission_id,
                step_id=last_step_id,
                concept_ids=concept_ids,
                curriculum_entity_id=mission.objective.primary_concept_id,
                outcome_achieved=True,
                occurred_at=when,
                persist=True,
                reason=True,
                refresh_mission=False,
            )
        except Exception:  # noqa: BLE001 — assessment emission is best-effort
            return

    def _emit_completion_assessment(
        self,
        mission: AdaptiveMission,
        *,
        outcome_achieved: bool,
        reflection_response: str,
        feedback_summary: str,
        when: datetime,
        refresh_mission: bool,
    ) -> None:
        """AP-001: mission completion becomes structured educational evidence."""
        try:
            from app.application.assessment_pipeline import (
                assessment_pipeline_service as ap_svc,
            )

            ap_svc.AssessmentPipelineService().record_mission_completion(
                twin_id=mission.twin_id,
                mission_id=mission.mission_id,
                concept_ids=[
                    mission.objective.primary_concept_id,
                    *mission.objective.supporting_concept_ids,
                ],
                curriculum_entity_id=mission.objective.primary_concept_id,
                outcome_achieved=outcome_achieved,
                reflection_response=reflection_response,
                feedback_summary=feedback_summary,
                occurred_at=when,
                persist=True,
                reason=True,
                refresh_mission=refresh_mission,
                available_minutes=mission.schedule.total_minutes,
            )
        except Exception:  # noqa: BLE001 — assessment emission is best-effort
            return

    def diagnostics_for_twin(self, twin_id: str) -> dict[str, Any]:
        twin = self._twins.get(twin_id)
        if twin is None:
            return {"ok": False, "error": f"twin {twin_id!r} not found"}
        graph = self._graphs.get_for_twin(twin_id)
        prioritisation = prioritise_candidates(
            recommendations=twin.recommendations,
            gaps=twin.knowledge_gaps,
            learning_state=twin.learning_state,
            observations=twin.observations,
            learning_graph=graph,
        )
        active = self.get_active(twin_id)
        return {
            "ok": True,
            "engine_version": self.ENGINE_VERSION,
            "twin_id": twin_id,
            "recommendation_count": len(twin.recommendations),
            "gap_count": len(twin.knowledge_gaps),
            "learning_state": {
                "exam_readiness": twin.learning_state.exam_readiness,
                "momentum": twin.learning_state.momentum,
                "confidence": twin.learning_state.confidence,
            },
            "graph": {
                "present": graph is not None,
                "node_count": graph.node_count if graph else 0,
                "edge_count": graph.edge_count if graph else 0,
            },
            "prioritisation": {
                "explanation": prioritisation.explanation,
                "ranked_concept_ids": list(prioritisation.ranked_concept_ids),
                "selected_concept_id": (
                    prioritisation.selected.concept_id
                    if prioritisation.selected
                    else None
                ),
                "selected_score": (
                    prioritisation.selected.priority_score.score
                    if prioritisation.selected
                    else None
                ),
            },
            "active_mission": (
                self.as_dict(active) if active is not None else None
            ),
        }

    def as_dict(self, mission: AdaptiveMission) -> dict[str, Any]:
        return self._persistence.mission_as_dict(mission)

    def _enrich_candidate_evidence(self, twin: StudentDigitalTwin, candidate):
        """Optionally append retrieval evidence ids without inventing decisions."""
        if candidate.evidence_ids:
            return candidate
        workspace_id = (twin.student.workspace_id or "").strip()
        if not workspace_id:
            return candidate
        retrieval = self._retrieval
        if retrieval is None:
            try:
                retrieval = CurriculumRetrievalService()
            except Exception:  # noqa: BLE001
                return candidate
        try:
            result = retrieval.retrieve(
                RetrievalQuery(
                    text=candidate.concept_title or candidate.concept_id,
                    workspace_id=workspace_id,
                    profile=RetrievalProfile.MISSION_ENGINE,
                    subject_code=twin.student.subject_code or "",
                    seed_entity_id=candidate.concept_id,
                    limit=3,
                    expand_graph_hops=1,
                )
            )
        except Exception:  # noqa: BLE001 — evidence enrichment is best-effort
            return candidate
        evidence_ids: list[str] = []
        for ranked in result.results or ():
            for item in ranked.evidence:
                if item.evidence_id:
                    evidence_ids.append(item.evidence_id)
            evidence_ids.append(f"ranked:{ranked.entity_id}")
        if result.retrieval_log_id:
            evidence_ids.append(str(result.retrieval_log_id))
        if not evidence_ids:
            return candidate
        from dataclasses import replace

        return replace(
            candidate,
            evidence_ids=tuple(dict.fromkeys([*candidate.evidence_ids, *evidence_ids])),
        )
