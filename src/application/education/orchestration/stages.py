"""Canonical Educational Orchestration stages in lawful execution order.

Architecture Source
    EDU-003.6 Educational Orchestration Layer

Stages record composition progress. They are not educational decisions.
"""

from __future__ import annotations

from enum import StrEnum


class OrchestrationStage(StrEnum):
    """Lawful orchestration stage names for Education OS composition."""

    RECORD_EVIDENCE = "record_evidence"
    LOAD_STUDENT_STATE = "load_student_state"
    LOAD_KNOWLEDGE_GRAPH = "load_knowledge_graph"
    LOAD_EVIDENCE = "load_evidence"
    ESTIMATE_MASTERY = "estimate_mastery"
    GENERATE_RECOMMENDATIONS = "generate_recommendations"
    PUBLISH_ASSESSMENT = "publish_assessment"
    PUBLISH_RECOMMENDATIONS = "publish_recommendations"
    COMPOSE_RESULT = "compose_result"


# Full interaction pipeline order (evidence-producing workflows).
INTERACTION_PIPELINE: tuple[OrchestrationStage, ...] = (
    OrchestrationStage.RECORD_EVIDENCE,
    OrchestrationStage.LOAD_STUDENT_STATE,
    OrchestrationStage.LOAD_KNOWLEDGE_GRAPH,
    OrchestrationStage.LOAD_EVIDENCE,
    OrchestrationStage.ESTIMATE_MASTERY,
    OrchestrationStage.GENERATE_RECOMMENDATIONS,
    OrchestrationStage.PUBLISH_ASSESSMENT,
    OrchestrationStage.PUBLISH_RECOMMENDATIONS,
    OrchestrationStage.COMPOSE_RESULT,
)

# Evaluation / refresh pipeline (no new interaction evidence).
EVALUATION_PIPELINE: tuple[OrchestrationStage, ...] = (
    OrchestrationStage.LOAD_STUDENT_STATE,
    OrchestrationStage.LOAD_KNOWLEDGE_GRAPH,
    OrchestrationStage.LOAD_EVIDENCE,
    OrchestrationStage.ESTIMATE_MASTERY,
    OrchestrationStage.GENERATE_RECOMMENDATIONS,
    OrchestrationStage.PUBLISH_ASSESSMENT,
    OrchestrationStage.PUBLISH_RECOMMENDATIONS,
    OrchestrationStage.COMPOSE_RESULT,
)
