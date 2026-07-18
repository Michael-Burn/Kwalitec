"""Learner — educational identity referenced by the Twin.

The Twin observes the learner. It does not store UI state or credentials.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Learner:
    """Minimal learner identity for Twin scoping."""

    learner_id: str
    display_name: str | None = None
    subject_codes: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        learner_id: str,
        *,
        display_name: str | None = None,
        subject_codes: list[str] | tuple[str, ...] | None = None,
    ) -> Learner:
        """Construct a Learner after validating invariants."""
        lid = _require_non_empty(learner_id, "learner_id")
        name = None
        if display_name is not None:
            name = display_name.strip() or None
        subjects = tuple(
            _require_non_empty(code, "subject_code")
            for code in (subject_codes or ())
        )
        if len(subjects) != len(set(subjects)):
            raise ValueError("duplicate subject_code within learner")
        return cls(learner_id=lid, display_name=name, subject_codes=subjects)

    @property
    def subject_count(self) -> int:
        """Number of registered subject scopes."""
        return len(self.subject_codes)

    def with_subject(self, subject_code: str) -> Learner:
        """Return a learner with an appended subject code."""
        code = _require_non_empty(subject_code, "subject_code")
        if code in self.subject_codes:
            raise ValueError(f"duplicate subject_code: {code!r}")
        return Learner(
            learner_id=self.learner_id,
            display_name=self.display_name,
            subject_codes=(*self.subject_codes, code),
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
