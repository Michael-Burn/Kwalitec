"""Kwalitec Console navigation (CONSOLE-001).

Primary navigation is workflow-oriented and kept short. Secondary destinations
remain reachable from module hubs and Console Home.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CommandCentreNavItem:
    """One section in the Kwalitec Console shell."""

    endpoint: str
    label: str
    section_id: str


# Primary Console hierarchy — operational workflows, not feature laundry lists.
COMMAND_CENTRE_NAV: tuple[CommandCentreNavItem, ...] = (
    CommandCentreNavItem("founder_dashboard.index", "Overview", "overview"),
    CommandCentreNavItem(
        "founder_dashboard.operational_health",
        "Operations",
        "operations",
    ),
    CommandCentreNavItem(
        "founder_dashboard.participants", "Students", "students"
    ),
    CommandCentreNavItem(
        "founder_dashboard.founder_intelligence",
        "Learning",
        "learning",
    ),
    CommandCentreNavItem(
        "founder_dashboard.evidence_gates",
        "Assessments",
        "assessments",
    ),
    CommandCentreNavItem("curriculum_studio.index", "Content", "content"),
    CommandCentreNavItem(
        "founder_dashboard.research", "Analytics", "analytics"
    ),
    CommandCentreNavItem(
        "founder_dashboard.alpha_observability",
        "Platform",
        "platform",
    ),
    CommandCentreNavItem("founder_dashboard.settings", "Settings", "settings"),
    CommandCentreNavItem("founder_dashboard.feedback", "Support", "support"),
)

# Secondary operational destinations kept reachable (not primary nav).
COMMAND_CENTRE_SECONDARY_NAV: tuple[CommandCentreNavItem, ...] = (
    CommandCentreNavItem("founder_dashboard.attention", "Attention", "attention"),
    CommandCentreNavItem("founder_dashboard.findings", "Findings", "findings"),
    CommandCentreNavItem(
        "founder_dashboard.internal_alpha", "Internal Alpha", "internal_alpha"
    ),
    CommandCentreNavItem(
        "founder_dashboard.operations", "System Operations", "system_operations"
    ),
    CommandCentreNavItem(
        "founder_dashboard.releases", "Releases", "releases"
    ),
    CommandCentreNavItem(
        "founder_dashboard.vision_journal", "Vision Journal", "vision"
    ),
    CommandCentreNavItem("founder_dashboard.search", "Search", "search"),
)


def active_section_id(endpoint: str | None) -> str:
    """Map a Flask endpoint to the Console section id."""
    if not endpoint:
        return "overview"
    if endpoint == "founder_dashboard.index":
        return "overview"
    if endpoint in {
        "founder_dashboard.feedback",
        "founder_dashboard.review_submission",
        "founder_dashboard.findings",
        "founder_dashboard.finding_detail",
    }:
        return "support"
    if endpoint in {
        "founder_dashboard.vision_journal",
        "founder_dashboard.vision_timeline",
        "founder_dashboard.vision_new",
        "founder_dashboard.vision_entry",
        "founder_dashboard.vision_edit",
        "founder_dashboard.vision_export",
        "founder_dashboard.vision_remove_relation",
    }:
        return "platform"
    if endpoint in {
        "founder_dashboard.operational_health",
        "founder_dashboard.operations",
        "founder_dashboard.attention",
    }:
        return "operations"
    if endpoint == "founder_dashboard.participants":
        return "students"
    if endpoint == "founder_dashboard.founder_intelligence":
        return "learning"
    if endpoint == "founder_dashboard.evidence_gates":
        return "assessments"
    if endpoint == "founder_dashboard.research":
        return "analytics"
    if endpoint in {
        "founder_dashboard.alpha_observability",
        "founder_dashboard.internal_alpha",
        "founder_dashboard.releases",
    }:
        return "platform"
    if endpoint == "founder_dashboard.settings":
        return "settings"
    if endpoint == "founder_dashboard.search":
        return "search"
    if endpoint in {
        "curriculum_studio.index",
        "curriculum_studio.workspace",
        "curriculum_studio.create_subject",
        "curriculum_studio.create_workspace",
        "curriculum_studio.advance",
        "curriculum_studio.validate",
        "curriculum_studio.preview",
        "curriculum_studio.approve",
        "curriculum_studio.publish",
        "curriculum_studio.assign_version",
    } or (endpoint and endpoint.startswith("curriculum_studio.")):
        return "content"
    if endpoint.startswith("founder_dashboard."):
        suffix = endpoint.removeprefix("founder_dashboard.")
        for item in COMMAND_CENTRE_NAV:
            if item.section_id == suffix:
                return item.section_id
        for item in COMMAND_CENTRE_SECONDARY_NAV:
            if item.section_id == suffix:
                return item.section_id
    return "overview"
