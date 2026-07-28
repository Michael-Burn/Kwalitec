"""Validation for assessment evidence packaging (structural only).

Validates traceability, duplicates, references, completeness, schema, and
metadata consistency. Does not perform educational / mastery validation.
"""

from __future__ import annotations

from collections.abc import Sequence

from domain.assessment.aggregation.observation_collection import ObservationCollection
from domain.assessment.entities.assessment_observation import AssessmentObservation
from domain.assessment.evidence.models import (
    PACKAGING_VERSION,
    EvidenceBundle,
    EvidenceItem,
)
from domain.assessment.exceptions import AssessmentInvariantViolation


def assert_observation_traceability(
    observations: Sequence[AssessmentObservation],
    items: Sequence[EvidenceItem],
) -> None:
    """Every evidence item must reference an originating observation; no loss."""
    obs_ids = {o.observation_id.value for o in observations}
    item_obs_ids = {item.reference.observation_id.value for item in items}
    missing_from_items = obs_ids - item_obs_ids
    if missing_from_items:
        raise AssessmentInvariantViolation(
            "evidence items missing observations: "
            + ", ".join(sorted(missing_from_items)),
            invariant="EvidencePackaging.traceability.missing_item",
        )
    orphan_items = item_obs_ids - obs_ids
    if orphan_items:
        raise AssessmentInvariantViolation(
            "evidence items reference unknown observations: "
            + ", ".join(sorted(orphan_items)),
            invariant="EvidencePackaging.traceability.orphan_item",
        )
    if len(items) != len(observations):
        raise AssessmentInvariantViolation(
            "evidence item count must equal observation count",
            invariant="EvidencePackaging.traceability.count",
        )


def assert_no_duplicate_observations(
    observations: Sequence[AssessmentObservation],
) -> None:
    seen: set[str] = set()
    for observation in observations:
        oid = observation.observation_id.value
        if oid in seen:
            raise AssessmentInvariantViolation(
                f"duplicate observation_id: {oid}",
                invariant="EvidencePackaging.observations.duplicate",
            )
        seen.add(oid)


def assert_observation_references(
    observations: Sequence[AssessmentObservation],
) -> None:
    for observation in observations:
        if observation.observation_id is None:
            raise AssessmentInvariantViolation(
                "observation_id is required",
                invariant="EvidencePackaging.observation_id.required",
            )
        if observation.session_id is None:
            raise AssessmentInvariantViolation(
                "session_id is required on observation",
                invariant="EvidencePackaging.session_id.required",
            )


def assert_bundle_schema(bundle: EvidenceBundle) -> None:
    """Validate packaging schema / metadata consistency (not educational meaning)."""
    if bundle.metadata.packaging_version != PACKAGING_VERSION:
        raise AssessmentInvariantViolation(
            f"unexpected packaging_version: {bundle.metadata.packaging_version}",
            invariant="EvidencePackaging.metadata.packaging_version",
        )
    if not bundle.items and bundle.summary.observation_count != 0:
        raise AssessmentInvariantViolation(
            "empty bundle cannot declare non-zero observation_count",
            invariant="EvidencePackaging.completeness.empty",
        )
    session_id = bundle.context.session_id
    for item in bundle.items:
        # Session uniformity checked at collection; re-check references.
        if item.reference.observation_id is None:
            raise AssessmentInvariantViolation(
                "evidence item missing observation reference",
                invariant="EvidencePackaging.reference.required",
            )
    if bundle.summary.observation_count != len(bundle.items):
        raise AssessmentInvariantViolation(
            "summary observation_count inconsistent with items",
            invariant="EvidencePackaging.summary.consistency",
        )
    # Metadata question ids must be a subset of item question refs when present.
    item_qids = {
        item.reference.question_id.value
        for item in bundle.items
        if item.reference.question_id is not None
    }
    for qid in bundle.metadata.question_ids:
        if qid.value not in item_qids and item_qids:
            raise AssessmentInvariantViolation(
                f"metadata question_id not present in items: {qid.value}",
                invariant="EvidencePackaging.metadata.question_refs",
            )
    _ = session_id  # context already validated on construction


def validate_packaging_inputs(collection: ObservationCollection) -> None:
    """Validate observations before packaging."""
    assert_no_duplicate_observations(collection.observations)
    assert_observation_references(collection.observations)


def validate_packaged_bundle(
    collection: ObservationCollection,
    bundle: EvidenceBundle,
) -> None:
    """Validate a packaged bundle against its source observations."""
    assert_observation_traceability(collection.observations, bundle.items)
    assert_bundle_schema(bundle)
