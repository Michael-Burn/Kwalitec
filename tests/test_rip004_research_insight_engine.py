"""RIP-004 Research Insight Engine tests.

Covers insight generation, aggregation, trend comparison, confidence
assignment, release comparison, history preservation, educational isolation,
and architecture boundaries.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta

import pytest

from app.extensions import db
from app.models.mission import Mission, MissionTask
from app.models.research_feedback import (
    ResearchFeedbackStatusTransition,
    ResearchFeedbackSubmission,
    ResearchProductFinding,
)
from app.models.subject import Subject
from app.models.topic_progress import TopicProgress
from app.models.user import User
from app.services.founder_research_service import FounderResearchService
from app.services.research_feedback_service import (
    SOURCE_SETTINGS,
    ResearchFeedbackService,
)
from app.services.research_insight_service import (
    CONFIDENCE_HIGH,
    CONFIDENCE_LOW,
    CONFIDENCE_MEDIUM,
    INSIGHT_FAMILY_BEHAVIOUR,
    INSIGHT_FAMILY_EXPERIENCE,
    INSIGHT_FAMILY_FRICTION,
    INSIGHT_FAMILY_RELEASE,
    INSIGHT_FAMILY_RESEARCH,
    INSIGHT_FAMILY_TREND,
    TIME_WINDOW_7_DAYS,
    TIME_WINDOW_CURRENT_RELEASE,
    TIME_WINDOW_TODAY,
    InsightFilters,
    ResearchInsightService,
)


def _make_user(email: str) -> User:
    user = User(email=email, is_active_user=True)
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


def _submit_checkin(
    user_id: int,
    *,
    experience: str = "Good",
    feature: str = "Dashboard",
    friction: str = "Navigation",
    free_text: str | None = None,
    classification: str | None = None,
    version: str = "1.0.0",
    submitted_at: datetime | None = None,
) -> ResearchFeedbackSubmission:
    result = ResearchFeedbackService.submit_checkin(
        user_id,
        experience_rating=experience,
        feature_helped_most=feature,
        friction_area=friction,
        confidence_rating="High",
        return_intent="Probably",
        submission_source=SOURCE_SETTINGS,
        free_text=free_text,
        classification=classification,
        product_version=version,
        submitted_at=submitted_at,
    )
    return result.submission


@pytest.fixture
def founder(app):
    app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
    return _make_user("founder@kwalitec.example")


@pytest.mark.usefixtures("ctx")
class TestInsightGeneration:
    def test_generates_all_six_families(self, user):
        _submit_checkin(user.id)
        result = ResearchInsightService.generate_insights(as_of=date.today())
        families = {i.family for i in result.insights}
        assert INSIGHT_FAMILY_EXPERIENCE in families
        assert INSIGHT_FAMILY_BEHAVIOUR in families
        assert INSIGHT_FAMILY_FRICTION in families
        assert INSIGHT_FAMILY_TREND in families
        assert INSIGHT_FAMILY_RELEASE in families
        assert INSIGHT_FAMILY_RESEARCH in families

    def test_insight_has_required_fields(self, user):
        _submit_checkin(user.id)
        result = ResearchInsightService.generate_insights(as_of=date.today())
        insight = result.insights[0]
        assert insight.title
        assert insight.summary
        assert insight.supporting_observation_count >= 1
        assert len(insight.supporting_submission_ids) >= 1
        assert insight.time_window
        assert insight.confidence in {
            CONFIDENCE_LOW,
            CONFIDENCE_MEDIUM,
            CONFIDENCE_HIGH,
        }
        assert insight.suggested_review_priority
        assert isinstance(insight.related_finding_ids, tuple)

    def test_no_recommendations_in_summaries(self, user):
        for _ in range(5):
            _submit_checkin(user.id, friction="Navigation")
        result = ResearchInsightService.generate_insights(as_of=date.today())
        forbidden = ("should", "recommend", "must fix", "roadmap")
        for insight in result.insights:
            lower = insight.summary.lower()
            for word in forbidden:
                assert word not in lower, f"Insight '{insight.title}' contains '{word}'"


@pytest.mark.usefixtures("ctx")
class TestAggregation:
    def test_experience_average(self, user):
        _submit_checkin(user.id, experience="Excellent")
        _submit_checkin(user.id, experience="Good")
        result = ResearchInsightService.generate_insights(as_of=date.today())
        exp_insights = [
            i for i in result.insights if i.title == "Average Product Experience"
        ]
        assert len(exp_insights) == 1
        assert "4.5/5" in exp_insights[0].summary

    def test_friction_most_reported(self, user):
        _submit_checkin(user.id, friction="Navigation")
        _submit_checkin(user.id, friction="Navigation")
        _submit_checkin(user.id, friction="Terminology")
        result = ResearchInsightService.generate_insights(as_of=date.today())
        friction_insights = [
            i for i in result.insights if i.title == "Most Reported Friction"
        ]
        assert len(friction_insights) == 1
        assert "Navigation" in friction_insights[0].summary
        assert friction_insights[0].supporting_observation_count == 2

    def test_filtered_by_feature(self, user):
        _submit_checkin(user.id, feature="Dashboard")
        _submit_checkin(user.id, feature="Analytics")
        filters = InsightFilters(feature="Dashboard")
        result = ResearchInsightService.generate_insights(filters, as_of=date.today())
        assert result.legacy.most_common_feature == "Dashboard"


@pytest.mark.usefixtures("ctx")
class TestTrendComparison:
    def test_weekly_movement_comparison(self, user):
        today = date.today()
        prior = today - timedelta(days=10)
        _submit_checkin(
            user.id,
            submitted_at=datetime.combine(prior, datetime.min.time()),
        )
        _submit_checkin(
            user.id, submitted_at=datetime.combine(today, datetime.min.time())
        )
        _submit_checkin(
            user.id, submitted_at=datetime.combine(today, datetime.min.time())
        )
        result = ResearchInsightService.generate_insights(
            time_window=TIME_WINDOW_7_DAYS,
            as_of=today,
        )
        weekly = [i for i in result.insights if i.title == "Weekly Movement"]
        assert len(weekly) == 1
        assert weekly[0].comparison is not None
        assert weekly[0].comparison.delta is not None

    def test_experience_trend_when_prior_data_exists(self, user):
        today = date.today()
        prior = today - timedelta(days=10)
        _submit_checkin(
            user.id,
            experience="Poor",
            submitted_at=datetime.combine(prior, datetime.min.time()),
        )
        _submit_checkin(
            user.id,
            experience="Excellent",
            submitted_at=datetime.combine(today, datetime.min.time()),
        )
        result = ResearchInsightService.generate_insights(
            time_window=TIME_WINDOW_7_DAYS,
            as_of=today,
        )
        trend = [i for i in result.insights if i.title == "Experience Trend"]
        assert len(trend) == 1
        assert "improved" in trend[0].summary.lower()


@pytest.mark.usefixtures("ctx")
class TestConfidenceAssignment:
    def test_low_confidence_for_few_observations(self, user):
        _submit_checkin(user.id)
        result = ResearchInsightService.generate_insights(as_of=date.today())
        exp = next(
            i for i in result.insights if i.title == "Average Product Experience"
        )
        assert exp.confidence == CONFIDENCE_LOW

    def test_medium_confidence_threshold(self, user):
        for _ in range(5):
            _submit_checkin(user.id)
        result = ResearchInsightService.generate_insights(as_of=date.today())
        exp = next(
            i for i in result.insights if i.title == "Average Product Experience"
        )
        assert exp.confidence == CONFIDENCE_MEDIUM

    def test_high_confidence_threshold(self, user):
        for _ in range(10):
            _submit_checkin(user.id)
        result = ResearchInsightService.generate_insights(as_of=date.today())
        exp = next(
            i for i in result.insights if i.title == "Average Product Experience"
        )
        assert exp.confidence == CONFIDENCE_HIGH


@pytest.mark.usefixtures("ctx")
class TestReleaseComparison:
    def test_version_comparison_insight(self, user):
        _submit_checkin(user.id, version="1.0.0", experience="Good")
        _submit_checkin(user.id, version="1.0.1", experience="Excellent")
        result = ResearchInsightService.generate_insights(
            time_window=TIME_WINDOW_CURRENT_RELEASE,
            current_release="1.0.1",
            previous_release="1.0.0",
            as_of=date.today(),
        )
        version_insights = [
            i for i in result.insights if i.title == "Version Comparison"
        ]
        assert len(version_insights) == 1
        assert "1.0.1" in version_insights[0].summary

    def test_release_panel_includes_findings(self, user, founder):
        submission = _submit_checkin(user.id, classification="Bug", free_text="Broken")
        finding = FounderResearchService.create_product_finding(
            founder.id,
            title="Dashboard bug",
            summary="Layout issue",
            severity="High",
            feature_area="Dashboard",
            linked_submission_ids=(submission.id,),
        )
        assert finding.id is not None
        result = ResearchInsightService.generate_insights(as_of=date.today())
        release_titles = {i.title for i in result.release_comparison}
        assert "New Findings" in release_titles


@pytest.mark.usefixtures("ctx")
class TestHistoryPreservation:
    def test_insights_do_not_modify_submissions(self, user, founder):
        submission = _submit_checkin(user.id)
        FounderResearchService.transition_submission_status(
            submission.id, founder.id, "under_review"
        )
        before_count = ResearchFeedbackStatusTransition.query.filter_by(
            submission_id=submission.id
        ).count()
        ResearchInsightService.generate_insights(as_of=date.today())
        after_count = ResearchFeedbackStatusTransition.query.filter_by(
            submission_id=submission.id
        ).count()
        assert before_count == after_count

    def test_insights_do_not_create_findings(self, user):
        before = ResearchProductFinding.query.count()
        _submit_checkin(user.id)
        ResearchInsightService.generate_insights(as_of=date.today())
        after = ResearchProductFinding.query.count()
        assert before == after


@pytest.mark.usefixtures("ctx")
class TestFounderIntegration:
    def test_legacy_get_insights_delegates(self, user):
        _submit_checkin(
            user.id,
            free_text="Add export",
            classification="Suggestion",
        )
        insights = FounderResearchService.get_insights()
        assert insights.most_common_feature == "Dashboard"
        assert insights.most_common_friction == "Navigation"
        assert insights.most_common_suggestion_category == "Suggestion"

    def test_dashboard_context_includes_insight_engine(self, user):
        _submit_checkin(user.id)
        context = FounderResearchService.build_dashboard_context()
        assert context.insight_engine is not None
        assert len(context.insight_engine.insights) >= 1
        assert context.insights.most_common_feature == "Dashboard"


@pytest.mark.usefixtures("ctx")
class TestEducationalIsolation:
    def test_insight_engine_does_not_mutate_educational_state(self, user):
        from app.models.curriculum import Curriculum, Topic

        curriculum = Curriculum(exam_name="IFoA CM1", version="2025", active=True)
        db.session.add(curriculum)
        db.session.flush()
        topic = Topic(
            name="Topic A",
            curriculum_id=curriculum.id,
            order=1,
            recommended_minutes=60,
            active=True,
        )
        db.session.add(topic)
        db.session.flush()

        subject = Subject(user_id=user.id, name="Exam")
        db.session.add(subject)
        db.session.flush()
        mission = Mission(
            user_id=user.id,
            subject_id=subject.id,
            mission_date=date.today(),
            title="Today",
            status="Completed",
        )
        mission.tasks.append(MissionTask(title="Study", order=0, completed=True))
        db.session.add(mission)
        db.session.flush()
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topic.id,
            mastery_score=55.0,
            current_stage=TopicProgress.STAGE_LEARNING,
            revision_count=1,
            average_accuracy=60.0,
            next_review_date=date.today() + timedelta(days=2),
            completed=False,
        )
        db.session.add(progress)
        db.session.commit()

        before_mastery = progress.mastery_score
        before_status = mission.status

        _submit_checkin(user.id)
        ResearchInsightService.generate_insights(as_of=date.today())

        db.session.refresh(mission)
        db.session.refresh(progress)
        assert mission.status == before_status
        assert progress.mastery_score == before_mastery


@pytest.mark.usefixtures("ctx")
class TestInsightEngineHttp:
    @pytest.fixture
    def founder_client(self, client, app):
        app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
        founder = _make_user("founder@kwalitec.example")
        client.post(
            "/auth/login",
            data={"email": founder.email, "password": "password123"},
            follow_redirects=True,
        )
        return client

    def test_dashboard_shows_insight_panels(self, founder_client, user):
        _submit_checkin(user.id)
        response = founder_client.get("/research/founder")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert 'data-rip004-insight-engine="1"' in body
        assert "Top Trends" in body
        assert "Emerging Concerns" in body
        assert "Most Improved Areas" in body
        assert "Stable Areas" in body
        assert "Participation" in body
        assert "Release Comparison" in body
        assert "Insights describe patterns" in body

    def test_time_window_filter(self, founder_client, user):
        _submit_checkin(user.id)
        response = founder_client.get(
            "/research/founder",
            query_string={"time_window": TIME_WINDOW_TODAY},
        )
        assert response.status_code == 200
        assert "Today" in response.get_data(as_text=True)
