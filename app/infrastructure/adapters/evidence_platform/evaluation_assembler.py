"""Policy evaluation assembler (MS-006 E3).

Projects PolicyAssessment + explainability into an immutable PolicyEvaluation.
Never mutates observations or evidence, never promotes policies, never changes
educational behaviour.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from app.infrastructure.adapters.evidence_platform.contracts import (
    AUTHORITY_EVIDENCE_PLATFORM,
    EVIDENCE_VERSION_E3,
    OutcomeMetric,
    PolicyDefinition,
    PolicyEvaluation,
    PolicyEvaluationExplanationBundle,
)
from app.infrastructure.adapters.evidence_platform.evaluation_explainability import (
    PolicyAssessment,
)
from app.infrastructure.adapters.evidence_platform.evaluation_validator import (
    EvaluationValidator,
)
from app.infrastructure.adapters.evidence_platform.provenance import (
    SOURCE_SERVICE_EVIDENCE,
    block_provenance,
    freeze_provenance_map,
)


class EvaluationAssembler:
    """Assemble immutable PolicyEvaluation artefacts from assessment drafts."""

    ASSEMBLER_ID = "evaluation_assembler"
    ASSEMBLER_VERSION = "1.0.0-e3"
    EVALUATION_VERSION = EVIDENCE_VERSION_E3
    ENGINE_VERSION = EVIDENCE_VERSION_E3

    def __init__(self, *, validator: EvaluationValidator | None = None) -> None:
        self._validator = validator or EvaluationValidator()

    @property
    def assembler_id(self) -> str:
        return self.ASSEMBLER_ID

    @property
    def assembler_version(self) -> str:
        return self.ASSEMBLER_VERSION

    @property
    def validator(self) -> EvaluationValidator:
        return self._validator

    def assemble(
        self,
        *,
        definition: PolicyDefinition,
        assessment: PolicyAssessment,
        explanation: PolicyEvaluationExplanationBundle,
        evaluation_id: str = "",
        created_at: str | None = None,
    ) -> PolicyEvaluation:
        """Project assessment + explanation into an immutable PolicyEvaluation.

        Gate result is applied here from validator rules. No deployment side
        effects.
        """
        validated_definition = self._validator.validate_definition(
            definition, require_evaluable=True
        )
        if not isinstance(assessment, PolicyAssessment):
            raise TypeError("assessment must be a PolicyAssessment")
        if not isinstance(explanation, PolicyEvaluationExplanationBundle):
            raise TypeError(
                "explanation must be a PolicyEvaluationExplanationBundle"
            )

        gate_result, gate_codes = self._validator.apply_gate_rules(
            explanation=explanation,
            gate_codes=assessment.gate_codes,
            recommendation=assessment.recommendation,
            statistical_summary=assessment.statistical_summary,
        )
        outcome_metrics = _build_outcome_metrics(assessment.outcome_metric_payloads)
        experiment_id = (
            assessment.experiment_refs[0] if assessment.experiment_refs else ""
        )
        provenance = freeze_provenance_map(
            {
                "assessment": block_provenance(
                    available=True,
                    source_service=SOURCE_SERVICE_EVIDENCE,
                    source_entity="PolicyAssessment",
                    collected_at=created_at,
                ),
                "explanation": block_provenance(
                    available=True,
                    source_service=SOURCE_SERVICE_EVIDENCE,
                    source_entity="PolicyEvaluationExplanationBundle",
                    collected_at=created_at,
                ),
                "policy": block_provenance(
                    available=True,
                    source_service=SOURCE_SERVICE_EVIDENCE,
                    source_entity="PolicyDefinition",
                    collected_at=created_at,
                ),
                "observations": block_provenance(
                    available=assessment.observation_count > 0,
                    source_service=SOURCE_SERVICE_EVIDENCE,
                    source_entity="ExperimentObservation",
                    collected_at=created_at,
                    unavailable_reason=(
                        ""
                        if assessment.observation_count > 0
                        else "no_observations"
                    ),
                ),
            }
        )
        evaluation = PolicyEvaluation(
            evaluation_id=(evaluation_id or "").strip(),
            evaluation_version=self.EVALUATION_VERSION,
            policy_id=validated_definition.policy_id,
            policy_version=validated_definition.policy_version,
            baseline_policy_version=validated_definition.baseline_policy_version,
            experiment_id=experiment_id,
            experiment_refs=assessment.experiment_refs,
            evidence_bundle_ids=assessment.evidence_bundle_ids,
            evidence_refs=assessment.evidence_refs,
            outcome_metrics=outcome_metrics,
            statistical_summary=assessment.statistical_summary,
            explanation=explanation,
            gate_result=gate_result,
            gate_codes=gate_codes,
            recommendation=assessment.recommendation,
            limitations=assessment.limitations,
            confidence_band=assessment.confidence_band,
            confidence_rationale=assessment.confidence_rationale,
            provenance=provenance,
            created_at=created_at,
            engine_version=self.ENGINE_VERSION,
            authority=AUTHORITY_EVIDENCE_PLATFORM,
        )
        return evaluation


def _build_outcome_metrics(
    payloads: Sequence[Mapping[str, Any]],
) -> tuple[OutcomeMetric, ...]:
    metrics: list[OutcomeMetric] = []
    for payload in payloads:
        metrics.append(
            OutcomeMetric(
                metric_id=str(payload.get("metric_id") or ""),
                metric_version=EVIDENCE_VERSION_E3,
                outcome_definition_id=str(
                    payload.get("outcome_definition_id") or ""
                ),
                claim_boundary=str(payload.get("claim_boundary") or ""),
                grain=str(payload.get("grain") or ""),
                value=payload.get("value"),
                uncertainty=str(payload.get("uncertainty") or ""),
                n=payload.get("n") if isinstance(payload.get("n"), int) else None,
                subject_scope=str(payload.get("subject_scope") or ""),
                evidence_bundle_id=str(payload.get("evidence_bundle_id") or ""),
                limitations=tuple(
                    str(item) for item in (payload.get("limitations") or ())
                ),
                filters=dict(payload.get("filters") or {}),
                authority=AUTHORITY_EVIDENCE_PLATFORM,
            )
        )
    return tuple(metrics)


def build_evaluation_assembler(
    *,
    enabled: bool,
    validator: EvaluationValidator | None = None,
) -> EvaluationAssembler | None:
    """DI helper — construct EvaluationAssembler only when the flag is on."""
    if not enabled:
        return None
    return EvaluationAssembler(validator=validator)
