"""PB-002 F8 — package selection chain reaches CA-R1 / CB-R1."""

from __future__ import annotations

from app.application.educational_packages.loader import reset_educational_package_cache
from app.application.educational_packages.selection import (
    resolve_active_educational_package,
    should_suppress_topic_completed,
)


def setup_function() -> None:
    reset_educational_package_cache()


def test_alpha_chain_reaches_ca_r1() -> None:
    completed: set[str] = set()
    last = ""

    p1 = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="1.1",
        completed_package_ids=completed,
        last_completed_package_id=last,
    )
    assert p1 is not None
    assert p1.package_id == "CS1-EP001-PKG-1.1-PURPOSE-FUNCTION"
    assert p1.campaign_day == "CA-D1"
    completed.add(p1.package_id)
    last = p1.package_id

    p2 = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="1.2",
        completed_package_ids=completed,
        last_completed_package_id=last,
    )
    assert p2 is not None
    assert p2.package_id == "CS1-EP001-PKG-1.2-EDA-SUMMARIES"
    assert should_suppress_topic_completed(p2, completed_package_ids=completed)
    completed.add(p2.package_id)
    last = p2.package_id

    p3 = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="1.2",
        completed_package_ids=completed,
        last_completed_package_id=last,
    )
    assert p3 is not None
    assert p3.package_id == "CS1-EP001-PKG-1.2-EDA-ASSOCIATION"
    assert should_suppress_topic_completed(p3, completed_package_ids=completed)
    completed.add(p3.package_id)
    last = p3.package_id

    p4 = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="1.2",
        completed_package_ids=completed,
        last_completed_package_id=last,
    )
    assert p4 is not None
    assert p4.package_id == "CS1-EP001-PKG-REV-PURPOSE-EDA"
    assert p4.campaign_day == "CA-R1"
    assert p4.mode == "revision"
    assert not should_suppress_topic_completed(p4, completed_package_ids=completed)


def test_beta_chain_reaches_cb_r1() -> None:
    # Simulate Alpha terminal already done; start Beta at 2.1 discrete.
    completed = {
        "CS1-EP001-PKG-1.1-PURPOSE-FUNCTION",
        "CS1-EP001-PKG-1.2-EDA-SUMMARIES",
        "CS1-EP001-PKG-1.2-EDA-ASSOCIATION",
        "CS1-EP001-PKG-REV-PURPOSE-EDA",
    }
    last = "CS1-EP001-PKG-REV-PURPOSE-EDA"

    # CA-R1 tomorrow points at 2.1 → first uncompleted 2.1 pack
    p1 = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="2.1",
        completed_package_ids=completed,
        last_completed_package_id=last,
    )
    assert p1 is not None
    assert p1.package_id == "CS1-CS1002-PKG-2.1-DISCRETE"
    completed.add(p1.package_id)
    last = p1.package_id

    p2 = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="2.1",
        completed_package_ids=completed,
        last_completed_package_id=last,
    )
    assert p2 is not None
    assert p2.package_id == "CS1-CS1002-PKG-2.1-CONTINUOUS"
    assert should_suppress_topic_completed(p2, completed_package_ids=completed)
    completed.add(p2.package_id)
    last = p2.package_id

    p3 = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="2.1",
        completed_package_ids=completed,
        last_completed_package_id=last,
    )
    assert p3 is not None
    assert p3.package_id == "CS1-CS1002-PKG-REV-PCA-DISTRIBUTIONS"
    assert p3.campaign_day == "CB-R1"


def test_campaign_day_parsed_on_packages() -> None:
    from app.application.educational_packages.loader import find_educational_package

    pack = find_educational_package(topic_code="1.1", subject_id="CS1")
    assert pack is not None
    assert pack.campaign_day == "CA-D1"
    rev = find_educational_package(topic_code="CA-R1", subject_id="CS1")
    assert rev is not None
    assert rev.campaign_day == "CA-R1"


def test_gamma_chain_reaches_cg_r1() -> None:
    """RO-001 — CB-R1 tomorrow_preview → CG-D1…CG-R1 joint inventory."""
    completed = {
        "CS1-EP001-PKG-1.1-PURPOSE-FUNCTION",
        "CS1-EP001-PKG-1.2-EDA-SUMMARIES",
        "CS1-EP001-PKG-1.2-EDA-ASSOCIATION",
        "CS1-EP001-PKG-REV-PURPOSE-EDA",
        "CS1-CS1002-PKG-2.1-DISCRETE",
        "CS1-CS1002-PKG-2.1-CONTINUOUS",
        "CS1-CS1002-PKG-REV-PCA-DISTRIBUTIONS",
    }
    last = "CS1-CS1002-PKG-REV-PCA-DISTRIBUTIONS"

    expected = [
        ("CS1-EP001-PKG-2.1-PROB-QUANTILES", "CG-D1"),
        ("CS1-EP001-PKG-2.1-POISSON-PROCESS", "CG-D2"),
        ("CS1-EP001-PKG-2.1-INVERSE-TRANSFORM", "CG-D3"),
        ("CS1-EP001-PKG-2.1-SOFTWARE-GENERATION", "CG-D4"),
        ("CS1-EP001-PKG-REV-DISTRIBUTIONS-GENERATION", "CG-R1"),
    ]
    for package_id, day in expected:
        pack = resolve_active_educational_package(
            subject_id="CS1",
            syllabus_topic_code="2.1",
            completed_package_ids=completed,
            last_completed_package_id=last,
        )
        assert pack is not None, f"missing successor before {day}"
        assert pack.package_id == package_id
        assert pack.campaign_day == day
        completed.add(pack.package_id)
        last = pack.package_id
