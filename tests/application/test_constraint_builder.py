"""Tests for ConstraintBuilder (Capability 3.4.2).

Covers known inputs, unknown values, missing duration, offline context,
immutable Constraints, dependency injection, framework independence, and
absence of educational reasoning in the ConstraintBuilder module.
"""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from pathlib import Path

import pytest

from app.application.constraints import (
    ConstraintBuilder,
    ConstraintProductConfiguration,
    ConstraintProductContext,
    InvalidConstraintInputError,
    MissingIdentityError,
)
from app.domain.decision.constraints import Constraints, IntensityPosture

CONSTRAINTS_ROOT = (
    Path(__file__).resolve().parents[2] / "app" / "application" / "constraints"
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
    "app.services",
)

FORBIDDEN_EDUCATIONAL_IMPORTS = (
    "app.domain.readiness",
    "app.domain.recommendation",
    "app.domain.mission",
    "app.domain.twin",
)

# Decision Constraints type is the closed output contract — import allowed.
# Decision Engine / nomination / selection must not appear.
FORBIDDEN_DECISION_LOGIC = (
    "app.domain.decision.engine",
    "app.domain.decision.nomination",
    "app.domain.decision.selection",
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
    "derive(",
    "evaluate(",
    "package(",
    "compose(",
)


# ═══════════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════════


def _context(**overrides: object) -> ConstraintProductContext:
    defaults: dict[str, object] = {
        "student_id": "student-42",
        "as_of": datetime(2026, 7, 12, 14, 0, tzinfo=UTC),
        "available_minutes": 45,
        "session_type": "standard_study",
        "preferred_intensity": IntensityPosture.MODERATE,
        "max_intensity_minutes": 30,
        "burnout_risk": False,
        "offline": False,
        "preferences": {"sustainability_protect": False},
    }
    defaults.update(overrides)
    return ConstraintProductContext(**defaults)  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════════
# Known inputs
# ═══════════════════════════════════════════════════════════════════════════════


class TestKnownInputs:
    def test_maps_known_product_facts_into_constraints(self) -> None:
        result = ConstraintBuilder().build(_context())

        assert isinstance(result, Constraints)
        assert result.available_minutes == 45
        assert result.intensity is IntensityPosture.MODERATE
        assert result.burnout_risk is False
        assert result.max_intensity_minutes == 30
        assert "session_type:standard_study" in result.note_tags
        assert "offline" not in result.note_tags
        assert "intensity_unknown" not in result.note_tags

    def test_forwards_known_burnout_risk_without_authoring_twin(self) -> None:
        result = ConstraintBuilder().build(_context(burnout_risk=True))

        assert result.burnout_risk is True
        assert result.intensity is IntensityPosture.MODERATE

    def test_accepts_intensity_as_string_label(self) -> None:
        result = ConstraintBuilder().build(
            _context(preferred_intensity="protect")
        )

        assert result.intensity is IntensityPosture.PROTECT

    def test_same_known_facts_yield_same_constraints(self) -> None:
        builder = ConstraintBuilder()
        context = _context()

        first = builder.build(context)
        second = builder.build(context)

        assert first == second


# ═══════════════════════════════════════════════════════════════════════════════
# Unknown values / missing duration
# ═══════════════════════════════════════════════════════════════════════════════


class TestUnknownValues:
    def test_missing_duration_remains_unknown(self) -> None:
        result = ConstraintBuilder().build(_context(available_minutes=None))

        assert result.available_minutes is None
        assert result.available_minutes != 60

    def test_does_not_invent_sixty_minutes_when_duration_missing(self) -> None:
        result = ConstraintBuilder().build(
            ConstraintProductContext(student_id="student-42")
        )

        assert result.available_minutes is None
        assert "intensity_unknown" in result.note_tags
        assert "preferences_absent" in result.note_tags

    def test_missing_preferences_do_not_invent_mid_intensity(self) -> None:
        result = ConstraintBuilder().build(
            ConstraintProductContext(
                student_id="student-42",
                available_minutes=40,
                preferred_intensity=None,
                preferences=None,
            )
        )

        # Domain factory default is AMPLE — never Mid theatre invented here.
        assert result.intensity is IntensityPosture.AMPLE
        assert "intensity_unknown" in result.note_tags
        assert result.intensity.value != "mid"

    def test_unknown_burnout_does_not_invent_protect_risk(self) -> None:
        result = ConstraintBuilder().build(
            ConstraintProductContext(
                student_id="student-42",
                burnout_risk=None,
            )
        )

        assert result.burnout_risk is False

    def test_unknown_max_intensity_minutes_remain_none(self) -> None:
        result = ConstraintBuilder().build(
            ConstraintProductContext(
                student_id="student-42",
                max_intensity_minutes=None,
            )
        )

        assert result.max_intensity_minutes is None


class TestMissingIdentity:
    def test_missing_student_id_raises(self) -> None:
        with pytest.raises(MissingIdentityError):
            ConstraintBuilder().build(ConstraintProductContext(student_id=None))

    def test_blank_student_id_raises(self) -> None:
        with pytest.raises(MissingIdentityError):
            ConstraintBuilder().build(ConstraintProductContext(student_id="  "))


class TestValidationFailures:
    def test_negative_duration_raises(self) -> None:
        with pytest.raises(InvalidConstraintInputError):
            ConstraintBuilder().build(_context(available_minutes=-1))

    def test_negative_max_intensity_raises(self) -> None:
        with pytest.raises(InvalidConstraintInputError):
            ConstraintBuilder().build(_context(max_intensity_minutes=-5))

    def test_invalid_intensity_label_raises(self) -> None:
        with pytest.raises(InvalidConstraintInputError):
            ConstraintBuilder().build(_context(preferred_intensity="mid"))

    def test_bool_minutes_rejected(self) -> None:
        with pytest.raises(InvalidConstraintInputError):
            ConstraintBuilder().build(_context(available_minutes=True))  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════════
# Offline context
# ═══════════════════════════════════════════════════════════════════════════════


class TestOfflineContext:
    def test_offline_marks_operational_tag_without_inventing_duration(self) -> None:
        result = ConstraintBuilder().build(
            ConstraintProductContext(
                student_id="student-42",
                available_minutes=None,
                offline=True,
            )
        )

        assert "offline" in result.note_tags
        assert result.available_minutes is None

    def test_offline_with_local_known_duration_preserves_minutes(self) -> None:
        result = ConstraintBuilder().build(
            _context(offline=True, available_minutes=20)
        )

        assert result.available_minutes == 20
        assert "offline" in result.note_tags

    def test_online_context_has_no_offline_tag(self) -> None:
        result = ConstraintBuilder().build(_context(offline=False))

        assert "offline" not in result.note_tags


# ═══════════════════════════════════════════════════════════════════════════════
# Immutable Constraints
# ═══════════════════════════════════════════════════════════════════════════════


class TestImmutableConstraints:
    def test_returned_constraints_are_frozen(self) -> None:
        result = ConstraintBuilder().build(_context())

        with pytest.raises(FrozenInstanceError):
            result.available_minutes = 99  # type: ignore[misc]

    def test_product_context_is_frozen(self) -> None:
        context = _context()
        with pytest.raises(FrozenInstanceError):
            context.available_minutes = 10  # type: ignore[misc]

    def test_configuration_is_frozen(self) -> None:
        config = ConstraintProductConfiguration(default_session_type="short_focus")
        with pytest.raises(FrozenInstanceError):
            config.default_session_type = "other"  # type: ignore[misc]

    def test_note_tags_are_tuple(self) -> None:
        result = ConstraintBuilder().build(_context(offline=True))
        assert isinstance(result.note_tags, tuple)


# ═══════════════════════════════════════════════════════════════════════════════
# Dependency injection / configuration defaults
# ═══════════════════════════════════════════════════════════════════════════════


class TestDependencyInjection:
    def test_injects_product_configuration_default_session_type(self) -> None:
        builder = ConstraintBuilder(
            configuration=ConstraintProductConfiguration(
                default_session_type="short_focus"
            )
        )

        result = builder.build(
            ConstraintProductContext(
                student_id="student-42",
                session_type=None,
            )
        )

        assert "session_type:short_focus" in result.note_tags

    def test_explicit_session_type_overrides_configuration_default(self) -> None:
        builder = ConstraintBuilder(
            configuration=ConstraintProductConfiguration(
                default_session_type="short_focus"
            )
        )

        result = builder.build(
            ConstraintProductContext(
                student_id="student-42",
                session_type="review_window",
            )
        )

        assert "session_type:review_window" in result.note_tags
        assert "session_type:short_focus" not in result.note_tags

    def test_default_builder_applies_no_session_type_when_absent(self) -> None:
        result = ConstraintBuilder().build(
            ConstraintProductContext(student_id="student-42", session_type=None)
        )

        assert not any(tag.startswith("session_type:") for tag in result.note_tags)

    def test_independent_builders_do_not_share_configuration(self) -> None:
        with_default = ConstraintBuilder(
            configuration=ConstraintProductConfiguration(
                default_session_type="standard_study"
            )
        )
        without = ConstraintBuilder()
        context = ConstraintProductContext(student_id="student-42")

        assert "session_type:standard_study" in with_default.build(context).note_tags
        assert not any(
            tag.startswith("session_type:") for tag in without.build(context).note_tags
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Framework independence / no educational reasoning
# ═══════════════════════════════════════════════════════════════════════════════


class TestFrameworkIndependence:
    def test_constraints_package_has_no_flask_route_orm_or_service_imports(
        self,
    ) -> None:
        violations: list[str] = []
        for path in sorted(CONSTRAINTS_ROOT.rglob("*.py")):
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
                    for prefix in FORBIDDEN_DECISION_LOGIC:
                        if node.module == prefix or node.module.startswith(
                            prefix + "."
                        ):
                            violations.append(
                                f"{path.name}: decision logic import {node.module}"
                            )
        assert violations == []

    def test_builder_source_has_no_flask_request_or_routes(self) -> None:
        src = (CONSTRAINTS_ROOT / "constraint_builder.py").read_text(encoding="utf-8")
        assert "flask.request" not in src
        assert "flask.session" not in src
        assert "Blueprint" not in src
        assert "bp.route" not in src
        assert "render_template" not in src
        assert "sqlalchemy" not in src.lower()


class TestNoEducationalReasoning:
    def test_builder_does_not_contain_scoring_or_selection_tokens(self) -> None:
        src = (CONSTRAINTS_ROOT / "constraint_builder.py").read_text(encoding="utf-8")
        hits = [token for token in FORBIDDEN_LOGIC_TOKENS if token in src]
        assert hits == []

    def test_builder_does_not_call_educational_engines(self) -> None:
        src = (CONSTRAINTS_ROOT / "constraint_builder.py").read_text(encoding="utf-8")
        assert "ReadinessAggregation" not in src
        assert "DecisionEngine" not in src
        assert "RecommendationEngine" not in src
        assert "MissionIntelligence" not in src
        assert "CurriculumService" not in src
        assert "DigitalTwin" not in src

    def test_builder_has_no_twin_mutation_or_curriculum_api(self) -> None:
        builder = ConstraintBuilder()
        assert not hasattr(builder, "save")
        assert not hasattr(builder, "update")
        assert not hasattr(builder, "persist")
        assert not hasattr(builder, "rank")
        assert not hasattr(builder, "optimise")
        assert not hasattr(builder, "optimize")
        assert not hasattr(builder, "estimate_need")

    def test_closed_output_is_constraints_only(self) -> None:
        result = ConstraintBuilder().build(_context())
        assert type(result) is Constraints

    def test_timestamp_does_not_fabricate_duration(self) -> None:
        result = ConstraintBuilder().build(
            ConstraintProductContext(
                student_id="student-42",
                as_of=datetime(2026, 7, 12, 23, 0, tzinfo=UTC),
                available_minutes=None,
            )
        )
        assert result.available_minutes is None
