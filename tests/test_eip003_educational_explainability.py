"""EIP-003 Educational Narrative & Explainability regression tests.

Negative tests: no engineering theatre; no estimates-as-fact; no unexplained
missions/recommendations; no readiness without basis; no unauthorised mastery.

Positive tests: recommendations and missions explain themselves; estimates are
labelled; next actions are clear; surfaces tell one coherent educational story.

Governing refs:
- EDUCATIONAL_EXPLAINABILITY_STANDARD.md
- Constitution Articles II, III, VII
- EL-008, EL-009, EL-010
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pytest

from app.application.config import EducationalIntelligenceFeatureFlags
from app.application.dashboard import RecommendationCardBuilder
from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.study_plan import StudyPlan, WeekPlan
from app.services.educational_explainability_service import (
    EducationalExplainabilityService,
)
from app.services.planning_service import PlanningService
from app.services.recommendation_service import RecommendationService
from app.services.study_plan_service import StudyPlanService

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = REPO_ROOT / "app" / "templates"

STUDENT_TEMPLATE_DIRS = (
    "dashboard",
    "study_plan",
    "mission",
    "analytics",
    "settings",
    "calibration",
)

# Engineering / Twin / Intelligence jargon forbidden on student surfaces.
FORBIDDEN_ENGINEERING_TERMS = (
    "digital twin",
    "educational intelligence",
    "knowledge state",
    "evidence_creating",
    "cold_start",
    "thin_warrant",
    "mission generation",
)

# Prefer practice-results language over evidence jargon in coach copy.
FORBIDDEN_EVIDENCE_LEAKS = (
    "study evidence",
)

FALSE_MASTERY_AS_FACT = (
    "already mastered",
    "you've mastered",
    "you have mastered",
    "mark as mastered",
    "topics mastered",
)


def _make_curriculum(
    exam_name: str, topic_names: list[str]
) -> tuple[Curriculum, list[Topic]]:
    curriculum = Curriculum(exam_name=exam_name, version="2025", active=True)
    db.session.add(curriculum)
    db.session.flush()
    topics: list[Topic] = []
    for index, name in enumerate(topic_names, start=1):
        topic = Topic(
            name=name,
            curriculum_id=curriculum.id,
            order=index,
            recommended_minutes=60,
            active=True,
        )
        db.session.add(topic)
        topics.append(topic)
    db.session.flush()
    return curriculum, topics


def _make_active_plan(
    user_id: int,
    *,
    exam_name: str,
    curriculum: Curriculum,
) -> StudyPlan:
    plan = StudyPlan(
        user_id=user_id,
        curriculum_id=curriculum.id,
        curriculum_version=curriculum.version,
        exam_name=exam_name,
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=180),
        weekday_study_minutes=120,
        weekend_study_minutes=180,
        current_stage="Chapter 1",
        study_preference="Mixed",
        target_grade="A",
        preferred_session_minutes=60,
        active=True,
        curriculum_topic_code=None,
    )
    db.session.add(plan)
    db.session.flush()
    week = WeekPlan(
        study_plan_id=plan.id,
        week_number=1,
        start_date=date.today() - timedelta(days=2),
        end_date=date.today() + timedelta(days=4),
    )
    db.session.add(week)
    db.session.commit()
    return plan


def _student_template_texts() -> list[tuple[Path, str]]:
    texts: list[tuple[Path, str]] = []
    for folder in STUDENT_TEMPLATE_DIRS:
        root = TEMPLATE_ROOT / folder
        if not root.exists():
            continue
        for path in root.rglob("*.html"):
            texts.append((path, path.read_text(encoding="utf-8")))
    return texts


# ═══════════════════════════════════════════════════════════════════════════
# Negative regression
# ═══════════════════════════════════════════════════════════════════════════


class TestNegativeEngineeringTerminology:
    def test_student_templates_forbid_engineering_terms(self) -> None:
        offenders: list[str] = []
        for path, text in _student_template_texts():
            # Strip HTML comments — engineering notes in comments are allowed.
            visible = text
            while "<!--" in visible:
                start = visible.find("<!--")
                end = visible.find("-->", start)
                if end < 0:
                    break
                visible = visible[:start] + visible[end + 3 :]
            lowered = visible.lower()
            for term in FORBIDDEN_ENGINEERING_TERMS:
                if term in lowered:
                    offenders.append(
                        f"{path.relative_to(REPO_ROOT)}: {term}"
                    )
        assert not offenders, "Engineering terms on student pages:\n" + "\n".join(
            offenders
        )

    def test_student_templates_avoid_study_evidence_jargon(self) -> None:
        offenders: list[str] = []
        for path, text in _student_template_texts():
            lowered = text.lower()
            for term in FORBIDDEN_EVIDENCE_LEAKS:
                if term in lowered:
                    offenders.append(
                        f"{path.relative_to(REPO_ROOT)}: {term}"
                    )
        assert not offenders, "Evidence jargon leaks:\n" + "\n".join(offenders)

    def test_student_templates_avoid_false_mastery_as_fact(self) -> None:
        offenders: list[str] = []
        for path, text in _student_template_texts():
            lowered = text.lower()
            for claim in FALSE_MASTERY_AS_FACT:
                if claim in lowered:
                    offenders.append(
                        f"{path.relative_to(REPO_ROOT)}: {claim}"
                    )
        assert not offenders, "False mastery-as-fact:\n" + "\n".join(offenders)


@pytest.mark.usefixtures("ctx")
class TestNegativeEstimateAsFact:
    def test_composite_readiness_is_labelled_estimate(self) -> None:
        narrative = EducationalExplainabilityService.explain_composite_readiness(
            {
                "score": 55.0,
                "coverage_pct": 40.0,
                "avg_mastery": 50.0,
                "review_discipline": 70.0,
                "total_topics": 10,
                "topics_started": 4,
            }
        )
        assert narrative.is_estimate is True
        assert "estimated" in narrative.label.lower()
        assert "estimated" in narrative.explanation.lower()
        assert narrative.can_estimate is True
        assert narrative.evidence_basis

    def test_empty_history_cannot_estimate_readiness(self) -> None:
        narrative = EducationalExplainabilityService.explain_composite_readiness(
            {
                "score": 0.0,
                "coverage_pct": 0.0,
                "avg_mastery": 0.0,
                "review_discipline": 0.0,
                "total_topics": 10,
                "topics_started": 0,
            }
        )
        assert narrative.can_estimate is False
        explanation = narrative.explanation.lower()
        assert (
            "cannot yet be estimated" in explanation
            or "more recorded practice before this estimate becomes available"
            in explanation
        )


@pytest.mark.usefixtures("ctx")
class TestNegativeUnexplainedDecisions:
    def test_every_legacy_recommendation_has_explanation(self, user) -> None:
        StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
        )
        raw = RecommendationService.generate_recommendations(user.id, limit=5)
        enriched = EducationalExplainabilityService.enrich_recommendations(raw)
        for rec in enriched:
            assert rec.get("reason"), f"Missing reason: {rec.get('title')}"
            assert rec.get("educational_advice"), f"Missing advice: {rec.get('title')}"
            assert rec.get("next_action"), f"Missing next action: {rec.get('title')}"
            assert rec.get("observed_facts") is not None

    def test_mission_without_title_has_no_false_narrative(self) -> None:
        assert (
            EducationalExplainabilityService.build_mission_narrative(
                mission_title=None
            )
            is None
        )


# ═══════════════════════════════════════════════════════════════════════════
# Positive regression
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.usefixtures("ctx")
class TestPositiveMissionExplainability:
    def test_mission_narrative_answers_four_questions(self, user) -> None:
        curriculum, _topics = _make_curriculum(
            "IFoA CS1", ["Alpha Topic", "Beta Topic"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        narrative = EducationalExplainabilityService.build_mission_narrative(
            mission_title="Alpha Topic",
            mission_status="Pending",
            exam_name=plan.exam_name,
            completed_topics=0,
            total_topics=2,
            syllabus_coverage_pct=0.0,
        )
        assert narrative is not None
        assert narrative.educational_purpose
        assert "Learning Mode" in narrative.reason_for_selection
        assert "Current Learning Topic" in narrative.reason_for_selection
        assert narrative.educational_position
        assert narrative.next_action
        assert narrative.observed_facts
        assert any("Estimated" in item or "estimate" in item.lower()
                   for item in narrative.estimates)

    def test_mission_page_explains_itself(self, app, user, logged_in_client) -> None:
        StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
        )
        PlanningService.generate_today_mission(user.id)

        response = logged_in_client.get("/missions/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Why you are studying this" in body
        assert "Learning objective:" in body
        assert "Next step:" in body
        assert "Learning Mode" in body
        assert "Current Learning Topic" in body
        assert "Observed Facts" in body
        assert "Estimates" in body
        lower = body.lower()
        for term in FORBIDDEN_ENGINEERING_TERMS:
            assert term not in lower


@pytest.mark.usefixtures("ctx")
class TestPositiveRecommendationExplainability:
    def test_recommendation_distinguishes_claim_types(self) -> None:
        narrative = EducationalExplainabilityService.explain_recommendation(
            {
                "title": "Practise lower Estimated Knowledge: Topic A",
                "category": "Weak Topic",
                "reason": "Your Estimated Knowledge for Topic A is below 30%.",
                "expected_benefit": "Raise Estimated Knowledge through practice.",
            }
        )
        assert narrative.observed_facts
        assert narrative.estimates
        assert "Suggested" in narrative.educational_advice
        assert narrative.next_action
        assert "does not replace Today's Study Session" in narrative.reason
        assert "Learning Mode" in narrative.educational_advice

    def test_dashboard_recommendations_show_claim_types(
        self, app, user, logged_in_client
    ) -> None:
        StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
        )
        PlanningService.generate_today_mission(user.id)

        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        # Mission authority label (not advice-shaped "Recommended Mission")
        assert "Today's Topic" in body or "Today's Study Session" in body
        assert "Today's Recommended Mission" not in body
        lower = body.lower()
        for term in FORBIDDEN_ENGINEERING_TERMS:
            assert term not in lower


class TestPositiveEiRecommendationCard:
    def test_card_includes_claim_type_fields(self) -> None:
        # Import experience helper pattern from IA-003 via light rebuild.
        from datetime import date as date_cls

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
        from app.domain.twin import DigitalTwin, GoalState, IdentityState

        class _Builder:
            def __init__(self, curriculum: CurriculumContext):
                self.curriculum = curriculum

            def build(self, curriculum_id: int | None) -> CurriculumContext:
                return self.curriculum

        class _Source:
            def __init__(self, twin: DigitalTwin):
                self.twin = twin

            def load(self, student_id: str, *, context=None) -> DigitalTwin | None:
                return self.twin

        twin = DigitalTwin.create(
            IdentityState.create(
                student_id="eip003",
                curriculum_id="CS1-2026",
                current_exam="CS1",
                target_sitting=date_cls(2026, 9, 15),
            ),
            goals=GoalState.create(
                target_pass_probability=0.8,
                target_completion_date=date_cls(2026, 9, 15),
                planned_study_hours_per_week=10.0,
            ),
        )
        curriculum = CurriculumContext.create(
            "CS1-2026",
            format=CurriculumFormat.V1,
            topics=[
                CurriculumTopicRef.create("18", weight=0.4),
                CurriculumTopicRef.create("42", weight=0.4),
                CurriculumTopicRef.create("7", weight=0.2),
            ],
        )
        experience = EducationalOrchestrator(
            twin_provider=TwinProvider(source=_Source(twin)),
            curriculum_context_builder=_Builder(curriculum),
        ).build_experience(
            student_id=twin.identity.student_id,
            curriculum_id=1,
            constraints=Constraints.create(
                available_minutes=60,
                intensity=IntensityPosture.AMPLE,
            ),
        )
        assert isinstance(experience, EducationalExperience)
        flags = EducationalIntelligenceFeatureFlags(ENABLE_EI_RECOMMENDATIONS=True)
        card = RecommendationCardBuilder.build(experience, flags=flags)
        assert card is not None
        assert card.observed_facts
        assert card.educational_advice
        assert card.next_action
        assert "Suggested:" in (card.reason_summary or "")


@pytest.mark.usefixtures("ctx")
class TestPositiveReadinessExplainability:
    def test_analytics_explains_readiness(self, app, user, logged_in_client) -> None:
        StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
        )
        response = logged_in_client.get("/analytics/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Estimated readiness" in body or "cannot yet be estimated" in body
        assert "data-eip003-readiness" in body

    def test_coverage_readiness_not_called_mastery(self) -> None:
        narrative = EducationalExplainabilityService.explain_coverage_readiness(
            readiness_percentage=0.42
        )
        assert narrative.is_estimate is False
        assert "not Estimated Knowledge" in narrative.explanation
        assert narrative.evidence_basis


@pytest.mark.usefixtures("ctx")
class TestPositiveStageLabels:
    def test_mastered_stage_mapped_to_estimated_language(self) -> None:
        label = EducationalExplainabilityService.student_stage_label("Mastered")
        assert label == "Strong estimated knowledge"
        assert "Mastered" not in label

    def test_enrich_topic_rows_adds_stage_label(self) -> None:
        rows = EducationalExplainabilityService.enrich_topic_rows(
            [{"topic_name": "X", "stage": "Mastered", "mastery_score": 90}]
        )
        assert rows[0]["stage_label"] == "Strong estimated knowledge"


@pytest.mark.usefixtures("ctx")
class TestPositiveCoherentStory:
    def test_dashboard_and_mission_share_learning_mode_story(
        self, app, user, logged_in_client
    ) -> None:
        StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
        )
        PlanningService.generate_today_mission(user.id)

        mission_body = logged_in_client.get("/missions/").get_data(as_text=True)
        dash_body = logged_in_client.get("/dashboard/").get_data(as_text=True)

        assert "Learning Mode" in mission_body
        assert "Current Learning Topic" in mission_body
        assert "Study Progress" in mission_body or "Study Progress" in dash_body
        # One coherent story: mission authority is topic, not advice theatre
        assert "Today's Recommended Mission" not in dash_body
