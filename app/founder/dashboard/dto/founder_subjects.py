"""Founder Subjects catalogue DTO — DX-004B object permanence projection."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SubjectCatalogueRow:
    """One Subject in the operator catalogue (L0 / L2)."""

    subject_id: str
    name: str
    code: str
    stage_label: str
    publication_status: str
    updated_label: str
    updated_at: str
    created_at: str
    published_at: str
    workspace_href: str
    status_filter_keys: tuple[str, ...]


@dataclass(frozen=True)
class FilterOption:
    """Quiet select option for Status or Sort."""

    value: str
    label: str


@dataclass(frozen=True)
class FounderSubjectsPage:
    """Subjects catalogue page model — presentation only."""

    page_title: str
    rows: tuple[SubjectCatalogueRow, ...]
    query: str
    status: str
    sort: str
    status_options: tuple[FilterOption, ...]
    sort_options: tuple[FilterOption, ...]
    create_href: str
    clear_query_href: str
    clear_filters_href: str
    is_empty_catalogue: bool
    is_zero_results: bool
    empty_reason: str
    empty_action_label: str
    empty_action_href: str
    show_create_form: bool
    primary_label: str
    primary_href: str
    show_header_primary: bool
