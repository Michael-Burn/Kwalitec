"""StudentInitializationService — birth Twin + seed evidence + first pipeline.

Converts ``CompletedOnboarding`` into a persistent Educational Digital Twin,
seeds the observational evidence catalogue, and executes the Educational
Pipeline for the student's first result.

Forbidden outside the Educational Pipeline: recommendations / missions.
Forbidden entirely: Flask, presentation, HTML, AI.
"""

from __future__ import annotations

from application.errors import ConflictError
from application.events.twin import DigitalTwinUpdatedApplicationEvent
from application.onboarding.results import (
    CompletedOnboarding,
    StudentTwinInitializationRequest,
)
from application.pipeline.pipeline_request import PipelineRequest
from application.ports.event_publisher import ApplicationEventPublisher
from application.ports.unit_of_work import UnitOfWork
from application.student_initialization.availability_mapper import (
    build_availability,
)
from application.student_initialization.errors import (
    OnboardingValidationError,
)
from application.student_initialization.evidence_seeder import (
    EvidenceCatalogueSeeder,
    evidence_id_for_onboarding,
)
from application.student_initialization.ports import (
    Clock,
    EducationalPipelinePort,
    PipelineSessionContextFactory,
    TwinIdGenerator,
)
from application.student_initialization.results import (
    InitialEvidence,
    InitializationResult,
)
from application.student_initialization.session_context_factory import (
    FirstRunSessionContextFactory,
)
from application.student_initialization.twin_builder import build_student_twin
from domain.education.digital_twin import EducationalDigitalTwin
from domain.education.evidence import EvidenceRecord
from domain.education.foundation.enums import EvidenceType
from domain.education.foundation.errors import EducationalDomainError
from domain.education.foundation.ids import EvidenceId


class EducationalPipelineAdapter(EducationalPipelinePort):
    """Adapt a composition-rooted pipeline to the initialization outbound port.

    The concrete ``EducationalPipeline`` must be constructed in a composition
    root and injected — this adapter never constructs wired services.
    """

    def __init__(self, pipeline: EducationalPipelinePort) -> None:
        self._pipeline = pipeline

    def run(self, request: PipelineRequest):
        return self._pipeline.run(request)


class DeterministicTwinIdGenerator(TwinIdGenerator):
    """Stable twin ids keyed by onboarding identity (idempotent births)."""

    def next_identity(self, *, onboarding_id: str, student_id: str) -> str:
        cleaned = (onboarding_id or "").strip()
        if not cleaned:
            raise OnboardingValidationError("onboarding_id is required")
        _ = student_id  # retained for explicit coupling to the learner
        return f"twin-onboarding-{cleaned}"


class StudentInitializationService:
    """Orchestrate Twin birth, evidence seeding, and first pipeline execution.

    Input: ``CompletedOnboarding``.
    Output: ``InitializationResult`` (StudentTwin, InitialEvidence, PipelineResult).

    Transactional via ``UnitOfWork``. Idempotent on ``onboarding_id``.
    """

    def __init__(
        self,
        *,
        uow: UnitOfWork,
        events: ApplicationEventPublisher,
        clock: Clock,
        pipeline: EducationalPipelinePort,
        twin_ids: TwinIdGenerator | None = None,
        session_context_factory: PipelineSessionContextFactory | None = None,
    ) -> None:
        self._uow = uow
        self._events = events
        self._clock = clock
        self._pipeline = pipeline
        self._twin_ids = twin_ids or DeterministicTwinIdGenerator()
        self._session_context_factory = (
            session_context_factory or FirstRunSessionContextFactory()
        )

    def initialize(self, completed: CompletedOnboarding) -> InitializationResult:
        """Validate onboarding, persist Twin + evidence, run Educational Pipeline.

        Args:
            completed: Sealed onboarding outcome with Twin initialization cargo.

        Returns:
            ``InitializationResult`` with twin, seeded evidence, and pipeline
            artefacts.

        Raises:
            OnboardingValidationError: When onboarding cargo is invalid.
            ConflictError: When an existing twin conflicts with this onboarding.
            StudentInitializationError: When coordination fails.
        """
        declarations = self._validate_completed(completed)
        evidence_id = EvidenceId(evidence_id_for_onboarding(declarations.onboarding_id))
        twin_id_value = self._twin_ids.next_identity(
            onboarding_id=declarations.onboarding_id,
            student_id=declarations.student_id,
        )

        with self._uow:
            existing_evidence = self._uow.evidence.get(evidence_id)
            existing_twin = self._uow.digital_twins.get_by_student(
                declarations.student_id
            )

            if existing_evidence is not None:
                result = self._replay_existing(
                    declarations=declarations,
                    twin_id_value=twin_id_value,
                    existing_twin=existing_twin,
                    existing_evidence=existing_evidence,
                )
                self._uow.commit()
                return result

            if existing_twin is not None:
                raise ConflictError(
                    "EducationalDigitalTwin already exists for student "
                    f"{declarations.student_id} without matching onboarding evidence"
                )

            twin = build_student_twin(
                twin_id=twin_id_value,
                declarations=declarations,
            )
            twin.pull_events()

            initial_evidence = EvidenceCatalogueSeeder.seed(
                declarations,
                occurred_at=completed.completed_at,
            )
            availability = build_availability(declarations)

            for record in initial_evidence.records:
                try:
                    twin.record_evidence(
                        record.evidence_id,
                        EvidenceType.SELF_REPORT,
                        note="onboarding_declaration",
                    )
                except EducationalDomainError as exc:
                    raise ConflictError(str(exc)) from exc

            twin.pull_events()
            self._uow.digital_twins.save(twin)
            for record in initial_evidence.records:
                self._uow.evidence.save(record)

            session_context = self._session_context_factory.build(
                twin=twin,
                declarations=declarations,
                evidence=initial_evidence.records,
                availability=availability,
            )
            pipeline_result = self._pipeline.run(
                PipelineRequest(
                    student_id=declarations.student_id,
                    educational_evidence=initial_evidence.records,
                    session_context=session_context,
                )
            )
            self._uow.commit()

        self._events.publish(
            DigitalTwinUpdatedApplicationEvent.create(
                twin_id=twin.twin_id.value,
                student_id=twin.student_id,
                update_kind="initialized",
                occurred_at=self._clock.now(),
            )
        )
        return InitializationResult(
            student_twin=twin,
            initial_evidence=initial_evidence,
            pipeline_result=pipeline_result,
            idempotent_replay=False,
        )

    def _replay_existing(
        self,
        *,
        declarations: StudentTwinInitializationRequest,
        twin_id_value: str,
        existing_twin: EducationalDigitalTwin | None,
        existing_evidence: EvidenceRecord,
    ) -> InitializationResult:
        if existing_twin is None:
            raise ConflictError(
                "onboarding evidence exists without an EducationalDigitalTwin"
            )
        if existing_twin.twin_id.value != twin_id_value:
            raise ConflictError(
                "existing twin identity does not match onboarding twin id"
            )
        if existing_evidence.student_id != declarations.student_id:
            raise ConflictError(
                "existing onboarding evidence belongs to a different student"
            )

        records = (existing_evidence,)
        # Prefer catalogue completeness: include any other onboarding-seeded rows.
        for record in self._uow.evidence.list_by_student(declarations.student_id):
            if (
                record.evidence_id != existing_evidence.evidence_id
                and record.evidence_id.value.startswith("evidence-onboarding-")
            ):
                records = (*records, record)

        initial_evidence = InitialEvidence(
            onboarding_id=declarations.onboarding_id,
            student_id=declarations.student_id,
            records=records,
        )
        availability = build_availability(declarations)
        session_context = self._session_context_factory.build(
            twin=existing_twin,
            declarations=declarations,
            evidence=initial_evidence.records,
            availability=availability,
        )
        pipeline_result = self._pipeline.run(
            PipelineRequest(
                student_id=declarations.student_id,
                educational_evidence=initial_evidence.records,
                session_context=session_context,
            )
        )
        return InitializationResult(
            student_twin=existing_twin,
            initial_evidence=initial_evidence,
            pipeline_result=pipeline_result,
            idempotent_replay=True,
        )

    def _validate_completed(
        self, completed: CompletedOnboarding
    ) -> StudentTwinInitializationRequest:
        if completed is None or not isinstance(completed, CompletedOnboarding):
            raise OnboardingValidationError(
                "completed must be a CompletedOnboarding"
            )
        if not (completed.student_id or "").strip():
            raise OnboardingValidationError("student_id is required")
        if not (completed.onboarding_id or "").strip():
            raise OnboardingValidationError("onboarding_id is required")
        if completed.completed_at is None:
            raise OnboardingValidationError("completed_at is required")
        if completed.completed_at.tzinfo is None:
            raise OnboardingValidationError(
                "completed_at must be timezone-aware"
            )
        declarations = completed.twin_initialization
        if declarations is None or not isinstance(
            declarations, StudentTwinInitializationRequest
        ):
            raise OnboardingValidationError(
                "twin_initialization is required on CompletedOnboarding"
            )
        if declarations.student_id.strip() != completed.student_id.strip():
            raise OnboardingValidationError(
                "twin_initialization.student_id must match completed.student_id"
            )
        if declarations.onboarding_id.strip() != completed.onboarding_id.strip():
            raise OnboardingValidationError(
                "twin_initialization.onboarding_id must match "
                "completed.onboarding_id"
            )
        if not declarations.declaration_confirmation:
            raise OnboardingValidationError(
                "declaration_confirmation must be true"
            )
        return declarations
