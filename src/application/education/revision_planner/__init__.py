"""Adaptive Revision Planner — PRD-002.

Application-layer capability that transforms an immutable
``MissionPlan`` into an adaptive ``StudySchedule``.

Organises educational work. Never creates educational work.

Does not estimate mastery, generate recommendations, generate missions,
modify MissionPlan, modify StudentEducationalState, persist, call
Flask/SQLAlchemy, or invoke AI.
"""

from __future__ import annotations

from application.education.revision_planner.adaptive_revision_planner import (
    AdaptiveRevisionPlanner,
)
from application.education.revision_planner.enums import (
    AbandonmentPolicy,
    DayKind,
    ScheduledMissionStatus,
    SessionPriority,
    SessionStatus,
    SpacingPolicy,
    Weekday,
    WorkloadBand,
)
from application.education.revision_planner.errors import (
    RevisionPlanningError,
    ScheduleInvariantViolation,
    ScheduleValidationError,
)
from application.education.revision_planner.exam_target import ExamTarget
from application.education.revision_planner.execution_history import ExecutionHistory
from application.education.revision_planner.ids import DayId, ScheduleId, SessionId
from application.education.revision_planner.models import (
    CalendarDayProjection,
    CompletionMetrics,
    DayWorkload,
    ScheduledMission,
    ScheduleMetrics,
    ScheduleSnapshot,
    ScheduleSummary,
    StudyCalendarProjection,
    StudyDay,
    StudySchedule,
    StudySession,
    WorkloadDistribution,
)
from application.education.revision_planner.planning_constraints import (
    PlanningConstraints,
)
from application.education.revision_planner.ports import (
    AvailabilityProvider,
    CalendarProvider,
    HolidayProvider,
    SchedulePublisher,
)
from application.education.revision_planner.services import (
    AllocationResult,
    DayCapacity,
    DependencyResolver,
    ScheduleRebalancer,
    ScheduleValidator,
    SessionAllocator,
    SpacingStrategy,
    WorkloadBalancer,
)
from application.education.revision_planner.student_availability import (
    AvailabilityWindow,
    StudentAvailability,
)

__all__ = [
    # Planner
    "AdaptiveRevisionPlanner",
    # Models
    "StudySchedule",
    "StudyDay",
    "StudySession",
    "ScheduledMission",
    "ScheduleSummary",
    "ScheduleSnapshot",
    "StudyCalendarProjection",
    "CalendarDayProjection",
    "ScheduleMetrics",
    "WorkloadDistribution",
    "DayWorkload",
    "CompletionMetrics",
    # Inputs
    "PlanningConstraints",
    "StudentAvailability",
    "AvailabilityWindow",
    "ExamTarget",
    "ExecutionHistory",
    # Identity
    "ScheduleId",
    "SessionId",
    "DayId",
    # Enums
    "SessionStatus",
    "SessionPriority",
    "ScheduledMissionStatus",
    "DayKind",
    "WorkloadBand",
    "SpacingPolicy",
    "AbandonmentPolicy",
    "Weekday",
    # Errors
    "RevisionPlanningError",
    "ScheduleInvariantViolation",
    "ScheduleValidationError",
    # Services
    "DependencyResolver",
    "SessionAllocator",
    "WorkloadBalancer",
    "SpacingStrategy",
    "ScheduleValidator",
    "ScheduleRebalancer",
    "AllocationResult",
    "DayCapacity",
    # Ports
    "CalendarProvider",
    "AvailabilityProvider",
    "SchedulePublisher",
    "HolidayProvider",
]
