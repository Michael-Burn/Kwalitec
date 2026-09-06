"""Mathematical notation inventory: reproducibility against the live catalogue."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "inventory_math_notation.py"
CHECKED_IN_JSON = REPO_ROOT / "docs" / "content" / "math_notation_inventory.json"

# Make the script importable without installing as a package.
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import inventory_math_notation as inventory  # noqa: E402


@pytest.fixture(scope="module")
def live_payload() -> dict:
    catalogue = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
    assert catalogue.is_dir()
    return inventory.build_inventory(catalogue)


def test_inventory_builds_against_live_catalogue(live_payload: dict) -> None:
    totals = live_payload["totals"]
    assert live_payload["live_package_count"] >= 130
    assert totals["mathish_strings"] > 0
    assert totals["needs_migration"] > 0
    assert totals["already_compliant"] + totals["needs_migration"] + totals[
        "correctly_excluded"
    ] == totals["mathish_strings"]
    assert totals["needs_manual_review"] >= 0
    assert totals["confident_automated"] + totals["needs_manual_review"] == totals[
        "mathish_strings"
    ]
    assert "content_fingerprint" in live_payload
    assert live_payload["packages"]


def test_inventory_is_reproducible(live_payload: dict) -> None:
    catalogue = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
    second = inventory.build_inventory(catalogue)
    assert second["content_fingerprint"] == live_payload["content_fingerprint"]
    assert second["totals"] == live_payload["totals"]


def test_checked_in_ledger_matches_live_catalogue(live_payload: dict) -> None:
    assert CHECKED_IN_JSON.is_file(), (
        "Checked-in inventory missing; run "
        "`python scripts/inventory_math_notation.py`"
    )
    checked = json.loads(CHECKED_IN_JSON.read_text(encoding="utf-8"))
    assert checked["content_fingerprint"] == live_payload["content_fingerprint"]
    assert checked["totals"] == live_payload["totals"]


def test_wave_recommendation_present(live_payload: dict) -> None:
    wave = live_payload["wave_recommendation"]["wave_1"]
    assert wave["package_count"] > 0
    assert wave["needs_migration_strings"] > 0
    assert "compound" in wave["label"].lower() or "tier" in wave["label"].lower()


def test_cli_runs_cleanly(tmp_path: Path) -> None:
    json_out = tmp_path / "inv.json"
    summary_out = tmp_path / "inv.md"
    rc = inventory.main(
        [
            "--catalogue",
            str(REPO_ROOT / "app/curriculum/data/educational_packages/cs1"),
            "--json",
            str(json_out),
            "--summary",
            str(summary_out),
        ]
    )
    assert rc == 0
    assert json_out.is_file()
    assert summary_out.is_file()
    payload = json.loads(json_out.read_text(encoding="utf-8"))
    assert payload["totals"]["mathish_strings"] > 0
