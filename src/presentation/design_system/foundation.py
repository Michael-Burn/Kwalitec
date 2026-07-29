"""DX-006B foundation export surface — approved catalogue only.

Import shared UI from this module for all DX-006B migrations:

    from presentation.design_system.foundation import CurrentWork, Button, …

Rejected / legacy KPI components are intentionally NOT re-exported here.
Legacy callers may still import them from presentation.design_system.components
until unmigrated surfaces are removed.
"""

from __future__ import annotations

from presentation.design_system.colours import (
    BRAND_COLOURS,
    SEMANTIC_COLOURS,
    BrandColour,
    SemanticColour,
    colour,
)
from presentation.design_system.components.buttons import (
    Button,
    ButtonVariant,
    danger_button,
    ghost_button,
    primary_button,
    secondary_button,
)
from presentation.design_system.components.cards import Card, CardVariant, MissionCard
from presentation.design_system.components.feedback import (
    EmptyState,
    LoadingState,
    Modal,
    Skeleton,
    SkeletonVariant,
    Toast,
    ToastTone,
)
from presentation.design_system.components.forms import (
    Checkbox,
    ErrorState,
    FieldState,
    Input,
    Radio,
    SearchInput,
    Select,
    Spinner,
    Textarea,
    Toggle,
)
from presentation.design_system.components.layout_primitives import (
    ContentContainer,
    DataList,
    DataTable,
    Inline,
    LayoutGrid,
    Page,
    Panel,
    PrimaryActionStrip,
    SearchBar,
    Stack,
    StackDirection,
    Toolbar,
)
from presentation.design_system.components.markers import Badge, Chip, Divider, Tone
from presentation.design_system.components.operational import (
    BlockingFinding,
    BlockingFindings,
    CurrentWork,
    Disclosure,
    EmptyOperationalState,
    FeedbackBlock,
    LearningQueue,
    MissionPanel,
    PersistentContext,
    PublicationQueue,
    PublicationStatus,
    QueueRow,
    RecentProgress,
    RecentPublications,
    SearchResults,
    SessionContext,
    StageIndicator,
)
from presentation.design_system.components.section import PageHeader, Section
from presentation.design_system.design_tokens import TOKENS, get_tokens
from presentation.design_system.layout import (
    BREAKPOINTS,
    CONTAINERS,
    Breakpoint,
    ContainerWidth,
)
from presentation.design_system.opacity import OPACITY, OpacityToken, opacity
from presentation.design_system.spacing import (
    PRODUCT_SPACING_PX,
    SPACING,
    SpacingToken,
    assert_product_spacing,
    is_product_spacing,
    space,
)
from presentation.design_system.typography import (
    CANONICAL_TYPE_SIZES_PX,
    TYPE_STYLES,
    TypeRole,
    type_style,
)

# Explicit denylist — must never appear in this module's public API.
REJECTED_COMPONENT_NAMES: frozenset[str] = frozenset(
    {
        "StatisticTile",
        "ProgressRing",
        "ProgressCard",
        "RecommendationCard",
        "Timeline",
        "Stepper",
        "Tag",  # consolidate into Badge / Chip
        "Accordion",  # prefer Disclosure collapsed
    }
)

__all__ = [
    "BRAND_COLOURS",
    "BREAKPOINTS",
    "CANONICAL_TYPE_SIZES_PX",
    "CONTAINERS",
    "OPACITY",
    "PRODUCT_SPACING_PX",
    "REJECTED_COMPONENT_NAMES",
    "SEMANTIC_COLOURS",
    "SPACING",
    "TOKENS",
    "TYPE_STYLES",
    "Badge",
    "BlockingFinding",
    "BlockingFindings",
    "BrandColour",
    "Breakpoint",
    "Button",
    "ButtonVariant",
    "Card",
    "CardVariant",
    "Checkbox",
    "Chip",
    "ContainerWidth",
    "ContentContainer",
    "CurrentWork",
    "DataList",
    "DataTable",
    "Disclosure",
    "Divider",
    "EmptyOperationalState",
    "EmptyState",
    "ErrorState",
    "FeedbackBlock",
    "FieldState",
    "Inline",
    "Input",
    "LayoutGrid",
    "LearningQueue",
    "LoadingState",
    "MissionCard",
    "MissionPanel",
    "Modal",
    "OpacityToken",
    "Page",
    "PageHeader",
    "Panel",
    "PersistentContext",
    "PrimaryActionStrip",
    "PublicationQueue",
    "PublicationStatus",
    "QueueRow",
    "Radio",
    "RecentProgress",
    "RecentPublications",
    "SearchBar",
    "SearchInput",
    "SearchResults",
    "Section",
    "Select",
    "SemanticColour",
    "SessionContext",
    "Skeleton",
    "SkeletonVariant",
    "SpacingToken",
    "Spinner",
    "Stack",
    "StackDirection",
    "StageIndicator",
    "Textarea",
    "Toast",
    "ToastTone",
    "Toggle",
    "Tone",
    "Toolbar",
    "TypeRole",
    "assert_product_spacing",
    "colour",
    "danger_button",
    "get_tokens",
    "ghost_button",
    "is_product_spacing",
    "opacity",
    "primary_button",
    "secondary_button",
    "space",
    "type_style",
]
