"""Tests for the ConceptNetwork domain object."""

from __future__ import annotations

import pytest

from domain.education.foundation import EducationalInvariantViolation
from domain.education.foundation.enums import DependencyKind
from domain.education.foundation.ids import ConceptId
from domain.education.subject_knowledge import ConceptNetwork, Dependency
from tests.domain.education.subject_knowledge.conftest import make_dependency


@pytest.fixture
def network() -> ConceptNetwork:
    return ConceptNetwork()


@pytest.fixture
def populated_network() -> ConceptNetwork:
    network = ConceptNetwork()
    network.register_concept(ConceptId("c-pv"), "Present value")
    network.register_concept(ConceptId("c-eq"), "Equivalence principle")
    network.register_concept(ConceptId("c-net"), "Net premium")
    network.register_concept(ConceptId("c-gross"), "Gross premium")
    network.register_dependency(
        ConceptId("c-eq"),
        make_dependency(
            ConceptId("c-pv"),
            kind=DependencyKind.REQUIRED_PREREQUISITE,
            description="PV before equivalence",
        ),
    )
    network.register_dependency(
        ConceptId("c-net"),
        make_dependency(
            ConceptId("c-eq"),
            kind=DependencyKind.REQUIRED_PREREQUISITE,
            description="equivalence before net premium",
        ),
    )
    network.register_dependency(
        ConceptId("c-gross"),
        make_dependency(
            ConceptId("c-net"),
            kind=DependencyKind.EXTENSION,
            description="gross extends net",
        ),
    )
    network.register_dependency(
        ConceptId("c-gross"),
        make_dependency(
            ConceptId("c-eq"),
            kind=DependencyKind.HELPFUL_PREREQUISITE,
            description="equivalence helps gross",
        ),
    )
    return network


class TestConceptRegistration:
    def test_register_concept(self, network: ConceptNetwork) -> None:
        network.register_concept(ConceptId("c1"), "Concept One")
        assert network.is_registered(ConceptId("c1"))
        assert network.canonical_name(ConceptId("c1")) == "Concept One"
        assert network.registered_concept_count == 1

    def test_duplicate_concept_rejected(self, network: ConceptNetwork) -> None:
        network.register_concept(ConceptId("c1"), "Concept One")
        with pytest.raises(EducationalInvariantViolation):
            network.register_concept(ConceptId("c1"), "Again")

    def test_blank_name_rejected(self, network: ConceptNetwork) -> None:
        with pytest.raises(EducationalInvariantViolation):
            network.register_concept(ConceptId("c1"), "  ")

    def test_invalid_id_rejected(self, network: ConceptNetwork) -> None:
        with pytest.raises(EducationalInvariantViolation):
            network.register_concept("c1", "Name")  # type: ignore[arg-type]

    def test_canonical_name_unknown_rejected(
        self, network: ConceptNetwork
    ) -> None:
        with pytest.raises(EducationalInvariantViolation):
            network.canonical_name(ConceptId("missing"))


class TestDependencyRegistration:
    def test_register_dependency(self, network: ConceptNetwork) -> None:
        network.register_concept(ConceptId("c1"), "A")
        network.register_concept(ConceptId("c2"), "B")
        network.register_dependency(
            ConceptId("c1"),
            make_dependency(ConceptId("c2")),
        )
        assert network.dependency_count == 1

    def test_source_must_be_registered(self, network: ConceptNetwork) -> None:
        network.register_concept(ConceptId("c2"), "B")
        with pytest.raises(EducationalInvariantViolation):
            network.register_dependency(
                ConceptId("c1"),
                make_dependency(ConceptId("c2")),
            )

    def test_target_must_be_registered(self, network: ConceptNetwork) -> None:
        network.register_concept(ConceptId("c1"), "A")
        with pytest.raises(EducationalInvariantViolation):
            network.register_dependency(
                ConceptId("c1"),
                make_dependency(ConceptId("c2")),
            )

    def test_self_dependency_rejected(self, network: ConceptNetwork) -> None:
        network.register_concept(ConceptId("c1"), "A")
        with pytest.raises(EducationalInvariantViolation):
            network.register_dependency(
                ConceptId("c1"),
                make_dependency(ConceptId("c1")),
            )

    def test_duplicate_dependency_rejected(self, network: ConceptNetwork) -> None:
        network.register_concept(ConceptId("c1"), "A")
        network.register_concept(ConceptId("c2"), "B")
        dep = make_dependency(ConceptId("c2"))
        network.register_dependency(ConceptId("c1"), dep)
        with pytest.raises(EducationalInvariantViolation):
            network.register_dependency(ConceptId("c1"), dep)

    @pytest.mark.parametrize("kind", list(DependencyKind))
    def test_all_kinds_registerable(
        self, network: ConceptNetwork, kind: DependencyKind
    ) -> None:
        network.register_concept(ConceptId("c1"), "A")
        network.register_concept(ConceptId("c2"), "B")
        network.register_dependency(
            ConceptId("c1"),
            make_dependency(ConceptId("c2"), kind=kind),
        )
        assert network.dependency_count == 1


class TestNetworkQueries:
    def test_outgoing_dependencies(
        self, populated_network: ConceptNetwork
    ) -> None:
        outgoing = populated_network.outgoing_dependencies(ConceptId("c-gross"))
        assert len(outgoing) == 2
        targets = {edge.target_concept_id for edge in outgoing}
        assert targets == {ConceptId("c-net"), ConceptId("c-eq")}

    def test_incoming_dependencies(
        self, populated_network: ConceptNetwork
    ) -> None:
        incoming = populated_network.incoming_dependencies(ConceptId("c-eq"))
        assert len(incoming) == 2
        sources = {edge.source_concept_id for edge in incoming}
        assert sources == {ConceptId("c-net"), ConceptId("c-gross")}

    def test_query_prerequisites(
        self, populated_network: ConceptNetwork
    ) -> None:
        prereqs = populated_network.query_prerequisites(ConceptId("c-gross"))
        assert len(prereqs) == 1
        assert prereqs[0].kind is DependencyKind.HELPFUL_PREREQUISITE

    def test_query_extensions(self, populated_network: ConceptNetwork) -> None:
        extensions = populated_network.query_extensions(ConceptId("c-gross"))
        assert len(extensions) == 1
        assert extensions[0].target_concept_id == ConceptId("c-net")

    def test_query_unregistered_rejected(
        self, populated_network: ConceptNetwork
    ) -> None:
        with pytest.raises(EducationalInvariantViolation):
            populated_network.outgoing_dependencies(ConceptId("missing"))
        with pytest.raises(EducationalInvariantViolation):
            populated_network.incoming_dependencies(ConceptId("missing"))
        with pytest.raises(EducationalInvariantViolation):
            populated_network.query_prerequisites(ConceptId("missing"))
        with pytest.raises(EducationalInvariantViolation):
            populated_network.query_extensions(ConceptId("missing"))

    def test_empty_queries_for_leaf(
        self, populated_network: ConceptNetwork
    ) -> None:
        assert populated_network.outgoing_dependencies(ConceptId("c-pv")) == ()
        assert populated_network.query_prerequisites(ConceptId("c-pv")) == ()
        assert populated_network.query_extensions(ConceptId("c-pv")) == ()

    def test_network_dependency_properties(
        self, populated_network: ConceptNetwork
    ) -> None:
        edge = populated_network.outgoing_dependencies(ConceptId("c-eq"))[0]
        assert edge.kind is DependencyKind.REQUIRED_PREREQUISITE
        assert isinstance(edge.dependency, Dependency)
        assert edge.target_concept_id == ConceptId("c-pv")

    def test_concept_ids_frozenset(
        self, populated_network: ConceptNetwork
    ) -> None:
        ids = populated_network.concept_ids
        assert isinstance(ids, frozenset)
        assert ConceptId("c-pv") in ids
