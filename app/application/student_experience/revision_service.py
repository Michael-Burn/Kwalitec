"""RevisionService — Revision as the Spacing Scheduler's honest home.

Queries only ``get_spacing_scheduler().revision_board``. Does not calculate
due dates, priority, or educational ROI. Does not call Adaptive Decision.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import date

from app.application.educational_packages.loader import find_package_by_id
from app.application.spacing_scheduler import (
    SpacingBoardEntry,
    SpacingSchedulerService,
    get_spacing_scheduler,
)
from app.application.student_experience._snapshots import revision_snapshot
from app.application.student_experience.dto.revision_snapshot import RevisionSnapshot
from app.application.student_experience.exceptions import RevisionError
from app.domain.student_experience.revision_projection import (
    RevisionItem,
    RevisionOption,
    RevisionProjection,
)

logger = logging.getLogger(__name__)

_EMPTY_DUE_MESSAGE = (
    "Nothing is due for review yet. Packages return here after you "
    "complete them and enough time has passed."
)


class RevisionService:
    """Project Revision sections from the Spacing Scheduler only."""

    def __init__(
        self,
        *,
        spacing_scheduler: SpacingSchedulerService | None = None,
        as_of_factory: Callable[[], date] | None = None,
        **_ignored: object,
    ) -> None:
        # Adaptive Decision / EducationalState kwargs are intentionally ignored
        # so existing composition wiring stays compatible without ranking.
        self._spacing = spacing_scheduler
        self._as_of_factory = as_of_factory or date.today

    def revision(self, student_id: str) -> RevisionSnapshot:
        """Build the Revision projection for ``student_id``."""
        sid = _require_id(student_id)
        scheduler = self._spacing or get_spacing_scheduler()
        as_of = self._as_of_factory()
        board = scheduler.revision_board(learner_id=sid, as_of=as_of)

        due_now = tuple(_item_from_entry(e) for e in board.due_now)
        upcoming = tuple(_item_from_entry(e) for e in board.upcoming)
        recently = tuple(_item_from_entry(e) for e in board.recently_reviewed)

        primary = None
        alternatives: tuple[RevisionOption, ...] = ()
        if due_now:
            primary = _option_from_item(due_now[0], is_primary=True)
            alternatives = tuple(
                _option_from_item(item, is_primary=False) for item in due_now[1:]
            )

        empty_message = ""
        if not due_now:
            empty_message = _EMPTY_DUE_MESSAGE

        projection = RevisionProjection.create(
            sid,
            due_now=due_now,
            upcoming=upcoming,
            recently_reviewed=recently,
            empty_message=empty_message,
            primary=primary,
            alternatives=alternatives,
        )
        return revision_snapshot(projection)


def _item_from_entry(entry: SpacingBoardEntry) -> RevisionItem:
    pack = find_package_by_id(entry.package_id)
    title = ""
    if pack is not None:
        title = (
            str(getattr(pack, "display_title", "") or "").strip()
            or str(getattr(pack, "topic_title", "") or "").strip()
        )
    if not title:
        title = entry.package_id
    next_due = entry.state.next_due_on.isoformat() if entry.state.next_due_on else ""
    last_done = (
        entry.state.last_completed_on.isoformat()
        if entry.state.last_completed_on
        else ""
    )
    return RevisionItem.create(
        entry.package_id,
        title,
        explanation=entry.explanation,
        status=str(entry.decision.status.value),
        next_due_on=next_due,
        last_completed_on=last_done,
        interval_days=entry.state.current_interval_days,
    )


def _option_from_item(item: RevisionItem, *, is_primary: bool) -> RevisionOption:
    return RevisionOption.create(
        item.package_id,
        item.title,
        expected_benefit="",
        priority_label="",
        explanation=None,
        is_primary=is_primary,
        package_id=item.package_id,
    )


def _require_id(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RevisionError("student_id must be a non-empty string")
    return value.strip()
