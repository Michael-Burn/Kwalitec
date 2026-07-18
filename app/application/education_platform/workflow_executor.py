"""Workflow executor — runs Educational Core port steps in order.

Example chain:
Curriculum → Blueprint → Journey → Sessions → Activities → Mission → Response

Never invents educational content. Never uses AI.
"""

from __future__ import annotations

import time
from types import MappingProxyType

from app.application.education_platform.dependency_registry import DependencyRegistry
from app.application.education_platform.dto.education_request import EducationRequest
from app.application.education_platform.dto.education_response import EducationResponse
from app.application.education_platform.dto.generated_mission import GeneratedMission
from app.application.education_platform.dto.generated_session import GeneratedSession
from app.application.education_platform.dto.platform_snapshot import PlatformSnapshot
from app.application.education_platform.dto.subject_plan import SubjectPlan
from app.application.education_platform.dto.workflow_result import WorkflowResult
from app.application.education_platform.exceptions import (
    PortUnavailable,
    WorkflowError,
)
from app.application.education_platform.platform_validator import PlatformValidator
from app.application.education_platform.policies.orchestration_policy import (
    WORKFLOW_BUILD_PLATFORM_SNAPSHOT,
    WORKFLOW_GENERATE_DAILY_MISSIONS,
    WORKFLOW_GENERATE_JOURNEY,
    WORKFLOW_GENERATE_LEARNING_ACTIVITIES,
    WORKFLOW_GENERATE_LEARNING_SESSIONS,
    WORKFLOW_VALIDATE_PLATFORM,
    OrchestrationPolicy,
)


class WorkflowExecutor:
    """Execute a workflow by invoking registered ports in step order."""

    PLATFORM_VERSION = "education-platform-1"

    def __init__(self, *, validator: PlatformValidator | None = None) -> None:
        self._validator = validator or PlatformValidator()

    def run(
        self,
        *,
        request: EducationRequest,
        steps: tuple[str, ...],
        registry: DependencyRegistry,
    ) -> EducationResponse:
        """Run ``request.workflow`` using ``steps`` against ``registry``."""
        workflow = request.workflow
        started = time.perf_counter()
        step_timings: dict[str, float] = {}
        completed: list[str] = []

        subject_plan: SubjectPlan | None = None
        blueprint_id: str | None = None
        journey_id: str | None = request.journey_id
        sessions: tuple[GeneratedSession, ...] = ()
        activity_ids: tuple[str, ...] = ()
        missions: tuple[GeneratedMission, ...] = ()
        snapshot: PlatformSnapshot | None = None
        validation_passed: bool | None = None
        validation_issues: tuple[str, ...] = ()

        try:
            if workflow == WORKFLOW_VALIDATE_PLATFORM:
                result = self._validator.validate(registry)
                validation_passed = result.passed
                validation_issues = result.issues
                completed.append("validate")
                step_timings["validate"] = (
                    time.perf_counter() - started
                ) * 1000.0
            else:
                for step in steps:
                    step_started = time.perf_counter()
                    port = registry.get(step)
                    if not port.is_available():
                        raise PortUnavailable(
                            f"Port {step!r} is unavailable"
                        )

                    if step == "curriculum":
                        subject_plan = port.resolve_subject(request)
                    elif step == "blueprint":
                        blueprint_id = port.select_blueprint_id(request)
                    elif step == "journey":
                        if journey_id is None:
                            journey_id = port.create_journey(request)
                    elif step == "session":
                        count = 1
                        if blueprint_id is not None and registry.has("blueprint"):
                            bp = registry.get("blueprint")
                            count = max(1, int(bp.estimate_session_count(request)))
                        if journey_id is None:
                            raise WorkflowError(
                                "session step requires journey_id"
                            )
                        sessions = port.plan_sessions(
                            request, journey_id=journey_id, count=count
                        )
                    elif step == "activity":
                        if not sessions:
                            raise WorkflowError(
                                "activity step requires planned sessions"
                            )
                        session_id = (
                            request.session_id or sessions[0].session_id
                        )
                        activity_ids = port.plan_activity_ids(
                            request, session_id=session_id
                        )
                        # Attach activity ids onto first session structurally
                        # by rebuilding an immutable copy when empty.
                        first = sessions[0]
                        if not first.activity_ids and activity_ids:
                            updated = GeneratedSession(
                                session_id=first.session_id,
                                journey_id=first.journey_id,
                                topic_id=first.topic_id,
                                sequence_index=first.sequence_index,
                                effort=first.effort,
                                activity_ids=activity_ids,
                                metadata=first.metadata,
                            )
                            sessions = (updated, *sessions[1:])
                    elif step == "mission":
                        if journey_id is None or not sessions:
                            raise WorkflowError(
                                "mission step requires journey_id and sessions"
                            )
                        topic_id = request.topic_id
                        if topic_id is None and subject_plan and subject_plan.topic_ids:
                            topic_id = subject_plan.topic_ids[0]
                        if topic_id is None:
                            topic_id = sessions[0].topic_id
                        missions = port.generate_missions(
                            request,
                            journey_id=journey_id,
                            session_id=sessions[0].session_id,
                            topic_id=topic_id,
                        )
                    else:
                        raise WorkflowError(f"Unknown workflow step: {step!r}")

                    completed.append(step)
                    step_timings[step] = (
                        time.perf_counter() - step_started
                    ) * 1000.0

                if workflow == WORKFLOW_BUILD_PLATFORM_SNAPSHOT:
                    snapshot = self._build_snapshot(
                        request=request,
                        registry=registry,
                        subject_plan=subject_plan,
                        journey_id=journey_id,
                        sessions=sessions,
                        missions=missions,
                    )

            duration_ms = (time.perf_counter() - started) * 1000.0
            workflow_result = WorkflowResult(
                workflow=workflow,
                success=True,
                steps=tuple(completed),
                duration_ms=duration_ms,
                step_timings_ms=MappingProxyType(step_timings),
            )
            include_journey = workflow in {
                WORKFLOW_GENERATE_JOURNEY,
                WORKFLOW_GENERATE_LEARNING_SESSIONS,
                WORKFLOW_GENERATE_LEARNING_ACTIVITIES,
                WORKFLOW_GENERATE_DAILY_MISSIONS,
                WORKFLOW_BUILD_PLATFORM_SNAPSHOT,
            }
            include_sessions = workflow in {
                WORKFLOW_GENERATE_LEARNING_SESSIONS,
                WORKFLOW_GENERATE_LEARNING_ACTIVITIES,
                WORKFLOW_GENERATE_DAILY_MISSIONS,
                WORKFLOW_BUILD_PLATFORM_SNAPSHOT,
            }
            include_activities = workflow in {
                WORKFLOW_GENERATE_LEARNING_ACTIVITIES,
                WORKFLOW_GENERATE_DAILY_MISSIONS,
            }
            include_missions = workflow in {
                WORKFLOW_GENERATE_DAILY_MISSIONS,
                WORKFLOW_BUILD_PLATFORM_SNAPSHOT,
            }
            include_subject = workflow != WORKFLOW_VALIDATE_PLATFORM
            return EducationResponse(
                workflow=workflow,
                success=True,
                request_correlation_id=request.correlation_id,
                subject_plan=subject_plan if include_subject else None,
                journey_id=journey_id if include_journey else None,
                blueprint_id=blueprint_id if include_journey else None,
                sessions=sessions if include_sessions else (),
                activity_ids=activity_ids if include_activities else (),
                missions=missions if include_missions else (),
                snapshot=snapshot,
                workflow_result=workflow_result,
                validation_passed=validation_passed,
                validation_issues=validation_issues,
            )
        except Exception as exc:
            duration_ms = (time.perf_counter() - started) * 1000.0
            workflow_result = WorkflowResult(
                workflow=workflow,
                success=False,
                steps=tuple(completed),
                duration_ms=duration_ms,
                step_timings_ms=MappingProxyType(step_timings),
                error=f"{type(exc).__name__}: {exc}",
            )
            return EducationResponse(
                workflow=workflow,
                success=False,
                request_correlation_id=request.correlation_id,
                subject_plan=subject_plan,
                journey_id=journey_id,
                blueprint_id=blueprint_id,
                sessions=sessions,
                activity_ids=activity_ids,
                missions=missions,
                snapshot=snapshot,
                workflow_result=workflow_result,
                validation_passed=validation_passed,
                validation_issues=validation_issues,
                error=f"{type(exc).__name__}: {exc}",
            )

    def _build_snapshot(
        self,
        *,
        request: EducationRequest,
        registry: DependencyRegistry,
        subject_plan: SubjectPlan | None,
        journey_id: str | None,
        sessions: tuple[GeneratedSession, ...],
        missions: tuple[GeneratedMission, ...],
    ) -> PlatformSnapshot:
        registered = set(registry.registered_names())
        readiness = {
            wf: OrchestrationPolicy.workflow_ready(wf, registered=registered)
            for wf in sorted(OrchestrationPolicy.known_workflows())
        }
        return PlatformSnapshot(
            platform_version=self.PLATFORM_VERSION,
            learner_id=request.learner_id,
            curriculum_id=request.curriculum_id
            or (subject_plan.curriculum_id if subject_plan else None),
            subject_plan=subject_plan,
            journey_id=journey_id,
            sessions=sessions,
            missions=missions,
            registered_ports=registry.registered_names(),
            missing_ports=registry.missing_names(),
            workflow_readiness=MappingProxyType(readiness),
        )
