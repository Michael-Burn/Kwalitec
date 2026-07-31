"""Coexistence policy between JSON Runtime A and published-curriculum Runtime C.

V1S-007 / A9 — Educational Runtime Singularity: student educational execution
for published curricula runs exclusively through the Educational Runtime
(Runtime C). JSON Runtime A may remain as on-disk syllabus substrate and as a
TEMPORARY path for students without Runtime C enrolment (RI-002 retirement),
but must never be used as a fallback when Educational Runtime is already the
authority for that student.

V1S-002 dogfood cutover: when Runtime C enrolment is enabled and an active
published package exists for CS1 / CB2 / CM1, platform routing selects
``PUBLISHED_CURRICULUM`` as the sole student curriculum authority for that
subject (including legacy IFoA catalogue selections).

PI-002A adds a student-facing Founder → Student bridge with feature flags and
audited routing. This coexistence helper remains the engine-level check used
by ``EducationalRuntimeEngineService``; flag gating for live student enrolment
lives in ``app.application.platform_integration``.
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

        Absence of a published package keeps the subject on JSON substrate
        (or unsupported). This method does not authorise Runtime A fallback
        from an existing Educational Runtime enrolment (A9).
        """
        if self.has_published_curriculum(subject_code):
            return RuntimeAuthority.PUBLISHED_CURRICULUM
        return RuntimeAuthority.JSON_BUNDLED

    def json_runtime_remains_default(self) -> bool:
        """JSON Runtime A substrate still exists pending RI-002 hard removal.

        Dogfood / Runtime C enrolments must not fall back to JSON execution
        (V1S-007 A9). This flag means the package remains in-repo as substrate
        and TEMPORARY non–Runtime-C path only — not an alternate educational
        execution path for enrolled Educational Runtime students.
        """
        return True
