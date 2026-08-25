"""Parse session activity body text into labelled sections for Session UI.

Presentation-only. Educational package fields remain the source of truth;
this module only shapes already-assembled body text for readable rendering.
"""

from __future__ import annotations

from dataclasses import dataclass

# Phrases authored for internal CMP-authority reminders — never show to students.
_AUTHOR_VOICE_PHRASES: tuple[str, ...] = (
    "Kwalitec is the guide; the CMP is the authoritative material — "
    "do not treat this activity body as a substitute textbook. ",
    "Kwalitec is the guide; the CMP is the authoritative material — "
    "do not treat this activity body as a substitute textbook.",
    "Kwalitec is the guide; the CMP is authoritative. ",
    "Kwalitec is the guide; the CMP is authoritative.",
    "Kwalitec directs revision; the CMP is reopened only as a targeted "
    "instrument after a failed retrieval — not as a fresh chapter read "
    "and not as a substitute for the checks. ",
)


@dataclass(frozen=True)
class ContentSection:
    """One labelled block in the Session content area."""

    label: str = ""
    paragraphs: tuple[str, ...] = ()
    bullets: tuple[str, ...] = ()


def strip_author_voice(text: str) -> str:
    """Remove internal-authoring meta-commentary from student-facing copy."""
    cleaned = text or ""
    for phrase in _AUTHOR_VOICE_PHRASES:
        cleaned = cleaned.replace(phrase, "")
    # Collapse leftover double spaces / awkward ". ." from phrase removal.
    while "  " in cleaned:
        cleaned = cleaned.replace("  ", " ")
    cleaned = cleaned.replace(" .", ".")
    return cleaned.strip()


def parse_session_content_body(body: str) -> tuple[ContentSection, ...]:
    """Turn newline-oriented guidance text into labelled sections + lists.

    Recognises section headers (a line ending with ``:`` with no leading bullet)
    followed by ``•`` / ``-`` bullet lines. Other lines become paragraphs.
    Returns an empty tuple when the body has no usable structure (caller should
    fall back to plain rendering).
    """
    raw = strip_author_voice(body or "")
    if not raw.strip():
        return ()

    lines = [line.rstrip() for line in raw.splitlines()]
    sections: list[ContentSection] = []
    label = ""
    paragraphs: list[str] = []
    bullets: list[str] = []

    def flush() -> None:
        nonlocal label, paragraphs, bullets
        if not label and not paragraphs and not bullets:
            return
        sections.append(
            ContentSection(
                label=label,
                paragraphs=tuple(paragraphs),
                bullets=tuple(bullets),
            )
        )
        label = ""
        paragraphs = []
        bullets = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            # Blank line ends the current section when we already have content.
            if label or paragraphs or bullets:
                flush()
            continue

        bullet = _bullet_text(stripped)
        if bullet is not None:
            bullets.append(bullet)
            continue

        if _is_section_header(stripped):
            flush()
            label = stripped[:-1].strip() if stripped.endswith(":") else stripped
            continue

        # Prose line — if we were collecting bullets under a header, keep going
        # as a paragraph in the same section; otherwise start/continue prose.
        paragraphs.append(strip_author_voice(stripped))

    flush()

    # Prefer structured render only when we have at least one labelled block
    # or one bullet list — otherwise leave rendering to the plain path.
    if not any(s.label or s.bullets for s in sections):
        return ()
    return tuple(sections)


def _bullet_text(line: str) -> str | None:
    for prefix in ("• ", "- ", "* "):
        if line.startswith(prefix):
            return strip_author_voice(line[len(prefix) :].strip())
    if line.startswith("•"):
        return strip_author_voice(line[1:].strip())
    return None


def _is_section_header(line: str) -> bool:
    if not line.endswith(":"):
        return False
    # Avoid treating "Stop when: Through CMP…" as a bare header.
    if len(line) > 60:
        return False
    # Headers are short labels, not full sentences with mid-line periods.
    head = line[:-1]
    if ". " in head:
        return False
    return True
