"""Policy governing lawful revision of an educational hypothesis.

Architecture Source
    EDUCATIONAL_HYPOTHESIS_MODEL.md
Concept
    Hypothesis Revision Policy
"""

from __future__ import annotations

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.hypothesis.enums import HypothesisStatus, RevisionForm
from domain.education.hypothesis.value_objects.plausibility import Plausibility

_TERMINAL_STATUSES = frozenset({HypothesisStatus.DISCARDED})
_REVISABLE_STATUSES = frozenset(
    {
        HypothesisStatus.ACTIVE,
        HypothesisStatus.REVISED,
        HypothesisStatus.SUSPENDED,
    }
)


class HypothesisRevisionPolicy:
    """Enforces revisability, discard, strengthen, and weaken invariants."""

    @staticmethod
    def assert_revisable(status: HypothesisStatus, *, action: str) -> None:
        """Hypotheses must remain revisable until discarded."""
        if status in _TERMINAL_STATUSES:
            raise EducationalInvariantViolation(
                f"cannot {action} a discarded hypothesis",
                invariant="EducationalHypothesis.status.revisable",
            )
        if status not in _REVISABLE_STATUSES:
            raise EducationalInvariantViolation(
                f"cannot {action} hypothesis in status {status.value}",
                invariant="EducationalHypothesis.status.revisable",
            )

    @staticmethod
    def assert_can_strengthen(status: HypothesisStatus) -> None:
        """Discarded hypotheses cannot be strengthened."""
        if status is HypothesisStatus.DISCARDED:
            raise EducationalInvariantViolation(
                "discarded hypotheses cannot be strengthened",
                invariant="EducationalHypothesis.strengthen.not_discarded",
            )
        HypothesisRevisionPolicy.assert_revisable(status, action="strengthen")

    @staticmethod
    def assert_can_weaken(status: HypothesisStatus) -> None:
        if status is HypothesisStatus.DISCARDED:
            raise EducationalInvariantViolation(
                "cannot weaken a discarded hypothesis",
                invariant="EducationalHypothesis.weaken.not_discarded",
            )
        HypothesisRevisionPolicy.assert_revisable(status, action="weaken")

    @staticmethod
    def assert_can_discard(status: HypothesisStatus) -> None:
        if status is HypothesisStatus.DISCARDED:
            raise EducationalInvariantViolation(
                "hypothesis is already discarded",
                invariant="EducationalHypothesis.discard.already",
            )

    @staticmethod
    def assert_revision_form(revision_form: RevisionForm | None) -> RevisionForm | None:
        if revision_form is None:
            return None
        if not isinstance(revision_form, RevisionForm):
            raise EducationalInvariantViolation(
                "revision_form must be a RevisionForm when provided",
                invariant="EducationalHypothesis.revision_form.type",
            )
        return revision_form

    @staticmethod
    def assert_plausibility_allows_strength_change(
        plausibility: Plausibility, *, action: str
    ) -> None:
        """Suspended plausibility cannot be strengthened or weakened in place."""
        if plausibility.is_suspended():
            raise EducationalInvariantViolation(
                f"cannot {action} while plausibility is suspended; "
                "revise plausibility first",
                invariant="EducationalHypothesis.plausibility.not_suspended",
            )

    @staticmethod
    def next_status_after_revision(
        current: HypothesisStatus,
        *,
        suspend: bool = False,
    ) -> HypothesisStatus:
        if suspend:
            return HypothesisStatus.SUSPENDED
        if current is HypothesisStatus.SUSPENDED:
            return HypothesisStatus.REVISED
        return HypothesisStatus.REVISED
