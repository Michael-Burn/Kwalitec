"""Mission warrant / cold-start posture vocabulary.

Inherits Decision warrant honesty. Never coerces unknown / low warrant /
``not_yet_knowable`` into Mid or High preparedness theatre.
"""

from __future__ import annotations

from enum import StrEnum

from app.domain.decision.decision import DecisionWarrantPosture


class MissionWarrantPosture(StrEnum):
    """Evidence-density honesty inherited onto Mission composition.

    Thin / cold-start / not_yet_knowable remain first-class. Never rewrite
    into Mid or High preparedness claims under thin Decision warrant.
    """

    HONEST_LOW = "honest_low"
    COLD_START = "cold_start"
    NOT_YET_KNOWABLE = "not_yet_knowable"
    HONEST_MEDIUM = "honest_medium"
    HONEST_HIGH = "honest_high"


_WARRANT_TO_MISSION: dict[DecisionWarrantPosture, MissionWarrantPosture] = {
    DecisionWarrantPosture.COLD_START: MissionWarrantPosture.COLD_START,
    DecisionWarrantPosture.NOT_YET_KNOWABLE: MissionWarrantPosture.NOT_YET_KNOWABLE,
    DecisionWarrantPosture.INHERITED_LOW: MissionWarrantPosture.HONEST_LOW,
    DecisionWarrantPosture.INHERITED_MEDIUM: MissionWarrantPosture.HONEST_MEDIUM,
    DecisionWarrantPosture.INHERITED_HIGH: MissionWarrantPosture.HONEST_HIGH,
}


# Postures that must never be narrated as Mid/High preparedness packing.
THIN_MISSION_WARRANT_POSTURES: frozenset[MissionWarrantPosture] = frozenset(
    {
        MissionWarrantPosture.HONEST_LOW,
        MissionWarrantPosture.COLD_START,
        MissionWarrantPosture.NOT_YET_KNOWABLE,
    }
)


def inherit_mission_warrant(
    warrant: DecisionWarrantPosture | str,
) -> MissionWarrantPosture:
    """Propagate Decision warrant honesty into Mission warrant posture.

    Args:
        warrant: Decision warrant posture (inherited from readiness).

    Returns:
        Matching Mission warrant honesty posture.
    """
    posture = (
        warrant
        if isinstance(warrant, DecisionWarrantPosture)
        else DecisionWarrantPosture(warrant)
    )
    return _WARRANT_TO_MISSION[posture]


def aggregate_mission_warrant(
    warrants: list[DecisionWarrantPosture] | tuple[DecisionWarrantPosture, ...],
) -> MissionWarrantPosture:
    """Aggregate batch Decision warrants with thin-warrant precedence.

    Cold-start / not_yet_knowable / low win over medium / high so a batch
    never coerces honesty upward.
    """
    if not warrants:
        raise ValueError("at least one Decision warrant is required")
    inherited = [inherit_mission_warrant(w) for w in warrants]
    precedence = (
        MissionWarrantPosture.NOT_YET_KNOWABLE,
        MissionWarrantPosture.COLD_START,
        MissionWarrantPosture.HONEST_LOW,
        MissionWarrantPosture.HONEST_MEDIUM,
        MissionWarrantPosture.HONEST_HIGH,
    )
    for posture in precedence:
        if posture in inherited:
            return posture
    return inherited[0]
