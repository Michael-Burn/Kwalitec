"""Evidence ingress DTOs — AP-001 boundary into StudentReasoningService.

Consumes Assessment ``EvidenceBundleDTO`` export. Does not redefine packaging.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from application.assessment.evidence.dto import EvidenceBundleDTO


@dataclass(frozen=True, slots=True)
class EvidenceIngressRequest:
    """Lawful handoff of packaged assessment evidence into AP-001 ingress."""

    twin_id: str
    bundle: EvidenceBundleDTO
    correlation_id: str
    reasoning_request_id: str | None = None


@dataclass(frozen=True, slots=True)
class EvidenceIngressTraceability:
    """Identifiers that must survive the complete reasoning request."""

    assessment_session_id: str
    evidence_bundle_id: str
    observation_ids: tuple[str, ...]
    question_references: tuple[str, ...]
    learning_objective_references: tuple[str, ...]
    correlation_id: str
    reasoning_request_id: str
    ingress_contract_version: str
    packaging_version: str


@dataclass(frozen=True, slots=True)
class MappedEvidenceObservation:
    """Twin observation draft produced by ingress mapping (facts only)."""

    observation_id: str
    kind: str
    curriculum_entity_id: str
    curriculum_entity_kind: str
    evidence_reference: str
    provenance: str
    metadata: dict[str, Any] = field(default_factory=dict)
    correct: bool | None = None
    source_observation_id: str = ""
    question_id: str | None = None


@dataclass(frozen=True, slots=True)
class EvidenceIngressMapping:
    """Validated mapping of one EvidenceBundle into Twin observation drafts."""

    twin_id: str
    correlation_id: str
    reasoning_request_id: str
    triggered_by: str
    traceability: EvidenceIngressTraceability
    observations: tuple[MappedEvidenceObservation, ...]


@dataclass(frozen=True, slots=True)
class EvidenceIngressResult:
    """Outcome of a successful evidence ingress + existing reasoning cycle."""

    twin_id: str
    twin_observation_ids: tuple[str, ...]
    triggered_by: str
    traceability: EvidenceIngressTraceability
    mapping: EvidenceIngressMapping
