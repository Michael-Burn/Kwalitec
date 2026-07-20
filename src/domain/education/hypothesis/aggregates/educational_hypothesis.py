"""EducationalHypothesis aggregate root — revisable educational explanation.

Architecture Source
    EDUCATIONAL_HYPOTHESIS_MODEL.md
Concept
    Educational Hypothesis
"""

from __future__ import annotations

from domain.education.foundation.base import require_non_empty_text
from domain.education.foundation.enums import DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DiagnosisId, EvidenceId, HypothesisId
from domain.education.hypothesis.entities.competing_hypothesis import (
    CompetingHypothesis,
)
from domain.education.hypothesis.entities.hypothesis_reason import (
    DiagnosisReference,
    HypothesisReason,
    InterpretationReference,
)
from domain.education.hypothesis.entities.hypothesis_scope import HypothesisScope
from domain.education.hypothesis.enums import (
    HypothesisKind,
    HypothesisStatus,
    PlausibilityLevel,
    RevisionForm,
)
from domain.education.hypothesis.events.hypothesis_created import HypothesisCreated
from domain.education.hypothesis.events.hypothesis_discarded import HypothesisDiscarded
from domain.education.hypothesis.events.hypothesis_revised import HypothesisRevised
from domain.education.hypothesis.policies.hypothesis_revision_policy import (
    HypothesisRevisionPolicy,
)
from domain.education.hypothesis.policies.hypothesis_validation_policy import (
    HypothesisValidationPolicy,
)
from domain.education.hypothesis.value_objects.explanatory_strength import (
    ExplanatoryStrength,
)
from domain.education.hypothesis.value_objects.plausibility import Plausibility

DomainEvent = HypothesisCreated | HypothesisRevised | HypothesisDiscarded


class EducationalHypothesis:
    """Aggregate root for educational hypothesis.

    Owns diagnosis references, interpretation references, evidence references,
    explanation, plausibility, explanatory strength, supporting reasons, and
    competing hypotheses. Behaviour is exposed only through methods — no
    public setters.

    This aggregate produces revisable educational explanations of *why* a
    diagnosed difficulty exists. It does not diagnose, prioritise, select
    teaching strategies, or generate teaching intentions.
    """

    def __init__(
        self,
        hypothesis_id: HypothesisId,
        student_id: str,
        hypothesis_kind: HypothesisKind,
        explanation: str,
        scope: HypothesisScope,
        plausibility: Plausibility,
        explanatory_strength: ExplanatoryStrength,
        diagnosis_references: list[DiagnosisReference]
        | tuple[DiagnosisReference, ...],
        reasons: list[HypothesisReason] | tuple[HypothesisReason, ...],
        *,
        interpretation_references: list[InterpretationReference]
        | tuple[InterpretationReference, ...]
        | None = None,
        evidence_ids: list[EvidenceId] | tuple[EvidenceId, ...] | None = None,
        competing_hypotheses: list[CompetingHypothesis]
        | tuple[CompetingHypothesis, ...]
        | None = None,
        known_evidence_ids: frozenset[EvidenceId]
        | set[EvidenceId]
        | tuple[EvidenceId, ...]
        | None = None,
        known_interpretation_ids: frozenset[str]
        | set[str]
        | tuple[str, ...]
        | None = None,
        status: HypothesisStatus = HypothesisStatus.ACTIVE,
        discard_reason: str | None = None,
        _record_created: bool = False,
    ) -> None:
        self._hypothesis_id = HypothesisValidationPolicy.assert_identity(
            hypothesis_id
        )
        self._student_id = HypothesisValidationPolicy.assert_student_id(student_id)
        self._hypothesis_kind = HypothesisValidationPolicy.assert_hypothesis_kind(
            hypothesis_kind
        )
        self._explanation = HypothesisValidationPolicy.assert_explanation(explanation)
        self._scope = HypothesisValidationPolicy.assert_scope(scope)
        self._plausibility = HypothesisValidationPolicy.assert_plausibility(
            plausibility
        )
        self._explanatory_strength = (
            HypothesisValidationPolicy.assert_explanatory_strength(
                explanatory_strength
            )
        )
        self._diagnosis_references = list(
            HypothesisValidationPolicy.assert_diagnosis_references(
                diagnosis_references
            )
        )
        self._reasons = list(HypothesisValidationPolicy.assert_reasons(reasons))
        self._interpretation_references = list(
            HypothesisValidationPolicy.assert_interpretation_references(
                interpretation_references or ()
            )
        )
        self._evidence_ids = list(
            HypothesisValidationPolicy.assert_evidence_ids(evidence_ids or ())
        )
        self._competing_hypotheses = list(
            HypothesisValidationPolicy.assert_competing_hypotheses(
                competing_hypotheses or (),
                primary_kind=self._hypothesis_kind,
                primary_explanation=self._explanation,
            )
        )
        self._status = HypothesisValidationPolicy.assert_status(status)
        self._discard_reason = (
            require_non_empty_text(discard_reason, "discard_reason")
            if discard_reason is not None
            else None
        )

        HypothesisValidationPolicy.assert_compatible_with_diagnosis(
            self._hypothesis_kind,
            self._diagnosis_references,
        )

        self._known_evidence_ids: frozenset[EvidenceId] = frozenset(
            known_evidence_ids or ()
        )
        self._known_interpretation_ids: frozenset[str] = frozenset(
            known_interpretation_ids or ()
        )
        referenced_evidence = self._collect_evidence_ids()
        referenced_interpretations = frozenset(
            ref.interpretation_id for ref in self._interpretation_references
        )
        HypothesisValidationPolicy.assert_known_evidence(
            self._known_evidence_ids, referenced_evidence
        )
        HypothesisValidationPolicy.assert_known_interpretations(
            self._known_interpretation_ids, referenced_interpretations
        )

        self._pending_events: list[DomainEvent] = []
        if _record_created:
            self._pending_events.append(
                HypothesisCreated(
                    hypothesis_id=self._hypothesis_id,
                    student_id=self._student_id,
                    hypothesis_kind=self._hypothesis_kind,
                    plausibility_level=self._plausibility.level,
                    explanatory_strength_level=self._explanatory_strength.level,
                    diagnosis_count=len(self._diagnosis_references),
                    reason_count=len(self._reasons),
                )
            )

    @classmethod
    def propose(
        cls,
        hypothesis_id: HypothesisId,
        student_id: str,
        hypothesis_kind: HypothesisKind,
        explanation: str,
        scope: HypothesisScope,
        plausibility: Plausibility,
        explanatory_strength: ExplanatoryStrength,
        diagnosis_references: list[DiagnosisReference]
        | tuple[DiagnosisReference, ...],
        reasons: list[HypothesisReason] | tuple[HypothesisReason, ...],
        *,
        interpretation_references: list[InterpretationReference]
        | tuple[InterpretationReference, ...]
        | None = None,
        evidence_ids: list[EvidenceId] | tuple[EvidenceId, ...] | None = None,
        competing_hypotheses: list[CompetingHypothesis]
        | tuple[CompetingHypothesis, ...]
        | None = None,
        known_evidence_ids: frozenset[EvidenceId]
        | set[EvidenceId]
        | tuple[EvidenceId, ...]
        | None = None,
        known_interpretation_ids: frozenset[str]
        | set[str]
        | tuple[str, ...]
        | None = None,
    ) -> EducationalHypothesis:
        """Factory: propose a revisable educational explanation for a diagnosis."""
        return cls(
            hypothesis_id=hypothesis_id,
            student_id=student_id,
            hypothesis_kind=hypothesis_kind,
            explanation=explanation,
            scope=scope,
            plausibility=plausibility,
            explanatory_strength=explanatory_strength,
            diagnosis_references=diagnosis_references,
            reasons=reasons,
            interpretation_references=interpretation_references,
            evidence_ids=evidence_ids,
            competing_hypotheses=competing_hypotheses,
            known_evidence_ids=known_evidence_ids,
            known_interpretation_ids=known_interpretation_ids,
            status=HypothesisStatus.ACTIVE,
            _record_created=True,
        )

    # --- identity / read models (no setters) ---

    @property
    def hypothesis_id(self) -> HypothesisId:
        return self._hypothesis_id

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def hypothesis_kind(self) -> HypothesisKind:
        return self._hypothesis_kind

    @property
    def explanation(self) -> str:
        return self._explanation

    @property
    def scope(self) -> HypothesisScope:
        return self._scope

    @property
    def plausibility(self) -> Plausibility:
        return self._plausibility

    @property
    def explanatory_strength(self) -> ExplanatoryStrength:
        return self._explanatory_strength

    @property
    def diagnosis_references(self) -> tuple[DiagnosisReference, ...]:
        return tuple(self._diagnosis_references)

    @property
    def reasons(self) -> tuple[HypothesisReason, ...]:
        return tuple(self._reasons)

    @property
    def interpretation_references(self) -> tuple[InterpretationReference, ...]:
        return tuple(self._interpretation_references)

    @property
    def evidence_ids(self) -> tuple[EvidenceId, ...]:
        return tuple(self._evidence_ids)

    @property
    def competing_hypotheses(self) -> tuple[CompetingHypothesis, ...]:
        return tuple(self._competing_hypotheses)

    @property
    def known_evidence_ids(self) -> frozenset[EvidenceId]:
        return self._known_evidence_ids

    @property
    def known_interpretation_ids(self) -> frozenset[str]:
        return self._known_interpretation_ids

    @property
    def status(self) -> HypothesisStatus:
        return self._status

    @property
    def discard_reason(self) -> str | None:
        return self._discard_reason

    def pull_events(self) -> list[DomainEvent]:
        """Return and clear pending domain events."""
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    # --- behaviour ---

    def revise(
        self,
        *,
        hypothesis_kind: HypothesisKind | None = None,
        explanation: str | None = None,
        scope: HypothesisScope | None = None,
        plausibility: Plausibility | None = None,
        explanatory_strength: ExplanatoryStrength | None = None,
        diagnosis_references: list[DiagnosisReference]
        | tuple[DiagnosisReference, ...]
        | None = None,
        reasons: list[HypothesisReason] | tuple[HypothesisReason, ...] | None = None,
        interpretation_references: list[InterpretationReference]
        | tuple[InterpretationReference, ...]
        | None = None,
        evidence_ids: list[EvidenceId] | tuple[EvidenceId, ...] | None = None,
        competing_hypotheses: list[CompetingHypothesis]
        | tuple[CompetingHypothesis, ...]
        | None = None,
        revision_form: RevisionForm | None = None,
    ) -> None:
        """Revise explanatory detail without selecting strategy or intention."""
        HypothesisRevisionPolicy.assert_revisable(self._status, action="revise")
        form = HypothesisRevisionPolicy.assert_revision_form(revision_form)

        next_kind = (
            HypothesisValidationPolicy.assert_hypothesis_kind(hypothesis_kind)
            if hypothesis_kind is not None
            else self._hypothesis_kind
        )
        next_explanation = (
            HypothesisValidationPolicy.assert_explanation(explanation)
            if explanation is not None
            else self._explanation
        )
        next_scope = (
            HypothesisValidationPolicy.assert_scope(scope)
            if scope is not None
            else self._scope
        )
        next_plausibility = (
            HypothesisValidationPolicy.assert_plausibility(plausibility)
            if plausibility is not None
            else self._plausibility
        )
        next_strength = (
            HypothesisValidationPolicy.assert_explanatory_strength(
                explanatory_strength
            )
            if explanatory_strength is not None
            else self._explanatory_strength
        )
        next_diagnoses = (
            list(
                HypothesisValidationPolicy.assert_diagnosis_references(
                    diagnosis_references
                )
            )
            if diagnosis_references is not None
            else list(self._diagnosis_references)
        )
        next_reasons = (
            list(HypothesisValidationPolicy.assert_reasons(reasons))
            if reasons is not None
            else list(self._reasons)
        )
        next_interpretations = (
            list(
                HypothesisValidationPolicy.assert_interpretation_references(
                    interpretation_references
                )
            )
            if interpretation_references is not None
            else list(self._interpretation_references)
        )
        next_evidence = (
            list(HypothesisValidationPolicy.assert_evidence_ids(evidence_ids))
            if evidence_ids is not None
            else list(self._evidence_ids)
        )
        next_competitors = (
            list(
                HypothesisValidationPolicy.assert_competing_hypotheses(
                    competing_hypotheses,
                    primary_kind=next_kind,
                    primary_explanation=next_explanation,
                )
            )
            if competing_hypotheses is not None
            else list(
                HypothesisValidationPolicy.assert_competing_hypotheses(
                    self._competing_hypotheses,
                    primary_kind=next_kind,
                    primary_explanation=next_explanation,
                )
            )
        )

        HypothesisValidationPolicy.assert_compatible_with_diagnosis(
            next_kind, next_diagnoses
        )

        referenced_evidence = frozenset(next_evidence)
        for reason in next_reasons:
            referenced_evidence |= frozenset(reason.evidence_ids)
        referenced_interpretations = frozenset(
            ref.interpretation_id for ref in next_interpretations
        )
        HypothesisValidationPolicy.assert_known_evidence(
            self._known_evidence_ids, referenced_evidence
        )
        HypothesisValidationPolicy.assert_known_interpretations(
            self._known_interpretation_ids, referenced_interpretations
        )

        self._hypothesis_kind = next_kind
        self._explanation = next_explanation
        self._scope = next_scope
        self._plausibility = next_plausibility
        self._explanatory_strength = next_strength
        self._diagnosis_references = next_diagnoses
        self._reasons = next_reasons
        self._interpretation_references = next_interpretations
        self._evidence_ids = next_evidence
        self._competing_hypotheses = next_competitors
        self._status = HypothesisRevisionPolicy.next_status_after_revision(
            self._status,
            suspend=next_plausibility.level is PlausibilityLevel.SUSPENDED,
        )
        self._pending_events.append(
            HypothesisRevised(
                hypothesis_id=self._hypothesis_id,
                student_id=self._student_id,
                hypothesis_kind=self._hypothesis_kind,
                plausibility_level=self._plausibility.level,
                explanatory_strength_level=self._explanatory_strength.level,
                revision_form=form,
            )
        )

    def strengthen(self) -> None:
        """Increase explanatory strength (and ordered plausibility when possible)."""
        HypothesisRevisionPolicy.assert_can_strengthen(self._status)
        HypothesisRevisionPolicy.assert_plausibility_allows_strength_change(
            self._plausibility, action="strengthen"
        )
        self._explanatory_strength = self._explanatory_strength.strengthened()
        try:
            self._plausibility = self._plausibility.strengthened()
        except EducationalInvariantViolation:
            # Strength can rise while plausibility is already at maximum.
            pass
        self._status = HypothesisStatus.REVISED
        self._pending_events.append(
            HypothesisRevised(
                hypothesis_id=self._hypothesis_id,
                student_id=self._student_id,
                hypothesis_kind=self._hypothesis_kind,
                plausibility_level=self._plausibility.level,
                explanatory_strength_level=self._explanatory_strength.level,
                revision_form=RevisionForm.BROADENING,
            )
        )

    def weaken(self) -> None:
        """Decrease explanatory strength (and ordered plausibility when possible)."""
        HypothesisRevisionPolicy.assert_can_weaken(self._status)
        HypothesisRevisionPolicy.assert_plausibility_allows_strength_change(
            self._plausibility, action="weaken"
        )
        self._explanatory_strength = self._explanatory_strength.weakened()
        try:
            self._plausibility = self._plausibility.weakened()
        except EducationalInvariantViolation:
            pass
        self._status = HypothesisStatus.REVISED
        self._pending_events.append(
            HypothesisRevised(
                hypothesis_id=self._hypothesis_id,
                student_id=self._student_id,
                hypothesis_kind=self._hypothesis_kind,
                plausibility_level=self._plausibility.level,
                explanatory_strength_level=self._explanatory_strength.level,
                revision_form=RevisionForm.NARROWING,
            )
        )

    def discard(self, reason: str) -> None:
        """Retire explanatory trust in this hypothesis (compensating posture)."""
        HypothesisRevisionPolicy.assert_can_discard(self._status)
        self._discard_reason = HypothesisValidationPolicy.assert_discard_reason(
            reason
        )
        self._status = HypothesisStatus.DISCARDED
        self._pending_events.append(
            HypothesisDiscarded(
                hypothesis_id=self._hypothesis_id,
                student_id=self._student_id,
                hypothesis_kind=self._hypothesis_kind,
                reason=self._discard_reason,
            )
        )

    def add_competing_hypothesis(self, competitor: CompetingHypothesis) -> None:
        """Register an educationally distinct competing explanation."""
        HypothesisRevisionPolicy.assert_revisable(
            self._status, action="add_competing_hypothesis"
        )
        next_competitors = list(self._competing_hypotheses) + [competitor]
        self._competing_hypotheses = list(
            HypothesisValidationPolicy.assert_competing_hypotheses(
                next_competitors,
                primary_kind=self._hypothesis_kind,
                primary_explanation=self._explanation,
            )
        )
        self._status = HypothesisStatus.REVISED

    # --- queries ---

    def is_active(self) -> bool:
        return self._status is HypothesisStatus.ACTIVE

    def is_revised(self) -> bool:
        return self._status is HypothesisStatus.REVISED

    def is_suspended(self) -> bool:
        return self._status is HypothesisStatus.SUSPENDED

    def is_discarded(self) -> bool:
        return self._status is HypothesisStatus.DISCARDED

    def primary_diagnosis_id(self) -> DiagnosisId:
        return self._diagnosis_references[0].diagnosis_id

    def primary_diagnosis_type(self) -> DiagnosisType:
        return self._diagnosis_references[0].diagnosis_type

    def supporting_diagnosis_ids(self) -> frozenset[DiagnosisId]:
        return frozenset(ref.diagnosis_id for ref in self._diagnosis_references)

    def supporting_interpretation_ids(self) -> frozenset[str]:
        return frozenset(
            ref.interpretation_id for ref in self._interpretation_references
        )

    def supporting_evidence_ids(self) -> frozenset[EvidenceId]:
        return self._collect_evidence_ids()

    def has_diagnosis(self, diagnosis_id: DiagnosisId) -> bool:
        return diagnosis_id in self.supporting_diagnosis_ids()

    def has_interpretation(self, interpretation_id: str) -> bool:
        return interpretation_id in self.supporting_interpretation_ids()

    def has_evidence(self, evidence_id: EvidenceId) -> bool:
        return evidence_id in self.supporting_evidence_ids()

    def reason_count(self) -> int:
        return len(self._reasons)

    def competitor_count(self) -> int:
        return len(self._competing_hypotheses)

    def _collect_evidence_ids(self) -> frozenset[EvidenceId]:
        ids: set[EvidenceId] = set(self._evidence_ids)
        for reason in self._reasons:
            ids.update(reason.evidence_ids)
        return frozenset(ids)

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True
        if not isinstance(other, EducationalHypothesis):
            return NotImplemented
        return self._hypothesis_id == other._hypothesis_id

    def __hash__(self) -> int:
        return hash((type(self), self._hypothesis_id))

    def __repr__(self) -> str:
        return (
            f"EducationalHypothesis(hypothesis_id={self._hypothesis_id!r}, "
            f"kind={self._hypothesis_kind!r}, status={self._status!r})"
        )
