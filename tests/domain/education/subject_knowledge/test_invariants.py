"""Exhaustive invariant coverage for Subject Knowledge educational law."""

from __future__ import annotations

import pytest

from domain.education.foundation import EducationalInvariantViolation
from domain.education.foundation.enums import (
    DependencyKind,
    RepresentationKind,
    TransferLevel,
)
from domain.education.foundation.ids import ConceptId
from domain.education.subject_knowledge import (
    ApplicationContextId,
    Concept,
    ConceptBoundary,
    ConceptNetwork,
    Dependency,
    RepresentationId,
    TransferContextId,
)
from tests.domain.education.subject_knowledge.conftest import (
    make_application_context,
    make_concept,
    make_dependency,
    make_misconception,
    make_objective,
    make_representation,
    make_transfer_context,
)


@pytest.mark.parametrize(
    "name",
    [
        "Force of mortality",
        "Present value",
        "Equivalence principle",
        "Net premium",
        "Select mortality",
    ],
)
def test_concept_accepts_canonical_names(name: str) -> None:
    concept = make_concept(ConceptId(f"c-{name.lower().replace(' ', '-')}"), name=name)
    assert concept.canonical_name == name


@pytest.mark.parametrize("blank", ["", " ", "\t", "\n"])
def test_concept_rejects_blank_core_meaning(blank: str) -> None:
    concept_id = ConceptId("c1")
    with pytest.raises(EducationalInvariantViolation):
        Concept(
            concept_id=concept_id,
            canonical_name="Name",
            core_meaning=blank,
            boundary=ConceptBoundary(inclusion="in", exclusion="out"),
            learning_objectives=[make_objective(concept_id)],
        )


@pytest.mark.parametrize(
    "kind",
    [
        DependencyKind.REQUIRED_PREREQUISITE,
        DependencyKind.HELPFUL_PREREQUISITE,
        DependencyKind.PARALLEL,
        DependencyKind.EXTENSION,
        DependencyKind.REMEDIATION,
    ],
)
def test_concept_self_dependency_rejected_for_every_kind(kind: DependencyKind) -> None:
    concept = make_concept(ConceptId("c-self"))
    with pytest.raises(EducationalInvariantViolation):
        concept.add_dependency(
            Dependency(
                target_concept_id=ConceptId("c-self"),
                kind=kind,
                description="illegal",
            )
        )


@pytest.mark.parametrize(
    "kind",
    list(RepresentationKind),
)
def test_representation_kind_uniqueness_per_kind(kind: RepresentationKind) -> None:
    concept = make_concept(ConceptId("c-rep"))
    concept.register_representation(
        make_representation(
            ConceptId("c-rep"),
            representation_id=f"rep-a-{kind.value}",
            kind=kind,
        )
    )
    with pytest.raises(EducationalInvariantViolation):
        concept.register_representation(
            make_representation(
                ConceptId("c-rep"),
                representation_id=f"rep-b-{kind.value}",
                kind=kind,
            )
        )


@pytest.mark.parametrize("suffix", [str(i) for i in range(12)])
def test_duplicate_misconception_ids_rejected(suffix: str) -> None:
    concept = make_concept(ConceptId("c-misc"))
    misc_id = f"misc-{suffix}"
    concept.register_misconception(
        make_misconception(ConceptId("c-misc"), misconception_id=misc_id)
    )
    with pytest.raises(EducationalInvariantViolation):
        concept.register_misconception(
            make_misconception(ConceptId("c-misc"), misconception_id=misc_id)
        )


@pytest.mark.parametrize("suffix", [str(i) for i in range(12)])
def test_duplicate_application_context_ids_rejected(suffix: str) -> None:
    concept = make_concept(ConceptId("c-app"))
    context_id = f"app-{suffix}"
    concept.add_application_context(
        make_application_context(ConceptId("c-app"), context_id=context_id)
    )
    with pytest.raises(EducationalInvariantViolation):
        concept.add_application_context(
            make_application_context(ConceptId("c-app"), context_id=context_id)
        )


@pytest.mark.parametrize("suffix", [str(i) for i in range(12)])
def test_duplicate_transfer_context_ids_rejected(suffix: str) -> None:
    concept = make_concept(ConceptId("c-xfer"))
    context_id = f"xfer-{suffix}"
    concept.add_transfer_context(
        make_transfer_context(ConceptId("c-xfer"), context_id=context_id)
    )
    with pytest.raises(EducationalInvariantViolation):
        concept.add_transfer_context(
            make_transfer_context(ConceptId("c-xfer"), context_id=context_id)
        )


@pytest.mark.parametrize("suffix", [str(i) for i in range(10)])
def test_duplicate_dependency_edges_rejected(suffix: str) -> None:
    owner = ConceptId("c-dep-owner")
    target = ConceptId(f"c-dep-target-{suffix}")
    concept = make_concept(owner)
    concept.add_dependency(make_dependency(target))
    with pytest.raises(EducationalInvariantViolation):
        concept.add_dependency(make_dependency(target))


@pytest.mark.parametrize("level", [TransferLevel.NEAR, TransferLevel.FAR])
@pytest.mark.parametrize("suffix", [str(i) for i in range(5)])
def test_transfer_levels_near_far_accepted(level: TransferLevel, suffix: str) -> None:
    concept = make_concept(ConceptId("c-level"))
    concept.add_transfer_context(
        make_transfer_context(
            ConceptId("c-level"),
            context_id=f"xfer-{level.value}-{suffix}",
            level=level,
        )
    )
    assert len(concept.transfer_contexts) == 1


@pytest.mark.parametrize(
    "raw_id",
    ["rep-1", "rep_2", "REP-3", "r" * 40],
)
def test_representation_id_tokens(raw_id: str) -> None:
    assert RepresentationId(raw_id).value == raw_id


@pytest.mark.parametrize(
    "raw_id",
    ["app-1", "app_2", "APP-3", "a" * 40],
)
def test_application_context_id_tokens(raw_id: str) -> None:
    assert ApplicationContextId(raw_id).value == raw_id


@pytest.mark.parametrize(
    "raw_id",
    ["xfer-1", "xfer_2", "XFER-3", "t" * 40],
)
def test_transfer_context_id_tokens(raw_id: str) -> None:
    assert TransferContextId(raw_id).value == raw_id


@pytest.mark.parametrize(
    "raw_id",
    ["bad id", "has space", "tab\tid"],
)
def test_local_ids_reject_whitespace(raw_id: str) -> None:
    with pytest.raises(EducationalInvariantViolation):
        RepresentationId(raw_id)
    with pytest.raises(EducationalInvariantViolation):
        ApplicationContextId(raw_id)
    with pytest.raises(EducationalInvariantViolation):
        TransferContextId(raw_id)


@pytest.mark.parametrize(
    ("source", "target", "kind"),
    [
        ("a", "b", DependencyKind.REQUIRED_PREREQUISITE),
        ("b", "a", DependencyKind.HELPFUL_PREREQUISITE),
        ("a", "c", DependencyKind.PARALLEL),
        ("c", "a", DependencyKind.EXTENSION),
        ("b", "c", DependencyKind.REMEDIATION),
    ],
)
def test_network_registers_typed_edges(
    source: str, target: str, kind: DependencyKind
) -> None:
    network = ConceptNetwork()
    for cid in {source, target}:
        if not network.is_registered(ConceptId(cid)):
            network.register_concept(ConceptId(cid), cid.upper())
    network.register_dependency(
        ConceptId(source),
        make_dependency(ConceptId(target), kind=kind),
    )
    outgoing = network.outgoing_dependencies(ConceptId(source))
    assert any(edge.kind is kind for edge in outgoing)


@pytest.mark.parametrize("node", ["a", "b", "c", "d", "e"])
def test_network_incoming_outgoing_symmetry_empty(node: str) -> None:
    network = ConceptNetwork()
    network.register_concept(ConceptId(node), node)
    assert network.outgoing_dependencies(ConceptId(node)) == ()
    assert network.incoming_dependencies(ConceptId(node)) == ()


@pytest.mark.parametrize("count", list(range(1, 8)))
def test_concept_can_hold_multiple_objectives(count: int) -> None:
    concept_id = ConceptId("c-multi-lo")
    concept = make_concept(concept_id, objective_id="lo-0")
    for i in range(1, count):
        concept.add_learning_objective(
            make_objective(concept_id, objective_id=f"lo-{i}")
        )
    assert len(concept.learning_objectives) == count


@pytest.mark.parametrize(
    "kinds",
    [
        (RepresentationKind.SYMBOLIC, RepresentationKind.VERBAL),
        (RepresentationKind.GRAPHICAL, RepresentationKind.TABULAR),
        (RepresentationKind.TIMELINE, RepresentationKind.ANALOGY),
        (
            RepresentationKind.WORKED_EXAMPLE,
            RepresentationKind.COUNTEREXAMPLE,
            RepresentationKind.SIMULATION,
        ),
    ],
)
def test_distinct_representation_kinds_coexist(
    kinds: tuple[RepresentationKind, ...]
) -> None:
    concept = make_concept(ConceptId("c-kinds"))
    for index, kind in enumerate(kinds):
        concept.register_representation(
            make_representation(
                ConceptId("c-kinds"),
                representation_id=f"rep-{index}",
                kind=kind,
            )
        )
    assert len(concept.representations) == len(kinds)


def test_remove_final_objective_after_adding_and_removing_others() -> None:
    concept_id = ConceptId("c-final")
    concept = make_concept(concept_id, objective_id="lo-keep")
    concept.add_learning_objective(make_objective(concept_id, objective_id="lo-temp"))
    concept.remove_learning_objective(
        make_objective(concept_id, objective_id="lo-temp").objective_id
    )
    with pytest.raises(EducationalInvariantViolation):
        concept.remove_learning_objective(
            make_objective(concept_id, objective_id="lo-keep").objective_id
        )
