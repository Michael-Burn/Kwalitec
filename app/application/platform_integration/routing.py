"""Runtime routing with auditable enrolment selection (PI-002A / V1S-002).

Runtime A (JSON bundled) remains the default for non-dogfood subjects.
Runtime C (published curriculum) is selected when feature flags and
routing rules allow. V1S-002 unions dogfood subjects (CS1/CB2/CM1) into
the Runtime C allowlist whenever enrolment is enabled so each dogfood
subject has exactly one student curriculum authority when a published
package is active. Every decision is persisted for audit.
"""

from __future__ import annotations

import json
import uuid
from typing import Any

from app.application.curriculum_studio_foundation.authority import (
    PublishedCurriculumAuthority,
)
from app.application.educational_runtime_engine.coexistence import (
    RuntimeAuthority,
)
from app.application.platform_integration.discovery import (
    PUBLISHED_CATEGORY_CODE,
)
from app.application.platform_integration.dto import (
    RoutingAuditSnapshot,
    RoutingDecision,
)
from app.application.platform_integration.flags import (
    DOGFOOD_CURRICULUM_SUBJECTS,
    FounderStudentBridgeFlags,
    effective_runtime_c_allowlist,
    resolve_founder_student_bridge_flags,
)
from app.extensions import db
from app.models.platform_integration import RuntimeEnrolmentRoutingAudit


def _new_audit_id() -> str:
    return f"rta_{uuid.uuid4().hex}"


class RuntimeRoutingService:
    """Resolve and audit which educational runtime owns an enrolment."""

    def __init__(
        self,
        *,
        authority: PublishedCurriculumAuthority | None = None,
        flags: FounderStudentBridgeFlags | None = None,
    ) -> None:
        self._authority = authority or PublishedCurriculumAuthority()
        self._flags = flags

    def _resolve_flags(self) -> FounderStudentBridgeFlags:
        return self._flags or resolve_founder_student_bridge_flags()

    def resolve(
        self,
        *,
        subject_code: str,
        category_code: str = "",
    ) -> RoutingDecision:
        """Decide runtime authority without writing audit yet.

        Rules (in order):
        1. Runtime C enrolment flag must be ON — otherwise always Runtime A.
        2. An active published package must exist for the subject.
        3. Category is ``Published``, OR subject is on the effective Runtime C
           allowlist (explicit allowlist ∪ dogfood subjects when enrolment on).
        4. Otherwise Runtime A (JSON bundled) remains authoritative.
        """
        flags = self._resolve_flags()
        code = (subject_code or "").strip().upper()
        category = (category_code or "").strip()
        package = self._authority.get_active(code) if code else None
        allowlist = effective_runtime_c_allowlist(flags)
        flags_snapshot = {
            "ENABLE_PUBLISHED_SUBJECT_DISCOVERY": (
                flags.ENABLE_PUBLISHED_SUBJECT_DISCOVERY
            ),
            "ENABLE_RUNTIME_C_ENROLMENT": flags.ENABLE_RUNTIME_C_ENROLMENT,
            "RUNTIME_C_SUBJECT_ALLOWLIST": sorted(
                flags.RUNTIME_C_SUBJECT_ALLOWLIST
            ),
            "EFFECTIVE_RUNTIME_C_ALLOWLIST": sorted(allowlist),
        }

        if not flags.ENABLE_RUNTIME_C_ENROLMENT:
            return RoutingDecision(
                subject_code=code,
                category_code=category,
                runtime_authority=RuntimeAuthority.JSON_BUNDLED,
                reason="runtime_c_enrolment_disabled",
                published_package_id=(
                    package.package_id if package is not None else None
                ),
                curriculum_identity=(
                    f"{code}:{package.version_label}"
                    if package is not None
                    else None
                ),
                discovery_enabled=flags.ENABLE_PUBLISHED_SUBJECT_DISCOVERY,
                enrolment_enabled=False,
                flags_snapshot=flags_snapshot,
            )

        if package is None:
            return RoutingDecision(
                subject_code=code,
                category_code=category,
                runtime_authority=RuntimeAuthority.JSON_BUNDLED,
                reason="no_active_published_package",
                published_package_id=None,
                curriculum_identity=None,
                discovery_enabled=flags.ENABLE_PUBLISHED_SUBJECT_DISCOVERY,
                enrolment_enabled=True,
                flags_snapshot=flags_snapshot,
            )

        identity = f"{code}:{package.version_label}"
        from_published_category = category == PUBLISHED_CATEGORY_CODE
        on_allowlist = code in allowlist
        dogfood_cutover = (
            code in DOGFOOD_CURRICULUM_SUBJECTS
            and code not in flags.RUNTIME_C_SUBJECT_ALLOWLIST
        )

        if from_published_category or on_allowlist:
            if from_published_category:
                reason = "published_category_selection"
            elif dogfood_cutover:
                reason = "dogfood_curriculum_cutover"
            else:
                reason = "subject_allowlist"
            return RoutingDecision(
                subject_code=code,
                category_code=category,
                runtime_authority=RuntimeAuthority.PUBLISHED_CURRICULUM,
                reason=reason,
                published_package_id=package.package_id,
                curriculum_identity=identity,
                discovery_enabled=flags.ENABLE_PUBLISHED_SUBJECT_DISCOVERY,
                enrolment_enabled=True,
                flags_snapshot=flags_snapshot,
            )

        return RoutingDecision(
            subject_code=code,
            category_code=category,
            runtime_authority=RuntimeAuthority.JSON_BUNDLED,
            reason="legacy_catalogue_defaults_to_runtime_a",
            published_package_id=package.package_id,
            curriculum_identity=identity,
            discovery_enabled=flags.ENABLE_PUBLISHED_SUBJECT_DISCOVERY,
            enrolment_enabled=True,
            flags_snapshot=flags_snapshot,
        )

    def record_decision(
        self,
        *,
        user_id: int,
        decision: RoutingDecision,
        enrolment_id: str | None = None,
        study_plan_id: int | None = None,
        commit: bool = False,
    ) -> RoutingAuditSnapshot:
        """Persist an immutable routing audit row."""
        row = RuntimeEnrolmentRoutingAudit(
            audit_id=_new_audit_id(),
            user_id=user_id,
            subject_code=decision.subject_code,
            category_code=decision.category_code or "",
            runtime_authority=decision.runtime_authority.value,
            decision_reason=decision.reason,
            published_package_id=decision.published_package_id,
            curriculum_identity=decision.curriculum_identity,
            enrolment_id=enrolment_id,
            study_plan_id=study_plan_id,
            flags_json=json.dumps(decision.flags_snapshot, sort_keys=True),
        )
        db.session.add(row)
        if commit:
            db.session.commit()
        else:
            db.session.flush()
        return self._snapshot(row)

    def list_audits_for_user(
        self, user_id: int
    ) -> tuple[RoutingAuditSnapshot, ...]:
        rows = (
            RuntimeEnrolmentRoutingAudit.query.filter_by(user_id=user_id)
            .order_by(
                RuntimeEnrolmentRoutingAudit.created_at.asc(),
                RuntimeEnrolmentRoutingAudit.id.asc(),
            )
            .all()
        )
        return tuple(self._snapshot(row) for row in rows)

    def get_audit(self, audit_id: str) -> RoutingAuditSnapshot | None:
        row = RuntimeEnrolmentRoutingAudit.query.filter_by(
            audit_id=audit_id
        ).first()
        if row is None:
            return None
        return self._snapshot(row)

    @staticmethod
    def _snapshot(row: RuntimeEnrolmentRoutingAudit) -> RoutingAuditSnapshot:
        flags: dict[str, Any] = {}
        try:
            flags = json.loads(row.flags_json or "{}")
        except json.JSONDecodeError:
            flags = {}
        return RoutingAuditSnapshot(
            audit_id=row.audit_id,
            user_id=row.user_id,
            subject_code=row.subject_code,
            category_code=row.category_code,
            runtime_authority=row.runtime_authority,
            decision_reason=row.decision_reason,
            published_package_id=row.published_package_id,
            curriculum_identity=row.curriculum_identity,
            enrolment_id=row.enrolment_id,
            study_plan_id=row.study_plan_id,
            flags_json=flags,
            created_at=row.created_at,
        )
