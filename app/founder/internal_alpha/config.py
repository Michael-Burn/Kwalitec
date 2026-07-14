"""Single configuration location for the Internal Alpha Processing Pipeline (FOS-003).

All categories, keyword rules, folder names, similarity threshold, and output
filenames live here. Future versions may add categories by extending this module
without changing pipeline coordination.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

# ---------------------------------------------------------------------------
# Categories (order is stable for exports and tests)
# ---------------------------------------------------------------------------

DEFAULT_CATEGORIES: tuple[str, ...] = (
    "Architecture",
    "Engineering",
    "Product",
    "Educational",
    "UX",
    "Performance",
    "Bug",
    "Question",
    "Suggestion",
    "Other",
)

# ---------------------------------------------------------------------------
# Keyword rules: category → keywords (case-insensitive substring match)
# First matching category in DEFAULT_CATEGORIES order wins when scanning
# rules; rules are evaluated in the order listed in KEYWORD_RULES.
# ---------------------------------------------------------------------------

_KEYWORD_RULES: dict[str, tuple[str, ...]] = {
    "Architecture": (
        "architecture",
        "layering",
        "dependency",
        "bounded context",
        "module boundary",
        "constitution",
        "adr",
    ),
    "Engineering": (
        "engineering",
        "refactor",
        "technical debt",
        "test coverage",
        "ci",
        "ruff",
        "pytest",
        "typed",
        "service layer",
    ),
    "Product": (
        "product",
        "roadmap",
        "mvp",
        "alpha",
        "release",
        "priority",
        "feature request",
    ),
    "Educational": (
        "educational",
        "curriculum",
        "mastery",
        "learning",
        "syllabus",
        "twin",
        "pedagog",
        "study plan",
    ),
    "UX": (
        "ux",
        "ui",
        "usability",
        "confusing",
        "navigation",
        "dashboard layout",
        "button",
        "copy",
    ),
    "Performance": (
        "performance",
        "slow",
        "latency",
        "timeout",
        "memory",
        "n+1",
    ),
    "Bug": (
        "bug",
        "crash",
        "error",
        "broken",
        "exception",
        "regression",
        "traceback",
    ),
    "Question": (
        "question",
        "how do",
        "why does",
        "unclear whether",
        "?",
    ),
    "Suggestion": (
        "suggest",
        "recommendation",
        "should we",
        "consider",
        "it would help",
        "proposal",
    ),
}

DEFAULT_KEYWORD_RULES: Mapping[str, tuple[str, ...]] = MappingProxyType(
    {k: v for k, v in _KEYWORD_RULES.items()}
)

# ---------------------------------------------------------------------------
# Folder / file layout
# ---------------------------------------------------------------------------

DEFAULT_RAW_FEEDBACK_DIRNAME = "raw_feedback"
DEFAULT_PROCESSED_DIRNAME = "processed"
DEFAULT_FEEDBACK_EXTENSION = ".txt"

# ---------------------------------------------------------------------------
# Duplicate detection
# ---------------------------------------------------------------------------

DEFAULT_SIMILARITY_THRESHOLD = 0.85

# ---------------------------------------------------------------------------
# Output filenames (written under processed/)
# ---------------------------------------------------------------------------

OUTPUT_CLASSIFIED_FEEDBACK = "classified_feedback.json"
OUTPUT_FEEDBACK_STATISTICS = "feedback_statistics.json"
OUTPUT_DUPLICATE_REPORT = "duplicate_report.json"
OUTPUT_WEEK_SUMMARY = "WEEK_SUMMARY.md"
OUTPUT_ARCHITECTURE = "architecture.md"
OUTPUT_ENGINEERING = "engineering.md"
OUTPUT_PRODUCT = "product.md"
OUTPUT_EDUCATIONAL = "educational.md"
OUTPUT_UX = "ux.md"
OUTPUT_PROPOSED_ACTIONS = "proposed_actions.md"
OUTPUT_RELEASE_READINESS = "release_readiness.md"

DEFAULT_OUTPUT_FILENAMES: Mapping[str, str] = MappingProxyType(
    {
        "classified_feedback": OUTPUT_CLASSIFIED_FEEDBACK,
        "feedback_statistics": OUTPUT_FEEDBACK_STATISTICS,
        "duplicate_report": OUTPUT_DUPLICATE_REPORT,
        "week_summary": OUTPUT_WEEK_SUMMARY,
        "architecture": OUTPUT_ARCHITECTURE,
        "engineering": OUTPUT_ENGINEERING,
        "product": OUTPUT_PRODUCT,
        "educational": OUTPUT_EDUCATIONAL,
        "ux": OUTPUT_UX,
        "proposed_actions": OUTPUT_PROPOSED_ACTIONS,
        "release_readiness": OUTPUT_RELEASE_READINESS,
    }
)

# Category → markdown export key (subset of categories with dedicated files)
CATEGORY_MARKDOWN_KEYS: Mapping[str, str] = MappingProxyType(
    {
        "Architecture": "architecture",
        "Engineering": "engineering",
        "Product": "product",
        "Educational": "educational",
        "UX": "ux",
    }
)


@dataclass(frozen=True)
class InternalAlphaPipelineConfig:
    """Immutable pipeline configuration snapshot.

    Construct via :func:`default_config` or supply overrides for tests.
    """

    categories: tuple[str, ...] = DEFAULT_CATEGORIES
    keyword_rules: Mapping[str, tuple[str, ...]] = field(
        default_factory=lambda: DEFAULT_KEYWORD_RULES
    )
    raw_feedback_dirname: str = DEFAULT_RAW_FEEDBACK_DIRNAME
    processed_dirname: str = DEFAULT_PROCESSED_DIRNAME
    feedback_extension: str = DEFAULT_FEEDBACK_EXTENSION
    similarity_threshold: float = DEFAULT_SIMILARITY_THRESHOLD
    output_filenames: Mapping[str, str] = field(
        default_factory=lambda: DEFAULT_OUTPUT_FILENAMES
    )
    default_category: str = "Other"

    def __post_init__(self) -> None:
        if not 0.0 <= self.similarity_threshold <= 1.0:
            raise ValueError(
                "similarity_threshold must be in [0, 1], "
                f"got {self.similarity_threshold}"
            )
        if self.default_category not in self.categories:
            raise ValueError(
                f"default_category {self.default_category!r} not in categories"
            )


def default_config() -> InternalAlphaPipelineConfig:
    """Return the Version 1 default configuration."""

    return InternalAlphaPipelineConfig()
