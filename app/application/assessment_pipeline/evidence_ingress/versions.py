"""Version-aware AP-001 evidence ingress contract (AP-002D1)."""

from __future__ import annotations

# Ingress contract identity — bump when validation / mapping semantics change.
INGRESS_CONTRACT_VERSION = "AP-001.evidence_ingress.v1"

# Packaging versions lawfully accepted across the Evidence Boundary.
# Coordinated with Assessment packaging ``PACKAGING_VERSION`` (AP-002C.1).
SUPPORTED_PACKAGING_VERSIONS: frozenset[str] = frozenset({"AP-002C.1"})

# Provenance prefix for Twin observations created by this ingress.
INGRESS_PROVENANCE_PREFIX = "assessment_pipeline:evidence_bundle"

# triggered_by value passed to StudentReasoningService.reason
INGRESS_TRIGGERED_BY = "assessment_pipeline:evidence_bundle"
