"""Learning Session Runtime persistence adapter (SR-002 P1 / LXP-003 P2).

Persists SessionHandle bindings via SessionDocumentStore so Home can
resume and Session Experience can project overview without inventing a
second FSM. Additive opaque documents — no Alembic schema change.

P2 adds finish review, plan checklist, and workspace surface so session
progress survives browser refresh and navigation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from app.application.learning_session.dto.finish_review import FinishReview
from app.application.learning_session.dto.learning_session_plan import (
    LearningSessionPlan,
)
from app.application.learning_session.runtime import SessionHandle
from app.application.learning_session.runtime_phase import RuntimePhase
from app.domain.learning_journey.entities.learning_session import LearningSession
from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate
from app.domain.learning_journey.value_objects.session_state import SessionState
from app.infrastructure.session.store import SessionDocumentStore

NS_HANDLE = "lsr.handle"
NS_OPEN = "lsr.open"
NS_MISSION = "lsr.mission"
NS_PROGRESS = "lsr.progress"
NS_CANDIDATES = "lsr.evidence_candidates"
NS_EVIDENCE_PACKAGE = "lsr.evidence_package"

DEFAULT_CHECKLIST: tuple[dict[str, Any], ...] = (
    {"id": "read", "label": "Read today's topic", "done": False},
    {"id": "examples", "label": "Work through examples", "done": False},
    {"id": "practice", "label": "Attempt practice questions", "done": False},
    {"id": "review", "label": "Review mistakes", "done": False},
)


class LearningSessionPersistenceAdapter:
    """Durable (or in-memory) store for LearningSessionRuntime bindings."""

    def __init__(self, *, store: SessionDocumentStore | None = None) -> None:
        self._store = store or SessionDocumentStore()

    @property
    def store(self) -> SessionDocumentStore:
        return self._store

    def save_binding(
        self,
        *,
        student_id: str,
        mission_instance_id: str,
        handle: SessionHandle,
        topic_title: str = "",
        topic_id: str = "",
        estimated_minutes: int | None = None,
        curriculum_identity: str = "",
        active_surface: str | None = None,
        checklist: list[dict[str, Any]] | tuple[dict[str, Any], ...] | None = None,
        educational_package_id: str = "",
    ) -> dict[str, Any]:
        sid = student_id.strip()
        session_id = handle.session.session_id
        existing = self.load(session_id=session_id) or {}
        progress = self.load_progress(session_id=session_id) or {}
        surface = active_surface or progress.get("active_surface") or "overview"
        items = checklist
        if items is None:
            items = progress.get("checklist") or list(DEFAULT_CHECKLIST)
        document = {
            "session_id": session_id,
            "student_id": sid,
            "mission_instance_id": (mission_instance_id or "").strip(),
            "topic_title": topic_title or existing.get("topic_title") or "",
            "topic_id": topic_id
            or (handle.plan.topic_id if handle.plan else "")
            or existing.get("topic_id")
            or "",
            "estimated_minutes": (
                estimated_minutes
                if estimated_minutes is not None
                else existing.get("estimated_minutes")
            ),
            "curriculum_identity": curriculum_identity
            or existing.get("curriculum_identity")
            or "",
            "educational_package_id": (
                (educational_package_id or "").strip()
                or str(existing.get("educational_package_id") or "")
            ),
            "objective_ids": list(
                getattr(handle.plan, "objective_ids", ()) or ()
            )
            or list(existing.get("objective_ids") or []),
            "phase": handle.phase.value,
            "session_state": handle.session.state.value,
            "status": "open"
            if handle.phase
            not in (RuntimePhase.COMPLETED, RuntimePhase.ARCHIVED)
            else "completed",
            "authority": "learning_session_runtime",
            "finish_review": (
                handle.finish_review.to_opaque()
                if handle.finish_review is not None
                else existing.get("finish_review")
            ),
            "handle": _serialize_handle(handle),
        }
        self._store.save(NS_HANDLE, session_id, document)
        self.save_progress(
            session_id=session_id,
            student_id=sid,
            active_surface=str(surface),
            checklist=list(items),
            phase=handle.phase.value,
            paused=handle.phase == RuntimePhase.PAUSED,
        )
        if document["status"] == "open":
            self._store.save(NS_OPEN, sid, {"session_id": session_id})
            if mission_instance_id:
                self._store.save(
                    NS_MISSION,
                    f"{sid}::{mission_instance_id.strip()}",
                    {"session_id": session_id},
                )
        return deepcopy(document)

    def load(self, *, session_id: str) -> dict[str, Any] | None:
        doc = self._store.get(NS_HANDLE, session_id.strip())
        return None if doc is None else deepcopy(doc)

    def load_handle(self, *, session_id: str) -> SessionHandle | None:
        doc = self.load(session_id=session_id)
        if doc is None:
            return None
        raw = doc.get("handle")
        if not isinstance(raw, dict):
            return None
        handle = _deserialize_handle(raw)
        review = FinishReview.from_opaque(doc.get("finish_review"))
        if review is not None and handle.finish_review is None:
            handle = SessionHandle(
                session=handle.session,
                phase=handle.phase,
                plan=handle.plan,
                finish_review=review,
            )
        return handle

    def save_progress(
        self,
        *,
        session_id: str,
        student_id: str,
        active_surface: str = "overview",
        checklist: list[dict[str, Any]] | None = None,
        phase: str = "",
        paused: bool = False,
        elapsed_active_seconds: int | None = None,
    ) -> dict[str, Any]:
        existing = self.load_progress(session_id=session_id) or {}
        document = {
            "session_id": session_id.strip(),
            "student_id": student_id.strip(),
            "active_surface": (
                active_surface
                or existing.get("active_surface")
                or "overview"
            ),
            "checklist": checklist
            if checklist is not None
            else existing.get("checklist")
            or list(DEFAULT_CHECKLIST),
            "phase": phase or existing.get("phase") or "",
            "paused": bool(paused),
            "elapsed_active_seconds": (
                elapsed_active_seconds
                if elapsed_active_seconds is not None
                else existing.get("elapsed_active_seconds") or 0
            ),
        }
        self._store.save(NS_PROGRESS, session_id.strip(), document)
        return deepcopy(document)

    def load_progress(self, *, session_id: str) -> dict[str, Any] | None:
        doc = self._store.get(NS_PROGRESS, session_id.strip())
        return None if doc is None else deepcopy(doc)

    def update_checklist_item(
        self,
        *,
        session_id: str,
        student_id: str,
        item_id: str,
        done: bool,
    ) -> dict[str, Any] | None:
        progress = self.load_progress(session_id=session_id)
        if progress is None or str(progress.get("student_id")) != student_id.strip():
            return None
        items = list(progress.get("checklist") or DEFAULT_CHECKLIST)
        updated: list[dict[str, Any]] = []
        for item in items:
            row = dict(item)
            if str(row.get("id")) == item_id.strip():
                row["done"] = bool(done)
            updated.append(row)
        return self.save_progress(
            session_id=session_id,
            student_id=student_id,
            active_surface=str(progress.get("active_surface") or "overview"),
            checklist=updated,
            phase=str(progress.get("phase") or ""),
            paused=bool(progress.get("paused")),
            elapsed_active_seconds=progress.get("elapsed_active_seconds"),
        )

    def find_open(
        self,
        *,
        student_id: str,
        mission_instance_id: str | None = None,
    ) -> dict[str, Any] | None:
        sid = student_id.strip()
        session_id = None
        if mission_instance_id:
            ptr = self._store.get(
                NS_MISSION, f"{sid}::{mission_instance_id.strip()}"
            )
            if ptr is not None:
                session_id = str(ptr.get("session_id") or "").strip() or None
        if not session_id:
            ptr = self._store.get(NS_OPEN, sid)
            if ptr is not None:
                session_id = str(ptr.get("session_id") or "").strip() or None
        if not session_id:
            return None
        doc = self.load(session_id=session_id)
        if doc is None or doc.get("status") != "open":
            return None
        if str(doc.get("student_id") or "") != sid:
            return None
        return doc

    def mark_completed(self, *, session_id: str) -> None:
        doc = self.load(session_id=session_id)
        if doc is None:
            return
        doc = {**doc, "status": "completed", "phase": RuntimePhase.COMPLETED.value}
        self._store.save(NS_HANDLE, session_id.strip(), doc)
        sid = str(doc.get("student_id") or "")
        if sid:
            open_ptr = self._store.get(NS_OPEN, sid)
            if open_ptr and str(open_ptr.get("session_id")) == session_id.strip():
                self._store.delete(NS_OPEN, sid)
        progress = self.load_progress(session_id=session_id)
        if progress is not None:
            self.save_progress(
                session_id=session_id,
                student_id=sid or str(progress.get("student_id") or ""),
                active_surface="complete",
                checklist=list(progress.get("checklist") or DEFAULT_CHECKLIST),
                phase=RuntimePhase.COMPLETED.value,
                paused=False,
                elapsed_active_seconds=progress.get("elapsed_active_seconds"),
            )

    def save_sitting_outcome(
        self,
        *,
        session_id: str,
        progress_advanced: bool = False,
        mission_completed: bool = False,
        twin_updated: bool = False,
        evidence_disposition: str | None = None,
        finish_review: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Persist student-safe sitting outcome flags for Sitting Report (KWP-005)."""
        doc = self.load(session_id=session_id)
        if doc is None:
            return None
        updated = {
            **doc,
            "progress_advanced": bool(progress_advanced),
            "mission_completed": bool(mission_completed),
            "twin_updated": bool(twin_updated),
        }
        if evidence_disposition is not None:
            updated["evidence_disposition"] = evidence_disposition
        if finish_review is not None:
            updated["finish_review"] = finish_review
        self._store.save(NS_HANDLE, session_id.strip(), updated)
        return deepcopy(updated)

    def save_reflection_note(
        self, *, session_id: str, note: str, student_id: str = ""
    ) -> dict[str, Any] | None:
        """Persist free-text session reflection onto the handle document.

        Queryable via ``load`` / completion summary. Does not score or interpret
        the note. Empty notes clear any prior stored text. When ``student_id``
        is provided, ownership must match.
        """
        doc = self.load(session_id=session_id)
        if doc is None:
            return None
        sid = (student_id or "").strip()
        if sid and str(doc.get("student_id") or "") != sid:
            return None
        cleaned = (note or "").strip()
        updated = {**doc, "reflection_note": cleaned}
        self._store.save(NS_HANDLE, session_id.strip(), updated)
        return deepcopy(updated)

    # ------------------------------------------------------------------
    # EV-001B — candidate observations + accepted evidence packages
    # ------------------------------------------------------------------

    def append_candidate(
        self, *, session_id: str, observation: dict[str, Any]
    ) -> dict[str, Any]:
        """Append one Generated candidate observation (idempotent by id)."""
        key = session_id.strip()
        existing = self._store.get(NS_CANDIDATES, key) or {
            "session_id": key,
            "items": [],
        }
        items = list(existing.get("items") or [])
        oid = str(observation.get("observation_id") or "")
        if oid and any(str(i.get("observation_id")) == oid for i in items):
            return deepcopy(existing)
        items.append(deepcopy(observation))
        document = {"session_id": key, "items": items}
        self._store.save(NS_CANDIDATES, key, document)
        return deepcopy(document)

    def load_candidates(self, *, session_id: str) -> list[dict[str, Any]]:
        doc = self._store.get(NS_CANDIDATES, session_id.strip())
        if not isinstance(doc, dict):
            return []
        return [deepcopy(i) for i in (doc.get("items") or [])]

    def save_evidence_package(
        self, *, session_id: str, package: dict[str, Any]
    ) -> dict[str, Any]:
        """Persist an Accepted / Rejected package (no silent rewrite of history).

        Rollback of SR_EVIDENCE_GATE must not delete rows (EV-001A C10).
        """
        key = session_id.strip()
        document = deepcopy(package)
        document["session_id"] = key
        self._store.save(NS_EVIDENCE_PACKAGE, key, document)
        # Also retain on the handle document for recovery.
        handle_doc = self.load(session_id=key)
        if handle_doc is not None:
            handle_doc = {
                **handle_doc,
                "evidence_package_id": document.get("package_id"),
                "evidence_disposition": (
                    (document.get("validation") or {}).get("disposition")
                ),
            }
            self._store.save(NS_HANDLE, key, handle_doc)
        return deepcopy(document)

    def load_evidence_package(self, *, session_id: str) -> dict[str, Any] | None:
        doc = self._store.get(NS_EVIDENCE_PACKAGE, session_id.strip())
        return None if doc is None else deepcopy(doc)


def _serialize_handle(handle: SessionHandle) -> dict[str, Any]:
    session = handle.session
    plan = handle.plan
    return {
        "phase": handle.phase.value,
        "finish_review": (
            handle.finish_review.to_opaque()
            if handle.finish_review is not None
            else None
        ),
        "session": {
            "session_id": session.session_id,
            "journey_id": session.journey_id,
            "sequence_index": session.sequence_index,
            "state": session.state.value,
            "estimated_effort": session.estimated_effort.value,
            "objective_id": session.objective_id,
            "actual_duration_minutes": session.actual_duration_minutes,
        },
        "plan": None
        if plan is None
        else {
            "session_id": plan.session_id,
            "journey_id": plan.journey_id,
            "topic_id": plan.topic_id,
            "sequence_index": plan.sequence_index,
            "objective_ids": list(plan.objective_ids),
            "estimated_effort": plan.estimated_effort.value,
            "recommended_activities": list(plan.recommended_activities),
            "previous_evidence_count": plan.previous_evidence_count,
            "rationale_tags": list(plan.rationale_tags),
        },
    }


def _deserialize_handle(raw: dict[str, Any]) -> SessionHandle:
    session_raw = raw["session"]
    session = LearningSession.create(
        str(session_raw["session_id"]),
        str(session_raw["journey_id"]),
        sequence_index=int(session_raw.get("sequence_index") or 0),
        state=SessionState(str(session_raw["state"])),
        estimated_effort=EffortEstimate(
            str(session_raw.get("estimated_effort") or EffortEstimate.MEDIUM.value)
        ),
        objective_id=session_raw.get("objective_id"),
        actual_duration_minutes=session_raw.get("actual_duration_minutes"),
    )
    plan = None
    plan_raw = raw.get("plan")
    if isinstance(plan_raw, dict):
        plan = LearningSessionPlan(
            session_id=str(plan_raw["session_id"]),
            journey_id=str(plan_raw["journey_id"]),
            topic_id=str(plan_raw["topic_id"]),
            sequence_index=int(plan_raw.get("sequence_index") or 0),
            objective_ids=tuple(plan_raw.get("objective_ids") or ()),
            estimated_effort=EffortEstimate(
                str(plan_raw.get("estimated_effort") or EffortEstimate.MEDIUM.value)
            ),
            recommended_activities=tuple(
                plan_raw.get("recommended_activities") or ()
            ),
            previous_evidence_count=int(
                plan_raw.get("previous_evidence_count") or 0
            ),
            rationale_tags=tuple(plan_raw.get("rationale_tags") or ()),
        )
    return SessionHandle(
        session=session,
        phase=RuntimePhase(str(raw["phase"])),
        plan=plan,
        finish_review=FinishReview.from_opaque(raw.get("finish_review")),
    )
