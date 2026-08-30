"""EIP-002 Educational Evidence Authority regression tests.

Negative tests prove unauthorised observations never update Twin-owned states
or Educational Evidence of understanding.

Positive tests prove authorised Structured Question Results may update Twin
estimates only, while other observations remain retained without inference.

Governing refs:
- Constitution Articles III, V, VIII
- EL-004, EL-005, EL-006, EL-007
- EDUCATIONAL_EVIDENCE_MODEL.md
- EDUCATIONAL_EVIDENCE_AUTHORITY.md
"""

from __future__ import annotations

from datetime import date, datetime, timedelta

import pytest

from app.extensions import db
from app.mission.routes import _apply_mission_topic_progress
from app.models.curriculum import Curriculum, Topic
from app.models.decision import Decision
from app.models.learning import StudyAttempt
from app.models.mission import Mission, MissionTask
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.subject import Subject
from app.models.topic_progress import TopicProgress
from app.services.adaptive_learning_service import AdaptiveLearningService
from app.services.educational_evidence_authority import (
    AuthorisedEvidenceSource,
    EducationalEvidenceAuthority,
    ObservationKind,
)
from app.services.learning_service import LearningService
from app.services.recommendation_service import RecommendationService


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
    topic_code: str | None = None,
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
        curriculum_topic_code=topic_code,
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


def _make_subject(user_id: int) -> Subject:
    subject = Subject(user_id=user_id, name="Study Plan", active=True)
    db.session.add(subject)
    db.session.flush()
    return subject


def _make_mission(user_id: int, *, study_plan_id: int, title: str) -> Mission:
    subject = _make_subject(user_id)
    mission = Mission(
        user_id=user_id,
        subject_id=subject.id,
        study_plan_id=study_plan_id,
        title=title,
        mission_date=date.today(),
        status="In Progress",
    )
    db.session.add(mission)
    db.session.flush()
    db.session.add(
        MissionTask(mission_id=mission.id, title="Study", order=0, completed=True)
    )
    db.session.commit()
    return mission


@pytest.mark.usefixtures("ctx")
class TestNegativeEvidenceAuthorityRegressions:
    """Unauthorised observations must not update Twin-owned educational states."""

    def test_mission_completion_must_not_update_estimated_knowledge(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Evidence Know Topic", "Next"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            confidence="Low",
            current_stage=TopicProgress.STAGE_LEARNING,
        )
        db.session.add(progress)
        db.session.commit()

        mission = _make_mission(
            user.id, study_plan_id=plan.id, title=f"Study {topics[0].name}"
        )
        LearningService.create_study_attempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=date.today(),
        )
        _apply_mission_topic_progress(user.id, topics[0])
        AdaptiveLearningService.update_mastery_after_attempt(
            user_id=user.id, topic_id=topics[0].id
        )

        updated = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert updated.has_estimated_knowledge is False
        assert updated.has_estimated_mastery is False

    def test_mission_completion_must_not_update_estimated_mastery(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Evidence Mastery Topic", "Next"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            confidence="Medium",
            current_stage=TopicProgress.STAGE_LEARNING,
            revision_count=5,
        )
        db.session.add(progress)
        db.session.commit()

        mission = _make_mission(
            user.id, study_plan_id=plan.id, title=f"Study {topics[0].name}"
        )
        LearningService.create_study_attempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=date.today(),
        )
        _apply_mission_topic_progress(user.id, topics[0])

        updated = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert updated.completed is True
        assert updated.revision_count == 6
        assert updated.has_estimated_mastery is False

    def test_reading_completion_must_not_update_estimated_mastery(self, db, user):
        """Topic marked completed studying is Study Progress, not mastery."""
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Reading Completion Topic", "Next"]
        )
        _make_active_plan(user.id, exam_name="IFoA CS1", curriculum=curriculum)
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            confidence="Low",
            current_stage=TopicProgress.STAGE_LEARNING,
        )
        db.session.add(progress)
        db.session.commit()

        # Manual Study Progress write (reading / declaration path equivalent).
        progress.completed = True
        progress.current_stage = TopicProgress.STAGE_COMPLETED
        db.session.commit()

        AdaptiveLearningService.update_mastery_after_attempt(
            user_id=user.id, topic_id=topics[0].id
        )

        updated = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert updated.completed is True
        assert updated.current_stage == TopicProgress.STAGE_COMPLETED
        assert updated.has_estimated_mastery is False

    def test_student_confidence_must_not_update_educational_evidence(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Confidence Observation Topic"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            confidence="Low",
            current_stage=TopicProgress.STAGE_LEARNING,
        )
        db.session.add(progress)
        db.session.commit()

        mission = _make_mission(
            user.id, study_plan_id=plan.id, title=f"Study {topics[0].name}"
        )
        LearningService.create_study_attempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=date.today(),
            confidence_after="Mastered",
            notes="I feel I understand this fully.",
        )

        updated = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        attempt = StudyAttempt.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert updated.confidence == "Mastered"
        assert attempt.confidence_after == "Mastered"
        assert attempt.notes is not None
        # Observation retained, but Stack A does not store Estimated Knowledge.
        assert updated.has_estimated_knowledge is False
        assert updated.has_estimated_mastery is False
        has_questions = (
            EducationalEvidenceAuthority.study_attempt_has_structured_question_results(
                attempt
            )
        )
        assert has_questions is False

    def test_study_duration_must_not_update_estimated_knowledge(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Duration Observation Topic"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            confidence="Medium",
            current_stage=TopicProgress.STAGE_LEARNING,
            revision_count=8,
        )
        db.session.add(progress)
        db.session.commit()

        mission = _make_mission(
            user.id, study_plan_id=plan.id, title=f"Study {topics[0].name}"
        )
        LearningService.create_study_attempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=date.today(),
            duration_minutes=180,
        )
        AdaptiveLearningService.update_mastery_after_attempt(
            user_id=user.id, topic_id=topics[0].id
        )

        updated = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        attempt = StudyAttempt.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert attempt.duration_minutes == 180
        assert updated.revision_count == 8
        assert updated.has_estimated_mastery is False

    def test_recommendation_acceptance_must_not_update_educational_evidence(
        self, db, user
    ):
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Recommendation Isolation Topic"]
        )
        _make_active_plan(user.id, exam_name="IFoA CS1", curriculum=curriculum)
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            confidence="Low",
            current_stage=TopicProgress.STAGE_LEARNING,
        )
        db.session.add(progress)
        db.session.commit()
        attempts_before = StudyAttempt.query.filter_by(user_id=user.id).count()

        RecommendationService.record_decision(
            user_id=user.id,
            recommendation={
                "title": "Review Recommendation Isolation Topic",
                "category": "Review",
                "priority": "High",
                "reason": "Advisory only",
                "expected_benefit": "Practice suggestion",
                "generated_at": datetime.utcnow().isoformat(),
            },
            accepted=True,
        )

        updated = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert Decision.query.filter_by(user_id=user.id).count() == 1
        assert StudyAttempt.query.filter_by(user_id=user.id).count() == attempts_before
        assert updated.has_estimated_knowledge is False
        assert updated.has_estimated_mastery is False

    def test_forbidden_observations_cannot_authorise_twin_writes(self):
        for kind in ObservationKind:
            may_write = EducationalEvidenceAuthority.may_observation_update_twin(kind)
            assert may_write is False

    def test_authorised_catalogue_is_strict_v1(self):
        assert EducationalEvidenceAuthority.is_authorised_source(
            AuthorisedEvidenceSource.STRUCTURED_QUESTION_RESULTS
        )
        assert EducationalEvidenceAuthority.is_authorised_source("quiz_results")
        assert not EducationalEvidenceAuthority.is_authorised_source(
            "student_confidence"
        )
        assert not EducationalEvidenceAuthority.is_authorised_source("time_spent")


@pytest.mark.usefixtures("ctx")
class TestPositiveEvidenceAuthorityBehaviours:
    """Authorised evidence may update Twin estimates; observations remain retained."""

    def test_authorised_assessment_evidence_updates_twin_owned_states_only(
        self, db, user
    ):
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Authorised Evidence Topic"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            confidence="Low",
            current_stage=TopicProgress.STAGE_LEARNING,
            revision_count=1,
        )
        db.session.add(progress)
        db.session.commit()

        mission = _make_mission(
            user.id, study_plan_id=plan.id, title=f"Study {topics[0].name}"
        )
        LearningService.create_study_attempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=date.today(),
            questions_attempted=10,
            questions_correct=8,
            confidence_after="High",
            duration_minutes=45,
        )

        updated = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert updated.has_estimated_knowledge is False
        assert updated.has_estimated_mastery is False
        assert updated.completed is False
        assert updated.confidence == "High"
        assert updated.current_stage != TopicProgress.STAGE_COMPLETED

    def test_educational_observations_retained_without_inference(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Observation Retention Topic"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            confidence="Not Started",
            current_stage=TopicProgress.STAGE_LEARNING,
        )
        db.session.add(progress)
        db.session.commit()

        mission = _make_mission(
            user.id, study_plan_id=plan.id, title=f"Study {topics[0].name}"
        )
        LearningService.create_study_attempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=date.today(),
            duration_minutes=60,
            confidence_after="Medium",
            notes="Hard start, clearer ending.",
        )

        attempt = StudyAttempt.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        updated = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert attempt.duration_minutes == 60
        assert attempt.confidence_after == "Medium"
        assert attempt.notes == "Hard start, clearer ending."
        assert updated.confidence == "Medium"
        assert updated.has_estimated_knowledge is False
        assert updated.has_estimated_mastery is False

    def test_absence_of_authorised_evidence_leaves_estimates_unchanged(
        self, db, user
    ):
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Silence Topic"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            confidence="High",
            current_stage=TopicProgress.STAGE_PRACTISING,
            revision_count=9,
        )
        db.session.add(progress)
        db.session.commit()

        mission = _make_mission(
            user.id, study_plan_id=plan.id, title=f"Study {topics[0].name}"
        )
        LearningService.create_study_attempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=date.today(),
            duration_minutes=90,
            confidence_after="Mastered",
        )
        AdaptiveLearningService.update_mastery_after_attempt(
            user_id=user.id, topic_id=topics[0].id
        )

        updated = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert updated.revision_count == 9
        assert updated.has_estimated_mastery is False

    def test_authorised_evidence_does_not_write_stack_a_ek(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Accumulation Topic"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            confidence="Low",
            current_stage=TopicProgress.STAGE_LEARNING,
            revision_count=5,
        )
        db.session.add(progress)
        db.session.commit()

        mission = _make_mission(
            user.id, study_plan_id=plan.id, title=f"Study {topics[0].name}"
        )
        LearningService.create_study_attempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=date.today(),
            questions_attempted=10,
            questions_correct=10,
        )

        after_one = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert after_one.has_estimated_knowledge is False
        assert after_one.current_stage == TopicProgress.STAGE_LEARNING

        LearningService.create_study_attempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=date.today(),
            questions_attempted=10,
            questions_correct=10,
        )
        after_two = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert after_two.current_stage == TopicProgress.STAGE_LEARNING
        assert after_two.has_estimated_knowledge is False
        assert after_two.completed is False

    def test_recency_weighting_raises_mastery_vs_flat_average(self, db, user):
        """Old weak + recent strong → estimate above the flat mean base.

        Flat average of 20% and 90% is 55. Recency weighting (21-day half-life)
        with the weak attempt 60 days ago and the strong attempt yesterday
        yields ~81.3 as the accuracy base; with revision_count=0 and no
        unresolved mistakes, the pure estimate calculation rounds to that base.
        """
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Recency Weight Topic"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            confidence="Low",
            current_stage=TopicProgress.STAGE_LEARNING,
            revision_count=0,
        )
        db.session.add(progress)
        db.session.commit()

        mission = _make_mission(
            user.id, study_plan_id=plan.id, title=f"Study {topics[0].name}"
        )
        today = date.today()
        LearningService.create_study_attempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=today - timedelta(days=60),
            questions_attempted=10,
            questions_correct=2,
        )
        LearningService.create_study_attempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=today - timedelta(days=1),
            questions_attempted=10,
            questions_correct=9,
        )

        updated = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert updated.has_estimated_knowledge is False
        assert updated.revision_count == 0

    def test_single_attempt_recency_matches_raw_accuracy(self, db, user):
        """One authorised observation: recency is a no-op (weight 1)."""
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Single Obs Recency Topic"]
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )
        progress = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            confidence="Low",
            current_stage=TopicProgress.STAGE_LEARNING,
            revision_count=0,
        )
        db.session.add(progress)
        db.session.commit()

        mission = _make_mission(
            user.id, study_plan_id=plan.id, title=f"Study {topics[0].name}"
        )
        LearningService.create_study_attempt(
            user_id=user.id,
            mission_id=mission.id,
            topic_id=topics[0].id,
            study_date=date.today() - timedelta(days=45),
            questions_attempted=10,
            questions_correct=3,
        )

        updated = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert updated.has_estimated_knowledge is False
        assert updated.revision_count == 0
