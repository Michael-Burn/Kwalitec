"""Regression snapshots for Design System renderer HTML (V4-003)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from adapters.flask.rendering import ComponentRenderer
from presentation.dashboard.dashboard_view_model import AchievementView
from presentation.design_system import (
    Badge,
    MissionCard,
    PageHeader,
    ProgressBar,
    Section,
    StatisticTile,
    Timeline,
    TimelineItem,
    Tone,
    primary_button,
    secondary_button,
)
from presentation.design_system.components.cards import Card

SNAPSHOT_DIR = Path(__file__).resolve().parent / "snapshots"

_WHITESPACE_RE = re.compile(r"\s+")


def _normalise(html: str) -> str:
    """Collapse insignificant whitespace for stable snapshot comparison."""
    text = html.strip()
    text = _WHITESPACE_RE.sub(" ", text)
    text = text.replace("> <", "><")
    return text


def _assert_snapshot(name: str, html: str) -> None:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SNAPSHOT_DIR / f"{name}.html"
    normalised = _normalise(html)
    if not path.exists():
        path.write_text(normalised + "\n", encoding="utf-8")
    expected = _normalise(path.read_text(encoding="utf-8"))
    assert normalised == expected, (
        f"Snapshot drift for {name}. Update {path.name} if the change is intentional."
    )


@pytest.fixture
def renderer() -> ComponentRenderer:
    return ComponentRenderer()


def test_snapshot_page_header(renderer: ComponentRenderer) -> None:
    html = renderer.render_page_header(
        PageHeader(
            title="Learning Dashboard",
            description="Your next focused study step.",
            eyebrow="Today",
        )
    )
    _assert_snapshot("page_header", html)


def test_snapshot_mission_card(renderer: ComponentRenderer) -> None:
    html = renderer.render_mission_card(
        MissionCard(
            title="Review loss models",
            body="Complete the scheduled practice set.",
            eyebrow="Mission",
            duration_label="25 min",
            status_label="Ready",
        )
    )
    _assert_snapshot("mission_card", html)


def test_snapshot_section(renderer: ComponentRenderer) -> None:
    html = renderer.render_section(
        Section(title="Good afternoon", description="One clear next action.")
    )
    _assert_snapshot("section", html)


def test_snapshot_progress_bar(renderer: ComponentRenderer) -> None:
    html = renderer.render_progress_bar(
        ProgressBar(label="Plan progress", percent=40, value_text="40%")
    )
    _assert_snapshot("progress_bar", html)


def test_snapshot_badge(renderer: ComponentRenderer) -> None:
    html = renderer.render_badge(Badge(label="On track", tone=Tone.SUCCESS))
    _assert_snapshot("badge", html)


def test_snapshot_timeline(renderer: ComponentRenderer) -> None:
    html = renderer.render_timeline(
        Timeline(
            label="Session timeline",
            items=(
                TimelineItem(title="Start", active=True),
                TimelineItem(title="Practice"),
                TimelineItem(title="Reflect"),
            ),
        )
    )
    _assert_snapshot("timeline", html)


def test_snapshot_buttons(renderer: ComponentRenderer) -> None:
    primary = renderer.render_primary_button(primary_button("Start mission"))
    secondary = renderer.render_secondary_button(secondary_button("Review later"))
    _assert_snapshot("primary_button", primary)
    _assert_snapshot("secondary_button", secondary)


def test_snapshot_achievement_and_statistic(renderer: ComponentRenderer) -> None:
    achievement = renderer.render_achievement_card(
        AchievementView(
            title="First week complete",
            message="You finished seven planned sessions.",
            kind_label="Continuity",
            sequence=1,
            badge=Badge(label="Continuity", tone=Tone.SUCCESS),
            card=Card(
                title="First week complete",
                body="You finished seven planned sessions.",
                eyebrow="Continuity",
            ),
        )
    )
    statistic = renderer.render_statistic_card(
        StatisticTile(label="Sessions", value="12", detail="This plan")
    )
    _assert_snapshot("achievement_card", achievement)
    _assert_snapshot("statistic_card", statistic)


def test_snapshot_token_style_tag(renderer: ComponentRenderer) -> None:
    # Token values are authoritative; assert stable structural markers only.
    tag = renderer.token_style_tag()
    assert "<style data-ds-tokens>" in tag
    assert ":root {" in tag
    assert "--primary:" in tag
    assert "prefers-reduced-motion" in tag
    _assert_snapshot("token_style_tag_markers", "\n".join(
        line.strip()
        for line in tag.splitlines()
        if line.strip().startswith(
            ("<style", ":root", "@media", ".ds-container", "</style")
        )
        or "--primary:" in line
        or "prefers-reduced-motion" in line
    ))
