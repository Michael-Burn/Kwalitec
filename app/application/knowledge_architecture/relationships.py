"""Educational relationship mapping (KWP-014).

Maps DependencyType ↔ EducationalRelationship without duplicating topic
metadata. Curriculum structure remains authoritative in CurriculumGraph.
"""

from __future__ import annotations

from app.application.knowledge_architecture.dto import EducationalRelationship
from app.domain.curriculum.value_objects.dependency_type import DependencyType

# DependencyType → educational label (student-facing catalogue).
DEPENDENCY_TO_EDUCATIONAL: dict[DependencyType, EducationalRelationship] = {
    DependencyType.REQUIRES: EducationalRelationship.PREREQUISITE,
    DependencyType.FOUNDATION: EducationalRelationship.FOUNDATION,
    DependencyType.EXTENSION: EducationalRelationship.EXTENSION,
    DependencyType.REVISION: EducationalRelationship.FREQUENTLY_REVISED_TOGETHER,
    DependencyType.HIGH_DEPENDENCY: EducationalRelationship.HIGH_DEPENDENCY,
    DependencyType.OPTIONAL: EducationalRelationship.OPTIONAL_REINFORCEMENT,
    DependencyType.RECOMMENDS: EducationalRelationship.OPTIONAL_REINFORCEMENT,
    DependencyType.RELATED: EducationalRelationship.EXTENSION,
}

EDUCATIONAL_TO_DEPENDENCY: dict[EducationalRelationship, DependencyType] = {
    EducationalRelationship.PREREQUISITE: DependencyType.REQUIRES,
    EducationalRelationship.FOUNDATION: DependencyType.FOUNDATION,
    EducationalRelationship.EXTENSION: DependencyType.EXTENSION,
    EducationalRelationship.FREQUENTLY_REVISED_TOGETHER: DependencyType.REVISION,
    EducationalRelationship.HIGH_DEPENDENCY: DependencyType.HIGH_DEPENDENCY,
    EducationalRelationship.OPTIONAL_REINFORCEMENT: DependencyType.OPTIONAL,
}


def educational_for(dependency_type: DependencyType | str) -> EducationalRelationship:
    """Map a graph dependency kind to the educational relationship catalogue."""
    dtype = (
        dependency_type
        if isinstance(dependency_type, DependencyType)
        else DependencyType(dependency_type)
    )
    return DEPENDENCY_TO_EDUCATIONAL.get(
        dtype, EducationalRelationship.EXTENSION
    )


def dependency_for(
    relationship: EducationalRelationship | str,
) -> DependencyType:
    """Map an educational relationship label to DependencyType."""
    rel = (
        relationship
        if isinstance(relationship, EducationalRelationship)
        else EducationalRelationship(relationship)
    )
    return EDUCATIONAL_TO_DEPENDENCY[rel]
