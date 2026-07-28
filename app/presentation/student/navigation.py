"""Student Experience navigation chrome.

One canonical navigation tree for the Education Operating System.
Maps Experience surfaces and system destinations to Flask endpoints.
Navigation ownership only — no educational authority.

When ``ENABLE_UNIFIED_JOURNEY`` is on, primary chrome reflects journey
stages instead of feature-oriented labels (P2-MS001).
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.unified_journey.navigation_map import endpoint_for_stage
from app.application.unified_journey.stages import (
    PRIMARY_NAV_STAGES,
    JourneyStage,
    stage_label,
)
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
    journey_stage: str = ""


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

# Help remains available under unified journey chrome.
_UNIFIED_SYSTEM_NAV_ITEMS: tuple[tuple[str, str, str], ...] = (
    ("help", "Help", "alpha.help_centre"),
)


def build_navigation(
    active_surface: ExperienceSurface | str | None = None,
    *,
    include_system: bool = True,
    active_endpoint: str | None = None,
    unified_journey: bool | None = None,
    active_stage: JourneyStage | str | None = None,
) -> tuple[StudentNavItem, ...]:
    """Return the canonical student nav tree with active highlighting.

    Feature mode (default / flag off):
        Home · Journey · Revision · History · Settings · Study Plan · Help

    Unified journey mode (``ENABLE_UNIFIED_JOURNEY``):
        Today · Planning · Exam Readiness · Revision · Archive · Onboarding · Help
    """
    use_unified = (
        unified_journey
        if unified_journey is not None
        else _unified_journey_enabled()
    )
    if use_unified:
        return _build_journey_navigation(
            active_surface=active_surface,
            active_endpoint=active_endpoint,
            active_stage=active_stage,
            include_system=include_system,
        )
    return _build_feature_navigation(
        active_surface=active_surface,
        active_endpoint=active_endpoint,
        include_system=include_system,
    )


def endpoint_for(surface: ExperienceSurface | str) -> str:
    """Return the Flask endpoint for an experience surface."""
    return SURFACE_ENDPOINTS[_resolve(surface)]


def surface_for_endpoint(endpoint: str | None) -> ExperienceSurface:
    """Map a Flask endpoint back to an experience surface."""
    if not endpoint:
        return ExperienceSurface.HOME
    # Settings subpages share the Profile / Settings nav destination.
    if endpoint.startswith("settings."):
        return ExperienceSurface.PROFILE
    # ILE-002 Decision Journal sits under History chrome.
    if endpoint == "student.decision_journal":
        return ExperienceSurface.HISTORY
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


def build_navigation_for_request(
    endpoint: str | None,
    *,
    include_system: bool = True,
    unified_journey: bool | None = None,
) -> tuple[StudentNavItem, ...]:
    """Build EOS nav with active highlighting for any student-facing endpoint.

    Used by the global template context so Study Plan / Help / Settings pages
    that lack a Student Experience ``page`` view-model still render the
    canonical Education OS navigation (DEP-003).
    """
    active_surface: ExperienceSurface | None = None
    active_endpoint = endpoint
    if endpoint:
        if endpoint.startswith("student.") or endpoint.startswith("settings."):
            active_surface = surface_for_endpoint(endpoint)
            if endpoint.startswith("settings."):
                # Highlight Settings; do not also mark Study Plan/Help.
                active_endpoint = SURFACE_ENDPOINTS[ExperienceSurface.PROFILE]
        elif endpoint.startswith("study_plan.") or endpoint.startswith("alpha."):
            active_surface = None
        else:
            active_surface = surface_for_endpoint(endpoint)
    return build_navigation(
        active_surface,
        include_system=include_system,
        active_endpoint=active_endpoint,
        unified_journey=unified_journey,
    )


def _build_feature_navigation(
    *,
    active_surface: ExperienceSurface | str | None,
    active_endpoint: str | None,
    include_system: bool,
) -> tuple[StudentNavItem, ...]:
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
                        active_endpoint
                        and active_endpoint.startswith(
                            endpoint.rsplit(".", 1)[0]
                        )
                    ),
                )
            )
    return tuple(items)


def _build_journey_navigation(
    *,
    active_surface: ExperienceSurface | str | None,
    active_endpoint: str | None,
    active_stage: JourneyStage | str | None,
    include_system: bool,
) -> tuple[StudentNavItem, ...]:
    from app.application.unified_journey.navigation_map import (
        stage_for_endpoint,
        stage_for_surface,
    )
    from app.application.unified_journey.stages import resolve_journey_stage

    resolved_stage: JourneyStage | None = None
    if active_stage is not None:
        resolved_stage = resolve_journey_stage(active_stage)
    elif active_endpoint:
        resolved_stage = stage_for_endpoint(active_endpoint)
    elif active_surface:
        resolved_stage = stage_for_surface(active_surface)

    items: list[StudentNavItem] = []
    for stage in PRIMARY_NAV_STAGES:
        endpoint = endpoint_for_stage(stage)
        items.append(
            StudentNavItem(
                surface=stage.value,
                label=stage_label(stage),
                endpoint=endpoint,
                active=resolved_stage is stage,
                journey_stage=stage.value,
            )
        )
    if include_system:
        for surface_key, label, endpoint in _UNIFIED_SYSTEM_NAV_ITEMS:
            items.append(
                StudentNavItem(
                    surface=surface_key,
                    label=label,
                    endpoint=endpoint,
                    active=bool(
                        active_endpoint
                        and active_endpoint.startswith(
                            endpoint.rsplit(".", 1)[0]
                        )
                    ),
                )
            )
    return tuple(items)


def _unified_journey_enabled() -> bool:
    try:
        from app.application.config.v2_flags import resolve_v2_feature_flags

        return bool(resolve_v2_feature_flags().ENABLE_UNIFIED_JOURNEY)
    except Exception:
        return False


def _resolve(value: ExperienceSurface | str) -> ExperienceSurface:
    if isinstance(value, ExperienceSurface):
        return value
    return ExperienceSurface(str(value).strip().lower())
