"""Examination identity for Experience projections.

Canonical source: active Study Plan via ``StudyPlanService.get_user_active_plan``.
Shared by Profile (CQ-002 / PX-003 B2) and Student Home (RC-2026.07.29-06).
"""

from __future__ import annotations


def exam_label_from_active_plan(student_id: str) -> str:
    """Best-effort examination name from the active Study Plan (fail-open).

    Returns "" when the identity is non-numeric, no active plan exists, or
    the Study Plan service is unavailable — callers keep Twin/readiness labels.
    """
    try:
        user_id = int(student_id)
    except (TypeError, ValueError):
        return ""
    try:
        from app.services.study_plan_service import StudyPlanService

        plan = StudyPlanService.get_user_active_plan(user_id)
    except Exception:  # noqa: BLE001 — presentation fallback only
        return ""
    if plan is None:
        return ""
    return str(getattr(plan, "exam_name", "") or "").strip()
