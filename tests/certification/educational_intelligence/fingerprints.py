"""Deterministic fingerprints for Educational Intelligence artefacts."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from app.domain.intelligent_tutor.explainability.result import ExplanationResult
from app.domain.learning_graph.projections.result import ProjectionResult
from app.domain.mission.planning.result import PlanningResult
from app.domain.reasoning.decisions.decision_set import EducationalDecisionSet
from app.domain.reasoning.observations.observation_set import EducationalObservationSet
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin


@dataclass(frozen=True, slots=True)
class PipelineFingerprints:
    """Comparable stage snapshots for deterministic replay certification."""

    observation: tuple[Any, ...]
    decision: tuple[Any, ...]
    twin: tuple[Any, ...]
    projection: tuple[Any, ...]
    mission: tuple[Any, ...]
    explanation: tuple[Any, ...]


def fingerprint_observations(
    observation_set: EducationalObservationSet,
) -> tuple[Any, ...]:
    return (
        observation_set.set_id,
        observation_set.interpretation_version,
        observation_set.evidence_bundle_id,
        observation_set.reasoning_request_id,
        tuple(
            (
                o.observation_id,
                o.category.value,
                dict(o.value) if isinstance(o.value, Mapping) else o.value,
                o.provenance,
                dict(o.traceability),
            )
            for o in observation_set.observations
        ),
    )


def fingerprint_decisions(decision_set: EducationalDecisionSet) -> tuple[Any, ...]:
    return (
        decision_set.set_id,
        decision_set.decision_version,
        decision_set.context.evidence_bundle_id,
        decision_set.context.reasoning_request_id,
        decision_set.context.correlation_id,
        decision_set.context.prior_twin_version,
        tuple(
            (
                d.decision_id,
                d.category.value,
                d.value,
                d.subject_ref,
                dict(d.provenance),
                tuple(d.reference.educational_observation_ids),
            )
            for d in decision_set.decisions
        ),
    )


def fingerprint_twin(twin: StudentDigitalTwin) -> tuple[Any, ...]:
    mastery = tuple(
        sorted(
            (
                r.concept_id,
                round(float(r.mastery_score), 6),
                round(float(r.confidence), 6),
                r.trend.value if hasattr(r.trend, "value") else str(r.trend),
            )
            for r in (twin.mastery.records if twin.mastery else ())
        )
    )
    return (
        twin.twin_id,
        twin.version,
        round(float(twin.confidence.score), 6),
        mastery,
        tuple(h.reasoning_id for h in twin.reasoning_history),
    )


def fingerprint_projection(result: ProjectionResult) -> tuple[Any, ...]:
    return (
        result.graph_projection.projection_id,
        result.context.projection_version,
        result.context.twin_version,
        result.relationship_count,
        tuple(
            sorted(
                (
                    r.projection_id,
                    r.relationship_type.value,
                    r.from_ref,
                    r.to_ref,
                    r.decision_id,
                    dict(r.provenance),
                )
                for r in result.batch.relationships
            )
        ),
    )


def fingerprint_mission(result: PlanningResult) -> tuple[Any, ...]:
    plan = result.study_mission_plan
    selected = plan.selected_candidate
    return (
        result.plan_id,
        result.mission_id,
        plan.planning_version,
        plan.twin_version,
        plan.goal,
        selected.candidate_id if selected else None,
        selected.concept_id if selected else None,
        selected.priority_score if selected else None,
        tuple(
            (c.candidate_id, c.concept_id, c.priority_score)
            for c in result.batch.candidates
        ),
    )


def fingerprint_explanation(result: ExplanationResult) -> tuple[Any, ...]:
    explanation = result.explanation
    return (
        result.explanation_id,
        explanation.explanation_version,
        explanation.twin_version,
        explanation.summary,
        explanation.available,
        tuple(explanation.decision_ids),
        tuple(explanation.uncertainty_notes),
        tuple(
            (s.section_id, s.kind.value if hasattr(s.kind, "value") else s.kind, s.body)
            for s in explanation.sections
        ),
        dict(explanation.provenance),
    )


def build_fingerprints(
    *,
    observation_set: EducationalObservationSet,
    decision_set: EducationalDecisionSet,
    twin: StudentDigitalTwin,
    projection: ProjectionResult,
    mission: PlanningResult,
    explanation: ExplanationResult,
) -> PipelineFingerprints:
    return PipelineFingerprints(
        observation=fingerprint_observations(observation_set),
        decision=fingerprint_decisions(decision_set),
        twin=fingerprint_twin(twin),
        projection=fingerprint_projection(projection),
        mission=fingerprint_mission(mission),
        explanation=fingerprint_explanation(explanation),
    )
