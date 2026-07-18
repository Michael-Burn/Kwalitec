"""Twin identity — stable identity for a Student Digital Twin instance."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TwinIdentity:
    """Stable identity binding a Twin to a learner and subject scope."""

    twin_id: str
    learner_id: str
    subject_code: str | None = None

    @classmethod
    def create(
        cls,
        twin_id: str,
        learner_id: str,
        *,
        subject_code: str | None = None,
    ) -> TwinIdentity:
        """Construct a TwinIdentity after validating invariants."""
        tid = _require_non_empty(twin_id, "twin_id")
        lid = _require_non_empty(learner_id, "learner_id")
        subject = None
        if subject_code is not None:
            subject = _require_non_empty(subject_code, "subject_code")
        return cls(twin_id=tid, learner_id=lid, subject_code=subject)

    def with_subject(self, subject_code: str | None) -> TwinIdentity:
        """Return identity with a replacement subject scope."""
        subject = None
        if subject_code is not None:
            subject = _require_non_empty(subject_code, "subject_code")
        return TwinIdentity(
            twin_id=self.twin_id,
            learner_id=self.learner_id,
            subject_code=subject,
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
