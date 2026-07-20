"""Observability wrappers for AI enrichers (timing + success/failure metrics)."""

from __future__ import annotations

from typing import Protocol

from domain.mission_generation.mission_specification import MissionSpecification
from domain.recommendation.recommendation_specification import (
    RecommendationSpecification,
)
from domain.student_experience.student_experience import StudentExperience
from infrastructure.observability.logging import StructuredLogger
from infrastructure.observability.metrics import PipelineMetrics
from infrastructure.observability.timing import timed


class _MissionEnricherLike(Protocol):
    def enrich(
        self,
        mission: MissionSpecification,
        experience: StudentExperience,
    ) -> object: ...


class _RecommendationEnricherLike(Protocol):
    def enrich(
        self,
        recommendations: RecommendationSpecification,
        experience: StudentExperience,
    ) -> object: ...


class ObservedMissionEnricher:
    """Record AI enrichment timing without changing enrichment behaviour."""

    def __init__(
        self,
        enricher: _MissionEnricherLike,
        *,
        metrics: PipelineMetrics,
        logger: StructuredLogger | None = None,
    ) -> None:
        self._enricher = enricher
        self._metrics = metrics
        self._logger = logger or StructuredLogger("kwalitec.eos.ai")

    def enrich(
        self,
        mission: MissionSpecification,
        experience: StudentExperience,
    ) -> object:
        self._metrics.incr("ai_enrichment_started")
        try:
            with timed("ai_enrichment_mission") as slot:
                result = self._enricher.enrich(mission, experience)
            self._metrics.record_timing("ai_enrichment_mission", slot[0])
            self._metrics.incr("ai_enrichment_succeeded")
            self._logger.info(
                "ai_enrichment_succeeded",
                event="ai_enrichment_succeeded",
                target="mission",
                duration_ms=round(slot[0], 3),
            )
            return result
        except Exception as exc:
            self._metrics.incr("ai_enrichment_failed")
            self._metrics.incr("ai_enrichment_fallback")
            self._logger.warning(
                "ai_enrichment_failed",
                event="ai_enrichment_failed",
                target="mission",
                error_type=type(exc).__name__,
            )
            raise


class ObservedRecommendationEnricher:
    """Record recommendation enrichment timing without changing behaviour."""

    def __init__(
        self,
        enricher: _RecommendationEnricherLike,
        *,
        metrics: PipelineMetrics,
        logger: StructuredLogger | None = None,
    ) -> None:
        self._enricher = enricher
        self._metrics = metrics
        self._logger = logger or StructuredLogger("kwalitec.eos.ai")

    def enrich(
        self,
        recommendations: RecommendationSpecification,
        experience: StudentExperience,
    ) -> object:
        self._metrics.incr("ai_enrichment_started")
        try:
            with timed("ai_enrichment_recommendations") as slot:
                result = self._enricher.enrich(recommendations, experience)
            self._metrics.record_timing("ai_enrichment_recommendations", slot[0])
            self._metrics.incr("ai_enrichment_succeeded")
            self._logger.info(
                "ai_enrichment_succeeded",
                event="ai_enrichment_succeeded",
                target="recommendations",
                duration_ms=round(slot[0], 3),
            )
            return result
        except Exception as exc:
            self._metrics.incr("ai_enrichment_failed")
            self._metrics.incr("ai_enrichment_fallback")
            self._logger.warning(
                "ai_enrichment_failed",
                event="ai_enrichment_failed",
                target="recommendations",
                error_type=type(exc).__name__,
            )
            raise
