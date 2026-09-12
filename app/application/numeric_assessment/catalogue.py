"""Load migrated Answer Specifications from live educational package JSON.

Canonical store: each numeric checkpoint's ``answer_specification`` field in
``app/curriculum/data/educational_packages/``. Live ``score_practice_response``
uses these specs only when ``SR_NUMERIC_ASSESSMENT_FRAMEWORK`` is ON; otherwise
the legacy ``numeric_tolerance`` / ``accepted_keywords`` path remains.

This module does not import the educational package ORM models beyond the
shared package-root path helper, and it never calls ``score_practice_response``.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.application.educational_packages.loader import package_data_root
from app.application.numeric_assessment.specs import (
    AnswerSpecification,
    AssessmentIntent,
    ComparisonPolicy,
    DiagnosticRule,
    EvaluationPolicy,
    FeedbackPolicy,
    PrecisionPolicy,
    PrecisionRequirement,
    QuantityType,
    RepresentationForm,
    RepresentationPolicy,
    RoundingPolicy,
)

# Expected live CS1 numeric checkpoint count (publication-approved catalogue).
LIVE_NUMERIC_CHECKPOINT_COUNT = 30

# Banked precision-tolerance mismatches fixed under decimal_precision migration.
BANKED_PRECISION_TOLERANCE_ITEM_IDS: frozenset[str] = frozenset(
    {
        "cs1003-4.2.5-cp-01",
        "cs1003-4.2.8-cp-01",
        "cs1004-cgr1-cp-01",
        "cs1014-4.2.5-cp-01",
    }
)


def _enum(enum_cls: type, value: str) -> Any:
    return enum_cls(str(value).strip())


def _parse_comparison(raw: dict[str, Any]) -> ComparisonPolicy:
    return ComparisonPolicy(
        policy=_enum(EvaluationPolicy, raw["policy"]),
        absolute_tolerance=raw.get("absolute_tolerance"),
        relative_tolerance=raw.get("relative_tolerance"),
        decimal_places=raw.get("decimal_places"),
        significant_figures=raw.get("significant_figures"),
        interval_low=raw.get("interval_low"),
        interval_high=raw.get("interval_high"),
        custom_rule_id=raw.get("custom_rule_id"),
    )


def _parse_precision(raw: dict[str, Any] | None) -> PrecisionPolicy:
    if not raw:
        return PrecisionPolicy()
    return PrecisionPolicy(
        requirement=_enum(
            PrecisionRequirement, raw.get("requirement") or "none"
        ),
        decimal_places=raw.get("decimal_places"),
    )


def _parse_diagnostics(raw_list: list[Any] | None) -> tuple[DiagnosticRule, ...]:
    rules: list[DiagnosticRule] = []
    for raw in raw_list or ():
        if not isinstance(raw, dict):
            continue
        rules.append(
            DiagnosticRule(
                rule_id=str(raw.get("rule_id") or "").strip(),
                match_value=float(raw["match_value"]),
                consistent_with=str(raw.get("consistent_with") or "").strip(),
                match_absolute_tolerance=float(
                    raw.get("match_absolute_tolerance") or 0.0
                ),
                rationale=str(raw.get("rationale") or "").strip(),
            )
        )
    return tuple(rules)


def answer_specification_from_dict(raw: dict[str, Any]) -> AnswerSpecification:
    """Build an AnswerSpecification from a package JSON object."""
    forms_raw = raw.get("accepted_forms") or ("decimal",)
    forms = tuple(_enum(RepresentationForm, f) for f in forms_raw)
    feedback_raw = raw.get("feedback_policy") or {}
    feedback = FeedbackPolicy(
        tier3_message=str(
            feedback_raw.get("tier3_message")
            or FeedbackPolicy().tier3_message
        ),
        prefer_first_matching_diagnostic=bool(
            feedback_raw.get("prefer_first_matching_diagnostic", True)
        ),
    )
    return AnswerSpecification(
        item_id=str(raw.get("item_id") or "").strip(),
        canonical_value=float(raw["canonical_value"]),
        quantity_type=_enum(QuantityType, raw["quantity_type"]),
        assessment_intent=_enum(AssessmentIntent, raw["assessment_intent"]),
        comparison_policy=_parse_comparison(raw["comparison_policy"]),
        unit=str(raw.get("unit") or ""),
        representation_policy=RepresentationPolicy(accepted_forms=forms),
        precision_policy=_parse_precision(raw.get("precision_policy")),
        rounding_policy=_enum(
            RoundingPolicy, raw.get("rounding_policy") or "none"
        ),
        diagnostic_rules=_parse_diagnostics(raw.get("diagnostic_rules")),
        feedback_policy=feedback,
    )


def _iter_package_json_files() -> list[Path]:
    root = package_data_root()
    if not root.is_dir():
        return []
    return sorted(root.rglob("*.json"))


def _extract_specs_from_package(path: Path) -> list[AnswerSpecification]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(raw, dict):
        return []
    status = str(raw.get("status") or "").strip().lower()
    if status not in {"publication_approved", "approved", "certified"}:
        return []
    specs: list[AnswerSpecification] = []
    for check in raw.get("knowledge_checks") or ():
        if not isinstance(check, dict):
            continue
        if str(check.get("response_type") or "").strip() != "numeric":
            continue
        if str(check.get("kind") or "").strip() != "checkpoint":
            continue
        block = check.get("answer_specification")
        if not isinstance(block, dict):
            continue
        # Ensure item_id is present even if omitted inside the block.
        if not block.get("item_id"):
            block = {**block, "item_id": str(check.get("item_id") or "").strip()}
        specs.append(answer_specification_from_dict(block))
    return specs


@lru_cache(maxsize=1)
def load_live_answer_specifications() -> dict[str, AnswerSpecification]:
    """Return all migrated live numeric Answer Specifications keyed by item_id."""
    found: dict[str, AnswerSpecification] = {}
    for path in _iter_package_json_files():
        for spec in _extract_specs_from_package(path):
            if spec.item_id in found:
                raise ValueError(
                    f"Duplicate answer_specification for item_id {spec.item_id!r}"
                )
            found[spec.item_id] = spec
    return found


def reset_live_answer_specification_cache() -> None:
    """Clear catalogue cache (tests)."""
    load_live_answer_specifications.cache_clear()


def get_live_answer_specification(item_id: str) -> AnswerSpecification | None:
    """Lookup one migrated specification by item id."""
    return load_live_answer_specifications().get((item_id or "").strip())
