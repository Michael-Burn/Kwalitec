"""FH-001 — Founder Feedback Hub aggregation tests."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from app.extensions import db
from app.models.user import User
from app.services.alpha_feedback_service import (
    KIND_REPORT_PROBLEM,
    AlphaFeedbackService,
)
from app.services.founder_feedback_hub import (
    SOURCE_ALPHA,
    SOURCE_PRIVATE_BETA,
    SOURCE_RESEARCH,
    FounderFeedbackHubService,
    HubFilters,
)
from app.services.private_beta.feedback_service import PrivateBetaFeedbackService
from app.services.research_feedback_service import (
    SOURCE_SETTINGS,
    ResearchFeedbackService,
)


def _make_user(email: str) -> User:
    user = User(email=email, is_active_user=True)
    user.set_password("password123")
    user.alpha_onboarding_completed = True
    db.session.add(user)
    db.session.commit()
    return user


def _login_founder(client, app) -> User:
    app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
    founder = _make_user("founder@kwalitec.example")
    client.post(
        "/auth/login",
        data={"email": founder.email, "password": "password123"},
        follow_redirects=True,
    )
    return founder


def _submit_beta(user_id: int, *, message: str = "Beta bug report unique"):
    return PrivateBetaFeedbackService.submit(
        user_id=user_id,
        category="bug",
        message=message,
        subject_code="0607",
    )


def _submit_alpha(user_id: int, *, message: str = "Alpha problem unique"):
    return AlphaFeedbackService.submit(
        user_id=user_id,
        kind=KIND_REPORT_PROBLEM,
        message=message,
    )


def _submit_research(user_id: int, *, free_text: str = "Check-in note unique"):
    result = ResearchFeedbackService.submit_checkin(
        user_id,
        experience_rating="Good",
        feature_helped_most="Dashboard",
        friction_area="Nothing",
        confidence_rating="High",
        return_intent="Probably",
        free_text=free_text,
        classification="Suggestion",
        submission_source=SOURCE_SETTINGS,
    )
    return result.submission


@pytest.mark.usefixtures("ctx")
class TestFounderFeedbackHubService:
    def test_aggregates_all_three_sources(self):
        student = _make_user("hub-student@kwalitec.example")
        beta = _submit_beta(student.id)
        alpha = _submit_alpha(student.id)
        research = _submit_research(student.id)
        assert beta.ok and alpha.ok and research is not None

        page = FounderFeedbackHubService().list_items()
        sources = {item.source for item in page.items}
        assert SOURCE_PRIVATE_BETA in sources
        assert SOURCE_ALPHA in sources
        assert SOURCE_RESEARCH in sources
        assert page.total == 3

        ids = [item.id for item in page.items]
        assert len(ids) == len(set(ids))

    def test_filter_by_source(self):
        student = _make_user("hub-source@kwalitec.example")
        _submit_beta(student.id)
        _submit_alpha(student.id)
        _submit_research(student.id)

        page = FounderFeedbackHubService().list_items(
            HubFilters(source=SOURCE_PRIVATE_BETA)
        )
        assert page.total == 1
        assert page.items[0].source == SOURCE_PRIVATE_BETA
        assert page.items[0].source_label == "PRIVATE BETA"
        assert page.items[0].origin_colour == "blue"

    def test_filter_by_severity(self):
        student = _make_user("hub-sev@kwalitec.example")
        _submit_beta(student.id, message="critical data loss on save")
        _submit_alpha(student.id)
        _submit_research(student.id)

        page = FounderFeedbackHubService().list_items(
            HubFilters(severity="critical")
        )
        assert page.total >= 1
        assert all(item.severity == "critical" for item in page.items)
        assert all(item.source == SOURCE_PRIVATE_BETA for item in page.items)

    def test_filter_by_status(self):
        student = _make_user("hub-status@kwalitec.example")
        _submit_beta(student.id)
        _submit_alpha(student.id)
        _submit_research(student.id)

        page = FounderFeedbackHubService().list_items(HubFilters(status="new"))
        assert page.total == 3

    def test_keyword_search(self):
        student = _make_user("hub-kw@kwalitec.example")
        _submit_beta(student.id, message="zebra-stripe layout broken")
        _submit_alpha(student.id, message="ordinary alpha note")
        _submit_research(student.id, free_text="ordinary checkin")

        page = FounderFeedbackHubService().list_items(
            HubFilters(keyword="zebra-stripe")
        )
        assert page.total == 1
        assert "zebra-stripe" in (page.items[0].message or "")

    def test_sort_newest_first(self):
        student = _make_user("hub-sort@kwalitec.example")
        older = _submit_beta(student.id, message="older beta")
        newer = _submit_alpha(student.id, message="newer alpha")
        assert older.ok and newer.ok

        from app.models.private_beta import PrivateBetaFeedback

        row = db.session.get(PrivateBetaFeedback, older.feedback_id)
        assert row is not None
        row.created_at = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=2)
        db.session.commit()

        page = FounderFeedbackHubService().list_items()
        assert page.items[0].source == SOURCE_ALPHA
        assert page.items[-1].source == SOURCE_PRIVATE_BETA

    def test_pagination(self):
        student = _make_user("hub-page@kwalitec.example")
        for i in range(5):
            _submit_beta(student.id, message=f"beta page item {i}")

        page1 = FounderFeedbackHubService().list_items(page=1, per_page=2)
        page2 = FounderFeedbackHubService().list_items(page=2, per_page=2)
        assert page1.total == 5
        assert len(page1.items) == 2
        assert len(page2.items) == 2
        assert page1.items[0].id != page2.items[0].id
        assert page1.has_next is True
        assert page2.has_prev is True

    def test_open_links_route_to_specialists(self):
        student = _make_user("hub-open@kwalitec.example")
        beta = _submit_beta(student.id)
        alpha = _submit_alpha(student.id)
        research = _submit_research(student.id)

        page = FounderFeedbackHubService().list_items()
        by_source = {item.source: item for item in page.items}
        assert (
            f"/console/beta?feedback_id={beta.feedback_id}"
            in by_source[SOURCE_PRIVATE_BETA].link_to_original
        )
        assert (
            f"/console/alpha-observability?feedback_id={alpha.submission_id}"
            in by_source[SOURCE_ALPHA].link_to_original
        )
        assert (
            f"/console/feedback/checkins?submission={research.id}"
            in by_source[SOURCE_RESEARCH].link_to_original
        )

    def test_null_fields_not_fabricated_for_alpha(self):
        student = _make_user("hub-null@kwalitec.example")
        _submit_alpha(student.id)
        page = FounderFeedbackHubService().list_items(
            HubFilters(source=SOURCE_ALPHA)
        )
        item = page.items[0]
        assert item.severity is None
        assert item.subject is None
        assert item.updated_at is None


@pytest.mark.usefixtures("ctx")
class TestFounderFeedbackHubHttp:
    def test_hub_landing_shows_all_sources(self, client, app):
        _login_founder(client, app)
        student = _make_user("hub-http@kwalitec.example")
        _submit_beta(student.id, message="http beta visible")
        _submit_alpha(student.id, message="http alpha visible")
        _submit_research(student.id, free_text="http research visible")

        response = client.get("/console/feedback")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert 'data-fh001-feedback-hub="1"' in body
        assert "PRIVATE BETA" in body
        assert "ALPHA" in body
        assert "PRODUCT CHECK-IN" in body
        assert "http beta visible" in body
        assert "http alpha visible" in body
        assert "http research visible" in body

    def test_hub_source_filter_http(self, client, app):
        _login_founder(client, app)
        student = _make_user("hub-http-src@kwalitec.example")
        _submit_beta(student.id, message="only-beta-marker")
        _submit_alpha(student.id, message="only-alpha-marker")

        response = client.get(
            "/console/feedback",
            query_string={"source": "private_beta"},
        )
        body = response.get_data(as_text=True)
        assert "only-beta-marker" in body
        assert "only-alpha-marker" not in body

    def test_open_links_present(self, client, app):
        _login_founder(client, app)
        student = _make_user("hub-http-open@kwalitec.example")
        beta = _submit_beta(student.id)
        response = client.get("/console/feedback")
        body = response.get_data(as_text=True)
        assert f"/console/beta?feedback_id={beta.feedback_id}" in body
        assert 'data-fh001-open="1"' in body

    def test_specialist_pages_still_work(self, client, app):
        _login_founder(client, app)
        student = _make_user("hub-spec@kwalitec.example")
        _submit_beta(student.id)
        _submit_alpha(student.id)
        research = _submit_research(student.id)

        assert client.get("/console/beta").status_code == 200
        assert client.get("/console/alpha-observability").status_code == 200
        checkins = client.get("/console/feedback/checkins")
        assert checkins.status_code == 200
        body = checkins.get_data(as_text=True)
        assert 'data-rip003-command-centre="1"' in body
        assert f"#{research.id}" in body

    def test_hub_is_read_only_get(self, client, app):
        _login_founder(client, app)
        response = client.post("/console/feedback", data={"action": "accept"})
        assert response.status_code == 405
