"""Founder Command Centre secondary navigation (POP-002 / IAHF-003)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CommandCentreNavItem:
    """One section in the Founder Command Centre shell."""

    endpoint: str
    label: str
    section_id: str


# Primary Founder Command Centre hierarchy (V1SP-001C / POP-002).
# Operational Health is the actionable decision layer beneath Overview.
COMMAND_CENTRE_NAV: tuple[CommandCentreNavItem, ...] = (
    CommandCentreNavItem("founder_dashboard.index", "Overview", "overview"),
    CommandCentreNavItem(
        "founder_dashboard.operational_health",
        "Operational Health",
        "operational_health",
    ),
    CommandCentreNavItem("curriculum_studio.index", "Studio", "studio"),
    CommandCentreNavItem(
        "founder_dashboard.founder_intelligence",
        "Intelligence",
        "intelligence",
    ),
    CommandCentreNavItem(
        "founder_dashboard.evidence_gates", "Evidence Gates", "evidence_gates"
    ),
    CommandCentreNavItem("founder_dashboard.feedback", "Feedback", "feedback"),
    CommandCentreNavItem("founder_dashboard.research", "Research", "research"),
    CommandCentreNavItem(
        "founder_dashboard.vision_journal", "Vision Journal", "vision"
    ),
    CommandCentreNavItem("founder_dashboard.releases", "Releases", "releases"),
    CommandCentreNavItem("founder_dashboard.settings", "Settings", "settings"),
)

# Secondary operational destinations kept reachable (not primary nav).
COMMAND_CENTRE_SECONDARY_NAV: tuple[CommandCentreNavItem, ...] = (
    CommandCentreNavItem("founder_dashboard.attention", "Attention", "attention"),
    CommandCentreNavItem("founder_dashboard.findings", "Findings", "findings"),
    CommandCentreNavItem(
        "founder_dashboard.internal_alpha", "Internal Alpha", "internal_alpha"
    ),
    CommandCentreNavItem(
        "founder_dashboard.participants", "Participants", "participants"
    ),
    CommandCentreNavItem(
        "founder_dashboard.operations", "Operations", "operations"
    ),
)


def active_section_id(endpoint: str | None) -> str:
    """Map a Flask endpoint to the Command Centre section id."""
    if not endpoint:
        return "overview"
    if endpoint == "founder_dashboard.index":
        return "overview"
    if endpoint in {
        "founder_dashboard.feedback",
        "founder_dashboard.review_submission",
    }:
        return "feedback"
    if endpoint in {
        "founder_dashboard.findings",
        "founder_dashboard.finding_detail",
    }:
        return "findings"
    if endpoint in {
        "founder_dashboard.vision_journal",
        "founder_dashboard.vision_timeline",
        "founder_dashboard.vision_new",
        "founder_dashboard.vision_entry",
        "founder_dashboard.vision_edit",
        "founder_dashboard.vision_export",
        "founder_dashboard.vision_remove_relation",
    }:
        return "vision"
    if endpoint == "founder_dashboard.operational_health":
        return "operational_health"
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
        return "studio"
    if endpoint == "founder_dashboard.founder_intelligence":
        return "intelligence"
    if endpoint in {
        "founder_dashboard.operations",
        "founder_dashboard.attention",
    }:
        return "operational_health"
    if endpoint.startswith("founder_dashboard."):
        suffix = endpoint.removeprefix("founder_dashboard.")
        for item in COMMAND_CENTRE_NAV:
            if item.section_id == suffix:
                return item.section_id
        for item in COMMAND_CENTRE_SECONDARY_NAV:
            if item.section_id == suffix:
                return item.section_id
    return "overview"
