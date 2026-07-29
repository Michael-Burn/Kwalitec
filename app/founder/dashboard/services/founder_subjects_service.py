"""Founder Subjects catalogue service — DX-004B Catalogue First.

Presentation projection only. Does not alter publication or curriculum rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from urllib.parse import urlencode

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
from app.founder.dashboard.dto.founder_subjects import (
    FilterOption,
    FounderSubjectsPage,
    SubjectCatalogueRow,
)
from app.presentation.curriculum_studio.factory import get_studio_service

# DX-004B / mission Status filter vocabulary.
STATUS_ALL = "all"
STATUS_DRAFT = "draft"
STATUS_VALIDATION = "validation"
STATUS_APPROVAL = "approval"
STATUS_READY = "ready_to_publish"
STATUS_PUBLISHED = "published"
STATUS_ARCHIVED = "archived"
STATUS_IN_PROGRESS = "in_progress"
STATUS_RECENT = "recently_updated"

SORT_RECENT_ACTIVE = "recent_active"
SORT_ALPHA = "alphabetical"
SORT_RECENT_PUBLISHED = "recent_published"
SORT_RECENT_CREATED = "recent_created"

_STATUS_OPTIONS: tuple[FilterOption, ...] = (
    FilterOption(STATUS_ALL, "All"),
    FilterOption(STATUS_DRAFT, "Draft"),
    FilterOption(STATUS_VALIDATION, "Validation"),
    FilterOption(STATUS_APPROVAL, "Approval"),
    FilterOption(STATUS_READY, "Ready to publish"),
    FilterOption(STATUS_PUBLISHED, "Published"),
    FilterOption(STATUS_ARCHIVED, "Archived"),
    FilterOption(STATUS_IN_PROGRESS, "In progress"),
    FilterOption(STATUS_RECENT, "Recently updated"),
)

_SORT_OPTIONS: tuple[FilterOption, ...] = (
    FilterOption(SORT_RECENT_ACTIVE, "Most recently active"),
    FilterOption(SORT_ALPHA, "Alphabetical"),
    FilterOption(SORT_RECENT_PUBLISHED, "Recently published"),
    FilterOption(SORT_RECENT_CREATED, "Recently created"),
)

_EMPTY_CATALOGUE_REASON = "No subjects yet."
_EMPTY_MATCHES_REASON = "No matches."
_EMPTY_FILTERS_REASON = "No subjects match."
_CREATE_LABEL = "Create Subject"
_CLEAR_QUERY_LABEL = "Clear query"
_CLEAR_FILTERS_LABEL = "Clear filters"

_RECENT_WINDOW = timedelta(days=7)


@dataclass(frozen=True)
class _RowCandidate:
    row: SubjectCatalogueRow
    workspace: WorkspaceSnapshot


class FounderSubjectsService:
    """Build the Founder Subjects catalogue from Studio + published packages."""

    def __init__(
        self,
        *,
        studio: CurriculumStudioService | None = None,
        authority: PublishedCurriculumAuthority | None = None,
    ) -> None:
        self._studio = studio
        self._authority = authority or PublishedCurriculumAuthority()

    def build_page(
        self,
        *,
        query: str = "",
        status: str = STATUS_ALL,
        sort: str = SORT_RECENT_ACTIVE,
        create: bool = False,
    ) -> FounderSubjectsPage:
        """Assemble L0 catalogue + L1 search/filter state."""
        studio = self._studio or get_studio_service()
        q = (query or "").strip()
        status_key = (status or STATUS_ALL).strip().lower() or STATUS_ALL
        sort_key = (sort or SORT_RECENT_ACTIVE).strip().lower() or SORT_RECENT_ACTIVE
        if status_key not in {o.value for o in _STATUS_OPTIONS}:
            status_key = STATUS_ALL
        if sort_key not in {o.value for o in _SORT_OPTIONS}:
            sort_key = SORT_RECENT_ACTIVE

        activity = self._activity_rank(studio)
        published = self._published_map()
        candidates = [
            self._candidate(ws, activity=activity, published=published)
            for ws in studio.list_workspaces()
        ]
        catalogue_empty = len(candidates) == 0
        filtered = self._apply_status(candidates, status_key)
        filtered = self._apply_query(filtered, q)
        ordered = self._apply_sort(filtered, sort_key)
        rows = tuple(c.row for c in ordered)

        create_href = self._subjects_url(create=True)
        clear_query_href = self._subjects_url(status=status_key, sort=sort_key)
        clear_filters_href = self._subjects_url(query=q, sort=sort_key)

        zero_results = (not catalogue_empty) and len(rows) == 0
        show_create_form = bool(create)

        if show_create_form:
            empty_reason = ""
            empty_action_label = ""
            empty_action_href = ""
            show_header_primary = False
            primary_href = create_href
        elif catalogue_empty:
            empty_reason = _EMPTY_CATALOGUE_REASON
            empty_action_label = _CREATE_LABEL
            empty_action_href = create_href
            show_header_primary = False
            primary_href = create_href
        elif zero_results and q:
            empty_reason = _EMPTY_MATCHES_REASON
            empty_action_label = _CLEAR_QUERY_LABEL
            empty_action_href = clear_query_href
            show_header_primary = True
            primary_href = create_href
        elif zero_results:
            empty_reason = (
                "No archived subjects."
                if status_key == STATUS_ARCHIVED
                else _EMPTY_FILTERS_REASON
            )
            empty_action_label = _CLEAR_FILTERS_LABEL
            empty_action_href = clear_filters_href
            show_header_primary = True
            primary_href = create_href
        else:
            empty_reason = ""
            empty_action_label = ""
            empty_action_href = ""
            show_header_primary = True
            primary_href = create_href

        return FounderSubjectsPage(
            page_title="Subjects",
            rows=rows,
            query=q,
            status=status_key,
            sort=sort_key,
            status_options=_STATUS_OPTIONS,
            sort_options=_SORT_OPTIONS,
            create_href=create_href,
            clear_query_href=clear_query_href,
            clear_filters_href=clear_filters_href,
            is_empty_catalogue=catalogue_empty,
            is_zero_results=zero_results,
            empty_reason=empty_reason,
            empty_action_label=empty_action_label,
            empty_action_href=empty_action_href,
            show_create_form=show_create_form,
            primary_label=_CREATE_LABEL,
            primary_href=primary_href,
            show_header_primary=show_header_primary,
        )

    def _published_map(self) -> dict[str, object]:
        return {
            p.subject_code.strip().upper(): p
            for p in self._authority.list_published()
            if p.is_active
        }

    def _candidate(
        self,
        workspace: WorkspaceSnapshot,
        *,
        activity: dict[str, str],
        published: dict[str, object],
    ) -> _RowCandidate:
        code = (workspace.subject_code or "").strip().upper()
        name = self._subject_display(workspace)
        stage = self._stage_display(workspace)
        pub_status = self._publication_status(workspace, published.get(code))
        updated_at = activity.get(workspace.workspace_id, "")
        created_at = updated_at  # Alpha: no separate created_at on workspace DTO
        pkg = published.get(code)
        published_at = ""
        if pkg is not None:
            published_at = (getattr(pkg, "published_at", None) or "").strip()
        keys = self._filter_keys(workspace, pub_status, updated_at)
        row = SubjectCatalogueRow(
            subject_id=workspace.workspace_id,
            name=name,
            code=code,
            stage_label=stage,
            publication_status=pub_status,
            updated_label=self._relative_updated(updated_at),
            updated_at=updated_at or "0000",
            created_at=created_at or "0000",
            published_at=published_at,
            workspace_href=url_for(
                "curriculum_studio.workspace",
                workspace_id=workspace.workspace_id,
            ),
            status_filter_keys=keys,
        )
        return _RowCandidate(row=row, workspace=workspace)

    def _filter_keys(
        self,
        workspace: WorkspaceSnapshot,
        publication_status: str,
        updated_at: str,
    ) -> tuple[str, ...]:
        keys: list[str] = [STATUS_ALL]
        status_token = (workspace.status or "").strip().lower()
        if status_token == "archived":
            keys.append(STATUS_ARCHIVED)
        if status_token == "published" or publication_status == "Published":
            keys.append(STATUS_PUBLISHED)
        if workspace.ready_to_publish or publication_status == "Ready to publish":
            keys.append(STATUS_READY)
        stage = resolve_workflow_stage(workspace.current_stage)
        if stage is WorkflowStage.VALIDATION:
            keys.append(STATUS_VALIDATION)
        if stage in {WorkflowStage.APPROVAL, WorkflowStage.PREVIEW}:
            keys.append(STATUS_APPROVAL)
        if stage in {WorkflowStage.SUBJECT, WorkflowStage.CONTENT_SOURCES}:
            keys.append(STATUS_DRAFT)
        if status_token not in {"archived", "abandoned"} and (
            publication_status in {"In progress", "Ready to publish"}
            or status_token == "active"
        ):
            if publication_status != "Published":
                keys.append(STATUS_IN_PROGRESS)
        if self._is_recent(updated_at):
            keys.append(STATUS_RECENT)
        return tuple(dict.fromkeys(keys))

    @staticmethod
    def _apply_status(
        candidates: list[_RowCandidate],
        status_key: str,
    ) -> list[_RowCandidate]:
        if status_key == STATUS_ALL:
            return [
                c
                for c in candidates
                if (c.workspace.status or "").strip().lower() != "abandoned"
            ]
        return [
            c
            for c in candidates
            if status_key in c.row.status_filter_keys
            and (
                status_key == STATUS_ARCHIVED
                or (c.workspace.status or "").strip().lower() != "abandoned"
            )
        ]

    @staticmethod
    def _apply_query(
        candidates: list[_RowCandidate],
        query: str,
    ) -> list[_RowCandidate]:
        if not query:
            return candidates
        token = query.casefold()
        out: list[_RowCandidate] = []
        for c in candidates:
            haystacks = (
                c.row.name,
                c.row.code,
                c.row.publication_status,
                c.row.stage_label,
            )
            if any(token in (h or "").casefold() for h in haystacks):
                out.append(c)
        return out

    @staticmethod
    def _apply_sort(
        candidates: list[_RowCandidate],
        sort_key: str,
    ) -> list[_RowCandidate]:
        if sort_key == SORT_ALPHA:
            return sorted(candidates, key=lambda c: c.row.name.casefold())
        if sort_key == SORT_RECENT_PUBLISHED:
            return sorted(
                candidates,
                key=lambda c: (c.row.published_at or "", c.row.name.casefold()),
                reverse=True,
            )
        if sort_key == SORT_RECENT_CREATED:
            return sorted(
                candidates,
                key=lambda c: (c.row.created_at, c.row.name.casefold()),
                reverse=True,
            )
        # Default: most recently active
        return sorted(
            candidates,
            key=lambda c: (c.row.updated_at, c.row.name.casefold()),
            reverse=True,
        )

    def _activity_rank(self, studio: CurriculumStudioService) -> dict[str, str]:
        rank: dict[str, str] = {}
        try:
            dash = studio.founder_dashboard(activity_limit=100)
        except Exception:  # noqa: BLE001 — catalogue must render without activity
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
    def _publication_status(workspace: WorkspaceSnapshot, package) -> str:
        status_token = (workspace.status or "").strip().lower()
        if status_token == "archived":
            return "Archived"
        if status_token == "published" or package is not None:
            return "Published"
        if workspace.ready_to_publish:
            return "Ready to publish"
        stage = resolve_workflow_stage(workspace.current_stage)
        if stage is WorkflowStage.PUBLICATION:
            return "Ready to publish"
        return "In progress"

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
    def _relative_updated(raw: str) -> str:
        token = (raw or "").strip()
        if not token or token == "0000":
            return "—"
        try:
            parsed = datetime.fromisoformat(token.replace("Z", "+00:00"))
        except ValueError:
            return token[:10]
        now = datetime.now(tz=parsed.tzinfo or UTC)
        if parsed.tzinfo is None:
            now = datetime.now()
        delta = now - parsed
        seconds = int(delta.total_seconds())
        if seconds < 0:
            return "Just now"
        if seconds < 60:
            return "Just now"
        if seconds < 3600:
            mins = seconds // 60
            return f"{mins}m ago"
        if seconds < 86400:
            hours = seconds // 3600
            return f"{hours}h ago"
        if seconds < 172800:
            return "Yesterday"
        days = seconds // 86400
        if days < 14:
            return f"{days} days ago"
        return f"{parsed.day} {parsed.strftime('%b')}"

    @staticmethod
    def _is_recent(raw: str) -> bool:
        token = (raw or "").strip()
        if not token or token == "0000":
            return False
        try:
            parsed = datetime.fromisoformat(token.replace("Z", "+00:00"))
        except ValueError:
            return False
        now = datetime.now(tz=parsed.tzinfo or UTC)
        if parsed.tzinfo is None:
            now = datetime.now()
        return (now - parsed) <= _RECENT_WINDOW

    @staticmethod
    def _subjects_url(
        *,
        query: str = "",
        status: str = STATUS_ALL,
        sort: str = SORT_RECENT_ACTIVE,
        create: bool = False,
    ) -> str:
        params: dict[str, str] = {}
        if query:
            params["q"] = query
        if status and status != STATUS_ALL:
            params["status"] = status
        if sort and sort != SORT_RECENT_ACTIVE:
            params["sort"] = sort
        if create:
            params["create"] = "1"
        base = url_for("curriculum_studio.subjects_hub")
        if not params:
            return base
        return f"{base}?{urlencode(params)}"
