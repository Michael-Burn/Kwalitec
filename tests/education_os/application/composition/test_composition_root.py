"""Composition-root assembly and dependency-injection tests (APP-001)."""

from __future__ import annotations

import ast
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from application.composition import (
    SERVICE_NAMES,
    ApplicationContainer,
    CompositionError,
    RequestScope,
    ServiceRegistry,
    assemble,
    create_application,
    create_request_scope,
)
from application.pipeline import EducationalPipeline
from application.ports.clock import Clock
from application.ports.event_publisher import ApplicationEventPublisher
from application.ports.uuid_generator import UUIDGenerator
from application.services import (
    AssessmentApplicationService,
    DashboardApplicationService,
    LearningApplicationService,
    PlanningApplicationService,
    TwinApplicationService,
)
from domain.explainability import ExplanationBuilder
from domain.mission_generation import MissionGenerator
from domain.progress_evaluation import ProgressEvaluator
from domain.recommendation import RecommendationGenerator
from domain.student_experience import ExperienceGenerator
from domain.study_planning import StudyPlanner
from infrastructure.ai.enrichment.mission_enricher import MissionEnricher
from infrastructure.ai.enrichment.recommendation_enricher import RecommendationEnricher
from infrastructure.ai.providers.ai_provider import AIProvider
from infrastructure.ai.providers.openai_provider import OpenAIProvider
from infrastructure.composition import (
    SynchronousApplicationEventPublisher,
    SystemClock,
    SystemUUIDGenerator,
)
from infrastructure.persistence.sqlalchemy import SqlAlchemyUnitOfWork
from infrastructure.resilience import ResilientAIProvider
from tests.education_os.application.fakes import (
    FixedClock,
    InMemoryEventPublisher,
    SequenceUUIDGenerator,
)
from tests.education_os.infrastructure.ai.helpers import FakeAIProvider

COMPOSITION_ROOT = (
    Path(__file__).resolve().parents[4] / "src" / "application" / "composition"
)
SRC_ROOT = Path(__file__).resolve().parents[4] / "src"


def make_session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=create_engine("sqlite+pysqlite:///:memory:"))


def test_assemble_wires_complete_dependency_graph() -> None:
    session_factory = make_session_factory()

    container = assemble(session_factory)

    assert isinstance(container, ApplicationContainer)
    assert container.session_factory is session_factory
    assert isinstance(container.unit_of_work, SqlAlchemyUnitOfWork)
    assert isinstance(container.clock, SystemClock)
    assert isinstance(container.uuid_generator, SystemUUIDGenerator)
    assert isinstance(
        container.event_publisher,
        SynchronousApplicationEventPublisher,
    )
    assert isinstance(container.services.learning, LearningApplicationService)
    assert isinstance(container.services.twin, TwinApplicationService)
    assert isinstance(container.services.assessment, AssessmentApplicationService)
    assert isinstance(container.services.planning, PlanningApplicationService)
    assert isinstance(container.services.dashboard, DashboardApplicationService)
    assert container.mission_generator is MissionGenerator
    assert container.recommendation_generator is RecommendationGenerator
    assert container.study_planner is StudyPlanner
    assert container.progress_evaluator is ProgressEvaluator
    assert container.explanation_builder is ExplanationBuilder
    assert container.experience_generator is ExperienceGenerator
    provider = container.ai_provider
    if isinstance(provider, ResilientAIProvider):
        provider = provider.inner
    assert isinstance(provider, OpenAIProvider)
    assert isinstance(container.mission_enricher, MissionEnricher)
    assert isinstance(container.recommendation_enricher, RecommendationEnricher)
    assert container.mission_enricher.provider is container.ai_provider
    assert container.recommendation_enricher.provider is container.ai_provider
    assert isinstance(container.educational_pipeline, EducationalPipeline)
    assert isinstance(container.registry, ServiceRegistry)
    assert container.registry.missing_names() == ()
    assert container.registry.registered_names() == SERVICE_NAMES


def test_dependency_graph_shares_injected_collaborators() -> None:
    clock = FixedClock()
    uuids = SequenceUUIDGenerator()
    events = InMemoryEventPublisher()
    provider = FakeAIProvider()

    container = assemble(
        make_session_factory(),
        clock=clock,
        uuid_generator=uuids,
        event_publisher=events,
        ai_provider=provider,
    )

    assert container.clock is clock
    assert container.uuid_generator is uuids
    assert container.event_publisher is events
    assert container.ai_provider is provider
    for service in (
        container.services.learning,
        container.services.twin,
        container.services.assessment,
        container.services.planning,
    ):
        assert service._uow is container.unit_of_work
        assert service._clock is clock
        assert service._events is events
    assert container.services.dashboard._twin is container.services.twin
    assert container.services.dashboard._planning is container.services.planning
    assert container.services.dashboard._clock is clock
    assert container.registry.get("ai_provider") is provider
    assert container.registry.get("clock") is clock
    assert container.registry.get("learning") is container.services.learning


def test_provider_replacement_uses_injected_ai_provider() -> None:
    provider = FakeAIProvider(name="replacement")

    container = assemble(make_session_factory(), ai_provider=provider)

    assert container.ai_provider is provider
    assert container.mission_enricher.provider is provider
    assert container.recommendation_enricher.provider is provider
    assert isinstance(container.ai_provider, AIProvider)
    assert not isinstance(container.ai_provider, OpenAIProvider)


def test_default_ai_provider_is_only_constructed_in_application_factory() -> None:
    factory_source = (
        COMPOSITION_ROOT / "application_factory.py"
    ).read_text(encoding="utf-8")
    other_sources = [
        (COMPOSITION_ROOT / "container.py").read_text(encoding="utf-8"),
        (COMPOSITION_ROOT / "service_registry.py").read_text(encoding="utf-8"),
        (COMPOSITION_ROOT / "__init__.py").read_text(encoding="utf-8"),
    ]

    # APP-004: default provider comes from config-driven build_ai_provider.
    assert "build_ai_provider" in factory_source
    assert "_default_ai_provider" in factory_source
    for source in other_sources:
        assert "OpenAIProvider(" not in source
        assert "build_ai_provider(" not in source


def test_create_application_constructs_session_factory_from_bind() -> None:
    container = create_application("sqlite+pysqlite:///:memory:")

    with container.unit_of_work:
        assert container.unit_of_work.is_active


def test_create_request_scope_builds_isolated_unit_of_work() -> None:
    container = assemble(make_session_factory())

    scope = create_request_scope(container)

    assert isinstance(scope, RequestScope)
    assert scope.unit_of_work is not container.unit_of_work
    assert isinstance(scope.services.learning, LearningApplicationService)
    assert scope.services.learning._uow is scope.unit_of_work
    assert scope.services.learning._events is container.event_publisher
    assert scope.services.learning._clock is container.clock


def test_registry_replace_updates_registration() -> None:
    container = assemble(make_session_factory())
    replacement = FakeAIProvider(name="registry-fake")

    previous = container.registry.replace("ai_provider", replacement)

    if isinstance(previous, ResilientAIProvider):
        previous = previous.inner
    assert isinstance(previous, OpenAIProvider)
    assert container.registry.get("ai_provider") is replacement

def test_registry_rejects_unknown_and_duplicate_names() -> None:
    registry = ServiceRegistry()
    registry.register("clock", FixedClock())

    with pytest.raises(CompositionError, match="Unknown"):
        registry.register("not-a-service", object())
    with pytest.raises(CompositionError, match="already registered"):
        registry.register("clock", FixedClock())
    with pytest.raises(CompositionError, match="unregistered"):
        registry.replace("learning", object())


def test_default_providers_satisfy_application_ports() -> None:
    clock = SystemClock()
    uuids = SystemUUIDGenerator()
    events = SynchronousApplicationEventPublisher()

    assert isinstance(clock, Clock)
    assert isinstance(uuids, UUIDGenerator)
    assert isinstance(events, ApplicationEventPublisher)
    assert clock.now().tzinfo is UTC
    assert str(UUID(uuids.new_id()))


def test_event_handlers_and_publisher_are_mutually_exclusive() -> None:
    with pytest.raises(ValueError, match="not both"):
        assemble(
            make_session_factory(),
            event_publisher=InMemoryEventPublisher(),
            event_handlers=(lambda event: None,),
        )


def test_event_publisher_notifies_injected_handlers_in_order() -> None:
    from application.events.base import ApplicationEvent

    published: list[tuple[str, ApplicationEvent]] = []
    event = ApplicationEvent(occurred_at=datetime(2026, 7, 20, tzinfo=UTC))
    container = assemble(
        make_session_factory(),
        event_handlers=(
            lambda value: published.append(("first", value)),
            lambda value: published.append(("second", value)),
        ),
    )

    container.event_publisher.publish(event)

    assert published == [("first", event), ("second", event)]


def _module_imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
            names.add(node.module)
    return names


def test_no_circular_dependencies_in_composition_root() -> None:
    """Composition may import infrastructure; infrastructure must not import back."""
    composition_files = sorted(COMPOSITION_ROOT.rglob("*.py"))
    infra_composition = SRC_ROOT / "infrastructure" / "composition"

    for path in composition_files:
        source = path.read_text(encoding="utf-8")
        assert "from sqlalchemy" not in source
        assert "import sqlalchemy" not in source
        if path.name == "application_factory.py":
            assert "infrastructure.composition.container" not in source

    for path in sorted(infra_composition.rglob("*.py")):
        imported = _module_imports(path)
        assert "application.composition" not in imported
        assert not any(
            name.startswith("application.composition") for name in imported
        ), f"{path.name} imports application.composition"


def test_composition_package_has_no_import_cycles_internally() -> None:
    graph: dict[str, set[str]] = defaultdict(set)
    package = "application.composition"
    files = {
        path: f"{package}.{path.stem}" if path.name != "__init__.py" else package
        for path in COMPOSITION_ROOT.glob("*.py")
    }

    for path, module_name in files.items():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                if node.module == package or node.module.startswith(f"{package}."):
                    graph[module_name].add(node.module)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == package or alias.name.startswith(f"{package}."):
                        graph[module_name].add(alias.name)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visited:
            return
        assert node not in visiting, f"cycle involving {node}"
        visiting.add(node)
        for child in graph.get(node, ()):
            visit(child)
        visiting.remove(node)
        visited.add(node)

    for name in files.values():
        visit(name)
