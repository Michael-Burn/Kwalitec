"""SQLAlchemy OnboardingSession draft repository (BR-004)."""

from __future__ import annotations

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from application.onboarding.ports import OnboardingRepository
from domain.onboarding.enums import OnboardingStatus
from domain.onboarding.ids import OnboardingId, StudentId
from domain.onboarding.onboarding_session import OnboardingSession
from infrastructure.persistence.dto.onboarding import OnboardingSessionDTO
from infrastructure.persistence.mappers.onboarding_mapper import OnboardingSessionMapper
from infrastructure.persistence.sqlalchemy.models.onboarding_session import (
    OnboardingSessionModel,
)
from infrastructure.persistence.sqlalchemy.repositories.row_codec import (
    dto_from_model,
    model_from_dto,
)
from infrastructure.persistence.user_repository import ConcurrentUpdateError


class SqlAlchemyOnboardingRepository(OnboardingRepository):
    """Persist onboarding draft sessions via SQLAlchemy.

    Remembers ``row_version`` at load time so optimistic locks survive
    SQLAlchemy's weak-referenced identity map.
    """

    def __init__(self, session: Session) -> None:
        self._session = session
        self._row_versions: dict[str, int] = {}

    def get(self, onboarding_id: OnboardingId) -> OnboardingSession | None:
        row = self._session.get(OnboardingSessionModel, str(onboarding_id))
        if row is None:
            return None
        dto = dto_from_model(OnboardingSessionDTO, row)
        self._row_versions[dto.onboarding_id] = int(dto.row_version)
        return OnboardingSessionMapper.to_domain(dto)

    def get_in_progress_for_student(
        self, student_id: StudentId
    ) -> OnboardingSession | None:
        statement = (
            select(OnboardingSessionModel)
            .where(
                OnboardingSessionModel.student_id == str(student_id),
                OnboardingSessionModel.status == OnboardingStatus.IN_PROGRESS.value,
            )
            .order_by(OnboardingSessionModel.updated_at.desc())
        )
        row = self._session.scalars(statement).first()
        if row is None:
            return None
        dto = dto_from_model(OnboardingSessionDTO, row)
        self._row_versions[dto.onboarding_id] = int(dto.row_version)
        return OnboardingSessionMapper.to_domain(dto)

    def save(self, session: OnboardingSession) -> None:
        key = str(session.onboarding_id)
        existing = self._session.get(OnboardingSessionModel, key)
        if existing is None:
            dto = OnboardingSessionMapper.to_persistence(session, row_version=1)
            self._session.add(model_from_dto(OnboardingSessionModel, dto))
            self._row_versions[key] = 1
            return

        expected = self._row_versions.get(key)
        if expected is None:
            expected = int(existing.row_version)
        dto = OnboardingSessionMapper.to_persistence(
            session, row_version=expected + 1
        )
        result = self._session.execute(
            update(OnboardingSessionModel)
            .where(
                OnboardingSessionModel.onboarding_id == key,
                OnboardingSessionModel.row_version == expected,
            )
            .values(
                student_id=dto.student_id,
                status=dto.status,
                current_step=dto.current_step,
                payloads=dto.payloads,
                saved_steps=dto.saved_steps,
                created_at=dto.created_at,
                updated_at=dto.updated_at,
                completed_at=dto.completed_at,
                row_version=dto.row_version,
            )
        )
        if result.rowcount != 1:
            raise ConcurrentUpdateError(
                f"onboarding {session.onboarding_id} was updated concurrently"
            )
        existing.student_id = dto.student_id
        existing.status = dto.status
        existing.current_step = dto.current_step
        existing.payloads = dto.payloads
        existing.saved_steps = dto.saved_steps
        existing.created_at = dto.created_at
        existing.updated_at = dto.updated_at
        existing.completed_at = dto.completed_at
        existing.row_version = dto.row_version
        self._row_versions[key] = dto.row_version
