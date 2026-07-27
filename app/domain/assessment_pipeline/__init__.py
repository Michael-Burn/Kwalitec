"""Assessment & Learning Feedback Pipeline (AP-001) domain package.

Records learner activity as structured educational evidence and delegates
learner-state updates to StudentReasoningService. Never performs educational
reasoning itself. No LLM.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "ActivityAttempt",
    "ActivityCompletion",
    "AssessmentEvent",
    "AssessmentEventType",
    "AssessmentResult",
    "EVENT_TO_OBSERVATION_KIND",
    "FeedbackSource",
    "FeedbackValidationIssue",
    "FeedbackValidationResult",
    "LearningFeedback",
    "PerformanceSummary",
    "ValidationSeverity",
    "build_assessment_result",
    "build_learning_feedback",
    "build_observation_from_event",
    "confidence_for_event",
    "evidence_ids_for_event",
    "observation_kind_for_event",
    "performance_label_for_event",
    "prepare_pipeline_artifacts",
    "suggested_next_action_for_event",
    "validate_assessment_event",
    "validate_learning_feedback",
]

_EXPORT_MODULES = {
    "AssessmentEvent": "app.domain.assessment_pipeline.assessment_event",
    "AssessmentEventType": "app.domain.assessment_pipeline.assessment_event",
    "AssessmentResult": "app.domain.assessment_pipeline.assessment_result",
    "LearningFeedback": "app.domain.assessment_pipeline.learning_feedback",
    "FeedbackSource": "app.domain.assessment_pipeline.feedback_source",
    "ActivityAttempt": "app.domain.assessment_pipeline.attempt",
    "PerformanceSummary": "app.domain.assessment_pipeline.performance_summary",
    "ActivityCompletion": "app.domain.assessment_pipeline.activity_completion",
    "FeedbackValidationIssue": "app.domain.assessment_pipeline.feedback_validator",
    "FeedbackValidationResult": "app.domain.assessment_pipeline.feedback_validator",
    "ValidationSeverity": "app.domain.assessment_pipeline.feedback_validator",
    "validate_assessment_event": "app.domain.assessment_pipeline.feedback_validator",
    "validate_learning_feedback": "app.domain.assessment_pipeline.feedback_validator",
    "EVENT_TO_OBSERVATION_KIND": "app.domain.assessment_pipeline.assessment_pipeline",
    "observation_kind_for_event": "app.domain.assessment_pipeline.assessment_pipeline",
    "performance_label_for_event": "app.domain.assessment_pipeline.assessment_pipeline",
    "evidence_ids_for_event": "app.domain.assessment_pipeline.assessment_pipeline",
    "confidence_for_event": "app.domain.assessment_pipeline.assessment_pipeline",
    "suggested_next_action_for_event": (
        "app.domain.assessment_pipeline.assessment_pipeline"
    ),
    "build_observation_from_event": (
        "app.domain.assessment_pipeline.assessment_pipeline"
    ),
    "build_assessment_result": "app.domain.assessment_pipeline.assessment_pipeline",
    "build_learning_feedback": "app.domain.assessment_pipeline.assessment_pipeline",
    "prepare_pipeline_artifacts": "app.domain.assessment_pipeline.assessment_pipeline",
}


def __getattr__(name: str) -> Any:
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from importlib import import_module

    module = import_module(module_name)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
