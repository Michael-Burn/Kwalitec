"""Student Twin Experience Projection (MS-004 T5).

Projects immutable TwinSnapshots into Experience-facing
StudentTwinProjection values and implements StudentTwinPort without exposing
Twin internals, triggering Twin synthesis, mutating Twin state, writing
Runtime A, or changing Experience UX authority.
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable, Mapping
from typing import Any

from app.infrastructure.adapters.digital_twin.contracts import (
    AUTHORITY_DIGITAL_TWIN,
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    FACET_COGNITIVE_LOAD,
    FACET_CONFIDENCE_TREND,
    FACET_CONSISTENCY,
    FACET_LEARNING_RHYTHM,
    FACET_PERSISTENCE,
    FACET_REVISION_BEHAVIOUR,
    FACET_SESSION_HABITS,
    TWIN_FACET_NAMES,
    ExplanationSummaryProjection,
    FacetSummaryProjection,
    ProjectionProvenance,
    SnapshotExplanation,
    StudentTwinProjection,
    TwinSnapshot,
)

PROJECTION_VERSION = "t5.0"

REASON_TWIN_UNAVAILABLE = "twin_unavailable"
REASON_TWIN_FLAG_OFF = "twin_flag_off"
REASON_TWIN_INVALID = "twin_invalid_snapshot"
REASON_READINESS_PASS_THROUGH_DEFERRED = "readiness_pass_through_deferred"

SOURCE_SERVICE_EXPERIENCE_PROJECTION = "student_twin_projector"

# Facet attribute holding the student-safe note for each Twin facet DTO.
_FACET_NOTE_ATTR: Mapping[str, str] = {
    FACET_LEARNING_RHYTHM: "cadence_note",
    FACET_CONSISTENCY: "adherence_note",
    FACET_PERSISTENCE: "continuity_note",
    FACET_REVISION_BEHAVIOUR: "revision_note",
    FACET_CONFIDENCE_TREND: "trend_note",
    FACET_SESSION_HABITS: "habits_note",
    FACET_COGNITIVE_LOAD: "load_note",
}


def _facet_obj(snapshot: TwinSnapshot, facet_name: str) -> Any:
    return getattr(snapshot.profile, facet_name)


class StudentTwinProjector:
    """Project TwinSnapshots into Experience StudentTwinProjection values.

    Rules:
    - MAY read TwinSnapshot, Twin explanations, and Twin provenance
    - MUST NOT mutate Twin state, trigger Twin synthesis, persist Twin data,
      write Runtime A, or replace Experience UX authority
    - Identical TwinSnapshot (+ optional explanation) → identical serialize()
    """

    PROJECTOR_ID = "student_twin_projector"
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

    def twin_snapshot_ref(self, snapshot: TwinSnapshot) -> str:
        """Deterministic fingerprint of TwinSnapshot material serialize."""
        if not isinstance(snapshot, TwinSnapshot):
            raise TypeError("snapshot must be a TwinSnapshot")
        digest = hashlib.sha256(snapshot.serialize().encode("utf-8")).hexdigest()
        return f"twin-{digest[:16]}"

    def unavailable_projection(
        self,
        *,
        student_id: str = "",
        as_of: str | None = None,
        reason: str = REASON_TWIN_UNAVAILABLE,
    ) -> StudentTwinProjection:
        """Build an explicit unavailable Experience projection (never estimated)."""
        return StudentTwinProjection(
            student_id=(student_id or "").strip(),
            twin_snapshot_ref="",
            twin_id="",
            as_of=as_of,
            projection_version=PROJECTION_VERSION,
            learner_profile_summary={
                "student_id": (student_id or "").strip(),
                "limitations_codes": [reason],
                "limitations_summary": reason,
            },
            facet_summaries={},
            completeness={},
            explanation_summary=ExplanationSummaryProjection(),
            provenance=ProjectionProvenance(
                twin_snapshot_ref="",
                twin_id="",
                authority=AUTHORITY_DIGITAL_TWIN,
                as_of=as_of,
                provenance_refs=(),
            ),
            availability=AVAILABILITY_UNAVAILABLE,
            unavailable_reason=reason,
            limitations_codes=(reason,),
        )

    def project(
        self,
        snapshot: TwinSnapshot,
        *,
        explanation: SnapshotExplanation | None = None,
        as_of: str | None = None,
    ) -> StudentTwinProjection:
        """Project an immutable TwinSnapshot into an Experience projection.

        Identical TwinSnapshot (+ optional explanation) material → identical
        StudentTwinProjection.serialize() every execution.
        """
        if not isinstance(snapshot, TwinSnapshot):
            raise TypeError("snapshot must be a TwinSnapshot")
        if explanation is not None and not isinstance(explanation, SnapshotExplanation):
            raise TypeError("explanation must be a SnapshotExplanation or None")

        clock = as_of if as_of is not None else snapshot.generated_at
        ref = self.twin_snapshot_ref(snapshot)
        profile = snapshot.profile
        facet_summaries = self._facet_summaries(snapshot)
        limitations = list(profile.limitations_codes or ())
        if snapshot.unavailable_summary.facets:
            limitations.append("twin_facets_unavailable")
        if snapshot.completeness.status and snapshot.completeness.status != "complete":
            limitations.append(f"twin_completeness_{snapshot.completeness.status}")
        ordered_limitations = tuple(
            dict.fromkeys(str(item) for item in limitations if item)
        )

        explanation_summary = self._explanation_summary(explanation)
        provenance_refs = self._provenance_refs(snapshot, explanation)
        preferred_minutes = None
        rhythm = profile.learning_rhythm
        if (
            getattr(rhythm, "availability", "") == AVAILABILITY_AVAILABLE
            and rhythm.typical_session_minutes is not None
        ):
            preferred_minutes = float(rhythm.typical_session_minutes)

        return StudentTwinProjection(
            student_id=profile.student_id,
            twin_snapshot_ref=ref,
            twin_id=snapshot.twin_id,
            as_of=clock,
            projection_version=PROJECTION_VERSION,
            learner_profile_summary={
                "student_id": profile.student_id,
                "limitations_codes": list(ordered_limitations),
                "limitations_summary": profile.limitations_summary,
                "profile_version": snapshot.profile_version,
                "preferred_session_minutes": preferred_minutes,
                "facet_labels": {
                    name: str(summary.get("label") or "")
                    for name, summary in sorted(facet_summaries.items())
                },
            },
            facet_summaries=facet_summaries,
            completeness=snapshot.completeness.to_canonical_dict(),
            explanation_summary=explanation_summary,
            provenance=ProjectionProvenance(
                twin_snapshot_ref=ref,
                twin_id=snapshot.twin_id,
                authority=snapshot.authority or AUTHORITY_DIGITAL_TWIN,
                source_evidence_version=snapshot.source_evidence_version,
                as_of=clock,
                provenance_refs=provenance_refs,
                contributing_runtime_a_sources=(
                    snapshot.provenance_summary.contributing_runtime_a_sources
                ),
                snapshot_provenance=snapshot.provenance.to_canonical_dict(),
                provenance_summary=snapshot.provenance_summary.to_canonical_dict(),
            ),
            availability=AVAILABILITY_AVAILABLE,
            unavailable_reason="",
            limitations_codes=ordered_limitations,
        )

    def _facet_summaries(self, snapshot: TwinSnapshot) -> dict[str, Any]:
        summaries: dict[str, Any] = {}
        for name in sorted(TWIN_FACET_NAMES):
            facet = _facet_obj(snapshot, name)
            note_attr = _FACET_NOTE_ATTR.get(name, "")
            note = str(getattr(facet, note_attr, "") or "") if note_attr else ""
            summaries[name] = FacetSummaryProjection(
                facet_name=name,
                label=str(getattr(facet, "label", "") or ""),
                availability=str(getattr(facet, "availability", "") or ""),
                unavailable_reason=str(
                    getattr(facet, "unavailable_reason", "") or ""
                ),
                summary_note=note,
                evidence_refs=tuple(getattr(facet, "evidence_refs", ()) or ()),
            ).to_canonical_dict()
        return summaries

    def _explanation_summary(
        self,
        explanation: SnapshotExplanation | None,
    ) -> ExplanationSummaryProjection:
        if explanation is None:
            return ExplanationSummaryProjection()
        facet_summaries: list[str] = []
        for item in explanation.facet_explanations:
            derivation = (item.derivation_summary or "").strip()
            unavailable = (item.unavailable_reasoning or "").strip()
            text = derivation or unavailable
            if text:
                facet_summaries.append(f"{item.facet_name}: {text}")
        return ExplanationSummaryProjection(
            overall_completeness_explanation=(
                explanation.overall_completeness_explanation
            ),
            unavailable_summary_explanation=(
                explanation.unavailable_summary_explanation
            ),
            evidence_coverage_summary=explanation.evidence_coverage_summary,
            facet_explanation_summaries=tuple(facet_summaries),
            provenance_refs=tuple(explanation.provenance_refs),
        )

    def _provenance_refs(
        self,
        snapshot: TwinSnapshot,
        explanation: SnapshotExplanation | None,
    ) -> tuple[str, ...]:
        refs: list[str] = []
        for source in snapshot.provenance_summary.contributing_runtime_a_sources:
            if source:
                refs.append(str(source))
        for facet_name in sorted(TWIN_FACET_NAMES):
            facet = _facet_obj(snapshot, facet_name)
            for ref in getattr(facet, "evidence_refs", ()) or ():
                if ref:
                    refs.append(str(ref))
        if explanation is not None:
            for ref in explanation.provenance_refs:
                if ref:
                    refs.append(str(ref))
        return tuple(dict.fromkeys(refs))


class StudentTwinProjectionPort:
    """StudentTwinPort implementation backed by Twin Experience projections.

    Experience consumes StudentTwinProjection-derived opaque dicts only.
    Does not synthesise Twin, mutate Twin state, persist Twin data, write
    Runtime A, or change Adaptive / Experience UX authority.
    """

    ADAPTER_ID = "student_twin_projection_port"
    ADAPTER_VERSION = PROJECTION_VERSION

    def __init__(
        self,
        *,
        projector: StudentTwinProjector | None = None,
        enabled: bool = True,
        snapshot_provider: Callable[[str], TwinSnapshot | None] | None = None,
        explanation_provider: (
            Callable[[TwinSnapshot], SnapshotExplanation | None] | None
        ) = None,
    ) -> None:
        self._enabled = bool(enabled)
        self._projector = projector or StudentTwinProjector(enabled=enabled)
        self._snapshot_provider = snapshot_provider
        self._explanation_provider = explanation_provider
        self._bound: dict[str, StudentTwinProjection] = {}

    @property
    def component_id(self) -> str:
        return self.ADAPTER_ID

    @property
    def component_version(self) -> str:
        return self.ADAPTER_VERSION

    def is_available(self) -> bool:
        return self._enabled and self._projector.is_enabled()

    def projector(self) -> StudentTwinProjector:
        return self._projector

    def serve_projection(
        self,
        snapshot: TwinSnapshot,
        *,
        explanation: SnapshotExplanation | None = None,
        as_of: str | None = None,
    ) -> StudentTwinProjection:
        """Project and bind a TwinSnapshot for subsequent StudentTwinPort reads.

        Does not trigger Twin synthesis — caller supplies an assembled snapshot.
        """
        projection = self._projector.project(
            snapshot, explanation=explanation, as_of=as_of
        )
        if projection.student_id:
            self._bound[projection.student_id] = projection
        return projection

    def get_projection(self, student_id: str) -> StudentTwinProjection | None:
        """Return the bound / provider-resolved projection, or None."""
        return self._resolve_projection(student_id)

    def get_learner_summary(self, student_id: str) -> dict[str, Any] | None:
        projection = self._resolve_projection(student_id)
        if projection is None:
            return None
        return self._opaque_learner_summary(projection)

    def get_readiness_summary(self, student_id: str) -> dict[str, Any] | None:
        projection = self._resolve_projection(student_id)
        if projection is None:
            return None
        return self._opaque_readiness_summary(projection)

    def get_learning_insights(self, student_id: str) -> dict[str, Any] | None:
        projection = self._resolve_projection(student_id)
        if projection is None:
            return None
        return self._opaque_learning_insights(projection)

    def _resolve_projection(self, student_id: str) -> StudentTwinProjection | None:
        if not self.is_available():
            return self._projector.unavailable_projection(
                student_id=student_id,
                reason=REASON_TWIN_FLAG_OFF,
            )
        sid = (student_id or "").strip()
        if not sid:
            return None
        bound = self._bound.get(sid)
        if bound is not None:
            return bound
        if self._snapshot_provider is None:
            return None
        snapshot = self._snapshot_provider(sid)
        if snapshot is None:
            return None
        if not isinstance(snapshot, TwinSnapshot):
            return self._projector.unavailable_projection(
                student_id=sid,
                reason=REASON_TWIN_INVALID,
            )
        explanation = None
        if self._explanation_provider is not None:
            explanation = self._explanation_provider(snapshot)
        twin_sid = (snapshot.profile.student_id or "").strip()
        if twin_sid and twin_sid != sid:
            return self._projector.unavailable_projection(
                student_id=sid,
                reason=REASON_TWIN_INVALID,
            )
        return self.serve_projection(snapshot, explanation=explanation)

    def _opaque_learner_summary(
        self, projection: StudentTwinProjection
    ) -> dict[str, Any]:
        preferred_minutes = projection.learner_profile_summary.get(
            "preferred_session_minutes"
        )
        return {
            "display_name": "",
            "examination_label": "",
            "exam_countdown_days": None,
            "preferences": {
                "preferred_session_minutes": preferred_minutes,
                "preferred_study_days": (),
                "reminder_enabled": False,
                "quiet_hours_label": "",
            },
            "goals": (),
            "account": {},
            "statistics": {
                "total_study_minutes": 0,
                "sessions_completed": 0,
                "topics_mastered": 0,
                "current_exam_readiness": None,
                "study_streak_days": 0,
            },
            "student_id": projection.student_id,
            "twin_snapshot_ref": projection.twin_snapshot_ref,
            "twin_id": projection.twin_id,
            "facet_summaries": {
                str(k): dict(v) if isinstance(v, Mapping) else v
                for k, v in sorted(projection.facet_summaries.items())
            },
            "completeness": dict(projection.completeness),
            "provenance_refs": list(projection.provenance.provenance_refs),
            "limitations_codes": list(projection.limitations_codes),
            "learner_profile_summary": dict(projection.learner_profile_summary),
            "availability": projection.availability,
            "unavailable_reason": projection.unavailable_reason,
            "authority": AUTHORITY_DIGITAL_TWIN,
        }

    def _opaque_readiness_summary(
        self, projection: StudentTwinProjection
    ) -> dict[str, Any]:
        # Twin must not invent readiness maths — PredictionFacet pass-through
        # is deferred. Return authentic empty readiness with limitation.
        return {
            "examination_label": "",
            "exam_countdown_days": None,
            "exam_readiness": None,
            "readiness_score": None,
            "readiness_label": "",
            "availability": AVAILABILITY_UNAVAILABLE,
            "unavailable_reason": REASON_READINESS_PASS_THROUGH_DEFERRED,
            "twin_snapshot_ref": projection.twin_snapshot_ref,
            "twin_id": projection.twin_id,
            "provenance_refs": list(projection.provenance.provenance_refs),
            "limitations_codes": list(
                dict.fromkeys(
                    [
                        *projection.limitations_codes,
                        REASON_READINESS_PASS_THROUGH_DEFERRED,
                    ]
                )
            ),
            "authority": AUTHORITY_DIGITAL_TWIN,
        }

    def _opaque_learning_insights(
        self, projection: StudentTwinProjection
    ) -> dict[str, Any]:
        # History Bridge remains narrative SoT for session cards — Twin must
        # not fabricate completed_sessions / revision history entries.
        return {
            "completed_sessions": (),
            "total_study_minutes": 0,
            "readiness_progression": (),
            "mastered_topics": (),
            "revision_history": (),
            "recent_achievements": (),
            "sessions_completed": 0,
            "topics_mastered": 0,
            "student_id": projection.student_id,
            "twin_snapshot_ref": projection.twin_snapshot_ref,
            "twin_id": projection.twin_id,
            "facet_summaries": {
                str(k): dict(v) if isinstance(v, Mapping) else v
                for k, v in sorted(projection.facet_summaries.items())
            },
            "completeness": dict(projection.completeness),
            "explanation_summary": (
                projection.explanation_summary.to_canonical_dict()
            ),
            "provenance_refs": list(projection.provenance.provenance_refs),
            "limitations_codes": list(projection.limitations_codes),
            "availability": projection.availability,
            "unavailable_reason": projection.unavailable_reason,
            "authority": AUTHORITY_DIGITAL_TWIN,
        }


def build_student_twin_projector(*, enabled: bool) -> StudentTwinProjector | None:
    """DI helper — construct StudentTwinProjector only when Digital Twin is ON."""
    if not enabled:
        return None
    return StudentTwinProjector(enabled=True)


def build_student_twin_projection_port(
    *,
    enabled: bool,
    projector: StudentTwinProjector | None = None,
    snapshot_provider: Callable[[str], TwinSnapshot | None] | None = None,
    explanation_provider: (
        Callable[[TwinSnapshot], SnapshotExplanation | None] | None
    ) = None,
) -> StudentTwinProjectionPort | None:
    """DI helper — construct StudentTwinProjectionPort only when flag is ON."""
    if not enabled:
        return None
    resolved = projector or StudentTwinProjector(enabled=True)
    return StudentTwinProjectionPort(
        projector=resolved,
        enabled=True,
        snapshot_provider=snapshot_provider,
        explanation_provider=explanation_provider,
    )


__all__ = [
    "PROJECTION_VERSION",
    "REASON_READINESS_PASS_THROUGH_DEFERRED",
    "REASON_TWIN_FLAG_OFF",
    "REASON_TWIN_INVALID",
    "REASON_TWIN_UNAVAILABLE",
    "SOURCE_SERVICE_EXPERIENCE_PROJECTION",
    "StudentTwinProjectionPort",
    "StudentTwinProjector",
    "build_student_twin_projection_port",
    "build_student_twin_projector",
]
