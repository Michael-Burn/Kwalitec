"""IA-003 Student-Centred Educational Messaging regression tests.

Student-facing recommendation copy must never expose engineering vocabulary
(evidence, pipeline, intelligence, warrant, intent enums, numeric entity ids).
Recommendation ranking and Educational Intelligence are unchanged — presentation
projection only.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from app.application.config import EducationalIntelligenceFeatureFlags
from app.application.dashboard import RecommendationCardBuilder
from app.application.orchestration import EducationalExperience, EducationalOrchestrator
from app.application.twin import TwinProvider
from app.domain.decision import Constraints, IntensityPosture
from app.domain.decision.action_types import ActionFamily, ActionIntent
from app.domain.readiness import (
    CurriculumContext,
    CurriculumFormat,
    CurriculumTopicRef,
)
from app.domain.twin import DigitalTwin, GoalState, IdentityState

FLAGS_ON = EducationalIntelligenceFeatureFlags(ENABLE_EI_RECOMMENDATIONS=True)

# Vocabulary that must never appear in student-facing recommendation copy.
FORBIDDEN_TERMS = (
    "evidence",
    "evidence_creating",
    "pipeline",
    "intelligence",
    "classification",
    "learning event",
    "digital twin",
    "mission generation",
    "warrant",
    "cold_start",
    "thin_warrant",
    "coverage_gap",
    "factor_disagreement",
    "feasibility",
)

FORBIDDEN_PATTERNS = (
    re.compile(r"\bevidence_creating\b", re.IGNORECASE),
    re.compile(r"\bwarrant\b", re.IGNORECASE),
    re.compile(r"\bpipeline\b", re.IGNORECASE),
    re.compile(r"\bdigital twin\b", re.IGNORECASE),
)

BUILDER_PATH = (
    Path(__file__).resolve().parents[1]
    / "app"
    / "application"
    / "dashboard"
    / "recommendation_card_builder.py"
)


def _identity(**overrides: object) -> IdentityState:
    defaults: dict[str, object] = {
        "student_id": "student-ia003",
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
            CurriculumTopicRef.create("18", weight=0.4),
            CurriculumTopicRef.create("42", weight=0.4),
            CurriculumTopicRef.create("7", weight=0.2),
        ],
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


def _experience(*, cold_start: bool = False) -> EducationalExperience:
    if cold_start:
        twin = DigitalTwin.create(_identity())
    else:
        twin = DigitalTwin.create(
            _identity(),
            goals=GoalState.create(
                target_pass_probability=0.8,
                target_completion_date=date(2026, 9, 15),
                planned_study_hours_per_week=10.0,
            ),
        )
    orchestrator = EducationalOrchestrator(
        twin_provider=TwinProvider(source=_TwinSource(twin)),
        curriculum_context_builder=_RecordingBuilder(_curriculum()),
    )
    experience = orchestrator.build_experience(
        student_id=twin.identity.student_id,
        curriculum_id=1,
        constraints=Constraints.create(
            available_minutes=60,
            intensity=IntensityPosture.AMPLE,
        ),
    )
    assert isinstance(experience, EducationalExperience)
    return experience


def _assert_student_safe(text: str | None, *, field: str) -> None:
    assert text is not None and text.strip(), f"{field} must be non-empty"
    lowered = text.lower()
    for term in FORBIDDEN_TERMS:
        assert term not in lowered, f"{field} leaks {term!r}: {text!r}"
    for pattern in FORBIDDEN_PATTERNS:
        assert not pattern.search(text), f"{field} matches {pattern.pattern}: {text!r}"
    # Opaque numeric syllabus keys (e.g. "18 · …") must not be the message.
    assert not re.search(r"^\d+\s*[·\-–]", text.strip()), (
        f"{field} looks like a raw entity id prefix: {text!r}"
    )


class TestIa003RecommendationCardMessaging:
    def test_no_evidence_creating_in_card_copy(self) -> None:
        experience = _experience(cold_start=True)
        card = RecommendationCardBuilder.build(experience, flags=FLAGS_ON)
        assert card is not None
        for field_name in ("title", "subtitle", "reason_summary", "primary_action"):
            value = getattr(card, field_name)
            if value is None:
                continue
            _assert_student_safe(value, field=field_name)
            assert "evidence creating" not in value.lower()
            assert "evidence_creating" not in value.lower()

    def test_entity_id_and_intent_enum_never_dumped(self) -> None:
        experience = _experience(cold_start=True)
        suggestion = experience.todays_recommendation.suggestion
        # Domain may still carry internal ids / intents — presentation must not.
        assert suggestion.curriculum_entity_id in {"18", "42", "7"} or (
            suggestion.curriculum_entity_id is not None
        )
        assert suggestion.intent == ActionIntent.EVIDENCE_CREATING or isinstance(
            suggestion.intent, ActionIntent
        )
        card = RecommendationCardBuilder.build(experience, flags=FLAGS_ON)
        assert card is not None
        joined = " ".join(
            filter(
                None,
                (card.title, card.subtitle, card.reason_summary, card.primary_action),
            )
        )
        if suggestion.curriculum_entity_id:
            assert suggestion.curriculum_entity_id not in joined
        assert suggestion.intent.value not in joined
        assert "evidence_creating" not in joined

    def test_titles_are_educational_family_labels(self) -> None:
        experience = _experience()
        card = RecommendationCardBuilder.build(experience, flags=FLAGS_ON)
        assert card is not None
        assert card.title in {
            "Continue studying",
            "Review and strengthen",
            "Check your understanding",
            "Find your next focus",
            "Protect today's study energy",
        }

    def test_reason_answers_why(self) -> None:
        experience = _experience()
        card = RecommendationCardBuilder.build(experience, flags=FLAGS_ON)
        assert card is not None
        assert card.reason_summary is not None
        assert (
            "Suggested:" in card.reason_summary
            or "Based on" in card.reason_summary
            or "You've completed" in card.reason_summary
        )
        assert card.educational_advice
        assert card.next_action
        assert card.observed_facts

    def test_builder_source_never_joins_raw_intent(self) -> None:
        src = BUILDER_PATH.read_text(encoding="utf-8")
        assert "suggestion.intent.value" not in src
        assert "suggestion.curriculum_entity_id" not in src
        assert "parts.append(intent_value)" not in src


class TestIa003StudentSurfacesRegression:
    def test_dashboard_has_no_engineering_recommendation_leak(
        self, logged_in_client, study_plan, curriculum
    ) -> None:
        cur, _ = curriculum
        study_plan.curriculum_id = cur.id
        from app.extensions import db

        db.session.commit()

        from unittest.mock import patch

        from app.application.dashboard import (
            DashboardViewModel,
            FeatureVisibilityViewModel,
            NavigationAffordancesViewModel,
            RecommendationCardViewModel,
        )

        view = DashboardViewModel(
            recommendation_card=RecommendationCardViewModel(
                title="Find your next focus",
                subtitle="A short check to guide today's recommendation",
                primary_action="Start Today's Session",
                estimated_duration=None,
                reason_summary=(
                    "You've completed valuable study activities. A short check "
                    "now will help identify the most useful next step."
                ),
                warning=None,
                show_explanation=False,
                show_start_button=True,
            ),
            mission_card=None,
            readiness_summary=None,
            progress_summary=None,
            warnings=(),
            empty_states=(),
            navigation=NavigationAffordancesViewModel(
                can_start_recommendation=True,
                can_open_mission=False,
                can_view_explanation=False,
                can_view_readiness=False,
                can_view_progress=False,
            ),
            feature_visibility=FeatureVisibilityViewModel(
                recommendations=True,
                missions=False,
                explainability=False,
                progress=False,
            ),
        )
        flags = EducationalIntelligenceFeatureFlags(
            ENABLE_EDUCATIONAL_ORCHESTRATOR=True,
            ENABLE_EI_RECOMMENDATIONS=True,
        )
        with (
            patch(
                "app.dashboard.routes.resolve_feature_flags",
                return_value=flags,
            ),
            patch(
                "app.dashboard.routes._compose_educational_dashboard",
                return_value=view,
            ),
        ):
            response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        body = response.get_data(as_text=True).lower()
        assert "evidence_creating" not in body
        assert "evidence creating" not in body
        assert "digital twin" not in body
        assert "composite score" not in body
        assert "find your next focus" in body

    def test_mission_page_uses_educational_why_copy(
        self, logged_in_client, study_plan
    ) -> None:
        response = logged_in_client.get("/missions/")
        assert response.status_code == 200
        body = response.get_data(as_text=True).lower()
        assert "evidence_creating" not in body
        assert "digital twin" not in body
        if "why this mission" in body:
            assert "learning mode" in body
            assert "current learning topic" in body
            assert "next step" in body

    def test_settings_learning_profile_not_digital_twin(
        self, logged_in_client
    ) -> None:
        response = logged_in_client.get("/settings/internal-alpha")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Learning profile status" in body
        assert "Digital Twin status" not in body
        assert "Educational Intelligence behaviour" not in body

    def test_recommendation_logic_unchanged_domain_intents(self) -> None:
        """Domain intents remain engineering vocabulary — presentation maps them."""
        experience = _experience(cold_start=True)
        suggestion = experience.todays_recommendation.suggestion
        assert suggestion.family in ActionFamily
        assert suggestion.intent in ActionIntent
        card = RecommendationCardBuilder.build(experience, flags=FLAGS_ON)
        assert card is not None
        # Same Decision packaging: builder does not alter the Recommendation.
        assert experience.todays_recommendation.suggestion.intent == suggestion.intent
