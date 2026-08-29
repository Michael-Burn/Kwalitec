"""Phase 0 — MCQ infrastructure for checkpoint Knowledge Checks.

Proves package JSON → loader → substance → scoring → UI branch wiring.
Batch 1 Section 3 packages (see _BATCH1_MCQ_PACKAGE_STEMS), Batch 2 Continuity
Front packages (see _BATCH2_MCQ_PACKAGE_STEMS), Batch 3 Memory/Publication
Front packages (see _BATCH3_MCQ_PACKAGE_STEMS), and Batch 4 Delta CS1-003
packages (see _BATCH4_MCQ_PACKAGE_STEMS) are live MCQ content; all other
live inventory packages remain short_structured until later batches.
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


# Batch 1 MCQ content conversion (Section 3 / checkpoint Batch A file set).
# Inventory stems under educational_packages/cs1/ - keep in sync with
# scripts/_mcq_batch1_section3_payload.py CONVERSIONS keys.
_BATCH1_MCQ_PACKAGE_STEMS = frozenset(
    {
        "3.1.1-method-of-moments-cs1010",
        "3.1.2-maximum-likelihood-cs1010",
        "3.1.3-efficiency-bias-consistency-mse-cs1010",
        "3.1.4-comparison-mse-cs1010",
        "3.1.5-asymptotic-mle-cs1010",
        "3.1.6-bootstrap-estimator-cs1010",
        "3.2.1-confidence-interval-parameter-cs1011",
        "3.2.2-prediction-interval-cs1011",
        "3.2.3-ci-given-sampling-distribution-cs1011",
        "3.2.4-ci-normal-mean-variance-cs1011",
        "3.2.5-ci-binomial-poisson-cs1011",
        "3.2.6-ci-two-sample-cs1011",
        "3.2.7-ci-paired-means-cs1011",
        "3.2.8-bootstrap-confidence-interval-cs1011",
        "3.3.1-hypothesis-concepts-cs1012",
        "3.3.2-basic-tests-cs1012",
        "3.3.3-permutation-tests-cs1012",
        "3.3.4-chi-square-gof-cs1012",
        "3.3.5-contingency-independence-cs1012",
        "cp-3.1.1-estimators-cs1016",
        "cp-3.2.1-ci-sample-cs1016",
        "cp-3.3.1-hypothesis-testing-cs1016",
    }
)

# Batch 2 MCQ content conversion (Continuity Front / checkpoint Batch B file set).
# Keep in sync with scripts/_mcq_batch2_continuity_front_payload.py CONVERSIONS keys.
_BATCH2_MCQ_PACKAGE_STEMS = frozenset(
    {
        "4.1.1-response-explanatory-cs1013",
        "4.1.2-simple-multiple-cs1013",
        "4.1.3-least-squares-cs1013",
        "4.1.4-software-fit-cs1013",
        "4.1.5-variable-selection-cs1013",
        "4.2.1-exponential-family-cs1014",
        "4.2.2-mean-variance-cs1014",
        "4.2.3-link-canonical-cs1014",
        "4.2.4-factors-interactions-cs1014",
        "4.2.5-linear-predictor-cs1014",
        "4.2.6-deviance-estimation-cs1014",
        "4.2.7-model-choice-cs1014",
        "4.2.8-residuals-cs1014",
        "4.2.9-goodness-tests-cs1014",
        "4.2.10-fit-interpret-cs1014",
        "5.1.1-bayes-theorem-cs1015",
        "5.1.2-prior-posterior-cs1015",
        "5.1.3-posterior-simple-cs1015",
        "5.1.4-loss-estimators-cs1015",
        "5.1.5-credible-intervals-cs1015",
        "5.1.6-credibility-premium-cs1015",
        "5.1.7-bayesian-credibility-cs1015",
        "5.1.8-empirical-bayes-cs1015",
        "5.1.9-bayes-vs-eb-cs1015",
    }
)

# Batch 3 MCQ content conversion (Memory Front remainder + Publication Front).
# Keep in sync with scripts/_mcq_batch3_memory_publication_payload.py CONVERSIONS keys.
_BATCH3_MCQ_PACKAGE_STEMS = frozenset(
    {
        "cp-2.1.3-prob-quantiles-cs1016",
        "cp-2.2.1-marginal-conditional-cs1016",
        "cp-2.5.1-clt-cs1016",
        "cp-2.6.1-random-samples-cs1016",
        "cp-4.1.1-linear-regression-cs1016",
        "cp-5.1.1-bayes-theorem-cs1016",
        "cr-1.1.1-aims-analysis-cs1017",
        "cr-1.1.2-stages-tools-cs1017",
        "cr-1.1.3-data-sources-cs1017",
        "cr-1.1.4-reproducible-cs1017",
        "cr-1.2.1-eda-summaries-cs1017",
        "cr-1.2.2-correlation-cs1017",
        "cr-1.2.3-pca-cs1017",
        "cr-2.1.1-discrete-cs1017",
        "cr-2.1.2-continuous-cs1017",
    }
)

# Batch 4 MCQ content conversion (Campaign Delta CS1-003 / checkpoint Batch D file set).
# Keep in sync with scripts/_mcq_batch4_delta_payload.py CONVERSIONS keys.
# Excludes 4.2.3, 4.2.5, 5.1.1, 5.1.5 (Batch 6 / STRONG untouched).
_BATCH4_MCQ_PACKAGE_STEMS = frozenset(
    {
        "4.1.1-response-explanatory-cs1003",
        "4.1.2-simple-multiple-cs1003",
        "4.1.3-least-squares-cs1003",
        "4.1.4-software-inference-cs1003",
        "4.1.5-variable-selection-cs1003",
        "4.2.1-exponential-family-cs1003",
        "4.2.2-mean-variance-cs1003",
        "4.2.4-factors-interactions-cs1003",
        "4.2.6-deviance-estimation-cs1003",
        "4.2.7-model-choice-cs1003",
        "4.2.8-residuals-cs1003",
        "4.2.9-goodness-tests-cs1003",
        "5.1.2-prior-posterior-cs1003",
        "5.1.3-posterior-simple-cs1003",
        "5.1.4-loss-estimators-cs1003",
        "5.1.6-credibility-premium-cs1003",
        "5.1.7-bayesian-credibility-cs1003",
        "5.1.8-empirical-bayes-cs1003",
    }
)

# Batch 5 MCQ content conversion (checkpoint Batch E file set).
# Keep in sync with scripts/_mcq_batch5_batch_e_payload.py CONVERSIONS keys.
# Includes WEAK Delta 4.2.10 and 5.1.9; excludes STRONG Batch 6 (4.2.3, 4.2.5, 5.1.1, 5.1.5).
_BATCH5_MCQ_PACKAGE_STEMS = frozenset(
    {
        "2.1.6-software-generation-cs1004",
        "2.2.1-marginal-conditional-cs1005",
        "2.2.3-cov-corr-expectation-cs1005",
        "2.2.4-linear-combinations-cs1005",
        "2.3.1-conditional-expectation-cs1006",
        "2.3.2-mean-variance-conditioning-cs1006",
        "2.4.1-mgf-cgf-cs1007",
        "2.4.2-moment-via-gf-cs1007",
        "2.5.1-clt-cs1008",
        "2.5.2-simulated-sample-normal-cs1008",
        "2.6.1-random-samples-cs1009",
        "2.6.3-mean-var-sample-cs1009",
        "2.6.4-normal-sample-mean-var-cs1009",
        "2.6.5-t-statistic-cs1009",
        "2.6.6-f-distribution-cs1009",
        "4.2.10-fit-interpret-cs1003",
        "5.1.9-bayes-vs-eb-cs1003",
    }
)

_MCQ_CONVERTED_STEMS = (
    _BATCH1_MCQ_PACKAGE_STEMS
    | _BATCH2_MCQ_PACKAGE_STEMS
    | _BATCH3_MCQ_PACKAGE_STEMS
    | _BATCH4_MCQ_PACKAGE_STEMS
    | _BATCH5_MCQ_PACKAGE_STEMS
)


def test_live_packages_outside_mcq_batches_remain_short_structured() -> None:
    """Live inventory outside Batch 1–5 MCQ conversion stays short_structured."""
    reset_educational_package_cache()
    packs = EducationalPackageLoader(root=LIVE_PACKAGE_ROOT).all_approved()
    assert packs, "expected live educational packages"
    batch1_seen = 0
    batch2_seen = 0
    batch3_seen = 0
    batch4_seen = 0
    batch5_seen = 0
    for pack in packs:
        assert pack.package_id != "CS1-MCQ-PHASE0-REF"
        stem = Path(pack.source_path).stem if pack.source_path else ""
        is_batch1 = stem in _BATCH1_MCQ_PACKAGE_STEMS
        is_batch2 = stem in _BATCH2_MCQ_PACKAGE_STEMS
        is_batch3 = stem in _BATCH3_MCQ_PACKAGE_STEMS
        is_batch4 = stem in _BATCH4_MCQ_PACKAGE_STEMS
        is_batch5 = stem in _BATCH5_MCQ_PACKAGE_STEMS
        for check in pack.knowledge_checks:
            if (
                (is_batch1 or is_batch2 or is_batch3 or is_batch4 or is_batch5)
                and check.kind in {"active_recall", "checkpoint"}
            ):
                if is_batch1:
                    batch1_seen += 1
                elif is_batch2:
                    batch2_seen += 1
                elif is_batch3:
                    batch3_seen += 1
                elif is_batch4:
                    batch4_seen += 1
                else:
                    batch5_seen += 1
                assert check.response_type == "mcq"
                assert len(check.choices) == 4
                assert check.correct_choice_id in {c.id for c in check.choices}
                continue
            assert check.response_type == "short_structured"
            assert check.choices == ()
            assert check.correct_choice_id == ""
            assert check.accepted_keywords  # existing keyword scoring still present
    assert batch1_seen == 44  # 22 packages × AR + CP
    assert batch2_seen == 48  # 24 packages × AR + CP
    assert batch3_seen == 30  # 15 packages × AR + CP
    assert batch4_seen == 36  # 18 packages × AR + CP
    assert batch5_seen == 34  # 17 packages × AR + CP

    # Spot-check a live package still outside Batches 1–5 (topic 1.1).
    live = find_educational_package(topic_code="1.1", subject_id="CS1")
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
