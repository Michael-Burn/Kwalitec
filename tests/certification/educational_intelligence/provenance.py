"""Provenance chain audit for Educational Intelligence artefacts."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.intelligent_tutor.explainability.result import ExplanationResult
from app.domain.learning_graph.projections.result import ProjectionResult
from app.domain.mission.planning.result import PlanningResult
from app.domain.reasoning.decisions.decision_set import EducationalDecisionSet
from app.domain.reasoning.observations.observation_set import EducationalObservationSet
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin

REQUIRED_PROVENANCE_KEYS = (
    "assessment_session_id",
    "evidence_bundle_id",
    "observation_ids",
    "decision_ids",
    "reasoning_request_id",
    "twin_version",
    "mission_plan_id",
    "explanation_id",
    "correlation_id",
)


@dataclass(frozen=True, slots=True)
class ProvenanceChain:
    """End-to-end educational provenance for one certified pipeline run."""

    assessment_session_id: str
    evidence_bundle_id: str
    observation_ids: tuple[str, ...]
    observation_set_id: str
    decision_ids: tuple[str, ...]
    decision_set_id: str
    reasoning_request_id: str
    twin_id: str
    twin_version: int
    projection_id: str
    mission_plan_id: str
    mission_id: str
    explanation_id: str
    correlation_id: str
    broken_links: tuple[str, ...] = ()

    @property
    def is_complete(self) -> bool:
        return not self.broken_links


def audit_provenance(
    *,
    observation_set: EducationalObservationSet,
    decision_set: EducationalDecisionSet,
    twin: StudentDigitalTwin,
    projection: ProjectionResult,
    mission: PlanningResult,
    explanation: ExplanationResult,
) -> ProvenanceChain:
    """Verify every learner-facing artefact traces to upstream identities."""
    broken: list[str] = []
    ctx = decision_set.context
    session_id = ctx.session_id
    bundle_id = ctx.evidence_bundle_id
    request_id = ctx.reasoning_request_id
    correlation_id = ctx.correlation_id

    if observation_set.evidence_bundle_id != bundle_id:
        broken.append("observation_set.evidence_bundle_id != decision_set.context")
    if observation_set.reasoning_request_id != request_id:
        broken.append("observation_set.reasoning_request_id != decision_set.context")

    obs_ids = observation_set.observation_ids
    for decision in decision_set.decisions:
        ref_obs = decision.reference.educational_observation_ids
        if not ref_obs:
            broken.append(f"decision {decision.decision_id} missing observation ids")
        elif any(oid not in obs_ids for oid in ref_obs):
            broken.append(
                f"decision {decision.decision_id} references unknown observation ids"
            )
        if decision.reference.evidence_bundle_id != bundle_id:
            broken.append(f"decision {decision.decision_id} broken evidence link")
        if decision.reference.reasoning_request_id != request_id:
            broken.append(f"decision {decision.decision_id} broken reasoning link")
        if decision.reference.correlation_id != correlation_id:
            broken.append(f"decision {decision.decision_id} broken correlation link")
        if decision.reference.assessment_session_id != session_id:
            broken.append(f"decision {decision.decision_id} broken session link")

    if twin.twin_id != ctx.twin_id:
        broken.append("twin_id mismatch with decision context")
    if not twin.reasoning_history:
        broken.append("twin missing reasoning history after decision apply")

    if projection.context.evidence_bundle_id != bundle_id:
        broken.append("projection broken evidence link")
    if projection.context.reasoning_request_id != request_id:
        broken.append("projection broken reasoning link")
    if projection.context.correlation_id != correlation_id:
        broken.append("projection broken correlation link")
    if projection.context.twin_version != twin.version:
        broken.append("projection twin_version mismatch")
    for rel in projection.batch.relationships:
        if rel.reference.decision_id not in {
            d.decision_id for d in decision_set.decisions
        }:
            broken.append(f"projection {rel.projection_id} unknown decision_id")

    plan = mission.study_mission_plan
    if plan.context.evidence_bundle_id != bundle_id:
        broken.append("mission broken evidence link")
    if plan.context.reasoning_request_id != request_id:
        broken.append("mission broken reasoning link")
    if plan.context.correlation_id != correlation_id:
        broken.append("mission broken correlation link")
    if plan.twin_version != twin.version:
        broken.append("mission twin_version mismatch")
    if plan.selected_candidate is not None:
        selected_decision = plan.selected_candidate.decision_id
        if selected_decision and selected_decision not in {
            d.decision_id for d in decision_set.decisions
        }:
            broken.append("mission selected candidate unknown decision_id")

    expl = explanation.explanation
    if expl.context.evidence_bundle_id != bundle_id:
        broken.append("explanation broken evidence link")
    if expl.context.reasoning_request_id != request_id:
        broken.append("explanation broken reasoning link")
    if expl.context.correlation_id != correlation_id:
        broken.append("explanation broken correlation link")
    if expl.twin_version != twin.version:
        broken.append("explanation twin_version mismatch")
    if expl.mission_plan_id and expl.mission_plan_id != plan.plan_id:
        broken.append("explanation mission_plan_id mismatch")
    for section in expl.sections:
        if hasattr(section, "reference") and section.reference is not None:
            ref = section.reference
            if getattr(ref, "evidence_bundle_id", "") not in ("", bundle_id):
                broken.append(
                    f"explanation section {section.section_id} broken evidence link"
                )
            if getattr(ref, "reasoning_request_id", "") not in ("", request_id):
                broken.append(
                    f"explanation section {section.section_id} broken reasoning link"
                )

    if explanation.available and not expl.sections:
        broken.append("available explanation has no sections")
    if explanation.available and not expl.decision_ids:
        broken.append("available explanation missing decision_ids")

    return ProvenanceChain(
        assessment_session_id=session_id,
        evidence_bundle_id=bundle_id,
        observation_ids=obs_ids,
        observation_set_id=observation_set.set_id,
        decision_ids=tuple(d.decision_id for d in decision_set.decisions),
        decision_set_id=decision_set.set_id,
        reasoning_request_id=request_id,
        twin_id=twin.twin_id,
        twin_version=twin.version,
        projection_id=projection.graph_projection.projection_id,
        mission_plan_id=plan.plan_id,
        mission_id=plan.mission_id,
        explanation_id=expl.explanation_id,
        correlation_id=correlation_id,
        broken_links=tuple(broken),
    )
