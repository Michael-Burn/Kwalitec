"""Student Baseline application service — draft autosave, resume, reset.

Never deletes study history. Supersede-only on restart / Founder reset.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.application.student_baseline.declarations import (
    BaselineDeclarations,
    BaselineSubjectScope,
)
from app.application.student_baseline.enums import (
    BaselineStatus,
    ConfidenceBand,
    ExamHistory,
    LearningObjective,
    PositionMode,
    PreviousExperience,
)
from app.extensions import db
from app.models.student_baseline import StudentBaseline


@dataclass(frozen=True)
class BaselineResumeView:
    """Read model for returning students — no re-ask."""

    baseline_id: int
    subject_key: str
    experience: str | None
    position_mode: str | None
    curriculum_topic_code: str | None
    study_phase: str | None
    learning_objective: str | None
    confidence: str | None
    exam_history: str | None
    completed_at: datetime | None
    twin_snapshot_id: str | None
    study_plan_id: int | None
    enrolment_id: str | None


class StudentBaselineService:
    """CRUD / lifecycle for StudentBaseline rows."""

    @staticmethod
    def subject_key(category_code: str, subject_code: str) -> str:
        return f"{(category_code or '').strip()}:{(subject_code or '').strip()}"

    @classmethod
    def get_complete(
        cls, user_id: int, subject_key: str
    ) -> StudentBaseline | None:
        return (
            StudentBaseline.query.filter_by(
                user_id=user_id,
                subject_key=subject_key,
                status=BaselineStatus.COMPLETE.value,
            )
            .order_by(StudentBaseline.id.desc())
            .first()
        )

    @classmethod
    def get_draft(
        cls, user_id: int, subject_key: str
    ) -> StudentBaseline | None:
        return (
            StudentBaseline.query.filter_by(
                user_id=user_id,
                subject_key=subject_key,
                status=BaselineStatus.DRAFT.value,
            )
            .order_by(StudentBaseline.id.desc())
            .first()
        )

    @classmethod
    def get_by_id(
        cls, baseline_id: int, *, user_id: int | None = None
    ) -> StudentBaseline | None:
        row = db.session.get(StudentBaseline, baseline_id)
        if row is None:
            return None
        if user_id is not None and row.user_id != user_id:
            return None
        return row

    @classmethod
    def ensure_draft(
        cls, user_id: int, scope: BaselineSubjectScope
    ) -> StudentBaseline:
        """Return existing draft or create a new one for the subject."""
        key = scope.subject_key or cls.subject_key(
            scope.category_code, scope.subject_code
        )
        existing = cls.get_draft(user_id, key)
        if existing is not None:
            existing.curriculum_version = (
                scope.curriculum_version or existing.curriculum_version
            )
            existing.updated_at = datetime.utcnow()
            db.session.commit()
            return existing

        row = StudentBaseline(
            user_id=user_id,
            subject_key=key,
            category_code=scope.category_code,
            subject_code=scope.subject_code,
            curriculum_version=scope.curriculum_version,
            status=BaselineStatus.DRAFT.value,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.session.add(row)
        db.session.commit()
        return row

    @classmethod
    def save_answer(
        cls,
        baseline_id: int,
        user_id: int,
        *,
        experience: str | None = None,
        position_mode: str | None = None,
        curriculum_topic_code: str | None = None,
        exam_history: str | None = None,
        highest_mark: str | None = None,
        learning_objective: str | None = None,
        confidence: str | None = None,
        clear_topic: bool = False,
    ) -> StudentBaseline:
        """Autosave one or more draft fields after a step POST."""
        row = cls.get_by_id(baseline_id, user_id=user_id)
        if row is None or row.status != BaselineStatus.DRAFT.value:
            raise ValueError("Baseline draft not found")

        if experience is not None:
            row.experience = PreviousExperience(experience).value
        if position_mode is not None:
            row.position_mode = PositionMode(position_mode).value
            if position_mode == PositionMode.START_BEGINNING.value:
                row.curriculum_topic_code = None
        if clear_topic:
            row.curriculum_topic_code = None
        if curriculum_topic_code is not None:
            row.curriculum_topic_code = curriculum_topic_code.strip() or None
        if exam_history is not None:
            row.exam_history = ExamHistory(exam_history).value
        if highest_mark is not None:
            cleaned = highest_mark.strip()
            row.highest_mark = cleaned or None
        if learning_objective is not None:
            row.learning_objective = LearningObjective(learning_objective).value
            if learning_objective == LearningObjective.RESTART.value:
                row.position_mode = PositionMode.START_BEGINNING.value
                row.curriculum_topic_code = None
        if confidence is not None:
            row.confidence = ConfidenceBand(confidence).value

        row.updated_at = datetime.utcnow()
        db.session.commit()
        return row

    @classmethod
    def declarations_from_row(
        cls, row: StudentBaseline
    ) -> BaselineDeclarations | None:
        """Build closed declarations when all required draft fields exist."""
        try:
            if not all(
                [
                    row.experience,
                    row.position_mode,
                    row.exam_history,
                    row.learning_objective,
                    row.confidence,
                ]
            ):
                return None
            decls = BaselineDeclarations(
                experience=PreviousExperience(row.experience),
                position_mode=PositionMode(row.position_mode),
                exam_history=ExamHistory(row.exam_history),
                learning_objective=LearningObjective(row.learning_objective),
                confidence=ConfidenceBand(row.confidence),
                curriculum_topic_code=row.curriculum_topic_code,
                highest_mark=row.highest_mark,
            )
        except (TypeError, ValueError):
            return None
        if not decls.is_complete():
            return None
        return decls

    @classmethod
    def mark_complete(
        cls,
        row: StudentBaseline,
        *,
        twin_snapshot_id: str | None,
        study_plan_id: int | None = None,
        enrolment_id: str | None = None,
        runtime_authority: str | None = None,
    ) -> StudentBaseline:
        """Mark draft complete and supersede any prior complete for scope."""
        prior = cls.get_complete(row.user_id, row.subject_key)
        if prior is not None and prior.id != row.id:
            prior.status = BaselineStatus.SUPERSEDED.value
            prior.updated_at = datetime.utcnow()
            row.supersedes_baseline_id = prior.id

        row.status = BaselineStatus.COMPLETE.value
        row.completed_at = datetime.utcnow()
        row.updated_at = datetime.utcnow()
        row.twin_snapshot_id = twin_snapshot_id
        if study_plan_id is not None:
            row.study_plan_id = study_plan_id
        if enrolment_id is not None:
            row.enrolment_id = enrolment_id
        if runtime_authority is not None:
            row.runtime_authority = runtime_authority
        db.session.commit()
        return row

    @classmethod
    def resume_view(cls, row: StudentBaseline) -> BaselineResumeView:
        from app.application.student_baseline.mapper import experience_to_position

        phase = None
        if row.experience:
            try:
                phase = experience_to_position(PreviousExperience(row.experience))
            except ValueError:
                phase = row.experience
        return BaselineResumeView(
            baseline_id=row.id,
            subject_key=row.subject_key,
            experience=row.experience,
            position_mode=row.position_mode,
            curriculum_topic_code=row.curriculum_topic_code,
            study_phase=phase,
            learning_objective=row.learning_objective,
            confidence=row.confidence,
            exam_history=row.exam_history,
            completed_at=row.completed_at,
            twin_snapshot_id=row.twin_snapshot_id,
            study_plan_id=row.study_plan_id,
            enrolment_id=row.enrolment_id,
        )

    @classmethod
    def restart_for_student(
        cls, user_id: int, subject_key: str
    ) -> StudentBaseline:
        """Student voluntary restart — supersede complete; new draft. History intact."""
        complete = cls.get_complete(user_id, subject_key)
        if complete is None:
            raise ValueError("No complete baseline to restart")
        complete.status = BaselineStatus.SUPERSEDED.value
        complete.updated_at = datetime.utcnow()
        draft = StudentBaseline(
            user_id=user_id,
            subject_key=complete.subject_key,
            category_code=complete.category_code,
            subject_code=complete.subject_code,
            curriculum_version=complete.curriculum_version,
            status=BaselineStatus.DRAFT.value,
            supersedes_baseline_id=complete.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.session.add(draft)
        db.session.commit()
        return draft

    @classmethod
    def founder_reset(cls, user_id: int, subject_key: str) -> StudentBaseline | None:
        """Founder reset — supersede complete baseline; never delete history."""
        complete = cls.get_complete(user_id, subject_key)
        if complete is None:
            return None
        complete.status = BaselineStatus.SUPERSEDED.value
        complete.updated_at = datetime.utcnow()
        # Leave twin snapshots and study artefacts untouched.
        db.session.commit()
        return complete

    @classmethod
    def list_for_user(cls, user_id: int) -> list[StudentBaseline]:
        return (
            StudentBaseline.query.filter_by(user_id=user_id)
            .order_by(StudentBaseline.id.desc())
            .all()
        )

    @classmethod
    def inspect(cls, baseline_id: int) -> BaselineResumeView | None:
        row = cls.get_by_id(baseline_id)
        if row is None:
            return None
        return cls.resume_view(row)
