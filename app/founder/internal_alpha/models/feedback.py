"""Core domain objects for the Internal Alpha Processing Pipeline (FOS-003)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType


def _empty_counts() -> Mapping[str, int]:
    return MappingProxyType({})


@dataclass(frozen=True)
class FeedbackItem:
    """One raw Internal Alpha feedback observation."""

    id: str
    filename: str
    contributor: str
    week: str
    raw_text: str
    created_at: datetime


@dataclass(frozen=True)
class ClassifiedFeedback:
    """Feedback after rule-based classification (and optional duplicate link)."""

    feedback_item: FeedbackItem
    category: str
    confidence: float
    duplicate_of: str | None = None


@dataclass(frozen=True)
class WeeklySummary:
    """Aggregated statistics for one Internal Alpha week."""

    week: str
    total_feedback: int
    category_counts: Mapping[str, int]
    duplicate_count: int
    generated_at: datetime
    contributor_counts: Mapping[str, int] = field(default_factory=_empty_counts)


@dataclass(frozen=True)
class PipelineResult:
    """Outcome of one InternalAlphaPipelineService run."""

    success: bool
    processed_items: tuple[ClassifiedFeedback, ...]
    warnings: tuple[str, ...]
    output_files: tuple[str, ...]
