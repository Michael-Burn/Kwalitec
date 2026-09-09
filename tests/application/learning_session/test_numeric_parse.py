"""Numeric answer parser: reject silent mangling of ambiguous student input.

Covers the _parse_number / numeric scoring path only. Does not touch MCQ or
other response types.
"""

from __future__ import annotations

import pytest

from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    reset_educational_package_cache,
)
from app.application.educational_packages.substance import substance_from_package
from app.application.learning_session.educational_flow import EducationalStage
from app.application.learning_session.scoreable_practice import (
    AnswerKey,
    PracticeResponseType,
    ScoreablePracticeItem,
    _parse_number,
    score_practice_response,
)

# Live CS1 numeric checkpoints (educational_packages, one per converted pack).
LIVE_NUMERIC_ACCEPTED = (
    ("cs1004-2.1c-cp-01", "0.3297", 0.001),
    ("cs1008-2.5.1-cp-01", "0.159", 0.001),
    ("cs1010-3.1.1-cp-01", "2200", 0.5),
    ("cs1010-3.1.2-cp-01", "0.4", 0.001),
    ("cs1003-4.2.10-cp-01", "0.8607", 0.001),
    ("cs1014-4.2.10-cp-01", "1.2214", 0.001),
    ("cs1003-5.1.6-cp-01", "1110", 0.5),
    ("cs1015-5.1.6-cp-01", "680", 0.5),
    ("cs1016-2.5.1-cp-01", "0.159", 0.001),
    ("cs1016-3.1.1-cp-01", "2", 0.001),
)


def _numeric_item(
    accepted: str,
    *,
    tolerance: float | None = 0.001,
    item_id: str = "t-num",
) -> ScoreablePracticeItem:
    return ScoreablePracticeItem(
        item_id=item_id,
        prompt="Numeric?",
        response_type=PracticeResponseType.NUMERIC,
        answer_key=AnswerKey(accepted=(accepted,), numeric_tolerance=tolerance),
        explanation="Because.",
        model_answer=accepted,
    )


# ---------------------------------------------------------------------------
# Previously correct behaviour must stay unchanged
# ---------------------------------------------------------------------------


class TestParseNumberPreservesValidShapes:
    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("0", 0.0),
            ("12", 12.0),
            ("-12", -12.0),
            ("+12", 12.0),
            ("0.5", 0.5),
            ("-0.5", -0.5),
            ("+0.5", 0.5),
            (".5", 0.5),
            ("2.", 2.0),
            ("95.24", 95.24),
            ("1e2", 100.0),
            ("1E-3", 0.001),
            ("1,000", 1000.0),
            ("1,000.5", 1000.5),
            ("12,345.67", 12345.67),
            ("2,200", 2200.0),
            ("  0.5  ", 0.5),
        ],
    )
    def test_valid_numbers_parse(self, raw: str, expected: float) -> None:
        assert _parse_number(raw) == pytest.approx(expected)

    @pytest.mark.parametrize(
        ("response", "accepted", "tolerance", "correct"),
        [
            ("95", "95.24", 0.5, True),
            ("90", "95.24", 0.5, False),
            ("0.5", "0.5", 0.01, True),
            ("0.505", "0.5", 0.01, True),
            ("0.52", "0.5", 0.01, False),
            ("1,000", "1000", 1e-6, True),
            ("1,110", "1110", 0.5, True),
            ("-0.5", "-0.5", 1e-6, True),
        ],
    )
    def test_valid_scoring_unchanged(
        self,
        response: str,
        accepted: str,
        tolerance: float,
        correct: bool,
    ) -> None:
        item = _numeric_item(accepted, tolerance=tolerance)
        result = score_practice_response(item, response)
        assert result.scored is True
        assert result.correct is correct
        assert result.feedback_outcome == ("Correct" if correct else "Incorrect")


# ---------------------------------------------------------------------------
# Dangerous / ambiguous shapes: unparseable, honest Incorrect (never coerced)
# ---------------------------------------------------------------------------


class TestParseNumberRejectsAmbiguousShapes:
    """Every character-stripping mangle found in investigation must reject."""

    @pytest.mark.parametrize(
        "raw",
        [
            # Fractions (the confirmed silent 1/2 -> 12.0 defect)
            "1/2",
            "3/4",
            "1/2.0",
            "12/3",
            "1.0/2",
            "1 2/3",
            # Letters / units / currency / percent (digits kept, rest stripped)
            "12abc",
            "abc12",
            "12kg",
            "kg12",
            "$12",
            "12%",
            "50%",
            "$1,000",
            "100USD",
            # Separators / operators that concatenated digits
            "1:2",
            "1;2",
            "1|2",
            "1*2",
            "1^2",
            "1 2",
            "1 000",
            # Brackets / approx marks
            "(12)",
            "[12]",
            "~12",
            "≈12",
            "≈0.5",
            # European-style comma decimal (not thousands) — was 1,2 -> 12
            "1,2",
            "1,00",
            # Empty / non-numeric already None; keep covered
            "",
            "   ",
            "abc",
            "NaN",
            "inf",
            # Multiple decimals / broken scientific (already None; keep covered)
            "1.2.3",
            "1e2e3",
            "1-2",
            "1+2",
        ],
    )
    def test_ambiguous_input_is_unparseable(self, raw: str) -> None:
        assert _parse_number(raw) is None

    @pytest.mark.parametrize(
        "raw",
        [
            "1/2",
            "3/4",
            "12kg",
            "$12",
            "12%",
            "1:2",
            "1 2",
            "(12)",
            "1,2",
            "≈0.5",
        ],
    )
    def test_ambiguous_scored_incorrect_never_coerced_to_match(self, raw: str) -> None:
        """Unparseable attempt is scored Incorrect, same as other malformed input.

        Crucially it must not silently become a different number that happens
        to match an accepted key (e.g. "1/2" must never match accepted "12").
        """
        # Accepted value that the OLD strip-then-float path would have matched
        # after mangling several of these inputs.
        item = _numeric_item("12", tolerance=1e-6)
        result = score_practice_response(item, raw)
        assert result.scored is True
        assert result.correct is False
        assert result.feedback_outcome == "Incorrect"
        assert result.matched_key == ""
        assert result.marks_awarded == 0.0

    def test_fraction_does_not_false_correct_against_concatenated_digits(self) -> None:
        item = _numeric_item("12", tolerance=1e-6)
        # Pre-fix: _parse_number("1/2") == 12.0 and this scored Correct.
        assert score_practice_response(item, "1/2").correct is False
        assert score_practice_response(item, "12").correct is True

    def test_unit_suffix_does_not_false_correct(self) -> None:
        item = _numeric_item("2", tolerance=0.001)
        # Pre-fix: "2%" / "2kg" stripped to 2.0 and scored Correct.
        assert score_practice_response(item, "2%").correct is False
        assert score_practice_response(item, "2kg").correct is False
        assert score_practice_response(item, "2").correct is True

    def test_genuine_unparseable_still_incorrect_like_before(self) -> None:
        item = _numeric_item("0.5", tolerance=0.01)
        for raw in ("abc", "NaN", "1.2.3"):
            result = score_practice_response(item, raw)
            assert result.scored is True
            assert result.correct is False
            assert result.feedback_outcome == "Incorrect"


# ---------------------------------------------------------------------------
# Live numeric checkpoints: identical scoring on clean accepted values
# ---------------------------------------------------------------------------


class TestLiveNumericCheckpointsUnchanged:
    """All 10 live numeric checkpoints: clean decimals/integers only."""

    def setup_method(self) -> None:
        reset_educational_package_cache()

    def test_ten_live_numeric_checkpoints_exist(self) -> None:
        loader = EducationalPackageLoader()
        found: dict[str, tuple[str, float | None]] = {}
        for pack in loader.all_approved():
            for check in pack.knowledge_checks:
                if check.kind == "checkpoint" and check.response_type == "numeric":
                    found[check.item_id] = (
                        check.accepted_keywords[0],
                        check.numeric_tolerance,
                    )
        assert len(found) == 10
        for item_id, accepted, tol in LIVE_NUMERIC_ACCEPTED:
            assert item_id in found
            assert found[item_id][0] == accepted
            assert found[item_id][1] == pytest.approx(tol)

    @pytest.mark.parametrize(
        ("item_id", "accepted", "tolerance"),
        LIVE_NUMERIC_ACCEPTED,
    )
    def test_live_item_scores_identically_on_clean_inputs(
        self,
        item_id: str,
        accepted: str,
        tolerance: float,
    ) -> None:
        """Exact / within-tol / outside-tol outcomes for real keys.

        All 10 accepted values are clean decimals or integers with no
        punctuation this fix changes. Snapshot expectations match the
        pre-fix scorer on these probes.
        """
        loader = EducationalPackageLoader()
        item: ScoreablePracticeItem | None = None
        for pack in loader.all_approved():
            substance = substance_from_package(
                pack,
                curriculum_identity=f"CS1:{pack.topic_code}",
                topic_id=pack.topic_code,
            )
            for act in substance.activities:
                if (
                    act.stage is EducationalStage.PRACTICE
                    and act.scoreable is not None
                    and act.scoreable.item_id == item_id
                ):
                    item = act.scoreable
                    break
            if item is not None:
                break
        assert item is not None
        assert item.response_type is PracticeResponseType.NUMERIC
        assert item.answer_key.accepted == (accepted,)
        assert item.answer_key.numeric_tolerance == pytest.approx(tolerance)

        expected = float(accepted)
        within = str(expected + tolerance * 0.5)
        outside = str(expected + tolerance * 2 + 0.01)

        exact = score_practice_response(item, accepted)
        assert exact.scored is True and exact.correct is True
        assert exact.feedback_outcome == "Correct"

        near = score_practice_response(item, within)
        assert near.scored is True and near.correct is True

        far = score_practice_response(item, outside)
        assert far.scored is True and far.correct is False
        assert far.feedback_outcome == "Incorrect"

        # Fraction / unit probes: honest Incorrect, never coerced.
        for bad in ("1/2", "2%", f"{accepted}kg"):
            mangled = score_practice_response(item, bad)
            assert mangled.scored is True
            assert mangled.correct is False
            assert mangled.feedback_outcome == "Incorrect"
