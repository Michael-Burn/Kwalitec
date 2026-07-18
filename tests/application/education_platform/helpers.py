"""Shared helpers for Educational Composition Layer tests."""

from __future__ import annotations

from datetime import UTC, datetime
from types import MappingProxyType

from app.application.education_platform.dto.education_request import EducationRequest
from app.application.education_platform.dto.generated_mission import GeneratedMission
from app.application.education_platform.dto.generated_session import GeneratedSession
from app.application.education_platform.dto.subject_plan import SubjectPlan
from app.application.education_platform.platform import EducationPlatform

NOW = datetime(2026, 7, 18, 16, 0, tzinfo=UTC)


class FakeCurriculum:
    """Deterministic CurriculumPort double."""

    def __init__(
        self,
        *,
        subject_id: str = "subject-1",
        curriculum_id: str = "curr-1",
        topic_ids: tuple[str, ...] = ("topic-a", "topic-b"),
        module_ids: tuple[str, ...] = ("mod-1",),
        available: bool = True,
        call_log: list[str] | None = None,
        component_version: str = "1.0.0",
    ) -> None:
        self._subject_id = subject_id
        self._curriculum_id = curriculum_id
        self._topic_ids = topic_ids
        self._module_ids = module_ids
        self._available = available
        self.calls: list[str] = call_log if call_log is not None else []
        self._component_version = component_version

    @property
    def component_id(self) -> str:
        return "curriculum"

    @property
    def component_version(self) -> str:
        return self._component_version

    def set_available(self, available: bool) -> None:
        self._available = available

    def is_available(self) -> bool:
        return self._available

    def resolve_subject(self, request: EducationRequest) -> SubjectPlan:
        self.calls.append("resolve_subject")
        sid = request.subject_id or self._subject_id
        cid = request.curriculum_id or self._curriculum_id
        return SubjectPlan(
            subject_id=sid,
            curriculum_id=cid,
            topic_ids=self._topic_ids,
            module_ids=self._module_ids,
            title=f"Subject {sid}",
        )

    def topic_available(self, topic_id: str) -> bool:
        return topic_id in self._topic_ids

    def ordered_topic_ids(self, subject_id: str | None = None) -> tuple[str, ...]:
        return self._topic_ids


class FakeBlueprint:
    """Deterministic BlueprintPort double."""

    def __init__(
        self,
        *,
        blueprint_id: str = "bp-standard",
        session_count: int = 2,
        available: bool = True,
        call_log: list[str] | None = None,
        component_version: str = "1.0.0",
    ) -> None:
        self._blueprint_id = blueprint_id
        self._session_count = session_count
        self._available = available
        self.calls: list[str] = call_log if call_log is not None else []
        self._component_version = component_version

    @property
    def component_id(self) -> str:
        return "blueprint"

    @property
    def component_version(self) -> str:
        return self._component_version

    def set_available(self, available: bool) -> None:
        self._available = available

    def is_available(self) -> bool:
        return self._available

    def select_blueprint_id(self, request: EducationRequest) -> str:
        self.calls.append("select_blueprint_id")
        return self._blueprint_id

    def estimate_session_count(self, request: EducationRequest) -> int:
        self.calls.append("estimate_session_count")
        return self._session_count


class FakeJourney:
    """Deterministic JourneyPort double."""

    def __init__(
        self,
        *,
        journey_id: str = "journey-1",
        available: bool = True,
        call_log: list[str] | None = None,
        component_version: str = "1.0.0",
    ) -> None:
        self._journey_id = journey_id
        self._known: set[str] = {journey_id}
        self._available = available
        self.calls: list[str] = call_log if call_log is not None else []
        self._component_version = component_version

    @property
    def component_id(self) -> str:
        return "journey"

    @property
    def component_version(self) -> str:
        return self._component_version

    def set_available(self, available: bool) -> None:
        self._available = available

    def is_available(self) -> bool:
        return self._available

    def create_journey(self, request: EducationRequest) -> str:
        self.calls.append("create_journey")
        if request.journey_id:
            self._known.add(request.journey_id)
            return request.journey_id
        self._known.add(self._journey_id)
        return self._journey_id

    def journey_exists(self, journey_id: str) -> bool:
        return journey_id in self._known


class FakeSession:
    """Deterministic SessionPort double."""

    def __init__(
        self,
        *,
        available: bool = True,
        call_log: list[str] | None = None,
        component_version: str = "1.0.0",
        topic_id: str = "topic-a",
    ) -> None:
        self._available = available
        self.calls: list[str] = call_log if call_log is not None else []
        self._component_version = component_version
        self._topic_id = topic_id

    @property
    def component_id(self) -> str:
        return "session"

    @property
    def component_version(self) -> str:
        return self._component_version

    def set_available(self, available: bool) -> None:
        self._available = available

    def is_available(self) -> bool:
        return self._available

    def plan_sessions(
        self,
        request: EducationRequest,
        *,
        journey_id: str,
        count: int = 1,
    ) -> tuple[GeneratedSession, ...]:
        self.calls.append("plan_sessions")
        topic = request.topic_id or self._topic_id
        return tuple(
            GeneratedSession(
                session_id=f"session-{i + 1}",
                journey_id=journey_id,
                topic_id=topic,
                sequence_index=i,
                effort="medium",
            )
            for i in range(max(1, count))
        )


class FakeActivity:
    """Deterministic ActivityPort double."""

    def __init__(
        self,
        *,
        activity_ids: tuple[str, ...] = ("act-1", "act-2", "act-3"),
        available: bool = True,
        call_log: list[str] | None = None,
        component_version: str = "1.0.0",
    ) -> None:
        self._activity_ids = activity_ids
        self._available = available
        self.calls: list[str] = call_log if call_log is not None else []
        self._component_version = component_version

    @property
    def component_id(self) -> str:
        return "activity"

    @property
    def component_version(self) -> str:
        return self._component_version

    def set_available(self, available: bool) -> None:
        self._available = available

    def is_available(self) -> bool:
        return self._available

    def plan_activity_ids(
        self,
        request: EducationRequest,
        *,
        session_id: str,
    ) -> tuple[str, ...]:
        self.calls.append("plan_activity_ids")
        return tuple(f"{session_id}:{a}" for a in self._activity_ids)


class FakeMission:
    """Deterministic MissionPort double."""

    def __init__(
        self,
        *,
        available: bool = True,
        call_log: list[str] | None = None,
        component_version: str = "1.0.0",
        mission_type: str = "today",
    ) -> None:
        self._available = available
        self.calls: list[str] = call_log if call_log is not None else []
        self._component_version = component_version
        self._mission_type = mission_type

    @property
    def component_id(self) -> str:
        return "mission"

    @property
    def component_version(self) -> str:
        return self._component_version

    def set_available(self, available: bool) -> None:
        self._available = available

    def is_available(self) -> bool:
        return self._available

    def generate_missions(
        self,
        request: EducationRequest,
        *,
        journey_id: str,
        session_id: str,
        topic_id: str,
    ) -> tuple[GeneratedMission, ...]:
        self.calls.append("generate_missions")
        mid = request.mission_id or "mission-1"
        return (
            GeneratedMission(
                mission_id=mid,
                learner_id=request.learner_id,
                journey_id=journey_id,
                topic_id=topic_id,
                session_id=session_id,
                mission_type=self._mission_type,
                effort="medium",
                metadata=MappingProxyType({"source": "fake"}),
            ),
        )


def make_request(
    *,
    workflow: str = "generate_subject",
    learner_id: str = "learner-1",
    curriculum_id: str | None = "curr-1",
    subject_id: str | None = "subject-1",
    topic_id: str | None = "topic-a",
    journey_id: str | None = None,
    session_id: str | None = None,
    mission_id: str | None = None,
    correlation_id: str | None = "corr-1",
) -> EducationRequest:
    return EducationRequest(
        workflow=workflow,
        learner_id=learner_id,
        curriculum_id=curriculum_id,
        subject_id=subject_id,
        topic_id=topic_id,
        journey_id=journey_id,
        session_id=session_id,
        mission_id=mission_id,
        correlation_id=correlation_id,
    )


def make_platform(
    *,
    curriculum: FakeCurriculum | None = None,
    blueprint: FakeBlueprint | None = None,
    journey: FakeJourney | None = None,
    session: FakeSession | None = None,
    activity: FakeActivity | None = None,
    mission: FakeMission | None = None,
    require_complete: bool = False,
    omit: frozenset[str] | set[str] | None = None,
) -> EducationPlatform:
    """Build a fully (or partially) wired EducationPlatform with fakes."""
    omit = set(omit or ())
    kwargs: dict = {"require_complete": require_complete, "clock": lambda: NOW}
    if "curriculum" not in omit:
        kwargs["curriculum"] = (
            curriculum if curriculum is not None else FakeCurriculum()
        )
    if "blueprint" not in omit:
        kwargs["blueprint"] = (
            blueprint if blueprint is not None else FakeBlueprint()
        )
    if "journey" not in omit:
        kwargs["journey"] = journey if journey is not None else FakeJourney()
    if "session" not in omit:
        kwargs["session"] = session if session is not None else FakeSession()
    if "activity" not in omit:
        kwargs["activity"] = activity if activity is not None else FakeActivity()
    if "mission" not in omit:
        kwargs["mission"] = mission if mission is not None else FakeMission()
    return EducationPlatform.create(**kwargs)


def make_full_ports() -> dict[str, object]:
    return {
        "curriculum": FakeCurriculum(),
        "blueprint": FakeBlueprint(),
        "journey": FakeJourney(),
        "session": FakeSession(),
        "activity": FakeActivity(),
        "mission": FakeMission(),
    }
