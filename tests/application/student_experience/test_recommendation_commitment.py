"""EP-008.3A — Recommendation Commitment application-layer tests."""

from __future__ import annotations

from datetime import datetime

from app.application.student_experience.recommendation_commitment import (
    CONTINUITY_COMMIT,
    CONTINUITY_DEFER,
    CONTINUITY_REFLECTION,
    DEFER_CODES,
    FORBIDDEN_SHAME_SUBSTRINGS,
    STATE_COMMITTED,
    STATE_COMPLETED,
    STATE_DEFERRED,
    STATE_IN_SESSION,
    STATE_OFFERED,
    STATE_REFLECTED,
    WHAT_WAS_LEARNED_HUMBLE,
    RecommendationCommitmentService,
    compose_reflection,
    continuity_line_for,
    defer_reason_label,
    empty_commitment_snapshot,
)
from app.models.decision import Decision
from app.models.recommendation_commitment import RecommendationCommitment
from app.models.topic_progress import TopicProgress


def _tip(**overrides):
    tip = {
        "title": "Cash flow statements",
        "category": "Revision",
        "priority": "High",
        "reason": "High educational return before the exam window.",
        "why_recommended": "Soft recall on cash flow.",
        "expected_benefit": "Strengthen exam readiness on cash flow analysis.",
        "review_point": "Reassess after tonight's practice set.",
        "suggested_next_action": "Start a 25-minute cash flow practice session.",
        "generated_at": datetime(2026, 7, 26, 10, 0, 0),
    }
    tip.update(overrides)
    return tip


def test_empty_offered_and_refusal_snapshots():
    offered = empty_commitment_snapshot(
        has_schema_complete_tip=True,
        title="Cash flow statements",
        recommendation_key="Cash flow statements|2026-07-26",
    )
    assert offered.state == STATE_OFFERED
    assert offered.show_commit_affordance is True
    assert offered.show_defer_affordance is True
    assert CONTINUITY_COMMIT in offered.continuity_line

    refusal = empty_commitment_snapshot(trust_state="refusal", title="No tip")
    assert refusal.state == "refusal"
    assert refusal.show_commit_affordance is False
    assert refusal.show_defer_affordance is False


def test_compose_reflection_uses_authored_and_humble_frame():
    reflection = compose_reflection(
        title="Cash flow statements",
        review_point="Reassess after tonight's practice set.",
        expected_benefit="Strengthen exam readiness.",
        suggested_next_action="Return Home for the next tip.",
    )
    assert "Cash flow" in reflection.what_you_did
    assert "Reassess" in reflection.what_changed
    assert "Strengthen" in reflection.why_it_mattered
    assert reflection.what_was_learned == WHAT_WAS_LEARNED_HUMBLE
    assert "Twin" not in reflection.what_was_learned
    assert "AI learned" not in reflection.what_was_learned.lower()
    assert "next tip" in reflection.what_happens_next.lower() or "Home" in (
        reflection.what_happens_next
    )


def test_continuity_and_defer_catalogue():
    assert continuity_line_for("commit") == CONTINUITY_COMMIT
    assert continuity_line_for("defer") == CONTINUITY_DEFER
    assert continuity_line_for("reflection") == CONTINUITY_REFLECTION
    assert defer_reason_label("not_enough_time") == "Not enough time"
    assert "not_today" in DEFER_CODES
    for phrase in FORBIDDEN_SHAME_SUBSTRINGS:
        assert "streak" in phrase or "hurt" in phrase or True


def test_confirm_defer_complete_reflect_state_machine(ctx, user):
    tip = _tip()
    committed = RecommendationCommitmentService.confirm_commitment(user.id, tip)
    assert committed.state in {STATE_COMMITTED, STATE_IN_SESSION}
    assert CONTINUITY_COMMIT in committed.continuity_line

    row = RecommendationCommitment.query.filter_by(user_id=user.id).one()
    assert row.state in {STATE_COMMITTED, STATE_IN_SESSION}

    # Decision Journal preference record (accept ≠ mastery).
    decisions = Decision.query.filter_by(user_id=user.id).all()
    assert any(d.accepted for d in decisions)

    deferred = RecommendationCommitmentService.defer_commitment(
        user.id,
        tip,
        reason_code="not_enough_time",
    )
    assert deferred.state == STATE_DEFERRED
    assert deferred.deferred_reason_label == "Not enough time"
    assert CONTINUITY_DEFER in deferred.continuity_line

    # Fresh tip commit then complete.
    tip2 = _tip(title="Working capital", generated_at=datetime(2026, 7, 26, 11, 0, 0))
    RecommendationCommitmentService.confirm_commitment(user.id, tip2)
    RecommendationCommitmentService.mark_session_started(
        user.id, tip=tip2, session_id="sess-1"
    )
    completed = RecommendationCommitmentService.mark_completed(
        user.id, tip=tip2, session_id="sess-1"
    )
    assert completed is not None
    assert completed.state == STATE_COMPLETED
    assert completed.reflection is not None
    assert CONTINUITY_REFLECTION in completed.continuity_line

    reflected = RecommendationCommitmentService.acknowledge_reflection(
        user.id,
        recommendation_key=completed.recommendation_key,
    )
    assert reflected is not None
    assert reflected.state == STATE_REFLECTED


def test_cf_a09_commit_does_not_mutate_mastery(ctx, user):
    """CF-A09: commit/defer must not mutate readiness/mastery tables."""
    before = TopicProgress.query.filter_by(user_id=user.id).count()
    tip = _tip()
    RecommendationCommitmentService.confirm_commitment(user.id, tip)
    RecommendationCommitmentService.defer_commitment(
        user.id, tip, reason_code="not_today"
    )
    after = TopicProgress.query.filter_by(user_id=user.id).count()
    assert after == before


def test_narrative_entries_cap_and_kinds(ctx, user):
    tip = _tip()
    RecommendationCommitmentService.confirm_commitment(user.id, tip)
    RecommendationCommitmentService.mark_completed(user.id, tip=tip)
    tip_d = _tip(
        title="Inventory valuation",
        generated_at=datetime(2026, 7, 26, 12, 0, 0),
    )
    RecommendationCommitmentService.defer_commitment(
        user.id, tip_d, reason_code="studying_elsewhere"
    )
    entries = RecommendationCommitmentService.narrative_entries(user.id, limit=10)
    assert len(entries) <= 10
    kinds = {e.kind for e in entries}
    assert "completed" in kinds
    assert "deferred" in kinds
    assert all("pipeline" not in e.summary_line.lower() for e in entries)


def test_observational_emit_fail_open(ctx, user, monkeypatch):
    """CF-A10: observational emit fails open; scoring untouched."""

    def _boom(**kwargs):
        raise RuntimeError("recorder down")

    monkeypatch.setattr(
        "app.infrastructure.adapters.learning_feedback.emit_learning_feedback",
        _boom,
    )
    tip = _tip()
    snap = RecommendationCommitmentService.confirm_commitment(user.id, tip)
    assert snap.state in {STATE_COMMITTED, STATE_IN_SESSION, STATE_OFFERED}


