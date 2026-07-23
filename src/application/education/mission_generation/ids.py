"""Identity tokens for Adaptive Mission Generation.

Opaque, immutable identifiers scoped to this application package.
Identities are not database keys and carry no persistence semantics.
"""

from __future__ import annotations

from dataclasses import dataclass

from application.education.mission_generation.errors import MissionInvariantViolation


def _require_identity(value: str | None, type_name: str) -> str:
    if value is None:
        raise MissionInvariantViolation(
            f"{type_name} is required",
            invariant=f"{type_name}.required",
        )
    cleaned = value.strip()
    if not cleaned:
        raise MissionInvariantViolation(
            f"{type_name} must be non-empty",
            invariant=f"{type_name}.non_empty",
        )
    if any(ch.isspace() for ch in cleaned):
        raise MissionInvariantViolation(
            f"{type_name} must not contain whitespace",
            invariant=f"{type_name}.no_whitespace",
        )
    return cleaned


@dataclass(frozen=True, slots=True)
class MissionPlanId:
    """Identity of a single MissionPlan produced by the generator."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "value", _require_identity(self.value, "MissionPlanId")
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class MissionId:
    """Identity of a single Mission within a MissionPlan."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _require_identity(self.value, "MissionId"))

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class MissionStepId:
    """Identity of a single MissionStep within a Mission."""

    value: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "value", _require_identity(self.value, "MissionStepId")
        )

    def __str__(self) -> str:
        return self.value
