"""Immutable Knowledge Engine artefact DTOs (FOS-001)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KnowledgeArtefactDTO:
    """One indexed knowledge artefact.

    Identifiers and collections are logical only — no filesystem paths.
    """

    artefact_id: str
    title: str
    collection: str
    document_id: str = ""
