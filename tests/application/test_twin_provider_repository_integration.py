"""Tests for TwinProvider → InMemoryTwinRepository integration (Capability 3.7.6).

Covers Birth / Successor retrieval, TwinAbsent when none exists, corrupt
repository honesty, framework independence, repository unchanged, and absence
of educational reasoning. Composition only — Provider retrieves; Repository
persists.
"""

from __future__ import annotations

import ast
from datetime import date
from pathlib import Path

from app.application.twin import (
    TwinAbsenceReason,
    TwinAbsent,
    TwinProvider,
    TwinRetrievalContext,
)
from app.application.twin_repository import (
    TwinPersistenceFailure,
    TwinPersistenceFailureReason,
    InMemoryTwinRepository,
    TwinScope,
)
from app.domain.twin import DigitalTwin, GoalState, IdentityState, KnowledgeState

TWIN_ROOT = Path(__file__).resolve().parents[2] / "app" / "application" / "twin"
REPO_ROOT = (
    Path(__file__).resolve().parents[2] / "app" / "application" / "twin_repository"
)

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

FORBIDDEN_EDUCATIONAL_IMPORTS = (
    "app.domain.readiness",
    "app.domain.decision",
    "app.domain.recommendation",
    "app.domain.mission",
    "app.application.orchestration",
    "app.application.calibration",
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
    "ReadinessAggregation",
    "DecisionEngine",
    "RecommendationEngine",
    "MissionIntelligence",
    "TopicProgress",
    "EducationalOrchestrator",
    "DigitalTwin.create",
    "persist_birth_twin",
    "persist_successor_twin",
)


def _identity(**overrides: object) -> IdentityState:
    defaults: dict[str, object] = {
        "student_id": "student-42",
        "curriculum_id": "7",
        "current_exam": "CS1",
        "target_sitting": date(2026, 9, 1),
    }
    defaults.update(overrides)
    return IdentityState.create(**defaults)  # type: ignore[arg-type]


def _twin(**overrides: object) -> DigitalTwin:
    identity = overrides.pop("identity", None)
    if identity is None:
        identity = _identity()
    goals = overrides.pop(
        "goals",
        GoalState.create(target_completion_date=date(2026, 9, 1)),
    )
    knowledge = overrides.pop("knowledge", KnowledgeState.create())
    return DigitalTwin.create(
        identity,  # type: ignore[arg-type]
        goals=goals,  # type: ignore[arg-type]
        knowledge=knowledge,  # type: ignore[arg-type]
        **overrides,  # type: ignore[arg-type]
    )


def _scope(**overrides: object) -> TwinScope:
    defaults: dict[str, object] = {
        "student_id": "student-42",
        "sitting_id": "sep-2026",
        "curriculum_id": "7",
    }
    defaults.update(overrides)
    return TwinScope.create(**defaults)  # type: ignore[arg-type]


def _context(**overrides: object) -> TwinRetrievalContext:
    defaults: dict[str, object] = {
        "sitting_id": "sep-2026",
        "curriculum_id": "7",
    }
    defaults.update(overrides)
    return TwinRetrievalContext(**defaults)  # type: ignore[arg-type]


class _CorruptRepository:
    """Test double that returns TwinPersistenceFailure.CORRUPT."""

    def retrieve_current_twin(self, scope: TwinScope) -> TwinPersistenceFailure:
        return TwinPersistenceFailure(
            reason=TwinPersistenceFailureReason.CORRUPT,
            scope=scope,
            snapshot_id="corrupt-1",
            detail="stored cargo is not a DigitalTwin",
        )


class _NonTwinCargoRepository:
    """Test double that returns non-DigitalTwin cargo (Provider must reject)."""

    def retrieve_current_twin(self, scope: TwinScope) -> object:
        return {"knowledge": "fake"}


# ═══════════════════════════════════════════════════════════════════════════════
# Birth Twin retrieval
# ═══════════════════════════════════════════════════════════════════════════════


class TestRetrievesPersistedBirthTwin:
    def test_retrieves_persisted_birth_twin(self) -> None:
        repo = InMemoryTwinRepository()
        scope = _scope()
        birth = _twin()
        ack = repo.persist_birth_twin(birth, scope=scope, snapshot_id="birth-1")
        assert ack.snapshot_id == "birth-1"  # type: ignore[union-attr]

        provider = TwinProvider(repository=repo)
        result = provider.retrieve("student-42", context=_context())

        assert result is birth
        assert isinstance(result, DigitalTwin)
        assert result.identity.student_id == "student-42"

    def test_forwards_sitting_and_curriculum_scope(self) -> None:
        repo = InMemoryTwinRepository()
        birth = _twin()
        repo.persist_birth_twin(birth, scope=_scope(), snapshot_id="birth-1")

        provider = TwinProvider(repository=repo)
        # Wrong sitting → Missing Twin (honest absence for that scope)
        absent = provider.retrieve(
            "student-42",
            context=_context(sitting_id="other-sitting"),
        )
        assert isinstance(absent, TwinAbsent)
        assert absent.reason is TwinAbsenceReason.MISSING

        present = provider.retrieve("student-42", context=_context())
        assert present is birth


# ═══════════════════════════════════════════════════════════════════════════════
# Successor Twin retrieval
# ═══════════════════════════════════════════════════════════════════════════════


class TestRetrievesPersistedSuccessorTwin:
    def test_retrieves_persisted_successor_twin(self) -> None:
        repo = InMemoryTwinRepository()
        scope = _scope()
        birth = _twin()
        successor = _twin(
            goals=GoalState.create(
                target_completion_date=date(2026, 9, 1),
                planned_study_hours_per_week=12.0,
            )
        )
        repo.persist_birth_twin(birth, scope=scope, snapshot_id="birth-1")
        repo.persist_successor_twin(
            successor, scope=scope, snapshot_id="succ-1"
        )

        provider = TwinProvider(repository=repo)
        result = provider.retrieve("student-42", context=_context())

        assert result is successor
        assert isinstance(result, DigitalTwin)
        assert result.goals.planned_study_hours_per_week == 12.0


# ═══════════════════════════════════════════════════════════════════════════════
# TwinAbsent when none exists
# ═══════════════════════════════════════════════════════════════════════════════


class TestReturnsTwinAbsentWhenNoneExists:
    def test_empty_repository_returns_twin_absent(self) -> None:
        repo = InMemoryTwinRepository()
        provider = TwinProvider(repository=repo)

        result = provider.retrieve("student-42", context=_context())

        assert isinstance(result, TwinAbsent)
        assert result.reason is TwinAbsenceReason.MISSING
        assert result.student_id == "student-42"
        assert not isinstance(result, DigitalTwin)

    def test_unavailable_repository_returns_unavailable(self) -> None:
        repo = InMemoryTwinRepository()
        repo.persist_birth_twin(_twin(), scope=_scope(), snapshot_id="birth-1")
        repo.mark_unavailable()
        provider = TwinProvider(repository=repo)

        result = provider.retrieve("student-42", context=_context())

        assert isinstance(result, TwinAbsent)
        assert result.reason is TwinAbsenceReason.UNAVAILABLE


# ═══════════════════════════════════════════════════════════════════════════════
# Corrupt repository result
# ═══════════════════════════════════════════════════════════════════════════════


class TestCorruptRepositoryResult:
    def test_corrupt_persistence_failure_mapped_to_twin_absent(self) -> None:
        provider = TwinProvider(repository=_CorruptRepository())  # type: ignore[arg-type]

        result = provider.retrieve("student-42", context=_context())

        assert isinstance(result, TwinAbsent)
        assert result.reason is TwinAbsenceReason.CORRUPT
        assert result.student_id == "student-42"
        assert result.detail is not None

    def test_non_twin_cargo_never_repaired(self) -> None:
        provider = TwinProvider(
            repository=_NonTwinCargoRepository()  # type: ignore[arg-type]
        )

        result = provider.retrieve("student-42", context=_context())

        assert isinstance(result, TwinAbsent)
        assert result.reason is TwinAbsenceReason.CORRUPT
        assert not isinstance(result, DigitalTwin)


# ═══════════════════════════════════════════════════════════════════════════════
# Framework independence / repository unchanged / no educational reasoning
# ═══════════════════════════════════════════════════════════════════════════════


class TestFrameworkIndependence:
    def test_provider_package_has_no_flask_orm_or_service_imports(self) -> None:
        violations: list[str] = []
        for path in sorted(TWIN_ROOT.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".", 1)[0]
                        if root in FORBIDDEN_ROOT_MODULES or alias.name.startswith(
                            FORBIDDEN_PREFIXES
                        ):
                            violations.append(f"{path.name}: import {alias.name}")
                elif isinstance(node, ast.ImportFrom) and node.module:
                    root = node.module.split(".", 1)[0]
                    if root in FORBIDDEN_ROOT_MODULES or node.module.startswith(
                        FORBIDDEN_PREFIXES
                    ):
                        violations.append(f"{path.name}: from {node.module}")
                    for prefix in FORBIDDEN_EDUCATIONAL_IMPORTS:
                        if node.module == prefix or node.module.startswith(
                            prefix + "."
                        ):
                            violations.append(
                                f"{path.name}: educational import {node.module}"
                            )
        assert violations == []

    def test_provider_source_has_no_flask_request_or_orm(self) -> None:
        src = (TWIN_ROOT / "twin_provider.py").read_text(encoding="utf-8")
        assert "flask.request" not in src
        assert "flask.session" not in src
        assert "Blueprint" not in src
        assert "bp.route" not in src
        assert "render_template" not in src
        assert "sqlalchemy" not in src.lower()
        assert "db.session" not in src


class TestRepositoryRemainsUnchanged:
    def test_repository_has_no_provider_coupling(self) -> None:
        """InMemoryTwinRepository must not import or name TwinProvider (composition only)."""
        for path in sorted(REPO_ROOT.rglob("*.py")):
            src = path.read_text(encoding="utf-8")
            assert "TwinProvider" not in src
            assert "TwinAbsent" not in src
            assert "TwinAbsenceReason" not in src
            assert "from app.application.twin import" not in src
            assert "from app.application.twin." not in src
            assert "import app.application.twin\n" not in src
            assert "import app.application.twin " not in src

    def test_repository_api_surface_unchanged(self) -> None:
        repo = InMemoryTwinRepository()
        assert hasattr(repo, "persist_birth_twin")
        assert hasattr(repo, "persist_successor_twin")
        assert hasattr(repo, "retrieve_current_twin")
        assert hasattr(repo, "retrieve_snapshot_history")
        assert hasattr(repo, "determine_current_snapshot")
        assert not hasattr(repo, "retrieve")  # Provider owns Orchestrator retrieve

    def test_provider_does_not_mutate_repository_contract(self) -> None:
        """Provider may call retrieve_current_twin only — never persist or invent."""
        src = (TWIN_ROOT / "twin_provider.py").read_text(encoding="utf-8")
        assert "retrieve_current_twin" in src
        assert "persist_birth_twin" not in src
        assert "persist_successor_twin" not in src
        assert "DigitalTwin.create" not in src


class TestNoEducationalReasoning:
    def test_provider_does_not_contain_scoring_or_selection_tokens(self) -> None:
        src = (TWIN_ROOT / "twin_provider.py").read_text(encoding="utf-8")
        hits = [token for token in FORBIDDEN_LOGIC_TOKENS if token in src]
        assert hits == []

    def test_provider_does_not_call_calibration_or_orchestrator(self) -> None:
        src = (TWIN_ROOT / "twin_provider.py").read_text(encoding="utf-8")
        tree = ast.parse(src)
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
                for alias in node.names:
                    imported.add(f"{node.module}.{alias.name}")
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name)
        assert not any(
            mod == "app.application.calibration"
            or mod.startswith("app.application.calibration.")
            for mod in imported
        )
        assert not any(
            mod == "app.application.orchestration"
            or mod.startswith("app.application.orchestration.")
            for mod in imported
        )
        assert not any(
            mod.startswith("app.domain.readiness")
            or mod.startswith("app.domain.decision")
            or mod.startswith("app.domain.recommendation")
            or mod.startswith("app.domain.mission")
            for mod in imported
        )
        assert "ReadinessAggregation" not in src
        assert "DecisionEngine" not in src
        assert "RecommendationEngine" not in src
        assert "MissionIntelligence" not in src
        # Docstring may name forbidden collaborators; executable body must not.
        body = src.split('"""', 2)[-1] if src.startswith('"""') else src
        assert "StudentCalibrationBuilder" not in body
        assert "CalibrationBirthPersister" not in body
        assert "EducationalOrchestrator" not in body

    def test_provider_has_no_write_or_mutation_api(self) -> None:
        provider = TwinProvider(repository=InMemoryTwinRepository())
        assert not hasattr(provider, "save")
        assert not hasattr(provider, "update")
        assert not hasattr(provider, "persist")
        assert not hasattr(provider, "create")
        assert not hasattr(provider, "compute")
        assert not hasattr(provider, "persist_birth")
        assert not hasattr(provider, "persist_successor")

    def test_closed_output_is_twin_or_absent_only(self) -> None:
        repo = InMemoryTwinRepository()
        twin = _twin()
        repo.persist_birth_twin(twin, scope=_scope(), snapshot_id="birth-1")
        provider = TwinProvider(repository=repo)

        present = provider.retrieve("student-42", context=_context())
        absent = TwinProvider(repository=InMemoryTwinRepository()).retrieve(
            "student-42", context=_context()
        )

        assert isinstance(present, DigitalTwin)
        assert isinstance(absent, TwinAbsent)
        assert type(present) is DigitalTwin
        assert type(absent) is TwinAbsent

    def test_repository_preferred_over_interim_source(self) -> None:
        """Durable InMemoryTwinRepository wins over interim TwinSource when both set."""
        repo = InMemoryTwinRepository()
        birth = _twin()
        repo.persist_birth_twin(birth, scope=_scope(), snapshot_id="birth-1")

        class _InterimSource:
            def load(
                self,
                student_id: str,
                *,
                context: TwinRetrievalContext | None = None,
            ) -> DigitalTwin | None:
                return _twin(
                    identity=_identity(student_id=student_id),
                    goals=GoalState.create(planned_study_hours_per_week=99.0),
                )

        provider = TwinProvider(repository=repo, source=_InterimSource())
        result = provider.retrieve("student-42", context=_context())
        assert result is birth
