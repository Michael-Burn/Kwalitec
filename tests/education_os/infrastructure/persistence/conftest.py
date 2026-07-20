"""Shared fixtures for INF-001 persistence mapper tests."""

from __future__ import annotations

from domain.education.digital_twin import (
    MasteryBand,
    MasteryState,
    MisconceptionPresence,
)
from domain.education.foundation.enums import (
    EvidenceType,
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.ids import ConceptId, EvidenceId, MisconceptionId
from tests.domain.education.decision.conftest import make_approved_decision
from tests.domain.education.diagnosis.conftest import make_diagnosis
from tests.domain.education.digital_twin.conftest import make_confidence, make_twin
from tests.domain.education.evidence.conftest import make_record
from tests.domain.education.hypothesis.conftest import make_competitor, make_hypothesis
from tests.domain.education.learning_episode.conftest import complete_happy_path
from tests.domain.education.orchestrator.conftest import make_started_orchestrator
from tests.domain.education.priority.conftest import make_constraint, make_priority
from tests.domain.education.teaching_intention.conftest import make_intention
from tests.domain.education.subject_knowledge.conftest import (
    make_application_context,
    make_concept,
    make_dependency,
    make_misconception,
    make_representation,
    make_transfer_context,
)
from tests.domain.education.teaching_strategy.conftest import (
    CANONICAL_SECONDARIES,
    CompositionPattern,
    make_secondary,
    make_strategy,
)


def build_concept():
    concept = make_concept()
    concept.register_representation(make_representation(concept.concept_id))
    concept.register_misconception(make_misconception(concept.concept_id))
    concept.add_application_context(make_application_context(concept.concept_id))
    app = concept.application_contexts[0]
    concept.add_transfer_context(
        make_transfer_context(
            concept.concept_id,
            base=app.context_id,
        )
    )
    concept.add_dependency(make_dependency(ConceptId("concept-present-value")))
    concept.pull_events()
    return concept


def build_digital_twin():
    twin = make_twin(confidence=make_confidence())
    twin.record_evidence(
        EvidenceId("evidence-001"),
        EvidenceType.PERFORMANCE,
        concept_id=ConceptId("concept-001"),
        note="probe",
    )
    twin.record_intervention(
        "intervention-001",
        strategy_type=TeachingStrategyType.WORKED_EXAMPLE,
        intention_type=TeachingIntentionType.STRENGTHEN_PREREQUISITE,
        concept_id=ConceptId("concept-001"),
    )
    twin.update_mastery(
        ConceptId("concept-001"),
        MasteryState.of(MasteryBand.DEVELOPING, ratio=0.55),
    )
    twin.record_misconception_state(
        MisconceptionId("misc-001"),
        MisconceptionPresence.ACTIVE,
        related_concept_id=ConceptId("concept-001"),
    )
    twin.pull_events()
    return twin


def build_learning_episode():
    episode = complete_happy_path()
    episode.pull_events()
    return episode


def build_evidence():
    record = make_record()
    record.pull_events()
    return record


def build_diagnosis():
    diagnosis = make_diagnosis()
    diagnosis.pull_events()
    return diagnosis


def build_hypothesis():
    hypothesis = make_hypothesis(competing_hypotheses=[make_competitor()])
    hypothesis.pull_events()
    return hypothesis


def build_priority():
    priority = make_priority(constraints=[make_constraint()])
    priority.pull_events()
    return priority


def build_intention():
    intention = make_intention(activate=True)
    intention.pull_events()
    return intention


def build_strategy():
    pattern = CompositionPattern.MODELLING_TO_INDEPENDENCE
    secondaries = [
        make_secondary(strategy_type, index + 1)
        for index, strategy_type in enumerate(CANONICAL_SECONDARIES[pattern])
    ]
    strategy = make_strategy(
        composition_pattern=pattern,
        secondary_strategies=secondaries,
        select=True,
    )
    strategy.pull_events()
    return strategy


def build_decision():
    decision = make_approved_decision()
    decision.pull_events()
    return decision


def build_orchestrator():
    orch = make_started_orchestrator()
    orch.pull_events()
    return orch
