"""DX-006B Phase 1 — Founder Home service unit tests."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.curriculum_studio.dto.workspace_snapshot import (
    WorkspaceSnapshot,
)
from app.founder.dashboard.services.founder_home_service import (
    STATUS_AWAITING_APPROVAL,
    STATUS_AWAITING_VALIDATION,
    STATUS_INCOMPLETE,
    STATUS_READY_TO_PUBLISH,
    FounderHomeService,
)


@dataclass
class _FakeAuthority:
    packages: tuple = ()

    def list_published(self, subject_code: str | None = None):
        return self.packages


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


def test_empty_home(app):
    with app.test_request_context("/console/"):
        page = FounderHomeService(
            studio=_FakeStudio(),
            authority=_FakeAuthority(),
        ).build_home()
    assert page.current_work is None
    assert page.queue == ()
    assert page.recent_publications == ()
    assert page.empty_title == "No subjects have been created yet."
    assert "Create your first subject" in page.empty_reason
    assert page.empty_action_label == "Create Subject"


def test_queue_priority_and_primary(app):
    studio = _FakeStudio(
        workspaces=(
            _ws(workspace_id="ws-a", subject_code="A", stage="subject"),
            _ws(workspace_id="ws-b", subject_code="B", stage="validation"),
            _ws(
                workspace_id="ws-c",
                subject_code="C",
                stage="publication",
                ready=True,
            ),
            _ws(workspace_id="ws-d", subject_code="D", stage="approval"),
        )
    )
    with app.test_request_context("/console/"):
        page = FounderHomeService(
            studio=studio,
            authority=_FakeAuthority(),
        ).build_home()
    assert [r.status_label for r in page.queue] == [
        STATUS_READY_TO_PUBLISH,
        STATUS_AWAITING_APPROVAL,
        STATUS_AWAITING_VALIDATION,
        STATUS_INCOMPLETE,
    ]
    assert page.current_work is not None
    assert page.current_work.primary_label == "Publish"
    assert page.current_work.subject_name == "C"


def test_published_workspaces_excluded_from_queue(app):
    studio = _FakeStudio(
        workspaces=(
            _ws(
                workspace_id="ws-p",
                subject_code="P",
                stage="publication",
                ready=True,
                status="published",
            ),
        )
    )
    with app.test_request_context("/console/"):
        page = FounderHomeService(
            studio=studio,
            authority=_FakeAuthority(),
        ).build_home()
    assert page.queue == ()
    assert page.current_work is None
