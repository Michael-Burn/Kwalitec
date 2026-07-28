"""Validate evidence bundles before educational interpretation."""

from __future__ import annotations

from collections.abc import Collection

from app.application.reasoning.interpretation.errors import (
    BrokenEvidenceReference,
    InvalidConceptMapping,
    MissingLearningObjective,
    UnsupportedEvidenceSchema,
)
from app.application.reasoning.interpretation.versions import (
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


def validate_evidence_for_interpretation(
    bundle: object,
    *,
    supported_versions: Collection[str] | None = None,
) -> EvidenceBundleDTO:
    """Fail-closed validation for interpretation (never invent missing data).

    Raises:
        UnsupportedEvidenceSchema: unknown packaging version / wrong type
        BrokenEvidenceReference: broken observation / item references
        MissingLearningObjective: no learning objective references
        InvalidConceptMapping: blank concept ids when declared
    """
    if bundle is None:
        raise UnsupportedEvidenceSchema("evidence bundle payload is null")
    if not isinstance(bundle, EvidenceBundleDTO):
        raise UnsupportedEvidenceSchema(
            f"evidence bundle must be EvidenceBundleDTO, got {type(bundle).__name__}"
        )

    _require_non_empty(
        bundle.bundle_id, field="bundle_id", error=BrokenEvidenceReference
    )
    _require_non_empty(
        bundle.session_id, field="session_id", error=BrokenEvidenceReference
    )

    if bundle.context is None:
        raise UnsupportedEvidenceSchema("missing evidence context")
    if not (bundle.context.session_id or "").strip():
        raise BrokenEvidenceReference("missing context.session_id")
    if bundle.context.session_id.strip() != bundle.session_id.strip():
        raise BrokenEvidenceReference(
            "bundle.session_id does not match context.session_id"
        )

    metadata = bundle.metadata
    if metadata is None or not isinstance(metadata, EvidenceMetadataDTO):
        raise UnsupportedEvidenceSchema("missing evidence metadata")
    _validate_metadata(metadata, supported_versions=supported_versions)
    _validate_curriculum_refs(metadata)

    items = bundle.items
    if items is None or not isinstance(items, tuple) or len(items) == 0:
        raise BrokenEvidenceReference("evidence bundle contains no items")
    if bundle.observation_ids is None or not isinstance(bundle.observation_ids, tuple):
        raise BrokenEvidenceReference("missing observation_ids")

    _validate_items(items, observation_ids=bundle.observation_ids)

    if bundle.summary is None:
        raise UnsupportedEvidenceSchema("missing evidence summary")
    if bundle.summary.observation_count != len(items):
        raise UnsupportedEvidenceSchema(
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
        error=UnsupportedEvidenceSchema,
    )
    allowed = (
        frozenset(supported_versions)
        if supported_versions is not None
        else SUPPORTED_PACKAGING_VERSIONS
    )
    if packaging_version not in allowed:
        raise UnsupportedEvidenceSchema(
            f"unsupported packaging_version: {packaging_version!r}; "
            f"supported={sorted(allowed)}"
        )


def _validate_curriculum_refs(metadata: EvidenceMetadataDTO) -> None:
    raw_lo_ids = metadata.learning_objective_ids or ()
    if not raw_lo_ids:
        raise MissingLearningObjective(
            "learning_objective_ids required for educational interpretation"
        )
    lo_ids: list[str] = []
    for index, oid in enumerate(raw_lo_ids):
        if oid is None or not str(oid).strip():
            raise MissingLearningObjective(
                f"learning_objective_ids[{index}] is blank or invalid"
            )
        lo_ids.append(str(oid).strip())

    concept_ids = metadata.concept_ids or ()
    for index, concept_id in enumerate(concept_ids):
        if concept_id is None or not str(concept_id).strip():
            raise InvalidConceptMapping(
                f"concept_ids[{index}] is blank or invalid"
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
            raise UnsupportedEvidenceSchema(
                f"corrupted evidence item at index {index}"
            )
        item_id = _require_non_empty(
            item.item_id,
            field=f"items[{index}].item_id",
            error=BrokenEvidenceReference,
        )
        if item_id in seen_item_ids:
            raise BrokenEvidenceReference(f"duplicate evidence item_id: {item_id!r}")
        seen_item_ids.add(item_id)

        obs_id = (item.observation_id or "").strip()
        if not obs_id:
            raise BrokenEvidenceReference(
                f"items[{index}] missing observation_id"
            )
        if obs_id in seen_obs_ids:
            raise BrokenEvidenceReference(
                f"duplicate observation_id in evidence items: {obs_id!r}"
            )
        seen_obs_ids.add(obs_id)
        item_obs_ids.append(obs_id)

        if not (item.kind or "").strip():
            raise UnsupportedEvidenceSchema(f"items[{index}] missing kind")
        if not (item.evidence_source or "").strip():
            raise UnsupportedEvidenceSchema(
                f"items[{index}] missing evidence_source"
            )

    declared = tuple(oid.strip() for oid in observation_ids if (oid or "").strip())
    if len(declared) != len(observation_ids):
        raise BrokenEvidenceReference(
            "observation_ids contains blank observation identifiers"
        )
    if len(set(declared)) != len(declared):
        raise BrokenEvidenceReference("observation_ids contains duplicates")

    item_set = set(item_obs_ids)
    declared_set = set(declared)
    if item_set != declared_set:
        missing_from_declared = sorted(item_set - declared_set)
        missing_from_items = sorted(declared_set - item_set)
        if missing_from_declared:
            raise BrokenEvidenceReference(
                "observation_ids missing item observation references: "
                f"{missing_from_declared}"
            )
        raise BrokenEvidenceReference(
            "observation_ids reference unknown observations: "
            f"{missing_from_items}"
        )
