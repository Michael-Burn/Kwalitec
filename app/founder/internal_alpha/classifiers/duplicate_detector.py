"""Duplicate detection for Internal Alpha feedback (relationships only)."""

from __future__ import annotations

import re
from difflib import SequenceMatcher

from app.founder.internal_alpha.config import (
    InternalAlphaPipelineConfig,
    default_config,
)
from app.founder.internal_alpha.dto import DuplicateRelation
from app.founder.internal_alpha.models import FeedbackItem

_WHITESPACE_RE = re.compile(r"\s+")
_PUNCT_RE = re.compile(r"[^\w\s]", re.UNICODE)


def normalise_feedback_text(text: str) -> str:
    """Normalise text for duplicate comparison (deterministic)."""

    lowered = text.casefold().strip()
    without_punct = _PUNCT_RE.sub(" ", lowered)
    return _WHITESPACE_RE.sub(" ", without_punct).strip()


class DuplicateDetector:
    """Detect identical, normalised-identical, and near-duplicate feedback.

    Returns duplicate relationships only. Never removes feedback.
    """

    def __init__(self, config: InternalAlphaPipelineConfig | None = None) -> None:
        self._config = config or default_config()

    def detect(
        self, items: tuple[FeedbackItem, ...] | list[FeedbackItem]
    ) -> tuple[DuplicateRelation, ...]:
        """Return duplicate relationships among ``items``.

        Later items may be marked as duplicates of earlier canonical items
        (stable order by input sequence).
        """
        ordered = list(items)
        relations: list[DuplicateRelation] = []
        canonical: list[FeedbackItem] = []

        for item in ordered:
            match = self._find_duplicate(item, canonical)
            if match is None:
                canonical.append(item)
            else:
                relations.append(match)

        return tuple(relations)

    def _find_duplicate(
        self,
        item: FeedbackItem,
        canonical: list[FeedbackItem],
    ) -> DuplicateRelation | None:
        raw = item.raw_text
        norm = normalise_feedback_text(raw)
        threshold = self._config.similarity_threshold

        for prior in canonical:
            if item.id == prior.id:
                continue
            if raw == prior.raw_text:
                return DuplicateRelation(
                    source_id=item.id,
                    target_id=prior.id,
                    reason="identical",
                    similarity=1.0,
                )
            prior_norm = normalise_feedback_text(prior.raw_text)
            if norm == prior_norm and norm != "":
                return DuplicateRelation(
                    source_id=item.id,
                    target_id=prior.id,
                    reason="normalised_identical",
                    similarity=1.0,
                )
            similarity = SequenceMatcher(None, norm, prior_norm).ratio()
            if similarity >= threshold:
                return DuplicateRelation(
                    source_id=item.id,
                    target_id=prior.id,
                    reason="similar",
                    similarity=round(similarity, 4),
                )
        return None
