#!/usr/bin/env python3
"""Inventory live CS1 package strings against the Mathematical Notation Standard.

Reads publication-approved packages under
``app/curriculum/data/educational_packages/cs1/``, classifies mathish
student-facing strings, and writes a reproducible ledger JSON (and optional
Markdown summary).

Does not modify authored package content or rendering code.

Usage:
    python scripts/inventory_math_notation.py
    python scripts/inventory_math_notation.py --json path --summary path
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOGUE = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
DEFAULT_JSON_OUT = REPO_ROOT / "docs/content/math_notation_inventory.json"
DEFAULT_SUMMARY_OUT = REPO_ROOT / "docs/content/math_notation_inventory_summary.md"

LIVE_STATUSES = frozenset({"publication_approved", "approved", "certified"})

# Same bare-fragment family as app.presentation.session.math_markup (read-only mirror).
_BARE_LATEX_FRAGMENT = re.compile(
    r"(?<!\$)"
    r"(?:"
    r"e\^\{(?P<eexp>[^{}]+)\}"
    r"|"
    r"(?P<id>[A-Za-zλμθηβΣℓ]+)\^\{(?P<idexp>[^{}]+)\}"
    r"|"
    r"(?P<id2>[A-Za-zλμθηβΣℓ]+)\^(?P<sup>[0-9]+)"
    r")"
    r"(?!\$)"
)

GREEK = set(
    "αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩϕϖϱςϑϵ"
)
OPS = set("±×÷−≠≈≤≥∈∅∞∂∇√∑∏∫≃≅≡≪≫")
SUPS = set("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ⁿ²³")
SUBS = set("₀₁₂₃₄₅₆₇₈₉ₙ")
LETTERLIKE = set("ℓΦφχρΔεη")
COMBINING = set("\u0304\u0305\u0302\u0303")  # macron, overline, hat, tilde
MATH_UNICODE = GREEK | OPS | SUPS | SUBS | LETTERLIKE | COMBINING

_ACTUARIAL = re.compile(
    r"\bP\s*\([^)]{0,80}\)"
    r"|\bE\s*\[[^\]]{0,80}\]"
    r"|\bVar\s*\([^)]{0,80}\)"
    r"|\bCov\s*\([^)]{0,80}\)"
    r"|\bCorr\s*\([^)]{0,40}\)"
    r"|\bsd\s*\([^)]{0,40}\)"
    r"|\bΦ\s*\("
)

_ASCII_MATH = [
    re.compile(r"\bsqrt\s*\("),
    re.compile(r"\bexp\s*\("),
    re.compile(r"\bsum_[A-Za-z0-9{]"),
    re.compile(
        r"(?<![A-Za-z/])[A-Za-zλμσθβΣχ]_(?:\{[^}]+\}|[0-9A-Za-z]{1,8})\b"
    ),
    re.compile(r"(?:\)|\d)\^[{\dA-Za-z]"),
    re.compile(r"\b(?:lambda|mu|sigma|theta|rho|beta)\s*=", re.I),
    re.compile(r"\bM_[A-Za-z]"),
]

_EQUATIONISH = re.compile(
    r"[=≈≠≤≥<>]|[√∑∏∫]|\^|_(?:\{|[0-9A-Za-z])|(?<![A-Za-z])/|(?<=[A-Za-zσμλθβ])/"
)
_COMPOUND = re.compile(
    r"√|σ\s*/|σ²\s*/|/\s*√|−√|Σ|\bS_x|ℓ\(|dℓ/|d²ℓ|"
    r"β̂|λ̂|μ̂|X̄\s*≈|N\([^)]*σ|/\s*n\b"
)
_PROSE_MENTION = re.compile(
    r"(?i)\b(denotes|denote|stands for|called|known as|refers to|"
    r"the symbol|written as|we write|notation for|means the)\b"
)
_DOLLAR_MATH = re.compile(r"(?<!\$)\$[^$]+\$")

# Student-facing field roots inventoried (matches prior landscape investigation).
_SCOPE_ROOTS = (
    "worked_example",
    "knowledge_checks",
    "reading_guidance",
    "mission",
)

# Paths that are never conversion targets even if pattern-matched.
_SKIP_SUFFIXES = (
    ".misconception_tag",
    ".kind",
    ".item_id",
    ".episode_id",
    ".correct_choice_id",
    ".response_type",
    ".accepted_keywords",
)

_MATH_OBJECT_PATH = re.compile(
    r"(?:"
    r"problem_statement|final_answer|calculation|result|"
    r"model_answer|prompt|"
    r"choices\[\d+\]\.label|"
    r"given\[\d+\]\.(?:symbol|value)"
    r")$"
)

_NARRATIVE_PATH = re.compile(
    r"(?:"
    r"explanation|attempt_cue|attempt_before_reveal|common_pitfall|"
    r"common_mistake|hints\[\d+\]|success_criteria(?:\[\d+\])?|body|title|"
    r"label|note|open_point|exit_line|misconception_watch\[\d+\]|"
    r"out_of_scope_today\[\d+\]|focus_questions\[\d+\]|annotation_task|"
    r"stop_condition|concept_focus|task_descriptions\[\d+\]|tutor_intent|"
    r"expected_benefit|mission_purpose|why_now|prior_bridge|"
    r"educational_intent|learning_objective|display_title"
    r")$"
)

Category = str  # already_compliant | needs_migration | correctly_excluded

# Human-reviewed Wave 1 leftovers: prose exclusions locked by semantic-role review.
# Keys are (package_file, field_path, text_hash). Hash mismatch means content moved;
# do not silently keep the old decision.
_MANUAL_PROSE_EXCLUSIONS: frozenset[tuple[str, str, str]] = frozenset(
    {
        (
            "4.2.8-residuals-cs1014.json",
            "mission.mission_purpose",
            "850bd0e8b1a91fe3",
        ),
        (
            "4.2.8-residuals-cs1014.json",
            "reading_guidance.misconception_watch[1]",
            "ee133dda448be2f9",
        ),
        (
            "4.2.8-residuals-cs1014.json",
            "reading_guidance.stop_condition",
            "aa084b69b59b2958",
        ),
        (
            "4.2.8-residuals-cs1014.json",
            "reading_guidance.out_of_scope_today[0]",
            "0de776128df469d8",
        ),
        (
            "4.2.8-residuals-cs1014.json",
            "reading_guidance.exit_line",
            "ad996a45339ce1a2",
        ),
        (
            "4.2.8-residuals-cs1003.json",
            "reading_guidance.out_of_scope_today[0]",
            "020e0de14be38996",
        ),
        (
            "2.6.4-normal-sample-mean-var-cs1009.json",
            "mission.success_criteria[1]",
            "63dc8ebf902f3ff4",
        ),
        (
            "2.6.4-normal-sample-mean-var-cs1009.json",
            "reading_guidance.misconception_watch[1]",
            "af83592dd55596ca",
        ),
        # Wave 3 leftovers: η as syllabus topic name (not live math).
        (
            "4.2.6-deviance-estimation-cs1003.json",
            "mission.prior_bridge",
            "fd95a7a521964a4c",
        ),
        (
            "4.2.6-deviance-estimation-cs1014.json",
            "mission.why_now",
            "c911f5a1b83f02e2",
        ),
        # Wave 4 leftover: χ² as CMP syllabus topic name (not live math).
        (
            "4.2.9-goodness-tests-cs1003.json",
            "reading_guidance.exit_line",
            "128fa0d3e098e42e",
        ),
        # Wave 6 leftovers: η-form / topic coupling, or exp() as software brand.
        (
            "4.2.4-factors-interactions-cs1014.json",
            "mission.tutor_intent",
            "e354a000f891d3af",
        ),
        (
            "4.2.4-factors-interactions-cs1014.json",
            "mission.why_now",
            "35fb4f7db2117adb",
        ),
        (
            "4.2.5-linear-predictor-cs1003.json",
            "mission.prior_bridge",
            "0bb776511886a9b1",
        ),
        (
            "4.2.1-exponential-family-cs1014.json",
            "knowledge_checks[0].explanation",
            "206e61ffbb954598",
        ),
        (
            "4.2.1-exponential-family-cs1014.json",
            "knowledge_checks[1].explanation",
            "f2de1c8e9ff25fed",
        ),
        # Wave 7 leftovers: exp() software brand, χ²/LRT topic, fit-measure path,
        # Family/η/Link sketch columns (not live math in these fields).
        (
            "4.2.1-exponential-family-cs1003.json",
            "knowledge_checks[0].explanation",
            "206e61ffbb954598",
        ),
        (
            "4.2.1-exponential-family-cs1003.json",
            "knowledge_checks[1].explanation",
            "f2de1c8e9ff25fed",
        ),
        (
            "4.2.7-model-choice-cs1014.json",
            "reading_guidance.out_of_scope_today[1]",
            "0de776128df469d8",
        ),
        (
            "4.1.5-variable-selection-cs1003.json",
            "mission.concept_focus",
            "e93d97704a81d974",
        ),
        (
            "4.1.5-variable-selection-cs1013.json",
            "mission.concept_focus",
            "e93d97704a81d974",
        ),
        (
            "4.2.3-link-canonical-cs1003.json",
            "mission.task_descriptions[0]",
            "189f5bd5e2eb5799",
        ),
        # Wave 8 leftovers: Z/μ as concept-focus path landmarks, or μ/k named
        # only inside explanatory "including …" prose (not live formulas).
        (
            "5.1.7-bayesian-credibility-cs1015.json",
            "mission.concept_focus",
            "727493caa693dc03",
        ),
        (
            "5.1.7-bayesian-credibility-cs1015.json",
            "worked_example.steps[0].explanation",
            "76726aae6ef329b9",
        ),
        (
            "5.1.7-bayesian-credibility-cs1003.json",
            "mission.concept_focus",
            "727493caa693dc03",
        ),
        # Wave 9 leftovers: χ² as syllabus checklist topic; η as schematic
        # campaign/revision path waypoint (not live math in these fields).
        (
            "revision-glm-cs1014.json",
            "mission.learning_objective",
            "3ddf965eabfeabe1",
        ),
        (
            "revision-glm-cs1014.json",
            "mission.concept_focus",
            "bc9127f81da35a77",
        ),
        (
            "revision-regression-glm-cs1003.json",
            "mission.concept_focus",
            "9f53a348764e212f",
        ),
    }
)


@dataclass(frozen=True)
class InventoryItem:
    package_id: str
    package_file: str
    field_path: str
    field_group: str
    text: str
    text_hash: str
    category: Category
    needs_manual_review: bool
    reason_code: str
    risk_tier: int
    migration_status: str
    signals: tuple[str, ...]


def _normalise_path(path: str) -> str:
    return path[2:] if path.startswith("$.") else path


def _field_group(path: str) -> str:
    p = _normalise_path(path)
    return re.sub(r"\[\d+\]", "[]", p)


def _walk_strings(obj: Any, path: str = "$") -> Iterator[tuple[str, str]]:
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield from _walk_strings(value, f"{path}.{key}")
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            yield from _walk_strings(value, f"{path}[{index}]")
    elif isinstance(obj, str) and obj.strip():
        yield path, obj


def _in_scope(path: str) -> bool:
    p = _normalise_path(path)
    if not any(
        p == root or p.startswith(f"{root}.") or p.startswith(f"{root}[")
        for root in _SCOPE_ROOTS
    ):
        return False
    if p.endswith(_SKIP_SUFFIXES):
        return False
    return True


def is_mathish(text: str) -> bool:
    """Return True when the string matches the investigation-era mathish detectors."""
    if any(ch in MATH_UNICODE for ch in text):
        return True
    if _BARE_LATEX_FRAGMENT.search(text):
        return True
    if _ACTUARIAL.search(text):
        return True
    if any(pattern.search(text) for pattern in _ASCII_MATH):
        return True
    if _DOLLAR_MATH.search(text):
        return True
    return False


def _signals(text: str) -> list[str]:
    found: list[str] = []
    if any(ch in GREEK for ch in text):
        found.append("greek")
    if any(ch in OPS for ch in text):
        found.append("unicode_ops")
    if "√" in text:
        found.append("root")
    if any(ch in "∑∏∫" for ch in text):
        found.append("sum_or_integral")
    if _BARE_LATEX_FRAGMENT.search(text):
        found.append("bare_latex")
    if _DOLLAR_MATH.search(text):
        found.append("dollar_delimited")
    if _ACTUARIAL.search(text):
        found.append("actuarial_fn")
    if any(pattern.search(text) for pattern in _ASCII_MATH):
        found.append("ascii_approx")
    if _COMPOUND.search(text):
        found.append("compound")
    if _EQUATIONISH.search(text):
        found.append("equationish")
    return found


def _strip_compliant_spans(text: str) -> str:
    stripped = _DOLLAR_MATH.sub("", text)
    return _BARE_LATEX_FRAGMENT.sub("", stripped)


def _remaining_math(text: str) -> bool:
    return is_mathish(_strip_compliant_spans(text))


def _risk_tier(path: str, text: str, signals: list[str]) -> int:
    """1 = highest-risk compound calculations; 4 = light / chrome."""
    p = _normalise_path(path)
    in_calc = any(
        token in p
        for token in (
            ".calculation",
            ".final_answer",
            ".result",
            ".problem_statement",
            ".model_answer",
            ".choices[",
        )
    )
    if "compound" in signals or "root" in signals:
        return 1 if in_calc else 2
    if "actuarial_fn" in signals and in_calc:
        return 2
    if in_calc or "equationish" in signals:
        return 3
    return 4


def classify_string(path: str, text: str) -> tuple[Category, bool, str, list[str]]:
    """Classify one mathish string.

    Returns (category, needs_manual_review, reason_code, signals).

    Ambiguous cases always set needs_manual_review=True and still receive a
    provisional category so the ledger remains countable; they are never
    silently forced without the flag.
    """
    signals = _signals(text)
    p = _normalise_path(path)

    # Properly typeset today: only delimited math and/or bare LaTeX that the
    # existing session wrapper typesets, with no leftover math objects.
    covered = "dollar_delimited" in signals or "bare_latex" in signals
    if covered and not _remaining_math(text):
        return (
            "already_compliant",
            False,
            "fully_covered_by_current_typesetting",
            signals,
        )

    math_field = bool(_MATH_OBJECT_PATH.search(p))
    narrative = bool(_NARRATIVE_PATH.search(p))
    has_eq = (
        "equationish" in signals
        or "actuarial_fn" in signals
        or "bare_latex" in signals
    )
    has_compound = "compound" in signals or "root" in signals
    prose_cue = bool(_PROSE_MENTION.search(text))

    if math_field:
        return "needs_migration", False, "math_object_field", signals

    if has_compound:
        return "needs_migration", False, "compound_structure", signals

    if "actuarial_fn" in signals and (
        has_eq
        or any(
            token in p
            for token in (
                "calculation",
                "final_answer",
                "choices",
                "prompt",
                "model_answer",
                "problem_statement",
            )
        )
    ):
        return "needs_migration", False, "actuarial_expression", signals

    # Confident prose exclusion: narrative + explicit mention cue, no equation.
    if narrative and prose_cue and not has_eq and not has_compound:
        return "correctly_excluded", False, "prose_mention_cue", signals

    # Isolated symbol / light math in narrative: ambiguous under the standard.
    if narrative and not has_compound:
        if ("greek" in signals or "unicode_ops" in signals) and not has_eq:
            # Lean exclude (prose mention) but require human confirmation.
            return (
                "correctly_excluded",
                True,
                "isolated_symbol_in_narrative_ambiguous",
                signals,
            )
        if has_eq or "actuarial_fn" in signals or "ascii_approx" in signals:
            return (
                "needs_migration",
                True,
                "narrative_with_inline_math_ambiguous",
                signals,
            )

    if has_eq or "ascii_approx" in signals or "bare_latex" in signals:
        return "needs_migration", True, "mathish_default_ambiguous", signals

    if signals:
        return "correctly_excluded", True, "mathish_role_unclear", signals

    return "correctly_excluded", True, "mathish_role_unclear", signals


def _text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def iter_live_packages(catalogue_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    packages: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(catalogue_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("status") not in LIVE_STATUSES:
            continue
        packages.append((path, data))
    return packages


def build_inventory(catalogue_dir: Path) -> dict[str, Any]:
    items: list[InventoryItem] = []
    category_counts: Counter[str] = Counter()
    manual_review_count = 0
    signal_counts: Counter[str] = Counter()
    reason_counts: Counter[str] = Counter()
    tier_counts: Counter[int] = Counter()

    packages_out: list[dict[str, Any]] = []

    for path, data in iter_live_packages(catalogue_dir):
        package_id = str(data.get("package_id") or path.stem)
        pkg_items: list[InventoryItem] = []
        for field_path, text in _walk_strings(data):
            if not _in_scope(field_path):
                continue
            if not is_mathish(text):
                continue
            category, needs_review, reason, signals = classify_string(field_path, text)
            field_norm = _normalise_path(field_path)
            text_hash = _text_hash(text)
            if (path.name, field_norm, text_hash) in _MANUAL_PROSE_EXCLUSIONS:
                category = "correctly_excluded"
                needs_review = False
                reason = "manual_review_prose_exclusion"
            tier = _risk_tier(field_path, text, signals)
            # Dollar-delimited LaTeX that fully covers the string is a completed
            # migration (Wave 1 onward). Bare-LaTeX-only compliance stays pending
            # until an authoring wave records it. Manual prose exclusions are
            # recorded as correctly_excluded (not a migration backlog item).
            if category == "already_compliant" and "dollar_delimited" in signals:
                status = "migrated"
            elif reason == "manual_review_prose_exclusion":
                status = "correctly_excluded"
            else:
                status = "pending"
            item = InventoryItem(
                package_id=package_id,
                package_file=path.name,
                field_path=field_norm,
                field_group=_field_group(field_path),
                text=text,
                text_hash=text_hash,
                category=category,
                needs_manual_review=needs_review,
                reason_code=reason,
                risk_tier=tier,
                migration_status=status,
                signals=tuple(signals),
            )
            pkg_items.append(item)
            items.append(item)
            category_counts[category] += 1
            if needs_review:
                manual_review_count += 1
            for signal in signals:
                signal_counts[signal] += 1
            reason_counts[reason] += 1
            tier_counts[tier] += 1

        pkg_counts = Counter(i.category for i in pkg_items)
        pkg_manual = sum(1 for i in pkg_items if i.needs_manual_review)
        pkg_tier1 = sum(
            1
            for i in pkg_items
            if i.category == "needs_migration" and i.risk_tier == 1
        )
        packages_out.append(
            {
                "package_id": package_id,
                "package_file": path.name,
                "topic_code": data.get("topic_code"),
                "campaign_id": data.get("campaign_id"),
                "counts": {
                    "mathish_strings": len(pkg_items),
                    "already_compliant": pkg_counts["already_compliant"],
                    "needs_migration": pkg_counts["needs_migration"],
                    "correctly_excluded": pkg_counts["correctly_excluded"],
                    "needs_manual_review": pkg_manual,
                    "risk_tier_1_needs_migration": pkg_tier1,
                },
                "migration_status": "pending"
                if pkg_counts["needs_migration"]
                else ("clear" if pkg_items else "no_mathish"),
                "remaining_backlog": pkg_counts["needs_migration"],
                "items": [asdict(i) for i in pkg_items],
            }
        )

    packages_out.sort(
        key=lambda row: (
            -row["counts"]["risk_tier_1_needs_migration"],
            -row["counts"]["needs_migration"],
            row["package_id"],
        )
    )

    wave_recommendation = recommend_migration_waves(packages_out)

    payload = {
        "schema_version": 1,
        "standard_ref": "docs/content/MATHEMATICAL_NOTATION_STANDARD.md",
        "generated_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "catalogue_dir": str(catalogue_dir.relative_to(REPO_ROOT)),
        "live_package_count": len(packages_out),
        "totals": {
            "mathish_strings": len(items),
            "already_compliant": category_counts["already_compliant"],
            "needs_migration": category_counts["needs_migration"],
            "correctly_excluded": category_counts["correctly_excluded"],
            "needs_manual_review": manual_review_count,
            "confident_automated": len(items) - manual_review_count,
            "remaining_backlog": category_counts["needs_migration"],
            "migrated": sum(
                1 for item in items if item.migration_status == "migrated"
            ),
            "packages_with_migration_backlog": sum(
                1 for row in packages_out if row["counts"]["needs_migration"] > 0
            ),
        },
        "by_reason_code": dict(reason_counts.most_common()),
        "by_signal": dict(signal_counts.most_common()),
        "by_risk_tier_needs_migration": {
            str(tier): sum(
                1
                for item in items
                if item.category == "needs_migration" and item.risk_tier == tier
            )
            for tier in (1, 2, 3, 4)
        },
        "limits_of_automation": {
            "note": (
                "Semantic role (live mathematical object vs prose mention) cannot "
                "be decided by pattern matching in every case. Strings with "
                "needs_manual_review=true must be human-checked before a wave "
                "marks them done or skips them."
            ),
            "needs_manual_review_count": manual_review_count,
        },
        "wave_recommendation": wave_recommendation,
        "packages": packages_out,
    }
    payload["content_fingerprint"] = fingerprint_payload(payload)
    return payload


def fingerprint_payload(payload: dict[str, Any]) -> str:
    """Stable hash over classification outcomes (ignores generated_at)."""
    digest_source = {
        "totals": payload["totals"],
        "by_reason_code": payload["by_reason_code"],
        "packages": [
            {
                "package_id": row["package_id"],
                "counts": row["counts"],
                "items": [
                    {
                        "field_path": item["field_path"],
                        "text_hash": item["text_hash"],
                        "category": item["category"],
                        "needs_manual_review": item["needs_manual_review"],
                        "reason_code": item["reason_code"],
                        "risk_tier": item["risk_tier"],
                    }
                    for item in row["items"]
                ],
            }
            for row in payload["packages"]
        ],
    }
    blob = json.dumps(digest_source, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def recommend_migration_waves(packages: list[dict[str, Any]]) -> dict[str, Any]:
    """Order-only recommendation: highest-risk compound calculation packages first.

    Prefer packages with tier-1 ``needs_migration`` strings. When none remain,
    fall through to the next 12 packages by the ledger ranking already applied
    to ``packages`` (tier-1 count, then backlog size).
    """
    tier1 = [
        row
        for row in packages
        if row["counts"]["risk_tier_1_needs_migration"] > 0
    ]
    remaining_tier1 = tier1[12:]
    other = [
        row
        for row in packages
        if row["counts"]["needs_migration"] > 0
        and row["counts"]["risk_tier_1_needs_migration"] == 0
    ]
    if tier1:
        wave1 = tier1[:12]
        wave_label = "Highest-risk compound calculation boards"
    else:
        backlog = [row for row in packages if row["counts"]["needs_migration"] > 0]
        wave1 = backlog[:12]
        wave_label = "Highest-backlog migration boards (no tier-1 remaining)"

    def slim(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            {
                "package_id": row["package_id"],
                "package_file": row["package_file"],
                "needs_migration": row["counts"]["needs_migration"],
                "risk_tier_1_needs_migration": row["counts"][
                    "risk_tier_1_needs_migration"
                ],
                "needs_manual_review": row["counts"]["needs_manual_review"],
            }
            for row in rows
        ]

    return {
        "principle": (
            "Order only: tackle highest-risk compound calculations first for "
            "immediate student benefit. This does not narrow ultimate scope; "
            "every needs_migration string remains in backlog until migrated or "
            "reclassified by manual review."
        ),
        "wave_1": {
            "label": wave_label,
            "packages": slim(wave1),
            "package_count": len(wave1),
            "needs_migration_strings": sum(
                row["counts"]["needs_migration"] for row in wave1
            ),
        },
        "wave_2_candidates": {
            "label": "Remaining tier-1 compound packages",
            "packages": slim(remaining_tier1[:15]),
            "package_count_remaining_tier1": len(remaining_tier1),
        },
        "later_waves": {
            "label": (
                "Non-tier-1 backlog (actuarial functions, simple variables, "
                "KC options, narrative inline math)"
            ),
            "package_count": len(other),
            "needs_migration_strings": sum(
                row["counts"]["needs_migration"] for row in other
            ),
        },
    }


def render_summary_markdown(payload: dict[str, Any]) -> str:
    totals = payload["totals"]
    wave1 = payload["wave_recommendation"]["wave_1"]
    lines = [
        "# Mathematical Notation Inventory Summary",
        "",
        f"**Generated:** {payload['generated_at']}",
        f"**Standard:** `{payload['standard_ref']}`",
        f"**Content fingerprint:** `{payload['content_fingerprint']}`",
        f"**Live packages scanned:** {payload['live_package_count']}",
        "",
        "## Totals",
        "",
        "| Category | Count |",
        "|---|---:|",
        f"| Mathish strings inventoried | {totals['mathish_strings']} |",
        f"| Already compliant | {totals['already_compliant']} |",
        f"| Needs migration | {totals['needs_migration']} |",
        f"| Migrated (dollar-delimited) | {totals.get('migrated', 0)} |",
        f"| Correctly excluded | {totals['correctly_excluded']} |",
        f"| Needs manual review (flag) | {totals['needs_manual_review']} |",
        f"| Confident automated (no flag) | {totals['confident_automated']} |",
        (
            "| Packages with migration backlog | "
            f"{totals['packages_with_migration_backlog']} |"
        ),
        "",
        "## Limits of automation",
        "",
        payload["limits_of_automation"]["note"],
        "",
        "## Recommended first migration wave (order only)",
        "",
        payload["wave_recommendation"]["principle"],
        "",
        f"**Wave 1:** {wave1['label']} "
        f"({wave1['package_count']} packages, "
        f"{wave1['needs_migration_strings']} needs_migration strings).",
        "",
    ]
    for row in wave1["packages"]:
        lines.append(
            f"- `{row['package_file']}` (`{row['package_id']}`): "
            f"{row['needs_migration']} migrate, "
            f"{row['risk_tier_1_needs_migration']} tier-1, "
            f"{row['needs_manual_review']} manual-review flags"
        )
    lines.extend(
        [
            "",
            "## How to refresh",
            "",
            "```bash",
            "python scripts/inventory_math_notation.py",
            "```",
            "",
            "Ledger JSON: `docs/content/math_notation_inventory.json`.",
            "",
            "## Per-package backlog (top 25 by tier-1 then backlog)",
            "",
        ]
    )
    for row in payload["packages"][:25]:
        c = row["counts"]
        if c["needs_migration"] == 0:
            continue
        lines.append(
            f"- `{row['package_file']}`: backlog {c['needs_migration']} "
            f"(tier-1 {c['risk_tier_1_needs_migration']}, "
            f"manual-review {c['needs_manual_review']}, "
            f"compliant {c['already_compliant']}, "
            f"excluded {c['correctly_excluded']})"
        )
    lines.append("")
    return "\n".join(lines)


def write_inventory(
    catalogue_dir: Path,
    json_out: Path,
    summary_out: Path | None,
) -> dict[str, Any]:
    payload = build_inventory(catalogue_dir)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    if summary_out is not None:
        summary_out.parent.mkdir(parents=True, exist_ok=True)
        summary_out.write_text(render_summary_markdown(payload), encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--catalogue",
        type=Path,
        default=DEFAULT_CATALOGUE,
        help="Directory of educational package JSON files",
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=DEFAULT_JSON_OUT,
        help="Output ledger JSON path",
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=DEFAULT_SUMMARY_OUT,
        help="Output Markdown summary path (use empty string to skip)",
    )
    parser.add_argument(
        "--stdout-totals-only",
        action="store_true",
        help="Print totals JSON to stdout after writing files",
    )
    args = parser.parse_args(argv)

    summary_path: Path | None
    if str(args.summary) == "":
        summary_path = None
    else:
        summary_path = args.summary

    payload = write_inventory(args.catalogue, args.json, summary_path)
    totals = payload["totals"]
    print(
        f"Inventoried {totals['mathish_strings']} mathish strings across "
        f"{payload['live_package_count']} live packages.",
        file=sys.stderr,
    )
    print(
        "already_compliant={already_compliant} "
        "needs_migration={needs_migration} "
        "correctly_excluded={correctly_excluded} "
        "needs_manual_review={needs_manual_review}".format(**totals),
        file=sys.stderr,
    )
    print(f"Wrote {args.json}", file=sys.stderr)
    if summary_path is not None:
        print(f"Wrote {summary_path}", file=sys.stderr)
    if args.stdout_totals_only:
        print(
            json.dumps(
                {
                    "totals": totals,
                    "fingerprint": payload["content_fingerprint"],
                },
                indent=2,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
