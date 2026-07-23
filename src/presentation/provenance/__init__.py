"""RR-001 Explainability & Trust — presentation-only educational provenance.

Surfaces deterministic reasons already produced by the Education OS and
Application layer. Never changes recommendation logic, never adds educational
reasoning, and never uses an LLM.
"""

from __future__ import annotations

from presentation.provenance.enums import ProvenanceKind
from presentation.provenance.mapper import (
    ProvenanceMapper,
    iter_reason_sentences,
    merge_provenance,
)
from presentation.provenance.narration import (
    kind_for_reason_code,
    kind_for_sentence,
    narrate_reason_code,
    one_sentence,
)
from presentation.provenance.view_models import (
    DEFAULT_PROVENANCE_TITLE,
    MAX_PROVENANCE_REASONS,
    ProvenanceReasonView,
    ProvenanceViewModel,
)

__all__ = [
    "DEFAULT_PROVENANCE_TITLE",
    "MAX_PROVENANCE_REASONS",
    "ProvenanceKind",
    "ProvenanceMapper",
    "ProvenanceReasonView",
    "ProvenanceViewModel",
    "iter_reason_sentences",
    "kind_for_reason_code",
    "kind_for_sentence",
    "merge_provenance",
    "narrate_reason_code",
    "one_sentence",
]
