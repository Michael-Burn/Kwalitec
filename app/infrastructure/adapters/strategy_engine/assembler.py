"""Strategy Context Assembler (MS-005 S1).

Freezes Runtime A evidence, Twin snapshot, and Adaptive recommendation into an
immutable StrategyContext. Collect / normalize / annotate only — no planning,
ranking, estimation of missing facets, or mutation of inputs.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.infrastructure.adapters.strategy_engine.contracts import (
    AUTHORITY_ADAPTIVE_ENGINE,
    AUTHORITY_DIGITAL_TWIN,
    AUTHORITY_RUNTIME_A,
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    StrategyContext,
)
from app.infrastructure.adapters.strategy_engine.validation import (
    StrategyValidationError,
    mapping_nonempty,
    validate_as_of,
    validate_student_id,
)


class StrategyContextAssembler:
    """Assemble StrategyContext from consumed Runtime A / Twin / Adaptive inputs.

    Rules:
    - MAY freeze, validate, annotate availability / provenance / refs
    - MUST NOT estimate missing Twin facets, re-rank Adaptive, or mutate inputs
    - MUST NOT call Planning / Evidence / Twin synthesis / Adaptive write APIs
    """

    ASSEMBLER_ID = "strategy_context_assembler"
    ASSEMBLER_VERSION = "1.0.0-s1"

    def __init__(self, *, enabled: bool = True) -> None:
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
        student_id: str,
        *,
        as_of: str | None = None,
        runtime_a: Mapping[str, Any] | Any | None = None,
        twin: Mapping[str, Any] | Any | None = None,
        adaptive: Mapping[str, Any] | Any | None = None,
        intervention_kinds: tuple[str, ...] | list[str] | None = None,
    ) -> StrategyContext:
        """Freeze contributing inputs into an immutable StrategyContext.

        Identical material inputs + identical ``as_of`` → identical serialize().
        """
        if not self._enabled:
            raise StrategyValidationError(
                "StrategyContextAssembler is disabled (feature flag OFF)"
            )

        sid = validate_student_id(student_id)
        clock = validate_as_of(as_of)

        runtime_payload = _freeze_payload(runtime_a)
        twin_payload = _freeze_payload(twin)
        adaptive_payload = _freeze_payload(adaptive)

        runtime_available = mapping_nonempty(runtime_payload)
        twin_available = mapping_nonempty(twin_payload)
        adaptive_available = mapping_nonempty(adaptive_payload)

        mission = dict(runtime_payload.get("mission") or {})
        mission_id = str(
            mission.get("mission_id") or mission.get("id") or ""
        ).strip()
        lifecycle_stage = str(
            runtime_payload.get("lifecycle_stage")
            or mission.get("lifecycle_stage")
            or ""
        ).strip()

        runtime_ref = _runtime_a_ref(runtime_payload, mission_id=mission_id)
        twin_ref = _twin_ref(twin_payload)
        adaptive_ref = _adaptive_ref(adaptive_payload)

        field_provenance: dict[str, Any] = {
            "runtime_a": _block_provenance(
                available=runtime_available,
                source_service="runtime_a",
                source_entity="educational_evidence",
                collected_at=clock,
                unavailable_reason="" if runtime_available else "runtime_a_unavailable",
            ),
            "twin": _block_provenance(
                available=twin_available,
                source_service="digital_twin",
                source_entity="TwinSnapshot",
                collected_at=clock,
                unavailable_reason="" if twin_available else "twin_unavailable",
            ),
            "adaptive": _block_provenance(
                available=adaptive_available,
                source_service="adaptive_engine",
                source_entity="AdaptiveDecisionRecord",
                collected_at=clock,
                unavailable_reason=(
                    "" if adaptive_available else "adaptive_unavailable"
                ),
            ),
        }

        authority_tags: list[str] = []
        if runtime_available:
            authority_tags.append(AUTHORITY_RUNTIME_A)
        if twin_available:
            authority_tags.append(AUTHORITY_DIGITAL_TWIN)
        if adaptive_available:
            authority_tags.append(AUTHORITY_ADAPTIVE_ENGINE)

        return StrategyContext(
            student_id=sid,
            as_of=clock,
            adaptive_recommendation_ref=adaptive_ref,
            twin_ref=twin_ref,
            runtime_a_evidence_ref=runtime_ref,
            adaptive_availability=(
                AVAILABILITY_AVAILABLE
                if adaptive_available
                else AVAILABILITY_UNAVAILABLE
            ),
            twin_availability=(
                AVAILABILITY_AVAILABLE if twin_available else AVAILABILITY_UNAVAILABLE
            ),
            runtime_a_availability=(
                AVAILABILITY_AVAILABLE
                if runtime_available
                else AVAILABILITY_UNAVAILABLE
            ),
            adaptive_unavailable_reason=(
                "" if adaptive_available else "adaptive_unavailable"
            ),
            twin_unavailable_reason="" if twin_available else "twin_unavailable",
            runtime_a_unavailable_reason=(
                "" if runtime_available else "runtime_a_unavailable"
            ),
            intervention_kinds=tuple(intervention_kinds or ()),
            lifecycle_stage=lifecycle_stage,
            mission_id=mission_id,
            field_provenance=field_provenance,
            authority_tags=tuple(authority_tags),
            runtime_a=runtime_payload,
            twin=twin_payload,
            adaptive=adaptive_payload,
        )


def build_strategy_context_assembler(
    *,
    enabled: bool,
) -> StrategyContextAssembler | None:
    """DI helper — construct assembler only when Strategy Engine flag is on."""
    if not enabled:
        return None
    return StrategyContextAssembler(enabled=True)


def _freeze_payload(value: Mapping[str, Any] | Any | None) -> dict[str, Any]:
    """Deep-copy input into a plain dict without mutating or aliasing the original."""
    if value is None:
        return {}
    if hasattr(value, "to_canonical_dict"):
        payload = value.to_canonical_dict()
        if not isinstance(payload, dict):
            raise StrategyValidationError(
                "input to_canonical_dict() must return a mapping"
            )
        return _deep_copy_mapping(payload)
    if isinstance(value, Mapping):
        return _deep_copy_mapping(value)
    raise StrategyValidationError(
        "runtime_a / twin / adaptive must be a mapping or contract DTO"
    )


def _deep_copy_mapping(value: Mapping[str, Any]) -> dict[str, Any]:
    """Recursively copy mappings / sequences into plain mutable-then-frozen trees."""
    result: dict[str, Any] = {}
    for key, item in value.items():
        result[str(key)] = _deep_copy_value(item)
    return result


def _deep_copy_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return _deep_copy_mapping(value)
    if isinstance(value, list | tuple):
        return [_deep_copy_value(item) for item in value]
    return value


def _block_provenance(
    *,
    available: bool,
    source_service: str,
    source_entity: str,
    collected_at: str | None,
    unavailable_reason: str,
) -> dict[str, Any]:
    return {
        "availability": (
            AVAILABILITY_AVAILABLE if available else AVAILABILITY_UNAVAILABLE
        ),
        "collected_at": collected_at,
        "kind": (
            "fact"
            if source_service == "runtime_a"
            else (
                "twin_derived"
                if source_service == "digital_twin"
                else "adaptive_derived"
            )
        ),
        "source_entity": source_entity,
        "source_service": source_service,
        "unavailable_reason": unavailable_reason,
    }


def _runtime_a_ref(payload: Mapping[str, Any], *, mission_id: str) -> str:
    evidence = dict(payload.get("evidence") or {})
    evidence_id = str(
        evidence.get("evidence_id")
        or evidence.get("id")
        or payload.get("evidence_ref")
        or ""
    ).strip()
    if evidence_id:
        return evidence_id
    if mission_id:
        return f"mission:{mission_id}"
    plan_id = str(
        (payload.get("student_goals") or {}).get("study_plan_id")
        or payload.get("study_plan_id")
        or ""
    ).strip()
    if plan_id:
        return f"study_plan:{plan_id}"
    return ""


def _twin_ref(payload: Mapping[str, Any]) -> str:
    return str(
        payload.get("twin_snapshot_ref")
        or payload.get("snapshot_version")
        or payload.get("twin_id")
        or ""
    ).strip()


def _adaptive_ref(payload: Mapping[str, Any]) -> str:
    return str(
        payload.get("decision_id")
        or payload.get("adaptive_decision_id")
        or ""
    ).strip()
