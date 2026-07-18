"""Stateless versioning policy."""

from __future__ import annotations

import re

from app.application.curriculum_management.exceptions import PolicyViolation
from app.domain.curriculum_management.publication_state import PublicationState
from app.domain.curriculum_management.subject import Subject
from app.domain.curriculum_management.subject_version import SubjectVersion

_VERSION_LABEL_RE = re.compile(r"^\d{4}\.\d+$")


class VersionPolicy:
    """Deterministic subject-version rules (stateless)."""

    @staticmethod
    def assert_valid_label(version_label: str) -> str:
        """Return normalised label or raise PolicyViolation."""
        if not isinstance(version_label, str):
            raise PolicyViolation("version_label must be a non-empty string")
        label = version_label.strip()
        if not _VERSION_LABEL_RE.match(label):
            raise PolicyViolation(
                "version_label must match YYYY.N (e.g. 2026.1); "
                f"got {version_label!r}"
            )
        return label

    @staticmethod
    def assert_belongs_to_subject(
        version: SubjectVersion,
        subject: Subject,
    ) -> None:
        """Raise when version.subject_id mismatches subject."""
        if version.subject_id != subject.subject_id:
            raise PolicyViolation(
                f"Version {version.version_id!r} does not belong to "
                f"subject {subject.subject_id!r}"
            )

    @staticmethod
    def assert_mutable(version: SubjectVersion) -> None:
        """Raise when version is published or archived (structural lock)."""
        if version.state in {
            PublicationState.PUBLISHED,
            PublicationState.ARCHIVED,
            PublicationState.APPROVED,
        }:
            raise PolicyViolation(
                f"Version is locked in state {version.state.value}"
            )

    @staticmethod
    def assert_can_activate(
        subject: Subject,
        version: SubjectVersion,
    ) -> None:
        """Raise when a version cannot become the active published pointer."""
        VersionPolicy.assert_belongs_to_subject(version, subject)
        if version.state is not PublicationState.PUBLISHED:
            raise PolicyViolation(
                "Only PUBLISHED versions may be activated; "
                f"got {version.state.value}"
            )

    @staticmethod
    def compare_labels(left: str, right: str) -> int:
        """Compare version labels; negative if left < right."""
        ly, ln = left.split(".")
        ry, rn = right.split(".")
        if int(ly) != int(ry):
            return int(ly) - int(ry)
        return int(ln) - int(rn)
