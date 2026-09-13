"""Founder Progression Readiness detail: full internal contract evaluation."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from app.application.objective_evidence.records import AssessmentEvidenceRecord
from app.application.objective_evidence.store import ObjectiveAssessmentEvidenceStore
from app.application.progression_readiness import (
    CS1_A_T01_LO01,
    CS1_B_T03_LO01,
    PREREQUISITE_JOINT_DISTRIBUTION_LO,
)
from app.extensions import db
from app.founder.dashboard.services.progression_readiness_detail_service import (
    ProgressionReadinessDetailService,
)
from app.infrastructure.session.store import SessionDocumentStore
from app.models import User
from app.security.roles import Role
from app.services.identity_service import IdentityService


def _when(offset: int = 0) -> datetime:
    return datetime(2026, 9, 13, 9, 0, 0, tzinfo=UTC) + timedelta(seconds=offset)


def _record(
    *,
    student_id: str,
    objective_id: str,
    item_id: str,
    scored_correct: bool | None,
    offset: int = 0,
) -> AssessmentEvidenceRecord:
    return AssessmentEvidenceRecord(
        evidence_id=str(uuid4()),
        student_id=student_id,
        objective_id=objective_id,
        item_id=item_id,
        package_id="test-package",
        session_id="test-session",
        response_type="mcq",
        scored_correct=scored_correct,
        occurred_at=_when(offset),
        source="test",
    )


def _make_user(email: str) -> User:
    user = User(email=email, is_active_user=True)
    user.set_password("password123")
    user.alpha_onboarding_completed = True
    db.session.add(user)
    db.session.commit()
    return user


def test_founder_detail_shows_complete_internal_evaluation(ctx):
    store = ObjectiveAssessmentEvidenceStore(store=SessionDocumentStore())
    student_id = "42"
    for i, (spec, ok) in enumerate(
        zip(
            CS1_A_T01_LO01.evidence_items,
            [True, True, False],
            strict=True,
        )
    ):
        store.append(
            _record(
                student_id=student_id,
                objective_id=CS1_A_T01_LO01.objective_id,
                item_id=spec.item_id,
                scored_correct=ok,
                offset=i,
            )
        )
    for i, (spec, ok) in enumerate(
        zip(
            CS1_B_T03_LO01.evidence_items,
            [True, True],
            strict=True,
        )
    ):
        store.append(
            _record(
                student_id=student_id,
                objective_id=CS1_B_T03_LO01.objective_id,
                item_id=spec.item_id,
                scored_correct=ok,
                offset=10 + i,
            )
        )

    page = ProgressionReadinessDetailService(store=store).build(
        user_id=42,
        student_email="learner@example.com",
    )
    assert page.student_id == 42
    assert len(page.contracts) == 15

    by_id = {c.objective_id: c for c in page.contracts}
    lo01 = by_id["CS1-A-T01-LO01"]
    assert lo01.readiness == "READY"
    assert lo01.reason_code == ""
    assert "at least 2 of 3" in lo01.requirement_summary
    assert lo01.critical_misconception_tags == ()
    assert lo01.critical_misconception_hit is False
    assert [i.correctness for i in lo01.items] == [
        "correct",
        "correct",
        "incorrect",
    ]

    topic_12 = by_id["CS1-A-T02-LO01"]
    assert topic_12.readiness == "INSUFFICIENT_EVIDENCE"
    assert topic_12.reason_code == "INSUFFICIENT_SAMPLE"
    assert "at least 3 of 4" in topic_12.requirement_summary
    assert not topic_12.prerequisite_objective_id
    assert all(i.correctness == "unobserved" for i in topic_12.items)

    mixed = by_id["CS1-B-T03-LO01"]
    assert mixed.readiness == "INSUFFICIENT_EVIDENCE"
    assert mixed.reason_code == "REQUIRED_PREREQUISITE_UNVERIFIED"
    assert mixed.prerequisite_objective_id == PREREQUISITE_JOINT_DISTRIBUTION_LO
    assert mixed.prerequisite_verified is False
    assert "Prerequisite:" in mixed.requirement_summary
    assert [i.correctness for i in mixed.items] == ["correct", "correct"]

    cold = by_id["CS1-A-T01-LO02"]
    assert cold.readiness == "INSUFFICIENT_EVIDENCE"
    assert cold.reason_code == "INSUFFICIENT_SAMPLE"
    assert all(i.correctness == "unobserved" for i in cold.items)


def test_founder_route_renders_detail_for_founder(client, ctx):
    founder = _make_user("pr-detail-founder@kwalitec.example")
    IdentityService.grant_role(founder, Role.FOUNDER)
    student = _make_user("pr-detail-student@kwalitec.example")
    client.post(
        "/auth/login",
        data={"email": founder.email, "password": "password123"},
        follow_redirects=True,
    )
    response = client.get(
        f"/console/participants/{student.id}/progression-readiness",
        follow_redirects=True,
    )
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Progression Readiness" in html
    assert "CS1-A-T01-LO01" in html
    assert "CS1-B-T03-LO01" in html
    assert 'data-pr-status="CS1-A-T01-LO01"' in html
    assert "none flagged" in html
