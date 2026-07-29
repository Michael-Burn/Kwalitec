"""L3 operational components — Founder & Student OS shared patterns.

Authority: DX-004 / DX-005 / DX-006A COMPONENT_CATALOGUE.
No domain logic. Presentation fields only.
"""

from __future__ import annotations

from dataclasses import dataclass

from presentation.design_system.colours import SemanticColour
from presentation.design_system.components.base import (
    AccessibilityContract,
    StyleContract,
)
from presentation.design_system.components.markers import Tone
from presentation.design_system.elevation import ElevationToken
from presentation.design_system.radius import RadiusToken
from presentation.design_system.spacing import SpacingToken
from presentation.design_system.typography import TypeRole


@dataclass(frozen=True, slots=True)
class QueueRow:
    """One attention or recent row — labels and href only."""

    title: str
    status_label: str = ""
    meta_label: str = ""
    href: str = ""


@dataclass(frozen=True, slots=True)
class CurrentWork:
    """Founder Home L0 — subject, stage, one Primary (Resume)."""

    subject_name: str
    stage_label: str
    primary_label: str
    primary_href: str = ""
    supporting_text: str = ""

    def style(self) -> StyleContract:
        return StyleContract(
            background=SemanticColour.SURFACE,
            foreground=SemanticColour.TEXT,
            border=SemanticColour.BORDER_SUBTLE,
            typography=TypeRole.SECTION,
            padding_x=SpacingToken.XL,
            padding_y=SpacingToken.XL,
            gap=SpacingToken.LG,
            radius=RadiusToken.LG,
            elevation=ElevationToken.NONE,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="region",
            label_required=True,
            keyboard_focusable=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
        )


@dataclass(frozen=True, slots=True)
class PublicationQueue:
    """Founder Home L1 — attention-only publication rows."""

    rows: tuple[QueueRow, ...] = ()
    empty_title: str = "Nothing needs attention"
    empty_action_label: str = ""

    def style(self) -> StyleContract:
        return StyleContract(
            foreground=SemanticColour.TEXT,
            typography=TypeRole.SECTION,
            gap=SpacingToken.SM,
            padding_y=SpacingToken.LG,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="list",
            label_required=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.BACKGROUND,
        )


@dataclass(frozen=True, slots=True)
class RecentPublications:
    """Founder Home L2 — quiet recent published ≤5."""

    rows: tuple[QueueRow, ...] = ()
    max_items: int = 5

    def style(self) -> StyleContract:
        return StyleContract(
            foreground=SemanticColour.TEXT_SECONDARY,
            typography=TypeRole.SUPPORT,
            gap=SpacingToken.SM,
            padding_y=SpacingToken.LG,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="list",
            label_required=True,
            contrast_fg=SemanticColour.TEXT_SECONDARY,
            contrast_bg=SemanticColour.BACKGROUND,
            min_contrast_ratio=3.0,
        )


@dataclass(frozen=True, slots=True)
class PublicationStatus:
    """Curriculum release state that changes operator decisions."""

    label: str
    tone: Tone = Tone.NEUTRAL
    supporting_text: str = ""

    def style(self) -> StyleContract:
        return StyleContract(
            typography=TypeRole.CAPTION,
            gap=SpacingToken.XS,
            extras=(("tone", self.tone.value),),
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="status",
            label_required=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
            min_contrast_ratio=3.0,
        )


@dataclass(frozen=True, slots=True)
class BlockingFinding:
    """One hard blocker."""

    title: str
    detail: str = ""
    href: str = ""


@dataclass(frozen=True, slots=True)
class BlockingFindings:
    """Hard blockers that prevent lawful Primary success."""

    findings: tuple[BlockingFinding, ...] = ()

    def style(self) -> StyleContract:
        return StyleContract(
            background=SemanticColour.DANGER_BG,
            foreground=SemanticColour.DANGER,
            border=SemanticColour.DANGER,
            typography=TypeRole.SUPPORT,
            padding_x=SpacingToken.LG,
            padding_y=SpacingToken.LG,
            gap=SpacingToken.SM,
            radius=RadiusToken.MD,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="alert",
            label_required=True,
            contrast_fg=SemanticColour.DANGER,
            contrast_bg=SemanticColour.DANGER_BG,
            min_contrast_ratio=3.0,
        )


@dataclass(frozen=True, slots=True)
class PersistentContext:
    """Persistent orientation header (Workspace / Session)."""

    title: str
    meta_labels: tuple[str, ...] = ()
    stage_label: str = ""

    def style(self) -> StyleContract:
        return StyleContract(
            background=SemanticColour.SURFACE,
            foreground=SemanticColour.TEXT,
            border=SemanticColour.BORDER_SUBTLE,
            typography=TypeRole.SUPPORT,
            padding_x=SpacingToken.XL,
            padding_y=SpacingToken.LG,
            gap=SpacingToken.SM,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="banner",
            label_required=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
        )


@dataclass(frozen=True, slots=True)
class StageIndicator:
    """Founder workspace stage position — Upload → … → Publish."""

    stages: tuple[str, ...] = (
        "Upload",
        "Validate",
        "Review",
        "Approve",
        "Publish",
    )
    current_index: int = 0

    def style(self) -> StyleContract:
        return StyleContract(
            foreground=SemanticColour.TEXT,
            typography=TypeRole.CAPTION,
            gap=SpacingToken.SM,
            padding_y=SpacingToken.SM,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="navigation",
            label_required=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.BACKGROUND,
        )


@dataclass(frozen=True, slots=True)
class MissionPanel:
    """Student Home L0 Mission — subject, objective, one Primary."""

    subject_name: str
    objective: str
    primary_label: str
    primary_href: str = ""
    why_now: str = ""
    status_label: str = ""
    after_completion: str = ""
    section_title: str = "Today's Mission"

    def style(self) -> StyleContract:
        return StyleContract(
            background=SemanticColour.SURFACE,
            foreground=SemanticColour.TEXT,
            border=SemanticColour.PRIMARY,
            typography=TypeRole.SECTION,
            padding_x=SpacingToken.XL,
            padding_y=SpacingToken.XL,
            gap=SpacingToken.LG,
            radius=RadiusToken.LG,
            elevation=ElevationToken.NONE,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="region",
            label_required=True,
            keyboard_focusable=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
        )


@dataclass(frozen=True, slots=True)
class LearningQueue:
    """Student Home L1 — attention-only learning rows."""

    rows: tuple[QueueRow, ...] = ()
    empty_title: str = "Your queue is clear"

    def style(self) -> StyleContract:
        return PublicationQueue(rows=self.rows).style()

    def accessibility(self) -> AccessibilityContract:
        return PublicationQueue(rows=self.rows).accessibility()


@dataclass(frozen=True, slots=True)
class RecentProgress:
    """Student Home L2 — quiet recent ≤5."""

    rows: tuple[QueueRow, ...] = ()
    max_items: int = 5

    def style(self) -> StyleContract:
        return RecentPublications(rows=self.rows).style()

    def accessibility(self) -> AccessibilityContract:
        return RecentPublications(rows=self.rows).accessibility()


@dataclass(frozen=True, slots=True)
class FeedbackBlock:
    """Session educational feedback — outcome + explanation."""

    outcome_label: str
    explanation: str = ""
    next_hint: str = ""

    def style(self) -> StyleContract:
        return StyleContract(
            background=SemanticColour.SURFACE,
            foreground=SemanticColour.TEXT,
            border=SemanticColour.BORDER_SUBTLE,
            typography=TypeRole.BODY,
            padding_x=SpacingToken.XL,
            padding_y=SpacingToken.LG,
            gap=SpacingToken.SM,
            radius=RadiusToken.LG,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="status",
            label_required=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
        )


@dataclass(frozen=True, slots=True)
class SearchResults:
    """Catalogue / discovery hits."""

    rows: tuple[QueueRow, ...] = ()
    query: str = ""
    empty_title: str = "No matches"

    def style(self) -> StyleContract:
        return StyleContract(
            foreground=SemanticColour.TEXT,
            typography=TypeRole.BODY,
            gap=SpacingToken.SM,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="list",
            label_required=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.BACKGROUND,
        )


@dataclass(frozen=True, slots=True)
class EmptyOperationalState:
    """Operational empty — Reason + Next Action only."""

    reason: str
    action_label: str = ""
    action_href: str = ""

    def style(self) -> StyleContract:
        return StyleContract(
            background=SemanticColour.SURFACE,
            foreground=SemanticColour.TEXT,
            typography=TypeRole.SECTION,
            padding_x=SpacingToken.XXL,
            padding_y=SpacingToken.XXXL,
            gap=SpacingToken.LG,
            radius=RadiusToken.LG,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="status",
            label_required=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.SURFACE,
        )


@dataclass(frozen=True, slots=True)
class Disclosure:
    """Collapsed detail — default closed (no Coach walls)."""

    title: str
    body: str = ""
    open: bool = False

    def style(self) -> StyleContract:
        return StyleContract(
            foreground=SemanticColour.TEXT,
            typography=TypeRole.SUPPORT,
            gap=SpacingToken.SM,
            padding_y=SpacingToken.SM,
        )

    def accessibility(self) -> AccessibilityContract:
        return AccessibilityContract(
            role="group",
            label_required=True,
            keyboard_focusable=True,
            contrast_fg=SemanticColour.TEXT,
            contrast_bg=SemanticColour.BACKGROUND,
        )


# Alias kept for catalogue naming clarity.
SessionContext = PersistentContext
