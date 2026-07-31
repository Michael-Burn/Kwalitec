"""Educational yield metrics for Founder observability (KWP-004).

Summarises Accepted Educational+ vs Behavioural sittings from persisted
Evidence Packages. Does not change Evidence Authority, Twin, or Progress.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.application.learning_session.dto.candidate_observation import (
    RuntimeEvidenceType,
)
from app.application.learning_session.dto.evidence_package import (
    EvidenceDisposition,
)

_EDUCATIONAL_TYPES = frozenset(
    {
        RuntimeEvidenceType.PRACTICE_CORRECT.value,
        RuntimeEvidenceType.PRACTICE_INCORRECT.value,
        RuntimeEvidenceType.STRUCTURED_QUESTION_RESULTS.value,
    }
)
_BEHAVIOURAL_PRACTICE = frozenset(
    {
        RuntimeEvidenceType.PRACTICE_ATTEMPTED.value,
        RuntimeEvidenceType.PRACTICE_PARTIAL_UNSCORED.value,
    }
)


@dataclass(frozen=True)
class EducationalYieldSnapshot:
    """Founder-facing Educational+ density metrics."""

    sittings_total: int = 0
    educational_plus_accepted: int = 0
    behavioural_only: int = 0
    restricted: int = 0
    rejected: int = 0
    educational_plus_rate: float = 0.0
    behavioural_rate: float = 0.0
    educational_observations: int = 0
    behavioural_practice_observations: int = 0
    learning_yield: float = 0.0
    first_twin_activation_sittings: int = 0
    twin_updated_sittings: int = 0
    # KWP-005 — sitting product signals (presentation analytics only).
    finish_review_yes: int = 0
    finish_review_partial: int = 0
    finish_review_no: int = 0
    reflection_submitted: int = 0
    reflection_rate: float = 0.0
    average_observation_density: float = 0.0

    def to_opaque(self) -> dict[str, Any]:
        return {
            "sittings_total": self.sittings_total,
            "educational_plus_accepted": self.educational_plus_accepted,
            "behavioural_only": self.behavioural_only,
            "restricted": self.restricted,
            "rejected": self.rejected,
            "educational_plus_rate": round(self.educational_plus_rate, 4),
            "behavioural_rate": round(self.behavioural_rate, 4),
            "educational_observations": self.educational_observations,
            "behavioural_practice_observations": (
                self.behavioural_practice_observations
            ),
            "learning_yield": round(self.learning_yield, 4),
            "first_twin_activation_sittings": self.first_twin_activation_sittings,
            "twin_updated_sittings": self.twin_updated_sittings,
            "finish_review_yes": self.finish_review_yes,
            "finish_review_partial": self.finish_review_partial,
            "finish_review_no": self.finish_review_no,
            "reflection_submitted": self.reflection_submitted,
            "reflection_rate": round(self.reflection_rate, 4),
            "average_observation_density": round(
                self.average_observation_density, 4
            ),
        }


class EducationalYieldMetrics:
    """Compute Learning Yield from persisted sitting Evidence Packages."""

    @staticmethod
    def from_packages(
        packages: list[dict[str, Any]] | tuple[dict[str, Any], ...],
    ) -> EducationalYieldSnapshot:
        total = 0
        edu_accepted = 0
        behavioural_only = 0
        restricted = 0
        rejected = 0
        edu_obs = 0
        behavioural_obs = 0
        twin_updated = 0
        twin_first = 0
        finish_yes = 0
        finish_partial = 0
        finish_no = 0
        reflection_n = 0
        observation_total = 0

        for raw in packages:
            if not isinstance(raw, dict):
                continue
            total += 1
            validation = raw.get("validation") or {}
            disposition = str(
                validation.get("disposition") or raw.get("disposition") or ""
            ).strip()
            type_ids = _observation_type_ids(raw)
            edu_count = len(type_ids & _EDUCATIONAL_TYPES)
            beh_count = len(type_ids & _BEHAVIOURAL_PRACTICE)
            edu_obs += edu_count
            behavioural_obs += beh_count
            observation_total += len(type_ids)

            may_update_twin = bool(validation.get("may_update_twin"))
            twin_status = str(
                (raw.get("twin_consumption") or {}).get("twin_status")
                or raw.get("twin_status")
                or ""
            ).strip().lower()
            if may_update_twin or twin_status == "active":
                twin_updated += 1
            if twin_status in {"active", "activated"} and edu_count:
                twin_first += 1

            verdict = str(
                raw.get("finish_review_verdict")
                or (raw.get("finish_review") or {}).get("verdict")
                or ""
            ).strip().lower()
            if (
                verdict == "yes"
                or RuntimeEvidenceType.FINISH_REVIEW_YES.value in type_ids
            ):
                finish_yes += 1
            elif (
                verdict == "partially"
                or RuntimeEvidenceType.FINISH_REVIEW_PARTIALLY.value in type_ids
            ):
                finish_partial += 1
            elif (
                verdict == "no"
                or RuntimeEvidenceType.FINISH_REVIEW_NO.value in type_ids
            ):
                finish_no += 1
            if RuntimeEvidenceType.REFLECTION_SUBMITTED.value in type_ids:
                reflection_n += 1

            if disposition == EvidenceDisposition.ACCEPTED.value:
                if edu_count or bool(validation.get("may_update_twin")):
                    edu_accepted += 1
                else:
                    behavioural_only += 1
            elif disposition == EvidenceDisposition.ACCEPTED_WITH_RESTRICTIONS.value:
                restricted += 1
                if edu_count == 0:
                    behavioural_only += 1
            elif disposition == EvidenceDisposition.REJECTED.value:
                rejected += 1
            elif edu_count:
                edu_accepted += 1
            else:
                behavioural_only += 1

        rate = (edu_accepted / total) if total else 0.0
        beh_rate = (behavioural_only / total) if total else 0.0
        yield_per = (edu_obs / total) if total else 0.0
        reflection_rate = (reflection_n / total) if total else 0.0
        density = (observation_total / total) if total else 0.0
        return EducationalYieldSnapshot(
            sittings_total=total,
            educational_plus_accepted=edu_accepted,
            behavioural_only=behavioural_only,
            restricted=restricted,
            rejected=rejected,
            educational_plus_rate=rate,
            behavioural_rate=beh_rate,
            educational_observations=edu_obs,
            behavioural_practice_observations=behavioural_obs,
            learning_yield=yield_per,
            first_twin_activation_sittings=twin_first,
            twin_updated_sittings=twin_updated,
            finish_review_yes=finish_yes,
            finish_review_partial=finish_partial,
            finish_review_no=finish_no,
            reflection_submitted=reflection_n,
            reflection_rate=reflection_rate,
            average_observation_density=density,
        )

    @classmethod
    def from_store(cls, store: Any) -> EducationalYieldSnapshot:
        """Scan a SessionDocumentStore for ``lsr.evidence_package`` rows."""
        packages = list_evidence_packages(store)
        return cls.from_packages(packages)


def list_evidence_packages(store: Any) -> list[dict[str, Any]]:
    """Best-effort list of persisted Evidence Packages from a document store."""
    if store is None:
        return []
    namespace = "lsr.evidence_package"
    if hasattr(store, "list_documents"):
        docs = store.list_documents(namespace)
        return [d for d in docs if isinstance(d, dict)]
    docs_map = getattr(store, "_docs", None)
    if isinstance(docs_map, dict):
        return [
            dict(doc)
            for (ns, _key), doc in docs_map.items()
            if ns == namespace and isinstance(doc, dict)
        ]
    return []


def _observation_type_ids(package: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for obs in package.get("observations") or ():
        if isinstance(obs, dict) and obs.get("type_id"):
            ids.add(str(obs["type_id"]))
    # Also honour precomputed type lists when present.
    for tid in package.get("observation_type_ids") or ():
        ids.add(str(tid))
    return ids
