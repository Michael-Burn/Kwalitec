"""Persistence for Intelligent Tutor conversations (TUTOR-001).

Stores sessions, messages, explanations, and optional feedback only.
Does not duplicate Student Digital Twin mastery / gap / recommendation rows.
"""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from typing import Any

from app.domain.intelligent_tutor.conversation_memory import ConversationMemory
from app.domain.intelligent_tutor.explanation import Explanation, ExplanationKind
from app.domain.intelligent_tutor.tutor_context import TutorContext
from app.domain.intelligent_tutor.tutor_question import TutorQuestion, TutorQuestionKind
from app.domain.intelligent_tutor.tutor_response import TutorResponse
from app.domain.intelligent_tutor.tutor_session import TutorSession, TutorSessionStatus
from app.extensions import db
from app.models.intelligent_tutor import (
    TutorExplanationRow,
    TutorFeedbackRow,
    TutorMessageRow,
    TutorSessionRow,
)


def _dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)


def _loads(raw: str | None, default: Any) -> Any:
    if not raw:
        return default
    return json.loads(raw)


class IntelligentTutorPersistenceService:
    """Load and persist Tutor conversation aggregates."""

    def save_session(self, session: TutorSession) -> TutorSessionRow:
        row = TutorSessionRow.query.filter_by(session_id=session.session_id).first()
        memory = session.memory
        payload = {
            "session_id": session.session_id,
            "twin_id": session.twin_id,
            "student_id": session.student_id,
            "status": session.status.value,
            "title": session.title or "",
            "active_mission_id": session.active_mission_id or "",
            "memory_json": _dumps(
                {
                    "memory_id": memory.memory_id if memory else "",
                    "referenced_concept_ids": list(
                        memory.referenced_concept_ids if memory else ()
                    ),
                    "learner_state_summary": (
                        memory.learner_state_summary if memory else ""
                    ),
                    "turn_count": memory.turn_count if memory else 0,
                    "last_question_kind": (
                        memory.last_question_kind if memory else ""
                    ),
                    "last_response_id": memory.last_response_id if memory else "",
                }
            ),
            "version": session.version,
            "created_at": session.created_at,
            "updated_at": session.updated_at,
        }
        if row is None:
            row = TutorSessionRow(**payload)
            db.session.add(row)
        else:
            for key, value in payload.items():
                setattr(row, key, value)
        return row

    def save_turn(
        self,
        *,
        session: TutorSession,
        question: TutorQuestion,
        response: TutorResponse,
        context: TutorContext,
        evidence_ids: tuple[str, ...] = (),
    ) -> None:
        """Persist one question + response + explanation for a session."""
        asked_at = question.asked_at or datetime.now(UTC).replace(tzinfo=None)
        db.session.add(
            TutorMessageRow(
                message_id=question.question_id,
                session_id=session.session_id,
                twin_id=session.twin_id,
                role="student",
                kind=question.kind.value,
                body=question.text,
                concept_id=question.concept_id or "",
                mission_id=question.mission_id or "",
                context_id=context.context_id,
                evidence_json=_dumps(list(evidence_ids)),
                metadata_json=_dumps(
                    {
                        "question_id": question.question_id,
                        "context": {
                            "primary_concept_id": context.primary_concept_id,
                            "reasoning_run_id": context.reasoning_run_id,
                            "active_mission_id": context.active_mission_id,
                        },
                    }
                ),
                created_at=asked_at,
            )
        )
        created = response.created_at or asked_at
        db.session.add(
            TutorMessageRow(
                message_id=response.response_id,
                session_id=session.session_id,
                twin_id=session.twin_id,
                role="tutor",
                kind=response.explanation.kind.value,
                body=response.body,
                concept_id=(
                    response.explanation.concept_ids[0]
                    if response.explanation.concept_ids
                    else ""
                ),
                mission_id=response.explanation.mission_id or "",
                context_id=response.context_id or context.context_id,
                evidence_json=_dumps(list(response.supporting_evidence_ids)),
                metadata_json=_dumps(
                    {
                        "question_id": response.question_id,
                        "generation_backend": response.generation_backend,
                        "suggested_next_action": response.suggested_next_action,
                        "related_concepts": list(response.related_concepts),
                        "recovery_guidance": response.recovery_guidance,
                        "reflection_prompt": response.reflection_prompt,
                        "evidence_summaries": list(response.evidence_summaries),
                    }
                ),
                created_at=created,
            )
        )
        exp = response.explanation
        db.session.add(
            TutorExplanationRow(
                explanation_id=exp.explanation_id,
                session_id=session.session_id,
                twin_id=session.twin_id,
                response_id=response.response_id,
                kind=exp.kind.value,
                summary=exp.summary,
                detail=exp.detail,
                evidence_json=_dumps(list(exp.evidence_ids)),
                concept_ids_json=_dumps(list(exp.concept_ids)),
                reasoning_run_id=exp.reasoning_run_id or "",
                mission_id=exp.mission_id or "",
                created_at=exp.created_at or created,
            )
        )

    def save_feedback(
        self,
        *,
        twin_id: str,
        session_id: str,
        response_id: str,
        rating: int,
        comment: str = "",
        helpful: bool | None = None,
    ) -> TutorFeedbackRow:
        row = TutorFeedbackRow(
            feedback_id=f"tfb-{uuid.uuid4().hex[:12]}",
            twin_id=twin_id,
            session_id=session_id,
            response_id=response_id,
            rating=int(rating),
            comment=comment or "",
            helpful=helpful,
            created_at=datetime.now(UTC).replace(tzinfo=None),
        )
        db.session.add(row)
        return row

    def load_session(self, session_id: str) -> TutorSession | None:
        row = TutorSessionRow.query.filter_by(session_id=session_id).first()
        if row is None:
            return None
        return self._session_from_row(row)

    def list_sessions(self, twin_id: str) -> list[TutorSession]:
        rows = (
            TutorSessionRow.query.filter_by(twin_id=twin_id)
            .order_by(TutorSessionRow.updated_at.desc())
            .all()
        )
        return [self._session_from_row(row) for row in rows]

    def list_messages(self, session_id: str) -> list[dict[str, Any]]:
        rows = (
            TutorMessageRow.query.filter_by(session_id=session_id)
            .order_by(TutorMessageRow.created_at.asc())
            .all()
        )
        return [
            {
                "message_id": r.message_id,
                "role": r.role,
                "kind": r.kind,
                "body": r.body,
                "concept_id": r.concept_id,
                "mission_id": r.mission_id,
                "context_id": r.context_id,
                "evidence_ids": _loads(r.evidence_json, []),
                "metadata": _loads(r.metadata_json, {}),
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]

    def list_explanations(self, twin_id: str) -> list[dict[str, Any]]:
        rows = (
            TutorExplanationRow.query.filter_by(twin_id=twin_id)
            .order_by(TutorExplanationRow.created_at.desc())
            .all()
        )
        return [
            {
                "explanation_id": r.explanation_id,
                "session_id": r.session_id,
                "response_id": r.response_id,
                "kind": r.kind,
                "summary": r.summary,
                "detail": r.detail,
                "evidence_ids": _loads(r.evidence_json, []),
                "concept_ids": _loads(r.concept_ids_json, []),
                "reasoning_run_id": r.reasoning_run_id,
                "mission_id": r.mission_id,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]

    def list_feedback(self, twin_id: str) -> list[dict[str, Any]]:
        rows = (
            TutorFeedbackRow.query.filter_by(twin_id=twin_id)
            .order_by(TutorFeedbackRow.created_at.desc())
            .all()
        )
        return [
            {
                "feedback_id": r.feedback_id,
                "session_id": r.session_id,
                "response_id": r.response_id,
                "rating": r.rating,
                "comment": r.comment,
                "helpful": r.helpful,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]

    def _session_from_row(self, row: TutorSessionRow) -> TutorSession:
        mem = _loads(row.memory_json, {})
        memory = ConversationMemory(
            memory_id=mem.get("memory_id") or f"mem-{row.session_id}",
            session_id=row.session_id,
            twin_id=row.twin_id,
            referenced_concept_ids=tuple(mem.get("referenced_concept_ids") or ()),
            active_mission_id=row.active_mission_id or "",
            learner_state_summary=mem.get("learner_state_summary") or "",
            turn_count=int(mem.get("turn_count") or 0),
            last_question_kind=mem.get("last_question_kind") or "",
            last_response_id=mem.get("last_response_id") or "",
            updated_at=row.updated_at,
        )
        messages = (
            TutorMessageRow.query.filter_by(session_id=row.session_id)
            .order_by(TutorMessageRow.created_at.asc())
            .all()
        )
        questions: list[TutorQuestion] = []
        responses: list[TutorResponse] = []
        explanations: list[Explanation] = []

        by_id = {m.message_id: m for m in messages}
        for msg in messages:
            if msg.role == "student":
                questions.append(
                    TutorQuestion(
                        question_id=msg.message_id,
                        twin_id=msg.twin_id,
                        text=msg.body,
                        kind=TutorQuestionKind(msg.kind)
                        if msg.kind in TutorQuestionKind._value2member_map_
                        else TutorQuestionKind.GENERAL,
                        concept_id=msg.concept_id or "",
                        mission_id=msg.mission_id or "",
                        session_id=msg.session_id,
                        asked_at=msg.created_at,
                    )
                )
            elif msg.role == "tutor":
                meta = _loads(msg.metadata_json, {})
                exp_row = TutorExplanationRow.query.filter_by(
                    response_id=msg.message_id
                ).first()
                if exp_row is not None:
                    explanation = Explanation(
                        explanation_id=exp_row.explanation_id,
                        twin_id=exp_row.twin_id,
                        kind=ExplanationKind(exp_row.kind)
                        if exp_row.kind in ExplanationKind._value2member_map_
                        else ExplanationKind.GENERAL,
                        summary=exp_row.summary,
                        detail=exp_row.detail,
                        evidence_ids=tuple(_loads(exp_row.evidence_json, [])),
                        concept_ids=tuple(_loads(exp_row.concept_ids_json, [])),
                        reasoning_run_id=exp_row.reasoning_run_id or "",
                        mission_id=exp_row.mission_id or "",
                        created_at=exp_row.created_at,
                    )
                else:
                    explanation = Explanation(
                        explanation_id=f"exp-{msg.message_id}",
                        twin_id=msg.twin_id,
                        kind=ExplanationKind.GENERAL,
                        summary=msg.body[:160],
                        detail=msg.body,
                        evidence_ids=tuple(_loads(msg.evidence_json, [])),
                        created_at=msg.created_at,
                    )
                explanations.append(explanation)
                qid = meta.get("question_id") or ""
                # Ensure linked student message exists in map when present.
                _ = by_id.get(qid)
                responses.append(
                    TutorResponse(
                        response_id=msg.message_id,
                        session_id=msg.session_id,
                        twin_id=msg.twin_id,
                        question_id=qid,
                        body=msg.body,
                        explanation=explanation,
                        supporting_evidence_ids=tuple(
                            _loads(msg.evidence_json, [])
                        ),
                        suggested_next_action=meta.get("suggested_next_action") or "",
                        related_concepts=tuple(meta.get("related_concepts") or ()),
                        recovery_guidance=meta.get("recovery_guidance") or "",
                        reflection_prompt=meta.get("reflection_prompt") or "",
                        evidence_summaries=tuple(
                            meta.get("evidence_summaries") or ()
                        ),
                        context_id=msg.context_id or "",
                        generation_backend=meta.get("generation_backend")
                        or "deterministic_placeholder",
                        created_at=msg.created_at,
                    )
                )

        return TutorSession(
            session_id=row.session_id,
            twin_id=row.twin_id,
            student_id=row.student_id,
            status=TutorSessionStatus(row.status),
            title=row.title or "",
            active_mission_id=row.active_mission_id or "",
            memory=memory,
            questions=tuple(questions),
            responses=tuple(responses),
            explanations=tuple(explanations),
            created_at=row.created_at,
            updated_at=row.updated_at,
            version=row.version or 1,
        )
