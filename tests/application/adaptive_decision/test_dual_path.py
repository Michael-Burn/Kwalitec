"""ADR-027 M0 dual-path behaviour preservation and audit suite."""

from __future__ import annotations

import ast
import json
import random
from datetime import date, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest

from app.application.adaptive_decision import (
    DecisionOutcome,
    PolicyV0AdaptiveDecisionEngine,
    SittingDecisionOrchestrator,
)
from app.application.adaptive_decision.types import (
    BLOCK_CERTIFIED_GUIDANCE_UNAVAILABLE,
    BLOCK_ENROLMENT_INACTIVE,
    BLOCK_SYLLABUS_COMPLETE,
    DailySittingRequest,
)
from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.educational_runtime_engine.exceptions import (
    CertifiedGuidanceUnavailable,
    IllegalRuntimeState,
    SyllabusAlreadyComplete,
)
from app.application.educational_runtime_engine.service import (
    EducationalRuntimeEngineService,
)
from app.domain.educational_runtime_engine.events import EducationalEventType
from app.domain.educational_runtime_engine.state import EnrolmentStatus
from app.extensions import db
from app.models.educational_runtime_engine import (
    RuntimeEducationalEvent,
    RuntimeEnrolment,
)
from tests.application.educational_runtime_engine.helpers import (
    make_user,
    publish_subject,
)
from tests.certification.pi001d_helpers import (
    make_certified_user,
    publish_certified_subject,
)


def _identity_from_spec(spec) -> dict:
    return {
        "topic_id": spec.topic_id,
        "educational_package_id": spec.educational_package_id or None,
        "certified_mission_id": spec.certified_mission_id or None,
        "objective_ids": tuple(spec.objective_ids),
        "blocked": False,
        "block_reason": None,
    }


def _identity_from_decision(decision) -> dict:
    return {
        "topic_id": decision.topic_id,
        "educational_package_id": decision.educational_package_id,
        "certified_mission_id": decision.certified_mission_id,
        "objective_ids": tuple(decision.objective_ids),
        "blocked": decision.outcome == DecisionOutcome.BLOCKED,
        "block_reason": decision.block_reason,
    }


def _legacy_identity(runtime, *, user_id, subject_code, mission_date) -> dict:
    try:
        spec = runtime.compute_daily_sitting_selection(
            user_id=user_id,
            subject_code=subject_code,
            mission_date=mission_date,
        )
        return _identity_from_spec(spec)
    except SyllabusAlreadyComplete:
        return {
            "topic_id": None,
            "educational_package_id": None,
            "certified_mission_id": None,
            "objective_ids": (),
            "blocked": True,
            "block_reason": BLOCK_SYLLABUS_COMPLETE,
        }
    except CertifiedGuidanceUnavailable:
        return {
            "topic_id": None,
            "educational_package_id": None,
            "certified_mission_id": None,
            "objective_ids": (),
            "blocked": True,
            "block_reason": BLOCK_CERTIFIED_GUIDANCE_UNAVAILABLE,
        }
    except IllegalRuntimeState as exc:
        from app.application.adaptive_decision.policy_v0 import (
            _map_illegal_runtime_state,
        )

        return {
            "topic_id": None,
            "educational_package_id": None,
            "certified_mission_id": None,
            "objective_ids": (),
            "blocked": True,
            "block_reason": _map_illegal_runtime_state(str(exc)),
        }


def _policy_identity(engine, *, user_id, subject_code, mission_date) -> dict:
    enrolment = RuntimeEnrolment.query.filter_by(
        user_id=user_id, subject_code=subject_code
    ).first()
    decision = engine.decide_daily_sitting(
        DailySittingRequest(
            user_id=user_id,
            subject_code=subject_code,
            mission_date=mission_date,
            curriculum_identity=(
                enrolment.curriculum_identity if enrolment else None
            ),
        )
    )
    assert decision.outcome != DecisionOutcome.ADAPTIVE
    return _identity_from_decision(decision)


def _normalize_identity(ident: dict) -> dict:
    """Normalize non-deterministic certified mission ids from independent calls.

    CertifiedMissionEngine generates ``cm_<uuid>`` per invocation. Dual-path
    compares two independent selection calls, so equality on that opaque id is
    not meaningful; presence vs absence remains part of decision identity.
    """
    out = dict(ident)
    cid = out.get("certified_mission_id")
    if cid and str(cid).startswith("cm_"):
        out["certified_mission_id"] = "<generated>"
    return out


def _assert_same_identity(legacy: dict, policy: dict, *, case: str) -> None:
    left = _normalize_identity(legacy)
    right = _normalize_identity(policy)
    assert left == right, (
        f"dual-path divergence on {case}:\n"
        f"  legacy={legacy!r}\n"
        f"  policy={policy!r}"
    )


@pytest.fixture()
def runtime(ctx):
    return EducationalRuntimeEngineService()


@pytest.fixture()
def engine(runtime):
    return PolicyV0AdaptiveDecisionEngine(runtime=runtime)


# ---------------------------------------------------------------------------
# §7.2 table-driven dual-path cases
# ---------------------------------------------------------------------------


def test_dual_path_cold_start(ctx, runtime, engine):
    user = make_user("m0-cold@example.com")
    subject = publish_subject("M0COLD")
    runtime.enrol_student(user_id=user.id, subject_code=subject)
    day = date(2026, 8, 1)
    legacy = _legacy_identity(
        runtime, user_id=user.id, subject_code=subject, mission_date=day
    )
    policy = _policy_identity(
        engine, user_id=user.id, subject_code=subject, mission_date=day
    )
    _assert_same_identity(legacy, policy, case="cold_start")
    assert legacy["blocked"] is False
    assert legacy["topic_id"]
    assert legacy["objective_ids"]


def test_dual_path_mid_campaign(ctx, runtime, engine):
    user = make_user("m0-mid@example.com")
    subject = publish_subject("M0MID")
    runtime.enrol_student(user_id=user.id, subject_code=subject)
    day0 = date(2026, 8, 1)
    m0 = runtime.generate_daily_mission(
        user_id=user.id, subject_code=subject, mission_date=day0
    )
    runtime.complete_mission(
        user_id=user.id, mission_instance_id=m0.mission_instance_id
    )
    day1 = date(2026, 8, 2)
    legacy = _legacy_identity(
        runtime, user_id=user.id, subject_code=subject, mission_date=day1
    )
    policy = _policy_identity(
        engine, user_id=user.id, subject_code=subject, mission_date=day1
    )
    _assert_same_identity(legacy, policy, case="mid_campaign")
    assert legacy["blocked"] is False
    assert legacy["topic_id"] != m0.topic_id


def test_dual_path_same_leaf_multi_day(ctx, runtime, engine, monkeypatch):
    """Package chain still owed; topic must not advance across days."""
    user = make_user("m0-leaf@example.com")
    subject = publish_subject("M0LEAF")
    runtime.enrol_student(user_id=user.id, subject_code=subject)

    class _FakePack:
        package_id = "FAKE-LEAF-D1"
        mode = "learning"
        campaign_day = "FAKE-D1"
        topic_code = "1.1"
        display_title = "Leaf Day 1"
        task_descriptions = ("Read", "Practice")

    monkeypatch.setattr(
        "app.application.educational_packages.guard.certified_guidance_enforced",
        lambda subject_id: True,
    )
    monkeypatch.setattr(
        "app.application.educational_packages.selection.resolve_active_educational_package",
        lambda **kwargs: _FakePack(),
    )
    monkeypatch.setattr(
        "app.application.educational_packages.loader.find_package_by_id",
        lambda pid: _FakePack() if pid == _FakePack.package_id else None,
    )

    day0 = date(2026, 8, 1)
    day1 = date(2026, 8, 2)
    legacy0 = _legacy_identity(
        runtime, user_id=user.id, subject_code=subject, mission_date=day0
    )
    policy0 = _policy_identity(
        engine, user_id=user.id, subject_code=subject, mission_date=day0
    )
    _assert_same_identity(legacy0, policy0, case="same_leaf_day0")
    m0 = runtime.materialise_daily_mission_from_spec(
        runtime.compute_daily_sitting_selection(
            user_id=user.id, subject_code=subject, mission_date=day0
        )
    )
    assert m0.educational_package_id == "FAKE-LEAF-D1"
    # Do not complete: leaf still owed; topic must not advance across days.
    legacy1 = _legacy_identity(
        runtime, user_id=user.id, subject_code=subject, mission_date=day1
    )
    policy1 = _policy_identity(
        engine, user_id=user.id, subject_code=subject, mission_date=day1
    )
    _assert_same_identity(legacy1, policy1, case="same_leaf_day1")
    assert legacy0["topic_id"] == legacy1["topic_id"]
    assert legacy0["educational_package_id"] == legacy1["educational_package_id"]


def test_dual_path_post_tip_memory_front(ctx, runtime, engine, monkeypatch):
    user = make_certified_user("m0-cp@example.com")
    subject = publish_certified_subject("M0CP")
    runtime.enrol_student(user_id=user.id, subject_code=subject)
    # Complete full syllabus.
    day = date(2026, 8, 1)
    for offset in range(5):
        try:
            mission = runtime.generate_daily_mission(
                user_id=user.id,
                subject_code=subject,
                mission_date=day + timedelta(days=offset),
            )
        except SyllabusAlreadyComplete:
            break
        runtime.complete_mission(
            user_id=user.id, mission_instance_id=mission.mission_instance_id
        )
    enrolment = RuntimeEnrolment.query.filter_by(
        user_id=user.id, subject_code=subject
    ).first()
    enrolment.status = EnrolmentStatus.COMPLETED.value
    db.session.commit()

    class _MemoryPack:
        package_id = "FAKE-CP-D1"
        mode = "learning"
        campaign_day = "CP-D1"
        topic_code = "3.1"
        display_title = "Memory Front"
        task_descriptions = ("Recall",)

    monkeypatch.setattr(
        "app.application.educational_packages.selection.pending_post_tip_front_package",
        lambda **kwargs: _MemoryPack(),
    )
    monkeypatch.setattr(
        "app.application.educational_packages.guard.certified_guidance_enforced",
        lambda subject_id: False,
    )
    monkeypatch.setattr(
        "app.application.educational_packages.loader.find_package_by_id",
        lambda pid: _MemoryPack() if pid == _MemoryPack.package_id else None,
    )

    tip_day = date(2026, 8, 10)
    legacy = _legacy_identity(
        runtime, user_id=user.id, subject_code=subject, mission_date=tip_day
    )
    policy = _policy_identity(
        engine, user_id=user.id, subject_code=subject, mission_date=tip_day
    )
    _assert_same_identity(legacy, policy, case="post_tip_memory_front")
    assert legacy["blocked"] is False
    assert legacy["educational_package_id"] == "FAKE-CP-D1"


def test_dual_path_post_tip_publication_front(ctx, runtime, engine, monkeypatch):
    user = make_certified_user("m0-cr@example.com")
    subject = publish_certified_subject("M0CR")
    runtime.enrol_student(user_id=user.id, subject_code=subject)
    day = date(2026, 8, 1)
    for offset in range(5):
        try:
            mission = runtime.generate_daily_mission(
                user_id=user.id,
                subject_code=subject,
                mission_date=day + timedelta(days=offset),
            )
        except SyllabusAlreadyComplete:
            break
        runtime.complete_mission(
            user_id=user.id, mission_instance_id=mission.mission_instance_id
        )
    enrolment = RuntimeEnrolment.query.filter_by(
        user_id=user.id, subject_code=subject
    ).first()
    enrolment.status = EnrolmentStatus.COMPLETED.value
    db.session.commit()

    class _PubPack:
        package_id = "FAKE-CR-D1"
        mode = "learning"
        campaign_day = "CR-D1"
        topic_code = "3.1"
        display_title = "Publication Front"
        task_descriptions = ("Publish practice",)

    monkeypatch.setattr(
        "app.application.educational_packages.selection.pending_post_tip_front_package",
        lambda **kwargs: _PubPack(),
    )
    monkeypatch.setattr(
        "app.application.educational_packages.guard.certified_guidance_enforced",
        lambda subject_id: False,
    )
    monkeypatch.setattr(
        "app.application.educational_packages.loader.find_package_by_id",
        lambda pid: _PubPack() if pid == _PubPack.package_id else None,
    )

    tip_day = date(2026, 8, 11)
    legacy = _legacy_identity(
        runtime, user_id=user.id, subject_code=subject, mission_date=tip_day
    )
    policy = _policy_identity(
        engine, user_id=user.id, subject_code=subject, mission_date=tip_day
    )
    _assert_same_identity(legacy, policy, case="post_tip_publication_front")
    assert legacy["educational_package_id"] == "FAKE-CR-D1"


def test_dual_path_syllabus_complete_no_fronts(ctx, runtime, engine, monkeypatch):
    user = make_certified_user("m0-done@example.com")
    subject = publish_certified_subject("M0DONE")
    runtime.enrol_student(user_id=user.id, subject_code=subject)
    day = date(2026, 8, 1)
    for offset in range(5):
        try:
            mission = runtime.generate_daily_mission(
                user_id=user.id,
                subject_code=subject,
                mission_date=day + timedelta(days=offset),
            )
        except SyllabusAlreadyComplete:
            break
        runtime.complete_mission(
            user_id=user.id, mission_instance_id=mission.mission_instance_id
        )
    monkeypatch.setattr(
        "app.application.educational_packages.selection.pending_post_tip_front_package",
        lambda **kwargs: None,
    )
    tip_day = date(2026, 8, 20)
    legacy = _legacy_identity(
        runtime, user_id=user.id, subject_code=subject, mission_date=tip_day
    )
    policy = _policy_identity(
        engine, user_id=user.id, subject_code=subject, mission_date=tip_day
    )
    _assert_same_identity(legacy, policy, case="syllabus_complete_no_fronts")
    assert legacy["blocked"] is True
    assert legacy["block_reason"] == BLOCK_SYLLABUS_COMPLETE


def test_dual_path_guidance_enforced_missing_package(
    ctx, runtime, engine, monkeypatch
):
    user = make_user("m0-gap@example.com")
    subject = publish_subject("M0GAP")
    runtime.enrol_student(user_id=user.id, subject_code=subject)
    monkeypatch.setattr(
        "app.application.educational_packages.guard.certified_guidance_enforced",
        lambda subject_id: True,
    )
    monkeypatch.setattr(
        "app.application.educational_packages.selection.resolve_active_educational_package",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        "app.application.educational_packages.selection.pending_post_tip_front_package",
        lambda **kwargs: None,
    )
    day = date(2026, 8, 1)
    legacy = _legacy_identity(
        runtime, user_id=user.id, subject_code=subject, mission_date=day
    )
    policy = _policy_identity(
        engine, user_id=user.id, subject_code=subject, mission_date=day
    )
    _assert_same_identity(legacy, policy, case="guidance_missing_package")
    assert legacy["blocked"] is True
    assert legacy["block_reason"] == BLOCK_CERTIFIED_GUIDANCE_UNAVAILABLE


def test_dual_path_certified_lo_overlay(ctx, runtime, engine, monkeypatch):
    user = make_user("m0-cert@example.com")
    subject = publish_subject("M0CERT")
    runtime.enrol_student(user_id=user.id, subject_code=subject)
    progress = runtime.get_progress(user_id=user.id, subject_code=subject)

    class _CertSpec:
        mission_id = "cert-msn-overlay"
        topic_id = progress.current_topic_id
        objective_ids = ("overlay-lo-1",)
        selection_reasons = ()
        calibration_notes = ()
        provenance = SimpleNamespace(
            chain_id="chain",
            snapshot_id="snap",
            authority="certified_snapshot",
            status="certified",
        )

    monkeypatch.setattr(
        runtime,
        "_select_certified_mission",
        lambda *args, **kwargs: _CertSpec(),
    )
    monkeypatch.setattr(
        "app.application.educational_packages.guard.certified_guidance_enforced",
        lambda subject_id: False,
    )
    day = date(2026, 8, 1)
    legacy = _legacy_identity(
        runtime, user_id=user.id, subject_code=subject, mission_date=day
    )
    policy = _policy_identity(
        engine, user_id=user.id, subject_code=subject, mission_date=day
    )
    _assert_same_identity(legacy, policy, case="certified_lo_overlay")
    assert legacy["certified_mission_id"] == "cert-msn-overlay"
    assert "overlay-lo-1" in legacy["objective_ids"]


def test_dual_path_certified_mismatch_mission_002(ctx, runtime, engine, monkeypatch):
    user = make_user("m0-mm@example.com")
    subject = publish_subject("M0MM")
    runtime.enrol_student(user_id=user.id, subject_code=subject)
    progress = runtime.get_progress(user_id=user.id, subject_code=subject)
    other_topic = next(
        tid for tid in progress.topic_ids if tid != progress.current_topic_id
    )

    class _MismatchSpec:
        mission_id = "cert-msn-mismatch"
        topic_id = other_topic
        objective_ids = ("mismatch-lo",)
        selection_reasons = ()
        calibration_notes = ()
        provenance = SimpleNamespace(
            chain_id="chain",
            snapshot_id="snap",
            authority="certified_snapshot",
            status="certified",
        )

    monkeypatch.setattr(
        runtime,
        "_select_certified_mission",
        lambda *args, **kwargs: _MismatchSpec(),
    )
    monkeypatch.setattr(
        "app.application.educational_packages.guard.certified_guidance_enforced",
        lambda subject_id: False,
    )
    day = date(2026, 8, 1)
    legacy = _legacy_identity(
        runtime, user_id=user.id, subject_code=subject, mission_date=day
    )
    policy = _policy_identity(
        engine, user_id=user.id, subject_code=subject, mission_date=day
    )
    _assert_same_identity(legacy, policy, case="certified_mismatch")
    assert legacy["topic_id"] == progress.current_topic_id
    assert legacy["topic_id"] != other_topic


def test_dual_path_idempotent_same_day(ctx, runtime, engine):
    user = make_user("m0-idem@example.com")
    subject = publish_subject("M0IDEM")
    runtime.enrol_student(user_id=user.id, subject_code=subject)
    day = date(2026, 8, 1)
    first = runtime.generate_daily_mission(
        user_id=user.id, subject_code=subject, mission_date=day
    )
    again = runtime.try_return_existing_daily_mission(
        user_id=user.id, subject_code=subject, mission_date=day
    )
    assert again is not None
    assert again.mission_instance_id == first.mission_instance_id
    # Policy V0 not required when short-circuit applies.
    orch = SittingDecisionOrchestrator(runtime=runtime, engine=engine)
    before = RuntimeEducationalEvent.query.filter_by(
        user_id=user.id,
        event_type=EducationalEventType.DECISION_RECORDED.value,
    ).count()
    returned = orch.ensure_todays_sitting(
        user_id=user.id, subject_code=subject, mission_date=day
    )
    after = RuntimeEducationalEvent.query.filter_by(
        user_id=user.id,
        event_type=EducationalEventType.DECISION_RECORDED.value,
    ).count()
    assert returned.mission_instance_id == first.mission_instance_id
    assert after == before


def test_dual_path_wrong_package_regeneration(ctx, runtime, engine, monkeypatch):
    user = make_user("m0-regen@example.com")
    subject = publish_subject("M0REGEN")
    runtime.enrol_student(user_id=user.id, subject_code=subject)

    class _Owed:
        package_id = "OWED-PACK"
        mode = "learning"
        campaign_day = "CA-D1"
        topic_code = "1.1"
        display_title = "Owed"
        task_descriptions = ("Task",)

    class _Wrong:
        package_id = "WRONG-PACK"
        mode = "learning"
        campaign_day = "CA-D2"
        topic_code = "1.1"
        display_title = "Wrong"
        task_descriptions = ("Wrong task",)

    monkeypatch.setattr(
        "app.application.educational_packages.guard.certified_guidance_enforced",
        lambda subject_id: True,
    )
    monkeypatch.setattr(
        "app.application.educational_packages.selection.pending_post_tip_front_package",
        lambda **kwargs: None,
    )
    monkeypatch.setattr(
        "app.application.educational_packages.selection.resolve_active_educational_package",
        lambda **kwargs: _Wrong(),
    )
    monkeypatch.setattr(
        "app.application.educational_packages.loader.find_package_by_id",
        lambda pid: {
            _Wrong.package_id: _Wrong(),
            _Owed.package_id: _Owed(),
        }.get(pid),
    )
    day = date(2026, 8, 1)
    wrong = runtime.generate_daily_mission(
        user_id=user.id, subject_code=subject, mission_date=day
    )
    assert wrong.educational_package_id == "WRONG-PACK"

    monkeypatch.setattr(
        "app.application.educational_packages.selection.resolve_active_educational_package",
        lambda **kwargs: _Owed(),
    )
    # Ops delete wrong package then new decision matches legacy/policy.
    existing = runtime.try_return_existing_daily_mission(
        user_id=user.id, subject_code=subject, mission_date=day
    )
    assert existing is None  # retired wrong package
    legacy = _legacy_identity(
        runtime, user_id=user.id, subject_code=subject, mission_date=day
    )
    policy = _policy_identity(
        engine, user_id=user.id, subject_code=subject, mission_date=day
    )
    _assert_same_identity(legacy, policy, case="wrong_package_regeneration")
    assert legacy["educational_package_id"] == "OWED-PACK"


def test_dual_path_enrolment_inactive_blocked(ctx, runtime, engine, monkeypatch):
    user = make_user("m0-inactive@example.com")
    subject = publish_subject("M0INACT")
    runtime.enrol_student(user_id=user.id, subject_code=subject)
    enrolment = RuntimeEnrolment.query.filter_by(
        user_id=user.id, subject_code=subject
    ).first()
    enrolment.status = EnrolmentStatus.COMPLETED.value
    db.session.commit()
    monkeypatch.setattr(
        "app.application.educational_packages.selection.pending_post_tip_front_package",
        lambda **kwargs: None,
    )
    day = date(2026, 8, 1)
    legacy = _legacy_identity(
        runtime, user_id=user.id, subject_code=subject, mission_date=day
    )
    policy = _policy_identity(
        engine, user_id=user.id, subject_code=subject, mission_date=day
    )
    _assert_same_identity(legacy, policy, case="enrolment_inactive")
    assert legacy["blocked"] is True
    assert legacy["block_reason"] == BLOCK_ENROLMENT_INACTIVE


# ---------------------------------------------------------------------------
# §7.2 point 5: randomized seeded soak (N >= 50)
# ---------------------------------------------------------------------------


def test_dual_path_randomized_soak_n50(ctx, runtime, engine, monkeypatch):
    monkeypatch.setattr(
        "app.application.educational_packages.guard.certified_guidance_enforced",
        lambda subject_id: False,
    )
    monkeypatch.setattr(
        "app.application.educational_packages.selection.pending_post_tip_front_package",
        lambda **kwargs: None,
    )
    rng = random.Random(20260830)
    comparisons = 0
    divergences: list[str] = []
    for i in range(50):
        user = make_user(f"m0-soak-{i}@example.com")
        subject = publish_subject(f"M0S{i:02d}")
        runtime.enrol_student(user_id=user.id, subject_code=subject)
        progress = runtime.get_progress(user_id=user.id, subject_code=subject)
        # Complete a random prefix of topics (0..all).
        n_complete = rng.randint(0, len(progress.topic_ids))
        day = date(2026, 7, 1)
        for j in range(n_complete):
            try:
                mission = runtime.generate_daily_mission(
                    user_id=user.id,
                    subject_code=subject,
                    mission_date=day + timedelta(days=j),
                )
            except (SyllabusAlreadyComplete, IllegalRuntimeState):
                break
            runtime.complete_mission(
                user_id=user.id, mission_instance_id=mission.mission_instance_id
            )
        probe = day + timedelta(days=n_complete + 1)
        legacy = _legacy_identity(
            runtime, user_id=user.id, subject_code=subject, mission_date=probe
        )
        policy = _policy_identity(
            engine, user_id=user.id, subject_code=subject, mission_date=probe
        )
        comparisons += 1
        if _normalize_identity(legacy) != _normalize_identity(policy):
            divergences.append(
                f"i={i} n_complete={n_complete} legacy={legacy} policy={policy}"
            )
    assert comparisons >= 50
    assert divergences == [], (
        "soak divergences:\n" + "\n".join(divergences)
    )


# ---------------------------------------------------------------------------
# Outcomes / audit / flag / import boundary
# ---------------------------------------------------------------------------


def test_adaptive_outcome_count_always_zero(ctx, runtime, engine):
    user = make_user("m0-adapt0@example.com")
    subject = publish_subject("M0AD0")
    runtime.enrol_student(user_id=user.id, subject_code=subject)
    orch = SittingDecisionOrchestrator(runtime=runtime, engine=engine)
    orch.ensure_todays_sitting(
        user_id=user.id,
        subject_code=subject,
        mission_date=date(2026, 8, 1),
    )
    rows = RuntimeEducationalEvent.query.filter_by(
        user_id=user.id,
        event_type=EducationalEventType.DECISION_RECORDED.value,
    ).all()
    assert rows
    adaptive = 0
    for row in rows:
        payload = json.loads(row.payload_json or "{}")
        if payload.get("outcome") == DecisionOutcome.ADAPTIVE.value:
            adaptive += 1
        assert payload.get("outcome") in {
            DecisionOutcome.SAFE_FALLBACK.value,
            DecisionOutcome.BLOCKED.value,
            DecisionOutcome.ADAPTIVE.value,
        }
    assert adaptive == 0


def test_blocked_records_stable_reason(ctx, runtime, engine, monkeypatch):
    user = make_certified_user("m0-block@example.com")
    subject = publish_certified_subject("M0BLK")
    runtime.enrol_student(user_id=user.id, subject_code=subject)
    day = date(2026, 8, 1)
    for offset in range(5):
        try:
            mission = runtime.generate_daily_mission(
                user_id=user.id,
                subject_code=subject,
                mission_date=day + timedelta(days=offset),
            )
        except SyllabusAlreadyComplete:
            break
        runtime.complete_mission(
            user_id=user.id, mission_instance_id=mission.mission_instance_id
        )
    monkeypatch.setattr(
        "app.application.educational_packages.selection.pending_post_tip_front_package",
        lambda **kwargs: None,
    )
    orch = SittingDecisionOrchestrator(runtime=runtime, engine=engine)
    with pytest.raises(SyllabusAlreadyComplete):
        orch.ensure_todays_sitting(
            user_id=user.id,
            subject_code=subject,
            mission_date=date(2026, 8, 30),
        )
    rows = RuntimeEducationalEvent.query.filter_by(
        user_id=user.id,
        event_type=EducationalEventType.DECISION_RECORDED.value,
    ).all()
    assert rows
    payload = json.loads(rows[-1].payload_json or "{}")
    assert payload["outcome"] == DecisionOutcome.BLOCKED.value
    assert payload["block_reason"] == BLOCK_SYLLABUS_COMPLETE


def test_flag_defaults_off_and_explicit_env_only():
    bare = resolve_v2_feature_flags(environ={})
    assert bare.ADR027_M0_DECISION_BOUNDARY is False
    loop = resolve_v2_feature_flags(environ={"KWALITEC_COMMERCIAL_LOOP": "1"})
    assert loop.ADR027_M0_DECISION_BOUNDARY is False
    on = resolve_v2_feature_flags(
        environ={"KWALITEC_ADR027_M0_DECISION_BOUNDARY": "1"}
    )
    assert on.ADR027_M0_DECISION_BOUNDARY is True


def test_runtime_c_does_not_import_adaptive_decision():
    root = Path(__file__).resolve().parents[3]
    runtime_dir = root / "app" / "application" / "educational_runtime_engine"
    offenders: list[str] = []
    for path in runtime_dir.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if "adaptive_decision" in alias.name:
                        offenders.append(f"{path}:{alias.name}")
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                if "adaptive_decision" in mod:
                    offenders.append(f"{path}:{mod}")
    assert offenders == []


def test_policy_v0_has_no_twin_or_ek_branches():
    root = Path(__file__).resolve().parents[3]
    policy_path = (
        root / "app" / "application" / "adaptive_decision" / "policy_v0.py"
    )
    text = policy_path.read_text(encoding="utf-8").lower()
    forbidden = (
        "estimated_knowledge",
        "student_digital_twin",
        "sr_twin_daily_loop",
        "domain.decision.engine",
        "mastery_score",
    )
    for token in forbidden:
        assert token not in text, f"Policy V0 contains forbidden token {token}"
