"""Snapshot service — immutable Twin snapshot projection."""

from __future__ import annotations

from datetime import datetime

from app.application.student_twin.dto.twin_snapshot import TwinSnapshotDTO
from app.application.student_twin.exceptions import SnapshotError
from app.domain.student_twin.digital_twin import DigitalTwin
from app.domain.student_twin.twin_snapshot import TwinSnapshot


class SnapshotService:
    """Project immutable Twin snapshots for consumers."""

    @staticmethod
    def capture(twin: DigitalTwin, *, as_of: datetime | None = None) -> TwinSnapshot:
        """Capture a domain TwinSnapshot."""
        try:
            return twin.to_snapshot(captured_at=as_of)
        except Exception as exc:  # noqa: BLE001 — wrap as SnapshotError
            raise SnapshotError(str(exc)) from exc

    @staticmethod
    def to_dto(snapshot: TwinSnapshot) -> TwinSnapshotDTO:
        """Project a domain snapshot to an application DTO."""
        return TwinSnapshotDTO.from_domain(snapshot)
