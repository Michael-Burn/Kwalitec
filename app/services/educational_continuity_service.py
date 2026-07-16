"""Educational Continuity (EIP-005).

Educational history belongs to the learner, not the Study Plan container.

Deleting, replacing, or migrating a Study Plan may dispose of temporary
planning artefacts. It must never silently destroy Study Progress, Study
Attempts, Educational Evidence posture, Estimated Knowledge, or Estimated
Mastery.

Governing refs:
- Constitution Articles II §1.8, IV, VIII.15, IX §4
- EL-001, EL-011
- EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md §4–5
- EDUCATIONAL_CONTINUITY_STANDARD.md
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.mission import Mission
from app.models.study_plan import StudyPlan
from app.models.topic_progress import TopicProgress

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RemapResult:
    """Outcome of an educational remapping attempt across curricula."""

    remapped_topic_ids: tuple[int, ...] = ()
    retained_unmapped_topic_ids: tuple[int, ...] = ()
    skipped_existing_topic_ids: tuple[int, ...] = ()
    notes: tuple[str, ...] = field(default_factory=tuple)

    @property
    def remapped_count(self) -> int:
        return len(self.remapped_topic_ids)


class EducationalContinuityService:
    """Enforce learner-owned educational history across Study Plan lifecycles."""

    # Coverage / estimate fields that may lawfully continue to a mapped unit.
    _CONTINUITY_FIELDS: tuple[str, ...] = (
        "confidence",
        "completed",
        "last_reviewed",
        "revision_count",
        "mastery_score",
        "average_accuracy",
        "average_confidence",
        "next_review_date",
        "current_stage",
    )

    @staticmethod
    def release_plan_planning_artifacts(study_plan: StudyPlan) -> int:
        """Detach planning-only links so a Study Plan can be deleted safely.

        Preserves Missions, Study Attempts, TopicProgress, and Decision Journal
        rows as learner educational history. Clears active mission plan pointers
        so temporary planning context does not block deletion.

        Args:
            study_plan: The Study Plan about to be removed.

        Returns:
            Number of Mission rows whose ``study_plan_id`` was cleared.
        """
        missions = Mission.query.filter_by(study_plan_id=study_plan.id).all()
        detached = 0
        for mission in missions:
            mission.study_plan_id = None
            detached += 1

        if detached:
            logger.info(
                "EIP-005: detached %s mission pointer(s) from study plan %s "
                "(missions retained as educational history).",
                detached,
                study_plan.id,
            )
        return detached

    @staticmethod
    def resolve_official_topic_code(
        db_topic: Topic,
        *,
        exam_name: str,
        curriculum_version: str,
    ) -> str | None:
        """Resolve the official syllabus topic code for a DB topic.

        Matches engine topic title to ``Topic.name``. When identity cannot be
        determined objectively, returns ``None`` (honest uncertainty).

        Args:
            db_topic: Persisted topic row.
            exam_name: Study-plan style exam name (e.g. ``\"IFoA CS1\"``).
            curriculum_version: Syllabus version string.

        Returns:
            Official topic code, or ``None`` when remapping identity is unknown.
        """
        parts = (exam_name or "").split(" ", 1)
        if len(parts) != 2 or not curriculum_version:
            return None

        organisation, paper = parts
        from app.services.study_plan_service import StudyPlanService

        load_result = StudyPlanService._load_engine_curriculum_auto(
            organisation, paper, curriculum_version
        )
        if load_result is None:
            return None

        engine_curriculum, is_v2 = load_result
        for engine_topic in StudyPlanService._get_engine_topics_ordered(
            engine_curriculum, is_v2
        ):
            if engine_topic.title == db_topic.name:
                code = getattr(engine_topic, "code", None)
                return str(code) if code else None
        return None

    @staticmethod
    def remap_study_progress_to_curriculum(
        user_id: int,
        target_curriculum: Curriculum,
        *,
        exam_name: str | None = None,
    ) -> RemapResult:
        """Remap learner Study Progress onto a target curriculum where lawful.

        Remapping requires an objective official topic-code match between a
        prior curriculum topic (same exam family) and a target topic.

        Rules:
        - Never invent equivalence when code identity is unknown.
        - Never overwrite richer existing target progress.
        - Retain unmapped prior rows as historical learner assets.

        Args:
            user_id: Learner whose educational history may continue.
            target_curriculum: Curriculum the new / repaired plan uses.
            exam_name: Optional exam label override; defaults to curriculum.

        Returns:
            RemapResult describing remapped, retained, and skipped units.
        """
        exam_label = exam_name or target_curriculum.exam_name
        prior_curricula = (
            Curriculum.query.filter(
                Curriculum.exam_name == target_curriculum.exam_name,
                Curriculum.id != target_curriculum.id,
            ).all()
        )
        if not prior_curricula:
            return RemapResult(notes=("No prior curricula for exam family.",))

        prior_ids = [c.id for c in prior_curricula]
        prior_topics = Topic.query.filter(Topic.curriculum_id.in_(prior_ids)).all()
        if not prior_topics:
            return RemapResult(notes=("No prior topics to remap.",))

        prior_by_id = {t.id: t for t in prior_topics}
        prior_curriculum_by_id = {c.id: c for c in prior_curricula}

        source_by_code: dict[str, list[TopicProgress]] = {}
        retained_unmapped: list[int] = []

        for source_tp in TopicProgress.query.filter(
            TopicProgress.user_id == user_id,
            TopicProgress.topic_id.in_([t.id for t in prior_topics]),
        ).all():
            source_topic = prior_by_id.get(source_tp.topic_id)
            if source_topic is None:
                retained_unmapped.append(source_tp.topic_id)
                continue
            source_curriculum = prior_curriculum_by_id.get(source_topic.curriculum_id)
            if source_curriculum is None:
                retained_unmapped.append(source_tp.topic_id)
                continue
            code = EducationalContinuityService.resolve_official_topic_code(
                source_topic,
                exam_name=exam_label,
                curriculum_version=source_curriculum.version,
            )
            if not code:
                retained_unmapped.append(source_tp.topic_id)
                continue
            source_by_code.setdefault(code, []).append(source_tp)

        remapped: list[int] = []
        skipped_existing: list[int] = []
        notes: list[str] = []
        consumed_codes: set[str] = set()

        target_topics = Topic.query.filter_by(
            curriculum_id=target_curriculum.id, active=True
        ).all()

        for target_topic in target_topics:
            code = EducationalContinuityService.resolve_official_topic_code(
                target_topic,
                exam_name=exam_label,
                curriculum_version=target_curriculum.version,
            )
            if not code:
                continue

            candidates = source_by_code.get(code)
            if not candidates:
                continue

            consumed_codes.add(code)

            # Prefer the richest prior row for this code (evidence > coverage).
            source_tp = max(
                candidates,
                key=lambda tp: (
                    tp.average_accuracy is not None,
                    float(tp.mastery_score or 0.0),
                    bool(tp.completed),
                    int(tp.revision_count or 0),
                ),
            )

            existing = TopicProgress.query.filter_by(
                user_id=user_id, topic_id=target_topic.id
            ).first()

            has_history = EducationalContinuityService._has_learner_history(
                existing
            ) if existing is not None else False

            if existing is not None and has_history:
                # Fill missing estimate posture from mapped prior history without
                # rewriting Study Progress coverage the learner already holds.
                can_fill = EducationalContinuityService._can_fill_estimates(
                    existing, source_tp
                )
                if can_fill:
                    EducationalContinuityService._copy_estimate_fields(
                        source_tp, existing
                    )
                    remapped.append(target_topic.id)
                else:
                    skipped_existing.append(target_topic.id)
                continue

            if existing is None:
                existing = TopicProgress(
                    user_id=user_id,
                    topic_id=target_topic.id,
                    confidence="Not Started",
                    completed=False,
                    mastery_score=0.0,
                    revision_count=0,
                    current_stage=TopicProgress.STAGE_NOT_STARTED,
                )
                db.session.add(existing)
                db.session.flush()

            EducationalContinuityService._copy_continuity_fields(source_tp, existing)
            remapped.append(target_topic.id)

        # Prior units whose official codes had no target match remain historical
        # learner assets — do not invent equivalence.
        for code, candidates in source_by_code.items():
            if code in consumed_codes:
                continue
            for source_tp in candidates:
                retained_unmapped.append(source_tp.topic_id)

        if remapped:
            notes.append(
                f"Remapped {len(remapped)} syllabus unit(s) by official topic code."
            )
        if retained_unmapped:
            notes.append(
                f"Retained {len(retained_unmapped)} unmapped historical unit(s) "
                "without inventing equivalence."
            )

        logger.info(
            "EIP-005 remap user=%s target_curriculum=%s remapped=%s "
            "retained_unmapped=%s skipped_existing=%s",
            user_id,
            target_curriculum.id,
            len(remapped),
            len(retained_unmapped),
            len(skipped_existing),
        )
        return RemapResult(
            remapped_topic_ids=tuple(remapped),
            retained_unmapped_topic_ids=tuple(retained_unmapped),
            skipped_existing_topic_ids=tuple(skipped_existing),
            notes=tuple(notes),
        )

    @staticmethod
    def _has_learner_history(tp: TopicProgress) -> bool:
        """Return True when a TopicProgress row already holds educational history."""
        if tp.completed:
            return True
        if tp.average_accuracy is not None:
            return True
        if (tp.mastery_score or 0.0) > 0.0:
            return True
        if (tp.revision_count or 0) > 0:
            return True
        if tp.last_reviewed is not None:
            return True
        if tp.current_stage not in (
            TopicProgress.STAGE_NOT_STARTED,
            TopicProgress.STAGE_LEARNING,
            None,
            "",
        ):
            return True
        return False

    @staticmethod
    def _can_fill_estimates(target: TopicProgress, source: TopicProgress) -> bool:
        """True when target lacks estimate/evidence posture but source has it."""
        target_has_estimates = (
            target.average_accuracy is not None or (target.mastery_score or 0.0) > 0.0
        )
        source_has_estimates = (
            source.average_accuracy is not None or (source.mastery_score or 0.0) > 0.0
        )
        return (not target_has_estimates) and source_has_estimates

    @staticmethod
    def _copy_estimate_fields(source: TopicProgress, target: TopicProgress) -> None:
        """Continue estimate / evidence posture without rewriting Study Progress."""
        target.mastery_score = source.mastery_score
        target.average_accuracy = source.average_accuracy
        target.average_confidence = source.average_confidence
        if source.last_reviewed is not None and target.last_reviewed is None:
            target.last_reviewed = source.last_reviewed
        if (source.revision_count or 0) > (target.revision_count or 0):
            target.revision_count = source.revision_count
        # Preserve coverage stages (Completed / Learning). Only adopt stage when
        # target remains a cold coverage start and source stage is estimate-bearing.
        if (
            target.current_stage
            in (TopicProgress.STAGE_NOT_STARTED, TopicProgress.STAGE_LEARNING)
            and source.current_stage
            in (
                TopicProgress.STAGE_PRACTISING,
                TopicProgress.STAGE_MASTERED,
                TopicProgress.STAGE_NEEDS_REVIEW,
            )
        ):
            target.current_stage = source.current_stage

    @staticmethod
    def _copy_continuity_fields(source: TopicProgress, target: TopicProgress) -> None:
        """Copy learner-owned continuity fields without inventing new values."""
        for field_name in EducationalContinuityService._CONTINUITY_FIELDS:
            setattr(target, field_name, getattr(source, field_name))
