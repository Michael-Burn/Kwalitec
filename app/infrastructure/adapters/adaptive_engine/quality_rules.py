"""Explainability quality rules for AdaptiveOutputBundle (MS-003 A3).

Rules validate completeness only. They never mutate recommendations or
grant authority.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from app.infrastructure.adapters.adaptive_engine.contracts import (
    AdaptiveOutputBundle,
    ExplanationBundle,
)

# Stable rule identifiers for telemetry / diagnostics.
RULE_RECOMMENDATION_PRESENT = "explainability.recommendation_present"
RULE_CONFIDENCE_PRESENT = "explainability.confidence_present"
RULE_EVIDENCE_REFS_PRESENT = "explainability.evidence_refs_present"
RULE_INPUTS_USED_POPULATED = "explainability.inputs_used_populated"
RULE_INPUTS_UNAVAILABLE_POPULATED = "explainability.inputs_unavailable_populated"
RULE_RECOMMENDATION_RATIONALE_PRESENT = (
    "explainability.recommendation_rationale_present"
)
RULE_RULE_REFS_PRESENT = "explainability.rule_refs_present"

GATE_RULE_IDS: tuple[str, ...] = (
    RULE_RECOMMENDATION_PRESENT,
    RULE_CONFIDENCE_PRESENT,
    RULE_EVIDENCE_REFS_PRESENT,
    RULE_INPUTS_USED_POPULATED,
    RULE_INPUTS_UNAVAILABLE_POPULATED,
    RULE_RECOMMENDATION_RATIONALE_PRESENT,
    RULE_RULE_REFS_PRESENT,
)


@dataclass(frozen=True)
class QualityViolation:
    """One failed explainability quality check (observational)."""

    rule_id: str
    message: str

    def to_canonical_dict(self) -> dict[str, str]:
        return {"message": self.message, "rule_id": self.rule_id}


QualityCheck = Callable[[AdaptiveOutputBundle], QualityViolation | None]


def _recommendation_present(output: AdaptiveOutputBundle) -> QualityViolation | None:
    rec = output.recommendation
    present = bool(
        (rec.topic_code or "").strip()
        or (rec.title or "").strip()
        or (rec.label or "").strip()
        or (rec.decision_kind or "").strip()
    )
    if present:
        return None
    return QualityViolation(
        rule_id=RULE_RECOMMENDATION_PRESENT,
        message=(
            "Recommendation must include topic_code, title, label, or decision_kind"
        ),
    )


def _confidence_present(output: AdaptiveOutputBundle) -> QualityViolation | None:
    confidence = output.confidence
    band = (confidence.band or "").strip()
    if band or confidence.score is not None:
        return None
    # Also accept explanation-level confidence when top-level is empty shell.
    expl_conf = output.explanation.confidence
    expl_band = (expl_conf.band or "").strip()
    if expl_band or expl_conf.score is not None:
        return None
    return QualityViolation(
        rule_id=RULE_CONFIDENCE_PRESENT,
        message="Confidence must include a band or score",
    )


def _evidence_refs_present(output: AdaptiveOutputBundle) -> QualityViolation | None:
    refs = output.explanation.evidence_refs or ()
    material = [
        ref
        for ref in refs
        if (ref.kind or "").strip() and (ref.id or "").strip()
    ]
    if material:
        return None
    return QualityViolation(
        rule_id=RULE_EVIDENCE_REFS_PRESENT,
        message="ExplanationBundle must include at least one evidence reference",
    )


def _inputs_used_populated(output: AdaptiveOutputBundle) -> QualityViolation | None:
    used = output.explanation.inputs_used
    if used is None:
        return QualityViolation(
            rule_id=RULE_INPUTS_USED_POPULATED,
            message="ExplanationBundle.inputs_used must be populated",
        )
    if len(used) == 0:
        return QualityViolation(
            rule_id=RULE_INPUTS_USED_POPULATED,
            message="ExplanationBundle.inputs_used must list at least one used input",
        )
    return None


def _inputs_unavailable_populated(
    output: AdaptiveOutputBundle,
) -> QualityViolation | None:
    unavailable = output.explanation.inputs_unavailable
    # May be empty, but the field must be present as a sequence.
    if unavailable is None:
        return QualityViolation(
            rule_id=RULE_INPUTS_UNAVAILABLE_POPULATED,
            message=(
                "ExplanationBundle.inputs_unavailable must be populated "
                "(may be empty)"
            ),
        )
    return None


def _recommendation_rationale_present(
    output: AdaptiveOutputBundle,
) -> QualityViolation | None:
    rationale = (output.explanation.recommendation_rationale or "").strip()
    if rationale:
        return None
    return QualityViolation(
        rule_id=RULE_RECOMMENDATION_RATIONALE_PRESENT,
        message="ExplanationBundle.recommendation_rationale must be present",
    )


def _rule_refs_present(output: AdaptiveOutputBundle) -> QualityViolation | None:
    refs = output.explanation.rule_refs or ()
    material = [
        ref for ref in refs if (ref.rule_or_model_id or "").strip()
    ]
    if material:
        return None
    return QualityViolation(
        rule_id=RULE_RULE_REFS_PRESENT,
        message="ExplanationBundle must include at least one rule reference",
    )


QUALITY_CHECKS: tuple[QualityCheck, ...] = (
    _recommendation_present,
    _confidence_present,
    _evidence_refs_present,
    _inputs_used_populated,
    _inputs_unavailable_populated,
    _recommendation_rationale_present,
    _rule_refs_present,
)


def evaluate_quality_rules(
    output: AdaptiveOutputBundle,
) -> tuple[QualityViolation, ...]:
    """Run all quality rules; return violations (empty when all pass).

    Does not mutate ``output``.
    """
    if not isinstance(output, AdaptiveOutputBundle):
        raise TypeError("output must be an AdaptiveOutputBundle")
    violations: list[QualityViolation] = []
    for check in QUALITY_CHECKS:
        violation = check(output)
        if violation is not None:
            violations.append(violation)
    return tuple(violations)


def validate_explanation_bundle(
    explanation: ExplanationBundle,
    *,
    require_recommendation_shell: bool = False,
) -> tuple[QualityViolation, ...]:
    """Validate ExplanationBundle facets required by the Explainability Gate.

    When called standalone, recommendation/confidence presence are checked via
    a temporary AdaptiveOutputBundle shell only if ``require_recommendation_shell``
    is True. Prefer ``evaluate_quality_rules`` for full AdaptiveOutputBundle gates.
    """
    if not isinstance(explanation, ExplanationBundle):
        raise TypeError("explanation must be an ExplanationBundle")
    from app.infrastructure.adapters.adaptive_engine.contracts import (
        ConfidencePlaceholder,
        RecommendationPlaceholder,
    )

    shell = AdaptiveOutputBundle(
        recommendation=RecommendationPlaceholder(
            topic_code="gate-shell" if require_recommendation_shell else None,
            decision_kind="GATE_SHELL" if require_recommendation_shell else "",
        ),
        confidence=ConfidencePlaceholder(score=0.0, band="low"),
        explanation=explanation,
    )
    # Only ExplanationBundle-scoped rules when validating the bundle alone.
    explanation_rule_ids = {
        RULE_EVIDENCE_REFS_PRESENT,
        RULE_INPUTS_USED_POPULATED,
        RULE_INPUTS_UNAVAILABLE_POPULATED,
        RULE_RECOMMENDATION_RATIONALE_PRESENT,
        RULE_RULE_REFS_PRESENT,
    }
    return tuple(
        v
        for v in evaluate_quality_rules(shell)
        if v.rule_id in explanation_rule_ids
    )
