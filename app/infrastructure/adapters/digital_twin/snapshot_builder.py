"""Twin Snapshot Builder (MS-004 T2).

Assembles immutable Twin facets into coherent versioned TwinSnapshots.
Performs snapshot assembly, versioning, provenance aggregation, and
structural completeness evaluation only — no persistence, Adaptive
integration, Experience cutover, or educational writes.
"""

from __future__ import annotations

from app.infrastructure.adapters.digital_twin.assembler import (
    TwinFacetAssembler,
    TwinFacetBundle,
)
from app.infrastructure.adapters.digital_twin.completeness import (
    CompletenessEvaluator,
)
from app.infrastructure.adapters.digital_twin.contracts import (
    AUTHORITY_DIGITAL_TWIN,
    TWIN_FACET_NAMES,
    SnapshotVersion,
    TwinProfile,
    TwinSnapshot,
)
from app.infrastructure.adapters.digital_twin.provenance import (
    FACET_SYNTHESIS_ORDER,
    SOURCE_SERVICE_TWIN_SNAPSHOT,
    aggregate_snapshot_provenance,
    freeze_provenance_map,
    snapshot_root_provenance,
)
from app.infrastructure.adapters.digital_twin.validation import (
    TwinFacetValidationError,
    validate_as_of,
    validate_facet_provenance_map,
    validate_student_id,
)

# Snapshot construction / schema versions (immutable constants).
SNAPSHOT_CONSTRUCTION_VERSION = "t2.0"
SNAPSHOT_SCHEMA_VERSION = "twin_snapshot.v2"


class TwinSnapshotValidationError(TwinFacetValidationError):
    """Raised when Twin snapshot assembly inputs or outputs violate contracts."""


class TwinSnapshotBuilder:
    """Assemble a versioned TwinSnapshot from synthesised Twin facets.

    Atomicity: one ``build`` / ``build_from_bundle`` call yields a single
    immutable TwinSnapshot containing all seven facets and complete metadata.
    No intermediate mutable snapshot state is published.

    Determinism: identical TwinFacetBundle material inputs + identical
    ``generated_at`` → identical TwinSnapshot.serialize().

    Rules:
    - MAY assemble facets, aggregate provenance, evaluate structural
      completeness, and stamp version metadata
    - MUST NOT persist snapshots, call Adaptive decision paths, write
      Runtime A, cut over Experience TwinPort, or estimate missing values
    """

    BUILDER_ID = "twin_snapshot_builder"
    BUILDER_VERSION = "1.0.0-t2"

    def __init__(
        self,
        *,
        facet_assembler: TwinFacetAssembler | None = None,
        completeness_evaluator: CompletenessEvaluator | None = None,
        enabled: bool = True,
        snapshot_version: str = SNAPSHOT_CONSTRUCTION_VERSION,
        schema_version: str = SNAPSHOT_SCHEMA_VERSION,
    ) -> None:
        self._facet_assembler = facet_assembler
        self._completeness = completeness_evaluator or CompletenessEvaluator()
        self._enabled = bool(enabled)
        self._snapshot_version = snapshot_version
        self._schema_version = schema_version

    @property
    def builder_id(self) -> str:
        return self.BUILDER_ID

    @property
    def builder_version(self) -> str:
        return self.BUILDER_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    def build(
        self,
        student_id: str,
        *,
        as_of: str | None = None,
    ) -> TwinSnapshot:
        """Collect facets via TwinFacetAssembler and assemble a TwinSnapshot.

        Requires an injected ``facet_assembler``. Identical Runtime A evidence
        and ``as_of`` yield identical TwinSnapshots (deterministic).
        """
        if not self._enabled:
            raise TwinSnapshotValidationError(
                "TwinSnapshotBuilder is disabled (feature flag OFF)"
            )
        if self._facet_assembler is None:
            raise TwinSnapshotValidationError(
                "TwinSnapshotBuilder requires a TwinFacetAssembler"
            )
        clock = validate_as_of(as_of)
        sid = validate_student_id(student_id)
        bundle = self._facet_assembler.assemble(sid, as_of=clock)
        return self.build_from_bundle(bundle, generated_at=clock)

    def build_from_bundle(
        self,
        bundle: TwinFacetBundle,
        *,
        generated_at: str | None = None,
    ) -> TwinSnapshot:
        """Assemble an immutable TwinSnapshot from a TwinFacetBundle.

        Atomic: all seven facets, version triad, provenance summary,
        completeness, and unavailable summary are constructed together.
        """
        if not self._enabled:
            raise TwinSnapshotValidationError(
                "TwinSnapshotBuilder is disabled (feature flag OFF)"
            )
        if not isinstance(bundle, TwinFacetBundle):
            raise TwinSnapshotValidationError(
                "bundle must be a TwinFacetBundle"
            )

        clock = validate_as_of(
            generated_at if generated_at is not None else bundle.as_of
        )
        profile = bundle.profile
        if not isinstance(profile, TwinProfile):
            raise TwinSnapshotValidationError("bundle.profile must be TwinProfile")

        self._assert_seven_facets(profile)
        field_provenance = freeze_provenance_map(bundle.field_provenance)
        validate_facet_provenance_map(field_provenance)

        completeness = self._completeness.evaluate(profile, field_provenance)
        unavailable = self._completeness.unavailable_summary(
            profile,
            field_provenance,
            completeness=completeness,
        )
        provenance_summary = aggregate_snapshot_provenance(
            field_provenance,
            as_of=clock,
        )
        root_provenance = snapshot_root_provenance(
            collected_at=clock,
            completeness_status=completeness.status,
            contributing_sources=provenance_summary.contributing_runtime_a_sources,
        )

        version = SnapshotVersion(
            snapshot_version=self._snapshot_version,
            schema_version=self._schema_version,
            evidence_version=bundle.source_evidence_version,
        )
        twin_id = (
            f"twin-{profile.student_id}" if profile.student_id else ""
        )

        # Single immutable construction — no partial publish.
        return TwinSnapshot(
            profile=profile,
            profile_version=bundle.profile_version,
            source_evidence_version=version.evidence_version,
            generated_at=clock,
            provenance=root_provenance,
            completeness=completeness,
            twin_id=twin_id,
            authority=AUTHORITY_DIGITAL_TWIN,
            field_provenance=field_provenance,
            snapshot_version=version.snapshot_version,
            schema_version=version.schema_version,
            provenance_summary=provenance_summary,
            unavailable_summary=unavailable,
        )

    def build_version(
        self,
        *,
        evidence_version: str,
    ) -> SnapshotVersion:
        """Construct the snapshot version triad for a given evidence version."""
        return SnapshotVersion(
            snapshot_version=self._snapshot_version,
            schema_version=self._schema_version,
            evidence_version=evidence_version,
        )

    @staticmethod
    def _assert_seven_facets(profile: TwinProfile) -> None:
        """Ensure the profile exposes all seven Twin facets structurally."""
        missing = [
            name
            for name in FACET_SYNTHESIS_ORDER
            if getattr(profile, name, None) is None
        ]
        if missing:
            raise TwinSnapshotValidationError(
                f"TwinSnapshot missing facets: {missing}"
            )
        # Catalogue guard — profile attributes cover the directive set.
        if frozenset(FACET_SYNTHESIS_ORDER) != TWIN_FACET_NAMES:
            raise TwinSnapshotValidationError(
                "facet catalogue mismatch between synthesis order and contract"
            )


def build_twin_snapshot_builder(
    *,
    enabled: bool,
    facet_assembler: TwinFacetAssembler | None = None,
    completeness_evaluator: CompletenessEvaluator | None = None,
) -> TwinSnapshotBuilder | None:
    """DI helper — construct TwinSnapshotBuilder only when the flag is on."""
    if not enabled:
        return None
    return TwinSnapshotBuilder(
        facet_assembler=facet_assembler,
        completeness_evaluator=completeness_evaluator,
        enabled=True,
    )


__all__ = [
    "SNAPSHOT_CONSTRUCTION_VERSION",
    "SNAPSHOT_SCHEMA_VERSION",
    "SOURCE_SERVICE_TWIN_SNAPSHOT",
    "TwinSnapshotBuilder",
    "TwinSnapshotValidationError",
    "build_twin_snapshot_builder",
]
