"""Extractor package for the Evidence Extraction Engine.

Contains the abstract extractor contract. Specialised extractors are registered
with ``EvidenceExtractor`` in later capabilities.
"""

from __future__ import annotations

from app.domain.evidence.extractors.base_extractor import BaseExtractor

__all__ = [
    "BaseExtractor",
]
