"""Component purity — tokenised styles, no duplicated variants, no logic."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from presentation.design_system import (
    Accordion,
    AccordionPanel,
    Badge,
    ButtonVariant,
    Card,
    Chip,
    Divider,
    EmptyState,
    LoadingState,
    MissionCard,
    Modal,
    PageHeader,
    ProgressBar,
    ProgressCard,
    ProgressRing,
    RecommendationCard,
    Section,
    Skeleton,
    StatisticTile,
    Stepper,
    StepperStep,
    Tag,
    Timeline,
    TimelineItem,
    Toast,
    danger_button,
    ghost_button,
    primary_button,
    secondary_button,
)
from presentation.design_system.colours import SemanticColour
from presentation.design_system.components.base import StyleContract

COMPONENTS_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "presentation"
    / "design_system"
    / "components"
)


def _components():
    return {
        "primary_button": primary_button("Continue"),
        "secondary_button": secondary_button("Cancel"),
        "danger_button": danger_button("Delete"),
        "ghost_button": ghost_button("Skip"),
        "card": Card(title="Overview", body="Detail"),
        "mission_card": MissionCard(title="Today's mission", body="Study CS1"),
        "recommendation_card": RecommendationCard(title="Revise", reason_label="Gap"),
        "progress_card": ProgressCard(title="Progress", metric_label="62%"),
        "section": Section(title="Journey"),
        "page_header": PageHeader(title="Home"),
        "statistic_tile": StatisticTile(label="Readiness", value="72%"),
        "progress_ring": ProgressRing(label="Coverage", percent=40),
        "progress_bar": ProgressBar(label="Session", percent=55),
        "badge": Badge(label="Priority"),
        "chip": Chip(label="CS1"),
        "tag": Tag(label="Exam"),
        "divider": Divider(),
        "timeline": Timeline(items=(TimelineItem(title="Started"),)),
        "stepper": Stepper(steps=(StepperStep(label="One", current=True),)),
        "accordion": Accordion(panels=(AccordionPanel(title="Why", body="Because"),)),
        "modal": Modal(title="Confirm", body="Proceed?"),
        "toast": Toast(message="Saved"),
        "empty_state": EmptyState(title="Nothing here"),
        "loading_state": LoadingState(),
        "skeleton": Skeleton(),
    }


@pytest.mark.parametrize("name", list(_components()))
def test_component_exposes_style_contract(name: str) -> None:
    component = _components()[name]
    style = component.style()
    assert isinstance(style, StyleContract)
    # Tokenised via enum fields and/or named extras
    has_tokens = bool(style.token_names()) or any(
        getattr(style, field) is not None
        for field in (
            "background",
            "foreground",
            "border",
            "typography",
            "padding_x",
            "padding_y",
            "gap",
            "radius",
            "elevation",
            "motion",
        )
    )
    assert has_tokens


@pytest.mark.parametrize("name", list(_components()))
def test_component_exposes_accessibility_contract(name: str) -> None:
    component = _components()[name]
    a11y = component.accessibility()
    assert a11y.min_contrast_ratio >= 3.0


def test_button_variants_are_unique() -> None:
    variants = {v.value for v in ButtonVariant}
    assert variants == {"primary", "secondary", "danger", "ghost"}
    styles = {
        primary_button("A").style(),
        secondary_button("A").style(),
        danger_button("A").style(),
        ghost_button("A").style(),
    }
    assert len(styles) == 4


def test_mission_and_recommendation_cards_emphasize_primary_border() -> None:
    mission = MissionCard(title="Mission")
    recommendation = RecommendationCard(title="Next")
    assert mission.style().border == SemanticColour.PRIMARY
    assert recommendation.style().border == SemanticColour.PRIMARY
    assert mission.variant.value == "mission"
    assert recommendation.variant.value == "recommendation"


def test_progress_clamps_percent() -> None:
    assert ProgressBar(label="x", percent=150).percent == 100.0
    assert ProgressRing(label="x", percent=-5).percent == 0.0


def test_style_contracts_never_embed_raw_hex() -> None:
    """Component Python sources must not hard-code colour or rem literals."""
    for path in COMPONENTS_ROOT.rglob("*.py"):
        if path.name == "__init__.py":
            continue
        source = path.read_text(encoding="utf-8")
        assert "#3B4FB8" not in source
        assert "#0f766e" not in source.lower()
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                assert not node.value.endswith(
                    "rem"
                ), f"{path.name} embeds rem literal {node.value!r}"
                assert not (
                    node.value.startswith("#") and len(node.value) in {4, 7}
                ), f"{path.name} embeds hex literal {node.value!r}"


def test_no_duplicate_component_class_names() -> None:
    names: list[str] = []
    for path in COMPONENTS_ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                names.append(node.name)
    assert len(names) == len(set(names))
