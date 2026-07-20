"""EducationalOrchestrator aggregate root — coordinates approved decisions.

Architecture Source
    EDUCATIONAL_ORCHESTRATION_MODEL.md
    ORCHESTRATION_INVARIANTS.md
Concept
    Educational Orchestrator
"""

from __future__ import annotations

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import LearningEpisodeId, OrchestratorId
from domain.education.orchestrator.entities.orchestration_plan import (
    OrchestrationPlan,
)
from domain.education.orchestrator.entities.orchestration_reference import (
    ApprovedDecisionReference,
    EpisodeReference,
    StrategyReference,
)
from domain.education.orchestrator.entities.orchestration_stage import (
    OrchestrationStage,
    OrchestrationStageId,
)
from domain.education.orchestrator.enums import OrchestrationStatus
from domain.education.orchestrator.events.orchestration_completed import (
    OrchestrationCompleted,
)
from domain.education.orchestrator.events.orchestration_paused import (
    OrchestrationPaused,
)
from domain.education.orchestrator.events.orchestration_started import (
    OrchestrationStarted,
)
from domain.education.orchestrator.policies.orchestration_policy import (
    OrchestrationPolicy,
)
from domain.education.orchestrator.policies.sequencing_policy import (
    SequencingPolicy,
)
from domain.education.orchestrator.value_objects.orchestration_progress import (
    OrchestrationProgress,
)
from domain.education.orchestrator.value_objects.orchestration_state import (
    OrchestrationState,
)

DomainEvent = OrchestrationStarted | OrchestrationCompleted | OrchestrationPaused


class EducationalOrchestrator:
    """Aggregate root for coordinating approved educational decisions.

    Owns approved decision references, teaching strategy references, learning
    episode references, execution stages, progress, and current orchestration
    state.

    Behaviour is exposed only through methods — no public setters.

    This aggregate coordinates. It does not reason, diagnose, reprioritize,
    or select strategies.
    """

    def __init__(
        self,
        orchestrator_id: OrchestratorId,
        student_id: str,
        decision_reference: ApprovedDecisionReference,
        strategy_references: list[StrategyReference]
        | tuple[StrategyReference, ...],
        plan: OrchestrationPlan,
        *,
        episode_references: list[EpisodeReference]
        | tuple[EpisodeReference, ...]
        | None = None,
        state: OrchestrationState | None = None,
        _record_created: bool = False,
    ) -> None:
        self._orchestrator_id = OrchestrationPolicy.assert_identity(orchestrator_id)
        self._student_id = OrchestrationPolicy.assert_student_id(student_id)
        self._decision_reference = OrchestrationPolicy.assert_decision_reference(
            decision_reference
        )
        self._strategy_references = list(
            OrchestrationPolicy.assert_strategy_references(strategy_references)
        )
        self._plan = OrchestrationPolicy.assert_plan(plan)
        self._episode_references = list(
            OrchestrationPolicy.assert_episode_references(episode_references or ())
        )
        self._state = OrchestrationPolicy.assert_state(
            state or OrchestrationState.planned()
        )
        self._pending_events: list[DomainEvent] = []
        _ = _record_created

    @classmethod
    def create(
        cls,
        orchestrator_id: OrchestratorId,
        student_id: str,
        decision_reference: ApprovedDecisionReference,
        strategy_references: list[StrategyReference]
        | tuple[StrategyReference, ...],
        plan: OrchestrationPlan,
        *,
        episode_references: list[EpisodeReference]
        | tuple[EpisodeReference, ...]
        | None = None,
    ) -> EducationalOrchestrator:
        """Factory: create a PLANNED orchestrator for an approved decision."""
        return cls(
            orchestrator_id=orchestrator_id,
            student_id=student_id,
            decision_reference=decision_reference,
            strategy_references=strategy_references,
            plan=plan,
            episode_references=episode_references,
            state=OrchestrationState.planned(),
            _record_created=True,
        )

    # --- identity / read models (no setters) ---

    @property
    def orchestrator_id(self) -> OrchestratorId:
        return self._orchestrator_id

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def decision_reference(self) -> ApprovedDecisionReference:
        return self._decision_reference

    @property
    def strategy_references(self) -> tuple[StrategyReference, ...]:
        return tuple(self._strategy_references)

    @property
    def episode_references(self) -> tuple[EpisodeReference, ...]:
        return tuple(self._episode_references)

    @property
    def plan(self) -> OrchestrationPlan:
        return self._plan

    @property
    def stages(self) -> tuple[OrchestrationStage, ...]:
        return self._plan.stages

    @property
    def state(self) -> OrchestrationState:
        return self._state

    @property
    def status(self) -> OrchestrationStatus:
        return self._state.status

    @property
    def progress(self) -> OrchestrationProgress:
        return SequencingPolicy.progress_of(self._plan.stages)

    def pull_events(self) -> list[DomainEvent]:
        """Return and clear pending domain events."""
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    # --- behaviour ---

    def start(self) -> None:
        """Begin orchestration: PLANNED → ACTIVE; activate first stage."""
        OrchestrationPolicy.assert_can_start(self._state.status)
        stages = list(self._plan.stages)
        stages = SequencingPolicy.activate_first_pending(stages)
        first_active = next(stage for stage in stages if stage.is_active())
        self._plan = self._plan.with_stages(stages)
        self._state = OrchestrationState.active(first_active.stage_id)
        self._pending_events.append(
            OrchestrationStarted(
                orchestrator_id=self._orchestrator_id,
                student_id=self._student_id,
                decision_id=self._decision_reference.decision_id,
                first_stage_id=first_active.stage_id,
                stage_count=len(stages),
            )
        )

    def advance(self) -> OrchestrationStage:
        """Complete the active stage and activate the next pending stage.

        Returns the stage that was completed. Raises when required sequence
        would be skipped or no stage remains.
        """
        OrchestrationPolicy.assert_can_advance(self._state.status)
        stages = list(self._plan.stages)
        current = SequencingPolicy.assert_can_advance(stages)
        if current.is_pending():
            activated = current.activate()
            stages = SequencingPolicy.replace_stage(stages, activated)
            current = activated
        completed = current.complete()
        stages = SequencingPolicy.replace_stage(stages, completed)

        try:
            nxt = SequencingPolicy.assert_can_advance(stages)
        except EducationalInvariantViolation as exc:
            if exc.invariant == "SequencingPolicy.exhausted":
                self._plan = self._plan.with_stages(stages)
                self._state = OrchestrationState(
                    status=OrchestrationStatus.ACTIVE,
                    current_stage_id=None,
                )
                return completed
            raise
        if nxt.is_pending():
            stages = SequencingPolicy.replace_stage(stages, nxt.activate())
            nxt = next(s for s in stages if s.stage_id == nxt.stage_id)
        self._plan = self._plan.with_stages(stages)
        self._state = OrchestrationState.active(nxt.stage_id)
        return completed

    def pause(self, reason: str) -> None:
        """Suspend active orchestration coordination."""
        OrchestrationPolicy.assert_can_pause(self._state.status)
        pause_reason = OrchestrationPolicy.assert_pause_reason(reason)
        self._state = OrchestrationState.paused(
            pause_reason,
            current_stage_id=self._state.current_stage_id,
        )
        self._pending_events.append(
            OrchestrationPaused(
                orchestrator_id=self._orchestrator_id,
                student_id=self._student_id,
                reason=pause_reason,
                current_stage_id=self._state.current_stage_id,
                completed_stages=self.progress.completed_stages,
            )
        )

    def resume(self) -> None:
        """Resume a paused orchestration; forbids completed turns."""
        OrchestrationPolicy.assert_can_resume(self._state.status)
        current_stage_id = self._state.current_stage_id
        if current_stage_id is None:
            # Resume after stages exhausted but not yet completed — unlawful
            # unless an active stage exists, or re-derive from stages.
            active = next(
                (stage for stage in self._plan.stages if stage.is_active()),
                None,
            )
            if active is None:
                raise EducationalInvariantViolation(
                    "cannot resume without an active or pending stage",
                    invariant="EducationalOrchestrator.resume.no_stage",
                )
            current_stage_id = active.stage_id
        else:
            SequencingPolicy.assert_stage_belongs(
                self._plan.stages, current_stage_id
            )
        self._state = OrchestrationState.active(current_stage_id)

    def complete(self) -> None:
        """Terminate orchestration correctly when required stages are done."""
        OrchestrationPolicy.assert_can_complete(
            self._state.status,
            required_stages_complete=SequencingPolicy.required_stages_complete(
                self._plan.stages
            ),
        )
        progress = self.progress
        self._state = OrchestrationState.completed()
        self._pending_events.append(
            OrchestrationCompleted(
                orchestrator_id=self._orchestrator_id,
                student_id=self._student_id,
                decision_id=self._decision_reference.decision_id,
                completed_stages=progress.completed_stages,
                evidence_collection_points_reached=(
                    progress.evidence_collection_points_reached
                ),
                episode_count=len(self._episode_references),
            )
        )

    def register_episode(self, episode_id: LearningEpisodeId) -> None:
        """Coordinate Learning Episode creation against the active stage.

        Records an opaque episode reference. Does not construct pedagogy,
        diagnose, or select strategies.
        """
        OrchestrationPolicy.assert_can_advance(self._state.status)
        if self._state.current_stage_id is None:
            raise EducationalInvariantViolation(
                "cannot register an episode without an active stage",
                invariant="EducationalOrchestrator.register_episode.no_stage",
            )
        stage = SequencingPolicy.assert_stage_belongs(
            self._plan.stages, self._state.current_stage_id
        )
        OrchestrationPolicy.assert_episode_creation_stage(stage)
        reference = EpisodeReference(episode_id=episode_id)
        existing = OrchestrationPolicy.assert_episode_references(
            [*self._episode_references, reference]
        )
        bound = stage.bind_episode(episode_id)
        stages = SequencingPolicy.replace_stage(list(self._plan.stages), bound)
        self._plan = self._plan.with_stages(stages)
        self._episode_references = list(existing)

    # --- queries ---

    def stage_by_id(self, stage_id: OrchestrationStageId) -> OrchestrationStage:
        return SequencingPolicy.assert_stage_belongs(self._plan.stages, stage_id)

    def has_strategy(self, strategy_id: object) -> bool:
        return any(
            ref.strategy_id == strategy_id for ref in self._strategy_references
        )

    def has_episode(self, episode_id: LearningEpisodeId) -> bool:
        return any(
            ref.episode_id == episode_id for ref in self._episode_references
        )

    def evidence_collection_stages(self) -> tuple[OrchestrationStage, ...]:
        return tuple(
            stage
            for stage in SequencingPolicy.ordered(self._plan.stages)
            if stage.is_evidence_collection_point()
        )

    def is_planned(self) -> bool:
        return self._state.is_planned()

    def is_active(self) -> bool:
        return self._state.is_active()

    def is_paused(self) -> bool:
        return self._state.is_paused()

    def is_completed(self) -> bool:
        return self._state.is_completed()

    def is_terminal(self) -> bool:
        return self._state.is_terminal()

    def strategy_count(self) -> int:
        return len(self._strategy_references)

    def episode_count(self) -> int:
        return len(self._episode_references)

    def stage_count(self) -> int:
        return self._plan.stage_count()

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True
        if not isinstance(other, EducationalOrchestrator):
            return NotImplemented
        return self._orchestrator_id == other._orchestrator_id

    def __hash__(self) -> int:
        return hash((type(self), self._orchestrator_id))

    def __repr__(self) -> str:
        return (
            f"EducationalOrchestrator(orchestrator_id={self._orchestrator_id!r}, "
            f"status={self._state.status!r})"
        )
