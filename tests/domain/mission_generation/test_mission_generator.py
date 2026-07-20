"""Mission generation engine tests (EDU-001).

Covers: generation, ordering, duration calculation, priority mapping,
educational rationale, and determinism.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from domain.education.diagnosis import DiagnosisSeverityLevel, DiagnosisStatus
from domain.education.digital_twin import (
    LearningTrajectory,
    TrajectoryPoint,
    TrajectoryPointKind,
)
from domain.education.foundation.enums import DiagnosisType, TeachingStrategyType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.priority import PriorityScoreBand, UrgencyLevel
from domain.education.teaching_strategy import (
    ComplexityLevel,
    CompositionPattern,
    StrategyStatus,
)
from domain.mission_generation import (
    CompletionConditionCode,
    MissionDuration,
    MissionDurationBand,
    MissionGenerator,
    MissionPriorityBand,
    MissionSequence,
    MissionSpecification,
    MissionTask,
    MissionTaskId,
    base_minutes_for,
    map_priority_band,
)
from tests.domain.education.diagnosis.conftest import make_severity
from tests.domain.education.digital_twin.conftest import make_archived_twin, make_twin
from tests.domain.education.teaching_strategy.conftest import (
    CANONICAL_SECONDARIES,
    make_complexity,
    make_strategy,
)
from tests.domain.mission_generation.conftest import (
    generate_mission,
    make_aligned_diagnosis,
    make_aligned_priority,
    make_aligned_strategy,
)

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[3] / "src" / "domain" / "mission_generation"
)

FORBIDDEN_MODULES = frozenset(
    {
        "flask",
        "sqlalchemy",
        "alembic",
        "jinja2",
        "wtforms",
        "requests",
        "httpx",
        "celery",
        "redis",
        "boto3",
        "openai",
        "anthropic",
        "random",
        "secrets",
        "uuid",
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "app.",
    "openai.",
    "anthropic.",
)


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def test_package_exports_required_types() -> None:
    from domain import mission_generation as package

    for name in (
        "MissionSpecification",
        "MissionObjective",
        "MissionTask",
        "MissionSequence",
        "MissionDuration",
        "MissionPriority",
        "MissionGenerator",
    ):
        assert hasattr(package, name), name


@pytest.mark.parametrize(
    "path",
    sorted(PACKAGE_ROOT.glob("*.py")),
    ids=lambda p: p.name,
)
def test_no_forbidden_infrastructure_or_ai_imports(path: Path) -> None:
    imported = _imported_modules(path)
    for name in imported:
        assert name not in FORBIDDEN_MODULES, f"{path.name} imports {name}"
        assert not any(
            name == prefix.rstrip(".") or name.startswith(prefix)
            for prefix in FORBIDDEN_PREFIXES
        ), f"{path.name} imports {name}"


def test_generator_source_has_no_randomness() -> None:
    source = (PACKAGE_ROOT / "mission_generator.py").read_text(encoding="utf-8")
    for token in (
        "import random",
        "from random",
        "import uuid",
        "from uuid",
        "import secrets",
        "from secrets",
        "datetime.now",
        "time.time",
    ):
        assert token not in source


def test_generate_mission_returns_complete_specification() -> None:
    mission = generate_mission(with_secondaries=True)

    assert isinstance(mission, MissionSpecification)
    assert mission.student_id == "student-ada"
    assert mission.objective.diagnosis_type is DiagnosisType.PREREQUISITE_GAP
    assert mission.objective.primary_strategy is TeachingStrategyType.WORKED_EXAMPLE
    assert mission.sequence.length >= 1
    assert mission.duration.planned_minutes > 0
    assert mission.priority.band is MissionPriorityBand.HIGH
    assert len(mission.success_criteria) >= 2
    assert len(mission.completion_conditions) == 4
    assert "prerequisite_gap" in mission.educational_rationale
    assert mission.twin_id.value == "twin-001"
    assert mission.diagnosis_id.value == "diag-001"
    assert mission.priority_id.value == "prio-001"
    assert mission.strategy_id.value == "ts-001"


def test_generate_rejects_draft_strategy() -> None:
    strategy = make_strategy(select=False)
    assert strategy.status is StrategyStatus.DRAFT
    with pytest.raises(EducationalInvariantViolation, match="selected or revised"):
        MissionGenerator.generate(
            make_twin(),
            make_aligned_diagnosis(),
            make_aligned_priority(),
            strategy,
        )


def test_generate_rejects_archived_twin() -> None:
    with pytest.raises(EducationalInvariantViolation, match="archived"):
        MissionGenerator.generate(
            make_archived_twin(),
            make_aligned_diagnosis(),
            make_aligned_priority(),
            make_aligned_strategy(),
        )


def test_generate_rejects_invalidated_diagnosis() -> None:
    diagnosis = make_aligned_diagnosis()
    diagnosis.invalidate("evidence no longer supports this deficiency")
    assert diagnosis.status is DiagnosisStatus.INVALIDATED
    with pytest.raises(EducationalInvariantViolation, match="invalidated"):
        MissionGenerator.generate(
            make_twin(),
            diagnosis,
            make_aligned_priority(),
            make_aligned_strategy(),
        )


def test_generate_rejects_student_mismatch() -> None:
    with pytest.raises(EducationalInvariantViolation, match="student_id"):
        MissionGenerator.generate(
            make_twin(student_id="student-ada"),
            make_aligned_diagnosis(student_id="student-other"),
            make_aligned_priority(),
            make_aligned_strategy(),
        )


def test_generate_rejects_priority_without_diagnosis_link() -> None:
    priority = make_aligned_priority(diagnosis_id="diag-other")
    with pytest.raises(EducationalInvariantViolation, match="priority must reference"):
        MissionGenerator.generate(
            make_twin(),
            make_aligned_diagnosis(),
            priority,
            make_aligned_strategy(),
        )


def test_task_ordering_follows_strategy_composition_sequence() -> None:
    pattern = CompositionPattern.MODELLING_TO_INDEPENDENCE
    strategy = make_aligned_strategy(
        with_secondaries=True,
        composition_pattern=pattern,
    )
    mission = generate_mission(strategy=strategy)

    expected = (
        TeachingStrategyType.WORKED_EXAMPLE,
        *CANONICAL_SECONDARIES[pattern],
    )
    actual = tuple(task.strategy_type for task in mission.sequence.tasks)
    assert actual == expected
    assert [task.sequence_index for task in mission.sequence.tasks] == list(
        range(1, len(expected) + 1)
    )


def test_single_primary_strategy_yields_one_task() -> None:
    mission = generate_mission(with_secondaries=False)
    assert mission.sequence.length == 1
    assert mission.ordered_tasks[0].strategy_type is TeachingStrategyType.WORKED_EXAMPLE
    assert mission.ordered_tasks[0].sequence_index == 1


def test_mission_sequence_rejects_gapped_indexes() -> None:
    with pytest.raises(EducationalInvariantViolation, match="contiguous"):
        MissionSequence.of(
            MissionTask(
                task_id=MissionTaskId("task-a"),
                sequence_index=1,
                strategy_type=TeachingStrategyType.WORKED_EXAMPLE,
                label="a",
                estimated_minutes=5,
            ),
            MissionTask(
                task_id=MissionTaskId("task-b"),
                sequence_index=3,
                strategy_type=TeachingStrategyType.FADED_GUIDANCE,
                label="b",
                estimated_minutes=5,
            ),
        )


def test_duration_equals_sum_of_task_minutes() -> None:
    mission = generate_mission(with_secondaries=True)
    assert (
        mission.duration.planned_minutes == mission.sequence.total_estimated_minutes()
    )
    assert mission.duration.band is MissionDuration.band_for(
        mission.duration.planned_minutes
    )


def test_duration_band_thresholds() -> None:
    assert MissionDuration.band_for(10) is MissionDurationBand.SHORT
    assert MissionDuration.band_for(15) is MissionDurationBand.SHORT
    assert MissionDuration.band_for(16) is MissionDurationBand.MEDIUM
    assert MissionDuration.band_for(35) is MissionDurationBand.MEDIUM
    assert MissionDuration.band_for(36) is MissionDurationBand.LONG


def test_duration_scales_with_complexity() -> None:
    low = generate_mission(
        strategy=make_aligned_strategy(complexity=make_complexity(ComplexityLevel.LOW))
    )
    high = generate_mission(
        strategy=make_aligned_strategy(
            complexity=make_complexity(ComplexityLevel.VERY_HIGH)
        )
    )
    assert high.duration.planned_minutes > low.duration.planned_minutes


def test_duration_severity_adds_only_to_primary_task() -> None:
    mild = generate_mission(
        diagnosis=make_aligned_diagnosis(
            severity=make_severity(DiagnosisSeverityLevel.MILD)
        ),
        with_secondaries=True,
    )
    severe = generate_mission(
        diagnosis=make_aligned_diagnosis(
            severity=make_severity(DiagnosisSeverityLevel.SEVERE)
        ),
        with_secondaries=True,
    )
    assert severe.ordered_tasks[0].estimated_minutes == (
        mild.ordered_tasks[0].estimated_minutes + 3
    )
    for mild_task, severe_task in zip(
        mild.ordered_tasks[1:], severe.ordered_tasks[1:], strict=True
    ):
        assert mild_task.estimated_minutes == severe_task.estimated_minutes


def test_base_minutes_catalogue_covers_worked_example() -> None:
    assert base_minutes_for(TeachingStrategyType.WORKED_EXAMPLE) == 10


@pytest.mark.parametrize(
    ("score_band", "expected"),
    [
        (PriorityScoreBand.NEGLIGIBLE, MissionPriorityBand.NEGLIGIBLE),
        (PriorityScoreBand.LOW, MissionPriorityBand.LOW),
        (PriorityScoreBand.MEDIUM, MissionPriorityBand.MEDIUM),
        (PriorityScoreBand.HIGH, MissionPriorityBand.HIGH),
        (PriorityScoreBand.CRITICAL, MissionPriorityBand.CRITICAL),
    ],
)
def test_priority_band_mapping(
    score_band: PriorityScoreBand,
    expected: MissionPriorityBand,
) -> None:
    assert map_priority_band(score_band) is expected
    mission = generate_mission(
        priority=make_aligned_priority(
            score_band=score_band,
            urgency_level=UrgencyLevel.IMMEDIATE,
        )
    )
    assert mission.priority.band is expected
    assert mission.priority.urgency is UrgencyLevel.IMMEDIATE
    assert mission.priority.rationale is not None
    assert "peak factor" in mission.priority.rationale


def test_educational_rationale_is_explainable_and_substantive() -> None:
    trajectory = LearningTrajectory.of(
        TrajectoryPoint(
            sequence=1,
            kind=TrajectoryPointKind.CREATED,
            label="twin-created",
        ),
        TrajectoryPoint(
            sequence=2,
            kind=TrajectoryPointKind.INTERVENTION,
            label="prior-scaffold",
        ),
    )
    twin = make_twin()
    mission = generate_mission(twin=twin, trajectory=trajectory, with_secondaries=True)

    rationale = mission.educational_rationale
    assert len(rationale) >= 24
    assert DiagnosisType.PREREQUISITE_GAP.value in rationale
    assert TeachingStrategyType.WORKED_EXAMPLE.value in rationale
    assert "Ordered task arc:" in rationale
    assert "Estimated duration" in rationale
    assert "prior-scaffold" in rationale
    assert twin.twin_id.value in rationale
    assert "peak factor" in rationale


def test_success_criteria_and_completion_conditions_present() -> None:
    mission = generate_mission()
    codes = {c.code for c in mission.completion_conditions}
    assert CompletionConditionCode.ALL_TASKS_COMPLETED in codes
    assert CompletionConditionCode.PRIMARY_STRATEGY_ENGAGED in codes
    assert CompletionConditionCode.SUCCESS_CRITERIA_MET in codes
    assert CompletionConditionCode.EVIDENCE_CAPTURED in codes
    assert any(c.code == "strategy_goal_advanced" for c in mission.success_criteria)


def test_same_educational_state_always_generates_same_mission() -> None:
    twin = make_twin()
    diagnosis = make_aligned_diagnosis()
    priority = make_aligned_priority()
    strategy = make_aligned_strategy(with_secondaries=True)

    first = MissionGenerator.generate(twin, diagnosis, priority, strategy)
    second = MissionGenerator.generate(twin, diagnosis, priority, strategy)

    assert first == second
    assert first.mission_id == second.mission_id
    assert first.sequence == second.sequence
    assert first.duration == second.duration
    assert first.priority == second.priority
    assert first.educational_rationale == second.educational_rationale
    assert first.success_criteria == second.success_criteria
    assert first.completion_conditions == second.completion_conditions


def test_repeated_generation_is_stable_across_many_runs() -> None:
    twin = make_twin()
    diagnosis = make_aligned_diagnosis()
    priority = make_aligned_priority(score_band=PriorityScoreBand.CRITICAL)
    strategy = make_aligned_strategy(with_secondaries=True)
    missions = [
        MissionGenerator.generate(twin, diagnosis, priority, strategy)
        for _ in range(20)
    ]
    assert all(m == missions[0] for m in missions)


def test_mission_id_is_deterministic_from_input_identities() -> None:
    mission = generate_mission()
    assert mission.mission_id.value == "msn-twin-001-diag-001-prio-001-ts-001"


def test_different_input_identities_change_mission_id() -> None:
    a = generate_mission(strategy=make_aligned_strategy(strategy_id="ts-a"))
    b = generate_mission(strategy=make_aligned_strategy(strategy_id="ts-b"))
    assert a.mission_id != b.mission_id
    assert a.strategy_id != b.strategy_id
