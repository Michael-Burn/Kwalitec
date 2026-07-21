"""First-run Educational OS session context for the initial pipeline.

Builds diagnosis / priority / strategy / availability prerequisites required by
``EducationalPipeline``. Does **not** generate missions or recommendations —
those remain exclusive Educational Pipeline responsibilities.
"""

from __future__ import annotations

from application.onboarding.results import StudentTwinInitializationRequest
from application.pipeline.pipeline_request import PipelineSessionContext
from application.student_initialization.errors import OnboardingValidationError
from application.student_initialization.ports import PipelineSessionContextFactory
from domain.education.diagnosis import (
    DiagnosisConfidence,
    DiagnosisIndicator,
    DiagnosisIndicatorId,
    DiagnosisReason,
    DiagnosisReasonId,
    DiagnosisScope,
    DiagnosisScopeId,
    DiagnosisSeverity,
    DiagnosisSeverityLevel,
    EducationalDiagnosis,
    EducationalScopeKind,
    IndicatorKind,
    InterpretationReference,
)
from domain.education.digital_twin import EducationalDigitalTwin
from domain.education.evidence import EvidenceRecord
from domain.education.foundation.enums import (
    ConfidenceLevel,
    DiagnosisType,
    LearningDimension,
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.ids import (
    ConceptId,
    DiagnosisId,
    EvidenceId,
    HypothesisId,
    LearningObjectiveId,
    PriorityId,
    TeachingIntentionId,
    TeachingStrategyId,
)
from domain.education.foundation.references import (
    ConceptReference,
    LearningObjectiveReference,
)
from domain.education.priority import (
    DiagnosisReference as PriorityDiagnosisReference,
)
from domain.education.priority import (
    EducationalPriority,
    InstructionalImpact,
    InstructionalImpactLevel,
    PriorityFactor,
    PriorityFactorId,
    PriorityFactorKind,
    PriorityScope,
    PriorityScopeId,
    PriorityScopeKind,
    PriorityScore,
    PriorityScoreBand,
    Urgency,
    UrgencyLevel,
)
from domain.education.priority import (
    HypothesisReference as PriorityHypothesisReference,
)
from domain.education.teaching_strategy import (
    ComplexityLevel,
    EffectivenessLevel,
    InstructionalComplexity,
    IntentionReference,
    StrategyEffectiveness,
    StrategyGoal,
    StrategyGoalId,
    StrategyRationale,
    StrategyRationaleId,
    TeachingStrategy,
)
from domain.education.teaching_strategy import (
    DiagnosisReference as StrategyDiagnosisReference,
)
from domain.education.teaching_strategy import (
    HypothesisReference as StrategyHypothesisReference,
)
from domain.onboarding.enums import ConfidenceBand, CoreReadingDeclaration
from domain.study_planning import LearnerAvailability

_SOFT_CONFIDENCE_BANDS = frozenset(
    {
        ConfidenceBand.LOW.value,
        ConfidenceBand.UNSURE.value,
    }
)


class FirstRunSessionContextFactory(PipelineSessionContextFactory):
    """Deterministic first-run session context from twin + declarations."""

    def build(
        self,
        *,
        twin: EducationalDigitalTwin,
        declarations: StudentTwinInitializationRequest,
        evidence: tuple[EvidenceRecord, ...],
        availability: LearnerAvailability,
    ) -> PipelineSessionContext:
        if twin.student_id != declarations.student_id:
            raise OnboardingValidationError(
                "twin student_id must match onboarding declarations"
            )
        if availability.student_id != declarations.student_id:
            raise OnboardingValidationError(
                "availability student_id must match onboarding declarations"
            )
        if not evidence:
            raise OnboardingValidationError(
                "seeded evidence is required for first-run session context"
            )
        for record in evidence:
            if record.student_id != declarations.student_id:
                raise OnboardingValidationError(
                    "evidence student_id must match onboarding declarations"
                )

        diagnosis_type, intention, strategy_type = self._select_first_run_posture(
            declarations
        )
        onboarding_id = declarations.onboarding_id.strip()
        paper = declarations.exam_paper.strip()
        concept = ConceptId(self._concept_id_for_paper(paper))
        objective = LearningObjectiveId(f"lo-paper-{self._slug(paper)}")
        evidence_ids = tuple(record.evidence_id for record in evidence)
        diagnosis_id = DiagnosisId(f"diag-onboarding-{onboarding_id}")
        interpretation_id = f"interp-onboarding-{onboarding_id}"
        hypothesis_id = HypothesisId(f"hyp-onboarding-{onboarding_id}")

        diagnosis = self._build_diagnosis(
            diagnosis_id=diagnosis_id,
            student_id=declarations.student_id,
            diagnosis_type=diagnosis_type,
            paper=paper,
            concept=concept,
            objective=objective,
            evidence_ids=evidence_ids,
            interpretation_id=interpretation_id,
        )
        priority = self._build_priority(
            priority_id=PriorityId(f"prio-onboarding-{onboarding_id}"),
            student_id=declarations.student_id,
            diagnosis_id=diagnosis_id,
            diagnosis_type=diagnosis_type,
            hypothesis_id=hypothesis_id,
            concept=concept,
            objective=objective,
            paper=paper,
        )
        strategy = self._build_strategy(
            strategy_id=TeachingStrategyId(f"ts-onboarding-{onboarding_id}"),
            student_id=declarations.student_id,
            diagnosis_id=diagnosis_id,
            diagnosis_type=diagnosis_type,
            hypothesis_id=hypothesis_id,
            intention=intention,
            strategy_type=strategy_type,
            paper=paper,
        )
        return PipelineSessionContext(
            twin=twin,
            diagnosis=diagnosis,
            priority=priority,
            strategy=strategy,
            availability=availability,
            trajectory=twin.trajectory,
            completed_missions=(),
            prior_study_plans=(),
        )

    @classmethod
    def _select_first_run_posture(
        cls,
        declarations: StudentTwinInitializationRequest,
    ) -> tuple[DiagnosisType, TeachingIntentionType, TeachingStrategyType]:
        band = (declarations.confidence_band or "").strip().lower()
        reading = (declarations.core_reading or "").strip().lower()
        if band in _SOFT_CONFIDENCE_BANDS:
            return (
                DiagnosisType.LOW_CONFIDENCE,
                TeachingIntentionType.RECOVER_CONFIDENCE,
                TeachingStrategyType.PROGRESSIVE_SCAFFOLDING,
            )
        if reading in {
            CoreReadingDeclaration.NONE.value,
            CoreReadingDeclaration.PARTIAL.value,
        }:
            return (
                DiagnosisType.INCOMPLETE_UNDERSTANDING,
                TeachingIntentionType.COMPLETE_MISSING_FACETS,
                TeachingStrategyType.GUIDED_DISCOVERY,
            )
        return (
            DiagnosisType.PREREQUISITE_GAP,
            TeachingIntentionType.STRENGTHEN_PREREQUISITE,
            TeachingStrategyType.WORKED_EXAMPLE,
        )

    @classmethod
    def _build_diagnosis(
        cls,
        *,
        diagnosis_id: DiagnosisId,
        student_id: str,
        diagnosis_type: DiagnosisType,
        paper: str,
        concept: ConceptId,
        objective: LearningObjectiveId,
        evidence_ids: tuple[EvidenceId, ...],
        interpretation_id: str,
    ) -> EducationalDiagnosis:
        indicator_kind = {
            DiagnosisType.LOW_CONFIDENCE: IndicatorKind.UNDERESTIMATED_CAPACITY,
            DiagnosisType.INCOMPLETE_UNDERSTANDING: IndicatorKind.PARTIAL_FACET_GRASP,
            DiagnosisType.PREREQUISITE_GAP: IndicatorKind.UPSTREAM_CAPABILITY_ABSENCE,
        }[diagnosis_type]
        soft = diagnosis_type is DiagnosisType.LOW_CONFIDENCE
        return EducationalDiagnosis.create(
            diagnosis_id=diagnosis_id,
            student_id=student_id,
            diagnosis_type=diagnosis_type,
            scope=DiagnosisScope(
                scope_id=DiagnosisScopeId(f"scope-{diagnosis_id.value}"),
                statement=(
                    f"Relative to exam paper {paper}, first-run educational "
                    f"starting posture is {diagnosis_type.value}"
                ),
                scope_kind=EducationalScopeKind.LEARNING_OBJECTIVE,
                learning_dimension=LearningDimension.UNDERSTANDING,
                concept_references=(
                    ConceptReference(concept_id=concept, label=paper),
                ),
                learning_objective_references=(
                    LearningObjectiveReference(
                        objective_id=objective,
                        label=f"Begin study of {paper}",
                    ),
                ),
            ),
            confidence=DiagnosisConfidence.of(
                ConfidenceLevel.MEDIUM if soft else ConfidenceLevel.HIGH,
                ratio=0.6 if soft else 0.75,
            ),
            severity=DiagnosisSeverity.of(
                DiagnosisSeverityLevel.MODERATE,
                rationale="first-run educational starting posture from declarations",
            ),
            indicators=[
                DiagnosisIndicator(
                    indicator_id=DiagnosisIndicatorId(
                        f"indicator-{diagnosis_id.value}"
                    ),
                    kind=indicator_kind,
                    description=(
                        "Onboarding self-report warrants the named first-run "
                        f"deficiency category ({diagnosis_type.value})"
                    ),
                    interpretation_references=(
                        InterpretationReference(
                            interpretation_id=interpretation_id
                        ),
                    ),
                    evidence_ids=evidence_ids,
                )
            ],
            reasons=[
                DiagnosisReason(
                    reason_id=DiagnosisReasonId(f"reason-{diagnosis_id.value}"),
                    statement=(
                        f"Warrant for {diagnosis_type.value.replace('_', ' ')} "
                        "from sealed onboarding declarations"
                    ),
                    code="onboarding_declaration",
                )
            ],
            known_evidence_ids=frozenset(evidence_ids),
            known_interpretation_ids=frozenset({interpretation_id}),
        )

    @classmethod
    def _build_priority(
        cls,
        *,
        priority_id: PriorityId,
        student_id: str,
        diagnosis_id: DiagnosisId,
        diagnosis_type: DiagnosisType,
        hypothesis_id: HypothesisId,
        concept: ConceptId,
        objective: LearningObjectiveId,
        paper: str,
    ) -> EducationalPriority:
        return EducationalPriority.assign(
            priority_id=priority_id,
            student_id=student_id,
            scope=PriorityScope(
                scope_id=PriorityScopeId(f"pscope-{priority_id.value}"),
                statement=(
                    f"Order first study for {paper} ahead of later extension"
                ),
                scope_kind=PriorityScopeKind.COMPETING_DIAGNOSES,
                learning_dimension=LearningDimension.UNDERSTANDING,
                concept_references=(
                    ConceptReference(concept_id=concept, label=paper),
                ),
                learning_objective_references=(
                    LearningObjectiveReference(
                        objective_id=objective,
                        label=f"Begin study of {paper}",
                    ),
                ),
            ),
            diagnosis_references=[
                PriorityDiagnosisReference(
                    diagnosis_id=diagnosis_id,
                    diagnosis_type=diagnosis_type,
                )
            ],
            hypothesis_references=[
                PriorityHypothesisReference(hypothesis_id=hypothesis_id)
            ],
            factors=[
                PriorityFactor(
                    factor_id=PriorityFactorId(f"factor-{priority_id.value}"),
                    kind=PriorityFactorKind.PREREQUISITE_IMPORTANCE,
                    contribution=0.85,
                    rationale="First-run study should unlock paper progress",
                )
            ],
            score=PriorityScore.of(
                PriorityScoreBand.HIGH,
                ratio=0.7,
                rationale="first-run instructional ordering",
            ),
            urgency=Urgency.of(
                UrgencyLevel.ELEVATED,
                rationale="material educational pressure at twin birth",
            ),
            instructional_impact=InstructionalImpact.of(
                InstructionalImpactLevel.SUBSTANTIAL,
                "Unlocks dependent objective progress for the declared paper",
            ),
        )

    @classmethod
    def _build_strategy(
        cls,
        *,
        strategy_id: TeachingStrategyId,
        student_id: str,
        diagnosis_id: DiagnosisId,
        diagnosis_type: DiagnosisType,
        hypothesis_id: HypothesisId,
        intention: TeachingIntentionType,
        strategy_type: TeachingStrategyType,
        paper: str,
    ) -> TeachingStrategy:
        strategy = TeachingStrategy.create(
            strategy_id=strategy_id,
            student_id=student_id,
            primary_strategy=strategy_type,
            goal=StrategyGoal(
                goal_id=StrategyGoalId(f"goal-{strategy_id.value}"),
                statement=(
                    f"Pursue {strategy_type.value.replace('_', ' ')} for "
                    f"first study of {paper}"
                ),
                strategy_type=strategy_type,
                expected_evidence_hint="Student engages with first guided study",
            ),
            rationale=StrategyRationale(
                rationale_id=StrategyRationaleId(
                    f"rationale-{strategy_id.value}"
                ),
                statement=(
                    "Selected because first-run diagnosis and intention require "
                    "this instructional approach"
                ),
                diagnosis_link="aligned with onboarding first-run diagnosis",
                intention_link="serves named teaching intention",
            ),
            effectiveness=StrategyEffectiveness.of(
                EffectivenessLevel.MODERATE,
                rationale="expected instructional efficacy for first run",
            ),
            complexity=InstructionalComplexity.of(
                ComplexityLevel.MODERATE,
                rationale="instructional demand estimate for first run",
            ),
            intention_references=[
                IntentionReference(
                    intention_id=TeachingIntentionId(
                        f"ti-onboarding-{strategy_id.value}"
                    ),
                    intention_type=intention,
                )
            ],
            diagnosis_references=[
                StrategyDiagnosisReference(
                    diagnosis_id=diagnosis_id,
                    diagnosis_type=diagnosis_type,
                )
            ],
            hypothesis_references=[
                StrategyHypothesisReference(hypothesis_id=hypothesis_id)
            ],
        )
        strategy.select()
        return strategy

    @staticmethod
    def _concept_id_for_paper(paper: str) -> str:
        return f"concept-paper-{FirstRunSessionContextFactory._slug(paper)}"

    @staticmethod
    def _slug(value: str) -> str:
        cleaned = "".join(
            ch.lower() if ch.isalnum() else "-" for ch in (value or "").strip()
        )
        while "--" in cleaned:
            cleaned = cleaned.replace("--", "-")
        return cleaned.strip("-") or "paper"
