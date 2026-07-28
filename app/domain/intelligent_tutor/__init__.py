"""Evidence-Backed Intelligent Tutor (TUTOR-001) domain package.

The Tutor explains educational decisions already produced by the platform.
It never performs educational reasoning itself.

Pipeline:
  Student Question
    → Student Digital Twin
    → Educational Reasoning (decisions already on Twin)
    → Learning Graph
    → Curriculum Retrieval
    → Evidence Assembly
    → Explanation Builder
    → Tutor Response

No LLM dependency in this package. Response prose is produced behind
TutorGenerationPort at the application layer.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "AssembledEvidence",
    "CoachingMessage",
    "ConceptExplanation",
    "ConversationMemory",
    "DecisionExplanation",
    "EvidenceCategory",
    "EvidenceExplanation",
    "EvidenceItemRef",
    "EXPLANATION_VERSION",
    "Explanation",
    "ExplanationContext",
    "ExplanationKind",
    "ExplanationReference",
    "ExplanationResult",
    "ExplanationSection",
    "ExplanationSectionKind",
    "ExplanationVersion",
    "LearningHint",
    "LearningObjectiveExplanation",
    "MissionExplanation",
    "ResponseBlueprint",
    "TutorContext",
    "TutorExplanation",
    "TutorExplanationGenerated",
    "TutorExplanationRequested",
    "TutorExplanationUnavailable",
    "TutorQuestion",
    "TutorQuestionKind",
    "TutorResponse",
    "TutorSession",
    "TutorSessionStatus",
    "assemble_evidence",
    "build_response_blueprint",
    "classify_question",
    "update_conversation_memory",
]

_EXPORT_MODULES = {
    "TutorSession": "app.domain.intelligent_tutor.tutor_session",
    "TutorSessionStatus": "app.domain.intelligent_tutor.tutor_session",
    "TutorContext": "app.domain.intelligent_tutor.tutor_context",
    "TutorQuestion": "app.domain.intelligent_tutor.tutor_question",
    "TutorQuestionKind": "app.domain.intelligent_tutor.tutor_question",
    "classify_question": "app.domain.intelligent_tutor.tutor_question",
    "TutorResponse": "app.domain.intelligent_tutor.tutor_response",
    "Explanation": "app.domain.intelligent_tutor.explanation",
    "ExplanationKind": "app.domain.intelligent_tutor.explanation",
    "LearningHint": "app.domain.intelligent_tutor.learning_hint",
    "CoachingMessage": "app.domain.intelligent_tutor.coaching_message",
    "ConversationMemory": "app.domain.intelligent_tutor.conversation_memory",
    "update_conversation_memory": "app.domain.intelligent_tutor.conversation_memory",
    "AssembledEvidence": "app.domain.intelligent_tutor.response_evidence",
    "EvidenceCategory": "app.domain.intelligent_tutor.response_evidence",
    "EvidenceItemRef": "app.domain.intelligent_tutor.response_evidence",
    "assemble_evidence": "app.domain.intelligent_tutor.response_evidence",
    "ResponseBlueprint": "app.domain.intelligent_tutor.response_builder",
    "build_response_blueprint": "app.domain.intelligent_tutor.response_builder",
    "EXPLANATION_VERSION": "app.domain.intelligent_tutor.explainability.version",
    "ExplanationVersion": "app.domain.intelligent_tutor.explainability.version",
    "ExplanationContext": "app.domain.intelligent_tutor.explainability.context",
    "ExplanationReference": "app.domain.intelligent_tutor.explainability.reference",
    "ExplanationResult": "app.domain.intelligent_tutor.explainability.result",
    "TutorExplanation": "app.domain.intelligent_tutor.explainability.explanation",
    "ExplanationSection": "app.domain.intelligent_tutor.explainability.section",
    "ExplanationSectionKind": "app.domain.intelligent_tutor.explainability.section",
    "ConceptExplanation": "app.domain.intelligent_tutor.explainability.section",
    "DecisionExplanation": "app.domain.intelligent_tutor.explainability.section",
    "EvidenceExplanation": "app.domain.intelligent_tutor.explainability.section",
    "LearningObjectiveExplanation": (
        "app.domain.intelligent_tutor.explainability.section"
    ),
    "MissionExplanation": "app.domain.intelligent_tutor.explainability.section",
    "TutorExplanationRequested": "app.domain.intelligent_tutor.explainability.events",
    "TutorExplanationGenerated": "app.domain.intelligent_tutor.explainability.events",
    "TutorExplanationUnavailable": "app.domain.intelligent_tutor.explainability.events",
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
