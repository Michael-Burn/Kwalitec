"""Experience Feedback reader — Evidence read → ExperienceFeedback (P2-MS008).

Integrates only through Evidence's public query/read interface.
"""

from __future__ import annotations

import logging
from typing import Any

from app.infrastructure.adapters.evidence_platform.contracts import (
    EvidenceFactualSummary,
    EvidenceResult,
)
from app.infrastructure.adapters.experience_feedback.assembler import (
    ExperienceFeedbackAssembler,
)
from app.infrastructure.adapters.experience_feedback.contracts import (
    DEFAULT_SOURCE_DESCRIPTION,
    EvidenceFeedbackReadPort,
    ExperienceFeedback,
)

logger = logging.getLogger(__name__)

REASON_FLAG_OFF = "experience_feedback_flag_off"
REASON_EVIDENCE_UNAVAILABLE = "evidence_read_unavailable"
REASON_EVIDENCE_REJECTED = "evidence_read_rejected"
REASON_EMPTY = "evidence_summary_empty"


class ExperienceFeedbackReader:
    """Load factual ExperienceFeedback via Evidence public read only.

    Never accesses repositories, never calculates educational metrics, never
    mutates recommendations / Runtime A / Twin / Adaptive / Strategy.
    """

    READER_ID = "experience_feedback_reader"
    READER_VERSION = "1.0.0-p2.ms008"

    def __init__(
        self,
        *,
        enabled: bool = True,
        evidence: EvidenceFeedbackReadPort | None = None,
        assembler: ExperienceFeedbackAssembler | None = None,
    ) -> None:
        self._enabled = bool(enabled)
        self._evidence = evidence
        self._assembler = assembler or ExperienceFeedbackAssembler()

    @property
    def reader_id(self) -> str:
        return self.READER_ID

    @property
    def reader_version(self) -> str:
        return self.READER_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    @property
    def evidence(self) -> EvidenceFeedbackReadPort | None:
        return self._evidence

    def load(
        self,
        student_id: str,
        *,
        reporting_period: str = "this_week",
        as_of: str | None = None,
        evidence_records: Any = None,
    ) -> ExperienceFeedback | None:
        """Return ExperienceFeedback or None when gated / unavailable."""
        if not self._enabled:
            return None
        sid = (student_id or "").strip()
        if not sid:
            return None
        if self._evidence is None:
            logger.debug(
                "experience_feedback_skip reason=%s student_id=%s",
                REASON_EVIDENCE_UNAVAILABLE,
                sid,
            )
            return None
        try:
            result = self._evidence.query_factual_summary(
                sid,
                reporting_period=reporting_period,
                as_of=as_of,
                evidence_records=evidence_records,
            )
        except Exception:
            logger.warning(
                "experience_feedback_failed reason=%s student_id=%s",
                REASON_EVIDENCE_REJECTED,
                sid,
                exc_info=True,
            )
            return None
        if not isinstance(result, EvidenceResult) or not result.ok:
            message = getattr(result, "message", None) if result is not None else None
            logger.debug(
                "experience_feedback_skip reason=%s student_id=%s message=%s",
                REASON_EVIDENCE_REJECTED,
                sid,
                message,
            )
            return None
        summary = result.value
        if not isinstance(summary, EvidenceFactualSummary):
            logger.debug(
                "experience_feedback_skip reason=%s student_id=%s",
                REASON_EMPTY,
                sid,
            )
            return None
        try:
            return self._assembler.assemble(summary, generated_at=as_of)
        except (TypeError, ValueError) as exc:
            logger.warning(
                "experience_feedback_assemble_failed student_id=%s error=%s",
                sid,
                exc,
            )
            return None


def build_experience_feedback_reader(
    *,
    enabled: bool,
    evidence: EvidenceFeedbackReadPort | None = None,
    assembler: ExperienceFeedbackAssembler | None = None,
) -> ExperienceFeedbackReader | None:
    """DI helper — construct reader only when ENABLE_EXPERIENCE_FEEDBACK is ON."""
    if not enabled:
        return None
    return ExperienceFeedbackReader(
        enabled=True,
        evidence=evidence,
        assembler=assembler or ExperienceFeedbackAssembler(),
    )


__all__ = [
    "DEFAULT_SOURCE_DESCRIPTION",
    "REASON_EMPTY",
    "REASON_EVIDENCE_REJECTED",
    "REASON_EVIDENCE_UNAVAILABLE",
    "REASON_FLAG_OFF",
    "ExperienceFeedbackReader",
    "build_experience_feedback_reader",
]
