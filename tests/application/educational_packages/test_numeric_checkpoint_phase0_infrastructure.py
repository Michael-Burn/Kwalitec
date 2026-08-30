"""Phase 0 — numeric infrastructure for checkpoint Knowledge Checks.

Proves package JSON → loader → substance → scoring → UI branch wiring.
Does not convert live CS1 content; Active Recall stays short_structured.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    reset_educational_package_cache,
)
from app.application.educational_packages.models import KnowledgeCheck
from app.application.educational_packages.substance import (
    _scoreable_from_check,
    substance_from_package,
)
from app.application.learning_session.educational_flow import EducationalStage
from app.application.learning_session.scoreable_practice import (
    PracticeResponseType,
    score_practice_response,
)
from app.application.session_experience.activity_service import _build_activity
from app.infrastructure.adapters.learning_session.package_activity_engine import (
    _spec_to_sequence_item,
)

FIXTURE_ROOT = Path("tests/fixtures/numeric_checkpoint_phase0_packages")
SESSION_BODY = Path("app/templates/session/partials/session_body.html")


def setup_function() -> None:
    reset_educational_package_cache()


def _load_reference_package():
    loader = EducationalPackageLoader(root=FIXTURE_ROOT)
    packs = loader.all_approved()
    assert len(packs) == 1
    pack = packs[0]
    assert pack.package_id == "CS1-NUMERIC-PHASE0-REF"
    return pack


def test_loader_reads_numeric_tolerance_optional_field() -> None:
    pack = _load_reference_package()
    assert len(pack.knowledge_checks) == 3

    ar = pack.knowledge_checks[0]
    assert ar.kind == "active_recall"
    assert ar.response_type == "short_structured"
    assert ar.numeric_tolerance is None

    with_tol = pack.knowledge_checks[1]
    assert with_tol.kind == "checkpoint"
    assert with_tol.response_type == "numeric"
    assert with_tol.accepted_keywords == ("0.5",)
    assert with_tol.numeric_tolerance == pytest.approx(0.01)

    default_tol = pack.knowledge_checks[2]
    assert default_tol.kind == "checkpoint"
    assert default_tol.response_type == "numeric"
    assert default_tol.accepted_keywords == ("0.3",)
    assert default_tol.numeric_tolerance is None


def test_custom_tolerance_scores_against_authored_tolerance() -> None:
    """(a) Custom tolerance is used — not the scorer's 1e-6 default."""
    pack = _load_reference_package()
    substance = substance_from_package(
        pack,
        curriculum_identity="CS1:numeric-phase0",
        topic_id="NUMERIC-PHASE0-REF",
    )
    practice = [a for a in substance.activities if a.stage is EducationalStage.PRACTICE]
    assert len(practice) == 3

    custom = practice[1]
    assert custom.scoreable is not None
    assert custom.scoreable.response_type is PracticeResponseType.NUMERIC
    assert custom.scoreable.answer_key.accepted == ("0.5",)
    assert custom.scoreable.answer_key.numeric_tolerance == pytest.approx(0.01)
    assert custom.answer_prompt == "Your numeric answer"

    # Within 0.01 of 0.5, but far outside 1e-6 → must score correct.
    near = score_practice_response(custom.scoreable, "0.505")
    assert near.scored is True
    assert near.correct is True
    assert near.feedback_outcome == "Correct"

    # Outside authored 0.01 → incorrect.
    far = score_practice_response(custom.scoreable, "0.52")
    assert far.scored is True
    assert far.correct is False
    assert far.feedback_outcome == "Incorrect"


def test_omitted_tolerance_keeps_scorer_1e6_default() -> None:
    """(b) Packages without numeric_tolerance keep AnswerKey.None → 1e-6."""
    pack = _load_reference_package()
    substance = substance_from_package(
        pack,
        curriculum_identity="CS1:numeric-phase0",
        topic_id="NUMERIC-PHASE0-REF",
    )
    practice = [a for a in substance.activities if a.stage is EducationalStage.PRACTICE]
    default_item = practice[2]
    assert default_item.scoreable is not None
    assert default_item.scoreable.response_type is PracticeResponseType.NUMERIC
    assert default_item.scoreable.answer_key.numeric_tolerance is None

    exact = score_practice_response(default_item.scoreable, "0.3")
    assert exact.correct is True

    # 2e-6 away — accepted under a looser custom tol, rejected under 1e-6.
    slightly_off = score_practice_response(default_item.scoreable, "0.300002")
    assert slightly_off.correct is False

    within_default = score_practice_response(default_item.scoreable, "0.3000005")
    assert within_default.correct is True


def test_numeric_empty_accepted_keywords_raises_authoring_error() -> None:
    """(c) Footgun fix: numeric must not fall back to ('explain', 'link')."""
    pack = _load_reference_package()
    bad = KnowledgeCheck(
        episode_id="lep-bad-numeric",
        kind="checkpoint",
        item_id="bad-numeric-empty-kw",
        title="Bad numeric",
        prompt="Enter a number",
        response_type="numeric",
        accepted_keywords=(),
    )
    with pytest.raises(ValueError, match="accepted_keywords"):
        _scoreable_from_check(bad, pack=pack)


def test_package_engine_opaque_carries_numeric_tolerance() -> None:
    pack = _load_reference_package()
    substance = substance_from_package(
        pack,
        curriculum_identity="CS1:numeric-phase0",
        topic_id="NUMERIC-PHASE0-REF",
    )
    practice = [a for a in substance.activities if a.stage is EducationalStage.PRACTICE]
    custom_spec = practice[1]
    item = _spec_to_sequence_item(custom_spec, index=2, total=3)
    assert item["response_type"] == "numeric"
    assert item["scoreable"]["answer_key"]["accepted"] == ["0.5"]
    assert item["scoreable"]["answer_key"]["numeric_tolerance"] == pytest.approx(0.01)

    domain = _build_activity("sess-numeric-phase0", item)
    assert domain.response_type == "numeric"


def test_session_body_branches_on_numeric() -> None:
    """(d) Template: numeric input for numeric; MCQ/textarea branches intact."""
    text = SESSION_BODY.read_text(encoding="utf-8")
    assert "s.response_type == 'numeric'" in text
    assert 'inputmode="decimal"' in text
    assert 'class="ds-input"' in text
    # MCQ and textarea fallback unchanged.
    assert "s.response_type == 'mcq'" in text
    assert "s.practice_choices" in text
    assert "ds-exam-row" in text
    assert "ds-textarea" in text
    assert "answer_form.choice.name" in text
    # Textarea remains the else-branch fallback for non-mcq / non-numeric.
    numeric_idx = text.index("s.response_type == 'numeric'")
    textarea_idx = text.index("ds-textarea", numeric_idx)
    assert textarea_idx > numeric_idx
