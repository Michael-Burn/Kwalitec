"""Shared helpers for Curriculum Studio Founder UX presentation tests."""

from __future__ import annotations

from app.application.curriculum_studio.dto.dashboard_snapshot import (
    ActivityEntrySnapshot,
    DashboardSnapshot,
)
from app.application.curriculum_studio.dto.workspace_snapshot import WorkspaceSnapshot
from app.extensions import db
from app.models.user import User
from app.presentation.curriculum_studio.factory import set_studio_service
from tests.application.curriculum_studio.helpers import (
    make_studio_with_ports,
    seed_workspace,
)

FOUNDER_EMAIL = "founder@kwalitec.example"

STUDIO_TEMPLATE_MARKERS = (
    "founder_dashboard/base.html",
    "founder-breadcrumb",
    "founder-next-action",
    "founder-empty-state",
    "founder-required",
    "btn-primary",
)

FORBIDDEN_FOUNDER_COPY = (
    "execute publish",
    "validation passed.",
    "run publish",
    "force publish",
)


def make_workspace(
    *,
    workspace_id: str = "ws-cs1",
    subject_code: str = "CS1",
    subject_title: str = "Core Statistics",
    current_stage: str = "subject",
    version_label: str = "",
    status: str = "active",
) -> WorkspaceSnapshot:
    return WorkspaceSnapshot(
        workspace_id=workspace_id,
        subject_code=subject_code,
        subject_title=subject_title,
        version_label=version_label,
        status=status,
        current_stage=current_stage,
    )


def make_empty_dashboard() -> DashboardSnapshot:
    return DashboardSnapshot()


def make_populated_dashboard() -> DashboardSnapshot:
    ws = make_workspace(current_stage="validation")
    return DashboardSnapshot(
        draft_curricula=(ws,),
        draft_count=1,
        pending_validation_count=1,
        pending_validation=(ws,),
        recent_activity=(
            ActivityEntrySnapshot(
                activity_id="a1",
                kind="validation",
                message="We've completed validation successfully.",
            ),
        ),
    )


def make_founder_user() -> User:
    user = User(email=FOUNDER_EMAIL, is_active_user=True)
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


def login_founder(client, app) -> User:
    app.config["FOUNDER_EMAILS"] = FOUNDER_EMAIL
    founder = make_founder_user()
    client.post(
        "/auth/login",
        data={"email": founder.email, "password": "password123"},
        follow_redirects=True,
    )
    return founder


def wire_studio(app, *, with_workspace: bool = False):
    studio, _, _, _ = make_studio_with_ports()
    if with_workspace:
        seed_workspace(studio, workspace_id="ws-cs1", subject_code="CS1")
    set_studio_service(studio, app=app)
    return studio
