"""Guided Reading body assembly and Session content-section rendering."""

from __future__ import annotations

from app.application.educational_packages.loader import find_package_by_id
from app.application.educational_packages.substance import substance_from_package
from app.presentation.session.content_sections import (
    parse_session_content_body,
    strip_author_voice,
)

_AUTHOR_VOICE = (
    "Kwalitec is the guide; the CMP is the authoritative material — "
    "do not treat this activity body as a substitute textbook"
)


def test_strip_author_voice_removes_cmp_guide_commentary() -> None:
    raw = (
        "Open your CMP at 2.6.5. "
        f"{_AUTHOR_VOICE}. "
        "Hunt with the focus questions."
    )
    cleaned = strip_author_voice(raw)
    assert "substitute textbook" not in cleaned
    assert "Kwalitec is the guide" not in cleaned
    assert "Open your CMP at 2.6.5" in cleaned


def test_parse_session_content_body_builds_labelled_lists() -> None:
    body = "\n".join(
        [
            "Topic: t-statistic (2.6)",
            "Mission: Describe the t-statistic",
            "",
            "Open the CMP:",
            "• Open your CMP at Syllabus 2.6.5",
            "• Stop when: Through CMP 2.6.5",
            "",
            "Focus questions:",
            "• What is the core move?",
            "• What claim must you refuse?",
            "",
            "Misconception watch:",
            "• Watch for using z when S replaces σ",
        ]
    )
    sections = parse_session_content_body(body)
    assert sections
    labels = [s.label for s in sections if s.label]
    assert "Open the CMP" in labels
    assert "Focus questions" in labels
    assert "Misconception watch" in labels
    focus = next(s for s in sections if s.label == "Focus questions")
    assert len(focus.bullets) == 2
    assert focus.bullets[0].startswith("What is the core move")


def test_cs1009_2_6_5_reading_body_has_no_exit_line_duplication() -> None:
    pack = find_package_by_id("CS1-EP001-PKG-2.6-T-STATISTIC")
    assert pack is not None
    assert "2.6.5" in pack.topic_aliases
    substance = substance_from_package(
        pack, curriculum_identity="cs1-test", topic_id="t1"
    )
    reading = next(
        a for a in substance.activities if a.activity_id == "act-read-1"
    )
    body = reading.body or ""
    assert "substitute textbook" not in body
    assert "Kwalitec is the guide" not in body
    assert body.count("Open your CMP") <= 1
    assert "Focus questions:" in body
    assert "Misconception watch:" in body
    assert "Out of scope today:" in body
    # exit_line must not be appended or mirrored as supporting material
    assert reading.supporting_material == ""
    assert pack.reading.exit_line
    assert pack.reading.exit_line not in body
    sections = parse_session_content_body(body)
    assert any(s.label == "Focus questions" and s.bullets for s in sections)
