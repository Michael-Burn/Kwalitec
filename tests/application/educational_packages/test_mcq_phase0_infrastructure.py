"""Phase 0 — MCQ infrastructure for checkpoint Knowledge Checks.

Proves package JSON → loader → substance → scoring → UI branch wiring.
Does not rewrite live short_structured content. Active Recall remains
short_structured in the synthetic fixture (separate later scoping pass).
"""

from __future__ import annotations

from pathlib import Path

from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    find_educational_package,
    reset_educational_package_cache,
)
from app.application.educational_packages.substance import substance_from_package
from app.application.learning_session.educational_flow import EducationalStage
from app.application.learning_session.scoreable_practice import (
    PracticeResponseType,
    score_practice_response,
)
from app.application.session_experience.activity_service import _build_activity
from app.infrastructure.adapters.learning_session.package_activity_engine import (
    _spec_to_sequence_item,
)
from app.presentation.session.forms import SubmitAnswerForm

FIXTURE_ROOT = Path("tests/fixtures/educational_packages")
SESSION_BODY = Path("app/templates/session/partials/session_body.html")
LIVE_PACKAGE_ROOT = Path("app/curriculum/data/educational_packages")


def setup_function() -> None:
    reset_educational_package_cache()


def _load_reference_package():
    loader = EducationalPackageLoader(root=FIXTURE_ROOT)
    packs = loader.all_approved()
    assert len(packs) == 1
    pack = packs[0]
    assert pack.package_id == "CS1-MCQ-PHASE0-REF"
    return pack


def test_loader_reads_mcq_choices_and_correct_choice_id() -> None:
    pack = _load_reference_package()
    assert len(pack.knowledge_checks) == 2

    ar = pack.knowledge_checks[0]
    assert ar.kind == "active_recall"
    assert ar.response_type == "short_structured"
    assert ar.choices == ()
    assert ar.correct_choice_id == ""

    cp = pack.knowledge_checks[1]
    assert cp.kind == "checkpoint"
    assert cp.response_type == "mcq"
    assert cp.correct_choice_id == "b"
    assert [c.id for c in cp.choices] == ["a", "b", "c"]
    assert cp.choices[0].label == "3"
    assert cp.choices[0].misconception_tag == "off_by_one"
    assert cp.choices[1].label == "4"
    assert cp.accepted_keywords == ()


def test_scoreable_from_check_scores_correct_and_incorrect() -> None:
    pack = _load_reference_package()
    substance = substance_from_package(
        pack,
        curriculum_identity="CS1:mcq-phase0",
        topic_id="MCQ-PHASE0-REF",
    )
    practice = [a for a in substance.activities if a.stage is EducationalStage.PRACTICE]
    assert len(practice) == 2

    short = practice[0]
    assert short.scoreable is not None
    assert short.scoreable.response_type is PracticeResponseType.SHORT_STRUCTURED
    assert short.scoreable.choices == ()
    assert short.answer_prompt == "Your answer"

    mcq = practice[1]
    assert mcq.scoreable is not None
    assert mcq.scoreable.response_type is PracticeResponseType.MCQ
    assert mcq.scoreable.answer_key.correct_choice_id == "b"
    assert mcq.scoreable.choices == (("a", "3"), ("b", "4"), ("c", "5"))
    assert mcq.answer_prompt == "Select your answer"

    ok = score_practice_response(mcq.scoreable, "b")
    assert ok.scored is True
    assert ok.correct is True
    assert ok.feedback_outcome == "Correct"
    assert ok.scored_correct is True

    bad = score_practice_response(mcq.scoreable, "a")
    assert bad.scored is True
    assert bad.correct is False
    assert bad.feedback_outcome == "Incorrect"
    assert bad.scored_correct is False
    assert bad.common_mistake == "Selecting an adjacent integer."


def test_package_engine_opaque_carries_choices() -> None:
    pack = _load_reference_package()
    substance = substance_from_package(
        pack,
        curriculum_identity="CS1:mcq-phase0",
        topic_id="MCQ-PHASE0-REF",
    )
    practice = [a for a in substance.activities if a.stage is EducationalStage.PRACTICE]
    mcq_spec = practice[1]
    item = _spec_to_sequence_item(mcq_spec, index=2, total=2)
    assert item["response_type"] == "mcq"
    assert item["choices"] == [
        {"id": "a", "label": "3"},
        {"id": "b", "label": "4"},
        {"id": "c", "label": "5"},
    ]
    assert item["scoreable"]["answer_key"]["correct_choice_id"] == "b"

    domain = _build_activity("sess-mcq-phase0", item)
    assert domain.response_type == "mcq"
    assert domain.choices == (("a", "3"), ("b", "4"), ("c", "5"))


def test_submit_answer_form_resolves_choice_id(app) -> None:
    with app.app_context():
        form = SubmitAnswerForm(
            data={
                "session_id": "sess-1",
                "activity_id": "act-practice-2",
                "choice": "b",
            }
        )
        assert form.resolved_response() == "b"
        assert form.validate() is True

        empty = SubmitAnswerForm(
            data={
                "session_id": "sess-1",
                "activity_id": "act-practice-2",
                "response": "",
                "choice": "",
            }
        )
        assert empty.resolved_response() == ""
        assert empty.validate() is False


def test_session_body_branches_on_mcq() -> None:
    text = SESSION_BODY.read_text(encoding="utf-8")
    assert "s.response_type == 'mcq'" in text
    assert "s.practice_choices" in text
    assert "ds-exam-row" in text
    assert "ds-textarea" in text
    assert "answer_form.choice.name" in text


def test_live_short_structured_packages_untouched() -> None:
    """All live inventory packages remain short_structured; no choices authored."""
    reset_educational_package_cache()
    packs = EducationalPackageLoader(root=LIVE_PACKAGE_ROOT).all_approved()
    assert packs, "expected live educational packages"
    for pack in packs:
        assert pack.package_id != "CS1-MCQ-PHASE0-REF"
        for check in pack.knowledge_checks:
            assert check.response_type == "short_structured"
            assert check.choices == ()
            assert check.correct_choice_id == ""
            assert check.accepted_keywords  # existing keyword scoring still present

    # Spot-check a known live package still resolves and scores as before.
    live = find_educational_package(topic_code="2.5", subject_id="CS1")
    assert live is not None
    substance = substance_from_package(
        live,
        curriculum_identity="CS1:live-compat",
        topic_id=live.topic_code,
    )
    practice = [a for a in substance.activities if a.stage is EducationalStage.PRACTICE]
    assert practice
    for act in practice:
        assert act.scoreable is not None
        assert act.scoreable.response_type is PracticeResponseType.SHORT_STRUCTURED
        assert act.scoreable.choices == ()
        assert act.scoreable.answer_key.correct_choice_id == ""
