"""Stateless normalisation policy for extracted curriculum structures."""

from __future__ import annotations

import re

_SLUG_RE = re.compile(r"[^a-z0-9]+")
_NUMBER_RE = re.compile(r"^(\d+)(?:\.(\d+))?(?:\.(\d+))?$")


class NormalizationPolicy:
    """Deterministic identity and numbering rules (stateless)."""

    DEFAULT_SECTION_ID = "section-default"
    DEFAULT_SECTION_TITLE = "General"
    DEFAULT_SECTION_NUMBER = "1"

    @staticmethod
    def slugify(text: str, *, prefix: str = "") -> str:
        """Produce a stable lowercase slug from ``text``."""
        raw = (text or "").strip().lower()
        slug = _SLUG_RE.sub("-", raw).strip("-")
        if not slug:
            slug = "item"
        if prefix:
            return f"{prefix}-{slug}"
        return slug

    @staticmethod
    def canonical_id(raw_id: str, *, prefix: str, fallback_title: str) -> str:
        """Canonicalise an identity token."""
        token = (raw_id or "").strip().lower()
        if token:
            return NormalizationPolicy.slugify(token, prefix=prefix)
        return NormalizationPolicy.slugify(fallback_title, prefix=prefix)

    @staticmethod
    def canonical_number(
        number: str | None,
        *,
        order_index: int,
        parent_number: str | None = None,
    ) -> str:
        """Derive a stable display number.

        Prefer an explicit well-formed number; otherwise synthesise from order.
        """
        if number:
            token = number.strip()
            if _NUMBER_RE.match(token):
                return token
            # Keep non-empty explicit tokens that are not pure garbage
            if token and not token.isspace():
                return token
        if parent_number:
            return f"{parent_number}.{order_index + 1}"
        return str(order_index + 1)

    @staticmethod
    def parse_number_parts(number: str) -> tuple[int, ...]:
        """Parse a dotted number into integer parts; empty on failure."""
        match = _NUMBER_RE.match((number or "").strip())
        if not match:
            return ()
        return tuple(int(p) for p in match.groups() if p is not None)

    @staticmethod
    def numbers_are_consistent(numbers: list[str] | tuple[str, ...]) -> bool:
        """True when numbers are strictly increasing in document order."""
        prev: tuple[int, ...] | None = None
        for number in numbers:
            parts = NormalizationPolicy.parse_number_parts(number)
            if not parts:
                continue
            if prev is not None and parts <= prev:
                return False
            prev = parts
        return True

    @staticmethod
    def collapse_whitespace(text: str) -> str:
        """Collapse internal whitespace and strip."""
        return " ".join((text or "").split())
