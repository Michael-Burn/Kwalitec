"""Personal Learning Profile (EP-004.1).

Persistent, evidence-based summary of long-term observed learning behaviours
and preferences. Summarises Learning Feedback evidence; does not make
educational decisions.

Feature flag: ``KWALITEC_PERSONAL_LEARNING_PROFILE`` /
``ENABLE_PERSONAL_LEARNING_PROFILE`` (default OFF).

Does not change Recommendation, Readiness, or Planning authority. Services
may consume profile attributes via ``PersonalLearningProfilePort`` /
``consume_personal_learning_profile`` without depending on aggregator or
store implementation details.
"""

from __future__ import annotations

from .adapter import (
    PersonalLearningProfileAdapter,
    as_profile_port,
    build_personal_learning_profile_adapter,
)
from .aggregator import (
    PersonalLearningProfileAggregator,
    build_personal_learning_profile_aggregator,
)
from .consumer import (
    bind_personal_learning_profile_store,
    consume_personal_learning_profile,
    get_cached_personal_learning_profile,
    get_personal_learning_profile_store,
    resolve_personal_learning_profile,
)
from .contracts import (
    ALLOWED_ATTRIBUTE_KINDS,
    ALLOWED_ATTRIBUTE_STATUSES,
    ALLOWED_CLAIM_BOUNDARIES,
    ATTR_CONSISTENCY_TREND,
    ATTR_PLANNING_COMPLETION_RATE,
    ATTR_PREFERRED_SESSION_DURATION,
    ATTR_PREFERRED_STUDY_WINDOWS,
    ATTR_RECOMMENDATION_RESPONSIVENESS,
    ATTR_RECOVERY_EFFECTIVENESS,
    ATTR_REVISION_ADHERENCE,
    AUTHORITY_PERSONAL_LEARNING_PROFILE,
    CLAIM_BEHAVIOUR_SUMMARY,
    CLAIM_HABIT_SUMMARY,
    CLAIM_PREFERENCE_SUMMARY,
    CLAIM_UNSUPPORTED,
    CONFIDENCE_FULL_SAMPLE,
    CONFIDENCE_MIN_SAMPLE,
    CONTRACT_VERSION,
    FORBIDDEN_INFERENCE_KEYS,
    KIND_DERIVED_INDICATOR,
    KIND_OBSERVED_FACT,
    KIND_UNSUPPORTED,
    PROFILE_ATTRIBUTE_KEYS,
    REASON_AGGREGATOR_ERROR,
    REASON_FLAG_OFF,
    REASON_FORBIDDEN_INFERENCE,
    REASON_NO_EVIDENCE,
    REASON_SCHEMA_INVALID,
    REASON_STORE_ERROR,
    RESOLVE_STATUS_FAILED,
    RESOLVE_STATUS_OK,
    RESOLVE_STATUS_SKIPPED,
    RESOLVE_STATUSES,
    STATUS_AVAILABLE,
    STATUS_UNAVAILABLE,
    STATUS_UNSUPPORTED,
    PersonalLearningProfile,
    PersonalLearningProfilePort,
    ProfileAttribute,
    ProfileEvidenceRef,
    ProfileResolveResult,
    confidence_from_sample_size,
    deterministic_profile_id,
    serialize_canonical,
)
from .store import (
    PersonalLearningProfileStore,
    build_personal_learning_profile_store,
)

__all__ = [
    "ALLOWED_ATTRIBUTE_KINDS",
    "ALLOWED_ATTRIBUTE_STATUSES",
    "ALLOWED_CLAIM_BOUNDARIES",
    "ATTR_CONSISTENCY_TREND",
    "ATTR_PLANNING_COMPLETION_RATE",
    "ATTR_PREFERRED_SESSION_DURATION",
    "ATTR_PREFERRED_STUDY_WINDOWS",
    "ATTR_RECOMMENDATION_RESPONSIVENESS",
    "ATTR_RECOVERY_EFFECTIVENESS",
    "ATTR_REVISION_ADHERENCE",
    "AUTHORITY_PERSONAL_LEARNING_PROFILE",
    "CLAIM_BEHAVIOUR_SUMMARY",
    "CLAIM_HABIT_SUMMARY",
    "CLAIM_PREFERENCE_SUMMARY",
    "CLAIM_UNSUPPORTED",
    "CONFIDENCE_FULL_SAMPLE",
    "CONFIDENCE_MIN_SAMPLE",
    "CONTRACT_VERSION",
    "FORBIDDEN_INFERENCE_KEYS",
    "KIND_DERIVED_INDICATOR",
    "KIND_OBSERVED_FACT",
    "KIND_UNSUPPORTED",
    "PROFILE_ATTRIBUTE_KEYS",
    "REASON_AGGREGATOR_ERROR",
    "REASON_FLAG_OFF",
    "REASON_FORBIDDEN_INFERENCE",
    "REASON_NO_EVIDENCE",
    "REASON_SCHEMA_INVALID",
    "REASON_STORE_ERROR",
    "RESOLVE_STATUS_FAILED",
    "RESOLVE_STATUS_OK",
    "RESOLVE_STATUS_SKIPPED",
    "RESOLVE_STATUSES",
    "STATUS_AVAILABLE",
    "STATUS_UNAVAILABLE",
    "STATUS_UNSUPPORTED",
    "PersonalLearningProfile",
    "PersonalLearningProfileAdapter",
    "PersonalLearningProfileAggregator",
    "PersonalLearningProfilePort",
    "PersonalLearningProfileStore",
    "ProfileAttribute",
    "ProfileEvidenceRef",
    "ProfileResolveResult",
    "as_profile_port",
    "bind_personal_learning_profile_store",
    "build_personal_learning_profile_adapter",
    "build_personal_learning_profile_aggregator",
    "build_personal_learning_profile_store",
    "confidence_from_sample_size",
    "consume_personal_learning_profile",
    "deterministic_profile_id",
    "get_cached_personal_learning_profile",
    "get_personal_learning_profile_store",
    "resolve_personal_learning_profile",
    "serialize_canonical",
]
