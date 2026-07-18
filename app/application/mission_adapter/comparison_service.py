"""Structural comparison of dual-engine mission outputs.

When PARALLEL / SHADOW modes are active, executes comparison across
structural dimensions only. Never exposes V2 to production users —
exposure is owned by routing. Never compares generated educational
content.
"""

from __future__ import annotations

from uuid import uuid4

from app.application.mission_adapter.dto.comparison_result import ComparisonResult
from app.application.mission_adapter.dto.mission_snapshot import MissionSnapshot
from app.application.mission_adapter.exceptions import ComparisonFailure
from app.application.mission_adapter.policies.comparison_policy import (
    ComparisonPolicy,
)


class ComparisonService:
    """Compare V1 and V2 structural mission snapshots.

    In-memory only — never persists comparison data.
    """

    def __init__(self, *, id_factory=None) -> None:
        self._id_factory = id_factory or (lambda: uuid4().hex[:16])
        self._history: list[ComparisonResult] = []

    @property
    def history(self) -> tuple[ComparisonResult, ...]:
        """In-memory comparison history for this process."""
        return tuple(self._history)

    def clear_history(self) -> None:
        """Drop in-memory history (tests / process reset)."""
        self._history.clear()

    def compare(
        self,
        v1: MissionSnapshot | None,
        v2: MissionSnapshot | None,
        *,
        comparison_id: str | None = None,
    ) -> ComparisonResult:
        """Compare two snapshots and record the result.

        Raises:
            ComparisonFailure: When either snapshot is missing.
        """
        if v1 is None or v2 is None:
            raise ComparisonFailure(
                "Both V1 and V2 snapshots are required for comparison"
            )
        # Guard: refuse forbidden educational fields if sneaked into metadata.
        for key in (v1.metadata or {}):
            if ComparisonPolicy.is_forbidden_field(str(key)):
                raise ComparisonFailure(
                    f"Refusing to compare educational field: {key}"
                )
        for key in (v2.metadata or {}):
            if ComparisonPolicy.is_forbidden_field(str(key)):
                raise ComparisonFailure(
                    f"Refusing to compare educational field: {key}"
                )

        dimensions = ComparisonPolicy.compare_dimensions(v1, v2)
        result = ComparisonResult(
            comparison_id=comparison_id or self._id_factory(),
            matched=ComparisonPolicy.all_matched(dimensions),
            dimensions=dimensions,
            v1_mission_id=v1.mission_id,
            v2_mission_id=v2.mission_id,
            divergence_count=ComparisonPolicy.divergence_count(dimensions),
        )
        self._history.append(result)
        return result

    def summary(self) -> dict[str, float | int | bool]:
        """Aggregate comparison statistics (no student payloads)."""
        total = len(self._history)
        if total == 0:
            return {
                "total": 0,
                "matched": 0,
                "diverged": 0,
                "match_rate": 0.0,
            }
        matched = sum(1 for c in self._history if c.matched)
        diverged = total - matched
        return {
            "total": total,
            "matched": matched,
            "diverged": diverged,
            "match_rate": matched / total,
        }
