"""Unit tests for RecommendationSetValidator (FOS-006)."""

from __future__ import annotations

from dataclasses import replace

from app.founder.recommendations.config import (
    STATUS_HEALTHY,
    TEMPLATE_WAIT_FOR_INTERNAL_ALPHA,
)
from app.founder.recommendations.models import (
    Recommendation,
    RecommendationEvidence,
    RecommendationSet,
)
from app.founder.recommendations.tests.helpers import (
    RECOMMENDATION_NOW,
    make_engine,
    make_healthy_state,
    make_state,
)
from app.founder.recommendations.validators import RecommendationSetValidator


def _valid_set() -> RecommendationSet:
    state = make_state(alpha_overrides={"feedback_count": 0, "duplicate_count": 0})
    return make_engine().evaluate(state)


class TestRecommendationSetValidator:
    def test_valid_set_ok(self) -> None:
        report = RecommendationSetValidator().validate(_valid_set())
        assert report.ok is True
        assert report.issues == ()

    def test_empty_healthy_set_ok(self) -> None:
        empty = make_engine().evaluate(make_healthy_state())
        assert empty.overall_status == STATUS_HEALTHY
        report = RecommendationSetValidator().validate(empty)
        assert report.ok is True

    def test_missing_snapshot_version(self) -> None:
        bad = replace(_valid_set(), snapshot_version="")
        report = RecommendationSetValidator().validate(bad)
        assert any(i.code == "missing_snapshot_version" for i in report.issues)

    def test_duplicate_recommendation_ids(self) -> None:
        base = _valid_set()
        rec = base.recommendations[0]
        dup = replace(base, recommendations=(rec, replace(rec)))
        report = RecommendationSetValidator().validate(dup)
        assert any(i.code == "duplicate_recommendation_id" for i in report.issues)

    def test_invalid_priority(self) -> None:
        base = _valid_set()
        rec = replace(base.recommendations[0], priority="Urgent")
        bad = replace(base, recommendations=(rec,))
        report = RecommendationSetValidator().validate(bad)
        assert any(i.code == "invalid_priority" for i in report.issues)

    def test_unknown_template(self) -> None:
        base = _valid_set()
        rec = replace(base.recommendations[0], id="not_a_template")
        bad = replace(base, recommendations=(rec,))
        report = RecommendationSetValidator().validate(bad)
        assert any(i.code == "unknown_template" for i in report.issues)

    def test_invalid_evidence_source(self) -> None:
        base = _valid_set()
        evidence = RecommendationEvidence(source="", metric="feedback_count", value=0)
        rec = replace(base.recommendations[0], evidence=(evidence,))
        bad = replace(base, recommendations=(rec,))
        report = RecommendationSetValidator().validate(bad)
        assert any(i.code == "invalid_evidence_source" for i in report.issues)

    def test_missing_evidence(self) -> None:
        base = _valid_set()
        rec = replace(base.recommendations[0], evidence=())
        bad = replace(base, recommendations=(rec,))
        report = RecommendationSetValidator().validate(bad)
        assert any(i.code == "missing_evidence" for i in report.issues)

    def test_empty_title(self) -> None:
        rec = Recommendation(
            id=TEMPLATE_WAIT_FOR_INTERNAL_ALPHA,
            category="release",
            priority="High",
            title="",
            explanation="e",
            rationale="r",
            evidence=(
                RecommendationEvidence(source="internal_alpha", metric="x", value=0),
            ),
            created_at=RECOMMENDATION_NOW,
        )
        bad = RecommendationSet(
            snapshot_version="1.0",
            generated_at=RECOMMENDATION_NOW,
            recommendations=(rec,),
            overall_status="attention",
        )
        report = RecommendationSetValidator().validate(bad)
        assert any(i.code == "empty_title" for i in report.issues)
