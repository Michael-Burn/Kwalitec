"""Internal Alpha product status — informational presentation only.

Assembles version, curriculum, study-plan, and Twin presence labels for the
Internal Alpha settings page. Never scores readiness, mutates Twin, or drives
Educational Intelligence behaviour.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from app.application.config.internal_alpha import (
    build_twin_provider,
    is_internal_alpha_enabled,
)
from app.application.twin.twin_provider import TwinAbsent
from app.services.study_plan_service import StudyPlanService

# Product experience labels — keep in sync with pyproject / release notes.
APP_VERSION = "1.0.0"
INTERNAL_ALPHA_VERSION = "4.3"


@dataclass(frozen=True)
class InternalAlphaStatus:
    """Read-only Internal Alpha status for settings presentation."""

    app_version: str
    internal_alpha_version: str
    build_number: str
    internal_alpha_enabled: bool
    curriculum_label: str
    study_plan_label: str
    twin_status: str


class InternalAlphaStatusService:
    """Build informational Internal Alpha status for the current user."""

    @staticmethod
    def build_status(user_id: int) -> InternalAlphaStatus:
        """Assemble status fields for *user_id* without educational side effects."""
        plan = StudyPlanService.get_user_active_plan(user_id)
        if plan is None:
            curriculum_label = "No active curriculum"
            study_plan_label = "No active study plan"
        else:
            version = plan.curriculum_version or "—"
            curriculum_label = f"{plan.exam_name} · {version}"
            sitting = plan.exam_sitting or "—"
            study_plan_label = f"{plan.exam_name} · {sitting}"

        twin_status = InternalAlphaStatusService._twin_status_label(user_id)

        return InternalAlphaStatus(
            app_version=APP_VERSION,
            internal_alpha_version=INTERNAL_ALPHA_VERSION,
            build_number=_build_number(),
            internal_alpha_enabled=is_internal_alpha_enabled(),
            curriculum_label=curriculum_label,
            study_plan_label=study_plan_label,
            twin_status=twin_status,
        )

    @staticmethod
    def _twin_status_label(user_id: int) -> str:
        """Return a student-facing Twin presence label — never Twin contents."""
        result = build_twin_provider().retrieve(str(user_id))
        if isinstance(result, TwinAbsent):
            reason = result.reason.value
            if reason == "missing":
                return "Not yet calibrated"
            if reason == "missing_identity":
                return "Unavailable"
            if reason == "corrupt":
                return "Needs recalibration"
            return "Unavailable"
        return "Present"


def _build_number() -> str:
    """Resolve build number from environment, else a local development marker."""
    raw = os.environ.get("KWALITEC_BUILD_NUMBER", "").strip()
    return raw or "local"
