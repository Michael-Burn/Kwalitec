"""MISSION-002 — Student-facing syllabus identity helpers.

Educational Intelligence node identifiers (``node-…``) must never appear in
student-facing chrome. These helpers project human syllabus codes and scrub
internal ids from presentation strings.
"""

from __future__ import annotations

import re

_NODE_ID_RE = re.compile(r"^node-[0-9a-z]+$", re.IGNORECASE)
_NODE_SUBSTRING_RE = re.compile(r"\bnode-[0-9a-z]+\b", re.IGNORECASE)
_SYLLABUS_CODE_IN_TITLE = re.compile(r"^(\d+(?:\.\d+)*)\b")
_STUDY_NODE_PREFIX = re.compile(
    r"^Study\s+node-[0-9a-z]+\s*[—\-:]?\s*",
    re.IGNORECASE,
)
_PUBLISHED_TOPIC_NODE = re.compile(
    r"Published topic\s+node-[0-9a-z]+(?:\s*\([^)]*\))?",
    re.IGNORECASE,
)
_OBJECTIVE_IDS_LINE = re.compile(
    r"Learning objective ids:\s*[^\n]*",
    re.IGNORECASE,
)
# Persisted / composed titles that dropped a chapter digit (DF-016).
_MANGLED_STUDY_TITLE = re.compile(
    r"^Study\s+(\d+)\s*[—\-]\s*\.(\d+(?:\.\d+)*)\s*(.*)$",
    re.IGNORECASE,
)
_LEADING_STUDY_PREFIX = re.compile(r"^Study\s+", re.IGNORECASE)


def is_internal_node_identifier(value: str | None) -> bool:
    """Return True when *value* is an EI / package node identifier."""
    text = (value or "").strip()
    if not text:
        return False
    if _NODE_ID_RE.match(text):
        return True
    return text.lower().startswith("node-")


def student_syllabus_code(
    *,
    code: str = "",
    title: str = "",
    number: str = "",
) -> str:
    """Resolve a human syllabus code; never return a ``node-`` identifier.

    When a provided code truncates a fuller syllabus number in the title
    (e.g. code ``1`` vs title ``1.1 Describe…``), prefer the title number so
    student chrome never shows ``Study 1 — .1 …`` (V1S-008 / DF-016).

    When the package code is only a bare sequence index (``2``, ``15``) but the
    title carries a dotted syllabus number (``1.2``, ``4.1``), prefer the title
    number so Baseline / mission chrome stay syllabus-faithful.
    """
    code_text = ""
    for candidate in (code, number):
        text = (candidate or "").strip()
        if text and not is_internal_node_identifier(text):
            code_text = text
            break
    title_text = (title or "").strip()
    title_match = _SYLLABUS_CODE_IN_TITLE.match(title_text)
    title_code = title_match.group(1) if title_match else ""
    if title_code and code_text:
        if title_code.startswith(code_text) and len(title_code) > len(code_text):
            # Truncated chapter code vs full section number (1 vs 1.1).
            if title_code[len(code_text)] == ".":
                return title_code
        # Bare display-order index vs dotted syllabus code in the title.
        if (
            code_text.isdigit()
            and "." in title_code
            and title_code != code_text
        ):
            return title_code
    if code_text and not (
        code_text.isdigit() and title_code and "." in title_code
    ):
        return code_text
    if code_text and not title_code:
        return code_text
    return title_code or code_text


def repair_mangled_study_title(text: str | None) -> str:
    """Repair ``Study 1 — .1 …`` into a rebuildable topic string.

    Returns a syllabus-leading title (``1.1 Describe…``) when the mangled
    Study pattern is detected; otherwise returns the stripped input.
    """
    raw = (text or "").strip()
    if not raw:
        return ""
    mangled = _MANGLED_STUDY_TITLE.match(raw)
    if mangled:
        chapter, remainder, rest = mangled.group(1), mangled.group(2), mangled.group(3)
        recovered = f"{chapter}.{remainder}"
        rest = (rest or "").strip(" —:-")
        return f"{recovered} {rest}".strip() if rest else recovered
    return raw


def repair_truncated_topic_title(*, code: str = "", title: str = "") -> str:
    """Join truncated chapter code with a leading ``.N`` title fragment."""
    code_text = (code or "").strip()
    title_text = repair_mangled_study_title(title)
    if (
        code_text
        and code_text.isdigit()
        and title_text.startswith(".")
        and len(title_text) > 1
        and title_text[1].isdigit()
    ):
        return f"{code_text}{title_text}"
    return title_text


def display_topic_title(*, title: str = "", code: str = "") -> str:
    """Topic title suitable for students (no leading duplicate code required)."""
    text = repair_truncated_topic_title(code=code, title=title)
    if text and _LEADING_STUDY_PREFIX.match(text):
        # Already a Study chrome string — strip prefix before re-composing.
        text = _LEADING_STUDY_PREFIX.sub("", text, count=1).strip(" —:-")
    if not text:
        return student_syllabus_code(code=code, title=title) or "Today's topic"
    return text


def student_mission_title(*, code: str = "", title: str = "") -> str:
    """Build ``Study {code} — {title}`` using only human syllabus references."""
    repaired = repair_truncated_topic_title(code=code, title=title)
    human_code = student_syllabus_code(code=code, title=repaired)
    display = display_topic_title(title=repaired, code=code)
    if human_code and display.startswith(human_code):
        rest = display[len(human_code) :]
        # Never strip a partial syllabus number (code "1" from "1.1 …").
        if rest[:1].isdigit() or rest.startswith("."):
            title_match = _SYLLABUS_CODE_IN_TITLE.match(display)
            if title_match and len(title_match.group(1)) >= len(human_code):
                human_code = title_match.group(1)
                rest = display[len(human_code) :].lstrip(" —:-")
                if rest:
                    display = rest
        else:
            rest = rest.lstrip(" —:-")
            if rest:
                display = rest
    if human_code and display:
        if display.startswith(human_code):
            return f"Study {display}"
        return f"Study {human_code} — {display}"
    if display:
        return f"Study {display}"
    return "Today's mission"


def sanitize_student_text(text: str | None) -> str:
    """Strip internal node identifiers from student-facing copy."""
    raw = (text or "").strip()
    if not raw:
        return ""
    cleaned = _STUDY_NODE_PREFIX.sub("Study ", raw)
    cleaned = _PUBLISHED_TOPIC_NODE.sub("Published topic", cleaned)
    cleaned = _OBJECTIVE_IDS_LINE.sub("", cleaned)
    cleaned = _NODE_SUBSTRING_RE.sub("", cleaned)
    cleaned = re.sub(r"\(\s*\)", "", cleaned)
    cleaned = re.sub(r"\s*—\s*—\s*", " — ", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    cleaned = re.sub(r"\s+,", ",", cleaned)
    return cleaned.strip(" ,;—-")


def contains_internal_node_identifier(text: str | None) -> bool:
    """True when any ``node-`` substring appears in *text*."""
    return bool(_NODE_SUBSTRING_RE.search(text or ""))
