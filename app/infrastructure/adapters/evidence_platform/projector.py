"""Evidence Projection (MS-006 E4).

Projects immutable AnalyticsSummary into governance-facing EvidenceProjection
values and implements EvidenceProjectionPort without exposing raw evaluation
objects, mutating Evidence / Twin / Adaptive / Strategy / Runtime A state, or
changing Experience UX authority.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import replace

from app.infrastructure.adapters.evidence_platform.contracts import (
    ANALYTICS_AUDIENCE_GOVERNANCE,
    ANALYTICS_AUDIENCES,
    AUTHORITY_EVIDENCE_PLATFORM,
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    AnalyticsSummary,
    ConfidenceSummaryProjection,
    EvidenceProjection,
    EvidenceProjectionProvenance,
    EvidenceProjectionResult,
    TrendMetadata,
    serialize_canonical,
)

PROJECTION_VERSION = "e4.0"

REASON_ANALYTICS_UNAVAILABLE = "analytics_unavailable"
REASON_ANALYTICS_FLAG_OFF = "analytics_flag_off"
REASON_ANALYTICS_INVALID = "analytics_invalid_summary"
REASON_ANALYTICS_EMPTY = "empty_authentic"

SOURCE_SERVICE_EVIDENCE_PROJECTION = "evidence_projector"


class EvidenceProjector:
    """Project AnalyticsSummary into governance EvidenceProjection values.

    Rules:
    - MAY read AnalyticsSummary
    - MUST NOT mutate Evidence / Twin / Adaptive / Strategy / Runtime A state,
      persist analytics, promote policies, or replace Experience UX authority
    - Identical AnalyticsSummary → identical serialize()
    """

    PROJECTOR_ID = "evidence_projector"
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
        summary_id: str = "",
        as_of: str | None = None,
        audience: str = ANALYTICS_AUDIENCE_GOVERNANCE,
        reason: str = REASON_ANALYTICS_UNAVAILABLE,
    ) -> EvidenceProjection:
        """Build an explicit unavailable governance projection (never estimated)."""
        resolved_audience = _normalize_audience(audience)
        return EvidenceProjection(
            summary_id=summary_id,
            as_of=as_of,
            projection_version=PROJECTION_VERSION,
            authority=AUTHORITY_EVIDENCE_PLATFORM,
            audience=resolved_audience,
            availability=AVAILABILITY_UNAVAILABLE,
            unavailable_reason=reason,
            limitations_codes=(reason,),
            headline=reason,
            confidence_summary=ConfidenceSummaryProjection(
                dominant_band="insufficient",
                rationale_summary=reason,
                not_proven=(reason,),
            ),
            trend_metadata=TrendMetadata(
                grain="system",
                comparable=False,
                direction="not_estimable",
                limitations=(reason,),
            ),
            provenance=EvidenceProjectionProvenance(
                summary_id=summary_id,
                authority=AUTHORITY_EVIDENCE_PLATFORM,
                as_of=as_of,
                source_services=(SOURCE_SERVICE_EVIDENCE_PROJECTION,),
            ),
        )

    def project(
        self,
        summary: AnalyticsSummary,
        *,
        audience: str | None = None,
        as_of: str | None = None,
    ) -> EvidenceProjection:
        """Project an immutable AnalyticsSummary into EvidenceProjection.

        Identical AnalyticsSummary material → identical EvidenceProjection
        serialize() every execution.
        """
        if not isinstance(summary, AnalyticsSummary):
            raise TypeError("summary must be an AnalyticsSummary")
        resolved_audience = _normalize_audience(audience or summary.audience)
        clock = as_of if as_of is not None else summary.as_of

        if summary.availability == AVAILABILITY_UNAVAILABLE:
            return self.unavailable_projection(
                summary_id=summary.summary_id,
                as_of=clock,
                audience=resolved_audience,
                reason=summary.unavailable_reason or REASON_ANALYTICS_EMPTY,
            )

        evidence_counts: Mapping[str, int] = {
            "evidence": summary.evidence_count,
            "observations": summary.observation_count,
            "students": summary.student_count,
            "evaluations": summary.evaluation_count,
            "experiments": summary.experiment_count,
        }
        headline = (
            f"{summary.evaluation_count} evaluations, "
            f"{summary.experiment_count} experiments, "
            f"{summary.evidence_count} evidence refs"
        )
        limitations = tuple(
            dict.fromkeys([*summary.limitations, *summary.narrative_constraints])
        )
        provenance_refs = tuple(
            sorted(
                {
                    *summary.evaluation_ids,
                    *summary.experiment_refs,
                    *summary.evidence_refs,
                    summary.contents_ref,
                }
            )
        )
        draft = EvidenceProjection(
            summary_id=summary.summary_id,
            as_of=clock,
            projection_version=PROJECTION_VERSION,
            authority=summary.authority or AUTHORITY_EVIDENCE_PLATFORM,
            audience=resolved_audience,
            availability=AVAILABILITY_AVAILABLE,
            unavailable_reason="",
            limitations_codes=limitations,
            headline=headline,
            policy_summaries=summary.policy_summaries,
            experiment_summaries=summary.experiment_summaries,
            evidence_counts=evidence_counts,
            confidence_summary=summary.confidence_summary,
            metric_series=summary.metric_series,
            scorecard_slice=summary.scorecard_slice,
            trend_metadata=summary.trend_metadata,
            export_ref=summary.contents_ref,
            redaction_level="standard",
            provenance=EvidenceProjectionProvenance(
                summary_id=summary.summary_id,
                evaluation_ids=summary.evaluation_ids,
                experiment_refs=summary.experiment_refs,
                evidence_refs=summary.evidence_refs,
                authority=AUTHORITY_EVIDENCE_PLATFORM,
                as_of=clock,
                provenance_refs=provenance_refs,
                source_services=(
                    SOURCE_SERVICE_EVIDENCE_PROJECTION,
                    "analytics_engine",
                    "policy_evaluation",
                    "experiment_framework",
                ),
            ),
        )
        projection_id = deterministic_projection_id(draft)
        return replace(draft, projection_id=projection_id)


class EvidenceGovernanceProjectionPort:
    """EvidenceProjectionPort implementation for governance consumers (E4).

    Read-only relative to educational history. Never promotes policies or
    serves student coaching surfaces.
    """

    PORT_ID = "evidence_governance_projection_port"

    def __init__(
        self,
        *,
        projector: EvidenceProjector | None = None,
        enabled: bool = True,
    ) -> None:
        self._projector = projector or EvidenceProjector(enabled=True)
        self._enabled = bool(enabled)
        self._bound: dict[str, EvidenceProjection] = {}

    @property
    def port_id(self) -> str:
        return self.PORT_ID

    @property
    def projector(self) -> EvidenceProjector:
        return self._projector

    def is_available(self) -> bool:
        return self._enabled and self._projector.is_enabled()

    def project_summary(
        self,
        summary: AnalyticsSummary,
        *,
        audience: str = ANALYTICS_AUDIENCE_GOVERNANCE,
        as_of: str | None = None,
    ) -> EvidenceProjection:
        """Project and bind an AnalyticsSummary for later governance export."""
        if not self.is_available():
            return self._projector.unavailable_projection(
                summary_id=getattr(summary, "summary_id", ""),
                as_of=as_of,
                audience=audience,
                reason=REASON_ANALYTICS_FLAG_OFF,
            )
        if not isinstance(summary, AnalyticsSummary):
            return self._projector.unavailable_projection(
                as_of=as_of,
                audience=audience,
                reason=REASON_ANALYTICS_INVALID,
            )
        projection = self._projector.project(
            summary, audience=audience, as_of=as_of
        )
        if projection.summary_id:
            self._bound[projection.summary_id] = projection
        return projection

    def get_projection(self, summary_id: str) -> EvidenceProjection | None:
        key = (summary_id or "").strip()
        if not key:
            return None
        return self._bound.get(key)

    def get_governance_export(
        self, summary_id: str
    ) -> EvidenceProjectionResult:
        """Return a governance-facing export envelope for a bound projection."""
        if not self.is_available():
            return EvidenceProjectionResult(
                ok=False,
                value=self._projector.unavailable_projection(
                    summary_id=summary_id,
                    reason=REASON_ANALYTICS_FLAG_OFF,
                ),
                error_code="UNAVAILABLE",
                message="EvidenceProjectionPort is disabled (feature flag OFF)",
                fallback_used=True,
            )
        projection = self.get_projection(summary_id)
        if projection is None:
            return EvidenceProjectionResult(
                ok=False,
                value=self._projector.unavailable_projection(
                    summary_id=summary_id,
                    reason=REASON_ANALYTICS_UNAVAILABLE,
                ),
                error_code="NOT_FOUND",
                message="No projection bound for summary_id",
                fallback_used=True,
            )
        return EvidenceProjectionResult(ok=True, value=projection)


def deterministic_projection_id(projection: EvidenceProjection) -> str:
    """Derive projection_id from material fields (excludes projection_id)."""
    material = projection.to_canonical_dict()
    material["projection_id"] = ""
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()
    return f"aproj-{digest[:24]}"


def _normalize_audience(audience: str) -> str:
    resolved = (audience or "").strip().lower() or ANALYTICS_AUDIENCE_GOVERNANCE
    if resolved not in ANALYTICS_AUDIENCES or not resolved:
        allowed = sorted(k for k in ANALYTICS_AUDIENCES if k)
        raise ValueError(f"audience must be one of {allowed}")
    if resolved == "student_coaching":
        raise ValueError("student_coaching is a forbidden analytics audience")
    return resolved


def build_evidence_projector(*, enabled: bool) -> EvidenceProjector | None:
    """DI helper — construct EvidenceProjector only when the flag is on."""
    if not enabled:
        return None
    return EvidenceProjector(enabled=True)


def build_evidence_projection_port(
    *,
    enabled: bool,
    projector: EvidenceProjector | None = None,
) -> EvidenceGovernanceProjectionPort | None:
    """DI helper — construct EvidenceProjectionPort only when the flag is on."""
    if not enabled:
        return None
    wired = projector or build_evidence_projector(enabled=True)
    if wired is None:
        return None
    return EvidenceGovernanceProjectionPort(projector=wired, enabled=True)


__all__ = [
    "REASON_ANALYTICS_EMPTY",
    "REASON_ANALYTICS_FLAG_OFF",
    "REASON_ANALYTICS_INVALID",
    "REASON_ANALYTICS_UNAVAILABLE",
    "SOURCE_SERVICE_EVIDENCE_PROJECTION",
    "EvidenceGovernanceProjectionPort",
    "EvidenceProjector",
    "build_evidence_projection_port",
    "build_evidence_projector",
    "deterministic_projection_id",
]
