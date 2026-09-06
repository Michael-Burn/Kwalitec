"""Study Curriculum presentation: syllabus map with four honest states.

Calls the Study Curriculum assembler once per page load and projects its
flat topic rows into a sectioned view. Coverage uses Runtime C
``get_study_progress`` (the same call Journey, Home, and Honest Progress
use). Continue is a Home resume deep-link, never a new recommendation.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Mapping

from flask import url_for

from app.application.study_curriculum.states import TopicLearningState
from app.application.study_curriculum.types import (
    CurriculumLearningSnapshot,
    TopicCurriculumState,
)
from app.presentation.student.dto.study_curriculum import (
    StudentStudyCurriculumPage,
    StudySectionView,
    StudyTopicView,
)

logger = logging.getLogger(__name__)

_STATE_LABELS: dict[TopicLearningState, str] = {
    TopicLearningState.NOT_STARTED: "Not started",
    TopicLearningState.NOT_YET_ASSESSED: "Not yet assessed",
    TopicLearningState.DEVELOPING: "Developing",
    TopicLearningState.MASTERED: "Mastered",
}
_STATE_ICONS: dict[TopicLearningState, str] = {
    TopicLearningState.NOT_STARTED: "",
    TopicLearningState.NOT_YET_ASSESSED: "clock",
    TopicLearningState.DEVELOPING: "journey",
    TopicLearningState.MASTERED: "topics",
}
_EMPTY_NO_EXAM = "Choose an exam to see your syllabus."
_EMPTY_NO_TOPICS = "Your syllabus appears when a study plan is active."
_EMPTY_ACTION = "Choose Exam"
_PAGE_TITLE = "Study"
_PAGE_QUESTION = "Where am I on the syllabus?"


class StudentStudyCurriculumPresentationService:
    """Project assembler output into the Study Curriculum template."""

    def __init__(
        self,
        *,
        assembler=None,
        study_progress=None,
        why_lookup: Callable[[str], Mapping[str, str]] | None = None,
    ) -> None:
        self._assembler = assembler
        self._study_progress = study_progress
        self._why_lookup = why_lookup

    def build(
        self,
        *,
        user_id: int,
        subject_code: str = "",
        subject_label: str = "",
        continue_href: str = "",
        continue_label: str = "Continue",
    ) -> StudentStudyCurriculumPage:
        """Assemble one Study Curriculum page for a learner."""
        choose_href = _choose_exam_href()
        empty = StudentStudyCurriculumPage(
            page_title=_PAGE_TITLE,
            page_question=_PAGE_QUESTION,
            surface="study",
            subject_label=subject_label,
            coverage_label="",
            covered_count=0,
            topic_count=0,
            coverage_ratio=0.0,
            sections=(),
            continue_href=(continue_href or "").strip(),
            continue_label=(continue_label or "Continue").strip() or "Continue",
            empty_reason=_EMPTY_NO_EXAM,
            empty_action_label=_EMPTY_ACTION,
            empty_action_href=choose_href,
        )
        code = (subject_code or "").strip().upper()
        if not code:
            return empty

        snapshot = self._assemble(user_id=user_id, subject_code=code)
        covered, total, ratio = self._coverage(
            user_id=user_id, subject_code=code
        )
        why_by_topic = self._why_for_subject(code)
        sections = _group_sections(snapshot.topics, why_by_topic=why_by_topic)
        has_topics = bool(snapshot.topics)
        coverage_label = (
            f"{covered} of {total} topics covered" if total else ""
        )
        return StudentStudyCurriculumPage(
            page_title=_PAGE_TITLE,
            page_question=_PAGE_QUESTION,
            surface="study",
            subject_label=subject_label or code,
            coverage_label=coverage_label,
            covered_count=covered,
            topic_count=total,
            coverage_ratio=ratio,
            sections=sections,
            continue_href=(continue_href or "").strip(),
            continue_label=(continue_label or "Continue").strip() or "Continue",
            empty_reason="" if has_topics else _EMPTY_NO_TOPICS,
            empty_action_label="" if has_topics else _EMPTY_ACTION,
            empty_action_href="" if has_topics else choose_href,
        )

    def _assemble(
        self, *, user_id: int, subject_code: str
    ) -> CurriculumLearningSnapshot:
        assembler = self._assembler
        if assembler is None:
            from app.infrastructure.adapters.study_curriculum.runtime_query import (
                curriculum_learning_state_assembler,
            )

            assembler = curriculum_learning_state_assembler()
        try:
            return assembler.assemble(user_id=user_id, subject_code=subject_code)
        except Exception:  # noqa: BLE001 — presentation soft-fail
            logger.warning("study_curriculum_assemble_failed", exc_info=True)
            return CurriculumLearningSnapshot(
                user_id=user_id,
                subject_code=subject_code,
                curriculum_identity="",
                topics=(),
            )

    def _coverage(
        self, *, user_id: int, subject_code: str
    ) -> tuple[int, int, float]:
        """Reuse Runtime C ``get_study_progress`` coverage, not four-state counts."""
        try:
            progress = self._study_progress
            if progress is None:
                from app.application.educational_runtime_engine.service import (
                    EducationalRuntimeEngineService,
                )

                progress = EducationalRuntimeEngineService()
            snap = progress.get_study_progress(
                user_id=user_id,
                subject_code=subject_code,
            )
            total = len(snap.topic_ids or ())
            covered = len(snap.completed_topic_ids or ())
            ratio = float(snap.coverage_ratio or 0.0)
            return covered, total, ratio
        except Exception:  # noqa: BLE001 — presentation soft-fail
            logger.warning("study_curriculum_coverage_failed", exc_info=True)
            return 0, 0, 0.0

    def _why_for_subject(self, subject_code: str) -> Mapping[str, str]:
        if self._why_lookup is not None:
            try:
                return self._why_lookup(subject_code)
            except Exception:  # noqa: BLE001
                logger.warning("study_curriculum_why_lookup_failed", exc_info=True)
                return {}
        return _why_from_knowledge_architecture(subject_code)


def _choose_exam_href() -> str:
    try:
        return url_for("study_plan.index")
    except Exception:  # noqa: BLE001
        return "/study-plan"


def _group_sections(
    topics: tuple[TopicCurriculumState, ...],
    *,
    why_by_topic: Mapping[str, str],
) -> tuple[StudySectionView, ...]:
    sections: list[StudySectionView] = []
    current_id = None
    current_title = ""
    current_rows: list[StudyTopicView] = []
    for row in topics:
        key = (row.section_id or "").strip()
        title = (row.section_title or "").strip() or "Syllabus"
        if current_id is None:
            current_id = key
            current_title = title
        elif key != current_id:
            sections.append(
                StudySectionView(
                    section_id=current_id,
                    title=current_title,
                    topics=tuple(current_rows),
                )
            )
            current_id = key
            current_title = title
            current_rows = []
        current_rows.append(_topic_view(row, why_by_topic))
    if current_rows:
        sections.append(
            StudySectionView(
                section_id=current_id or "",
                title=current_title or "Syllabus",
                topics=tuple(current_rows),
            )
        )
    return tuple(sections)


def _topic_view(
    row: TopicCurriculumState,
    why_by_topic: Mapping[str, str],
) -> StudyTopicView:
    state = row.state
    return StudyTopicView(
        topic_id=row.topic_id,
        topic_code=row.topic_code,
        title=row.title or row.topic_id,
        state=str(state),
        state_label=_STATE_LABELS.get(state, str(state).replace("_", " ")),
        state_icon=_STATE_ICONS.get(state, ""),
        why_it_matters=(why_by_topic.get(row.topic_id) or "").strip(),
        is_quiet=state is TopicLearningState.NOT_STARTED,
    )


def _why_from_knowledge_architecture(subject_code: str) -> dict[str, str]:
    """Per-topic curriculum rationale from the existing graph helper.

    ``why_topic_matters`` already accepts any topic_id. This loads the graph
    once and asks it for each node. Soft-fails to empty when unpublished.
    """
    code = (subject_code or "").strip().upper()
    if not code:
        return {}
    try:
        from app.application.curriculum_intelligence import (
            certified_learning_service as cls,
        )
        from app.application.knowledge_architecture.graph_adapter import (
            graph_from_learner_package,
        )
        from app.application.knowledge_architecture.prerequisite_reasoning import (
            why_topic_matters,
        )

        package = cls.CertifiedLearningService().load_package(code)
        graph = graph_from_learner_package(package)
        if graph is None or graph.topic_count() == 0:
            return {}
        return {
            node.topic_id.value: why_topic_matters(graph, node.topic_id.value)
            for node in graph.nodes()
            if node.topic_id and node.topic_id.value
        }
    except Exception:  # noqa: BLE001 — presentation soft-fail
        logger.warning("study_curriculum_why_graph_failed", exc_info=True)
        return {}
