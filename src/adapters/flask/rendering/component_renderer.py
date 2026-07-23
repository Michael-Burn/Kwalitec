"""ComponentRenderer — Design System contracts → reusable HTML.

Renders presentation components and view-model fragments into HTML strings.
Uses Jinja templates under ``templates/components/`` as the reusable markup
source of truth for Flask includes, while remaining Flask-import free.
"""

from __future__ import annotations

from dataclasses import is_dataclass
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from adapters.flask.rendering.accessibility_renderer import AccessibilityRenderer
from adapters.flask.rendering.html_helpers import escape, join_classes
from adapters.flask.rendering.style_renderer import StyleRenderer
from adapters.flask.rendering.token_renderer import TokenRenderer
from presentation.dashboard.dashboard_view_model import (
    AchievementView,
    DashboardViewModel,
)
from presentation.design_system import (
    Badge,
    Button,
    ButtonVariant,
    EmptyState,
    LoadingState,
    MissionCard,
    PageHeader,
    ProgressBar,
    Section,
    Skeleton,
    StatisticTile,
    Timeline,
    Toast,
    primary_button,
    secondary_button,
)
from presentation.design_system.components.base import (
    AccessibilityContract,
    StyleContract,
)
from presentation.provenance import ProvenanceViewModel

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
COMPONENT_TEMPLATE_DIR = TEMPLATES_DIR / "components"

COMPONENT_TEMPLATES = {
    "page_header": "components/page_header.html",
    "mission_card": "components/mission_card.html",
    "section": "components/section.html",
    "progress_bar": "components/progress_bar.html",
    "badge": "components/badge.html",
    "timeline": "components/timeline.html",
    "primary_button": "components/primary_button.html",
    "secondary_button": "components/secondary_button.html",
    "achievement_card": "components/achievement_card.html",
    "statistic_card": "components/statistic_card.html",
    "empty_state": "components/empty_state.html",
    "skeleton": "components/skeleton.html",
    "toast": "components/toast.html",
    "loading_state": "components/loading_state.html",
    "provenance": "components/provenance.html",
}


class ComponentRenderer:
    """Render Design System components and view models into HTML."""

    def __init__(
        self,
        *,
        style_renderer: StyleRenderer | None = None,
        accessibility_renderer: AccessibilityRenderer | None = None,
        token_renderer: TokenRenderer | None = None,
        templates_dir: Path | None = None,
    ) -> None:
        self.styles = style_renderer or StyleRenderer()
        self.a11y = accessibility_renderer or AccessibilityRenderer()
        self.tokens = token_renderer or TokenRenderer()
        self._token_style_cache: str | None = None
        root = templates_dir or TEMPLATES_DIR
        self._env = Environment(
            loader=FileSystemLoader(str(root)),
            autoescape=select_autoescape(enabled_extensions=("html", "htm")),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, component: Any) -> str:
        """Dispatch a Design System / presentation object to HTML."""
        if isinstance(component, PageHeader):
            return self.render_page_header(component)
        if isinstance(component, MissionCard):
            return self.render_mission_card(component)
        if isinstance(component, Section):
            return self.render_section(component)
        if isinstance(component, ProgressBar):
            return self.render_progress_bar(component)
        if isinstance(component, Badge):
            return self.render_badge(component)
        if isinstance(component, Timeline):
            return self.render_timeline(component)
        if isinstance(component, Button):
            return self.render_button(component)
        if isinstance(component, AchievementView):
            return self.render_achievement_card(component)
        if isinstance(component, StatisticTile):
            return self.render_statistic_card(component)
        if isinstance(component, EmptyState):
            return self.render_empty_state(component)
        if isinstance(component, Skeleton):
            return self.render_skeleton(component)
        if isinstance(component, Toast):
            return self.render_toast(component)
        if isinstance(component, LoadingState):
            return self.render_loading_state(component)
        if isinstance(component, ProvenanceViewModel):
            return self.render_provenance(component)
        if isinstance(component, DashboardViewModel):
            return self.render_view_model(component)
        raise TypeError(
            f"Unsupported component type for rendering: {type(component)!r}"
        )

    def render_view_model(self, view_model: Any) -> str:
        """Render a presentation view model by composing known components."""
        if isinstance(view_model, DashboardViewModel):
            return self._render_dashboard(view_model)
        if is_dataclass(view_model) and not isinstance(view_model, type):
            parts: list[str] = []
            for field_name in view_model.__dataclass_fields__:  # type: ignore[attr-defined]
                value = getattr(view_model, field_name)
                if self._is_renderable(value):
                    parts.append(self.render(value))
                elif isinstance(value, tuple):
                    for item in value:
                        if self._is_renderable(item):
                            parts.append(self.render(item))
            return "\n".join(parts)
        raise TypeError(
            f"Unsupported view model type for rendering: {type(view_model)!r}"
        )

    def render_page_header(self, header: PageHeader) -> str:
        return self._render_template(
            "page_header",
            component=header,
            **self._chrome(header, class_name="ds-page-header", label=header.title),
        )

    def render_mission_card(self, card: MissionCard) -> str:
        return self._render_template(
            "mission_card",
            component=card,
            **self._chrome(card, class_name="ds-mission-card", label=card.title),
        )

    def render_section(self, section: Section) -> str:
        return self._render_template(
            "section",
            component=section,
            **self._chrome(section, class_name="ds-section", label=section.title),
        )

    def render_progress_bar(self, bar: ProgressBar) -> str:
        style = bar.style()
        a11y = bar.accessibility()
        attrs = self.a11y.attributes(
            a11y,
            label=bar.label,
            valuenow=bar.percent,
            valuetext=bar.value_text or f"{int(round(bar.percent))}%",
        )
        return self._render_template(
            "progress_bar",
            component=bar,
            class_name=join_classes("ds-component", "ds-progress-bar"),
            style_attr=self.styles.inline_style(style),
            a11y_attrs=attrs,
            percent=bar.percent,
        )

    def render_badge(self, badge: Badge) -> str:
        return self._render_template(
            "badge",
            component=badge,
            **self._chrome(badge, class_name="ds-badge", label=badge.label),
        )

    def render_timeline(self, timeline: Timeline) -> str:
        return self._render_template(
            "timeline",
            component=timeline,
            **self._chrome(
                timeline,
                class_name="ds-timeline",
                label=timeline.label,
            ),
        )

    def render_button(self, button: Button) -> str:
        if button.variant == ButtonVariant.PRIMARY:
            return self.render_primary_button(button)
        if button.variant == ButtonVariant.SECONDARY:
            return self.render_secondary_button(button)
        class_name = f"ds-btn-{button.variant.value}"
        return self._render_button_variant(button, class_name=class_name)

    def render_primary_button(
        self, button: Button | None = None, *, label: str = ""
    ) -> str:
        target = button or primary_button(label or "Continue")
        return self._render_template(
            "primary_button",
            component=target,
            **self._button_context(target, class_name="ds-btn-primary"),
        )

    def render_secondary_button(
        self, button: Button | None = None, *, label: str = ""
    ) -> str:
        target = button or secondary_button(label or "Back")
        return self._render_template(
            "secondary_button",
            component=target,
            **self._button_context(target, class_name="ds-btn-secondary"),
        )

    def render_achievement_card(self, achievement: AchievementView) -> str:
        card = achievement.card
        style = card.style() if card is not None else StyleContract()
        a11y = (
            card.accessibility()
            if card is not None
            else AccessibilityContract(role="region", label_required=True)
        )
        if achievement.badge is not None:
            badge_html = self.render_badge(achievement.badge)
        else:
            badge_html = ""
        attrs = self.a11y.attributes(a11y, label=achievement.title)
        return self._render_template(
            "achievement_card",
            component=achievement,
            class_name=join_classes("ds-component", "ds-achievement-card"),
            style_attr=self.styles.inline_style(style),
            a11y_attrs=attrs,
            badge_html=badge_html,
        )

    def render_statistic_card(self, tile: StatisticTile) -> str:
        return self._render_template(
            "statistic_card",
            component=tile,
            **self._chrome(tile, class_name="ds-statistic-card", label=tile.label),
        )

    def render_empty_state(self, empty: EmptyState) -> str:
        return self._render_template(
            "empty_state",
            component=empty,
            **self._chrome(empty, class_name="ds-empty-state", label=empty.title),
        )

    def render_skeleton(self, skeleton: Skeleton) -> str:
        return self._render_template(
            "skeleton",
            component=skeleton,
            **self._chrome(
                skeleton, class_name="ds-skeleton", label=skeleton.label
            ),
        )

    def render_toast(self, toast: Toast) -> str:
        return self._render_template(
            "toast",
            component=toast,
            **self._chrome(toast, class_name="ds-toast", label=toast.message),
        )

    def render_loading_state(self, loading: LoadingState) -> str:
        return self._render_template(
            "loading_state",
            component=loading,
            **self._chrome(loading, class_name="ds-loading-state", label=loading.label),
        )

    def render_provenance(self, provenance: ProvenanceViewModel | None) -> str:
        """Render expandable provenance reasons — empty string when unavailable."""
        if provenance is None or not provenance.available:
            return ""
        accordion = provenance.as_accordion()
        style = accordion.style()
        a11y = accordion.accessibility()
        return self._render_template(
            "provenance",
            provenance=provenance,
            class_name=join_classes("ds-component", "eos-provenance"),
            style_attr=self.styles.inline_style(style),
            a11y_attrs=self.a11y.attributes(a11y, label=provenance.title),
        )

    def token_style_tag(self) -> str:
        """Expose Design System CSS variables for embedding beside components.

        Cached per renderer instance to avoid duplicate token stylesheet work
        across fragment renders in one page assembly (PX-004).
        """
        if self._token_style_cache is None:
            self._token_style_cache = self.tokens.style_tag()
        return self._token_style_cache

    def template_path(self, key: str) -> Path:
        """Return the filesystem path for a named component template."""
        relative = COMPONENT_TEMPLATES[key]
        return TEMPLATES_DIR / relative

    def _render_dashboard(self, view: DashboardViewModel) -> str:
        parts = [
            self.token_style_tag(),
            self.render_page_header(view.header),
        ]
        if view.greeting is not None:
            parts.append(self.render_section(view.greeting))
        mission = view.mission_card or (
            view.hero.mission_card if view.hero is not None else None
        )
        if mission is not None:
            parts.append(self.render_mission_card(mission))
        action = view.primary_action or (
            view.hero.primary_action if view.hero is not None else None
        )
        if action is not None:
            parts.append(self.render_button(action))
        if view.progress_bar is not None:
            parts.append(self.render_progress_bar(view.progress_bar))
        # PX-003: decision screen does not render statistic / achievement grids.
        return "\n".join(parts)

    def _chrome(
        self,
        component: Any,
        *,
        class_name: str,
        label: str,
    ) -> dict[str, Any]:
        style = component.style()
        a11y = component.accessibility()
        return {
            "class_name": join_classes("ds-component", class_name),
            "style_attr": self.styles.inline_style(style),
            "a11y_attrs": self.a11y.attributes(a11y, label=label),
        }

    def _button_context(self, button: Button, *, class_name: str) -> dict[str, Any]:
        style = button.style()
        a11y = button.accessibility()
        attrs = self.a11y.attributes(
            a11y,
            label=button.label,
            disabled=button.disabled,
            extra={"type": "button", "disabled": button.disabled or None},
        )
        return {
            "class_name": join_classes("ds-component", "ds-btn", class_name),
            "style_attr": self.styles.inline_style(style),
            "a11y_attrs": attrs,
        }

    def _render_button_variant(self, button: Button, *, class_name: str) -> str:
        context = self._button_context(button, class_name=class_name)
        disabled_attr = " disabled" if button.disabled else ""
        attrs = " ".join(
            f'{key}="{escape(value)}"'
            for key, value in context["a11y_attrs"].items()
            if value is not None and value is not False and key != "disabled"
        )
        style = context["style_attr"]
        return (
            f'<button class="{context["class_name"]}" style="{style}" '
            f"{attrs}{disabled_attr}>{escape(button.label)}</button>"
        )

    def _render_template(self, key: str, **context: Any) -> str:
        template_name = COMPONENT_TEMPLATES[key]
        return self._env.get_template(template_name).render(**context).strip()

    @staticmethod
    def _is_renderable(value: Any) -> bool:
        return isinstance(
            value,
            PageHeader
            | MissionCard
            | Section
            | ProgressBar
            | Badge
            | Timeline
            | Button
            | AchievementView
            | StatisticTile
            | EmptyState
            | Skeleton
            | Toast
            | LoadingState
            | ProvenanceViewModel
            | DashboardViewModel,
        )
