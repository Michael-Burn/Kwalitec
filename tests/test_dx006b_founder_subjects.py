"""DX-006B Phase 2 — Founder Subjects catalogue tests."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from app.application.curriculum_studio.dto.workspace_snapshot import (
    WorkspaceSnapshot,
)
from app.founder.dashboard.services.founder_subjects_service import (
    STATUS_ARCHIVED,
    STATUS_PUBLISHED,
    STATUS_READY,
    STATUS_VALIDATION,
    FounderSubjectsService,
)
from tests.presentation.workflows.helpers import login_founder, wire_studio


@pytest.fixture
def founder_client(app, client, ctx):
    wire_studio(app, with_workspace=True)
    login_founder(client, app)
    return client


@dataclass
class _FakeAuthority:
    packages: tuple = ()

    def list_published(self, subject_code: str | None = None):
        return self.packages


@dataclass
class _FakePackage:
    subject_code: str
    version_label: str = "v1"
    published_at: str = "2026-07-01T00:00:00+00:00"
    is_active: bool = True


@dataclass
class _FakeStudio:
    workspaces: tuple[WorkspaceSnapshot, ...] = ()

    def list_workspaces(self):
        return self.workspaces

    def founder_dashboard(self, *, activity_limit: int = 20):
        @dataclass
        class _Dash:
            recent_activity: tuple = ()

        return _Dash()


def _ws(
    *,
    workspace_id: str,
    subject_code: str,
    stage: str,
    ready: bool = False,
    title: str = "",
    status: str = "active",
) -> WorkspaceSnapshot:
    return WorkspaceSnapshot(
        workspace_id=workspace_id,
        subject_code=subject_code,
        subject_title=title or subject_code,
        status=status,
        current_stage=stage,
        ready_to_publish=ready,
    )


def test_empty_catalogue(app):
    with app.test_request_context("/console/studio/subjects"):
        page = FounderSubjectsService(
            studio=_FakeStudio(),
            authority=_FakeAuthority(),
        ).build_page()
    assert page.is_empty_catalogue
    assert page.empty_reason == "No subjects yet."
    assert page.primary_label == "Create Subject"
    assert page.show_header_primary is False
    assert page.rows == ()


def test_catalogue_rows_and_default_sort(app):
    studio = _FakeStudio(
        workspaces=(
            _ws(
                workspace_id="ws-b",
                subject_code="B",
                stage="validation",
                title="Beta",
            ),
            _ws(
                workspace_id="ws-a",
                subject_code="A",
                stage="publication",
                ready=True,
                title="Alpha",
            ),
        )
    )
    with app.test_request_context("/console/studio/subjects"):
        page = FounderSubjectsService(
            studio=studio,
            authority=_FakeAuthority(),
        ).build_page()
    assert page.is_empty_catalogue is False
    assert page.show_header_primary is True
    assert len(page.rows) == 2
    assert all(r.workspace_href for r in page.rows)


def test_search_filters_name_and_code(app):
    studio = _FakeStudio(
        workspaces=(
            _ws(
                workspace_id="ws-1",
                subject_code="CS1",
                stage="subject",
                title="Financial",
            ),
            _ws(
                workspace_id="ws-2",
                subject_code="CS2",
                stage="subject",
                title="Valuation",
            ),
        )
    )
    with app.test_request_context("/console/studio/subjects"):
        page = FounderSubjectsService(
            studio=studio,
            authority=_FakeAuthority(),
        ).build_page(query="cs1")
    assert len(page.rows) == 1
    assert page.rows[0].code == "CS1"


def test_status_filter_validation(app):
    studio = _FakeStudio(
        workspaces=(
            _ws(workspace_id="ws-1", subject_code="A", stage="validation"),
            _ws(workspace_id="ws-2", subject_code="B", stage="approval"),
        )
    )
    with app.test_request_context("/console/studio/subjects"):
        page = FounderSubjectsService(
            studio=studio,
            authority=_FakeAuthority(),
        ).build_page(status=STATUS_VALIDATION)
    assert len(page.rows) == 1
    assert page.rows[0].code == "A"


def test_ready_and_published_filters(app):
    studio = _FakeStudio(
        workspaces=(
            _ws(workspace_id="ws-r", subject_code="R", stage="publication", ready=True),
            _ws(
                workspace_id="ws-p",
                subject_code="P",
                stage="publication",
                status="published",
            ),
            _ws(
                workspace_id="ws-a",
                subject_code="X",
                stage="subject",
                status="archived",
            ),
        )
    )
    authority = _FakeAuthority(packages=(_FakePackage(subject_code="P"),))
    with app.test_request_context("/console/studio/subjects"):
        svc = FounderSubjectsService(studio=studio, authority=authority)
        ready = svc.build_page(status=STATUS_READY)
        published = svc.build_page(status=STATUS_PUBLISHED)
        archived = svc.build_page(status=STATUS_ARCHIVED)
    assert {r.code for r in ready.rows} == {"R"}
    assert {r.code for r in published.rows} == {"P"}
    assert {r.code for r in archived.rows} == {"X"}


def test_zero_results_clear_query(app):
    studio = _FakeStudio(
        workspaces=(_ws(workspace_id="ws-1", subject_code="CS1", stage="subject"),)
    )
    with app.test_request_context("/console/studio/subjects"):
        page = FounderSubjectsService(
            studio=studio,
            authority=_FakeAuthority(),
        ).build_page(query="zzzz")
    assert page.is_zero_results
    assert page.empty_reason == "No matches."
    assert page.empty_action_label == "Clear query"
    assert page.show_header_primary is True


def test_subjects_route_catalogue_first(founder_client):
    response = founder_client.get("/console/studio/subjects")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "<h1" in html
    assert html.count('class="ds-page-header__title"') == 1 or html.count("<h1") == 1
    assert "Subjects" in html
    assert "Curriculum workflow" not in html
    assert "Open Curriculum Studio" not in html
    assert "Platform Summary" not in html
    assert "command-metric" not in html


def test_legacy_hubs_redirect_to_subjects(founder_client):
    for path, status in (
        ("/console/studio/review-queue", "validation"),
        ("/console/studio/publishing", "ready_to_publish"),
        ("/console/studio/quality", "validation"),
    ):
        response = founder_client.get(path, follow_redirects=False)
        assert response.status_code in {301, 302}
        loc = response.headers.get("Location", "")
        assert "/console/studio/subjects" in loc
        assert f"status={status}" in loc

    response = founder_client.get("/console/studio/versions", follow_redirects=False)
    assert response.status_code in {301, 302}
    assert "/console/studio/subjects" in response.headers.get("Location", "")
