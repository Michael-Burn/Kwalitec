"""UX-001 / FV-001B — Founder routing and Experience Selection."""

from __future__ import annotations

from unittest.mock import patch

from app.extensions import db
from app.models import User
from app.presentation.consolidation import (
    CANONICAL_HOME_ENDPOINT,
    CONSOLE_HOME_ENDPOINT,
    canonical_home_endpoint,
)
from app.security.roles import Role
from app.services.identity_service import IdentityService
from tests.presentation.workflows.helpers import dual_run_flags


def _make_user(email: str) -> User:
    user = User(email=email, is_active_user=True)
    user.set_password("password123")
    user.alpha_onboarding_completed = True
    db.session.add(user)
    db.session.commit()
    return user


def _login_post(client, email: str):
    return client.post(
        "/auth/login",
        data={"email": email, "password": "password123"},
        follow_redirects=False,
    )


def _assert_lands_on_experience_selection(response) -> None:
    """Dual-access operators choose Founder vs Student after login (FV-001B)."""
    assert response.status_code in {302, 303}
    location = response.headers.get("Location", "")
    assert "/auth/experience" in location
    assert "/student" not in location or "/auth/experience" in location


def _assert_lands_on_student_os(response) -> None:
    assert response.status_code in {302, 303}
    location = response.headers.get("Location", "")
    assert "/console/" not in location
    assert "/auth/experience" not in location
    assert any(
        token in location for token in ("/student", "study-plan", "alpha/onboarding")
    )


def test_founder_login_lands_on_experience_selection(app, client, ctx):
    user = _make_user("ux001-founder@kwalitec.example")
    IdentityService.grant_role(user, Role.FOUNDER)
    _assert_lands_on_experience_selection(_login_post(client, user.email))


def test_administrator_login_lands_on_experience_selection(app, client, ctx):
    """Administrator role alone (no UserCapability rows) → Experience Selection."""
    user = _make_user("ux001-admin@kwalitec.example")
    IdentityService.grant_role(user, Role.ADMINISTRATOR)
    db.session.refresh(user)
    assert not user.get_capabilities()
    _assert_lands_on_experience_selection(_login_post(client, user.email))


def test_student_only_login_lands_on_student_os(app, client, ctx):
    user = _make_user("ux001-student@kwalitec.example")
    IdentityService.ensure_student_defaults(user)
    _assert_lands_on_student_os(_login_post(client, user.email))


def test_founder_plus_student_lands_on_experience_selection(app, client, ctx):
    user = _make_user("ux001-founder-student@kwalitec.example")
    IdentityService.grant_role(user, Role.FOUNDER)
    IdentityService.grant_role(user, Role.STUDENT)
    _assert_lands_on_experience_selection(_login_post(client, user.email))


def test_administrator_plus_student_lands_on_experience_selection(app, client, ctx):
    user = _make_user("ux001-admin-student@kwalitec.example")
    IdentityService.grant_role(user, Role.ADMINISTRATOR)
    IdentityService.grant_role(user, Role.STUDENT)
    _assert_lands_on_experience_selection(_login_post(client, user.email))


def test_canonical_home_endpoint_role_matrix(app, client, ctx):
    """Authenticated home endpoint follows Console vs Student OS rules."""
    founder = _make_user("ux001-home-founder@kwalitec.example")
    IdentityService.grant_role(founder, Role.FOUNDER)
    admin = _make_user("ux001-home-admin@kwalitec.example")
    IdentityService.grant_role(admin, Role.ADMINISTRATOR)
    student = _make_user("ux001-home-student@kwalitec.example")
    IdentityService.ensure_student_defaults(student)

    with patch(
        "app.presentation.consolidation.resolve_v2_feature_flags",
        return_value=dual_run_flags(SOLE_RUNTIME=True),
    ):
        for user, expected in (
            (founder, CONSOLE_HOME_ENDPOINT),
            (admin, CONSOLE_HOME_ENDPOINT),
            (student, CANONICAL_HOME_ENDPOINT),
        ):
            client.post(
                "/auth/login",
                data={"email": user.email, "password": "password123"},
                follow_redirects=True,
            )
            with client:
                client.get("/")
                assert canonical_home_endpoint() == expected, user.email
            client.post("/auth/logout")


def test_console_exposes_switch_and_enter_student(app, client, ctx):
    user = _make_user("ux001-entry@kwalitec.example")
    IdentityService.ensure_founder_admin(user)
    client.post(
        "/auth/login",
        data={"email": user.email, "password": "password123"},
        follow_redirects=True,
    )
    response = client.get("/console/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Switch Experience" in html
    assert 'data-testid="switch-experience"' in html
    assert "Enter Student Experience" in html
    assert 'data-testid="enter-student-experience"' in html
    assert "/student/" in html
    assert "/auth/experience" in html


def test_experience_selection_page_for_founder(app, client, ctx):
    user = _make_user("ux001-exp@kwalitec.example")
    IdentityService.grant_role(user, Role.FOUNDER)
    client.post(
        "/auth/login",
        data={"email": user.email, "password": "password123"},
        follow_redirects=False,
    )
    response = client.get("/auth/experience")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Choose your experience" in html
    assert 'data-testid="choose-founder-console"' in html
    assert 'data-testid="choose-student-experience"' in html
    assert "always_ask" in html
    assert "remember_founder" in html
    assert "remember_student" in html
    assert "experience_preference.js" in html


def test_experience_selection_forbidden_for_student_only(app, client, ctx):
    user = _make_user("ux001-exp-student@kwalitec.example")
    IdentityService.ensure_student_defaults(user)
    client.post(
        "/auth/login",
        data={"email": user.email, "password": "password123"},
        follow_redirects=True,
    )
    response = client.get("/auth/experience", follow_redirects=False)
    assert response.status_code in {302, 303}
    assert "/auth/experience" not in response.headers.get("Location", "")


def test_student_journey_home_ignores_founder_console_rbac(app, client, ctx):
    """Dual-access Completing student setup must not resolve Console as Home."""
    from app.presentation.consolidation import (
        canonical_home_url,
        student_home_url,
    )

    user = _make_user("ux001-student-journey@kwalitec.example")
    IdentityService.grant_role(user, Role.FOUNDER)
    IdentityService.grant_role(user, Role.STUDENT)
    client.post(
        "/auth/login",
        data={"email": user.email, "password": "password123"},
        follow_redirects=True,
    )
    with client:
        client.get("/student/")
        assert "/student" in student_home_url()
        assert "/console" in canonical_home_url()


def test_baseline_finalize_keeps_founder_in_student_experience(
    app, client, ctx, monkeypatch
):
    """Begin learning must open Student Home, not Founder Console."""
    from datetime import date, timedelta
    from types import SimpleNamespace

    from app.application.student_baseline import (
        BaselineSubjectScope,
        StudentBaselineService,
    )
    from app.application.student_baseline.enums import (
        ConfidenceBand,
        ExamHistory,
        LearningObjective,
        PositionMode,
        PreviousExperience,
    )

    user = _make_user("ux001-baseline-finalize@kwalitec.example")
    IdentityService.grant_role(user, Role.FOUNDER)
    client.post(
        "/auth/login",
        data={"email": user.email, "password": "password123"},
        follow_redirects=True,
    )

    with client.session_transaction() as sess:
        sess["wizard_data"] = {
            "exam_category": "IFoA",
            "exam_paper": "CS1",
            "exam_sitting": "April 2027",
            "exam_date": (date.today() + timedelta(days=200)).isoformat(),
            "weekday_study_minutes": 60,
            "weekend_study_minutes": 90,
            "preferred_session_minutes": 60,
            "study_preference": "Mixed",
            "target_grade": "Pass",
            "curriculum_version": "2026",
        }

    scope = BaselineSubjectScope(
        subject_key="IFoA:CS1",
        category_code="IFoA",
        subject_code="CS1",
        curriculum_version="2026",
        exam_name="IFoA CS1",
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=200),
        weekday_study_minutes=60,
        weekend_study_minutes=90,
        preferred_session_minutes=60,
        study_preference="Mixed",
        target_grade="Pass",
    )
    draft = StudentBaselineService.ensure_draft(user.id, scope)
    StudentBaselineService.save_answer(
        draft.id,
        user.id,
        experience=PreviousExperience.BRAND_NEW.value,
        position_mode=PositionMode.START_BEGINNING.value,
        exam_history=ExamHistory.FIRST_SITTING.value,
        learning_objective=LearningObjective.RECOMMEND.value,
        confidence=ConfidenceBand.MODERATE.value,
    )

    monkeypatch.setattr(
        "app.student_baseline.routes.BaselineFinalizeCoordinator.finalize",
        lambda self, **kwargs: SimpleNamespace(
            message=(
                "Enrolled in published curriculum CS1:2026.1 (Runtime C)."
            ),
        ),
    )

    resp = client.post(
        "/baseline/step/6",
        data={},
        follow_redirects=False,
    )
    assert resp.status_code in {302, 303}
    location = resp.headers.get("Location", "")
    assert "/student" in location
    assert "/console" not in location
