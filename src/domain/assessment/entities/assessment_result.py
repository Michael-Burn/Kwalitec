"""AssessmentResult — evidence packaging for a session (not a grade).

Architecture Source
    knowledge/product/AP-002/SCORING_MODEL.md
    knowledge/product/AP-002/EVIDENCE_MODEL.md
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.assessment.enums import AttemptOutcome
from domain.assessment.exceptions import AssessmentInvariantViolation
from domain.assessment.value_objects.ids import ObservationId, ResultId, SessionId
from domain.assessment.value_objects.levels import EvidenceStrength
from domain.education.foundation.base import EducationalEntity


@dataclass(frozen=True, slots=True, eq=False)
class AssessmentResult(EducationalEntity):
    """Evidence-only rollup linking a session to recorded observations.

    Must not duplicate Twin mastery rows or invent readiness percentages.
    """

    result_id: ResultId
    session_id: SessionId
    observation_ids: tuple[ObservationId, ...] = ()
    correctness_counts: tuple[tuple[AttemptOutcome, int], ...] = ()
    evidence_strength: EvidenceStrength | None = None

    @property
    def entity_id(self) -> ResultId:
        return self.result_id

    def _validate(self) -> None:
        if not isinstance(self.result_id, ResultId):
            raise AssessmentInvariantViolation(
                "result_id must be a ResultId",
                invariant="AssessmentResult.result_id.type",
            )
        if not isinstance(self.session_id, SessionId):
            raise AssessmentInvariantViolation(
                "session_id must be a SessionId",
                invariant="AssessmentResult.session_id.type",
            )
        ids: list[ObservationId] = []
        seen: set[str] = set()
        for observation_id in self.observation_ids or ():
            if not isinstance(observation_id, ObservationId):
                raise AssessmentInvariantViolation(
                    "observation_ids must contain ObservationId values",
                    invariant="AssessmentResult.observation_ids.type",
                )
            if observation_id.value in seen:
                raise AssessmentInvariantViolation(
                    "duplicate observation_id in AssessmentResult",
                    invariant="AssessmentResult.observation_ids.unique",
                )
            seen.add(observation_id.value)
            ids.append(observation_id)
        object.__setattr__(self, "observation_ids", tuple(ids))

        counts: list[tuple[AttemptOutcome, int]] = []
        for key, value in self.correctness_counts or ():
            if not isinstance(key, AttemptOutcome):
                raise AssessmentInvariantViolation(
                    "correctness_counts keys must be AttemptOutcome",
                    invariant="AssessmentResult.correctness_counts.key",
                )
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise AssessmentInvariantViolation(
                    "correctness_counts values must be non-negative integers",
                    invariant="AssessmentResult.correctness_counts.value",
                )
            counts.append((key, value))
        object.__setattr__(self, "correctness_counts", tuple(counts))

        if self.evidence_strength is not None and not isinstance(
            self.evidence_strength, EvidenceStrength
        ):
            raise AssessmentInvariantViolation(
                "evidence_strength must be an EvidenceStrength when provided",
                invariant="AssessmentResult.evidence_strength.type",
            )

    def correctness_count_map(self) -> dict[AttemptOutcome, int]:
        return dict(self.correctness_counts)
