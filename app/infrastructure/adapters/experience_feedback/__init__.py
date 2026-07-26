"""Experience Feedback Loop (P2-MS008).

Surfaces previously observed, non-interpretive Evidence facts back into the
Experience Layer. Display only — no educational adaptation, recommendation
changes, or behavioural optimisation.

Feature flag:
- ``KWALITEC_EXPERIENCE_FEEDBACK`` / ``ENABLE_EXPERIENCE_FEEDBACK``
  (default OFF). Independently controllable from all previous flags.
"""

from __future__ import annotations

from .assembler import (
    ExperienceFeedbackAssembler,
    build_experience_feedback_assembler,
)
from .contracts import (
    AUTHORITY_EXPERIENCE_FEEDBACK,
    CONTRACT_VERSION,
    DEFAULT_SOURCE_DESCRIPTION,
    REPORTING_PERIOD_LABELS,
    REPORTING_PERIOD_THIS_WEEK,
    EvidenceFeedbackReadPort,
    ExperienceFeedback,
    ExperienceFeedbackFact,
    deterministic_feedback_id,
    serialize_canonical,
)
from .reader import (
    REASON_EMPTY,
    REASON_EVIDENCE_REJECTED,
    REASON_EVIDENCE_UNAVAILABLE,
    REASON_FLAG_OFF,
    ExperienceFeedbackReader,
    build_experience_feedback_reader,
)

__all__ = [
    "AUTHORITY_EXPERIENCE_FEEDBACK",
    "CONTRACT_VERSION",
    "DEFAULT_SOURCE_DESCRIPTION",
    "REPORTING_PERIOD_LABELS",
    "REPORTING_PERIOD_THIS_WEEK",
    "REASON_EMPTY",
    "REASON_EVIDENCE_REJECTED",
    "REASON_EVIDENCE_UNAVAILABLE",
    "REASON_FLAG_OFF",
    "EvidenceFeedbackReadPort",
    "ExperienceFeedback",
    "ExperienceFeedbackAssembler",
    "ExperienceFeedbackFact",
    "ExperienceFeedbackReader",
    "build_experience_feedback_assembler",
    "build_experience_feedback_reader",
    "deterministic_feedback_id",
    "serialize_canonical",
]
