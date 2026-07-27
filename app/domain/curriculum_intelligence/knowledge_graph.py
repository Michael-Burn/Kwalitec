"""Knowledge graph relationship contracts for CIP-001.

The graph is the canonical educational model extension point for the
Student Digital Twin. Embeddings attach in CIP-003 — not here.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class KnowledgeRelationType(StrEnum):
    """Directed relationship kinds between curriculum knowledge entities."""

    DEPENDS_ON = "depends_on"
    REQUIRES = "requires"
    SUPPORTS = "supports"
    EXTENDS = "extends"
    CONTRADICTS = "contradicts"
    APPEARS_IN = "appears_in"
    TESTED_IN = "tested_in"
    DERIVED_FROM = "derived_from"
    EXAMPLE_OF = "example_of"
    FORMULA_FOR = "formula_for"
    LEARNING_OBJECTIVE_OF = "learning_objective_of"
    PARENT_OF = "parent_of"
    CHILD_OF = "child_of"


@dataclass(frozen=True)
class KnowledgeRelation:
    """One directed edge in the curriculum knowledge graph."""

    relation_id: str
    relation_type: KnowledgeRelationType
    from_entity_id: str
    to_entity_id: str
    source_document_id: int
    confidence: float
    needs_review: bool = False
    attributes: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class KnowledgeGraph:
    """Graph snapshot for one mapped curriculum document."""

    graph_id: str
    document_id: int
    map_id: str
    entity_ids: tuple[str, ...]
    relations: tuple[KnowledgeRelation, ...]
    diagnostics: tuple[str, ...] = ()
