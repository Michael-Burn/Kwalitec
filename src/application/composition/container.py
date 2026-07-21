"""Typed dependency graph assembled by the application composition root."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from application.composition.service_registry import ServiceRegistry
from application.pipeline import EducationalPipeline
from application.ports.clock import Clock
from application.ports.event_publisher import ApplicationEventPublisher
from application.ports.unit_of_work import UnitOfWork
from application.ports.uuid_generator import UUIDGenerator
from domain.explainability import ExplanationBuilder
from domain.mission_generation import MissionGenerator
from domain.progress_evaluation import ProgressEvaluator
from domain.recommendation import RecommendationGenerator
from domain.student_experience import ExperienceGenerator
from domain.study_planning import StudyPlanner
from infrastructure.ai.enrichment.mission_enricher import MissionEnricher
from infrastructure.ai.enrichment.recommendation_enricher import RecommendationEnricher
from infrastructure.ai.providers.ai_provider import AIProvider
from infrastructure.composition.factories import ApplicationServices

if TYPE_CHECKING:
    from infrastructure.composition.product_factories import ProductServices
    from infrastructure.persistence.sqlalchemy.unit_of_work import SessionFactory


@dataclass(frozen=True, slots=True)
class ApplicationContainer:
    """Explicit dependency graph for one Educational Operating System scope.

    Constructed only by ``application.composition.application_factory``.
    Callers receive fully wired collaborators; they must not construct
    repositories, providers, or services themselves.
    """

    session_factory: SessionFactory
    unit_of_work: UnitOfWork
    clock: Clock
    uuid_generator: UUIDGenerator
    event_publisher: ApplicationEventPublisher
    services: ApplicationServices
    product: ProductServices
    mission_generator: type[MissionGenerator]
    recommendation_generator: type[RecommendationGenerator]
    study_planner: type[StudyPlanner]
    progress_evaluator: type[ProgressEvaluator]
    explanation_builder: type[ExplanationBuilder]
    experience_generator: type[ExperienceGenerator]
    ai_provider: AIProvider
    mission_enricher: MissionEnricher
    recommendation_enricher: RecommendationEnricher
    educational_pipeline: EducationalPipeline
    registry: ServiceRegistry


@dataclass(frozen=True, slots=True)
class RequestScope:
    """Request-scoped unit of work and application services."""

    unit_of_work: UnitOfWork
    services: ApplicationServices
