"""Enrolment bridge between study-plan wizard and runtimes (PI-002A)."""

from __future__ import annotations

from datetime import date
from typing import Any

from app.application.educational_runtime_engine.coexistence import (
    RuntimeAuthority,
)
from app.application.educational_runtime_engine.exceptions import (
    EnrolmentAlreadyExists,
    PublishedCurriculumUnavailable,
)
from app.application.educational_runtime_engine.service import (
    EducationalRuntimeEngineService,
)
from app.application.platform_integration.discovery import (
    PUBLISHED_CATEGORY_CODE,
    PublishedSubjectDiscoveryService,
)
from app.application.platform_integration.dto import EnrolmentBridgeResult
from app.application.platform_integration.exceptions import (
    BridgeEnrolmentBlocked,
    PublishedSubjectNotDiscoverable,
)
from app.application.platform_integration.flags import (
    FounderStudentBridgeFlags,
    resolve_founder_student_bridge_flags,
)
from app.application.platform_integration.routing import RuntimeRoutingService
from app.services.study_plan_service import StudyPlanService


class FounderStudentEnrolmentBridge:
    """Orchestrate enrolment with audited runtime selection.

    Runtime A path delegates to ``StudyPlanService`` unchanged.
    Runtime C path enrols via ``EducationalRuntimeEngineService``.
    """

    def __init__(
        self,
        *,
        routing: RuntimeRoutingService | None = None,
        discovery: PublishedSubjectDiscoveryService | None = None,
        runtime_c: EducationalRuntimeEngineService | None = None,
        flags: FounderStudentBridgeFlags | None = None,
    ) -> None:
        self._flags = flags
        self._discovery = discovery or PublishedSubjectDiscoveryService(
            flags=flags
        )
        self._routing = routing or RuntimeRoutingService(flags=flags)
        self._runtime_c = runtime_c or EducationalRuntimeEngineService()

    def _resolve_flags(self) -> FounderStudentBridgeFlags:
        return self._flags or resolve_founder_student_bridge_flags()

    def should_use_bridge(
        self, *, category_code: str, subject_code: str
    ) -> bool:
        """True when the selection may need Runtime C routing evaluation."""
        flags = self._resolve_flags()
        if not flags.ENABLE_RUNTIME_C_ENROLMENT:
            return False
        if (category_code or "").strip() == PUBLISHED_CATEGORY_CODE:
            return True
        code = (subject_code or "").strip().upper()
        return code in flags.RUNTIME_C_SUBJECT_ALLOWLIST

    def enrol(
        self,
        *,
        user_id: int,
        category_code: str,
        subject_code: str,
        exam_date: date | None = None,
        # Runtime A study-plan kwargs (ignored for Runtime C)
        runtime_a_kwargs: dict[str, Any] | None = None,
    ) -> EnrolmentBridgeResult:
        """Enrol the student using the resolved runtime.

        Raises:
            PublishedSubjectNotDiscoverable: Published category selected but
                discovery is off or no active package.
            BridgeEnrolmentBlocked: Runtime C selected but enrolment flag off
                or package unavailable.
            EnrolmentAlreadyExists: Runtime C duplicate enrolment.
        """
        code = (subject_code or "").strip().upper()
        category = (category_code or "").strip()
        flags = self._resolve_flags()

        if category == PUBLISHED_CATEGORY_CODE:
            if not flags.ENABLE_PUBLISHED_SUBJECT_DISCOVERY:
                raise PublishedSubjectNotDiscoverable(
                    "Published curriculum discovery is disabled"
                )
            offer = self._discovery.get_offer(code)
            if offer is None:
                # Discovery may be on with no matching active package.
                raise PublishedSubjectNotDiscoverable(
                    f"no discoverable published subject {code}"
                )
            if not flags.ENABLE_RUNTIME_C_ENROLMENT:
                raise BridgeEnrolmentBlocked(
                    "Runtime C enrolment is disabled; "
                    "published subjects cannot enrol until the flag is enabled"
                )

        decision = self._routing.resolve(
            subject_code=code, category_code=category
        )

        if decision.runtime_authority == RuntimeAuthority.PUBLISHED_CURRICULUM:
            return self._enrol_runtime_c(
                user_id=user_id,
                decision=decision,
                exam_date=exam_date,
            )

        return self._enrol_runtime_a(
            user_id=user_id,
            decision=decision,
            runtime_a_kwargs=runtime_a_kwargs or {},
        )

    def _enrol_runtime_c(
        self,
        *,
        user_id: int,
        decision,
        exam_date: date | None,
    ) -> EnrolmentBridgeResult:
        try:
            journey = self._runtime_c.enrol_student(
                user_id=user_id,
                subject_code=decision.subject_code,
                exam_date=exam_date,
                auto_instantiate_plan=True,
            )
        except PublishedCurriculumUnavailable as exc:
            raise BridgeEnrolmentBlocked(str(exc)) from exc
        except EnrolmentAlreadyExists:
            raise

        audit = self._routing.record_decision(
            user_id=user_id,
            decision=decision,
            enrolment_id=journey.enrolment.enrolment_id,
            study_plan_id=None,
            commit=True,
        )
        return EnrolmentBridgeResult(
            runtime_authority=RuntimeAuthority.PUBLISHED_CURRICULUM,
            routing=decision,
            audit_id=audit.audit_id,
            enrolment_id=journey.enrolment.enrolment_id,
            curriculum_identity=journey.enrolment.curriculum_identity,
            study_plan_id=None,
            redirect_target="student_home",
            message=(
                f"Enrolled in published curriculum "
                f"{journey.enrolment.curriculum_identity} (Runtime C)."
            ),
        )

    def _enrol_runtime_a(
        self,
        *,
        user_id: int,
        decision,
        runtime_a_kwargs: dict[str, Any],
    ) -> EnrolmentBridgeResult:
        if not runtime_a_kwargs:
            raise BridgeEnrolmentBlocked(
                "Runtime A enrolment requires study plan parameters"
            )
        study_plan = StudyPlanService.create_study_plan(
            user_id=user_id,
            **runtime_a_kwargs,
        )
        audit = self._routing.record_decision(
            user_id=user_id,
            decision=decision,
            enrolment_id=None,
            study_plan_id=study_plan.id,
            commit=True,
        )
        return EnrolmentBridgeResult(
            runtime_authority=RuntimeAuthority.JSON_BUNDLED,
            routing=decision,
            audit_id=audit.audit_id,
            enrolment_id=None,
            curriculum_identity=None,
            study_plan_id=study_plan.id,
            redirect_target="calibration",
            message=f"Study plan {study_plan.id} created (Runtime A).",
        )
