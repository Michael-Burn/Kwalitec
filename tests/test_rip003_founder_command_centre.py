"""RIP-003 Founder Research Command Centre tests.

Covers inbox workflow, status transitions, product findings, filtering,
searching, history preservation, contributor integration, and
educational state isolation.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.extensions import db
from app.models.mission import Mission, MissionTask
from app.models.research_feedback import (
    ResearchContributorBadge,
    ResearchFeedbackStatusTransition,
    ResearchFeedbackSubmission,
    ResearchProductFindingStatusTransition,
)
from app.models.subject import Subject
from app.models.topic_progress import TopicProgress
from app.models.user import User
from app.services.contributor_recognition_service import BADGE_PRODUCT_SHAPER
from app.services.founder_research_service import (
    FounderResearchService,
    InboxFilters,
)
from app.services.research_feedback_service import (
    SOURCE_SETTINGS,
    ResearchFeedbackService,
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
    )
    return result.submission


@pytest.fixture
def founder(app):
    app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
    return _make_user("founder@kwalitec.example")


@pytest.fixture
def founder_client(client, founder):
    client.post(
        "/auth/login",
        data={"email": founder.email, "password": "password123"},
        follow_redirects=True,
    )
    return client


@pytest.mark.usefixtures("ctx")
class TestWorkflowTransitions:
    def test_new_submission_starts_in_new_status(self, user):
        submission = _submit_checkin(user.id)
        assert submission.workflow_status == "new"

    def test_transition_records_history(self, user, founder):
        submission = _submit_checkin(user.id)
        result = FounderResearchService.transition_submission_status(
            submission.id,
            founder.id,
            "under_review",
            rationale="Initial triage",
        )
        assert result.submission.workflow_status == "under_review"
        history = ResearchFeedbackStatusTransition.query.filter_by(
            submission_id=submission.id
        ).all()
        assert len(history) == 1
        assert history[0].from_status == "new"
        assert history[0].to_status == "under_review"
        assert history[0].rationale == "Initial triage"
        assert history[0].reviewer_user_id == founder.id

    def test_history_never_overwritten(self, user, founder):
        submission = _submit_checkin(user.id)
        FounderResearchService.transition_submission_status(
            submission.id, founder.id, "under_review"
        )
        FounderResearchService.transition_submission_status(
            submission.id, founder.id, "accepted"
        )
        transitions = ResearchFeedbackStatusTransition.query.filter_by(
            submission_id=submission.id
        ).order_by(ResearchFeedbackStatusTransition.id).all()
        assert len(transitions) == 2
        assert transitions[0].to_status == "under_review"
        assert transitions[1].to_status == "accepted"

    def test_full_workflow_lifecycle(self, user, founder):
        submission = _submit_checkin(user.id)
        for status in (
            "under_review",
            "accepted",
            "planned",
            "implemented",
            "released",
            "verified",
        ):
            FounderResearchService.transition_submission_status(
                submission.id, founder.id, status
            )
        db.session.refresh(submission)
        assert submission.workflow_status == "verified"
        assert (
            ResearchFeedbackStatusTransition.query.filter_by(
                submission_id=submission.id
            ).count()
            == 6
        )

    def test_implement_awards_product_shaper(self, user, founder):
        submission = _submit_checkin(user.id)
        result = FounderResearchService.transition_submission_status(
            submission.id, founder.id, "implemented"
        )
        assert BADGE_PRODUCT_SHAPER in result.newly_earned_badges
        badge = ResearchContributorBadge.query.filter_by(
            user_id=user.id, badge_slug=BADGE_PRODUCT_SHAPER
        ).one()
        assert badge.trigger_submission_id == submission.id


@pytest.mark.usefixtures("ctx")
class TestProductFindings:
    def test_create_finding_with_linked_feedback(self, user, founder):
        submission = _submit_checkin(user.id)
        finding = FounderResearchService.create_product_finding(
            founder.id,
            title="Dashboard clarity",
            summary="Students find dashboard metrics confusing.",
            severity="High",
            feature_area="Dashboard",
            target_release="1.0.1",
            linked_submission_ids=(submission.id,),
        )
        assert finding.id is not None
        assert finding.target_release == "1.0.1"
        detail = FounderResearchService.get_finding_detail(finding.id)
        assert detail is not None
        assert len(detail.linked_submissions) == 1
        assert detail.linked_submissions[0].id == submission.id
        assert len(detail.status_history) == 1

    def test_finding_status_transition_preserves_history(self, user, founder):
        submission = _submit_checkin(user.id)
        finding = FounderResearchService.create_product_finding(
            founder.id,
            title="Nav friction",
            summary="Navigation labels unclear.",
            severity="Medium",
            feature_area="Navigation",
            linked_submission_ids=(submission.id,),
        )
        FounderResearchService.transition_finding_status(
            finding.id, founder.id, "planned", target_release="1.1.0"
        )
        db.session.refresh(finding)
        assert finding.status == "planned"
        assert finding.target_release == "1.1.0"
        transitions = ResearchProductFindingStatusTransition.query.filter_by(
            finding_id=finding.id
        ).all()
        assert len(transitions) == 2


@pytest.mark.usefixtures("ctx")
class TestFilteringAndSearch:
    def test_filter_by_status(self, user):
        sub_new = _submit_checkin(user.id, friction="Nothing")
        sub2 = _submit_checkin(user.id, feature="Study Plan")
        founder = _make_user("founder2@kwalitec.example")
        FounderResearchService.transition_submission_status(
            sub2.id, founder.id, "accepted"
        )
        inbox = FounderResearchService.list_inbox(InboxFilters(status="new"))
        ids = {s.id for s in inbox}
        assert sub_new.id in ids
        assert sub2.id not in ids

    def test_filter_by_version(self, user):
        v1 = _submit_checkin(user.id, version="1.0.0")
        v2 = _submit_checkin(user.id, version="1.1.0")
        inbox = FounderResearchService.list_inbox(InboxFilters(version="1.1.0"))
        assert [s.id for s in inbox] == [v2.id]
        assert v1.id not in {s.id for s in inbox}

    def test_keyword_search(self, user):
        _submit_checkin(user.id)
        tagged = _submit_checkin(
            user.id,
            free_text="The analytics chart is slow",
            classification="Bug",
        )
        inbox = FounderResearchService.list_inbox(
            InboxFilters(keyword="analytics")
        )
        assert [s.id for s in inbox] == [tagged.id]

    def test_student_search(self, user):
        _submit_checkin(user.id)
        _submit_checkin(user.id)
        inbox = FounderResearchService.list_inbox(
            InboxFilters(student=user.email)
        )
        assert len(inbox) == 2


@pytest.mark.usefixtures("ctx")
class TestFounderNotes:
    def test_add_founder_note(self, user, founder):
        submission = _submit_checkin(user.id)
        note = FounderResearchService.add_founder_note(
            submission.id,
            founder.id,
            "Worth exploring for 1.0.1",
        )
        assert note.note_text == "Worth exploring for 1.0.1"
        detail = FounderResearchService.get_submission_detail(submission.id)
        assert detail is not None
        assert len(detail.founder_notes) == 1


@pytest.mark.usefixtures("ctx")
class TestDashboardAggregations:
    def test_internal_alpha_summary(self, user):
        _submit_checkin(user.id, experience="Excellent")
        _submit_checkin(user.id, experience="Good")
        summary = FounderResearchService.get_internal_alpha_summary()
        assert summary.active_participants == 1
        assert summary.completed_checkins == 2
        assert summary.outstanding_reviews == 2
        assert summary.avg_product_experience == 4.5

    def test_product_health_aggregation(self, user):
        _submit_checkin(user.id, feature="Dashboard", friction="Navigation")
        _submit_checkin(user.id, feature="Dashboard", friction="Navigation")
        health = FounderResearchService.get_product_health()
        assert health.most_loved_feature == "Dashboard"
        assert health.most_mentioned_friction == "Navigation"

    def test_insights_aggregation(self, user):
        _submit_checkin(
            user.id,
            free_text="Add export",
            classification="Suggestion",
        )
        insights = FounderResearchService.get_insights()
        assert insights.most_common_feature == "Dashboard"
        assert insights.most_common_friction == "Navigation"
        assert insights.most_common_suggestion_category == "Suggestion"


@pytest.mark.usefixtures("ctx")
class TestContributorIntegration:
    def test_helpful_marks_via_service(self, user, founder):
        submission = _submit_checkin(user.id)
        review = FounderResearchService.apply_founder_marks(
            submission.id, founder.id, helpful=True
        )
        assert review.is_helpful is True
        assert review.is_insightful is False


@pytest.mark.usefixtures("ctx")
class TestEducationalIsolation:
    def test_command_centre_does_not_mutate_educational_state(self, user, founder):
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

        submission = _submit_checkin(user.id)
        FounderResearchService.transition_submission_status(
            submission.id, founder.id, "implemented"
        )
        FounderResearchService.create_product_finding(
            founder.id,
            title="Test",
            summary="Test finding",
            severity="Low",
            feature_area="Dashboard",
            linked_submission_ids=(submission.id,),
        )

        db.session.refresh(mission)
        db.session.refresh(progress)
        assert mission.status == before_status
        assert progress.mastery_score == before_mastery


@pytest.mark.usefixtures("ctx")
class TestCommandCentreHttp:
    def test_founder_dashboard_access(self, founder_client):
        response = founder_client.get("/research/founder")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert 'data-rip003-command-centre="1"' in body
        assert "Research Command Centre" in body
        assert "Internal Alpha Summary" in body

    def test_student_forbidden(self, client, app, user):
        app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
        _submit_checkin(user.id)
        client.post(
            "/auth/login",
            data={"email": user.email, "password": "password123"},
            follow_redirects=True,
        )
        response = client.get("/research/founder")
        assert response.status_code == 403

    def test_workflow_action_via_http(self, founder_client, user, founder):
        submission = _submit_checkin(user.id)
        response = founder_client.post(
            "/research/founder",
            data={
                "action": "accept",
                "submission_id": str(submission.id),
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        db.session.refresh(submission)
        assert submission.workflow_status == "accepted"

    def test_finding_detail_page(self, founder_client, user, founder):
        submission = _submit_checkin(user.id)
        finding = FounderResearchService.create_product_finding(
            founder.id,
            title="Study Session timing",
            summary="Session duration unclear.",
            severity="Medium",
            feature_area="Study Session",
            linked_submission_ids=(submission.id,),
        )
        response = founder_client.get(f"/research/founder/finding/{finding.id}")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert 'data-rip003-finding-detail="1"' in body
        assert "Study Session timing" in body

    def test_founder_review_redirects_to_command_centre(
        self, client, app, user, founder
    ):
        app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
        submission = _submit_checkin(user.id)
        client.post(
            "/auth/login",
            data={"email": founder.email, "password": "password123"},
            follow_redirects=True,
        )
        response = client.post(
            f"/research/founder/review/{submission.id}",
            data={"implemented": "y"},
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert "/research/founder" in response.location
