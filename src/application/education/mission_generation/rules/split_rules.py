"""SplitRules — split oversized missions into manageable chunks."""

from __future__ import annotations

from collections.abc import Sequence

from application.education.mission_generation.ids import MissionId, MissionStepId
from application.education.mission_generation.models.mission import Mission
from application.education.mission_generation.models.mission_estimate import (
    MissionEstimate,
)
from application.education.mission_generation.models.mission_ordering import (
    MissionOrdering,
)
from application.education.mission_generation.models.mission_step import MissionStep
from application.education.mission_generation.rules.mapping_rules import MappingRules


class SplitRules:
    """Split large missions into manageable, ordered chunks."""

    @staticmethod
    def needs_split(mission: Mission, *, maximum_mission_minutes: int) -> bool:
        return mission.estimate.duration_minutes > maximum_mission_minutes

    @staticmethod
    def split_large_missions(
        missions: Sequence[Mission],
        *,
        maximum_mission_minutes: int,
    ) -> tuple[Mission, ...]:
        """Split any mission exceeding ``maximum_mission_minutes``.

        Chunks preserve mission type, objective, recurrence, and source
        recommendation ids. Duration is divided evenly across chunks with
        remainder minutes applied to the earliest chunks.
        """
        if maximum_mission_minutes < 1:
            maximum_mission_minutes = 1

        result: list[Mission] = []
        for mission in missions:
            if not SplitRules.needs_split(
                mission, maximum_mission_minutes=maximum_mission_minutes
            ):
                result.append(mission)
                continue
            result.extend(
                SplitRules._split_one(
                    mission, maximum_mission_minutes=maximum_mission_minutes
                )
            )
        return tuple(result)

    @staticmethod
    def _split_one(
        mission: Mission, *, maximum_mission_minutes: int
    ) -> tuple[Mission, ...]:
        total = mission.estimate.duration_minutes
        chunk_count = (total + maximum_mission_minutes - 1) // maximum_mission_minutes
        base = total // chunk_count
        remainder = total % chunk_count
        chunks: list[Mission] = []
        for index in range(1, chunk_count + 1):
            minutes = base + (1 if index <= remainder else 0)
            minutes = max(1, minutes)
            workload = round(
                mission.estimate.workload_units * (minutes / total),
                4,
            )
            step_action = MappingRules.step_action_for(mission.mission_type)
            step = MissionStep(
                step_id=MissionStepId(f"{mission.mission_id.value}:s{index}"),
                action=step_action,
                order=1,
                estimated_minutes=minutes,
                subject_id=mission.subject_id,
                competency_id=mission.competency_id,
                action_detail=f"chunk:{index}/{chunk_count}",
            )
            chunk_id = MissionId(f"{mission.mission_id.value}:c{index}")
            chunks.append(
                Mission(
                    mission_id=chunk_id,
                    mission_type=mission.mission_type,
                    objective=mission.objective,
                    estimate=MissionEstimate(
                        duration_minutes=minutes,
                        workload_units=max(0.1, workload),
                    ),
                    ordering=MissionOrdering(
                        rank=mission.ordering.rank,
                        priority_magnitude=mission.ordering.priority_magnitude,
                    ),
                    steps=(step,),
                    constraints=mission.constraints,
                    source_recommendation_ids=mission.source_recommendation_ids,
                    subject_id=mission.subject_id,
                    competency_id=mission.competency_id,
                    recurrence=mission.recurrence,
                    chunk_index=index,
                    chunk_count=chunk_count,
                )
            )
        return tuple(chunks)
