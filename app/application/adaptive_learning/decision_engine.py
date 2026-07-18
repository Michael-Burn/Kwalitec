"""Adaptive Decision Engine — public application facade.

Consumes Digital Twin Snapshot + journey/curriculum context.
Produces explainable revision decisions with priority, ROI, and study time.
Phase 1 implements REVISION only. Framework-independent.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4

from app.application.adaptive_learning.diagnostics import (
    AdaptiveDiagnostics,
    AdaptiveDiagnosticsReport,
)
from app.application.adaptive_learning.dto.decision_snapshot import (
    DecisionExplanationDTO,
    DecisionSnapshotDTO,
)
from app.application.adaptive_learning.dto.intervention_snapshot import (
    InterventionSnapshot,
)
from app.application.adaptive_learning.dto.revision_snapshot import RevisionSnapshot
from app.application.adaptive_learning.dto.roi_snapshot import ROISnapshot
from app.application.adaptive_learning.explanation_service import ExplanationService
from app.application.adaptive_learning.intervention_selector import InterventionSelector
from app.application.adaptive_learning.policies.intervention_policy import (
    InterventionPolicy,
)
from app.application.adaptive_learning.policies.priority_policy import PriorityPolicy
from app.application.adaptive_learning.revision_planner import RevisionPlanner
from app.application.adaptive_learning.revision_scheduler import RevisionScheduler
from app.domain.adaptive_learning.adaptive_decision import AdaptiveDecision
from app.domain.adaptive_learning.decision_explanation import DecisionExplanation
from app.domain.adaptive_learning.decision_snapshot import DecisionSnapshot
from app.domain.adaptive_learning.educational_roi import EducationalROI
from app.domain.adaptive_learning.intervention_type import InterventionType
from app.domain.adaptive_learning.revision_plan import RevisionPlan
from app.domain.student_twin.confidence_band import ConfidenceBand
from app.domain.student_twin.twin_snapshot import TwinSnapshot


@dataclass(frozen=True)
class JourneyPositionInput:
    """Current Learning Journey position consumed by the decision engine."""

    journey_id: str = ""
    current_topic_id: str | None = None
    progress_ratio: float = 0.0

    @classmethod
    def create(
        cls,
        *,
        journey_id: str = "",
        current_topic_id: str | None = None,
        progress_ratio: float = 0.0,
    ) -> JourneyPositionInput:
        """Construct JourneyPositionInput."""
        ratio = float(progress_ratio)
        if ratio < 0.0 or ratio > 1.0:
            raise ValueError("progress_ratio must be in [0, 1]")
        tid = (
            current_topic_id.strip()
            if isinstance(current_topic_id, str) and current_topic_id.strip()
            else None
        )
        return cls(
            journey_id=(journey_id or "").strip(),
            current_topic_id=tid,
            progress_ratio=ratio,
        )


@dataclass(frozen=True)
class CurriculumContextInput:
    """Current curriculum context consumed by the decision engine."""

    subject_code: str = ""
    topic_importance: tuple[tuple[str, float], ...] = field(default_factory=tuple)
    prerequisite_criticality: tuple[tuple[str, float], ...] = field(
        default_factory=tuple
    )
    historical_struggle: tuple[tuple[str, float], ...] = field(default_factory=tuple)
    exam_proximity: float = 0.0

    @classmethod
    def create(
        cls,
        *,
        subject_code: str = "",
        topic_importance: Mapping[str, float] | None = None,
        prerequisite_criticality: Mapping[str, float] | None = None,
        historical_struggle: Mapping[str, float] | None = None,
        exam_proximity: float = 0.0,
    ) -> CurriculumContextInput:
        """Construct CurriculumContextInput from mappings."""
        proximity = float(exam_proximity)
        if proximity < 0.0 or proximity > 1.0:
            raise ValueError("exam_proximity must be in [0, 1]")
        return cls(
            subject_code=(subject_code or "").strip(),
            topic_importance=_mapping_pairs(topic_importance),
            prerequisite_criticality=_mapping_pairs(prerequisite_criticality),
            historical_struggle=_mapping_pairs(historical_struggle),
            exam_proximity=proximity,
        )

    def importance_map(self) -> dict[str, float]:
        """Return topic importance as a dict."""
        return dict(self.topic_importance)

    def prerequisite_map(self) -> dict[str, float]:
        """Return prerequisite criticality as a dict."""
        return dict(self.prerequisite_criticality)

    def struggle_map(self) -> dict[str, float]:
        """Return historical struggle as a dict."""
        return dict(self.historical_struggle)


class AdaptiveDecisionEngine:
    """Public facade for Adaptive Decision Engine Phase 1 (Revision).

    Framework-independent. Callers remain responsible for persistence.
    Same Twin + context inputs → same decision (deterministic).
    """

    ENGINE_ID = "adaptive_decision"
    ENGINE_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        clock: Callable[[], datetime] | None = None,
        id_factory: Callable[[], str] | None = None,
    ) -> None:
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._id_factory = id_factory or (lambda: uuid4().hex[:12])

    def decide(
        self,
        twin_snapshot: TwinSnapshot,
        *,
        journey_position: JourneyPositionInput | None = None,
        curriculum_context: CurriculumContextInput | None = None,
        as_of: datetime | None = None,
        max_interventions: int | None = None,
    ) -> AdaptiveDecision:
        """Evaluate learner state and recommend the highest-value revision.

        Consumes Twin Snapshot (knowledge, mastery, retention, readiness,
        weakness, velocity, history ids) plus optional journey/curriculum
        context. Does not mutate Twin state.
        """
        when = as_of if as_of is not None else self._clock()
        if when.tzinfo is None:
            when = when.replace(tzinfo=UTC)

        journey = journey_position or JourneyPositionInput()
        curriculum = curriculum_context or CurriculumContextInput()
        cap = max_interventions or InterventionPolicy.max_interventions()

        candidates = RevisionPlanner.build_candidates(
            knowledge=twin_snapshot.knowledge,
            mastery=twin_snapshot.mastery,
            retention=twin_snapshot.retention,
            confidence=twin_snapshot.confidence,
            weaknesses=twin_snapshot.weaknesses,
            velocity=twin_snapshot.velocity,
            topic_importance=curriculum.importance_map(),
            prerequisite_criticality=curriculum.prerequisite_map(),
            historical_struggle=curriculum.struggle_map(),
            exam_proximity=curriculum.exam_proximity,
            current_topic_id=journey.current_topic_id,
        )

        windows = RevisionScheduler.schedule(
            candidates,
            as_of=when,
            exam_proximity=curriculum.exam_proximity,
            max_windows=cap,
        )

        plan_id = f"plan-{self._id_factory()}"
        selected, plan = InterventionSelector.select_revision(
            candidates,
            windows=windows,
            plan_id=plan_id,
            id_prefix=f"rev-{self._id_factory()}",
        )
        # Cap interventions if caller requested fewer.
        if selected is not None and plan.intervention_count > cap:
            capped = plan.interventions[:cap]
            plan = RevisionPlan.create(
                plan.plan_id,
                interventions=capped,
                candidates=plan.candidates,
                windows=plan.windows[:cap],
                primary_topic_id=capped[0].topic_id if capped else None,
            )
            selected = capped[0] if capped else None

        decision_id = f"dec-{self._id_factory()}"
        if selected is None:
            explanation = DecisionExplanation.create(
                evidence_considered=twin_snapshot.history_event_ids[:8],
                rationale="no_revision_candidate_above_threshold",
                priority=0.0,
                expected_educational_benefit="maintain_current_readiness",
                confidence=twin_snapshot.readiness.confidence,
                detail_lines=(
                    f"readiness={twin_snapshot.readiness.readiness_score:.3f}",
                    f"min_priority={PriorityPolicy.MIN_REVISION_PRIORITY:.3f}",
                ),
            )
            evidence = twin_snapshot.history_event_ids
            alternatives: tuple[str, ...] = ()
        else:
            explanation = selected.explanation
            evidence = tuple(
                dict.fromkeys(
                    (
                        *selected.explanation.evidence_considered,
                        *twin_snapshot.history_event_ids[:8],
                    )
                )
            )
            alternatives = tuple(
                c.topic_id
                for c in plan.candidates
                if c.topic_id != selected.topic_id
            )[:5]

        return AdaptiveDecision.create(
            decision_id,
            twin_snapshot.learner_id,
            when,
            selected_intervention=selected,
            revision_plan=plan,
            explanation=explanation,
            twin_version_label=twin_snapshot.version_label,
            evidence_ids=evidence,
            alternative_topic_ids=alternatives,
        )

    def snapshot(self, decision: AdaptiveDecision) -> DecisionSnapshot:
        """Project a domain DecisionSnapshot from a decision."""
        return DecisionSnapshot.from_decision(decision)

    def snapshot_dto(self, decision: AdaptiveDecision) -> DecisionSnapshotDTO:
        """Project an application DecisionSnapshotDTO."""
        return DecisionSnapshotDTO.from_decision(decision)

    def revision_snapshot(self, decision: AdaptiveDecision) -> RevisionSnapshot:
        """Project the revision plan DTO."""
        return RevisionSnapshot.from_plan(decision.revision_plan)

    def roi_snapshot(self, decision: AdaptiveDecision) -> ROISnapshot:
        """Project the educational ROI DTO."""
        return ROISnapshot.from_roi(decision.roi)

    def intervention_snapshot(
        self,
        decision: AdaptiveDecision,
    ) -> InterventionSnapshot | None:
        """Project the selected intervention DTO, if any."""
        if decision.selected_intervention is None:
            return None
        return InterventionSnapshot.from_intervention(decision.selected_intervention)

    def explain(self, decision: AdaptiveDecision) -> DecisionExplanationDTO:
        """Explain an adaptive decision."""
        return ExplanationService.explain_decision(decision)

    def diagnostics(self, decision: AdaptiveDecision) -> AdaptiveDiagnosticsReport:
        """Inspect decision integrity."""
        return AdaptiveDiagnostics.inspect(decision)

    def empty_decision(
        self,
        learner_id: str,
        *,
        rationale: str = "insufficient_evidence",
    ) -> AdaptiveDecision:
        """Produce an explicit empty revision decision."""
        when = self._clock()
        if when.tzinfo is None:
            when = when.replace(tzinfo=UTC)
        explanation = DecisionExplanation.create(
            evidence_considered=(),
            rationale=rationale,
            priority=0.0,
            expected_educational_benefit="await_additional_evidence",
            confidence=ConfidenceBand.VERY_LOW,
        )
        return AdaptiveDecision.create(
            f"dec-{self._id_factory()}",
            learner_id,
            when,
            selected_intervention=None,
            revision_plan=RevisionPlan.empty(f"plan-{self._id_factory()}"),
            explanation=explanation,
        )

    @staticmethod
    def supported_intervention_types() -> frozenset[InterventionType]:
        """Return Phase-1 implemented intervention types."""
        return InterventionPolicy.phase1_types()

    @staticmethod
    def zero_roi() -> EducationalROI:
        """Return a zero educational ROI placeholder."""
        return EducationalROI.zero()


def _mapping_pairs(
    mapping: Mapping[str, float] | None,
) -> tuple[tuple[str, float], ...]:
    if not mapping:
        return ()
    pairs: list[tuple[str, float]] = []
    for key, value in mapping.items():
        token = str(key).strip()
        if not token:
            continue
        numeric = float(value)
        if numeric < 0.0 or numeric > 1.0:
            raise ValueError(f"mapping value for {token!r} must be in [0, 1]")
        pairs.append((token, numeric))
    pairs.sort(key=lambda item: item[0])
    return tuple(pairs)
