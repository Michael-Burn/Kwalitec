"""Phase-0 prototype — choice-aware feedback via misconception_tag.

Proves allowlisted items get choice-specific mistake copy, correctness
matching is unchanged, correct-answer path is untouched, and the selected
misconception_tag is captured on the score / evidence log path.
"""

from __future__ import annotations

from pathlib import Path

from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    reset_educational_package_cache,
)
from app.application.educational_packages.substance import substance_from_package
from app.application.learning_session.choice_aware_feedback_prototype import (
    PROTOTYPE_CHOICE_FEEDBACK,
    PROTOTYPE_ITEM_IDS,
    assemble_choice_aware_mistake,
)
from app.application.learning_session.educational_flow import EducationalStage
from app.application.learning_session.scoreable_practice import (
    PracticeResponseType,
    ScoreablePracticeItem,
    _match_mcq,
    score_practice_response,
)
from app.infrastructure.adapters.learning_session.package_activity_engine import (
    PackageActivityEngine,
)
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.session.store import SessionDocumentStore

LIVE_PACKAGE_ROOT = Path("app/curriculum/data/educational_packages")

# (package stem under cs1/, item_id)
_PROTOTYPE_PACKAGES: tuple[tuple[str, str], ...] = (
    ("3.1.3-efficiency-bias-consistency-mse-cs1010", "cs1010-3.1.3-cp-01"),
    ("4.2.1-exponential-family-cs1014", "cs1014-4.2.1-ar-01"),
    ("cr-2.1.2-continuous-cs1017", "cs1017-2.1.2-cp-01"),
    ("revision-estimators-cs1010", "cs1010-ck-r1-cp-01"),
)


def setup_function() -> None:
    reset_educational_package_cache()


def _scoreable_for(item_id: str) -> ScoreablePracticeItem:
    loader = EducationalPackageLoader(root=LIVE_PACKAGE_ROOT)
    for stem, want_id in _PROTOTYPE_PACKAGES:
        if want_id != item_id:
            continue
        packs = [
            p
            for p in loader.all_approved()
            if p.source_path and Path(p.source_path).stem == stem
        ]
        assert packs, f"package for {stem} not found"
        pack = packs[0]
        substance = substance_from_package(
            pack,
            curriculum_identity=f"CS1:choice-aware:{stem}",
            topic_id=pack.topic_code,
        )
        for act in substance.activities:
            if (
                act.stage is EducationalStage.PRACTICE
                and act.scoreable is not None
                and act.scoreable.item_id == item_id
            ):
                return act.scoreable
        raise AssertionError(f"scoreable {item_id} not found in {stem}")
    raise AssertionError(f"unknown prototype item_id {item_id}")


def test_prototype_allowlist_is_exactly_four_items() -> None:
    assert PROTOTYPE_ITEM_IDS == {want for _, want in _PROTOTYPE_PACKAGES}
    assert len(PROTOTYPE_ITEM_IDS) == 4


def test_wrong_answers_on_same_item_yield_distinct_choice_aware_feedback() -> None:
    item = _scoreable_for("cs1014-4.2.1-ar-01")
    assert item.response_type is PracticeResponseType.MCQ

    bad_b = score_practice_response(item, "b")
    bad_c = score_practice_response(item, "c")
    assert bad_b.scored is True and bad_b.correct is False
    assert bad_c.scored is True and bad_c.correct is False
    assert bad_b.common_mistake != bad_c.common_mistake
    assert bad_b.common_mistake == PROTOTYPE_CHOICE_FEEDBACK[
        ("cs1014-4.2.1-ar-01", "b")
    ]
    assert bad_c.common_mistake == PROTOTYPE_CHOICE_FEEDBACK[
        ("cs1014-4.2.1-ar-01", "c")
    ]
    # Distinct from the bundled generic common_mistake.
    assert bad_b.common_mistake != item.common_mistake
    assert bad_c.common_mistake != item.common_mistake


def test_correct_answer_path_unaffected() -> None:
    item = _scoreable_for("cs1010-3.1.3-cp-01")
    ok = score_practice_response(item, "a")
    assert ok.scored is True
    assert ok.correct is True
    assert ok.feedback_outcome == "Correct"
    assert ok.common_mistake == ""
    assert ok.selected_misconception_tag == ""
    assert ok.explanation == item.explanation
    assert ok.model_answer == item.model_answer
    assert ok.marks_awarded == float(item.mark_scheme.max_marks)


def test_scoring_correctness_logic_unchanged_for_choice_tuples() -> None:
    """_match_mcq returns the same verdicts with or without misconception_tag."""
    item = _scoreable_for("cs1017-2.1.2-cp-01")
    stripped_choices = tuple((c[0], c[1]) for c in item.choices)
    stripped = ScoreablePracticeItem(
        item_id=item.item_id,
        prompt=item.prompt,
        response_type=item.response_type,
        answer_key=item.answer_key,
        explanation=item.explanation,
        model_answer=item.model_answer,
        mark_scheme=item.mark_scheme,
        common_mistake=item.common_mistake,
        next_action=item.next_action,
        choices=stripped_choices,
        emit_structured=item.emit_structured,
        body=item.body,
        supporting_material=item.supporting_material,
        hints=item.hints,
    )
    for response in ("a", "b", "c", "d"):
        assert _match_mcq(item, response) == _match_mcq(stripped, response)


def test_misconception_tag_captured_on_score_and_evidence_log() -> None:
    item = _scoreable_for("cs1010-ck-r1-cp-01")
    bad = score_practice_response(item, "b")
    assert bad.correct is False
    assert bad.selected_misconception_tag == "unsquared_bias"
    opaque = bad.to_opaque()
    assert opaque["selected_misconception_tag"] == "unsquared_bias"
    # Tag must not appear in student-facing common_mistake copy.
    assert "unsquared_bias" not in bad.common_mistake

    loader = EducationalPackageLoader(root=LIVE_PACKAGE_ROOT)
    packs = [
        p
        for p in loader.all_approved()
        if p.source_path and Path(p.source_path).stem == "revision-estimators-cs1010"
    ]
    assert packs
    pack = packs[0]
    substance = substance_from_package(
        pack,
        curriculum_identity="CS1:choice-aware-evidence",
        topic_id=pack.topic_code,
    )
    store = SessionDocumentStore()
    persistence = LearningSessionPersistenceAdapter(store=store)
    engine = PackageActivityEngine(store=store, persistence=persistence)
    engine.provision_sequence("stu-ca", session_id="sess-ca", substance=substance)

    current = engine.get_current_activity_opaque("stu-ca", session_id="sess-ca")
    while current is not None:
        seq = store.get(
            PackageActivityEngine.NS_SEQUENCE,
            PackageActivityEngine._key("stu-ca", "sess-ca"),
        )
        assert seq is not None
        index = int(seq.get("index") or 1)
        act = list(seq.get("activities") or [])[index - 1]
        item_id = str((act.get("scoreable") or {}).get("item_id") or "")
        if item_id == "cs1010-ck-r1-cp-01":
            result = engine.submit_response_opaque(
                "stu-ca",
                session_id="sess-ca",
                activity_id=str(current["activity_id"]),
                response="b",
            )
            assert result.get("common_mistake") == PROTOTYPE_CHOICE_FEEDBACK[
                ("cs1010-ck-r1-cp-01", "b")
            ]
            responses = store.get(
                PackageActivityEngine.NS_RESPONSES,
                PackageActivityEngine._key("stu-ca", "sess-ca"),
            )
            assert responses is not None
            logged = responses["items"][-1]
            assert logged["selected_misconception_tag"] == "unsquared_bias"
            assert logged["score"]["selected_misconception_tag"] == "unsquared_bias"
            return
        engine.submit_response_opaque(
            "stu-ca",
            session_id="sess-ca",
            activity_id=str(current["activity_id"]),
            response="a" if current.get("response_type") == "mcq" else "noted",
        )
        current = engine.advance_activity_opaque("stu-ca", session_id="sess-ca")

    raise AssertionError("checkpoint practice item never reached")


def test_all_prototype_items_have_authored_feedback_for_distractors() -> None:
    for item_id in sorted(PROTOTYPE_ITEM_IDS):
        item = _scoreable_for(item_id)
        correct_id = item.answer_key.correct_choice_id
        for choice in item.choices:
            cid = choice[0]
            if cid == correct_id:
                continue
            text, tag = assemble_choice_aware_mistake(item, cid, correct=False)
            assert (item_id, cid) in PROTOTYPE_CHOICE_FEEDBACK
            assert text == PROTOTYPE_CHOICE_FEEDBACK[(item_id, cid)]
            assert text != item.common_mistake
            assert tag  # every distractor carries a misconception_tag
            assert tag not in text  # slug not echoed to the student
