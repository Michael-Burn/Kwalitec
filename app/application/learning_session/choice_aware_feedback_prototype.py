"""Phase-0 prototype: choice-aware MCQ feedback for a fixed allowlist.

Proves misconception_tag plumbing and editorial feedback quality on 3–5 live
items before any full-inventory rollout. Correctness matching stays in
``score_practice_response`` / ``_match_mcq``; this module only supplies
student-facing mistake copy and the analytics tag for allowlisted items
(and resolves the tag for logging whenever a selected choice is known).

Do not expand ``PROTOTYPE_ITEM_IDS`` without an explicit editorial review.
"""

from __future__ import annotations

from app.application.learning_session.scoreable_practice import (
    ScoreablePracticeItem,
    _normalise,
    choice_parts,
)

# Live Knowledge Check item_ids only — Batch 1 estimators (numeric),
# Batch 2 GLM, Batch 3 Rho conceptual vignette, Batch 6B revision.
PROTOTYPE_ITEM_IDS: frozenset[str] = frozenset(
    {
        "cs1010-3.1.3-cp-01",  # Batch 1 — efficiency / MSE comparison
        "cs1014-4.2.1-ar-01",  # Batch 2 — exponential-family GLM
        "cs1017-2.1.2-cp-01",  # Batch 3 — Rho continuous waiting times
        "cs1010-ck-r1-cp-01",  # Batch 6B — revision MSE identity
    }
)

# Authored choice-aware mistake text: (item_id, wrong_choice_id) → copy.
# Keys are distractors only; correct choices are never looked up.
PROTOTYPE_CHOICE_FEEDBACK: dict[tuple[str, str], str] = {
    # --- cs1010-3.1.3-cp-01 ---
    (
        "cs1010-3.1.3-cp-01",
        "b",
    ): (
        "That choice treats unbiasedness as an MSE guarantee. "
        "MSE(A)=4/n while MSE(B)=1/n²+1/n≈1/n for large n, so the biased "
        "estimator can win on MSE. Unbiasedness is not optimality."
    ),
    (
        "cs1010-3.1.3-cp-01",
        "c",
    ): (
        "That choice drops Var(B) from the MSE and keeps only bias². "
        "MSE is variance plus squared bias, so MSE(B)=1/n²+1/n, not 1/n² alone."
    ),
    (
        "cs1010-3.1.3-cp-01",
        "d",
    ): (
        "That choice equates consistency with Bias=0 for every finite n. "
        "Consistency is large-sample concentration in probability; a biased "
        "estimator can still be consistent and can still beat an unbiased one "
        "on MSE."
    ),
    # --- cs1014-4.2.1-ar-01 ---
    (
        "cs1014-4.2.1-ar-01",
        "b",
    ): (
        "That choice collapses GLM into renamed OLS. A GLM needs a named "
        "exponential-family response (and a link); package naming alone does "
        "not define the model class."
    ),
    (
        "cs1014-4.2.1-ar-01",
        "c",
    ): (
        "That choice treats Normal as the only GLM response. Poisson and "
        "binomial are standard exponential-family GLM members; Normal with "
        "identity link is a special case inside the family list, not the "
        "whole definition."
    ),
    (
        "cs1014-4.2.1-ar-01",
        "d",
    ): (
        "That choice treats any exp() in a density as exponential-family "
        "membership. Family membership is a specific exponential-family "
        "structure for named responses, not the mere presence of an "
        "exponential symbol."
    ),
    # --- cs1017-2.1.2-cp-01 ---
    (
        "cs1017-2.1.2-cp-01",
        "b",
    ): (
        "That choice misuses the CLT to force Normal waiting times. The CLT "
        "is about sample means for large n, not a licence to ignore strictly "
        "positive, memoryless waiting-time support—which points first to "
        "exponential."
    ),
    (
        "cs1017-2.1.2-cp-01",
        "c",
    ): (
        "That choice forces a Beta model because times are 'between zero and "
        "one.' Waiting times here are unbounded positive durations under "
        "constant hazard; Beta support on (0,1) does not match that story."
    ),
    (
        "cs1017-2.1.2-cp-01",
        "d",
    ): (
        "That choice wrongly bans lognormal for every waiting-time problem "
        "and ties memorylessness to discrete data. Memoryless continuous "
        "waiting under constant hazard selects exponential first; lognormal "
        "is a different positive-support model, not ruled out by a "
        "discrete-data claim."
    ),
    # --- cs1010-ck-r1-cp-01 ---
    (
        "cs1010-ck-r1-cp-01",
        "b",
    ): (
        "That choice adds Bias(T) without squaring. MSE is variance plus "
        "squared bias, so the bias term must be Bias(T)²."
    ),
    (
        "cs1010-ck-r1-cp-01",
        "c",
    ): (
        "That choice keeps only Bias(T)² and drops variance. An estimator's "
        "MSE always includes both Var(T) and Bias(T)²."
    ),
    (
        "cs1010-ck-r1-cp-01",
        "d",
    ): (
        "That choice sets MSE equal to variance for every estimator. That "
        "holds only when bias is zero; in general MSE = Var(T) + Bias(T)²."
    ),
}


def find_selected_choice(
    item: ScoreablePracticeItem,
    response: str,
) -> tuple[str, str, str] | None:
    """Locate the learner's selected MCQ choice by id or label."""
    raw = (response or "").strip()
    if not raw or not item.choices:
        return None
    normalised = _normalise(raw, case_sensitive=False)
    for choice in item.choices:
        cid, label, tag = choice_parts(choice)
        if normalised in {
            _normalise(cid, case_sensitive=False),
            _normalise(label, case_sensitive=False),
        }:
            return cid, label, tag
    return None


def assemble_choice_aware_mistake(
    item: ScoreablePracticeItem,
    response: str,
    *,
    correct: bool,
) -> tuple[str, str]:
    """Return (student-facing common_mistake, misconception_tag for logging).

    Correct answers: empty mistake text and empty tag.
    Non-prototype items: existing bundled ``item.common_mistake``; tag still
    resolved from the selected choice when available (analytics plumbing).
    Prototype items: authored choice-specific copy when the selected
    distractor is mapped; otherwise fall back to the bundled common_mistake.
    """
    if correct:
        return "", ""
    selected = find_selected_choice(item, response)
    tag = selected[2] if selected else ""
    if item.item_id in PROTOTYPE_ITEM_IDS and selected is not None:
        authored = PROTOTYPE_CHOICE_FEEDBACK.get((item.item_id, selected[0]))
        if authored:
            return authored, tag
    return item.common_mistake, tag
