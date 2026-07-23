"""ALPHA-001 Internal Alpha infrastructure tests.

Covers onboarding, lightweight feedback, presentation telemetry,
error pages with reference IDs, release info, accessibility basics,
and architecture purity (no analytics on domain models / no Education OS
coupling).
"""

from __future__ import annotations

import ast
from pathlib import Path

from app.extensions import db
from app.models.alpha_infrastructure import (
    AlphaFeedbackSubmission,
    PresentationEvent,
)
from app.models.user import User
from app.services.alpha_feedback_service import (
    KIND_MISSION_HELPFUL,
    KIND_REPORT_PROBLEM,
    AlphaFeedbackService,
)
from app.services.alpha_onboarding_service import AlphaOnboardingService
from app.services.presentation_telemetry_service import (
    ALLOWED_EVENTS,
    EVENT_DASHBOARD_OPENED,
    EVENT_FEEDBACK_SUBMITTED,
    EVENT_MISSION_STARTED,
    PresentationTelemetryService,
)
from app.services.release_info_service import ReleaseInfoService


def _login(
    client,
    email: str = "alpha@kwalitec.example",
    password: str = "password123",
):
    return client.post(
        "/auth/login",
        data={"email": email, "password": password},
        follow_redirects=False,
    )


def _make_alpha_user(
    *,
    email: str = "alpha@kwalitec.example",
    onboarding_done: bool = False,
) -> User:
    user = User(email=email, is_active_user=True)
    user.set_password("password123")
    user.alpha_onboarding_completed = onboarding_done
    user.alpha_onboarding_skipped = False
    db.session.add(user)
    db.session.commit()
    return user


class TestAlphaOnboarding:
    def test_onboarding_page_explains_core_concepts(self, client, ctx):
        _make_alpha_user()
        _login(client)
        response = client.get("/alpha/onboarding")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "What Kwalitec is" in body
        assert "How missions work" in body
        assert "Why recommendations are explainable" in body
        assert "How reflection works" in body
        assert 'role="main"' in body or "<main" in body or "section-title" in body

    def test_dashboard_redirects_to_onboarding_when_pending(self, client, ctx):
        _make_alpha_user(onboarding_done=False)
        _login(client)
        response = client.get("/dashboard/")
        assert response.status_code == 302
        assert "/alpha/onboarding" in response.headers["Location"]

    def test_complete_onboarding_allows_dashboard(self, client, ctx):
        user = _make_alpha_user(onboarding_done=False)
        _login(client)
        response = client.post("/alpha/onboarding/complete", follow_redirects=False)
        assert response.status_code == 302
        db.session.refresh(user)
        assert user.alpha_onboarding_completed is True
        dash = client.get("/dashboard/")
        assert dash.status_code == 200

    def test_skip_onboarding(self, client, ctx):
        user = _make_alpha_user(onboarding_done=False)
        _login(client)
        client.post("/alpha/onboarding/skip")
        db.session.refresh(user)
        assert user.alpha_onboarding_skipped is True
        assert AlphaOnboardingService.should_show(user) is False


class TestAlphaFeedback:
    def test_mission_helpful_stores_structured_feedback(self, client, ctx):
        user = _make_alpha_user(onboarding_done=True)
        _login(client)
        response = client.post(
            "/alpha/feedback/mission-helpful",
            data={
                "kind": KIND_MISSION_HELPFUL,
                "rating": "yes",
                "message": "Focused well",
                "surface": "mission",
            },
            follow_redirects=False,
        )
        assert response.status_code == 302
        row = AlphaFeedbackSubmission.query.filter_by(user_id=user.id).one()
        assert row.kind == KIND_MISSION_HELPFUL
        assert row.rating == "yes"
        assert row.message == "Focused well"
        assert row.product_version

    def test_report_problem_requires_message(self, client, ctx):
        _make_alpha_user(onboarding_done=True)
        _login(client)
        response = client.post(
            "/alpha/feedback/report-problem",
            data={"kind": KIND_REPORT_PROBLEM, "message": ""},
        )
        assert response.status_code == 200
        assert AlphaFeedbackSubmission.query.count() == 0

    def test_feedback_service_rejects_unknown_kind(self, ctx):
        user = _make_alpha_user(onboarding_done=True)
        result = AlphaFeedbackService.submit(
            user_id=user.id,
            kind="not_a_real_kind",
            message="x",
        )
        assert result.ok is False


class TestPresentationTelemetry:
    def test_allowed_events_match_alpha_contract(self):
        expected = {
            "dashboard_opened",
            "mission_started",
            "mission_completed",
            "reflection_completed",
            "coach_opened",
            "journey_opened",
            "readiness_opened",
            "provenance_expanded",
            "feedback_submitted",
        }
        assert ALLOWED_EVENTS == expected

    def test_dashboard_records_opened_event(self, client, ctx):
        user = _make_alpha_user(onboarding_done=True)
        _login(client)
        response = client.get("/dashboard/")
        assert response.status_code == 200
        event = PresentationEvent.query.filter_by(
            user_id=user.id, event_type=EVENT_DASHBOARD_OPENED
        ).one()
        assert event.path == "/dashboard/"

    def test_rejects_unknown_event(self, ctx):
        user = _make_alpha_user(onboarding_done=True)
        result = PresentationTelemetryService.record(
            "secret_domain_score",
            user_id=user.id,
        )
        assert result is None
        assert PresentationEvent.query.count() == 0

    def test_client_telemetry_ingest(self, client, ctx):
        user = _make_alpha_user(onboarding_done=True)
        _login(client)
        response = client.post(
            "/alpha/telemetry",
            data={"event_type": "provenance_expanded", "surface": "home"},
        )
        assert response.status_code == 200
        assert response.get_json()["ok"] is True
        assert (
            PresentationEvent.query.filter_by(
                user_id=user.id, event_type="provenance_expanded"
            ).count()
            == 1
        )

    def test_client_telemetry_rejects_non_client_event(self, client, ctx):
        _make_alpha_user(onboarding_done=True)
        _login(client)
        response = client.post(
            "/alpha/telemetry",
            data={"event_type": EVENT_MISSION_STARTED},
        )
        assert response.status_code == 400

    def test_feedback_emits_feedback_submitted(self, client, ctx):
        user = _make_alpha_user(onboarding_done=True)
        _login(client)
        client.post(
            "/alpha/feedback/mission-helpful",
            data={"kind": KIND_MISSION_HELPFUL, "rating": "no", "surface": "mission"},
        )
        assert (
            PresentationEvent.query.filter_by(
                user_id=user.id, event_type=EVENT_FEEDBACK_SUBMITTED
            ).count()
            == 1
        )


class TestErrorPages:
    def test_404_includes_reference_and_retry_path(self, client, ctx):
        _make_alpha_user(onboarding_done=True)
        _login(client)
        response = client.get("/this-route-does-not-exist-alpha-001")
        assert response.status_code == 404
        body = response.get_data(as_text=True)
        assert "Reference ID" in body
        assert "Help" in body or "Dashboard" in body
        assert response.headers.get("X-Correlation-ID") or "Reference ID" in body

    def test_correlation_header_on_normal_request(self, client, ctx):
        _make_alpha_user(onboarding_done=True)
        _login(client)
        response = client.get(
            "/alpha/help",
            headers={"X-Correlation-ID": "abc123correlation"},
        )
        assert response.status_code == 200
        assert response.headers.get("X-Correlation-ID") == "abc123correlation"


class TestReleaseInfo:
    def test_help_centre_shows_release_fields(self, client, ctx, monkeypatch):
        monkeypatch.setenv("KWALITEC_BUILD_DATE", "2026-07-23")
        monkeypatch.setenv("KWALITEC_BUILD_NUMBER", "alpha-test")
        monkeypatch.setenv("KWALITEC_GIT_COMMIT", "deadbeefcafebabe")
        monkeypatch.setenv("KWALITEC_SUPPORT_CONTACT", "alpha-test@kwalitec.com")
        # Clear cached process start date if any — ReleaseInfo rebuilds each call
        # except _process_start_date cache which is unused when BUILD_DATE is set.
        _make_alpha_user(onboarding_done=True)
        _login(client)
        response = client.get("/alpha/help")
        body = response.get_data(as_text=True)
        assert response.status_code == 200
        assert "2026-07-23" in body
        assert "alpha-test" in body
        assert "deadbeefcafebabe" in body
        assert "alpha-test@kwalitec.com" in body

    def test_settings_general_shows_release_info(self, client, ctx):
        _make_alpha_user(onboarding_done=True)
        _login(client)
        response = client.get("/settings/")
        body = response.get_data(as_text=True)
        assert "Build date" in body
        assert "Environment" in body
        assert "Support contact" in body

    def test_health_includes_release_metadata(self, client, ctx, monkeypatch):
        monkeypatch.setenv("KWALITEC_BUILD_DATE", "2026-07-23")
        response = client.get("/health")
        payload = response.get_json()
        assert payload["status"] in {"ok", "degraded"}
        assert "version" in payload
        assert "environment" in payload
        assert payload["build_date"] == "2026-07-23"

    def test_release_info_service_defaults(self, monkeypatch):
        monkeypatch.delenv("KWALITEC_SUPPORT_CONTACT", raising=False)
        monkeypatch.delenv("KWALITEC_GIT_COMMIT", raising=False)
        monkeypatch.delenv("RENDER_GIT_COMMIT", raising=False)
        monkeypatch.delenv("SOURCE_VERSION", raising=False)
        info = ReleaseInfoService.current()
        assert info.app_version
        assert info.environment
        assert info.support_contact
        assert "@" in info.support_contact


class TestAccessibilityBasics:
    def test_onboarding_has_landmarks_and_headings(self, client, ctx):
        _make_alpha_user()
        _login(client)
        body = client.get("/alpha/onboarding").get_data(as_text=True)
        assert "<h1" in body
        assert "<h2" in body
        assert "Continue to Dashboard" in body

    def test_feedback_form_exposes_labels(self, client, ctx):
        _make_alpha_user(onboarding_done=True)
        _login(client)
        body = client.get("/alpha/feedback/mission-helpful").get_data(as_text=True)
        assert "Was this mission helpful?" in body
        assert 'type="submit"' in body
        assert "Cancel" in body

    def test_error_page_has_main_landmark(self, client, ctx):
        body = client.get("/missing-alpha-page").get_data(as_text=True)
        assert 'role="main"' in body
        assert "404" in body


class TestArchitecturePurity:
    def test_alpha_models_do_not_import_education_os_or_domain(self):
        path = Path("app/models/alpha_infrastructure.py")
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module)
        forbidden = {
            name
            for name in imports
            if name.startswith(
                (
                    "src.",
                    "domain.",
                    "application.education",
                    "app.domain",
                    "app.application.education",
                    "app.services.analytics",
                    "app.services.readiness",
                    "app.services.recommendation",
                )
            )
        }
        assert not forbidden

    def test_domain_learning_model_has_no_telemetry_fields(self):
        source = Path("app/models/learning.py").read_text(encoding="utf-8")
        assert "presentation_event" not in source.lower()
        assert "telemetry" not in source.lower()
        assert "analytics_event" not in source.lower()

    def test_alpha_blueprint_does_not_touch_education_os_packages(self):
        root = Path("app/alpha")
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "src.application.education" not in text
            assert "application.education" not in text


class TestFounderAlphaObservability:
    def test_founder_route_requires_auth(self, client, ctx):
        response = client.get("/console/alpha-observability")
        assert response.status_code in {302, 401, 403}
