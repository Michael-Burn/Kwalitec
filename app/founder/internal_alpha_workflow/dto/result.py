"""WorkflowResult model for Internal Alpha Live Workflow (FSI-003)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class WorkflowResult:
    """Immutable outcome of one Internal Alpha live workflow run."""

    week: str
    started_at: datetime
    completed_at: datetime
    pipeline_success: bool
    operational_state_success: bool
    recommendations_success: bool
    briefing_success: bool
    exported_files: tuple[str, ...]
    warnings: tuple[str, ...]
    errors: tuple[str, ...]

    @property
    def success(self) -> bool:
        """True when every stage succeeded and no errors were recorded."""

        return (
            self.pipeline_success
            and self.operational_state_success
            and self.recommendations_success
            and self.briefing_success
            and not self.errors
        )
