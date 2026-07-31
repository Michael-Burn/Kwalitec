"""Progress Engine — sole curriculum progression AUTHORITY (SR-003 / P6).

Consumes Accepted evidence decisions, mission completion, curriculum
structure, and optional Twin estimates. Produces Study Progress coverage,
position, and projections. Does not evaluate evidence or update Twin.
"""

from __future__ import annotations

from app.application.progress_engine.dto import (
    CoverageAdvanceDecision,
    CurriculumPosition,
    MissionCompositionInputs,
    ProgressProjection,
    StudyProgress,
    TwinEstimateInput,
)
from app.application.progress_engine.engine import (
    ProgressEngine,
    clear_progress_writer_registry,
    register_progress_writer,
    registered_progress_writer,
)
from app.application.progress_engine.exceptions import (
    CoverageAdvanceRejected,
    DuplicateProgressWriter,
    ProgressEngineError,
    ProgressSingularityDisabled,
)

__all__ = [
    "CoverageAdvanceDecision",
    "CoverageAdvanceRejected",
    "CurriculumPosition",
    "DuplicateProgressWriter",
    "MissionCompositionInputs",
    "ProgressEngine",
    "ProgressEngineError",
    "ProgressProjection",
    "ProgressSingularityDisabled",
    "StudyProgress",
    "TwinEstimateInput",
    "clear_progress_writer_registry",
    "register_progress_writer",
    "registered_progress_writer",
]
