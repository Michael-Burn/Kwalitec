"""Timeline service — ordered Twin snapshot evolution."""

from __future__ import annotations

from app.domain.student_twin.twin_snapshot import TwinSnapshot


class TimelineService:
    """Build ordered Twin snapshot timelines from versioned captures."""

    @staticmethod
    def build(
        snapshots: list[TwinSnapshot] | tuple[TwinSnapshot, ...],
    ) -> tuple[TwinSnapshot, ...]:
        """Return snapshots ordered by version then captured_at."""
        return tuple(
            sorted(
                snapshots,
                key=lambda s: (
                    s.version.major,
                    s.version.minor,
                    s.version.patch,
                    s.captured_at,
                ),
            )
        )

    @staticmethod
    def event_ids_evolution(
        snapshots: list[TwinSnapshot] | tuple[TwinSnapshot, ...],
    ) -> tuple[tuple[str, ...], ...]:
        """Return history_event_ids per snapshot in timeline order."""
        ordered = TimelineService.build(snapshots)
        return tuple(s.history_event_ids for s in ordered)
