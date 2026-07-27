"""IntelligentTutorService — evidence-backed tutoring orchestration.

Pipeline (never bypassed):
  Student Question
    → Student Digital Twin
    → Educational Reasoning decisions (already on Twin)
    → Learning Graph
    → Curriculum Retrieval
    → Evidence Assembly
    → Explanation Builder
    → TutorGenerationPort
    → Tutor Response

The Tutor explains decisions. It does not create them.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from app.application.adaptive_mission.adaptive_mission_service import (
    AdaptiveMissionService,
)
from app.application.assessment_pipeline.assessment_pipeline_service import (
    AssessmentPipelineService,
)
from app.application.curriculum_retrieval.curriculum_retrieval_service import (
    CurriculumRetrievalService,
)
from app.application.intelligent_tutor.persistence import (
    IntelligentTutorPersistenceService,
)
from app.application.intelligent_tutor.ports.deterministic_tutor_generation import (
    DeterministicTutorGeneration,
)
from app.application.intelligent_tutor.ports.tutor_generation_port import (
    TutorGenerationPort,
    TutorGenerationRequest,
)
from app.application.learning_graph.learning_graph_service import LearningGraphService
from app.application.learning_graph.learning_graph_traversal_service import (
    LearningGraphTraversalService,
)
from app.application.student_digital_twin.student_digital_twin_service import (
    StudentDigitalTwinService,
)
from app.domain.curriculum_retrieval.profile import RetrievalProfile
from app.domain.curriculum_retrieval.query import RetrievalQuery
from app.domain.intelligent_tutor.conversation_memory import (
    ConversationMemory,
    update_conversation_memory,
)
from app.domain.intelligent_tutor.response_builder import build_response_blueprint
from app.domain.intelligent_tutor.response_evidence import assemble_evidence
from app.domain.intelligent_tutor.tutor_context import TutorContext
from app.domain.intelligent_tutor.tutor_question import (
    TutorQuestion,
    TutorQuestionKind,
    classify_question,
)
from app.domain.intelligent_tutor.tutor_response import TutorResponse
from app.domain.intelligent_tutor.tutor_session import TutorSession, TutorSessionStatus
from app.domain.learning_graph.learning_graph import LearningGraph
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin
from app.extensions import db


class IntelligentTutorService:
    """Public facade for the Evidence-Backed Intelligent Tutor.

    Educational reasoning is never performed here. Twin / Reasoning / Graph /
    Mission / Assessment / Retrieval outputs are consumed and explained.
    """

    ENGINE_VERSION = "tutor001.intelligent_tutor_v1"

    def __init__(
        self,
        *,
        twins: StudentDigitalTwinService | None = None,
        graphs: LearningGraphService | None = None,
        traversal: LearningGraphTraversalService | None = None,
        retrieval: CurriculumRetrievalService | None = None,
        missions: AdaptiveMissionService | None = None,
        assessments: AssessmentPipelineService | None = None,
        generation: TutorGenerationPort | None = None,
        persistence: IntelligentTutorPersistenceService | None = None,
    ) -> None:
        self._twins = twins or StudentDigitalTwinService()
        self._graphs = graphs or LearningGraphService()
        self._traversal = traversal or LearningGraphTraversalService()
        self._retrieval = retrieval
        self._missions = missions or AdaptiveMissionService()
        self._assessments = assessments or AssessmentPipelineService()
        self._generation = generation or DeterministicTutorGeneration()
        self._persistence = persistence or IntelligentTutorPersistenceService()

    # ------------------------------------------------------------------
    # Session lifecycle
    # ------------------------------------------------------------------

    def open_session(
        self,
        twin_id: str,
        *,
        title: str = "",
        persist: bool = True,
        created_at: datetime | None = None,
    ) -> TutorSession:
        """Open a new Tutor conversation for a Twin."""
        twin = self._require_twin(twin_id)
        when = created_at or datetime.now(UTC).replace(tzinfo=None)
        session_id = f"tutor-sess-{uuid.uuid4().hex[:12]}"
        mission = self._missions.get_active(twin_id)
        memory = ConversationMemory(
            memory_id=f"mem-{session_id}",
            session_id=session_id,
            twin_id=twin_id,
            active_mission_id=mission.mission_id if mission else "",
            learner_state_summary=self._learning_state_summary(twin),
            updated_at=when,
        )
        session = TutorSession(
            session_id=session_id,
            twin_id=twin_id,
            student_id=twin.student.student_id,
            status=TutorSessionStatus.ACTIVE,
            title=title or "Tutor conversation",
            active_mission_id=memory.active_mission_id,
            memory=memory,
            created_at=when,
            updated_at=when,
        )
        if persist:
            self._persistence.save_session(session)
            db.session.commit()
        return session

    def get_session(self, session_id: str) -> TutorSession | None:
        return self._persistence.load_session(session_id)

    def list_sessions(self, twin_id: str) -> list[TutorSession]:
        return self._persistence.list_sessions(twin_id)

    def close_session(
        self,
        session_id: str,
        *,
        persist: bool = True,
    ) -> TutorSession:
        session = self._persistence.load_session(session_id)
        if session is None:
            raise ValueError(f"Tutor session {session_id!r} not found")
        closed = session.close()
        if persist:
            self._persistence.save_session(closed)
            db.session.commit()
        return closed

    # ------------------------------------------------------------------
    # Ask pipeline
    # ------------------------------------------------------------------

    def ask(
        self,
        twin_id: str,
        text: str,
        *,
        session_id: str | None = None,
        concept_id: str = "",
        kind: TutorQuestionKind | str | None = None,
        persist: bool = True,
        enrich_evidence: bool = True,
        asked_at: datetime | None = None,
    ) -> TutorResponse:
        """Run the full Tutor pipeline for one student question."""
        twin = self._require_twin(twin_id)
        when = asked_at or datetime.now(UTC).replace(tzinfo=None)

        session = None
        if session_id:
            session = self._persistence.load_session(session_id)
            if session is None:
                raise ValueError(f"Tutor session {session_id!r} not found")
            if session.twin_id != twin_id:
                raise ValueError("session twin_id mismatch")
        else:
            session = self.open_session(twin_id, persist=persist, created_at=when)

        resolved_kind = (
            TutorQuestionKind(str(kind))
            if kind is not None
            else classify_question(text)
        )
        question = TutorQuestion(
            question_id=f"tq-{uuid.uuid4().hex[:12]}",
            twin_id=twin_id,
            text=text,
            kind=resolved_kind,
            concept_id=concept_id,
            mission_id=session.active_mission_id,
            session_id=session.session_id,
            asked_at=when,
        )

        context = self.build_context(
            twin,
            question,
            session=session,
            enrich_evidence=enrich_evidence,
            assembled_at=when,
        )
        evidence = assemble_evidence(
            context,
            assembly_id=f"asm-{uuid.uuid4().hex[:10]}",
            question_kind=question.kind,
        )
        blueprint = build_response_blueprint(
            context=context,
            evidence=evidence,
            question_kind=question.kind,
            explanation_id=f"exp-{uuid.uuid4().hex[:12]}",
            response_seed=f"r-{uuid.uuid4().hex[:8]}",
        )
        generated = self._generation.generate(
            TutorGenerationRequest(
                question=question,
                context=context,
                blueprint=blueprint,
            )
        )
        response = TutorResponse(
            response_id=f"tr-{uuid.uuid4().hex[:12]}",
            session_id=session.session_id,
            twin_id=twin_id,
            question_id=question.question_id,
            body=generated.body,
            explanation=blueprint.explanation,
            supporting_evidence_ids=blueprint.supporting_evidence_ids,
            suggested_next_action=blueprint.suggested_next_action,
            related_concepts=blueprint.related_concepts,
            recovery_guidance=blueprint.recovery_guidance,
            reflection_prompt=blueprint.reflection_prompt,
            hints=blueprint.hints,
            coaching=blueprint.coaching,
            evidence_summaries=blueprint.evidence_summaries,
            context_id=context.context_id,
            generation_backend=generated.backend,
            created_at=when,
        )

        memory = session.memory or ConversationMemory(
            memory_id=f"mem-{session.session_id}",
            session_id=session.session_id,
            twin_id=twin_id,
        )
        memory = update_conversation_memory(
            memory,
            concept_ids=tuple(
                c
                for c in (
                    context.primary_concept_id,
                    *context.concept_ids,
                    *context.related_concept_ids,
                )
                if c
            ),
            active_mission_id=context.active_mission_id,
            learner_state_summary=context.learning_state_summary,
            question_kind=question.kind.value,
            response_id=response.response_id,
            updated_at=when,
        )
        session = session.with_turn(
            question=question,
            response=response,
            memory=memory,
            updated_at=when,
        )

        if persist:
            self._persistence.save_session(session)
            self._persistence.save_turn(
                session=session,
                question=question,
                response=response,
                context=context,
                evidence_ids=evidence.evidence_ids,
            )
            db.session.commit()

        return response

    def explain_mission(
        self,
        twin_id: str,
        *,
        persist: bool = True,
        enrich_evidence: bool = True,
    ) -> TutorResponse:
        """Explain today's adaptive mission using the Tutor pipeline."""
        mission = self._missions.get_active(twin_id)
        if mission and mission.goal:
            text = f"Why is today's mission focused on {mission.goal}?"
        else:
            text = "What should I do for today's mission and why?"
        primary = ""
        if mission is not None:
            primary = mission.objective.primary_concept_id
        return self.ask(
            twin_id,
            text,
            kind=TutorQuestionKind.DAILY_MISSION,
            concept_id=primary,
            persist=persist,
            enrich_evidence=enrich_evidence,
        )

    def preview_mission_guidance(self, twin_id: str) -> dict[str, str]:
        """Lightweight mission explanation preview for student Home.

        Does not open a session or call TutorGenerationPort. Surfaces Twin /
        Adaptive Mission decisions already available — the Tutor's voice without
        redesigning Home.
        """
        twin = self._twins.get(twin_id)
        if twin is None:
            return {"available": "", "guidance": "", "next_action": ""}
        mission = self._missions.get_active(twin_id)
        guidance = ""
        if mission and mission.reason.educational_explanation:
            guidance = mission.reason.educational_explanation
        elif twin.recommendations:
            guidance = twin.recommendations[0].reason
        elif twin.knowledge_gaps:
            gap = twin.knowledge_gaps[0]
            guidance = (
                f"Your Twin shows a knowledge gap on {gap.concept_id} "
                f"({gap.severity.value})."
            )
        next_action = ""
        if mission and mission.goal:
            next_action = f"Continue today's mission: {mission.goal}"
        elif twin.recommendations:
            next_action = twin.recommendations[0].title
        return {
            "available": "1" if guidance else "",
            "guidance": guidance,
            "next_action": next_action,
        }

    # ------------------------------------------------------------------
    # Context / evidence
    # ------------------------------------------------------------------

    def build_context(
        self,
        twin: StudentDigitalTwin,
        question: TutorQuestion,
        *,
        session: TutorSession | None = None,
        enrich_evidence: bool = True,
        assembled_at: datetime | None = None,
    ) -> TutorContext:
        """Assemble TutorContext from Twin → Reasoning → Graph → Retrieval."""
        when = assembled_at or datetime.now(UTC).replace(tzinfo=None)
        graph = self._graphs.get_for_twin(twin.twin_id)
        mission = self._missions.get_active(twin.twin_id)

        primary = (
            question.concept_id
            or (mission.objective.primary_concept_id if mission else "")
            or self._primary_concept_from_twin(twin)
        )
        recovery: tuple[str, ...] = ()
        prerequisites: tuple[str, ...] = ()
        related: tuple[str, ...] = ()
        if graph is not None and primary:
            recovery, prerequisites, related = self._graph_relations(
                graph, primary
            )

        curriculum_ids: list[str] = []
        curriculum_excerpts: list[str] = []
        if enrich_evidence and primary:
            curriculum_ids, curriculum_excerpts = self._retrieve_curriculum(
                twin, primary, question
            )
            # Prefer retrieval prerequisites when graph is sparse.
            if not prerequisites:
                prerequisites = tuple(
                    eid for eid in curriculum_ids if eid != primary
                )[:4]

        feedback_summaries = self._assessment_summaries(twin.twin_id)

        conversation_concepts: tuple[str, ...] = ()
        if session and session.memory:
            conversation_concepts = session.memory.referenced_concept_ids

        reasoning_run_id = ""
        if twin.reasoning_history:
            reasoning_run_id = twin.reasoning_history[-1].reasoning_id

        concept_ids = tuple(
            dict.fromkeys(
                [
                    c
                    for c in (
                        primary,
                        *(mission.concepts_covered if mission else ()),
                        *[g.concept_id for g in twin.knowledge_gaps[:5]],
                        *[r.curriculum_entity_id for r in twin.recommendations[:5]],
                    )
                    if c
                ]
            )
        )

        return TutorContext(
            context_id=f"ctx-{uuid.uuid4().hex[:12]}",
            twin_id=twin.twin_id,
            student_id=twin.student.student_id,
            question_kind=question.kind.value,
            question_text=question.text,
            active_mission_id=mission.mission_id if mission else "",
            active_mission_goal=mission.goal if mission else "",
            active_mission_reason=(
                mission.reason.educational_explanation if mission else ""
            ),
            primary_concept_id=primary,
            concept_ids=concept_ids,
            recommendation_summaries=tuple(
                f"{r.title}: {r.reason}" for r in twin.recommendations[:5]
            ),
            knowledge_gap_summaries=tuple(
                f"{g.concept_id} ({g.severity.value})"
                for g in twin.knowledge_gaps[:5]
            ),
            recovery_path=recovery,
            prerequisite_ids=prerequisites,
            related_concept_ids=related,
            mastery_notes=self._mastery_notes(twin, primary),
            confidence_notes=self._confidence_notes(twin),
            assessment_feedback_summaries=feedback_summaries,
            curriculum_evidence_ids=tuple(curriculum_ids),
            curriculum_excerpts=tuple(curriculum_excerpts),
            reasoning_run_id=reasoning_run_id,
            learning_state_summary=self._learning_state_summary(twin),
            conversation_concept_ids=conversation_concepts,
            assembled_at=when,
            metadata={
                "engine_version": self.ENGINE_VERSION,
                "generation_backend": self._generation.backend_name,
            },
        )

    def diagnostics_for_twin(self, twin_id: str) -> dict[str, Any]:
        """Founder diagnostics for Tutor state."""
        twin = self._twins.get(twin_id)
        sessions = self.list_sessions(twin_id) if twin else []
        active = [s for s in sessions if s.status == TutorSessionStatus.ACTIVE]
        mission = self._missions.get_active(twin_id) if twin else None
        return {
            "ok": True,
            "engine_version": self.ENGINE_VERSION,
            "generation_backend": self._generation.backend_name,
            "twin_id": twin_id,
            "twin_found": twin is not None,
            "session_count": len(sessions),
            "active_session_count": len(active),
            "active_mission_id": mission.mission_id if mission else None,
            "recommendation_count": len(twin.recommendations) if twin else 0,
            "knowledge_gap_count": len(twin.knowledge_gaps) if twin else 0,
            "reasoning_history_count": len(twin.reasoning_history) if twin else 0,
            "generated_at": datetime.now(UTC).replace(tzinfo=None).isoformat() + "Z",
        }

    def as_dict(self, response: TutorResponse) -> dict[str, Any]:
        """Serialise a TutorResponse for Founder / API diagnostics."""
        return {
            "response_id": response.response_id,
            "session_id": response.session_id,
            "twin_id": response.twin_id,
            "question_id": response.question_id,
            "body": response.body,
            "explanation": {
                "explanation_id": response.explanation.explanation_id,
                "kind": response.explanation.kind.value,
                "summary": response.explanation.summary,
                "detail": response.explanation.detail,
                "evidence_ids": list(response.explanation.evidence_ids),
                "concept_ids": list(response.explanation.concept_ids),
                "reasoning_run_id": response.explanation.reasoning_run_id,
                "mission_id": response.explanation.mission_id,
            },
            "supporting_evidence_ids": list(response.supporting_evidence_ids),
            "evidence_summaries": list(response.evidence_summaries),
            "suggested_next_action": response.suggested_next_action,
            "related_concepts": list(response.related_concepts),
            "recovery_guidance": response.recovery_guidance,
            "reflection_prompt": response.reflection_prompt,
            "hints": [
                {
                    "hint_id": h.hint_id,
                    "text": h.text,
                    "concept_id": h.concept_id,
                    "evidence_ids": list(h.evidence_ids),
                }
                for h in response.hints
            ],
            "coaching": [
                {
                    "message_id": m.message_id,
                    "text": m.text,
                    "tone": m.tone.value,
                    "evidence_ids": list(m.evidence_ids),
                }
                for m in response.coaching
            ],
            "context_id": response.context_id,
            "generation_backend": response.generation_backend,
            "created_at": (
                response.created_at.isoformat() if response.created_at else None
            ),
            "student_card": response.as_student_card(),
        }

    def session_as_dict(self, session: TutorSession) -> dict[str, Any]:
        return {
            "session_id": session.session_id,
            "twin_id": session.twin_id,
            "student_id": session.student_id,
            "status": session.status.value,
            "title": session.title,
            "active_mission_id": session.active_mission_id,
            "turn_count": session.turn_count,
            "memory": {
                "referenced_concept_ids": list(
                    session.memory.referenced_concept_ids if session.memory else ()
                ),
                "learner_state_summary": (
                    session.memory.learner_state_summary if session.memory else ""
                ),
                "turn_count": session.memory.turn_count if session.memory else 0,
                "last_question_kind": (
                    session.memory.last_question_kind if session.memory else ""
                ),
            }
            if session.memory
            else None,
            "created_at": (
                session.created_at.isoformat() if session.created_at else None
            ),
            "updated_at": (
                session.updated_at.isoformat() if session.updated_at else None
            ),
        }

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _require_twin(self, twin_id: str) -> StudentDigitalTwin:
        twin = self._twins.get(twin_id)
        if twin is None:
            raise ValueError(f"Student Digital Twin {twin_id!r} not found")
        return twin

    def _primary_concept_from_twin(self, twin: StudentDigitalTwin) -> str:
        if twin.recommendations:
            cid = twin.recommendations[0].curriculum_entity_id
            if cid:
                return cid
        if twin.knowledge_gaps:
            return twin.knowledge_gaps[0].concept_id
        return ""

    def _learning_state_summary(self, twin: StudentDigitalTwin) -> str:
        state = twin.learning_state
        return (
            "Learner state: "
            f"readiness={state.exam_readiness:.2f}, "
            f"momentum={state.momentum:.2f}, "
            f"consistency={state.consistency:.2f}, "
            f"knowledge={state.knowledge:.2f}"
        )

    def _mastery_notes(
        self, twin: StudentDigitalTwin, primary: str
    ) -> tuple[str, ...]:
        notes: list[str] = []
        if primary:
            entry = twin.mastery.get(primary)
            if entry is not None:
                notes.append(
                    f"Mastery for {primary}: {entry.mastery_score:.2f} "
                    f"({entry.trend.value})"
                )
        for record in twin.mastery.records[:3]:
            if primary and record.concept_id == primary:
                continue
            notes.append(
                f"Mastery for {record.concept_id}: {record.mastery_score:.2f}"
            )
        return tuple(notes[:5])

    def _confidence_notes(self, twin: StudentDigitalTwin) -> tuple[str, ...]:
        conf = twin.confidence
        notes = [f"Overall confidence: {conf.score:.2f} ({conf.band.value})"]
        if conf.reason:
            notes.append(f"Confidence reason: {conf.reason}")
        return tuple(notes)

    def _graph_relations(
        self, graph: LearningGraph, primary: str
    ) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
        recovery: tuple[str, ...] = ()
        prerequisites: tuple[str, ...] = ()
        related: tuple[str, ...] = ()
        try:
            path = self._traversal.recovery_path(graph, primary)
            recovery = tuple(path.concept_ids)
        except Exception:  # noqa: BLE001 — graph relations are best-effort
            recovery = ()
        try:
            trav = self._traversal.prerequisites(graph, primary)
            prerequisites = tuple(
                c for c in trav.visited_concept_ids if c != primary
            )[:6]
        except Exception:  # noqa: BLE001
            prerequisites = ()
        try:
            connected = self._traversal.connected(graph, primary, max_depth=2)
            related = tuple(
                c
                for c in connected.visited_concept_ids
                if c != primary and c not in prerequisites
            )[:4]
        except Exception:  # noqa: BLE001
            related = tuple(
                n.concept_id
                for n in graph.nodes
                if n.concept_id != primary and n.concept_id not in prerequisites
            )[:4]
        return recovery, prerequisites, related

    def _retrieve_curriculum(
        self,
        twin: StudentDigitalTwin,
        primary: str,
        question: TutorQuestion,
    ) -> tuple[list[str], list[str]]:
        workspace_id = (twin.student.workspace_id or "").strip()
        if not workspace_id:
            return [], []
        retrieval = self._retrieval
        if retrieval is None:
            try:
                retrieval = CurriculumRetrievalService()
                self._retrieval = retrieval
            except Exception:  # noqa: BLE001
                return [], []
        try:
            result = retrieval.retrieve(
                RetrievalQuery(
                    text=question.text or primary,
                    workspace_id=workspace_id,
                    profile=RetrievalProfile.TUTOR,
                    subject_code=twin.student.subject_code or "",
                    seed_entity_id=primary or None,
                    limit=5,
                    expand_graph_hops=1,
                )
            )
        except Exception:  # noqa: BLE001 — evidence enrichment is best-effort
            return [], []

        ids: list[str] = []
        excerpts: list[str] = []
        for ranked in result.results[:5]:
            ids.append(ranked.entity_id)
            if ranked.evidence:
                excerpts.append(ranked.evidence[0].excerpt or ranked.title)
            elif ranked.body:
                excerpts.append((ranked.body or ranked.title)[:240])
            else:
                excerpts.append(ranked.title)
        for prereq in result.prerequisite_ids[:4]:
            if prereq not in ids:
                ids.append(prereq)
        return ids, excerpts

    def _assessment_summaries(self, twin_id: str) -> tuple[str, ...]:
        try:
            feedback = self._assessments.list_feedback(twin_id, limit=5)
        except Exception:  # noqa: BLE001
            return ()
        summaries: list[str] = []
        for fb in feedback:
            bit = f"{fb.activity}: {fb.performance}"
            if fb.suggested_next_action:
                bit += f" → {fb.suggested_next_action}"
            summaries.append(bit)
        return tuple(summaries)
