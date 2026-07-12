"""Tests for DashboardAssembler (Capability 3.4.3).

Covers immutable DashboardViewModel, feature-flag gating, warning / empty-state
propagation, RecommendationCardBuilder reuse, framework independence, and
absence of domain leakage.
"""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, fields, is_dataclass, replace
from datetime import date
from pathlib import Path
from typing import get_args, get_origin
from unittest.mock import patch

import pytest

from app.application.config import EducationalIntelligenceFeatureFlags
from app.application.dashboard import (
    DashboardAssembler,
    DashboardViewModel,
    RecommendationCardBuilder,
    RecommendationCardViewModel,
)
from app.application.orchestration import (
    EducationalExperience,
    EducationalOrchestrator,
)
from app.domain.decision import Constraints, IntensityPosture
from app.domain.readiness import (
    CurriculumContext,
    CurriculumFormat,
    CurriculumTopicRef,
)
from app.domain.twin import DigitalTwin, GoalState, IdentityState

DASHBOARD_ROOT = (
    Path(__file__).resolve().parents[2] / "app" / "application" / "dashboard"
)

FORBIDDEN_ROOT_MODULES = frozenset(
    {
        "flask",
        "flask_login",
        "flask_sqlalchemy",
        "flask_wtf",
        "wtforms",
        "dotenv",
    }
)

FORBIDDEN_PREFIXES = (
    "app.auth",
    "app.dashboard",
    "app.mission",
    "app.analytics",
    "app.models",
    "app.services",
)

ALLOWED_VALUE_TYPES = (str, bool, int, type(None), tuple)
FORBIDDEN_DOMAIN_TYPE_NAMES = frozenset(
    {
        "Decision",
        "Recommendation",
        "Mission",
        "DigitalTwin",
        "ReadinessState",
        "SelectedAction",
        "ActionableSuggestion",
        "DecisionLineage",
        "ExplanationChainPresentation",
        "MissionTask",
        "OverallPosture",
        "WarrantPosture",
        "CurriculumContext",
    }
)

FLAGS_OFF = EducationalIntelligenceFeatureFlags()
FLAGS_RECOMMENDATIONS = EducationalIntelligenceFeatureFlags(
    ENABLE_EI_RECOMMENDATIONS=True,
)
FLAGS_MISSIONS = EducationalIntelligenceFeatureFlags(
    ENABLE_EI_MISSIONS=True,
)
FLAGS_EXPLAINABILITY = EducationalIntelligenceFeatureFlags(
    ENABLE_EI_RECOMMENDATIONS=True,
    ENABLE_EI_EXPLAINABILITY=True,
)
FLAGS_PROGRESS = EducationalIntelligenceFeatureFlags(
    ENABLE_EI_PROGRESS=True,
)
FLAGS_ALL = EducationalIntelligenceFeatureFlags(
    ENABLE_EI_RECOMMENDATIONS=True,
    ENABLE_EI_MISSIONS=True,
    ENABLE_EI_EXPLAINABILITY=True,
    ENABLE_EI_PROGRESS=True,
)


# ═══════════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════════


def _identity(**overrides: object) -> IdentityState:
    defaults: dict[str, object] = {
        "student_id": "student-42",
        "curriculum_id": "CS1-2026",
        "current_exam": "CS1",
        "target_sitting": date(2026, 9, 15),
    }
    defaults.update(overrides)
    return IdentityState.create(**defaults)  # type: ignore[arg-type]


def _curriculum() -> CurriculumContext:
    return CurriculumContext.create(
        "CS1-2026",
        format=CurriculumFormat.V1,
        topics=[
            CurriculumTopicRef.create("topic-a", weight=0.4),
            CurriculumTopicRef.create("topic-b", weight=0.4),
            CurriculumTopicRef.create("topic-c", weight=0.2),
        ],
    )


def _twin() -> DigitalTwin:
    return DigitalTwin.create(
        _identity(),
        goals=GoalState.create(
            target_pass_probability=0.8,
            target_completion_date=date(2026, 9, 15),
            planned_study_hours_per_week=10.0,
        ),
    )


def _constraints() -> Constraints:
    return Constraints.create(
        available_minutes=60,
        intensity=IntensityPosture.AMPLE,
    )


class _RecordingBuilder:
    def __init__(self, curriculum: CurriculumContext):
        self.curriculum = curriculum

    def build(self, curriculum_id: int | None) -> CurriculumContext:
        return self.curriculum


def _experience() -> EducationalExperience:
    orchestrator = EducationalOrchestrator(
        curriculum_context_builder=_RecordingBuilder(_curriculum()),
    )
    return orchestrator.build_experience(
        curriculum_id=1,
        twin=_twin(),
        constraints=_constraints(),
    )


def _cold_start_experience() -> EducationalExperience:
    twin = DigitalTwin.create(_identity())
    orchestrator = EducationalOrchestrator(
        curriculum_context_builder=_RecordingBuilder(_curriculum()),
    )
    return orchestrator.build_experience(
        curriculum_id=1,
        twin=twin,
        constraints=_constraints(),
    )


def _tagged_experience(
    *,
    warnings: tuple[str, ...] = (),
    empty_state_guidance: tuple[str, ...] = (),
) -> EducationalExperience:
    experience = _experience()
    return EducationalExperience(
        student_summary=experience.student_summary,
        todays_recommendation=experience.todays_recommendation,
        todays_mission=experience.todays_mission,
        readiness_summary=experience.readiness_summary,
        progress_snapshot=experience.progress_snapshot,
        explainability=experience.explainability,
        warnings=warnings,
        empty_state_guidance=empty_state_guidance,
        metadata=experience.metadata,
    )


def _annotation_type_names(annotation: object) -> set[str]:
    names: set[str] = set()
    origin = get_origin(annotation)
    if origin is not None:
        for arg in get_args(annotation):
            names |= _annotation_type_names(arg)
        return names
    if annotation is type(None):
        return names
    if isinstance(annotation, str):
        names.add(annotation)
        return names
    name = getattr(annotation, "__name__", None)
    if isinstance(name, str):
        names.add(name)
    return names


def _assert_presentation_tree(value: object, *, path: str = "root") -> None:
    """Recursively assert ViewModel values are presentation primitives only."""
    if value is None or isinstance(value, str | bool | int):
        return
    if isinstance(value, tuple):
        for index, item in enumerate(value):
            _assert_presentation_tree(item, path=f"{path}[{index}]")
        return
    if is_dataclass(value) and not isinstance(value, type):
        for field in fields(value):
            _assert_presentation_tree(
                getattr(value, field.name),
                path=f"{path}.{field.name}",
            )
        return
    raise AssertionError(f"{path} leaked non-presentation type: {type(value)!r}")


# ═══════════════════════════════════════════════════════════════════════════════
# Immutable DashboardViewModel
# ═══════════════════════════════════════════════════════════════════════════════


class TestImmutableDashboardViewModel:
    def test_returns_dashboard_view_model(self) -> None:
        vm = DashboardAssembler.assemble(_experience(), flags=FLAGS_ALL)
        assert isinstance(vm, DashboardViewModel)

    def test_view_model_is_frozen(self) -> None:
        vm = DashboardAssembler.assemble(_experience(), flags=FLAGS_ALL)
        with pytest.raises(FrozenInstanceError):
            vm.warnings = ("mutated",)  # type: ignore[misc]

    def test_nested_cards_are_frozen(self) -> None:
        vm = DashboardAssembler.assemble(_experience(), flags=FLAGS_ALL)
        assert vm.recommendation_card is not None
        assert vm.mission_card is not None
        with pytest.raises(FrozenInstanceError):
            vm.recommendation_card.title = "x"  # type: ignore[misc]
        with pytest.raises(FrozenInstanceError):
            vm.mission_card.title = "x"  # type: ignore[misc]


# ═══════════════════════════════════════════════════════════════════════════════
# Feature flags
# ═══════════════════════════════════════════════════════════════════════════════


class TestRecommendationFlag:
    def test_default_flags_omit_recommendation_card(self) -> None:
        vm = DashboardAssembler.assemble(_experience())
        assert vm.recommendation_card is None
        assert vm.feature_visibility.recommendations is False

    def test_recommendations_flag_places_card(self) -> None:
        vm = DashboardAssembler.assemble(_experience(), flags=FLAGS_RECOMMENDATIONS)
        assert isinstance(vm.recommendation_card, RecommendationCardViewModel)
        assert vm.feature_visibility.recommendations is True

    def test_recommendations_flag_off_leaves_empty_section(self) -> None:
        vm = DashboardAssembler.assemble(_experience(), flags=FLAGS_OFF)
        assert vm.recommendation_card is None


class TestMissionFlag:
    def test_default_flags_omit_mission_card(self) -> None:
        vm = DashboardAssembler.assemble(_experience())
        assert vm.mission_card is None
        assert vm.feature_visibility.missions is False

    def test_missions_flag_places_card(self) -> None:
        vm = DashboardAssembler.assemble(_experience(), flags=FLAGS_MISSIONS)
        assert vm.mission_card is not None
        assert vm.mission_card.title.strip()
        assert vm.feature_visibility.missions is True

    def test_missions_flag_off_leaves_empty_section(self) -> None:
        vm = DashboardAssembler.assemble(_experience(), flags=FLAGS_OFF)
        assert vm.mission_card is None


class TestExplainabilityFlag:
    def test_explainability_off_hides_card_explanation(self) -> None:
        experience = _experience()
        assert experience.explainability.explanation_chain is not None
        vm = DashboardAssembler.assemble(experience, flags=FLAGS_RECOMMENDATIONS)
        assert vm.recommendation_card is not None
        assert vm.recommendation_card.show_explanation is False
        assert vm.navigation.can_view_explanation is False
        assert vm.feature_visibility.explainability is False

    def test_explainability_on_preserves_explanation_affordance(self) -> None:
        experience = _experience()
        vm = DashboardAssembler.assemble(experience, flags=FLAGS_EXPLAINABILITY)
        assert vm.recommendation_card is not None
        assert vm.recommendation_card.show_explanation is True
        assert vm.navigation.can_view_explanation is True
        assert vm.feature_visibility.explainability is True


class TestProgressFlag:
    def test_progress_flag_off_omits_progress_summary(self) -> None:
        vm = DashboardAssembler.assemble(_experience(), flags=FLAGS_OFF)
        assert vm.progress_summary is None
        assert vm.navigation.can_view_progress is False

    def test_progress_flag_on_places_progress_summary(self) -> None:
        vm = DashboardAssembler.assemble(_experience(), flags=FLAGS_PROGRESS)
        assert vm.progress_summary is not None
        assert vm.progress_summary.progress_cues
        assert vm.navigation.can_view_progress is True


# ═══════════════════════════════════════════════════════════════════════════════
# Warnings + empty states
# ═══════════════════════════════════════════════════════════════════════════════


class TestWarningAndEmptyStatePropagation:
    def test_warnings_remain_visible_when_cards_empty(self) -> None:
        experience = _tagged_experience(warnings=("thin_warrant", "cold_start"))
        vm = DashboardAssembler.assemble(experience, flags=FLAGS_OFF)
        assert vm.recommendation_card is None
        assert vm.mission_card is None
        assert vm.warnings == ("thin_warrant", "cold_start")

    def test_empty_states_forwarded_verbatim(self) -> None:
        experience = _tagged_experience(
            empty_state_guidance=("empty_or_cold_start_posture",),
        )
        vm = DashboardAssembler.assemble(experience, flags=FLAGS_OFF)
        assert vm.empty_states == ("empty_or_cold_start_posture",)

    def test_cold_start_warnings_propagate_with_cards(self) -> None:
        experience = _cold_start_experience()
        vm = DashboardAssembler.assemble(experience, flags=FLAGS_ALL)
        assert vm.warnings
        assert any(
            tag in " ".join(vm.warnings)
            for tag in ("cold_start", "thin_warrant", "not_yet_knowable")
        )
        assert vm.readiness_summary is not None
        assert vm.readiness_summary.cold_start is True

    def test_assembler_never_fabricates_mid_high_theatre(self) -> None:
        vm = DashboardAssembler.assemble(_cold_start_experience(), flags=FLAGS_ALL)
        joined = " ".join(vm.warnings) + " ".join(vm.empty_states)
        assert "Mid" not in joined
        assert "High" not in joined
        assert "honest_medium" not in joined
        assert "honest_high" not in joined


# ═══════════════════════════════════════════════════════════════════════════════
# RecommendationCardBuilder reuse
# ═══════════════════════════════════════════════════════════════════════════════


class TestRecommendationCardBuilderReuse:
    def test_assembler_delegates_to_recommendation_card_builder(self) -> None:
        experience = _experience()
        expected = RecommendationCardBuilder.build(
            experience, flags=FLAGS_RECOMMENDATIONS
        )
        with patch.object(
            RecommendationCardBuilder,
            "build",
            wraps=RecommendationCardBuilder.build,
        ) as mocked:
            vm = DashboardAssembler.assemble(experience, flags=FLAGS_RECOMMENDATIONS)
        assert mocked.called
        assert vm.recommendation_card is not None
        assert expected is not None
        # Explainability off → assembler may clear show_explanation only.
        assert vm.recommendation_card == replace(
            expected, show_explanation=False
        )

    def test_builder_output_preserved_when_explainability_enabled(self) -> None:
        experience = _experience()
        expected = RecommendationCardBuilder.build(
            experience, flags=FLAGS_EXPLAINABILITY
        )
        vm = DashboardAssembler.assemble(experience, flags=FLAGS_EXPLAINABILITY)
        assert vm.recommendation_card == expected


# ═══════════════════════════════════════════════════════════════════════════════
# No domain leakage
# ═══════════════════════════════════════════════════════════════════════════════


class TestNoDomainLeakage:
    def test_view_model_tree_is_presentation_only(self) -> None:
        vm = DashboardAssembler.assemble(_experience(), flags=FLAGS_ALL)
        _assert_presentation_tree(vm)

    def test_dashboard_annotations_exclude_domain_types(self) -> None:
        assert is_dataclass(DashboardViewModel)
        for field in fields(DashboardViewModel):
            leaked = _annotation_type_names(field.type) & FORBIDDEN_DOMAIN_TYPE_NAMES
            assert not leaked, f"{field.name} annotation leaks {leaked}"

    def test_view_model_has_no_domain_attributes(self) -> None:
        vm = DashboardAssembler.assemble(_experience(), flags=FLAGS_ALL)
        for name in (
            "decision",
            "recommendation",
            "mission",
            "todays_recommendation",
            "todays_mission",
            "twin",
            "lineage",
            "selected",
        ):
            assert not hasattr(vm, name)


# ═══════════════════════════════════════════════════════════════════════════════
# Framework independence + no educational engines
# ═══════════════════════════════════════════════════════════════════════════════


class TestFrameworkIndependence:
    def test_dashboard_package_has_no_flask_route_or_service_imports(self) -> None:
        violations: list[str] = []
        for path in sorted(DASHBOARD_ROOT.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".", 1)[0]
                        if root in FORBIDDEN_ROOT_MODULES or alias.name.startswith(
                            FORBIDDEN_PREFIXES
                        ):
                            violations.append(f"{path.name}: import {alias.name}")
                elif isinstance(node, ast.ImportFrom) and node.module:
                    root = node.module.split(".", 1)[0]
                    if root in FORBIDDEN_ROOT_MODULES or node.module.startswith(
                        FORBIDDEN_PREFIXES
                    ):
                        violations.append(f"{path.name}: from {node.module}")
        assert violations == []

    def test_assembler_source_has_no_flask_or_engines(self) -> None:
        src = (DASHBOARD_ROOT / "dashboard_assembler.py").read_text(encoding="utf-8")
        assert "flask.request" not in src
        assert "Blueprint" not in src
        assert "render_template" not in src
        assert "sqlalchemy" not in src.lower()
        assert "DecisionEngine" not in src
        assert "RecommendationEngine" not in src
        assert "MissionIntelligence" not in src
        assert "MissionEngine" not in src
        assert "ReadinessAggregation" not in src
        assert "TwinProvider" not in src
        assert "CurriculumContextBuilder" not in src
        assert "evaluate(" not in src
        assert "package(" not in src
        assert "compose(" not in src
        assert "derive(" not in src

    def test_experience_unchanged_after_assembly(self) -> None:
        experience = _experience()
        before_rec = experience.todays_recommendation
        before_mission = experience.todays_mission
        DashboardAssembler.assemble(experience, flags=FLAGS_ALL)
        assert experience.todays_recommendation is before_rec
        assert experience.todays_mission is before_mission


# ═══════════════════════════════════════════════════════════════════════════════
# Readiness always forwarded
# ═══════════════════════════════════════════════════════════════════════════════


class TestReadinessAndNavigation:
    def test_readiness_summary_always_assembled(self) -> None:
        vm = DashboardAssembler.assemble(_experience(), flags=FLAGS_OFF)
        assert vm.readiness_summary is not None
        assert isinstance(vm.readiness_summary.overall_posture, str)
        assert vm.navigation.can_view_readiness is True

    def test_navigation_start_aligned_with_recommendation_card(self) -> None:
        vm = DashboardAssembler.assemble(_experience(), flags=FLAGS_ALL)
        assert vm.recommendation_card is not None
        assert (
            vm.navigation.can_start_recommendation
            is vm.recommendation_card.show_start_button
        )
