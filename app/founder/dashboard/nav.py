"""Kwalitec Console navigation (CONSOLE-001 / DX-004A).

Primary navigation is the ≤6 Console tree. Operational destinations
remain reachable from Settings and secondary nav.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CommandCentreNavItem:
    """One section in the Kwalitec Console shell."""

    endpoint: str
    label: str
    section_id: str


# DX-004A / DX-002 target primary Console tree (≤6).
COMMAND_CENTRE_NAV: tuple[CommandCentreNavItem, ...] = (
    CommandCentreNavItem("founder_dashboard.index", "Home", "home"),
    CommandCentreNavItem(
        "curriculum_studio.subjects_hub", "Subjects", "subjects"
    ),
    CommandCentreNavItem(
        "curriculum_studio.index", "Curriculum Studio", "curriculum_studio"
    ),
    CommandCentreNavItem(
        "founder_dashboard.participants", "Students", "students"
    ),
    CommandCentreNavItem("founder_dashboard.feedback", "Support", "support"),
    CommandCentreNavItem("founder_dashboard.settings", "Settings", "settings"),
)

# Secondary / nested destinations (not equal-weight chrome).
# Legacy Review / Publishing / Versions / Quality hubs collapsed into
# Subjects filter presets (DX-004B NAVIGATION_BOUNDARIES).
COMMAND_CENTRE_SECONDARY_NAV: tuple[CommandCentreNavItem, ...] = (
    CommandCentreNavItem(
        "founder_dashboard.operational_health",
        "Operations",
        "operations",
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
    CommandCentreNavItem(
        "founder_dashboard.research", "Analytics", "analytics"
    ),
    CommandCentreNavItem(
        "founder_dashboard.alpha_observability",
        "Platform",
        "platform",
    ),
    CommandCentreNavItem("founder_dashboard.attention", "Attention", "attention"),
    CommandCentreNavItem(
        "founder_dashboard.runtime_health", "Runtime Health", "runtime_health"
    ),
    CommandCentreNavItem(
        "founder_dashboard.curriculum_health",
        "Curriculum Health",
        "curriculum_health",
    ),
    CommandCentreNavItem(
        "founder_dashboard.beta",
        "Private Beta",
        "beta",
    ),
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
        return "home"
    if endpoint == "founder_dashboard.index":
        return "home"
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
        return "settings"
    if endpoint in {
        "founder_dashboard.operational_health",
        "founder_dashboard.operations",
        "founder_dashboard.attention",
        "founder_dashboard.runtime_health",
        "founder_dashboard.curriculum_health",
        "founder_dashboard.beta",
        "founder_dashboard.beta_enrol",
        "founder_dashboard.beta_observe",
        "founder_dashboard.beta_report",
        "founder_dashboard.alpha_observability",
        "founder_dashboard.internal_alpha",
        "founder_dashboard.releases",
        "founder_dashboard.founder_intelligence",
        "founder_dashboard.evidence_gates",
        "founder_dashboard.research",
        "founder_dashboard.search",
    }:
        return "settings"
    if endpoint == "founder_dashboard.participants":
        return "students"
    if endpoint == "founder_dashboard.settings":
        return "settings"
    if endpoint == "curriculum_studio.subjects_hub":
        return "subjects"
    if endpoint in {
        "curriculum_studio.review_hub",
        "curriculum_studio.publishing_hub",
        "curriculum_studio.versions_hub",
        "curriculum_studio.quality_hub",
        "curriculum_studio.create_subject",
    }:
        return "subjects"
    if endpoint == "curriculum_studio.index":
        return "curriculum_studio"
    if endpoint in {
        "curriculum_studio.workspace",
        "curriculum_studio.create_workspace",
        "curriculum_studio.advance",
        "curriculum_studio.validate",
        "curriculum_studio.preview",
        "curriculum_studio.approve",
        "curriculum_studio.publish",
        "curriculum_studio.assign_version",
    } or (endpoint and endpoint.startswith("curriculum_studio.")):
        return "curriculum_studio"
    if endpoint.startswith("founder_dashboard."):
        suffix = endpoint.removeprefix("founder_dashboard.")
        for item in COMMAND_CENTRE_NAV:
            if item.section_id == suffix:
                return item.section_id
        for item in COMMAND_CENTRE_SECONDARY_NAV:
            if item.section_id == suffix:
                return "settings"
    return "home"
