"""Syllabus topic choices for SB-001A Baseline position step.

Supports JSON-bundled curricula (CurriculumEngine) and founder-published
subjects (Educational Engine Foundation artefacts).
"""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)

# Official syllabus topics use hierarchical codes (e.g. 1.1, 2.6). Bare integers
# and free-text rows (addresses, footers) must not appear in the picker.
_HIERARCHICAL_SYLLABUS_CODE = re.compile(r"^\d+\.\d+(?:\.\d+)*$")
_TITLE_LEADING_SYLLABUS = re.compile(
    r"^(\d+\.\d+(?:\.\d+)*)\s+(.+)$",
)


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


def format_baseline_topic_choice(
    *,
    code: str = "",
    title: str = "",
    number: str = "",
) -> tuple[str, str] | None:
    """Build a clean picker row, or ``None`` when the topic is not syllabus-like.

    Labels are ``{code} — {title}`` without duplicating the code in the title.
    """
    from app.domain.educational_runtime_engine.student_facing_identity import (
        display_topic_title,
        student_syllabus_code,
    )

    raw_title = (title or "").strip()
    human_code = student_syllabus_code(code=code, title=raw_title, number=number)
    if not human_code or not _HIERARCHICAL_SYLLABUS_CODE.match(human_code):
        return None

    display = display_topic_title(title=raw_title, code=code or human_code)
    title_match = _TITLE_LEADING_SYLLABUS.match(display)
    if title_match:
        # Prefer the hierarchical code embedded in the title when present.
        embedded = title_match.group(1)
        if _HIERARCHICAL_SYLLABUS_CODE.match(embedded):
            human_code = embedded
        rest = title_match.group(2).strip(" —:-")
        if rest:
            display = rest
    elif display.startswith(human_code):
        rest = display[len(human_code) :].lstrip(" —:-")
        display = rest or display

    display = display.strip()
    if not display:
        return None
    # Reject footers / addresses that slipped through numbering.
    if _looks_like_non_syllabus_noise(display):
        return None
    return human_code, f"{human_code} — {display}"


def _looks_like_non_syllabus_noise(text: str) -> bool:
    lowered = text.lower()
    noise_markers = (
        "singapore",
        " jln ",
        "jalan ",
        " street",
        " avenue",
        " road",
        "#0",
        "postal",
        "zip",
        "@",
    )
    if any(marker in f" {lowered} " or marker in lowered for marker in noise_markers):
        return True
    # No alphabetic learning verb/noun after stripping — likely garbage.
    letters = sum(1 for ch in text if ch.isalpha())
    return letters < 8


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
        formatted = format_baseline_topic_choice(
            code=str(topic.get("code") or "").strip(),
            title=str(topic.get("title") or "").strip(),
            number=str(topic.get("number") or "").strip(),
        )
        if formatted is None:
            continue
        value, label = formatted
        if value in seen:
            continue
        seen.add(value)
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
        choices: list[tuple[str, str]] = []
        for topic in topics:
            formatted = format_baseline_topic_choice(
                code=topic.code,
                title=topic.title,
            )
            if formatted is None:
                # JSON curricula may use undotted codes; keep a clean fallback.
                title = (topic.title or "").strip()
                if topic.code and title:
                    if title.startswith(topic.code):
                        rest = title[len(topic.code) :].lstrip(" —:-")
                        label = f"{topic.code} — {rest}" if rest else topic.code
                    else:
                        label = f"{topic.code} — {title}"
                    choices.append((topic.code, label))
                continue
            choices.append(formatted)
        return choices
    except Exception:
        logger.exception(
            "baseline_topics: failed loading JSON curriculum %s/%s/%s",
            category_code,
            subject_code,
            curriculum_version,
        )
        return []
