"""Tests for TwinUpdateCoordinator (Capability 4.9.7).

Covers happy path, missing Current Twin, invalid Evidence, Strategy / Composer /
Repository failures, dependency injection, operational logging, immutability,
framework independence, and absence of educational reasoning / Twin mutation.
"""

from __future__ import annotations

import ast
import logging
from dataclasses import FrozenInstanceError
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import pytest

from app.application.twin_repository import (
    InMemoryTwinRepository,
    PersistAcknowledgement,
    TwinAuthorship,
    TwinPersistenceFailure,
    TwinPersistenceFailureReason,
    TwinScope,
)
from app.application.twin_update import (
    DomainStrategyOutput,
    EducationalEvidencePackage,
    ObservedEvent,
    TwinUpdateCoordinator,
    TwinUpdateFailure,
    TwinUpdateFailureReason,
    TwinUpdateSuccess,
)
from app.domain.twin import DigitalTwin, GoalState, IdentityState, KnowledgeState

TWIN_UPDATE_ROOT = (
    Path(__file__).resolve().parents[2] / "app" / "application" / "twin_update"
)

FORBIDDEN_ROOT_MODULES = frozenset(
    {
        "flask",
        "flask_login",
        "flask_sqlalchemy",
        "flask_wtf",
        "wtforms",
    }
)

FORBIDDEN_PREFIXES = (
    "app.auth",
    "app.dashboard",
    "app.mission",
    "app.analytics",
    "app.models",
    "app.domain.readiness",
    "app.domain.decision",
    "app.domain.recommendation",
    "app.domain.mission",
)

FORBIDDEN_LOGIC_TOKENS = (
    "mastery_belief",
    "average(",
    "pass_probability",
    "OverallPosture",
    "WarrantPosture",
    "nominate_candidates",
    "DecisionEngine",
    "RecommendationEngine",
    "MissionIntelligence",
    "ReadinessAggregation",
    "hybrid",
    "re_rank",
    "rerank",
)


# ═══════════════════════════════════════════════════════════════════════════════
# Fixtures / fakes
# ═══════════════════════════════════════════════════════════════════════════════


def _identity(**overrides: object) -> IdentityState:
    defaults: dict[str, object] = {
        "student_id": "student-42",
        "curriculum_id": "CS1-2026",
        "current_exam": "CS1",
        "target_sitting": date(2026, 9, 15),
    }
    defaults.update(overrides)
    return IdentityState.create(**defaults)  # type: ignore[arg-type]


def _twin(**overrides: object) -> DigitalTwin:
    identity = overrides.pop("identity", None)
    if identity is None:
        identity = _identity()
    goals = overrides.pop("goals", GoalState.create())
    knowledge = overrides.pop("knowledge", KnowledgeState.create())
    return DigitalTwin.create(
        identity,  # type: ignore[arg-type]
        goals=goals,  # type: ignore[arg-type]
        knowledge=knowledge,  # type: ignore[arg-type]
        **overrides,  # type: ignore[arg-type]
    )


def _evidence(**overrides: object) -> EducationalEvidencePackage:
    defaults: dict[str, object] = {
        "evidence_id": "ev-001",
        "student_id": "student-42",
        "evidence_timestamp": datetime(2026, 7, 14, 10, 0, tzinfo=UTC),
        "provenance": "observed:end_of_session",
        "curriculum_id": "CS1-2026",
        "study_plan_id": "plan-1",
        "topic_id": "topic-a",
        "observed_events": (ObservedEvent.MISSION_COMPLETED,),
    }
    defaults.update(overrides)
    return EducationalEvidencePackage.create(**defaults)  # type: ignore[arg-type]


def _scope() -> TwinScope:
    return TwinScope.create("student-42", curriculum_id="CS1-2026")


class _FakeStrategy:
    """Twin Update Strategy double — no educational algorithms."""

    def __init__(
        self,
        identity: str = "Knowledge",
        *,
        owned_domain: str = "knowledge",
        preserved: bool = False,
        error: Exception | None = None,
        unlawful_output: object | None = None,
        mutate_twin: bool = False,
        mutate_evidence: bool = False,
    ) -> None:
        self._identity = identity
        self._owned_domain = owned_domain
        self._preserved = preserved
        self._error = error
        self._unlawful_output = unlawful_output
        self._mutate_twin = mutate_twin
        self._mutate_evidence = mutate_evidence
        self.calls: list[tuple[DigitalTwin, EducationalEvidencePackage]] = []

    @property
    def strategy_identity(self) -> str:
        return self._identity

    def interpret(
        self,
        current_twin: DigitalTwin,
        evidence: EducationalEvidencePackage,
    ) -> DomainStrategyOutput:
        self.calls.append((current_twin, evidence))
        if self._mutate_twin:
            object.__setattr__(current_twin.identity, "student_id", "mutated")
        if self._mutate_evidence:
            object.__setattr__(evidence, "evidence_id", "mutated")
        if self._error is not None:
            raise self._error
        if self._unlawful_output is not None:
            return self._unlawful_output  # type: ignore[return-value]
        return DomainStrategyOutput.create(
            self._identity,
            self._owned_domain,
            domain_contribution=current_twin.knowledge,
            preserved=self._preserved,
        )


class _FakeComposer:
    """Twin Composer double — assembly stub only."""

    def __init__(
        self,
        *,
        error: Exception | None = None,
        unlawful: bool = False,
        successor: DigitalTwin | None = None,
    ) -> None:
        self._error = error
        self._unlawful = unlawful
        self._successor = successor
        self.calls: list[tuple[DigitalTwin, tuple[DomainStrategyOutput, ...]]] = []

    def compose(
        self,
        current_twin: DigitalTwin,
        outputs: tuple[DomainStrategyOutput, ...],
    ) -> DigitalTwin:
        self.calls.append((current_twin, outputs))
        if self._error is not None:
            raise self._error
        if self._unlawful:
            return "not-a-twin"  # type: ignore[return-value]
        if self._successor is not None:
            return self._successor
        # Carry-forward succession snapshot (no educational densification).
        return DigitalTwin.create(
            current_twin.identity,
            goals=current_twin.goals,
            knowledge=current_twin.knowledge,
            memory=current_twin.memory,
            behaviour=current_twin.behaviour,
            performance=current_twin.performance,
            predictions=current_twin.predictions,
        )


class _FakeRepository:
    """Repository double with controllable persist outcomes."""

    def __init__(
        self,
        *,
        failure: TwinPersistenceFailure | None = None,
        error: Exception | None = None,
        unrecognised: bool = False,
    ) -> None:
        self._failure = failure
        self._error = error
        self._unrecognised = unrecognised
        self.calls: list[DigitalTwin] = []

    def persist_successor_twin(
        self,
        twin: DigitalTwin,
        *,
        scope: TwinScope | None = None,
        snapshot_id: str | None = None,
        expected_current_snapshot_id: str | None = None,
        provenance: dict[str, Any] | None = None,
        persisted_at: datetime | None = None,
    ) -> PersistAcknowledgement | TwinPersistenceFailure | str:
        self.calls.append(twin)
        if self._error is not None:
            raise self._error
        if self._failure is not None:
            return self._failure
        if self._unrecognised:
            return "unexpected"
        resolved = scope if scope is not None else TwinScope.create(
            twin.identity.student_id,
            curriculum_id=twin.identity.curriculum_id,
        )
        return PersistAcknowledgement(
            snapshot_id=snapshot_id or "snap-succ-1",
            sequence=2,
            scope=resolved,
            authorship=TwinAuthorship.SUCCESSOR,
        )


def _coordinator(
    *,
    strategies: list[_FakeStrategy] | None = None,
    composer: _FakeComposer | None = None,
    repository: _FakeRepository | InMemoryTwinRepository | None = None,
) -> TwinUpdateCoordinator:
    return TwinUpdateCoordinator(
        strategies=strategies if strategies is not None else [_FakeStrategy()],
        composer=composer if composer is not None else _FakeComposer(),
        repository=repository if repository is not None else _FakeRepository(),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Happy path
# ═══════════════════════════════════════════════════════════════════════════════


class TestHappyPath:
    def test_orchestrates_strategy_composer_repository(self) -> None:
        strategy = _FakeStrategy("Knowledge")
        composer = _FakeComposer()
        repository = _FakeRepository()
        coord = _coordinator(
            strategies=[strategy],
            composer=composer,
            repository=repository,
        )
        twin = _twin()
        evidence = _evidence()

        result = coord.update(twin, evidence)

        assert isinstance(result, TwinUpdateSuccess)
        assert result.strategy_identities == ("Knowledge",)
        assert result.acknowledgement.authorship is TwinAuthorship.SUCCESSOR
        assert len(strategy.calls) == 1
        assert len(composer.calls) == 1
        assert len(repository.calls) == 1
        assert composer.calls[0][1][0].strategy_identity == "Knowledge"
        assert repository.calls[0] is result.successor_twin

    def test_preservation_strategy_output_continues(self) -> None:
        coord = _coordinator(strategies=[_FakeStrategy(preserved=True)])
        result = coord.update(_twin(), _evidence())
        assert isinstance(result, TwinUpdateSuccess)

    def test_multiple_strategies_collected_before_composer(self) -> None:
        knowledge = _FakeStrategy("Knowledge", owned_domain="knowledge")
        behaviour = _FakeStrategy("Behaviour", owned_domain="behaviour")
        composer = _FakeComposer()
        coord = _coordinator(
            strategies=[knowledge, behaviour],
            composer=composer,
        )

        result = coord.update(_twin(), _evidence())

        assert isinstance(result, TwinUpdateSuccess)
        assert result.strategy_identities == ("Knowledge", "Behaviour")
        assert len(composer.calls[0][1]) == 2

    def test_in_memory_repository_integration(self) -> None:
        repo = InMemoryTwinRepository()
        twin = _twin()
        scope = _scope()
        birth = repo.persist_birth_twin(twin, scope=scope, snapshot_id="birth-1")
        assert isinstance(birth, PersistAcknowledgement)

        coord = _coordinator(repository=repo)
        result = coord.update(twin, _evidence(), scope=scope)

        assert isinstance(result, TwinUpdateSuccess)
        loaded = repo.retrieve_current_twin(scope)
        assert isinstance(loaded, DigitalTwin)
        assert loaded.identity.student_id == "student-42"


# ═══════════════════════════════════════════════════════════════════════════════
# Missing Current Twin
# ═══════════════════════════════════════════════════════════════════════════════


class TestMissingCurrentTwin:
    def test_none_current_twin_fails(self) -> None:
        result = _coordinator().update(None, _evidence())
        assert isinstance(result, TwinUpdateFailure)
        assert result.reason is TwinUpdateFailureReason.MISSING_CURRENT_TWIN

    def test_does_not_invoke_collaborators_when_twin_missing(self) -> None:
        strategy = _FakeStrategy()
        composer = _FakeComposer()
        repository = _FakeRepository()
        coord = _coordinator(
            strategies=[strategy],
            composer=composer,
            repository=repository,
        )

        coord.update(None, _evidence())

        assert strategy.calls == []
        assert composer.calls == []
        assert repository.calls == []


# ═══════════════════════════════════════════════════════════════════════════════
# Invalid Evidence
# ═══════════════════════════════════════════════════════════════════════════════


class TestInvalidEvidence:
    def test_none_evidence_fails(self) -> None:
        result = _coordinator().update(_twin(), None)
        assert isinstance(result, TwinUpdateFailure)
        assert result.reason is TwinUpdateFailureReason.INVALID_EVIDENCE

    def test_student_mismatch_fails(self) -> None:
        result = _coordinator().update(
            _twin(),
            _evidence(student_id="other-student"),
        )
        assert isinstance(result, TwinUpdateFailure)
        assert result.reason is TwinUpdateFailureReason.INVALID_EVIDENCE

    def test_curriculum_mismatch_fails(self) -> None:
        result = _coordinator().update(
            _twin(),
            _evidence(curriculum_id="OTHER-CURRICULUM"),
        )
        assert isinstance(result, TwinUpdateFailure)
        assert result.reason is TwinUpdateFailureReason.INVALID_EVIDENCE

    def test_provenance_stripped_create_rejects(self) -> None:
        with pytest.raises(ValueError, match="provenance"):
            EducationalEvidencePackage.create(
                "ev-1",
                "student-42",
                datetime(2026, 7, 14, tzinfo=UTC),
                "   ",
                study_plan_id="plan-1",
                curriculum_id="CS1-2026",
                observed_events=(ObservedEvent.SESSION_ENDED_MANUAL,),
            )

    def test_does_not_invoke_strategy_when_evidence_invalid(self) -> None:
        strategy = _FakeStrategy()
        coord = _coordinator(strategies=[strategy])
        coord.update(_twin(), None)
        assert strategy.calls == []


# ═══════════════════════════════════════════════════════════════════════════════
# Strategy / Composer / Repository failures
# ═══════════════════════════════════════════════════════════════════════════════


class TestStrategyFailure:
    def test_strategy_exception_fails_honestly(self) -> None:
        coord = _coordinator(
            strategies=[_FakeStrategy(error=RuntimeError("strategy boom"))]
        )
        result = coord.update(_twin(), _evidence())
        assert isinstance(result, TwinUpdateFailure)
        assert result.reason is TwinUpdateFailureReason.STRATEGY_FAILURE
        assert result.detail is not None
        assert "strategy boom" in result.detail

    def test_unlawful_strategy_output_fails(self) -> None:
        coord = _coordinator(
            strategies=[_FakeStrategy(unlawful_output={"patch": True})]
        )
        result = coord.update(_twin(), _evidence())
        assert isinstance(result, TwinUpdateFailure)
        assert result.reason is TwinUpdateFailureReason.STRATEGY_FAILURE

    def test_empty_strategy_catalogue_fails(self) -> None:
        coord = TwinUpdateCoordinator(
            strategies=[],
            composer=_FakeComposer(),
            repository=_FakeRepository(),
        )
        result = coord.update(_twin(), _evidence())
        assert isinstance(result, TwinUpdateFailure)
        assert result.reason is TwinUpdateFailureReason.STRATEGY_FAILURE

    def test_strategy_failure_skips_composer_and_repository(self) -> None:
        composer = _FakeComposer()
        repository = _FakeRepository()
        coord = _coordinator(
            strategies=[_FakeStrategy(error=RuntimeError("fail"))],
            composer=composer,
            repository=repository,
        )
        coord.update(_twin(), _evidence())
        assert composer.calls == []
        assert repository.calls == []


class TestComposerFailure:
    def test_composer_exception_fails_honestly(self) -> None:
        coord = _coordinator(composer=_FakeComposer(error=RuntimeError("compose boom")))
        result = coord.update(_twin(), _evidence())
        assert isinstance(result, TwinUpdateFailure)
        assert result.reason is TwinUpdateFailureReason.COMPOSER_FAILURE
        assert result.detail is not None
        assert "compose boom" in result.detail

    def test_composer_unlawful_return_fails(self) -> None:
        coord = _coordinator(composer=_FakeComposer(unlawful=True))
        result = coord.update(_twin(), _evidence())
        assert isinstance(result, TwinUpdateFailure)
        assert result.reason is TwinUpdateFailureReason.COMPOSER_FAILURE

    def test_composer_failure_skips_repository(self) -> None:
        repository = _FakeRepository()
        coord = _coordinator(
            composer=_FakeComposer(error=RuntimeError("fail")),
            repository=repository,
        )
        coord.update(_twin(), _evidence())
        assert repository.calls == []


class TestRepositoryFailure:
    def test_repository_persistence_failure_fails_honestly(self) -> None:
        failure = TwinPersistenceFailure(
            reason=TwinPersistenceFailureReason.UNAVAILABLE,
            detail="Twin storage unavailable",
        )
        coord = _coordinator(repository=_FakeRepository(failure=failure))
        result = coord.update(_twin(), _evidence())
        assert isinstance(result, TwinUpdateFailure)
        assert result.reason is TwinUpdateFailureReason.REPOSITORY_FAILURE
        assert result.detail is not None
        assert "unavailable" in result.detail.lower()

    def test_repository_exception_fails_honestly(self) -> None:
        coord = _coordinator(
            repository=_FakeRepository(error=RuntimeError("persist boom"))
        )
        result = coord.update(_twin(), _evidence())
        assert isinstance(result, TwinUpdateFailure)
        assert result.reason is TwinUpdateFailureReason.REPOSITORY_FAILURE

    def test_never_fabricates_successor_on_repository_failure(self) -> None:
        failure = TwinPersistenceFailure(
            reason=TwinPersistenceFailureReason.UNAVAILABLE,
            detail="down",
        )
        coord = _coordinator(repository=_FakeRepository(failure=failure))
        result = coord.update(_twin(), _evidence())
        assert isinstance(result, TwinUpdateFailure)
        assert not hasattr(result, "successor_twin")


# ═══════════════════════════════════════════════════════════════════════════════
# Never interprets / never mutates
# ═══════════════════════════════════════════════════════════════════════════════


class TestNeverInterpretsEducationalMeaning:
    def test_coordinator_source_has_no_forbidden_educational_tokens(self) -> None:
        # Orchestration / contract modules only. Domain Strategies
        # (*_strategy.py) own educational interpretation and are tested
        # separately under Capability 4.9.9+.
        for path in sorted(TWIN_UPDATE_ROOT.glob("*.py")):
            if path.name.endswith("_strategy.py"):
                continue
            src = path.read_text(encoding="utf-8")
            hits = [token for token in FORBIDDEN_LOGIC_TOKENS if token in src]
            assert hits == [], f"{path.name} contains educational tokens: {hits}"

    def test_coordinator_does_not_inspect_domain_contribution(self) -> None:
        src = (TWIN_UPDATE_ROOT / "coordinator.py").read_text(encoding="utf-8")
        assert "output.domain_contribution" not in src
        assert ".domain_contribution" not in src
        tree = ast.parse(src)
        names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                names.add(node.id)
            elif isinstance(node, ast.Attribute):
                names.add(node.attr)
        for banned in (
            "mastery_belief",
            "pass_probability",
            "OverallPosture",
            "WarrantPosture",
            "DecisionEngine",
            "RecommendationEngine",
            "MissionIntelligence",
            "ReadinessAggregation",
        ):
            assert banned not in names


class TestNeverMutatesTwins:
    def test_current_twin_unchanged_after_update(self) -> None:
        twin = _twin()
        original_knowledge = twin.knowledge
        result = _coordinator().update(twin, _evidence())
        assert isinstance(result, TwinUpdateSuccess)
        assert twin.knowledge is original_knowledge
        with pytest.raises(FrozenInstanceError):
            twin.identity.student_id = "hijacked"  # type: ignore[misc]

    def test_evidence_unchanged_after_update(self) -> None:
        evidence = _evidence()
        eid = evidence.evidence_id
        _coordinator().update(_twin(), evidence)
        assert evidence.evidence_id == eid
        with pytest.raises(FrozenInstanceError):
            evidence.provenance = "tampered"  # type: ignore[misc]

    def test_coordinator_source_never_assigns_twin_fields(self) -> None:
        src = (TWIN_UPDATE_ROOT / "coordinator.py").read_text(encoding="utf-8")
        tree = ast.parse(src)
        banned_attrs = {
            "knowledge",
            "memory",
            "behaviour",
            "performance",
            "goals",
            "predictions",
            "identity",
            "mastery_belief",
        }
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if (
                        isinstance(target, ast.Attribute)
                        and target.attr in banned_attrs
                    ):
                        pytest.fail(
                            f"Coordinator assigns Twin field .{target.attr}"
                        )


# ═══════════════════════════════════════════════════════════════════════════════
# Logging / DI / architecture firewalls
# ═══════════════════════════════════════════════════════════════════════════════


class TestOperationalLogging:
    def test_happy_path_logs_operational_stages(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        coord = _coordinator(strategies=[_FakeStrategy("Knowledge")])
        logger_name = "app.application.twin_update.coordinator"
        with caplog.at_level(logging.INFO, logger=logger_name):
            result = coord.update(_twin(), _evidence())
        assert isinstance(result, TwinUpdateSuccess)
        messages = [r.getMessage() for r in caplog.records]
        assert "Twin update started" in messages
        assert "Knowledge Strategy invoked" in messages
        assert "Composer completed" in messages
        assert "Repository persisted successor" in messages
        assert "Twin update completed" in messages
        joined = " ".join(messages).lower()
        assert "mastery" not in joined
        assert "ready" not in joined
        assert "recommend" not in joined


class TestDependencyInjection:
    def test_injects_strategy_composer_repository(self) -> None:
        strategy = _FakeStrategy("Memory", owned_domain="memory")
        composer = _FakeComposer()
        repository = _FakeRepository()
        coord = TwinUpdateCoordinator(
            strategies=[strategy],
            composer=composer,
            repository=repository,
        )
        result = coord.update(_twin(), _evidence())
        assert isinstance(result, TwinUpdateSuccess)
        assert strategy.calls
        assert composer.calls
        assert repository.calls


class TestArchitectureFirewalls:
    def test_no_forbidden_framework_imports(self) -> None:
        for path in sorted(TWIN_UPDATE_ROOT.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".", 1)[0]
                        assert root not in FORBIDDEN_ROOT_MODULES
                        assert not alias.name.startswith(FORBIDDEN_PREFIXES)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    root = node.module.split(".", 1)[0]
                    assert root not in FORBIDDEN_ROOT_MODULES
                    assert not node.module.startswith(FORBIDDEN_PREFIXES)

    def test_result_types_are_frozen(self) -> None:
        success = TwinUpdateSuccess(
            successor_twin=_twin(),
            acknowledgement=PersistAcknowledgement(
                snapshot_id="s1",
                sequence=2,
                scope=_scope(),
                authorship=TwinAuthorship.SUCCESSOR,
            ),
            strategy_identities=("Knowledge",),
        )
        with pytest.raises(FrozenInstanceError):
            success.strategy_identities = ("Other",)  # type: ignore[misc]

        failure = TwinUpdateFailure(
            reason=TwinUpdateFailureReason.STRATEGY_FAILURE,
            detail="x",
        )
        with pytest.raises(FrozenInstanceError):
            failure.detail = "y"  # type: ignore[misc]

    def test_evidence_package_is_frozen(self) -> None:
        package = _evidence()
        with pytest.raises(FrozenInstanceError):
            package.evidence_id = "x"  # type: ignore[misc]
