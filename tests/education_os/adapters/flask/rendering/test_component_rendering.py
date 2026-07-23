"""HTML and component rendering tests for V4-003."""

from __future__ import annotations

import pytest

from adapters.flask.rendering import ComponentRenderer
from presentation.dashboard import DashboardPresenter
from presentation.design_system import (
    Badge,
    MissionCard,
    PageHeader,
    ProgressBar,
    Section,
    StatisticTile,
    Timeline,
    primary_button,
    secondary_button,
)


def test_render_page_header(
    component_renderer: ComponentRenderer,
    page_header: PageHeader,
) -> None:
    html = component_renderer.render_page_header(page_header)
    assert 'class="ds-component ds-page-header"' in html
    assert "<h1" in html
    assert "Learning Dashboard" in html
    assert 'role="banner"' in html
    assert 'aria-label="Learning Dashboard"' in html


def test_render_mission_card(
    component_renderer: ComponentRenderer, mission_card: MissionCard
) -> None:
    html = component_renderer.render_mission_card(mission_card)
    assert "ds-mission-card" in html
    assert "Review loss models" in html
    assert "25 min" in html
    assert 'role="region"' in html


def test_render_section(
    component_renderer: ComponentRenderer,
    section: Section,
) -> None:
    html = component_renderer.render_section(section)
    assert "ds-section" in html
    assert "Good afternoon" in html
    assert 'role="region"' in html


def test_render_progress_bar(
    component_renderer: ComponentRenderer, progress_bar: ProgressBar
) -> None:
    html = component_renderer.render_progress_bar(progress_bar)
    assert "ds-progress-bar" in html
    assert 'role="progressbar"' in html
    assert 'aria-valuenow="42"' in html or 'aria-valuenow="43"' in html
    assert 'aria-valuemin="0"' in html
    assert 'aria-valuemax="100"' in html
    assert "width: 42.5%" in html


def test_render_badge(component_renderer: ComponentRenderer, badge: Badge) -> None:
    html = component_renderer.render_badge(badge)
    assert "ds-badge" in html
    assert "On track" in html
    assert 'role="status"' in html
    assert "ds-badge--success" in html


def test_render_timeline(
    component_renderer: ComponentRenderer,
    timeline: Timeline,
) -> None:
    html = component_renderer.render_timeline(timeline)
    assert "ds-timeline" in html
    assert "<ol" in html
    assert "Start" in html
    assert 'aria-current="step"' in html
    assert 'role="list"' in html


def test_render_primary_and_secondary_buttons(
    component_renderer: ComponentRenderer,
) -> None:
    primary = component_renderer.render_primary_button(
        primary_button("Start mission")
    )
    secondary = component_renderer.render_secondary_button(
        secondary_button("Review later")
    )
    assert "ds-btn-primary" in primary
    assert "Start mission" in primary
    assert 'role="button"' in primary
    assert "ds-btn-secondary" in secondary
    assert "Review later" in secondary


def test_render_achievement_and_statistic(
    component_renderer: ComponentRenderer,
    achievement,
    statistic: StatisticTile,
) -> None:
    achievement_html = component_renderer.render_achievement_card(achievement)
    statistic_html = component_renderer.render_statistic_card(statistic)
    assert "ds-achievement-card" in achievement_html
    assert "First week complete" in achievement_html
    assert "ds-badge" in achievement_html
    assert "ds-statistic-card" in statistic_html
    assert "Sessions" in statistic_html
    assert "12" in statistic_html


def test_render_dispatch(
    component_renderer: ComponentRenderer,
    page_header: PageHeader,
) -> None:
    html = component_renderer.render(page_header)
    assert "Learning Dashboard" in html


def test_render_view_model_dashboard(component_renderer: ComponentRenderer) -> None:
    view = DashboardPresenter.present(None)
    html = component_renderer.render_view_model(view)
    assert "data-ds-tokens" in html
    assert "ds-page-header" in html
    assert "ds-mission-card" in html
    assert "ds-progress-bar" in html
    # PX-003 / PX-004: decision screen does not render statistic grids.
    assert "ds-statistic-card" not in html
    assert "ds-achievement-card" not in html


def test_html_escapes_user_facing_text(component_renderer: ComponentRenderer) -> None:
    header = PageHeader(title='<script>alert("x")</script>', description="A & B")
    html = component_renderer.render_page_header(header)
    assert "<script>" not in html
    assert "&lt;script&gt;" in html
    assert "A &amp; B" in html


def test_style_contracts_emit_css_variables(
    component_renderer: ComponentRenderer, mission_card: MissionCard
) -> None:
    html = component_renderer.render_mission_card(mission_card)
    assert "style=" in html
    assert "var(--" in html


@pytest.mark.parametrize(
    "method_name",
    [
        "render_page_header",
        "render_mission_card",
        "render_section",
        "render_progress_bar",
        "render_badge",
        "render_timeline",
        "render_primary_button",
        "render_secondary_button",
        "render_achievement_card",
        "render_statistic_card",
    ],
)
def test_component_templates_exist(
    component_renderer: ComponentRenderer,
    method_name: str,
) -> None:
    key = method_name.removeprefix("render_")
    path = component_renderer.template_path(key)
    assert path.is_file()
    assert path.read_text(encoding="utf-8").strip()
