"""Runtime A Evidence Advisory injection point (P2-MS009).

Runtime A may read advisory inputs through ``EvidenceAdvisoryPort``.
Runtime A may ignore advisory inputs.
Runtime A must document any advisory data it consumes.
Runtime A remains solely responsible for recommendations.

This milestone creates the integration point only — recommendation generation
behaviour is unchanged when advisory inputs are present or absent.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Protocol, runtime_checkable

from app.infrastructure.adapters.evidence_platform.contracts import (
    EvidenceAdvisory,
    EvidenceResult,
)

logger = logging.getLogger(__name__)

REASON_FLAG_OFF = "evidence_advisory_flag_off"
REASON_PORT_UNAVAILABLE = "evidence_advisory_port_unavailable"
REASON_READ_REJECTED = "evidence_advisory_read_rejected"
REASON_EMPTY = "evidence_advisory_empty"
REASON_INTEGRATION_ONLY = "integration_point_only_no_behaviour_change"

AUTHORITY_RUNTIME_A = "runtime_a"


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    raw = dict(value or {})
    frozen: dict[str, Any] = {}
    for key, item in raw.items():
        if isinstance(item, Mapping):
            frozen[str(key)] = dict(item)
        elif isinstance(item, list | tuple):
            frozen[str(key)] = list(item)
        else:
            frozen[str(key)] = item
    return MappingProxyType(frozen)


@runtime_checkable
class EvidenceAdvisoryReadPort(Protocol):
    """Evidence public advisory surface used by Runtime A.

    Callers must use this contract only — no repository / collector bypass.
    """

    @property
    def port_id(self) -> str:
        """Stable EvidenceAdvisoryPort identity."""

    def is_available(self) -> bool:
        """Whether the advisory port is enabled and wired."""

    def query_advisory(
        self,
        student_id: str,
        *,
        reporting_period: str = "this_week",
        as_of: str | None = None,
        evidence_records: Any = None,
    ) -> EvidenceResult:
        """Return an EvidenceResult carrying EvidenceAdvisory."""


@dataclass(frozen=True)
class AdvisoryConsiderationRecord:
    """Explainability record of advisory inputs Runtime A considered.

    Documents read / ignored status without influencing recommendations.
    """

    considered: bool
    ignored_for_decisions: bool
    advisory_id: str = ""
    student_id: str = ""
    fields_considered: tuple[str, ...] = ()
    provenance_refs: Mapping[str, Any] = field(default_factory=dict)
    source_description: str = ""
    reason: str = REASON_INTEGRATION_ONLY
    authority: str = AUTHORITY_RUNTIME_A

    def __post_init__(self) -> None:
        object.__setattr__(self, "advisory_id", (self.advisory_id or "").strip())
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(
            self,
            "fields_considered",
            tuple(str(item) for item in (self.fields_considered or ())),
        )
        object.__setattr__(
            self, "provenance_refs", _freeze_mapping(self.provenance_refs)
        )
        object.__setattr__(
            self, "source_description", (self.source_description or "").strip()
        )
        object.__setattr__(self, "reason", (self.reason or "").strip())
        object.__setattr__(
            self, "authority", (self.authority or AUTHORITY_RUNTIME_A).strip()
        )

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "advisory_id": self.advisory_id,
            "authority": self.authority,
            "considered": self.considered,
            "fields_considered": list(self.fields_considered),
            "ignored_for_decisions": self.ignored_for_decisions,
            "provenance_refs": dict(self.provenance_refs),
            "reason": self.reason,
            "source_description": self.source_description,
            "student_id": self.student_id,
        }


class RuntimeAEvidenceAdvisoryInjection:
    """Optional Evidence advisory intake for Runtime A.

    Rules:
    - MAY read EvidenceAdvisory via EvidenceAdvisoryPort
    - MAY ignore advisory inputs
    - MUST document any advisory data consumed (consideration record)
    - MUST NOT change recommendation / educational decision behaviour
    - MUST NOT access repositories or Evidence internals
    """

    INJECTION_ID = "runtime_a_evidence_advisory_injection"
    INJECTION_VERSION = "1.0.0-p2.ms009"

    ADVISORY_FIELDS: tuple[str, ...] = (
        "advisory_id",
        "reporting_period",
        "observed_patterns",
        "engagement_summary",
        "consistency_summary",
        "factual_constraints",
        "provenance",
        "generated_at",
        "source_description",
    )

    def __init__(
        self,
        *,
        enabled: bool = True,
        port: EvidenceAdvisoryReadPort | None = None,
    ) -> None:
        self._enabled = bool(enabled)
        self._port = port
        self._last_consideration: AdvisoryConsiderationRecord | None = None
        self._last_advisory: EvidenceAdvisory | None = None

    @property
    def injection_id(self) -> str:
        return self.INJECTION_ID

    @property
    def injection_version(self) -> str:
        return self.INJECTION_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    @property
    def port(self) -> EvidenceAdvisoryReadPort | None:
        return self._port

    @property
    def last_consideration(self) -> AdvisoryConsiderationRecord | None:
        """Most recent explainability record produced by this injection."""
        return self._last_consideration

    @property
    def last_advisory(self) -> EvidenceAdvisory | None:
        """Most recent advisory retrieved (may be ignored for decisions)."""
        return self._last_advisory

    def read_advisory(
        self,
        student_id: str,
        *,
        reporting_period: str = "this_week",
        as_of: str | None = None,
        evidence_records: Sequence[Any] | None = None,
    ) -> EvidenceAdvisory | None:
        """Return EvidenceAdvisory or None when gated / unavailable.

        Callers may ignore the result. Recommendation logic must not depend
        on presence or absence of advisory data in this milestone.
        """
        self._last_advisory = None
        if not self._enabled:
            return None
        sid = (student_id or "").strip()
        if not sid:
            return None
        if self._port is None or not self._port.is_available():
            logger.debug(
                "evidence_advisory_skip reason=%s student_id=%s",
                REASON_PORT_UNAVAILABLE,
                sid,
            )
            return None
        try:
            result = self._port.query_advisory(
                sid,
                reporting_period=reporting_period,
                as_of=as_of,
                evidence_records=evidence_records,
            )
        except Exception:
            logger.warning(
                "evidence_advisory_failed reason=%s student_id=%s",
                REASON_READ_REJECTED,
                sid,
                exc_info=True,
            )
            return None
        if not isinstance(result, EvidenceResult) or not result.ok:
            message = getattr(result, "message", None) if result is not None else None
            logger.debug(
                "evidence_advisory_skip reason=%s student_id=%s message=%s",
                REASON_READ_REJECTED,
                sid,
                message,
            )
            return None
        advisory = result.value
        if not isinstance(advisory, EvidenceAdvisory):
            logger.debug(
                "evidence_advisory_skip reason=%s student_id=%s",
                REASON_EMPTY,
                sid,
            )
            return None
        self._last_advisory = advisory
        return advisory

    def document_consideration(
        self,
        advisory: EvidenceAdvisory | None,
        *,
        student_id: str = "",
        reason: str = REASON_INTEGRATION_ONLY,
    ) -> AdvisoryConsiderationRecord:
        """Document which advisory inputs were considered (explainability)."""
        sid = (student_id or "").strip()
        if advisory is None:
            record = AdvisoryConsiderationRecord(
                considered=False,
                ignored_for_decisions=True,
                student_id=sid,
                fields_considered=(),
                provenance_refs={},
                source_description="",
                reason=reason or REASON_EMPTY,
            )
            self._last_consideration = record
            return record
        sid = sid or advisory.student_id
        record = AdvisoryConsiderationRecord(
            considered=True,
            ignored_for_decisions=True,
            advisory_id=advisory.advisory_id,
            student_id=sid,
            fields_considered=self.ADVISORY_FIELDS,
            provenance_refs={
                "advisory_id": advisory.advisory_id,
                "evidence_summary_id": advisory.evidence_summary_id,
                "evidence_refs": list(advisory.evidence_refs),
                "evidence_provenance": dict(advisory.provenance),
                "authority": advisory.authority,
            },
            source_description=advisory.source_description,
            reason=reason or REASON_INTEGRATION_ONLY,
        )
        self._last_consideration = record
        return record

    def prepare_for_recommendation(
        self,
        user_id: int | str,
        *,
        reporting_period: str = "this_week",
        as_of: str | None = None,
        evidence_records: Sequence[Any] | None = None,
    ) -> AdvisoryConsiderationRecord:
        """Injection point invoked around Runtime A recommendation generation.

        Reads advisory when enabled, documents consideration, and returns the
        explainability record. Does **not** alter recommendation inputs or
        outputs — Runtime A remains sole educational authority.
        """
        if not self._enabled:
            return self.document_consideration(
                None, student_id=str(user_id), reason=REASON_FLAG_OFF
            )
        student_id = str(user_id).strip()
        advisory = self.read_advisory(
            student_id,
            reporting_period=reporting_period,
            as_of=as_of,
            evidence_records=evidence_records,
        )
        record = self.document_consideration(
            advisory,
            student_id=student_id,
            reason=REASON_INTEGRATION_ONLY,
        )
        logger.debug(
            "evidence_advisory_considered student_id=%s advisory_id=%s "
            "ignored_for_decisions=%s reason=%s",
            record.student_id,
            record.advisory_id or "-",
            record.ignored_for_decisions,
            record.reason,
        )
        return record


def build_runtime_a_evidence_advisory_injection(
    *,
    enabled: bool,
    port: EvidenceAdvisoryReadPort | None = None,
) -> RuntimeAEvidenceAdvisoryInjection | None:
    """DI helper — construct injection only when ENABLE_EVIDENCE_ADVISORY is ON."""
    if not enabled:
        return None
    return RuntimeAEvidenceAdvisoryInjection(enabled=True, port=port)


__all__ = [
    "AUTHORITY_RUNTIME_A",
    "AdvisoryConsiderationRecord",
    "EvidenceAdvisoryReadPort",
    "REASON_EMPTY",
    "REASON_FLAG_OFF",
    "REASON_INTEGRATION_ONLY",
    "REASON_PORT_UNAVAILABLE",
    "REASON_READ_REJECTED",
    "RuntimeAEvidenceAdvisoryInjection",
    "build_runtime_a_evidence_advisory_injection",
]
