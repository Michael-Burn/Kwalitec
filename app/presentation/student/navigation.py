"""Student Experience navigation chrome.

One canonical navigation tree for the Education Operating System.
Maps Experience surfaces and system destinations to Flask endpoints.
Navigation ownership only — no educational authority.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.student_experience.experience_workspace import (
    CANONICAL_SURFACES,
    SURFACE_LABELS,
    ExperienceSurface,
)


@dataclass(frozen=True)
class StudentNavItem:
    """One primary student navigation destination."""

    surface: str
    label: str
    endpoint: str
    active: bool = False


SURFACE_ENDPOINTS: dict[ExperienceSurface, str] = {
    ExperienceSurface.HOME: "student.home",
    ExperienceSurface.JOURNEY: "student.journey",
    ExperienceSurface.REVISION: "student.revision",
    ExperienceSurface.HISTORY: "student.history",
    ExperienceSurface.PROFILE: "student.profile",
}

# System destinations that complete the single OS nav tree (Phase 1).
# Study Plan wizard and Help remain shared blueprints — not competing products.
SYSTEM_NAV_ITEMS: tuple[tuple[str, str, str], ...] = (
    ("study_plan", "Study Plan", "study_plan.index"),
    ("help", "Help", "alpha.help_centre"),
)


def build_navigation(
    active_surface: ExperienceSurface | str | None = None,
    *,
    include_system: bool = True,
    active_endpoint: str | None = None,
) -> tuple[StudentNavItem, ...]:
    """Return the canonical student nav tree with active highlighting.

    Order: Dashboard · Journey · Revision · Analytics · Settings · Study Plan · Help.
    Today's Session and Coach live on Dashboard (workflow, not duplicate products).
    """
    active = _resolve(active_surface) if active_surface else None
    items: list[StudentNavItem] = []
    for surface in CANONICAL_SURFACES:
        items.append(
            StudentNavItem(
                surface=surface.value,
                label=SURFACE_LABELS[surface],
                endpoint=SURFACE_ENDPOINTS[surface],
                active=active is surface,
            )
        )
    if include_system:
        for surface_key, label, endpoint in SYSTEM_NAV_ITEMS:
            items.append(
                StudentNavItem(
                    surface=surface_key,
                    label=label,
                    endpoint=endpoint,
                    active=bool(
                        active_endpoint and active_endpoint.startswith(
                            endpoint.rsplit(".", 1)[0]
                        )
                    ),
                )
            )
    return tuple(items)


def endpoint_for(surface: ExperienceSurface | str) -> str:
    """Return the Flask endpoint for an experience surface."""
    return SURFACE_ENDPOINTS[_resolve(surface)]


def surface_for_endpoint(endpoint: str | None) -> ExperienceSurface:
    """Map a Flask endpoint back to an experience surface."""
    if not endpoint:
        return ExperienceSurface.HOME
    for surface, ep in SURFACE_ENDPOINTS.items():
        if ep == endpoint:
            return surface
    if endpoint.startswith("student."):
        suffix = endpoint.removeprefix("student.")
        try:
            return ExperienceSurface(suffix)
        except ValueError:
            pass
    return ExperienceSurface.HOME


def _resolve(value: ExperienceSurface | str) -> ExperienceSurface:
    if isinstance(value, ExperienceSurface):
        return value
    return ExperienceSurface(str(value).strip().lower())
