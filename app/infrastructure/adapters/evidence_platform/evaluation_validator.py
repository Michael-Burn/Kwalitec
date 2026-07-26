"""Policy evaluation validation (MS-006 E3).

Validates PolicyDefinition structure for registration and evaluation
readiness, ExperimentObservation inputs, and completed PolicyEvaluation
artefacts. Does not mutate observations or evidence, does not promote
policies, and does not change educational behaviour.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from app.infrastructure.adapters.evidence_platform.contracts import (
    EVALUABLE_POLICY_STATUSES,
    EVALUATION_KINDS,
    GATE_CODE_CLAIM_BOUNDARY_LEAKAGE,
    GATE_CODE_DEMO_THEATRE,
    GATE_CODE_INCOMPLETE_EXPLAINABILITY,
    GATE_CODE_INSUFFICIENT_OBSERVATIONS,
    GATE_CODE_MISSING_RUNTIME_A,
    GATE_CODE_OVERCLAIM,
    GATE_CODE_STATISTICS_INCOMPLETE,
    GATE_FAILED,
    GATE_INELIGIBLE,
    GATE_PASSED,
    POLICY_OWNER_LAYERS,
    POLICY_STATUSES,
    RECOMMENDATION_KEEP,
    ExperimentObservation,
    PolicyDefinition,
    PolicyEvaluation,
    PolicyEvaluationExplanationPlaceholder,
)


class EvaluationValidationError(ValueError):
    """Raised when policy definitions or evaluation inputs fail validation."""


class EvaluationValidator:
    """Structural validator for E3 policy evaluation artefacts."""

    VALIDATOR_ID = "evaluation_validator"
    VALIDATOR_VERSION = "1.0.0-e3"

    @property
    def validator_id(self) -> str:
        return self.VALIDATOR_ID

    @property
    def validator_version(self) -> str:
        return self.VALIDATOR_VERSION

    def validate_definition(
        self,
        definition: PolicyDefinition,
        *,
        require_evaluable: bool = False,
    ) -> PolicyDefinition:
        """Validate a PolicyDefinition for registry / evaluation use."""
        if not isinstance(definition, PolicyDefinition):
            raise EvaluationValidationError(
                "definition must be a PolicyDefinition"
            )
        policy_id = (definition.policy_id or "").strip()
        if not policy_id:
            raise EvaluationValidationError("policy_id must be a non-empty string")
        if not (definition.policy_version or "").strip():
            raise EvaluationValidationError(
                "policy_version must be a non-empty string"
            )
        if not (definition.definition_version or "").strip():
            raise EvaluationValidationError(
                "definition_version must be a non-empty string"
            )
        owner = (definition.owner_layer or "").strip().lower()
        if owner not in POLICY_OWNER_LAYERS:
            raise EvaluationValidationError(f"unknown owner_layer: {owner}")
        status = (definition.status or "").strip().lower()
        if status not in POLICY_STATUSES:
            raise EvaluationValidationError(f"unknown policy status: {status}")
        if require_evaluable and status not in EVALUABLE_POLICY_STATUSES:
            allowed = sorted(EVALUABLE_POLICY_STATUSES)
            raise EvaluationValidationError(
                f"policy status must be one of {allowed} for evaluation; "
                f"got {status!r}"
            )
        kind = (definition.evaluation_kind or "").strip().lower()
        if kind not in EVALUATION_KINDS:
            raise EvaluationValidationError(f"unknown evaluation_kind: {kind}")
        if require_evaluable and not kind:
            raise EvaluationValidationError(
                "evaluation_kind must be set for evaluation"
            )
        return definition

    def validate_observations(
        self,
        observations: Sequence[ExperimentObservation],
        definition: PolicyDefinition,
    ) -> tuple[ExperimentObservation, ...]:
        """Validate and freeze-order observations for evaluation.

        Never mutates observation instances.
        """
        if not isinstance(observations, Sequence):
            raise EvaluationValidationError(
                "observations must be a sequence of ExperimentObservation"
            )
        if not observations:
            raise EvaluationValidationError(
                "at least one ExperimentObservation is required"
            )
        validated: list[ExperimentObservation] = []
        allowed_experiments = {
            (experiment_id or "").strip()
            for experiment_id in definition.experiment_ids
            if (experiment_id or "").strip()
        }
        seen_ids: set[str] = set()
        for observation in observations:
            if not isinstance(observation, ExperimentObservation):
                raise EvaluationValidationError(
                    "observations must contain ExperimentObservation values"
                )
            obs = self.validate_observation(observation)
            if obs.observation_id in seen_ids:
                raise EvaluationValidationError(
                    f"duplicate observation_id: {obs.observation_id}"
                )
            seen_ids.add(obs.observation_id)
            if allowed_experiments and obs.experiment_id not in allowed_experiments:
                raise EvaluationValidationError(
                    f"observation experiment_id {obs.experiment_id!r} not in "
                    f"policy experiment_ids"
                )
            validated.append(obs)
        return tuple(sorted(validated, key=lambda item: item.observation_id))

    def validate_observation(
        self, observation: ExperimentObservation
    ) -> ExperimentObservation:
        """Validate a single ExperimentObservation for evaluation input."""
        if not isinstance(observation, ExperimentObservation):
            raise EvaluationValidationError(
                "observation must be an ExperimentObservation"
            )
        if not (observation.observation_id or "").strip():
            raise EvaluationValidationError(
                "observation_id must be a non-empty string"
            )
        if not (observation.experiment_id or "").strip():
            raise EvaluationValidationError(
                "experiment_id must be a non-empty string"
            )
        if not (observation.evidence_id or "").strip():
            raise EvaluationValidationError(
                "evidence_id must be a non-empty string"
            )
        if not (observation.student_id or "").strip():
            raise EvaluationValidationError(
                "student_id must be a non-empty string"
            )
        if not (observation.arm_id or "").strip():
            raise EvaluationValidationError("arm_id must be a non-empty string")
        return observation

    def validate_explanation(
        self, explanation: PolicyEvaluationExplanationPlaceholder
    ) -> tuple[bool, tuple[str, ...]]:
        """Return (complete, missing_section_names) for five-answer gate."""
        if not isinstance(explanation, PolicyEvaluationExplanationPlaceholder):
            raise EvaluationValidationError(
                "explanation must be a PolicyEvaluationExplanationPlaceholder"
            )
        missing: list[str] = []
        for section_name in (
            "evidence_considered",
            "statistical_basis",
            "educational_rationale",
            "policy_version",
            "confidence",
        ):
            section = getattr(explanation, section_name)
            if not isinstance(section, Mapping) or not section:
                missing.append(section_name)
                continue
            if not _section_has_substance(section):
                missing.append(section_name)
        return (not missing, tuple(missing))

    def apply_gate_rules(
        self,
        *,
        explanation: PolicyEvaluationExplanationPlaceholder,
        gate_codes: Sequence[str],
        recommendation: str,
        statistical_summary: Mapping[str, Any],
    ) -> tuple[str, tuple[str, ...]]:
        """Apply explainability + claim-boundary + quality gates.

        Returns ``(gate_result, effective_gate_codes)``.
        """
        codes = sorted({(code or "").strip() for code in gate_codes if code})
        complete, missing = self.validate_explanation(explanation)
        if not complete:
            codes.append(GATE_CODE_INCOMPLETE_EXPLAINABILITY)
            codes.extend(f"missing:{name}" for name in missing)

        confidence = dict(explanation.confidence or {})
        what_not = confidence.get("what_this_does_not_prove")
        if recommendation == RECOMMENDATION_KEEP:
            if not what_not:
                codes.append(GATE_CODE_OVERCLAIM)
            uncertainty = dict(explanation.statistical_basis or {}).get(
                "uncertainty_summary"
            )
            if not uncertainty or str(uncertainty).strip() in {
                "",
                "not_estimable",
            }:
                design = str(
                    (statistical_summary or {}).get("design")
                    or dict(explanation.statistical_basis or {}).get("design")
                    or ""
                ).strip()
                if design == "descriptive_soak":
                    codes.append(GATE_CODE_STATISTICS_INCOMPLETE)

        unique_codes = tuple(sorted(set(codes)))
        hard_fails = {
            GATE_CODE_CLAIM_BOUNDARY_LEAKAGE,
            GATE_CODE_DEMO_THEATRE,
            GATE_CODE_OVERCLAIM,
            GATE_CODE_MISSING_RUNTIME_A,
            GATE_CODE_STATISTICS_INCOMPLETE,
            GATE_CODE_INCOMPLETE_EXPLAINABILITY,
        }
        if any(code in hard_fails for code in unique_codes):
            return GATE_FAILED, unique_codes
        if GATE_CODE_INSUFFICIENT_OBSERVATIONS in unique_codes:
            return GATE_INELIGIBLE, unique_codes
        if not complete:
            return GATE_INELIGIBLE, unique_codes
        return GATE_PASSED, unique_codes

    def validate_evaluation(
        self, evaluation: PolicyEvaluation
    ) -> PolicyEvaluation:
        """Validate a completed PolicyEvaluation artefact."""
        if not isinstance(evaluation, PolicyEvaluation):
            raise EvaluationValidationError(
                "evaluation must be a PolicyEvaluation"
            )
        if not (evaluation.evaluation_id or "").strip():
            raise EvaluationValidationError(
                "evaluation_id must be a non-empty string"
            )
        if not (evaluation.policy_id or "").strip():
            raise EvaluationValidationError(
                "policy_id must be a non-empty string"
            )
        if not (evaluation.policy_version or "").strip():
            raise EvaluationValidationError(
                "policy_version must be a non-empty string"
            )
        if not evaluation.recommendation:
            raise EvaluationValidationError(
                "recommendation must be set on PolicyEvaluation"
            )
        if not evaluation.gate_result:
            raise EvaluationValidationError(
                "gate_result must be set on PolicyEvaluation"
            )
        if not evaluation.confidence_band:
            raise EvaluationValidationError(
                "confidence_band must be set on PolicyEvaluation"
            )
        complete, missing = self.validate_explanation(evaluation.explanation)
        if not complete and evaluation.gate_result == GATE_PASSED:
            raise EvaluationValidationError(
                "gate_result=passed requires complete explainability; "
                f"missing={missing}"
            )
        return evaluation


def _section_has_substance(section: Mapping[str, Any]) -> bool:
    """True when a five-answer section has at least one non-empty value."""
    for value in section.values():
        if value is None:
            continue
        if isinstance(value, str) and value.strip():
            return True
        if isinstance(value, list | tuple | Mapping) and value:
            return True
        if isinstance(value, int | float | bool):
            return True
    return False


def build_evaluation_validator() -> EvaluationValidator:
    """DI helper — construct EvaluationValidator."""
    return EvaluationValidator()
