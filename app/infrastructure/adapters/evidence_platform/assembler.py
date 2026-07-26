"""Evidence Assembler (MS-006 E1).

Projects CollectedObservation into an immutable EvidenceRecord draft
(quality + availability + provenance). Does not assign evidence_id (Factory),
estimate facts, score outcomes, or mutate inputs.
"""

from __future__ import annotations

from collections.abc import Mapping

from app.infrastructure.adapters.evidence_platform.collector import CollectedObservation
from app.infrastructure.adapters.evidence_platform.contracts import (
    AUTHORITY_EVIDENCE_PLATFORM,
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    CLASS_FACT_EVENT,
    CLASS_OPS_EVENT,
    CLASS_RESEARCH_EVENT,
    EVIDENCE_VERSION_E1,
    QUALITY_FAIL,
    QUALITY_INELIGIBLE,
    QUALITY_PASS,
    REF_KIND_RUNTIME_A,
    EvidenceQuality,
    EvidenceRecord,
)
from app.infrastructure.adapters.evidence_platform.provenance import (
    REASON_CLAIM_BOUNDARY,
    REASON_EMPTY_OBSERVATION,
    REASON_MISSING_RUNTIME_A,
    SOURCE_SERVICE_EVIDENCE,
    freeze_provenance_map,
)
from app.infrastructure.adapters.evidence_platform.validation import (
    EvidenceValidationError,
    EvidenceValidator,
)


class EvidenceAssembler:
    """Assemble EvidenceRecord structure from CollectedObservation.

    Rules:
    - MAY annotate quality / availability / provenance
    - MUST NOT estimate missing Runtime A facts, score outcomes, or mutate inputs
    - MUST NOT persist, run experiments, or evaluate policies
    """

    ASSEMBLER_ID = "evidence_assembler"
    ASSEMBLER_VERSION = "1.0.0-e1"

    def __init__(
        self,
        *,
        validator: EvidenceValidator | None = None,
        enabled: bool = True,
    ) -> None:
        self._validator = validator or EvidenceValidator()
        self._enabled = bool(enabled)

    @property
    def assembler_id(self) -> str:
        return self.ASSEMBLER_ID

    @property
    def assembler_version(self) -> str:
        return self.ASSEMBLER_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    def assemble(
        self,
        observation: CollectedObservation,
        *,
        evidence_id: str = "",
    ) -> EvidenceRecord:
        """Project CollectedObservation into EvidenceRecord (optional id)."""
        if not self._enabled:
            raise EvidenceValidationError(
                "EvidenceAssembler is disabled (feature flag OFF)"
            )
        if not isinstance(observation, CollectedObservation):
            raise EvidenceValidationError(
                "observation must be a CollectedObservation"
            )

        sid = self._validator.validate_student_id(observation.student_id)
        quality, limitations, availability, unavailable_reason = _evaluate_quality(
            observation
        )
        provenance = {
            **{
                str(k): dict(v) if isinstance(v, Mapping) else v
                for k, v in observation.field_provenance.items()
            },
            "collection": {
                "availability": AVAILABILITY_AVAILABLE,
                "collected_at": (
                    observation.ingested_at or observation.observed_at or ""
                ),
                "source_entity": "EvidenceRecord",
                "source_service": SOURCE_SERVICE_EVIDENCE,
                "unavailable_reason": "",
                "collector_version": "1.0.0-e1",
                "assembler_version": self.ASSEMBLER_VERSION,
            },
        }

        return EvidenceRecord(
            evidence_id=(evidence_id or "").strip(),
            evidence_version=EVIDENCE_VERSION_E1,
            student_id=sid,
            source_refs=observation.source_refs,
            evidence_class=observation.evidence_class,
            event_type=observation.event_type,
            claim_boundary=observation.claim_boundary,
            quality=quality,
            payload_summary=dict(observation.payload_summary),
            provenance=freeze_provenance_map(provenance),
            limitations=tuple(
                dict.fromkeys([*observation.limitations, *limitations])
            ),
            engine_version=EVIDENCE_VERSION_E1,
            observed_at=observation.observed_at,
            ingested_at=observation.ingested_at,
            as_of=observation.as_of,
            authority=AUTHORITY_EVIDENCE_PLATFORM,
            availability=availability,
            unavailable_reason=unavailable_reason,
        )


def build_evidence_assembler(
    *,
    enabled: bool,
    validator: EvidenceValidator | None = None,
) -> EvidenceAssembler | None:
    """DI helper — construct EvidenceAssembler only when the flag is on."""
    if not enabled:
        return None
    return EvidenceAssembler(validator=validator, enabled=True)


def _evaluate_quality(
    observation: CollectedObservation,
) -> tuple[EvidenceQuality, list[str], str, str]:
    """Structural quality gate — no scoring / interpretation."""
    codes: list[str] = []
    limitations: list[str] = []
    runtime_a_present = any(
        ref.ref_kind == REF_KIND_RUNTIME_A for ref in observation.source_refs
    )

    if not observation.source_refs:
        codes.append(REASON_EMPTY_OBSERVATION)
        limitations.append(REASON_EMPTY_OBSERVATION)

    evidence_class = observation.evidence_class
    if (
        evidence_class == CLASS_FACT_EVENT
        and not runtime_a_present
        and evidence_class not in {CLASS_OPS_EVENT, CLASS_RESEARCH_EVENT}
    ):
        codes.append(REASON_MISSING_RUNTIME_A)
        limitations.append(REASON_MISSING_RUNTIME_A)

    # Claim-boundary honesty: organisation-tagged learning_depth leakage.
    for ref in observation.source_refs:
        if (
            observation.claim_boundary == "learning_depth"
            and ref.claim_boundary == "organisation"
            and ref.ref_kind == REF_KIND_RUNTIME_A
        ):
            codes.append(REASON_CLAIM_BOUNDARY)
            limitations.append(REASON_CLAIM_BOUNDARY)
            break

    if REASON_CLAIM_BOUNDARY in codes:
        result = QUALITY_FAIL
        availability = AVAILABILITY_AVAILABLE
        unavailable_reason = ""
        summary = "Claim-boundary mismatch — gate failed."
    elif not observation.source_refs:
        result = QUALITY_INELIGIBLE
        availability = AVAILABILITY_UNAVAILABLE
        unavailable_reason = REASON_EMPTY_OBSERVATION
        summary = "Empty observation — no source refs."
    elif REASON_MISSING_RUNTIME_A in codes:
        result = QUALITY_INELIGIBLE
        availability = AVAILABILITY_AVAILABLE
        unavailable_reason = ""
        summary = "FACT_EVENT without Runtime A ref — ineligible for promote-grade use."
    else:
        result = QUALITY_PASS
        availability = AVAILABILITY_AVAILABLE
        unavailable_reason = ""
        summary = "Structural quality gate passed."

    quality = EvidenceQuality(
        result=result,
        codes=tuple(dict.fromkeys(codes)),
        summary=summary,
        runtime_a_ref_present=runtime_a_present,
    )
    return quality, limitations, availability, unavailable_reason
