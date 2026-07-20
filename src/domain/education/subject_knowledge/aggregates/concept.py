"""Concept aggregate root — teachable knowledge entity.

Architecture Source
    SUBJECT_KNOWLEDGE_MODEL.md / CONCEPT_ARCHITECTURE.md
Concept
    Concept
"""

from __future__ import annotations

from domain.education.foundation.enums import DependencyKind, RepresentationKind
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    ConceptId,
    LearningObjectiveId,
    MisconceptionId,
)
from domain.education.subject_knowledge.entities.application_context import (
    ApplicationContext,
    ApplicationContextId,
)
from domain.education.subject_knowledge.entities.learning_objective import (
    LearningObjective,
)
from domain.education.subject_knowledge.entities.misconception import Misconception
from domain.education.subject_knowledge.entities.representation import (
    Representation,
    RepresentationId,
)
from domain.education.subject_knowledge.entities.transfer_context import (
    TransferContext,
    TransferContextId,
)
from domain.education.subject_knowledge.events.concept_created import ConceptCreated
from domain.education.subject_knowledge.events.dependency_added import DependencyAdded
from domain.education.subject_knowledge.events.misconception_registered import (
    MisconceptionRegistered,
)
from domain.education.subject_knowledge.policies.concept_validation_policy import (
    ConceptValidationPolicy,
)
from domain.education.subject_knowledge.policies.dependency_policy import (
    DependencyPolicy,
)
from domain.education.subject_knowledge.policies.representation_policy import (
    RepresentationPolicy,
)
from domain.education.subject_knowledge.value_objects.concept_boundary import (
    ConceptBoundary,
)
from domain.education.subject_knowledge.value_objects.dependency import Dependency

DomainEvent = ConceptCreated | MisconceptionRegistered | DependencyAdded


class Concept:
    """Aggregate root for a named, teachable subject-knowledge concept.

    Owns learning objectives, representations, misconceptions, application and
    transfer contexts, and typed dependencies. Behaviour is exposed only through
    methods — no public setters. Educational integrity is enforced via policies
    aligned with SUBJECT_INVARIANTS.md.
    """

    def __init__(
        self,
        concept_id: ConceptId,
        canonical_name: str,
        core_meaning: str,
        boundary: ConceptBoundary,
        learning_objectives: list[LearningObjective],
        *,
        representations: list[Representation] | None = None,
        misconceptions: list[Misconception] | None = None,
        application_contexts: list[ApplicationContext] | None = None,
        transfer_contexts: list[TransferContext] | None = None,
        dependencies: list[Dependency] | None = None,
        _record_created: bool = False,
    ) -> None:
        self._concept_id = ConceptValidationPolicy.assert_identity(concept_id)
        self._canonical_name = ConceptValidationPolicy.assert_canonical_name(
            canonical_name
        )
        self._core_meaning = ConceptValidationPolicy.assert_core_meaning(core_meaning)
        self._boundary = ConceptValidationPolicy.assert_boundary(boundary)

        self._learning_objectives: list[LearningObjective] = []
        self._representations: list[Representation] = []
        self._misconceptions: list[Misconception] = []
        self._application_contexts: list[ApplicationContext] = []
        self._transfer_contexts: list[TransferContext] = []
        self._dependencies: list[Dependency] = []
        self._pending_events: list[DomainEvent] = []

        for objective in learning_objectives:
            ConceptValidationPolicy.assert_objective_belongs(
                self._concept_id, objective
            )
            ConceptValidationPolicy.assert_objective_not_duplicate(
                self._learning_objectives, objective
            )
            self._learning_objectives.append(objective)

        ConceptValidationPolicy.assert_has_learning_objective(
            self._learning_objectives
        )

        for representation in representations or []:
            RepresentationPolicy.assert_can_register(
                self._representations, representation
            )
            if not representation.belongs_to(self._concept_id):
                raise EducationalInvariantViolation(
                    "representation must belong to this concept",
                    invariant="Concept.representation.ownership",
                )
            self._representations.append(representation)

        for misconception in misconceptions or []:
            ConceptValidationPolicy.assert_misconception_belongs(
                self._concept_id, misconception
            )
            ConceptValidationPolicy.assert_misconception_not_duplicate(
                self._misconceptions, misconception
            )
            self._misconceptions.append(misconception)

        for context in application_contexts or []:
            ConceptValidationPolicy.assert_application_context_belongs(
                self._concept_id, context
            )
            ConceptValidationPolicy.assert_application_context_not_duplicate(
                self._application_contexts, context
            )
            self._application_contexts.append(context)

        for context in transfer_contexts or []:
            ConceptValidationPolicy.assert_transfer_context_belongs(
                self._concept_id, context
            )
            ConceptValidationPolicy.assert_transfer_context_not_duplicate(
                self._transfer_contexts, context
            )
            self._transfer_contexts.append(context)

        for dependency in dependencies or []:
            DependencyPolicy.assert_can_add(
                self._concept_id, self._dependencies, dependency
            )
            self._dependencies.append(dependency)

        if _record_created:
            self._pending_events.append(
                ConceptCreated(
                    concept_id=self._concept_id,
                    canonical_name=self._canonical_name,
                    initial_objective_id=self._learning_objectives[0].objective_id,
                )
            )

    @classmethod
    def create(
        cls,
        concept_id: ConceptId,
        canonical_name: str,
        core_meaning: str,
        boundary: ConceptBoundary,
        initial_objective: LearningObjective,
    ) -> Concept:
        """Factory: create a Concept with exactly one initial learning objective.

        Records a ``ConceptCreated`` domain event.
        """
        return cls(
            concept_id=concept_id,
            canonical_name=canonical_name,
            core_meaning=core_meaning,
            boundary=boundary,
            learning_objectives=[initial_objective],
            _record_created=True,
        )

    # --- identity / read models (no setters) ---

    @property
    def concept_id(self) -> ConceptId:
        return self._concept_id

    @property
    def canonical_name(self) -> str:
        return self._canonical_name

    @property
    def core_meaning(self) -> str:
        return self._core_meaning

    @property
    def boundary(self) -> ConceptBoundary:
        return self._boundary

    @property
    def learning_objectives(self) -> tuple[LearningObjective, ...]:
        return tuple(self._learning_objectives)

    @property
    def representations(self) -> tuple[Representation, ...]:
        return tuple(self._representations)

    @property
    def misconceptions(self) -> tuple[Misconception, ...]:
        return tuple(self._misconceptions)

    @property
    def application_contexts(self) -> tuple[ApplicationContext, ...]:
        return tuple(self._application_contexts)

    @property
    def transfer_contexts(self) -> tuple[TransferContext, ...]:
        return tuple(self._transfer_contexts)

    @property
    def dependencies(self) -> tuple[Dependency, ...]:
        return tuple(self._dependencies)

    def pull_events(self) -> list[DomainEvent]:
        """Return and clear pending domain events."""
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    # --- behaviour ---

    def add_learning_objective(self, objective: LearningObjective) -> None:
        """Add a learning objective owned by this concept."""
        ConceptValidationPolicy.assert_objective_belongs(self._concept_id, objective)
        ConceptValidationPolicy.assert_objective_not_duplicate(
            self._learning_objectives, objective
        )
        self._learning_objectives.append(objective)

    def remove_learning_objective(self, objective_id: LearningObjectiveId) -> None:
        """Remove a learning objective; refuses to remove the final one."""
        ConceptValidationPolicy.assert_can_remove_learning_objective(
            self._learning_objectives, objective_id
        )
        self._learning_objectives = [
            obj
            for obj in self._learning_objectives
            if obj.objective_id != objective_id
        ]

    def register_representation(self, representation: Representation) -> None:
        """Register a representation; kinds and identities must be unique."""
        if not representation.belongs_to(self._concept_id):
            raise EducationalInvariantViolation(
                "representation must belong to this concept",
                invariant="Concept.representation.ownership",
            )
        RepresentationPolicy.assert_can_register(
            self._representations, representation
        )
        self._representations.append(representation)

    def register_misconception(self, misconception: Misconception) -> None:
        """Register a misconception attached to this concept (K4)."""
        ConceptValidationPolicy.assert_misconception_belongs(
            self._concept_id, misconception
        )
        ConceptValidationPolicy.assert_misconception_not_duplicate(
            self._misconceptions, misconception
        )
        self._misconceptions.append(misconception)
        self._pending_events.append(
            MisconceptionRegistered(
                concept_id=self._concept_id,
                misconception_id=misconception.misconception_id,
            )
        )

    def add_dependency(self, dependency: Dependency) -> None:
        """Add a typed educational dependency; rejects self and duplicates."""
        DependencyPolicy.assert_can_add(
            self._concept_id, self._dependencies, dependency
        )
        self._dependencies.append(dependency)
        self._pending_events.append(
            DependencyAdded(
                concept_id=self._concept_id,
                target_concept_id=dependency.target_concept_id,
                kind=dependency.kind,
            )
        )

    def remove_dependency(
        self,
        target_concept_id: ConceptId,
        kind: DependencyKind | None = None,
    ) -> None:
        """Remove a dependency matching target (and optional kind)."""
        edge = DependencyPolicy.find_edge(
            self._dependencies, target_concept_id, kind
        )
        if edge is None:
            raise EducationalInvariantViolation(
                "dependency not found on this concept",
                invariant="Concept.dependency.not_found",
            )
        self._dependencies = [
            item
            for item in self._dependencies
            if not (
                item.target_concept_id == target_concept_id
                and (kind is None or item.kind is kind)
            )
        ]

    def add_application_context(self, context: ApplicationContext) -> None:
        """Add a unique application context (K14)."""
        ConceptValidationPolicy.assert_application_context_belongs(
            self._concept_id, context
        )
        ConceptValidationPolicy.assert_application_context_not_duplicate(
            self._application_contexts, context
        )
        self._application_contexts.append(context)

    def add_transfer_context(self, context: TransferContext) -> None:
        """Add a unique transfer context (K15)."""
        ConceptValidationPolicy.assert_transfer_context_belongs(
            self._concept_id, context
        )
        ConceptValidationPolicy.assert_transfer_context_not_duplicate(
            self._transfer_contexts, context
        )
        if context.base_application_context_id is not None:
            known = {
                item.context_id for item in self._application_contexts
            }
            if context.base_application_context_id not in known:
                raise EducationalInvariantViolation(
                    "transfer context base application context must be owned "
                    "by this concept",
                    invariant="Concept.transfer_context.base_owned",
                )
        self._transfer_contexts.append(context)

    # --- queries ---

    def has_learning_objective(self, objective_id: LearningObjectiveId) -> bool:
        return any(
            obj.objective_id == objective_id for obj in self._learning_objectives
        )

    def has_misconception(self, misconception_id: MisconceptionId) -> bool:
        return any(
            item.misconception_id == misconception_id
            for item in self._misconceptions
        )

    def has_representation(self, representation_id: RepresentationId) -> bool:
        return any(
            item.representation_id == representation_id
            for item in self._representations
        )

    def has_representation_kind(self, kind: RepresentationKind) -> bool:
        return any(item.kind is kind for item in self._representations)

    def has_application_context(self, context_id: ApplicationContextId) -> bool:
        return any(
            item.context_id == context_id for item in self._application_contexts
        )

    def has_transfer_context(self, context_id: TransferContextId) -> bool:
        return any(item.context_id == context_id for item in self._transfer_contexts)

    def prerequisites(self) -> tuple[Dependency, ...]:
        """Outgoing required and helpful prerequisite dependencies."""
        return tuple(
            edge
            for edge in self._dependencies
            if DependencyPolicy.is_prerequisite_kind(edge.kind)
        )

    def extensions(self) -> tuple[Dependency, ...]:
        """Outgoing extension dependencies (K16)."""
        return tuple(
            edge
            for edge in self._dependencies
            if DependencyPolicy.is_extension_kind(edge.kind)
        )

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True
        if not isinstance(other, Concept):
            return NotImplemented
        return self._concept_id == other._concept_id

    def __hash__(self) -> int:
        return hash((type(self), self._concept_id))

    def __repr__(self) -> str:
        return (
            f"Concept(concept_id={self._concept_id!r}, "
            f"canonical_name={self._canonical_name!r})"
        )
