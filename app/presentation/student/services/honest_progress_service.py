"""Honest Progress / Stats presentation service.

Read-only assembly over QualifyingStudyDayQueryPort, the Study Curriculum
assembler, Study Progress, and the append-only milestones-shown store. Does
not write Twin state, Study Progress, or ADR-027 decision artefacts.
"""

from __future__ import annotations

import logging
from datetime import date

from flask import flash, url_for

from app.application.learner_progress.milestone_detector import (
    LearnerProgressMilestoneDetector,
)
from app.application.learner_progress.milestones import (
    SectionProgressSpec,
)
from app.application.learner_progress.query import (
    QualifyingStudyDayQueryPort,
    StreakStats,
)
from app.application.study_curriculum.states import TopicLearningState
from app.infrastructure.adapters.learner_progress.query_adapter import (
    qualifying_study_day_query,
)
from app.infrastructure.adapters.learner_progress.shown_milestones_persistence import (
    MilestonesShownPersistence,
)
from app.presentation.student.coverage_honesty import (
    verified_coverage_from_progress,
)
from app.presentation.student.dto.honest_progress import (
    HonestProgressPage,
    LearningStateCountRow,
    ProgressMilestoneRow,
)

logger = logging.getLogger(__name__)

_EMPTY_MILESTONES = "No milestones reached yet."
_PAGE_TITLE = "Stats"
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
_STATE_ORDER: tuple[TopicLearningState, ...] = (
    TopicLearningState.NOT_STARTED,
    TopicLearningState.NOT_YET_ASSESSED,
    TopicLearningState.DEVELOPING,
    TopicLearningState.MASTERED,
)


class HonestProgressService:
    """Present honest streak, one-shot milestones, and Stats page facts."""

    def __init__(
        self,
        *,
        study_day_query: QualifyingStudyDayQueryPort | None = None,
        shown_store: MilestonesShownPersistence | None = None,
        twin_query=None,
        detector: LearnerProgressMilestoneDetector | None = None,
        assembler=None,
        study_progress=None,
    ) -> None:
        self._study_day_query = study_day_query or qualifying_study_day_query()
        self._shown = shown_store or MilestonesShownPersistence()
        self._twin_query = twin_query
        self._detector = detector
        self._assembler = assembler
        self._study_progress = study_progress

    def streak_stats(self, *, user_id: int, as_of: date | None = None) -> StreakStats:
        """Current and longest streak from the qualifying study day port."""
        day = as_of or date.today()
        try:
            return self._study_day_query.streak_stats(user_id=user_id, as_of=day)
        except Exception:  # noqa: BLE001 - fail-open for presentation
            logger.warning("honest_progress_streak_failed", exc_info=True)
            return StreakStats(
                current_streak_days=0,
                longest_streak_days=0,
                qualifying_dates=(),
            )

    def consume_new_milestones(
        self,
        *,
        user_id: int,
        as_of: date | None = None,
        flash_messages: bool = False,
    ) -> tuple[str, ...]:
        """Detect newly earned milestones, record as shown, return labels.

        Used by Home (with flash) and Session complete (inline, no flash).
        """
        day = as_of or date.today()
        announced: list[str] = []
        try:
            subject_code = self._resolve_subject_code(user_id)
            if not subject_code:
                return ()

            previously = self._shown.previously_shown_ids(
                learner_id=str(user_id)
            )
            sections, topic_titles = self._section_specs(subject_code)
            completed = self._completed_topic_ids(
                user_id=user_id, subject_code=subject_code
            )
            detector = self._milestone_detector()
            new_milestones = detector.detect_new_milestones(
                user_id=user_id,
                subject_code=subject_code,
                sections=sections,
                completed_topic_ids=completed,
                previously_earned=previously,
                as_of=day,
                topic_titles=topic_titles,
            )
            for milestone in new_milestones:
                recorded = self._shown.record_shown(
                    learner_id=str(user_id),
                    milestone_id=milestone.milestone_id,
                    label=milestone.label,
                    shown_at=day,
                )
                if not recorded:
                    continue
                if flash_messages:
                    flash(milestone.label, "success")
                announced.append(milestone.label)
        except Exception:  # noqa: BLE001 - fail-open; never break callers
            logger.warning("honest_progress_announce_failed", exc_info=True)
            return tuple(announced)
        return tuple(announced)

    def announce_new_milestones_on_home(
        self,
        *,
        user_id: int,
        as_of: date | None = None,
    ) -> tuple[str, ...]:
        """Detect newly earned milestones, flash once, record as shown.

        Checkpoint: Student Home load. Returns labels that were announced.
        """
        return self.consume_new_milestones(
            user_id=user_id,
            as_of=as_of,
            flash_messages=True,
        )

    def build_progress_page(
        self,
        *,
        user_id: int,
        as_of: date | None = None,
    ) -> HonestProgressPage:
        """Assemble the dedicated Stats page from read-only ports."""
        day = as_of or date.today()
        streak = self.streak_stats(user_id=user_id, as_of=day)
        (
            covered,
            total,
            coverage_percent,
            coverage_label,
            claimed_count,
            claim_label,
        ) = self._syllabus_coverage(user_id)
        learning_counts = self._learning_state_counts(user_id)
        mastered = next(
            (
                row.count
                for row in learning_counts
                if row.state == TopicLearningState.MASTERED.value
            ),
            0,
        )
        shown = self._shown.list_shown(learner_id=str(user_id))
        rows = tuple(
            ProgressMilestoneRow(
                milestone_id=r.milestone_id,
                label=r.label,
                shown_at=r.shown_at,
                shown_at_label=r.shown_at.isoformat(),
            )
            for r in shown
        )
        try:
            href = url_for("student.progress")
        except Exception:  # noqa: BLE001
            href = "/student/progress"
        return HonestProgressPage(
            page_title=_PAGE_TITLE,
            current_streak_days=streak.current_streak_days,
            longest_streak_days=streak.longest_streak_days,
            syllabus_coverage_percent=coverage_percent,
            syllabus_coverage_label=coverage_label,
            covered_count=covered,
            topic_count=total,
            prior_knowledge_claimed_count=claimed_count,
            prior_knowledge_claim_label=claim_label,
            learning_state_counts=learning_counts,
            topics_mastered_count=mastered,
            milestones=rows,
            empty_milestones_message=_EMPTY_MILESTONES,
            progress_href=href,
        )

    def _milestone_detector(self) -> LearnerProgressMilestoneDetector:
        if self._detector is not None:
            return self._detector
        twin = self._twin_query
        if twin is None:
            from app.services.twin_cutover_service import learner_twin_query

            twin = learner_twin_query()
        return LearnerProgressMilestoneDetector(
            twin_query=twin,
            study_day_query=self._study_day_query,
        )

    @staticmethod
    def _resolve_subject_code(user_id: int) -> str:
        try:
            from app.services.twin_cutover_service import subject_code_for_user

            code = subject_code_for_user(user_id)
            return (code or "").strip().upper()
        except Exception:  # noqa: BLE001
            logger.warning("honest_progress_subject_failed", exc_info=True)
            return ""

    def _completed_topic_ids(
        self, *, user_id: int, subject_code: str
    ) -> frozenset[str]:
        try:
            progress = self._study_progress_service()
            snap = progress.get_study_progress(
                user_id=user_id,
                subject_code=subject_code,
            )
            return frozenset(
                str(tid).strip()
                for tid in (snap.completed_topic_ids or ())
                if str(tid).strip()
            )
        except Exception:  # noqa: BLE001
            logger.warning("honest_progress_completed_failed", exc_info=True)
            return frozenset()

    def _section_specs(
        self, subject_code: str
    ) -> tuple[tuple[SectionProgressSpec, ...], dict[str, str]]:
        """Build section specs from certified package graph; soft-fail empty."""
        try:
            from app.application.curriculum_intelligence import (
                certified_learning_service as cls,
            )
            from app.domain.curriculum_intelligence.certified_learning import (
                CertifiedNodeKind,
            )

            service = cls.CertifiedLearningService()
            package = service.load_package(subject_code)
            graph = service.knowledge_graph(package)
        except Exception:  # noqa: BLE001
            return (), {}

        topic_titles: dict[str, str] = {}
        by_parent: dict[str, list[str]] = {}
        section_titles: dict[str, str] = {}
        for node in graph.nodes:
            kind = node.kind
            kind_value = kind.value if hasattr(kind, "value") else str(kind)
            if kind in {
                CertifiedNodeKind.TOPIC,
            } or kind_value == "topic":
                tid = (node.node_id or "").strip()
                if tid:
                    topic_titles[tid] = (node.title or "").strip() or tid
                    parent = (node.parent_node_id or "").strip()
                    if parent:
                        by_parent.setdefault(parent, []).append(tid)
            if kind in {
                CertifiedNodeKind.CHAPTER,
                CertifiedNodeKind.SECTION,
            } or kind_value in {"chapter", "section"}:
                sid = (node.node_id or "").strip()
                if sid:
                    section_titles[sid] = (node.title or "").strip() or sid

        sections: list[SectionProgressSpec] = []
        for section_id, title in section_titles.items():
            topic_ids = frozenset(by_parent.get(section_id) or ())
            if not topic_ids:
                continue
            sections.append(
                SectionProgressSpec(
                    section_id=section_id,
                    title=title,
                    topic_ids=topic_ids,
                )
            )
        return tuple(sections), topic_titles

    def _study_progress_service(self):
        if self._study_progress is not None:
            return self._study_progress
        from app.application.educational_runtime_engine.service import (
            EducationalRuntimeEngineService,
        )

        return EducationalRuntimeEngineService()

    def _syllabus_coverage(
        self, user_id: int
    ) -> tuple[int, int, int | None, str, int, str]:
        """Verified Study Progress coverage (same honesty rule as Study/Home)."""
        subject_code = self._resolve_subject_code(user_id)
        if not subject_code:
            return 0, 0, None, "", 0, ""
        try:
            snap = self._study_progress_service().get_study_progress(
                user_id=user_id,
                subject_code=subject_code,
            )
            parts = verified_coverage_from_progress(snap)
            return (
                parts.verified_count,
                parts.topic_count,
                parts.verified_percent if parts.topic_count else None,
                parts.coverage_label,
                parts.claimed_count,
                parts.claim_label,
            )
        except Exception:  # noqa: BLE001
            logger.warning("honest_progress_coverage_failed", exc_info=True)
            return 0, 0, None, "", 0, ""

    def _learning_state_counts(
        self, user_id: int
    ) -> tuple[LearningStateCountRow, ...]:
        """Aggregate four-state counts from the Study Curriculum assembler."""
        empty = tuple(
            LearningStateCountRow(
                state=state.value,
                state_label=_STATE_LABELS[state],
                state_icon=_STATE_ICONS[state],
                count=0,
            )
            for state in _STATE_ORDER
        )
        subject_code = self._resolve_subject_code(user_id)
        if not subject_code:
            return empty
        try:
            assembler = self._assembler
            if assembler is None:
                from app.infrastructure.adapters.study_curriculum.runtime_query import (
                    curriculum_learning_state_assembler,
                )

                assembler = curriculum_learning_state_assembler()
            snapshot = assembler.assemble(
                user_id=user_id, subject_code=subject_code
            )
            tallies = {state: 0 for state in _STATE_ORDER}
            for row in snapshot.topics or ():
                state = row.state
                if state in tallies:
                    tallies[state] += 1
            return tuple(
                LearningStateCountRow(
                    state=state.value,
                    state_label=_STATE_LABELS[state],
                    state_icon=_STATE_ICONS[state],
                    count=tallies[state],
                )
                for state in _STATE_ORDER
            )
        except Exception:  # noqa: BLE001
            logger.warning("honest_progress_learning_states_failed", exc_info=True)
            return empty
