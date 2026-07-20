"""EducationalDigitalTwin aggregate root — educational memory of a learner.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
    EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md
Concept
    Educational Digital Twin
"""

from __future__ import annotations

from domain.education.digital_twin.entities.concept_state import (
    ConceptState,
    ConceptStateId,
)
from domain.education.digital_twin.entities.evidence_history import (
    EvidenceHistoryEntry,
    EvidenceHistoryEntryId,
)
from domain.education.digital_twin.entities.intervention_history import (
    InterventionHistoryEntry,
    InterventionHistoryEntryId,
)
from domain.education.digital_twin.entities.learner_state import (
    LearnerState,
    LearnerStateId,
)
from domain.education.digital_twin.entities.misconception_state import (
    MisconceptionState,
    MisconceptionStateId,
)
from domain.education.digital_twin.enums import (
    LearnerActivityStatus,
    MasteryBand,
    MisconceptionPresence,
    TrajectoryPointKind,
    TwinStatus,
    TwinUpdateKind,
)
from domain.education.digital_twin.events.mastery_changed import MasteryChanged
from domain.education.digital_twin.events.twin_created import TwinCreated
from domain.education.digital_twin.events.twin_updated import TwinUpdated
from domain.education.digital_twin.policies.state_validation_policy import (
    StateValidationPolicy,
)
from domain.education.digital_twin.policies.twin_update_policy import TwinUpdatePolicy
from domain.education.digital_twin.specifications.state_transition_is_valid import (
    StateTransitionIsValidSpecification,
)
from domain.education.digital_twin.value_objects.confidence_profile import (
    ConfidenceProfile,
)
from domain.education.digital_twin.value_objects.learning_trajectory import (
    LearningTrajectory,
    TrajectoryPoint,
)
from domain.education.digital_twin.value_objects.mastery_state import MasteryState
from domain.education.digital_twin.value_objects.retention_state import RetentionState
from domain.education.foundation.enums import (
    EvidenceType,
    TeachingIntentionType,
    TeachingStrategyType,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    ConceptId,
    DigitalTwinId,
    EvidenceId,
    MisconceptionId,
)

DomainEvent = TwinCreated | TwinUpdated | MasteryChanged


class EducationalDigitalTwin:
    """Aggregate root for Educational Digital Twin memory.

    Owns learner state, concept states, misconception states, evidence history,
    intervention history, retention state, confidence profile, and learning
    trajectory.

    The Twin remembers. It does not diagnose, interpret evidence, create
    hypotheses, choose priorities or strategies, approve interventions, or
    orchestrate sessions.

    Behaviour is exposed only through methods — no public setters.
    """

    def __init__(
        self,
        twin_id: DigitalTwinId,
        student_id: str,
        learner_state: LearnerState,
        *,
        concept_states: list[ConceptState] | tuple[ConceptState, ...] | None = None,
        misconception_states: list[MisconceptionState]
        | tuple[MisconceptionState, ...]
        | None = None,
        evidence_history: list[EvidenceHistoryEntry]
        | tuple[EvidenceHistoryEntry, ...]
        | None = None,
        intervention_history: list[InterventionHistoryEntry]
        | tuple[InterventionHistoryEntry, ...]
        | None = None,
        retention: RetentionState | None = None,
        confidence: ConfidenceProfile | None = None,
        trajectory: LearningTrajectory | None = None,
        status: TwinStatus = TwinStatus.ACTIVE,
        _record_created: bool = False,
    ) -> None:
        self._twin_id = StateValidationPolicy.assert_identity(twin_id)
        self._student_id = StateValidationPolicy.assert_student_id(student_id)
        self._learner_state = StateValidationPolicy.assert_learner_state(learner_state)
        StateValidationPolicy.assert_learner_matches_student(
            self._learner_state, self._student_id
        )
        self._concept_states = StateValidationPolicy.assert_concept_states(
            concept_states or ()
        )
        self._misconception_states = StateValidationPolicy.assert_misconception_states(
            misconception_states or ()
        )
        self._evidence_history = StateValidationPolicy.assert_evidence_history(
            evidence_history or ()
        )
        self._intervention_history = StateValidationPolicy.assert_intervention_history(
            intervention_history or ()
        )
        self._retention = StateValidationPolicy.assert_retention(
            retention if retention is not None else RetentionState.unknown()
        )
        self._confidence = StateValidationPolicy.assert_confidence(
            confidence if confidence is not None else ConfidenceProfile.unknown()
        )
        self._trajectory = StateValidationPolicy.assert_trajectory(
            trajectory if trajectory is not None else LearningTrajectory.empty()
        )
        self._status = StateValidationPolicy.assert_status(status)
        self._pending_events: list[DomainEvent] = []
        if _record_created:
            self._pending_events.append(
                TwinCreated(
                    twin_id=self._twin_id,
                    student_id=self._student_id,
                    status=self._status,
                    learner_state_id=self._learner_state.learner_state_id.value,
                )
            )

    @classmethod
    def create(
        cls,
        twin_id: DigitalTwinId,
        student_id: str,
        *,
        learner_state_id: str | LearnerStateId | None = None,
        activity_status: LearnerActivityStatus = LearnerActivityStatus.ENGAGED,
        retention: RetentionState | None = None,
        confidence: ConfidenceProfile | None = None,
    ) -> EducationalDigitalTwin:
        """Factory: create an ACTIVE Twin that owns learner state."""
        if isinstance(learner_state_id, LearnerStateId):
            state_id = learner_state_id
        elif learner_state_id is None:
            state_id = LearnerStateId(f"learner-{student_id}")
        else:
            state_id = LearnerStateId(learner_state_id)
        learner_state = LearnerState(
            learner_state_id=state_id,
            student_id=student_id,
            activity_status=activity_status,
        )
        trajectory = LearningTrajectory.of(
            TrajectoryPoint(
                sequence=1,
                kind=TrajectoryPointKind.CREATED,
                label="twin-created",
            )
        )
        return cls(
            twin_id=twin_id,
            student_id=student_id,
            learner_state=learner_state,
            retention=retention,
            confidence=confidence,
            trajectory=trajectory,
            status=TwinStatus.ACTIVE,
            _record_created=True,
        )

    # --- identity / read models (no setters) ---

    @property
    def twin_id(self) -> DigitalTwinId:
        return self._twin_id

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def learner_state(self) -> LearnerState:
        return self._learner_state

    @property
    def concept_states(self) -> tuple[ConceptState, ...]:
        return tuple(self._concept_states)

    @property
    def misconception_states(self) -> tuple[MisconceptionState, ...]:
        return tuple(self._misconception_states)

    @property
    def evidence_history(self) -> tuple[EvidenceHistoryEntry, ...]:
        return tuple(self._evidence_history)

    @property
    def intervention_history(self) -> tuple[InterventionHistoryEntry, ...]:
        return tuple(self._intervention_history)

    @property
    def retention(self) -> RetentionState:
        return self._retention

    @property
    def confidence(self) -> ConfidenceProfile:
        return self._confidence

    @property
    def trajectory(self) -> LearningTrajectory:
        return self._trajectory

    @property
    def status(self) -> TwinStatus:
        return self._status

    def pull_events(self) -> list[DomainEvent]:
        """Return and clear pending domain events."""
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    def evidence_count(self) -> int:
        return len(self._evidence_history)

    def intervention_count(self) -> int:
        return len(self._intervention_history)

    def concept_count(self) -> int:
        return len(self._concept_states)

    def misconception_count(self) -> int:
        return len(self._misconception_states)

    def is_active(self) -> bool:
        return self._status is TwinStatus.ACTIVE

    def is_archived(self) -> bool:
        return self._status is TwinStatus.ARCHIVED

    def has_concept(self, concept_id: ConceptId | str) -> bool:
        key = concept_id.value if isinstance(concept_id, ConceptId) else concept_id
        return any(state.concept_id.value == key for state in self._concept_states)

    def concept_state_for(self, concept_id: ConceptId | str) -> ConceptState | None:
        key = concept_id.value if isinstance(concept_id, ConceptId) else concept_id
        for state in self._concept_states:
            if state.concept_id.value == key:
                return state
        return None

    def has_misconception(self, misconception_id: MisconceptionId | str) -> bool:
        key = (
            misconception_id.value
            if isinstance(misconception_id, MisconceptionId)
            else misconception_id
        )
        return any(
            state.misconception_id.value == key
            for state in self._misconception_states
        )

    def misconception_state_for(
        self, misconception_id: MisconceptionId | str
    ) -> MisconceptionState | None:
        key = (
            misconception_id.value
            if isinstance(misconception_id, MisconceptionId)
            else misconception_id
        )
        for state in self._misconception_states:
            if state.misconception_id.value == key:
                return state
        return None

    def has_evidence(self, evidence_id: EvidenceId | str) -> bool:
        key = evidence_id.value if isinstance(evidence_id, EvidenceId) else evidence_id
        return any(entry.evidence_id.value == key for entry in self._evidence_history)

    # --- behaviour ---

    def record_evidence(
        self,
        evidence_id: EvidenceId | str,
        evidence_type: EvidenceType,
        *,
        entry_id: str | EvidenceHistoryEntryId | None = None,
        concept_id: ConceptId | str | None = None,
        note: str | None = None,
    ) -> None:
        """Append evidence to Twin history without interpreting it."""
        TwinUpdatePolicy.assert_mutable(self._status, action="record_evidence")
        eid = (
            evidence_id
            if isinstance(evidence_id, EvidenceId)
            else EvidenceId(evidence_id)
        )
        cid: ConceptId | None
        if concept_id is None:
            cid = None
        elif isinstance(concept_id, ConceptId):
            cid = concept_id
        else:
            cid = ConceptId(concept_id)
        if isinstance(entry_id, EvidenceHistoryEntryId):
            hid = entry_id
        elif entry_id is None:
            hid = EvidenceHistoryEntryId(
                f"eh-{eid.value}-{TwinUpdatePolicy.next_evidence_sequence(self._evidence_history)}"
            )
        else:
            hid = EvidenceHistoryEntryId(entry_id)
        entry = EvidenceHistoryEntry(
            entry_id=hid,
            evidence_id=eid,
            evidence_type=evidence_type,
            sequence=TwinUpdatePolicy.next_evidence_sequence(self._evidence_history),
            concept_id=cid,
            note=note,
        )
        before = len(self._evidence_history)
        TwinUpdatePolicy.assert_evidence_appendable(self._evidence_history, entry)
        self._evidence_history.append(entry)
        TwinUpdatePolicy.assert_history_preserved(
            before, len(self._evidence_history), kind="evidence"
        )
        if cid is not None:
            self._bump_concept_evidence_count(cid)
        self._append_trajectory(
            TrajectoryPointKind.EVIDENCE,
            f"evidence:{eid.value}",
        )
        self._emit_updated(TwinUpdateKind.EVIDENCE_RECORDED)

    def record_intervention(
        self,
        intervention_ref: str,
        *,
        entry_id: str | InterventionHistoryEntryId | None = None,
        strategy_type: TeachingStrategyType | None = None,
        intention_type: TeachingIntentionType | None = None,
        concept_id: ConceptId | str | None = None,
        note: str | None = None,
    ) -> None:
        """Append an intervention memory entry — never rewrites history."""
        TwinUpdatePolicy.assert_mutable(self._status, action="record_intervention")
        cid: ConceptId | None
        if concept_id is None:
            cid = None
        elif isinstance(concept_id, ConceptId):
            cid = concept_id
        else:
            cid = ConceptId(concept_id)
        seq = TwinUpdatePolicy.next_intervention_sequence(self._intervention_history)
        if isinstance(entry_id, InterventionHistoryEntryId):
            hid = entry_id
        elif entry_id is None:
            hid = InterventionHistoryEntryId(f"ih-{intervention_ref}-{seq}")
        else:
            hid = InterventionHistoryEntryId(entry_id)
        entry = InterventionHistoryEntry(
            entry_id=hid,
            intervention_ref=intervention_ref,
            sequence=seq,
            strategy_type=strategy_type,
            intention_type=intention_type,
            concept_id=cid,
            note=note,
        )
        before = len(self._intervention_history)
        TwinUpdatePolicy.assert_intervention_appendable(
            self._intervention_history, entry
        )
        # Freeze prior entries by identity — never mutate historical rows.
        prior_snapshot = tuple(self._intervention_history)
        self._intervention_history.append(entry)
        TwinUpdatePolicy.assert_history_preserved(
            before, len(self._intervention_history), kind="intervention"
        )
        if tuple(self._intervention_history[:-1]) != prior_snapshot:
            raise EducationalInvariantViolation(
                "cannot rewrite historical interventions",
                invariant="EducationalDigitalTwin.intervention_history.immutable",
            )
        self._append_trajectory(
            TrajectoryPointKind.INTERVENTION,
            f"intervention:{intervention_ref}",
        )
        self._emit_updated(TwinUpdateKind.INTERVENTION_RECORDED)

    def update_mastery(
        self,
        concept_id: ConceptId | str,
        mastery: MasteryState,
        *,
        concept_state_id: str | ConceptStateId | None = None,
    ) -> None:
        """Record supplied mastery memory for a concept — does not diagnose."""
        TwinUpdatePolicy.assert_mutable(self._status, action="update_mastery")
        mastery = StateValidationPolicy.assert_mastery(mastery)
        cid = concept_id if isinstance(concept_id, ConceptId) else ConceptId(concept_id)
        existing = self.concept_state_for(cid)
        previous_band = (
            existing.mastery.band if existing is not None else MasteryBand.UNKNOWN
        )
        if existing is None:
            if isinstance(concept_state_id, ConceptStateId):
                state_id = concept_state_id
            elif concept_state_id is None:
                state_id = ConceptStateId(f"cs-{cid.value}")
            else:
                state_id = ConceptStateId(concept_state_id)
            state = ConceptState(
                concept_state_id=state_id,
                concept_id=cid,
                mastery=mastery,
                retention=RetentionState.unknown(),
            )
            self._concept_states = StateValidationPolicy.assert_concept_states(
                [*self._concept_states, state]
            )
        else:
            updated = existing.with_mastery(mastery)
            self._replace_concept_state(updated)
        self._append_trajectory(
            TrajectoryPointKind.MASTERY,
            f"mastery:{cid.value}:{mastery.band.value}",
        )
        self._pending_events.append(
            MasteryChanged(
                twin_id=self._twin_id,
                student_id=self._student_id,
                concept_id=cid,
                previous_band=previous_band,
                new_band=mastery.band,
            )
        )
        self._emit_updated(TwinUpdateKind.MASTERY_UPDATED)

    def update_retention(
        self,
        retention: RetentionState,
        *,
        concept_id: ConceptId | str | None = None,
    ) -> None:
        """Record supplied retention memory (twin-level or per-concept)."""
        TwinUpdatePolicy.assert_mutable(self._status, action="update_retention")
        retention = StateValidationPolicy.assert_retention(retention)
        if concept_id is None:
            self._retention = retention
            label = f"retention:{retention.band.value}"
        else:
            cid = (
                concept_id
                if isinstance(concept_id, ConceptId)
                else ConceptId(concept_id)
            )
            existing = self.concept_state_for(cid)
            if existing is None:
                state = ConceptState(
                    concept_state_id=ConceptStateId(f"cs-{cid.value}"),
                    concept_id=cid,
                    mastery=MasteryState.unknown(),
                    retention=retention,
                )
                self._concept_states = StateValidationPolicy.assert_concept_states(
                    [*self._concept_states, state]
                )
            else:
                self._replace_concept_state(existing.with_retention(retention))
            label = f"retention:{cid.value}:{retention.band.value}"
        self._append_trajectory(TrajectoryPointKind.RETENTION, label)
        self._emit_updated(TwinUpdateKind.RETENTION_UPDATED)

    def update_confidence(self, confidence: ConfidenceProfile) -> None:
        """Record supplied confidence profile memory."""
        TwinUpdatePolicy.assert_mutable(self._status, action="update_confidence")
        self._confidence = StateValidationPolicy.assert_confidence(confidence)
        self._append_trajectory(
            TrajectoryPointKind.CONFIDENCE,
            f"confidence:{confidence.overall.value}",
        )
        self._emit_updated(TwinUpdateKind.CONFIDENCE_UPDATED)

    def update_learner_activity(self, activity_status: LearnerActivityStatus) -> None:
        """Record learner activity posture on owned LearnerState."""
        TwinUpdatePolicy.assert_mutable(
            self._status, action="update_learner_activity"
        )
        StateTransitionIsValidSpecification().assert_learner_activity(
            self._learner_state.activity_status, activity_status
        )
        nxt = TwinUpdatePolicy.assert_learner_activity_transition(
            self._learner_state.activity_status, activity_status
        )
        self._learner_state = self._learner_state.with_activity_status(nxt)
        self._append_trajectory(
            TrajectoryPointKind.LEARNER,
            f"learner:{nxt.value}",
        )
        self._emit_updated(TwinUpdateKind.LEARNER_STATE_UPDATED)

    def record_misconception_state(
        self,
        misconception_id: MisconceptionId | str,
        presence: MisconceptionPresence,
        *,
        misconception_state_id: str | MisconceptionStateId | None = None,
        related_concept_id: ConceptId | str | None = None,
    ) -> None:
        """Remember misconception presence — does not diagnose."""
        TwinUpdatePolicy.assert_mutable(
            self._status, action="record_misconception_state"
        )
        mid = (
            misconception_id
            if isinstance(misconception_id, MisconceptionId)
            else MisconceptionId(misconception_id)
        )
        rid: ConceptId | None
        if related_concept_id is None:
            rid = None
        elif isinstance(related_concept_id, ConceptId):
            rid = related_concept_id
        else:
            rid = ConceptId(related_concept_id)
        existing = self.misconception_state_for(mid)
        if existing is None:
            if isinstance(misconception_state_id, MisconceptionStateId):
                state_id = misconception_state_id
            elif misconception_state_id is None:
                state_id = MisconceptionStateId(f"ms-{mid.value}")
            else:
                state_id = MisconceptionStateId(misconception_state_id)
            state = MisconceptionState(
                misconception_state_id=state_id,
                misconception_id=mid,
                presence=presence,
                related_concept_id=rid if rid is not None else None,
            )
            self._misconception_states = (
                StateValidationPolicy.assert_misconception_states(
                    [*self._misconception_states, state]
                )
            )
        else:
            StateTransitionIsValidSpecification().assert_misconception_presence(
                existing.presence, presence
            )
            TwinUpdatePolicy.assert_misconception_presence_transition(
                existing.presence, presence
            )
            updated = existing.with_presence(presence)
            if rid is not None and existing.related_concept_id != rid:
                updated = MisconceptionState(
                    misconception_state_id=existing.misconception_state_id,
                    misconception_id=existing.misconception_id,
                    presence=presence,
                    related_concept_id=rid,
                )
            self._replace_misconception_state(updated)
        self._append_trajectory(
            TrajectoryPointKind.MISCONCEPTION,
            f"misconception:{mid.value}:{presence.value}",
        )
        self._emit_updated(TwinUpdateKind.MISCONCEPTION_STATE_UPDATED)

    def archive(self, *, note: str | None = None) -> None:
        """Archive the Twin — history is preserved; further mutation is refused."""
        TwinUpdatePolicy.assert_can_archive(self._status)
        StateTransitionIsValidSpecification().assert_status(
            self._status, TwinStatus.ARCHIVED
        )
        TwinUpdatePolicy.assert_archive_note(note)
        before_evidence = len(self._evidence_history)
        before_interventions = len(self._intervention_history)
        self._status = TwinStatus.ARCHIVED
        TwinUpdatePolicy.assert_history_preserved(
            before_evidence, len(self._evidence_history), kind="evidence"
        )
        TwinUpdatePolicy.assert_history_preserved(
            before_interventions,
            len(self._intervention_history),
            kind="intervention",
        )
        label = "archived" if note is None else f"archived:{note}"
        self._append_trajectory(TrajectoryPointKind.ARCHIVE, label)
        self._emit_updated(TwinUpdateKind.ARCHIVED)

    # --- internals ---

    def _append_trajectory(self, kind: TrajectoryPointKind, label: str) -> None:
        point = TrajectoryPoint(
            sequence=self._trajectory.next_sequence(),
            kind=kind,
            label=label,
        )
        self._trajectory = TwinUpdatePolicy.assert_trajectory_append(
            self._trajectory, point
        )

    def _emit_updated(self, kind: TwinUpdateKind) -> None:
        self._pending_events.append(
            TwinUpdated(
                twin_id=self._twin_id,
                student_id=self._student_id,
                status=self._status,
                update_kind=kind,
                evidence_count=len(self._evidence_history),
                intervention_count=len(self._intervention_history),
                trajectory_length=self._trajectory.length(),
            )
        )

    def _replace_concept_state(self, updated: ConceptState) -> None:
        replaced: list[ConceptState] = []
        found = False
        for state in self._concept_states:
            if state.concept_id == updated.concept_id:
                replaced.append(updated)
                found = True
            else:
                replaced.append(state)
        if not found:
            raise EducationalInvariantViolation(
                "concept state not found for replacement",
                invariant="EducationalDigitalTwin.concept_states.replace",
            )
        self._concept_states = StateValidationPolicy.assert_concept_states(replaced)

    def _replace_misconception_state(self, updated: MisconceptionState) -> None:
        replaced: list[MisconceptionState] = []
        found = False
        for state in self._misconception_states:
            if state.misconception_id == updated.misconception_id:
                replaced.append(updated)
                found = True
            else:
                replaced.append(state)
        if not found:
            raise EducationalInvariantViolation(
                "misconception state not found for replacement",
                invariant="EducationalDigitalTwin.misconception_states.replace",
            )
        self._misconception_states = StateValidationPolicy.assert_misconception_states(
            replaced
        )

    def _bump_concept_evidence_count(self, concept_id: ConceptId) -> None:
        existing = self.concept_state_for(concept_id)
        if existing is None:
            state = ConceptState(
                concept_state_id=ConceptStateId(f"cs-{concept_id.value}"),
                concept_id=concept_id,
                mastery=MasteryState.unknown(),
                retention=RetentionState.unknown(),
                evidence_count=1,
            )
            self._concept_states = StateValidationPolicy.assert_concept_states(
                [*self._concept_states, state]
            )
            return
        self._replace_concept_state(
            existing.with_evidence_count(existing.evidence_count + 1)
        )
