"""Digital Twin Adapter — MS-004 T0 contract surface.

Implements StudentDigitalTwinContract / TwinAdapter. T0 is contracts-only:
no synthesis, no Runtime A collectors, no Experience cutover, no persistence.
"""

from __future__ import annotations

from app.infrastructure.adapters.digital_twin.contracts import (
    AUTHORITY_DIGITAL_TWIN,
    AVAILABILITY_UNAVAILABLE,
    COMPLETENESS_EMPTY,
    TWIN_FACET_NAMES,
    TwinCompleteness,
    TwinProfile,
    TwinProvenance,
    TwinResult,
    TwinSnapshot,
)


class DigitalTwinAdapter:
    """Digital Twin Adapter — inert T0 contracts stub.

    When constructed behind ``ENABLE_DIGITAL_TWIN``, exposes Twin snapshot
    contracts only. Facet synthesis is owned by ``TwinFacetAssembler`` (T1).
    Does not persist snapshots, serve Experience ``StudentTwinPort``, or
    attach Adaptive inputs.
    """

    ADAPTER_ID = "digital_twin"
    ADAPTER_VERSION = "0.1.0-t0"
    PROFILE_VERSION = "t0.1"
    SOURCE_EVIDENCE_VERSION = ""

    def __init__(self) -> None:
        self._available = True

    @property
    def adapter_id(self) -> str:
        return self.ADAPTER_ID

    @property
    def adapter_version(self) -> str:
        return self.ADAPTER_VERSION

    def is_available(self) -> bool:
        return self._available

    def snapshot(self, profile: TwinProfile) -> TwinSnapshot:
        """Project a TwinProfile into an immutable TwinSnapshot (no synthesis)."""
        if not isinstance(profile, TwinProfile):
            raise TypeError("profile must be a TwinProfile")
        return empty_twin_snapshot(profile=profile)

    def assemble_snapshot(
        self,
        student_id: str,
        *,
        profile: TwinProfile | None = None,
        as_of: str | None = None,
        mode: str = "contracts",
    ) -> TwinResult:
        """Produce a TwinSnapshot behind the Student Digital Twin contract.

        ``mode`` is accepted for interface stability (shadow / authority later).
        T0 never writes Runtime A or Experience state and performs no synthesis.
        """
        sid = (student_id or "").strip()
        if not sid:
            return TwinResult(
                ok=False,
                error_code="INVALID_STATE",
                message="student_id must be a non-empty string",
            )
        if as_of is not None and not isinstance(as_of, str):
            return TwinResult(
                ok=False,
                error_code="INVALID_STATE",
                message="as_of must be an ISO string or None",
            )
        resolved = profile
        if resolved is None:
            resolved = TwinProfile(student_id=sid)
        elif resolved.student_id and resolved.student_id != sid:
            return TwinResult(
                ok=False,
                error_code="INVALID_STATE",
                message="profile.student_id must match student_id",
            )
        elif not resolved.student_id:
            resolved = TwinProfile(
                student_id=sid,
                learning_rhythm=resolved.learning_rhythm,
                consistency=resolved.consistency,
                persistence=resolved.persistence,
                revision_behaviour=resolved.revision_behaviour,
                confidence_trend=resolved.confidence_trend,
                session_habits=resolved.session_habits,
                cognitive_load_indicators=resolved.cognitive_load_indicators,
                limitations_codes=resolved.limitations_codes,
                limitations_summary=resolved.limitations_summary,
            )
        _ = mode
        return TwinResult(
            ok=True,
            value=empty_twin_snapshot(profile=resolved, generated_at=as_of),
        )


def empty_twin_snapshot(
    *,
    profile: TwinProfile | None = None,
    generated_at: str | None = None,
) -> TwinSnapshot:
    """Build a structurally complete empty TwinSnapshot (T0 stub)."""
    resolved = profile or TwinProfile()
    facet_names = tuple(sorted(TWIN_FACET_NAMES))
    return TwinSnapshot(
        profile=resolved,
        profile_version=DigitalTwinAdapter.PROFILE_VERSION,
        source_evidence_version=DigitalTwinAdapter.SOURCE_EVIDENCE_VERSION,
        generated_at=generated_at,
        provenance=TwinProvenance(
            source_service="digital_twin",
            source_entity="TwinSnapshot",
            collected_at=generated_at,
            availability=AVAILABILITY_UNAVAILABLE,
            unavailable_reason="contracts_only_no_synthesis",
            kind="twin_derived",
        ),
        completeness=TwinCompleteness(
            score=None,
            facets_present=(),
            facets_unavailable=facet_names,
            status=COMPLETENESS_EMPTY,
            summary="T0 contracts only — Twin synthesis not implemented.",
        ),
        twin_id=(
            f"twin-{resolved.student_id}" if resolved.student_id else ""
        ),
        authority=AUTHORITY_DIGITAL_TWIN,
    )


def build_digital_twin_adapter(*, enabled: bool) -> DigitalTwinAdapter | None:
    """DI helper — construct DigitalTwinAdapter only when the flag is on."""
    if not enabled:
        return None
    return DigitalTwinAdapter()
