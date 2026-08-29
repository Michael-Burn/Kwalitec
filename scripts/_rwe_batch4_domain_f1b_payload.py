#!/usr/bin/env python3
"""Real Worked Examples Batch 4 - Domain F1b (Delta / cs1003).

Injects genuine ``worked_example`` objects into the 24 confirmed Delta packages
(linear regression, GLM structure, Bayesian foundations), then synchronises
catalogue and campaign-delta-cs1003 twins.

Content lives in ``_rwe_batch4_domain_f1b_data.json`` beside this module
so the large verified numeric payloads stay reviewable as structured data.

Every example is authored to be scenario- and number-distinct from its Batch 2
twin (Nu/Xi/Omicron cs1013-cs1015) and from Batches 1 and 3 / Phase 0.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

_DATA = Path(__file__).with_name("_rwe_batch4_domain_f1b_data.json")
_BLOB = json.loads(_DATA.read_text(encoding="utf-8"))
WORKED_EXAMPLES: dict[str, dict[str, Any]] = _BLOB["worked_examples"]
CAMPAIGN_TWINS: dict[str, str] = _BLOB["campaign_twins"]


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

    if len(WORKED_EXAMPLES) != 24:
        defects.append(f"expected 24 examples, got {len(WORKED_EXAMPLES)}")
    return defects


if __name__ == "__main__":
    assert len(WORKED_EXAMPLES) == 24, len(WORKED_EXAMPLES)
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
