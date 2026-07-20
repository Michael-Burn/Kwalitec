"""Policy governing EducationalHypothesis construction and identity integrity.

Architecture Source
    EDUCATIONAL_HYPOTHESIS_MODEL.md
Concept
    Hypothesis Validation Policy
"""

from __future__ import annotations

from domain.education.foundation.base import (
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import EvidenceId, HypothesisId
from domain.education.hypothesis.entities.competing_hypothesis import (
    CompetingHypothesis,
)
from domain.education.hypothesis.entities.hypothesis_reason import (
    DiagnosisReference,
    HypothesisReason,
    InterpretationReference,
)
from domain.education.hypothesis.entities.hypothesis_scope import HypothesisScope
from domain.education.hypothesis.enums import HypothesisKind, HypothesisStatus
from domain.education.hypothesis.value_objects.explanatory_strength import (
    ExplanatoryStrength,
)
from domain.education.hypothesis.value_objects.plausibility import Plausibility

# Hypothesis kinds that lawfully explain each deficiency category.
_COMPATIBLE_DIAGNOSIS: dict[HypothesisKind, frozenset[DiagnosisType]] = {
    HypothesisKind.PREREQUISITE_DEFICIENCY: frozenset(
        {
            DiagnosisType.PREREQUISITE_GAP,
            DiagnosisType.INCOMPLETE_UNDERSTANDING,
            DiagnosisType.APPLICATION_WEAKNESS,
        }
    ),
    HypothesisKind.REPRESENTATION_MISMATCH: frozenset(
        {
            DiagnosisType.CONCEPTUAL_MISUNDERSTANDING,
            DiagnosisType.INCOMPLETE_UNDERSTANDING,
            DiagnosisType.KNOWLEDGE_FRAGMENTATION,
        }
    ),
    HypothesisKind.WEAK_ABSTRACTION: frozenset(
        {
            DiagnosisType.CONCEPTUAL_MISUNDERSTANDING,
            DiagnosisType.INCOMPLETE_UNDERSTANDING,
            DiagnosisType.KNOWLEDGE_FRAGMENTATION,
            DiagnosisType.APPLICATION_WEAKNESS,
        }
    ),
    HypothesisKind.SURFACE_MEMORISATION: frozenset(
        {
            DiagnosisType.WEAK_RETENTION,
            DiagnosisType.TRANSFER_WEAKNESS,
            DiagnosisType.APPLICATION_WEAKNESS,
            DiagnosisType.EXAM_TECHNIQUE_WEAKNESS,
        }
    ),
    HypothesisKind.PROCEDURAL_FIXATION: frozenset(
        {
            DiagnosisType.PROCEDURAL_WEAKNESS,
            DiagnosisType.APPLICATION_WEAKNESS,
            DiagnosisType.MISCONCEPTION,
        }
    ),
    HypothesisKind.TRANSFER_LIMITATION: frozenset(
        {
            DiagnosisType.TRANSFER_WEAKNESS,
            DiagnosisType.APPLICATION_WEAKNESS,
            DiagnosisType.KNOWLEDGE_FRAGMENTATION,
        }
    ),
    HypothesisKind.CONFIDENCE_CALIBRATION_ISSUE: frozenset(
        {
            DiagnosisType.LOW_CONFIDENCE,
            DiagnosisType.FALSE_CONFIDENCE,
        }
    ),
}

# Direct contradictions: diagnosis types that deny the explanation family.
_CONTRADICTORY_DIAGNOSIS: dict[HypothesisKind, frozenset[DiagnosisType]] = {
    HypothesisKind.PREREQUISITE_DEFICIENCY: frozenset(
        {DiagnosisType.FALSE_CONFIDENCE}
    ),
    HypothesisKind.CONFIDENCE_CALIBRATION_ISSUE: frozenset(
        {
            DiagnosisType.PREREQUISITE_GAP,
            DiagnosisType.MISCONCEPTION,
            DiagnosisType.PROCEDURAL_WEAKNESS,
        }
    ),
    HypothesisKind.TRANSFER_LIMITATION: frozenset(
        {DiagnosisType.PREREQUISITE_GAP}
    ),
    HypothesisKind.SURFACE_MEMORISATION: frozenset(
        {DiagnosisType.MISCONCEPTION}
    ),
}

_TERMINAL_STATUSES = frozenset({HypothesisStatus.DISCARDED})


class HypothesisValidationPolicy:
    """Enforces EducationalHypothesis identity, ownership, and support invariants."""

    @staticmethod
    def assert_identity(hypothesis_id: HypothesisId) -> HypothesisId:
        if not isinstance(hypothesis_id, HypothesisId):
            raise EducationalInvariantViolation(
                "hypothesis must possess a HypothesisId identity",
                invariant="EducationalHypothesis.identity.required",
            )
        return hypothesis_id

    @staticmethod
    def assert_student_id(student_id: str) -> str:
        return require_identity_value(student_id, "student_id")

    @staticmethod
    def assert_hypothesis_kind(hypothesis_kind: HypothesisKind) -> HypothesisKind:
        if not isinstance(hypothesis_kind, HypothesisKind):
            raise EducationalInvariantViolation(
                "hypothesis must name a HypothesisKind from the authoritative "
                "explanation catalogue",
                invariant="EducationalHypothesis.kind.required",
            )
        return hypothesis_kind

    @staticmethod
    def assert_explanation(explanation: str) -> str:
        cleaned = require_non_empty_text(explanation, "explanation")
        HypothesisValidationPolicy._reject_how_to_smuggling(cleaned)
        HypothesisValidationPolicy._reject_unfalsifiable(cleaned)
        return cleaned

    @staticmethod
    def _reject_how_to_smuggling(explanation: str) -> None:
        lowered = explanation.casefold()
        forbidden_fragments = (
            "therefore teach",
            "therefore use",
            "recommend strategy",
            "select strategy",
            "we should drill",
            "assign episode",
            "priority is",
            "prioritise",
            "prioritize",
        )
        for fragment in forbidden_fragments:
            if fragment in lowered:
                raise EducationalInvariantViolation(
                    "hypothesis explanation must not encode teaching strategy, "
                    "priority, or recommendation",
                    invariant="EducationalHypothesis.explanation.no_how_to",
                )

    @staticmethod
    def _reject_unfalsifiable(explanation: str) -> None:
        lowered = explanation.casefold()
        forbidden_fragments = (
            "just bad at",
            "naturally unable",
            "cannot learn",
            "hopeless at",
        )
        for fragment in forbidden_fragments:
            if fragment in lowered:
                raise EducationalInvariantViolation(
                    "hypothesis explanation must be educationally falsifiable",
                    invariant="EducationalHypothesis.explanation.falsifiable",
                )

    @staticmethod
    def assert_scope(scope: HypothesisScope) -> HypothesisScope:
        if not isinstance(scope, HypothesisScope):
            raise EducationalInvariantViolation(
                "hypothesis must identify educational scope",
                invariant="EducationalHypothesis.scope.required",
            )
        if not scope.statement.strip():
            raise EducationalInvariantViolation(
                "hypothesis must identify educational scope",
                invariant="EducationalHypothesis.scope.statement.required",
            )
        return scope

    @staticmethod
    def assert_plausibility(plausibility: Plausibility) -> Plausibility:
        if not isinstance(plausibility, Plausibility):
            raise EducationalInvariantViolation(
                "hypothesis must possess plausibility",
                invariant="EducationalHypothesis.plausibility.required",
            )
        return plausibility

    @staticmethod
    def assert_explanatory_strength(
        strength: ExplanatoryStrength,
    ) -> ExplanatoryStrength:
        if not isinstance(strength, ExplanatoryStrength):
            raise EducationalInvariantViolation(
                "hypothesis must possess explanatory strength",
                invariant="EducationalHypothesis.explanatory_strength.required",
            )
        return strength

    @staticmethod
    def assert_status(status: HypothesisStatus) -> HypothesisStatus:
        if not isinstance(status, HypothesisStatus):
            raise EducationalInvariantViolation(
                "status must be a HypothesisStatus",
                invariant="EducationalHypothesis.status.type",
            )
        return status

    @staticmethod
    def assert_diagnosis_references(
        references: tuple[DiagnosisReference, ...] | list[DiagnosisReference],
    ) -> tuple[DiagnosisReference, ...]:
        """Hypothesis must reference at least one diagnosis."""
        collected = tuple(references)
        if not collected:
            raise EducationalInvariantViolation(
                "hypothesis must reference diagnosis",
                invariant="EducationalHypothesis.diagnosis_references.min_one",
            )
        seen: set[str] = set()
        for ref in collected:
            if not isinstance(ref, DiagnosisReference):
                raise EducationalInvariantViolation(
                    "diagnosis_references must be DiagnosisReference values",
                    invariant="EducationalHypothesis.diagnosis_references.type",
                )
            if ref.diagnosis_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate diagnosis reference is not allowed",
                    invariant=(
                        "EducationalHypothesis.diagnosis_references.no_duplicate"
                    ),
                )
            seen.add(ref.diagnosis_id.value)
        return collected

    @staticmethod
    def assert_interpretation_references(
        references: tuple[InterpretationReference, ...]
        | list[InterpretationReference],
    ) -> tuple[InterpretationReference, ...]:
        collected = tuple(references)
        seen: set[str] = set()
        for ref in collected:
            if not isinstance(ref, InterpretationReference):
                raise EducationalInvariantViolation(
                    "interpretation_references must be InterpretationReference "
                    "values",
                    invariant="EducationalHypothesis.interpretation_references.type",
                )
            if ref.interpretation_id in seen:
                raise EducationalInvariantViolation(
                    "duplicate interpretation reference is not allowed",
                    invariant=(
                        "EducationalHypothesis.interpretation_references.no_duplicate"
                    ),
                )
            seen.add(ref.interpretation_id)
        return collected

    @staticmethod
    def assert_evidence_ids(
        evidence_ids: tuple[EvidenceId, ...] | list[EvidenceId],
    ) -> tuple[EvidenceId, ...]:
        collected = tuple(evidence_ids)
        seen: set[str] = set()
        for evidence_id in collected:
            if not isinstance(evidence_id, EvidenceId):
                raise EducationalInvariantViolation(
                    "evidence_ids must be EvidenceId values",
                    invariant="EducationalHypothesis.evidence_ids.type",
                )
            if evidence_id.value in seen:
                raise EducationalInvariantViolation(
                    "duplicate evidence id is not allowed",
                    invariant="EducationalHypothesis.evidence_ids.no_duplicate",
                )
            seen.add(evidence_id.value)
        return collected

    @staticmethod
    def assert_reasons(
        reasons: tuple[HypothesisReason, ...] | list[HypothesisReason],
    ) -> tuple[HypothesisReason, ...]:
        """Hypothesis must state at least one supporting reason."""
        collected = tuple(reasons)
        if not collected:
            raise EducationalInvariantViolation(
                "hypothesis must possess at least one supporting reason",
                invariant="EducationalHypothesis.reasons.min_one",
            )
        seen_ids: set[str] = set()
        seen_signatures: set[tuple[str, str | None]] = set()
        for reason in collected:
            if not isinstance(reason, HypothesisReason):
                raise EducationalInvariantViolation(
                    "reasons must be HypothesisReason entities",
                    invariant="EducationalHypothesis.reasons.type",
                )
            if reason.reason_id.value in seen_ids:
                raise EducationalInvariantViolation(
                    "duplicate hypothesis reason identity is not allowed",
                    invariant="EducationalHypothesis.reasons.no_duplicate_id",
                )
            signature = reason.reason_signature()
            if signature in seen_signatures:
                raise EducationalInvariantViolation(
                    "cannot duplicate supporting reasons",
                    invariant="EducationalHypothesis.reasons.no_identical_duplicate",
                )
            seen_ids.add(reason.reason_id.value)
            seen_signatures.add(signature)
        return collected

    @staticmethod
    def assert_competing_hypotheses(
        competitors: tuple[CompetingHypothesis, ...] | list[CompetingHypothesis],
        *,
        primary_kind: HypothesisKind,
        primary_explanation: str,
    ) -> tuple[CompetingHypothesis, ...]:
        """Competitors must be distinct; cannot duplicate primary or each other."""
        collected = tuple(competitors)
        seen_ids: set[str] = set()
        seen_signatures: set[tuple[str, str]] = set()
        primary_signature = (primary_kind.value, primary_explanation.casefold())
        for competitor in collected:
            if not isinstance(competitor, CompetingHypothesis):
                raise EducationalInvariantViolation(
                    "competing_hypotheses must be CompetingHypothesis entities",
                    invariant="EducationalHypothesis.competitors.type",
                )
            if competitor.competing_id.value in seen_ids:
                raise EducationalInvariantViolation(
                    "duplicate competing hypothesis identity is not allowed",
                    invariant="EducationalHypothesis.competitors.no_duplicate_id",
                )
            signature = competitor.competitor_signature()
            if signature in seen_signatures:
                raise EducationalInvariantViolation(
                    "cannot duplicate competing hypotheses",
                    invariant=(
                        "EducationalHypothesis.competitors.no_identical_duplicate"
                    ),
                )
            if signature == primary_signature:
                raise EducationalInvariantViolation(
                    "competing hypothesis must be educationally distinct "
                    "from the primary explanation",
                    invariant="EducationalHypothesis.competitors.distinct_from_primary",
                )
            if competitor.hypothesis_kind is primary_kind and (
                competitor.explanation.casefold() == primary_explanation.casefold()
            ):
                raise EducationalInvariantViolation(
                    "competing hypothesis must be educationally distinct "
                    "from the primary explanation",
                    invariant="EducationalHypothesis.competitors.distinct_from_primary",
                )
            seen_ids.add(competitor.competing_id.value)
            seen_signatures.add(signature)
        return collected

    @staticmethod
    def assert_compatible_with_diagnosis(
        hypothesis_kind: HypothesisKind,
        diagnosis_references: tuple[DiagnosisReference, ...]
        | list[DiagnosisReference],
    ) -> None:
        """Hypothesis cannot contradict supporting diagnosis."""
        compatible = _COMPATIBLE_DIAGNOSIS.get(hypothesis_kind, frozenset())
        contradictory = _CONTRADICTORY_DIAGNOSIS.get(hypothesis_kind, frozenset())
        for ref in diagnosis_references:
            if ref.diagnosis_type in contradictory:
                raise EducationalInvariantViolation(
                    "hypothesis cannot contradict supporting diagnosis",
                    invariant="EducationalHypothesis.diagnosis.no_contradiction",
                )
            if ref.diagnosis_type not in compatible:
                raise EducationalInvariantViolation(
                    "hypothesis cannot contradict supporting diagnosis",
                    invariant="EducationalHypothesis.diagnosis.compatible",
                )

    @staticmethod
    def assert_known_evidence(
        known: frozenset[EvidenceId],
        referenced: frozenset[EvidenceId],
    ) -> None:
        if not known:
            return
        unknown = referenced - known
        if unknown:
            raise EducationalInvariantViolation(
                "hypothesis references unknown evidence identities",
                invariant="EducationalHypothesis.evidence.known",
            )

    @staticmethod
    def assert_known_interpretations(
        known: frozenset[str],
        referenced: frozenset[str],
    ) -> None:
        if not known:
            return
        unknown = referenced - known
        if unknown:
            raise EducationalInvariantViolation(
                "hypothesis references unknown interpretation identities",
                invariant="EducationalHypothesis.interpretation.known",
            )

    @staticmethod
    def assert_discard_reason(reason: str) -> str:
        return require_non_empty_text(reason, "discard_reason")

    @staticmethod
    def compatible_diagnosis_types(
        hypothesis_kind: HypothesisKind,
    ) -> frozenset[DiagnosisType]:
        return _COMPATIBLE_DIAGNOSIS.get(hypothesis_kind, frozenset())
