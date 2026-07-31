"""Mission writing rules — compose educational language (KWP-015).

Never copy CMP. Never concatenate raw objectives. Never repeat syllabus
wording. Compose calm, professional tutor language grounded in
curriculum titles and knowledge-graph relationships only.
"""

from __future__ import annotations

import re

from app.application.educational_authoring.guidance import scrub

# Patterns that look like pasted CMP / syllabus dump language.
_CMP_MARKERS: tuple[str, ...] = (
    "cmp",
    "learning outcome",
    "candidates should",
    "the aim of this unit",
    "syllabus objective",
    "unit aim",
)

_STUDY_PREFIX = re.compile(
    r"^\s*(study|learn|cover|revise|read about)\s+",
    re.IGNORECASE,
)


def looks_like_cmp_dump(text: str) -> bool:
    """True when text resembles raw CMP / syllabus extract."""
    lowered = (text or "").strip().lower()
    if not lowered:
        return False
    if len(lowered) > 280 and ";" in lowered:
        return True
    return any(marker in lowered for marker in _CMP_MARKERS)


def compose_learning_objective(
    *,
    topic_title: str,
    objective_text: str = "",
    concept_titles: tuple[str, ...] = (),
) -> str:
    """One clear educational objective — not a CMP paragraph."""
    title = scrub(topic_title)
    if not title:
        return ""

    raw = scrub(objective_text)
    if raw and not looks_like_cmp_dump(raw) and len(raw) <= 160:
        cleaned = _STUDY_PREFIX.sub("", raw).rstrip(".")
        if cleaned and cleaned.lower() != title.lower():
            if cleaned[0].islower():
                cleaned = cleaned[0].upper() + cleaned[1:]
            if not cleaned.lower().startswith(
                ("explain", "solve", "apply", "derive", "identify", "complete")
            ):
                return scrub(f"Strengthen {title} by focusing on {cleaned}.")
            return scrub(cleaned if cleaned.endswith(".") else f"{cleaned}.")

    if concept_titles:
        focus = scrub(concept_titles[0])
        if focus and focus.lower() != title.lower():
            return scrub(
                f"Develop a working command of {focus} "
                f"as the foundation for {title}."
            )
    return scrub(
        f"Develop a clear, exam-ready understanding of {title}."
    )


def compose_educational_context(
    *,
    topic_title: str,
    prerequisite_titles: tuple[str, ...] = (),
    foundation_titles: tuple[str, ...] = (),
    successor_titles: tuple[str, ...] = (),
    recently_strengthened_titles: tuple[str, ...] = (),
) -> str:
    """Why today's work matters — authored tutor prose."""
    title = scrub(topic_title)
    if not title:
        return ""

    foundation = _first(
        foundation_titles, prerequisite_titles, recently_strengthened_titles
    )
    unlocks = _first(successor_titles)

    if foundation and unlocks:
        return scrub(
            f"Today's session develops the foundations required for "
            f"{unlocks}. You'll begin by strengthening {foundation} "
            f"reasoning before applying those ideas within {title}."
        )
    if foundation:
        recent = any(
            scrub(t).lower() == foundation.lower()
            for t in recently_strengthened_titles
        )
        if recent:
            return scrub(
                f"Today's session builds directly on {foundation}, which "
                f"you strengthened recently, and applies that foundation "
                f"to {title}."
            )
        return scrub(
            f"Today's session develops the foundations required for "
            f"{title}. You'll begin by strengthening {foundation} "
            f"before applying those ideas to today's work."
        )
    if unlocks:
        return scrub(
            f"Today's session develops the foundations required for "
            f"{unlocks}. You'll deepen {title} so later topics rest "
            f"on solid understanding."
        )
    return scrub(
        f"Today's session develops a careful, structured understanding "
        f"of {title}, preparing you for the next stage of the syllabus."
    )


def compose_connection(
    *,
    topic_title: str,
    tomorrow_title: str = "",
    successor_titles: tuple[str, ...] = (),
) -> str:
    """Why tomorrow builds on today."""
    title = scrub(topic_title)
    next_title = scrub(tomorrow_title) or _first(successor_titles)
    if title and next_title and next_title.lower() != title.lower():
        return scrub(
            f"Tomorrow builds directly on today's {title} work as you "
            f"move into {next_title}."
        )
    if title:
        return scrub(
            f"Tomorrow continues from today's {title} work, deepening "
            f"the same line of reasoning."
        )
    return scrub("Tomorrow continues from today's foundations.")


def compose_success_criteria(
    *,
    topic_title: str,
    concept_titles: tuple[str, ...] = (),
    objective_text: str = "",
) -> tuple[str, ...]:
    """Exact student-facing definition of finished."""
    title = scrub(topic_title)
    concepts = [scrub(c) for c in concept_titles if scrub(c)][:3]
    criteria: list[str] = []

    # Prefer a distinct concept — never "explain X within X" (V1S-008 trust).
    distinct = [c for c in concepts if c.lower() != title.lower()]
    if distinct:
        criteria.append(f"Explain the role of {distinct[0]} within {title}.")
        if len(distinct) >= 2:
            criteria.append(f"Solve a standard problem using {distinct[1]}.")
        else:
            criteria.append(f"Solve a standard problem involving {title}.")
    else:
        criteria.append(f"Explain the core ideas in {title} in your own words.")
        criteria.append(f"Solve a standard problem involving {title}.")

    obj = scrub(objective_text)
    if obj and not looks_like_cmp_dump(obj) and len(obj) <= 120:
        short = _STUDY_PREFIX.sub("", obj).rstrip(".")
        if short and short.lower() not in " ".join(criteria).lower():
            criteria.append(f"Complete: {short}.")
    else:
        criteria.append(f"Complete today's practice for {title}.")

    return tuple(scrub(c) for c in criteria[:4] if scrub(c))


def compose_mission_narrative(
    *,
    topic_title: str,
    educational_context: str,
) -> str:
    """Short mission-level authored summary (not topic dump)."""
    context = scrub(educational_context)
    if context:
        return context
    title = scrub(topic_title)
    if not title:
        return ""
    return scrub(
        f"Today's Mission is a carefully prepared session on {title}."
    )


def compose_checkpoint_prompt(*, topic_title: str) -> str:
    title = scrub(topic_title)
    if not title:
        return "Pause and check that today's objective is secure."
    return scrub(
        f"Checkpoint: can you explain {title} clearly and solve a "
        f"standard problem without notes?"
    )


def compose_reflection_prompt(*, topic_title: str) -> str:
    title = scrub(topic_title)
    if not title:
        return (
            "Note what became clearer today and what still needs "
            "careful attention."
        )
    return scrub(
        f"Reflect briefly: what in {title} is now clearer, and what "
        f"still needs careful attention?"
    )


def select_concept_focus(
    *,
    topic_title: str,
    concept_titles: tuple[str, ...] = (),
    prerequisite_titles: tuple[str, ...] = (),
    foundation_titles: tuple[str, ...] = (),
) -> tuple[str, ...]:
    """Ordered 2–5 concept focus list — curriculum-grounded only."""
    ordered: list[str] = []
    seen: set[str] = set()

    def _add(label: str) -> None:
        clean = scrub(label)
        key = clean.lower()
        if not clean or key in seen:
            return
        seen.add(key)
        ordered.append(clean)

    for title in concept_titles:
        _add(title)
        if len(ordered) >= 5:
            break

    if len(ordered) < 2:
        for title in foundation_titles:
            _add(title)
            if len(ordered) >= 5:
                break
    if len(ordered) < 2:
        for title in prerequisite_titles:
            _add(title)
            if len(ordered) >= 5:
                break

    topic = scrub(topic_title)
    if topic and topic.lower() not in seen:
        if len(ordered) < 2:
            ordered.insert(0, topic)
        elif len(ordered) < 5:
            ordered.append(topic)

    if len(ordered) == 1 and topic and ordered[0].lower() != topic.lower():
        ordered.append(topic)
    return tuple(ordered[:5])


def _first(*groups: tuple[str, ...]) -> str:
    for group in groups:
        for item in group:
            clean = scrub(item)
            if clean:
                return clean
    return ""
