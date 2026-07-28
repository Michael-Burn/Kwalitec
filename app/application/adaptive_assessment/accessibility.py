"""Accessibility foundation for Adaptive Assessment components.

Infrastructure and standards only — no UI redesign. Components must expose
accessible labels, keyboard support metadata, semantic structure hints,
screen-reader descriptions, and reduced-motion compatibility flags.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.adaptive_assessment.copy_registry import get_copy
from app.application.adaptive_assessment.localisation import format_message
from app.application.adaptive_assessment.session_registry import (
    SessionTypeDefinition,
    get_session_type,
)


@dataclass(frozen=True)
class AccessibilityMetadata:
    """Immutable accessibility contract for an Adaptive Assessment surface.

    Attributes:
        accessible_label: Primary accessible name for the region / control.
        screen_reader_description: Longer SR-only description when needed.
        semantic_role: Suggested ARIA / HTML landmark role (e.g. ``region``).
        keyboard_navigable: Surface must be fully operable by keyboard.
        focus_order_hint: Suggested focus order token for implementers.
        reduced_motion_compatible: Animations must respect prefers-reduced-motion.
        colour_not_sole_encoding: State must not rely on colour alone.
    """

    accessible_label: str
    screen_reader_description: str
    semantic_role: str = "region"
    keyboard_navigable: bool = True
    focus_order_hint: str = "primary"
    reduced_motion_compatible: bool = True
    colour_not_sole_encoding: bool = True


def reduced_motion_safe(*, prefers_reduced_motion: bool) -> bool:
    """Return True when motion may run given the user's preference.

    Adaptive Assessment chrome must skip non-essential motion when
    ``prefers_reduced_motion`` is True.
    """
    return not prefers_reduced_motion


def accessibility_for_session(
    session_type_id: str,
    *,
    explain_control: bool = True,
    defer_control: bool = True,
) -> AccessibilityMetadata:
    """Build accessibility metadata for a registered session type.

    Args:
        session_type_id: Registry identifier.
        explain_control: Include explain-control SR description.
        defer_control: Include defer-control SR description.
    """
    session: SessionTypeDefinition = get_session_type(session_type_id)
    label = format_message(
        get_copy("a11y.session_region").default,
        session_name=session.display_name,
    )
    parts = [
        session.short_description,
        session.expected_duration_label,
    ]
    if explain_control:
        parts.append(get_copy("a11y.explain_button").default)
    if defer_control:
        parts.append(get_copy("a11y.defer_button").default)
    description = " ".join(parts)
    return AccessibilityMetadata(
        accessible_label=label,
        screen_reader_description=description,
        semantic_role="region",
        keyboard_navigable=True,
        focus_order_hint="entry_frame",
        reduced_motion_compatible=True,
        colour_not_sole_encoding=True,
    )
