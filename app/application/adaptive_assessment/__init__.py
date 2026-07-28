"""ILE-001A — Adaptive Assessment product foundations.

Presentation and product-infrastructure only. No educational selection,
Twin reasoning, Mission planning, Tutor reasoning, or Assessment algorithms.

Safe defaults keep every Adaptive Assessment surface disabled until later
milestones (ILE-001B+) explicitly enable them.
"""

from __future__ import annotations

from app.application.adaptive_assessment.accessibility import (
    AccessibilityMetadata,
    accessibility_for_session,
    reduced_motion_safe,
)
from app.application.adaptive_assessment.contracts import (
    AdaptiveAssessmentProductContracts,
    ExplanationPresentationContract,
    MissionPresentationContract,
    SessionPresentationContract,
    StudentFacingContentContract,
    build_mission_presentation_contract,
    build_product_contracts,
    build_session_presentation_contract,
    build_student_facing_content_contract,
)
from app.application.adaptive_assessment.copy_registry import (
    COPY_KEYS,
    AdaptiveAssessmentCopy,
    get_copy,
    iter_copy_entries,
)
from app.application.adaptive_assessment.feature_flags import (
    ADAPTIVE_ASSESSMENT_FEATURE_FLAGS,
    AdaptiveAssessmentFeatureFlags,
    resolve_adaptive_assessment_flags,
)
from app.application.adaptive_assessment.localisation import (
    MessageCatalogue,
    format_message,
    get_default_catalogue,
    resolve_copy,
)
from app.application.adaptive_assessment.session_registry import (
    SESSION_TYPES,
    SessionTypeDefinition,
    SessionTypeId,
    get_session_type,
    iter_session_types,
)
from app.application.adaptive_assessment.telemetry import (
    AdaptiveAssessmentTelemetryEvent,
    ProductTelemetryRecorder,
    TelemetryEventName,
    build_telemetry_event,
)
from app.application.adaptive_assessment.terminology import (
    APPROVED_REPLACEMENTS,
    FORBIDDEN_STUDENT_TERMS,
    TerminologyViolation,
    assert_adaptive_assessment_copy_safe,
    validate_product_resources,
    validate_registered_adaptive_assessment_resources,
)

__all__ = [
    "ADAPTIVE_ASSESSMENT_FEATURE_FLAGS",
    "APPROVED_REPLACEMENTS",
    "COPY_KEYS",
    "FORBIDDEN_STUDENT_TERMS",
    "SESSION_TYPES",
    "AccessibilityMetadata",
    "AdaptiveAssessmentCopy",
    "AdaptiveAssessmentFeatureFlags",
    "AdaptiveAssessmentProductContracts",
    "AdaptiveAssessmentTelemetryEvent",
    "ExplanationPresentationContract",
    "MessageCatalogue",
    "MissionPresentationContract",
    "ProductTelemetryRecorder",
    "SessionPresentationContract",
    "SessionTypeDefinition",
    "SessionTypeId",
    "StudentFacingContentContract",
    "TelemetryEventName",
    "TerminologyViolation",
    "accessibility_for_session",
    "assert_adaptive_assessment_copy_safe",
    "build_mission_presentation_contract",
    "build_product_contracts",
    "build_session_presentation_contract",
    "build_student_facing_content_contract",
    "build_telemetry_event",
    "format_message",
    "get_copy",
    "get_default_catalogue",
    "get_session_type",
    "iter_copy_entries",
    "iter_session_types",
    "reduced_motion_safe",
    "resolve_adaptive_assessment_flags",
    "resolve_copy",
    "validate_product_resources",
    "validate_registered_adaptive_assessment_resources",
]
