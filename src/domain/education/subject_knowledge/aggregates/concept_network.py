"""Concept network — educational relationships among concepts.

Architecture Source
    CONCEPT_NETWORK_MODEL.md / KNOWLEDGE_DEPENDENCY_MODEL.md
Concept
    Concept Network
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import require_non_empty_text
from domain.education.foundation.enums import DependencyKind
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId
from domain.education.subject_knowledge.policies.dependency_policy import (
    DependencyPolicy,
)
from domain.education.subject_knowledge.value_objects.dependency import Dependency


@dataclass(frozen=True, slots=True)
class NetworkDependency:
    """Directed educational dependency edge within the concept network.

    ``source_concept_id`` is the concept that owns / depends; ``dependency``
    carries the target and kind.
    """

    source_concept_id: ConceptId
    dependency: Dependency

    @property
    def target_concept_id(self) -> ConceptId:
        return self.dependency.target_concept_id

    @property
    def kind(self) -> DependencyKind:
        return self.dependency.kind


class ConceptNetwork:
    """Domain object representing typed educational relationships among concepts.

    Supports registration and queries. Does not run graph algorithms (path
    finding, cycle detection, topological sort) — those are deferred.
    """

    def __init__(self) -> None:
        self._concepts: dict[ConceptId, str] = {}
        self._dependencies: list[NetworkDependency] = []

    @property
    def concept_ids(self) -> frozenset[ConceptId]:
        return frozenset(self._concepts)

    @property
    def registered_concept_count(self) -> int:
        return len(self._concepts)

    @property
    def dependency_count(self) -> int:
        return len(self._dependencies)

    def is_registered(self, concept_id: ConceptId) -> bool:
        return concept_id in self._concepts

    def canonical_name(self, concept_id: ConceptId) -> str:
        """Return the registered canonical name for a concept."""
        if concept_id not in self._concepts:
            raise EducationalInvariantViolation(
                "concept is not registered in the network",
                invariant="ConceptNetwork.concept.not_registered",
            )
        return self._concepts[concept_id]

    def register_concept(self, concept_id: ConceptId, canonical_name: str) -> None:
        """Register a concept node in the network."""
        if not isinstance(concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "concept_id must be a ConceptId",
                invariant="ConceptNetwork.concept_id.type",
            )
        name = require_non_empty_text(canonical_name, "canonical_name")
        if concept_id in self._concepts:
            raise EducationalInvariantViolation(
                "concept is already registered in the network",
                invariant="ConceptNetwork.concept.duplicate",
            )
        self._concepts[concept_id] = name

    def register_dependency(
        self,
        source_concept_id: ConceptId,
        dependency: Dependency,
    ) -> None:
        """Register a typed dependency edge; both endpoints must be registered."""
        if source_concept_id not in self._concepts:
            raise EducationalInvariantViolation(
                "source concept must be registered before adding a dependency",
                invariant="ConceptNetwork.source.not_registered",
            )
        if dependency.target_concept_id not in self._concepts:
            raise EducationalInvariantViolation(
                "target concept must be registered before adding a dependency",
                invariant="ConceptNetwork.target.not_registered",
            )
        DependencyPolicy.assert_can_add(
            source_concept_id,
            tuple(
                edge.dependency
                for edge in self._dependencies
                if edge.source_concept_id == source_concept_id
            ),
            dependency,
        )
        for edge in self._dependencies:
            if (
                edge.source_concept_id == source_concept_id
                and edge.dependency.same_edge(dependency)
            ):
                raise EducationalInvariantViolation(
                    "duplicate network dependency is not allowed",
                    invariant="ConceptNetwork.dependency.duplicate",
                )
        self._dependencies.append(
            NetworkDependency(
                source_concept_id=source_concept_id,
                dependency=dependency,
            )
        )

    def outgoing_dependencies(
        self, concept_id: ConceptId
    ) -> tuple[NetworkDependency, ...]:
        """Dependencies owned by ``concept_id`` (outgoing edges)."""
        self._require_registered(concept_id)
        return tuple(
            edge
            for edge in self._dependencies
            if edge.source_concept_id == concept_id
        )

    def incoming_dependencies(
        self, concept_id: ConceptId
    ) -> tuple[NetworkDependency, ...]:
        """Dependencies that point at ``concept_id`` (incoming edges)."""
        self._require_registered(concept_id)
        return tuple(
            edge
            for edge in self._dependencies
            if edge.target_concept_id == concept_id
        )

    def query_prerequisites(
        self, concept_id: ConceptId
    ) -> tuple[NetworkDependency, ...]:
        """Outgoing required and helpful prerequisite edges for ``concept_id``."""
        return tuple(
            edge
            for edge in self.outgoing_dependencies(concept_id)
            if DependencyPolicy.is_prerequisite_kind(edge.kind)
        )

    def query_extensions(
        self, concept_id: ConceptId
    ) -> tuple[NetworkDependency, ...]:
        """Outgoing extension edges for ``concept_id`` (K16)."""
        return tuple(
            edge
            for edge in self.outgoing_dependencies(concept_id)
            if DependencyPolicy.is_extension_kind(edge.kind)
        )

    def _require_registered(self, concept_id: ConceptId) -> None:
        if concept_id not in self._concepts:
            raise EducationalInvariantViolation(
                "concept is not registered in the network",
                invariant="ConceptNetwork.concept.not_registered",
            )
