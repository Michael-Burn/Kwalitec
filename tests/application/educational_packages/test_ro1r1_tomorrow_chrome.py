"""RO1-R1 — Tomorrow Preview chrome binds to approved package identity."""

from __future__ import annotations

from app.application.educational_authoring.composition import compose_mission
from app.application.educational_authoring.dto import AuthoringContext
from app.application.educational_packages.loader import (
    find_educational_package,
    find_package_by_id,
    reset_educational_package_cache,
)
from app.application.educational_packages.tomorrow_chrome import (
    format_tomorrow_preview_text,
    resolve_package_for_tomorrow_chrome,
)
from app.presentation.session.sitting_report import build_sitting_report

_TOPIC_21 = (
    "2.1 Understand the characteristics of basic univariate distributions"
)


def setup_function() -> None:
    reset_educational_package_cache()


def test_shared_topic_first_match_is_stale_beta_discrete() -> None:
    """Document the pre-RO1-R1 failure mode: bare 2.1 → CB-D2 tomorrow."""
    stale = find_educational_package(topic_code="2.1", subject_id="CS1")
    assert stale is not None
    assert stale.package_id == "CS1-CS1002-PKG-2.1-DISCRETE"
    text = format_tomorrow_preview_text(stale)
    assert "2.1.2" in text


def test_resolve_by_package_id_returns_gamma_day4_tomorrow() -> None:
    pack = resolve_package_for_tomorrow_chrome(
        educational_package_id="CS1-EP001-PKG-2.1-SOFTWARE-GENERATION"
    )
    assert pack is not None
    assert pack.campaign_day == "CG-D4"
    text = format_tomorrow_preview_text(pack)
    assert "Gamma Revision" in text
    assert "2.1.2" not in text


def test_day_complete_prefers_last_completed_package() -> None:
    completed = frozenset(
        {
            "CS1-EP001-PKG-2.1-PROB-QUANTILES",
            "CS1-EP001-PKG-2.1-POISSON-PROCESS",
            "CS1-EP001-PKG-2.1-INVERSE-TRANSFORM",
            "CS1-EP001-PKG-2.1-SOFTWARE-GENERATION",
        }
    )
    pack = resolve_package_for_tomorrow_chrome(
        subject_id="CS1",
        syllabus_topic_code="2.1",
        completed_package_ids=completed,
        last_completed_package_id="CS1-EP001-PKG-2.1-SOFTWARE-GENERATION",
        prefer_completed_package=True,
    )
    assert pack is not None
    assert pack.package_id == "CS1-EP001-PKG-2.1-SOFTWARE-GENERATION"
    assert "Gamma Revision" in format_tomorrow_preview_text(pack)


def test_compose_mission_uses_package_id_not_shared_code() -> None:
    composition = compose_mission(
        AuthoringContext(
            topic_title=_TOPIC_21,
            topic_code="2.1",
            subject_code="CS1",
            educational_package_id="CS1-EP001-PKG-2.1-SOFTWARE-GENERATION",
        )
    )
    assert composition.has_composition
    assert composition.tomorrow_preview is not None
    assert composition.tomorrow_preview.has_preview
    title = composition.tomorrow_preview.topic_title or ""
    continuity = (composition.tomorrow_preview.continuity_line or "").lower()
    assert "Gamma" in title or "revision" in continuity
    assert "2.1.2" not in title
    assert "2.1.2" not in continuity


def test_sitting_report_tomorrow_uses_educational_package_id() -> None:
    pack = find_package_by_id("CS1-EP001-PKG-2.1-SOFTWARE-GENERATION")
    assert pack is not None
    expected = format_tomorrow_preview_text(pack)
    report = build_sitting_report(
        topic_title=_TOPIC_21,
        opaque_summary={
            "topic_title": _TOPIC_21,
            "educational_package_id": pack.package_id,
            "subject_id": "CS1",
            "learning_objectives": (pack.learning_objective,),
            "progress_advanced": False,
            "mission_completed": True,
        },
        metadata={"educational_package_id": pack.package_id},
    )
    assert report.tomorrow_preview == expected
    assert "2.1.2" not in report.tomorrow_preview
