"""Choose Exam discovery projection (DX-005B / DX-006B Phase 5).

Maps SubjectCatalogueService entries into a discovery DTO.
No educational authority — presentation only.
"""

from __future__ import annotations

from app.application.platform_integration.subject_catalogue import (
    CatalogueAvailability,
    SubjectCatalogueEntry,
    SubjectCatalogueService,
)
from app.presentation.student.dto.choose_exam import (
    ChooseExamFilterOption,
    ChooseExamPage,
    ExamOfferingRow,
    SelectedExamSummary,
)

_STATUS_OPTIONS = (
    ChooseExamFilterOption("all", "All"),
    ChooseExamFilterOption("ready", "Ready"),
    ChooseExamFilterOption("coming_soon", "Coming Soon"),
)

_SORT_OPTIONS = (
    ChooseExamFilterOption("updated", "Recently updated"),
    ChooseExamFilterOption("alpha", "Alphabetical"),
)

_EMPTY_FAMILY = (ChooseExamFilterOption("all", "All"),)

_SOON_LINE = (
    "This subject’s verified curriculum is still under preparation. "
    "You cannot start studying this exam yet."
)


class ChooseExamService:
    """Build the Choose Exam discovery page model."""

    def __init__(
        self, catalogue: SubjectCatalogueService | None = None
    ) -> None:
        self._catalogue = catalogue or SubjectCatalogueService()

    def build(
        self,
        *,
        selected_key: str = "",
        query: str = "",
        status_filter: str = "all",
        sort: str = "updated",
        family_filter: str = "all",
    ) -> ChooseExamPage:
        entries = self._catalogue.list_entries(include_coming_soon=True)
        ready_all = [
            self._to_row(e)
            for e in entries
            if e.availability is CatalogueAvailability.READY
        ]
        soon_all = [
            self._to_row(e)
            for e in entries
            if e.availability is CatalogueAvailability.COMING_SOON
        ]

        status = (status_filter or "all").strip().lower()
        if status not in {"all", "ready", "coming_soon"}:
            status = "all"
        sort_key = (sort or "updated").strip().lower()
        if sort_key not in {"updated", "alpha"}:
            sort_key = "updated"
        family = (family_filter or "all").strip()
        q = (query or "").strip().lower()

        ready = self._filter_rows(ready_all, q=q, family=family)
        soon = self._filter_rows(soon_all, q=q, family=family)

        if status == "ready":
            soon = []
        elif status == "coming_soon":
            ready = []

        ready = self._sort_ready(ready, sort_key)
        soon = sorted(soon, key=lambda r: r.title.lower())

        families = self._family_options(ready_all + soon_all)
        selected = (selected_key or "").strip()
        selected_row = next(
            (r for r in ready_all if r.subject_key == selected and r.selectable),
            None,
        )
        summary = (
            self._summary_for(selected_row) if selected_row is not None else None
        )

        empty_ready = not ready_all
        zero_matches = bool(q or status != "all" or family != "all") and not (
            ready or soon
        )

        return ChooseExamPage(
            ready_offerings=tuple(ready),
            coming_soon=tuple(soon),
            selected_key=selected if selected_row is not None else "",
            selected_summary=summary,
            query=query or "",
            status_filter=status,
            sort=sort_key,
            family_filter=family if any(f.value == family for f in families) else "all",
            status_options=_STATUS_OPTIONS,
            sort_options=_SORT_OPTIONS,
            family_options=families,
            primary_enabled=selected_row is not None,
            empty_ready=empty_ready and not q and status == "all" and family == "all",
            zero_matches=zero_matches,
        )

    def summary_for_key(self, subject_key: str) -> SelectedExamSummary | None:
        entry = self._catalogue.get_entry(subject_key)
        if entry is None or not entry.selectable:
            return None
        return self._summary_for(self._to_row(entry))

    def _to_row(self, entry: SubjectCatalogueEntry) -> ExamOfferingRow:
        description = ""
        if entry.is_ready and entry.selectable:
            description = (
                f"Verified curriculum for {entry.name}."
                if not entry.current_published_edition
                else f"{entry.name} · ready to begin."
            )
            if entry.version:
                description = f"{entry.name} · {entry.version}."
        elif entry.is_ready and not entry.selectable:
            description = entry.preparation_message or (
                "Enrolment opens when student access is enabled."
            )
        else:
            description = _SOON_LINE

        scope = ""
        if entry.version:
            scope = f"Edition · {entry.version}"
        elif entry.is_ready:
            scope = "Verified curriculum"

        return ExamOfferingRow(
            subject_key=entry.subject_key,
            exam_code=entry.paper,
            title=entry.name,
            description=description,
            scope_label=scope,
            updated_label=entry.release_date_label,
            availability_label=entry.availability_label,
            selectable=entry.selectable,
            preparation_line=(
                entry.preparation_message
                if (entry.is_ready and not entry.selectable)
                else ""
            ),
            family=entry.paper,
        )

    def _filter_rows(
        self,
        rows: list[ExamOfferingRow],
        *,
        q: str,
        family: str,
    ) -> list[ExamOfferingRow]:
        out = rows
        if family and family != "all":
            out = [r for r in out if r.family == family or r.exam_code == family]
        if q:
            out = [
                r
                for r in out
                if q in r.title.lower()
                or q in r.exam_code.lower()
                or q in r.subject_key.lower()
            ]
        return list(out)

    def _sort_ready(
        self, rows: list[ExamOfferingRow], sort_key: str
    ) -> list[ExamOfferingRow]:
        if sort_key == "alpha":
            return sorted(rows, key=lambda r: (r.title.lower(), r.exam_code))
        # Recently updated — entries with dates first (label non-empty), then alpha.
        return sorted(
            rows,
            key=lambda r: (
                0 if r.updated_label else 1,
                r.updated_label,
                r.title.lower(),
            ),
            reverse=False,
        )

    def _family_options(
        self, rows: list[ExamOfferingRow]
    ) -> tuple[ChooseExamFilterOption, ...]:
        codes = sorted({r.exam_code for r in rows if r.exam_code})
        if len(codes) < 2:
            return _EMPTY_FAMILY
        return (
            ChooseExamFilterOption("all", "All"),
            *(ChooseExamFilterOption(c, c) for c in codes),
        )

    def _summary_for(self, row: ExamOfferingRow) -> SelectedExamSummary:
        duration = row.scope_label or "Structured study path"
        return SelectedExamSummary(
            exam_title=row.title,
            exam_code=row.exam_code,
            qualification_stage="Ready to begin",
            expected_path="Verified curriculum study path",
            estimated_duration=duration,
            next_step="Continue to set your exam date",
        )
