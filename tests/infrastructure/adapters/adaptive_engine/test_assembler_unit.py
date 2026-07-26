"""Unit tests — Adaptive Input Assembler (MS-003 A1)."""

from __future__ import annotations

from typing import Any

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.adaptive_engine import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    INPUT_FIELD_NAMES,
    REASON_NO_ACTIVE_PLAN,
    AdaptiveEngineAdapter,
    AdaptiveInputAssembler,
    AdaptiveInputBundle,
    CollectorResult,
    FieldProvenance,
    build_adaptive_input_assembler,
    serialize_canonical,
)
from app.infrastructure.adapters.adaptive_engine.normalization import (
    normalize_evidence,
    normalize_topic_progress,
)
from app.infrastructure.adapters.adaptive_engine.provenance import (
    available_provenance,
    unavailable_provenance,
)
from app.infrastructure.adapters.adaptive_engine.validation import (
    AdaptiveInputValidationError,
    validate_provenance_map,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)


class _StubCollector:
    def __init__(
        self,
        field_name: str,
        *,
        available: bool = True,
        payload: Any = None,
        reason: str = "",
        source_service: str = "stub_service",
        source_entity: str = "StubEntity",
    ) -> None:
        self.field_name = field_name
        self._available = available
        self._payload = payload if payload is not None else (
            [] if field_name in {"topic_progress", "study_attempts"} else {}
        )
        self._reason = reason
        self._source_service = source_service
        self._source_entity = source_entity
        self.calls = 0

    def collect(
        self,
        user_id: int,
        *,
        as_of: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> CollectorResult:
        self.calls += 1
        _ = (user_id, as_of, context)
        return CollectorResult(
            available=self._available,
            payload=self._payload,
            source_service=self._source_service,
            source_entity=self._source_entity,
            unavailable_reason=self._reason,
        )


def _stub_collectors(**overrides: _StubCollector) -> dict[str, _StubCollector]:
    collectors: dict[str, _StubCollector] = {}
    for name in INPUT_FIELD_NAMES:
        if name in overrides:
            collectors[name] = overrides[name]
            continue
        if name == "evidence":
            payload: Any = {
                "attempt_count": 0,
                "authorised_count": 0,
                "attempts": [],
            }
        elif name == "topic_progress":
            payload = []
        elif name == "study_attempts":
            payload = []
        elif name == "mission":
            payload = {"today": None, "history": [], "history_count": 0}
        elif name == "readiness":
            payload = {"overall": {"score": 1.0}, "coverage": {}, "review_backlog": {}}
        elif name == "curriculum":
            payload = {
                "curriculum_id": "9",
                "exam_name": "CM1",
                "version": "2025",
                "leaves": [{"topic_id": "1", "topic_name": "A", "order": 1}],
                "leaf_count": 1,
            }
        elif name == "student_goals":
            payload = {"study_plan_id": "3", "exam_date": "2026-09-01", "minutes": 45}
        else:
            payload = {"stage": "learning"}
        collectors[name] = _StubCollector(name, payload=payload)
    return collectors


def test_assembler_builds_deterministic_bundle():
    collectors = _stub_collectors()
    assembler = AdaptiveInputAssembler(
        collectors=collectors,
        study_plan_service=_FakePlanService(None),
    )
    first = assembler.assemble("42", as_of="2026-07-25")
    second = assembler.assemble("42", as_of="2026-07-25")
    assert first.serialize() == second.serialize()
    assert serialize_canonical(first.to_canonical_dict()) == first.serialize()


def test_assembler_provenance_on_every_field():
    assembler = AdaptiveInputAssembler(
        collectors=_stub_collectors(),
        study_plan_service=_FakePlanService(None),
    )
    bundle = assembler.assemble("7", as_of="2026-07-25T12:00:00")
    assert set(INPUT_FIELD_NAMES).issubset(bundle.field_provenance.keys())
    for name in INPUT_FIELD_NAMES:
        entry = dict(bundle.field_provenance[name])
        assert entry["source_service"]
        assert entry["source_entity"]
        assert entry["collected_at"] == "2026-07-25T12:00:00"
        assert entry["availability"] in {
            AVAILABILITY_AVAILABLE,
            AVAILABILITY_UNAVAILABLE,
        }


def test_missing_inputs_return_explicit_unavailable():
    collectors = _stub_collectors(
        student_goals=_StubCollector(
            "student_goals",
            available=False,
            payload={},
            reason=REASON_NO_ACTIVE_PLAN,
            source_service="study_plan_service",
            source_entity="StudyPlan",
        ),
        curriculum=_StubCollector(
            "curriculum",
            available=False,
            payload={},
            reason=REASON_NO_ACTIVE_PLAN,
            source_service="curriculum_service",
            source_entity="Curriculum",
        ),
    )
    assembler = AdaptiveInputAssembler(
        collectors=collectors,
        study_plan_service=_FakePlanService(None),
    )
    bundle = assembler.assemble("11", as_of="2026-07-25")
    goals_prov = dict(bundle.field_provenance["student_goals"])
    assert goals_prov["availability"] == AVAILABILITY_UNAVAILABLE
    assert goals_prov["unavailable_reason"] == REASON_NO_ACTIVE_PLAN
    assert dict(bundle.student_goals) == {}
    curr_prov = dict(bundle.field_provenance["curriculum"])
    assert curr_prov["availability"] == AVAILABILITY_UNAVAILABLE
    assert dict(bundle.curriculum) == {}


def test_invalid_student_id_yields_unavailable_contract():
    assembler = AdaptiveInputAssembler(
        collectors=_stub_collectors(),
        study_plan_service=_FakePlanService(None),
    )
    bundle = assembler.assemble(" ", as_of="2026-07-25")
    for name in INPUT_FIELD_NAMES:
        assert (
            dict(bundle.field_provenance[name])["availability"]
            == AVAILABILITY_UNAVAILABLE
        )


def test_normalization_sorts_topic_progress():
    rows = normalize_topic_progress(
        [
            {"topic_id": "2", "topic_progress_id": "9"},
            {"topic_id": "1", "topic_progress_id": "3"},
        ]
    )
    assert [r["topic_id"] for r in rows] == ["1", "2"]


def test_normalize_evidence_stable():
    payload = normalize_evidence(
        {
            "attempt_count": 2,
            "authorised_count": 1,
            "attempts": [
                {"attempt_id": "2", "study_date": "2026-07-02"},
                {"attempt_id": "1", "study_date": "2026-07-01"},
            ],
        }
    )
    assert [a["attempt_id"] for a in payload["attempts"]] == ["1", "2"]


def test_field_provenance_requires_reason_when_unavailable():
    with pytest.raises(ValueError, match="unavailable_reason"):
        FieldProvenance(
            source_service="x",
            source_entity="y",
            collected_at="2026-07-25",
            availability=AVAILABILITY_UNAVAILABLE,
            unavailable_reason="",
        )


def test_validate_provenance_map_requires_all_fields():
    with pytest.raises(AdaptiveInputValidationError, match="missing entry"):
        validate_provenance_map({})


def test_available_and_unavailable_helpers():
    ok = available_provenance(
        source_service="s", source_entity="e", collected_at="t"
    )
    assert ok.availability == AVAILABILITY_AVAILABLE
    bad = unavailable_provenance(
        source_service="s",
        source_entity="e",
        collected_at="t",
        reason=REASON_NO_ACTIVE_PLAN,
    )
    assert bad.unavailable_reason == REASON_NO_ACTIVE_PLAN


def test_flag_default_off_and_assembler_di():
    flags_off = resolve_v2_feature_flags(environ={})
    assert flags_off.ENABLE_ADAPTIVE_ENGINE is False
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.adaptive_engine is None
    assert composition_off.adaptive_input_assembler is None
    assert build_adaptive_input_assembler(enabled=False) is None

    flags_on = resolve_v2_feature_flags(environ={"KWALITEC_ADAPTIVE_ENGINE": "1"})
    composition_on, _ = build_production_experience(flags=flags_on)
    assert isinstance(composition_on.adaptive_input_assembler, AdaptiveInputAssembler)
    assert isinstance(composition_on.adaptive_engine, AdaptiveEngineAdapter)
    assert (
        composition_on.adaptive_engine.input_assembler
        is composition_on.adaptive_input_assembler
    )
    # Still no Experience AdaptiveDecisionPort cutover.
    assert composition_on.adaptive._recommendation_read is None
    assert composition_on.adaptive_engine is not composition_on.adaptive


def test_disabled_assembler_raises():
    assembler = AdaptiveInputAssembler(
        collectors=_stub_collectors(),
        enabled=False,
    )
    with pytest.raises(AdaptiveInputValidationError, match="disabled"):
        assembler.assemble("1")


def test_bundle_field_provenance_in_canonical_dict():
    bundle = AdaptiveInputBundle(
        student_id="1",
        field_provenance={
            "evidence": available_provenance(
                source_service="s", source_entity="e", collected_at="t"
            ).to_canonical_dict()
        },
    )
    assert "field_provenance" in bundle.to_canonical_dict()
    assert bundle.to_canonical_dict()["field_provenance"]["evidence"][
        "availability"
    ] == AVAILABILITY_AVAILABLE


class _FakePlanService:
    def __init__(self, plan: Any) -> None:
        self._plan = plan

    def read_active_plan(self, user_id: int) -> Any:
        _ = user_id
        return self._plan
