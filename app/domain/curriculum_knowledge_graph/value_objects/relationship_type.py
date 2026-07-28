"""Typed educational relationships in the Curriculum Knowledge Graph."""

from __future__ import annotations

from enum import StrEnum


class CkgRelationshipType(StrEnum):
    """Directed educational relationship between two CKG nodes.

    ``contains`` models structural ownership.
    ``references`` links learning objectives to educational objects.
    ``requires`` is a hard prerequisite (must remain acyclic).
    ``cross_references`` is a soft advisory link between structural nodes.
    ``exemplifies`` / ``defines`` / ``assesses`` / ``reads`` refine object roles.
    """

    CONTAINS = "contains"
    REFERENCES = "references"
    REQUIRES = "requires"
    CROSS_REFERENCES = "cross_references"
    EXEMPLIFIES = "exemplifies"
    DEFINES = "defines"
    ASSESSES = "assesses"
    READS = "reads"


# Relationship types that participate in hard-prerequisite cycle detection.
HARD_PREREQUISITE_TYPES: frozenset[CkgRelationshipType] = frozenset(
    {CkgRelationshipType.REQUIRES}
)
