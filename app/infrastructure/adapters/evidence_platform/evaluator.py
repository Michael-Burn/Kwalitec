"""Deterministic policy evaluator (MS-006 E3).

Assesses immutable ExperimentObservations against a registered
PolicyDefinition. Produces a PolicyAssessment draft only — never mutates
observations or evidence, never promotes policies, never changes educational
behaviour.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from typing import Any

from app.infrastructure.adapters.evidence_platform.contracts import (
    CLAIM_LEARNING_DEPTH,
    CLAIM_ORGANISATION,
    EVALUATION_KIND_POST_HOC_INCIDENT,
    EVALUATION_KIND_RESEARCH_LINKAGE,
    EVALUATION_KIND_SHADOW_COMPARE,
    EVALUATION_KIND_SHADOW_DESCRIPTIVE,
    GATE_CODE_CLAIM_BOUNDARY_LEAKAGE,
    GATE_CODE_DEMO_THEATRE,
    GATE_CODE_INSUFFICIENT_OBSERVATIONS,
    GATE_CODE_MISSING_RUNTIME_A,
    RECOMMENDATION_EXPAND_SOAK,
    RECOMMENDATION_INCONCLUSIVE,
    RECOMMENDATION_REVISE,
    RECOMMENDATION_ROLL_BACK,
    STATISTICAL_DESIGN_DESCRIPTIVE_SOAK,
    ExperimentObservation,
    PolicyDefinition,
)
from app.infrastructure.adapters.evidence_platform.evaluation_explainability import (
    PolicyAssessment,
)
from app.infrastructure.adapters.evidence_platform.evaluation_validator import (
    EvaluationValidationError,
    EvaluationValidator,
)

DEFAULT_MIN_OBSERVATIONS = 3
DEFAULT_MIN_STUDENTS = 2

_DEMO_MARKERS = frozenset(
    {
        "demo",
        "seed",
        "fixture_demo",
        "theatre",
        "synthetic_demo",
    }
)


class PolicyEvaluator:
    """Deterministic observational policy assessor (E3).

    Identical ExperimentObservations + Identical PolicyDefinition → Identical
    PolicyAssessment every execution.
    """

    EVALUATOR_ID = "policy_evaluator"
    EVALUATOR_VERSION = "1.0.0-e3"

    def __init__(self, *, validator: EvaluationValidator | None = None) -> None:
        self._validator = validator or EvaluationValidator()

    @property
    def evaluator_id(self) -> str:
        return self.EVALUATOR_ID

    @property
    def evaluator_version(self) -> str:
        return self.EVALUATOR_VERSION

    @property
    def validator(self) -> EvaluationValidator:
        return self._validator

    def assess(
        self,
        observations: Sequence[ExperimentObservation],
        definition: PolicyDefinition,
    ) -> PolicyAssessment:
        """Assess observations against a registered policy definition.

        Does not mutate ``observations`` or ``definition``.
        """
        validated_definition = self._validator.validate_definition(
            definition, require_evaluable=True
        )
        validated_observations = self._validator.validate_observations(
            observations, validated_definition
        )

        arm_counts = Counter(obs.arm_id for obs in validated_observations)
        student_ids = sorted({obs.student_id for obs in validated_observations})
        experiment_refs = tuple(
            sorted({obs.experiment_id for obs in validated_observations})
        )
        evidence_refs = tuple(
            sorted({obs.evidence_id for obs in validated_observations})
        )
        evidence_bundle_ids = evidence_refs

        runtime_a_ref_count = 0
        supporting_upstream: set[str] = set()
        claim_boundaries: set[str] = set()
        quality_codes: list[str] = []
        demo_markers: list[str] = []
        for obs in validated_observations:
            meta = dict(obs.metadata or {})
            evidence_ref = dict(obs.evidence_ref or {})
            if _has_runtime_a(meta, evidence_ref):
                runtime_a_ref_count += 1
            for layer in ("twin", "adaptive", "strategy", "experience"):
                if meta.get(layer) or evidence_ref.get(layer):
                    supporting_upstream.add(layer)
            boundary = str(
                meta.get("claim_boundary")
                or evidence_ref.get("claim_boundary")
                or ""
            ).strip().lower()
            if boundary:
                claim_boundaries.add(boundary)
            for code in _as_str_seq(meta.get("quality_codes")):
                quality_codes.append(code)
            for marker in _detect_demo_markers(meta, evidence_ref, obs):
                demo_markers.append(marker)

        quality_codes = sorted(set(quality_codes))
        demo_markers = sorted(set(demo_markers))
        claim_boundaries_present = tuple(sorted(claim_boundaries))
        supporting_upstream_refs = tuple(sorted(supporting_upstream))

        gate_codes: list[str] = []
        limitations: list[str] = list(validated_definition.limitations)
        limitations.append("descriptive_only_no_causal_claim")
        limitations.append("governance_recommendation_only")

        if demo_markers:
            gate_codes.append(GATE_CODE_DEMO_THEATRE)
            limitations.append("demo_or_seed_markers_present")

        if _claim_boundary_leakage(
            validated_definition, claim_boundaries_present
        ):
            gate_codes.append(GATE_CODE_CLAIM_BOUNDARY_LEAKAGE)
            limitations.append("organisation_narrated_as_learning_depth")

        requires_runtime_a = (
            validated_definition.claim_boundary_intent
            in {CLAIM_LEARNING_DEPTH, ""}
            and validated_definition.evaluation_kind
            != EVALUATION_KIND_RESEARCH_LINKAGE
            and validated_definition.claim_boundary_intent == CLAIM_LEARNING_DEPTH
        )
        if requires_runtime_a and runtime_a_ref_count == 0:
            gate_codes.append(GATE_CODE_MISSING_RUNTIME_A)
            limitations.append("missing_runtime_a_for_learning_outcome_claim")

        min_observations = _eligibility_int(
            validated_definition.evaluation_eligibility,
            "min_observations",
            DEFAULT_MIN_OBSERVATIONS,
        )
        min_students = _eligibility_int(
            validated_definition.evaluation_eligibility,
            "min_students",
            DEFAULT_MIN_STUDENTS,
        )
        observation_count = len(validated_observations)
        student_count = len(student_ids)
        if observation_count < min_observations or student_count < min_students:
            gate_codes.append(GATE_CODE_INSUFFICIENT_OBSERVATIONS)
            limitations.append("insufficient_observation_sample")

        design = str(
            (validated_definition.statistical_plan or {}).get("design")
            or STATISTICAL_DESIGN_DESCRIPTIVE_SOAK
        ).strip()
        if not design:
            design = STATISTICAL_DESIGN_DESCRIPTIVE_SOAK

        not_proven = (
            "Learner-visible educational authority improvement",
            "Causal superiority of treatment arm",
            "Learning-depth gain from organisation metrics alone",
            "Automatic policy promotion eligibility",
        )

        recommendation, confidence_band, confidence_rationale = _recommend(
            definition=validated_definition,
            gate_codes=gate_codes,
            observation_count=observation_count,
            student_count=student_count,
            arm_counts=arm_counts,
            design=design,
        )

        effect_summary = (
            f"arm_distribution={dict(sorted(arm_counts.items()))}; "
            f"experiments={list(experiment_refs)}"
        )
        statistical_summary = {
            "design": design,
            "sample": {
                "n_observations": observation_count,
                "n_students": student_count,
                "n_experiments": len(experiment_refs),
                "arms": dict(sorted(arm_counts.items())),
            },
            "estimator": "descriptive_only",
            "effect": effect_summary,
            "uncertainty": "not_estimable",
            "multiplicity": "not_adjusted_descriptive",
            "pre_registration_id": str(
                (validated_definition.statistical_plan or {}).get(
                    "pre_registration_id"
                )
                or validated_definition.spec_ref
                or ""
            ),
            "failure_modes": [
                "demo_markers",
                "claim_boundary_leakage",
                "insufficient_sample",
            ],
        }
        outcome_metric_payloads = (
            {
                "metric_id": "observation_count",
                "claim_boundary": (
                    validated_definition.claim_boundary_intent or CLAIM_ORGANISATION
                ),
                "value": observation_count,
                "n": observation_count,
                "uncertainty": "not_estimable",
                "grain": "evaluation",
                "subject_scope": "policy_evaluation",
            },
            {
                "metric_id": "arm_entropy_proxy",
                "claim_boundary": CLAIM_ORGANISATION,
                "value": len(arm_counts),
                "n": observation_count,
                "uncertainty": "not_estimable",
                "grain": "evaluation",
                "subject_scope": "policy_evaluation",
            },
        )

        return PolicyAssessment(
            recommendation=recommendation,
            confidence_band=confidence_band,
            confidence_rationale=confidence_rationale,
            gate_codes=tuple(sorted(set(gate_codes))),
            limitations=tuple(dict.fromkeys(limitations)),
            statistical_summary=statistical_summary,
            outcome_metric_payloads=outcome_metric_payloads,
            experiment_refs=experiment_refs,
            evidence_refs=evidence_refs,
            evidence_bundle_ids=evidence_bundle_ids,
            arm_distribution=dict(sorted(arm_counts.items())),
            observation_count=observation_count,
            student_count=student_count,
            runtime_a_ref_count=runtime_a_ref_count,
            quality_codes=tuple(quality_codes),
            supporting_upstream_refs=supporting_upstream_refs,
            claim_boundaries_present=claim_boundaries_present,
            demo_markers=tuple(demo_markers),
            design=design,
            estimator="descriptive_only",
            effect_summary=effect_summary,
            uncertainty_summary="not_estimable",
            not_proven=not_proven,
        )


def _recommend(
    *,
    definition: PolicyDefinition,
    gate_codes: Sequence[str],
    observation_count: int,
    student_count: int,
    arm_counts: Mapping[str, int],
    design: str,
) -> tuple[str, str, str]:
    """Deterministic recommendation / confidence selection (no promotion)."""
    codes = set(gate_codes)
    kind = definition.evaluation_kind or EVALUATION_KIND_SHADOW_DESCRIPTIVE

    if GATE_CODE_DEMO_THEATRE in codes:
        return (
            RECOMMENDATION_ROLL_BACK,
            "insufficient",
            "Demo or seed markers present; evaluation is non-actionable for promote.",
        )
    if GATE_CODE_CLAIM_BOUNDARY_LEAKAGE in codes:
        return (
            RECOMMENDATION_REVISE,
            "insufficient",
            "Claim-boundary leakage detected; revise policy narrative before soak.",
        )
    if GATE_CODE_MISSING_RUNTIME_A in codes:
        return (
            RECOMMENDATION_REVISE,
            "insufficient",
            "Learning-depth claim lacks Runtime A evidence references.",
        )
    if GATE_CODE_INSUFFICIENT_OBSERVATIONS in codes:
        return (
            RECOMMENDATION_EXPAND_SOAK,
            "insufficient",
            (
                f"Insufficient sample "
                f"(observations={observation_count}, students={student_count})."
            ),
        )
    if kind == EVALUATION_KIND_RESEARCH_LINKAGE:
        return (
            RECOMMENDATION_INCONCLUSIVE,
            "low",
            "Research linkage never upgrades qualitative themes to Runtime A fact.",
        )
    if kind == EVALUATION_KIND_POST_HOC_INCIDENT:
        return (
            RECOMMENDATION_REVISE,
            "low",
            "Post-hoc incident review is biased against celebration metrics.",
        )
    if kind in {
        EVALUATION_KIND_SHADOW_DESCRIPTIVE,
        EVALUATION_KIND_SHADOW_COMPARE,
    } or design == STATISTICAL_DESIGN_DESCRIPTIVE_SOAK:
        band = "medium" if observation_count >= 10 and student_count >= 5 else "low"
        return (
            RECOMMENDATION_EXPAND_SOAK,
            band,
            (
                "Descriptive soak complete enough for expand_soak only; "
                f"arms={dict(sorted(arm_counts.items()))}. "
                "Descriptive_only cannot justify keep of learner-visible Authority."
            ),
        )
    return (
        RECOMMENDATION_INCONCLUSIVE,
        "low",
        "No promote-grade estimator available; governance recommendation inconclusive.",
    )


def _has_runtime_a(meta: Mapping[str, Any], evidence_ref: Mapping[str, Any]) -> bool:
    if meta.get("runtime_a_ref_present") is True:
        return True
    if meta.get("runtime_a") or evidence_ref.get("runtime_a"):
        return True
    if str(evidence_ref.get("evidence_id") or "").startswith("ev-"):
        # Evidence ids from E1 collection imply Runtime A may be present; only
        # count when explicitly flagged or nested runtime_a payload exists.
        return bool(meta.get("runtime_a_ref_present"))
    return False


def _claim_boundary_leakage(
    definition: PolicyDefinition,
    claim_boundaries_present: Sequence[str],
) -> bool:
    rationale = dict(definition.educational_rationale or {})
    narrative = " ".join(
        str(rationale.get(key) or "")
        for key in (
            "student_impact_hypothesis",
            "organisation_vs_learning_note",
            "summary",
        )
    ).lower()
    org_as_learning = (
        "organisation" in narrative
        and ("learning depth" in narrative or "learning_depth" in narrative)
        and (
            "as learning" in narrative
            or "equals learning" in narrative
            or "is learning depth" in narrative
        )
    )
    if org_as_learning:
        return True
    if definition.claim_boundary_intent == CLAIM_ORGANISATION:
        if CLAIM_LEARNING_DEPTH in claim_boundaries_present and bool(
            rationale.get("treat_organisation_as_learning_depth")
        ):
            return True
    return False


def _detect_demo_markers(
    meta: Mapping[str, Any],
    evidence_ref: Mapping[str, Any],
    observation: ExperimentObservation,
) -> list[str]:
    found: list[str] = []
    candidates = [
        meta.get("demo"),
        meta.get("seed"),
        meta.get("marker"),
        meta.get("source"),
        evidence_ref.get("marker"),
        observation.assignment_rationale,
    ]
    for raw in _as_str_seq(meta.get("markers")):
        candidates.append(raw)
    for candidate in candidates:
        token = str(candidate or "").strip().lower()
        if not token:
            continue
        for marker in _DEMO_MARKERS:
            if marker in token:
                found.append(marker)
    return found


def _as_str_seq(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,) if value.strip() else ()
    if isinstance(value, Sequence) and not isinstance(value, str | bytes):
        return tuple(str(item) for item in value if str(item).strip())
    return ()


def _eligibility_int(
    eligibility: Mapping[str, Any] | None,
    key: str,
    default: int,
) -> int:
    if not eligibility:
        return default
    raw = eligibility.get(key, default)
    try:
        value = int(raw)
    except (TypeError, ValueError) as exc:
        raise EvaluationValidationError(
            f"evaluation_eligibility.{key} must be an int"
        ) from exc
    if value < 0:
        raise EvaluationValidationError(
            f"evaluation_eligibility.{key} must be >= 0"
        )
    return value


def build_policy_evaluator(
    *,
    enabled: bool,
    validator: EvaluationValidator | None = None,
) -> PolicyEvaluator | None:
    """DI helper — construct PolicyEvaluator only when the flag is on."""
    if not enabled:
        return None
    return PolicyEvaluator(validator=validator)
