"""Immutable provenance contracts for Curriculum Intelligence (CIP-002).

Every educational fact must answer: where it came from, which parser/job
created it, which pages/blocks support it, and which curriculum version
it derives from. Provenance is append-only — never overwritten by review.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

PARSER_VERSION = "cip-structural-parser/1.0"
MAPPER_VERSION = "cip-curriculum-mapper/1.0"
GRAPH_BUILDER_VERSION = "cip-knowledge-graph-builder/1.0"


class ProvenanceSubjectKind(StrEnum):
    """What a provenance record describes."""

    ENTITY = "entity"
    RELATION = "relation"
    STRUCTURAL_NODE = "structural_node"
    EDUCATIONAL_NODE = "educational_node"


class ProvenanceChainStage(StrEnum):
    """Navigable production chain stages."""

    DOCUMENT = "document"
    EXTRACTION = "extraction"
    PARSER = "parser"
    CURRICULUM_MAPPING = "curriculum_mapping"
    KNOWLEDGE_GRAPH = "knowledge_graph"


@dataclass(frozen=True)
class SupportingEvidence:
    """One piece of source evidence backing an educational fact."""

    page_number: int | None
    paragraph_index: int | None
    block_id: str | None
    excerpt: str
    evidence_role: str = "source"


@dataclass(frozen=True)
class ProvenanceRecord:
    """Immutable provenance for one curriculum knowledge artefact."""

    provenance_id: str
    subject_kind: ProvenanceSubjectKind
    subject_id: str
    source_document_id: int
    source_version_label: str
    source_pages: tuple[int, ...]
    source_paragraphs: tuple[int, ...]
    source_block_ids: tuple[str, ...]
    parser_version: str
    mapper_version: str
    graph_builder_version: str
    pipeline_job_id: str
    extraction_id: str
    parse_id: str
    map_id: str
    graph_id: str
    chain_stage: ProvenanceChainStage
    evidence: tuple[SupportingEvidence, ...]
    created_at_iso: str
    attributes: tuple[tuple[str, str], ...] = ()
