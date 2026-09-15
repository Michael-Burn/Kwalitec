"""Load, score, and coverage checks for CS1 topic 4.2 retry items.

cs1003-4.2.1-ar-02 evaluates Bernoulli natural parameter and Normal-in-family.
cs1003-4.2.2-ar-02 evaluates binomial and gamma mean/variance/V(mu) (criterion 3).
cs1003-4.2.3-ar-02 evaluates canonical logit and Poisson log-link inversion.
cs1003-4.2.4-ar-02 evaluates factor and interaction linear predictor values.
cs1003-4.2.6-ar-02 evaluates Poisson deviance contribution and scaled deviance.
cs1003-4.2.7-ar-02 evaluates nested deviance difference model choice.
cs1003-4.2.9-ar-02 evaluates Pearson chi-square GOF versus LRT contrast.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    reset_educational_package_cache,
)
from app.application.educational_packages.substance import substance_from_package
from app.application.learning_session.educational_flow import EducationalStage
from app.application.learning_session.scoreable_practice import score_practice_response

LIVE_ROOT = Path("app/curriculum/data/educational_packages")

_SPECS = (
    {
        "stem": "4.2.1-exponential-family-cs1003",
        "item_id": "cs1003-4.2.1-ar-02",
        "objective_id": "CS1-D-T02-LO01",
        "tags": {
            "b": "theta_equals_p",
            "c": "theta_equals_ln_p",
            "d": "software_skips_natural_parameter",
        },
    },
    {
        "stem": "4.2.2-mean-variance-cs1003",
        "item_id": "cs1003-4.2.2-ar-02",
        "objective_id": "CS1-D-T02-LO02",
        "tags": {
            "b": "poisson_variance_copied",
            "c": "link_finishes_mean_variance",
            "d": "gamma_as_normal_vmu",
        },
    },
    {
        "stem": "4.2.3-link-canonical-cs1003",
        "item_id": "cs1003-4.2.3-ar-02",
        "objective_id": "CS1-D-T02-LO03",
        "tags": {
            "b": "identity_always_canonical",
            "c": "logit_for_poisson",
            "d": "software_default_canonical",
        },
    },
    {
        "stem": "4.2.4-factors-interactions-cs1003",
        "item_id": "cs1003-4.2.4-ar-02",
        "objective_id": "CS1-D-T02-LO04",
        "tags": {
            "b": "interaction_when_either",
            "c": "factors_forbidden_in_glm",
            "d": "eta_as_mean",
        },
    },
    {
        "stem": "4.2.6-deviance-estimation-cs1003",
        "item_id": "cs1003-4.2.6-ar-02",
        "objective_id": "CS1-D-T02-LO06",
        "tags": {
            "b": "pearson_as_deviance_and_pchop",
            "c": "omit_factor_two",
            "d": "scaled_deviance_normal_only",
        },
    },
    {
        "stem": "4.2.7-model-choice-cs1003",
        "item_id": "cs1003-4.2.7-ar-02",
        "objective_id": "CS1-D-T02-LO07",
        "tags": {
            "b": "compare_full_deviance_alone",
            "c": "reversed_delta_d",
            "d": "p_only_model_choice",
        },
    },
    {
        "stem": "4.2.9-goodness-tests-cs1003",
        "item_id": "cs1003-4.2.9-ar-02",
        "objective_id": "CS1-D-T02-LO09",
        "tags": {
            "b": "abs_dev_and_lrt_same",
            "c": "coefficients_as_acceptability",
            "d": "nonsig_proves_all_fit",
        },
    },
)

_TWIN_STEMS = (
    "4.2.1-exponential-family-cs1014",
    "4.2.2-mean-variance-cs1014",
    "4.2.3-link-canonical-cs1014",
    "4.2.4-factors-interactions-cs1014",
    "4.2.6-deviance-estimation-cs1014",
    "4.2.7-model-choice-cs1014",
    "4.2.9-goodness-tests-cs1014",
)

_LO02_CRITERION3_REQUIRED = (
    "binomial",
    "gamma",
    "4.8",
    "32",
)

_LO02_ABSENT_FROM_PRIOR = (
    "binomial",
    "gamma",
)


def setup_function() -> None:
    reset_educational_package_cache()


def _pack(stem: str):
    loader = EducationalPackageLoader(root=LIVE_ROOT)
    packs = [
        p
        for p in loader.all_approved()
        if p.source_path and Path(p.source_path).stem == stem
    ]
    assert packs, f"missing live package {stem}"
    return packs[0]


def _scoreable(stem: str, item_id: str):
    pack = _pack(stem)
    substance = substance_from_package(
        pack,
        curriculum_identity=f"CS1:{pack.package_id}",
        topic_id=pack.topic_code,
    )
    for activity in substance.activities:
        if activity.stage is not EducationalStage.PRACTICE:
            continue
        assert activity.scoreable is not None
        if activity.scoreable.item_id == item_id:
            return activity.scoreable
    raise AssertionError(f"missing practice item {item_id} in {stem}")


def test_topic42_retry_items_load_with_correct_objective_and_tags() -> None:
    for spec in _SPECS:
        pack = _pack(spec["stem"])
        check = next(
            (c for c in pack.knowledge_checks if c.item_id == spec["item_id"]),
            None,
        )
        assert check is not None, f"{spec['item_id']} did not load"
        assert check.response_type == "mcq"
        assert (check.objective_id or "").strip() == spec["objective_id"]
        assert check.correct_choice_id == "a"
        assert [c.id for c in check.choices] == ["a", "b", "c", "d"]
        assert check.choices[0].misconception_tag == ""
        for choice_id, tag in spec["tags"].items():
            match = next(c for c in check.choices if c.id == choice_id)
            assert match.misconception_tag == tag


def test_topic42_retry_items_score_correct_and_distractors() -> None:
    for spec in _SPECS:
        item = _scoreable(spec["stem"], spec["item_id"])
        assert score_practice_response(item, "a").correct is True
        for cid in spec["tags"]:
            scored = score_practice_response(item, cid)
            assert scored.correct is False


def test_topic42_retry_items_absent_from_twin_packages() -> None:
    loader = EducationalPackageLoader(root=LIVE_ROOT)
    retry_ids = {spec["item_id"] for spec in _SPECS}
    for stem in _TWIN_STEMS:
        packs = [
            p
            for p in loader.all_approved()
            if p.source_path and Path(p.source_path).stem == stem
        ]
        assert packs, f"missing twin package {stem}"
        twin_ids = {c.item_id for c in packs[0].knowledge_checks}
        assert retry_ids.isdisjoint(twin_ids)


def test_topic42_retry_items_present_only_in_named_live_packages() -> None:
    root = Path("app/curriculum/data/educational_packages/cs1")
    expected = {spec["item_id"]: spec["stem"] for spec in _SPECS}
    found: dict[str, str] = {}
    for path in root.glob("*.json"):
        data = json.loads(path.read_text())
        for check in data.get("knowledge_checks") or []:
            item_id = check.get("item_id")
            if item_id in expected:
                found[item_id] = path.stem
    assert found == expected


def test_lo02_ar02_closes_binomial_gamma_criterion3_gap() -> None:
    """Prior LO02 scored text lacks binomial/gamma evaluation; ar-02 supplies it."""
    pack = _pack("4.2.2-mean-variance-cs1003")
    by_id = {c.item_id: c for c in pack.knowledge_checks}
    assert "cs1003-4.2.2-ar-01" in by_id
    assert "cs1003-4.2.2-cp-01" in by_id
    assert "cs1003-4.2.2-ar-02" in by_id

    prior_blob = json.dumps(
        [
            {
                "prompt": by_id["cs1003-4.2.2-ar-01"].prompt,
                "choices": [c.label for c in by_id["cs1003-4.2.2-ar-01"].choices],
                "explanation": by_id["cs1003-4.2.2-ar-01"].explanation,
            },
            {
                "prompt": by_id["cs1003-4.2.2-cp-01"].prompt,
                "choices": [c.label for c in by_id["cs1003-4.2.2-cp-01"].choices],
                "explanation": by_id["cs1003-4.2.2-cp-01"].explanation,
            },
        ]
    ).lower()
    assert "poisson" in prior_blob
    assert "normal" in prior_blob
    for phrase in _LO02_ABSENT_FROM_PRIOR:
        assert phrase not in prior_blob, (
            f"prior scored LO02 items unexpectedly already cover {phrase!r}"
        )

    ar02 = by_id["cs1003-4.2.2-ar-02"]
    ar02_blob = json.dumps(
        {
            "prompt": ar02.prompt,
            "choices": [c.label for c in ar02.choices],
            "explanation": ar02.explanation,
        }
    ).lower()
    for phrase in _LO02_CRITERION3_REQUIRED:
        assert phrase in ar02_blob, f"ar-02 must score {phrase!r}"

    correct = next(c for c in ar02.choices if c.id == "a").label.lower()
    assert "binomial" in correct
    assert "gamma" in correct
    assert "4.8" in correct
    assert "32" in correct
    assert "poisson" in correct  # refuses copying Poisson V(mu) onto Gamma
