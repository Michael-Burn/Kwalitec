"""Timeline ordering for the Study Session Runner (V3-003)."""

from __future__ import annotations

from presentation.study_session import (
    SECTION_ORDER,
    SessionSectionView,
    SessionTimeline,
)


def test_section_order_matches_milestone_sections() -> None:
    assert SECTION_ORDER == (
        "mission_header",
        "mission_objective",
        "educational_explanation",
        "estimated_duration",
        "learning_resources",
        "worked_example",
        "progress_indicator",
        "study_notes",
        "reflection_prompt",
        "completion_summary",
        "next_step",
    )
    assert SessionTimeline.section_keys() == SECTION_ORDER


def test_order_sections_sorts_into_canonical_order() -> None:
    shuffled = (
        SessionSectionView(key="next_step", title="Next"),
        SessionSectionView(key="mission_objective", title="Objective"),
        SessionSectionView(key="mission_header", title="Header"),
        SessionSectionView(key="reflection_prompt", title="Reflect"),
    )
    ordered = SessionTimeline.order_sections(shuffled)
    assert [section.key for section in ordered] == [
        "mission_header",
        "mission_objective",
        "reflection_prompt",
        "next_step",
    ]


def test_order_sections_appends_unknown_keys_last() -> None:
    sections = (
        SessionSectionView(key="zz_extra", title="Extra"),
        SessionSectionView(key="mission_header", title="Header"),
        SessionSectionView(key="aa_bonus", title="Bonus"),
    )
    ordered = SessionTimeline.order_sections(sections)
    assert [section.key for section in ordered] == [
        "mission_header",
        "aa_bonus",
        "zz_extra",
    ]


def test_build_timeline_marks_active_item() -> None:
    sections = tuple(
        SessionSectionView(key=key, title=SessionTimeline.title_for(key), body=key)
        for key in SECTION_ORDER
    )
    timeline = SessionTimeline.build_timeline(
        sections, active_key="learning_resources"
    )
    assert len(timeline.items) == len(SECTION_ORDER)
    active = [item for item in timeline.items if item.active]
    assert len(active) == 1
    assert active[0].title == SessionTimeline.title_for("learning_resources")


def test_build_stepper_marks_complete_and_current() -> None:
    sections = tuple(
        SessionSectionView(key=key, title=SessionTimeline.title_for(key))
        for key in SECTION_ORDER[:4]
    )
    stepper = SessionTimeline.build_stepper(
        sections, current_key="educational_explanation"
    )
    assert stepper.current_index() == 2
    assert stepper.steps[0].complete is True
    assert stepper.steps[1].complete is True
    assert stepper.steps[2].current is True
    assert stepper.steps[3].complete is False
    assert stepper.steps[3].current is False


def test_progress_percent_from_section_position() -> None:
    sections = tuple(
        SessionSectionView(key=key, title=key) for key in SECTION_ORDER
    )
    assert (
        SessionTimeline.progress_percent(sections, current_key="mission_header")
        == 0.0
    )
    mid = SessionTimeline.progress_percent(
        sections, current_key="progress_indicator"
    )
    assert 0.0 < mid < 100.0
    assert (
        SessionTimeline.progress_percent(sections, current_key="next_step") == 100.0
    )


def test_empty_sections_are_safe() -> None:
    assert SessionTimeline.order_sections(()) == ()
    timeline = SessionTimeline.build_timeline(())
    stepper = SessionTimeline.build_stepper(())
    assert timeline.items == ()
    assert stepper.steps == ()
    assert SessionTimeline.progress_percent(()) == 0.0
