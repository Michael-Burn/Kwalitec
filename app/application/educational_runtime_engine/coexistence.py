"""Coexistence policy between JSON Runtime A and published-curriculum Runtime C.

PI-001C does not cut over existing bundled JSON subjects. The curriculum-driven
runtime activates only when a student enrols against an active published
package. Existing StudyPlanService / PlanningService paths remain authoritative
for JSON-backed exams until an evidence-backed cutover programme.

PI-002A adds a student-facing Founder → Student bridge with feature flags and
audited routing. The student wizard routes to Runtime C only when
``KWALITEC_RUNTIME_C_ENROLMENT`` (or the umbrella
``KWALITEC_FOUNDER_STUDENT_BRIDGE``) is enabled and the selection matches the
Published category or the Runtime C allowlist. This coexistence helper remains
the engine-level check used by ``EducationalRuntimeEngineService``; flag gating
for live student enrolment lives in
``app.application.platform_integration``.
"""

from __future__ import annotations

from enum import StrEnum

from app.application.curriculum_studio_foundation.authority import (
    PublishedCurriculumAuthority,
)


class RuntimeAuthority(StrEnum):
    """Which educational runtime owns a given student/subject path."""

    JSON_BUNDLED = "json_bundled"
    PUBLISHED_CURRICULUM = "published_curriculum"


class RuntimeCoexistencePolicy:
    """Resolve which runtime may own enrolment for a subject code."""

    def __init__(
        self,
        *,
        authority: PublishedCurriculumAuthority | None = None,
    ) -> None:
        self._authority = authority or PublishedCurriculumAuthority()

    def has_published_curriculum(self, subject_code: str) -> bool:
        return self._authority.get_active(subject_code) is not None

    def resolve_for_enrolment(self, subject_code: str) -> RuntimeAuthority:
        """Published package present → curriculum runtime may enrol.

        Absence of a published package keeps the subject on JSON Runtime A
        (or unsupported). This method does not disable Runtime A.
        """
        if self.has_published_curriculum(subject_code):
            return RuntimeAuthority.PUBLISHED_CURRICULUM
        return RuntimeAuthority.JSON_BUNDLED

    def json_runtime_remains_default(self) -> bool:
        """Existing student paths remain on Runtime A until cutover."""
        return True
