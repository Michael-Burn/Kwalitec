"""Tests for EducationalEvidencePackage alignment (Capability 4.9.7a).

Aligns Application-layer package transport with frozen Educational Evidence
Contract Version 1.0 (Capability 4.8.4). Structural validation only —
no educational correctness scoring.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from types import MappingProxyType

import pytest

from app.application.twin_repository import InMemoryTwinRepository, TwinScope
from app.application.twin_update import (
    CONTRACT_VERSION_1_0,
    EVIDENCE_PACKAGE_VERSION_1_0,
    DomainStrategyOutput,
    EducationalEvidencePackage,
    ObservedEvent,
    TwinComposer,
    TwinUpdateCoordinator,
    TwinUpdateSuccess,
)
from app.domain.twin import DigitalTwin, GoalState, IdentityState, KnowledgeState


def _ts() -> datetime:
    return datetime(2026, 7, 14, 10, 0, tzinfo=UTC)


def _package(**overrides: object) -> EducationalEvidencePackage:
    defaults: dict[str, object] = {
        "evidence_id": "ev-001",
        "student_id": "student-42",
        "evidence_timestamp": _ts(),
        "provenance": "observed:end_of_session",
        "study_plan_id": "plan-1",
        "curriculum_id": "CS1-2026",
        "observed_events": (ObservedEvent.MISSION_COMPLETED,),
    }
    defaults.update(overrides)
    return EducationalEvidencePackage.create(**defaults)  # type: ignore[arg-type]


def _twin() -> DigitalTwin:
    return DigitalTwin.create(
        IdentityState.create(
            student_id="student-42",
            curriculum_id="CS1-2026",
            current_exam="CS1",
        ),
        goals=GoalState.create(),
        knowledge=KnowledgeState.create(),
    )


class _PassthroughStrategy:
    @property
    def strategy_identity(self) -> str:
        return "Knowledge"

    def interpret(
        self,
        current_twin: DigitalTwin,
        evidence: EducationalEvidencePackage,
    ) -> DomainStrategyOutput:
        return DomainStrategyOutput.create(
            strategy_identity=self.strategy_identity,
            owned_domain="knowledge",
            domain_contribution=current_twin.knowledge,
            preserved=True,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Construction / required spine
# ═══════════════════════════════════════════════════════════════════════════════


class TestPackageConstruction:
    def test_constructs_required_spine(self) -> None:
        package = _package(topic_id="topic-a")
        assert package.evidence_id == "ev-001"
        assert package.student_id == "student-42"
        assert package.study_plan_id == "plan-1"
        assert package.curriculum_id == "CS1-2026"
        assert package.topic_id == "topic-a"
        assert package.evidence_timestamp == _ts()
        assert package.provenance == "observed:end_of_session"
        assert package.contract_version == CONTRACT_VERSION_1_0
        assert package.observed_events == (ObservedEvent.MISSION_COMPLETED,)

    def test_rejects_blank_required_identities(self) -> None:
        for field in (
            "evidence_id",
            "student_id",
            "study_plan_id",
            "curriculum_id",
            "provenance",
        ):
            with pytest.raises(ValueError, match=field):
                _package(**{field: "   "})

    def test_rejects_non_datetime_timestamp(self) -> None:
        with pytest.raises(ValueError, match="evidence_timestamp"):
            _package(evidence_timestamp="2026-07-14")  # type: ignore[arg-type]

    def test_strips_identity_whitespace(self) -> None:
        package = _package(
            evidence_id="  ev-x  ",
            student_id="  student-42  ",
            study_plan_id="  plan-1  ",
            curriculum_id="  CS1-2026  ",
        )
        assert package.evidence_id == "ev-x"
        assert package.student_id == "student-42"
        assert package.study_plan_id == "plan-1"
        assert package.curriculum_id == "CS1-2026"


class TestImmutablePackage:
    def test_package_is_frozen(self) -> None:
        package = _package()
        with pytest.raises(FrozenInstanceError):
            package.evidence_id = "other"  # type: ignore[misc]

    def test_assessment_result_mapping_is_immutable(self) -> None:
        package = _package(
            assessment_result={"score": 7, "max_score": 10},
            observed_events=(ObservedEvent.PRACTICE_COMPLETED,),
        )
        assert isinstance(package.assessment_result, MappingProxyType)
        with pytest.raises(TypeError):
            package.assessment_result["score"] = 9  # type: ignore[index]


# ═══════════════════════════════════════════════════════════════════════════════
# Observed events
# ═══════════════════════════════════════════════════════════════════════════════


class TestObservedEvents:
    def test_transports_closed_vocabulary(self) -> None:
        events = (
            ObservedEvent.MISSION_COMPLETED,
            ObservedEvent.TOPIC_STUDIED,
            ObservedEvent.PRACTICE_COMPLETED,
            ObservedEvent.STUDY_DURATION,
            ObservedEvent.SESSION_ENDED_MANUAL,
            ObservedEvent.SYSTEM_TIMESTAMP,
        )
        package = _package(observed_events=events)
        assert package.observed_events == events

    def test_accepts_string_tokens(self) -> None:
        package = _package(
            observed_events=("mission_abandoned", "session_ended_timeout"),
        )
        assert package.observed_events == (
            ObservedEvent.MISSION_ABANDONED,
            ObservedEvent.SESSION_ENDED_TIMEOUT,
        )

    def test_rejects_empty_observed_events(self) -> None:
        with pytest.raises(ValueError, match="observed_events"):
            _package(observed_events=())

    def test_rejects_unrecognised_token(self) -> None:
        with pytest.raises(ValueError, match="unrecognised"):
            _package(observed_events=("assessment_recorded",))

    def test_rejects_mission_completed_and_abandoned(self) -> None:
        with pytest.raises(ValueError, match="mission_completed"):
            _package(
                observed_events=(
                    ObservedEvent.MISSION_COMPLETED,
                    ObservedEvent.MISSION_ABANDONED,
                ),
            )

    def test_dedupes_preserving_order(self) -> None:
        package = _package(
            observed_events=(
                ObservedEvent.TOPIC_STUDIED,
                ObservedEvent.PRACTICE_ATTEMPTED,
                ObservedEvent.TOPIC_STUDIED,
            ),
        )
        assert package.observed_events == (
            ObservedEvent.TOPIC_STUDIED,
            ObservedEvent.PRACTICE_ATTEMPTED,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Optional observational cargo
# ═══════════════════════════════════════════════════════════════════════════════


class TestOptionalFields:
    def test_optional_assessment_result(self) -> None:
        package = _package(
            assessment_result={"assessment_id": "quiz-1", "score": 8},
            observed_events=(ObservedEvent.PRACTICE_COMPLETED,),
        )
        assert package.assessment_result is not None
        assert package.assessment_result["assessment_id"] == "quiz-1"
        assert package.assessment_result["score"] == 8

    def test_optional_practice_count(self) -> None:
        package = _package(
            practice_count=12,
            observed_events=(ObservedEvent.PRACTICE_COMPLETED,),
        )
        assert package.practice_count == 12

    def test_rejects_negative_practice_count(self) -> None:
        with pytest.raises(ValueError, match="practice_count"):
            _package(practice_count=-1)

    def test_optional_declared_duration(self) -> None:
        package = _package(
            declared_duration=45.5,
            observed_events=(ObservedEvent.STUDY_DURATION,),
        )
        assert package.declared_duration == 45.5

    def test_optional_reflection(self) -> None:
        package = _package(reflection="  Felt focused  ")
        assert package.reflection == "Felt focused"

    def test_optional_session_notes(self) -> None:
        package = _package(session_notes="  Review formulas  ")
        assert package.session_notes == "Review formulas"

    def test_omitted_optionals_remain_none(self) -> None:
        package = _package()
        assert package.assessment_result is None
        assert package.practice_count is None
        assert package.declared_duration is None
        assert package.reflection is None
        assert package.session_notes is None
        assert package.mission_id is None
        assert package.topic_id is None


# ═══════════════════════════════════════════════════════════════════════════════
# Contract version / backward compatibility
# ═══════════════════════════════════════════════════════════════════════════════


class TestContractVersion:
    def test_default_contract_version(self) -> None:
        package = _package()
        assert package.contract_version == "1.0"
        assert package.contract_version == CONTRACT_VERSION_1_0
        assert EVIDENCE_PACKAGE_VERSION_1_0 == CONTRACT_VERSION_1_0

    def test_package_version_alias_property(self) -> None:
        package = _package()
        assert package.package_version == package.contract_version

    def test_accepts_legacy_package_version_kwarg(self) -> None:
        package = EducationalEvidencePackage.create(
            "ev-001",
            "student-42",
            _ts(),
            "observed:end_of_session",
            study_plan_id="plan-1",
            curriculum_id="CS1-2026",
            observed_events=(ObservedEvent.TOPIC_STUDIED,),
            package_version="1.0",
        )
        assert package.contract_version == "1.0"

    def test_rejects_mismatched_version_aliases(self) -> None:
        with pytest.raises(ValueError, match="must match"):
            EducationalEvidencePackage.create(
                "ev-001",
                "student-42",
                _ts(),
                "observed:end_of_session",
                study_plan_id="plan-1",
                curriculum_id="CS1-2026",
                observed_events=(ObservedEvent.TOPIC_STUDIED,),
                contract_version="1.0",
                package_version="2.0",
            )


# ═══════════════════════════════════════════════════════════════════════════════
# Coordinator compatibility
# ═══════════════════════════════════════════════════════════════════════════════


class TestCoordinatorCompatibility:
    def test_coordinator_accepts_aligned_package(self) -> None:
        repo = InMemoryTwinRepository()
        scope = TwinScope.create("student-42", curriculum_id="CS1-2026")
        twin = _twin()
        birth = repo.persist_birth_twin(twin, scope=scope, snapshot_id="birth-1")
        assert birth is not None

        coord = TwinUpdateCoordinator(
            strategies=[_PassthroughStrategy()],
            composer=TwinComposer(),
            repository=repo,
        )
        package = _package(
            observed_events=(
                ObservedEvent.MISSION_COMPLETED,
                ObservedEvent.TOPIC_STUDIED,
            ),
            reflection="Steady progress",
            practice_count=3,
        )
        result = coord.update(twin, package, scope=scope)
        assert isinstance(result, TwinUpdateSuccess)
        assert result.acknowledgement.sequence >= 1
