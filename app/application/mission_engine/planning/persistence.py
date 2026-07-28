"""Planning persistence — append-only store for Twin→Mission plans.

No Alembic migrations. Stores planning batches / candidates / events
in-process for deterministic replay and duplicate-request protection.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from threading import RLock

from app.domain.mission.planning.batch import PlanningBatch
from app.domain.mission.planning.candidate import MissionCandidateProjection
from app.domain.mission.planning.plan import StudyMissionPlan
from app.domain.mission.planning.result import PlanningEvent, PlanningResult


@dataclass
class _TwinPlanningLedger:
    """Append-only ledger for one twin."""

    twin_id: str
    candidates_by_id: dict[str, MissionCandidateProjection] = field(
        default_factory=dict
    )
    batches: list[PlanningBatch] = field(default_factory=list)
    plans: list[StudyMissionPlan] = field(default_factory=list)
    events: list[PlanningEvent] = field(default_factory=list)
    request_ids: set[str] = field(default_factory=set)
    versions: list[str] = field(default_factory=list)


class PlanningPersistenceService:
    """Deterministic, idempotent planning store with replay support."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._ledgers: dict[str, _TwinPlanningLedger] = {}

    def _ledger(self, *, twin_id: str) -> _TwinPlanningLedger:
        ledger = self._ledgers.get(twin_id)
        if ledger is None:
            ledger = _TwinPlanningLedger(twin_id=twin_id)
            self._ledgers[twin_id] = ledger
        return ledger

    def existing_candidate_ids(self, *, twin_id: str) -> frozenset[str]:
        with self._lock:
            ledger = self._ledgers.get(twin_id)
            if ledger is None:
                return frozenset()
            return frozenset(ledger.candidates_by_id.keys())

    def existing_request_ids(self, *, twin_id: str) -> frozenset[str]:
        with self._lock:
            ledger = self._ledgers.get(twin_id)
            if ledger is None:
                return frozenset()
            return frozenset(ledger.request_ids)

    def get_candidate(
        self, *, twin_id: str, candidate_id: str
    ) -> MissionCandidateProjection | None:
        with self._lock:
            ledger = self._ledgers.get(twin_id)
            if ledger is None:
                return None
            return ledger.candidates_by_id.get(candidate_id)

    def list_candidates(
        self, *, twin_id: str
    ) -> tuple[MissionCandidateProjection, ...]:
        with self._lock:
            ledger = self._ledgers.get(twin_id)
            if ledger is None:
                return ()
            return tuple(
                ledger.candidates_by_id[cid]
                for cid in sorted(ledger.candidates_by_id.keys())
            )

    def list_events(self, *, twin_id: str) -> tuple[PlanningEvent, ...]:
        with self._lock:
            ledger = self._ledgers.get(twin_id)
            if ledger is None:
                return ()
            return tuple(ledger.events)

    def list_batches(self, *, twin_id: str) -> tuple[PlanningBatch, ...]:
        with self._lock:
            ledger = self._ledgers.get(twin_id)
            if ledger is None:
                return ()
            return tuple(ledger.batches)

    def version_history(self, *, twin_id: str) -> tuple[str, ...]:
        with self._lock:
            ledger = self._ledgers.get(twin_id)
            if ledger is None:
                return ()
            return tuple(ledger.versions)

    def persist(self, result: PlanningResult) -> PlanningResult:
        """Append planning result. Idempotent for identical candidate ids."""
        context = result.context
        with self._lock:
            ledger = self._ledger(twin_id=context.twin_id)
            for cand in result.batch.candidates:
                ledger.candidates_by_id[cand.candidate_id] = cand
            ledger.batches.append(result.batch)
            ledger.plans.append(result.study_mission_plan)
            ledger.events.extend(result.events)
            ledger.request_ids.add(context.mission_request_id)
            ledger.versions.append(result.study_mission_plan.plan_id)
            return result

    def snapshot(self, *, twin_id: str) -> dict:
        """Deterministic serialisable snapshot for replay comparison."""
        with self._lock:
            ledger = self._ledgers.get(twin_id)
            if ledger is None:
                return {
                    "twin_id": twin_id,
                    "candidates": [],
                    "batch_ids": [],
                    "event_kinds": [],
                    "request_ids": [],
                    "versions": [],
                }
            return {
                "twin_id": twin_id,
                "candidates": [
                    {
                        "candidate_id": c.candidate_id,
                        "activity_type": c.activity_type.value,
                        "concept_id": c.concept_id,
                        "decision_id": c.decision_id,
                        "priority_score": c.priority_score,
                        "planning_version": c.planning_version,
                        "provenance": dict(c.provenance),
                    }
                    for c in sorted(
                        ledger.candidates_by_id.values(),
                        key=lambda item: item.candidate_id,
                    )
                ],
                "batch_ids": [b.batch_id for b in ledger.batches],
                "event_kinds": [e.kind.value for e in ledger.events],
                "request_ids": sorted(ledger.request_ids),
                "versions": list(ledger.versions),
            }

    def clear(self) -> None:
        with self._lock:
            self._ledgers.clear()

    def clone_empty(self) -> PlanningPersistenceService:
        """Fresh store for isolated replay runs."""
        return PlanningPersistenceService()

    def deep_copy(self) -> PlanningPersistenceService:
        """Copy store state (tests / diagnostics)."""
        clone = PlanningPersistenceService()
        with self._lock:
            clone._ledgers = deepcopy(self._ledgers)
        return clone
