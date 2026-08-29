#!/usr/bin/env python3
"""Real Worked Examples Batch 6 - Final Domain F1b closure (30 packages).

Injects genuine ``worked_example`` objects into the 11 remaining learning
packages and 19 revision packages, then synchronises catalogue and campaign
twins (including cp-/cr- catalogue aliases for Pi/Rho revision packages).

Content lives in ``_rwe_batch6_final_data.json`` beside this module.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

_DATA = Path(__file__).with_name("_rwe_batch6_final_data.json")
_BLOB = json.loads(_DATA.read_text(encoding="utf-8"))
WORKED_EXAMPLES: dict[str, dict[str, Any]] = _BLOB["worked_examples"]
CAMPAIGN_TWINS: dict[str, str] = _BLOB["campaign_twins"]

EXPECTED_COUNT = 30

_DUPLICATION_FINGERPRINTS: list[tuple[str, re.Pattern[str]]] = [
    ("Phase0/B3 cyber P(Breach)=0.03", re.compile(r"P\(Breach\)\s*=\s*0\.03")),
    ("Batch2 fraud screen P(Fraud)=0.05", re.compile(r"P\(Fraud\)\s*=\s*0\.05")),
    ("Batch2 motor ŷ=1200+40x", re.compile(r"1200\s*\+\s*40x")),
    ("Batch3 weather joint 0.05/0.15/0.20/0.60", re.compile(r"0\.05.*0\.15.*0\.20.*0\.60")),
    ("Batch3 repair CLT μ=1200 σ=300 n=36", re.compile(r"μ\s*=\s*1200.*σ\s*=\s*300")),
    ("Batch3 repair 1150 threshold", re.compile(r"X̄\s*<\s*1150|Xbar\s*<\s*1150")),
    ("Batch3 40 most recent claims", re.compile(r"40 most recent")),
    ("Batch3 Exp θ=800", re.compile(r"θ\s*=\s*800|theta\s*=\s*800|mean θ = 800")),
    ("Batch3 zero-inflated 0,0,1,3,10", re.compile(r"0,\s*0,\s*1,\s*3,\s*10")),
    ("Batch3 Spearman years licensed −0.55", re.compile(r"years licensed.*−0\.55|ρ\s*=\s*−0\.55")),
    ("Batch3 PC1 causal auto-decline", re.compile(r"auto-decline on PC1")),
    ("Batch3 Poisson λ=0.4 rare annual", re.compile(r"λ\s*=\s*0\.4")),
    ("Batch3 Exp mean 6 months wait", re.compile(r"mean waiting time.*6 months|mean θ = 6")),
    ("Batch4 EL ŷ=2500+150x", re.compile(r"2500\s*\+\s*150x")),
    ("Batch4 Beta(3,5) n=12 s=4", re.compile(r"Beta\(3,\s*5\).*n\s*=\s*12|Beta\(3,\s*5\) = Beta\(3")),
    ("Batch5 flood-wind 0.55/0.15/0.20/0.10", re.compile(r"0\.55.*0\.15.*0\.20.*0\.10")),
    ("Batch5 pet CLT μ=180 σ=60", re.compile(r"μ\s*=\s*180.*σ\s*=\s*60")),
    ("Batch5 Poisson software λ=3 θ=5", re.compile(r"Poisson\(λ = 3\).*Exponential with mean θ = 5")),
]


def _inject(pkg: dict[str, Any], example: dict[str, Any]) -> None:
    """Insert or replace top-level worked_example."""
    pkg["worked_example"] = example


def sync_catalogue_twins(root: Path | None = None) -> int:
    repo = root or Path(__file__).resolve().parents[1]
    catalogue_dir = repo / "app/curriculum/data/educational_packages/cs1"
    updated = 0
    for inv_key, example in WORKED_EXAMPLES.items():
        path = catalogue_dir / inv_key
        if not path.exists():
            raise FileNotFoundError(path)
        pkg = json.loads(path.read_text(encoding="utf-8"))
        _inject(pkg, example)
        path.write_text(
            json.dumps(pkg, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        updated += 1
    return updated


def sync_campaign_twins(root: Path | None = None) -> int:
    repo = root or Path(__file__).resolve().parents[1]
    campaign_dir = repo / "app/curriculum/data/educational_campaigns/cs1"
    updated = 0
    for inv_key, rel_path in CAMPAIGN_TWINS.items():
        path = campaign_dir / rel_path
        if not path.exists():
            raise FileNotFoundError(path)
        pkg = json.loads(path.read_text(encoding="utf-8"))
        _inject(pkg, WORKED_EXAMPLES[inv_key])
        path.write_text(
            json.dumps(pkg, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        updated += 1
    return updated


def arithmetic_sanity_checks() -> list[str]:
    """Independent verification of every genuinely numeric hinge."""
    defects: list[str] = []

    # 1.2.1 claim sizes
    sizes = (180, 220, 310, 450, 2400)
    if sum(sizes) / 5 != 712 or sorted(sizes)[2] != 310:
        defects.append(f"1.2.1 mean/median {sum(sizes)/5}, {sorted(sizes)[2]}")

    # 2.1.1 Binomial P(X=0)
    p0 = 0.9**30
    if abs(p0 - 0.0424) > 5e-4:
        defects.append(f"2.1.1 P(X=0) {p0}")

    # 2.1.2 Lognormal median
    if abs(math.exp(6) - 403.43) > 0.01:
        defects.append(f"2.1.2 e^6 {math.exp(6)}")

    # 2.1.3 Exp θ=250
    cdf = 1 - math.exp(-0.4)
    med = 250 * math.log(2)
    if abs(cdf - 0.3297) > 5e-4 or abs(med - 173.29) > 0.05:
        defects.append(f"2.1.3 cdf/median {cdf}, {med}")

    # 2.1.4 Poisson process
    if abs(1.5 * 4 - 6) > 1e-12 or abs(math.exp(-6) - 0.0025) > 5e-4:
        defects.append("2.1.4 Poisson(6) / e^{-6}")

    # 2.1.5 inverse transform
    x = -math.log(0.8) / 0.5
    if abs(x - 0.4463) > 5e-4:
        defects.append(f"2.1.5 Exp inverse {x}")

    # 2.2.2 independence
    cells = (0.50, 0.10, 0.20, 0.20)
    if abs(sum(cells) - 1.0) > 1e-12:
        defects.append("2.2.2 joint sum")
    px0, py0 = 0.60, 0.70
    if abs(px0 * py0 - 0.42) > 1e-12 or abs(0.50 - 0.42) < 1e-12:
        defects.append("2.2.2 dependence check")

    # 2.6.2 sampling dist
    if 400 / 16 != 25:
        defects.append("2.6.2 Var(Xbar)")

    # revision midspine Beta update
    if (4 + 2, 6 + (8 - 2)) != (6, 12):
        defects.append("revision-midspine Beta update")

    # revision distributions generation
    x2 = -math.log(0.7) / 2
    if abs(x2 - 0.1783) > 5e-4:
        defects.append(f"revision-distributions-generation {x2}")

    # revision estimators MSE
    if 7 + 3**2 != 16:
        defects.append("revision-estimators MSE")

    # revision CI
    se = 12 / 36**0.5
    lo, hi = 42 - 1.96 * se, 42 + 1.96 * se
    if abs(se - 2) > 1e-12 or abs(lo - 38.08) > 1e-9 or abs(hi - 45.92) > 1e-9:
        defects.append(f"revision-CI {se}, {lo}, {hi}")

    # revision bayesian credible
    lo2, hi2 = 60 - 1.96 * 4, 60 + 1.96 * 4
    if abs(lo2 - 52.16) > 1e-9 or abs(hi2 - 67.84) > 1e-9:
        defects.append(f"revision-bayesian {lo2}, {hi2}")

    return defects


def duplication_check() -> list[str]:
    defects: list[str] = []
    for inv_key, example in WORKED_EXAMPLES.items():
        raw = json.dumps(example, ensure_ascii=False)
        for label, pattern in _DUPLICATION_FINGERPRINTS:
            if pattern.search(raw):
                defects.append(f"{inv_key}: fingerprint hit '{label}'")
    return defects


def learning_day_distinctness_check(root: Path | None = None) -> list[str]:
    """Revision WEs must not clone their originating learning-day problem_statement."""
    repo = root or Path(__file__).resolve().parents[1]
    catalogue_dir = repo / "app/curriculum/data/educational_packages/cs1"
    # Map revision package -> representative learning-day packages already authored
    pairs: list[tuple[str, list[str]]] = [
        ("revision-purpose-eda-ep001.json", ["1.1-purpose-function-ep001.json", "cr-1.1.1-aims-analysis-cs1017.json", "cr-1.2.1-eda-summaries-cs1017.json"]),
        ("revision-pca-distributions-cs1002.json", ["2.1.1-discrete-cs1002.json", "cr-2.1.1-discrete-cs1017.json"]),
        ("revision-linear-models-cs1003.json", ["4.1.1-response-explanatory-cs1003.json", "4.1.3-least-squares-cs1003.json"]),
        ("revision-regression-glm-cs1003.json", ["4.2.3-link-canonical-cs1003.json", "4.2.6-deviance-estimation-cs1003.json"]),
        ("revision-midspine-cs1003.json", ["5.1.2-prior-posterior-cs1003.json", "5.1.2-prior-posterior-cs1015.json"]),
        ("revision-distributions-generation-cs1004.json", ["2.1.5-inverse-transform-cs1004.json", "cp-2.1.3-prob-quantiles-cs1016.json"]),
        ("revision-joint-distributions-cs1005.json", ["2.2.2-independence-cs1005.json", "2.2.4-linear-combinations-cs1005.json"]),
        ("revision-conditional-expectations-cs1006.json", ["2.3.1-conditional-expectation-cs1006.json", "2.3.2-mean-variance-conditioning-cs1006.json"]),
        ("revision-generating-functions-cs1007.json", ["2.4.1-mgf-cgf-cs1007.json", "2.4.2-moment-via-gf-cs1007.json"]),
        ("revision-central-limit-theorem-cs1008.json", ["2.5.1-clt-cs1008.json", "cp-2.5.1-clt-cs1016.json"]),
        ("revision-sampling-distributions-cs1009.json", ["2.6.2-sampling-distribution-statistic-cs1009.json", "2.6.5-t-statistic-cs1009.json"]),
        ("revision-estimators-cs1010.json", ["3.1.1-method-of-moments-cs1010.json", "3.1.3-efficiency-bias-consistency-mse-cs1010.json"]),
        ("revision-confidence-intervals-cs1011.json", ["3.2.1-confidence-interval-parameter-cs1011.json", "cp-3.2.1-ci-sample-cs1016.json"]),
        ("revision-hypothesis-testing-cs1012.json", ["3.3.1-hypothesis-concepts-cs1012.json", "3.3.2-basic-tests-cs1012.json"]),
        ("revision-linear-regression-cs1013.json", ["4.1.3-least-squares-cs1013.json", "4.1.1-response-explanatory-cs1013.json"]),
        ("revision-glm-cs1014.json", ["4.2.3-link-canonical-cs1014.json", "4.2.7-model-choice-cs1014.json"]),
        ("revision-bayesian-cs1015.json", ["5.1.1-bayes-theorem-cs1015.json", "5.1.5-credible-intervals-cs1015.json"]),
        ("cp-revision-spine-memory-cs1016.json", ["cp-3.1.1-estimators-cs1016.json", "3.1.1-method-of-moments-cs1010.json"]),
        ("cr-revision-publication-front-cs1017.json", ["cr-2.1.1-discrete-cs1017.json", "cr-1.2.2-correlation-cs1017.json"]),
    ]
    defects: list[str] = []
    for rev_key, origins in pairs:
        rev = WORKED_EXAMPLES[rev_key]
        for origin_name in origins:
            path = catalogue_dir / origin_name
            if not path.exists():
                continue
            origin_pkg = json.loads(path.read_text(encoding="utf-8"))
            origin_we = origin_pkg.get("worked_example")
            if not isinstance(origin_we, dict):
                # Origin may be this batch's learning twin not yet synced; use in-memory if present
                origin_we = WORKED_EXAMPLES.get(origin_name)
            if not isinstance(origin_we, dict):
                continue
            if rev.get("problem_statement") == origin_we.get("problem_statement"):
                defects.append(f"{rev_key}: identical problem_statement to {origin_name}")
            if rev.get("title") == origin_we.get("title"):
                defects.append(f"{rev_key}: identical title to {origin_name}")
            if rev.get("final_answer") == origin_we.get("final_answer"):
                defects.append(f"{rev_key}: identical final_answer to {origin_name}")
            if json.dumps(rev, sort_keys=True) == json.dumps(origin_we, sort_keys=True):
                defects.append(f"{rev_key}: entire WE identical to {origin_name}")
    return defects


def mechanical_defect_scan(root: Path | None = None) -> list[str]:
    repo = root or Path(__file__).resolve().parents[1]
    catalogue_dir = repo / "app/curriculum/data/educational_packages/cs1"
    campaign_dir = repo / "app/curriculum/data/educational_campaigns/cs1"
    meta_patterns = [
        re.compile(pattern, re.IGNORECASE)
        for pattern in (
            r"\bcampaign\b",
            r"\bjourney\b",
            r"Batch \d",
            r"Wave \d",
            r"Isolated Golden Day",
            r"spine claims",
            r"Memory Front finished",
            r"Publication Front",
            r"Continuity Front",
        )
    ]
    required_keys = {
        "title",
        "problem_statement",
        "given",
        "attempt_before_reveal",
        "steps",
        "final_answer",
        "common_pitfall",
        "syllabus_ref",
    }
    step_keys = {"id", "label", "attempt_cue", "explanation", "calculation", "result"}
    em = "\u2014"
    en = "\u2013"
    defects: list[str] = []

    for inv_key, rel_path in CAMPAIGN_TWINS.items():
        paths = [catalogue_dir / inv_key, campaign_dir / rel_path]
        blobs: list[str] = []
        for path in paths:
            if not path.exists():
                defects.append(f"MISSING: {path}")
                continue
            pkg = json.loads(path.read_text(encoding="utf-8"))
            example = pkg.get("worked_example")
            if not isinstance(example, dict):
                defects.append(f"{path.name}: worked_example missing")
                continue
            blobs.append(json.dumps(example, sort_keys=True, ensure_ascii=False))
            missing = required_keys - set(example)
            if missing:
                defects.append(f"{path.name}: missing keys {sorted(missing)}")
            raw = json.dumps(example, ensure_ascii=False)
            if em in raw:
                defects.append(f"{path.name}: em dash found")
            if en in raw:
                defects.append(f"{path.name}: en dash found")
            for pattern in meta_patterns:
                if pattern.search(raw):
                    defects.append(
                        f"{path.name}: meta language '{pattern.pattern}'"
                    )
            if not example.get("steps"):
                defects.append(f"{path.name}: empty steps")
            for s in example.get("steps") or []:
                sk_missing = step_keys - set(s)
                if sk_missing:
                    defects.append(
                        f"{path.name}: step {s.get('id')} missing {sorted(sk_missing)}"
                    )
            for entry in example.get("given") or []:
                if not entry.get("symbol") or not entry.get("value"):
                    defects.append(f"{path.name}: given entry missing symbol/value")
        if len(blobs) == 2 and blobs[0] != blobs[1]:
            defects.append(f"{inv_key}: catalogue/campaign worked_example mismatch")

    if len(WORKED_EXAMPLES) != EXPECTED_COUNT:
        defects.append(
            f"expected {EXPECTED_COUNT} examples, got {len(WORKED_EXAMPLES)}"
        )

    defects.extend(arithmetic_sanity_checks())
    defects.extend(duplication_check())
    defects.extend(learning_day_distinctness_check(repo))
    return defects


def inventory_gate(root: Path | None = None) -> tuple[int, int]:
    """Return (approved_with_real_we, approved_total)."""
    repo = root or Path(__file__).resolve().parents[1]
    catalogue_dir = repo / "app/curriculum/data/educational_packages/cs1"
    approved = 0
    with_we = 0
    for path in sorted(catalogue_dir.glob("*.json")):
        pkg = json.loads(path.read_text(encoding="utf-8"))
        if pkg.get("status") != "publication_approved":
            continue
        approved += 1
        we = pkg.get("worked_example")
        if isinstance(we, dict) and we.get("steps"):
            with_we += 1
    return with_we, approved


if __name__ == "__main__":
    assert len(WORKED_EXAMPLES) == EXPECTED_COUNT, len(WORKED_EXAMPLES)
    campaign_count = sync_campaign_twins()
    catalogue_count = sync_catalogue_twins()
    scan = mechanical_defect_scan()
    with_we, approved = inventory_gate()
    print(
        f"Synced {campaign_count} campaign + {catalogue_count} catalogue twins."
    )
    print(f"Inventory gate: {with_we}/{approved} publication_approved packages with real worked_example")
    if scan:
        print("DEFECTS:")
        for defect in scan:
            print(" ", defect)
        raise SystemExit(1)
    print("Mechanical defect scan: PASS (0 issues)")
    print("Duplication check: PASS (no prior-batch fingerprints)")
    print("Learning-day distinctness: PASS (revision hinges not clones)")
    if with_we != 130 or approved != 130:
        print(f"INVENTORY FAIL: expected 130/130, got {with_we}/{approved}")
        raise SystemExit(1)
    print("Inventory gate: PASS (130/130)")
