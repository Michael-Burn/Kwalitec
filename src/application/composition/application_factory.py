"""Application factory — single composition root for the Educational OS.

All dependency construction for repositories, unit of work, domain engines,
application services, AI providers, explainability, and experience generation
occurs here. Collaborators elsewhere receive injected dependencies.

Provider replacement: set ``AI_PROVIDER`` / ``EOS_AI_PROVIDER`` (and related
timeout/retry env vars) without editing this file, or pass ``ai_provider=`` /
``settings=`` at assembly time for tests.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from application.composition.container import ApplicationContainer, RequestScope
from application.composition.service_registry import ServiceRegistry
from application.pipeline import EducationalPipeline
from application.ports.clock import Clock
from application.ports.event_publisher import ApplicationEventPublisher
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
from infrastructure.composition.factories import (
    ApplicationServices,
    build_application_services,
    build_session_factory,
    build_unit_of_work,
)
from infrastructure.composition.provider_factory import build_ai_provider
from infrastructure.composition.providers import (
    ApplicationEventHandler,
    SynchronousApplicationEventPublisher,
    SystemClock,
    SystemUUIDGenerator,
)
from infrastructure.config.settings import AppSettings, load_settings
from infrastructure.events.dispatcher import EventDispatcher
from infrastructure.events.publisher import DomainEventPublisher
from infrastructure.observability.enrichment_observer import (
    ObservedMissionEnricher,
    ObservedRecommendationEnricher,
)
from infrastructure.observability.metrics import PipelineMetrics
from infrastructure.persistence.sqlalchemy.unit_of_work import SessionFactory


def _default_ai_provider(settings: AppSettings | None = None) -> AIProvider:
    """Construct the production AI provider from typed configuration."""
    resolved = settings or load_settings(validate=False)
    assert resolved.ai is not None
    return build_ai_provider(resolved.ai)


def _build_registry(
    *,
    session_factory: SessionFactory,
    unit_of_work: object,
    clock: Clock,
    uuid_generator: UUIDGenerator,
    event_publisher: ApplicationEventPublisher,
    services: ApplicationServices,
    mission_generator: type[MissionGenerator],
    recommendation_generator: type[RecommendationGenerator],
    study_planner: type[StudyPlanner],
    progress_evaluator: type[ProgressEvaluator],
    explanation_builder: type[ExplanationBuilder],
    experience_generator: type[ExperienceGenerator],
    ai_provider: AIProvider,
    mission_enricher: MissionEnricher,
    recommendation_enricher: RecommendationEnricher,
    educational_pipeline: EducationalPipeline,
) -> ServiceRegistry:
    registry = ServiceRegistry()
    registry.register("session_factory", session_factory)
    registry.register("unit_of_work", unit_of_work)
    registry.register("clock", clock)
    registry.register("uuid_generator", uuid_generator)
    registry.register("event_publisher", event_publisher)
    registry.register("learning", services.learning)
    registry.register("twin", services.twin)
    registry.register("assessment", services.assessment)
    registry.register("planning", services.planning)
    registry.register("dashboard", services.dashboard)
    registry.register("mission_generator", mission_generator)
    registry.register("recommendation_generator", recommendation_generator)
    registry.register("study_planner", study_planner)
    registry.register("progress_evaluator", progress_evaluator)
    registry.register("explanation_builder", explanation_builder)
    registry.register("experience_generator", experience_generator)
    registry.register("ai_provider", ai_provider)
    registry.register("mission_enricher", mission_enricher)
    registry.register("recommendation_enricher", recommendation_enricher)
    registry.register("educational_pipeline", educational_pipeline)
    return registry


def assemble(
    session_factory: SessionFactory,
    *,
    clock: Clock | None = None,
    uuid_generator: UUIDGenerator | None = None,
    event_publisher: ApplicationEventPublisher | None = None,
    event_handlers: Iterable[ApplicationEventHandler] = (),
    ai_provider: AIProvider | None = None,
    settings: AppSettings | None = None,
    pipeline_metrics: PipelineMetrics | None = None,
    mission_generator: type[MissionGenerator] = MissionGenerator,
    recommendation_generator: type[RecommendationGenerator] = RecommendationGenerator,
    study_planner: type[StudyPlanner] = StudyPlanner,
    progress_evaluator: type[ProgressEvaluator] = ProgressEvaluator,
    explanation_builder: type[ExplanationBuilder] = ExplanationBuilder,
    experience_generator: type[ExperienceGenerator] = ExperienceGenerator,
) -> ApplicationContainer:
    """Wire the full Educational Operating System dependency graph.

    Args:
        session_factory: SQLAlchemy session factory shared by units of work.
        clock: Optional Clock; defaults to SystemClock.
        uuid_generator: Optional UUIDGenerator; defaults to SystemUUIDGenerator.
        event_publisher: Optional application event publisher.
        event_handlers: Handlers for the default synchronous publisher.
            Mutually exclusive with ``event_publisher``.
        ai_provider: Optional AIProvider; defaults from ``AI_PROVIDER`` config.
        settings: Optional typed settings; defaults from the environment.
        pipeline_metrics: Optional shared operational metrics sink.
        mission_generator: Domain mission projection engine.
        recommendation_generator: Domain recommendation engine.
        study_planner: Domain study-planning engine.
        progress_evaluator: Domain progress-evaluation engine.
        explanation_builder: Domain explainability builder.
        experience_generator: Domain student-experience generator.

    Returns:
        Fully configured ApplicationContainer.
    """
    resolved_event_handlers = tuple(event_handlers)
    if event_publisher is not None and resolved_event_handlers:
        raise ValueError("provide event_publisher or event_handlers, not both")

    resolved_settings = settings or load_settings(validate=False)
    resolved_clock = clock or SystemClock()
    resolved_uuid_generator = uuid_generator or SystemUUIDGenerator()
    resolved_event_publisher = event_publisher or SynchronousApplicationEventPublisher(
        resolved_event_handlers
    )
    resolved_ai_provider = ai_provider or _default_ai_provider(resolved_settings)
    metrics = pipeline_metrics or PipelineMetrics()

    domain_publisher = DomainEventPublisher()
    domain_dispatcher = EventDispatcher(domain_publisher)
    unit_of_work = build_unit_of_work(
        session_factory, event_dispatcher=domain_dispatcher
    )
    services = build_application_services(
        uow=unit_of_work,
        events=resolved_event_publisher,
        clock=resolved_clock,
    )
    mission_enricher = MissionEnricher(resolved_ai_provider)
    recommendation_enricher = RecommendationEnricher(resolved_ai_provider)

    ai_enabled = bool(resolved_settings.ai and resolved_settings.ai.enabled)
    if ai_enabled:
        pipeline_mission_enricher: object | None = ObservedMissionEnricher(
            mission_enricher, metrics=metrics
        )
        pipeline_recommendation_enricher: object | None = (
            ObservedRecommendationEnricher(
                recommendation_enricher, metrics=metrics
            )
        )
    else:
        # Deterministic enrichment fallback — pipeline skips AI entirely.
        pipeline_mission_enricher = None
        pipeline_recommendation_enricher = None

    educational_pipeline = EducationalPipeline(
        mission_generator=mission_generator,
        study_planner=study_planner,
        progress_evaluator=progress_evaluator,
        recommendation_generator=recommendation_generator,
        explanation_builder=explanation_builder,
        experience_generator=experience_generator,
        mission_enricher=pipeline_mission_enricher,  # type: ignore[arg-type]
        recommendation_enricher=pipeline_recommendation_enricher,  # type: ignore[arg-type]
    )
    # Keep a reference for create_app / diagnostics without altering the
    # ApplicationContainer contract (APP-004 operational readiness).
    educational_pipeline.__dict__["pipeline_metrics"] = metrics

    # Lazy import avoids circular import with application.composition package init.
    from infrastructure.composition.product_factories import build_product_services

    product = build_product_services(
        session_factory,
        events=resolved_event_publisher,
        clock=resolved_clock,  # type: ignore[arg-type]
        educational_pipeline=educational_pipeline,
    )

    registry = _build_registry(
        session_factory=session_factory,
        unit_of_work=unit_of_work,
        clock=resolved_clock,
        uuid_generator=resolved_uuid_generator,
        event_publisher=resolved_event_publisher,
        services=services,
        mission_generator=mission_generator,
        recommendation_generator=recommendation_generator,
        study_planner=study_planner,
        progress_evaluator=progress_evaluator,
        explanation_builder=explanation_builder,
        experience_generator=experience_generator,
        ai_provider=resolved_ai_provider,
        mission_enricher=mission_enricher,
        recommendation_enricher=recommendation_enricher,
        educational_pipeline=educational_pipeline,
    )

    return ApplicationContainer(
        session_factory=session_factory,
        unit_of_work=unit_of_work,
        clock=resolved_clock,
        uuid_generator=resolved_uuid_generator,
        event_publisher=resolved_event_publisher,
        services=services,
        product=product,
        mission_generator=mission_generator,
        recommendation_generator=recommendation_generator,
        study_planner=study_planner,
        progress_evaluator=progress_evaluator,
        explanation_builder=explanation_builder,
        experience_generator=experience_generator,
        ai_provider=resolved_ai_provider,
        mission_enricher=mission_enricher,
        recommendation_enricher=recommendation_enricher,
        educational_pipeline=educational_pipeline,
        registry=registry,
    )


def create_application(
    bind: Any,
    *,
    clock: Clock | None = None,
    uuid_generator: UUIDGenerator | None = None,
    event_publisher: ApplicationEventPublisher | None = None,
    event_handlers: Iterable[ApplicationEventHandler] = (),
    ai_provider: AIProvider | None = None,
    settings: AppSettings | None = None,
    pipeline_metrics: PipelineMetrics | None = None,
    mission_generator: type[MissionGenerator] = MissionGenerator,
    recommendation_generator: type[RecommendationGenerator] = RecommendationGenerator,
    study_planner: type[StudyPlanner] = StudyPlanner,
    progress_evaluator: type[ProgressEvaluator] = ProgressEvaluator,
    explanation_builder: type[ExplanationBuilder] = ExplanationBuilder,
    experience_generator: type[ExperienceGenerator] = ExperienceGenerator,
    **engine_kwargs: Any,
) -> ApplicationContainer:
    """Construct a session factory and assemble the complete dependency graph.

    Args:
        bind: SQLAlchemy ``Engine`` or database URL string.
    """
    session_factory = build_session_factory(bind, **engine_kwargs)
    return assemble(
        session_factory,
        clock=clock,
        uuid_generator=uuid_generator,
        event_publisher=event_publisher,
        event_handlers=event_handlers,
        ai_provider=ai_provider,
        settings=settings,
        pipeline_metrics=pipeline_metrics,
        mission_generator=mission_generator,
        recommendation_generator=recommendation_generator,
        study_planner=study_planner,
        progress_evaluator=progress_evaluator,
        explanation_builder=explanation_builder,
        experience_generator=experience_generator,
    )


def create_request_scope(container: ApplicationContainer) -> RequestScope:
    """Create a request-scoped unit of work and application services.

    Construction of the scoped UnitOfWork and services remains inside the
    composition root so web/presentation layers never call constructors.
    """
    dispatcher = EventDispatcher(DomainEventPublisher())
    unit_of_work = build_unit_of_work(
        container.session_factory,
        event_dispatcher=dispatcher,
    )
    services = build_application_services(
        uow=unit_of_work,
        events=container.event_publisher,
        clock=container.clock,
    )
    return RequestScope(unit_of_work=unit_of_work, services=services)
