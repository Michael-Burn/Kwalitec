"""Adaptive Engine Executor (MS-003 A2).

Deterministic AdaptiveInputBundle → AdaptiveOutputBundle evaluation.
Pure snapshot compute — no Runtime A writes, no Experience side effects,
no RecommendationService / Planning calls, no wall-clock dependence.
"""

from __future__ import annotations

import hashlib
from typing import Any

from app.infrastructure.adapters.adaptive_engine.contracts import (
    AUTHORITY_ADAPTIVE_ENGINE,
    AdaptiveInputBundle,
    AdaptiveOutputBundle,
    ConfidencePlaceholder,
    EvidenceRef,
    ExplanationBundle,
    RecommendationPlaceholder,
    RuleRef,
    TopicRef,
)
from app.infrastructure.adapters.adaptive_engine.provenance import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    FIELD_CURRICULUM,
    FIELD_MISSION,
    FIELD_READINESS,
    FIELD_TWIN,
    INPUT_FIELD_NAMES,
)

# Registered deterministic rule ids (ADAPTIVE_EXPLAINABILITY.md).
RULE_MISSION_ALIGNED = "adaptive.shadow.mission_aligned"
RULE_NEXT_INCOMPLETE_LEAF = "adaptive.shadow.next_incomplete_leaf"
RULE_WEAK_TOPIC_PRIORITY = "adaptive.shadow.weak_topic_priority"
RULE_SPARSE_FALLBACK = "adaptive.shadow.sparse_evidence"

RULE_VERSION = "1.0.0-a2"

DECISION_NEXT_FOCUS = "NEXT_FOCUS"
DECISION_REVISION_SET = "REVISION_SET"
DECISION_COMPOSITE = "COMPOSITE"

# Assembler normalizes lifecycle to lowercase ("revision"); accept any case.
LIFECYCLE_REVISION = "revision"


class AdaptiveEngineExecutor:
    """Deterministic Adaptive Decision compute for shadow / later cutover.

    Identical AdaptiveInputBundles → identical AdaptiveOutputBundles.
    Must not mutate Runtime A or Experience state.
    """

    EXECUTOR_ID = "adaptive_engine_executor"
    EXECUTOR_VERSION = RULE_VERSION

    def evaluate(self, inputs: AdaptiveInputBundle) -> AdaptiveOutputBundle:
        """Evaluate an AdaptiveInputBundle into an AdaptiveOutputBundle."""
        if not isinstance(inputs, AdaptiveInputBundle):
            raise TypeError("inputs must be an AdaptiveInputBundle")

        used, unavailable = _partition_inputs(inputs)
        evidence_refs = _build_evidence_refs(inputs)
        primary, alternatives, rule_id, reason_codes, mission_aligned, mission_note = (
            _select_recommendation(inputs)
        )

        confidence = _compute_confidence(
            inputs,
            used=used,
            unavailable=unavailable,
            evidence_refs=evidence_refs,
            primary=primary,
        )
        explanation = _build_explanation(
            inputs=inputs,
            used=used,
            unavailable=unavailable,
            evidence_refs=evidence_refs,
            primary=primary,
            alternatives=alternatives,
            rule_id=rule_id,
            reason_codes=reason_codes,
            confidence=confidence,
            mission_aligned=mission_aligned,
            mission_note=mission_note,
        )
        recommendation = RecommendationPlaceholder(
            topic_code=primary.get("topic_code"),
            title=primary.get("title"),
            decision_kind=str(primary.get("decision_kind") or ""),
            label=str(primary.get("label") or primary.get("title") or ""),
        )
        return AdaptiveOutputBundle(
            recommendation=recommendation,
            confidence=confidence,
            explanation=explanation,
            decision_id=_deterministic_decision_id(inputs),
            authority=AUTHORITY_ADAPTIVE_ENGINE,
        )


def build_adaptive_engine_executor(*, enabled: bool) -> AdaptiveEngineExecutor | None:
    """DI helper — construct executor only when adaptive compute is enabled."""
    if not enabled:
        return None
    return AdaptiveEngineExecutor()


def _deterministic_decision_id(inputs: AdaptiveInputBundle) -> str:
    digest = hashlib.sha256(inputs.serialize().encode("utf-8")).hexdigest()[:16]
    return f"a2-{digest}"


def _partition_inputs(
    inputs: AdaptiveInputBundle,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    used: list[str] = []
    unavailable: list[str] = []
    names = list(INPUT_FIELD_NAMES)
    # Twin is optional enrichment — include only when provenance was attached.
    if FIELD_TWIN in inputs.field_provenance:
        names.append(FIELD_TWIN)
    for name in names:
        prov = inputs.field_provenance.get(name)
        availability = ""
        if prov is None:
            unavailable.append(name)
            continue
        if hasattr(prov, "get"):
            availability = str(prov.get("availability") or "")
        else:
            availability = str(getattr(prov, "availability", "") or "")
        if availability == AVAILABILITY_UNAVAILABLE:
            unavailable.append(name)
        elif availability == AVAILABILITY_AVAILABLE:
            used.append(name)
        else:
            # Missing / unknown availability treated as unavailable.
            unavailable.append(name)
    return tuple(used), tuple(unavailable)


def _build_evidence_refs(inputs: AdaptiveInputBundle) -> tuple[EvidenceRef, ...]:
    refs: list[EvidenceRef] = []
    evidence = dict(inputs.evidence or {})
    attempts = list(evidence.get("attempts") or [])
    for row in attempts[:10]:
        if not isinstance(row, dict):
            continue
        attempt_id = str(row.get("attempt_id") or "").strip()
        if not attempt_id:
            continue
        refs.append(
            EvidenceRef(
                kind="attempt",
                id=attempt_id,
                observed_at=str(row.get("study_date") or "") or None,
                note="authorised"
                if row.get("authorised_structured_results")
                else "observed",
            )
        )
    today = (dict(inputs.mission or {})).get("today")
    if isinstance(today, dict):
        mission_id = str(today.get("mission_id") or "").strip()
        if mission_id:
            refs.append(
                EvidenceRef(
                    kind="mission",
                    id=mission_id,
                    observed_at=str(today.get("mission_date") or "") or None,
                    note="today_mission",
                )
            )
    for row in list(inputs.topic_progress or ())[:5]:
        topic_id = str(row.get("topic_id") or "").strip()
        if not topic_id:
            continue
        refs.append(
            EvidenceRef(
                kind="topic_progress",
                id=topic_id,
                observed_at=str(row.get("last_reviewed") or "") or None,
                note="mastery_signal",
            )
        )
    # Optional Twin attachment ref (MS-004 T4) — consume-only lineage.
    twin = dict(inputs.twin or {})
    twin_ref = str(twin.get("twin_snapshot_ref") or "").strip()
    if twin_ref and str(twin.get("availability") or "") == AVAILABILITY_AVAILABLE:
        refs.append(
            EvidenceRef(
                kind="twin_snapshot",
                id=twin_ref,
                observed_at=str(twin.get("as_of") or "") or None,
                note="twin_enrichment",
            )
        )
    return tuple(refs)


def _select_recommendation(
    inputs: AdaptiveInputBundle,
) -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
    str,
    tuple[str, ...],
    bool | None,
    str,
]:
    """Select primary recommendation from snapshot signals only."""
    today = (dict(inputs.mission or {})).get("today")
    if isinstance(today, dict):
        title = str(today.get("title") or "").strip()
        mission_id = str(today.get("mission_id") or "").strip()
        if title:
            # Mission-alignment policy (MS-001): primary follows today's mission.
            alt = _next_incomplete_leaf(inputs) or _weakest_topic(inputs)
            alternatives: list[dict[str, Any]] = []
            if alt and (
                alt.get("topic_code") != mission_id
                and alt.get("title") != title
            ):
                alternatives.append({**alt, "role": "alternative"})
            primary = {
                "topic_code": None,
                "title": title,
                "label": title,
                "decision_kind": DECISION_COMPOSITE,
                "role": "primary",
            }
            return (
                primary,
                alternatives,
                RULE_MISSION_ALIGNED,
                ("mission_aligned", "today_mission"),
                True,
                "Tonight's session follows your mission; adaptive advice agrees.",
            )

    stage = (inputs.lifecycle_stage or "").strip().lower()
    if stage == LIFECYCLE_REVISION:
        weak = _weakest_topic(inputs)
        if weak:
            alts = [
                {**row, "role": "alternative"}
                for row in _weak_topic_candidates(inputs)[1:3]
            ]
            return (
                {**weak, "decision_kind": DECISION_REVISION_SET, "role": "primary"},
                alts,
                RULE_WEAK_TOPIC_PRIORITY,
                ("revision_lifecycle", "weak_topic_priority"),
                False,
                "",
            )

    nxt = _next_incomplete_leaf(inputs)
    if nxt:
        weak = _weakest_topic(inputs)
        alts: list[dict[str, Any]] = []
        if weak and weak.get("topic_code") != nxt.get("topic_code"):
            alts.append({**weak, "role": "alternative"})
        return (
            {**nxt, "decision_kind": DECISION_NEXT_FOCUS, "role": "primary"},
            alts,
            RULE_NEXT_INCOMPLETE_LEAF,
            ("curriculum_progression", "next_incomplete_leaf"),
            False,
            "",
        )

    weak = _weakest_topic(inputs)
    if weak:
        return (
            {**weak, "decision_kind": DECISION_REVISION_SET, "role": "primary"},
            [],
            RULE_WEAK_TOPIC_PRIORITY,
            ("weak_topic_priority",),
            False,
            "",
        )

    return (
        {
            "topic_code": None,
            "title": None,
            "label": "",
            "decision_kind": "",
            "role": "primary",
        },
        [],
        RULE_SPARSE_FALLBACK,
        ("sparse_evidence", "no_candidate"),
        None,
        "",
    )


def _next_incomplete_leaf(inputs: AdaptiveInputBundle) -> dict[str, Any] | None:
    curriculum = dict(inputs.curriculum or {})
    leaves = list(curriculum.get("leaves") or [])
    if not leaves:
        return None
    completed_ids = {
        str(row.get("topic_id") or "")
        for row in inputs.topic_progress or ()
        if bool(row.get("completed"))
    }
    for leaf in leaves:
        if not isinstance(leaf, dict):
            continue
        topic_id = str(leaf.get("topic_id") or "").strip()
        if not topic_id or topic_id in completed_ids:
            continue
        title = str(leaf.get("topic_name") or "").strip() or topic_id
        return {
            "topic_code": topic_id,
            "title": title,
            "label": title,
        }
    return None


def _weak_topic_candidates(inputs: AdaptiveInputBundle) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in inputs.topic_progress or ():
        topic_id = str(row.get("topic_id") or "").strip()
        if not topic_id:
            continue
        # Prefer completed / practised topics with lower mastery for revision.
        if not bool(row.get("completed")) and row.get("mastery_score") is None:
            continue
        title = str(row.get("topic_name") or "").strip() or topic_id
        mastery = float(row.get("mastery_score") or 0.0)
        rows.append(
            {
                "topic_code": topic_id,
                "title": title,
                "label": title,
                "mastery_score": mastery,
            }
        )
    rows.sort(key=lambda r: (float(r["mastery_score"]), str(r["topic_code"])))
    return rows


def _weakest_topic(inputs: AdaptiveInputBundle) -> dict[str, Any] | None:
    candidates = _weak_topic_candidates(inputs)
    if not candidates:
        return None
    best = candidates[0]
    return {
        "topic_code": best["topic_code"],
        "title": best["title"],
        "label": best["label"],
    }


def _compute_confidence(
    inputs: AdaptiveInputBundle,
    *,
    used: tuple[str, ...],
    unavailable: tuple[str, ...],
    evidence_refs: tuple[EvidenceRef, ...],
    primary: dict[str, Any],
) -> ConfidencePlaceholder:
    attempt_count = int((dict(inputs.evidence or {})).get("attempt_count") or 0)
    has_primary = bool(primary.get("title") or primary.get("topic_code"))
    if not has_primary:
        return ConfidencePlaceholder(
            score=0.1,
            band="low",
            rationale="No candidate topic or mission signal in the input snapshot.",
        )
    if len(unavailable) >= 4 or attempt_count == 0:
        return ConfidencePlaceholder(
            score=0.25,
            band="low",
            rationale="Sparse evidence or several input fields unavailable.",
        )
    if (
        FIELD_MISSION in used
        and isinstance((dict(inputs.mission or {})).get("today"), dict)
        and attempt_count >= 3
    ):
        return ConfidencePlaceholder(
            score=0.85,
            band="high",
            rationale="Today's mission present with recent attempt evidence.",
        )
    if evidence_refs and FIELD_CURRICULUM in used:
        return ConfidencePlaceholder(
            score=0.6,
            band="medium",
            rationale="Curriculum and evidence signals available; partial coverage.",
        )
    return ConfidencePlaceholder(
        score=0.4,
        band="medium",
        rationale="Partial snapshot signals available for a deterministic choice.",
    )


def _build_explanation(
    *,
    inputs: AdaptiveInputBundle,
    used: tuple[str, ...],
    unavailable: tuple[str, ...],
    evidence_refs: tuple[EvidenceRef, ...],
    primary: dict[str, Any],
    alternatives: list[dict[str, Any]],
    rule_id: str,
    reason_codes: tuple[str, ...],
    confidence: ConfidencePlaceholder,
    mission_aligned: bool | None,
    mission_note: str,
) -> ExplanationBundle:
    title = str(primary.get("title") or primary.get("label") or "").strip()
    topic_code = primary.get("topic_code")
    topic_refs: list[TopicRef] = []
    if title or topic_code:
        topic_refs.append(
            TopicRef(
                topic_code=str(topic_code or ""),
                title=title,
                role="primary",
            )
        )
    for alt in alternatives:
        topic_refs.append(
            TopicRef(
                topic_code=str(alt.get("topic_code") or ""),
                title=str(alt.get("title") or ""),
                role=str(alt.get("role") or "alternative"),
            )
        )

    rule_description = {
        RULE_MISSION_ALIGNED: "Align primary recommendation to today's mission",
        RULE_NEXT_INCOMPLETE_LEAF: "Select next incomplete curriculum leaf",
        RULE_WEAK_TOPIC_PRIORITY: "Prioritise lowest-mastery practised topic",
        RULE_SPARSE_FALLBACK: "No candidate — sparse or unavailable inputs",
    }.get(rule_id, "Adaptive shadow deterministic rule")

    limitations: list[str] = []
    if not evidence_refs:
        limitations.append("sparse_evidence")
    if unavailable:
        limitations.append("inputs_unavailable")
    if not title and not topic_code:
        limitations.append("no_candidate")
    if FIELD_READINESS in unavailable:
        limitations.append("stale_or_missing_readiness")

    if title:
        why_summary = f"Recommend focusing on {title} based on snapshot signals."
        rationale = (
            f"Selected via {rule_id}: {rule_description}. "
            f"Inputs used: {', '.join(used) or 'none'}."
        )
    else:
        why_summary = (
            "No adaptive primary recommendation could be derived from the snapshot."
        )
        rationale = (
            "Sparse or unavailable inputs prevented a topic or mission selection."
        )

    alt_rationale = ""
    if alternatives:
        names = ", ".join(
            str(a.get("title") or a.get("topic_code") or "") for a in alternatives
        )
        alt_rationale = (
            f"Considered alternative(s) {names} but selected primary by {rule_id}."
        )
    elif title:
        alt_rationale = "No competing alternatives ranked above the primary signal."

    limitations_summary = ""
    if limitations:
        limitations_summary = (
            "Decision bounds: "
            + "; ".join(limitations)
            + ". Does not mutate Runtime A or Experience."
        )

    input_summary = (
        f"student_id={inputs.student_id}; as_of={inputs.as_of or ''}; "
        f"used=[{','.join(used)}]; unavailable=[{','.join(unavailable)}]"
    )

    return ExplanationBundle(
        evidence_refs=evidence_refs,
        rule_refs=(
            RuleRef(
                rule_or_model_id=rule_id,
                version=RULE_VERSION,
                description=rule_description,
            ),
        ),
        confidence=confidence,
        input_summary=input_summary,
        recommendation_rationale=rationale,
        why_summary=why_summary,
        why_reason_codes=reason_codes,
        topic_refs=tuple(topic_refs),
        alternatives_rationale=alt_rationale,
        limitations_codes=tuple(limitations),
        limitations_summary=limitations_summary,
        mission_aligned=mission_aligned,
        mission_note=mission_note,
        inputs_used=used,
        inputs_unavailable=unavailable,
    )
