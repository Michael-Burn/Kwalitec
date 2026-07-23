"""Missing optional inputs — graceful degradation."""

from __future__ import annotations

from application.student_experience.home import (
    FocusActionKind,
    HomeInputs,
    MasteryTrendLabel,
    ReadinessTrend,
    StudentHomeService,
)
from tests.application.student_experience.home.conftest import AS_OF, STUDENT_ID


def test_home_with_only_student_and_as_of(service: StudentHomeService) -> None:
    home = service.build_home(HomeInputs(student_id=STUDENT_ID, as_of=AS_OF))
    assert home.todays_focus.has_focus is False
    assert home.todays_focus.primary_action_kind is FocusActionKind.NONE
    assert home.todays_study_session.has_session is False
    assert home.progress.mastery_trend is MasteryTrendLabel.NOT_YET_ASSESSED
    assert home.exam_readiness.available is False
    assert home.exam_readiness.trend is ReadinessTrend.UNKNOWN
    assert home.achievements.has_achievements is False
    assert home.learning_insights.has_insights is False
    assert home.quick_actions.actions == ()


def test_exam_readiness_absent_without_exam_target(
    service: StudentHomeService,
) -> None:
    from tests.application.student_experience.home.conftest import make_full_inputs

    home = service.build_home(
        make_full_inputs(exam_target=None, schedule=None)
    )
    assert home.exam_readiness.available is False


def test_home_with_plan_only(service: StudentHomeService) -> None:
    from tests.application.student_experience.home.conftest import (
        make_full_inputs,
        make_plan,
    )

    home = service.build_home(
        make_full_inputs(
            mission_plan=make_plan(),
            schedule=None,
            assessment=None,
            evaluation=None,
            recommendation_set=None,
            execution_history=None,
            exam_target=None,
            current_execution=None,
        )
    )
    assert home.todays_focus.has_focus is True
    assert home.todays_focus.primary_action_kind is FocusActionKind.START_MISSION
