"""Subject Knowledge bounded context — pure educational domain model.

IMP-002 implementation of the Subject Knowledge Architecture.

Pure Domain-Driven Design only: aggregates, entities, value objects, policies,
and lightweight domain events. No persistence, Flask, SQLAlchemy, APIs,
repositories, serialization, or DTOs.
"""

from __future__ import annotations

from domain.education.subject_knowledge.aggregates.concept import Concept
from domain.education.subject_knowledge.aggregates.concept_network import (
    ConceptNetwork,
    NetworkDependency,
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
from domain.education.subject_knowledge.value_objects.mastery_indicator import (
    MasteryIndicator,
)

__all__ = [
    # Aggregates
    "Concept",
    "ConceptNetwork",
    "NetworkDependency",
    # Entities
    "LearningObjective",
    "Misconception",
    "Representation",
    "RepresentationId",
    "ApplicationContext",
    "ApplicationContextId",
    "TransferContext",
    "TransferContextId",
    # Value objects
    "Dependency",
    "ConceptBoundary",
    "MasteryIndicator",
    # Policies
    "DependencyPolicy",
    "ConceptValidationPolicy",
    "RepresentationPolicy",
    # Events
    "ConceptCreated",
    "MisconceptionRegistered",
    "DependencyAdded",
]
