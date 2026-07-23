"""AdaptiveMissionGenerator — RecommendationSet → MissionPlan.

Architecture Source
    PRD-001 Adaptive Mission Generator

Transforms an immutable RecommendationSet into an executable MissionPlan.
Consumes educational decisions and produces learning work.

Must not:
- generate educational recommendations
- estimate mastery
- modify StudentEducationalState
- persist, call Flask/SQLAlchemy, invoke AI, or use randomness

Every method is a pure function of its explicit, caller-supplied inputs —
the same inputs always produce the same output. Callers always supply
``generated_at`` / plan identity explicitly.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime

from application.education.mission_generation.enums import (
    LearningPace,
    MissionConstraintKind,
    MissionRecurrenceBand,
    MissionType,
)
from application.education.mission_generation.errors import MissionGenerationError
from application.education.mission_generation.ids import (
    MissionId,
    MissionPlanId,
    MissionStepId,
)
from application.education.mission_generation.models.mission import Mission
from application.education.mission_generation.models.mission_constraint import (
    MissionConstraint,
)
from application.education.mission_generation.models.mission_estimate import (
    MissionEstimate,
)
from application.education.mission_generation.models.mission_objective import (
    MissionObjective,
)
from application.education.mission_generation.models.mission_ordering import (
    MissionOrdering,
)
from application.education.mission_generation.models.mission_plan import MissionPlan
from application.education.mission_generation.models.mission_snapshot import (
    MissionSnapshot,
)
from application.education.mission_generation.models.mission_step import MissionStep
from application.education.mission_generation.planning_constraints import (
    PlanningConstraints,
)
from application.education.mission_generation.rules.constraint_rules import (
    ConstraintRules,
)
from application.education.mission_generation.rules.duration_rules import DurationRules
from application.education.mission_generation.rules.mapping_rules import (
    MappingRules,
    MissionIntent,
)
from application.education.mission_generation.rules.merge_rules import (
    MergedRecommendationGroup,
    MergeRules,
)
from application.education.mission_generation.rules.ordering_rules import OrderingRules
from application.education.mission_generation.rules.split_rules import SplitRules
from domain.education.recommendation_engine.aggregates.recommendation_set import (
    RecommendationSet,
)
from domain.education.recommendation_engine.value_objects.recommendation import (
    Recommendation,
)


class AdaptiveMissionGenerator:
    """Deterministic generator producing MissionPlan from RecommendationSet.

    Pure application composition. Domain RecommendationEngine remains the
    sole producer of educational recommendations; this generator only
    transforms those decisions into executable learning work.
    """

    # --- top-level generation -----------------------------------------------

    @staticmethod
    def generate(
        recommendation_set: RecommendationSet,
        *,
        plan_id: MissionPlanId,
        generated_at: datetime,
        planning_constraints: PlanningConstraints | None = None,
    ) -> MissionPlan:
        """Transform a full RecommendationSet into a MissionPlan.

        Pipeline (deterministic):
        1. Merge similar recommendations
        2. Build missions from merged groups
        3. Split oversized missions
        4. Prioritise (prerequisites before dependents)
        5. Apply daily/available time caps when provided
        6. Attach projected constraints
        """
        AdaptiveMissionGenerator._assert_inputs(
            recommendation_set, plan_id=plan_id, generated_at=generated_at
        )
        constraints = planning_constraints or PlanningConstraints()

        groups = AdaptiveMissionGenerator.merge_similar_recommendations(
            recommendation_set.recommendations
        )
        missions = tuple(
            AdaptiveMissionGenerator._mission_from_group(
                group,
                plan_id=plan_id,
                ordinal=index,
                learning_pace=constraints.learning_pace,
            )
            for index, group in enumerate(groups, start=1)
        )
        missions = AdaptiveMissionGenerator.split_large_missions(
            missions,
            maximum_mission_minutes=constraints.maximum_mission_minutes,
        )
        missions = AdaptiveMissionGenerator.prioritise(missions)
        missions = AdaptiveMissionGenerator._apply_time_cap(
            missions, constraints.effective_daily_cap_minutes()
        )
        missions = AdaptiveMissionGenerator.prioritise(missions)

        plan_constraints = ConstraintRules.aggregate(
            ConstraintRules.from_recommendation_constraints(
                recommendation_set.constraints
            ),
            ConstraintRules.from_planning_constraints(constraints),
            AdaptiveMissionGenerator._recurrence_constraints(missions),
        )
        return MissionPlan(
            plan_id=plan_id,
            student_id=recommendation_set.student_id,
            source_recommendation_set_id=recommendation_set.set_id.value,
            generated_at=generated_at,
            missions=missions,
            constraints=plan_constraints,
        )

    @staticmethod
    def generate_daily_plan(
        recommendation_set: RecommendationSet,
        *,
        plan_id: MissionPlanId,
        generated_at: datetime,
        planning_constraints: PlanningConstraints | None = None,
    ) -> MissionPlan:
        """Generate a plan bounded by daily workload / available study time.

        Equivalent to ``generate`` with an explicit daily cap: when no cap is
        supplied, defaults to 60 minutes of daily workload.
        """
        base = planning_constraints or PlanningConstraints()
        if base.effective_daily_cap_minutes() is None:
            base = PlanningConstraints(
                available_study_minutes=base.available_study_minutes,
                target_examination=base.target_examination,
                preferred_mission_types=base.preferred_mission_types,
                learning_pace=base.learning_pace,
                maximum_daily_workload_minutes=60,
                maximum_mission_minutes=base.maximum_mission_minutes,
            )
        return AdaptiveMissionGenerator.generate(
            recommendation_set,
            plan_id=plan_id,
            generated_at=generated_at,
            planning_constraints=base,
        )

    @staticmethod
    def generate_single_mission(
        recommendation: Recommendation,
        *,
        mission_id: MissionId,
        learning_pace: LearningPace = LearningPace.NORMAL,
    ) -> Mission | None:
        """Generate one mission from a single recommendation.

        Returns ``None`` when the recommendation category does not produce
        a mission (for example DelayAdvancedTopic).
        """
        intent = MappingRules.resolve(recommendation)
        if intent is None:
            return None
        return AdaptiveMissionGenerator._build_mission(
            intent,
            mission_id=mission_id,
            learning_pace=learning_pace,
            rank=1,
        )

    # --- behaviours ---------------------------------------------------------

    @staticmethod
    def prioritise(missions: Sequence[Mission]) -> tuple[Mission, ...]:
        """Deterministically order missions for execution."""
        return OrderingRules.prioritise(missions)

    @staticmethod
    def estimate_duration(
        mission_type: MissionType,
        *,
        learning_pace: LearningPace = LearningPace.NORMAL,
        recurrence: MissionRecurrenceBand = MissionRecurrenceBand.NORMAL,
        coverage_weight: float = 1.0,
        source_count: int = 1,
    ) -> MissionEstimate:
        """Estimate duration for a mission type without generating a plan."""
        return DurationRules.estimate(
            mission_type,
            learning_pace=learning_pace,
            recurrence=recurrence,
            coverage_weight=coverage_weight,
            source_count=source_count,
        )

    @staticmethod
    def merge_similar_recommendations(
        recommendations: Sequence[Recommendation],
    ) -> tuple[MergedRecommendationGroup, ...]:
        """Merge related recommendations into coherent groups."""
        return MergeRules.merge_similar_recommendations(recommendations)

    @staticmethod
    def split_large_missions(
        missions: Sequence[Mission],
        *,
        maximum_mission_minutes: int,
    ) -> tuple[Mission, ...]:
        """Split oversized missions into manageable chunks."""
        return SplitRules.split_large_missions(
            missions, maximum_mission_minutes=maximum_mission_minutes
        )

    @staticmethod
    def produce_snapshot(mission_plan: MissionPlan) -> MissionSnapshot:
        """Produce an immutable snapshot of a mission plan."""
        return mission_plan.produce_snapshot()

    # --- internal builders --------------------------------------------------

    @staticmethod
    def _mission_from_group(
        group: MergedRecommendationGroup,
        *,
        plan_id: MissionPlanId,
        ordinal: int,
        learning_pace: LearningPace,
    ) -> Mission:
        mission_id = MissionId(f"{plan_id.value}:m{ordinal:04d}")
        return AdaptiveMissionGenerator._build_mission(
            group.intent,
            mission_id=mission_id,
            learning_pace=learning_pace,
            rank=ordinal,
            source_count=len(group.recommendations),
        )

    @staticmethod
    def _build_mission(
        intent: MissionIntent,
        *,
        mission_id: MissionId,
        learning_pace: LearningPace,
        rank: int,
        source_count: int = 1,
    ) -> Mission:
        estimate = DurationRules.estimate(
            intent.mission_type,
            learning_pace=learning_pace,
            recurrence=intent.recurrence,
            source_count=source_count,
        )
        objective = MissionObjective(
            code=intent.objective_code,
            subject_id=intent.subject_id,
            competency_id=intent.competency_id,
        )
        step = MissionStep(
            step_id=MissionStepId(f"{mission_id.value}:s1"),
            action=intent.step_action,
            order=1,
            estimated_minutes=estimate.duration_minutes,
            subject_id=intent.subject_id,
            competency_id=intent.competency_id,
            action_detail=intent.mission_type.value,
        )
        constraints: tuple[MissionConstraint, ...] = ()
        if intent.mission_type is MissionType.REVISE_PREREQUISITE:
            constraints = (
                MissionConstraint(
                    kind=MissionConstraintKind.REQUIRE_PREREQUISITE_FIRST,
                    subject_id=intent.subject_id,
                    competency_id=intent.competency_id,
                ),
            )
        return Mission(
            mission_id=mission_id,
            mission_type=intent.mission_type,
            objective=objective,
            estimate=estimate,
            ordering=MissionOrdering(
                rank=rank,
                priority_magnitude=intent.priority_magnitude,
            ),
            steps=(step,),
            constraints=constraints,
            source_recommendation_ids=intent.source_recommendation_ids,
            subject_id=intent.subject_id,
            competency_id=intent.competency_id,
            recurrence=intent.recurrence,
        )

    @staticmethod
    def _apply_time_cap(
        missions: Sequence[Mission],
        cap_minutes: int | None,
    ) -> tuple[Mission, ...]:
        if cap_minutes is None:
            return tuple(missions)
        selected: list[Mission] = []
        used = 0
        for mission in missions:
            if used + mission.estimate.duration_minutes > cap_minutes:
                # Always keep at least the first (highest priority) mission
                # even if it alone exceeds the cap — caller can split later.
                if not selected:
                    selected.append(mission)
                break
            selected.append(mission)
            used += mission.estimate.duration_minutes
        return tuple(selected)

    @staticmethod
    def _recurrence_constraints(
        missions: Sequence[Mission],
    ) -> tuple[MissionConstraint, ...]:
        constraints: list[MissionConstraint] = []
        for mission in missions:
            if mission.recurrence is MissionRecurrenceBand.INCREASED:
                constraints.append(
                    MissionConstraint(
                        kind=MissionConstraintKind.INCREASE_RECURRENCE,
                        subject_id=mission.subject_id,
                        competency_id=mission.competency_id,
                        detail=float(
                            DurationRules.sessions_per_week(mission.recurrence)
                        ),
                    )
                )
            elif mission.recurrence is MissionRecurrenceBand.REDUCED:
                constraints.append(
                    MissionConstraint(
                        kind=MissionConstraintKind.DECREASE_RECURRENCE,
                        subject_id=mission.subject_id,
                        competency_id=mission.competency_id,
                        detail=float(
                            DurationRules.sessions_per_week(mission.recurrence)
                        ),
                    )
                )
                constraints.append(
                    MissionConstraint(
                        kind=MissionConstraintKind.PRESERVE_COVERAGE,
                        subject_id=mission.subject_id,
                        competency_id=mission.competency_id,
                    )
                )
        return tuple(constraints)

    @staticmethod
    def _assert_inputs(
        recommendation_set: RecommendationSet,
        *,
        plan_id: MissionPlanId,
        generated_at: datetime,
    ) -> None:
        if not isinstance(recommendation_set, RecommendationSet):
            raise MissionGenerationError(
                "recommendation_set must be a RecommendationSet",
                code="invalid_recommendation_set",
            )
        if not isinstance(plan_id, MissionPlanId):
            raise MissionGenerationError(
                "plan_id must be a MissionPlanId",
                code="invalid_plan_id",
            )
        if not isinstance(generated_at, datetime):
            raise MissionGenerationError(
                "generated_at must be a datetime",
                code="invalid_generated_at",
            )
