"""Educational Evidence Package — Application Layer Twin Update input.

Faithful Version 1.0 transport of the frozen Educational Evidence Contract
(Capability 4.8.4) for Twin Update Coordinator / Strategy consumption
(Capability 4.9.7a alignment).

This module transports observational cargo only. It does not create Evidence
from Presentation contracts, densify Twin belief, or invent educational
meaning. Closed observed-event tokens match Capability 4.8.4 exactly.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any

EVIDENCE_PACKAGE_VERSION_1_0 = "1.0"
CONTRACT_VERSION_1_0 = EVIDENCE_PACKAGE_VERSION_1_0


class ObservedEvent(StrEnum):
    """Closed Version 1.0 observational vocabulary (Capability 4.8.4).

    Tokens are observations — never mastery, readiness, or confidence.
    """

    MISSION_COMPLETED = "mission_completed"
    MISSION_ABANDONED = "mission_abandoned"
    STUDY_DURATION = "study_duration"
    TOPIC_STUDIED = "topic_studied"
    PRACTICE_COMPLETED = "practice_completed"
    PRACTICE_ATTEMPTED = "practice_attempted"
    SESSION_ENDED_MANUAL = "session_ended_manual"
    SESSION_ENDED_TIMEOUT = "session_ended_timeout"
    SYSTEM_TIMESTAMP = "system_timestamp"


@dataclass(frozen=True)
class EducationalEvidencePackage:
    """Immutable observational package for Twin Update strategy invocation.

    Application-layer representation of Educational Evidence Contract Version
    1.0. Attributes carry identities, provenance, observed events, and
    optional observational enrichment — never educational conclusions.
    """

    evidence_id: str
    student_id: str
    study_plan_id: str
    curriculum_id: str
    evidence_timestamp: datetime
    provenance: str
    contract_version: str
    observed_events: tuple[ObservedEvent, ...]
    topic_id: str | None = None
    mission_id: str | None = None
    sitting_id: str | None = None
    assessment_result: Mapping[str, object] | None = None
    practice_count: int | None = None
    declared_duration: float | None = None
    reflection: str | None = None
    session_notes: str | None = None

    @property
    def package_version(self) -> str:
        """Backward-compatible alias for ``contract_version``."""
        return self.contract_version

    @classmethod
    def create(
        cls,
        evidence_id: str,
        student_id: str,
        evidence_timestamp: datetime,
        provenance: str,
        *,
        study_plan_id: str,
        curriculum_id: str,
        observed_events: Iterable[ObservedEvent | str],
        contract_version: str | None = None,
        package_version: str | None = None,
        topic_id: str | None = None,
        mission_id: str | None = None,
        sitting_id: str | None = None,
        assessment_result: Mapping[str, object] | None = None,
        practice_count: int | None = None,
        declared_duration: float | None = None,
        reflection: str | None = None,
        session_notes: str | None = None,
    ) -> EducationalEvidencePackage:
        """Construct a structurally normalised Evidence Package.

        Validates Required identities, timestamp type, non-empty closed
        ``observed_events``, and contract version presence. Does not score
        educational correctness.

        Raises:
            ValueError: If required structural anchors are blank or illegal.
        """
        eid = _require_nonblank(evidence_id, "evidence_id")
        sid = _require_nonblank(student_id, "student_id")
        plan_id = _require_nonblank(study_plan_id, "study_plan_id")
        curr_id = _require_nonblank(curriculum_id, "curriculum_id")

        if not isinstance(evidence_timestamp, datetime):
            raise ValueError("evidence_timestamp must be a datetime")

        prov = _require_nonblank(provenance, "provenance")
        version = _resolve_contract_version(contract_version, package_version)
        events = _normalize_observed_events(observed_events)
        assessment = _freeze_assessment_result(assessment_result)
        count = _optional_non_negative_int(practice_count, "practice_count")
        duration = _optional_non_negative_float(
            declared_duration, "declared_duration"
        )
        reflection_text = _optional_text(reflection)
        notes = _optional_text(session_notes)

        return cls(
            evidence_id=eid,
            student_id=sid,
            study_plan_id=plan_id,
            curriculum_id=curr_id,
            evidence_timestamp=evidence_timestamp,
            provenance=prov,
            contract_version=version,
            observed_events=events,
            topic_id=_optional_nonblank(topic_id),
            mission_id=_optional_nonblank(mission_id),
            sitting_id=_optional_nonblank(sitting_id),
            assessment_result=assessment,
            practice_count=count,
            declared_duration=duration,
            reflection=reflection_text,
            session_notes=notes,
        )


def _resolve_contract_version(
    contract_version: str | None,
    package_version: str | None,
) -> str:
    if contract_version is not None and package_version is not None:
        left = _require_nonblank(contract_version, "contract_version")
        right = _require_nonblank(package_version, "package_version")
        if left != right:
            raise ValueError(
                "contract_version and package_version must match when both "
                f"are supplied: {left!r} != {right!r}"
            )
        return left
    if contract_version is not None:
        return _require_nonblank(contract_version, "contract_version")
    if package_version is not None:
        return _require_nonblank(package_version, "package_version")
    return CONTRACT_VERSION_1_0


def _normalize_observed_events(
    values: Iterable[ObservedEvent | str],
) -> tuple[ObservedEvent, ...]:
    if values is None:
        raise ValueError("observed_events must be a non-empty collection")
    try:
        iterator = iter(values)
    except TypeError as exc:
        raise ValueError(
            "observed_events must be an iterable of ObservedEvent or str"
        ) from exc

    normalized: list[ObservedEvent] = []
    seen: set[ObservedEvent] = set()
    for raw in iterator:
        event = _as_observed_event(raw)
        if event not in seen:
            seen.add(event)
            normalized.append(event)

    if not normalized:
        raise ValueError("observed_events must be non-empty")

    if (
        ObservedEvent.MISSION_COMPLETED in seen
        and ObservedEvent.MISSION_ABANDONED in seen
    ):
        raise ValueError(
            "observed_events must not contain both mission_completed and "
            "mission_abandoned"
        )

    return tuple(normalized)


def _as_observed_event(value: ObservedEvent | str) -> ObservedEvent:
    if isinstance(value, ObservedEvent):
        return value
    if isinstance(value, str):
        token = value.strip()
        try:
            return ObservedEvent(token)
        except ValueError as exc:
            raise ValueError(
                f"observed_events contains unrecognised token: {value!r}"
            ) from exc
    raise ValueError(
        "observed_events entries must be ObservedEvent or str, "
        f"got {type(value)!r}"
    )


def _freeze_assessment_result(
    value: Mapping[str, object] | None,
) -> Mapping[str, object] | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise ValueError(
            "assessment_result must be a mapping or None, "
            f"got {type(value)!r}"
        )
    frozen: dict[str, object] = {}
    for key, item in value.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError("assessment_result keys must be non-blank strings")
        frozen[key.strip()] = item
    return MappingProxyType(frozen)


def _require_nonblank(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _optional_nonblank(value: str | None) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    return cleaned or None


def _optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"optional text must be str or None, got {type(value)!r}")
    cleaned = value.strip()
    return cleaned or None


def _optional_non_negative_int(value: int | None, field_name: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int or None, got {type(value)!r}")
    if value < 0:
        raise ValueError(f"{field_name} must be non-negative, got {value}")
    return value


def _optional_non_negative_float(
    value: float | None,
    field_name: str,
) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(
            f"{field_name} must be a number or None, got {type(value)!r}"
        )
    amount = float(value)
    if amount < 0.0:
        raise ValueError(f"{field_name} must be non-negative, got {amount}")
    return amount
