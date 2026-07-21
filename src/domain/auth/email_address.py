"""Email address value object — normalised identity key."""

from __future__ import annotations

import re
from dataclasses import dataclass

from domain.auth.errors import AuthInvariantViolation

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True, slots=True)
class EmailAddress:
    """Canonical email identity (lowercased and stripped)."""

    value: str

    def __post_init__(self) -> None:
        cleaned = (self.value or "").strip().lower()
        if not cleaned:
            raise AuthInvariantViolation(
                "email is required",
                invariant="email_non_empty",
            )
        if len(cleaned) > 255:
            raise AuthInvariantViolation(
                "email exceeds maximum length",
                invariant="email_max_length",
            )
        if not _EMAIL_RE.match(cleaned):
            raise AuthInvariantViolation(
                "email format is invalid",
                invariant="email_format",
            )
        object.__setattr__(self, "value", cleaned)

    def __str__(self) -> str:
        return self.value
