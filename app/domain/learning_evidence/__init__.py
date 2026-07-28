"""Learning Evidence Engine (EI-005) — observable educational events.

Records educational observations against a Student Curriculum Instance.
Does not infer mastery, update confidence, generate recommendations, or
create study missions. Pure domain only: no Flask, SQLAlchemy, Twin writes,
or curriculum mutation.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "EvidenceEvent",
    "EvidenceInvariant",
    "EvidenceInvariantError",
    "EvidenceSource",
    "EvidenceType",
    "assert_can_record",
    "assert_payload_schema",
    "assert_valid_timestamp",
    "count_by_type",
    "is_known_evidence_type",
    "normalise_evidence_type",
]

_EXPORT_MODULES = {
    "EvidenceType": "app.domain.learning_evidence.evidence_type",
    "EvidenceSource": "app.domain.learning_evidence.evidence_type",
    "is_known_evidence_type": "app.domain.learning_evidence.evidence_type",
    "normalise_evidence_type": "app.domain.learning_evidence.evidence_type",
    "EvidenceEvent": "app.domain.learning_evidence.evidence_event",
    "EvidenceInvariant": "app.domain.learning_evidence.invariants",
    "EvidenceInvariantError": "app.domain.learning_evidence.invariants",
    "assert_can_record": "app.domain.learning_evidence.invariants",
    "assert_valid_timestamp": "app.domain.learning_evidence.invariants",
    "assert_payload_schema": "app.domain.learning_evidence.payload_schema",
    "count_by_type": "app.domain.learning_evidence.summary",
}


def __getattr__(name: str) -> Any:
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from importlib import import_module

    module = import_module(module_name)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
