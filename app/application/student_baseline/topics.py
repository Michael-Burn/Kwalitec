"""Syllabus topic choices for SB-001A Baseline position step.

Supports JSON-bundled curricula (CurriculumEngine) and founder-published
subjects (Educational Engine Foundation artefacts).

For published packages, Baseline continue-from lists **syllabus sections**
(e.g. CS1 ``Data Analysis``), not leaf learning objectives (1.1, 1.2, …).
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
_SECTION_LEADING_NUMBER = re.compile(r"^(\d+)\s+(.+)$")
_SMALL_WORDS = frozenset({"and", "or", "of", "the", "a", "an", "in", "on", "to", "for"})


def list_topic_choices(
    *,
    category_code: str,
    subject_code: str,
    curriculum_version: str | None,
) -> list[tuple[str, str]]:
    """Return ``(code, label)`` pairs for the Baseline topic picker.

    Published subjects use section codes (``1``, ``2``, …). JSON-bundled
    curricula use topic codes. Empty when no syllabus can be resolved —
    callers must not offer continue-from-topic without choices.
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
    """Ordered topic/section codes for completed-prefix inference on continue."""
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


def format_baseline_section_choice(
    *,
    number: str = "",
    title: str = "",
    code: str = "",
) -> tuple[str, str] | None:
    """Build a section-level picker row for published syllabi.

    CS1 example: title ``1 Data analysis`` → ``("1", "Data Analysis")``.
    """
    raw = (title or "").strip()
    num = (number or "").strip()
    if not num and code and str(code).strip().isdigit():
        num = str(code).strip()

    match = _SECTION_LEADING_NUMBER.match(raw)
    if match:
        if not num:
            num = match.group(1)
        raw = match.group(2).strip()
    elif num and raw.startswith(num):
        raw = raw[len(num) :].lstrip(" .:—-")

    raw = raw.strip()
    if not num or not raw:
        return None
    if not re.match(r"^\d+$", num):
        return None
    if _looks_like_non_syllabus_noise(raw):
        return None
    letters = sum(1 for ch in raw if ch.isalpha())
    if letters < 4:
        return None

    return num, _title_case_section(raw)


def _title_case_section(text: str) -> str:
    words = re.split(r"(\s+)", text.strip())
    out: list[str] = []
    word_index = 0
    for part in words:
        if not part or part.isspace():
            out.append(part)
            continue
        lower = part.lower()
        if word_index > 0 and lower in _SMALL_WORDS:
            out.append(lower)
        else:
            out.append(part[:1].upper() + part[1:].lower() if part else part)
        word_index += 1
    return "".join(out)


def is_non_syllabus_title(text: str) -> bool:
    """True when a title looks like publisher metadata, not a syllabus topic.

    Used by Baseline and student Curriculum Map surfaces to quarantine
    postal addresses and similar non-learning rows (EV-001 TB-003).
    """
    return _looks_like_non_syllabus_noise(text)


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

    if snapshot is None:
        return []

    # Prefer official syllabus sections (chapters), not leaf objectives.
    sections = getattr(snapshot, "sections", None) or ()
    if sections:
        choices: list[tuple[str, str]] = []
        seen: set[str] = set()
        for section in sorted(
            sections,
            key=lambda s: (
                int(s.get("display_order") or 0),
                str(s.get("number") or s.get("code") or ""),
            ),
        ):
            formatted = format_baseline_section_choice(
                number=str(section.get("number") or "").strip(),
                title=str(section.get("title") or "").strip(),
                code=str(section.get("code") or "").strip(),
            )
            if formatted is None:
                continue
            value, label = formatted
            if value in seen:
                continue
            seen.add(value)
            choices.append((value, label))
        if choices:
            return choices

    # Fallback: leaf topics only when the package has no usable sections.
    if not snapshot.topics:
        return []

    choices = []
    seen = set()
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
