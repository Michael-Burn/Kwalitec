"""Shared fixtures for Design System renderer tests (V4-003)."""

from __future__ import annotations

import pytest

from adapters.flask.rendering import (
    AccessibilityRenderer,
    ComponentRenderer,
    StyleRenderer,
    TokenRenderer,
)
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


@pytest.fixture
def style_renderer() -> StyleRenderer:
    return StyleRenderer()


@pytest.fixture
def token_renderer() -> TokenRenderer:
    return TokenRenderer()


@pytest.fixture
def accessibility_renderer() -> AccessibilityRenderer:
    return AccessibilityRenderer()


@pytest.fixture
def component_renderer(
    style_renderer: StyleRenderer,
    accessibility_renderer: AccessibilityRenderer,
    token_renderer: TokenRenderer,
) -> ComponentRenderer:
    return ComponentRenderer(
        style_renderer=style_renderer,
        accessibility_renderer=accessibility_renderer,
        token_renderer=token_renderer,
    )


@pytest.fixture
def page_header() -> PageHeader:
    return PageHeader(
        title="Learning Dashboard",
        description="Your next focused study step.",
        eyebrow="Today",
    )


@pytest.fixture
def mission_card() -> MissionCard:
    return MissionCard(
        title="Review loss models",
        body="Complete the scheduled practice set.",
        eyebrow="Mission",
        duration_label="25 min",
        status_label="Ready",
    )


@pytest.fixture
def section() -> Section:
    return Section(
        title="Good afternoon",
        description="One clear next action.",
        eyebrow="Greeting",
    )


@pytest.fixture
def progress_bar() -> ProgressBar:
    return ProgressBar(label="Plan progress", percent=42.5, value_text="43%")


@pytest.fixture
def badge() -> Badge:
    return Badge(label="On track", tone=Tone.SUCCESS)


@pytest.fixture
def timeline() -> Timeline:
    return Timeline(
        label="Session timeline",
        items=(
            TimelineItem(title="Start", detail="Open resources", active=True),
            TimelineItem(title="Practice", detail="Work the set"),
            TimelineItem(title="Reflect", timestamp_label="End"),
        ),
    )


@pytest.fixture
def achievement() -> AchievementView:
    return AchievementView(
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


@pytest.fixture
def statistic() -> StatisticTile:
    return StatisticTile(label="Sessions", value="12", detail="This plan")


@pytest.fixture
def primary_btn():
    return primary_button("Start mission")


@pytest.fixture
def secondary_btn():
    return secondary_button("Review later")
