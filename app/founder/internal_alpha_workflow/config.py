"""Configuration for Internal Alpha Live Workflow (FSI-003).

Single configuration location for week layout, naming, and managed export
filenames. Coordinator behaviour lives in the workflow service.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

# ---------------------------------------------------------------------------
# Repository layout
# ---------------------------------------------------------------------------

DEFAULT_INTERNAL_ALPHA_RELATIVE = ("research", "internal_alpha")
WEEK_TEMPLATE_DIRNAME = "week_template"
WEEK_DIR_PATTERN = r"^week_(\d+)$"

REQUIRED_WEEK_DIRNAMES: tuple[str, ...] = (
    "raw_feedback",
    "processed",
    "findings",
    "decisions",
    "weekly_review",
    "release",
    "archive",
)

OUTPUT_DIRNAMES: tuple[str, ...] = (
    "processed",
    "findings",
    "decisions",
    "weekly_review",
    "release",
    "archive",
)

RAW_FEEDBACK_DIRNAME = "raw_feedback"
PROCESSED_DIRNAME = "processed"
FINDINGS_DIRNAME = "findings"
DECISIONS_DIRNAME = "decisions"
WEEKLY_REVIEW_DIRNAME = "weekly_review"
RELEASE_DIRNAME = "release"
ARCHIVE_DIRNAME = "archive"

# ---------------------------------------------------------------------------
# Managed export filenames (workflow may overwrite only these)
# ---------------------------------------------------------------------------

FINDINGS_FROM_PROCESSED: tuple[str, ...] = (
    "WEEK_SUMMARY.md",
    "architecture.md",
    "engineering.md",
    "product.md",
    "educational.md",
    "ux.md",
)

RELEASE_FROM_PROCESSED: tuple[str, ...] = ("release_readiness.md",)

DECISIONS_FROM_PROCESSED: tuple[str, ...] = ("proposed_actions.md",)

RECOMMENDATIONS_JSON = "recommendations.json"
RECOMMENDATIONS_MD = "recommendations.md"
ARCHIVE_MANIFEST = "workflow_manifest.json"
ARCHIVE_WEEK_SUMMARY = "WEEK_SUMMARY.md"
ARCHIVE_RECOMMENDATIONS = "recommendations.json"
ARCHIVE_BRIEF_MD = "FOUNDER_WEEKLY_REPORT.md"

INTERNAL_ALPHA_SOURCE_VERSION = "fos-003-pipeline-1.0"


@dataclass(frozen=True)
class InternalAlphaWorkflowConfig:
    """Immutable workflow configuration snapshot."""

    week_dir_pattern: str = WEEK_DIR_PATTERN
    required_week_dirnames: tuple[str, ...] = REQUIRED_WEEK_DIRNAMES
    output_dirnames: tuple[str, ...] = OUTPUT_DIRNAMES
    week_template_dirname: str = WEEK_TEMPLATE_DIRNAME
    findings_from_processed: tuple[str, ...] = FINDINGS_FROM_PROCESSED
    release_from_processed: tuple[str, ...] = RELEASE_FROM_PROCESSED
    decisions_from_processed: tuple[str, ...] = DECISIONS_FROM_PROCESSED
    recommendations_json: str = RECOMMENDATIONS_JSON
    recommendations_md: str = RECOMMENDATIONS_MD
    archive_manifest: str = ARCHIVE_MANIFEST
    internal_alpha_source_version: str = INTERNAL_ALPHA_SOURCE_VERSION
    feedback_extension: str = ".txt"
    managed_filenames: Mapping[str, tuple[str, ...]] = field(
        default_factory=lambda: MappingProxyType(
            {
                FINDINGS_DIRNAME: FINDINGS_FROM_PROCESSED,
                DECISIONS_DIRNAME: (
                    *DECISIONS_FROM_PROCESSED,
                    RECOMMENDATIONS_JSON,
                    RECOMMENDATIONS_MD,
                ),
                WEEKLY_REVIEW_DIRNAME: (
                    "FOUNDER_WEEKLY_REPORT.md",
                    "founder_weekly_report.json",
                ),
                RELEASE_DIRNAME: RELEASE_FROM_PROCESSED,
                ARCHIVE_DIRNAME: (
                    ARCHIVE_MANIFEST,
                    ARCHIVE_WEEK_SUMMARY,
                    ARCHIVE_RECOMMENDATIONS,
                    ARCHIVE_BRIEF_MD,
                ),
            }
        )
    )


def default_config() -> InternalAlphaWorkflowConfig:
    """Return the Version 1 default workflow configuration."""

    return InternalAlphaWorkflowConfig()
