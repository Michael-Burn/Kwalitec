"""TemplateMapper — view models → Jinja-friendly template contexts.

Framework-independent serialisation of presentation view models. Converts
dataclasses and enums into plain dicts / scalars suitable for ``render_template``.
Never contains educational logic, persistence, or AI.
"""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from enum import Enum
from typing import Any

from presentation.dashboard.dashboard_view_model import DashboardViewModel
from presentation.mission_workspace.workspace_view_model import (
    MissionWorkspaceViewModel,
)
from presentation.reflection.reflection_view_model import ReflectionViewModel
from presentation.study_session.session_view_model import StudySessionViewModel

DASHBOARD_TEMPLATE = "eos/dashboard.html"
MISSION_TEMPLATE = "eos/mission.html"
SESSION_TEMPLATE = "eos/session.html"
REFLECTION_TEMPLATE = "eos/reflection.html"
LOGIN_TEMPLATE = "eos/login.html"


class TemplateMapper:
    """Map presentation view models into template keyword arguments."""

    @classmethod
    def for_dashboard(cls, view_model: DashboardViewModel) -> dict[str, Any]:
        """Build template context for the student dashboard surface."""
        return {
            "page": "dashboard",
            "template_name": DASHBOARD_TEMPLATE,
            "view": cls.serialize(view_model),
            "title": _title(view_model),
            "container_width": _container_width(view_model),
        }

    @classmethod
    def for_mission(cls, view_model: MissionWorkspaceViewModel) -> dict[str, Any]:
        """Build template context for the mission workspace surface."""
        return {
            "page": "mission",
            "template_name": MISSION_TEMPLATE,
            "view": cls.serialize(view_model),
            "title": getattr(view_model, "mission_title", "") or "Mission",
            "container_width": "content",
        }

    @classmethod
    def for_session(cls, view_model: StudySessionViewModel) -> dict[str, Any]:
        """Build template context for the guided study-session surface."""
        return {
            "page": "session",
            "template_name": SESSION_TEMPLATE,
            "view": cls.serialize(view_model),
            "title": _title(view_model),
            "container_width": _container_width(view_model),
        }

    @classmethod
    def for_login(cls, *, student_id: str = "", error: str = "") -> dict[str, Any]:
        """Build template context for the student login surface."""
        return {
            "page": "login",
            "template_name": LOGIN_TEMPLATE,
            "title": "Student Login",
            "student_id": student_id or "",
            "error": error or "",
            "container_width": "narrow",
        }

    @classmethod
    def for_reflection(cls, view_model: ReflectionViewModel) -> dict[str, Any]:
        """Build template context for the reflection workspace surface."""
        return {
            "page": "reflection",
            "template_name": REFLECTION_TEMPLATE,
            "view": cls.serialize(view_model),
            "title": _title(view_model),
            "container_width": _container_width(view_model),
            "session_id": getattr(view_model, "session_id", "") or "",
            "is_ready": bool(getattr(view_model, "is_ready", False)),
        }

    @classmethod
    def serialize(cls, value: Any) -> Any:
        """Recursively convert dataclasses / enums into plain Python values."""
        if value is None:
            return None
        if isinstance(value, Enum):
            return value.value
        if is_dataclass(value) and not isinstance(value, type):
            return {
                field.name: cls.serialize(getattr(value, field.name))
                for field in fields(value)
            }
        if isinstance(value, tuple):
            return [cls.serialize(item) for item in value]
        if isinstance(value, list):
            return [cls.serialize(item) for item in value]
        if isinstance(value, dict):
            return {str(key): cls.serialize(item) for key, item in value.items()}
        return value


def _title(view_model: Any) -> str:
    header = getattr(view_model, "header", None)
    title = getattr(header, "title", None)
    if title:
        return str(title)
    return ""


def _container_width(view_model: Any) -> str:
    width = getattr(view_model, "container_width", None)
    if isinstance(width, Enum):
        return width.value
    if width is None:
        return ""
    return str(width)
