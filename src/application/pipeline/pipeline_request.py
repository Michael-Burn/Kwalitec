"""PipelineRequest — input to the Educational Pipeline Orchestrator.

Architecture Source
    APP-002 Educational Pipeline Orchestrator

Carries observational evidence and optional session context. Session context
supplies Educational OS state already decided upstream (twin, diagnosis,
priority, strategy, availability). The pipeline never invents those decisions.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.diagnosis import EducationalDiagnosis
from domain.education.digital_twin import EducationalDigitalTwin, LearningTrajectory
from domain.education.evidence import EvidenceRecord
from domain.education.priority import EducationalPriority
from domain.education.teaching_strategy import TeachingStrategy
from domain.progress_evaluation import CompletedMission
from domain.study_planning import LearnerAvailability, StudyPlan


@dataclass(frozen=True, slots=True)
class PipelineSessionContext:
    """Optional Educational OS state for one pipeline execution.

    Holds collaborators required by domain engines. Values must already be
    educationally consistent; the pipeline does not diagnose, prioritise, or
    select strategies.
    """

    twin: EducationalDigitalTwin
    diagnosis: EducationalDiagnosis
    priority: EducationalPriority
    strategy: TeachingStrategy
    availability: LearnerAvailability
    trajectory: LearningTrajectory | None = None
    completed_missions: tuple[CompletedMission, ...] = ()
    prior_study_plans: tuple[StudyPlan, ...] = ()


@dataclass(frozen=True, slots=True)
class PipelineRequest:
    """Input cargo for ``EducationalPipeline.run``.

    Attributes:
        student_id: Learner identity for this run.
        educational_evidence: Observational evidence records to analyse.
        session_context: Optional Educational OS state for engines that need
            twin / diagnosis / priority / strategy / availability.
    """

    student_id: str
    educational_evidence: (
        tuple[EvidenceRecord, ...] | list[EvidenceRecord] | EvidenceRecord
    )
    session_context: PipelineSessionContext | None = None

    def normalised_evidence(self) -> tuple[EvidenceRecord, ...]:
        """Return evidence as an immutable tuple."""
        raw = self.educational_evidence
        if isinstance(raw, EvidenceRecord):
            return (raw,)
        return tuple(raw)
