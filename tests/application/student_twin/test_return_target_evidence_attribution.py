"""Finding A — tip-surrogate mission topic must not receive practice evidence.

Campaign revision packages remount mission topic_id/topic_code onto tip 5.1
for generation only (PX-B-005). Twin, VP-001, and SQL write-through must
attribute via package return_targets (Policy V1 Twin-key resolver) instead.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from types import SimpleNamespace

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.educational_engine_foundation.dto import (
    EducationalArtefactSnapshot,
)
from app.application.educational_packages.loader import find_package_by_id
from app.application.learning_session.dto.candidate_observation import (
    CandidateObservation,
    RuntimeEvidenceType,
)
from app.application.learning_session.dto.evidence_package import (
    SessionEvidencePackage,
)
from app.application.student_runtime.evidence_write_through import (
    resolve_sql_topic_id_for_practice,
    resolve_sql_topic_ids_for_practice,
)
from app.application.student_twin.canonical_topic_id import CanonicalTopicId
from app.application.student_twin.practiced_identity import (
    resolve_practiced_twin_keys,
)
from app.application.student_twin.session_evidence_consumer import (
    SessionTwinEvidenceConsumer,
)
from app.infrastructure.adapters.learner_lifecycle.evidence_hook import (
    ATTRIBUTION_RETURN_TARGETS,
    record_session_evidence,
)
from app.models.learning_evidence import LeeEvidenceEvent
from app.services.educational_evidence_authority import EducationalEvidenceAuthority
from tests.application.adaptive_decision.test_policy_v1 import (
    _cs1_syllabus_artefacts,
)
from tests.application.version1_product.test_vp001_evidence_attribution import (
    _onboard,
    _save_session_handle,
)
from tests.conftest import _make_user

CR_R1_PACKAGE = "CS1-EP001-PKG-REV-PUBLICATION-FRONT-RHO"
TIP_SURROGATE_TOPIC_ID = "CS1-E-T01"  # 5.1 Bayesian methods
TIP_SURROGATE_CODE = "5.1"
FIXED = datetime(2026, 9, 12, 12, 0, tzinfo=UTC)


class _FakeFoundation:
    def __init__(self, snapshot: EducationalArtefactSnapshot | None) -> None:
        self._snapshot = snapshot

    def derive_active(self, subject_code: str):
        return self._snapshot


def _canonical() -> CanonicalTopicId:
    return CanonicalTopicId(foundation=_FakeFoundation(_cs1_syllabus_artefacts()))


def test_cr_r1_return_targets_resolve_away_from_tip_surrogate():
    """Genuine CR-R1 targets map to 1.1 / 1.2 / 2.1 Twin keys, never tip 5.1."""
    pack = find_package_by_id(CR_R1_PACKAGE)
    assert pack is not None
    assert pack.return_targets
    assert pack.topic_code == "CR-R1"

    resolution = resolve_practiced_twin_keys(
        educational_package_id=CR_R1_PACKAGE,
        subject_code="CS1",
        canonical=_canonical(),
    )
    assert resolution.source == "return_targets"
    assert resolution.unresolved is False
    assert TIP_SURROGATE_TOPIC_ID not in resolution.twin_keys
    assert set(resolution.twin_keys) == {"CS1-A-T01", "CS1-A-T02", "CS1-B-T01"}


def test_multiple_return_targets_fan_out_to_distinct_twin_keys():
    """Multiple LO parents stay as distinct Twin keys (Policy V1 key space)."""
    resolution = resolve_practiced_twin_keys(
        educational_package_id=CR_R1_PACKAGE,
        subject_code="CS1",
        canonical=_canonical(),
    )
    assert len(resolution.twin_keys) == 3
    assert len(resolution.twin_keys) == len(set(resolution.twin_keys))


def test_unresolved_return_targets_flag_honest_skip(monkeypatch):
    """When return_targets cannot resolve, mark unresolved — never tip keys."""

    def _none(*_a, **_k):
        return None

    monkeypatch.setattr(
        "app.application.student_twin.practiced_identity._resolve_return_target_twin_key",
        _none,
    )
    resolution = resolve_practiced_twin_keys(
        educational_package_id=CR_R1_PACKAGE,
        subject_code="CS1",
        canonical=_canonical(),
    )
    assert resolution.has_return_targets
    assert resolution.unresolved is True
    assert resolution.twin_keys == ()


def _validated_tip_surrogate_package(
    *,
    educational_package_id: str,
    tip_topic_id: str = TIP_SURROGATE_TOPIC_ID,
) -> SessionEvidencePackage:
    obs = CandidateObservation.create(
        observation_id="obs-practice-1",
        type_id=RuntimeEvidenceType.PRACTICE_CORRECT,
        student_id="42",
        session_id="lsr-finding-a",
        topic_id=tip_topic_id,
        mission_instance_id="m-cr-r1",
        recorded_at=FIXED,
        payload={"scored_correct": True},
    )
    package = SessionEvidencePackage.create(
        student_id="42",
        session_id="lsr-finding-a",
        mission_instance_id="m-cr-r1",
        topic_id=tip_topic_id,
        topic_title="5.1 Bayesian methods",
        curriculum_identity="CS1:2026",
        learning_objectives=("Revision retrieval",),
        observations=(obs,),
        finish_review_verdict="yes",
        created_at=FIXED,
        session_metadata={"educational_package_id": educational_package_id},
    )
    validation = EducationalEvidenceAuthority.validate_session_evidence_package(
        package
    )
    return package.with_validation(validation)


def test_twin_consumer_attributes_to_return_targets_not_tip(monkeypatch):
    """End-to-end Twin consume: tip package.topic_id must not receive EK."""
    monkeypatch.setattr(
        "app.application.student_twin.practiced_identity.CanonicalTopicId",
        lambda: _canonical(),
    )
    # Policy V1 resolver also constructs CanonicalTopicId internally via arg.
    package = _validated_tip_surrogate_package(
        educational_package_id=CR_R1_PACKAGE
    )
    consumer = SessionTwinEvidenceConsumer(
        store=None,
        clock=lambda: FIXED,
        id_factory=lambda: "fixed01",
        flag_resolver=lambda: resolve_v2_feature_flags(
            environ={"SR_TWIN_DAILY_LOOP": "1"}
        ),
    )
    # Inject canonical into practiced resolution path.
    monkeypatch.setattr(
        consumer,
        "_practiced_twin_keys",
        lambda pkg: resolve_practiced_twin_keys(
            educational_package_id=CR_R1_PACKAGE,
            subject_code="CS1",
            canonical=_canonical(),
        ),
    )
    events = consumer.extract_authorised_events(package)
    topic_ids = {e.topic_id for e in events}
    assert TIP_SURROGATE_TOPIC_ID not in topic_ids
    assert topic_ids == {"CS1-A-T01", "CS1-A-T02", "CS1-B-T01"}
    # One observation × three Twin keys.
    assert len(events) == 3

    result = consumer.consume(package)
    assert result.twin_updated is True
    assert TIP_SURROGATE_TOPIC_ID not in (result.estimated_knowledge or {})
    for key in ("CS1-A-T01", "CS1-A-T02", "CS1-B-T01"):
        assert key in (result.estimated_knowledge or {})


def test_twin_skips_when_return_targets_unresolved(monkeypatch):
    package = _validated_tip_surrogate_package(
        educational_package_id=CR_R1_PACKAGE
    )
    consumer = SessionTwinEvidenceConsumer(
        store=None,
        clock=lambda: FIXED,
        id_factory=lambda: "fixed01",
        flag_resolver=lambda: resolve_v2_feature_flags(
            environ={"SR_TWIN_DAILY_LOOP": "1"}
        ),
    )
    monkeypatch.setattr(
        consumer,
        "_practiced_twin_keys",
        lambda _pkg: resolve_practiced_twin_keys(
            educational_package_id=CR_R1_PACKAGE,
            subject_code="CS1",
            canonical=_canonical(),
        ).__class__(
            twin_keys=(),
            return_targets=("1.1.1",),
            source="return_targets",
            unresolved=True,
            educational_package_id=CR_R1_PACKAGE,
        ),
    )
    result = consumer.consume(package)
    assert result.twin_updated is False
    assert result.reason == "return_targets_unresolved_tip_surrogate_blocked"


def test_vp001_attributes_via_return_targets_not_tip(
    app, db, ctx, monkeypatch
) -> None:
    """VP-001 writes evidence for resolved return_target parents, not tip 5.1."""
    monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "1")
    user = _make_user()
    instance_id = _onboard(user.id, job_id="job-finding-a-vp001")

    # Tip-surrogate on the handle (what PX-B-005 writes onto the mission).
    session_id = "sess-finding-a-cr-r1"
    _save_session_handle(
        session_id=session_id,
        student_id=user.id,
        topic_id=TIP_SURROGATE_TOPIC_ID,
        topic_code=TIP_SURROGATE_CODE,
        educational_package_id=CR_R1_PACKAGE,
    )

    from app.models.student_curriculum_binding import SciCurriculumNodeState

    nodes = (
        SciCurriculumNodeState.query.filter_by(instance_id=instance_id)
        .order_by(SciCurriculumNodeState.id.asc())
        .all()
    )
    assert len(nodes) >= 2
    mapped = [nodes[0].node_stable_id, nodes[1].node_stable_id]

    monkeypatch.setattr(
        "app.application.student_twin.practiced_identity.resolve_practiced_twin_keys",
        lambda **_k: SimpleNamespace(
            has_return_targets=True,
            unresolved=False,
            twin_keys=("CS1-A-T01", "CS1-A-T02"),
            return_targets=("1.1.1", "1.2.1"),
            educational_package_id=CR_R1_PACKAGE,
        ),
    )

    import app.infrastructure.adapters.learner_lifecycle.evidence_hook as hook

    def _fake_syllabus_code(topic_id: str, *, subject_code: str) -> str | None:
        if topic_id == "CS1-A-T01":
            return "1.1"
        if topic_id == "CS1-A-T02":
            return "1.2"
        if topic_id == TIP_SURROGATE_TOPIC_ID:
            return TIP_SURROGATE_CODE
        return None

    def _fake_from_code(instance_id, *, subject_code, syllabus_code):
        if syllabus_code == TIP_SURROGATE_CODE:
            return None
        if syllabus_code == "1.1":
            return mapped[0]
        if syllabus_code == "1.2":
            return mapped[1]
        return None

    monkeypatch.setattr(
        hook, "_syllabus_code_from_published_topic", _fake_syllabus_code
    )
    monkeypatch.setattr(hook, "_resolve_from_syllabus_code", _fake_from_code)

    before = LeeEvidenceEvent.query.filter_by(instance_id=instance_id).count()
    result = record_session_evidence(
        student_id=user.id,
        session_id=session_id,
        activity_id="act-cr-r1",
        event="practice_attempt",
        metadata={"correct": True},
    )
    assert result is not None and result.succeeded
    after_rows = (
        LeeEvidenceEvent.query.filter_by(instance_id=instance_id)
        .order_by(LeeEvidenceEvent.id.asc())
        .all()
    )
    new_rows = after_rows[before:]
    assert len(new_rows) == 2
    node_ids = {r.node_stable_id for r in new_rows}
    assert node_ids == set(mapped)
    for row in new_rows:
        meta = json.loads(row.metadata_json or "{}")
        assert meta.get("attribution_source") == ATTRIBUTION_RETURN_TARGETS
        assert meta.get("practiced_educational_package_id") == CR_R1_PACKAGE


def test_vp001_skips_unresolved_return_targets_not_tip(
    app, db, ctx, monkeypatch
) -> None:
    monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "1")
    user = _make_user()
    instance_id = _onboard(user.id, job_id="job-finding-a-vp001-skip")
    session_id = "sess-finding-a-skip"
    _save_session_handle(
        session_id=session_id,
        student_id=user.id,
        topic_id=TIP_SURROGATE_TOPIC_ID,
        topic_code=TIP_SURROGATE_CODE,
        educational_package_id=CR_R1_PACKAGE,
    )
    monkeypatch.setattr(
        "app.application.student_twin.practiced_identity.resolve_practiced_twin_keys",
        lambda **_k: SimpleNamespace(
            has_return_targets=True,
            unresolved=True,
            twin_keys=(),
            return_targets=("1.1.1",),
            educational_package_id=CR_R1_PACKAGE,
        ),
    )
    import app.infrastructure.adapters.learner_lifecycle.evidence_hook as hook

    monkeypatch.setattr(hook, "_package_has_return_targets", lambda _pid: True)

    before = LeeEvidenceEvent.query.filter_by(instance_id=instance_id).count()
    result = record_session_evidence(
        student_id=user.id,
        session_id=session_id,
        activity_id="act-skip",
        event="practice_attempt",
    )
    assert result is None
    assert (
        LeeEvidenceEvent.query.filter_by(instance_id=instance_id).count()
        == before
    )


def test_sql_write_through_uses_return_targets_not_tip(monkeypatch):
    """SQL resolver prefers return_target parents over tip row.topic_code."""
    row = SimpleNamespace(
        mission_instance_id="mid-1",
        topic_code=TIP_SURROGATE_CODE,
        topic_id=TIP_SURROGATE_TOPIC_ID,
        curriculum_identity="CS1:2026",
        plan_instance_id="plan-1",
    )
    monkeypatch.setattr(
        "app.application.student_twin.practiced_identity.resolve_practiced_twin_keys",
        lambda **_k: SimpleNamespace(
            has_return_targets=True,
            unresolved=False,
            twin_keys=("CS1-A-T01", "CS1-A-T02", "CS1-B-T01"),
            return_targets=("1.1.1", "1.2.1", "2.1.1"),
            educational_package_id=CR_R1_PACKAGE,
        ),
    )
    monkeypatch.setattr(
        "app.application.student_twin.practiced_identity.syllabus_code_for_twin_key",
        lambda twin_key, **_k: {
            "CS1-A-T01": "1.1",
            "CS1-A-T02": "1.2",
            "CS1-B-T01": "2.1",
        }.get(twin_key),
    )
    code_to_sql = {"1.1": 101, "1.2": 102, "2.1": 201, TIP_SURROGATE_CODE: 501}

    def _sql_for_code(*, user_id, row, official_code, raw_topic_id=None):
        return code_to_sql.get(official_code)

    monkeypatch.setattr(
        "app.application.student_runtime.evidence_write_through."
        "_sql_topic_id_for_official_code",
        _sql_for_code,
    )
    monkeypatch.setattr(
        "app.application.student_runtime.evidence_write_through."
        "_subject_and_version_from_mission",
        lambda **_k: ("CS1", "2026"),
    )

    ids, disposition = resolve_sql_topic_ids_for_practice(
        user_id=1,
        row=row,
        educational_package_id=CR_R1_PACKAGE,
    )
    assert disposition == "return_targets"
    assert ids == [101, 102, 201]
    assert 501 not in ids
    # Multi-parent: single-id helper refuses to collapse arbitrarily.
    assert (
        resolve_sql_topic_id_for_practice(
            user_id=1,
            row=row,
            educational_package_id=CR_R1_PACKAGE,
        )
        is None
    )


def test_sql_skips_tip_when_return_targets_unresolved(monkeypatch):
    row = SimpleNamespace(
        mission_instance_id="mid-2",
        topic_code=TIP_SURROGATE_CODE,
        topic_id=TIP_SURROGATE_TOPIC_ID,
        curriculum_identity="CS1:2026",
        plan_instance_id="plan-1",
    )
    monkeypatch.setattr(
        "app.application.student_twin.practiced_identity.resolve_practiced_twin_keys",
        lambda **_k: SimpleNamespace(
            has_return_targets=True,
            unresolved=True,
            twin_keys=(),
            return_targets=("9.9.9",),
            educational_package_id=CR_R1_PACKAGE,
        ),
    )
    monkeypatch.setattr(
        "app.application.student_runtime.evidence_write_through."
        "_subject_and_version_from_mission",
        lambda **_k: ("CS1", "2026"),
    )
    ids, disposition = resolve_sql_topic_ids_for_practice(
        user_id=1,
        row=row,
        educational_package_id=CR_R1_PACKAGE,
    )
    assert disposition == "return_targets_unresolved"
    assert ids == []
    assert (
        resolve_sql_topic_id_for_practice(
            user_id=1,
            row=row,
            educational_package_id=CR_R1_PACKAGE,
        )
        is None
    )


def test_px_b005_tip_surrogate_mission_generation_unchanged():
    """PX-B-005 remapper itself remains correct for mission generation."""
    from app.application.educational_runtime_engine.service import (
        EducationalRuntimeEngineService,
    )

    artefacts = SimpleNamespace(
        topics=(
            {
                "topic_id": "topic-5-1",
                "topic_code": "5.1",
                "number": "5.1",
                "title": "5.1 Bayesian methods",
            },
        ),
        mission_templates=(),
    )
    svc = EducationalRuntimeEngineService()
    assert svc._topic_id_for_package_code(artefacts, "CR-R1") == "topic-5-1"
    assert svc._topic_id_for_package_code(artefacts, "CP-R1") == "topic-5-1"
