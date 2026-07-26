"""Twin Input Adapter (MS-004 T4).

Read-only Adaptive consumption of immutable TwinSnapshots. Projects Twin
profile / provenance / optional explanations into AdaptiveInputBundle
enrichment. Does not synthesise Twin, mutate Twin state, persist Twin data,
write Runtime A, or depend on Experience.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from typing import Any

from app.infrastructure.adapters.adaptive_engine.contracts import (
    AUTHORITY_RUNTIME_A,
    AdaptiveInputBundle,
    TwinAdaptiveInputAttachment,
)
from app.infrastructure.adapters.adaptive_engine.provenance import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    FIELD_TWIN,
    available_provenance,
    freeze_provenance_map,
    unavailable_provenance,
)
from app.infrastructure.adapters.digital_twin.contracts import (
    AUTHORITY_DIGITAL_TWIN,
    SnapshotExplanation,
    TwinSnapshot,
)
from app.infrastructure.adapters.digital_twin.contracts import (
    AVAILABILITY_AVAILABLE as TWIN_AVAILABLE,
)

REASON_TWIN_UNAVAILABLE = "twin_unavailable"
REASON_TWIN_FLAG_OFF = "twin_flag_off"
REASON_TWIN_INVALID = "twin_invalid_snapshot"

SOURCE_SERVICE_TWIN_INPUT = "twin_input_adapter"
SOURCE_ENTITY_TWIN_SNAPSHOT = "TwinSnapshot"


class TwinInputAdapter:
    """Project TwinSnapshots into Adaptive TwinAdaptiveInputAttachment values.

    Rules:
    - MAY read TwinSnapshot, Twin explanations, and Twin provenance
    - MUST NOT mutate Twin state, trigger Twin synthesis, persist Twin data,
      write Runtime A, or import Experience
    - Fail-open: missing Twin → unavailable attachment; Runtime A unchanged
    """

    ADAPTER_ID = "twin_input_adapter"
    ADAPTER_VERSION = "1.0.0-t4"

    def __init__(self, *, enabled: bool = True) -> None:
        self._enabled = bool(enabled)

    @property
    def adapter_id(self) -> str:
        return self.ADAPTER_ID

    @property
    def adapter_version(self) -> str:
        return self.ADAPTER_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    def twin_snapshot_ref(self, snapshot: TwinSnapshot) -> str:
        """Deterministic fingerprint of TwinSnapshot material serialize."""
        if not isinstance(snapshot, TwinSnapshot):
            raise TypeError("snapshot must be a TwinSnapshot")
        digest = hashlib.sha256(snapshot.serialize().encode("utf-8")).hexdigest()
        return f"twin-{digest[:16]}"

    def unavailable_attachment(
        self,
        *,
        as_of: str | None = None,
        reason: str = REASON_TWIN_UNAVAILABLE,
    ) -> TwinAdaptiveInputAttachment:
        """Build an explicit unavailable Twin attachment (never estimated)."""
        return TwinAdaptiveInputAttachment(
            twin_snapshot_ref="",
            twin_id="",
            as_of=as_of,
            behaviour={},
            memory={},
            predictions={},
            limitations=(reason,),
            completeness={},
            provenance={},
            explanation={},
            availability=AVAILABILITY_UNAVAILABLE,
            unavailable_reason=reason,
        )

    def project(
        self,
        snapshot: TwinSnapshot,
        *,
        explanation: SnapshotExplanation | None = None,
        as_of: str | None = None,
    ) -> TwinAdaptiveInputAttachment:
        """Project an immutable TwinSnapshot into Adaptive attachment fields.

        Identical TwinSnapshot (+ optional explanation) material → identical
        TwinAdaptiveInputAttachment.serialize() every execution.
        """
        if not isinstance(snapshot, TwinSnapshot):
            raise TypeError("snapshot must be a TwinSnapshot")
        if explanation is not None and not isinstance(explanation, SnapshotExplanation):
            raise TypeError("explanation must be a SnapshotExplanation or None")

        clock = as_of if as_of is not None else snapshot.generated_at
        profile = snapshot.profile
        behaviour = {
            "consistency": profile.consistency.to_canonical_dict(),
            "learning_rhythm": profile.learning_rhythm.to_canonical_dict(),
            "persistence": profile.persistence.to_canonical_dict(),
            "session_habits": profile.session_habits.to_canonical_dict(),
        }
        memory = {
            "confidence_trend": profile.confidence_trend.to_canonical_dict(),
            "revision_behaviour": profile.revision_behaviour.to_canonical_dict(),
        }
        # Structural Twin indicators only — never invent readiness / mastery.
        predictions = {
            "cognitive_load_indicators": (
                profile.cognitive_load_indicators.to_canonical_dict()
            ),
        }
        limitations = list(profile.limitations_codes or ())
        if snapshot.unavailable_summary.facets:
            limitations.append("twin_facets_unavailable")
        if snapshot.completeness.status and snapshot.completeness.status != "complete":
            limitations.append(f"twin_completeness_{snapshot.completeness.status}")

        explanation_payload: Mapping[str, Any] = {}
        if explanation is not None:
            explanation_payload = explanation.to_canonical_dict()

        return TwinAdaptiveInputAttachment(
            twin_snapshot_ref=self.twin_snapshot_ref(snapshot),
            twin_id=snapshot.twin_id,
            as_of=clock,
            behaviour=behaviour,
            memory=memory,
            predictions=predictions,
            limitations=tuple(dict.fromkeys(str(item) for item in limitations if item)),
            completeness=snapshot.completeness.to_canonical_dict(),
            provenance={
                "authority": snapshot.authority or AUTHORITY_DIGITAL_TWIN,
                "field_provenance": {
                    str(k): dict(v) if isinstance(v, Mapping) else v
                    for k, v in sorted(snapshot.field_provenance.items())
                },
                "provenance": snapshot.provenance.to_canonical_dict(),
                "provenance_summary": snapshot.provenance_summary.to_canonical_dict(),
                "source_evidence_version": snapshot.source_evidence_version,
                "version": snapshot.version().to_canonical_dict(),
            },
            explanation=explanation_payload,
            availability=AVAILABILITY_AVAILABLE,
            unavailable_reason="",
        )

    def enrich_bundle(
        self,
        bundle: AdaptiveInputBundle,
        *,
        snapshot: TwinSnapshot | None = None,
        explanation: SnapshotExplanation | None = None,
        collected_at: str = "",
    ) -> AdaptiveInputBundle:
        """Return a new AdaptiveInputBundle with Twin attachment + provenance.

        Fail-open: ``snapshot is None`` → unavailable Twin attachment. Runtime A
        blocks are copied unchanged. Never mutates the input bundle or Twin.
        """
        if not isinstance(bundle, AdaptiveInputBundle):
            raise TypeError("bundle must be an AdaptiveInputBundle")
        if not self._enabled:
            return self._with_twin(
                bundle,
                attachment=self.unavailable_attachment(
                    as_of=bundle.as_of,
                    reason=REASON_TWIN_FLAG_OFF,
                ),
                collected_at=collected_at or bundle.as_of or "",
                available=False,
                reason=REASON_TWIN_FLAG_OFF,
            )

        if snapshot is None:
            return self._with_twin(
                bundle,
                attachment=self.unavailable_attachment(
                    as_of=bundle.as_of,
                    reason=REASON_TWIN_UNAVAILABLE,
                ),
                collected_at=collected_at or bundle.as_of or "",
                available=False,
                reason=REASON_TWIN_UNAVAILABLE,
            )

        if not isinstance(snapshot, TwinSnapshot):
            return self._with_twin(
                bundle,
                attachment=self.unavailable_attachment(
                    as_of=bundle.as_of,
                    reason=REASON_TWIN_INVALID,
                ),
                collected_at=collected_at or bundle.as_of or "",
                available=False,
                reason=REASON_TWIN_INVALID,
            )

        # Twin student identity must align when present.
        twin_sid = (snapshot.profile.student_id or "").strip()
        if twin_sid and twin_sid != bundle.student_id:
            return self._with_twin(
                bundle,
                attachment=self.unavailable_attachment(
                    as_of=bundle.as_of,
                    reason=REASON_TWIN_INVALID,
                ),
                collected_at=collected_at or bundle.as_of or "",
                available=False,
                reason=REASON_TWIN_INVALID,
            )

        attachment = self.project(
            snapshot,
            explanation=explanation,
            as_of=bundle.as_of,
        )
        return self._with_twin(
            bundle,
            attachment=attachment,
            collected_at=collected_at or bundle.as_of or "",
            available=True,
            reason="",
        )

    def _with_twin(
        self,
        bundle: AdaptiveInputBundle,
        *,
        attachment: TwinAdaptiveInputAttachment,
        collected_at: str,
        available: bool,
        reason: str,
    ) -> AdaptiveInputBundle:
        provenance = {
            str(k): dict(v) if isinstance(v, Mapping) else v
            for k, v in bundle.field_provenance.items()
        }
        if available:
            provenance[FIELD_TWIN] = available_provenance(
                source_service=SOURCE_SERVICE_TWIN_INPUT,
                source_entity=SOURCE_ENTITY_TWIN_SNAPSHOT,
                collected_at=collected_at,
            ).to_canonical_dict()
        else:
            provenance[FIELD_TWIN] = unavailable_provenance(
                source_service=SOURCE_SERVICE_TWIN_INPUT,
                source_entity=SOURCE_ENTITY_TWIN_SNAPSHOT,
                collected_at=collected_at,
                reason=reason,
            ).to_canonical_dict()

        tags = list(bundle.authority_tags or ())
        if AUTHORITY_DIGITAL_TWIN not in tags and available:
            tags.append(AUTHORITY_DIGITAL_TWIN)
        if AUTHORITY_RUNTIME_A not in tags:
            tags.insert(0, AUTHORITY_RUNTIME_A)
        ordered_tags = tuple(
            sorted(set(tags), key=lambda t: (t != AUTHORITY_RUNTIME_A, t))
        )

        return AdaptiveInputBundle(
            student_id=bundle.student_id,
            as_of=bundle.as_of,
            evidence=dict(bundle.evidence),
            topic_progress=tuple(dict(item) for item in bundle.topic_progress),
            study_attempts=tuple(dict(item) for item in bundle.study_attempts),
            readiness=dict(bundle.readiness),
            mission=dict(bundle.mission),
            curriculum=dict(bundle.curriculum),
            student_goals=dict(bundle.student_goals),
            authority_tags=ordered_tags,
            lifecycle_stage=bundle.lifecycle_stage,
            field_provenance=freeze_provenance_map(provenance),
            twin=attachment,
        )


def build_twin_input_adapter(*, enabled: bool) -> TwinInputAdapter | None:
    """DI helper — construct TwinInputAdapter only when Digital Twin is ON."""
    if not enabled:
        return None
    return TwinInputAdapter(enabled=True)


def twin_attachment_is_available(twin: Mapping[str, Any] | None) -> bool:
    """True when AdaptiveInputBundle.twin carries an available attachment."""
    if not twin:
        return False
    return str(twin.get("availability") or "").strip().lower() == TWIN_AVAILABLE
