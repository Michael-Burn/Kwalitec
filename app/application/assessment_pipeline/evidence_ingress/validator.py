"""Evidence contract validation for AP-001 ingress (fail-closed)."""

from __future__ import annotations

from collections.abc import Collection

from app.application.assessment_pipeline.evidence_ingress.errors import (
    IncompleteEvidenceBundle,
    InvalidEvidenceBundle,
    MissingObservationReference,
    UnsupportedEvidenceVersion,
)
from app.application.assessment_pipeline.evidence_ingress.versions import (
    SUPPORTED_PACKAGING_VERSIONS,
)
from application.assessment.evidence.dto import (
    EvidenceBundleDTO,
    EvidenceItemDTO,
    EvidenceMetadataDTO,
)


def _require_non_empty(value: str | None, *, field: str, error: type[Exception]) -> str:
    if value is None or not str(value).strip():
        raise error(f"missing required field: {field}")
    return str(value).strip()


def validate_evidence_bundle(
    bundle: object,
    *,
    supported_versions: Collection[str] | None = None,
) -> EvidenceBundleDTO:
    """Validate an EvidenceBundleDTO against the ingress contract.

    Raises:
        InvalidEvidenceBundle: corrupted / structurally invalid payload
        IncompleteEvidenceBundle: missing required metadata or items
        MissingObservationReference: broken observation references
        UnsupportedEvidenceVersion: unknown packaging_version
    """
    if bundle is None:
        raise InvalidEvidenceBundle("evidence bundle payload is null")
    if not isinstance(bundle, EvidenceBundleDTO):
        raise InvalidEvidenceBundle(
            f"evidence bundle must be EvidenceBundleDTO, got {type(bundle).__name__}"
        )

    _require_non_empty(
        bundle.bundle_id, field="bundle_id", error=IncompleteEvidenceBundle
    )
    _require_non_empty(
        bundle.session_id, field="session_id", error=IncompleteEvidenceBundle
    )
    _require_non_empty(
        bundle.evidence_strength,
        field="evidence_strength",
        error=IncompleteEvidenceBundle,
    )

    if bundle.context is None:
        raise IncompleteEvidenceBundle("missing evidence context")
    if not (bundle.context.session_id or "").strip():
        raise IncompleteEvidenceBundle("missing context.session_id")
    if bundle.context.session_id.strip() != bundle.session_id.strip():
        raise InvalidEvidenceBundle(
            "bundle.session_id does not match context.session_id"
        )

    metadata = bundle.metadata
    if metadata is None or not isinstance(metadata, EvidenceMetadataDTO):
        raise IncompleteEvidenceBundle("missing evidence metadata")
    _validate_metadata(metadata, supported_versions=supported_versions)

    items = bundle.items
    if items is None:
        raise IncompleteEvidenceBundle("missing evidence items")
    if not isinstance(items, tuple):
        raise InvalidEvidenceBundle("evidence items must be a tuple")
    if len(items) == 0:
        raise IncompleteEvidenceBundle("evidence bundle contains no items")

    observation_ids = bundle.observation_ids
    if observation_ids is None:
        raise IncompleteEvidenceBundle("missing observation_ids")
    if not isinstance(observation_ids, tuple):
        raise InvalidEvidenceBundle("observation_ids must be a tuple")

    _validate_items(items, observation_ids=observation_ids)

    if bundle.summary is None:
        raise IncompleteEvidenceBundle("missing evidence summary")
    if bundle.summary.observation_count != len(items):
        raise InvalidEvidenceBundle(
            "summary.observation_count does not match items length"
        )

    return bundle


def _validate_metadata(
    metadata: EvidenceMetadataDTO,
    *,
    supported_versions: Collection[str] | None,
) -> None:
    packaging_version = _require_non_empty(
        metadata.packaging_version,
        field="metadata.packaging_version",
        error=IncompleteEvidenceBundle,
    )
    _require_non_empty(
        metadata.evidence_source,
        field="metadata.evidence_source",
        error=IncompleteEvidenceBundle,
    )
    allowed = (
        frozenset(supported_versions)
        if supported_versions is not None
        else SUPPORTED_PACKAGING_VERSIONS
    )
    if packaging_version not in allowed:
        raise UnsupportedEvidenceVersion(
            f"unsupported packaging_version: {packaging_version!r}; "
            f"supported={sorted(allowed)}"
        )


def _validate_items(
    items: tuple[EvidenceItemDTO, ...],
    *,
    observation_ids: tuple[str, ...],
) -> None:
    seen_item_ids: set[str] = set()
    seen_obs_ids: set[str] = set()
    item_obs_ids: list[str] = []

    for index, item in enumerate(items):
        if item is None or not isinstance(item, EvidenceItemDTO):
            raise InvalidEvidenceBundle(f"corrupted evidence item at index {index}")
        item_id = _require_non_empty(
            item.item_id,
            field=f"items[{index}].item_id",
            error=IncompleteEvidenceBundle,
        )
        if item_id in seen_item_ids:
            raise InvalidEvidenceBundle(f"duplicate evidence item_id: {item_id!r}")
        seen_item_ids.add(item_id)

        obs_id = (item.observation_id or "").strip()
        if not obs_id:
            raise MissingObservationReference(
                f"items[{index}] missing observation_id"
            )
        if obs_id in seen_obs_ids:
            raise InvalidEvidenceBundle(
                f"duplicate observation_id in evidence items: {obs_id!r}"
            )
        seen_obs_ids.add(obs_id)
        item_obs_ids.append(obs_id)

        if not (item.kind or "").strip():
            raise IncompleteEvidenceBundle(f"items[{index}] missing kind")
        if not (item.evidence_source or "").strip():
            raise IncompleteEvidenceBundle(f"items[{index}] missing evidence_source")

    declared = tuple(oid.strip() for oid in observation_ids if (oid or "").strip())
    if len(declared) != len(observation_ids):
        raise MissingObservationReference(
            "observation_ids contains blank observation identifiers"
        )
    if len(set(declared)) != len(declared):
        raise InvalidEvidenceBundle("observation_ids contains duplicates")

    item_set = set(item_obs_ids)
    declared_set = set(declared)
    if item_set != declared_set:
        missing_from_declared = sorted(item_set - declared_set)
        missing_from_items = sorted(declared_set - item_set)
        if missing_from_declared:
            raise MissingObservationReference(
                "observation_ids missing item observation references: "
                f"{missing_from_declared}"
            )
        raise MissingObservationReference(
            "observation_ids reference unknown observations: "
            f"{missing_from_items}"
        )
