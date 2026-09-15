"""Load, score, and coverage checks for CS1 topic 5.1 retry items.

cs1003-5.1.2-ar-02 evaluates Beta-Binomial conjugate update and means.
cs1003-5.1.3-ar-02 evaluates Gamma-Poisson posterior and mean.
cs1003-5.1.5-ar-02 evaluates central Normal credible interval endpoints.
cs1003-5.1.9-ar-02 evaluates Bayes versus Empirical Bayes premiums.
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
        "stem": "5.1.2-prior-posterior-cs1003",
        "item_id": "cs1003-5.1.2-ar-02",
        "objective_id": "CS1-E-T01-LO02",
        "tags": {
            "b": "conjugate_finishes_posterior",
            "c": "swapped_conjugate_counts",
            "d": "prior_equals_posterior",
        },
    },
    {
        "stem": "5.1.3-posterior-simple-cs1003",
        "item_id": "cs1003-5.1.3-ar-02",
        "objective_id": "CS1-E-T01-LO03",
        "tags": {
            "b": "swapped_gamma_update",
            "c": "prior_unchanged",
            "d": "posterior_finishes_loss_estimator",
        },
    },
    {
        "stem": "5.1.5-credible-intervals-cs1003",
        "item_id": "cs1003-5.1.5-ar-02",
        "objective_id": "CS1-E-T01-LO05",
        "tags": {
            "b": "one_sd_rule",
            "c": "frequentist_slogan",
            "d": "degenerate_interval",
        },
    },
    {
        "stem": "5.1.9-bayes-vs-eb-cs1003",
        "item_id": "cs1003-5.1.9-ar-02",
        "objective_id": "CS1-E-T01-LO09",
        "tags": {
            "b": "experience_only_premium",
            "c": "forced_agreement_rounding",
            "d": "assumptions_reversed",
        },
    },
)

_TWIN_STEMS = (
    "5.1.2-prior-posterior-cs1015",
    "5.1.3-posterior-simple-cs1015",
    "5.1.5-credible-intervals-cs1015",
    "5.1.9-bayes-vs-eb-cs1015",
)


def _package_path(stem: str) -> Path:
    return LIVE_ROOT / "cs1" / f"{stem}.json"


def test_topic_5_1_retry_items_load_score_and_stay_trust_only() -> None:
    reset_educational_package_cache()
    loader = EducationalPackageLoader(root=LIVE_ROOT)

    for spec in _SPECS:
        path = _package_path(spec["stem"])
        raw = json.loads(path.read_text())
        by_id = {check["item_id"]: check for check in raw["knowledge_checks"]}
        assert spec["item_id"] in by_id
        item = by_id[spec["item_id"]]
        assert item["objective_id"] == spec["objective_id"]
        assert item["response_type"] == "mcq"
        assert item["correct_choice_id"] == "a"
        for choice_id, tag in spec["tags"].items():
            choice = next(c for c in item["choices"] if c["id"] == choice_id)
            assert choice["misconception_tag"] == tag

        pack = next(
            p
            for p in loader.all_approved()
            if Path(p.source_path).name == path.name
        )
        substance = substance_from_package(
            pack, curriculum_identity="CS1:topic51", topic_id=pack.topic_code
        )
        practice = [
            a for a in substance.activities if a.stage is EducationalStage.PRACTICE
        ]
        scoreable = next(
            a.scoreable
            for a in practice
            if a.scoreable and a.scoreable.item_id == spec["item_id"]
        )
        correct = score_practice_response(scoreable, "a")
        assert correct.correct is True
        for wrong in ("b", "c", "d"):
            result = score_practice_response(scoreable, wrong)
            assert result.correct is False

    for twin_stem in _TWIN_STEMS:
        twin_path = _package_path(twin_stem)
        twin_raw = json.loads(twin_path.read_text())
        twin_ids = {check["item_id"] for check in twin_raw["knowledge_checks"]}
        assert not any(item_id.endswith("-ar-02") for item_id in twin_ids)
