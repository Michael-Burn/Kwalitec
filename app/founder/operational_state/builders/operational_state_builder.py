"""OperationalStateBuilder — assemble FounderOperationalState (FOS-005).

Collects subsystem DTOs, maps them into summary sections, and validates
completeness. No calculations beyond simple aggregation.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from types import MappingProxyType

from app.founder.operational_state.dto.capability import CapabilitySubsystemDTO
from app.founder.operational_state.dto.internal_alpha import (
    InternalAlphaSubsystemDTO,
)
from app.founder.operational_state.dto.knowledge import KnowledgeSubsystemDTO
from app.founder.operational_state.dto.validation import (
    OperationalStateValidationError,
)
from app.founder.operational_state.models.state import (
    SNAPSHOT_VERSION,
    CapabilityState,
    EngineeringState,
    FounderOperationalState,
    InternalAlphaState,
    KnowledgeState,
    ReleaseState,
    SourceVersions,
)
from app.founder.operational_state.validators.state_validator import (
    OperationalStateValidator,
)


class OperationalStateBuilder:
    """Assemble an immutable FounderOperationalState from subsystem DTOs."""

    def __init__(
        self,
        *,
        validator: OperationalStateValidator | None = None,
        clock: Callable[[], datetime] | None = None,
        snapshot_version: str = SNAPSHOT_VERSION,
        default_release: str = "1.0.0",
    ) -> None:
        self._validator = validator or OperationalStateValidator()
        self._clock = clock or (lambda: datetime.now(UTC))
        self._snapshot_version = snapshot_version
        self._default_release = default_release

    def build(
        self,
        knowledge: KnowledgeSubsystemDTO,
        capability: CapabilitySubsystemDTO,
        internal_alpha: InternalAlphaSubsystemDTO,
        *,
        generated_at: datetime | None = None,
        validate: bool = True,
    ) -> FounderOperationalState:
        """Assemble and optionally validate an operational snapshot.

        Args:
            knowledge: Knowledge Engine summary DTO.
            capability: Capability Archive summary DTO.
            internal_alpha: Internal Alpha summary DTO.
            generated_at: Optional fixed timestamp (tests / replay).
            validate: When True, run completeness validation and raise
                OperationalStateValidationError on failure.

        Returns:
            Immutable FounderOperationalState.

        Raises:
            OperationalStateValidationError: When validate=True and the
                assembled snapshot fails validation.
        """
        category_counts = MappingProxyType(dict(internal_alpha.category_counts))
        release_label = capability.current_release or self._default_release

        state = FounderOperationalState(
            generated_at=generated_at or self._clock(),
            snapshot_version=self._snapshot_version,
            source_versions=SourceVersions(
                knowledge=knowledge.source_version,
                capability_archive=capability.source_version,
                internal_alpha=internal_alpha.source_version,
            ),
            engineering=EngineeringState(
                standards_count=knowledge.engineering_standards,
                tests_pass=knowledge.tests_pass,
                validation_errors=knowledge.validation_errors,
            ),
            knowledge=KnowledgeState(
                engineering_standards=knowledge.engineering_standards,
                architecture_documents=knowledge.architecture_documents,
                research_documents=knowledge.research_documents,
                capability_documents=knowledge.capability_documents,
                indexed_artefacts=knowledge.indexed_artefacts,
            ),
            capability=CapabilityState(
                total_count=capability.total_count,
                completed_count=capability.completed_count,
                active_count=capability.active_count,
                archive_inconsistencies=capability.archive_inconsistencies,
                recent_capability_ids=capability.recent_capability_ids,
            ),
            internal_alpha=InternalAlphaState(
                current_week=internal_alpha.current_week,
                feedback_count=internal_alpha.feedback_count,
                duplicate_count=internal_alpha.duplicate_count,
                category_counts=category_counts,
                recent_week_labels=internal_alpha.recent_week_labels,
            ),
            release=ReleaseState(
                current_release=release_label,
                completed_capabilities=capability.completed_count,
            ),
        )

        if validate:
            report = self._validator.validate(state)
            if not report.ok:
                raise OperationalStateValidationError(report)

        return state
