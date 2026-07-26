"""Field provenance helpers for Evidence Collection (MS-006 E1).

Every collected block exposes source service, source entity, collection
timestamp, and availability. Missing upstream inputs are explicit
``unavailable`` entries — never estimated.
"""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Any

AVAILABILITY_AVAILABLE = "available"
AVAILABILITY_UNAVAILABLE = "unavailable"

SOURCE_SERVICE_EVIDENCE = "evidence_platform"
SOURCE_SERVICE_RUNTIME_A = "runtime_a"
SOURCE_SERVICE_EXPERIENCE = "experience"
SOURCE_SERVICE_STRATEGY = "strategy_engine"
SOURCE_SERVICE_ADAPTIVE = "adaptive_engine"
SOURCE_SERVICE_TWIN = "digital_twin"

REASON_RUNTIME_A_UNAVAILABLE = "runtime_a_unavailable"
REASON_EXPERIENCE_UNAVAILABLE = "experience_unavailable"
REASON_STRATEGY_UNAVAILABLE = "strategy_unavailable"
REASON_ADAPTIVE_UNAVAILABLE = "adaptive_unavailable"
REASON_TWIN_UNAVAILABLE = "twin_unavailable"
REASON_MISSING_RUNTIME_A = "MISSING_RUNTIME_A"
REASON_EMPTY_OBSERVATION = "empty_observation"
REASON_CROSS_STUDENT = "CROSS_STUDENT_FORBIDDEN"
REASON_CLAIM_BOUNDARY = "CLAIM_BOUNDARY_MISMATCH"


def freeze_provenance_map(
    value: Mapping[str, Mapping[str, Any] | Any] | None,
) -> Mapping[str, Any]:
    """Freeze a field→provenance mapping for EvidenceRecord.provenance."""
    if value is None:
        return MappingProxyType({})
    frozen: dict[str, Any] = {}
    for key in sorted(value.keys(), key=str):
        entry = value[key]
        if isinstance(entry, Mapping):
            frozen[str(key)] = MappingProxyType(dict(entry))
        else:
            frozen[str(key)] = entry
    return MappingProxyType(frozen)


def block_provenance(
    *,
    available: bool,
    source_service: str,
    source_entity: str,
    collected_at: str | None,
    unavailable_reason: str = "",
) -> dict[str, Any]:
    """Build one provenance block for a collected upstream input."""
    if available:
        return {
            "availability": AVAILABILITY_AVAILABLE,
            "collected_at": collected_at or "",
            "source_entity": source_entity,
            "source_service": source_service,
            "unavailable_reason": "",
        }
    return {
        "availability": AVAILABILITY_UNAVAILABLE,
        "collected_at": collected_at or "",
        "source_entity": source_entity,
        "source_service": source_service,
        "unavailable_reason": unavailable_reason
        or REASON_RUNTIME_A_UNAVAILABLE,
    }
