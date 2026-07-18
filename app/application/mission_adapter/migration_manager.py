"""Migration phase coordination for the Mission Adapter.

Responsible only for migration state. Never alters educational logic.
"""

from __future__ import annotations

from enum import Enum

from app.application.mission_adapter.exceptions import MigrationStateError


class MigrationPhase(str, Enum):
    """Lawful Mission Adapter migration phases."""

    LEGACY_ONLY = "legacy_only"
    PARALLEL_VALIDATION = "parallel_validation"
    LIMITED_V2 = "limited_v2"
    FULL_V2 = "full_v2"
    RETIRED_V1 = "retired_v1"


# Forward transitions only (plus explicit rollback edges below).
_FORWARD: dict[MigrationPhase, frozenset[MigrationPhase]] = {
    MigrationPhase.LEGACY_ONLY: frozenset(
        {MigrationPhase.PARALLEL_VALIDATION}
    ),
    MigrationPhase.PARALLEL_VALIDATION: frozenset(
        {MigrationPhase.LIMITED_V2, MigrationPhase.LEGACY_ONLY}
    ),
    MigrationPhase.LIMITED_V2: frozenset(
        {
            MigrationPhase.FULL_V2,
            MigrationPhase.PARALLEL_VALIDATION,
            MigrationPhase.LEGACY_ONLY,
        }
    ),
    MigrationPhase.FULL_V2: frozenset(
        {
            MigrationPhase.RETIRED_V1,
            MigrationPhase.LIMITED_V2,
            MigrationPhase.PARALLEL_VALIDATION,
            MigrationPhase.LEGACY_ONLY,
        }
    ),
    MigrationPhase.RETIRED_V1: frozenset(
        {
            MigrationPhase.FULL_V2,  # emergency re-enable V1 path via FULL_V2
        }
    ),
}


class MigrationManager:
    """Coordinates migration phases for mission engine cutover.

    Holds in-memory phase state only — no persistence. Operators advance
    or roll back through ``transition_to``. Rollback to LEGACY_ONLY is
    always available from non-retired phases for safety.
    """

    def __init__(
        self,
        *,
        initial_phase: MigrationPhase = MigrationPhase.LEGACY_ONLY,
    ) -> None:
        if not isinstance(initial_phase, MigrationPhase):
            raise MigrationStateError(
                f"Invalid initial migration phase: {initial_phase!r}"
            )
        self._phase = initial_phase
        self._history: list[MigrationPhase] = [initial_phase]

    @property
    def phase(self) -> MigrationPhase:
        """Current migration phase."""
        return self._phase

    @property
    def history(self) -> tuple[MigrationPhase, ...]:
        """Ordered phase visit history (including initial)."""
        return tuple(self._history)

    def allowed_transitions(self) -> frozenset[MigrationPhase]:
        """Phases reachable in one transition from the current phase."""
        return _FORWARD[self._phase]

    def can_transition_to(self, target: MigrationPhase) -> bool:
        """True when ``target`` is a lawful next phase."""
        return target in self.allowed_transitions()

    def transition_to(self, target: MigrationPhase) -> MigrationPhase:
        """Advance or roll back to ``target``.

        Raises:
            MigrationStateError: When the transition is unlawful.
        """
        if not isinstance(target, MigrationPhase):
            raise MigrationStateError(
                f"Invalid migration phase: {target!r}"
            )
        if target == self._phase:
            return self._phase
        if not self.can_transition_to(target):
            raise MigrationStateError(
                f"Cannot transition from {self._phase.value} to {target.value}"
            )
        self._phase = target
        self._history.append(target)
        return self._phase

    def rollback_to_legacy(self) -> MigrationPhase:
        """Emergency rollback toward LEGACY_ONLY when lawful.

        From RETIRED_V1, steps through FULL_V2 then caller may continue
        rollback; this helper only takes one lawful step toward legacy.
        """
        if self._phase == MigrationPhase.LEGACY_ONLY:
            return self._phase
        if self._phase == MigrationPhase.RETIRED_V1:
            return self.transition_to(MigrationPhase.FULL_V2)
        if MigrationPhase.LEGACY_ONLY in self.allowed_transitions():
            return self.transition_to(MigrationPhase.LEGACY_ONLY)
        # PARALLEL_VALIDATION → LEGACY_ONLY is allowed; LIMITED/FULL too.
        # If somehow stuck, raise.
        raise MigrationStateError(
            f"No direct legacy rollback from {self._phase.value}"
        )

    def v1_retired(self) -> bool:
        """True when Version 1 generation is retired."""
        return self._phase == MigrationPhase.RETIRED_V1

    def v2_authoritative(self) -> bool:
        """True when V2 is the authoritative production engine."""
        return self._phase in {
            MigrationPhase.FULL_V2,
            MigrationPhase.RETIRED_V1,
        }
