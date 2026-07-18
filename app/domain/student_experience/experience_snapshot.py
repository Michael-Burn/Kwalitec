"""Composite experience snapshot assembling primary student surfaces."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.student_experience.experience_workspace import (
    ExperienceSurface,
    ExperienceWorkspace,
)
from app.domain.student_experience.history_projection import HistoryProjection
from app.domain.student_experience.journey_projection import JourneyProjection
from app.domain.student_experience.profile_projection import ProfileProjection
from app.domain.student_experience.revision_projection import RevisionProjection
from app.domain.student_experience.student_home import StudentHome


@dataclass(frozen=True)
class ExperienceSnapshot:
    """Composite domain snapshot for the student experience.

    Projection only — never a system of record for educational state.
    """

    workspace: ExperienceWorkspace
    home: StudentHome | None = None
    journey: JourneyProjection | None = None
    revision: RevisionProjection | None = None
    history: HistoryProjection | None = None
    profile: ProfileProjection | None = None
    available_surfaces: tuple[ExperienceSurface, ...] = field(
        default_factory=tuple
    )

    @classmethod
    def create(
        cls,
        workspace: ExperienceWorkspace,
        *,
        home: StudentHome | None = None,
        journey: JourneyProjection | None = None,
        revision: RevisionProjection | None = None,
        history: HistoryProjection | None = None,
        profile: ProfileProjection | None = None,
        available_surfaces: (
            list[ExperienceSurface] | tuple[ExperienceSurface, ...] | None
        ) = None,
    ) -> ExperienceSnapshot:
        """Assemble a composite experience snapshot."""
        surfaces = tuple(available_surfaces) if available_surfaces is not None else (
            ExperienceSurface.HOME,
            ExperienceSurface.JOURNEY,
            ExperienceSurface.REVISION,
            ExperienceSurface.HISTORY,
            ExperienceSurface.PROFILE,
        )
        return cls(
            workspace=workspace,
            home=home,
            journey=journey,
            revision=revision,
            history=history,
            profile=profile,
            available_surfaces=surfaces,
        )

    @property
    def student_id(self) -> str:
        return self.workspace.student_id

    @property
    def active_surface(self) -> ExperienceSurface:
        return self.workspace.active_surface

    def surface_for(self, surface: ExperienceSurface) -> object | None:
        """Return the projection bound to ``surface``, if present."""
        mapping: dict[ExperienceSurface, object | None] = {
            ExperienceSurface.HOME: self.home,
            ExperienceSurface.JOURNEY: self.journey,
            ExperienceSurface.REVISION: self.revision,
            ExperienceSurface.HISTORY: self.history,
            ExperienceSurface.PROFILE: self.profile,
        }
        return mapping.get(surface)
