"""Read-only qualifying study day query adapter (infrastructure).

Wires QualifyingStudyDayIndexPersistence to the application query port.
"""

from __future__ import annotations

from datetime import date, timedelta

from app.application.learner_progress.index_document import parse_qualifying_dates
from app.application.learner_progress.query import (
    QualifyingStudyDayQueryPort,
    StreakStats,
)
from app.application.learner_progress.streak import (
    current_streak_days,
    dates_in_range,
    monotonic_longest_streak_days,
)
from app.infrastructure.adapters.learner_progress import (
    qualifying_study_day_persistence,
)


class QualifyingStudyDayQueryAdapter:
    """Concrete QualifyingStudyDayQueryPort over persisted index documents."""

    def __init__(
        self,
        *,
        index: qualifying_study_day_persistence.QualifyingStudyDayIndexPersistence
        | None = None,
    ) -> None:
        if index is None:
            index = (
                qualifying_study_day_persistence.QualifyingStudyDayIndexPersistence()
            )
        self._index = index

    def qualifying_study_dates(
        self,
        *,
        user_id: int,
        start_date: date,
        end_date: date,
    ) -> tuple[date, ...]:
        document = self._index.load_index(learner_id=str(user_id))
        study_days = parse_qualifying_dates(document)
        return dates_in_range(study_days, start_date=start_date, end_date=end_date)

    def streak_stats(
        self,
        *,
        user_id: int,
        as_of: date,
        lookback_days: int = 90,
    ) -> StreakStats:
        window_start = as_of - timedelta(days=max(lookback_days - 1, 0))
        document = self._index.load_index(learner_id=str(user_id))
        all_days = parse_qualifying_dates(document)
        in_window = dates_in_range(
            all_days,
            start_date=window_start,
            end_date=as_of,
        )
        window_set = set(in_window)
        stored_longest = int((document or {}).get("longest_streak_days") or 0)
        longest = monotonic_longest_streak_days(
            study_days=all_days,
            stored_longest=stored_longest,
        )
        return StreakStats(
            current_streak_days=current_streak_days(window_set, as_of=as_of),
            longest_streak_days=longest,
            qualifying_dates=in_window,
        )


def qualifying_study_day_query(
    *,
    index: qualifying_study_day_persistence.QualifyingStudyDayIndexPersistence
    | None = None,
) -> QualifyingStudyDayQueryPort:
    """Factory for the default query adapter."""
    return QualifyingStudyDayQueryAdapter(index=index)
