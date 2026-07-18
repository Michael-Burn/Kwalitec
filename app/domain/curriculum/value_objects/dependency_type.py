"""Educational dependency kinds between curriculum topics.

Structural relationship types only — no content payloads.
"""

from __future__ import annotations

from enum import StrEnum


class DependencyType(StrEnum):
    """Relationship kind between two topics in the curriculum graph.

    REQUIRES is the hard prerequisite edge used for eligibility and
    topological ordering. Other kinds are advisory or associative.
    """

    REQUIRES = "requires"
    RECOMMENDS = "recommends"
    RELATED = "related"
    OPTIONAL = "optional"
    REVISION = "revision"


# Hard dependency kinds that block eligibility when unsatisfied.
HARD_DEPENDENCY_TYPES: frozenset[DependencyType] = frozenset(
    {DependencyType.REQUIRES}
)

# Soft / advisory dependency kinds (do not block eligibility alone).
SOFT_DEPENDENCY_TYPES: frozenset[DependencyType] = frozenset(
    {
        DependencyType.RECOMMENDS,
        DependencyType.RELATED,
        DependencyType.OPTIONAL,
        DependencyType.REVISION,
    }
)


def is_hard_dependency(dependency_type: DependencyType) -> bool:
    """True when the dependency blocks topic eligibility if unmet."""
    return dependency_type in HARD_DEPENDENCY_TYPES
