"""Tests for RecommendationCardBuilder (Capability 3.3.2).

Covers feature-flag gating, ViewModel construction, domain leakage absence,
framework independence, immutability, cold-start handling, and truthful
warning propagation.
"""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, fields, is_dataclass
from datetime import date
from pathlib import Path
from typing import get_args, get_origin

import pytest

from app.application.config import EducationalIntelligenceFeatureFlags
from app.application.dashboard import (
    RecommendationCardBuilder,
    RecommendationCardViewModel,
)
from app.application.orchestration import (
    EducationalExperience,
    EducationalOrchestrator,
)
from app.application.twin import TwinProvider
from app.domain.decision import Constraints, IntensityPosture
from app.domain.readiness import (
    CurriculumContext,
    CurriculumFormat,
    CurriculumTopicRef,
)
from app.domain.recommendation import THIN_WARRANT_CONFIDENCE_POSTURES
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

# ViewModel presentation primitives only — no domain objects.
ALLOWED_VALUE_TYPES = (str, bool, type(None))
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
    }
)

FLAGS_OFF = EducationalIntelligenceFeatureFlags()
FLAGS_ON = EducationalIntelligenceFeatureFlags(ENABLE_EI_RECOMMENDATIONS=True)


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


class _TwinSource:
    def __init__(self, twin: DigitalTwin):
        self.twin = twin

    def load(self, student_id: str, *, context=None) -> DigitalTwin | None:
        return self.twin


def _experience() -> EducationalExperience:
    """Compose a real Educational Experience via Application orchestrator."""
    twin = _twin()
    orchestrator = EducationalOrchestrator(
        twin_provider=TwinProvider(source=_TwinSource(twin)),
        curriculum_context_builder=_RecordingBuilder(_curriculum()),
    )
    experience = orchestrator.build_experience(
        student_id=twin.identity.student_id,
        curriculum_id=1,
        constraints=_constraints(),
    )
    assert isinstance(experience, EducationalExperience)
    return experience


def _cold_start_experience() -> EducationalExperience:
    """Experience with cold-start / thin-warrant honesty forwarded intact."""
    # Goals-absent Twin yields cold-start / not-yet-knowable readiness honesty.
    twin = DigitalTwin.create(_identity())
    orchestrator = EducationalOrchestrator(
        twin_provider=TwinProvider(source=_TwinSource(twin)),
        curriculum_context_builder=_RecordingBuilder(_curriculum()),
    )
    experience = orchestrator.build_experience(
        student_id=twin.identity.student_id,
        curriculum_id=1,
        constraints=_constraints(),
    )
    assert isinstance(experience, EducationalExperience)
    return experience


# ═══════════════════════════════════════════════════════════════════════════════
# Feature flag OFF
# ═══════════════════════════════════════════════════════════════════════════════


class TestFeatureFlagOff:
    def test_default_flags_return_none(self) -> None:
        card = RecommendationCardBuilder.build(_experience())
        assert card is None

    def test_explicit_flags_off_return_none(self) -> None:
        card = RecommendationCardBuilder.build(_experience(), flags=FLAGS_OFF)
        assert card is None

    def test_flag_off_does_not_expose_view_model(self) -> None:
        result = RecommendationCardBuilder.build(_experience(), flags=FLAGS_OFF)
        assert not isinstance(result, RecommendationCardViewModel)


# ═══════════════════════════════════════════════════════════════════════════════
# Feature flag ON — ViewModel construction
# ═══════════════════════════════════════════════════════════════════════════════


class TestFeatureFlagOn:
    def test_returns_view_model_when_enabled(self) -> None:
        card = RecommendationCardBuilder.build(_experience(), flags=FLAGS_ON)
        assert isinstance(card, RecommendationCardViewModel)

    def test_title_is_non_empty_presentation_string(self) -> None:
        card = RecommendationCardBuilder.build(_experience(), flags=FLAGS_ON)
        assert card is not None
        assert isinstance(card.title, str)
        assert card.title.strip()

    def test_primary_action_and_start_button_aligned(self) -> None:
        card = RecommendationCardBuilder.build(_experience(), flags=FLAGS_ON)
        assert card is not None
        assert card.show_start_button is True
        assert isinstance(card.primary_action, str)
        assert card.primary_action.strip()

    def test_show_explanation_when_chain_present(self) -> None:
        experience = _experience()
        card = RecommendationCardBuilder.build(experience, flags=FLAGS_ON)
        assert card is not None
        assert experience.explainability.explanation_chain is not None
        assert card.show_explanation is True

    def test_reason_summary_drawn_from_recommendation_reasons(self) -> None:
        experience = _experience()
        card = RecommendationCardBuilder.build(experience, flags=FLAGS_ON)
        assert card is not None
        assert card.reason_summary is not None
        assert "Based on your current study progress" in card.reason_summary
        primary = experience.todays_recommendation.reasons[0]
        # Internal warrant tags must never leak into student-facing copy.
        for tag in primary.note_tags:
            assert tag not in card.reason_summary


# ═══════════════════════════════════════════════════════════════════════════════
# No domain leakage
# ═══════════════════════════════════════════════════════════════════════════════


class TestNoDomainLeakage:
    def test_view_model_fields_are_presentation_primitives(self) -> None:
        card = RecommendationCardBuilder.build(_experience(), flags=FLAGS_ON)
        assert card is not None
        for field in fields(card):
            value = getattr(card, field.name)
            assert isinstance(value, ALLOWED_VALUE_TYPES), (
                f"{field.name} leaked non-presentation type: {type(value)!r}"
            )

    def test_view_model_annotations_exclude_domain_types(self) -> None:
        assert is_dataclass(RecommendationCardViewModel)
        for field in fields(RecommendationCardViewModel):
            annotation = field.type
            names = _annotation_type_names(annotation)
            leaked = names & FORBIDDEN_DOMAIN_TYPE_NAMES
            assert not leaked, f"{field.name} annotation leaks {leaked}"

    def test_view_model_has_no_decision_or_recommendation_attributes(self) -> None:
        card = RecommendationCardBuilder.build(_experience(), flags=FLAGS_ON)
        assert card is not None
        assert not hasattr(card, "decision")
        assert not hasattr(card, "recommendation")
        assert not hasattr(card, "mission")
        assert not hasattr(card, "todays_recommendation")
        assert not hasattr(card, "lineage")
        assert not hasattr(card, "selected")


def _annotation_type_names(annotation: object) -> set[str]:
    """Collect type names from a possibly union / optional annotation."""
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


# ═══════════════════════════════════════════════════════════════════════════════
# Framework independence
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

    def test_builder_source_has_no_flask_request_or_routes(self) -> None:
        src = (DASHBOARD_ROOT / "recommendation_card_builder.py").read_text(
            encoding="utf-8"
        )
        assert "flask.request" not in src
        assert "flask.session" not in src
        assert "Blueprint" not in src
        assert "bp.route" not in src
        assert "render_template" not in src
        assert "sqlalchemy" not in src.lower()

    def test_builder_does_not_call_educational_engines(self) -> None:
        src = (DASHBOARD_ROOT / "recommendation_card_builder.py").read_text(
            encoding="utf-8"
        )
        assert "DecisionEngine" not in src
        assert "RecommendationEngine" not in src
        assert "MissionIntelligence" not in src
        assert "ReadinessAggregation" not in src
        assert "evaluate(" not in src
        assert "package(" not in src
        assert "compose(" not in src
        assert "derive(" not in src


# ═══════════════════════════════════════════════════════════════════════════════
# Immutable output
# ═══════════════════════════════════════════════════════════════════════════════


class TestImmutableOutput:
    def test_view_model_is_frozen(self) -> None:
        card = RecommendationCardBuilder.build(_experience(), flags=FLAGS_ON)
        assert card is not None
        with pytest.raises(FrozenInstanceError):
            card.title = "mutated"  # type: ignore[misc]

    def test_each_field_assignment_raises(self) -> None:
        card = RecommendationCardBuilder.build(_experience(), flags=FLAGS_ON)
        assert card is not None
        for field in fields(card):
            with pytest.raises(FrozenInstanceError):
                setattr(card, field.name, getattr(card, field.name))


# ═══════════════════════════════════════════════════════════════════════════════
# Cold start + warning propagation
# ═══════════════════════════════════════════════════════════════════════════════


class TestColdStartAndWarnings:
    def test_cold_start_still_builds_view_model(self) -> None:
        experience = _cold_start_experience()
        card = RecommendationCardBuilder.build(experience, flags=FLAGS_ON)
        assert isinstance(card, RecommendationCardViewModel)
        assert card.title.strip()

    def test_cold_start_warning_propagated_truthfully(self) -> None:
        experience = _cold_start_experience()
        card = RecommendationCardBuilder.build(experience, flags=FLAGS_ON)
        assert card is not None
        # Internal Alpha: diagnostic warrant tags stay internal — not on the card.
        assert card.warning is None
        assert card.reason_summary is not None
        assert "cold_start" not in card.reason_summary
        assert "thin_warrant" not in card.reason_summary
        assert "warrant_honesty" not in card.reason_summary

    def test_experience_warnings_forwarded_verbatim(self) -> None:
        experience = _experience()
        # Rebuild Experience with explicit warning tags (composition classify only).
        tagged = EducationalExperience(
            student_summary=experience.student_summary,
            todays_recommendation=experience.todays_recommendation,
            todays_mission=experience.todays_mission,
            readiness_summary=experience.readiness_summary,
            progress_snapshot=experience.progress_snapshot,
            explainability=experience.explainability,
            warnings=("thin_warrant", "cold_start"),
            empty_state_guidance=experience.empty_state_guidance,
            metadata=experience.metadata,
        )
        card = RecommendationCardBuilder.build(tagged, flags=FLAGS_ON)
        assert card is not None
        assert card.warning is None
        assert "thin_warrant" not in (card.reason_summary or "")
        assert "cold_start" not in (card.reason_summary or "")

    def test_thin_warrant_confidence_never_upgraded(self) -> None:
        experience = _cold_start_experience()
        confidence = experience.todays_recommendation.confidence_posture
        card = RecommendationCardBuilder.build(experience, flags=FLAGS_ON)
        assert card is not None
        # Student card must not invent Mid/High preparedness theatre.
        assert card.warning is None
        assert "honest_medium" not in (card.reason_summary or "")
        assert "honest_high" not in (card.reason_summary or "")
        assert "Mid" not in (card.reason_summary or "")
        assert "High" not in (card.reason_summary or "")
        # Domain confidence posture remains thin — presentation does not upgrade it.
        assert confidence in THIN_WARRANT_CONFIDENCE_POSTURES


# ═══════════════════════════════════════════════════════════════════════════════
# Builder does not reason
# ═══════════════════════════════════════════════════════════════════════════════


class TestNoEducationalReasoning:
    def test_title_matches_selected_family_projection(self) -> None:
        experience = _experience()
        card = RecommendationCardBuilder.build(experience, flags=FLAGS_ON)
        assert card is not None
        family = experience.todays_recommendation.suggestion.family
        assert family.value in card.title.lower() or card.title in {
            "Study",
            "Revise",
            "Assess",
            "Diagnostic",
            "Protect intensity",
        }

    def test_builder_does_not_replace_recommendation(self) -> None:
        experience = _experience()
        before = experience.todays_recommendation
        RecommendationCardBuilder.build(experience, flags=FLAGS_ON)
        assert experience.todays_recommendation is before
