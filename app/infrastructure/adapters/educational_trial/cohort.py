"""Deterministic educational trial cohort assignment (P4-MS001).

Stable, reproducible allocation of students to baseline vs treatment cohorts
under configurable rollout. Assignment never invents recommendations and
never expands advisory fields.
"""

from __future__ import annotations

import hashlib
from typing import Any

from .contracts import (
    AUTHORITY_EDUCATIONAL_TRIAL,
    COHORT_BASELINE,
    COHORT_TREATMENT,
    COHORT_UNASSIGNED,
    DEFAULT_ROLLOUT_SALT,
    EDUCATIONAL_TRIAL_VERSION,
    CohortAssignment,
    EducationalTrial,
    serialize_canonical,
)

ASSIGNER_ID = "educational_trial_cohort_assigner"
ASSIGNER_VERSION = EDUCATIONAL_TRIAL_VERSION


def student_bucket(
    student_id: str,
    *,
    trial_id: str,
    salt: str = DEFAULT_ROLLOUT_SALT,
) -> int:
    """Return a stable 0–99 bucket for ``student_id`` within a trial."""
    sid = (student_id or "").strip()
    if not sid:
        return -1
    material = (
        f"{(salt or DEFAULT_ROLLOUT_SALT).strip()}:"
        f"{(trial_id or '').strip()}:{sid}"
    )
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % 100


def student_in_treatment(
    student_id: str,
    *,
    rollout_percentage: int,
    trial_id: str,
    salt: str = DEFAULT_ROLLOUT_SALT,
) -> bool:
    """Deterministic treatment-cohort membership for configurable rollout."""
    percentage = max(0, min(100, int(rollout_percentage)))
    if percentage <= 0:
        return False
    if percentage >= 100:
        sid = (student_id or "").strip()
        return bool(sid)
    bucket = student_bucket(student_id, trial_id=trial_id, salt=salt)
    if bucket < 0:
        return False
    return bucket < percentage


def opaque_student_key(student_id: str, *, trial_id: str) -> str:
    """Opaque, stable student key for trial artefacts (no raw personal id)."""
    sid = (student_id or "").strip()
    material = {
        "student_id": sid,
        "trial_id": (trial_id or "").strip(),
        "purpose": "educational_trial_cohort",
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()[:16]
    return f"trialstu-{digest}"


def assign_cohort(
    student_id: str,
    trial: EducationalTrial,
    *,
    generated_at: str | None = None,
    provenance: dict[str, Any] | None = None,
) -> CohortAssignment:
    """Assign a student to baseline or treatment under an immutable trial.

    Rules:
    - Inactive / non-active trials → ``unassigned`` (no Runtime A change).
    - Active trials → deterministic baseline vs treatment by rollout %.
    - Treatment alone authorises policy weighting under the trial gate.
    """
    if not isinstance(trial, EducationalTrial):
        raise TypeError("trial must be EducationalTrial")

    sid = (student_id or "").strip()
    student_key = opaque_student_key(sid, trial_id=trial.trial_id) if sid else ""
    base_provenance = {
        "assigner_id": ASSIGNER_ID,
        "assigner_version": ASSIGNER_VERSION,
        "trial_status": trial.status,
        **dict(provenance or {}),
    }

    if not trial.is_active or not sid:
        return CohortAssignment(
            trial_id=trial.trial_id,
            student_key=student_key,
            cohort=COHORT_UNASSIGNED,
            rollout_percentage=trial.rollout_percentage,
            bucket=-1 if not sid else student_bucket(
                sid, trial_id=trial.trial_id, salt=trial.rollout_salt
            ),
            policy_version=trial.policy_version,
            authorised_for_weighting=False,
            generated_at=generated_at,
            provenance=base_provenance,
            authority=AUTHORITY_EDUCATIONAL_TRIAL,
            trial_version=EDUCATIONAL_TRIAL_VERSION,
        )

    bucket = student_bucket(
        sid, trial_id=trial.trial_id, salt=trial.rollout_salt
    )
    in_treatment = student_in_treatment(
        sid,
        rollout_percentage=trial.rollout_percentage,
        trial_id=trial.trial_id,
        salt=trial.rollout_salt,
    )
    cohort = COHORT_TREATMENT if in_treatment else COHORT_BASELINE
    return CohortAssignment(
        trial_id=trial.trial_id,
        student_key=student_key,
        cohort=cohort,
        rollout_percentage=trial.rollout_percentage,
        bucket=bucket,
        policy_version=trial.policy_version,
        authorised_for_weighting=in_treatment,
        generated_at=generated_at,
        provenance={
            **base_provenance,
            "advisory_field": trial.advisory_field,
        },
        authority=AUTHORITY_EDUCATIONAL_TRIAL,
        trial_version=EDUCATIONAL_TRIAL_VERSION,
    )


__all__ = [
    "ASSIGNER_ID",
    "ASSIGNER_VERSION",
    "assign_cohort",
    "opaque_student_key",
    "student_bucket",
    "student_in_treatment",
]
