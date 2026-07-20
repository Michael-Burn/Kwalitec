"""Shared factories for Mission Generation domain tests."""

from __future__ import annotations

import pytest

from domain.education.diagnosis import (
    DiagnosisSeverity,
    DiagnosisSeverityLevel,
    EducationalDiagnosis,
)
from domain.education.digital_twin import EducationalDigitalTwin, LearningTrajectory
from domain.education.foundation.enums import (
    DiagnosisType,
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.ids import DiagnosisId
from domain.education.priority import (
    EducationalPriority,
    PriorityScoreBand,
    UrgencyLevel,
)
from domain.education.teaching_strategy import (
    ComplexityLevel,
    CompositionPattern,
    InstructionalComplexity,
    TeachingStrategy,
)
from domain.mission_generation import MissionGenerator, MissionSpecification
from tests.domain.education.diagnosis.conftest import (
    make_diagnosis,
    make_severity,
)
from tests.domain.education.digital_twin.conftest import make_twin
from tests.domain.education.priority.conftest import (
    make_diagnosis_ref as make_priority_diagnosis_ref,
)
from tests.domain.education.priority.conftest import (
    make_priority,
    make_score,
    make_urgency,
)
from tests.domain.education.teaching_strategy.conftest import (
    CANONICAL_SECONDARIES,
    make_complexity,
    make_secondary,
    make_strategy,
)
from tests.domain.education.teaching_strategy.conftest import (
    make_diagnosis_ref as make_strategy_diagnosis_ref,
)

DEFAULT_DIAGNOSIS_TYPE = DiagnosisType.PREREQUISITE_GAP
DEFAULT_INTENTION = TeachingIntentionType.STRENGTHEN_PREREQUISITE
DEFAULT_STRATEGY = TeachingStrategyType.WORKED_EXAMPLE


@pytest.fixture
def student_id() -> str:
    return "student-ada"


def make_aligned_diagnosis(
    *,
    diagnosis_id: str = "diag-001",
    student_id: str = "student-ada",
    diagnosis_type: DiagnosisType = DEFAULT_DIAGNOSIS_TYPE,
    severity: DiagnosisSeverity | None = None,
) -> EducationalDiagnosis:
    return make_diagnosis(
        diagnosis_id=diagnosis_id,
        student_id=student_id,
        diagnosis_type=diagnosis_type,
        severity=severity or make_severity(DiagnosisSeverityLevel.MODERATE),
    )


def make_aligned_priority(
    *,
    priority_id: str = "prio-001",
    student_id: str = "student-ada",
    diagnosis_id: str | DiagnosisId = "diag-001",
    diagnosis_type: DiagnosisType = DEFAULT_DIAGNOSIS_TYPE,
    score_band: PriorityScoreBand = PriorityScoreBand.HIGH,
    urgency_level: UrgencyLevel = UrgencyLevel.ELEVATED,
) -> EducationalPriority:
    return make_priority(
        priority_id=priority_id,
        student_id=student_id,
        diagnosis_references=[
            make_priority_diagnosis_ref(
                diagnosis_id=diagnosis_id,
                diagnosis_type=diagnosis_type,
            )
        ],
        score=make_score(score_band),
        urgency=make_urgency(urgency_level),
        calculate=False,
    )


def make_aligned_strategy(
    *,
    strategy_id: str = "ts-001",
    student_id: str = "student-ada",
    diagnosis_id: str | DiagnosisId = "diag-001",
    diagnosis_type: DiagnosisType = DEFAULT_DIAGNOSIS_TYPE,
    primary_strategy: TeachingStrategyType = DEFAULT_STRATEGY,
    intention_type: TeachingIntentionType = DEFAULT_INTENTION,
    composition_pattern: CompositionPattern | None = None,
    complexity: InstructionalComplexity | None = None,
    with_secondaries: bool = False,
) -> TeachingStrategy:
    secondaries = None
    pattern = composition_pattern
    if with_secondaries:
        pattern = pattern or CompositionPattern.MODELLING_TO_INDEPENDENCE
        secondary_types = CANONICAL_SECONDARIES[pattern]
        secondaries = [
            make_secondary(stype, order)
            for order, stype in enumerate(secondary_types, start=1)
        ]
    return make_strategy(
        strategy_id=strategy_id,
        student_id=student_id,
        primary_strategy=primary_strategy,
        intention_type=intention_type,
        diagnosis_references=[
            make_strategy_diagnosis_ref(
                diagnosis_id=diagnosis_id,
                diagnosis_type=diagnosis_type,
            )
        ],
        secondary_strategies=secondaries,
        composition_pattern=pattern,
        complexity=complexity or make_complexity(ComplexityLevel.MODERATE),
        select=True,
    )


def generate_mission(
    *,
    twin: EducationalDigitalTwin | None = None,
    diagnosis: EducationalDiagnosis | None = None,
    priority: EducationalPriority | None = None,
    strategy: TeachingStrategy | None = None,
    trajectory: LearningTrajectory | None = None,
    with_secondaries: bool = False,
) -> MissionSpecification:
    twin = twin or make_twin()
    diagnosis = diagnosis or make_aligned_diagnosis()
    priority = priority or make_aligned_priority()
    strategy = strategy or make_aligned_strategy(with_secondaries=with_secondaries)
    return MissionGenerator.generate(
        twin,
        diagnosis,
        priority,
        strategy,
        trajectory=trajectory,
    )
