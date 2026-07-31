"""Session Evidence Package — one sitting under EV-001A / EV-001B.

LearningSessionRuntime emits candidates; EducationalEvidenceAuthority
validates the package. This DTO carries provenance and validation results.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from app.application.learning_session.dto.candidate_observation import (
    CandidateObservation,
)


class EvidenceDisposition(StrEnum):
    """Authority outcome for a sitting package (EV-001B)."""

    ACCEPTED = "accepted"
    ACCEPTED_WITH_RESTRICTIONS = "accepted_with_restrictions"
    REJECTED = "rejected"


class EvidenceLifecycleState(StrEnum):
    """EV-001A lifecycle states applicable to a package."""

    GENERATED = "generated"
    VALIDATED = "validated"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    PERSISTED = "persisted"
    CONSUMED = "consumed"
    ARCHIVED = "archived"


EVIDENCE_PACKAGE_CONTRACT = "EV-001A"
EVIDENCE_PACKAGE_VERSION = "1.0"


@dataclass(frozen=True)
class EvidenceValidationResult:
    """Authority decision for one Evidence Package."""

    disposition: EvidenceDisposition
    lifecycle_state: EvidenceLifecycleState
    may_complete_session: bool
    may_complete_mission: bool
    may_advance_progress: bool
    may_update_twin: bool
    reason: str
    student_explanation: str
    restrictions: tuple[str, ...] = ()
    highest_grade: str = "informational"
    validated_at: datetime | None = None

    def to_opaque(self) -> dict[str, Any]:
        return {
            "disposition": self.disposition.value,
            "lifecycle_state": self.lifecycle_state.value,
            "may_complete_session": self.may_complete_session,
            "may_complete_mission": self.may_complete_mission,
            "may_advance_progress": self.may_advance_progress,
            "may_update_twin": self.may_update_twin,
            "reason": self.reason,
            "student_explanation": self.student_explanation,
            "restrictions": list(self.restrictions),
            "highest_grade": self.highest_grade,
            "validated_at": (
                self.validated_at.isoformat() if self.validated_at else None
            ),
        }

    @classmethod
    def from_opaque(cls, raw: dict[str, Any] | None) -> EvidenceValidationResult | None:
        if not isinstance(raw, dict) or not raw.get("disposition"):
            return None
        validated = raw.get("validated_at")
        validated_at = None
        if isinstance(validated, str):
            try:
                validated_at = datetime.fromisoformat(validated)
            except ValueError:
                validated_at = None
        return cls(
            disposition=EvidenceDisposition(str(raw["disposition"])),
            lifecycle_state=EvidenceLifecycleState(
                str(
                    raw.get("lifecycle_state")
                    or EvidenceLifecycleState.VALIDATED.value
                )
            ),
            may_complete_session=bool(raw.get("may_complete_session")),
            may_complete_mission=bool(raw.get("may_complete_mission")),
            may_advance_progress=bool(raw.get("may_advance_progress")),
            may_update_twin=bool(raw.get("may_update_twin")),
            reason=str(raw.get("reason") or ""),
            student_explanation=str(raw.get("student_explanation") or ""),
            restrictions=tuple(str(r) for r in (raw.get("restrictions") or ())),
            highest_grade=str(raw.get("highest_grade") or "informational"),
            validated_at=validated_at,
        )


@dataclass(frozen=True)
class SessionEvidencePackage:
    """Single Evidence Package representing one Study Session sitting."""

    package_id: str
    student_id: str
    session_id: str
    mission_instance_id: str
    topic_id: str
    topic_title: str
    curriculum_identity: str
    learning_objectives: tuple[str, ...]
    observations: tuple[CandidateObservation, ...]
    finish_review_verdict: str | None
    finish_review_notes: str | None
    session_metadata: dict[str, Any]
    provenance: str
    contract_version: str
    created_at: datetime
    validation: EvidenceValidationResult | None = None
    lifecycle_state: EvidenceLifecycleState = EvidenceLifecycleState.GENERATED

    def observation_type_ids(self) -> frozenset[str]:
        return frozenset(obs.type_id.value for obs in self.observations)

    def with_validation(
        self, validation: EvidenceValidationResult
    ) -> SessionEvidencePackage:
        lifecycle = (
            EvidenceLifecycleState.ACCEPTED
            if validation.disposition
            in {
                EvidenceDisposition.ACCEPTED,
                EvidenceDisposition.ACCEPTED_WITH_RESTRICTIONS,
            }
            else EvidenceLifecycleState.REJECTED
        )
        return SessionEvidencePackage(
            package_id=self.package_id,
            student_id=self.student_id,
            session_id=self.session_id,
            mission_instance_id=self.mission_instance_id,
            topic_id=self.topic_id,
            topic_title=self.topic_title,
            curriculum_identity=self.curriculum_identity,
            learning_objectives=self.learning_objectives,
            observations=self.observations,
            finish_review_verdict=self.finish_review_verdict,
            finish_review_notes=self.finish_review_notes,
            session_metadata=dict(self.session_metadata),
            provenance=self.provenance,
            contract_version=self.contract_version,
            created_at=self.created_at,
            validation=validation,
            lifecycle_state=lifecycle,
        )

    def with_lifecycle(
        self, state: EvidenceLifecycleState
    ) -> SessionEvidencePackage:
        return SessionEvidencePackage(
            package_id=self.package_id,
            student_id=self.student_id,
            session_id=self.session_id,
            mission_instance_id=self.mission_instance_id,
            topic_id=self.topic_id,
            topic_title=self.topic_title,
            curriculum_identity=self.curriculum_identity,
            learning_objectives=self.learning_objectives,
            observations=self.observations,
            finish_review_verdict=self.finish_review_verdict,
            finish_review_notes=self.finish_review_notes,
            session_metadata=dict(self.session_metadata),
            provenance=self.provenance,
            contract_version=self.contract_version,
            created_at=self.created_at,
            validation=self.validation,
            lifecycle_state=state,
        )

    def to_opaque(self) -> dict[str, Any]:
        return {
            "package_id": self.package_id,
            "student_id": self.student_id,
            "session_id": self.session_id,
            "mission_instance_id": self.mission_instance_id,
            "topic_id": self.topic_id,
            "topic_title": self.topic_title,
            "curriculum_identity": self.curriculum_identity,
            "learning_objectives": list(self.learning_objectives),
            "observations": [obs.to_opaque() for obs in self.observations],
            "finish_review_verdict": self.finish_review_verdict,
            "finish_review_notes": self.finish_review_notes,
            "session_metadata": dict(self.session_metadata),
            "provenance": self.provenance,
            "contract_version": self.contract_version,
            "created_at": self.created_at.isoformat(),
            "validation": (
                self.validation.to_opaque() if self.validation is not None else None
            ),
            "lifecycle_state": self.lifecycle_state.value,
            "authority": "educational_evidence_authority",
            "twin_updated": False,
        }

    @classmethod
    def create(
        cls,
        *,
        student_id: str,
        session_id: str,
        mission_instance_id: str = "",
        topic_id: str = "",
        topic_title: str = "",
        curriculum_identity: str = "",
        learning_objectives: tuple[str, ...] | list[str] = (),
        observations: (
            tuple[CandidateObservation, ...] | list[CandidateObservation]
        ) = (),
        finish_review_verdict: str | None = None,
        finish_review_notes: str | None = None,
        session_metadata: dict[str, Any] | None = None,
        provenance: str = "learning_session_runtime",
        package_id: str | None = None,
        created_at: datetime | None = None,
    ) -> SessionEvidencePackage:
        return cls(
            package_id=package_id or f"evp-{uuid4().hex[:16]}",
            student_id=student_id.strip(),
            session_id=session_id.strip(),
            mission_instance_id=(mission_instance_id or "").strip(),
            topic_id=(topic_id or "").strip(),
            topic_title=(topic_title or "").strip(),
            curriculum_identity=(curriculum_identity or "").strip(),
            learning_objectives=tuple(
                str(o).strip() for o in learning_objectives if str(o).strip()
            ),
            observations=tuple(observations),
            finish_review_verdict=(
                (finish_review_verdict or "").strip().lower() or None
            ),
            finish_review_notes=(finish_review_notes or None),
            session_metadata=dict(session_metadata or {}),
            provenance=provenance.strip() or "learning_session_runtime",
            contract_version=f"{EVIDENCE_PACKAGE_CONTRACT}/{EVIDENCE_PACKAGE_VERSION}",
            created_at=created_at or datetime.now(tz=UTC),
            validation=None,
            lifecycle_state=EvidenceLifecycleState.GENERATED,
        )

    @classmethod
    def from_opaque(cls, raw: dict[str, Any] | None) -> SessionEvidencePackage | None:
        if not isinstance(raw, dict) or not raw.get("package_id"):
            return None
        observations: list[CandidateObservation] = []
        for item in raw.get("observations") or ():
            raw_item = item if isinstance(item, dict) else None
            obs = CandidateObservation.from_opaque(raw_item)
            if obs is not None:
                observations.append(obs)
        created = raw.get("created_at")
        if isinstance(created, str):
            try:
                created_at = datetime.fromisoformat(created)
            except ValueError:
                created_at = datetime.now(tz=UTC)
        elif isinstance(created, datetime):
            created_at = created
        else:
            created_at = datetime.now(tz=UTC)
        package = cls(
            package_id=str(raw["package_id"]),
            student_id=str(raw.get("student_id") or ""),
            session_id=str(raw.get("session_id") or ""),
            mission_instance_id=str(raw.get("mission_instance_id") or ""),
            topic_id=str(raw.get("topic_id") or ""),
            topic_title=str(raw.get("topic_title") or ""),
            curriculum_identity=str(raw.get("curriculum_identity") or ""),
            learning_objectives=tuple(
                str(o) for o in (raw.get("learning_objectives") or ()) if str(o).strip()
            ),
            observations=tuple(observations),
            finish_review_verdict=(
                str(raw["finish_review_verdict"]).strip().lower()
                if raw.get("finish_review_verdict")
                else None
            ),
            finish_review_notes=raw.get("finish_review_notes"),
            session_metadata=dict(raw.get("session_metadata") or {}),
            provenance=str(raw.get("provenance") or "learning_session_runtime"),
            contract_version=str(
                raw.get("contract_version")
                or f"{EVIDENCE_PACKAGE_CONTRACT}/{EVIDENCE_PACKAGE_VERSION}"
            ),
            created_at=created_at,
            validation=EvidenceValidationResult.from_opaque(raw.get("validation")),
            lifecycle_state=EvidenceLifecycleState(
                str(
                    raw.get("lifecycle_state")
                    or EvidenceLifecycleState.GENERATED.value
                )
            ),
        )
        return package
