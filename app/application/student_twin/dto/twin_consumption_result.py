"""Result of Twin consumption of an Accepted Educational+ Evidence Package."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TwinConsumptionResult:
    """Outcome of one Twin evidence-consumption attempt.

    Twin never evaluates evidence. It reports whether Authority-authorised
    Educational+ observations were applied to Estimated Knowledge / Mastery.
    """

    twin_updated: bool
    reason: str
    twin_id: str | None = None
    learner_id: str | None = None
    package_id: str | None = None
    events_ingested: int = 0
    twin_status: str | None = None
    estimated_knowledge: dict[str, float] | None = None
    estimated_mastery: dict[str, float] | None = None
    overall_knowledge: float | None = None
    overall_mastery: float | None = None

    def to_opaque(self) -> dict[str, Any]:
        return {
            "twin_updated": self.twin_updated,
            "reason": self.reason,
            "twin_id": self.twin_id,
            "learner_id": self.learner_id,
            "package_id": self.package_id,
            "events_ingested": self.events_ingested,
            "twin_status": self.twin_status,
            "estimated_knowledge": dict(self.estimated_knowledge or {}),
            "estimated_mastery": dict(self.estimated_mastery or {}),
            "overall_knowledge": self.overall_knowledge,
            "overall_mastery": self.overall_mastery,
            "authority": "student_digital_twin",
            "evidence_authority": "educational_evidence_authority",
        }

    @classmethod
    def ignored(
        cls,
        reason: str,
        *,
        package_id: str | None = None,
        learner_id: str | None = None,
    ) -> TwinConsumptionResult:
        return cls(
            twin_updated=False,
            reason=reason,
            package_id=package_id,
            learner_id=learner_id,
        )
