"""Parse session activity body text into labelled sections for Session UI.

Presentation-only. Educational package fields remain the source of truth;
this module only shapes already-assembled body text for readable rendering.
"""

from __future__ import annotations

from dataclasses import dataclass

# Phrases authored for internal CMP-authority reminders — never show to students.
_AUTHOR_VOICE_PHRASES: tuple[str, ...] = (
    # Current punctuation (no em dash)
    "Kwalitec is the guide; the CMP is the authoritative material. "
    "Do not treat this activity body as a substitute textbook. ",
    "Kwalitec is the guide; the CMP is the authoritative material. "
    "Do not treat this activity body as a substitute textbook.",
    # Legacy em-dash form (still strip if present in older assembled bodies)
    "Kwalitec is the guide; the CMP is the authoritative material — "
    "do not treat this activity body as a substitute textbook. ",
    "Kwalitec is the guide; the CMP is the authoritative material — "
    "do not treat this activity body as a substitute textbook.",
    "Kwalitec is the guide; the CMP is authoritative. ",
    "Kwalitec is the guide; the CMP is authoritative.",
    "Kwalitec directs revision; the CMP is reopened only as a targeted "
    "instrument after a failed retrieval. Not as a fresh chapter read "
    "and not as a substitute for the checks. ",
)


@dataclass(frozen=True)
class ContentSection:
    """One labelled block in the Session content area."""

    label: str = ""
    paragraphs: tuple[str, ...] = ()
    bullets: tuple[str, ...] = ()


@dataclass(frozen=True)
class ReadingContentPresentation:
    """Default-visible vs collapsed Reading sections (template-facing)."""

    intro_line: str = ""
    primary: tuple[ContentSection, ...] = ()
    more: tuple[ContentSection, ...] = ()


# Shown above the fold for Guided Reading / Revision reading bodies.
_READING_PRIMARY_LABELS: frozenset[str] = frozenset(
    {
        "Open the CMP",
        "Focus questions",
        "Revision focus: retrieve, do not re-learn",
        "Retrieval questions (answer closed-book first)",
    }
)

# Available behind the Session "More guidance" disclosure.
_READING_MORE_LABELS: frozenset[str] = frozenset(
    {
        "Misconception watch",
        "While you read",
        "While you retrieve",
        "Out of scope today",
        "When you finish",
        "Next after Revision",
    }
)

# Worked-example essentials vs secondary guidance.
_WORKED_EXAMPLE_PRIMARY_LABELS: frozenset[str] = frozenset(
    {
        "Confirm your structure sketch",
        "Pause-point harvest",
        "Given values",
        "Attempt before reveal",
    }
)
_WORKED_EXAMPLE_MORE_LABELS: frozenset[str] = frozenset(
    {
        "Success criteria you will stress-test next",
        "Before you continue",
        "Final answer",
        "Common pitfall",
    }
)


def present_reading_content(
    sections: tuple[ContentSection, ...],
) -> ReadingContentPresentation:
    """Split parsed Reading sections into intro + essentials + more guidance.

    Does not re-parse package text. Unlabelled Topic/Mission prose collapses to
    a single Mission line when present; secondary labelled blocks move to
    ``more`` for a default-closed disclosure.
    """
    if not sections:
        return ReadingContentPresentation()

    intro_line = ""
    primary: list[ContentSection] = []
    more: list[ContentSection] = []

    for section in sections:
        if not section.label:
            intro_line = _consolidate_reading_intro(section.paragraphs) or intro_line
            if section.bullets:
                primary.append(
                    ContentSection(
                        label="",
                        paragraphs=(),
                        bullets=section.bullets,
                    )
                )
            continue
        if section.label in _READING_MORE_LABELS:
            more.append(section)
        elif section.label in _READING_PRIMARY_LABELS:
            primary.append(section)
        else:
            # Unknown labelled block: keep visible rather than hide.
            primary.append(section)

    return ReadingContentPresentation(
        intro_line=intro_line,
        primary=tuple(primary),
        more=tuple(more),
    )


def _consolidate_reading_intro(paragraphs: tuple[str, ...]) -> str:
    """Prefer Mission over Topic (and other near-duplicate framing lines)."""
    if not paragraphs:
        return ""
    for para in paragraphs:
        stripped = para.strip()
        if stripped.lower().startswith("mission:"):
            return stripped
    # Single prose line — keep it; multiple non-Mission lines → shortest.
    if len(paragraphs) == 1:
        return paragraphs[0].strip()
    return min((p.strip() for p in paragraphs if p.strip()), key=len, default="")


def present_worked_example_content(
    sections: tuple[ContentSection, ...],
) -> ReadingContentPresentation:
    """Split worked-example sections into intro + essentials + more guidance."""
    if not sections:
        return ReadingContentPresentation()

    intro_line = ""
    primary: list[ContentSection] = []
    more: list[ContentSection] = []

    for section in sections:
        if not section.label:
            # Prefer the first non-empty prose block as the re-entry intro.
            for para in section.paragraphs:
                stripped = para.strip()
                if stripped:
                    intro_line = intro_line or stripped
                    break
            if section.bullets:
                primary.append(
                    ContentSection(
                        label="",
                        paragraphs=(),
                        bullets=section.bullets,
                    )
                )
            continue
        if section.label in _WORKED_EXAMPLE_MORE_LABELS or section.label.startswith(
            "Worked solution"
        ):
            more.append(section)
        elif section.label in _WORKED_EXAMPLE_PRIMARY_LABELS:
            primary.append(section)
        else:
            primary.append(section)

    return ReadingContentPresentation(
        intro_line=intro_line,
        primary=tuple(primary),
        more=tuple(more),
    )


def present_practice_content(
    *,
    prompt: str,
    body: str,
) -> ReadingContentPresentation:
    """Practice L1: show the question once; keep short stubs out of the title path.

    The educational prompt is the student-facing question. Package ``body`` is
    often a one-line authoring stub — omit it when it adds no new information.
    """
    question = strip_author_voice((prompt or "").strip())
    stub = strip_author_voice((body or "").strip())
    primary: list[ContentSection] = []
    if question:
        primary.append(
            ContentSection(
                label="Question",
                paragraphs=(question,),
                bullets=(),
            )
        )
    if stub and stub.lower() not in question.lower() and len(stub) >= 12:
        # Only keep a distinct stub that isn't already the question text.
        primary.append(
            ContentSection(
                label="Focus",
                paragraphs=(stub,),
                bullets=(),
            )
        )
    return ReadingContentPresentation(intro_line="", primary=tuple(primary), more=())


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
