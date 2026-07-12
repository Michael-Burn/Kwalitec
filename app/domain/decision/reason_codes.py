"""Stable reason-code vocabulary for Decision Engine authorship.

Versionable catalogue identities — not free-text slogans, not marketing copy.
Decision Engine alone authors reason codes for a Decision.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ReasonCodeFamily(StrEnum):
    """Reason-code families (architecture §9 / plan §6)."""

    CURRICULUM_WEIGHT = "curriculum_weight"
    KNOWLEDGE_GAP = "knowledge_gap"
    RETENTION_RISK = "retention_risk"
    ASSESSMENT_WARRANT_GAP = "assessment_warrant_gap"
    TIME_GOAL_PRESSURE = "time_goal_pressure"
    FEASIBILITY_DEMOTION = "feasibility_demotion"
    COLD_START_LOW_WARRANT = "cold_start_low_warrant"
    FACTOR_DISAGREEMENT = "factor_disagreement"
    HISTORY_ANTI_THRASH = "history_anti_thrash"
    CONFIDENCE_RISK_FRAMING = "confidence_risk_framing"


class ReasonCodeId(StrEnum):
    """Stable reason-code identities (versionable; additive only)."""

    # Curriculum weight
    HIGH_WEIGHT_COVERAGE = "high_weight_coverage"
    # Knowledge gap
    WEAK_OR_ABSENT_MASTERY = "weak_or_absent_mastery"
    # Retention risk
    MEMORY_STALENESS = "memory_staleness"
    # Assessment warrant
    THIN_PERFORMANCE_WARRANT = "thin_performance_warrant"
    # Time / goal pressure
    SITTING_TIME_PRESSURE = "sitting_time_pressure"
    # Feasibility
    SESSION_TIME_DEMOTION = "session_time_demotion"
    INTENSITY_PROTECTION = "intensity_protection"
    BEHAVIOUR_SUSTAINABILITY = "behaviour_sustainability"
    # Cold start / low warrant
    INSUFFICIENT_WARRANT = "insufficient_warrant"
    PREFER_EVIDENCE_CREATING = "prefer_evidence_creating"
    NOT_YET_KNOWABLE_CONTEXT = "not_yet_knowable_context"
    # Factor disagreement
    KNOWS_NOW_MAY_NOT_RETAIN = "knows_now_may_not_retain"
    BEHAVIOUR_STRONG_PERFORMANCE_THIN = "behaviour_strong_performance_thin"
    # History
    PRIOR_DISMISS_RESPECTED = "prior_dismiss_respected"
    # Confidence risk framing only
    CONFIDENCE_NOT_MASTERY = "confidence_not_mastery"


# Vocabulary version tag for audit / additive evolution.
REASON_CODE_VOCABULARY_VERSION = "1.0"

# Engine version tag emitted on Decision for audit lineage.
ENGINE_VERSION = "decision-engine/2.8.4-structural"

# Ordered catalogue of all reason-code ids (documentation / validation).
REASON_CODE_CATALOGUE: tuple[ReasonCodeId, ...] = tuple(ReasonCodeId)

# Family membership for each code identity.
REASON_CODE_FAMILY_MAP: dict[ReasonCodeId, ReasonCodeFamily] = {
    ReasonCodeId.HIGH_WEIGHT_COVERAGE: ReasonCodeFamily.CURRICULUM_WEIGHT,
    ReasonCodeId.WEAK_OR_ABSENT_MASTERY: ReasonCodeFamily.KNOWLEDGE_GAP,
    ReasonCodeId.MEMORY_STALENESS: ReasonCodeFamily.RETENTION_RISK,
    ReasonCodeId.THIN_PERFORMANCE_WARRANT: ReasonCodeFamily.ASSESSMENT_WARRANT_GAP,
    ReasonCodeId.SITTING_TIME_PRESSURE: ReasonCodeFamily.TIME_GOAL_PRESSURE,
    ReasonCodeId.SESSION_TIME_DEMOTION: ReasonCodeFamily.FEASIBILITY_DEMOTION,
    ReasonCodeId.INTENSITY_PROTECTION: ReasonCodeFamily.FEASIBILITY_DEMOTION,
    ReasonCodeId.BEHAVIOUR_SUSTAINABILITY: ReasonCodeFamily.FEASIBILITY_DEMOTION,
    ReasonCodeId.INSUFFICIENT_WARRANT: ReasonCodeFamily.COLD_START_LOW_WARRANT,
    ReasonCodeId.PREFER_EVIDENCE_CREATING: ReasonCodeFamily.COLD_START_LOW_WARRANT,
    ReasonCodeId.NOT_YET_KNOWABLE_CONTEXT: ReasonCodeFamily.COLD_START_LOW_WARRANT,
    ReasonCodeId.KNOWS_NOW_MAY_NOT_RETAIN: ReasonCodeFamily.FACTOR_DISAGREEMENT,
    ReasonCodeId.BEHAVIOUR_STRONG_PERFORMANCE_THIN: (
        ReasonCodeFamily.FACTOR_DISAGREEMENT
    ),
    ReasonCodeId.PRIOR_DISMISS_RESPECTED: ReasonCodeFamily.HISTORY_ANTI_THRASH,
    ReasonCodeId.CONFIDENCE_NOT_MASTERY: ReasonCodeFamily.CONFIDENCE_RISK_FRAMING,
}

# Codes that cite readiness and must inherit warrant honesty.
READINESS_CITING_REASON_CODES: frozenset[ReasonCodeId] = frozenset(
    {
        ReasonCodeId.INSUFFICIENT_WARRANT,
        ReasonCodeId.PREFER_EVIDENCE_CREATING,
        ReasonCodeId.NOT_YET_KNOWABLE_CONTEXT,
        ReasonCodeId.THIN_PERFORMANCE_WARRANT,
        ReasonCodeId.SITTING_TIME_PRESSURE,
        ReasonCodeId.KNOWS_NOW_MAY_NOT_RETAIN,
        ReasonCodeId.BEHAVIOUR_STRONG_PERFORMANCE_THIN,
    }
)


@dataclass(frozen=True)
class ReasonCodeRef:
    """One authored reason code with optional attribution hooks.

    Attributes:
        code_id: Stable catalogue identity.
        family: Educational family for the code.
        twin_domains: Twin domain tags cited.
        readiness_factor_ids: Readiness factor ids cited.
        curriculum_entity_ids: Curriculum identities cited.
        inherits_warrant: True when readiness warrant honesty applies.
        note_tags: Short structural tags — not marketing copy.
    """

    code_id: ReasonCodeId
    family: ReasonCodeFamily
    twin_domains: tuple[str, ...] = ()
    readiness_factor_ids: tuple[str, ...] = ()
    curriculum_entity_ids: tuple[str, ...] = ()
    inherits_warrant: bool = False
    note_tags: tuple[str, ...] = ()

    @classmethod
    def create(
        cls,
        code_id: ReasonCodeId | str,
        *,
        twin_domains: list[str] | tuple[str, ...] | None = None,
        readiness_factor_ids: list[str] | tuple[str, ...] | None = None,
        curriculum_entity_ids: list[str] | tuple[str, ...] | None = None,
        inherits_warrant: bool | None = None,
        note_tags: list[str] | tuple[str, ...] | None = None,
    ) -> ReasonCodeRef:
        """Construct a ReasonCodeRef from the catalogue."""
        cid = code_id if isinstance(code_id, ReasonCodeId) else ReasonCodeId(code_id)
        family = REASON_CODE_FAMILY_MAP[cid]
        warrant = (
            inherits_warrant
            if inherits_warrant is not None
            else cid in READINESS_CITING_REASON_CODES
        )
        return cls(
            code_id=cid,
            family=family,
            twin_domains=tuple(twin_domains or ()),
            readiness_factor_ids=tuple(readiness_factor_ids or ()),
            curriculum_entity_ids=tuple(curriculum_entity_ids or ()),
            inherits_warrant=warrant,
            note_tags=tuple(note_tags or ()),
        )
