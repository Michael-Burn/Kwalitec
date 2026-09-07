"""Prepare session-facing text for KaTeX auto-render.

Educational packages store mathematics as Unicode / actuarial notation, with
Wave 1 (and later) migrated strings wrapping real LaTeX in $...$ delimiters.
This module leaves genuine $...$ / $$...$$ content unchanged so KaTeX
auto-render can typeset it, and wraps only remaining bare superscript
fragments (e^{−λx}) at presentation time.
"""

from __future__ import annotations

import re

from app.presentation.session.content_sections import ContentSection
from app.presentation.session.dto.study_session import StudySessionPage

# Bare superscript fragments authored without $...$ delimiters.
_BARE_LATEX_FRAGMENT = re.compile(
    r"(?<!\$)"
    r"(?:"
    r"e\^\{(?P<eexp>[^{}]+)\}"
    r"|"
    r"(?P<id>[A-Za-zλμθηβΣℓ]+)\^\{(?P<idexp>[^{}]+)\}"
    r"|"
    r"(?P<id2>[A-Za-zλμθηβΣℓ]+)\^(?P<sup>[0-9]+)"
    r")"
    r"(?!\$)"
)


def prepare_math_markup(text: str) -> str:
    """Wrap bare LaTeX superscript fragments in inline math delimiters."""
    if not text or "$" in text:
        return text

    def _wrap(match: re.Match[str]) -> str:
        return f"${match.group(0)}$"

    return _BARE_LATEX_FRAGMENT.sub(_wrap, text)


def _markup_section(section: ContentSection) -> ContentSection:
    return ContentSection(
        label=section.label,
        paragraphs=tuple(prepare_math_markup(p) for p in section.paragraphs),
        bullets=tuple(prepare_math_markup(b) for b in section.bullets),
    )


def apply_math_markup(page: StudySessionPage) -> StudySessionPage:
    """Apply math delimiter normalization to learner-visible session strings."""
    from dataclasses import replace

    sections = tuple(_markup_section(s) for s in page.content_sections)
    sections_more = tuple(_markup_section(s) for s in page.content_sections_more)
    choices = tuple(
        (cid, prepare_math_markup(label)) for cid, label in page.practice_choices
    )

    return replace(
        page,
        content_body=prepare_math_markup(page.content_body),
        content_support=prepare_math_markup(page.content_support),
        content_intro_line=prepare_math_markup(page.content_intro_line),
        content_sections=sections,
        content_sections_more=sections_more,
        answer_prompt=prepare_math_markup(page.answer_prompt),
        feedback_explanation=prepare_math_markup(page.feedback_explanation),
        model_answer=prepare_math_markup(page.model_answer),
        common_mistake=prepare_math_markup(page.common_mistake),
        feedback_next_action=prepare_math_markup(page.feedback_next_action),
        feedback_what_happened=prepare_math_markup(page.feedback_what_happened),
        feedback_what_it_means=prepare_math_markup(page.feedback_what_it_means),
        feedback_what_to_understand=prepare_math_markup(
            page.feedback_what_to_understand
        ),
        submitted_response=prepare_math_markup(page.submitted_response),
        practice_choices=choices,
    )
