"""Domain Mission — session/day execution projection of Decision(s).

Immutable, Decision-bound, regenerable. Not a Twin write domain, not selection
authority, not Recommendation packaging, not WeekPlan policy, not the ORM
``app.models.mission.Mission`` (Stage A coexistence — named dual truth).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.domain.decision.decision import DecisionScope
from app.domain.mission.attribution import DecisionCitation
from app.domain.mission.evidence_hooks import MissionEvidenceHooks
from app.domain.mission.feasibility import FeasibilityAcknowledgement
from app.domain.mission.task import MissionTask
from app.domain.mission.warrant import MissionWarrantPosture
from app.domain.readiness.curriculum_context import CurriculumFormat

# Mission Intelligence version tag for audit lineage.
MISSION_INTELLIGENCE_VERSION = "mission-intelligence/2.10.4-structural"


@dataclass(frozen=True)
class MissionRegenerationIdentity:
    """Enough Decision / Twin snapshot reference for recomposition.

    Stale missions are disposable projections — not Twin truth.
    """

    decision_evaluation_ids: tuple[str, ...] = ()
    decision_engine_versions: tuple[str, ...] = ()
    twin_snapshot_ref: str | None = None
    compose_version: str = MISSION_INTELLIGENCE_VERSION
    session_window_id: str | None = None

    @classmethod
    def create(
        cls,
        *,
        decision_evaluation_ids: list[str] | tuple[str, ...] | None = None,
        decision_engine_versions: list[str] | tuple[str, ...] | None = None,
        twin_snapshot_ref: str | None = None,
        compose_version: str = MISSION_INTELLIGENCE_VERSION,
        session_window_id: str | None = None,
    ) -> MissionRegenerationIdentity:
        """Construct regeneration identity."""
        return cls(
            decision_evaluation_ids=tuple(decision_evaluation_ids or ()),
            decision_engine_versions=tuple(decision_engine_versions or ()),
            twin_snapshot_ref=twin_snapshot_ref,
            compose_version=compose_version,
            session_window_id=session_window_id,
        )


@dataclass(frozen=True)
class MissionScope:
    """Scope identity for one Mission composition.

    Attributes:
        student_id: Learner identity.
        curriculum_id: Syllabus identity when known.
        sitting_date: Target sitting when known.
        exam_label: Current exam label when known.
        session_window_id: Session / day window identity.
        session_date: Calendar day of the session when known.
    """

    student_id: str
    curriculum_id: str | None = None
    sitting_date: date | None = None
    exam_label: str | None = None
    session_window_id: str | None = None
    session_date: date | None = None

    @classmethod
    def create(
        cls,
        student_id: str,
        *,
        curriculum_id: str | None = None,
        sitting_date: date | None = None,
        exam_label: str | None = None,
        session_window_id: str | None = None,
        session_date: date | None = None,
    ) -> MissionScope:
        """Construct MissionScope."""
        normalized = student_id.strip() if isinstance(student_id, str) else ""
        if not normalized:
            raise ValueError("student_id must be a non-empty string")
        return cls(
            student_id=normalized,
            curriculum_id=curriculum_id,
            sitting_date=sitting_date,
            exam_label=exam_label,
            session_window_id=session_window_id,
            session_date=session_date,
        )

    @classmethod
    def from_decision_scope(
        cls,
        scope: DecisionScope,
        *,
        session_window_id: str | None = None,
        session_date: date | None = None,
    ) -> MissionScope:
        """Project DecisionScope into MissionScope with session window."""
        return cls.create(
            scope.student_id,
            curriculum_id=scope.curriculum_id,
            sitting_date=scope.sitting_date,
            exam_label=scope.exam_label,
            session_window_id=session_window_id,
            session_date=session_date,
        )


@dataclass(frozen=True)
class Mission:
    """Session/day executable projection of one Decision or Decision batch.

    Produced only by Mission Intelligence composition. Never writes Twin
    beliefs. Never re-selects. Never invents filler. Never owns Recommendation
    packaging or WeekPlan policy.

    Attributes:
        scope: Student / curriculum / sitting / session window.
        tasks: Ordered MissionTasks (may be empty — feasibility remainder).
        decision_citations: Decision(s) being operationalised.
        warrant_posture: Aggregated inherited honesty from Decision(s).
        feasibility_acknowledgements: How load was shaped.
        regeneration_identity: Recomposition hooks.
        evidence_hooks: Completion / Failure → Behaviour / planning only.
        curriculum_format: V1 / V2 format tag from Decision lineage.
        mission_intelligence_version: Additive audit tag.
        reason_code_vocabulary_note: Structural note that codes are Decision-owned.
    """

    scope: MissionScope
    tasks: tuple[MissionTask, ...]
    decision_citations: tuple[DecisionCitation, ...]
    warrant_posture: MissionWarrantPosture
    feasibility_acknowledgements: tuple[FeasibilityAcknowledgement, ...]
    regeneration_identity: MissionRegenerationIdentity
    evidence_hooks: MissionEvidenceHooks
    curriculum_format: CurriculumFormat
    mission_intelligence_version: str = MISSION_INTELLIGENCE_VERSION
    reason_code_vocabulary_note: str = "decision_engine_authors_reason_codes"

    @classmethod
    def create(
        cls,
        *,
        scope: MissionScope,
        tasks: list[MissionTask] | tuple[MissionTask, ...],
        decision_citations: list[DecisionCitation] | tuple[DecisionCitation, ...],
        warrant_posture: MissionWarrantPosture | str,
        feasibility_acknowledgements: list[FeasibilityAcknowledgement]
        | tuple[FeasibilityAcknowledgement, ...]
        | None = None,
        regeneration_identity: MissionRegenerationIdentity,
        evidence_hooks: MissionEvidenceHooks,
        curriculum_format: CurriculumFormat | str,
        mission_intelligence_version: str = MISSION_INTELLIGENCE_VERSION,
    ) -> Mission:
        """Construct a Mission after validating Decision-bound contracts.

        Raises:
            ValueError: If no Decision citations or task attribution broken.
        """
        citation_tuple = tuple(decision_citations)
        if not citation_tuple:
            raise ValueError("Mission.decision_citations must be non-empty")
        task_tuple = tuple(tasks)
        warrant = (
            warrant_posture
            if isinstance(warrant_posture, MissionWarrantPosture)
            else MissionWarrantPosture(warrant_posture)
        )
        fmt = (
            curriculum_format
            if isinstance(curriculum_format, CurriculumFormat)
            else CurriculumFormat(str(curriculum_format).strip().lower())
        )
        for task in task_tuple:
            if not task.attribution.reason_code_citations:
                raise ValueError(
                    "every MissionTask must cite at least one Decision reason code"
                )
        return cls(
            scope=scope,
            tasks=task_tuple,
            decision_citations=citation_tuple,
            warrant_posture=warrant,
            feasibility_acknowledgements=tuple(feasibility_acknowledgements or ()),
            regeneration_identity=regeneration_identity,
            evidence_hooks=evidence_hooks,
            curriculum_format=fmt,
            mission_intelligence_version=mission_intelligence_version,
        )

    @property
    def is_empty(self) -> bool:
        """True when Mission has zero tasks (valid feasibility remainder)."""
        return len(self.tasks) == 0

    @property
    def task_count(self) -> int:
        """Number of MissionTasks in this Mission."""
        return len(self.tasks)
