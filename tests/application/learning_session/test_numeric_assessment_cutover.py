"""Flag-gated Numeric Assessment Framework cutover for live scoring.

Proves:
1. Flag defaults OFF and is not inherited by Commercial Loop.
2. Flag OFF: all 30 migrated numerics score byte-for-byte as the legacy path.
3. Flag ON: all 30 score under the framework; the 4 banked precision items
   correctly reject previously-accepted 3dp rounding.
4. Evidence-relevant fields (OEA / Twin / Spacing) are identical across flag
   states whenever correctness agrees.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    reset_educational_package_cache,
)
from app.application.educational_packages.substance import substance_from_package
from app.application.learning_session.educational_flow import EducationalStage
from app.application.learning_session.scoreable_practice import (
    AnswerKey,
    MarkScheme,
    PracticeResponseType,
    ScoreablePracticeItem,
    score_practice_response,
)
from app.application.numeric_assessment import (
    BANKED_PRECISION_TOLERANCE_ITEM_IDS,
    LIVE_NUMERIC_CHECKPOINT_COUNT,
    evaluate,
    get_live_answer_specification,
    load_live_answer_specifications,
    reset_live_answer_specification_cache,
)
from app.application.objective_evidence.recorder import (
    ObjectiveAssessmentEvidenceRecorder,
)
from app.application.objective_evidence.store import (
    ObjectiveAssessmentEvidenceStore,
)


@pytest.fixture(autouse=True)
def _reset_caches() -> None:
    reset_educational_package_cache()
    reset_live_answer_specification_cache()


def _flags(*, framework: bool):
    return resolve_v2_feature_flags(
        environ={
            "SR_NUMERIC_ASSESSMENT_FRAMEWORK": "1" if framework else "0",
            "KWALITEC_COMMERCIAL_LOOP": "0",
            "KWALITEC_V2_SOLE_RUNTIME": "0",
        }
    )


def _live_numeric_accepted() -> dict[str, tuple[str, float]]:
    found: dict[str, tuple[str, float]] = {}
    for pack in EducationalPackageLoader().all_approved():
        for check in pack.knowledge_checks:
            if check.kind == "checkpoint" and check.response_type == "numeric":
                found[check.item_id] = (
                    check.accepted_keywords[0],
                    float(check.numeric_tolerance),
                )
    return found


def _all_item_ids() -> list[str]:
    reset_educational_package_cache()
    return sorted(_live_numeric_accepted().keys())


def _scoreable(item_id: str):
    for pack in EducationalPackageLoader().all_approved():
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
                return act.scoreable
    raise AssertionError(f"missing scoreable {item_id}")


def _score_snapshot(score) -> dict:
    """Student-facing + scoring fields for byte-for-byte OFF comparison."""
    return {
        "scored": score.scored,
        "correct": score.correct,
        "marks_awarded": score.marks_awarded,
        "marks_available": score.marks_available,
        "matched_key": score.matched_key,
        "feedback_outcome": score.feedback_outcome,
        "explanation": score.explanation,
        "model_answer": score.model_answer,
        "common_mistake": score.common_mistake,
        "next_action": score.next_action,
        "emit_structured": score.emit_structured,
        "item_id": score.item_id,
        "response_type": score.response_type,
        "selected_misconception_tag": score.selected_misconception_tag,
        "scored_correct": score.scored_correct,
        "opaque": score.to_opaque(),
    }


def _evidence_fields(score) -> dict:
    """Fields consumed by OEA / Twin / Spacing (not student feedback prose)."""
    return {
        "item_id": score.item_id,
        "response_type": score.response_type,
        "scored_correct": score.scored_correct,
        "selected_misconception_tag": score.selected_misconception_tag,
        "marks_awarded": score.marks_awarded,
        "marks_available": score.marks_available,
        "emit_structured": score.emit_structured,
    }


class TestNumericAssessmentFrameworkFlag:
    def test_defaults_off_and_not_inherited_from_commercial_loop(self):
        bare = resolve_v2_feature_flags(environ={})
        assert bare.SR_NUMERIC_ASSESSMENT_FRAMEWORK is False

        loop_on = resolve_v2_feature_flags(
            environ={"KWALITEC_COMMERCIAL_LOOP": "1"}
        )
        assert loop_on.SR_NUMERIC_ASSESSMENT_FRAMEWORK is False
        assert loop_on.SR_SESSION_PRIMARY is True

        explicit = resolve_v2_feature_flags(
            environ={"SR_NUMERIC_ASSESSMENT_FRAMEWORK": "1"}
        )
        assert explicit.SR_NUMERIC_ASSESSMENT_FRAMEWORK is True

    def test_enabled_in_render_yaml(self):
        from tests.operational.helpers import render_env_map

        env = render_env_map()
        assert env.get("SR_NUMERIC_ASSESSMENT_FRAMEWORK") == "1"


@pytest.mark.parametrize("item_id", _all_item_ids())
def test_flag_off_matches_forced_legacy_byte_for_byte(item_id: str) -> None:
    """Flag OFF (default posture) equals an explicit legacy scoring pass."""
    live = _live_numeric_accepted()
    accepted, _tol = live[item_id]
    item = _scoreable(item_id)

    via_default = score_practice_response(item, accepted)
    via_flag_off = score_practice_response(
        item, accepted, flags=_flags(framework=False)
    )
    assert _score_snapshot(via_default) == _score_snapshot(via_flag_off)

    wrong = "999999.123456"
    via_default_w = score_practice_response(item, wrong)
    via_flag_off_w = score_practice_response(
        item, wrong, flags=_flags(framework=False)
    )
    assert _score_snapshot(via_default_w) == _score_snapshot(via_flag_off_w)


@pytest.mark.parametrize("item_id", _all_item_ids())
def test_flag_on_accepted_answer_correct_under_framework(item_id: str) -> None:
    live = _live_numeric_accepted()
    accepted, _tol = live[item_id]
    item = _scoreable(item_id)
    spec = load_live_answer_specifications()[item_id]

    scored = score_practice_response(
        item, accepted, flags=_flags(framework=True)
    )
    framework = evaluate(spec, accepted)

    assert scored.scored is True
    assert scored.correct is True
    assert scored.correct is framework.value_correct
    assert scored.feedback_outcome == "Correct"
    assert scored.common_mistake == ""
    assert scored.selected_misconception_tag == ""


@pytest.mark.parametrize(
    "item_id",
    sorted(BANKED_PRECISION_TOLERANCE_ITEM_IDS),
)
def test_flag_on_rejects_banked_three_dp_rounding(item_id: str) -> None:
    """The only intentional correctness flip when the flag turns ON."""
    live = _live_numeric_accepted()
    accepted, legacy_tol = live[item_id]
    assert legacy_tol == pytest.approx(0.001)
    three_dp = f"{round(float(accepted), 3):.3f}"
    assert three_dp != accepted

    item = _scoreable(item_id)
    off = score_practice_response(
        item, three_dp, flags=_flags(framework=False)
    )
    on = score_practice_response(
        item, three_dp, flags=_flags(framework=True)
    )

    assert off.correct is True
    assert on.correct is False
    assert on.feedback_outcome == "Incorrect"
    assert on.common_mistake
    assert on.selected_misconception_tag == ""


def test_catalogue_count_is_thirty() -> None:
    assert len(_live_numeric_accepted()) == LIVE_NUMERIC_CHECKPOINT_COUNT
    assert len(load_live_answer_specifications()) == LIVE_NUMERIC_CHECKPOINT_COUNT


def test_only_banked_items_change_correctness_on_three_dp() -> None:
    """Across all 30, the sole OFF→ON correctness flip on 3dp is the banked four."""
    live = _live_numeric_accepted()
    flips: list[str] = []
    for item_id, (accepted, _tol) in live.items():
        three_dp = f"{round(float(accepted), 3):.3f}"
        if three_dp == accepted:
            continue
        item = _scoreable(item_id)
        off = score_practice_response(
            item, three_dp, flags=_flags(framework=False)
        )
        on = score_practice_response(
            item, three_dp, flags=_flags(framework=True)
        )
        if bool(off.correct) != bool(on.correct):
            flips.append(item_id)
    assert set(flips) == set(BANKED_PRECISION_TOLERANCE_ITEM_IDS)


def test_evidence_fields_identical_when_verdicts_agree() -> None:
    """OEA / Twin / Spacing consume scored_correct + tag; prose is irrelevant.

    For every migrated item, the canonical accepted answer and a far-wrong
    answer produce identical evidence fields under flag OFF and ON.
    """
    live = _live_numeric_accepted()
    for item_id, (accepted, _tol) in live.items():
        item = _scoreable(item_id)
        for response in (accepted, "999999.123456"):
            off = score_practice_response(
                item, response, flags=_flags(framework=False)
            )
            on = score_practice_response(
                item, response, flags=_flags(framework=True)
            )
            assert off.scored_correct == on.scored_correct
            assert _evidence_fields(off) == _evidence_fields(on)


def test_oea_recording_identical_when_verdicts_agree(app) -> None:
    """Recorder path untouched: same score evidence fields → same record body."""
    live = _live_numeric_accepted()
    item_id = sorted(live.keys())[0]
    accepted = live[item_id][0]
    item = _scoreable(item_id)
    if not any("-LO" in str(oid).upper() for oid in (item.objective_ids or ())):
        item = replace(item, objective_ids=("CS1-TEST-LO01",))

    store_off = ObjectiveAssessmentEvidenceStore()
    store_on = ObjectiveAssessmentEvidenceStore()
    rec_off = ObjectiveAssessmentEvidenceRecorder(store=store_off)
    rec_on = ObjectiveAssessmentEvidenceRecorder(store=store_on)

    score_off = score_practice_response(
        item, accepted, flags=_flags(framework=False)
    )
    score_on = score_practice_response(
        item, accepted, flags=_flags(framework=True)
    )
    assert _evidence_fields(score_off) == _evidence_fields(score_on)

    fixed = datetime(2026, 9, 12, 12, 0, 0, tzinfo=UTC)
    out_off = rec_off.record_if_tagged(
        student_id="s1",
        session_id="sess1",
        package_id="pkg1",
        scoreable=item,
        score=score_off,
        occurred_at=fixed,
    )
    out_on = rec_on.record_if_tagged(
        student_id="s1",
        session_id="sess1",
        package_id="pkg1",
        scoreable=item,
        score=score_on,
        occurred_at=fixed,
    )
    assert out_off is not None and out_on is not None
    assert out_off.student_id == out_on.student_id
    assert out_off.objective_id == out_on.objective_id
    assert out_off.item_id == out_on.item_id
    assert out_off.package_id == out_on.package_id
    assert out_off.session_id == out_on.session_id
    assert out_off.response_type == out_on.response_type
    assert out_off.scored_correct == out_on.scored_correct
    assert out_off.selected_misconception_tag == out_on.selected_misconception_tag
    assert out_off.source == out_on.source
    assert out_off.occurred_at == out_on.occurred_at


def test_fallback_to_legacy_when_no_answer_specification() -> None:
    """Safety: numeric item without a catalogue spec stays on the old path."""
    orphan = ScoreablePracticeItem(
        item_id="orphan-numeric-no-spec",
        prompt="Compute 2+2.",
        response_type=PracticeResponseType.NUMERIC,
        answer_key=AnswerKey(accepted=("4",), numeric_tolerance=1e-6),
        mark_scheme=MarkScheme(max_marks=1),
        explanation="Four.",
        model_answer="4",
        common_mistake="Arithmetic slip.",
    )
    assert get_live_answer_specification(orphan.item_id) is None

    on = score_practice_response(
        orphan, "4", flags=_flags(framework=True)
    )
    off = score_practice_response(
        orphan, "4", flags=_flags(framework=False)
    )
    assert _score_snapshot(on) == _score_snapshot(off)
    assert on.correct is True
    assert on.common_mistake == ""
