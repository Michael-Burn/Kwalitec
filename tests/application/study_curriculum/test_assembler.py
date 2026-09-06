"""Study Curriculum assembler tests.

Covers the four-state join, the Study-Progress-complete + zero-Twin-evidence
edge case, bulk call-count discipline, and threshold identity with existing
project constants.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.adaptive_decision.types import POLICY_V1_MIN_EVIDENCE
from app.application.educational_engine_foundation.dto import (
    EducationalArtefactSnapshot,
    JourneySnapshot,
)
from app.application.learner_progress.milestones import (
    EK_MASTERED_THRESHOLD,
    is_ek_mastered,
)
from app.application.progress_engine.dto import (
    CurriculumPosition,
    ProgressProjection,
    StudyProgress,
)
from app.application.student_twin.query import (
    LearnerKnowledgeSnapshot,
    TopicKnowledgeFact,
)
from app.application.study_curriculum import (
    EVIDENCE_RELIABILITY_FLOOR,
    MASTERY_THRESHOLD,
    CurriculumLearningStateAssembler,
    TopicLearningState,
)
from app.application.study_curriculum.assembler import resolve_topic_learning_state
from app.application.study_curriculum.states import TopicLearningState as StateEnum

FIXED = datetime(2026, 9, 6, 8, 0, tzinfo=UTC)

TOPIC_NOT_STARTED = "CS1-A-T04"
TOPIC_NOT_YET_ASSESSED = "CS1-A-T03"
TOPIC_DEVELOPING = "CS1-A-T02"
TOPIC_MASTERED = "CS1-A-T01"
TOPIC_COMPLETE_NO_EK = "CS1-A-T10"


def _position(
    *,
    topic_ids: tuple[str, ...],
    completed: tuple[str, ...],
    current_topic_id: str | None,
    curriculum_identity: str = "CS1:test",
) -> CurriculumPosition:
    remaining = tuple(tid for tid in topic_ids if tid not in completed)
    return CurriculumPosition(
        curriculum_identity=curriculum_identity,
        current_topic_id=current_topic_id,
        current_topic_index=(
            topic_ids.index(current_topic_id)
            if current_topic_id in topic_ids
            else None
        ),
        topic_count=len(topic_ids),
        completed_count=len(completed),
        remaining_count=len(remaining),
        coverage_ratio=(len(completed) / len(topic_ids)) if topic_ids else 0.0,
        journey_stage="in_progress",
        syllabus_complete=not remaining,
    )


def _progress(
    *,
    topic_ids: tuple[str, ...],
    completed: tuple[str, ...] = (),
    current_topic_id: str | None = None,
    curriculum_identity: str = "CS1:test",
) -> StudyProgress:
    completed_set = frozenset(completed)
    incomplete = tuple(tid for tid in topic_ids if tid not in completed_set)
    position = _position(
        topic_ids=topic_ids,
        completed=completed,
        current_topic_id=current_topic_id,
        curriculum_identity=curriculum_identity,
    )
    return StudyProgress(
        curriculum_identity=curriculum_identity,
        topic_ids=topic_ids,
        completed_topic_ids=completed,
        incomplete_topic_ids=incomplete,
        current_topic_id=current_topic_id,
        coverage_ratio=position.coverage_ratio,
        journey_stage=position.journey_stage,
        syllabus_complete=position.syllabus_complete,
        completed_objective_ids=(),
        remaining_objective_ids=(),
        position=position,
        projection=ProgressProjection(
            remaining_topic_ids=incomplete,
            next_topic_id=current_topic_id,
            estimated_topics_remaining=len(incomplete),
            twin_present=False,
        ),
    )


def _fact(
    topic_id: str,
    *,
    estimated_knowledge: float | None = None,
    evidence_count: int = 0,
    has_estimated_knowledge: bool | None = None,
    last_practised_at: datetime | None = None,
) -> TopicKnowledgeFact:
    has_ek = (
        has_estimated_knowledge
        if has_estimated_knowledge is not None
        else estimated_knowledge is not None
    )
    return TopicKnowledgeFact(
        topic_id=topic_id,
        has_estimated_knowledge=has_ek,
        estimated_knowledge=estimated_knowledge,
        estimated_mastery=estimated_knowledge,
        evidence_count=evidence_count,
        last_practised_at=last_practised_at,
    )


def _artefacts(
    *,
    topic_ids: tuple[str, ...],
    subject_code: str = "CS1",
    curriculum_identity: str = "CS1:test",
) -> EducationalArtefactSnapshot:
    sections: list[dict] = []
    for index, topic_id in enumerate(topic_ids):
        section_id = f"S{(index // 10) + 1}"
        if not sections or sections[-1]["section_id"] != section_id:
            sections.append(
                {
                    "section_id": section_id,
                    "code": section_id,
                    "title": f"Section {section_id}",
                    "topics": [],
                }
            )
        sections[-1]["topics"].append(
            {
                "topic_id": topic_id,
                "topic_code": topic_id,
                "title": f"Title {topic_id}",
                "objective_ids": (),
            }
        )
    return EducationalArtefactSnapshot(
        curriculum_identity=curriculum_identity,
        subject_code=subject_code,
        version_label="test",
        journey=JourneySnapshot(
            curriculum_identity=curriculum_identity,
            sections=tuple(
                {
                    **section,
                    "topics": tuple(section["topics"]),
                }
                for section in sections
            ),
        ),
    )


class RecordingTwinQuery:
    """LearnerTwinQueryPort fake that records bulk vs per-topic call counts."""

    def __init__(self, facts: tuple[TopicKnowledgeFact, ...] = ()) -> None:
        self._facts = facts
        self.knowledge_snapshot_calls = 0
        self.topic_knowledge_calls = 0
        self.topic_covered_calls = 0

    def knowledge_snapshot(
        self, *, user_id: int, subject_code: str
    ) -> LearnerKnowledgeSnapshot:
        self.knowledge_snapshot_calls += 1
        return LearnerKnowledgeSnapshot(
            user_id=user_id,
            subject_code=subject_code,
            curriculum_identity="CS1:test",
            overall_estimated_knowledge=None,
            topics=self._facts,
        )

    def topic_knowledge(
        self, *, user_id: int, subject_code: str, topic_id: str
    ) -> TopicKnowledgeFact:
        self.topic_knowledge_calls += 1
        for fact in self._facts:
            if fact.topic_id == topic_id:
                return fact
        return _fact(topic_id)

    def topics_with_estimated_knowledge(
        self, *, user_id: int, subject_code: str
    ) -> tuple[TopicKnowledgeFact, ...]:
        return tuple(f for f in self._facts if f.has_estimated_knowledge)

    def topic_covered(
        self, *, user_id: int, subject_code: str, topic_id: str
    ) -> bool:
        self.topic_covered_calls += 1
        return False


class RecordingStudyProgressQuery:
    def __init__(self, progress: StudyProgress) -> None:
        self._progress = progress
        self.get_study_progress_calls = 0

    def get_study_progress(
        self, *, user_id: int, subject_code: str
    ) -> StudyProgress:
        self.get_study_progress_calls += 1
        return self._progress


class RecordingSyllabus:
    def __init__(
        self, artefacts: EducationalArtefactSnapshot | None
    ) -> None:
        self._artefacts = artefacts
        self.artefact_snapshot_calls = 0

    def artefact_snapshot(
        self, *, subject_code: str
    ) -> EducationalArtefactSnapshot | None:
        self.artefact_snapshot_calls += 1
        return self._artefacts


def _assembler(
    *,
    topic_ids: tuple[str, ...],
    completed: tuple[str, ...] = (),
    current_topic_id: str | None = None,
    facts: tuple[TopicKnowledgeFact, ...] = (),
) -> tuple[
    CurriculumLearningStateAssembler,
    RecordingTwinQuery,
    RecordingStudyProgressQuery,
]:
    progress = _progress(
        topic_ids=topic_ids,
        completed=completed,
        current_topic_id=current_topic_id,
    )
    twin = RecordingTwinQuery(facts)
    study = RecordingStudyProgressQuery(progress)
    syllabus = RecordingSyllabus(_artefacts(topic_ids=topic_ids))
    assembler = CurriculumLearningStateAssembler(
        twin_query=twin,
        study_progress=study,
        syllabus=syllabus,
    )
    return assembler, twin, study


def test_study_progress_complete_with_zero_twin_evidence_is_not_yet_assessed():
    """Completing a mission does not mint EK; covered + empty Twin is not mastered."""
    assembler, _, _ = _assembler(
        topic_ids=(TOPIC_COMPLETE_NO_EK, "CS1-A-T11"),
        completed=(TOPIC_COMPLETE_NO_EK,),
        current_topic_id="CS1-A-T11",
        facts=(),
    )
    snapshot = assembler.assemble(user_id=42, subject_code="CS1")
    by_id = {row.topic_id: row for row in snapshot.topics}

    assert TOPIC_COMPLETE_NO_EK in by_id
    row = by_id[TOPIC_COMPLETE_NO_EK]
    assert row.state is TopicLearningState.NOT_YET_ASSESSED
    assert row.state is not TopicLearningState.MASTERED
    assert row.state is not TopicLearningState.DEVELOPING
    assert row.last_practised_at is None
    assert is_ek_mastered(None) is False


def test_each_of_the_four_states_resolves_from_study_progress_and_twin_join():
    mastered_ek = 0.95
    developing_ek = 0.50
    assert mastered_ek * 100 >= EK_MASTERED_THRESHOLD
    assert developing_ek * 100 < EK_MASTERED_THRESHOLD

    facts = (
        _fact(
            TOPIC_MASTERED,
            estimated_knowledge=mastered_ek,
            evidence_count=POLICY_V1_MIN_EVIDENCE,
            last_practised_at=FIXED,
        ),
        _fact(
            TOPIC_DEVELOPING,
            estimated_knowledge=developing_ek,
            evidence_count=POLICY_V1_MIN_EVIDENCE,
            last_practised_at=FIXED,
        ),
    )
    assembler, _, _ = _assembler(
        topic_ids=(
            TOPIC_MASTERED,
            TOPIC_DEVELOPING,
            TOPIC_NOT_YET_ASSESSED,
            TOPIC_NOT_STARTED,
        ),
        completed=(TOPIC_MASTERED, TOPIC_DEVELOPING),
        current_topic_id=TOPIC_NOT_YET_ASSESSED,
        facts=facts,
    )
    snapshot = assembler.assemble(user_id=7, subject_code="CS1")
    by_id = {row.topic_id: row.state for row in snapshot.topics}

    assert by_id[TOPIC_MASTERED] is TopicLearningState.MASTERED
    assert by_id[TOPIC_DEVELOPING] is TopicLearningState.DEVELOPING
    assert by_id[TOPIC_NOT_YET_ASSESSED] is TopicLearningState.NOT_YET_ASSESSED
    assert by_id[TOPIC_NOT_STARTED] is TopicLearningState.NOT_STARTED

    mastered_row = next(
        row for row in snapshot.topics if row.topic_id == TOPIC_MASTERED
    )
    assert mastered_row.section_id == "S1"
    assert mastered_row.section_title == "Section S1"
    assert mastered_row.last_practised_at == FIXED
    assert mastered_row.title == f"Title {TOPIC_MASTERED}"


def test_bulk_twin_snapshot_and_study_progress_called_once_for_large_syllabus():
    topic_ids = tuple(f"CS1-T{index:02d}" for index in range(1, 61))
    facts = (
        _fact(
            topic_ids[0],
            estimated_knowledge=0.4,
            evidence_count=POLICY_V1_MIN_EVIDENCE,
        ),
    )
    assembler, twin, study = _assembler(
        topic_ids=topic_ids,
        completed=(topic_ids[0],),
        current_topic_id=topic_ids[1],
        facts=facts,
    )
    snapshot = assembler.assemble(user_id=99, subject_code="CS1")

    assert len(snapshot.topics) == 60
    assert twin.knowledge_snapshot_calls == 1
    assert study.get_study_progress_calls == 1
    assert twin.topic_knowledge_calls == 0
    assert twin.topic_covered_calls == 0


def test_thresholds_are_the_existing_project_constants_not_new_numbers():
    assert EVIDENCE_RELIABILITY_FLOOR is POLICY_V1_MIN_EVIDENCE
    assert MASTERY_THRESHOLD is EK_MASTERED_THRESHOLD
    assert EVIDENCE_RELIABILITY_FLOOR == 3
    assert MASTERY_THRESHOLD == 90.0

    below_floor = _fact(
        "CS1-A-T01",
        estimated_knowledge=0.99,
        evidence_count=POLICY_V1_MIN_EVIDENCE - 1,
    )
    at_floor_below_mastery = _fact(
        "CS1-A-T01",
        estimated_knowledge=(EK_MASTERED_THRESHOLD - 0.1) / 100.0,
        evidence_count=POLICY_V1_MIN_EVIDENCE,
    )
    at_floor_mastered = _fact(
        "CS1-A-T01",
        estimated_knowledge=EK_MASTERED_THRESHOLD / 100.0,
        evidence_count=POLICY_V1_MIN_EVIDENCE,
    )
    assert is_ek_mastered(below_floor) is False
    assert is_ek_mastered(at_floor_below_mastery) is False
    assert is_ek_mastered(at_floor_mastered) is True

    progress = _progress(
        topic_ids=("CS1-A-T01",),
        completed=("CS1-A-T01",),
        current_topic_id=None,
    )
    assert (
        resolve_topic_learning_state(
            topic_id="CS1-A-T01",
            progress=progress,
            fact=below_floor,
        )
        is TopicLearningState.NOT_YET_ASSESSED
    )
    assert (
        resolve_topic_learning_state(
            topic_id="CS1-A-T01",
            progress=progress,
            fact=at_floor_below_mastery,
        )
        is TopicLearningState.DEVELOPING
    )
    assert (
        resolve_topic_learning_state(
            topic_id="CS1-A-T01",
            progress=progress,
            fact=at_floor_mastered,
        )
        is TopicLearningState.MASTERED
    )


def test_blocked_incomplete_topic_before_current_is_not_started():
    """Incomplete + not current (blocked on prereqs) is not reached."""
    blocked = "CS1-A-T01"
    current = "CS1-A-T02"
    later = "CS1-A-T03"
    progress = _progress(
        topic_ids=(blocked, current, later),
        completed=(),
        current_topic_id=current,
    )
    assert (
        resolve_topic_learning_state(
            topic_id=blocked, progress=progress, fact=None
        )
        is TopicLearningState.NOT_STARTED
    )
    assert (
        resolve_topic_learning_state(
            topic_id=current, progress=progress, fact=None
        )
        is TopicLearningState.NOT_YET_ASSESSED
    )
    assert (
        resolve_topic_learning_state(
            topic_id=later, progress=progress, fact=None
        )
        is TopicLearningState.NOT_STARTED
    )


def test_practiced_future_topic_is_not_yet_assessed_not_not_started():
    future = "CS1-A-T03"
    progress = _progress(
        topic_ids=("CS1-A-T01", "CS1-A-T02", future),
        completed=("CS1-A-T01",),
        current_topic_id="CS1-A-T02",
    )
    practiced = _fact(
        future,
        estimated_knowledge=0.2,
        evidence_count=1,
        last_practised_at=FIXED,
    )
    assert (
        resolve_topic_learning_state(
            topic_id=future, progress=progress, fact=practiced
        )
        is TopicLearningState.NOT_YET_ASSESSED
    )


def test_topic_learning_state_enum_values_are_stable():
    assert StateEnum.NOT_STARTED == "not_started"
    assert StateEnum.NOT_YET_ASSESSED == "not_yet_assessed"
    assert StateEnum.DEVELOPING == "developing"
    assert StateEnum.MASTERED == "mastered"
