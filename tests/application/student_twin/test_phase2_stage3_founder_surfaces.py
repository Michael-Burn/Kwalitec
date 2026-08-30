"""ADR-027 Phase 2 Stage 4 founder Stack C surface treatments.

Each design §6 surface is either:
- repointed to LearnerTwinQueryPort for student-knowledge reads, or
- explicitly labelled as a legacy SDT diagnostic sandbox with retention text.
"""

from __future__ import annotations

import pytest

from app.application.student_digital_twin.student_digital_twin_service import (
    StudentDigitalTwinService,
)
from app.application.student_twin.query import (
    LearnerKnowledgeSnapshot,
    TopicKnowledgeFact,
)
from app.presentation.stack_c_sandbox import (
    STACK_C_SANDBOX_LABEL,
    STACK_C_SANDBOX_META,
)
from tests.presentation.curriculum_studio.helpers import login_founder


def _assert_sandbox(payload: dict) -> None:
    assert payload.get("legacy_sdt_sandbox") is True
    assert payload.get("ek_authority") == "not_authoritative"
    assert payload.get("sandbox_label") == STACK_C_SANDBOX_LABEL
    assert (
        payload.get("sandbox_retention")
        == STACK_C_SANDBOX_META["sandbox_retention"]
    )
    assert "Phase 2 implementation" in payload["sandbox_label"]
    assert "one subsequent review cycle" in payload["sandbox_label"]


@pytest.fixture
def founder_twin(client, app, ctx):
    login_founder(client, app)
    create = client.post(
        "/founder/twin/",
        json={
            "student_id": "42",
            "external_user_id": "42",
            "workspace_id": "ws-s3",
            "subject_code": "CS1",
            "display_name": "Stage3",
        },
    )
    assert create.status_code == 201
    body = create.get_json()
    _assert_sandbox(body)
    return body["twin"]["twin_id"]


def test_sandbox_label_on_twin_detail(client, app, ctx, founder_twin):
    resp = client.get(f"/founder/twin/{founder_twin}")
    assert resp.status_code == 200
    _assert_sandbox(resp.get_json())


def test_sandbox_label_on_reasoning_rules(client, app, ctx):
    login_founder(client, app)
    resp = client.get("/founder/reasoning/rules")
    assert resp.status_code == 200
    _assert_sandbox(resp.get_json())


def test_sandbox_label_on_assessment_pipeline_describe(client, app, ctx):
    login_founder(client, app)
    resp = client.get("/founder/assessment/pipeline")
    assert resp.status_code == 200
    _assert_sandbox(resp.get_json())


def test_sandbox_label_on_tutor_sessions(client, app, ctx, founder_twin):
    resp = client.get(f"/founder/tutor/sessions?twin_id={founder_twin}")
    assert resp.status_code == 200
    _assert_sandbox(resp.get_json())


def test_sandbox_label_on_missions_index(client, app, ctx, founder_twin):
    resp = client.get(f"/founder/missions/?twin_id={founder_twin}")
    assert resp.status_code == 200
    _assert_sandbox(resp.get_json())


def test_sandbox_label_on_learning_graph_index(client, app, ctx):
    login_founder(client, app)
    twin = StudentDigitalTwinService().create(
        student_id="lg-s3",
        workspace_id="ws-lg",
        subject_code="CS1",
    )
    resp = client.get(f"/founder/learning-graph/{twin.student.student_id}")
    assert resp.status_code == 200
    _assert_sandbox(resp.get_json())


def test_twin_mastery_uses_canonical_twin(
    client, app, ctx, founder_twin, monkeypatch
):
    class _FakeQuery:
        def knowledge_snapshot(self, *, user_id, subject_code):
            assert user_id == 42
            assert subject_code == "CS1"
            return LearnerKnowledgeSnapshot(
                user_id=user_id,
                subject_code=subject_code,
                curriculum_identity=None,
                overall_estimated_knowledge=0.81,
                topics=(
                    TopicKnowledgeFact(
                        topic_id="CS1-A-T01",
                        has_estimated_knowledge=True,
                        estimated_knowledge=0.81,
                        estimated_mastery=0.81,
                        evidence_count=4,
                        last_practised_at=None,
                    ),
                ),
            )

    monkeypatch.setattr(
        "app.presentation.student_digital_twin.routes.learner_twin_query",
        lambda: _FakeQuery(),
    )
    resp = client.get(f"/founder/twin/{founder_twin}/mastery")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["ok"] is True
    assert body["ek_authority"] == "canonical_learner_twin"
    assert body["estimated_knowledge"][0]["estimated_knowledge"] == pytest.approx(
        0.81
    )
    legacy = body["legacy_sdt_sandbox_mastery"]
    _assert_sandbox(legacy)
    assert "mastery" in legacy


def test_orchestrator_docstring_notes_cert_harness_sandbox():
    from app.application.educational_intelligence_pipeline import orchestrator

    doc = orchestrator.__doc__ or ""
    assert "test/cert harness" in doc
    assert "not wired to student Home" in doc
    assert "one subsequent review cycle" in doc


def test_flag_matrix_records_sandbox_retention():
    from pathlib import Path

    text = (
        Path(__file__).resolve().parents[3]
        / "docs"
        / "production"
        / "VERSION_1_FLAG_MATRIX.md"
    ).read_text(encoding="utf-8")
    assert "Stack C founder sandbox retention" in text
    assert "one subsequent review cycle" in text
    assert "stack_c_sandbox.py" in text
