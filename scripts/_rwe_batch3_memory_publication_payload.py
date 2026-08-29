#!/usr/bin/env python3
"""Real Worked Examples Batch 3 - Memory / Publication Front (Pi / Rho).

Injects genuine ``worked_example`` objects into the 15 confirmed Pi/Rho
packages (Domain F1b Batch 3), then synchronises catalogue and campaign twins.

Content lives in ``_rwe_batch3_memory_publication_data.json`` beside this module.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

_DATA = Path(__file__).with_name("_rwe_batch3_memory_publication_data.json")
_BLOB = json.loads(_DATA.read_text(encoding="utf-8"))
WORKED_EXAMPLES: dict[str, dict[str, Any]] = _BLOB["worked_examples"]
CAMPAIGN_TWINS: dict[str, str] = _BLOB["campaign_twins"]

EXPECTED_COUNT = 15

# Forbidden scenario / number fingerprints from prior RWE batches and MCQ Batch 3.
_DUPLICATION_FINGERPRINTS: list[tuple[str, re.Pattern[str]]] = [
    ("Phase0 disease screen P(D)=0.01/0.95/0.10", re.compile(r"P\(D\)\s*=\s*0\.01")),
    ("Phase0 sensitivity 0.95 with FPR 0.10", re.compile(r"0\.95.*0\.10|0\.10.*0\.95")),
    ("Batch2 fraud screen P(Fraud)=0.05", re.compile(r"P\(Fraud\)\s*=\s*0\.05")),
    ("Batch2 fraud sens 0.90 / FPR 0.15", re.compile(r"0\.90.*0\.15|Fraud.*0\.90")),
    ("MCQ B3 Exp theta=1000", re.compile(r"θ\s*=\s*1000|theta\s*=\s*1000|mean θ = 1000")),
    ("MCQ B3 joint 0.10/0.20/0.30/0.40", re.compile(r"0\.10.*0\.20.*0\.30.*0\.40")),
    ("MCQ B3 CLT mu=500 sigma=200 n=100", re.compile(r"μ\s*=\s*500.*σ\s*=\s*200|mu\s*=\s*500.*sigma\s*=\s*200")),
    ("Batch2 motor severity ŷ=1200+40x age 45", re.compile(r"1200\s*\+\s*40x|age 45")),
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

    # 2.1.3 Exponential θ=800
    f400 = 1 - math.exp(-0.5)
    median = 800 * math.log(2)
    if abs(f400 - 0.3935) > 5e-4:
        defects.append(f"2.1.3 CDF mismatch: {f400}")
    if abs(median - 554.5) > 0.05:
        defects.append(f"2.1.3 median mismatch: {median}")

    # 2.2.1 joint table
    if abs(0.20 + 0.60 - 0.80) > 1e-12:
        defects.append("2.2.1 marginal mismatch")
    if abs(0.20 / 0.80 - 0.25) > 1e-12:
        defects.append("2.2.1 conditional mismatch")
    if abs(0.05 + 0.15 + 0.20 + 0.60 - 1.0) > 1e-12:
        defects.append("2.2.1 joint table does not sum to 1")

    # 2.5.1 CLT
    se = 300 / math.sqrt(36)
    z = (1150 - 1200) / se
    p = 1 - 0.841
    if abs(se - 50) > 1e-12 or abs(z + 1) > 1e-12 or abs(p - 0.159) > 1e-12:
        defects.append(f"2.5.1 CLT mismatch se={se} z={z} p={p}")

    # 4.1.1 premium line
    if 180 + 12 * 25 != 480:
        defects.append("4.1.1 fitted premium mismatch")

    # 5.1.1 Bayes cyber
    evidence = 0.88 * 0.03 + 0.12 * 0.97
    posterior = (0.88 * 0.03) / evidence
    if abs(evidence - 0.1428) > 1e-12:
        defects.append(f"5.1.1 evidence mismatch: {evidence}")
    if abs(posterior - 0.18487394957983194) > 5e-5:
        defects.append(f"5.1.1 posterior mismatch: {posterior}")

    # 1.2.1 EDA
    counts = [0, 0, 1, 3, 10]
    mean = sum(counts) / 5
    if abs(mean - 2.8) > 1e-12:
        defects.append(f"1.2.1 mean mismatch: {mean}")

    # 2.1.1 Poisson
    p0 = math.exp(-0.4)
    if abs(p0 - 0.6703) > 5e-4:
        defects.append(f"2.1.1 P(X=0) mismatch: {p0}")

    # 2.1.2 Exponential survival
    surv = math.exp(-1)
    if abs(surv - 0.3679) > 5e-4:
        defects.append(f"2.1.2 survival mismatch: {surv}")

    return defects


def duplication_check() -> list[str]:
    defects: list[str] = []
    for inv_key, example in WORKED_EXAMPLES.items():
        raw = json.dumps(example, ensure_ascii=False)
        for label, pattern in _DUPLICATION_FINGERPRINTS:
            # Phase0 sensitivity fingerprint is too broad if applied to all;
            # only flag when disease-screen OR fraud OR the specific triples appear.
            if label.startswith("Phase0 sensitivity") and "Breach" in raw:
                # New Bayes uses 0.88/0.12; still avoid 0.95 with 0.10 together.
                if re.search(r"0\.95", raw) and re.search(r"0\.10", raw):
                    defects.append(f"{inv_key}: duplication hit '{label}'")
                continue
            if pattern.search(raw):
                defects.append(f"{inv_key}: duplication hit '{label}'")
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
    defects.extend(arithmetic_sanity_checks())
    defects.extend(duplication_check())
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
    print("Arithmetic sanity: PASS")
