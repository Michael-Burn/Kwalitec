"""Syllabus topic choices for SB-001A Baseline position step.

Supports JSON-bundled curricula (CurriculumEngine) and founder-published
subjects (Educational Engine Foundation artefacts).
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def list_topic_choices(
    *,
    category_code: str,
    subject_code: str,
    curriculum_version: str | None,
) -> list[tuple[str, str]]:
    """Return ``(code, label)`` pairs for the Baseline topic picker.

    Codes are human syllabus codes where available (e.g. ``1.1``), matching
    Study Plan / completed-topic semantics. Empty when no syllabus can be
    resolved — callers must not offer continue-from-topic without choices.
    """
    version = (curriculum_version or "").strip()
    category = (category_code or "").strip()
    subject = (subject_code or "").strip()
    if not subject:
        return []

    if version == "published" or category.upper() == "PUBLISHED":
        return _published_topic_choices(subject)

    if not version or not category:
        return []

    return _json_bundled_topic_choices(category, subject, version)


def ordered_topic_codes(
    *,
    category_code: str,
    subject_code: str,
    curriculum_version: str | None,
) -> list[str]:
    """Ordered topic codes for completed-prefix inference on continue."""
    return [
        code
        for code, _label in list_topic_choices(
            category_code=category_code,
            subject_code=subject_code,
            curriculum_version=curriculum_version,
        )
    ]


def _published_topic_choices(subject_code: str) -> list[tuple[str, str]]:
    try:
        from app.application.educational_engine_foundation.service import (
            EducationalEngineFoundationService,
        )

        snapshot = EducationalEngineFoundationService().derive_active(subject_code)
    except Exception:
        logger.exception(
            "baseline_topics: failed deriving published artefacts subject=%s",
            subject_code,
        )
        return []

    if snapshot is None or not snapshot.topics:
        return []

    choices: list[tuple[str, str]] = []
    seen: set[str] = set()
    for topic in sorted(
        snapshot.topics,
        key=lambda t: (
            int(t.get("display_order") or 0),
            str(t.get("code") or t.get("topic_id") or ""),
        ),
    ):
        code = str(topic.get("code") or "").strip()
        topic_id = str(topic.get("topic_id") or "").strip()
        value = code or topic_id
        if not value or value in seen:
            continue
        seen.add(value)
        title = str(topic.get("title") or value).strip()
        label = f"{code} — {title}" if code else title
        choices.append((value, label))
    return choices


def _json_bundled_topic_choices(
    category_code: str,
    subject_code: str,
    curriculum_version: str,
) -> list[tuple[str, str]]:
    try:
        from app.services.curriculum_engine_service import CurriculumEngineService

        engine = CurriculumEngineService()
        if not engine.curriculum_exists(
            category_code, subject_code, curriculum_version
        ):
            return []
        curriculum = engine.load_auto(
            category_code, subject_code, curriculum_version
        )
        topics = CurriculumEngineService.get_topics_flat(curriculum)
        return [(t.code, f"{t.code} — {t.title}") for t in topics]
    except Exception:
        logger.exception(
            "baseline_topics: failed loading JSON curriculum %s/%s/%s",
            category_code,
            subject_code,
            curriculum_version,
        )
        return []
