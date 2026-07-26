"""Experiment definition / assignment validation (MS-006 E2).

Validates ExperimentDefinition structure for registration and assignment
readiness, and validated EvidenceRecord inputs for assignment. Does not
score experiments, declare winners, mutate evidence, or change educational
behaviour.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.infrastructure.adapters.evidence_platform.contracts import (
    ASSIGNABLE_EXPERIMENT_STATUSES,
    ASSIGNMENT_MECHANISM_MANUAL_ALLOWLIST,
    ASSIGNMENT_MECHANISM_OPS_OVERRIDE,
    ASSIGNMENT_MECHANISMS,
    EXPERIMENT_STATUSES,
    EXPOSURE_MODES,
    EvidenceRecord,
    ExperimentArm,
    ExperimentDefinition,
    ExperimentObservation,
)
from app.infrastructure.adapters.evidence_platform.validation import (
    EvidenceValidationError,
    validate_payload_privacy,
    validate_student_id,
)


class ExperimentValidationError(ValueError):
    """Raised when experiment definitions or assignment inputs fail validation."""


class ExperimentValidator:
    """Structural validator for E2 experiment assignment artefacts."""

    VALIDATOR_ID = "experiment_validator"
    VALIDATOR_VERSION = "1.0.0-e2"

    @property
    def validator_id(self) -> str:
        return self.VALIDATOR_ID

    @property
    def validator_version(self) -> str:
        return self.VALIDATOR_VERSION

    def validate_definition(
        self,
        definition: ExperimentDefinition,
        *,
        require_assignable: bool = False,
    ) -> ExperimentDefinition:
        """Validate an ExperimentDefinition for registry / assignment use."""
        if not isinstance(definition, ExperimentDefinition):
            raise ExperimentValidationError(
                "definition must be an ExperimentDefinition"
            )
        experiment_id = (definition.experiment_id or "").strip()
        if not experiment_id:
            raise ExperimentValidationError(
                "experiment_id must be a non-empty string"
            )
        if not (definition.definition_version or "").strip():
            raise ExperimentValidationError(
                "definition_version must be a non-empty string"
            )
        status = (definition.status or "").strip().lower()
        if status not in EXPERIMENT_STATUSES:
            raise ExperimentValidationError(f"unknown experiment status: {status}")
        if require_assignable and status not in ASSIGNABLE_EXPERIMENT_STATUSES:
            allowed = sorted(ASSIGNABLE_EXPERIMENT_STATUSES)
            raise ExperimentValidationError(
                f"experiment status must be one of {allowed} for assignment; "
                f"got {status!r}"
            )
        arms = tuple(definition.arms or ())
        if not arms:
            raise ExperimentValidationError(
                "experiment must declare at least one arm"
            )
        seen: set[str] = set()
        for arm in arms:
            if not isinstance(arm, ExperimentArm):
                raise ExperimentValidationError(
                    "arms must contain ExperimentArm values"
                )
            arm_id = (arm.arm_id or "").strip()
            if not arm_id:
                raise ExperimentValidationError("arm_id must be a non-empty string")
            if arm_id in seen:
                raise ExperimentValidationError(f"duplicate arm_id: {arm_id}")
            seen.add(arm_id)
            exposure = (arm.exposure or "").strip().lower()
            if exposure not in EXPOSURE_MODES:
                raise ExperimentValidationError(
                    f"unknown arm exposure: {exposure}"
                )
            validate_payload_privacy(arm.upstream_flag_snapshot)
        mechanism = (definition.assignment_mechanism or "").strip().lower()
        if mechanism not in ASSIGNMENT_MECHANISMS:
            allowed = sorted(k for k in ASSIGNMENT_MECHANISMS if k)
            raise ExperimentValidationError(
                f"assignment_mechanism must be one of {allowed} or empty"
            )
        if require_assignable and mechanism == ASSIGNMENT_MECHANISM_OPS_OVERRIDE:
            raise ExperimentValidationError(
                "ops_override assignment is not supported by E2 assigner"
            )
        try:
            validate_payload_privacy(definition.eligibility)
            validate_payload_privacy(definition.window)
            validate_payload_privacy(definition.statistical_plan)
            validate_payload_privacy(definition.rollback_map)
        except EvidenceValidationError as exc:
            raise ExperimentValidationError(str(exc)) from exc
        if mechanism == ASSIGNMENT_MECHANISM_MANUAL_ALLOWLIST:
            _validate_manual_allowlist(definition.eligibility, seen)
        return definition

    def validate_evidence_for_assignment(
        self, record: EvidenceRecord
    ) -> EvidenceRecord:
        """Validate that EvidenceRecord is structurally assignable.

        Never mutates the record. Does not re-score quality or invent fields.
        """
        if not isinstance(record, EvidenceRecord):
            raise ExperimentValidationError("record must be an EvidenceRecord")
        if not (record.evidence_id or "").strip():
            raise ExperimentValidationError(
                "evidence_id must be a non-empty string"
            )
        try:
            validate_student_id(record.student_id)
            validate_payload_privacy(record.payload_summary)
            validate_payload_privacy(record.provenance)
        except EvidenceValidationError as exc:
            raise ExperimentValidationError(str(exc)) from exc
        return record

    def validate_observation(
        self, observation: ExperimentObservation
    ) -> ExperimentObservation:
        """Validate a produced ExperimentObservation structure."""
        if not isinstance(observation, ExperimentObservation):
            raise ExperimentValidationError(
                "observation must be an ExperimentObservation"
            )
        if not (observation.observation_id or "").strip():
            raise ExperimentValidationError(
                "observation_id must be a non-empty string"
            )
        if not (observation.experiment_id or "").strip():
            raise ExperimentValidationError(
                "experiment_id must be a non-empty string"
            )
        if not (observation.arm_id or "").strip():
            raise ExperimentValidationError("arm_id must be a non-empty string")
        if not (observation.evidence_id or "").strip():
            raise ExperimentValidationError(
                "evidence_id must be a non-empty string"
            )
        try:
            validate_student_id(observation.student_id)
            validate_payload_privacy(observation.evidence_ref)
            validate_payload_privacy(observation.metadata)
        except EvidenceValidationError as exc:
            raise ExperimentValidationError(str(exc)) from exc
        return observation

    def evaluate_eligibility(
        self,
        record: EvidenceRecord,
        definition: ExperimentDefinition,
    ) -> tuple[bool, tuple[str, ...]]:
        """Deterministic eligibility check (pass/fail + reasons).

        Does not mutate evidence or definition.
        """
        self.validate_evidence_for_assignment(record)
        self.validate_definition(definition, require_assignable=True)
        return evaluate_eligibility(record, definition)


def evaluate_eligibility(
    record: EvidenceRecord,
    definition: ExperimentDefinition,
) -> tuple[bool, tuple[str, ...]]:
    """Return (eligible, reasons) for evidence against definition eligibility."""
    eligibility = dict(definition.eligibility or {})
    if not eligibility:
        return True, ("eligibility_unrestricted",)

    reasons: list[str] = []

    student_ids = eligibility.get("student_ids")
    if student_ids is not None:
        allowed = {str(item).strip() for item in _as_sequence(student_ids)}
        allowed.discard("")
        if record.student_id not in allowed:
            return False, ("student_not_in_allowlist",)
        reasons.append("student_allowlist_matched")

    claim_boundaries = eligibility.get("claim_boundaries")
    if claim_boundaries is not None:
        allowed = {
            str(item).strip().lower() for item in _as_sequence(claim_boundaries)
        }
        allowed.discard("")
        boundary = (record.claim_boundary or "").strip().lower()
        if boundary and boundary not in allowed:
            return False, ("claim_boundary_mismatch",)
        reasons.append("claim_boundary_matched")

    evidence_classes = eligibility.get("evidence_classes")
    if evidence_classes is not None:
        allowed = {
            str(item).strip().upper() for item in _as_sequence(evidence_classes)
        }
        allowed.discard("")
        klass = (record.evidence_class or "").strip().upper()
        if klass and klass not in allowed:
            return False, ("evidence_class_mismatch",)
        reasons.append("evidence_class_matched")

    if eligibility.get("require_quality_pass"):
        if (record.quality.result or "").strip().lower() != "pass":
            return False, ("quality_not_pass",)
        reasons.append("quality_pass_required_matched")

    if eligibility.get("require_available"):
        if (record.availability or "").strip().lower() != "available":
            return False, ("evidence_unavailable",)
        reasons.append("availability_required_matched")

    if not reasons:
        reasons.append("eligibility_passed")
    return True, tuple(reasons)


def _validate_manual_allowlist(
    eligibility: Mapping[str, Any],
    arm_ids: set[str],
) -> None:
    allowlist = eligibility.get("arm_allowlist")
    if allowlist is None:
        allowlist = eligibility.get("assignments")
    if not isinstance(allowlist, Mapping) or not allowlist:
        raise ExperimentValidationError(
            "manual_allowlist requires eligibility.arm_allowlist mapping"
        )
    for subject, arm_id in allowlist.items():
        if not str(subject).strip():
            raise ExperimentValidationError(
                "arm_allowlist keys must be non-empty subject keys"
            )
        normalised_arm = str(arm_id).strip()
        if normalised_arm not in arm_ids:
            raise ExperimentValidationError(
                f"arm_allowlist references unknown arm_id: {normalised_arm}"
            )


def _as_sequence(value: Any) -> tuple[Any, ...]:
    if isinstance(value, str | bytes):
        return (value,)
    if isinstance(value, list | tuple):
        return tuple(value)
    return (value,)


def build_experiment_validator() -> ExperimentValidator:
    """DI helper — construct ExperimentValidator."""
    return ExperimentValidator()


__all__ = [
    "ExperimentValidationError",
    "ExperimentValidator",
    "build_experiment_validator",
    "evaluate_eligibility",
]
