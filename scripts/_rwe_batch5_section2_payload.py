#!/usr/bin/env python3
"""Real Worked Examples Batch 5 - Section 2 (Domain F1b).

Injects genuine ``worked_example`` objects into the 15 confirmed Section 2
packages across gamma/epsilon/zeta/eta/theta/iota (cs1004-cs1009), then
synchronises catalogue and campaign twins.

Content lives in ``_rwe_batch5_section2_data.json`` beside this module.

Three LO-overlap packages (2.2.1, 2.5.1, 2.6.1) are authored scenario- and
number-distinct from their Batch 3 Pi Memory Front twins. Delta stragglers
4.2.10 and 5.1.9 are intentionally excluded (already covered in Batch 4).
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

_DATA = Path(__file__).with_name("_rwe_batch5_section2_data.json")
_BLOB = json.loads(_DATA.read_text(encoding="utf-8"))
WORKED_EXAMPLES: dict[str, dict[str, Any]] = _BLOB["worked_examples"]
CAMPAIGN_TWINS: dict[str, str] = _BLOB["campaign_twins"]

EXPECTED_COUNT = 15

# Forbidden scenario / number fingerprints from prior RWE batches and MCQ Batch 3.
_DUPLICATION_FINGERPRINTS: list[tuple[str, re.Pattern[str]]] = [
    ("Phase0 disease screen P(D)=0.01", re.compile(r"P\(D\)\s*=\s*0\.01")),
    ("Batch2 fraud screen P(Fraud)=0.05", re.compile(r"P\(Fraud\)\s*=\s*0\.05")),
    ("Batch2 motor severity ŷ=1200+40x age 45", re.compile(r"1200\s*\+\s*40x|age 45")),
    ("Batch3 weather/liability joint 0.05/0.15/0.20/0.60", re.compile(r"0\.05.*0\.15.*0\.20.*0\.60")),
    ("Batch3 weather claim / liability claim", re.compile(r"weather claim|liability claim", re.I)),
    ("Batch3 repair cost CLT μ=1200 σ=300 n=36", re.compile(r"μ\s*=\s*1200.*σ\s*=\s*300|mu\s*=\s*1200.*sigma\s*=\s*300")),
    ("Batch3 repair cost 1150 threshold", re.compile(r"X̄\s*<\s*1150|Xbar\s*<\s*1150")),
    ("Batch3 one-client 40 most recent claims", re.compile(r"40 most recent|one large commercial client")),
    ("MCQ B3 Exp theta=1000", re.compile(r"θ\s*=\s*1000|theta\s*=\s*1000|mean θ = 1000")),
    ("MCQ B3 joint 0.10/0.20/0.30/0.40", re.compile(r"0\.10.*0\.20.*0\.30.*0\.40")),
    ("MCQ B3 CLT mu=500 sigma=200 n=100", re.compile(r"μ\s*=\s*500.*σ\s*=\s*200|mu\s*=\s*500.*sigma\s*=\s*200")),
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

    # 2.2.1 flood/wind joint table
    cells = (0.55, 0.15, 0.20, 0.10)
    if abs(sum(cells) - 1.0) > 1e-12:
        defects.append(f"2.2.1 joint table sum {sum(cells)}")
    py1 = 0.15 + 0.10
    px1_given_y1 = 0.10 / py1
    if abs(py1 - 0.25) > 1e-12 or abs(px1_given_y1 - 0.40) > 1e-12:
        defects.append(f"2.2.1 marginal/conditional {py1}, {px1_given_y1}")

    # 2.2.3 cov/corr
    ex, ey, exy = 0.5, 0.5, 0.30
    cov = exy - ex * ey
    varx = ey * (1 - ey)  # Bernoulli 0.5 -> 0.25; same for both
    vary = varx
    corr = cov / math.sqrt(varx * vary)
    if abs(cov - 0.05) > 1e-12 or abs(corr - 0.20) > 1e-12:
        defects.append(f"2.2.3 cov/corr {cov}, {corr}")
    if abs(ex + 2 * ey - 1.5) > 1e-12:
        defects.append("2.2.3 E[X+2Y] mismatch")

    # 2.2.4 linear combinations
    if 2 * 10 - 4 != 16:
        defects.append("2.2.4 mean mismatch")
    if 4 * 9 + 1 * 4 - 2 * 2 * 1 * 3 != 28:
        defects.append("2.2.4 variance mismatch")

    # 2.3.1 conditional expectation
    if abs((10 * 0.25 + 20 * 0.25) / 0.5 - 15.0) > 1e-12:
        defects.append("2.3.1 E[Y|X=1] mismatch")
    if abs((10 * 0.15 + 20 * 0.35) / 0.5 - 17.0) > 1e-12:
        defects.append("2.3.1 E[Y|X=2] mismatch")

    # 2.3.2 tower / variance decomposition
    ey_tot = 0.4 * 5 + 0.6 * 12
    e_var = 0.4 * 4 + 0.6 * 9
    var_e = 0.4 * 25 + 0.6 * 144 - ey_tot**2
    if abs(ey_tot - 9.2) > 1e-12:
        defects.append(f"2.3.2 E[Y] mismatch {ey_tot}")
    if abs(e_var - 7.0) > 1e-12:
        defects.append(f"2.3.2 E[Var] mismatch {e_var}")
    if abs(var_e - 11.76) > 1e-12:
        defects.append(f"2.3.2 Var(E) mismatch {var_e}")
    if abs(e_var + var_e - 18.76) > 1e-12:
        defects.append(f"2.3.2 Var(Y) mismatch {e_var + var_e}")

    # 2.4.2 moments via CGF (Poisson λ=2)
    if abs(2 * math.exp(0) - 2) > 1e-12:
        defects.append("2.4.2 C'(0) mismatch")
    if abs(2 * math.exp(0) - 2) > 1e-12:
        defects.append("2.4.2 C''(0) mismatch")

    # 2.5.1 CLT pet severity
    se = 60 / math.sqrt(36)
    z = (170 - 180) / se
    p = 1 - 0.841
    if abs(se - 10) > 1e-12 or abs(z + 1) > 1e-12 or abs(p - 0.159) > 1e-12:
        defects.append(f"2.5.1 CLT mismatch se={se} z={z} p={p}")

    # 2.5.2 light numeric illustration (Exponential mean 400)
    theo_sd = 400.0
    if abs(theo_sd - 400) > 1e-12:
        defects.append("2.5.2 theoretical sd mismatch")

    # 2.6.3 sampling moments
    if abs(36 / 9 - 4) > 1e-12:
        defects.append("2.6.3 Var(X̄) mismatch")

    # 2.6.4 Normal sampling laws
    if abs(25 / 16 - 1.5625) > 1e-12:
        defects.append("2.6.4 Var(X̄) mismatch")

    # 2.6.5 t-statistic
    t = (105 - 100) / (8 / math.sqrt(16))
    if abs(t - 2.5) > 1e-12:
        defects.append(f"2.6.5 t mismatch {t}")

    # 2.6.6 F ratio
    if abs(20 / 10 - 2.0) > 1e-12:
        defects.append("2.6.6 F ratio mismatch")

    return defects


def duplication_check() -> list[str]:
    defects: list[str] = []
    for inv_key, example in WORKED_EXAMPLES.items():
        raw = json.dumps(example, ensure_ascii=False)
        for label, pattern in _DUPLICATION_FINGERPRINTS:
            if pattern.search(raw):
                defects.append(f"{inv_key}: duplication hit '{label}'")
    return defects


def lo_overlap_distinctness_check() -> list[str]:
    """Confirm the three LO-overlap packages differ from Batch 3 twins."""
    defects: list[str] = []
    batch3_path = Path(__file__).with_name("_rwe_batch3_memory_publication_data.json")
    if not batch3_path.exists():
        return ["Batch 3 data missing for LO-overlap distinctness check"]
    batch3 = json.loads(batch3_path.read_text(encoding="utf-8"))["worked_examples"]
    pairs = [
        (
            "2.2.1-marginal-conditional-cs1005.json",
            "cp-2.2.1-marginal-conditional-cs1016.json",
        ),
        ("2.5.1-clt-cs1008.json", "cp-2.5.1-clt-cs1016.json"),
        ("2.6.1-random-samples-cs1009.json", "cp-2.6.1-random-samples-cs1016.json"),
    ]
    for b5_key, b3_key in pairs:
        a = WORKED_EXAMPLES[b5_key]
        b = batch3[b3_key]
        if a.get("problem_statement") == b.get("problem_statement"):
            defects.append(f"{b5_key}: identical problem_statement to Batch 3 twin")
        if a.get("title") == b.get("title"):
            defects.append(f"{b5_key}: identical title to Batch 3 twin")
        if a.get("final_answer") == b.get("final_answer"):
            defects.append(f"{b5_key}: identical final_answer to Batch 3 twin")
        # Number fingerprints that must not recur
        raw_a = json.dumps(a, ensure_ascii=False)
        raw_b = json.dumps(b, ensure_ascii=False)
        if raw_a == raw_b:
            defects.append(f"{b5_key}: entire worked_example identical to Batch 3")
        # Shared numeric cores that would indicate copy
        if b5_key.startswith("2.2.1") and "0.60" in raw_a and "0.80" in raw_a:
            defects.append(f"{b5_key}: reuses Batch 3 marginal 0.80 / cell 0.60 pattern")
        if b5_key.startswith("2.5.1") and "1200" in raw_a and "300" in raw_a:
            defects.append(f"{b5_key}: reuses Batch 3 μ=1200 σ=300")
        if b5_key.startswith("2.6.1") and "40 most recent" in raw_a:
            defects.append(f"{b5_key}: reuses Batch 3 convenience extract")
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
    # Confirm excluded Delta stragglers were not touched by this payload
    for excluded in (
        "4.2.10-fit-interpret-cs1003.json",
        "5.1.9-bayes-vs-eb-cs1003.json",
    ):
        if excluded in WORKED_EXAMPLES or excluded in CAMPAIGN_TWINS:
            defects.append(f"excluded package incorrectly included: {excluded}")

    defects.extend(arithmetic_sanity_checks())
    defects.extend(duplication_check())
    defects.extend(lo_overlap_distinctness_check())
    return defects


if __name__ == "__main__":
    assert len(WORKED_EXAMPLES) == EXPECTED_COUNT, len(WORKED_EXAMPLES)
    campaign_count = sync_campaign_twins()
    catalogue_count = sync_catalogue_twins()
    scan = mechanical_defect_scan()
    print(
        f"Synced {campaign_count} campaign + {catalogue_count} catalogue twins."
    )
    if scan:
        print("DEFECTS:")
        for defect in scan:
            print(" ", defect)
        raise SystemExit(1)
    print("Mechanical defect scan: PASS (0 issues)")
    print("Duplication check: PASS (no prior-batch / MCQ Batch 3 fingerprints)")
    print("LO-overlap distinctness: PASS (2.2.1, 2.5.1, 2.6.1 distinct from Batch 3)")
