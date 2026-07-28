"""Contract version registry for AP-002D7 certification."""

from __future__ import annotations

from app.application.assessment_pipeline.evidence_ingress.versions import (
    INGRESS_CONTRACT_VERSION,
    SUPPORTED_PACKAGING_VERSIONS,
)
from app.application.intelligent_tutor.explainability.versions import (
    EXPLANATION_VERSION,
)
from app.application.learning_graph.projections.versions import PROJECTION_VERSION
from app.application.mission_engine.planning.versions import PLANNING_VERSION
from app.application.reasoning.decisions.versions import DECISION_VERSION
from app.application.reasoning.interpretation.versions import (
    INTERPRETATION_VERSION,
)
from app.application.reasoning.interpretation.versions import (
    SUPPORTED_PACKAGING_VERSIONS as INTERPRETATION_PACKAGING_VERSIONS,
)
from domain.assessment.evidence.models import PACKAGING_VERSION

# Canonical contract chain for Educational Intelligence Platform certification.
CERTIFIED_CONTRACTS: dict[str, str] = {
    "packaging": PACKAGING_VERSION,
    "evidence_ingress": INGRESS_CONTRACT_VERSION,
    "interpretation": INTERPRETATION_VERSION,
    "decision": DECISION_VERSION,
    "projection": PROJECTION_VERSION,
    "planning": PLANNING_VERSION,
    "explanation": EXPLANATION_VERSION,
}

EXPECTED_PACKAGING = "AP-002C.1"
EXPECTED_INGRESS = "AP-001.evidence_ingress.v1"
EXPECTED_INTERPRETATION = "AP-002D2.interpretation.v1"
EXPECTED_DECISION = "AP-002D3.decision.v1"
EXPECTED_PROJECTION = "AP-002D4.projection.v1"
EXPECTED_PLANNING = "AP-002D5.planning.v1"
EXPECTED_EXPLANATION = "AP-002D6.explanation.v1"

UNSUPPORTED_VERSION_PROBE = "AP-999.unsupported.v0"


def assert_certified_contract_matrix() -> None:
    """Fail closed when any certified contract drifts from the expected matrix."""
    assert PACKAGING_VERSION == EXPECTED_PACKAGING
    assert INGRESS_CONTRACT_VERSION == EXPECTED_INGRESS
    assert INTERPRETATION_VERSION == EXPECTED_INTERPRETATION
    assert DECISION_VERSION == EXPECTED_DECISION
    assert PROJECTION_VERSION == EXPECTED_PROJECTION
    assert PLANNING_VERSION == EXPECTED_PLANNING
    assert EXPLANATION_VERSION == EXPECTED_EXPLANATION
    assert SUPPORTED_PACKAGING_VERSIONS == frozenset({EXPECTED_PACKAGING})
    assert INTERPRETATION_PACKAGING_VERSIONS == frozenset({EXPECTED_PACKAGING})
