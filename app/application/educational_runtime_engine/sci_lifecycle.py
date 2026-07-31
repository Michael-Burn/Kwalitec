"""Student Curriculum Instance lifecycle for Educational Runtime Singularity.

V1S-007 / A9: SCI is a mandatory educational object owned by the Educational
Runtime path. Missing SCI is resolved (auto-create) or surfaced — never used
as a reason to switch the student onto Runtime A.
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime

from app.application.educational_runtime_engine.exceptions import (
    EducationalPrerequisiteMissing,
)
from app.application.runtime_integration.routing import resolve_active_instance
from app.domain.curriculum_extraction.publication_state import PublicationState
from app.extensions import db
from app.models.curriculum_knowledge_graph import CkgGraphEdition, CkgSubject, CkgTopic
from app.models.student_curriculum_binding import SciStudentCurriculumInstance

logger = logging.getLogger(__name__)

_BRIDGE_PROVIDER = "kwalitec-published-package"
_BRIDGE_EDITION_PREFIX = "ckg-runtime-bridge"


@dataclass(frozen=True)
class SciEnsureResult:
    """Outcome of ensuring an active SCI for a Runtime C enrolment."""

    instance_id: str
    subject_code: str
    edition_id: str
    created: bool
    source: str  # existing | onboard | bridge_onboard


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def ensure_active_sci(
    *,
    student_id: int,
    subject_code: str,
    correlation_id: str | None = None,
    require: bool = True,
) -> SciEnsureResult | None:
    """Ensure exactly one active SCI exists for the enrolment subject.

    Creation order:
      1. Return existing active SCI for subject
      2. Onboard against an existing published CKG edition
      3. Provision a published CKG bridge edition from the active published
         curriculum package, then onboard

    Args:
        student_id: Authenticated student user id.
        subject_code: Enrolment subject (e.g. ``CS1``).
        correlation_id: Optional lifecycle correlation token.
        require: When True, raise if SCI cannot be created; when False,
            return ``None`` (used by soft hooks).

    Returns:
        SciEnsureResult when SCI is present after the call.

    Raises:
        EducationalPrerequisiteMissing: When require=True and SCI cannot be
            materialised (no published package / onboard failure).
    """
    sid = int(student_id)
    code = (subject_code or "").strip().upper()
    if not code:
        if require:
            raise EducationalPrerequisiteMissing(
                "A subject enrolment is required before study can continue.",
                missing_prerequisite="subject_code",
            )
        return None

    existing = resolve_active_instance(sid, subject_code=code)
    if existing is not None:
        return SciEnsureResult(
            instance_id=existing.instance_id,
            subject_code=str(existing.subject_code or code),
            edition_id=str(existing.edition_id or ""),
            created=False,
            source="existing",
        )

    edition_id = _resolve_or_provision_edition(code)
    if not edition_id:
        logger.warning(
            "v1s007_sci_ensure_failed student=%s subject=%s "
            "reason=no_published_curriculum",
            sid,
            code,
        )
        if require:
            raise EducationalPrerequisiteMissing(
                "Your curriculum is not ready for study yet. "
                "A published curriculum package is required before a "
                "learning session can start.",
                missing_prerequisite="published_curriculum_or_ckg_edition",
                subject_code=code,
            )
        return None

    from app.infrastructure.adapters.learner_lifecycle import (
        onboard_after_enrolment,
    )

    corr = (correlation_id or "").strip() or f"v1s007-sci-{sid}-{code}"
    result = onboard_after_enrolment(
        student_id=sid,
        subject_code=code,
        edition_id=edition_id,
        correlation_id=corr,
    )
    instance = resolve_active_instance(sid, subject_code=code)
    if instance is None:
        logger.warning(
            "v1s007_sci_ensure_failed student=%s subject=%s edition=%s "
            "onboard_status=%s",
            sid,
            code,
            edition_id,
            getattr(result, "status", None),
        )
        if require:
            raise EducationalPrerequisiteMissing(
                "We could not prepare your curriculum binding for study. "
                "Please try again shortly, or contact support if this persists.",
                missing_prerequisite="student_curriculum_instance",
                subject_code=code,
            )
        return None

    created = bool(result and getattr(result, "succeeded", False))
    source = (
        "bridge_onboard"
        if edition_id.startswith(_BRIDGE_EDITION_PREFIX)
        else "onboard"
    )
    logger.info(
        "v1s007_sci_ensured student=%s subject=%s instance=%s "
        "edition=%s created=%s source=%s",
        sid,
        code,
        instance.instance_id,
        edition_id,
        created,
        source,
    )
    return SciEnsureResult(
        instance_id=instance.instance_id,
        subject_code=str(instance.subject_code or code),
        edition_id=str(instance.edition_id or edition_id),
        created=created,
        source=source,
    )


def _resolve_or_provision_edition(subject_code: str) -> str | None:
    """Return a published CKG edition id, provisioning from package if needed."""
    from app.infrastructure.adapters.learner_lifecycle import (
        resolve_published_edition_id,
    )

    existing = resolve_published_edition_id(subject_code)
    if existing:
        return existing
    return provision_ckg_edition_from_published_package(subject_code)


def provision_ckg_edition_from_published_package(
    subject_code: str,
) -> str | None:
    """Create a published CKG bridge edition from the active published package.

    Aligns the two curriculum substrates (PublishedCurriculumPackage ↔ CKG)
    so SCI binding can proceed without routing the student to Runtime A.

    Idempotent per subject: returns the existing bridge edition when present.
    """
    code = (subject_code or "").strip().upper()
    if not code:
        return None

    from app.application.curriculum_studio_foundation.authority import (
        PublishedCurriculumAuthority,
    )
    from app.application.educational_engine_foundation.service import (
        EducationalEngineFoundationService,
    )

    package = PublishedCurriculumAuthority().get_active(code)
    if package is None:
        return None

    bridge_id = f"{_BRIDGE_EDITION_PREFIX}-{code.lower()}-{package.version_label}"
    existing = CkgGraphEdition.query.filter_by(edition_id=bridge_id).first()
    if (
        existing is not None
        and existing.publication_state == PublicationState.PUBLISHED.value
    ):
        return bridge_id

    artefacts = EducationalEngineFoundationService().derive_from_package(
        package.package
    )
    if not artefacts.topics:
        logger.warning(
            "v1s007_ckg_bridge_empty subject=%s package=%s",
            code,
            package.version_label,
        )
        return None

    # Archive any prior published bridge for this subject label collision.
    prior = (
        CkgGraphEdition.query.filter_by(
            subject_code=code,
            publication_state=PublicationState.PUBLISHED.value,
        )
        .order_by(CkgGraphEdition.id.desc())
        .all()
    )
    now = _utc_now()
    for row in prior:
        if row.edition_id.startswith(_BRIDGE_EDITION_PREFIX):
            row.publication_state = PublicationState.ARCHIVED.value
            row.updated_at = now

    edition_label = str(package.version_label or "runtime-bridge")[:64]
    if existing is None:
        edition = CkgGraphEdition(
            edition_id=bridge_id,
            subject_code=code,
            edition_label=edition_label,
            provider=_BRIDGE_PROVIDER,
            title=f"{code} Educational Runtime bridge",
            publication_state=PublicationState.PUBLISHED.value,
            validation_status="passed",
            review_status="approved",
            published_at=now,
            published_by="v1s007-educational-runtime",
            publication_rationale=(
                "V1S-007 Educational Runtime Singularity — CKG bridge "
                "provisioned from active PublishedCurriculumPackage so SCI "
                "can bind without Runtime A fallback."
            ),
            created_at=now,
            updated_at=now,
        )
        db.session.add(edition)
    else:
        existing.publication_state = PublicationState.PUBLISHED.value
        existing.published_at = now
        existing.updated_at = now
        existing.publication_rationale = (
            "V1S-007 Educational Runtime Singularity — CKG bridge refreshed."
        )

    # Live CKG nodes are subject-scoped (unique stable_id). Replace any
    # prior subject/topic rows for this code so the bridge owns the live graph.
    CkgTopic.query.filter(CkgTopic.stable_id.like(f"{code}.T%")).delete(
        synchronize_session=False
    )
    CkgSubject.query.filter_by(stable_id=code).delete(synchronize_session=False)
    db.session.flush()

    db.session.add(
        CkgSubject(
            stable_id=code,
            graph_edition_id=bridge_id,
            code=code,
            title=f"{code} curriculum",
            provider=_BRIDGE_PROVIDER,
            edition_label=edition_label,
            sequence_index=0,
            created_at=now,
        )
    )

    for index, topic in enumerate(artefacts.topics, start=1):
        topic_sid = f"{code}.T{index:02d}"
        title = str(topic.get("title") or topic.get("code") or topic_sid)[:512]
        topic_code = str(topic.get("code") or f"T{index:02d}")[:64]
        minutes = int(topic.get("estimated_minutes") or 0)
        difficulty = str(topic.get("difficulty") or "foundational")[:32]
        db.session.add(
            CkgTopic(
                stable_id=topic_sid,
                subject_stable_id=code,
                code=topic_code,
                title=title,
                display_order=int(topic.get("display_order") or index),
                difficulty=difficulty,
                estimated_study_minutes=max(0, minutes),
                created_at=now,
            )
        )

    db.session.commit()
    logger.info(
        "v1s007_ckg_bridge_provisioned subject=%s edition=%s topics=%s",
        code,
        bridge_id,
        len(artefacts.topics),
    )
    return bridge_id


def active_sci_count(student_id: int, *, subject_code: str | None = None) -> int:
    """Count active SCI rows (diagnostics / tests)."""
    query = SciStudentCurriculumInstance.query.filter_by(
        student_id=int(student_id),
        is_active=True,
    )
    if subject_code:
        query = query.filter_by(subject_code=subject_code.strip().upper())
    return int(query.count())


def new_correlation_token(prefix: str = "v1s007") -> str:
    """Stable short correlation id for lifecycle telemetry."""
    return f"{prefix}-{uuid.uuid4().hex[:12]}"
