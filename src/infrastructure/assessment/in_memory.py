"""In-memory assessment persistence adapters (AP-002B delivery only).

No Alembic / SQLAlchemy tables — Alembic head remains unchanged.
"""

from __future__ import annotations

from application.assessment.delivery.question_content import QuestionContent
from application.assessment.delivery.sequencing import SessionDeliveryState
from application.assessment.ports.repositories import (
    AssessmentInstrumentBuilder,
    AssessmentInstrumentRepository,
    AssessmentObservationRepository,
    AssessmentResultRepository,
    AssessmentSessionBuilder,
    AssessmentSessionRepository,
    EvidenceBundleRepository,
    QuestionContentRepository,
    SessionDeliveryStateRepository,
)
from domain.assessment.entities.assessment_instrument import AssessmentInstrument
from domain.assessment.entities.assessment_observation import AssessmentObservation
from domain.assessment.entities.assessment_result import AssessmentResult
from domain.assessment.entities.assessment_session import AssessmentSession
from domain.assessment.enums import AssessmentPurpose, AssessmentType
from domain.assessment.evidence.ids import EvidenceBundleId
from domain.assessment.evidence.models import EvidenceBundle
from domain.assessment.factories import (
    AssessmentInstrumentFactory,
    AssessmentSessionFactory,
)
from domain.assessment.value_objects.configuration import (
    AssessmentConfiguration,
    AssessmentMetadata,
)
from domain.assessment.value_objects.ids import (
    InstrumentId,
    ObservationId,
    ResultId,
    SessionId,
)
from domain.assessment.value_objects.references import (
    LearningObjectiveReference,
    QuestionReference,
)


class InMemoryAssessmentSessionRepository(AssessmentSessionRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, AssessmentSession] = {}

    def get(self, session_id: SessionId) -> AssessmentSession | None:
        return self._by_id.get(session_id.value)

    def list_by_student(self, student_id: str) -> list[AssessmentSession]:
        return [
            session
            for session in self._by_id.values()
            if session.student_id == student_id
        ]

    def save(self, session: AssessmentSession) -> None:
        self._by_id[session.session_id.value] = session


class InMemoryAssessmentInstrumentRepository(AssessmentInstrumentRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, AssessmentInstrument] = {}

    def get(self, instrument_id: InstrumentId) -> AssessmentInstrument | None:
        return self._by_id.get(instrument_id.value)

    def list_by_purpose(
        self, purpose: AssessmentPurpose
    ) -> list[AssessmentInstrument]:
        return [
            instrument
            for instrument in self._by_id.values()
            if instrument.purpose is purpose
        ]

    def save(self, instrument: AssessmentInstrument) -> None:
        self._by_id[instrument.instrument_id.value] = instrument


class InMemoryAssessmentObservationRepository(AssessmentObservationRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, AssessmentObservation] = {}

    def get(self, observation_id: ObservationId) -> AssessmentObservation | None:
        return self._by_id.get(observation_id.value)

    def list_by_session(self, session_id: SessionId) -> list[AssessmentObservation]:
        return [
            observation
            for observation in self._by_id.values()
            if observation.session_id == session_id
        ]

    def save(self, observation: AssessmentObservation) -> None:
        self._by_id[observation.observation_id.value] = observation


class InMemoryAssessmentResultRepository(AssessmentResultRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, AssessmentResult] = {}
        self._by_session: dict[str, str] = {}

    def get(self, result_id: ResultId) -> AssessmentResult | None:
        return self._by_id.get(result_id.value)

    def get_by_session(self, session_id: SessionId) -> AssessmentResult | None:
        result_id = self._by_session.get(session_id.value)
        if result_id is None:
            return None
        return self._by_id.get(result_id)

    def save(self, result: AssessmentResult) -> None:
        self._by_id[result.result_id.value] = result
        self._by_session[result.session_id.value] = result.result_id.value


class InMemoryEvidenceBundleRepository(EvidenceBundleRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, EvidenceBundle] = {}
        self._by_session: dict[str, str] = {}

    def get(self, bundle_id: EvidenceBundleId) -> EvidenceBundle | None:  # type: ignore[override]
        if isinstance(bundle_id, EvidenceBundleId):
            key = bundle_id.value
        else:
            key = str(bundle_id)
        return self._by_id.get(key)

    def get_by_session(self, session_id: SessionId) -> EvidenceBundle | None:
        bundle_id = self._by_session.get(session_id.value)
        if bundle_id is None:
            return None
        return self._by_id.get(bundle_id)

    def save(self, bundle: EvidenceBundle) -> None:  # type: ignore[override]
        self._by_id[bundle.bundle_id.value] = bundle
        self._by_session[bundle.context.session_id.value] = bundle.bundle_id.value


class InMemoryQuestionContentRepository(QuestionContentRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, QuestionContent] = {}

    def get(self, question_id: str) -> QuestionContent | None:
        return self._by_id.get(question_id)

    def save(self, content: QuestionContent) -> None:  # type: ignore[override]
        self._by_id[content.question_id] = content


class InMemorySessionDeliveryStateRepository(SessionDeliveryStateRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, SessionDeliveryState] = {}

    def get(self, session_id: str) -> SessionDeliveryState | None:
        return self._by_id.get(session_id)

    def save(self, state: SessionDeliveryState) -> None:  # type: ignore[override]
        self._by_id[state.session_id] = state


class DomainAssessmentInstrumentBuilder(AssessmentInstrumentBuilder):
    def build(
        self,
        instrument_id: InstrumentId,
        assessment_type: AssessmentType,
        purpose: AssessmentPurpose,
        questions: list[QuestionReference] | tuple[QuestionReference, ...],
        learning_objectives: list[LearningObjectiveReference]
        | tuple[LearningObjectiveReference, ...],
        metadata: AssessmentMetadata,
        *,
        configuration: AssessmentConfiguration | None = None,
    ) -> AssessmentInstrument:
        return AssessmentInstrumentFactory.create(
            instrument_id=instrument_id,
            assessment_type=assessment_type,
            purpose=purpose,
            questions=questions,
            learning_objectives=learning_objectives,
            metadata=metadata,
            configuration=configuration,
        )


class DomainAssessmentSessionBuilder(AssessmentSessionBuilder):
    def build_from_instrument(
        self,
        session_id: SessionId,
        student_id: str,
        instrument: AssessmentInstrument,
        *,
        twin_id: str | None = None,
        mission_id: str | None = None,
    ) -> AssessmentSession:
        return AssessmentSessionFactory.create_from_instrument(
            session_id=session_id,
            student_id=student_id,
            instrument=instrument,
            twin_id=twin_id,
            mission_id=mission_id,
        )
