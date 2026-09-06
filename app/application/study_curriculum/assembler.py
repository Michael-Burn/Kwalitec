"""Join bulk Twin EK and bulk Study Progress into four honest topic states.

Uses exactly one ``knowledge_snapshot`` call and one ``get_study_progress``
call per invocation. Never loops ``topic_knowledge`` or ``topic_covered``.
"""

from __future__ import annotations

from app.application.educational_engine_foundation.dto import (
    EducationalArtefactSnapshot,
)
from app.application.learner_progress.milestones import is_ek_mastered
from app.application.progress_engine.dto import StudyProgress
from app.application.student_twin.cutover import ek_display_0_100
from app.application.student_twin.query import (
    LearnerTwinQueryPort,
    TopicKnowledgeFact,
)
from app.application.study_curriculum.ports import (
    StudyProgressQueryPort,
    SyllabusStructurePort,
)
from app.application.study_curriculum.states import (
    EVIDENCE_RELIABILITY_FLOOR,
    TopicLearningState,
)
from app.application.study_curriculum.types import (
    CurriculumLearningSnapshot,
    TopicCurriculumState,
)


def _has_trusted_estimated_knowledge(fact: TopicKnowledgeFact | None) -> bool:
    """True when Twin EK is present and meets the existing evidence floor."""
    if fact is None or not fact.has_estimated_knowledge:
        return False
    if int(fact.evidence_count or 0) < EVIDENCE_RELIABILITY_FLOOR:
        return False
    return ek_display_0_100(fact) is not None


def _has_practice_signal(fact: TopicKnowledgeFact | None) -> bool:
    """True when the Twin has any practice signal for the topic."""
    if fact is None:
        return False
    if fact.has_estimated_knowledge:
        return True
    if int(fact.evidence_count or 0) > 0:
        return True
    return fact.last_practised_at is not None


def topic_has_been_reached(topic_id: str, progress: StudyProgress) -> bool:
    """True when the sequential path has introduced this topic.

    Reached means: in ``completed_topic_ids``, or equal to ``current_topic_id``.
    Incomplete topics after current, and incomplete topics still blocked on
    prerequisites (incomplete but not current), have not been reached.
    ``get_study_progress`` expresses current as the first eligible incomplete
    topic; it does not expose a separate blocked set.
    """
    if topic_id in progress.completed_topic_ids:
        return True
    return bool(progress.current_topic_id) and topic_id == progress.current_topic_id


def _plan_has_reached(topic_id: str, progress: StudyProgress) -> bool:
    """Compatibility alias for ``topic_has_been_reached``."""
    return topic_has_been_reached(topic_id, progress)


def resolve_topic_learning_state(
    *,
    topic_id: str,
    progress: StudyProgress,
    fact: TopicKnowledgeFact | None,
) -> TopicLearningState:
    """Resolve one topic's four-state join. Pure; no I/O."""
    if is_ek_mastered(fact):
        return TopicLearningState.MASTERED
    if _has_trusted_estimated_knowledge(fact):
        return TopicLearningState.DEVELOPING
    if _plan_has_reached(topic_id, progress) or _has_practice_signal(fact):
        return TopicLearningState.NOT_YET_ASSESSED
    return TopicLearningState.NOT_STARTED


def _identity_from_topic_dict(
    topic: dict,
    *,
    section_id: str | None,
    section_title: str | None,
) -> tuple[str, str, str, str | None, str | None]:
    topic_id = str(topic.get("topic_id") or "").strip()
    topic_code = str(topic.get("topic_code") or topic.get("code") or "").strip()
    title = str(topic.get("title") or topic.get("text") or "").strip()
    return topic_id, topic_code, title, section_id, section_title


def _section_identity_index(
    artefacts: EducationalArtefactSnapshot | None,
) -> dict[str, tuple[str, str, str | None, str | None]]:
    """Map topic_id -> (topic_code, title, section_id, section_title)."""
    index: dict[str, tuple[str, str, str | None, str | None]] = {}
    if artefacts is None:
        return index

    journey = artefacts.journey
    if journey is not None:
        for section in journey.sections or ():
            if not isinstance(section, dict):
                continue
            section_id = str(section.get("section_id") or "").strip() or None
            section_title = str(section.get("title") or "").strip() or None
            for topic in section.get("topics") or ():
                if not isinstance(topic, dict):
                    continue
                topic_id, code, title, sid, stitle = _identity_from_topic_dict(
                    topic, section_id=section_id, section_title=section_title
                )
                if topic_id:
                    index[topic_id] = (code, title, sid, stitle)

    if index:
        return index

    section_titles = {
        str(section.get("section_id") or "").strip(): str(
            section.get("title") or ""
        ).strip()
        or None
        for section in (artefacts.sections or ())
        if isinstance(section, dict) and str(section.get("section_id") or "").strip()
    }
    for topic in artefacts.topics or ():
        if not isinstance(topic, dict):
            continue
        topic_id = str(topic.get("topic_id") or "").strip()
        if not topic_id:
            continue
        section_id = str(topic.get("section_id") or "").strip() or None
        section_title = section_titles.get(section_id) if section_id else None
        code = str(topic.get("code") or topic.get("topic_code") or "").strip()
        title = str(topic.get("title") or topic.get("text") or "").strip()
        index[topic_id] = (code, title, section_id, section_title)
    return index


class CurriculumLearningStateAssembler:
    """Assemble one honest learning state per syllabus topic.

    Given ``user_id`` and ``subject_code``, loads bulk Study Progress once,
    bulk Twin snapshot once, and published section membership once, then
    joins in memory.
    """

    def __init__(
        self,
        *,
        twin_query: LearnerTwinQueryPort,
        study_progress: StudyProgressQueryPort,
        syllabus: SyllabusStructurePort,
    ) -> None:
        self._twin_query = twin_query
        self._study_progress = study_progress
        self._syllabus = syllabus

    def assemble(
        self, *, user_id: int, subject_code: str
    ) -> CurriculumLearningSnapshot:
        """Return four-state rows for every published topic, in syllabus order."""
        progress = self._study_progress.get_study_progress(
            user_id=user_id,
            subject_code=subject_code,
        )
        snapshot = self._twin_query.knowledge_snapshot(
            user_id=user_id,
            subject_code=subject_code,
        )
        artefacts = self._syllabus.artefact_snapshot(subject_code=subject_code)
        facts_by_topic = {fact.topic_id: fact for fact in snapshot.topics}
        identity = _section_identity_index(artefacts)

        rows: list[TopicCurriculumState] = []
        for topic_id in progress.topic_ids:
            fact = facts_by_topic.get(topic_id)
            code, title, section_id, section_title = identity.get(
                topic_id, ("", "", None, None)
            )
            rows.append(
                TopicCurriculumState(
                    topic_id=topic_id,
                    topic_code=code,
                    title=title or topic_id,
                    section_id=section_id,
                    section_title=section_title,
                    state=resolve_topic_learning_state(
                        topic_id=topic_id,
                        progress=progress,
                        fact=fact,
                    ),
                    last_practised_at=(
                        fact.last_practised_at if fact is not None else None
                    ),
                    reached=topic_has_been_reached(topic_id, progress),
                )
            )
        return CurriculumLearningSnapshot(
            user_id=user_id,
            subject_code=subject_code,
            curriculum_identity=progress.curriculum_identity,
            topics=tuple(rows),
        )
