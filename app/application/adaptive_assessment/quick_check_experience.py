"""Quick Check learner experience — presentation state machine (ILE-001B/C).

Orchestrates Mission-embedded Quick Check surfaces using already-selected
learning check items. No adaptive selection, Twin writes, Mission planning,
Assessment Engine scoring, or Tutor reasoning.

ILE-001C adds optional Study Sensei contextual framing (Context Card,
Educational Summary, recommendation framing) behind
``ENABLE_CONTEXTUAL_FRAMING`` (default OFF). Framing is presentation-only.

Answers are accepted only to advance the presentation flow; they are not
persisted as educational state and must never appear in telemetry payloads.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import StrEnum
from typing import Any
from uuid import uuid4

from app.application.adaptive_assessment.educational_framing import (
    ContextCardContract,
    EducationalSummaryContract,
    EvidenceBand,
    PresentationIntentContext,
    RecommendationFrameContract,
    ReflectionFrameContract,
    build_context_card,
    build_educational_summary,
    build_recommendation_frame,
    build_reflection_frame,
    default_intent_context,
)
from app.application.adaptive_assessment.feature_flags import (
    AdaptiveAssessmentFeatureFlags,
    resolve_adaptive_assessment_flags,
)
from app.application.adaptive_assessment.quick_check_contracts import (
    QuickCheckCompletionContract,
    QuickCheckIntroductionContract,
    QuickCheckMissionCardContract,
    QuickCheckMissionReturnContract,
    QuickCheckPausedContract,
    QuickCheckQuestionContract,
    QuickCheckReflectionContract,
    build_quick_check_completion,
    build_quick_check_introduction,
    build_quick_check_mission_card,
    build_quick_check_mission_return,
    build_quick_check_paused,
    build_quick_check_question,
    build_quick_check_reflection,
    default_selected_learning_check,
)
from app.application.adaptive_assessment.selected_learning_check import (
    SelectedLearningCheck,
)
from app.application.adaptive_assessment.session_registry import (
    SessionTypeId,
    get_session_type,
)
from app.application.adaptive_assessment.telemetry import (
    ProductTelemetryRecorder,
    TelemetryEventName,
    build_telemetry_event,
)


class QuickCheckPhase(StrEnum):
    """Learner-visible Quick Check phases."""

    INVITATION = "invitation"
    INTRODUCTION = "introduction"
    QUESTION = "question"
    REFLECTION = "reflection"
    COMPLETION = "completion"
    PAUSED = "paused"
    DISMISSED = "dismissed"


class QuickCheckExperienceError(ValueError):
    """Raised when a Quick Check experience transition is invalid."""


@dataclass
class QuickCheckExperienceState:
    """Mutable presentation state for one Quick Check run.

    Answers are held only to support pause/resume of the UI flow; they are
    never emitted as educational telemetry or Twin observations in ILE-001B/C.
    """

    experience_id: str
    student_id: str
    mission_ref: str
    subject_code: str
    phase: QuickCheckPhase
    check: SelectedLearningCheck
    item_index: int = 0
    hint_visible: bool = False
    paused_from: QuickCheckPhase | None = None
    responses: dict[str, str] = field(default_factory=dict)
    reflection_text: str = ""
    recommendation_choice: str = ""
    context_viewed: bool = False
    completed: bool = False
    dismissed: bool = False
    evidence_band: str = EvidenceBand.EMERGING.value


@dataclass(frozen=True)
class QuickCheckSurfaceSnapshot:
    """Immutable snapshot for one renderable Quick Check surface."""

    experience_id: str
    student_id: str
    mission_ref: str
    phase: str
    subject_code: str
    card: QuickCheckMissionCardContract | None = None
    introduction: QuickCheckIntroductionContract | None = None
    question: QuickCheckQuestionContract | None = None
    reflection: QuickCheckReflectionContract | None = None
    completion: QuickCheckCompletionContract | None = None
    paused: QuickCheckPausedContract | None = None
    mission_return: QuickCheckMissionReturnContract | None = None
    focus_label: str = ""
    framing_enabled: bool = False
    context_card: ContextCardContract | None = None
    educational_summary: EducationalSummaryContract | None = None
    recommendation: RecommendationFrameContract | None = None
    reflection_frame: ReflectionFrameContract | None = None
    evidence_band: str = EvidenceBand.EMERGING.value


class QuickCheckExperienceStore:
    """In-process store for Quick Check presentation state (no database)."""

    def __init__(self) -> None:
        self._by_id: dict[str, QuickCheckExperienceState] = {}
        self._active_by_student_mission: dict[str, str] = {}

    @staticmethod
    def _mission_key(student_id: str, mission_ref: str) -> str:
        return f"{student_id.strip()}::{mission_ref.strip()}"

    def get(self, experience_id: str) -> QuickCheckExperienceState | None:
        return self._by_id.get(experience_id)

    def get_active(
        self, student_id: str, mission_ref: str
    ) -> QuickCheckExperienceState | None:
        key = self._mission_key(student_id, mission_ref)
        eid = self._active_by_student_mission.get(key)
        if not eid:
            return None
        state = self._by_id.get(eid)
        if state is None or state.completed or state.dismissed:
            return None
        return state

    def save(self, state: QuickCheckExperienceState) -> None:
        self._by_id[state.experience_id] = state
        key = self._mission_key(state.student_id, state.mission_ref)
        if state.completed or state.dismissed:
            self._active_by_student_mission.pop(key, None)
        else:
            self._active_by_student_mission[key] = state.experience_id

    def clear(self) -> None:
        self._by_id.clear()
        self._active_by_student_mission.clear()


class QuickCheckExperienceService:
    """Presentation orchestrator for Mission-embedded Quick Check.

    Args:
        store: Experience state store (defaults to in-memory).
        telemetry: Behavioural product telemetry recorder.
        flags: Feature flags (resolved from env when omitted).
        learning_check: Already-selected check (no selection performed).
        intent_context: Optional presentation intent for framing composition.
    """

    def __init__(
        self,
        *,
        store: QuickCheckExperienceStore | None = None,
        telemetry: ProductTelemetryRecorder | None = None,
        flags: AdaptiveAssessmentFeatureFlags | None = None,
        learning_check: SelectedLearningCheck | None = None,
        intent_context: PresentationIntentContext | None = None,
    ) -> None:
        self._store = store if store is not None else QuickCheckExperienceStore()
        self._telemetry = (
            telemetry if telemetry is not None else ProductTelemetryRecorder()
        )
        self._flags = flags
        self._learning_check = (
            learning_check
            if learning_check is not None
            else default_selected_learning_check()
        )
        self._intent_context = intent_context

    @property
    def store(self) -> QuickCheckExperienceStore:
        return self._store

    @property
    def telemetry(self) -> ProductTelemetryRecorder:
        return self._telemetry

    def _resolve_flags(self) -> AdaptiveAssessmentFeatureFlags:
        if self._flags is not None:
            return self._flags
        return resolve_adaptive_assessment_flags()

    def is_available(
        self,
        *,
        subject_code: str | None = None,
        cohort_id: str | None = None,
    ) -> bool:
        """True when Quick Check may appear for the learner context."""
        return self._resolve_flags().is_available(
            SessionTypeId.QUICK_CHECK,
            subject_code=subject_code,
            cohort_id=cohort_id,
        )

    def is_framing_enabled(
        self,
        *,
        subject_code: str | None = None,
        cohort_id: str | None = None,
    ) -> bool:
        """True when ILE-001C contextual framing is active."""
        return self._resolve_flags().is_contextual_framing_enabled(
            subject_code=subject_code,
            cohort_id=cohort_id,
        )

    def _intent_for(
        self,
        *,
        focus_label: str = "",
        evidence_band: str | EvidenceBand | None = None,
    ) -> PresentationIntentContext:
        if self._intent_context is not None and not focus_label and (
            evidence_band is None
        ):
            return self._intent_context
        band: EvidenceBand | str
        if evidence_band is not None:
            band = evidence_band
        elif self._intent_context is not None:
            band = self._intent_context.evidence_band
        else:
            band = EvidenceBand.EMERGING
        focus = focus_label or (
            self._intent_context.focus_label
            if self._intent_context is not None
            else self._learning_check.focus_label
        )
        return default_intent_context(focus_label=focus, evidence_band=band)

    def mission_card(
        self,
        *,
        subject_code: str | None = None,
        cohort_id: str | None = None,
    ) -> QuickCheckMissionCardContract:
        """Build Mission entry card (available flag included)."""
        available = self.is_available(
            subject_code=subject_code, cohort_id=cohort_id
        )
        framing = self.is_framing_enabled(
            subject_code=subject_code, cohort_id=cohort_id
        )
        intent = self._intent_for()
        return build_quick_check_mission_card(
            available=available,
            framing_enabled=framing,
            focus_label=intent.focus_label,
        )

    def view_mission_invitation(
        self,
        *,
        student_id: str,
        mission_ref: str,
        subject_code: str = "",
        cohort_id: str | None = None,
    ) -> QuickCheckSurfaceSnapshot | None:
        """Return invitation snapshot when Quick Check is available."""
        if not self.is_available(
            subject_code=subject_code or None, cohort_id=cohort_id
        ):
            return None
        card = self.mission_card(
            subject_code=subject_code or None, cohort_id=cohort_id
        )
        self._emit(
            TelemetryEventName.ADAPTIVE_ASSESSMENT_VIEWED,
            subject_code=subject_code,
            payload={"surface": "mission_entry_card"},
        )
        active = self._store.get_active(student_id, mission_ref)
        if active is not None:
            return self.snapshot(active.experience_id, student_id=student_id)
        return QuickCheckSurfaceSnapshot(
            experience_id="",
            student_id=student_id,
            mission_ref=mission_ref,
            phase=QuickCheckPhase.INVITATION,
            subject_code=subject_code,
            card=card,
            focus_label=self._learning_check.focus_label,
        )

    def start(
        self,
        *,
        student_id: str,
        mission_ref: str,
        subject_code: str = "",
        cohort_id: str | None = None,
    ) -> QuickCheckSurfaceSnapshot:
        """Start Quick Check from Mission invitation → introduction."""
        if not self.is_available(
            subject_code=subject_code or None, cohort_id=cohort_id
        ):
            raise QuickCheckExperienceError("Quick Check is not available")
        existing = self._store.get_active(student_id, mission_ref)
        if existing is not None:
            return self.snapshot(
                existing.experience_id, student_id=student_id
            )
        if not self._learning_check.items:
            raise QuickCheckExperienceError(
                "already-selected learning check has no items"
            )
        state = QuickCheckExperienceState(
            experience_id=f"qc-{uuid4().hex[:12]}",
            student_id=student_id.strip(),
            mission_ref=mission_ref.strip(),
            subject_code=(subject_code or "").strip(),
            phase=QuickCheckPhase.INTRODUCTION,
            check=self._learning_check,
            evidence_band=self._intent_for().evidence_band.value,
        )
        self._store.save(state)
        self._emit(
            TelemetryEventName.QUICK_CHECK_STARTED,
            subject_code=state.subject_code,
            payload={
                "surface": "introduction",
                "check_id": state.check.check_id,
            },
        )
        return self._snapshot_for(state)

    def begin_questions(
        self, experience_id: str, *, student_id: str
    ) -> QuickCheckSurfaceSnapshot:
        """Introduction → first question."""
        state = self._require(experience_id, student_id)
        if state.phase != QuickCheckPhase.INTRODUCTION:
            raise QuickCheckExperienceError(
                f"cannot begin questions from phase {state.phase}"
            )
        state.phase = QuickCheckPhase.QUESTION
        state.item_index = 0
        state.hint_visible = False
        self._store.save(state)
        return self._snapshot_for(state)

    def show_hint(
        self, experience_id: str, *, student_id: str
    ) -> QuickCheckSurfaceSnapshot:
        """Reveal hint on the current question (presentation only)."""
        state = self._require(experience_id, student_id)
        if state.phase != QuickCheckPhase.QUESTION:
            raise QuickCheckExperienceError("hint only on question phase")
        state.hint_visible = True
        self._store.save(state)
        return self._snapshot_for(state)

    def submit_response(
        self,
        experience_id: str,
        *,
        student_id: str,
        item_id: str,
        response: str,
    ) -> QuickCheckSurfaceSnapshot:
        """Accept a response and advance to next item or reflection.

        Response text is kept only for UI continuity; never telemetried.
        """
        state = self._require(experience_id, student_id)
        if state.phase != QuickCheckPhase.QUESTION:
            raise QuickCheckExperienceError(
                "responses only accepted on question phase"
            )
        item = state.check.items[state.item_index]
        if item.item_id != item_id:
            raise QuickCheckExperienceError("item_id does not match current item")
        # Store for pause/resume UI only — not educational persistence.
        state.responses[item_id] = (response or "").strip()
        state.hint_visible = False
        if state.item_index + 1 < len(state.check.items):
            state.item_index += 1
            state.phase = QuickCheckPhase.QUESTION
        else:
            state.phase = QuickCheckPhase.REFLECTION
        self._store.save(state)
        return self._snapshot_for(state)

    def submit_reflection(
        self,
        experience_id: str,
        *,
        student_id: str,
        reflection: str = "",
        recommendation_choice: str = "",
    ) -> QuickCheckSurfaceSnapshot:
        """Reflection → completion (Educational Summary when framing on)."""
        state = self._require(experience_id, student_id)
        if state.phase != QuickCheckPhase.REFLECTION:
            raise QuickCheckExperienceError(
                "reflection only accepted on reflection phase"
            )
        state.reflection_text = (reflection or "").strip()
        choice = (recommendation_choice or "").strip().lower()
        state.recommendation_choice = choice
        state.phase = QuickCheckPhase.COMPLETION
        state.completed = True
        self._store.save(state)
        self._emit(
            TelemetryEventName.REFLECTION_COMPLETED,
            subject_code=state.subject_code,
            payload={"surface": "reflection"},
        )
        if choice in {"accept", "accepted"}:
            self._emit(
                TelemetryEventName.RECOMMENDATION_ACCEPTED,
                subject_code=state.subject_code,
                payload={"surface": "reflection"},
            )
        elif choice in {"defer", "deferred", "later"}:
            self._emit(
                TelemetryEventName.RECOMMENDATION_DEFERRED,
                subject_code=state.subject_code,
                payload={"surface": "reflection"},
            )
        self._emit(
            TelemetryEventName.QUICK_CHECK_COMPLETED,
            subject_code=state.subject_code,
            payload={
                "surface": "completion",
                "check_id": state.check.check_id,
                "item_count": len(state.check.items),
            },
        )
        return self._snapshot_for(state)

    def mark_context_viewed(
        self, experience_id: str, *, student_id: str
    ) -> QuickCheckSurfaceSnapshot:
        """Record Context Card viewed (once per experience)."""
        state = self._require(experience_id, student_id)
        if not state.context_viewed:
            state.context_viewed = True
            self._store.save(state)
            self._emit(
                TelemetryEventName.CONTEXT_VIEWED,
                subject_code=state.subject_code,
                payload={"surface": "context_card"},
            )
        return self._snapshot_for(state)

    def expand_explanation(
        self,
        *,
        student_id: str = "",
        subject_code: str = "",
        surface: str = "why_recommendation",
        experience_id: str = "",
    ) -> None:
        """Record that the learner expanded educational reasoning."""
        _ = student_id, experience_id
        event = (
            TelemetryEventName.WHY_RECOMMENDATION_OPENED
            if surface in {"why_recommendation", "recommendation"}
            else TelemetryEventName.EXPLANATION_EXPANDED
        )
        self._emit(
            event,
            subject_code=subject_code,
            payload={"surface": surface},
        )

    def accept_recommendation(
        self,
        experience_id: str,
        *,
        student_id: str,
        surface: str = "completion",
    ) -> QuickCheckSurfaceSnapshot:
        """Record recommendation accepted (behavioural telemetry only)."""
        state = self._require(experience_id, student_id)
        state.recommendation_choice = "accept"
        self._store.save(state)
        self._emit(
            TelemetryEventName.RECOMMENDATION_ACCEPTED,
            subject_code=state.subject_code,
            payload={"surface": surface},
        )
        return self._snapshot_for(state)

    def defer_recommendation(
        self,
        experience_id: str,
        *,
        student_id: str,
        surface: str = "completion",
    ) -> QuickCheckSurfaceSnapshot:
        """Record recommendation deferred (behavioural telemetry only)."""
        state = self._require(experience_id, student_id)
        state.recommendation_choice = "defer"
        self._store.save(state)
        self._emit(
            TelemetryEventName.RECOMMENDATION_DEFERRED,
            subject_code=state.subject_code,
            payload={"surface": surface},
        )
        return self._snapshot_for(state)

    def pause(
        self, experience_id: str, *, student_id: str
    ) -> QuickCheckSurfaceSnapshot:
        """Pause from question or reflection."""
        state = self._require(experience_id, student_id)
        if state.phase not in {
            QuickCheckPhase.QUESTION,
            QuickCheckPhase.REFLECTION,
            QuickCheckPhase.INTRODUCTION,
        }:
            raise QuickCheckExperienceError(
                f"cannot pause from phase {state.phase}"
            )
        state.paused_from = state.phase
        state.phase = QuickCheckPhase.PAUSED
        self._store.save(state)
        return self._snapshot_for(state)

    def resume(
        self, experience_id: str, *, student_id: str
    ) -> QuickCheckSurfaceSnapshot:
        """Resume from paused phase."""
        state = self._require(experience_id, student_id)
        if state.phase != QuickCheckPhase.PAUSED:
            raise QuickCheckExperienceError("experience is not paused")
        restore = state.paused_from or QuickCheckPhase.QUESTION
        state.phase = restore
        state.paused_from = None
        self._store.save(state)
        return self._snapshot_for(state)

    def defer(
        self, experience_id: str, *, student_id: str
    ) -> QuickCheckMissionReturnContract:
        """Dismiss / defer Quick Check and return Mission acknowledgement."""
        state = self._require(experience_id, student_id)
        state.dismissed = True
        state.phase = QuickCheckPhase.DISMISSED
        self._store.save(state)
        self._emit(
            TelemetryEventName.QUICK_CHECK_DISMISSED,
            subject_code=state.subject_code,
            payload={"surface": "defer"},
        )
        self._emit(
            TelemetryEventName.ASSESSMENT_DEFERRED,
            subject_code=state.subject_code,
            payload={"session_type": SessionTypeId.QUICK_CHECK},
        )
        return build_quick_check_mission_return()

    def defer_from_invitation(
        self,
        *,
        student_id: str,
        mission_ref: str,
        subject_code: str = "",
    ) -> QuickCheckMissionReturnContract:
        """Defer before starting (no experience created)."""
        _ = student_id, mission_ref
        self._emit(
            TelemetryEventName.QUICK_CHECK_DISMISSED,
            subject_code=subject_code,
            payload={"surface": "mission_entry_card"},
        )
        self._emit(
            TelemetryEventName.ASSESSMENT_DEFERRED,
            subject_code=subject_code,
            payload={"session_type": SessionTypeId.QUICK_CHECK},
        )
        return build_quick_check_mission_return()

    def explain(
        self,
        *,
        student_id: str = "",
        subject_code: str = "",
        surface: str = "why_this",
    ) -> None:
        """Record that the learner opened the why-this explanation."""
        _ = student_id
        self._emit(
            TelemetryEventName.ASSESSMENT_EXPLAINED,
            subject_code=subject_code,
            payload={"surface": surface},
        )
        if surface in {"why_recommendation", "recommendation"}:
            self._emit(
                TelemetryEventName.WHY_RECOMMENDATION_OPENED,
                subject_code=subject_code,
                payload={"surface": surface},
            )
        elif surface in {"context_why", "explanation_expanded"}:
            self._emit(
                TelemetryEventName.EXPLANATION_EXPANDED,
                subject_code=subject_code,
                payload={"surface": surface},
            )

    def complete_return(
        self, experience_id: str, *, student_id: str
    ) -> QuickCheckMissionReturnContract:
        """Mission return after completion."""
        state = self._require(experience_id, student_id)
        if not state.completed and state.phase != QuickCheckPhase.COMPLETION:
            raise QuickCheckExperienceError(
                "cannot return to Mission before completion"
            )
        return build_quick_check_mission_return()

    def snapshot(
        self, experience_id: str, *, student_id: str
    ) -> QuickCheckSurfaceSnapshot:
        """Load a snapshot for an existing experience."""
        state = self._require(experience_id, student_id)
        return self._snapshot_for(state)

    def _require(
        self, experience_id: str, student_id: str
    ) -> QuickCheckExperienceState:
        state = self._store.get(experience_id)
        if state is None:
            raise QuickCheckExperienceError(
                f"unknown Quick Check experience: {experience_id}"
            )
        if state.student_id != student_id.strip():
            raise QuickCheckExperienceError(
                "Quick Check experience is not owned by this student"
            )
        return state

    def _snapshot_for(
        self, state: QuickCheckExperienceState
    ) -> QuickCheckSurfaceSnapshot:
        card = None
        introduction = None
        question = None
        reflection = None
        completion = None
        paused = None
        mission_return = None
        context_card = None
        educational_summary = None
        recommendation = None
        reflection_frame = None

        framing = self.is_framing_enabled(subject_code=state.subject_code or None)
        intent = self._intent_for(
            focus_label=state.check.focus_label,
            evidence_band=state.evidence_band,
        )

        if state.phase == QuickCheckPhase.INTRODUCTION:
            introduction = build_quick_check_introduction(
                framing_enabled=framing
            )
            if framing:
                session = get_session_type(SessionTypeId.QUICK_CHECK)
                context_card = build_context_card(
                    intent, duration_label=session.expected_duration_label
                )
        elif state.phase == QuickCheckPhase.QUESTION:
            item = state.check.items[state.item_index]
            question = build_quick_check_question(
                item,
                index=state.item_index,
                total=len(state.check.items),
                hint_visible=state.hint_visible,
            )
        elif state.phase == QuickCheckPhase.REFLECTION:
            reflection = build_quick_check_reflection()
            if framing:
                reflection_frame = build_reflection_frame(intent)
                recommendation = build_recommendation_frame(intent)
        elif state.phase == QuickCheckPhase.COMPLETION:
            completion = build_quick_check_completion()
            mission_return = build_quick_check_mission_return()
            if framing:
                educational_summary = build_educational_summary(intent)
                recommendation = build_recommendation_frame(intent)
        elif state.phase == QuickCheckPhase.PAUSED:
            paused = build_quick_check_paused()
        elif state.phase == QuickCheckPhase.INVITATION:
            card = build_quick_check_mission_card(
                available=True,
                framing_enabled=framing,
                focus_label=intent.focus_label,
            )

        return QuickCheckSurfaceSnapshot(
            experience_id=state.experience_id,
            student_id=state.student_id,
            mission_ref=state.mission_ref,
            phase=state.phase.value,
            subject_code=state.subject_code,
            card=card,
            introduction=introduction,
            question=question,
            reflection=reflection,
            completion=completion,
            paused=paused,
            mission_return=mission_return,
            focus_label=state.check.focus_label,
            framing_enabled=framing,
            context_card=context_card,
            educational_summary=educational_summary,
            recommendation=recommendation,
            reflection_frame=reflection_frame,
            evidence_band=state.evidence_band,
        )

    def _emit(
        self,
        event_name: TelemetryEventName,
        *,
        subject_code: str = "",
        payload: dict[str, Any] | None = None,
    ) -> None:
        event = build_telemetry_event(
            event_name,
            session_type_id=SessionTypeId.QUICK_CHECK,
            subject_code=subject_code,
            payload=payload,
        )
        self._telemetry.record(event)


# Process-default service for presentation wiring (tests inject their own).
_DEFAULT_SERVICE: QuickCheckExperienceService | None = None


def get_quick_check_experience_service() -> QuickCheckExperienceService:
    """Return the process-default Quick Check experience service."""
    global _DEFAULT_SERVICE
    if _DEFAULT_SERVICE is None:
        _DEFAULT_SERVICE = QuickCheckExperienceService()
    return _DEFAULT_SERVICE


def reset_quick_check_experience_service(
    service: QuickCheckExperienceService | None = None,
) -> QuickCheckExperienceService:
    """Replace the process-default service (tests / factory)."""
    global _DEFAULT_SERVICE
    _DEFAULT_SERVICE = (
        service if service is not None else QuickCheckExperienceService()
    )
    return _DEFAULT_SERVICE


def clone_state_without_answers(
    state: QuickCheckExperienceState,
) -> QuickCheckExperienceState:
    """Return a copy stripped of response text (telemetry / export safety)."""
    return replace(state, responses={}, reflection_text="")
