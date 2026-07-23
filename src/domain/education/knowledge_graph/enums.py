"""Knowledge Dependency Graph domain enumerations.

Architecture Source
    KNOWLEDGE_DEPENDENCY_MODEL.md
    CONCEPT_NETWORK_MODEL.md
Concept
    Relationship Type / Node Kind / Dependency Strength Band
"""

from __future__ import annotations

from enum import StrEnum


class RelationshipType(StrEnum):
    """Typed educational relationship between two knowledge nodes.

    Not every relationship is a strict prerequisite. ``PREREQUISITE``,
    ``REQUIRES``, ``FOUNDATIONAL``, and ``DERIVED_FROM`` are *structural*
    dependency relations subject to the acyclic invariant. ``SUPPORTS``,
    ``REINFORCES``, ``OPTIONAL``, and ``RELATED`` are *advisory* educational
    annotations that carry no acyclic requirement.
    """

    PREREQUISITE = "prerequisite"
    SUPPORTS = "supports"
    REINFORCES = "reinforces"
    OPTIONAL = "optional"
    RELATED = "related"
    REQUIRES = "requires"
    FOUNDATIONAL = "foundational"
    DERIVED_FROM = "derived_from"


class KnowledgeNodeKind(StrEnum):
    """Educational classification of what a knowledge node represents.

    The graph is independent of courses, subjects, and UI navigation — a
    node kind classifies the *nature* of the knowledge unit, not its
    curriculum placement.
    """

    CONCEPT = "concept"
    COMPETENCY = "competency"
    LEARNING_OBJECTIVE = "learning_objective"
    SKILL = "skill"
    TOPIC = "topic"


class DependencyStrengthBand(StrEnum):
    """Qualitative educational force of a dependency relationship.

    Mirrors the Knowledge Dependency Model's educational-force ladder from
    merely optional to strictly required.
    """

    OPTIONAL = "optional"
    HELPFUL = "helpful"
    IMPORTANT = "important"
    CRITICAL = "critical"
