"""ConstraintRules — project planning and recommendation constraints."""

from __future__ import annotations

from collections.abc import Sequence

from application.education.mission_generation.enums import MissionConstraintKind
from application.education.mission_generation.models.mission_constraint import (
    MissionConstraint,
)
from application.education.mission_generation.planning_constraints import (
    PlanningConstraints,
)
from domain.education.recommendation_engine.enums import RecommendationConstraintKind
from domain.education.recommendation_engine.value_objects.recommendation_constraint import (  # noqa: E501
    RecommendationConstraint,
)


class ConstraintRules:
    """Project recommendation and planning constraints onto mission plans."""

    @staticmethod
    def from_recommendation_constraints(
        constraints: Sequence[RecommendationConstraint],
    ) -> tuple[MissionConstraint, ...]:
        projected: list[MissionConstraint] = []
        for constraint in constraints:
            kind = ConstraintRules._map_kind(constraint.kind)
            if kind is None:
                continue
            projected.append(
                MissionConstraint(
                    kind=kind,
                    subject_id=(
                        constraint.subject_id.value
                        if constraint.subject_id is not None
                        else None
                    ),
                    competency_id=(
                        constraint.competency_id.value
                        if constraint.competency_id is not None
                        else None
                    ),
                    detail=constraint.detail,
                )
            )
        return tuple(projected)

    @staticmethod
    def from_planning_constraints(
        planning: PlanningConstraints | None,
    ) -> tuple[MissionConstraint, ...]:
        if planning is None:
            return ()
        projected: list[MissionConstraint] = []
        if planning.available_study_minutes is not None:
            projected.append(
                MissionConstraint(
                    kind=MissionConstraintKind.RESPECT_AVAILABLE_TIME,
                    detail=float(planning.available_study_minutes),
                )
            )
        if planning.maximum_daily_workload_minutes is not None:
            projected.append(
                MissionConstraint(
                    kind=MissionConstraintKind.LIMIT_DAILY_WORKLOAD,
                    detail=float(planning.maximum_daily_workload_minutes),
                )
            )
        if planning.target_examination is not None:
            projected.append(
                MissionConstraint(
                    kind=MissionConstraintKind.TARGET_EXAMINATION,
                    label=planning.target_examination,
                )
            )
        for mission_type in planning.preferred_mission_types:
            projected.append(
                MissionConstraint(
                    kind=MissionConstraintKind.PREFER_MISSION_TYPE,
                    label=mission_type.value,
                )
            )
        return tuple(projected)

    @staticmethod
    def aggregate(
        *groups: Sequence[MissionConstraint],
    ) -> tuple[MissionConstraint, ...]:
        seen: set[tuple] = set()
        result: list[MissionConstraint] = []
        for group in groups:
            for constraint in group:
                key = (
                    constraint.kind.value,
                    constraint.subject_id,
                    constraint.competency_id,
                    constraint.detail,
                    constraint.label,
                )
                if key in seen:
                    continue
                seen.add(key)
                result.append(constraint)
        return tuple(result)

    @staticmethod
    def _map_kind(
        kind: RecommendationConstraintKind,
    ) -> MissionConstraintKind | None:
        mapping = {
            RecommendationConstraintKind.REQUIRE_PREREQUISITE: (
                MissionConstraintKind.REQUIRE_PREREQUISITE_FIRST
            ),
            RecommendationConstraintKind.BLOCK_ADVANCEMENT: (
                MissionConstraintKind.BLOCK_ADVANCEMENT
            ),
            RecommendationConstraintKind.LIMIT_SCOPE: (
                MissionConstraintKind.LIMIT_DAILY_WORKLOAD
            ),
        }
        return mapping.get(kind)
