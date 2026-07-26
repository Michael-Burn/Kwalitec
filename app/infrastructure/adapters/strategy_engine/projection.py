"""Strategy Experience Projection (MS-005 S2).

Projects immutable LearningIntervention (+ StrategyExplanationBundle) into
Experience-facing StrategyProjection values and implements
StrategyProjectionPort without exposing raw LearningIntervention objects,
mutating Strategy / Twin / Adaptive / Runtime A state, or changing Experience
UX authority.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from app.infrastructure.adapters.strategy_engine.contracts import (
    AUTHORITY_STRATEGY_ENGINE,
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    STRATEGY_VERSION_S2,
    LearningIntervention,
    StrategyExplanationBundle,
    StrategyExplanationSummaryProjection,
    StrategyProjection,
    StrategyProjectionProvenance,
    StrategyProjectionResult,
)
from app.infrastructure.adapters.strategy_engine.explainability import (
    StrategyExplainabilityService,
    StrategyExplainabilityValidationError,
)

PROJECTION_VERSION = STRATEGY_VERSION_S2

REASON_STRATEGY_UNAVAILABLE = "strategy_unavailable"
REASON_STRATEGY_FLAG_OFF = "strategy_flag_off"
REASON_STRATEGY_INVALID = "strategy_invalid_intervention"
REASON_STRATEGY_EMPTY = "empty_authentic"

SOURCE_SERVICE_STRATEGY_PROJECTION = "strategy_projector"


class StrategyProjector:
    """Project LearningInterventions into Experience StrategyProjection values.

    Rules:
    - MAY read LearningIntervention and StrategyExplanationBundle
    - MUST NOT mutate Strategy / Twin / Adaptive / Runtime A state, persist
      interventions, or replace Experience UX authority
    - Identical LearningIntervention (+ optional explanation) → identical
      serialize()
    """

    PROJECTOR_ID = "strategy_projector"
    PROJECTOR_VERSION = PROJECTION_VERSION

    def __init__(self, *, enabled: bool = True) -> None:
        self._enabled = bool(enabled)

    @property
    def projector_id(self) -> str:
        return self.PROJECTOR_ID

    @property
    def projector_version(self) -> str:
        return self.PROJECTOR_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    def unavailable_projection(
        self,
        *,
        student_id: str = "",
        as_of: str | None = None,
        reason: str = REASON_STRATEGY_UNAVAILABLE,
    ) -> StrategyProjection:
        """Build an explicit unavailable Experience projection (never estimated)."""
        return StrategyProjection(
            student_id=(student_id or "").strip(),
            intervention_id="",
            strategy_decision_id="",
            as_of=as_of,
            projection_version=PROJECTION_VERSION,
            authority=AUTHORITY_STRATEGY_ENGINE,
            primary_intervention_kind="",
            educational_objective="",
            explanation_summary=StrategyExplanationSummaryProjection(
                why_summary=reason,
                limitations_codes=(reason,),
            ),
            provenance=StrategyProjectionProvenance(
                authority=AUTHORITY_STRATEGY_ENGINE,
                as_of=as_of,
                provenance_refs=(),
            ),
            availability=AVAILABILITY_UNAVAILABLE,
            unavailable_reason=reason,
            limitations_codes=(reason,),
        )

    def project(
        self,
        intervention: LearningIntervention,
        *,
        explanation: StrategyExplanationBundle | None = None,
        student_id: str = "",
        as_of: str | None = None,
    ) -> StrategyProjection:
        """Project an immutable LearningIntervention into StrategyProjection.

        Identical LearningIntervention (+ optional explanation) material →
        identical StrategyProjection.serialize() every execution.
        """
        if not isinstance(intervention, LearningIntervention):
            raise TypeError("intervention must be a LearningIntervention")
        if explanation is not None and not isinstance(
            explanation, StrategyExplanationBundle
        ):
            raise TypeError(
                "explanation must be a StrategyExplanationBundle or None"
            )

        clock = as_of
        if clock is None and intervention.provenance.collected_at is not None:
            clock = intervention.provenance.collected_at

        topic_code = ""
        if intervention.session.primary_topic:
            topic_code = intervention.session.primary_topic
        elif intervention.topic_refs:
            topic_code = intervention.topic_refs[0]

        adaptive_decision_id = (
            intervention.adaptive_recommendation_ref
            or intervention.session.adaptive_decision_ref
            or intervention.revision.adaptive_decision_ref
        )
        limitations = tuple(
            dict.fromkeys(
                [
                    *intervention.limitations,
                    *(
                        explanation.limitations.codes
                        if explanation is not None
                        else ()
                    ),
                ]
            )
        )
        if not intervention.kind:
            limitations = tuple(
                dict.fromkeys([*limitations, REASON_STRATEGY_EMPTY])
            )

        explanation_summary = self._explanation_summary(explanation, intervention)
        confidence_band = (
            explanation.confidence.band
            if explanation is not None
            else explanation_summary.confidence_band
        )
        explanation_dict: Mapping[str, Any] = (
            explanation.to_canonical_dict() if explanation is not None else {}
        )
        provenance_refs = self._provenance_refs(intervention, explanation)
        available = bool(intervention.kind) and (
            intervention.provenance.availability != AVAILABILITY_UNAVAILABLE
            or bool(intervention.kind)
        )
        unavailable_reason = ""
        if not available:
            unavailable_reason = (
                intervention.provenance.unavailable_reason
                or REASON_STRATEGY_EMPTY
            )

        return StrategyProjection(
            student_id=(student_id or "").strip(),
            intervention_id=intervention.intervention_id,
            strategy_decision_id=intervention.intervention_id,
            as_of=clock,
            projection_version=PROJECTION_VERSION,
            authority=intervention.authority or AUTHORITY_STRATEGY_ENGINE,
            primary_intervention_kind=intervention.kind,
            educational_objective=intervention.educational_objective,
            topic_code=topic_code,
            topic_title=topic_code,
            topic_refs=intervention.topic_refs,
            minutes_budget=intervention.minutes_budget,
            steps=tuple(step.to_canonical_dict() for step in intervention.steps),
            session_plan=intervention.session.to_canonical_dict(),
            study_plan=intervention.study.to_canonical_dict(),
            revision_plan=intervention.revision.to_canonical_dict(),
            recovery_plan=intervention.recovery.to_canonical_dict(),
            fatigue=intervention.fatigue.to_canonical_dict(),
            confidence_intervention=intervention.confidence.to_canonical_dict(),
            explanation_summary=explanation_summary,
            educational_principle_ids=intervention.educational_principle_ids,
            adaptive_decision_id=adaptive_decision_id,
            twin_snapshot_ref=intervention.twin_ref,
            confidence_band=confidence_band,
            mission_aligned=bool(intervention.session.mission_aligned),
            availability=(
                AVAILABILITY_AVAILABLE if available else AVAILABILITY_UNAVAILABLE
            ),
            unavailable_reason=unavailable_reason,
            limitations_codes=limitations,
            explanation=explanation_dict,
            provenance=StrategyProjectionProvenance(
                intervention_id=intervention.intervention_id,
                adaptive_decision_id=adaptive_decision_id,
                twin_snapshot_ref=intervention.twin_ref,
                runtime_a_evidence_ref=intervention.runtime_a_evidence_ref,
                authority=intervention.authority or AUTHORITY_STRATEGY_ENGINE,
                as_of=clock,
                provenance_refs=provenance_refs,
            ),
        )

    def _explanation_summary(
        self,
        explanation: StrategyExplanationBundle | None,
        intervention: LearningIntervention,
    ) -> StrategyExplanationSummaryProjection:
        if explanation is None:
            return StrategyExplanationSummaryProjection(
                why_summary=intervention.explanation.why_summary,
                educational_objective=intervention.educational_objective,
                principle_ids=intervention.educational_principle_ids,
                limitations_codes=intervention.limitations,
            )
        available_planners = tuple(
            item.planner_id
            for item in explanation.planner_contributions
            if item.available
        )
        return StrategyExplanationSummaryProjection(
            why_summary=explanation.why.summary,
            educational_objective=explanation.educational_objective,
            confidence_band=explanation.confidence.band,
            confidence_rationale=explanation.confidence.rationale,
            principle_ids=tuple(
                item.principle_id for item in explanation.educational_principles
            ),
            runtime_a_ref_count=len(explanation.runtime_a_evidence_refs),
            twin_factor_count=len(explanation.twin_factors.factors_considered),
            adaptive_availability=explanation.adaptive_consumed.availability,
            limitations_codes=explanation.limitations.codes,
            planner_ids=available_planners,
        )

    def _provenance_refs(
        self,
        intervention: LearningIntervention,
        explanation: StrategyExplanationBundle | None,
    ) -> tuple[str, ...]:
        refs: list[str] = []
        for token in (
            intervention.runtime_a_evidence_ref,
            *intervention.runtime_a_refs,
            intervention.twin_ref,
            intervention.adaptive_recommendation_ref,
        ):
            if token:
                refs.append(str(token))
        if explanation is not None:
            for item in explanation.runtime_a_evidence_refs:
                if item.kind and item.id:
                    refs.append(f"{item.kind}:{item.id}")
                elif item.id:
                    refs.append(item.id)
            if explanation.twin_factors.snapshot_ref:
                refs.append(explanation.twin_factors.snapshot_ref)
            if explanation.adaptive_consumed.decision_id:
                refs.append(explanation.adaptive_consumed.decision_id)
        return tuple(dict.fromkeys(refs))


class StrategyExperienceProjectionPort:
    """StrategyProjectionPort implementation backed by Strategy projections.

    Experience consumes StrategyProjection-derived opaque dicts only.
    Does not mutate Strategy Engine behaviour, Runtime A, Twin, or Adaptive.
    No Experience authority cutover in S2.
    """

    PORT_ID = "strategy_projection_port"
    PORT_VERSION = PROJECTION_VERSION

    def __init__(
        self,
        *,
        projector: StrategyProjector | None = None,
        explainability: StrategyExplainabilityService | None = None,
        enabled: bool = True,
        intervention_provider: (
            Callable[[str], LearningIntervention | None] | None
        ) = None,
    ) -> None:
        self._enabled = bool(enabled)
        self._projector = projector or StrategyProjector(enabled=enabled)
        self._explainability = explainability
        self._intervention_provider = intervention_provider
        self._bound: dict[str, StrategyProjection] = {}

    @property
    def port_id(self) -> str:
        return self.PORT_ID

    @property
    def port_version(self) -> str:
        return self.PORT_VERSION

    def is_available(self) -> bool:
        return self._enabled and self._projector.is_enabled()

    def projector(self) -> StrategyProjector:
        return self._projector

    def explainability(self) -> StrategyExplainabilityService | None:
        return self._explainability

    def project_intervention(
        self,
        intervention: LearningIntervention,
        *,
        student_id: str = "",
        explanation: StrategyExplanationBundle | None = None,
        as_of: str | None = None,
    ) -> StrategyProjection:
        """Project and optionally bind a LearningIntervention for Experience."""
        resolved = explanation
        if resolved is None and self._explainability is not None:
            resolved = self._explainability.explain(intervention)
        projection = self._projector.project(
            intervention,
            explanation=resolved,
            student_id=student_id,
            as_of=as_of,
        )
        sid = (projection.student_id or student_id or "").strip()
        if sid:
            self._bound[sid] = projection
        return projection

    def serve_projection(
        self,
        intervention: LearningIntervention,
        *,
        student_id: str = "",
        explanation: StrategyExplanationBundle | None = None,
        as_of: str | None = None,
    ) -> StrategyProjection:
        """Alias for project_intervention (Twin-port naming parity)."""
        return self.project_intervention(
            intervention,
            student_id=student_id,
            explanation=explanation,
            as_of=as_of,
        )

    def get_projection(self, student_id: str) -> StrategyProjection | None:
        """Return the bound / provider-resolved projection, or None."""
        return self._resolve_projection(student_id)

    def get_tonight_projection(self, student_id: str) -> StrategyProjectionResult:
        """Return tonight's Experience-safe Strategy projection for a student."""
        projection = self._resolve_projection(student_id)
        if projection is None:
            return StrategyProjectionResult(
                ok=False,
                error_code="NOT_FOUND",
                message="No Strategy projection bound for student",
            )
        if projection.availability == AVAILABILITY_UNAVAILABLE:
            return StrategyProjectionResult(
                ok=False,
                value=projection,
                error_code="UNAVAILABLE",
                message=projection.unavailable_reason or REASON_STRATEGY_UNAVAILABLE,
                fallback_used=True,
            )
        return StrategyProjectionResult(ok=True, value=projection)

    def get_tonight_opaque(self, student_id: str) -> dict[str, Any] | None:
        """Return Experience-safe opaque dict derived from StrategyProjection."""
        result = self.get_tonight_projection(student_id)
        if result.value is None:
            return None
        return self._opaque_tonight(result.value)

    def _resolve_projection(self, student_id: str) -> StrategyProjection | None:
        if not self.is_available():
            return self._projector.unavailable_projection(
                student_id=student_id,
                reason=REASON_STRATEGY_FLAG_OFF,
            )
        sid = (student_id or "").strip()
        if not sid:
            return None
        bound = self._bound.get(sid)
        if bound is not None:
            return bound
        if self._intervention_provider is None:
            return None
        intervention = self._intervention_provider(sid)
        if intervention is None:
            return None
        if not isinstance(intervention, LearningIntervention):
            return self._projector.unavailable_projection(
                student_id=sid,
                reason=REASON_STRATEGY_INVALID,
            )
        try:
            return self.project_intervention(intervention, student_id=sid)
        except (TypeError, ValueError, StrategyExplainabilityValidationError):
            return self._projector.unavailable_projection(
                student_id=sid,
                reason=REASON_STRATEGY_INVALID,
            )

    def _opaque_tonight(self, projection: StrategyProjection) -> dict[str, Any]:
        return {
            "primary_intervention_kind": projection.primary_intervention_kind,
            "topic_title": projection.topic_title,
            "topic_code": projection.topic_code,
            "session_plan": dict(projection.session_plan),
            "revision_plan": dict(projection.revision_plan),
            "recovery_plan": dict(projection.recovery_plan),
            "fatigue": dict(projection.fatigue),
            "confidence_intervention": dict(projection.confidence_intervention),
            "explanation_summary": projection.explanation_summary.why_summary,
            "educational_principle_ids": list(projection.educational_principle_ids),
            "adaptive_decision_id": projection.adaptive_decision_id,
            "twin_snapshot_ref": projection.twin_snapshot_ref,
            "confidence_band": projection.confidence_band,
            "mission_aligned": projection.mission_aligned,
            "strategy_decision_id": projection.strategy_decision_id,
            "authority": AUTHORITY_STRATEGY_ENGINE,
            "educational_objective": projection.educational_objective,
            "minutes_budget": projection.minutes_budget,
            "steps": [dict(step) for step in projection.steps],
            "study_plan": dict(projection.study_plan),
            "limitations_codes": list(projection.limitations_codes),
            "availability": projection.availability,
            "unavailable_reason": projection.unavailable_reason,
            "explanation": dict(projection.explanation),
            "provenance_refs": list(projection.provenance.provenance_refs),
            "projection_version": projection.projection_version,
            "student_id": projection.student_id,
        }


def build_strategy_projector(*, enabled: bool) -> StrategyProjector | None:
    """DI helper — construct StrategyProjector only when Strategy Engine is ON."""
    if not enabled:
        return None
    return StrategyProjector(enabled=True)


def build_strategy_projection_port(
    *,
    enabled: bool,
    projector: StrategyProjector | None = None,
    explainability: StrategyExplainabilityService | None = None,
    intervention_provider: (
        Callable[[str], LearningIntervention | None] | None
    ) = None,
) -> StrategyExperienceProjectionPort | None:
    """DI helper — construct StrategyProjectionPort only when flag is ON."""
    if not enabled:
        return None
    resolved = projector or StrategyProjector(enabled=True)
    return StrategyExperienceProjectionPort(
        projector=resolved,
        explainability=explainability,
        enabled=True,
        intervention_provider=intervention_provider,
    )


__all__ = [
    "PROJECTION_VERSION",
    "REASON_STRATEGY_EMPTY",
    "REASON_STRATEGY_FLAG_OFF",
    "REASON_STRATEGY_INVALID",
    "REASON_STRATEGY_UNAVAILABLE",
    "SOURCE_SERVICE_STRATEGY_PROJECTION",
    "StrategyExperienceProjectionPort",
    "StrategyProjector",
    "build_strategy_projection_port",
    "build_strategy_projector",
]
