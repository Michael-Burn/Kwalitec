"""Educational package artefacts — certified Mission+Session bundles (EA-006).

Stores and resolves publication-approved educational packages that replace
templated syllabus-paste substance for named topics. Content layer only —
does not redesign Runtime A/C, SCI, Twin, or recommendation selection.
"""

from __future__ import annotations

from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    find_educational_package,
    package_data_root,
    reset_educational_package_cache,
)
from app.application.educational_packages.models import (
    CertifiedEducationalPackage,
    KnowledgeCheck,
    ReadingGuidance,
    TomorrowPreviewPack,
)

__all__ = [
    "CertifiedEducationalPackage",
    "EducationalPackageLoader",
    "KnowledgeCheck",
    "ReadingGuidance",
    "TomorrowPreviewPack",
    "find_educational_package",
    "package_data_root",
    "reset_educational_package_cache",
]
