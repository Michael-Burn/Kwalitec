"""End-to-end Educational Intelligence learning loop (Capability 4.9.10).

Proves Evidence → Coordinator → Knowledge → Composer → Repository → Provider →
Educational Intelligence → Recommendation without layer violations or
educational algorithm invention.
"""

from __future__ import annotations

import ast
import inspect
import logging
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import pytest

from app.application.learning_loop import (
    EducationalLearningLoop,
    LearningLoopContext,
    LearningLoopFailure,
    LearningLoopFailureReason,
    LearningLoopSuccess,
    build_version_1_0_learning_loop,
    build_version_1_0_twin_update_coordinator,
)
from app.application.orchestration import (
    EducationalExperience,
    EducationalOrchestrator,
    ProductContext,
)
from app.application.twin import (
    TwinAbsenceReason,
    TwinAbsent,
    TwinProvider,
    TwinRetrievalContext,
)
from app.application.twin_repository import (
    InMemoryTwinRepository,
    PersistAcknowledgement,
    TwinAuthorship,
    TwinPersistenceFailure,
    TwinPersistenceFailureReason,
    TwinScope,
)
from app.application.twin_update import (
    EducationalEvidencePackage,
    KnowledgeUpdateStrategy,
    ObservedEvent,
    TwinComposer,
    TwinUpdateCoordinator,
    TwinUpdateFailureReason,
)
from app.application.twin_update.outputs import DomainStrategyOutput
from app.domain.decision import Constraints, IntensityPosture
from app.domain.readiness import (
    CurriculumContext,
    CurriculumFormat,
    CurriculumTopicRef,
)
from app.domain.recommendation.recommendation import Recommendation
from app.domain.twin import (
    DigitalTwin,
    GoalState,
    IdentityState,
    KnowledgeState,
    TopicMasteryRecord,
)

APP_ROOT = Path(__file__).resolve().parents[2] / "app" / "application"
PIPELINE_SOURCE = APP_ROOT / "learning_loop" / "pipeline.py"

FORBIDDEN_ROOT_MODULES = frozenset(
    {
        "flask",
        "flask_login",
        "flask_sqlalchemy",
        "flask_wtf",
        "wtforms",
        "sqlalchemy",
    }
)

FORBIDDEN_PREFIXES = (
    "app.auth",
    "app.dashboard",
    "app.mission",
    "app.analytics",
    "app.models",
    "app.services",
)

FORBIDDEN_LOGIC_TOKENS = (
    "average(",
    "hybrid",
    "re_rank",
    "rerank",
    "priority_score",
    "pass_probability",
    "OverallPosture.MID",
    "OverallPosture.HIGH",
    "WarrantPosture.MEDIUM",
    "WarrantPosture.HIGH",
    "nominate_candidates",
    "_judge_factor",
    "mastery_belief =",
    "ReadinessAggregation.derive",
    "DecisionEngine.evaluate",
    "RecommendationEngine.package",
    "MissionIntelligence.compose",
)


def _ts() -> datetime:
    return datetime(2026, 7, 14, 12, 0, tzinfo=UTC)


def _identity(**overrides: object) -> IdentityState:
    defaults: dict[str, object] = {
        "student_id": "student-42",
        "curriculum_id": "7",
        "current_exam": "CS1",
        "target_sitting": date(2026, 9, 15),
    }
    defaults.update(overrides)
    return IdentityState.create(**defaults)  # type: ignore[arg-type]


def _twin(**overrides: object) -> DigitalTwin:
    identity = overrides.pop("identity", None)
    if identity is None:
        identity = _identity()
    goals = overrides.pop(
        "goals",
        GoalState.create(target_completion_date=date(2026, 9, 15)),
    )
    knowledge = overrides.pop("knowledge", KnowledgeState.create())
    return DigitalTwin.create(
        identity,  # type: ignore[arg-type]
        goals=goals,  # type: ignore[arg-type]
        knowledge=knowledge,  # type: ignore[arg-type]
        **overrides,  # type: ignore[arg-type]
    )


def _evidence(**overrides: object) -> EducationalEvidencePackage:
    defaults: dict[str, object] = {
        "evidence_id": "ev-loop-001",
        "student_id": "student-42",
        "evidence_timestamp": _ts(),
        "provenance": "observed:end_of_session",
        "study_plan_id": "plan-1",
        "curriculum_id": "7",
        "observed_events": (ObservedEvent.MISSION_COMPLETED,),
        "topic_id": "topic-a",
        "mission_id": "mission-1",
    }
    defaults.update(overrides)
    return EducationalEvidencePackage.create(**defaults)  # type: ignore[arg-type]


def _assessment_evidence(**overrides: object) -> EducationalEvidencePackage:
    defaults: dict[str, object] = {
        "evidence_id": "ev-loop-assess-001",
        "observed_events": (ObservedEvent.PRACTICE_COMPLETED,),
        "topic_id": "topic-a",
        "assessment_result": {"score": 8, "max_score": 10},
    }
    defaults.update(overrides)
    return _evidence(**defaults)


def _scope(**overrides: object) -> TwinScope:
    defaults: dict[str, object] = {
        "student_id": "student-42",
        "curriculum_id": "7",
        "sitting_id": None,
    }
    defaults.update(overrides)
    return TwinScope.create(**defaults)  # type: ignore[arg-type]


def _constraints() -> Constraints:
    return Constraints.create(
        available_minutes=60,
        intensity=IntensityPosture.AMPLE,
    )


def _curriculum() -> CurriculumContext:
    return CurriculumContext.create(
        "7",
        format=CurriculumFormat.V1,
        topics=[
            CurriculumTopicRef.create("topic-a", weight=0.5),
            CurriculumTopicRef.create("topic-b", weight=0.5),
        ],
    )


class _RecordingBuilder:
    def __init__(self, curriculum: CurriculumContext | None = None) -> None:
        self.curriculum = curriculum or _curriculum()
        self.calls: list[int | None] = []

    def build(self, curriculum_id: int | None) -> CurriculumContext:
        self.calls.append(curriculum_id)
        return self.curriculum


def _retrieval_context(**overrides: object) -> TwinRetrievalContext:
    defaults: dict[str, object] = {
        "curriculum_id": "7",
        "sitting_id": None,
        "surface_intent": "learning_loop",
    }
    defaults.update(overrides)
    return TwinRetrievalContext(**defaults)  # type: ignore[arg-type]


def _loop_context(**overrides: object) -> LearningLoopContext:
    defaults: dict[str, object] = {
        "student_id": "student-42",
        "curriculum_id": 7,
        "constraints": _constraints(),
        "twin_retrieval_context": _retrieval_context(),
        "product_context": ProductContext(surface_intent="learning_loop"),
        "twin_scope": _scope(),
    }
    defaults.update(overrides)
    return LearningLoopContext(**defaults)  # type: ignore[arg-type]


def _seed_birth(
    repo: InMemoryTwinRepository,
    twin: DigitalTwin | None = None,
    *,
    scope: TwinScope | None = None,
    snapshot_id: str = "birth-1",
) -> DigitalTwin:
    birth = twin if twin is not None else _twin()
    resolved = scope if scope is not None else _scope()
    ack = repo.persist_birth_twin(birth, scope=resolved, snapshot_id=snapshot_id)
    assert isinstance(ack, PersistAcknowledgement)
    return birth


def _build_loop(
    repo: InMemoryTwinRepository,
    *,
    builder: _RecordingBuilder | None = None,
    coordinator: TwinUpdateCoordinator | None = None,
    twin_provider: TwinProvider | None = None,
) -> EducationalLearningLoop:
    provider = (
        twin_provider
        if twin_provider is not None
        else TwinProvider(repository=repo)  # type: ignore[arg-type]
    )
    orch = EducationalOrchestrator(
        twin_provider=provider,
        curriculum_context_builder=builder or _RecordingBuilder(),
    )
    return build_version_1_0_learning_loop(
        repository=repo,
        twin_provider=provider,
        coordinator=coordinator,
        orchestrator=orch,
    )


class _FailingStrategy:
    @property
    def strategy_identity(self) -> str:
        return "Knowledge"

    def interpret(
        self,
        current_twin: DigitalTwin,
        evidence: EducationalEvidencePackage,
    ) -> DomainStrategyOutput:
        raise RuntimeError("strategy boom")


class _FailingComposer:
    def compose(
        self,
        current_twin: DigitalTwin,
        outputs: tuple[DomainStrategyOutput, ...],
    ) -> DigitalTwin:
        raise RuntimeError("composer boom")


class _FailingRepository:
    def __init__(self, inner: InMemoryTwinRepository) -> None:
        self._inner = inner
        self.persist_calls = 0

    def persist_birth_twin(self, *args: Any, **kwargs: Any) -> Any:
        return self._inner.persist_birth_twin(*args, **kwargs)

    def retrieve_current_twin(self, *args: Any, **kwargs: Any) -> Any:
        return self._inner.retrieve_current_twin(*args, **kwargs)

    def retrieve_snapshot_history(self, *args: Any, **kwargs: Any) -> Any:
        return self._inner.retrieve_snapshot_history(*args, **kwargs)

    def persist_successor_twin(
        self,
        twin: DigitalTwin,
        *,
        scope: TwinScope | None = None,
        snapshot_id: str | None = None,
        expected_current_snapshot_id: str | None = None,
        provenance: dict[str, Any] | None = None,
        persisted_at: datetime | None = None,
    ) -> TwinPersistenceFailure:
        self.persist_calls += 1
        return TwinPersistenceFailure(
            reason=TwinPersistenceFailureReason.UNAVAILABLE,
            scope=scope,
            detail="repository unavailable",
        )


class _AbsentAfterWriteProvider:
    """Retrieves Current Twin once, then TwinAbsent (post-persistence failure)."""

    def __init__(self, inner: TwinProvider) -> None:
        self._inner = inner
        self.calls = 0

    def retrieve(
        self,
        student_id: str | None,
        *,
        context: TwinRetrievalContext | None = None,
    ) -> DigitalTwin | TwinAbsent:
        self.calls += 1
        if self.calls == 1:
            return self._inner.retrieve(student_id, context=context)
        return TwinAbsent(
            reason=TwinAbsenceReason.UNAVAILABLE,
            student_id=student_id,
            detail="provider failure after persistence",
        )


class TestCompleteSuccessfulLearningLoop:
    def test_evidence_to_recommendation(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        repo = InMemoryTwinRepository()
        birth = _seed_birth(repo)
        builder = _RecordingBuilder()
        loop = _build_loop(repo, builder=builder)

        with caplog.at_level(
            logging.INFO, logger="app.application.learning_loop.pipeline"
        ):
            result = loop.execute(_evidence(), context=_loop_context())

        assert isinstance(result, LearningLoopSuccess)
        assert isinstance(result.experience, EducationalExperience)
        assert isinstance(result.recommendation, Recommendation)
        assert result.successor_twin.identity.student_id == birth.identity.student_id
        assert (
            result.twin_update.acknowledgement.authorship
            is TwinAuthorship.SUCCESSOR
        )
        assert builder.calls == [7]

        messages = [r.getMessage() for r in caplog.records]
        assert "Pipeline started" in messages
        assert "Evidence accepted" in messages
        assert "Coordinator completed" in messages
        assert "Provider retrieved" in messages
        assert "Educational Intelligence invoked" in messages
        assert "Pipeline completed" in messages


class TestPreserveKnowledgePath:
    def test_mission_evidence_preserves_knowledge(self) -> None:
        repo = InMemoryTwinRepository()
        prior = TopicMasteryRecord.create(
            "topic-a",
            mastery_belief=None,
            evidence_ids=("ev-prior",),
        )
        birth = _twin(knowledge=KnowledgeState.create(topic_mastery=[prior]))
        _seed_birth(repo, birth)
        loop = _build_loop(repo)

        result = loop.execute(
            _evidence(observed_events=(ObservedEvent.MISSION_COMPLETED,)),
            context=_loop_context(),
        )

        assert isinstance(result, LearningLoopSuccess)
        assert (
            result.successor_twin.knowledge.evidence_ids
            == birth.knowledge.evidence_ids
        )
        topic = next(
            r
            for r in result.successor_twin.knowledge.topic_mastery
            if r.topic_id == "topic-a"
        )
        assert topic.evidence_ids == ("ev-prior",)


class TestAssessmentUpdatePath:
    def test_assessment_evidence_updates_knowledge(self) -> None:
        repo = InMemoryTwinRepository()
        birth = _seed_birth(repo)
        loop = _build_loop(repo)
        evidence = _assessment_evidence()

        result = loop.execute(evidence, context=_loop_context())

        assert isinstance(result, LearningLoopSuccess)
        assert result.successor_twin.knowledge is not birth.knowledge
        assert evidence.evidence_id in result.successor_twin.knowledge.evidence_ids
        assert "topic-a" in {
            r.topic_id for r in result.successor_twin.knowledge.topic_mastery
        }
        assert isinstance(result.recommendation, Recommendation)


class TestRepositoryProviderIntelligence:
    def test_exactly_one_successor_persisted(self) -> None:
        repo = InMemoryTwinRepository()
        _seed_birth(repo)
        loop = _build_loop(repo)

        result = loop.execute(_assessment_evidence(), context=_loop_context())
        assert isinstance(result, LearningLoopSuccess)

        history = repo.retrieve_snapshot_history(_scope())
        assert not isinstance(history, TwinPersistenceFailure)
        assert len(history.snapshots) == 2
        assert history.snapshots[0].authorship is TwinAuthorship.BIRTH
        assert history.snapshots[1].authorship is TwinAuthorship.SUCCESSOR
        assert history.current_snapshot_id == history.snapshots[1].identity.snapshot_id
        assert (
            result.twin_update.acknowledgement.snapshot_id
            == history.current_snapshot_id
        )

    def test_provider_retrieves_successor_for_intelligence(self) -> None:
        repo = InMemoryTwinRepository()
        _seed_birth(repo)
        shared = TwinProvider(repository=repo)  # type: ignore[arg-type]
        call_log: list[str] = []

        class _LoggedProvider:
            def retrieve(
                self,
                student_id: str | None,
                *,
                context: TwinRetrievalContext | None = None,
            ) -> DigitalTwin | TwinAbsent:
                call_log.append("retrieve")
                return shared.retrieve(student_id, context=context)

        logged = _LoggedProvider()
        loop = EducationalLearningLoop(
            twin_provider=logged,  # type: ignore[arg-type]
            coordinator=build_version_1_0_twin_update_coordinator(repo),
            orchestrator=EducationalOrchestrator(
                twin_provider=logged,  # type: ignore[arg-type]
                curriculum_context_builder=_RecordingBuilder(),
            ),
            repository=repo,
        )

        result = loop.execute(_assessment_evidence(), context=_loop_context())
        assert isinstance(result, LearningLoopSuccess)
        # Current Twin + successor verification + Orchestrator retrieve.
        assert call_log.count("retrieve") >= 2
        assert result.experience.student_summary.student_id == "student-42"

    def test_intelligence_consumes_only_provider_twin(self) -> None:
        params = inspect.signature(
            EducationalOrchestrator.build_experience
        ).parameters
        assert "twin" not in params


class TestFailureBeforePersistence:
    def test_invalid_evidence_terminates(self) -> None:
        repo = InMemoryTwinRepository()
        _seed_birth(repo)
        loop = _build_loop(repo)

        result = loop.execute(None, context=_loop_context())
        assert isinstance(result, LearningLoopFailure)
        assert result.reason is LearningLoopFailureReason.INVALID_EVIDENCE

        history = repo.retrieve_snapshot_history(_scope())
        assert not isinstance(history, TwinPersistenceFailure)
        assert len(history.snapshots) == 1
        assert history.snapshots[0].authorship is TwinAuthorship.BIRTH

    def test_strategy_failure_no_persistence(self) -> None:
        repo = InMemoryTwinRepository()
        _seed_birth(repo)
        coordinator = TwinUpdateCoordinator(
            strategies=[_FailingStrategy()],  # type: ignore[list-item]
            composer=TwinComposer(),
            repository=repo,
        )
        loop = _build_loop(repo, coordinator=coordinator)

        result = loop.execute(_evidence(), context=_loop_context())
        assert isinstance(result, LearningLoopFailure)
        assert result.reason is LearningLoopFailureReason.TWIN_UPDATE_FAILED
        assert result.twin_update_failure is not None
        assert (
            result.twin_update_failure.reason
            is TwinUpdateFailureReason.STRATEGY_FAILURE
        )

        history = repo.retrieve_snapshot_history(_scope())
        assert not isinstance(history, TwinPersistenceFailure)
        assert len(history.snapshots) == 1

    def test_composer_failure_no_persistence(self) -> None:
        repo = InMemoryTwinRepository()
        _seed_birth(repo)
        coordinator = TwinUpdateCoordinator(
            strategies=[KnowledgeUpdateStrategy()],
            composer=_FailingComposer(),  # type: ignore[arg-type]
            repository=repo,
        )
        loop = _build_loop(repo, coordinator=coordinator)

        result = loop.execute(_evidence(), context=_loop_context())
        assert isinstance(result, LearningLoopFailure)
        assert result.reason is LearningLoopFailureReason.TWIN_UPDATE_FAILED
        assert result.twin_update_failure is not None
        assert (
            result.twin_update_failure.reason
            is TwinUpdateFailureReason.COMPOSER_FAILURE
        )

        history = repo.retrieve_snapshot_history(_scope())
        assert not isinstance(history, TwinPersistenceFailure)
        assert len(history.snapshots) == 1

    def test_repository_failure_no_successor(self) -> None:
        inner = InMemoryTwinRepository()
        _seed_birth(inner)
        failing = _FailingRepository(inner)
        provider = TwinProvider(repository=inner)  # type: ignore[arg-type]
        loop = EducationalLearningLoop(
            twin_provider=provider,
            coordinator=build_version_1_0_twin_update_coordinator(failing),
            orchestrator=EducationalOrchestrator(
                twin_provider=provider,
                curriculum_context_builder=_RecordingBuilder(),
            ),
            repository=failing,
        )

        result = loop.execute(_evidence(), context=_loop_context())
        assert isinstance(result, LearningLoopFailure)
        assert result.reason is LearningLoopFailureReason.TWIN_UPDATE_FAILED
        assert failing.persist_calls == 1

        history = inner.retrieve_snapshot_history(_scope())
        assert not isinstance(history, TwinPersistenceFailure)
        assert len(history.snapshots) == 1

    def test_missing_current_twin_terminates(self) -> None:
        repo = InMemoryTwinRepository()
        loop = _build_loop(repo)

        result = loop.execute(_evidence(), context=_loop_context())
        assert isinstance(result, LearningLoopFailure)
        assert result.reason is LearningLoopFailureReason.MISSING_CURRENT_TWIN


class TestFailureAfterPersistence:
    def test_provider_failure_after_persist_marks_ei_unavailable(self) -> None:
        repo = InMemoryTwinRepository()
        _seed_birth(repo)
        real_provider = TwinProvider(repository=repo)  # type: ignore[arg-type]
        absent_provider = _AbsentAfterWriteProvider(real_provider)
        loop = EducationalLearningLoop(
            twin_provider=absent_provider,  # type: ignore[arg-type]
            coordinator=build_version_1_0_twin_update_coordinator(repo),
            orchestrator=EducationalOrchestrator(
                twin_provider=real_provider,
                curriculum_context_builder=_RecordingBuilder(),
            ),
            repository=repo,
        )

        result = loop.execute(_assessment_evidence(), context=_loop_context())
        assert isinstance(result, LearningLoopFailure)
        assert result.reason is LearningLoopFailureReason.PROVIDER_FAILURE
        assert result.twin_update_success is not None

        history = repo.retrieve_snapshot_history(_scope())
        assert not isinstance(history, TwinPersistenceFailure)
        assert len(history.snapshots) == 2
        assert history.snapshots[1].authorship is TwinAuthorship.SUCCESSOR


class TestDeterminismAndImmutability:
    def test_deterministic_successor_knowledge(self) -> None:
        evidence = _assessment_evidence(evidence_id="ev-det-1")

        def _run() -> KnowledgeState:
            repo = InMemoryTwinRepository()
            _seed_birth(repo, _twin())
            loop = _build_loop(repo)
            result = loop.execute(evidence, context=_loop_context())
            assert isinstance(result, LearningLoopSuccess)
            return result.successor_twin.knowledge

        first = _run()
        second = _run()
        assert first.evidence_ids == second.evidence_ids
        assert {r.topic_id for r in first.topic_mastery} == {
            r.topic_id for r in second.topic_mastery
        }
        assert first.last_updated == second.last_updated

    def test_immutable_twin_history(self) -> None:
        repo = InMemoryTwinRepository()
        birth = _seed_birth(repo)
        birth_knowledge = birth.knowledge
        birth_id = id(birth)
        loop = _build_loop(repo)

        result = loop.execute(_assessment_evidence(), context=_loop_context())
        assert isinstance(result, LearningLoopSuccess)

        history = repo.retrieve_snapshot_history(_scope())
        assert not isinstance(history, TwinPersistenceFailure)
        assert history.snapshots[0].twin.knowledge is birth_knowledge
        assert id(history.snapshots[0].twin) == birth_id
        assert history.snapshots[0].twin is not result.successor_twin
        assert (
            history.snapshots[0].twin.knowledge
            is not result.successor_twin.knowledge
        )
        # Birth snapshot remains historically true after succession.
        assert history.snapshots[0].authorship is TwinAuthorship.BIRTH
        assert history.snapshots[1].authorship is TwinAuthorship.SUCCESSOR
        assert history.snapshots[0].identity.snapshot_id == "birth-1"


class TestWiring:
    def test_build_version_1_0_learning_loop_wires_knowledge_path(self) -> None:
        repo = InMemoryTwinRepository()
        _seed_birth(repo)
        loop = build_version_1_0_learning_loop(repository=repo)
        assert isinstance(loop, EducationalLearningLoop)
        assert isinstance(loop.coordinator, TwinUpdateCoordinator)
        assert isinstance(loop.twin_provider, TwinProvider)
        assert isinstance(loop.orchestrator, EducationalOrchestrator)

        loop = _build_loop(repo)
        result = loop.execute(_evidence(), context=_loop_context())
        assert isinstance(result, LearningLoopSuccess)


class TestArchitectureCompliance:
    def test_pipeline_framework_independent(self) -> None:
        tree = ast.parse(PIPELINE_SOURCE.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".", 1)[0]
                    assert root not in FORBIDDEN_ROOT_MODULES
            elif isinstance(node, ast.ImportFrom) and node.module:
                root = node.module.split(".", 1)[0]
                assert root not in FORBIDDEN_ROOT_MODULES
                for prefix in FORBIDDEN_PREFIXES:
                    assert not node.module.startswith(prefix)

    def test_pipeline_does_not_embed_educational_algorithms(self) -> None:
        src = PIPELINE_SOURCE.read_text(encoding="utf-8")
        for token in FORBIDDEN_LOGIC_TOKENS:
            assert token not in src, f"forbidden educational token: {token}"

    def test_write_read_firewall_preserved_in_twin_update(self) -> None:
        coordinator_src = (
            APP_ROOT / "twin_update" / "coordinator.py"
        ).read_text(encoding="utf-8")
        assert "EducationalOrchestrator" not in coordinator_src
        assert "RecommendationEngine" not in coordinator_src
        assert "DecisionEngine" not in coordinator_src
        assert "ReadinessAggregation" not in coordinator_src

    def test_learning_loop_does_not_call_strategy_interpret_directly(self) -> None:
        src = PIPELINE_SOURCE.read_text(encoding="utf-8")
        assert ".interpret(" not in src
        assert ".compose(" not in src
        assert "persist_successor_twin" not in src
        assert "KnowledgeUpdateStrategy().interpret" not in src

    def test_no_partial_success_type(self) -> None:
        src = PIPELINE_SOURCE.read_text(encoding="utf-8")
        assert "Partial" not in src
        assert "LearningLoopSuccess" in src
        assert "LearningLoopFailure" in src
