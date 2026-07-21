"""Typed authentication identities."""

from __future__ import annotations

from dataclasses import dataclass

from domain.auth.errors import AuthInvariantViolation


@dataclass(frozen=True, slots=True)
class UserId:
    """Stable identity for an authenticated user account."""

    value: str

    def __post_init__(self) -> None:
        cleaned = (self.value or "").strip()
        if not cleaned:
            raise AuthInvariantViolation(
                "user id is required",
                invariant="user_id_non_empty",
            )
        object.__setattr__(self, "value", cleaned)

    def __str__(self) -> str:
        return self.value
