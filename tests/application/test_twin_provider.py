"""Tests for TwinProvider (Capability 3.4.1).

Covers Twin retrieved, Twin absent, corrupt retrieval, dependency injection,
immutable return behaviour, framework independence, and absence of educational
reasoning in the TwinProvider module.
"""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError
from datetime import date
from pathlib import Path
from types import SimpleNamespace

import pytest

from app.application.twin import (
    TwinAbsenceReason,
    TwinAbsent,
    TwinProvider,
    TwinRetrievalContext,
)
from app.domain.twin import DigitalTwin, GoalState, IdentityState

TWIN_ROOT = Path(__file__).resolve().parents[2] / "app" / "application" / "twin"

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
    "app.services",
)

FORBIDDEN_EDUCATIONAL_IMPORTS = (
    "app.domain.readiness",
    "app.domain.decision",
    "app.domain.recommendation",
    "app.domain.mission",
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
    "DigitalTwin.create",
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
    goals = overrides.pop(
        "goals",
        GoalState.create(
            target_pass_probability=0.8,
            target_completion_date=date(2026, 9, 15),
            planned_study_hours_per_week=10.0,
        ),
    )
    return DigitalTwin.create(identity, goals=goals, **overrides)  # type: ignore[arg-type]


class _RecordingSource:
    """Injectable Twin source that records load calls."""

    def __init__(
        self,
        twin: DigitalTwin | None = None,
        *,
        error: Exception | None = None,
        payload: object | None = None,
        use_payload: bool = False,
    ) -> None:
        self.twin = twin
        self.error = error
        self.payload = payload
        self.use_payload = use_payload
        self.calls: list[tuple[str, TwinRetrievalContext | None]] = []

    def load(
        self,
        student_id: str,
        *,
        context: TwinRetrievalContext | None = None,
    ) -> DigitalTwin | None:
        self.calls.append((student_id, context))
        if self.error is not None:
            raise self.error
        if self.use_payload:
            return self.payload  # type: ignore[return-value]
        return self.twin


# ═══════════════════════════════════════════════════════════════════════════════
# Twin retrieved
# ═══════════════════════════════════════════════════════════════════════════════


class TestTwinRetrieved:
    def test_returns_existing_digital_twin(self) -> None:
        twin = _twin()
        provider = TwinProvider(source=_RecordingSource(twin))

        result = provider.retrieve("student-42")

        assert result is twin
        assert isinstance(result, DigitalTwin)
        assert result.identity.student_id == "student-42"

    def test_forwards_retrieval_context_to_source(self) -> None:
        twin = _twin()
        source = _RecordingSource(twin)
        provider = TwinProvider(source=source)
        context = TwinRetrievalContext(
            curriculum_id="CS1-2026",
            sitting_id="sep-2026",
            surface_intent="dashboard",
            snapshot_hint="snap-1",
        )

        result = provider.retrieve("student-42", context=context)

        assert result is twin
        assert source.calls == [("student-42", context)]

    def test_strips_student_id_whitespace(self) -> None:
        twin = _twin()
        source = _RecordingSource(twin)
        provider = TwinProvider(source=source)

        result = provider.retrieve("  student-42  ")

        assert result is twin
        assert source.calls[0][0] == "student-42"


# ═══════════════════════════════════════════════════════════════════════════════
# Twin absent
# ═══════════════════════════════════════════════════════════════════════════════


class TestTwinAbsent:
    def test_no_source_configured_returns_absent(self) -> None:
        """Incomplete persistence must not fabricate a Twin."""
        provider = TwinProvider()

        result = provider.retrieve("student-42")

        assert isinstance(result, TwinAbsent)
        assert result.reason is TwinAbsenceReason.MISSING
        assert result.student_id == "student-42"
        assert result.detail is not None

    def test_source_returns_none_is_absent(self) -> None:
        provider = TwinProvider(source=_RecordingSource(None))

        result = provider.retrieve("student-42")

        assert isinstance(result, TwinAbsent)
        assert result.reason is TwinAbsenceReason.MISSING
        assert result.student_id == "student-42"

    def test_missing_identity_is_absent(self) -> None:
        source = _RecordingSource(_twin())
        provider = TwinProvider(source=source)

        for student_id in (None, "", "   "):
            result = provider.retrieve(student_id)
            assert isinstance(result, TwinAbsent)
            assert result.reason is TwinAbsenceReason.MISSING_IDENTITY
            assert result.student_id is None

        assert source.calls == []

    def test_source_unavailable_is_absent(self) -> None:
        provider = TwinProvider(
            source=_RecordingSource(error=RuntimeError("connection refused"))
        )

        result = provider.retrieve("student-42")

        assert isinstance(result, TwinAbsent)
        assert result.reason is TwinAbsenceReason.UNAVAILABLE
        assert result.student_id == "student-42"
        assert "connection refused" in (result.detail or "")


# ═══════════════════════════════════════════════════════════════════════════════
# Corrupt retrieval
# ═══════════════════════════════════════════════════════════════════════════════


class TestCorruptRetrieval:
    def test_non_digital_twin_payload_is_corrupt(self) -> None:
        provider = TwinProvider(
            source=_RecordingSource(
                use_payload=True,
                payload={"knowledge": "fake"},
            )
        )

        result = provider.retrieve("student-42")

        assert isinstance(result, TwinAbsent)
        assert result.reason is TwinAbsenceReason.CORRUPT

    def test_wrong_student_id_is_corrupt(self) -> None:
        other = _twin(identity=_identity(student_id="other-student"))
        provider = TwinProvider(source=_RecordingSource(other))

        result = provider.retrieve("student-42")

        assert isinstance(result, TwinAbsent)
        assert result.reason is TwinAbsenceReason.CORRUPT
        assert result.student_id == "student-42"

    def test_object_shaped_like_twin_but_wrong_type_is_corrupt(self) -> None:
        provider = TwinProvider(
            source=_RecordingSource(
                use_payload=True,
                payload=SimpleNamespace(
                    identity=SimpleNamespace(student_id="student-42")
                ),
            )
        )

        result = provider.retrieve("student-42")

        assert isinstance(result, TwinAbsent)
        assert result.reason is TwinAbsenceReason.CORRUPT

    def test_never_repairs_corrupt_into_digital_twin(self) -> None:
        provider = TwinProvider(
            source=_RecordingSource(use_payload=True, payload="not-a-twin")
        )

        result = provider.retrieve("student-42")

        assert not isinstance(result, DigitalTwin)
        assert isinstance(result, TwinAbsent)


# ═══════════════════════════════════════════════════════════════════════════════
# Dependency injection
# ═══════════════════════════════════════════════════════════════════════════════


class TestDependencyInjection:
    def test_uses_injected_source(self) -> None:
        twin = _twin()
        source = _RecordingSource(twin)
        provider = TwinProvider(source=source)

        first = provider.retrieve("student-42")
        second = TwinProvider(source=_RecordingSource(None)).retrieve("student-42")

        assert first is twin
        assert isinstance(second, TwinAbsent)
        assert len(source.calls) == 1

    def test_default_provider_behaves_as_absent_without_injected_source(self) -> None:
        result = TwinProvider().retrieve("student-42")
        assert isinstance(result, TwinAbsent)
        assert result.reason is TwinAbsenceReason.MISSING


# ═══════════════════════════════════════════════════════════════════════════════
# Immutable return behaviour
# ═══════════════════════════════════════════════════════════════════════════════


class TestImmutableReturnBehaviour:
    def test_returned_twin_is_frozen(self) -> None:
        twin = _twin()
        result = TwinProvider(source=_RecordingSource(twin)).retrieve("student-42")
        assert isinstance(result, DigitalTwin)

        with pytest.raises(FrozenInstanceError):
            result.identity = _identity(student_id="mutated")  # type: ignore[misc]

    def test_returned_absent_is_frozen(self) -> None:
        result = TwinProvider().retrieve("student-42")
        assert isinstance(result, TwinAbsent)

        with pytest.raises(FrozenInstanceError):
            result.reason = TwinAbsenceReason.CORRUPT  # type: ignore[misc]

    def test_retrieval_context_is_frozen(self) -> None:
        context = TwinRetrievalContext(curriculum_id="CS1-2026")
        with pytest.raises(FrozenInstanceError):
            context.curriculum_id = "mutated"  # type: ignore[misc]

    def test_provider_returns_source_twin_without_copy_mutation(self) -> None:
        twin = _twin()
        result = TwinProvider(source=_RecordingSource(twin)).retrieve("student-42")
        assert result is twin
        assert result.identity.student_id == "student-42"


# ═══════════════════════════════════════════════════════════════════════════════
# Framework independence / no educational reasoning
# ═══════════════════════════════════════════════════════════════════════════════


class TestFrameworkIndependence:
    def test_twin_package_has_no_flask_route_orm_or_service_imports(self) -> None:
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

    def test_provider_source_has_no_flask_request_or_routes(self) -> None:
        src = (TWIN_ROOT / "twin_provider.py").read_text(encoding="utf-8")
        assert "flask.request" not in src
        assert "flask.session" not in src
        assert "Blueprint" not in src
        assert "bp.route" not in src
        assert "render_template" not in src
        assert "sqlalchemy" not in src.lower()


class TestNoEducationalReasoning:
    def test_provider_does_not_contain_scoring_or_selection_tokens(self) -> None:
        src = (TWIN_ROOT / "twin_provider.py").read_text(encoding="utf-8")
        hits = [token for token in FORBIDDEN_LOGIC_TOKENS if token in src]
        assert hits == []

    def test_provider_does_not_call_educational_engines(self) -> None:
        src = (TWIN_ROOT / "twin_provider.py").read_text(encoding="utf-8")
        assert "derive(" not in src
        assert "evaluate(" not in src
        assert "package(" not in src
        assert "compose(" not in src
        assert ".apply(" not in src

    def test_provider_has_no_write_or_mutation_api(self) -> None:
        provider = TwinProvider()
        assert not hasattr(provider, "save")
        assert not hasattr(provider, "update")
        assert not hasattr(provider, "persist")
        assert not hasattr(provider, "create")
        assert not hasattr(provider, "compute")

    def test_closed_output_is_twin_or_absent_only(self) -> None:
        present = TwinProvider(source=_RecordingSource(_twin())).retrieve("student-42")
        absent = TwinProvider().retrieve("student-42")
        assert isinstance(present, DigitalTwin)
        assert isinstance(absent, TwinAbsent)
        assert type(present) is DigitalTwin
        assert type(absent) is TwinAbsent
