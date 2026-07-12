"""Educational Orchestrator — Application Layer composition entry.

Coordinates Educational Intelligence on the Twin-first product read path.
Owns lifecycle, lawful invocation order, context wiring, Experience assembly,
and truthful failure propagation.

Never scores readiness, selects next actions, ranks recommendations, alters
Decisions or Missions, mutates Twin, or imports Flask / routes / templates /
ORM. Educational judgement remains in domain owners (ADR-002).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Protocol

from app.application.curriculum.curriculum_context_builder import (
    CurriculumContextBuilder,
)
from app.domain.decision.constraints import Constraints
from app.domain.decision.decision import Decision, DecisionLineage
from app.domain.decision.engine import DecisionEngine
from app.domain.decision.history import DecisionHistory
from app.domain.decision.reason_codes import ReasonCodeRef
from app.domain.mission.context import MissionExecutionContext
from app.domain.mission.engine import MissionIntelligence
from app.domain.mission.mission import Mission
from app.domain.readiness.aggregation import ReadinessAggregation
from app.domain.readiness.curriculum_context import CurriculumContext
from app.domain.readiness.factors import OverallPosture, WarrantPosture
from app.domain.readiness.readiness_state import ReadinessState
from app.domain.recommendation.context import RecommendationContext
from app.domain.recommendation.engine import RecommendationEngine
from app.domain.recommendation.explanation import ExplanationChainPresentation
from app.domain.recommendation.recommendation import Recommendation
from app.domain.twin.digital_twin import DigitalTwin

# Contract version identity for Educational Experience Metadata (Capability 3.2.3).
CONTRACT_VERSION = "educational-experience/3.2.5-skeleton"


class CurriculumContextBuilderProtocol(Protocol):
    """Callable / type with ``build(curriculum_id) -> CurriculumContext``."""

    @staticmethod
    def build(curriculum_id: int | None) -> CurriculumContext: ...


class ReadinessAggregationProtocol(Protocol):
    """Callable / type with ``derive(twin, curriculum, ...) -> ReadinessState``."""

    @staticmethod
    def derive(
        twin: DigitalTwin,
        curriculum: CurriculumContext,
        *,
        as_of: datetime | None = None,
        derivation_id: str | None = None,
    ) -> ReadinessState: ...


class DecisionEngineProtocol(Protocol):
    """Callable / type with ``evaluate(...) -> Decision``."""

    @staticmethod
    def evaluate(
        twin: DigitalTwin,
        readiness: ReadinessState,
        curriculum: CurriculumContext,
        constraints: Constraints,
        *,
        decision_history: DecisionHistory | None = None,
        as_of: datetime | None = None,
        evaluation_id: str | None = None,
    ) -> Decision: ...


class RecommendationEngineProtocol(Protocol):
    """Callable / type with ``package(decision, ...) -> Recommendation``."""

    @staticmethod
    def package(
        decision: Decision,
        *,
        communication_context: RecommendationContext | None = None,
    ) -> Recommendation: ...


class MissionIntelligenceProtocol(Protocol):
    """Callable / type with ``compose(...) -> Mission``."""

    @staticmethod
    def compose(
        decision_or_batch: Decision,
        execution_context: MissionExecutionContext,
        recommendation_language: Recommendation | None = None,
    ) -> Mission: ...


# ═══════════════════════════════════════════════════════════════════════════════
# Educational Experience Contract (Capability 3.2.3) — closed component set
# ═══════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class StudentSummary:
    """Who the experience is for — authorised identity / sitting scope only."""

    student_id: str
    curriculum_id: str | None = None
    current_exam: str | None = None
    target_sitting: date | None = None


@dataclass(frozen=True)
class ReadinessSummary:
    """Factorable preparedness posture and warrant — forwarded, never recomputed."""

    overall_posture: OverallPosture
    overall_warrant: WarrantPosture
    cold_start: bool
    curriculum_format: str


@dataclass(frozen=True)
class ProgressSnapshot:
    """Honest, non-selecting cues of what is known — never next-action authority."""

    overall_posture: OverallPosture
    overall_warrant: WarrantPosture
    cold_start: bool
    student_id: str
    curriculum_id: str | None = None


@dataclass(frozen=True)
class Explainability:
    """Chain-supported *why* — Decision codes / lineage + Recommendation chain."""

    reason_codes: tuple[ReasonCodeRef, ...]
    lineage: DecisionLineage
    explanation_chain: ExplanationChainPresentation


@dataclass(frozen=True)
class ExperienceMetadata:
    """Non-educational composition facts — never a selection back door."""

    contract_version: str
    surface_intent: str | None = None
    cutover_mode: str | None = None
    locale: str | None = None
    composed_at: datetime | None = None


@dataclass(frozen=True)
class EducationalExperience:
    """Canonical product-facing Educational Experience (Capability 3.2.3).

    Closed set only. Carries domain answers; does not author educational meaning.
    """

    student_summary: StudentSummary
    todays_recommendation: Recommendation
    todays_mission: Mission
    readiness_summary: ReadinessSummary
    progress_snapshot: ProgressSnapshot
    explainability: Explainability
    warnings: tuple[str, ...]
    empty_state_guidance: tuple[str, ...]
    metadata: ExperienceMetadata


@dataclass(frozen=True)
class ProductContext:
    """Product / session facts for Metadata — never educational selection."""

    surface_intent: str | None = None
    cutover_mode: str | None = None
    locale: str | None = None
    composed_at: datetime | None = None


# ═══════════════════════════════════════════════════════════════════════════════
# Orchestrator
# ═══════════════════════════════════════════════════════════════════════════════


class EducationalOrchestrator:
    """Sole Application composition entry for the Twin-first educational read path.

    Invokes CurriculumContextBuilder → Readiness → Decision → Recommendation →
    Mission in lawful order, then assembles the Educational Experience Contract.
    """

    def __init__(
        self,
        *,
        curriculum_context_builder: CurriculumContextBuilderProtocol = (
            CurriculumContextBuilder
        ),
        readiness_aggregation: ReadinessAggregationProtocol = ReadinessAggregation,
        decision_engine: DecisionEngineProtocol = DecisionEngine,
        recommendation_engine: RecommendationEngineProtocol = RecommendationEngine,
        mission_intelligence: MissionIntelligenceProtocol = MissionIntelligence,
    ) -> None:
        """Wire educational domain owners and CurriculumContext construction.

        Args:
            curriculum_context_builder: Application builder for CurriculumContext.
            readiness_aggregation: Domain readiness derive API.
            decision_engine: Domain next-action evaluate API.
            recommendation_engine: Domain Decision packaging API.
            mission_intelligence: Domain Mission compose API.
        """
        self._curriculum_context_builder = curriculum_context_builder
        self._readiness_aggregation = readiness_aggregation
        self._decision_engine = decision_engine
        self._recommendation_engine = recommendation_engine
        self._mission_intelligence = mission_intelligence

    def build_experience(
        self,
        *,
        curriculum_id: int,
        twin: DigitalTwin,
        constraints: Constraints,
        mission_execution_context: MissionExecutionContext | None = None,
        decision_history: DecisionHistory | None = None,
        recommendation_context: RecommendationContext | None = None,
        product_context: ProductContext | None = None,
    ) -> EducationalExperience:
        """Compose one Educational Experience for an authorised product request.

        Twin must be supplied by the caller (TwinRepository is out of scope).
        Failures from builders or domains propagate without fabrication.

        Args:
            curriculum_id: Persisted curriculum primary key for CurriculumContext.
            twin: Authoritative Digital Twin snapshot (read-only; never mutated).
            constraints: Session feasibility envelope for Decision / Mission.
            mission_execution_context: Optional Mission bounds; defaults from
                constraints + curriculum identity (wiring only).
            decision_history: Optional Decision Journal anti-thrash context.
            recommendation_context: Optional packaging communication context.
            product_context: Optional Metadata facts (surface, cutover, locale).

        Returns:
            Immutable Educational Experience Contract snapshot.

        Raises:
            Exception: Any builder or domain failure, propagated truthfully.
        """
        # 1. CurriculumContext — syllabus denominator via Application builder.
        curriculum = self._curriculum_context_builder.build(curriculum_id)

        # 2. Twin is caller-supplied (read-only). No TwinRepository in this skeleton.

        # 3. Readiness Aggregation.
        readiness = self._readiness_aggregation.derive(twin, curriculum)

        # 4. Decision Engine — sole next-action selection.
        decision = self._decision_engine.evaluate(
            twin,
            readiness,
            curriculum,
            constraints,
            decision_history=decision_history,
        )

        # 5. Recommendation Engine — packaging only.
        recommendation = self._recommendation_engine.package(
            decision,
            communication_context=recommendation_context,
        )

        # 6. Mission Intelligence — operationalisation only.
        execution_context = mission_execution_context or _default_mission_context(
            constraints=constraints,
            curriculum=curriculum,
        )
        mission = self._mission_intelligence.compose(
            decision,
            execution_context,
            recommendation_language=recommendation,
        )

        # 7. Assemble closed Educational Experience (place, do not author).
        return _assemble_experience(
            twin=twin,
            readiness=readiness,
            decision=decision,
            recommendation=recommendation,
            mission=mission,
            product_context=product_context,
        )


def _default_mission_context(
    *,
    constraints: Constraints,
    curriculum: CurriculumContext,
) -> MissionExecutionContext:
    """Wire MissionExecutionContext from already-known inputs — no educational math."""
    return MissionExecutionContext.create(
        constraints=constraints,
        curriculum_id=curriculum.curriculum_id,
    )


def _assemble_experience(
    *,
    twin: DigitalTwin,
    readiness: ReadinessState,
    decision: Decision,
    recommendation: Recommendation,
    mission: Mission,
    product_context: ProductContext | None,
) -> EducationalExperience:
    """Map domain outputs into the closed Experience Contract without adding meaning."""
    identity = twin.identity
    student_summary = StudentSummary(
        student_id=identity.student_id,
        curriculum_id=identity.curriculum_id,
        current_exam=identity.current_exam,
        target_sitting=identity.target_sitting,
    )
    readiness_summary = ReadinessSummary(
        overall_posture=readiness.overall_posture,
        overall_warrant=readiness.overall_warrant,
        cold_start=readiness.cold_start,
        curriculum_format=str(readiness.curriculum_format),
    )
    progress_snapshot = ProgressSnapshot(
        overall_posture=readiness.overall_posture,
        overall_warrant=readiness.overall_warrant,
        cold_start=readiness.cold_start,
        student_id=identity.student_id,
        curriculum_id=identity.curriculum_id,
    )
    explainability = Explainability(
        reason_codes=decision.reason_codes,
        lineage=decision.lineage,
        explanation_chain=recommendation.explanation_chain,
    )
    warnings = _classify_warnings(readiness=readiness, decision=decision)
    empty_state = _empty_state_guidance(readiness=readiness, decision=decision)
    ctx = product_context or ProductContext()
    metadata = ExperienceMetadata(
        contract_version=CONTRACT_VERSION,
        surface_intent=ctx.surface_intent,
        cutover_mode=ctx.cutover_mode,
        locale=ctx.locale,
        composed_at=ctx.composed_at,
    )
    return EducationalExperience(
        student_summary=student_summary,
        todays_recommendation=recommendation,
        todays_mission=mission,
        readiness_summary=readiness_summary,
        progress_snapshot=progress_snapshot,
        explainability=explainability,
        warnings=warnings,
        empty_state_guidance=empty_state,
        metadata=metadata,
    )


def _classify_warnings(
    *,
    readiness: ReadinessState,
    decision: Decision,
) -> tuple[str, ...]:
    """Forward honesty / degradation signals — classify only, never upgrade warrant."""
    tags: list[str] = []
    if readiness.cold_start:
        tags.append("cold_start")
    if readiness.overall_warrant is WarrantPosture.LOW:
        tags.append("thin_warrant")
    if readiness.overall_posture is OverallPosture.NOT_YET_KNOWABLE:
        tags.append("not_yet_knowable")
    warrant_value = str(decision.warrant_posture)
    if warrant_value in {"cold_start", "not_yet_knowable", "inherited_low"}:
        tag = f"decision_warrant:{warrant_value}"
        if tag not in tags:
            tags.append(tag)
    return tuple(tags)


def _empty_state_guidance(
    *,
    readiness: ReadinessState,
    decision: Decision,
) -> tuple[str, ...]:
    """Forward lawful empty / cold-start postures — never fabricate Mid readiness."""
    if not (
        readiness.cold_start
        or readiness.overall_posture is OverallPosture.NOT_YET_KNOWABLE
        or str(decision.warrant_posture) in {"cold_start", "not_yet_knowable"}
    ):
        return ()
    tags = ["empty_or_cold_start_posture"]
    # Decision-authored selected family is domain guidance, not orchestrator invention.
    tags.append(f"decision_selected_family:{decision.selected.family.value}")
    return tuple(tags)
