"""Educational Intervention Effectiveness Engine — EI Phase 4 (KWP-010).

Answers whether previous educational recommendations improved learning.
Composes with Learning Strategy (WHAT), Diagnostics (WHY), and Difficulty
(Pace) without redesigning those authorities or Evidence / Progress /
Runtime.
"""

from __future__ import annotations

from app.application.intervention_effectiveness.dto import (
    EFFECTIVENESS_VERDICT_LABELS,
    INTERVENTION_KIND_LABELS,
    EffectivenessEvidenceInput,
    EffectivenessVerdict,
    InterventionEffectivenessReport,
    InterventionKind,
    PriorIntervention,
    kind_from_load,
    kind_from_strategy,
    prior_from_enrichment,
    prior_from_sitting,
    resolve_kind,
)
from app.application.intervention_effectiveness.engine import (
    InterventionEffectivenessEngine,
    get_intervention_effectiveness_engine,
)

__all__ = [
    "EFFECTIVENESS_VERDICT_LABELS",
    "INTERVENTION_KIND_LABELS",
    "EffectivenessEvidenceInput",
    "EffectivenessVerdict",
    "InterventionEffectivenessEngine",
    "InterventionEffectivenessReport",
    "InterventionKind",
    "PriorIntervention",
    "get_intervention_effectiveness_engine",
    "kind_from_load",
    "kind_from_strategy",
    "prior_from_enrichment",
    "prior_from_sitting",
    "resolve_kind",
]
