"""Educational package artefacts — certified Mission+Session bundles (EA-006).

Stores and resolves publication-approved educational packages that replace
templated syllabus-paste substance for named topics. Content layer only —
does not redesign Runtime A/C, SCI, Twin, or recommendation selection.
"""

from __future__ import annotations

from app.application.educational_packages.guard import (
    certified_guidance_enforced,
    withhold_message,
)
from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    find_educational_package,
    find_package_by_id,
    package_data_root,
    packages_for_subject,
    reset_educational_package_cache,
)
from app.application.educational_packages.models import (
    CertifiedEducationalPackage,
    KnowledgeCheck,
    KnowledgeCheckChoice,
    ReadingGuidance,
    TomorrowPreviewPack,
)
from app.application.educational_packages.selection import (
    resolve_active_educational_package,
)

__all__ = [
    "CertifiedEducationalPackage",
    "EducationalPackageLoader",
    "KnowledgeCheck",
    "KnowledgeCheckChoice",
    "ReadingGuidance",
    "TomorrowPreviewPack",
    "certified_guidance_enforced",
    "find_educational_package",
    "find_package_by_id",
    "package_data_root",
    "packages_for_subject",
    "reset_educational_package_cache",
    "resolve_active_educational_package",
    "withhold_message",
]
