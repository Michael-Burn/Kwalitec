"""Experience Integration view models (PX-002)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.student_experience.coach.models.celebration_moments import (
    CelebrationMoments,
)
from application.student_experience.coach.models.coach_context import CoachContext
from application.student_experience.coach.models.coach_snapshot import CoachSnapshot
from application.student_experience.coach.models.conversation_context import (
    ConversationContext,
)
from application.student_experience.coach.models.reflection_prompts import (
    ReflectionPrompts,
)
from application.student_experience.home.enums import FocusActionKind
from application.student_experience.home.models.home_snapshot import HomeSnapshot
from application.student_experience.home.models.home_view_model import HomeViewModel
from application.student_experience.home.models.primary_focus import PrimaryFocus
from application.student_experience.integration.enums import (
    CascadeStep,
    IntegrationTrigger,
    JourneySurface,
)
from application.student_experience.integration.errors import (
    IntegrationInvariantViolation,
)
from application.student_experience.integration.ids import ExperienceBundleId
from application.student_experience.progress.models.journey_snapshot import (
    JourneySnapshot,
)
from application.student_experience.progress.models.learning_journey_view_model import (
    LearningJourneyViewModel,
)
from application.student_experience.readiness.models.exam_readiness_view_model import (
    ExamReadinessViewModel,
)
from application.student_experience.readiness.models.readiness_snapshot import (
    ReadinessSnapshot,
)
from application.student_experience.workspace.models.study_workspace_view_model import (
    StudyWorkspaceViewModel,
)
from application.student_experience.workspace.models.workspace_snapshot import (
    WorkspaceSnapshot,
)


@dataclass(frozen=True, slots=True)
class IntegratedNextAction:
    """Single continuous-journey CTA projected for Home and navigation."""

    action_kind: FocusActionKind
    label: str
    reason: str
    destination: JourneySurface
    mission_id: str | None = None
    preserves_context: bool = True
    has_action: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.action_kind, FocusActionKind):
            raise IntegrationInvariantViolation(
                "action_kind must be a FocusActionKind",
                invariant="IntegratedNextAction.action_kind.type",
            )
        if not isinstance(self.destination, JourneySurface):
            raise IntegrationInvariantViolation(
                "destination must be a JourneySurface",
                invariant="IntegratedNextAction.destination.type",
            )
        for name in ("label", "reason"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise IntegrationInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"IntegratedNextAction.{name}.required",
                )
            object.__setattr__(self, name, value)
        object.__setattr__(
            self, "mission_id", (self.mission_id or "").strip() or None
        )


@dataclass(frozen=True, slots=True)
class SurfaceState:
    """Empty / success presentation state for one journey surface."""

    surface: JourneySurface
    is_empty: bool
    empty_reason: str | None
    success_message: str | None
    progress_visible: bool

    def __post_init__(self) -> None:
        if not isinstance(self.surface, JourneySurface):
            raise IntegrationInvariantViolation(
                "surface must be a JourneySurface",
                invariant="SurfaceState.surface.type",
            )
        if self.is_empty:
            reason = (self.empty_reason or "").strip()
            if not reason:
                raise IntegrationInvariantViolation(
                    "empty surfaces must explain why they are empty",
                    invariant="SurfaceState.empty_reason.required",
                )
            object.__setattr__(self, "empty_reason", reason)
        else:
            object.__setattr__(
                self, "empty_reason", (self.empty_reason or "").strip() or None
            )
        object.__setattr__(
            self,
            "success_message",
            (self.success_message or "").strip() or None,
        )


@dataclass(frozen=True, slots=True)
class ReadinessChangeNotice:
    """Natural readiness-change surface — never an isolated dashboard."""

    changed: bool
    previous_label: str | None
    current_label: str | None
    message: str

    def __post_init__(self) -> None:
        message = (self.message or "").strip()
        if not message:
            raise IntegrationInvariantViolation(
                "message must be a non-empty string",
                invariant="ReadinessChangeNotice.message.required",
            )
        object.__setattr__(self, "message", message)
        object.__setattr__(
            self, "previous_label", (self.previous_label or "").strip() or None
        )
        object.__setattr__(
            self, "current_label", (self.current_label or "").strip() or None
        )


@dataclass(frozen=True, slots=True)
class ExperienceSnapshotBundle:
    """Immutable cross-module snapshot bundle for continuous journey handoffs."""

    bundle_id: ExperienceBundleId
    student_id: str
    composed_at: datetime
    home_snapshot: HomeSnapshot
    journey_snapshot: JourneySnapshot
    readiness_snapshot: ReadinessSnapshot
    workspace_snapshot: WorkspaceSnapshot
    coach_snapshot: CoachSnapshot
    next_action: IntegratedNextAction
    readiness_change: ReadinessChangeNotice
    cascade_steps: tuple[CascadeStep, ...] = ()
    trigger: IntegrationTrigger = IntegrationTrigger.HOME_VIEW

    def __post_init__(self) -> None:
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise IntegrationInvariantViolation(
                "student_id must be a non-empty string",
                invariant="ExperienceSnapshotBundle.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.composed_at, datetime):
            raise IntegrationInvariantViolation(
                "composed_at must be a datetime",
                invariant="ExperienceSnapshotBundle.composed_at.type",
            )
        object.__setattr__(self, "cascade_steps", tuple(self.cascade_steps or ()))


@dataclass(frozen=True, slots=True)
class ExperienceJourneyViewModel:
    """Full continuous-journey composition across XP modules.

    Projection only — never educational reasoning.
    """

    bundle_id: ExperienceBundleId
    student_id: str
    composed_at: datetime
    trigger: IntegrationTrigger
    home: HomeViewModel
    journey: LearningJourneyViewModel
    readiness: ExamReadinessViewModel
    workspace: StudyWorkspaceViewModel
    coach_context: CoachContext
    conversation: ConversationContext
    reflection: ReflectionPrompts
    celebrations: CelebrationMoments
    home_snapshot: HomeSnapshot
    journey_snapshot: JourneySnapshot
    readiness_snapshot: ReadinessSnapshot
    workspace_snapshot: WorkspaceSnapshot
    coach_snapshot: CoachSnapshot
    next_action: IntegratedNextAction
    primary_focus: PrimaryFocus
    readiness_change: ReadinessChangeNotice
    surface_states: tuple[SurfaceState, ...]
    cascade_steps: tuple[CascadeStep, ...] = ()
    evidence_recorded: bool = False

    def __post_init__(self) -> None:
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise IntegrationInvariantViolation(
                "student_id must be a non-empty string",
                invariant="ExperienceJourneyViewModel.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        object.__setattr__(self, "surface_states", tuple(self.surface_states or ()))
        object.__setattr__(self, "cascade_steps", tuple(self.cascade_steps or ()))

    def to_snapshot_bundle(self) -> ExperienceSnapshotBundle:
        """Project into a compact cross-module snapshot bundle."""
        return ExperienceSnapshotBundle(
            bundle_id=self.bundle_id,
            student_id=self.student_id,
            composed_at=self.composed_at,
            home_snapshot=self.home_snapshot,
            journey_snapshot=self.journey_snapshot,
            readiness_snapshot=self.readiness_snapshot,
            workspace_snapshot=self.workspace_snapshot,
            coach_snapshot=self.coach_snapshot,
            next_action=self.next_action,
            readiness_change=self.readiness_change,
            cascade_steps=self.cascade_steps,
            trigger=self.trigger,
        )
