"""Assessment evidence packaging (strength, builder, validation)."""

from __future__ import annotations

from domain.assessment.packaging.builder import (
    EvidenceBundleBuilder,
    enrich_dimensions_from_observation,
    package_observations,
)
from domain.assessment.packaging.packager import EvidencePackager
from domain.assessment.packaging.strength import (
    EvidenceStrengthFactors,
    calculate_evidence_strength,
    derive_strength_factors,
)
from domain.assessment.packaging.validation import (
    assert_bundle_schema,
    assert_no_duplicate_observations,
    assert_observation_references,
    assert_observation_traceability,
    validate_packaged_bundle,
    validate_packaging_inputs,
)

__all__ = [
    "EvidenceBundleBuilder",
    "EvidencePackager",
    "EvidenceStrengthFactors",
    "assert_bundle_schema",
    "assert_no_duplicate_observations",
    "assert_observation_references",
    "assert_observation_traceability",
    "calculate_evidence_strength",
    "derive_strength_factors",
    "enrich_dimensions_from_observation",
    "package_observations",
    "validate_packaged_bundle",
    "validate_packaging_inputs",
]
