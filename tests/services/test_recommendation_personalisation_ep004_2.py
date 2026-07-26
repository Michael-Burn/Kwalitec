"""EP-004.2 Adaptive recommendation personalisation tests."""

from __future__ import annotations

from unittest.mock import patch

from app.services.recommendation_personalisation import (
    ATTR_CONSISTENCY_TREND,
    ATTR_PREFERRED_SESSION_DURATION,
    ATTR_PREFERRED_STUDY_WINDOWS,
    ATTR_RECOMMENDATION_RESPONSIVENESS,
    ATTR_RECOVERY_EFFECTIVENESS,
    ATTR_REVISION_ADHERENCE,
    MIN_CONFIDENCE,
    apply_profile_personalisation,
)
from app.services.recommendation_quality import (
    CATEGORY_MOCK_EXAM,
    CATEGORY_NEW_TOPIC,
    CATEGORY_REST,
    CATEGORY_REVISION,
    CATEGORY_STUDY_STRENGTH,
    CATEGORY_WEAK_TOPIC,
    LADDER_SAFETY,
    LADDER_WEAK_TOPIC,
    PRIORITY_CRITICAL,
    PRIORITY_HIGH,
    PRIORITY_LOW,
    PRIORITY_MEDIUM,
    apply_quality_contract,
    has_complete_explanation_schema,
)
from app.services.recommendation_service import RecommendationService


def _row(
    *,
    title: str,
    category: str,
    priority: str,
    reason: str = "Because evidence supports this step.",
    benefit: str = "Improve exam preparation.",
    ladder: int | None = None,
) -> dict:
    row = {
        "title": title,
        "category": category,
        "priority": priority,
        "reason": reason,
        "expected_benefit": benefit,
        "generated_at": "2026-07-26T00:00:00",
        "why_recommended": reason,
        "supporting_evidence": [reason],
        "suggested_next_action": f"Act on: {title}.",
        "next_action": f"Act on: {title}.",
        "confidence_level": "Moderate confidence",
        "review_point": "Reassess after next session.",
        "explanation_schema_version": "p001.2/v1",
        "explanation_level": "level_2",
        "explanation_schema_complete": True,
        "decision_ladder_rank": ladder
        if ladder is not None
        else (
            LADDER_SAFETY
            if category == CATEGORY_REST and priority == PRIORITY_CRITICAL
            else LADDER_WEAK_TOPIC
            if category == CATEGORY_WEAK_TOPIC
            else 6
        ),
        "plan_coherence": "advisory",
    }
    return row


def _attr(
    *,
    status: str = "available",
    kind: str = "derived_indicator",
    claim_boundary: str = "behaviour_summary",
    value: dict | None = None,
    confidence: float = 0.8,
    sample_size: int = 8,
    explanation: str = "Observed behavioural summary.",
) -> dict:
    return {
        "status": status,
        "kind": kind,
        "claim_boundary": claim_boundary,
        "value": value or {},
        "confidence": confidence,
        "sample_size": sample_size,
        "explanation": explanation,
        "limitations": [],
    }


def _profile(attributes: dict) -> dict:
    return {
        "profile_id": "plp-test-001",
        "student_id": "1",
        "authority": "personal_learning_profile",
        "contract_version": "ep004.1.1",
        "attributes": attributes,
        "limitations": [],
        "evidence_event_count": 12,
    }


class TestProfileDrivenRanking:
    def test_revision_adherence_boosts_revision_within_band(self):
        rows = [
            _row(
                title="Continue Algebra",
                category=CATEGORY_NEW_TOPIC,
                priority=PRIORITY_HIGH,
                ladder=6,
            ),
            _row(
                title="Revise Fractions",
                category=CATEGORY_REVISION,
                priority=PRIORITY_HIGH,
                ladder=6,
            ),
        ]
        profile = _profile(
            {
                ATTR_REVISION_ADHERENCE: _attr(
                    value={
                        "adherence_rate": 0.85,
                        "adhered_count": 7,
                        "deferred_count": 1,
                    },
                )
            }
        )
        result = apply_profile_personalisation(rows, profile, limit=2)
        assert result[0]["title"] == "Revise Fractions"
        assert result[0]["personalisation_applied"] is True
        assert any(
            f["effect"] == "prefer_revision_adherence"
            for f in result[0]["personalisation_factors"]
        )

    def test_recovery_follow_through_prefers_weak_topic_repair(self):
        rows = [
            _row(
                title="Continue Algebra",
                category=CATEGORY_NEW_TOPIC,
                priority=PRIORITY_HIGH,
                ladder=6,
            ),
            _row(
                title="Practise Fractions",
                category=CATEGORY_WEAK_TOPIC,
                priority=PRIORITY_HIGH,
                ladder=5,
            ),
        ]
        # Same ladder band for fair tie-break comparison.
        rows[1]["decision_ladder_rank"] = 6
        profile = _profile(
            {
                ATTR_RECOVERY_EFFECTIVENESS: _attr(
                    value={
                        "follow_through_rate": 0.75,
                        "recovery_count": 8,
                        "followed_by_completion_count": 6,
                    },
                )
            }
        )
        result = apply_profile_personalisation(rows, profile, limit=2)
        assert result[0]["title"] == "Practise Fractions"
        assert result[0]["personalisation_applied"] is True


class TestUnsupportedAndLowConfidence:
    def test_unsupported_attributes_ignored(self):
        rows = [
            _row(
                title="Continue Algebra",
                category=CATEGORY_NEW_TOPIC,
                priority=PRIORITY_HIGH,
                ladder=6,
            ),
            _row(
                title="Revise Fractions",
                category=CATEGORY_REVISION,
                priority=PRIORITY_HIGH,
                ladder=6,
            ),
        ]
        baseline = apply_profile_personalisation(rows, None, limit=2)
        profile = _profile(
            {
                ATTR_PREFERRED_STUDY_WINDOWS: _attr(
                    status="unsupported",
                    kind="unsupported",
                    claim_boundary="unsupported_assumption",
                    confidence=0.0,
                    sample_size=0,
                ),
                ATTR_REVISION_ADHERENCE: _attr(
                    status="unsupported",
                    kind="unsupported",
                    claim_boundary="unsupported_assumption",
                    confidence=0.0,
                    sample_size=0,
                ),
            }
        )
        result = apply_profile_personalisation(rows, profile, limit=2)
        assert [r["title"] for r in result] == [r["title"] for r in baseline]
        assert all(r["personalisation_applied"] is False for r in result)

    def test_low_confidence_attributes_ignored(self):
        rows = [
            _row(
                title="Continue Algebra",
                category=CATEGORY_NEW_TOPIC,
                priority=PRIORITY_HIGH,
                ladder=6,
            ),
            _row(
                title="Revise Fractions",
                category=CATEGORY_REVISION,
                priority=PRIORITY_HIGH,
                ladder=6,
            ),
        ]
        profile = _profile(
            {
                ATTR_REVISION_ADHERENCE: _attr(
                    value={"adherence_rate": 0.9},
                    confidence=MIN_CONFIDENCE - 0.1,
                    sample_size=2,
                )
            }
        )
        result = apply_profile_personalisation(rows, profile, limit=2)
        assert result[0]["title"] == "Continue Algebra"
        assert result[0]["personalisation_applied"] is False


class TestConfidenceAwareAdaptation:
    def test_declining_consistency_prefers_rest_within_band(self):
        rows = [
            _row(
                title="Continue Algebra",
                category=CATEGORY_NEW_TOPIC,
                priority=PRIORITY_MEDIUM,
                ladder=8,
            ),
            _row(
                title="Take a lighter day",
                category=CATEGORY_REST,
                priority=PRIORITY_MEDIUM,
                ladder=8,
            ),
        ]
        profile = _profile(
            {
                ATTR_CONSISTENCY_TREND: _attr(
                    claim_boundary="habit_summary",
                    value={
                        "direction": "declining",
                        "latest_streak": 1,
                        "observation_count": 6,
                    },
                )
            }
        )
        result = apply_profile_personalisation(rows, profile, limit=2)
        assert result[0]["title"] == "Take a lighter day"
        assert any(
            f["effect"] == "prefer_wellbeing_when_declining"
            for f in result[0]["personalisation_factors"]
        )

    def test_session_sizing_uses_declared_minutes(self):
        rows = [
            _row(
                title="Continue Algebra",
                category=CATEGORY_NEW_TOPIC,
                priority=PRIORITY_HIGH,
                ladder=6,
            )
        ]
        profile = _profile(
            {
                ATTR_PREFERRED_SESSION_DURATION: _attr(
                    kind="observed_fact",
                    claim_boundary="preference_summary",
                    value={"declared_session_minutes": 25},
                    confidence=1.0,
                    sample_size=1,
                )
            }
        )
        result = apply_profile_personalisation(rows, profile, limit=1)
        assert "25 minutes" in result[0]["suggested_next_action"]
        assert result[0]["session_sizing_guidance"]
        assert result[0]["personalisation_applied"] is True


class TestExplanationCompleteness:
    def test_personalisation_preserves_schema_and_flags_influence(self):
        profile = _profile(
            {
                ATTR_REVISION_ADHERENCE: _attr(
                    value={
                        "adherence_rate": 0.8,
                        "adhered_count": 8,
                        "deferred_count": 2,
                    },
                )
            }
        )
        with (
            patch(
                "app.services.recommendation_quality._resolve_authorised_today_focus",
                return_value=None,
            ),
            patch(
                "app.services.recommendation_quality._estimate_evidence_density",
                return_value="dense",
            ),
        ):
            result = apply_quality_contract(
                1,
                [
                    {
                        "title": "Revise Fractions",
                        "category": CATEGORY_REVISION,
                        "priority": PRIORITY_HIGH,
                        "reason": "Revision helps retention.",
                        "expected_benefit": "Retain weak topics.",
                        "generated_at": "2026-07-26T00:00:00",
                    }
                ],
                limit=1,
                profile_view=profile,
            )
        assert has_complete_explanation_schema(result[0])
        assert result[0]["personalisation_applied"] is True
        assert result[0]["personalisation_profile_id"] == "plp-test-001"
        assert any(
            "Personalisation evidence" in str(e)
            for e in result[0]["supporting_evidence"]
        )
        assert "Personalised using your observed study habits" in result[0][
            "why_recommended"
        ]


class TestConstitutionalOwnership:
    def test_personalisation_does_not_outrank_safety(self):
        rows = [
            _row(
                title="Take a rest day — study pattern notice",
                category=CATEGORY_REST,
                priority=PRIORITY_CRITICAL,
                ladder=LADDER_SAFETY,
            ),
            _row(
                title="Revise Fractions",
                category=CATEGORY_REVISION,
                priority=PRIORITY_HIGH,
                ladder=7,
            ),
        ]
        profile = _profile(
            {
                ATTR_REVISION_ADHERENCE: _attr(
                    value={
                        "adherence_rate": 1.0,
                        "adhered_count": 10,
                        "deferred_count": 0,
                    },
                    confidence=1.0,
                    sample_size=10,
                )
            }
        )
        result = apply_profile_personalisation(rows, profile, limit=2)
        assert result[0]["decision_ladder_rank"] == LADDER_SAFETY
        assert result[0]["title"].startswith("Take a rest day")

    def test_accept_rate_does_not_promote_categories(self):
        """High accept rate must not invent category promotion (Art. V §2)."""
        rows = [
            _row(
                title="Continue Algebra",
                category=CATEGORY_NEW_TOPIC,
                priority=PRIORITY_HIGH,
                ladder=6,
            ),
            _row(
                title="Revise Fractions",
                category=CATEGORY_REVISION,
                priority=PRIORITY_HIGH,
                ladder=6,
            ),
        ]
        profile = _profile(
            {
                ATTR_RECOMMENDATION_RESPONSIVENESS: _attr(
                    claim_boundary="preference_summary",
                    value={
                        "accept_rate": 0.95,
                        "accepted_count": 19,
                        "dismissed_count": 1,
                    },
                    sample_size=20,
                    confidence=1.0,
                )
            }
        )
        result = apply_profile_personalisation(rows, profile, limit=2)
        # Lexical title order preserved when no lawful ordering effect.
        assert [r["title"] for r in result] == [
            "Continue Algebra",
            "Revise Fractions",
        ]
        assert all(
            f.get("effect") != "prefer_accepted_category"
            for r in result
            for f in (r.get("personalisation_factors") or [])
        )

    def test_profile_is_evidence_not_authority_in_service_doc(self):
        import inspect

        src = inspect.getsource(RecommendationService.consume_personal_learning_profile)
        assert "never owns ranking" in src.lower() or "Never owns ranking" in src
        assert "PersonalLearningProfileAggregator" not in src


class TestCadenceAndRegression:
    def test_high_dismiss_rate_reduces_secondary_tips(self):
        rows = [
            _row(
                title="Practise Fractions",
                category=CATEGORY_WEAK_TOPIC,
                priority=PRIORITY_HIGH,
                ladder=5,
            ),
            _row(
                title="Keep momentum on Algebra",
                category=CATEGORY_STUDY_STRENGTH,
                priority=PRIORITY_LOW,
                ladder=9,
            ),
            _row(
                title="Continue Geometry",
                category=CATEGORY_NEW_TOPIC,
                priority=PRIORITY_MEDIUM,
                ladder=6,
            ),
            _row(
                title="Take a mock exam",
                category=CATEGORY_MOCK_EXAM,
                priority=PRIORITY_MEDIUM,
                ladder=4,
            ),
            _row(
                title="Extra tip five",
                category=CATEGORY_NEW_TOPIC,
                priority=PRIORITY_LOW,
                ladder=6,
            ),
        ]
        profile = _profile(
            {
                ATTR_RECOMMENDATION_RESPONSIVENESS: _attr(
                    claim_boundary="preference_summary",
                    value={
                        "accept_rate": 0.1,
                        "accepted_count": 1,
                        "dismissed_count": 9,
                    },
                    sample_size=10,
                    confidence=1.0,
                )
            }
        )
        result = apply_profile_personalisation(rows, profile, limit=5)
        assert len(result) <= 3
        assert all(r["category"] != CATEGORY_STUDY_STRENGTH for r in result)
        assert result[0]["personalisation_applied"] is True

    def test_none_profile_is_regression_safe(self):
        rows = [
            _row(
                title="B tip",
                category=CATEGORY_NEW_TOPIC,
                priority=PRIORITY_HIGH,
                ladder=6,
            ),
            _row(
                title="A tip",
                category=CATEGORY_NEW_TOPIC,
                priority=PRIORITY_HIGH,
                ladder=6,
            ),
        ]
        result = apply_profile_personalisation(rows, None, limit=2)
        assert [r["title"] for r in result] == ["A tip", "B tip"]
        assert all(r["personalisation_applied"] is False for r in result)

    def test_presentation_pass_through_keeps_personalisation_fields(self):
        from app.presentation.intelligence_surface import RuntimeAPresentationAdapter

        profile = _profile(
            {
                ATTR_REVISION_ADHERENCE: _attr(
                    value={
                        "adherence_rate": 0.9,
                        "adhered_count": 9,
                        "deferred_count": 1,
                    },
                )
            }
        )
        with (
            patch(
                "app.services.recommendation_quality._resolve_authorised_today_focus",
                return_value=None,
            ),
            patch(
                "app.services.recommendation_quality._estimate_evidence_density",
                return_value="dense",
            ),
        ):
            rows = apply_quality_contract(
                1,
                [
                    {
                        "title": "Revise Fractions",
                        "category": CATEGORY_REVISION,
                        "priority": PRIORITY_HIGH,
                        "reason": "Revision helps retention.",
                        "expected_benefit": "Retain weak topics.",
                        "generated_at": "2026-07-26T00:00:00",
                    }
                ],
                limit=1,
                profile_view=profile,
            )

        with patch(
            "app.presentation.intelligence_surface.adapter."
            "EducationalExplainabilityService.enrich_recommendations"
        ) as enrich:
            today, all_rows = (
                RuntimeAPresentationAdapter.enrich_recommendations_if_needed(
                    rows,
                    today_recommendation=rows[0],
                )
            )
            enrich.assert_not_called()
            assert today["personalisation_applied"] is True
            assert all_rows[0]["personalisation_factors"]
