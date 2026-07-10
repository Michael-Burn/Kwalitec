"""Transformer package for the Evidence Transformation Stage.

Contains the abstract transformer contract. Specialised transformers
(KnowledgeTransformer, BehaviourTransformer, ConfidenceTransformer,
RevisionTransformer, PlanningTransformer, TimeTransformer, …) are registered
with ``EvidenceTransformer`` in later capabilities.
"""

from __future__ import annotations

from app.domain.evidence.transformers.base_transformer import BaseTransformer

__all__ = [
    "BaseTransformer",
]
