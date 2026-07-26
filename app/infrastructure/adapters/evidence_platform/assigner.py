"""Deterministic experiment assignment (MS-006 E2).

Assigns validated EvidenceRecords to ExperimentDefinition arms. Identical
EvidenceRecord + Identical ExperimentDefinition → Identical
ExperimentObservation every execution. Never mutates evidence, never scores
experiments, never changes educational behaviour, never persists.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from typing import Any

from app.infrastructure.adapters.evidence_platform.contracts import (
    ASSIGNMENT_MECHANISM_HASH,
    ASSIGNMENT_MECHANISM_MANUAL_ALLOWLIST,
    EVIDENCE_VERSION_E2,
    EvidenceRecord,
    ExperimentArm,
    ExperimentDefinition,
    ExperimentObservation,
    serialize_canonical,
)
from app.infrastructure.adapters.evidence_platform.experiment_validator import (
    ExperimentValidationError,
    ExperimentValidator,
    evaluate_eligibility,
)


class ExperimentAssigner:
    """Deterministic cohort assigner for validated evidence."""

    ASSIGNER_ID = "experiment_assigner"
    ASSIGNER_VERSION = "1.0.0-e2"
    OBSERVATION_VERSION = EVIDENCE_VERSION_E2

    def __init__(self, *, validator: ExperimentValidator | None = None) -> None:
        self._validator = validator or ExperimentValidator()

    @property
    def assigner_id(self) -> str:
        return self.ASSIGNER_ID

    @property
    def assigner_version(self) -> str:
        return self.ASSIGNER_VERSION

    @property
    def validator(self) -> ExperimentValidator:
        return self._validator

    def assign(
        self,
        record: EvidenceRecord,
        definition: ExperimentDefinition,
    ) -> ExperimentObservation:
        """Assign evidence to an experiment arm; return immutable observation.

        Does not mutate ``record`` or ``definition``.
        """
        validated_record = self._validator.validate_evidence_for_assignment(record)
        validated_definition = self._validator.validate_definition(
            definition, require_assignable=True
        )
        eligible, eligibility_reasons = evaluate_eligibility(
            validated_record, validated_definition
        )
        if not eligible:
            raise ExperimentValidationError(
                "evidence not eligible for experiment: "
                + ",".join(eligibility_reasons)
            )

        mechanism = (
            validated_definition.assignment_mechanism or ASSIGNMENT_MECHANISM_HASH
        )
        if not mechanism:
            mechanism = ASSIGNMENT_MECHANISM_HASH

        arm, assignment_detail = self._select_arm(
            validated_record, validated_definition, mechanism=mechanism
        )
        salt = assignment_salt(validated_definition)
        rationale = build_assignment_rationale(
            mechanism=mechanism,
            experiment_id=validated_definition.experiment_id,
            subject_key=validated_record.student_id,
            salt=salt,
            arm=arm,
            detail=assignment_detail,
        )
        evidence_ref = {
            "evidence_id": validated_record.evidence_id,
            "evidence_version": validated_record.evidence_version,
            "student_id": validated_record.student_id,
        }
        metadata = {
            "arm_exposure": arm.exposure,
            "arm_label": arm.label,
            "assigner_id": self.ASSIGNER_ID,
            "assigner_version": self.ASSIGNER_VERSION,
            "definition_status": validated_definition.status,
            "eligibility_reasons": list(eligibility_reasons),
            "eligibility_result": "pass",
            "flag_snapshot": dict(arm.upstream_flag_snapshot),
            "salt": salt,
            **assignment_detail,
        }
        draft = ExperimentObservation(
            observation_id="",
            observation_version=self.OBSERVATION_VERSION,
            experiment_id=validated_definition.experiment_id,
            experiment_version=validated_definition.definition_version,
            arm_id=arm.arm_id,
            cohort=arm.label or arm.arm_id,
            evidence_id=validated_record.evidence_id,
            evidence_ref=evidence_ref,
            student_id=validated_record.student_id,
            assignment_mechanism=mechanism,
            assignment_rationale=rationale,
            metadata=metadata,
            observed_at=validated_record.observed_at,
        )
        observation_id = deterministic_observation_id(draft)
        observation = ExperimentObservation(
            observation_id=observation_id,
            observation_version=draft.observation_version,
            experiment_id=draft.experiment_id,
            experiment_version=draft.experiment_version,
            arm_id=draft.arm_id,
            cohort=draft.cohort,
            evidence_id=draft.evidence_id,
            evidence_ref=draft.evidence_ref,
            student_id=draft.student_id,
            assignment_mechanism=draft.assignment_mechanism,
            assignment_rationale=draft.assignment_rationale,
            metadata=draft.metadata,
            observed_at=draft.observed_at,
            authority=draft.authority,
        )
        return self._validator.validate_observation(observation)

    def _select_arm(
        self,
        record: EvidenceRecord,
        definition: ExperimentDefinition,
        *,
        mechanism: str,
    ) -> tuple[ExperimentArm, dict[str, Any]]:
        if mechanism == ASSIGNMENT_MECHANISM_MANUAL_ALLOWLIST:
            return select_manual_allowlist_arm(record, definition)
        if mechanism != ASSIGNMENT_MECHANISM_HASH:
            raise ExperimentValidationError(
                f"unsupported assignment_mechanism for E2: {mechanism}"
            )
        return select_hash_arm(record, definition)


def assignment_salt(definition: ExperimentDefinition) -> str:
    """Derive deterministic salt from pre_registration or definition identity."""
    pre = (definition.pre_registration or "").strip()
    if pre:
        return pre
    return (
        f"{definition.experiment_id}:{definition.definition_version}"
    )


def select_hash_arm(
    record: EvidenceRecord,
    definition: ExperimentDefinition,
) -> tuple[ExperimentArm, dict[str, Any]]:
    """Hash-partition subject into an arm (equal weight, sorted by arm_id)."""
    arms = sorted(definition.arms, key=lambda arm: arm.arm_id)
    if not arms:
        raise ExperimentValidationError("experiment must declare at least one arm")
    salt = assignment_salt(definition)
    material = (
        f"{definition.experiment_id}|{record.student_id}|{salt}"
    )
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    weights = _arm_weights(definition.eligibility, arms)
    if weights is not None:
        arm, bucket = _weighted_arm(digest, arms, weights)
        weighted = True
    else:
        bucket = int(digest[:16], 16) % len(arms)
        arm = arms[bucket]
        weighted = False
    return arm, {
        "arm_count": len(arms),
        "bucket": bucket,
        "hash_digest_prefix": digest[:16],
        "weighted": weighted,
    }


def select_manual_allowlist_arm(
    record: EvidenceRecord,
    definition: ExperimentDefinition,
) -> tuple[ExperimentArm, dict[str, Any]]:
    """Assign from eligibility.arm_allowlist[student_id]."""
    eligibility = dict(definition.eligibility or {})
    allowlist = eligibility.get("arm_allowlist")
    if allowlist is None:
        allowlist = eligibility.get("assignments")
    if not isinstance(allowlist, Mapping):
        raise ExperimentValidationError(
            "manual_allowlist requires eligibility.arm_allowlist mapping"
        )
    raw_arm = allowlist.get(record.student_id)
    if raw_arm is None:
        raise ExperimentValidationError(
            f"student_id not in arm_allowlist: {record.student_id}"
        )
    arm_id = str(raw_arm).strip()
    for arm in definition.arms:
        if arm.arm_id == arm_id:
            return arm, {"allowlist_matched": True}
    raise ExperimentValidationError(
        f"arm_allowlist references unknown arm_id: {arm_id}"
    )


def build_assignment_rationale(
    *,
    mechanism: str,
    experiment_id: str,
    subject_key: str,
    salt: str,
    arm: ExperimentArm,
    detail: Mapping[str, Any],
) -> str:
    """Human-readable deterministic assignment rationale (no scoring)."""
    parts = [
        f"mechanism={mechanism}",
        f"experiment={experiment_id}",
        f"subject={subject_key}",
        f"salt={salt}",
        f"arm={arm.arm_id}",
    ]
    if "bucket" in detail:
        parts.append(f"bucket={detail['bucket']}/{detail.get('arm_count', '?')}")
    if detail.get("allowlist_matched"):
        parts.append("allowlist_matched=true")
    if detail.get("weighted"):
        parts.append("weighted=true")
    return "; ".join(parts)


def deterministic_observation_id(observation: ExperimentObservation) -> str:
    """Derive observation_id from material fields (excludes observation_id)."""
    material = {
        "arm_id": observation.arm_id,
        "assignment_mechanism": observation.assignment_mechanism,
        "assignment_rationale": observation.assignment_rationale,
        "cohort": observation.cohort,
        "evidence_id": observation.evidence_id,
        "evidence_ref": dict(observation.evidence_ref),
        "experiment_id": observation.experiment_id,
        "experiment_version": observation.experiment_version,
        "metadata": dict(observation.metadata),
        "observation_version": observation.observation_version
        or EVIDENCE_VERSION_E2,
        "observed_at": observation.observed_at,
        "student_id": observation.student_id,
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()
    return f"obs-{digest[:24]}"


def _arm_weights(
    eligibility: Mapping[str, Any] | None,
    arms: list[ExperimentArm],
) -> tuple[int, ...] | None:
    if not eligibility:
        return None
    raw = eligibility.get("arm_weights")
    if raw is None:
        return None
    if not isinstance(raw, Mapping):
        raise ExperimentValidationError("eligibility.arm_weights must be a mapping")
    weights: list[int] = []
    for arm in arms:
        value = raw.get(arm.arm_id, 1)
        try:
            weight = int(value)
        except (TypeError, ValueError) as exc:
            raise ExperimentValidationError(
                f"arm_weights[{arm.arm_id}] must be an int"
            ) from exc
        if weight < 0:
            raise ExperimentValidationError(
                f"arm_weights[{arm.arm_id}] must be >= 0"
            )
        weights.append(weight)
    if sum(weights) <= 0:
        raise ExperimentValidationError("arm_weights must sum to > 0")
    return tuple(weights)


def _weighted_arm(
    digest: str,
    arms: list[ExperimentArm],
    weights: tuple[int, ...],
) -> tuple[ExperimentArm, int]:
    total = sum(weights)
    ticket = int(digest[:16], 16) % total
    cursor = 0
    for index, weight in enumerate(weights):
        cursor += weight
        if ticket < cursor:
            return arms[index], index
    return arms[-1], len(arms) - 1


def build_experiment_assigner(
    *,
    enabled: bool,
    validator: ExperimentValidator | None = None,
) -> ExperimentAssigner | None:
    """DI helper — construct ExperimentAssigner only when the flag is on."""
    if not enabled:
        return None
    return ExperimentAssigner(validator=validator)
