"""Legacy Stack C (SDT SQL) founder diagnostic sandbox labelling.

ADR-027 Phase 2 Stage 3 (design section 6 + accepted resolution #3):

Founder surfaces under /founder/twin, /founder/reasoning, /founder/assessment,
/founder/tutor, /founder/missions, and /founder/learning-graph that still
exercise the Epic-2 SDT SQL / DecisionGenerator sandbox must carry an explicit
non-authority banner. Sandbox mastery is never student-facing Estimated
Knowledge.

Retention lifetime (resolution #3): retain through Phase 2 implementation plus
one subsequent review cycle, then remove unless a separate initiative
explicitly claims the sandbox going forward. Also recorded in
docs/production/VERSION_1_FLAG_MATRIX.md.
"""

from __future__ import annotations

from typing import Any

# Visible on every labelled founder JSON response.
STACK_C_SANDBOX_LABEL = (
    "LEGACY SDT SQL DIAGNOSTIC SANDBOX — not student-facing Estimated Knowledge. "
    "Canonical EK lives on the Learner Twin (Stack B) via LearnerTwinQueryPort. "
    "Retention: Phase 2 implementation + one subsequent review cycle, then "
    "remove unless a separate initiative claims this sandbox."
)

STACK_C_SANDBOX_META: dict[str, Any] = {
    "legacy_sdt_sandbox": True,
    "ek_authority": "not_authoritative",
    "sandbox_label": STACK_C_SANDBOX_LABEL,
    "sandbox_retention": (
        "phase2_implementation_plus_one_review_cycle_then_remove_unless_claimed"
    ),
    "canonical_ek_source": "learner_twin_query_port",
}


def with_stack_c_sandbox_label(payload: dict[str, Any]) -> dict[str, Any]:
    """Merge the Stack C sandbox notice into a founder JSON payload."""
    labelled = dict(payload)
    labelled.update(STACK_C_SANDBOX_META)
    return labelled


def sandbox_jsonify(payload: dict[str, Any], status: int | None = None):
    """jsonify a founder payload with the Stack C sandbox notice attached."""
    from flask import jsonify

    body = jsonify(with_stack_c_sandbox_label(payload))
    if status is None:
        return body
    return body, status
