"""Student Runtime Coordinator — Home → Session spine (SR-002 P1).

Compose-only: Mission accept semantics + LearningSessionRuntime create/resume
+ Session Experience overview provisioning. Does not invent educational
substance, evidence, Twin writes, or progress advancement.
"""

from __future__ import annotations

import logging
from typing import Any
from uuid import uuid4

from app.application.config.v2_flags import (
    Version2FeatureFlags,
    resolve_v2_feature_flags,
)
from app.application.educational_runtime_engine.dto import MissionInstanceSnapshot
from app.application.educational_runtime_engine.exceptions import (
    IllegalRuntimeState,
    MissionAlreadyCompleted,
    MissionInstanceNotFound,
)
from app.application.educational_runtime_engine.service import (
    EducationalRuntimeEngineService,
)
from app.application.learning_session.runtime import (
    LearningSessionRuntime,
)
from app.application.student_runtime.dto import SessionBindingResult
from app.application.student_runtime.exceptions import (
    MissionNotAcceptable,
    SessionSpineUnavailable,
)
from app.domain.educational_runtime_engine.student_facing_identity import (
    format_learning_objective_label,
)
from app.domain.learning_journey.entities.learning_journey import LearningJourney
from app.domain.learning_journey.entities.learning_objective import (
    LearningObjective,
    ObjectiveKind,
)
from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate
from app.domain.learning_journey.value_objects.journey_state import JourneyState

logger = logging.getLogger(__name__)

_AUTHORITY = "learning_session_runtime"


class StudentRuntimeCoordinator:
    """Compose Mission Lifecycle + LearningSessionRuntime for published path.

    Session Experience remains an HTTP adapter; this coordinator elevates
    LearningSessionRuntime as session execution AUTHORITY for the spine.
    """

    SERVICE_ID = "student_runtime_coordinator"
    SERVICE_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        runtime_engine: EducationalRuntimeEngineService | None = None,
        session_runtime: LearningSessionRuntime | None = None,
        persistence: Any | None = None,
        session_overview_writer: Any | None = None,
        flags: Version2FeatureFlags | None = None,
        id_factory=None,
    ) -> None:
        self._engine = runtime_engine or EducationalRuntimeEngineService()
        self._lsr = session_runtime or LearningSessionRuntime()
        self._persistence = persistence
        self._overview_writer = session_overview_writer
        self._flags = flags
        self._id_factory = id_factory or (lambda: uuid4().hex[:12])

    def session_primary_enabled(self) -> bool:
        flags = self._flags or resolve_v2_feature_flags()
        return bool(flags.SR_SESSION_PRIMARY)

    def find_open_session(
        self,
        student_id: str,
        *,
        mission_instance_id: str | None = None,
    ) -> SessionBindingResult | None:
        """Return an open LearningSessionRuntime binding, if any."""
        store = self._require_persistence()
        record = store.find_open(
            student_id=str(student_id).strip(),
            mission_instance_id=(mission_instance_id or "").strip() or None,
        )
        if record is None:
            return None
        return SessionBindingResult(
            session_id=str(record["session_id"]),
            mission_instance_id=str(record.get("mission_instance_id") or ""),
            student_id=str(record["student_id"]),
            topic_title=str(record.get("topic_title") or ""),
            topic_id=str(record.get("topic_id") or ""),
            estimated_minutes=_optional_int(record.get("estimated_minutes")),
            resumed=True,
            phase=str(record.get("phase") or "active"),
            authority=_AUTHORITY,
        )

    def accept_and_start_session(
        self,
        *,
        user_id: int,
        mission_instance_id: str,
        topic_title: str = "",
        estimated_minutes: int | None = None,
    ) -> SessionBindingResult:
        """Mission Accepted ≡ create/start LearningSessionRuntime session.

        Idempotent resume when an open session already exists for the mission.
        Does not complete the mission or emit TOPIC_COMPLETED.
        """
        if not self.session_primary_enabled():
            raise SessionSpineUnavailable("SR_SESSION_PRIMARY is off")

        mid = (mission_instance_id or "").strip()
        if not mid:
            raise MissionNotAcceptable("mission_instance_id required")

        sid = str(user_id)
        existing = self.find_open_session(sid, mission_instance_id=mid)
        if existing is not None:
            if self._open_session_is_oversized(
                student_id=sid, session_id=existing.session_id
            ) or self._open_session_is_placeholder(
                student_id=sid, session_id=existing.session_id
            ):
                self._supersede_open_session(
                    student_id=sid,
                    session_id=existing.session_id,
                    mission_instance_id=mid,
                )
            else:
                return existing

        mission = self._load_mission(user_id=user_id, mission_instance_id=mid)
        title = (topic_title or mission.title or "").strip() or "Today's Study Session"
        minutes = estimated_minutes
        if minutes is None and mission.quality is not None:
            minutes = int(mission.quality.estimated_duration_minutes or 0) or None

        objectives = None
        substance_flag = self._substance_enabled()
        substance = None
        if substance_flag:
            substance = self._plan_substance(mission, topic_title=title)
            if substance is None:
                raise SessionSpineUnavailable(
                    "published curriculum substance is unavailable for this mission"
                )
            topic_l = (substance.topic_title or "").strip().lower()
            if topic_l == "core methods":
                raise SessionSpineUnavailable(
                    "session substance resolved to placeholder Core methods"
                )
            if substance.topic_title:
                title = substance.topic_title.strip() or title
            if substance.learning_objectives:
                objectives = tuple(
                    LearningObjective.create(
                        obj.objective_id[:64],
                        mission.curriculum_identity,
                        mission.topic_id,
                        ObjectiveKind.UNDERSTAND,
                        title=obj.text[:200],
                        sequence_index=index,
                    )
                    for index, obj in enumerate(substance.learning_objectives)
                )
        session_id = f"lsr-{self._id_factory()}"
        journey = self._journey_for_mission(sid, mission, session_id=session_id)
        handle = self._lsr.create_session(
            journey,
            topic_id=mission.topic_id,
            objectives=objectives,
            estimated_effort=_effort_from_minutes(minutes),
            session_id=session_id,
        )
        handle = self._lsr.prepare_session(handle)
        handle = self._lsr.start_session(handle)

        try:
            accepted = self._engine.accept_mission(
                user_id=user_id,
                mission_instance_id=mid,
                session_id=session_id,
            )
            if accepted is not None:
                mission = accepted
        except MissionAlreadyCompleted as exc:
            raise MissionNotAcceptable(str(exc)) from exc
        except (MissionInstanceNotFound, IllegalRuntimeState) as exc:
            raise MissionNotAcceptable(str(exc)) from exc

        store = self._require_persistence()
        store.save_binding(
            student_id=sid,
            mission_instance_id=mid,
            handle=handle,
            topic_title=title,
            topic_id=mission.topic_id,
            estimated_minutes=minutes,
            curriculum_identity=mission.curriculum_identity,
        )
        if substance is not None:
            self._provision_substance_sequence(
                student_id=sid,
                session_id=session_id,
                substance=substance,
            )
        self._provision_overview(
            student_id=sid,
            session_id=session_id,
            mission_id=mid,
            topic_title=title,
            estimated_minutes=minutes,
            substance=substance,
        )

        return SessionBindingResult(
            session_id=session_id,
            mission_instance_id=mid,
            student_id=sid,
            topic_title=title,
            topic_id=mission.topic_id,
            estimated_minutes=minutes,
            resumed=False,
            phase=str(handle.phase.value),
            authority=_AUTHORITY,
        )

    def resume_session(
        self,
        *,
        user_id: int,
        session_id: str | None = None,
        mission_instance_id: str | None = None,
    ) -> SessionBindingResult:
        """Resume an open LearningSessionRuntime session for Home Primary."""
        if not self.session_primary_enabled():
            raise SessionSpineUnavailable("SR_SESSION_PRIMARY is off")

        store = self._require_persistence()
        sid = str(user_id)
        record = None
        if session_id:
            record = store.load(session_id=session_id.strip())
            if record is not None and str(record.get("student_id")) != sid:
                record = None
        if record is None:
            record = store.find_open(
                student_id=sid,
                mission_instance_id=(mission_instance_id or "").strip() or None,
            )
        if record is None:
            raise SessionSpineUnavailable("no open study session to resume")

        if str(record.get("status") or "") in {"superseded", "completed"}:
            raise SessionSpineUnavailable("study session is no longer open")

        if self._open_session_is_oversized(
            student_id=sid, session_id=str(record["session_id"])
        ) or self._open_session_is_placeholder(
            student_id=sid, session_id=str(record["session_id"])
        ):
            self._supersede_open_session(
                student_id=sid,
                session_id=str(record["session_id"]),
                mission_instance_id=str(record.get("mission_instance_id") or ""),
            )
            raise SessionSpineUnavailable(
                "study session was a placeholder or exceeded session length; "
                "start again from Home"
            )

        # Mission may have been retired by session-budget rechunk.
        bound_mid = str(record.get("mission_instance_id") or "").strip()
        if bound_mid:
            try:
                self._load_mission(user_id=user_id, mission_instance_id=bound_mid)
            except MissionNotAcceptable as exc:
                self._supersede_open_session(
                    student_id=sid,
                    session_id=str(record["session_id"]),
                    mission_instance_id=bound_mid,
                )
                raise SessionSpineUnavailable(str(exc)) from exc

        handle = store.load_handle(session_id=str(record["session_id"]))
        if handle is not None:
            phase = str(handle.phase.value)
            if phase == "paused":
                handle = self._lsr.resume_session(handle)
                store.save_binding(
                    student_id=sid,
                    mission_instance_id=str(record.get("mission_instance_id") or ""),
                    handle=handle,
                    topic_title=str(record.get("topic_title") or ""),
                    topic_id=str(record.get("topic_id") or ""),
                    estimated_minutes=_optional_int(record.get("estimated_minutes")),
                    curriculum_identity=str(record.get("curriculum_identity") or ""),
                )
                phase = str(handle.phase.value)
        else:
            phase = str(record.get("phase") or "active")

        return SessionBindingResult(
            session_id=str(record["session_id"]),
            mission_instance_id=str(record.get("mission_instance_id") or ""),
            student_id=sid,
            topic_title=str(record.get("topic_title") or ""),
            topic_id=str(record.get("topic_id") or ""),
            estimated_minutes=_optional_int(record.get("estimated_minutes")),
            resumed=True,
            phase=phase,
            authority=_AUTHORITY,
        )

    def defer_mission(
        self,
        *,
        user_id: int,
        mission_instance_id: str,
        reason_code: str = "not_today",
    ) -> None:
        """Preserve ILE-004 Deferred without starting a session."""
        mid = (mission_instance_id or "").strip()
        if not mid:
            raise MissionNotAcceptable("mission_instance_id required")
        try:
            self._engine.defer_mission(
                user_id=user_id,
                mission_instance_id=mid,
                reason_code=reason_code,
            )
        except (
            MissionInstanceNotFound,
            IllegalRuntimeState,
            MissionAlreadyCompleted,
        ) as exc:
            raise MissionNotAcceptable(str(exc)) from exc

    def _load_mission(
        self, *, user_id: int, mission_instance_id: str
    ) -> MissionInstanceSnapshot:
        mission = self._engine.get_mission_instance(
            user_id=user_id,
            mission_instance_id=mission_instance_id,
        )
        if mission is None:
            raise MissionNotAcceptable(
                f"mission not found: {mission_instance_id}"
            )
        status = (mission.status or "").lower()
        if status == "completed":
            raise MissionNotAcceptable("mission already completed")
        return mission

    def _journey_for_mission(
        self,
        student_id: str,
        mission: MissionInstanceSnapshot,
        *,
        session_id: str,
    ) -> LearningJourney:
        journey_id = f"jrn-{mission.mission_instance_id}"
        objective = LearningObjective.create(
            f"obj-{mission.topic_id}"[:64],
            mission.curriculum_identity,
            mission.topic_id,
            ObjectiveKind.UNDERSTAND,
            title=(mission.title or "Study today's topic")[:200],
            sequence_index=0,
        )
        return LearningJourney.create(
            journey_id,
            student_id,
            mission.topic_id,
            mission.curriculum_identity,
            state=JourneyState.ACTIVE,
            objectives=(objective,),
            study_plan_id=mission.plan_instance_id,
        )

    def _provision_overview(
        self,
        *,
        student_id: str,
        session_id: str,
        mission_id: str,
        topic_title: str,
        estimated_minutes: int | None,
        substance: Any | None = None,
    ) -> None:
        writer = self._overview_writer
        if writer is None:
            return
        learning_objectives: list[str] = []
        activity_count = 3
        substance_status = "incomplete"
        why = (
            f"Today's Mission focuses on {topic_title}."
            if topic_title
            else "Today's Mission is ready."
        )
        objective = f"Strengthen {topic_title}" if topic_title else "Today's study"
        if substance is not None:
            learning_objectives = [
                format_learning_objective_label(code=obj.code, text=obj.text)
                for obj in substance.learning_objectives
            ]
            activity_count = max(1, substance.activity_count)
            substance_status = getattr(substance, "source", None) or "package"
            if substance_status == "educational_package":
                substance_status = "educational_package"
            else:
                substance_status = "package"
            rationale = (getattr(substance, "educational_rationale", "") or "").strip()
            if rationale:
                why = rationale
            if substance.learning_objectives:
                objective = format_learning_objective_label(
                    code=substance.learning_objectives[0].code,
                    text=substance.learning_objectives[0].text,
                )
        document = {
            "objective": objective,
            "learning_goal": topic_title or "Complete today's Study Session",
            "why_studying": why,
            "estimated_minutes": estimated_minutes or 30,
            "activity_count": activity_count,
            "topics": (topic_title or "Today's topic",),
            "topic_title": topic_title,
            "learning_objectives": tuple(learning_objectives),
            "educational_flow": (
                "learning_objectives",
                "read",
                "worked_example",
                "practice",
                "reflection",
                "ready_to_finish",
            ),
            "status": "in_progress",
            "mission_id": mission_id,
            "session_id": session_id,
            "student_id": student_id,
            "authority": _AUTHORITY,
            "substance": substance_status,
        }
        writer.put_overview(student_id, session_id=session_id, document=document)

    def _substance_enabled(self) -> bool:
        flags = self._flags or resolve_v2_feature_flags()
        return bool(getattr(flags, "SR_SESSION_SUBSTANCE", False))

    def _plan_substance(self, mission: MissionInstanceSnapshot, *, topic_title: str):
        from app.application.learning_session.substance_planner import (
            EducationalSubstancePlanner,
        )

        quality = mission.quality
        rationale = ""
        objective_ids: tuple[str, ...] = ()
        minutes = None
        if quality is not None:
            rationale = (quality.educational_rationale or "").strip()
            objective_ids = tuple(quality.objective_ids or ())
            minutes = int(quality.estimated_duration_minutes or 0) or None
        return EducationalSubstancePlanner().plan_for_topic(
            curriculum_identity=mission.curriculum_identity,
            topic_id=mission.topic_id,
            topic_title=topic_title or mission.title,
            task_descriptions=tuple(mission.task_descriptions or ()),
            educational_rationale=rationale,
            objective_ids=objective_ids,
            session_minutes=minutes,
        )

    def _open_session_is_placeholder(
        self, *, student_id: str, session_id: str
    ) -> bool:
        """True when a sitting still carries the Phase-I Core methods stub."""
        store = self._require_persistence()
        record = store.load(session_id=session_id.strip()) or {}
        topic = str(record.get("topic_title") or "").strip().lower()
        if "core methods" in topic:
            return True
        seq = store.store.get(
            "activity.sequence",
            f"{student_id.strip()}::{session_id.strip()}",
        )
        if not isinstance(seq, dict):
            overview = store.store.get(
                "runtime.overview",
                f"{student_id.strip()}::{session_id.strip()}",
            )
            blob = str(overview or "")
            return "core methods" in blob.lower()
        blob = str(seq.get("topic_title") or "") + str(
            seq.get("activities") or ()
        )
        return "core methods" in blob.lower()

    def _open_session_is_oversized(
        self, *, student_id: str, session_id: str
    ) -> bool:
        """True when a persisted sitting still packs more LOs than one session."""
        from app.application.curriculum_intelligence.objective_chunk import (
            select_objectives_for_session,
        )

        store = self._require_persistence()
        seq = store.store.get(
            "activity.sequence",
            f"{student_id.strip()}::{session_id.strip()}",
        )
        if not isinstance(seq, dict):
            return False
        raw = seq.get("learning_objectives") or ()
        ids = []
        for item in raw:
            if isinstance(item, dict):
                oid = str(item.get("objective_id") or "").strip()
                if oid:
                    ids.append(oid)
            elif isinstance(item, str) and item.strip():
                ids.append(item.strip())
        if len(ids) <= 1:
            return False
        chunked = select_objectives_for_session(ids, session_minutes=60)
        return len(chunked) < len(ids)

    def _supersede_open_session(
        self,
        *,
        student_id: str,
        session_id: str,
        mission_instance_id: str = "",
    ) -> None:
        from app.infrastructure.adapters.learning_session.persistence import (
            NS_HANDLE,
            NS_MISSION,
            NS_OPEN,
        )

        store = self._require_persistence()
        sid = student_id.strip()
        key = session_id.strip()
        handle = store.load(session_id=key) or {}
        store.store.save(
            NS_HANDLE,
            key,
            {
                **handle,
                "status": "superseded",
                "phase": "abandoned",
                "superseded_reason": "session_budget_rechunk",
            },
        )
        open_ptr = store.store.get(NS_OPEN, sid)
        if open_ptr and str(open_ptr.get("session_id")) == key:
            store.store.delete(NS_OPEN, sid)
        mid = (
            mission_instance_id
            or str(handle.get("mission_instance_id") or "")
        ).strip()
        if mid:
            store.store.delete(NS_MISSION, f"{sid}::{mid}")

    def _provision_substance_sequence(
        self,
        *,
        student_id: str,
        session_id: str,
        substance: Any,
    ) -> None:
        store = self._require_persistence()
        session_store = getattr(store, "store", None)
        if session_store is None:
            return
        from app.infrastructure.adapters.learning_session import (
            package_activity_engine as pkg_engine,
        )

        pkg_engine.PackageActivityEngine(
            store=session_store,
            persistence=store,
        ).provision_sequence(
            student_id, session_id=session_id, substance=substance
        )

    def _require_persistence(self) -> Any:
        if self._persistence is None:
            from app.infrastructure.adapters.learning_session.persistence import (
                LearningSessionPersistenceAdapter,
            )

            self._persistence = LearningSessionPersistenceAdapter()
        return self._persistence


def _effort_from_minutes(minutes: int | None) -> EffortEstimate:
    if minutes is None:
        return EffortEstimate.MEDIUM
    if minutes <= 20:
        return EffortEstimate.LOW
    if minutes >= 50:
        return EffortEstimate.HIGH
    return EffortEstimate.MEDIUM


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
