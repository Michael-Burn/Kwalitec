"""Composition root construction gates (APP-003).

Composition Root only constructs wired production services.
"""

from __future__ import annotations

from pathlib import Path

from tests.architecture import (
    APPLICATION_ROOT,
    INFRASTRUCTURE_ROOT,
    WEB_ROOT,
    call_names,
    is_under_composition,
    iter_python_files,
)

# Production constructors that must not appear outside composition (and web
# factory may call create_application only).
WIRED_CONSTRUCTORS = frozenset(
    {
        "EducationalPipeline",
        "MissionEnricher",
        "RecommendationEnricher",
        "OpenAIProvider",
    }
)

ALLOWED_CONSTRUCTION_ROOTS = (
    APPLICATION_ROOT / "composition",
    INFRASTRUCTURE_ROOT / "composition",
)


def _is_allowed_construction_site(path: Path) -> bool:
    for root in ALLOWED_CONSTRUCTION_ROOTS:
        try:
            path.relative_to(root)
            return True
        except ValueError:
            continue
    return False


def test_wired_services_constructed_only_in_composition_root() -> None:
    offenders: list[str] = []
    scan_roots = (APPLICATION_ROOT, INFRASTRUCTURE_ROOT, WEB_ROOT)
    for root in scan_roots:
        for path in iter_python_files(root):
            if _is_allowed_construction_site(path):
                continue
            # Default AI provider helper lives in application composition only.
            names = call_names(path)
            illegal = names.intersection(WIRED_CONSTRUCTORS)
            if illegal:
                offenders.append(
                    f"{path.relative_to(root.parent)}: {sorted(illegal)}"
                )
    assert not offenders, (
        "Wired production services must be constructed only in composition "
        f"roots; found: {offenders}"
    )


def test_web_does_not_construct_domain_engines() -> None:
    forbidden = frozenset(
        {
            "MissionGenerator",
            "StudyPlanner",
            "ProgressEvaluator",
            "RecommendationGenerator",
            "ExplanationBuilder",
            "ExperienceGenerator",
            "EducationalPipeline",
            "MissionEnricher",
            "RecommendationEnricher",
        }
    )
    for path in iter_python_files(WEB_ROOT):
        names = call_names(path)
        illegal = names.intersection(forbidden)
        assert not illegal, (
            f"web {path.name} constructs educational collaborators {illegal}"
        )


def test_application_business_modules_do_not_construct_pipeline() -> None:
    for path in iter_python_files(APPLICATION_ROOT):
        if is_under_composition(path, APPLICATION_ROOT):
            continue
        assert "EducationalPipeline" not in call_names(path), (
            f"{path} constructs EducationalPipeline outside composition"
        )
