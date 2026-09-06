"""Infrastructure adapters for Study Curriculum bulk reads.

Wires Runtime C Study Progress and published artefacts to the application
ports so ``app.application.study_curriculum`` stays framework-independent.
"""

from __future__ import annotations

from app.application.educational_engine_foundation.dto import (
    EducationalArtefactSnapshot,
)
from app.application.progress_engine.dto import StudyProgress
from app.application.study_curriculum.assembler import (
    CurriculumLearningStateAssembler,
)
from app.infrastructure.adapters.student_twin.cutover_bridge import (
    learner_twin_query,
)


class RuntimeStudyProgressQuery:
    """Bulk Study Progress via EducationalRuntimeEngineService."""

    def __init__(self, runtime=None) -> None:
        self._runtime = runtime

    def get_study_progress(
        self, *, user_id: int, subject_code: str
    ) -> StudyProgress:
        runtime = self._runtime or _runtime_engine()
        return runtime.get_study_progress(
            user_id=user_id,
            subject_code=subject_code,
        )


class RuntimeSyllabusStructureQuery:
    """Published artefact snapshot for section membership."""

    def __init__(self, foundation=None) -> None:
        self._foundation = foundation

    def artefact_snapshot(
        self, *, subject_code: str
    ) -> EducationalArtefactSnapshot | None:
        foundation = self._foundation or _foundation_service()
        return foundation.derive_active(subject_code)


def _runtime_engine():
    from app.application.educational_runtime_engine.service import (
        EducationalRuntimeEngineService,
    )

    return EducationalRuntimeEngineService()


def _foundation_service():
    from app.application.educational_engine_foundation.service import (
        EducationalEngineFoundationService,
    )

    return EducationalEngineFoundationService()


def curriculum_learning_state_assembler(
    *,
    twin_query=None,
    study_progress=None,
    syllabus=None,
) -> CurriculumLearningStateAssembler:
    """Factory for the default Study Curriculum assembler."""
    return CurriculumLearningStateAssembler(
        twin_query=twin_query or learner_twin_query(),
        study_progress=study_progress or RuntimeStudyProgressQuery(),
        syllabus=syllabus or RuntimeSyllabusStructureQuery(),
    )
