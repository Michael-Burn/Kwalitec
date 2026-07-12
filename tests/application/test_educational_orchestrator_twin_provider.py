"""Tests for EducationalOrchestrator → TwinProvider integration (Capability 3.7.7).

Covers automatic retrieval of a persisted Twin, TwinAbsent honesty, caller no
longer supplying Twin, unchanged educational behaviour when Twin is present,
and framework independence. Composition only — Orchestrator retrieves via
TwinProvider; TwinProvider remains sole retrieval authority.
"""

from __future__ import annotations

import ast
import inspect
from datetime import date
from pathlib import Path

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
from app.application.twin_repository import InMemoryTwinRepository, TwinScope
from app.domain.decision import Constraints, IntensityPosture
from app.domain.readiness import (
    CurriculumContext,
    CurriculumFormat,
    CurriculumTopicRef,
    OverallPosture,
    ReadinessAggregation,
    WarrantPosture,
)
from app.domain.twin import DigitalTwin, GoalState, IdentityState, KnowledgeState

ORCHESTRATION_ROOT = (
    Path(__file__).resolve().parents[2] / "app" / "application" / "orchestration"
)
ORCHESTRATOR_PATH = ORCHESTRATION_ROOT / "educational_orchestrator.py"

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
    "TopicProgress",
    "DigitalTwin.create",
    "persist_birth_twin",
    "persist_successor_twin",
    "retrieve_current_twin",
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


def _curriculum() -> CurriculumContext:
    return CurriculumContext.create(
        "7",
        format=CurriculumFormat.V1,
        topics=[
            CurriculumTopicRef.create("topic-a", weight=0.5),
            CurriculumTopicRef.create("topic-b", weight=0.5),
        ],
    )


def _constraints() -> Constraints:
    return Constraints.create(
        available_minutes=60,
        intensity=IntensityPosture.AMPLE,
    )


def _scope(**overrides: object) -> TwinScope:
    defaults: dict[str, object] = {
        "student_id": "student-42",
        "sitting_id": "sep-2026",
        "curriculum_id": "7",
    }
    defaults.update(overrides)
    return TwinScope.create(**defaults)  # type: ignore[arg-type]


class _RecordingBuilder:
    def __init__(self, curriculum: CurriculumContext | None = None):
        self.curriculum = curriculum or _curriculum()
        self.calls: list[int | None] = []

    def build(self, curriculum_id: int | None) -> CurriculumContext:
        self.calls.append(curriculum_id)
        return self.curriculum


# ═══════════════════════════════════════════════════════════════════════════════
# Persisted Twin retrieved automatically
# ═══════════════════════════════════════════════════════════════════════════════


class TestPersistedTwinRetrievedAutomatically:
    def test_persisted_birth_twin_retrieved_via_provider(self) -> None:
        repo = InMemoryTwinRepository()
        birth = _twin()
        ack = repo.persist_birth_twin(
            birth,
            scope=_scope(),
            snapshot_id="birth-1",
        )
        assert ack.snapshot_id == "birth-1"  # type: ignore[union-attr]

        builder = _RecordingBuilder()
        orchestrator = EducationalOrchestrator(
            twin_provider=TwinProvider(repository=repo),
            curriculum_context_builder=builder,
        )

        experience = orchestrator.build_experience(
            student_id="student-42",
            curriculum_id=7,
            constraints=_constraints(),
            twin_retrieval_context=TwinRetrievalContext(
                sitting_id="sep-2026",
                curriculum_id="7",
                surface_intent="dashboard",
            ),
            product_context=ProductContext(surface_intent="dashboard"),
        )

        assert isinstance(experience, EducationalExperience)
        assert experience.student_summary.student_id == "student-42"
        assert experience.student_summary.curriculum_id == "7"
        assert builder.calls == [7]

    def test_default_retrieval_context_from_curriculum_and_product(self) -> None:
        """Without twin_retrieval_context, curriculum_id + surface_intent are wired."""
        repo = InMemoryTwinRepository()
        birth = _twin()
        repo.persist_birth_twin(birth, scope=_scope(sitting_id=None), snapshot_id="b1")

        calls: list[TwinRetrievalContext | None] = []

        class _RecordingProvider:
            def retrieve(
                self,
                student_id: str | None,
                *,
                context: TwinRetrievalContext | None = None,
            ) -> DigitalTwin | TwinAbsent:
                calls.append(context)
                return TwinProvider(repository=repo).retrieve(
                    student_id, context=context
                )

        orchestrator = EducationalOrchestrator(
            twin_provider=_RecordingProvider(),
            curriculum_context_builder=_RecordingBuilder(),
        )
        result = orchestrator.build_experience(
            student_id="student-42",
            curriculum_id=7,
            constraints=_constraints(),
            product_context=ProductContext(surface_intent="dashboard"),
        )

        assert isinstance(result, EducationalExperience)
        assert calls[0] is not None
        assert calls[0].curriculum_id == "7"
        assert calls[0].surface_intent == "dashboard"


# ═══════════════════════════════════════════════════════════════════════════════
# TwinAbsent path preserved
# ═══════════════════════════════════════════════════════════════════════════════


class TestTwinAbsentPathPreserved:
    def test_missing_persisted_twin_returns_twin_absent(self) -> None:
        orchestrator = EducationalOrchestrator(
            twin_provider=TwinProvider(repository=InMemoryTwinRepository()),
            curriculum_context_builder=_RecordingBuilder(),
        )

        result = orchestrator.build_experience(
            student_id="student-42",
            curriculum_id=7,
            constraints=_constraints(),
            twin_retrieval_context=TwinRetrievalContext(
                sitting_id="sep-2026",
                curriculum_id="7",
            ),
        )

        assert isinstance(result, TwinAbsent)
        assert result.reason is TwinAbsenceReason.MISSING
        assert result.student_id == "student-42"

    def test_twin_absent_does_not_invoke_curriculum_or_domains(self) -> None:
        builder = _RecordingBuilder()
        readiness_calls: list[str] = []

        class _ReadinessProbe:
            def derive(self, twin, curriculum, *, as_of=None, derivation_id=None):
                readiness_calls.append("derive")
                return ReadinessAggregation.derive(twin, curriculum)

        orchestrator = EducationalOrchestrator(
            twin_provider=TwinProvider(repository=InMemoryTwinRepository()),
            curriculum_context_builder=builder,
            readiness_aggregation=_ReadinessProbe(),
        )

        result = orchestrator.build_experience(
            student_id="nobody",
            curriculum_id=7,
            constraints=_constraints(),
        )

        assert isinstance(result, TwinAbsent)
        assert builder.calls == []
        assert readiness_calls == []

    def test_unconfigured_provider_returns_honest_absence(self) -> None:
        """Default TwinProvider() yields TwinAbsent — never fabricates."""
        builder = _RecordingBuilder()
        orchestrator = EducationalOrchestrator(
            curriculum_context_builder=builder,
        )
        result = orchestrator.build_experience(
            student_id="student-42",
            curriculum_id=7,
            constraints=_constraints(),
        )
        assert isinstance(result, TwinAbsent)
        assert result.reason is TwinAbsenceReason.MISSING
        assert builder.calls == []


# ═══════════════════════════════════════════════════════════════════════════════
# Orchestrator no longer requires caller Twin
# ═══════════════════════════════════════════════════════════════════════════════


class TestCallerDoesNotSupplyTwin:
    def test_build_experience_has_no_twin_parameter(self) -> None:
        params = inspect.signature(
            EducationalOrchestrator.build_experience
        ).parameters
        assert "twin" not in params
        assert "student_id" in params
        assert "curriculum_id" in params
        assert "constraints" in params

    def test_orchestrator_requires_identity_not_twin_snapshot(self) -> None:
        repo = InMemoryTwinRepository()
        birth = _twin()
        repo.persist_birth_twin(
            birth, scope=_scope(sitting_id=None), snapshot_id="birth-1"
        )
        orchestrator = EducationalOrchestrator(
            twin_provider=TwinProvider(repository=repo),
            curriculum_context_builder=_RecordingBuilder(),
        )
        # Identity + request context only — Twin comes from Provider.
        experience = orchestrator.build_experience(
            student_id="student-42",
            curriculum_id=7,
            constraints=_constraints(),
        )
        assert isinstance(experience, EducationalExperience)


# ═══════════════════════════════════════════════════════════════════════════════
# No educational behaviour changes
# ═══════════════════════════════════════════════════════════════════════════════


class TestNoEducationalBehaviourChanges:
    def test_experience_matches_direct_domain_chain_honesty(self) -> None:
        """When Twin is present, Experience honesty matches domain-derived readiness."""
        twin = _twin()
        curriculum = _curriculum()
        readiness = ReadinessAggregation.derive(twin, curriculum)

        class _Source:
            def load(self, student_id, *, context=None):
                return twin

        orchestrator = EducationalOrchestrator(
            twin_provider=TwinProvider(source=_Source()),
            curriculum_context_builder=_RecordingBuilder(curriculum),
        )
        experience = orchestrator.build_experience(
            student_id="student-42",
            curriculum_id=7,
            constraints=_constraints(),
        )
        assert isinstance(experience, EducationalExperience)
        assert experience.readiness_summary.cold_start is readiness.cold_start
        assert experience.readiness_summary.overall_posture is (
            readiness.overall_posture
        )
        assert experience.readiness_summary.overall_warrant is (
            readiness.overall_warrant
        )
        # Goals-only Twin remains cold-start / not-yet-knowable — no Mid theatre.
        assert experience.readiness_summary.overall_posture is (
            OverallPosture.NOT_YET_KNOWABLE
        )
        assert experience.readiness_summary.overall_warrant is WarrantPosture.LOW
        assert "cold_start" in experience.warnings

    def test_orchestrator_does_not_import_educational_internals(self) -> None:
        src = ORCHESTRATOR_PATH.read_text(encoding="utf-8")
        hits = [token for token in FORBIDDEN_LOGIC_TOKENS if token in src]
        assert hits == []
        # Must not bypass TwinProvider to talk to InMemoryTwinRepository.
        assert "InMemoryTwinRepository" not in src
        assert "app.application.twin_repository" not in src


# ═══════════════════════════════════════════════════════════════════════════════
# Framework independence
# ═══════════════════════════════════════════════════════════════════════════════


class TestFrameworkIndependence:
    def test_orchestration_package_has_no_flask_orm_or_route_imports(self) -> None:
        violations: list[str] = []
        for path in sorted(ORCHESTRATION_ROOT.rglob("*.py")):
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
        assert violations == []

    def test_orchestrator_does_not_invoke_flask_or_sql(self) -> None:
        src = ORCHESTRATOR_PATH.read_text(encoding="utf-8")
        assert "flask.request" not in src
        assert "flask.session" not in src
        assert "import flask" not in src
        assert "from flask" not in src
        assert "sqlalchemy" not in src.lower()
        assert "session.query" not in src
        assert "db.session" not in src
        assert "SELECT " not in src
        assert "INSERT " not in src
