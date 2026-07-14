"""Knowledge Engine index summary DTO (FOS-001)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KnowledgeIndexSummaryDTO:
    """Aggregated counts from a Knowledge Engine repository scan.

    Count fields align with Operational State knowledge aggregation.
    """

    source_version: str
    engineering_standards: int
    architecture_documents: int
    research_documents: int
    capability_documents: int
    indexed_artefacts: int
    tests_pass: bool = True
    validation_errors: int = 0
    missing_roots: tuple[str, ...] = ()
