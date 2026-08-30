"""Read-only Learner Twin query adapter (infrastructure).

Wires DailyLoopTwinPersistence + Study Progress SQL/Runtime C sources to the
application LearnerTwinQueryPort. Lives here so application/student_twin stays
framework-independent (no models / infrastructure imports).
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from datetime import datetime

from app.application.student_twin.canonical_topic_id import CanonicalTopicId
from app.application.student_twin.daily_loop_codec import decode_daily_loop_twin
from app.application.student_twin.query import (
    AlwaysUncoveredStudyProgress,
    LearnerKnowledgeSnapshot,
    StudyProgressPort,
    TopicKnowledgeFact,
)
from app.application.student_twin.twin_engine import StudentTwinEngine
from app.domain.student_twin.digital_twin import DigitalTwin
from app.infrastructure.adapters.student_twin.daily_loop_persistence import (
    DailyLoopTwinPersistence,
)
from app.models.curriculum import Topic
from app.models.topic_progress import TopicProgress

RuntimeCompletedLoader = Callable[[int, str], frozenset[str] | set[str] | Sequence[str]]
OrmTopicsLoader = Callable[[str], Sequence[Topic]]
CurriculumIdentityLoader = Callable[[int, str], str | None]


class CompositeStudyProgressReader:
    """Union of Runtime C completed_topic_ids and TopicProgress.completed.

    Covered if either source says complete. Neither path mints Estimated
    Knowledge.
    """

    def __init__(
        self,
        *,
        canonical: CanonicalTopicId | None = None,
        runtime_completed: RuntimeCompletedLoader | None = None,
        orm_topics_loader: OrmTopicsLoader | None = None,
    ) -> None:
        self._canonical = canonical or CanonicalTopicId()
        self._runtime_completed = runtime_completed
        self._orm_topics_loader = orm_topics_loader

    def topic_covered(
        self, *, user_id: int, subject_code: str, topic_id: str
    ) -> bool:
        tid = (topic_id or "").strip()
        if not tid:
            return False

        if self._runtime_completed is not None:
            completed = self._runtime_completed(user_id, subject_code) or ()
            if tid in completed:
                return True

        if self._topic_progress_completed(
            user_id=user_id, subject_code=subject_code, topic_id=tid
        ):
            return True

        if self._runtime_completed is None:
            completed = _default_runtime_completed(user_id, subject_code)
            if tid in completed:
                return True

        return False

    def _topic_progress_completed(
        self, *, user_id: int, subject_code: str, topic_id: str
    ) -> bool:
        if self._orm_topics_loader is not None:
            topics = self._orm_topics_loader(subject_code)
        else:
            topics = _default_orm_topics_for_subject(subject_code)
        if not topics:
            return False
        orm_id = self._canonical.orm_topic_id_for_published(
            topic_id, subject_code=subject_code, topics=topics
        )
        if orm_id is None:
            return False
        row = TopicProgress.query.filter_by(
            user_id=user_id, topic_id=orm_id
        ).first()
        return bool(row is not None and row.completed)


def _default_runtime_completed(user_id: int, subject_code: str) -> frozenset[str]:
    """Best-effort Runtime C completed_topic_ids; empty on any failure."""
    try:
        from app.application.educational_runtime_engine.service import (
            EducationalRuntimeEngineService,
        )

        svc = EducationalRuntimeEngineService()
        inputs = svc.get_estimated_knowledge_inputs(
            user_id=user_id, subject_code=subject_code
        )
        return frozenset(inputs.completed_topic_ids or ())
    except Exception:
        return frozenset()


def _default_orm_topics_for_subject(subject_code: str) -> list[Topic]:
    """Load ORM topics for title reverse-join; empty when unavailable."""
    code = (subject_code or "").strip().upper()
    if not code:
        return []
    try:
        from app.models.curriculum import Curriculum

        curricula = Curriculum.query.filter(Curriculum.active.is_(True)).all()
        matched: list[Topic] = []
        for curriculum in curricula:
            paper = (getattr(curriculum, "paper", None) or "").strip().upper()
            name = (getattr(curriculum, "name", None) or "").strip().upper()
            if code not in paper and code not in name and paper != code:
                if code not in f"{paper} {name}":
                    continue
            matched.extend(
                Topic.query.filter_by(
                    curriculum_id=curriculum.id, active=True
                ).all()
            )
        return matched
    except Exception:
        return []


class DailyLoopLearnerTwinQueryAdapter:
    """Concrete LearnerTwinQueryPort over Stack B daily-loop Twin documents."""

    def __init__(
        self,
        *,
        persistence: DailyLoopTwinPersistence | None = None,
        engine: StudentTwinEngine | None = None,
        study_progress: StudyProgressPort | None = None,
        curriculum_identity_loader: CurriculumIdentityLoader | None = None,
    ) -> None:
        self._persistence = persistence or DailyLoopTwinPersistence()
        self._engine = engine or StudentTwinEngine()
        self._study_progress: StudyProgressPort = (
            study_progress or CompositeStudyProgressReader()
        )
        self._curriculum_identity_loader = curriculum_identity_loader

    def knowledge_snapshot(
        self, *, user_id: int, subject_code: str
    ) -> LearnerKnowledgeSnapshot:
        twin = self._load_twin(user_id=user_id, subject_code=subject_code)
        identity = self._curriculum_identity(user_id, subject_code, twin)
        if twin is None:
            return LearnerKnowledgeSnapshot(
                user_id=user_id,
                subject_code=subject_code,
                curriculum_identity=identity,
                overall_estimated_knowledge=None,
                topics=(),
            )
        facts = tuple(
            self._fact_from_twin(twin, record.topic_id)
            for record in twin.knowledge.topic_records
        )
        overall: float | None
        if twin.knowledge.topic_records:
            overall = float(twin.knowledge.overall_score)
        else:
            overall = None
        return LearnerKnowledgeSnapshot(
            user_id=user_id,
            subject_code=subject_code,
            curriculum_identity=identity,
            overall_estimated_knowledge=overall,
            topics=facts,
        )

    def topic_knowledge(
        self, *, user_id: int, subject_code: str, topic_id: str
    ) -> TopicKnowledgeFact:
        tid = (topic_id or "").strip()
        twin = self._load_twin(user_id=user_id, subject_code=subject_code)
        if twin is None or not tid:
            return TopicKnowledgeFact(
                topic_id=tid,
                has_estimated_knowledge=False,
                estimated_knowledge=None,
                estimated_mastery=None,
                evidence_count=0,
                last_practised_at=None,
            )
        return self._fact_from_twin(twin, tid)

    def topics_with_estimated_knowledge(
        self, *, user_id: int, subject_code: str
    ) -> tuple[TopicKnowledgeFact, ...]:
        snap = self.knowledge_snapshot(
            user_id=user_id, subject_code=subject_code
        )
        return tuple(f for f in snap.topics if f.has_estimated_knowledge)

    def topic_covered(
        self, *, user_id: int, subject_code: str, topic_id: str
    ) -> bool:
        return self._study_progress.topic_covered(
            user_id=user_id,
            subject_code=subject_code,
            topic_id=topic_id,
        )

    def _load_twin(
        self, *, user_id: int, subject_code: str
    ) -> DigitalTwin | None:
        learner_id = str(user_id)
        document = self._persistence.load_twin(
            learner_id=learner_id, subject_code=subject_code
        )
        decoded = decode_daily_loop_twin(document, engine=self._engine)
        if decoded is None:
            return None
        twin, _status = decoded
        return twin

    def _fact_from_twin(self, twin: DigitalTwin, topic_id: str) -> TopicKnowledgeFact:
        tid = (topic_id or "").strip()
        events = twin.history.events_for_topic(tid)
        knowledge = twin.knowledge.record_for(tid)
        mastery = twin.mastery.record_for(tid)
        has_ek = knowledge is not None or len(events) > 0
        last_at: datetime | None = None
        if events:
            last_at = max(event.occurred_at for event in events)
        return TopicKnowledgeFact(
            topic_id=tid,
            has_estimated_knowledge=has_ek,
            estimated_knowledge=(
                float(knowledge.knowledge_score) if knowledge is not None else None
            ),
            estimated_mastery=(
                float(mastery.mastery_score) if mastery is not None else None
            ),
            evidence_count=len(events),
            last_practised_at=last_at,
        )

    def _curriculum_identity(
        self,
        user_id: int,
        subject_code: str,
        twin: DigitalTwin | None,
    ) -> str | None:
        if self._curriculum_identity_loader is not None:
            return self._curriculum_identity_loader(user_id, subject_code)
        return None


# Re-export pure stubs for adapter consumers that imported the old module path.
__all__ = [
    "AlwaysUncoveredStudyProgress",
    "CompositeStudyProgressReader",
    "DailyLoopLearnerTwinQueryAdapter",
]
