"""Presentation-time MCQ display-order randomization.

Stored choice ids, labels, tags, and correct_choice_id are never reordered.
Radio values remain stored ids, so scoring, choice-aware feedback, and
Progression Readiness keep resolving by id regardless of display position.
"""

from __future__ import annotations

import random
import re
from datetime import UTC, datetime
from itertools import permutations
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    reset_educational_package_cache,
)
from app.application.educational_packages.substance import substance_from_package
from app.application.learning_session.choice_aware_feedback_prototype import (
    PROTOTYPE_CHOICE_FEEDBACK,
)
from app.application.learning_session.educational_flow import EducationalStage
from app.application.learning_session.scoreable_practice import (
    choice_parts,
    score_practice_response,
)
from app.application.objective_evidence.records import AssessmentEvidenceRecord
from app.application.progression_readiness import (
    CS1_C_T01_LO01,
    ProgressionReadiness,
    evaluate,
)
from app.domain.session_experience.session_workspace import SessionSurface
from app.presentation.session.mcq_display_order import shuffle_mcq_display_order
from app.presentation.session.services.study_session_service import (
    StudySessionService,
    _practice_feedback_parts,
)
from app.presentation.session.view_models import (
    ActivityViewModel,
    SessionPageViewModel,
    SessionShellViewModel,
)
from tests.presentation.session.test_session_redesign import _base_page, _render

LIVE_PACKAGE_ROOT = Path("app/curriculum/data/educational_packages")

# Representative live packages from different syllabus areas.
_SAMPLE_STEMS = (
    "1.1-purpose-function-ep001",
    "2.1.3-prob-quantiles-cs1004",
    "3.1.1-method-of-moments-cs1010",
    "4.2.1-exponential-family-cs1014",
    "4.2.9-goodness-tests-cs1014",
    "5.1.3-posterior-simple-cs1003",
    "5.1.5-credible-intervals-cs1003",
    "revision-estimators-cs1010",
)

# CAF items plus a known distractor id whose authored feedback must still fire.
_CAF_SAMPLES = (
    ("revision-estimators-cs1010", "cs1010-ck-r1-ar-01", "b"),
    ("5.1.3-posterior-simple-cs1003", "cs1003-5.1.3-cp-01", "c"),
    ("3.1.1-method-of-moments-cs1010", "cs1010-3.1.1-ar-01", "d"),
)


def setup_function() -> None:
    reset_educational_package_cache()


def _pack_for_stem(stem: str):
    loader = EducationalPackageLoader(root=LIVE_PACKAGE_ROOT)
    packs = [
        p
        for p in loader.all_approved()
        if p.source_path and Path(p.source_path).stem == stem
    ]
    assert packs, f"approved package for {stem} not found"
    return packs[0]


def _mcq_pairs_from_stem(stem: str) -> tuple[tuple[str, str], ...]:
    pack = _pack_for_stem(stem)
    for check in pack.knowledge_checks:
        rt = (check.response_type or "").strip().lower()
        if rt in {"mcq", "multiple_choice"} and len(check.choices) >= 3:
            return tuple((c.id, c.label) for c in check.choices)
    raise AssertionError(f"no MCQ with 3+ choices in {stem}")


def _scoreable(stem: str, item_id: str):
    pack = _pack_for_stem(stem)
    substance = substance_from_package(
        pack,
        curriculum_identity=f"CS1:display-order:{stem}",
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


def _activity_page(choices: tuple[tuple[str, str], ...]) -> SessionPageViewModel:
    return SessionPageViewModel(
        shell=SessionShellViewModel(
            session_id="sess-display-order",
            student_id="1",
            active_surface="activity",
        ),
        activity=ActivityViewModel(
            activity_id="act-mcq",
            activity_type="practice",
            response_type="mcq",
            requires_response=True,
            choices=choices,
        ),
    )


def _answer_form_stub():
    return SimpleNamespace(
        hidden_tag=lambda: "",
        session_id=lambda: "",
        activity_id=lambda: "",
        choice=SimpleNamespace(name="choice"),
        response=SimpleNamespace(name="response", id="response"),
    )


def test_shuffle_preserves_id_label_pairs_and_does_not_mutate_input() -> None:
    original = [("a", "First"), ("b", "Second"), ("c", "Third"), ("d", "Fourth")]
    snapshot = list(original)
    shuffled = shuffle_mcq_display_order(original, rng=random.Random(7))
    assert original == snapshot
    assert set(shuffled) == set(tuple(p) for p in original)
    assert shuffled != tuple(original)


def test_display_order_randomized_across_repeated_renders_of_live_items() -> None:
    """Repeated presentation of the same stored choices must not stay fixed."""
    service = StudySessionService()
    for stem in _SAMPLE_STEMS:
        stored = _mcq_pairs_from_stem(stem)
        assert stored[0][0] == "a"
        page = _activity_page(stored)
        seen: set[tuple[tuple[str, str], ...]] = set()
        for seed in range(48):
            # Seeded helper proves the shuffle itself is not identity.
            helper_order = shuffle_mcq_display_order(
                stored, rng=random.Random(seed)
            )
            seen.add(helper_order)
            assert set(helper_order) == set(stored)
        assert len(seen) >= 8, f"{stem} produced too few distinct helper orders"

        render_orders: set[tuple[tuple[str, str], ...]] = set()
        for _ in range(36):
            content = service._content(page, SessionSurface.ACTIVITY)
            order = tuple(content["practice_choices"])
            render_orders.add(order)
            assert set(order) == set(stored)
            # Stored activity choices stay in authored order.
            assert page.activity.choices == stored
        assert len(render_orders) >= 2, (
            f"{stem} display order was fixed across repeated _content renders"
        )


def test_correct_choice_and_distractor_feedback_independent_of_display_order() -> None:
    """Scoring and CAF resolve by stored id, never by displayed row."""
    for stem, item_id, distractor_id in _CAF_SAMPLES:
        item = _scoreable(stem, item_id)
        correct_id = item.answer_key.correct_choice_id
        assert correct_id
        pairs = tuple((choice_parts(c)[0], choice_parts(c)[1]) for c in item.choices)
        expected_feedback = PROTOTYPE_CHOICE_FEEDBACK[(item_id, distractor_id)]
        distractor_label = next(
            label for cid, label in pairs if cid == distractor_id
        )

        for displayed in permutations(pairs):
            displayed_t = tuple(displayed)
            assert set(displayed_t) == set(pairs)

            scored_ok = score_practice_response(item, correct_id)
            assert scored_ok.correct is True

            scored_wrong = score_practice_response(item, distractor_id)
            assert scored_wrong.correct is False
            assert scored_wrong.common_mistake == expected_feedback
            assert scored_wrong.selected_misconception_tag

            # The distractor may sit in any displayed row; submitting that
            # row's stored id still fires the same authored feedback.
            displayed_ids = [cid for cid, _label in displayed_t]
            assert distractor_id in displayed_ids
            row = displayed_ids.index(distractor_id)
            selected_from_row = displayed_t[row][0]
            assert selected_from_row == distractor_id
            from_row = score_practice_response(item, selected_from_row)
            assert from_row.correct is False
            assert from_row.common_mistake == expected_feedback
            assert (
                from_row.selected_misconception_tag
                == scored_wrong.selected_misconception_tag
            )

            parts = _practice_feedback_parts(
                outcome=scored_wrong.feedback_outcome,
                explanation=scored_wrong.explanation,
                common_mistake=scored_wrong.common_mistake,
                submitted_response=distractor_id,
                response_type="mcq",
                scored_correct=False,
                practice_choices=displayed_t,
            )
            assert parts["what_to_understand"] == expected_feedback
            assert distractor_label in parts["what_happened"]


def test_progression_readiness_depends_only_on_real_choice_id() -> None:
    """PR evaluate() is unchanged across every display permutation of the MCQ."""
    contract = CS1_C_T01_LO01
    item = _scoreable("3.1.1-method-of-moments-cs1010", "cs1010-3.1.1-ar-01")
    pairs = tuple((choice_parts(c)[0], choice_parts(c)[1]) for c in item.choices)
    correct_id = item.answer_key.correct_choice_id
    distractor_id = "d"
    occurred = datetime(2026, 9, 15, 12, 0, 0, tzinfo=UTC)

    def _row(
        *, item_id: str, scored_correct: bool, tag: str = "", rt: str
    ) -> AssessmentEvidenceRecord:
        return AssessmentEvidenceRecord(
            evidence_id=str(uuid4()),
            student_id="s-display-order",
            objective_id=contract.objective_id,
            item_id=item_id,
            package_id="test-package",
            session_id="test-session",
            response_type=rt,
            scored_correct=scored_correct,
            occurred_at=occurred,
            source="test",
            selected_misconception_tag=tag,
        )

    ready_results = []
    not_ready_results = []
    for displayed in permutations(pairs):
        displayed_ids = [cid for cid, _label in displayed]
        # Display order must not change which stored id is correct.
        assert displayed_ids.count(correct_id) == 1
        scored_ok = score_practice_response(item, correct_id)
        scored_wrong = score_practice_response(item, distractor_id)
        assert scored_ok.correct is True
        assert scored_wrong.correct is False

        numeric = _row(
            item_id="cs1010-3.1.1-cp-01",
            scored_correct=True,
            rt="numeric",
        )
        ready = evaluate(
            contract.objective_id,
            "s-display-order",
            contract,
            (
                _row(
                    item_id=item.item_id,
                    scored_correct=scored_ok.correct,
                    rt="mcq",
                ),
                numeric,
            ),
        )
        blocked = evaluate(
            contract.objective_id,
            "s-display-order",
            contract,
            (
                _row(
                    item_id=item.item_id,
                    scored_correct=scored_wrong.correct,
                    tag=scored_wrong.selected_misconception_tag,
                    rt="mcq",
                ),
                numeric,
            ),
        )
        ready_results.append((ready.readiness, ready.reason))
        not_ready_results.append((blocked.readiness, blocked.reason))

    assert len(set(ready_results)) == 1
    assert ready_results[0][0] is ProgressionReadiness.READY
    assert len(set(not_ready_results)) == 1
    assert not_ready_results[0] != ready_results[0]


def test_rendered_radios_keep_stored_ids_after_shuffle(app) -> None:
    stored = _mcq_pairs_from_stem("5.1.5-credible-intervals-cs1003")
    shuffled = shuffle_mcq_display_order(stored, rng=random.Random(7))
    assert shuffled != stored
    study = _base_page(
        content_stage="practice",
        stage_position_label="Practice",
        response_type="mcq",
        show_answer_input=True,
        primary_kind="answer_form",
        primary_label="Submit answer",
        practice_choices=shuffled,
    )
    html = _render(app, study, answer_form=_answer_form_stub())
    radio_ids = re.findall(
        r'type="radio"[^>]*value="([^"]+)"',
        html,
        flags=re.DOTALL,
    )
    assert radio_ids == [cid for cid, _label in shuffled]
    assert set(radio_ids) == {cid for cid, _label in stored}
    titles = re.findall(
        r'class="ds-exam-row__title">([^<]+)</span>',
        html,
    )
    assert titles == [label for _cid, label in shuffled]
