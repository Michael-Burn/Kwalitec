"""SessionMissionAdapter — MissionPort for Learning Session Experience."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from app.infrastructure.adapters.mission.experience_adapter import (
    ExperienceMissionAdapter,
)
from app.infrastructure.adapters.student_experience.defaults import (
    default_mission_document,
    seeded_demo_mission,
)
from app.infrastructure.adapters.student_experience.projection_store import (
    ExperienceProjectionStore,
)
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.session.defaults import default_mission_session


class SessionMissionAdapter:
    """Production adapter implementing Session Experience MissionPort.

    Reuses ExperienceMissionAdapter / Mission projections. Never generates
    missions or recommends next actions.
    """

    ADAPTER_ID = "session_mission"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        mission: ExperienceMissionAdapter | None = None,
        store: ExperienceProjectionStore | None = None,
        mission_engine: Any | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        available: bool = True,
        auto_provision: bool = True,
        seed_demo: bool = True,
    ) -> None:
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._available = available
        self._auto_provision = auto_provision
        self._seed_demo = seed_demo
        self._store = store
        self._delegate = mission or ExperienceMissionAdapter(
            store=store or ExperienceProjectionStore(),
            mission_engine=mission_engine,
            diagnostics=self._diagnostics,
            available=available,
            auto_provision=auto_provision,
        )
        self._diagnostics.record_health(
            self.ADAPTER_ID,
            available=available,
            version=self.ADAPTER_VERSION,
        )

    @property
    def component_id(self) -> str:
        return self.ADAPTER_ID

    @property
    def component_version(self) -> str:
        return self.ADAPTER_VERSION

    def is_available(self) -> bool:
        return self._available and self._delegate.is_available()

    def set_available(self, available: bool) -> None:
        self._available = available
        self._delegate.set_available(available)
        self._diagnostics.record_health(
            self.ADAPTER_ID,
            available=available,
            version=self.ADAPTER_VERSION,
        )

    @property
    def delegate(self) -> ExperienceMissionAdapter:
        """Underlying Experience mission adapter (reuse boundary)."""
        return self._delegate

    def put_projection(self, student_id: str, document: dict[str, Any]) -> None:
        """Provision opaque Mission projection via the Experience adapter."""
        self._delegate.put_projection(student_id, document)

    def get_todays_session(self, student_id: str) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        self._ensure_learner(student_id)
        session = self._delegate.get_todays_session(student_id)
        if session is not None:
            return dict(session)
        if not self._auto_provision:
            return None
        return default_mission_session(student_id.strip())

    def get_session_status(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        self._diagnostics.record_call(self.ADAPTER_ID)
        self._ensure_learner(student_id)
        status = self._delegate.get_session_status(
            student_id, session_id=session_id
        )
        if status is not None:
            return dict(status)
        today = self.get_todays_session(student_id) or {}
        if str(today.get("session_id") or "") == session_id.strip():
            return dict(today)
        return None

    def _ensure_learner(self, student_id: str) -> None:
        sid = student_id.strip()
        existing = self._delegate.get_todays_session(sid)
        if existing is not None:
            return
        if self._seed_demo and self._auto_provision:
            self._delegate.put_projection(sid, seeded_demo_mission(sid))
        elif self._auto_provision:
            doc = default_mission_document(sid)
            doc["todays_session"] = default_mission_session(sid)
            doc["sessions"] = {
                str(doc["todays_session"]["session_id"]): deepcopy(
                    doc["todays_session"]
                )
            }
            self._delegate.put_projection(sid, doc)
