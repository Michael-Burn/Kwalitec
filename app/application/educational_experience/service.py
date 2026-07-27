"""Educational Experience Service — Runtime C → student surfaces (PX-001).

Resolves an active Runtime C enrolment, ensures today's mission exists, and
projects EQ-001 quality / journey / pacing envelopes into student-safe
snapshots. Does not activate Twin or cut over Runtime A defaults.
"""

from __future__ import annotations

import logging
from datetime import date
from typing import Any

from app.application.educational_engine_foundation.service import (
    EducationalEngineFoundationService,
)
from app.application.educational_experience.dto import (
    CurriculumPositionSnapshot,
    EducationalExperienceSnapshot,
    JourneyEducationSnapshot,
    MissionEducationSnapshot,
    PacingEducationSnapshot,
)
from app.application.educational_quality.dto import (
    JourneyExplanationSnapshot,
    MissionQualityEnvelope,
    StudyPlanPacingSnapshot,
)
from app.application.educational_runtime_engine.dto import (
    MissionInstanceSnapshot,
    ProgressSnapshot,
    RuntimeJourneySnapshot,
)
from app.application.educational_runtime_engine.exceptions import (
    IllegalRuntimeState,
    MissionInstanceNotFound,
    SyllabusAlreadyComplete,
)
from app.application.educational_runtime_engine.service import (
    EducationalRuntimeEngineService,
)
from app.domain.educational_runtime_engine.state import EnrolmentStatus
from app.models.educational_runtime_engine import RuntimeEnrolment

logger = logging.getLogger(__name__)


class EducationalExperienceService:
    """Project Runtime C educational outputs for student Home / Journey."""

    SERVICE_ID = "educational_experience"
    SERVICE_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        runtime: EducationalRuntimeEngineService | None = None,
        artefacts: EducationalEngineFoundationService | None = None,
    ) -> None:
        self._runtime = runtime or EducationalRuntimeEngineService()
        self._artefacts = artefacts or EducationalEngineFoundationService()

    def find_active_enrolment(
        self, user_id: int
    ) -> RuntimeEnrolment | None:
        """Return the most recent active Runtime C enrolment, if any."""
        return (
            RuntimeEnrolment.query.filter_by(
                user_id=user_id,
                status=EnrolmentStatus.ACTIVE.value,
            )
            .order_by(RuntimeEnrolment.id.desc())
            .first()
        )

    def find_enrolment_for_experience(
        self, user_id: int
    ) -> RuntimeEnrolment | None:
        """Active enrolment, or a completed one for post-syllabus Home/Journey.

        PR-001B: after syllabus completion the enrolment leaves ACTIVE.
        Students must still see progress and a clear complete state rather
        than falling through to an empty Runtime A Home.
        """
        active = self.find_active_enrolment(user_id)
        if active is not None:
            return active
        return (
            RuntimeEnrolment.query.filter_by(
                user_id=user_id,
                status=EnrolmentStatus.COMPLETED.value,
            )
            .order_by(RuntimeEnrolment.id.desc())
            .first()
        )

    def has_runtime_c_enrolment(self, user_id: int) -> bool:
        return self.find_enrolment_for_experience(user_id) is not None

    def complete_mission(
        self,
        *,
        user_id: int,
        mission_instance_id: str,
    ) -> EducationalExperienceSnapshot | None:
        """Complete a Runtime C mission and return the refreshed experience.

        Thin student-facing wrapper over the educational runtime engine.
        Does not change mission selection or pacing algorithms.
        """
        mid = (mission_instance_id or "").strip()
        if not mid:
            raise MissionInstanceNotFound("")
        self._runtime.complete_mission(
            user_id=user_id,
            mission_instance_id=mid,
        )
        return self.load_for_user(user_id, ensure_mission=True)

    def load_for_user(
        self,
        user_id: int,
        *,
        subject_code: str | None = None,
        mission_date: date | None = None,
        ensure_mission: bool = True,
    ) -> EducationalExperienceSnapshot | None:
        """Build the educational experience for a Runtime C student.

        Returns ``None`` when the user has no Runtime C enrolment
        (Runtime A remains the default path).
        """
        enrolment = self._resolve_enrolment(user_id, subject_code)
        if enrolment is None:
            return None

        day = mission_date or date.today()
        artefacts = self._artefacts.derive_active(enrolment.subject_code)
        if artefacts is None:
            logger.warning(
                "educational_experience_missing_artefacts subject=%s",
                enrolment.subject_code,
            )
            return None

        mission: MissionInstanceSnapshot | None = None
        enrolment_active = (
            enrolment.status == EnrolmentStatus.ACTIVE.value
        )
        if ensure_mission and enrolment_active:
            try:
                mission = self._runtime.generate_daily_mission(
                    user_id=user_id,
                    subject_code=enrolment.subject_code,
                    mission_date=day,
                )
            except SyllabusAlreadyComplete:
                mission = None
            except IllegalRuntimeState as exc:
                logger.info(
                    "educational_experience_mission_deferred: %s",
                    exc,
                )
                mission = None

        journey = self._runtime.get_journey(
            user_id=user_id,
            subject_code=enrolment.subject_code,
        )
        if mission is None:
            mission = journey.open_mission

        explanation = self._runtime.get_journey_explanation(
            user_id=user_id,
            subject_code=enrolment.subject_code,
        )
        pacing = self._runtime.project_pacing(
            user_id=user_id,
            subject_code=enrolment.subject_code,
            as_of=day,
        )

        return self._project(
            user_id=user_id,
            enrolment=enrolment,
            journey=journey,
            mission=mission,
            explanation=explanation,
            pacing=pacing,
            artefacts=artefacts,
        )

    def _resolve_enrolment(
        self,
        user_id: int,
        subject_code: str | None,
    ) -> RuntimeEnrolment | None:
        if subject_code:
            code = subject_code.strip().upper()
            active = (
                RuntimeEnrolment.query.filter_by(
                    user_id=user_id,
                    subject_code=code,
                    status=EnrolmentStatus.ACTIVE.value,
                )
                .order_by(RuntimeEnrolment.id.desc())
                .first()
            )
            if active is not None:
                return active
            return (
                RuntimeEnrolment.query.filter_by(
                    user_id=user_id,
                    subject_code=code,
                    status=EnrolmentStatus.COMPLETED.value,
                )
                .order_by(RuntimeEnrolment.id.desc())
                .first()
            )
        return self.find_enrolment_for_experience(user_id)

    def _project(
        self,
        *,
        user_id: int,
        enrolment: RuntimeEnrolment,
        journey: RuntimeJourneySnapshot,
        mission: MissionInstanceSnapshot | None,
        explanation: JourneyExplanationSnapshot,
        pacing: StudyPlanPacingSnapshot,
        artefacts: Any,
    ) -> EducationalExperienceSnapshot:
        progress = journey.progress
        topic_lookup = {
            str(t.get("topic_id")): t for t in (artefacts.topics or ())
        }
        objective_lookup = {
            str(o.get("objective_id")): o
            for o in (artefacts.objectives or ())
        }
        section_by_topic = _section_titles_by_topic(artefacts)

        current_id = progress.current_topic_id or ""
        current = topic_lookup.get(current_id) or {}
        topic_ids = list(progress.topic_ids)
        position_index = (
            topic_ids.index(current_id) + 1
            if current_id and current_id in topic_ids
            else max(1, len(progress.completed_topic_ids) + 1)
        )
        topic_count = max(1, len(topic_ids))
        topic_title = str(
            current.get("title") or current.get("text") or "Current topic"
        )
        topic_code = str(current.get("topic_code") or current.get("code") or "")
        section_title = section_by_topic.get(current_id, "")
        coverage_percent = int(round(float(progress.coverage_ratio) * 100))
        completed_count = len(progress.completed_topic_ids)

        position = CurriculumPositionSnapshot(
            subject_code=enrolment.subject_code,
            subject_title=_subject_title(artefacts, enrolment.subject_code),
            version_label=enrolment.version_label,
            section_title=section_title,
            topic_id=current_id,
            topic_code=topic_code,
            topic_title=topic_title,
            position_index=min(position_index, topic_count),
            topic_count=topic_count,
            position_label=(
                f"Topic {min(position_index, topic_count)} of {topic_count}"
                f" · {completed_count} complete"
            ),
            coverage_ratio=float(progress.coverage_ratio),
            coverage_percent=coverage_percent,
            journey_stage=str(progress.journey_stage or ""),
        )

        mission_edu = None
        if mission is not None:
            mission_edu = self._mission_education(
                mission,
                topic_lookup=topic_lookup,
                objective_lookup=objective_lookup,
            )

        journey_edu = self._journey_education(
            explanation=explanation,
            progress=progress,
            topic_lookup=topic_lookup,
            current_title=topic_title,
        )
        pacing_edu = self._pacing_education(
            pacing,
            exam_date=enrolment.exam_date,
        )

        examination_label = (
            f"{position.subject_title} ({enrolment.subject_code})"
            if position.subject_title
            else enrolment.subject_code
        )
        return EducationalExperienceSnapshot(
            student_id=str(user_id),
            enrolment_id=enrolment.enrolment_id,
            subject_code=enrolment.subject_code,
            curriculum_identity=enrolment.curriculum_identity,
            runtime_authority=journey.runtime_authority,
            is_runtime_c=True,
            greeting="Today's learning",
            examination_label=examination_label,
            curriculum_position=position,
            mission=mission_edu,
            journey=journey_edu,
            pacing=pacing_edu,
            syllabus_complete=bool(progress.syllabus_complete),
        )

    def _mission_education(
        self,
        mission: MissionInstanceSnapshot,
        *,
        topic_lookup: dict[str, dict],
        objective_lookup: dict[str, dict],
    ) -> MissionEducationSnapshot:
        quality = mission.quality
        topic = topic_lookup.get(mission.topic_id) or {}
        topic_title = str(
            topic.get("title") or topic.get("text") or mission.title
        )
        minutes = 0
        rationale = ""
        completion = ""
        objective_ids: tuple[str, ...] = ()
        prereq_ok = True
        prereq_label = "Prerequisites satisfied"
        explanation: dict[str, Any] = {}

        if isinstance(quality, MissionQualityEnvelope):
            minutes = int(quality.estimated_duration_minutes or 0)
            rationale = (quality.educational_rationale or "").strip()
            completion = (quality.completion_definition or "").strip()
            objective_ids = tuple(quality.objective_ids or ())
            explanation = dict(quality.explanation or {})
            prereq = dict(quality.prerequisite_validation or {})
            prereq_ok = bool(prereq.get("satisfied", True))
            missing = tuple(prereq.get("missing_prerequisite_ids") or ())
            if prereq_ok:
                prereq_label = "Prerequisites satisfied"
            elif missing:
                prereq_label = (
                    "Earlier topics still required before this mission"
                )
            else:
                prereq_label = "Prerequisite status needs review"

        learning_objectives = tuple(
            _objective_label(oid, objective_lookup) for oid in objective_ids
        )
        if not learning_objectives and objective_ids:
            learning_objectives = objective_ids

        why = str(
            explanation.get("why_this_mission")
            or explanation.get("why_this_plan")
            or rationale
            or ""
        ).strip()
        evidence_raw = explanation.get("supporting_evidence") or ()
        if isinstance(evidence_raw, str):
            evidence = (evidence_raw,)
        else:
            evidence = tuple(str(item) for item in evidence_raw if item)

        return MissionEducationSnapshot(
            mission_instance_id=mission.mission_instance_id,
            title=mission.title or topic_title,
            topic_code=mission.topic_code or str(topic.get("topic_code") or ""),
            topic_title=topic_title,
            learning_objectives=learning_objectives,
            estimated_duration_minutes=minutes,
            estimated_duration_label=_minutes_label(minutes),
            completion_definition=completion,
            educational_rationale=rationale or why,
            prerequisite_status_label=prereq_label,
            prerequisite_satisfied=prereq_ok,
            task_descriptions=tuple(mission.task_descriptions or ()),
            status=mission.status,
            why_this_mission=why,
            supporting_evidence=evidence,
            confidence_label=str(
                explanation.get("confidence_level") or ""
            ).strip(),
            expected_benefit=str(
                explanation.get("expected_benefit") or ""
            ).strip(),
            suggested_next_action=str(
                explanation.get("suggested_next_action") or ""
            ).strip(),
            review_point=str(explanation.get("review_point") or "").strip(),
            judgement=str(explanation.get("judgement") or "").strip(),
        )

    def _journey_education(
        self,
        *,
        explanation: JourneyExplanationSnapshot,
        progress: ProgressSnapshot,
        topic_lookup: dict[str, dict],
        current_title: str,
    ) -> JourneyEducationSnapshot:
        completed = tuple(
            (
                tid,
                str(
                    (topic_lookup.get(tid) or {}).get("title")
                    or (topic_lookup.get(tid) or {}).get("text")
                    or tid
                ),
            )
            for tid in progress.completed_topic_ids
        )
        upcoming = tuple(
            (
                tid,
                str(
                    (topic_lookup.get(tid) or {}).get("title")
                    or (topic_lookup.get(tid) or {}).get("text")
                    or tid
                ),
            )
            for tid in progress.incomplete_topic_ids
            if tid != progress.current_topic_id
        )
        return JourneyEducationSnapshot(
            why_today=(explanation.why_today or "").strip(),
            why_previous_complete=(
                explanation.why_previous_complete or ""
            ).strip(),
            unlocks_next=(explanation.unlocks_next or "").strip(),
            supporting_evidence=tuple(explanation.supporting_evidence or ()),
            current_topic_title=current_title,
            completed_topics=completed,
            upcoming_topics=upcoming,
        )

    def _pacing_education(
        self,
        pacing: StudyPlanPacingSnapshot,
        *,
        exam_date: date | None,
    ) -> PacingEducationSnapshot:
        exam_label = exam_date.isoformat() if exam_date else "No exam date set"
        if pacing.feasible is True:
            feasibility = "On track for first-pass coverage before the exam"
        elif pacing.feasible is False:
            shortfall = pacing.shortfall_minutes or 0
            feasibility = (
                f"Not enough study time before the exam "
                f"(about {shortfall} minutes short)"
            )
        else:
            feasibility = "Pacing needs an exam date to judge feasibility"

        summary_parts = [
            f"First pass: {_minutes_label(pacing.first_pass_minutes)}",
            f"Revision: {_minutes_label(pacing.revision_minutes)}",
            f"Total planned: {_minutes_label(pacing.total_required_minutes)}",
        ]
        return PacingEducationSnapshot(
            exam_date=exam_date,
            exam_date_label=exam_label,
            exam_date_aware=bool(pacing.exam_date_aware),
            first_pass_minutes=int(pacing.first_pass_minutes or 0),
            revision_minutes=int(pacing.revision_minutes or 0),
            total_required_minutes=int(pacing.total_required_minutes or 0),
            feasible=pacing.feasible,
            shortfall_minutes=pacing.shortfall_minutes,
            pacing_summary=" · ".join(summary_parts),
            feasibility_label=feasibility,
        )


def _subject_title(artefacts: Any, subject_code: str) -> str:
    meta = dict(artefacts.metadata or ())
    for key in ("subject_title", "title", "name"):
        if meta.get(key):
            return str(meta[key])
    sections = artefacts.sections or ()
    if sections:
        first = sections[0]
        if isinstance(first, dict) and first.get("text"):
            return f"{subject_code} — {first['text']}"
    return subject_code


def _section_titles_by_topic(artefacts: Any) -> dict[str, str]:
    """Map topic_id → parent section title from journey sections when present."""
    mapping: dict[str, str] = {}
    journey = getattr(artefacts, "journey", None)
    sections = ()
    if journey is not None and getattr(journey, "sections", None):
        sections = journey.sections
    elif artefacts.sections:
        sections = artefacts.sections

    for section in sections:
        if not isinstance(section, dict):
            continue
        section_title = str(
            section.get("title") or section.get("text") or ""
        ).strip()
        for topic in section.get("topics") or ():
            if isinstance(topic, dict):
                tid = str(topic.get("topic_id") or "")
                if tid:
                    mapping[tid] = section_title
        # Flat CMP-style: topics may list parent_ref separately
    if mapping:
        return mapping

    # Fall back: topics with parent section entry in artefacts.sections
    section_titles = {
        str(s.get("entry_id") or s.get("section_id") or ""): str(
            s.get("text") or s.get("title") or ""
        )
        for s in (artefacts.sections or ())
        if isinstance(s, dict)
        and str(s.get("entry_type") or s.get("kind") or "").lower()
        in {"section", ""}
    }
    for topic in artefacts.topics or ():
        if not isinstance(topic, dict):
            continue
        tid = str(topic.get("topic_id") or "")
        parent = str(
            topic.get("section_id")
            or topic.get("parent_ref")
            or topic.get("parent_id")
            or ""
        )
        if tid and parent in section_titles:
            mapping[tid] = section_titles[parent]
    return mapping


def _objective_label(objective_id: str, lookup: dict[str, dict]) -> str:
    obj = lookup.get(objective_id) or {}
    code = str(obj.get("code") or obj.get("number") or "").strip()
    text = str(obj.get("text") or obj.get("title") or "").strip()
    if code and text:
        return f"{code} — {text}"
    if text:
        return text
    if code:
        return code
    return objective_id


def _minutes_label(minutes: int) -> str:
    mins = max(0, int(minutes or 0))
    if mins <= 0:
        return ""
    if mins < 60:
        return f"{mins} min"
    hours, rem = divmod(mins, 60)
    if rem == 0:
        return f"{hours} h" if hours != 1 else "1 h"
    return f"{hours} h {rem} min"
