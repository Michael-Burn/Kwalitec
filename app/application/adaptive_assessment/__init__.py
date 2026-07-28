"""ILE-001A/B/C — Adaptive Assessment foundations, Quick Check, framing.

Presentation and product-infrastructure only. No educational selection,
Twin reasoning, Mission planning, Tutor reasoning, or Assessment algorithms.

Safe defaults keep every Adaptive Assessment surface disabled until later
milestones explicitly enable them. ILE-001B adds Mission-embedded Quick Check
experience orchestration over an already-selected learning check. ILE-001C
adds optional Study Sensei contextual framing (default OFF).
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
from app.application.adaptive_assessment.educational_framing import (
    ContextCardContract,
    EducationalSummaryContract,
    EvidenceBand,
    PresentationIntentContext,
    RecommendationFrameContract,
    ReflectionFrameContract,
    build_context_card,
    build_educational_summary,
    build_recommendation_frame,
    build_reflection_frame,
    default_intent_context,
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
from app.application.adaptive_assessment.quick_check_contracts import (
    QuickCheckCompletionContract,
    QuickCheckIntroductionContract,
    QuickCheckMissionCardContract,
    QuickCheckMissionReturnContract,
    QuickCheckPausedContract,
    QuickCheckProgressContract,
    QuickCheckQuestionContract,
    QuickCheckReflectionContract,
    build_calm_progress,
    build_quick_check_completion,
    build_quick_check_introduction,
    build_quick_check_mission_card,
    build_quick_check_mission_return,
    build_quick_check_paused,
    build_quick_check_question,
    build_quick_check_reflection,
    default_selected_learning_check,
)
from app.application.adaptive_assessment.quick_check_experience import (
    QuickCheckExperienceError,
    QuickCheckExperienceService,
    QuickCheckExperienceState,
    QuickCheckExperienceStore,
    QuickCheckPhase,
    QuickCheckSurfaceSnapshot,
    get_quick_check_experience_service,
    reset_quick_check_experience_service,
)
from app.application.adaptive_assessment.selected_learning_check import (
    LearningCheckItem,
    SelectedLearningCheck,
    get_already_selected_quick_check,
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
    "ContextCardContract",
    "EducationalSummaryContract",
    "EvidenceBand",
    "ExplanationPresentationContract",
    "LearningCheckItem",
    "MessageCatalogue",
    "MissionPresentationContract",
    "PresentationIntentContext",
    "ProductTelemetryRecorder",
    "QuickCheckCompletionContract",
    "QuickCheckExperienceError",
    "QuickCheckExperienceService",
    "QuickCheckExperienceState",
    "QuickCheckExperienceStore",
    "QuickCheckIntroductionContract",
    "QuickCheckMissionCardContract",
    "QuickCheckMissionReturnContract",
    "QuickCheckPausedContract",
    "QuickCheckPhase",
    "QuickCheckProgressContract",
    "QuickCheckQuestionContract",
    "QuickCheckReflectionContract",
    "QuickCheckSurfaceSnapshot",
    "RecommendationFrameContract",
    "ReflectionFrameContract",
    "SelectedLearningCheck",
    "SessionPresentationContract",
    "SessionTypeDefinition",
    "SessionTypeId",
    "StudentFacingContentContract",
    "TelemetryEventName",
    "TerminologyViolation",
    "accessibility_for_session",
    "assert_adaptive_assessment_copy_safe",
    "build_calm_progress",
    "build_context_card",
    "build_educational_summary",
    "build_mission_presentation_contract",
    "build_product_contracts",
    "build_quick_check_completion",
    "build_quick_check_introduction",
    "build_quick_check_mission_card",
    "build_quick_check_mission_return",
    "build_quick_check_paused",
    "build_quick_check_question",
    "build_quick_check_reflection",
    "build_recommendation_frame",
    "build_reflection_frame",
    "build_session_presentation_contract",
    "build_student_facing_content_contract",
    "build_telemetry_event",
    "default_intent_context",
    "default_selected_learning_check",
    "format_message",
    "get_already_selected_quick_check",
    "get_copy",
    "get_default_catalogue",
    "get_quick_check_experience_service",
    "get_session_type",
    "iter_copy_entries",
    "iter_session_types",
    "reduced_motion_safe",
    "reset_quick_check_experience_service",
    "resolve_adaptive_assessment_flags",
    "resolve_copy",
    "validate_product_resources",
    "validate_registered_adaptive_assessment_resources",
]
