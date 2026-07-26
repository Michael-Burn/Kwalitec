"""Policy evaluation explainability (MS-006 E3).

Builds the five mandatory PolicyEvaluationExplanationBundle answers.
No hidden reasoning. Missing answers fail the explainability gate.
Never mutates observations, evidence, or educational behaviour.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from app.infrastructure.adapters.evidence_platform.contracts import (
    CLAIM_LEARNING_DEPTH,
    CLAIM_ORGANISATION,
    EVIDENCE_VERSION_E3,
    STATISTICAL_DESIGN_DESCRIPTIVE_SOAK,
    ExperimentObservation,
    PolicyDefinition,
    PolicyEvaluationExplanationBundle,
    serialize_canonical,
)


@dataclass(frozen=True)
class PolicyAssessment:
    """Immutable assessment draft produced by PolicyEvaluator (E3).

    Intermediate artefact — not a governance PolicyEvaluation and not a
    deployment action.
    """

    recommendation: str = ""
    confidence_band: str = ""
    confidence_rationale: str = ""
    gate_codes: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    statistical_summary: Mapping[str, Any] = field(default_factory=dict)
    outcome_metric_payloads: tuple[Mapping[str, Any], ...] = ()
    experiment_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    evidence_bundle_ids: tuple[str, ...] = ()
    arm_distribution: Mapping[str, int] = field(default_factory=dict)
    observation_count: int = 0
    student_count: int = 0
    runtime_a_ref_count: int = 0
    quality_codes: tuple[str, ...] = ()
    supporting_upstream_refs: tuple[str, ...] = ()
    claim_boundaries_present: tuple[str, ...] = ()
    demo_markers: tuple[str, ...] = ()
    design: str = STATISTICAL_DESIGN_DESCRIPTIVE_SOAK
    estimator: str = "descriptive_only"
    effect_summary: str = ""
    uncertainty_summary: str = "not_estimable"
    not_proven: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "gate_codes", tuple(self.gate_codes or ()))
        object.__setattr__(self, "limitations", tuple(self.limitations or ()))
        object.__setattr__(
            self,
            "statistical_summary",
            MappingProxyType(dict(self.statistical_summary or {})),
        )
        object.__setattr__(
            self,
            "outcome_metric_payloads",
            tuple(
                MappingProxyType(dict(item))
                for item in (self.outcome_metric_payloads or ())
            ),
        )
        object.__setattr__(
            self, "experiment_refs", tuple(self.experiment_refs or ())
        )
        object.__setattr__(self, "evidence_refs", tuple(self.evidence_refs or ()))
        object.__setattr__(
            self, "evidence_bundle_ids", tuple(self.evidence_bundle_ids or ())
        )
        object.__setattr__(
            self,
            "arm_distribution",
            MappingProxyType(dict(self.arm_distribution or {})),
        )
        object.__setattr__(self, "quality_codes", tuple(self.quality_codes or ()))
        object.__setattr__(
            self,
            "supporting_upstream_refs",
            tuple(self.supporting_upstream_refs or ()),
        )
        object.__setattr__(
            self,
            "claim_boundaries_present",
            tuple(self.claim_boundaries_present or ()),
        )
        object.__setattr__(self, "demo_markers", tuple(self.demo_markers or ()))
        object.__setattr__(self, "not_proven", tuple(self.not_proven or ()))

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "arm_distribution": dict(self.arm_distribution),
            "claim_boundaries_present": list(self.claim_boundaries_present),
            "confidence_band": self.confidence_band,
            "confidence_rationale": self.confidence_rationale,
            "demo_markers": list(self.demo_markers),
            "design": self.design,
            "effect_summary": self.effect_summary,
            "estimator": self.estimator,
            "evidence_bundle_ids": list(self.evidence_bundle_ids),
            "evidence_refs": list(self.evidence_refs),
            "experiment_refs": list(self.experiment_refs),
            "gate_codes": list(self.gate_codes),
            "limitations": list(self.limitations),
            "not_proven": list(self.not_proven),
            "observation_count": self.observation_count,
            "outcome_metric_payloads": [
                dict(item) for item in self.outcome_metric_payloads
            ],
            "quality_codes": list(self.quality_codes),
            "recommendation": self.recommendation,
            "runtime_a_ref_count": self.runtime_a_ref_count,
            "statistical_summary": dict(self.statistical_summary),
            "student_count": self.student_count,
            "supporting_upstream_refs": list(self.supporting_upstream_refs),
            "uncertainty_summary": self.uncertainty_summary,
        }

    def serialize(self) -> str:
        return serialize_canonical(self.to_canonical_dict())


class EvaluationExplainability:
    """Build five-answer explainability bundles for policy evaluation."""

    EXPLAINABILITY_ID = "evaluation_explainability"
    EXPLAINABILITY_VERSION = "1.0.0-e3"

    @property
    def explainability_id(self) -> str:
        return self.EXPLAINABILITY_ID

    @property
    def explainability_version(self) -> str:
        return self.EXPLAINABILITY_VERSION

    def build(
        self,
        *,
        definition: PolicyDefinition,
        observations: Sequence[ExperimentObservation],
        assessment: PolicyAssessment,
    ) -> PolicyEvaluationExplanationBundle:
        """Produce a complete five-answer explanation bundle."""
        evidence_considered = {
            "summary": (
                f"Considered {assessment.observation_count} experiment "
                f"observation(s) across {assessment.student_count} student(s) "
                f"and {len(assessment.experiment_refs)} experiment reference(s)."
            ),
            "evidence_bundle_ids": list(assessment.evidence_bundle_ids),
            "runtime_a_ref_count": assessment.runtime_a_ref_count,
            "supporting_upstream_refs": list(assessment.supporting_upstream_refs),
            "quality_codes": list(assessment.quality_codes),
            "claim_boundaries_present": list(assessment.claim_boundaries_present),
            "observation_ids": [
                obs.observation_id
                for obs in sorted(observations, key=lambda item: item.observation_id)
            ],
        }
        statistical_basis = {
            "design": assessment.design,
            "sample_summary": (
                f"n_observations={assessment.observation_count}; "
                f"n_students={assessment.student_count}; "
                f"arms={dict(assessment.arm_distribution)}"
            ),
            "estimator": assessment.estimator,
            "effect_summary": assessment.effect_summary
            or "No causal effect estimated; descriptive arm counts only.",
            "uncertainty_summary": assessment.uncertainty_summary,
            "pre_registration_id": str(
                (definition.statistical_plan or {}).get("pre_registration_id")
                or definition.spec_ref
                or ""
            ),
            "not_proven": list(assessment.not_proven),
        }
        rationale = dict(definition.educational_rationale or {})
        principles = [
            {
                "principle_id": principle_id,
                "version": definition.definition_version or EVIDENCE_VERSION_E3,
                "how_relevant": "declared_on_policy",
            }
            for principle_id in definition.principles
        ]
        educational_rationale = {
            "intent_summary": definition.intent
            or definition.title
            or "Registered policy intent not provided.",
            "principles": principles,
            "sp_mapping": list(definition.sp_mapping),
            "student_impact_hypothesis": str(
                rationale.get("student_impact_hypothesis")
                or "Observational evaluation only; no student-facing claim."
            ),
            "organisation_vs_learning_note": str(
                rationale.get("organisation_vs_learning_note")
                or _organisation_vs_learning_note(definition)
            ),
        }
        policy_version = {
            "policy_id": definition.policy_id,
            "policy_version": definition.policy_version,
            "owner_layer": definition.owner_layer,
            "upstream_flag_snapshot": dict(definition.upstream_controls),
            "baseline_policy_version": definition.baseline_policy_version,
            "spec_ref": definition.spec_ref,
            "evaluation_kind": definition.evaluation_kind,
        }
        confidence = {
            "band": assessment.confidence_band,
            "rationale": assessment.confidence_rationale,
            "limitations": list(assessment.limitations),
            "what_this_does_not_prove": list(assessment.not_proven),
        }
        return PolicyEvaluationExplanationBundle(
            evidence_considered=evidence_considered,
            statistical_basis=statistical_basis,
            educational_rationale=educational_rationale,
            policy_version=policy_version,
            confidence=confidence,
        )


def _organisation_vs_learning_note(definition: PolicyDefinition) -> str:
    intent = definition.claim_boundary_intent or CLAIM_ORGANISATION
    if intent == CLAIM_LEARNING_DEPTH:
        return (
            "Policy declares learning_depth intent; evaluation must not treat "
            "organisation lift as learning depth (EP-004 SP8)."
        )
    return (
        "Organisation outcomes remain typed separately from learning-depth "
        "claims (EP-004 SP8)."
    )


def build_evaluation_explainability() -> EvaluationExplainability:
    """DI helper — construct EvaluationExplainability."""
    return EvaluationExplainability()
