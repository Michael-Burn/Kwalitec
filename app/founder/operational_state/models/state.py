"""Immutable Founder Operational State snapshot model (FOS-005).

Summary sections only — no raw documents. Every snapshot carries
``generated_at``, ``snapshot_version``, and ``source_versions`` so
future intelligence services know exactly which snapshot they analyse.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType

SNAPSHOT_VERSION = "1.0"


@dataclass(frozen=True)
class EngineeringState:
    """Engineering signals summarised from the Knowledge Engine."""

    standards_count: int
    tests_pass: bool
    validation_errors: int


@dataclass(frozen=True)
class KnowledgeState:
    """Knowledge Engine document and artefact counts."""

    engineering_standards: int
    architecture_documents: int
    research_documents: int
    capability_documents: int
    indexed_artefacts: int


@dataclass(frozen=True)
class CapabilityState:
    """Capability Archive inventory summary."""

    total_count: int
    completed_count: int
    active_count: int
    archive_inconsistencies: int
    recent_capability_ids: tuple[str, ...]


@dataclass(frozen=True)
class InternalAlphaState:
    """Internal Alpha pipeline output summary."""

    current_week: str
    feedback_count: int
    duplicate_count: int
    category_counts: Mapping[str, int]
    recent_week_labels: tuple[str, ...]


@dataclass(frozen=True)
class ReleaseState:
    """Current release label summarised from the Capability Archive."""

    current_release: str
    completed_capabilities: int


@dataclass(frozen=True)
class SourceVersions:
    """Subsystem source versions that contributed to this snapshot.

    Keys are fixed subsystem identities. Values are version labels
    reported by each provider — not interpreted or compared for
    semantic meaning beyond non-emptiness and uniqueness.
    """

    knowledge: str
    capability_archive: str
    internal_alpha: str

    def as_mapping(self) -> Mapping[str, str]:
        """Return an immutable mapping view of source versions."""
        return MappingProxyType(
            {
                "knowledge": self.knowledge,
                "capability_archive": self.capability_archive,
                "internal_alpha": self.internal_alpha,
            }
        )


@dataclass(frozen=True)
class FounderOperationalState:
    """Canonical immutable Founder operational snapshot.

    Aggregation cargo only. Downstream intelligence capabilities must
    treat this as the sole input for Founder reasoning.
    """

    generated_at: datetime
    snapshot_version: str
    source_versions: SourceVersions
    engineering: EngineeringState
    knowledge: KnowledgeState
    capability: CapabilityState
    internal_alpha: InternalAlphaState
    release: ReleaseState
