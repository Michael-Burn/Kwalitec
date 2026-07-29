"""Founder Home service — publication-centred Current Work / Queue / Recent.

Authority: DX-004A Founder Home Architecture.
Presentation projection only. Does not alter publication or curriculum rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from flask import url_for

from app.application.curriculum_studio.curriculum_studio_service import (
    CurriculumStudioService,
)
from app.application.curriculum_studio.dto.workspace_snapshot import (
    WorkspaceSnapshot,
)
from app.application.curriculum_studio_foundation.authority import (
    PublishedCurriculumAuthority,
)
from app.domain.curriculum_studio.workflow_stage import (
    WorkflowStage,
    resolve_workflow_stage,
)
from app.founder.dashboard.dto.founder_home import (
    FounderHomePage,
    HomeCurrentWork,
    HomeQueueRow,
)
from app.presentation.curriculum_studio.factory import get_studio_service

# DX-004A L1 operator status vocabulary (ordered for queue priority).
STATUS_READY_TO_PUBLISH = "Ready to Publish"
STATUS_AWAITING_APPROVAL = "Awaiting Approval"
STATUS_AWAITING_VALIDATION = "Awaiting Validation"
STATUS_INCOMPLETE = "Incomplete"

_QUEUE_PRIORITY: dict[str, int] = {
    STATUS_READY_TO_PUBLISH: 0,
    STATUS_AWAITING_APPROVAL: 1,
    STATUS_AWAITING_VALIDATION: 2,
    STATUS_INCOMPLETE: 3,
}

_QUEUE_VISIBLE_MAX = 7
_RECENT_MAX = 5

_EMPTY_TITLE = "No subjects have been created yet."
_EMPTY_REASON = "Create your first subject to begin building your curriculum."
_EMPTY_ACTION_LABEL = "Create Subject"


@dataclass(frozen=True)
class _QueueCandidate:
    workspace: WorkspaceSnapshot
    status_label: str
    recency_key: str
    href: str


class FounderHomeService:
    """Build the Founder Home page from Curriculum Studio + published packages."""

    def __init__(
        self,
        *,
        studio: CurriculumStudioService | None = None,
        authority: PublishedCurriculumAuthority | None = None,
    ) -> None:
        self._studio = studio
        self._authority = authority or PublishedCurriculumAuthority()

    def build_home(self) -> FounderHomePage:
        """Assemble L0 Current Work, L1 Queue, and L2 Recent Publications."""
        studio = self._studio or get_studio_service()
        subjects_href = url_for("curriculum_studio.subjects_hub")
        workspaces = [
            ws
            for ws in studio.list_workspaces()
            if (ws.status or "").strip().lower()
            not in {"published", "archived", "abandoned"}
        ]
        activity_rank = self._activity_rank(studio)
        candidates = [
            self._candidate(ws, activity_rank=activity_rank) for ws in workspaces
        ]
        queue_sorted = self._order_queue(candidates)
        queue_truncated = len(queue_sorted) > _QUEUE_VISIBLE_MAX
        visible_queue = queue_sorted[:_QUEUE_VISIBLE_MAX]
        queue_rows = tuple(
            HomeQueueRow(
                title=self._subject_display(c.workspace),
                status_label=c.status_label,
                href=c.href,
            )
            for c in visible_queue
        )
        current = self._select_current_work(queue_sorted)
        recent = self._recent_publications()
        return FounderHomePage(
            current_work=current,
            queue=queue_rows,
            recent_publications=recent,
            queue_truncated=queue_truncated,
            empty_title=_EMPTY_TITLE,
            empty_reason=_EMPTY_REASON,
            empty_action_label=_EMPTY_ACTION_LABEL,
            empty_action_href=subjects_href,
            subjects_href=subjects_href,
        )

    @staticmethod
    def _order_queue(candidates: list[_QueueCandidate]) -> list[_QueueCandidate]:
        """Order: Ready → Approval → Validation → Incomplete; then most recent."""
        bands: dict[int, list[_QueueCandidate]] = {}
        for candidate in candidates:
            pri = _QUEUE_PRIORITY.get(candidate.status_label, 99)
            bands.setdefault(pri, []).append(candidate)
        ordered: list[_QueueCandidate] = []
        for pri in sorted(bands):
            band = sorted(
                bands[pri],
                key=lambda c: (c.recency_key, c.workspace.subject_code.lower()),
                reverse=True,
            )
            ordered.extend(band)
        return ordered

    def _select_current_work(
        self,
        ordered: list[_QueueCandidate],
    ) -> HomeCurrentWork | None:
        """Selection: most recently active incomplete, else highest-priority queue."""
        if not ordered:
            return None
        with_activity = [c for c in ordered if c.recency_key != "0000"]
        chosen = (
            max(with_activity, key=lambda c: c.recency_key)
            if with_activity
            else ordered[0]
        )
        return HomeCurrentWork(
            subject_name=self._subject_display(chosen.workspace),
            stage_label=self._stage_display(chosen.workspace),
            primary_label=self._primary_label(chosen.status_label),
            primary_href=chosen.href,
        )

    def _recent_publications(self) -> tuple[HomeQueueRow, ...]:
        packages = [p for p in self._authority.list_published() if p.is_active]
        packages.sort(
            key=lambda p: (p.published_at or "", p.subject_code),
            reverse=True,
        )
        rows: list[HomeQueueRow] = []
        for pkg in packages[:_RECENT_MAX]:
            date_label = self._format_published_date(pkg.published_at)
            rows.append(
                HomeQueueRow(
                    title=pkg.subject_code,
                    meta_label=(
                        f"Published {date_label}" if date_label else "Published"
                    ),
                    href=url_for("curriculum_studio.subjects_hub"),
                )
            )
        return tuple(rows)

    def _candidate(
        self,
        workspace: WorkspaceSnapshot,
        *,
        activity_rank: dict[str, str],
    ) -> _QueueCandidate:
        return _QueueCandidate(
            workspace=workspace,
            status_label=self._operator_status(workspace),
            recency_key=activity_rank.get(workspace.workspace_id, "0000"),
            href=url_for(
                "curriculum_studio.workspace",
                workspace_id=workspace.workspace_id,
            ),
        )

    def _activity_rank(self, studio: CurriculumStudioService) -> dict[str, str]:
        """Map workspace_id → latest activity timestamp (lexicographic)."""
        rank: dict[str, str] = {}
        try:
            dash = studio.founder_dashboard(activity_limit=50)
        except Exception:  # noqa: BLE001 — Home must render without activity
            return rank
        for entry in dash.recent_activity:
            wid = (entry.workspace_id or "").strip()
            if not wid:
                continue
            stamp = (entry.occurred_at or "").strip() or "0000"
            if stamp >= rank.get(wid, ""):
                rank[wid] = stamp
        return rank

    @staticmethod
    def _operator_status(workspace: WorkspaceSnapshot) -> str:
        if workspace.ready_to_publish:
            return STATUS_READY_TO_PUBLISH
        stage = resolve_workflow_stage(workspace.current_stage)
        if stage is WorkflowStage.PUBLICATION:
            return STATUS_READY_TO_PUBLISH
        if stage in {WorkflowStage.APPROVAL, WorkflowStage.PREVIEW}:
            return STATUS_AWAITING_APPROVAL
        if stage is WorkflowStage.VALIDATION:
            return STATUS_AWAITING_VALIDATION
        return STATUS_INCOMPLETE

    @staticmethod
    def _primary_label(status_label: str) -> str:
        if status_label == STATUS_READY_TO_PUBLISH:
            return "Publish"
        if status_label == STATUS_AWAITING_APPROVAL:
            return "Approve"
        if status_label == STATUS_AWAITING_VALIDATION:
            return "Validate"
        return "Resume Publication"

    @staticmethod
    def _subject_display(workspace: WorkspaceSnapshot) -> str:
        title = (workspace.subject_title or "").strip()
        if title:
            return title
        return (workspace.subject_code or workspace.workspace_id).strip()

    @staticmethod
    def _stage_display(workspace: WorkspaceSnapshot) -> str:
        from app.presentation.curriculum_studio.founder_stages import (
            founder_stage_label,
        )

        try:
            return founder_stage_label(workspace.current_stage)
        except ValueError:
            return (workspace.current_stage or "Upload").replace("_", " ").title()

    @staticmethod
    def _format_published_date(raw: str) -> str:
        token = (raw or "").strip()
        if not token:
            return ""
        try:
            parsed = datetime.fromisoformat(token.replace("Z", "+00:00"))
            return f"{parsed.day} {parsed.strftime('%b')}"
        except ValueError:
            return token[:10]
