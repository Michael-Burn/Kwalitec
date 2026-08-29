"""Guided Reading body assembly and Session content-section rendering."""

from __future__ import annotations

from app.application.educational_packages.loader import find_package_by_id
from app.application.educational_packages.substance import substance_from_package
from app.presentation.session.content_sections import (
    parse_session_content_body,
    present_practice_content,
    present_reading_content,
    present_worked_example_content,
    strip_author_voice,
)

_AUTHOR_VOICE = (
    "Kwalitec is the guide; the CMP is the authoritative material. "
    "Do not treat this activity body as a substitute textbook"
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


def test_present_reading_content_trims_to_essentials() -> None:
    body = "\n".join(
        [
            "Topic: t-statistic (2.6)",
            "Mission: Describe the t-statistic",
            "",
            "Open the CMP:",
            "• Open your CMP at Syllabus 2.6.5",
            "",
            "Focus questions:",
            "• What is the core move?",
            "",
            "Misconception watch:",
            "• Watch for using z when S replaces σ",
            "",
            "While you read:",
            "• Sketch the chain",
            "",
            "Out of scope today:",
            "• F distribution",
            "",
            "When you finish:",
            "• Close the CMP",
        ]
    )
    presented = present_reading_content(parse_session_content_body(body))
    assert presented.intro_line == "Mission: Describe the t-statistic"
    assert [s.label for s in presented.primary] == ["Open the CMP", "Focus questions"]
    assert [s.label for s in presented.more] == [
        "Misconception watch",
        "While you read",
        "Out of scope today",
        "When you finish",
    ]


def test_present_practice_content_shows_question_once() -> None:
    presented = present_practice_content(
        prompt="Closed-book. Name today's stop condition.",
        body="Checkpoint refuse/warrant for 2.6.5.",
    )
    assert len(presented.primary) == 2
    assert presented.primary[0].label == "Question"
    assert "stop condition" in presented.primary[0].paragraphs[0]
    assert presented.primary[1].label == "Focus"
    # Identical stub is dropped
    same = present_practice_content(
        prompt="Closed-book. Name today's stop.",
        body="Closed-book. Name today's stop.",
    )
    assert len(same.primary) == 1
    assert same.primary[0].label == "Question"


def test_present_worked_example_content_splits_essentials() -> None:
    body = "\n".join(
        [
            "Re-enter with the CMP closed.",
            "",
            "Confirm your structure sketch:",
            "• Concept focus: t",
            "",
            "Pause-point harvest:",
            "• PP1: df",
            "",
            "Success criteria you will stress-test next:",
            "• Name t vs z",
            "",
            "Before you continue:",
            "• Keep the CMP closed for retrieval.",
        ]
    )
    presented = present_worked_example_content(parse_session_content_body(body))
    assert "Re-enter" in presented.intro_line
    assert [s.label for s in presented.primary] == [
        "Confirm your structure sketch",
        "Pause-point harvest",
    ]
    assert [s.label for s in presented.more] == [
        "Success criteria you will stress-test next",
        "Before you continue",
    ]


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
    presented = present_reading_content(sections)
    assert presented.intro_line.startswith("Mission:")
    assert "Topic:" not in presented.intro_line
    assert {s.label for s in presented.primary} == {"Open the CMP", "Focus questions"}
    assert "Misconception watch" in {s.label for s in presented.more}
    assert "When you finish" in {s.label for s in presented.more}


def test_cs1009_2_6_5_worked_example_body_is_structured() -> None:
    pack = find_package_by_id("CS1-EP001-PKG-2.6-T-STATISTIC")
    assert pack is not None
    substance = substance_from_package(
        pack, curriculum_identity="cs1-test", topic_id="t1"
    )
    example = next(
        a for a in substance.activities if a.activity_id == "act-example-1"
    )
    assert example.supporting_material == ""
    assert "Confirm your structure sketch:" not in example.body
    assert dict(example.metadata).get("worked_example_kind") == "numeric"
    assert "t = 2.5" in example.body
    assert "15" in example.body
    presented = present_worked_example_content(
        parse_session_content_body(example.body)
    )
    assert presented.primary
    assert presented.more


def test_cs1009_2_6_5_checkpoint_prompt_has_subject() -> None:
    pack = find_package_by_id("CS1-EP001-PKG-2.6-T-STATISTIC")
    assert pack is not None
    checkpoint = next(
        c for c in pack.knowledge_checks if "Checkpoint" in (c.title or "")
    )
    assert "Refuse 't finished" not in checkpoint.prompt
    assert "The t-statistic finished" in checkpoint.prompt
