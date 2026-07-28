"""InterpretationContext — full traceability for one interpretation run."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.reasoning.interpretation.version import INTERPRETATION_VERSION


@dataclass(frozen=True, slots=True)
class InterpretationContext:
    """Traceability context for deterministic evidence interpretation."""

    reasoning_request_id: str
    evidence_bundle_id: str
    session_id: str
    packaging_version: str
    interpreter_version: str
    correlation_id: str

    def __post_init__(self) -> None:
        for field_name in (
            "reasoning_request_id",
            "evidence_bundle_id",
            "session_id",
            "packaging_version",
            "interpreter_version",
            "correlation_id",
        ):
            value = getattr(self, field_name)
            if not (value or "").strip():
                raise ValueError(f"{field_name} is required")

    @classmethod
    def create(
        cls,
        *,
        reasoning_request_id: str,
        evidence_bundle_id: str,
        session_id: str,
        packaging_version: str,
        correlation_id: str,
        interpreter_version: str = INTERPRETATION_VERSION,
    ) -> InterpretationContext:
        return cls(
            reasoning_request_id=reasoning_request_id.strip(),
            evidence_bundle_id=evidence_bundle_id.strip(),
            session_id=session_id.strip(),
            packaging_version=packaging_version.strip(),
            interpreter_version=interpreter_version.strip(),
            correlation_id=correlation_id.strip(),
        )
