"""Subject identity token for educational products (e.g. CS1, CM1, CB2)."""

from __future__ import annotations

import re
from dataclasses import dataclass

_IDENTIFIER_RE = re.compile(r"^[A-Z][A-Z0-9]{1,15}$")


@dataclass(frozen=True)
class SubjectIdentifier:
    """Canonical subject product code.

    Examples: CS1, CM1, CB2.
    Never encodes syllabus text or PDF content.
    """

    code: str

    @classmethod
    def create(cls, code: str) -> SubjectIdentifier:
        """Construct after normalising and validating the product code.

        Raises:
            ValueError: On empty or malformed codes.
        """
        if not isinstance(code, str):
            raise ValueError("code must be a non-empty string")
        normalized = code.strip().upper()
        if not normalized:
            raise ValueError("code must be a non-empty string")
        if not _IDENTIFIER_RE.match(normalized):
            raise ValueError(
                "code must match ^[A-Z][A-Z0-9]{1,15}$ "
                f"(got {code!r})"
            )
        return cls(code=normalized)

    def __str__(self) -> str:
        return self.code
