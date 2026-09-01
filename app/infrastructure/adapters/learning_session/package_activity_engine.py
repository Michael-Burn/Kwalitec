"""Package-derived activity engine for Session Experience (LXP-004A).

Implements the opaque ``*_opaque`` activity engine contract used by
SessionActivityAdapter. Builds a continuous Read → Worked Example → Practice
sequence from published package artefacts. Never scores mastery or writes Twin.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from app.application.learning_session.educational_flow import (
    EducationalActivitySpec,
    EducationalSessionSubstance,
    EducationalStage,
    stage_label,
)
from app.application.learning_session.scoreable_practice import (
    ScoreablePracticeItem,
    choice_parts,
    score_practice_response,
)
from app.application.learning_session.substance_planner import (
    EducationalSubstancePlanner,
)
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.session.store import SessionDocumentStore


class PackageActivityEngine:
    """Opaque activity engine backed by package-derived educational substance."""

    ENGINE_ID = "package_activity_engine"
    ENGINE_VERSION = "1.0.0"
    NS_SEQUENCE = "activity.sequence"
    NS_CURRENT = "activity.current"
    NS_RESPONSES = "activity.responses"

    def __init__(
        self,
        *,
        store: SessionDocumentStore | None = None,
        persistence: LearningSessionPersistenceAdapter | None = None,
        planner: EducationalSubstancePlanner | None = None,
    ) -> None:
        self._store = store or SessionDocumentStore()
        self._persistence = persistence or LearningSessionPersistenceAdapter(
            store=self._store
        )
        self._planner = planner or EducationalSubstancePlanner()

    def get_current_activity_opaque(
        self,
        student_id: str,
        *,
        session_id: str,
        topic_title: str = "",
    ) -> dict[str, Any] | None:
        seq = self._ensure_sequence(
            student_id, session_id=session_id, topic_title=topic_title
        )
        if seq is None:
            return None
        index = int(seq.get("index") or 1)
        activities = list(seq.get("activities") or ())
        total = len(activities)
        if total == 0 or index > total:
            return None
        item = dict(activities[index - 1])
        return self._to_opaque(
            student_id=student_id,
            session_id=session_id,
            item=item,
            index=index,
            total=total,
            topic_title=str(seq.get("topic_title") or topic_title),
        )

    def submit_response_opaque(
        self,
        student_id: str,
        *,
        session_id: str,
        activity_id: str,
        response: str,
        topic_title: str = "",
    ) -> dict[str, Any]:
        seq = self._ensure_sequence(
            student_id, session_id=session_id, topic_title=topic_title
        )
        if seq is None:
            return {
                "activity_id": activity_id,
                "explanation": "Continue when you are ready.",
                "phase": "explained",
                "authority": self.ENGINE_ID,
            }
        index = int(seq.get("index") or 1)
        activities = list(seq.get("activities") or ())
        total = max(1, len(activities))
        item = dict(activities[index - 1]) if activities else {}
        stage = str(item.get("stage") or EducationalStage.PRACTICE.value)
        topic = str(seq.get("topic_title") or topic_title or "today's topic")
        scoreable = ScoreablePracticeItem.from_opaque(item.get("scoreable"))
        score = score_practice_response(scoreable, response)
        explanation = _explanation_for_stage(
            stage,
            topic=topic,
            response=response,
            score=score,
        )
        key = self._key(student_id, session_id)
        responses = self._store.get(self.NS_RESPONSES, key) or {
            "student_id": student_id,
            "session_id": session_id,
            "items": [],
        }
        items = list(responses.get("items") or [])
        items.append(
            {
                "activity_id": activity_id,
                "stage": stage,
                "response": (response or "").strip(),
                "scored_correct": score.scored_correct,
                "item_id": score.item_id,
                "emit_structured": score.emit_structured,
                "score": score.to_opaque(),
                # Stable analytics id for selected distractor (not student-facing).
                "selected_misconception_tag": score.selected_misconception_tag,
            }
        )
        responses["items"] = items
        self._store.save(self.NS_RESPONSES, key, responses)

        # Mark checklist items for completed stages.
        self._mark_checklist(session_id=session_id, student_id=student_id, stage=stage)

        is_final = index >= total
        next_label = str(
            item.get("next_action_label")
            or score.next_action
            or ("Continue to Reflection" if is_final else "Continue")
        )
        result: dict[str, Any] = {
            "activity_id": activity_id,
            "explanation": explanation,
            "phase": "explained",
            "activity_index": index,
            "activities_total": total,
            "activity_type": stage,
            "stage": stage,
            "stage_label": stage_label(stage),
            "topic_title": topic,
            "next_action_label": next_label,
            "authority": self.ENGINE_ID,
            "substance": "package",
            "scored_correct": score.scored_correct,
            "feedback_outcome": score.feedback_outcome,
            "feedback_explanation": score.explanation or explanation,
            "model_answer": score.model_answer,
            "common_mistake": score.common_mistake,
            "next_action": score.next_action or next_label,
            # Presentation only: echo for locked "what happened" feedback.
            "submitted_response": (response or "").strip(),
            "response_type": score.response_type,
            "emit_structured": score.emit_structured,
            "score_payload": {
                "item_id": score.item_id,
                "response_type": score.response_type,
                "marks_awarded": score.marks_awarded,
                "marks_available": score.marks_available,
                "accuracy": (
                    (score.marks_awarded / score.marks_available)
                    if score.scored and score.marks_available
                    else None
                ),
            },
        }
        if scoreable is not None and scoreable.choices:
            # Learner UI: id + label only (never surface misconception_tag).
            result["choices"] = [
                {"id": cid, "label": label}
                for cid, label, _tag in (choice_parts(c) for c in scoreable.choices)
            ]
        return result

    def advance_activity_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        seq = self._ensure_sequence(student_id, session_id=session_id)
        if seq is None:
            return None
        index = int(seq.get("index") or 1)
        activities = list(seq.get("activities") or ())
        total = len(activities)
        if index >= total:
            seq["index"] = total + 1
            seq["completed"] = total
            self._store.save(
                self.NS_SEQUENCE, self._key(student_id, session_id), seq
            )
            return None
        seq["index"] = index + 1
        seq["completed"] = index
        self._store.save(self.NS_SEQUENCE, self._key(student_id, session_id), seq)
        return self.get_current_activity_opaque(student_id, session_id=session_id)

    def get_activity_progress_opaque(
        self, student_id: str, *, session_id: str
    ) -> dict[str, Any] | None:
        seq = self._ensure_sequence(student_id, session_id=session_id)
        if seq is None:
            return None
        completed = int(seq.get("completed") or 0)
        total = max(1, len(seq.get("activities") or ()))
        remaining = max(0, total - completed)
        topic = str(seq.get("topic_title") or "Today's topic")
        return {
            "student_id": student_id,
            "session_id": session_id,
            "activities_completed": completed,
            "activities_remaining": remaining,
            "activities_total": total,
            "estimated_remaining_minutes": remaining * 8,
            "current_topic": topic,
            "overall_progress": (completed / total) if total else 0.0,
            "authority": self.ENGINE_ID,
            "substance": "package",
        }

    def provision_sequence(
        self,
        student_id: str,
        *,
        session_id: str,
        substance: EducationalSessionSubstance,
    ) -> dict[str, Any]:
        """Persist a planned substance sequence for the session."""
        document = self._sequence_document(
            student_id=student_id,
            session_id=session_id,
            substance=substance,
        )
        self._store.save(
            self.NS_SEQUENCE, self._key(student_id, session_id), document
        )
        return deepcopy(document)

    def _ensure_sequence(
        self,
        student_id: str,
        *,
        session_id: str,
        topic_title: str = "",
    ) -> dict[str, Any] | None:
        key = self._key(student_id, session_id)
        existing = self._store.get(self.NS_SEQUENCE, key)
        if (
            isinstance(existing, dict)
            and existing.get("activities")
            and existing.get("substance") == "package"
        ):
            return deepcopy(existing)

        record = self._persistence.load(session_id=session_id) or {}
        owner = str(record.get("student_id") or "").strip()
        if owner and owner != student_id.strip():
            return None

        curriculum_identity = str(record.get("curriculum_identity") or "")
        topic_id = str(record.get("topic_id") or "")
        title = (
            topic_title
            or str(record.get("topic_title") or "")
            or "Today's topic"
        ).strip()

        handle = self._persistence.load_handle(session_id=session_id)
        objective_ids: tuple[str, ...] = ()
        raw_ids = record.get("objective_ids") or ()
        if raw_ids:
            objective_ids = tuple(
                str(oid).strip() for oid in raw_ids if str(oid).strip()
            )
        elif handle is not None and handle.plan is not None:
            objective_ids = tuple(handle.plan.objective_ids)

        minutes = None
        try:
            minutes = int(record.get("estimated_minutes") or 0) or None
        except (TypeError, ValueError):
            minutes = None

        substance = self._planner.plan_for_topic(
            curriculum_identity=curriculum_identity,
            topic_id=topic_id,
            topic_title=title,
            objective_ids=objective_ids,
            session_minutes=minutes,
        )
        if substance is None:
            return None
        return self.provision_sequence(
            student_id, session_id=session_id, substance=substance
        )

    def _sequence_document(
        self,
        *,
        student_id: str,
        session_id: str,
        substance: EducationalSessionSubstance,
    ) -> dict[str, Any]:
        activities = [
            _spec_to_sequence_item(spec, index=i + 1, total=len(substance.activities))
            for i, spec in enumerate(substance.activities)
        ]
        return {
            "student_id": student_id,
            "session_id": session_id,
            "index": 1,
            "completed": 0,
            "total": len(activities),
            "topic_title": substance.topic_title,
            "topic_id": substance.topic_id,
            "curriculum_identity": substance.curriculum_identity,
            "educational_package_id": _package_id_from_substance(substance),
            "learning_objectives": [
                {
                    "objective_id": obj.objective_id,
                    "code": obj.code,
                    "text": obj.text,
                }
                for obj in substance.learning_objectives
            ],
            "activities": activities,
            "flow": [
                EducationalStage.LEARNING_OBJECTIVES.value,
                *(a["stage"] for a in activities),
                EducationalStage.REFLECTION.value,
                EducationalStage.READY_TO_FINISH.value,
            ],
            "authority": self.ENGINE_ID,
            "substance": "package",
            "source": substance.source,
        }

    def _mark_checklist(
        self, *, session_id: str, student_id: str, stage: str
    ) -> None:
        mapping = {
            EducationalStage.READ.value: "read",
            EducationalStage.WORKED_EXAMPLE.value: "examples",
            EducationalStage.PRACTICE.value: "practice",
        }
        item_id = mapping.get(stage)
        if not item_id:
            return
        try:
            self._persistence.update_checklist_item(
                session_id=session_id,
                student_id=student_id,
                item_id=item_id,
                done=True,
            )
        except Exception:  # noqa: BLE001 — checklist sync is best-effort
            return

    def _to_opaque(
        self,
        *,
        student_id: str,
        session_id: str,
        item: dict[str, Any],
        index: int,
        total: int,
        topic_title: str,
    ) -> dict[str, Any]:
        stage = str(item.get("stage") or EducationalStage.PRACTICE.value)
        is_final = index >= total
        next_label = str(
            item.get("next_action_label")
            or ("Continue to Reflection" if is_final else "Continue")
        )
        return {
            "student_id": student_id,
            "session_id": session_id,
            "activity_id": str(item.get("activity_id") or f"act-{index}"),
            "question": str(item.get("prompt") or item.get("question") or ""),
            "context": str(item.get("body") or item.get("context") or ""),
            "supporting_material": str(item.get("supporting_material") or ""),
            "hints": tuple(item.get("hints") or ()),
            "answer_prompt": str(item.get("answer_prompt") or "Your notes"),
            "activity_index": index,
            "activities_total": total,
            "topic_title": topic_title,
            "phase": "ready",
            "activity_type": stage,
            "stage": stage,
            "stage_label": stage_label(stage),
            "title": str(item.get("title") or ""),
            "learning_objectives": list(item.get("learning_objectives") or []),
            "syllabus_refs": tuple(item.get("syllabus_refs") or ()),
            "next_action_label": next_label,
            "requires_response": bool(item.get("requires_response", True)),
            "authority": self.ENGINE_ID,
            "substance": "package",
            "response_type": str(item.get("response_type") or ""),
            "choices": list(item.get("choices") or []),
            "scoreable": bool(item.get("scoreable")),
        }

    @staticmethod
    def _key(student_id: str, session_id: str) -> str:
        return f"{student_id.strip()}::{session_id.strip()}"


def _spec_to_sequence_item(
    spec: EducationalActivitySpec, *, index: int, total: int
) -> dict[str, Any]:
    scoreable = spec.scoreable
    meta = dict(spec.metadata or ())
    item: dict[str, Any] = {
        "activity_id": spec.activity_id,
        "stage": spec.stage.value,
        "stage_label": spec.stage_label,
        "title": spec.title,
        "prompt": spec.prompt,
        "question": spec.prompt,
        "body": spec.body,
        "context": spec.body,
        "supporting_material": spec.supporting_material,
        "hints": list(spec.hints),
        "answer_prompt": spec.answer_prompt,
        "requires_response": spec.requires_response,
        "objective_ids": list(spec.objective_ids),
        "syllabus_refs": list(spec.syllabus_refs),
        "next_action_label": meta.get(
            "next_action_label",
            "Continue to Reflection" if index >= total else "Continue",
        ),
        "activity_index": index,
        "activities_total": total,
    }
    package_id = str(meta.get("package_id") or "").strip()
    if package_id:
        item["package_id"] = package_id
    if scoreable is not None:
        # Server-side scoring retains the full key; learner opaque omits it.
        item["scoreable"] = scoreable.to_opaque()
        item["response_type"] = scoreable.response_type.value
        # Learner-facing choice list omits misconception_tag.
        item["choices"] = [
            {"id": cid, "label": label}
            for cid, label, _tag in (choice_parts(c) for c in scoreable.choices)
        ]
        item["item_id"] = scoreable.item_id
    return item


def _package_id_from_substance(substance: EducationalSessionSubstance) -> str:
    """Recover approved educational_package_id from substance metadata / LO ids."""
    for act in substance.activities or ():
        meta = dict(getattr(act, "metadata", ()) or ())
        pid = str(meta.get("package_id") or "").strip()
        if pid:
            return pid
    for obj in substance.learning_objectives or ():
        oid = str(getattr(obj, "objective_id", "") or "").strip()
        if ":lo" in oid:
            return oid.split(":lo", 1)[0].strip()
        if ":sc-" in oid:
            return oid.split(":sc-", 1)[0].strip()
    return ""


def _explanation_for_stage(
    stage: str,
    *,
    topic: str,
    response: str,
    score=None,
) -> str:
    if score is not None and getattr(score, "scored", False):
        parts = [score.feedback_outcome]
        if score.explanation:
            parts.append(score.explanation)
        return " ".join(parts)
    note = (response or "").strip()
    preview = f" You noted: “{note[:120]}”." if note else ""
    if stage == EducationalStage.READ.value:
        return (
            f"Good — keep that idea in mind as you move into the worked example "
            f"for {topic}.{preview}"
        )
    if stage == EducationalStage.WORKED_EXAMPLE.value:
        return (
            f"Carry that method step into practice on {topic}. "
            f"Compare your next answer with the worked approach.{preview}"
        )
    return (
        f"Compare your reasoning with the worked example for {topic}. "
        f"Note one idea you would keep and one you would adjust.{preview}"
    )
