"""Tests for EducationalDashboardComposer (Capability 3.5.1).

Covers feature-flag gating, Twin/curriculum fallback, successful composition,
and absence of educational reasoning in the composer module.
"""

from __future__ import annotations

import ast
from datetime import date
from pathlib import Path

from app.application.config import EducationalIntelligenceFeatureFlags
from app.application.curriculum.curriculum_context_builder import MissingCurriculumError
from app.application.dashboard import (
    DashboardCompositionContext,
    DashboardViewModel,
    EducationalDashboardComposer,
)
from app.application.orchestration import EducationalOrchestrator
from app.application.twin import TwinAbsenceReason, TwinAbsent, TwinProvider
from app.domain.readiness import (
    CurriculumContext,
    CurriculumFormat,
    CurriculumTopicRef,
)
from app.domain.twin import DigitalTwin, GoalState, IdentityState

COMPOSER_PATH = (
    Path(__file__).resolve().parents[2]
    / "app"
    / "application"
    / "dashboard"
    / "educational_dashboard_composer.py"
)

FLAGS_OFF = EducationalIntelligenceFeatureFlags()
FLAGS_ORCHESTRATOR = EducationalIntelligenceFeatureFlags(
    ENABLE_EDUCATIONAL_ORCHESTRATOR=True,
)
FLAGS_RECOMMENDATIONS = EducationalIntelligenceFeatureFlags(
    ENABLE_EDUCATIONAL_ORCHESTRATOR=True,
    ENABLE_EI_RECOMMENDATIONS=True,
)


def _identity(student_id: str = "42") -> IdentityState:
    return IdentityState.create(
        student_id=student_id,
        curriculum_id="1",
        current_exam="CS1",
        target_sitting=date(2026, 9, 15),
    )


def _twin(student_id: str = "42") -> DigitalTwin:
    return DigitalTwin.create(
        _identity(student_id),
        goals=GoalState.create(
            target_pass_probability=0.8,
            target_completion_date=date(2026, 9, 15),
            planned_study_hours_per_week=10.0,
        ),
    )


def _curriculum() -> CurriculumContext:
    return CurriculumContext.create(
        "1",
        format=CurriculumFormat.V1,
        topics=[
            CurriculumTopicRef.create("topic-a", weight=0.5),
            CurriculumTopicRef.create("topic-b", weight=0.5),
        ],
    )


class _TwinSource:
    def __init__(
        self,
        twin: DigitalTwin | None = None,
        *,
        error: Exception | None = None,
    ):
        self.twin = twin
        self.error = error

    def load(self, student_id: str, *, context=None) -> DigitalTwin | None:
        if self.error is not None:
            raise self.error
        return self.twin


class _RecordingBuilder:
    def __init__(
        self,
        curriculum: CurriculumContext | None = None,
        *,
        error: Exception | None = None,
    ):
        self.curriculum = curriculum or _curriculum()
        self.error = error
        self.calls: list[int | None] = []

    def build(self, curriculum_id: int | None) -> CurriculumContext:
        self.calls.append(curriculum_id)
        if self.error is not None:
            raise self.error
        return self.curriculum


class TestEducationalDashboardComposerFlags:
    def test_flag_off_returns_none_without_twin_lookup(self) -> None:
        source = _TwinSource(_twin())
        provider = TwinProvider(source=source)
        composer = EducationalDashboardComposer(
            twin_provider=provider,
            flags=FLAGS_OFF,
        )
        result = composer.compose(
            DashboardCompositionContext(student_id="42", curriculum_id=1)
        )
        assert result is None

    def test_flag_on_with_twin_returns_view_model(self) -> None:
        composer = EducationalDashboardComposer(
            orchestrator=EducationalOrchestrator(
                twin_provider=TwinProvider(source=_TwinSource(_twin())),
                curriculum_context_builder=_RecordingBuilder(),
            ),
            flags=FLAGS_RECOMMENDATIONS,
        )
        result = composer.compose(
            DashboardCompositionContext(
                student_id="42",
                curriculum_id=1,
                available_minutes=60,
            )
        )
        assert isinstance(result, DashboardViewModel)
        assert result.recommendation_card is not None
        assert result.recommendation_card.title


class TestEducationalDashboardComposerFallback:
    def test_missing_twin_returns_none(self) -> None:
        composer = EducationalDashboardComposer(
            twin_provider=TwinProvider(source=_TwinSource(None)),
            flags=FLAGS_ORCHESTRATOR,
        )
        result = composer.compose(
            DashboardCompositionContext(student_id="42", curriculum_id=1)
        )
        assert result is None

    def test_default_twin_provider_without_source_returns_none(self) -> None:
        composer = EducationalDashboardComposer(flags=FLAGS_ORCHESTRATOR)
        result = composer.compose(
            DashboardCompositionContext(student_id="42", curriculum_id=1)
        )
        assert result is None

    def test_missing_curriculum_id_returns_none(self) -> None:
        composer = EducationalDashboardComposer(
            twin_provider=TwinProvider(source=_TwinSource(_twin())),
            flags=FLAGS_ORCHESTRATOR,
        )
        result = composer.compose(
            DashboardCompositionContext(student_id="42", curriculum_id=None)
        )
        assert result is None

    def test_curriculum_builder_failure_returns_none(self) -> None:
        composer = EducationalDashboardComposer(
            orchestrator=EducationalOrchestrator(
                twin_provider=TwinProvider(source=_TwinSource(_twin())),
                curriculum_context_builder=_RecordingBuilder(
                    error=MissingCurriculumError("curriculum not found"),
                ),
            ),
            flags=FLAGS_ORCHESTRATOR,
        )
        result = composer.compose(
            DashboardCompositionContext(student_id="42", curriculum_id=99)
        )
        assert result is None

    def test_does_not_fabricate_twin_on_absence(self) -> None:
        provider = TwinProvider(source=None)
        absent = provider.retrieve("42")
        assert isinstance(absent, TwinAbsent)
        assert absent.reason is TwinAbsenceReason.MISSING

        composer = EducationalDashboardComposer(
            twin_provider=provider,
            flags=FLAGS_ORCHESTRATOR,
        )
        assert (
            composer.compose(
                DashboardCompositionContext(student_id="42", curriculum_id=1)
            )
            is None
        )


class TestEducationalDashboardComposerIntegrity:
    def test_invokes_curriculum_builder_via_orchestrator(self) -> None:
        builder = _RecordingBuilder()
        composer = EducationalDashboardComposer(
            orchestrator=EducationalOrchestrator(
                twin_provider=TwinProvider(source=_TwinSource(_twin())),
                curriculum_context_builder=builder,
            ),
            flags=FLAGS_ORCHESTRATOR,
        )
        composer.compose(
            DashboardCompositionContext(student_id="42", curriculum_id=7)
        )
        assert builder.calls == [7]

    def test_framework_independent(self) -> None:
        source = COMPOSER_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert not alias.name.startswith("flask")
            if isinstance(node, ast.ImportFrom) and node.module:
                assert not node.module.startswith("flask")
                assert not node.module.startswith("app.dashboard")
                assert not node.module.startswith("app.services")

    def test_no_hybrid_or_legacy_service_imports(self) -> None:
        source = COMPOSER_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
                imported.update(
                    f"{node.module}.{alias.name}" for alias in node.names
                )
        assert not any("RecommendationService" in name for name in imported)
        assert not any("ReadinessService" in name for name in imported)
        assert "hybrid" not in source.lower()
