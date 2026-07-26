"""Runtime A Recovery Planner injection point (P2-MS010).

Runtime A may read recovery candidates through ``RecoveryPlannerPort``.
Runtime A may ignore recovery candidates.
Runtime A must document any recovery data it consumes.
Runtime A remains solely responsible for recommendations.

This milestone creates the integration point only — recommendation generation
behaviour is unchanged when recovery candidates are present or absent.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Protocol, runtime_checkable

from app.infrastructure.adapters.recovery_planner.contracts import (
    RecoveryContext,
    RecoveryPlanCandidate,
    RecoveryResult,
)

logger = logging.getLogger(__name__)

REASON_FLAG_OFF = "recovery_planner_flag_off"
REASON_PORT_UNAVAILABLE = "recovery_planner_port_unavailable"
REASON_READ_REJECTED = "recovery_planner_read_rejected"
REASON_EMPTY = "recovery_planner_empty"
REASON_CONTEXT_NOT_SUPPLIED = "recovery_context_not_supplied"
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
class RecoveryPlannerReadPort(Protocol):
    """Recovery public planning surface used by Runtime A.

    Callers must use this contract only — no adapter-internal bypass.
    """

    @property
    def port_id(self) -> str:
        """Stable RecoveryPlannerPort identity."""

    def is_available(self) -> bool:
        """Whether the recovery planner port is enabled and wired."""

    def plan_recovery(self, context: RecoveryContext) -> RecoveryResult:
        """Return a RecoveryResult carrying RecoveryPlanCandidate."""


@dataclass(frozen=True)
class RecoveryConsiderationRecord:
    """Explainability record of recovery candidates Runtime A considered.

    Documents read / ignored status without influencing recommendations.
    """

    considered: bool
    ignored_for_decisions: bool
    candidate_id: str = ""
    recovery_id: str = ""
    student_id: str = ""
    fields_considered: tuple[str, ...] = ()
    provenance_refs: Mapping[str, Any] = field(default_factory=dict)
    rationale: str = ""
    reason: str = REASON_INTEGRATION_ONLY
    authority: str = AUTHORITY_RUNTIME_A
    advisory_only: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "candidate_id", (self.candidate_id or "").strip())
        object.__setattr__(self, "recovery_id", (self.recovery_id or "").strip())
        object.__setattr__(self, "student_id", (self.student_id or "").strip())
        object.__setattr__(
            self,
            "fields_considered",
            tuple(str(item) for item in (self.fields_considered or ())),
        )
        object.__setattr__(
            self, "provenance_refs", _freeze_mapping(self.provenance_refs)
        )
        object.__setattr__(self, "rationale", (self.rationale or "").strip())
        object.__setattr__(self, "reason", (self.reason or "").strip())
        object.__setattr__(
            self, "authority", (self.authority or AUTHORITY_RUNTIME_A).strip()
        )
        object.__setattr__(self, "advisory_only", True)

    def to_canonical_dict(self) -> dict[str, Any]:
        return {
            "advisory_only": self.advisory_only,
            "authority": self.authority,
            "candidate_id": self.candidate_id,
            "considered": self.considered,
            "fields_considered": list(self.fields_considered),
            "ignored_for_decisions": self.ignored_for_decisions,
            "provenance_refs": dict(self.provenance_refs),
            "rationale": self.rationale,
            "reason": self.reason,
            "recovery_id": self.recovery_id,
            "student_id": self.student_id,
        }


class RuntimeARecoveryInjection:
    """Optional Recovery Planner intake for Runtime A.

    Rules:
    - MAY read RecoveryPlanCandidate via RecoveryPlannerPort
    - MAY ignore recovery candidates
    - MUST document any recovery data consumed (consideration record)
    - MUST NOT change recommendation / educational decision behaviour
    - MUST NOT access repositories or Recovery Planner internals
    """

    INJECTION_ID = "runtime_a_recovery_injection"
    INJECTION_VERSION = "1.0.0-p2.ms010"

    CANDIDATE_FIELDS: tuple[str, ...] = (
        "candidate_id",
        "strategy_type",
        "affected_period",
        "rationale",
        "provenance",
        "advisory_only",
        "recovery_id",
        "generated_at",
    )

    def __init__(
        self,
        *,
        enabled: bool = True,
        port: RecoveryPlannerReadPort | None = None,
    ) -> None:
        self._enabled = bool(enabled)
        self._port = port
        self._last_consideration: RecoveryConsiderationRecord | None = None
        self._last_candidate: RecoveryPlanCandidate | None = None

    @property
    def injection_id(self) -> str:
        return self.INJECTION_ID

    @property
    def injection_version(self) -> str:
        return self.INJECTION_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    @property
    def port(self) -> RecoveryPlannerReadPort | None:
        return self._port

    @property
    def last_consideration(self) -> RecoveryConsiderationRecord | None:
        """Most recent explainability record produced by this injection."""
        return self._last_consideration

    @property
    def last_candidate(self) -> RecoveryPlanCandidate | None:
        """Most recent candidate retrieved (may be ignored for decisions)."""
        return self._last_candidate

    def plan_recovery(
        self,
        context: RecoveryContext | None,
    ) -> RecoveryPlanCandidate | None:
        """Return RecoveryPlanCandidate or None when gated / unavailable.

        Callers may ignore the result. Recommendation logic must not depend
        on presence or absence of recovery candidates in this milestone.
        """
        self._last_candidate = None
        if not self._enabled:
            return None
        if context is None:
            return None
        if not isinstance(context, RecoveryContext):
            logger.debug(
                "recovery_injection_skip reason=%s",
                REASON_READ_REJECTED,
            )
            return None
        if self._port is None or not self._port.is_available():
            logger.debug(
                "recovery_injection_skip reason=%s student_id=%s",
                REASON_PORT_UNAVAILABLE,
                context.student_id,
            )
            return None
        try:
            result = self._port.plan_recovery(context)
        except Exception:
            logger.warning(
                "recovery_injection_failed reason=%s student_id=%s",
                REASON_READ_REJECTED,
                context.student_id,
                exc_info=True,
            )
            return None
        if not isinstance(result, RecoveryResult) or not result.ok:
            message = getattr(result, "message", None) if result is not None else None
            logger.debug(
                "recovery_injection_skip reason=%s student_id=%s message=%s",
                REASON_READ_REJECTED,
                context.student_id,
                message,
            )
            return None
        candidate = result.value
        if not isinstance(candidate, RecoveryPlanCandidate):
            logger.debug(
                "recovery_injection_skip reason=%s student_id=%s",
                REASON_EMPTY,
                context.student_id,
            )
            return None
        self._last_candidate = candidate
        return candidate

    def document_consideration(
        self,
        candidate: RecoveryPlanCandidate | None,
        *,
        student_id: str = "",
        reason: str = REASON_INTEGRATION_ONLY,
    ) -> RecoveryConsiderationRecord:
        """Document which recovery candidates were considered (explainability)."""
        sid = (student_id or "").strip()
        if candidate is None:
            record = RecoveryConsiderationRecord(
                considered=False,
                ignored_for_decisions=True,
                student_id=sid,
                fields_considered=(),
                provenance_refs={},
                rationale="",
                reason=reason or REASON_EMPTY,
                advisory_only=True,
            )
            self._last_consideration = record
            return record
        sid = sid or candidate.student_id
        record = RecoveryConsiderationRecord(
            considered=True,
            ignored_for_decisions=True,
            candidate_id=candidate.candidate_id,
            recovery_id=candidate.recovery_id,
            student_id=sid,
            fields_considered=self.CANDIDATE_FIELDS,
            provenance_refs={
                "candidate_id": candidate.candidate_id,
                "recovery_id": candidate.recovery_id,
                "strategy_type": candidate.strategy_type,
                "advisory_only": candidate.advisory_only,
                "recovery_provenance": dict(candidate.provenance),
                "authority": candidate.authority,
            },
            rationale=candidate.rationale,
            reason=reason or REASON_INTEGRATION_ONLY,
            advisory_only=True,
        )
        self._last_consideration = record
        return record

    def prepare_for_recommendation(
        self,
        user_id: int | str,
        *,
        context: RecoveryContext | None = None,
    ) -> RecoveryConsiderationRecord:
        """Injection point invoked around Runtime A recommendation generation.

        Reads a recovery candidate when enabled and a context is supplied,
        documents consideration, and returns the explainability record. Does
        **not** alter recommendation inputs or outputs — Runtime A remains
        sole educational authority.
        """
        if not self._enabled:
            return self.document_consideration(
                None, student_id=str(user_id), reason=REASON_FLAG_OFF
            )
        student_id = str(user_id).strip()
        if context is None:
            return self.document_consideration(
                None,
                student_id=student_id,
                reason=REASON_CONTEXT_NOT_SUPPLIED,
            )
        candidate = self.plan_recovery(context)
        record = self.document_consideration(
            candidate,
            student_id=student_id,
            reason=REASON_INTEGRATION_ONLY,
        )
        logger.debug(
            "recovery_candidate_considered student_id=%s candidate_id=%s "
            "ignored_for_decisions=%s advisory_only=%s reason=%s",
            record.student_id,
            record.candidate_id or "-",
            record.ignored_for_decisions,
            record.advisory_only,
            record.reason,
        )
        return record


def build_runtime_a_recovery_injection(
    *,
    enabled: bool,
    port: RecoveryPlannerReadPort | None = None,
) -> RuntimeARecoveryInjection | None:
    """DI helper — construct injection only when ENABLE_RECOVERY_PLANNER is ON."""
    if not enabled:
        return None
    return RuntimeARecoveryInjection(enabled=True, port=port)


__all__ = [
    "AUTHORITY_RUNTIME_A",
    "REASON_CONTEXT_NOT_SUPPLIED",
    "REASON_EMPTY",
    "REASON_FLAG_OFF",
    "REASON_INTEGRATION_ONLY",
    "REASON_PORT_UNAVAILABLE",
    "REASON_READ_REJECTED",
    "RecoveryConsiderationRecord",
    "RecoveryPlannerReadPort",
    "RuntimeARecoveryInjection",
    "build_runtime_a_recovery_injection",
]
