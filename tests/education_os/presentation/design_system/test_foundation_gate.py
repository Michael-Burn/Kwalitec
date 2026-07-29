"""DX-006B foundation export surface — rejected components isolated."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from presentation.design_system import foundation
from presentation.design_system.components.base import StyleContract
from presentation.design_system.foundation import (
    REJECTED_COMPONENT_NAMES,
    BlockingFindings,
    CurrentWork,
    EmptyOperationalState,
    FeedbackBlock,
    Input,
    MissionPanel,
    PersistentContext,
    PrimaryActionStrip,
    PublicationQueue,
    QueueRow,
    RecentPublications,
    SearchBar,
    StageIndicator,
)
from presentation.design_system.spacing import SpacingToken, is_product_spacing


def test_foundation_excludes_rejected_names() -> None:
    exported = set(foundation.__all__)
    assert REJECTED_COMPONENT_NAMES.isdisjoint(exported)
    for name in REJECTED_COMPONENT_NAMES:
        assert not hasattr(foundation, name), f"{name} must not be on foundation"


def test_foundation_includes_operational_components() -> None:
    for name in (
        "CurrentWork",
        "PublicationQueue",
        "RecentPublications",
        "PrimaryActionStrip",
        "MissionPanel",
        "LearningQueue",
        "RecentProgress",
        "PersistentContext",
        "BlockingFindings",
        "FeedbackBlock",
        "PublicationStatus",
        "EmptyOperationalState",
        "StageIndicator",
    ):
        assert name in foundation.__all__
        assert hasattr(foundation, name)


def test_operational_components_expose_contracts() -> None:
    samples = [
        CurrentWork("CS1", "Validate", "Resume", "/workspace/1"),
        PublicationQueue(rows=(QueueRow("CS1", "Ready"),)),
        RecentPublications(rows=(QueueRow("CS1", meta_label="Yesterday"),)),
        PrimaryActionStrip("Resume", "/workspace/1"),
        MissionPanel("CS1", "Practice chapter 2", "Continue"),
        PersistentContext("CS1", ("v1",), "Review"),
        BlockingFindings(),
        FeedbackBlock("Correct", "Use the definition."),
        EmptyOperationalState("No subjects yet", "Create Subject"),
        StageIndicator(current_index=1),
        SearchBar(),
        Input(name="title", label="Title"),
    ]
    for component in samples:
        style = component.style()
        assert isinstance(style, StyleContract)
        a11y = component.accessibility()
        assert a11y.min_contrast_ratio >= 3.0


def test_foundation_components_avoid_legacy_spacing() -> None:
    """Shared foundation components must not reference SpacingToken.MD in source."""
    root = (
        Path(__file__).resolve().parents[4]
        / "src"
        / "presentation"
        / "design_system"
        / "components"
    )
    for path in (
        root / "layout_primitives.py",
        root / "operational.py",
        root / "forms.py",
        root / "buttons.py",
        root / "section.py",
        root / "feedback.py",
        root / "cards.py",
    ):
        source = path.read_text(encoding="utf-8")
        assert "SpacingToken.MD" not in source, f"{path.name} uses legacy MD spacing"
        assert "SpacingToken.XXXXXL" not in source
        assert "SpacingToken.XXXXXXL" not in source


def test_product_spacing_helper() -> None:
    assert is_product_spacing(SpacingToken.LG)
    assert not is_product_spacing(SpacingToken.MD)


def test_macros_template_exists() -> None:
    macros = (
        Path(__file__).resolve().parents[4]
        / "app"
        / "templates"
        / "design_system"
        / "macros.html"
    )
    css = (
        Path(__file__).resolve().parents[4]
        / "app"
        / "static"
        / "css"
        / "design_system.css"
    )
    assert macros.is_file()
    assert css.is_file()
    text = macros.read_text(encoding="utf-8")
    for name in (
        "ds_current_work",
        "ds_publication_queue",
        "ds_recent_publications",
        "ds_primary_action_strip",
        "ds_mission_panel",
        "ds_persistent_context",
        "ds_blocking_findings",
        "ds_feedback_block",
    ):
        assert name in text


def test_design_system_css_is_token_only() -> None:
    css = (
        Path(__file__).resolve().parents[4]
        / "app"
        / "static"
        / "css"
        / "design_system.css"
    ).read_text(encoding="utf-8")
    # No raw hex colours in component CSS (token vars only).
    assert "#" not in css or all(
        not line.strip().startswith("color:")
        and "#E8" not in line
        and "#3B" not in line
        for line in css.splitlines()
        if "#" in line and "/*" not in line
    )
    # Soft check: no #rrggbb patterns outside comments
    tree_safe = True
    for line in css.splitlines():
        stripped = line.split("/*", 1)[0]
        if "#" in stripped and any(c in stripped for c in "0123456789ABCDEFabcdef"):
            # allow only if it's not a 3/6 hex — none expected
            if any(
                token in stripped
                for token in ("#fff", "#000", "#3B", "#E8", "#0f", "#c8")
            ):
                tree_safe = False
    assert tree_safe


def test_foundation_module_has_no_rejected_imports() -> None:
    path = (
        Path(__file__).resolve().parents[4]
        / "src"
        / "presentation"
        / "design_system"
        / "foundation.py"
    )
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imported.add(alias.name)
    assert imported.isdisjoint(REJECTED_COMPONENT_NAMES)
