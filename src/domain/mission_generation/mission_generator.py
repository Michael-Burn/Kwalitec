"""MissionGenerator — deterministic MissionSpecification from Educational OS.

Architecture Source
    EDUCATIONAL_ORCHESTRATION_MODEL.md
    STRATEGY_COMPOSITION_MODEL.md
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    Mission Generation

Rules
    No AI. No prompting. No randomness.
    Same educational state always yields the same MissionSpecification.
"""

from __future__ import annotations

from domain.education.diagnosis.aggregates.educational_diagnosis import (
    EducationalDiagnosis,
)
from domain.education.diagnosis.enums import DiagnosisSeverityLevel, DiagnosisStatus
from domain.education.digital_twin.aggregates.educational_digital_twin import (
    EducationalDigitalTwin,
)
from domain.education.digital_twin.enums import TwinStatus
from domain.education.digital_twin.value_objects.learning_trajectory import (
    LearningTrajectory,
)
from domain.education.foundation.enums import TeachingStrategyType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.priority.aggregates.educational_priority import (
    EducationalPriority,
)
from domain.education.priority.enums import PriorityScoreBand, PriorityStatus
from domain.education.teaching_strategy.aggregates.teaching_strategy import (
    TeachingStrategy,
)
from domain.education.teaching_strategy.enums import ComplexityLevel, StrategyStatus
from domain.mission_generation.enums import (
    CompletionConditionCode,
    MissionPriorityBand,
)
from domain.mission_generation.ids import (
    MissionObjectiveId,
    MissionSpecificationId,
    MissionTaskId,
)
from domain.mission_generation.mission_duration import MissionDuration
from domain.mission_generation.mission_objective import MissionObjective
from domain.mission_generation.mission_priority import MissionPriority
from domain.mission_generation.mission_sequence import MissionSequence
from domain.mission_generation.mission_specification import (
    CompletionCondition,
    MissionSpecification,
    SuccessCriterion,
)
from domain.mission_generation.mission_task import MissionTask

# Fixed base minutes per strategy type (deterministic catalogue).
_STRATEGY_BASE_MINUTES: dict[TeachingStrategyType, int] = {
    TeachingStrategyType.DIRECT_EXPLANATION: 8,
    TeachingStrategyType.ANALOGY: 7,
    TeachingStrategyType.WORKED_EXAMPLE: 10,
    TeachingStrategyType.GUIDED_DISCOVERY: 12,
    TeachingStrategyType.SOCRATIC_QUESTIONING: 10,
    TeachingStrategyType.RETRIEVAL_FIRST: 8,
    TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION: 8,
    TeachingStrategyType.CONCEPT_COMPARISON: 10,
    TeachingStrategyType.COUNTEREXAMPLE: 8,
    TeachingStrategyType.MISCONCEPTION_CONFRONTATION: 12,
    TeachingStrategyType.PROGRESSIVE_SCAFFOLDING: 12,
    TeachingStrategyType.FADED_GUIDANCE: 10,
    TeachingStrategyType.DELIBERATE_PRACTICE: 15,
    TeachingStrategyType.INTERLEAVING: 12,
    TeachingStrategyType.SPACED_REINFORCEMENT: 8,
    TeachingStrategyType.DUAL_REPRESENTATION: 10,
    TeachingStrategyType.CONCEPT_MAPPING: 12,
    TeachingStrategyType.ERROR_LED_TEACHING: 10,
    TeachingStrategyType.THINK_ALOUD_MODELLING: 9,
    TeachingStrategyType.EXAM_SIMULATION: 20,
}

_COMPLEXITY_NUMERATOR: dict[ComplexityLevel, int] = {
    ComplexityLevel.LOW: 10,
    ComplexityLevel.MODERATE: 12,
    ComplexityLevel.HIGH: 14,
    ComplexityLevel.VERY_HIGH: 16,
}

_SEVERITY_ADD_MINUTES: dict[DiagnosisSeverityLevel, int] = {
    DiagnosisSeverityLevel.MILD: 0,
    DiagnosisSeverityLevel.MODERATE: 1,
    DiagnosisSeverityLevel.SUBSTANTIAL: 2,
    DiagnosisSeverityLevel.SEVERE: 3,
}

_PRIORITY_BAND_MAP: dict[PriorityScoreBand, MissionPriorityBand] = {
    PriorityScoreBand.NEGLIGIBLE: MissionPriorityBand.NEGLIGIBLE,
    PriorityScoreBand.LOW: MissionPriorityBand.LOW,
    PriorityScoreBand.MEDIUM: MissionPriorityBand.MEDIUM,
    PriorityScoreBand.HIGH: MissionPriorityBand.HIGH,
    PriorityScoreBand.CRITICAL: MissionPriorityBand.CRITICAL,
}

_TASK_LABELS: dict[TeachingStrategyType, str] = {
    TeachingStrategyType.DIRECT_EXPLANATION: "Explain the target concept directly",
    TeachingStrategyType.ANALOGY: "Build intuition through analogy",
    TeachingStrategyType.WORKED_EXAMPLE: "Study a worked example",
    TeachingStrategyType.GUIDED_DISCOVERY: "Discover the relation with guidance",
    TeachingStrategyType.SOCRATIC_QUESTIONING: "Probe understanding through questions",
    TeachingStrategyType.RETRIEVAL_FIRST: "Retrieve prior knowledge first",
    TeachingStrategyType.RETRIEVAL_AFTER_INSTRUCTION: (
        "Retrieve after instruction to consolidate"
    ),
    TeachingStrategyType.CONCEPT_COMPARISON: "Compare related concepts",
    TeachingStrategyType.COUNTEREXAMPLE: "Test boundaries with a counterexample",
    TeachingStrategyType.MISCONCEPTION_CONFRONTATION: (
        "Confront the active misconception"
    ),
    TeachingStrategyType.PROGRESSIVE_SCAFFOLDING: (
        "Practise with progressive scaffolds"
    ),
    TeachingStrategyType.FADED_GUIDANCE: "Practise as scaffolds fade",
    TeachingStrategyType.DELIBERATE_PRACTICE: "Deliberate practice on the target skill",
    TeachingStrategyType.INTERLEAVING: "Interleave related problem types",
    TeachingStrategyType.SPACED_REINFORCEMENT: "Reinforce with spaced retrieval",
    TeachingStrategyType.DUAL_REPRESENTATION: "Link dual representations",
    TeachingStrategyType.CONCEPT_MAPPING: "Map concept relations",
    TeachingStrategyType.ERROR_LED_TEACHING: "Learn from the diagnosed error pattern",
    TeachingStrategyType.THINK_ALOUD_MODELLING: "Model expert think-aloud reasoning",
    TeachingStrategyType.EXAM_SIMULATION: "Simulate exam conditions",
}


class MissionGenerator:
    """Pure domain service that generates MissionSpecifications.

    Generation is fully deterministic and explainable from Educational OS
    inputs. No AI, no prompting, no randomness, no wall-clock dependence.
    """

    @classmethod
    def generate(
        cls,
        twin: EducationalDigitalTwin,
        diagnosis: EducationalDiagnosis,
        priority: EducationalPriority,
        strategy: TeachingStrategy,
        trajectory: LearningTrajectory | None = None,
    ) -> MissionSpecification:
        """Generate a MissionSpecification from Educational OS state.

        Args:
            twin: Educational Digital Twin (learner memory).
            diagnosis: Named educational deficiency to address.
            priority: Instructional ordering of the diagnosed need.
            strategy: Selected teaching strategy commitment.
            trajectory: Optional LearningTrajectory override; defaults to
                ``twin.trajectory``.

        Returns:
            Immutable MissionSpecification with objective, duration, priority,
            ordered tasks, success criteria, completion conditions, and
            educational rationale.

        Raises:
            EducationalInvariantViolation: When inputs are educationally
                inconsistent or not ready for mission generation.
        """
        learning_trajectory = (
            trajectory if trajectory is not None else twin.trajectory
        )
        cls._assert_inputs(twin, diagnosis, priority, strategy, learning_trajectory)

        mission_id = cls._mission_id(twin, diagnosis, priority, strategy)
        objective = cls._build_objective(diagnosis, strategy)
        mission_priority = cls._map_priority(priority)
        sequence = cls._build_sequence(diagnosis, strategy)
        duration = MissionDuration.of(sequence.total_estimated_minutes())
        success_criteria = cls._build_success_criteria(diagnosis, strategy)
        completion_conditions = cls._build_completion_conditions(strategy, sequence)
        rationale = cls._build_rationale(
            twin=twin,
            diagnosis=diagnosis,
            priority=priority,
            strategy=strategy,
            trajectory=learning_trajectory,
            sequence=sequence,
            duration=duration,
            mission_priority=mission_priority,
        )

        return MissionSpecification(
            mission_id=mission_id,
            student_id=twin.student_id,
            objective=objective,
            duration=duration,
            priority=mission_priority,
            sequence=sequence,
            success_criteria=success_criteria,
            completion_conditions=completion_conditions,
            educational_rationale=rationale,
            twin_id=twin.twin_id,
            diagnosis_id=diagnosis.diagnosis_id,
            priority_id=priority.priority_id,
            strategy_id=strategy.strategy_id,
        )

    # --- validation ---------------------------------------------------------

    @staticmethod
    def _assert_inputs(
        twin: EducationalDigitalTwin,
        diagnosis: EducationalDiagnosis,
        priority: EducationalPriority,
        strategy: TeachingStrategy,
        trajectory: LearningTrajectory,
    ) -> None:
        if not isinstance(twin, EducationalDigitalTwin):
            raise EducationalInvariantViolation(
                "twin must be an EducationalDigitalTwin",
                invariant="MissionGenerator.twin.type",
            )
        if not isinstance(diagnosis, EducationalDiagnosis):
            raise EducationalInvariantViolation(
                "diagnosis must be an EducationalDiagnosis",
                invariant="MissionGenerator.diagnosis.type",
            )
        if not isinstance(priority, EducationalPriority):
            raise EducationalInvariantViolation(
                "priority must be an EducationalPriority",
                invariant="MissionGenerator.priority.type",
            )
        if not isinstance(strategy, TeachingStrategy):
            raise EducationalInvariantViolation(
                "strategy must be a TeachingStrategy",
                invariant="MissionGenerator.strategy.type",
            )
        if not isinstance(trajectory, LearningTrajectory):
            raise EducationalInvariantViolation(
                "trajectory must be a LearningTrajectory",
                invariant="MissionGenerator.trajectory.type",
            )

        student_ids = {
            twin.student_id,
            diagnosis.student_id,
            priority.student_id,
            strategy.student_id,
        }
        if len(student_ids) != 1:
            raise EducationalInvariantViolation(
                "twin, diagnosis, priority, and strategy must share student_id",
                invariant="MissionGenerator.student_alignment",
            )

        if twin.status is TwinStatus.ARCHIVED:
            raise EducationalInvariantViolation(
                "cannot generate a mission from an archived twin",
                invariant="MissionGenerator.twin.active",
            )
        if diagnosis.status is DiagnosisStatus.INVALIDATED:
            raise EducationalInvariantViolation(
                "cannot generate a mission from an invalidated diagnosis",
                invariant="MissionGenerator.diagnosis.active",
            )
        if priority.status not in {
            PriorityStatus.ASSIGNED,
            PriorityStatus.REVISED,
            PriorityStatus.STABILISED,
        }:
            raise EducationalInvariantViolation(
                "priority must be assigned, revised, or stabilised",
                invariant="MissionGenerator.priority.status",
            )
        if strategy.status not in {
            StrategyStatus.SELECTED,
            StrategyStatus.REVISED,
        }:
            raise EducationalInvariantViolation(
                "strategy must be selected or revised before mission generation",
                invariant="MissionGenerator.strategy.committed",
            )

        if not any(
            ref.diagnosis_id == diagnosis.diagnosis_id
            for ref in priority.diagnosis_references
        ):
            raise EducationalInvariantViolation(
                "priority must reference the provided diagnosis",
                invariant="MissionGenerator.priority.diagnosis_link",
            )
        if not any(
            ref.diagnosis_id == diagnosis.diagnosis_id
            for ref in strategy.diagnosis_references
        ):
            raise EducationalInvariantViolation(
                "strategy must reference the provided diagnosis",
                invariant="MissionGenerator.strategy.diagnosis_link",
            )

    # --- identity -----------------------------------------------------------

    @staticmethod
    def _mission_id(
        twin: EducationalDigitalTwin,
        diagnosis: EducationalDiagnosis,
        priority: EducationalPriority,
        strategy: TeachingStrategy,
    ) -> MissionSpecificationId:
        return MissionSpecificationId(
            f"msn-{twin.twin_id.value}-{diagnosis.diagnosis_id.value}"
            f"-{priority.priority_id.value}-{strategy.strategy_id.value}"
        )

    # --- objective ----------------------------------------------------------

    @classmethod
    def _build_objective(
        cls,
        diagnosis: EducationalDiagnosis,
        strategy: TeachingStrategy,
    ) -> MissionObjective:
        concept_ids = tuple(
            sorted(diagnosis.scope.concept_ids(), key=lambda c: c.value)
        )
        statement = (
            f"Address {diagnosis.diagnosis_type.value.replace('_', ' ')} "
            f"using {strategy.primary_strategy.value.replace('_', ' ')}: "
            f"{strategy.goal.statement}"
        )
        return MissionObjective(
            objective_id=MissionObjectiveId(
                f"obj-{diagnosis.diagnosis_id.value}-{strategy.strategy_id.value}"
            ),
            statement=statement,
            diagnosis_type=diagnosis.diagnosis_type,
            primary_strategy=strategy.primary_strategy,
            concept_ids=concept_ids,
            learning_dimension=diagnosis.scope.learning_dimension,
            scope_statement=diagnosis.scope.statement,
        )

    # --- priority mapping ---------------------------------------------------

    @staticmethod
    def _map_priority(priority: EducationalPriority) -> MissionPriority:
        band = _PRIORITY_BAND_MAP[priority.score.band]
        peak = priority.peak_factor()
        rationale = (
            f"Mapped from educational priority {priority.score.band.value} "
            f"with urgency {priority.urgency.level.value}; peak factor "
            f"{peak.kind.value}"
        )
        return MissionPriority.of(
            band,
            priority.urgency.level,
            ratio=priority.score.ratio,
            rationale=rationale,
        )

    # --- sequence / duration ------------------------------------------------

    @classmethod
    def _build_sequence(
        cls,
        diagnosis: EducationalDiagnosis,
        strategy: TeachingStrategy,
    ) -> MissionSequence:
        composition = strategy.composition_sequence()
        tasks: list[MissionTask] = []
        for index, strategy_type in enumerate(composition, start=1):
            minutes = cls._task_minutes(strategy_type, diagnosis, strategy)
            tasks.append(
                MissionTask(
                    task_id=MissionTaskId(
                        f"task-{strategy.strategy_id.value}-{index:02d}-"
                        f"{strategy_type.value}"
                    ),
                    sequence_index=index,
                    strategy_type=strategy_type,
                    label=_TASK_LABELS[strategy_type],
                    estimated_minutes=minutes,
                    required=True,
                    success_hint=cls._task_success_hint(strategy_type, strategy),
                )
            )
        return MissionSequence.of(*tasks)

    @classmethod
    def _task_minutes(
        cls,
        strategy_type: TeachingStrategyType,
        diagnosis: EducationalDiagnosis,
        strategy: TeachingStrategy,
    ) -> int:
        base = _STRATEGY_BASE_MINUTES[strategy_type]
        complexity_n = _COMPLEXITY_NUMERATOR[strategy.complexity.level]
        # Integer arithmetic only: floor((base * numerator) / 10)
        scaled = (base * complexity_n) // 10
        severity_add = _SEVERITY_ADD_MINUTES[diagnosis.severity.level]
        # Primary task absorbs severity; follow-ons do not (deterministic).
        if strategy_type is strategy.primary_strategy:
            return max(1, scaled + severity_add)
        return max(1, scaled)

    @staticmethod
    def _task_success_hint(
        strategy_type: TeachingStrategyType,
        strategy: TeachingStrategy,
    ) -> str:
        if (
            strategy_type is strategy.primary_strategy
            and strategy.goal.expected_evidence_hint is not None
        ):
            return strategy.goal.expected_evidence_hint
        return (
            f"Complete {strategy_type.value.replace('_', ' ')} "
            "with observable engagement"
        )

    # --- success / completion -----------------------------------------------

    @staticmethod
    def _build_success_criteria(
        diagnosis: EducationalDiagnosis,
        strategy: TeachingStrategy,
    ) -> tuple[SuccessCriterion, ...]:
        criteria: list[SuccessCriterion] = [
            SuccessCriterion(
                statement=(
                    f"Produce evidence consistent with addressing "
                    f"{diagnosis.diagnosis_type.value.replace('_', ' ')}"
                ),
                code="diagnosis_addressed",
            ),
            SuccessCriterion(
                statement=strategy.goal.statement,
                code="strategy_goal_advanced",
            ),
        ]
        if strategy.goal.expected_evidence_hint is not None:
            criteria.append(
                SuccessCriterion(
                    statement=strategy.goal.expected_evidence_hint,
                    code="expected_evidence",
                )
            )
        criteria.append(
            SuccessCriterion(
                statement=(
                    f"Advance instructional priority "
                    f"{diagnosis.diagnosis_type.value} within scope "
                    f"'{diagnosis.scope.statement}'"
                ),
                code="priority_scope_advanced",
            )
        )
        return tuple(criteria)

    @staticmethod
    def _build_completion_conditions(
        strategy: TeachingStrategy,
        sequence: MissionSequence,
    ) -> tuple[CompletionCondition, ...]:
        required_count = len(sequence.required_tasks())
        return (
            CompletionCondition(
                statement=(
                    f"Complete all {required_count} required mission tasks "
                    f"in educational order"
                ),
                code=CompletionConditionCode.ALL_TASKS_COMPLETED,
            ),
            CompletionCondition(
                statement=(
                    f"Engage primary strategy "
                    f"{strategy.primary_strategy.value.replace('_', ' ')}"
                ),
                code=CompletionConditionCode.PRIMARY_STRATEGY_ENGAGED,
            ),
            CompletionCondition(
                statement="Satisfy declared success criteria for the sitting",
                code=CompletionConditionCode.SUCCESS_CRITERIA_MET,
            ),
            CompletionCondition(
                statement="Capture educational evidence attributable to this mission",
                code=CompletionConditionCode.EVIDENCE_CAPTURED,
            ),
        )

    # --- rationale ----------------------------------------------------------

    @classmethod
    def _build_rationale(
        cls,
        *,
        twin: EducationalDigitalTwin,
        diagnosis: EducationalDiagnosis,
        priority: EducationalPriority,
        strategy: TeachingStrategy,
        trajectory: LearningTrajectory,
        sequence: MissionSequence,
        duration: MissionDuration,
        mission_priority: MissionPriority,
    ) -> str:
        concept_ids = sorted(
            (c.value for c in diagnosis.scope.concept_ids()),
        )
        concepts = ", ".join(concept_ids) if concept_ids else "unscoped-concept"
        peak = priority.peak_factor()
        composition = " → ".join(
            task.strategy_type.value for task in sequence.tasks
        )
        last = trajectory.last()
        trajectory_clause = (
            f"Learning trajectory length {trajectory.length()}"
            + (
                f"; last point {last.kind.value}:{last.label}"
                if last is not None
                else "; empty trajectory beyond generation inputs"
            )
        )
        twin_memory = (
            f"Twin {twin.twin_id.value} remembers "
            f"{twin.concept_count()} concept state(s) and "
            f"{twin.misconception_count()} misconception state(s)"
        )
        return (
            f"Mission addresses diagnosis {diagnosis.diagnosis_type.value} "
            f"(severity {diagnosis.severity.level.value}) for concepts [{concepts}] "
            f"because priority band {mission_priority.band.value} "
            f"(urgency {mission_priority.urgency.value}, peak factor "
            f"{peak.kind.value}) requires this instructional work next. "
            f"Teaching strategy {strategy.primary_strategy.value} is committed "
            f"with rationale: {strategy.rationale.statement}. "
            f"Ordered task arc: {composition}. "
            f"Estimated duration {duration.planned_minutes} minutes "
            f"({duration.band.value}). {twin_memory}. {trajectory_clause}."
        )


# Public helper for tests / callers that only need priority mapping.
def map_priority_band(band: PriorityScoreBand) -> MissionPriorityBand:
    """Map an Educational Priority score band to a MissionPriorityBand."""
    try:
        return _PRIORITY_BAND_MAP[band]
    except KeyError as exc:
        raise EducationalInvariantViolation(
            "unknown priority score band",
            invariant="MissionGenerator.priority_band.unknown",
        ) from exc


def base_minutes_for(strategy_type: TeachingStrategyType) -> int:
    """Return the fixed base minutes catalogue entry for a strategy type."""
    try:
        return _STRATEGY_BASE_MINUTES[strategy_type]
    except KeyError as exc:
        raise EducationalInvariantViolation(
            "unknown teaching strategy type for duration catalogue",
            invariant="MissionGenerator.duration.unknown_strategy",
        ) from exc
