"""First-time student experience tests (Capability 4.4)."""

from __future__ import annotations

from app.extensions import db
from app.services.welcome_service import WelcomeService


class TestWelcomeService:
    def test_mark_eligible_and_should_show(self, db, user):
        assert WelcomeService.should_show(user) is False
        WelcomeService.mark_eligible(user.id)
        db.session.refresh(user)
        assert user.welcome_eligible is True
        assert WelcomeService.should_show(user) is True

    def test_dismiss_never_shows_again(self, db, user):
        WelcomeService.mark_eligible(user.id)
        assert WelcomeService.dismiss(user.id) is True
        db.session.refresh(user)
        assert user.welcome_dismissed is True
        assert user.welcome_eligible is False
        assert WelcomeService.should_show(user) is False
        # Re-mark after dismiss must not reopen the modal
        WelcomeService.mark_eligible(user.id)
        db.session.refresh(user)
        assert WelcomeService.should_show(user) is False

    def test_dashboard_shows_welcome_when_eligible(self, logged_in_client, user):
        WelcomeService.mark_eligible(user.id)
        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Welcome to Kwalitec" in body
        assert "Start Studying" in body
        assert "welcome-modal" in body

    def test_dashboard_hides_welcome_when_dismissed(self, logged_in_client, user):
        WelcomeService.mark_eligible(user.id)
        WelcomeService.dismiss(user.id)
        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        assert b"Welcome to Kwalitec" not in response.data

    def test_dismiss_endpoint_persists(self, logged_in_client, user):
        WelcomeService.mark_eligible(user.id)
        response = logged_in_client.post(
            "/dashboard/welcome/dismiss",
            follow_redirects=True,
        )
        assert response.status_code == 200
        db.session.refresh(user)
        assert user.welcome_dismissed is True
        assert b"Welcome to Kwalitec" not in response.data


class TestEmptyStatesAndOnboarding:
    def test_dashboard_next_step_without_plan(self, logged_in_client):
        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Create your study plan" in body
        assert "Create Study Plan" in body

    def test_mission_empty_state_without_plan(self, logged_in_client):
        response = logged_in_client.get("/missions/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "No Study Plan" in body
        assert "personalised recommendations" in body

    def test_mission_includes_study_tip(self, logged_in_client):
        response = logged_in_client.get("/missions/")
        assert response.status_code == 200
        assert b"Study Tip" in response.data

    def test_study_plan_list_empty_copy(self, logged_in_client):
        response = logged_in_client.get("/study-plan/plans/all")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "No Study Plan" in body
        assert "personalised recommendations" in body
