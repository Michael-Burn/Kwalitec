"""Adaptive Assessment feature flags — progressive product rollout.

Supports global enable/disable, subject-level enablement, and future cohort
rollout. Defaults keep Adaptive Assessment and every session type OFF.

No educational logic: flags gate product surfaces only.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

_TRUTHY = frozenset({"1", "true", "yes", "on"})

# Environment keys (global).
_ENV_ADAPTIVE_ASSESSMENT = "KWALITEC_ADAPTIVE_ASSESSMENT"
_ENV_QUICK_CHECK = "KWALITEC_QUICK_CHECK"
_ENV_DEEP_CHECK = "KWALITEC_DEEP_CHECK"
_ENV_RECOVERY_CHECK = "KWALITEC_RECOVERY_CHECK"
_ENV_CONFIDENCE_CHECK = "KWALITEC_CONFIDENCE_CHECK"
_ENV_READINESS_CHECK = "KWALITEC_READINESS_CHECK"
_ENV_SUBJECTS = "KWALITEC_ADAPTIVE_ASSESSMENT_SUBJECTS"
_ENV_COHORTS = "KWALITEC_ADAPTIVE_ASSESSMENT_COHORTS"


def _env_truthy(name: str, *, environ: dict[str, str] | None = None) -> bool:
    env = environ if environ is not None else os.environ
    return env.get(name, "").strip().lower() in _TRUTHY


def _parse_csv_set(raw: str) -> frozenset[str]:
    """Parse comma-separated identifiers into a frozenset of stripped tokens."""
    if not raw or not raw.strip():
        return frozenset()
    return frozenset(part.strip() for part in raw.split(",") if part.strip())


@dataclass(frozen=True)
class AdaptiveAssessmentFeatureFlags:
    """Immutable Adaptive Assessment product rollout switches.

    All session-type flags default to ``False``. Global Adaptive Assessment
    must be enabled before any session type is considered available for a
    subject / cohort.

    Attributes:
        ENABLE_ADAPTIVE_ASSESSMENT: Master switch for the Adaptive Assessment
            product surface.
        ENABLE_QUICK_CHECK: Quick Check session type.
        ENABLE_DEEP_CHECK: Deep Check session type.
        ENABLE_RECOVERY_CHECK: Recovery Check session type.
        ENABLE_CONFIDENCE_CHECK: Confidence Check session type.
        ENABLE_READINESS_CHECK: Readiness Check session type.
        enabled_subjects: Subject codes allowed when the master switch is on.
            Empty means all subjects (when master is on) — subject filtering
            is opt-in via an explicit allow-list.
        enabled_cohorts: Cohort identifiers for future progressive rollout.
            Empty means no cohort restriction (when master is on).
    """

    ENABLE_ADAPTIVE_ASSESSMENT: bool = False
    ENABLE_QUICK_CHECK: bool = False
    ENABLE_DEEP_CHECK: bool = False
    ENABLE_RECOVERY_CHECK: bool = False
    ENABLE_CONFIDENCE_CHECK: bool = False
    ENABLE_READINESS_CHECK: bool = False
    enabled_subjects: frozenset[str] = field(default_factory=frozenset)
    enabled_cohorts: frozenset[str] = field(default_factory=frozenset)

    def is_globally_enabled(self) -> bool:
        """True when the Adaptive Assessment master switch is on."""
        return bool(self.ENABLE_ADAPTIVE_ASSESSMENT)

    def is_subject_enabled(self, subject_code: str | None) -> bool:
        """Return whether Adaptive Assessment may appear for ``subject_code``.

        Empty ``enabled_subjects`` means no subject restriction (all subjects
        allowed when the master switch is on). A non-empty allow-list requires
        an exact match on the normalised subject code.
        """
        if not self.ENABLE_ADAPTIVE_ASSESSMENT:
            return False
        if not self.enabled_subjects:
            return True
        if subject_code is None or not str(subject_code).strip():
            return False
        return str(subject_code).strip() in self.enabled_subjects

    def is_cohort_enabled(self, cohort_id: str | None) -> bool:
        """Return whether Adaptive Assessment may appear for ``cohort_id``.

        Empty ``enabled_cohorts`` means no cohort restriction. A non-empty
        allow-list requires an exact match (future progressive rollout).
        """
        if not self.ENABLE_ADAPTIVE_ASSESSMENT:
            return False
        if not self.enabled_cohorts:
            return True
        if cohort_id is None or not str(cohort_id).strip():
            return False
        return str(cohort_id).strip() in self.enabled_cohorts

    def is_session_type_enabled(self, session_type_id: str) -> bool:
        """Return whether a named session type flag is on (ignores subject)."""
        if not self.ENABLE_ADAPTIVE_ASSESSMENT:
            return False
        mapping = {
            "quick_check": self.ENABLE_QUICK_CHECK,
            "deep_check": self.ENABLE_DEEP_CHECK,
            "recovery_check": self.ENABLE_RECOVERY_CHECK,
            "confidence_check": self.ENABLE_CONFIDENCE_CHECK,
            "readiness_check": self.ENABLE_READINESS_CHECK,
        }
        return bool(mapping.get(session_type_id, False))

    def is_available(
        self,
        session_type_id: str,
        *,
        subject_code: str | None = None,
        cohort_id: str | None = None,
    ) -> bool:
        """Combined gate: global + session type + subject + cohort."""
        return (
            self.is_session_type_enabled(session_type_id)
            and self.is_subject_enabled(subject_code)
            and self.is_cohort_enabled(cohort_id)
        )


def resolve_adaptive_assessment_flags(
    *,
    environ: dict[str, str] | None = None,
) -> AdaptiveAssessmentFeatureFlags:
    """Resolve Adaptive Assessment flags from the process environment.

    Safe default is all disabled when unset or non-truthy.
    """
    env = environ if environ is not None else os.environ
    subjects = _parse_csv_set(env.get(_ENV_SUBJECTS, ""))
    cohorts = _parse_csv_set(env.get(_ENV_COHORTS, ""))
    return AdaptiveAssessmentFeatureFlags(
        ENABLE_ADAPTIVE_ASSESSMENT=_env_truthy(
            _ENV_ADAPTIVE_ASSESSMENT, environ=environ
        ),
        ENABLE_QUICK_CHECK=_env_truthy(_ENV_QUICK_CHECK, environ=environ),
        ENABLE_DEEP_CHECK=_env_truthy(_ENV_DEEP_CHECK, environ=environ),
        ENABLE_RECOVERY_CHECK=_env_truthy(
            _ENV_RECOVERY_CHECK, environ=environ
        ),
        ENABLE_CONFIDENCE_CHECK=_env_truthy(
            _ENV_CONFIDENCE_CHECK, environ=environ
        ),
        ENABLE_READINESS_CHECK=_env_truthy(
            _ENV_READINESS_CHECK, environ=environ
        ),
        enabled_subjects=subjects,
        enabled_cohorts=cohorts,
    )


# Process default — prefer ``resolve_adaptive_assessment_flags`` in call sites.
ADAPTIVE_ASSESSMENT_FEATURE_FLAGS = AdaptiveAssessmentFeatureFlags()
