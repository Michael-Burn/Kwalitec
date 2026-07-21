"""Frozen result DTOs for Student Twin Initialization (BR-003).

``InitializationResult`` is the canonical output after converting completed
onboarding declarations into a persistent Educational Digital Twin and the
student's first Educational Pipeline run.
"""

from __future__ import annotations

from dataclasses import dataclass

from application.pipeline.pipeline_result import PipelineResult
from domain.education.digital_twin import EducationalDigitalTwin
from domain.education.evidence import EvidenceRecord

# Application-facing alias: the persistent Student Twin *is* the aggregate.
StudentTwin = EducationalDigitalTwin


@dataclass(frozen=True, slots=True)
class InitialEvidence:
    """Seeded observational evidence catalogue from onboarding declarations."""

    onboarding_id: str
    student_id: str
    records: tuple[EvidenceRecord, ...]

    @property
    def evidence_ids(self) -> tuple[str, ...]:
        return tuple(record.evidence_id.value for record in self.records)

    @property
    def primary_evidence_id(self) -> str:
        if not self.records:
            raise ValueError("InitialEvidence has no records")
        return self.records[0].evidence_id.value


@dataclass(frozen=True, slots=True)
class InitializationResult:
    """Outcome of Student Twin Initialization.

    Recommendations and missions live only inside ``pipeline_result`` — this
    package never invents them outside the Educational Pipeline.
    """

    student_twin: StudentTwin
    initial_evidence: InitialEvidence
    pipeline_result: PipelineResult
    idempotent_replay: bool = False

    @property
    def twin_id(self) -> str:
        return self.student_twin.twin_id.value

    @property
    def student_id(self) -> str:
        return self.student_twin.student_id
