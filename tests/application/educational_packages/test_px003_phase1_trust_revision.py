"""PX-003 Phase 1 — Trust chrome, verbs, duration, revision regenerate."""

from __future__ import annotations

from app.application.educational_packages.loader import (
    find_package_by_id,
    reset_educational_package_cache,
)
from app.application.educational_packages.ops_chrome_boundary import (
    OPS_ONLY_DAY_LABEL_KEYS,
)
from app.application.educational_packages.selection import (
    resolve_active_educational_package,
)
from app.application.educational_packages.student_chrome import (
    display_title_for_package_id,
    resolve_package_for_student_chrome,
)
from app.application.educational_packages.substance import substance_from_package
from app.application.educational_packages.tomorrow_chrome import (
    format_tomorrow_preview_text,
    resolve_package_for_tomorrow_chrome,
)
from app.application.student_experience.study_verbs import (
    CONTINUE,
    START_TODAY,
    canonical_start_label,
)
from app.presentation.formatting import format_minutes
from app.presentation.session.authoritative_path import (
    AUTHORITATIVE_SESSION_PREFIX,
    SOLE_RUNTIME_DECLARES_SESSION_PRIMARY,
)


def setup_function() -> None:
    reset_educational_package_cache()


def test_student_chrome_prefers_package_id_not_keyword() -> None:
    """PX-B-002 — soft title keywords must not drive student chrome."""
    pack = resolve_package_for_student_chrome(
        educational_package_id="CS1-EP001-PKG-CR-2.1-CONTINUOUS",
        subject_id="CS1",
        syllabus_topic_code="2.1",
    )
    assert pack is not None
    assert pack.package_id == "CS1-EP001-PKG-CR-2.1-CONTINUOUS"
    assert display_title_for_package_id(pack.package_id) == pack.display_title


def test_shared_topic_without_package_id_does_not_keyword_match() -> None:
    """Bare subject+code without journey state stays unresolved for chrome."""
    pack = resolve_package_for_student_chrome(
        subject_id="CS1",
        syllabus_topic_code="2.1",
    )
    assert pack is None


def test_tomorrow_chrome_revision_day_binds_to_package() -> None:
    """PX-B-001 — Revision package tomorrow chrome is package-bound."""
    pack = resolve_package_for_tomorrow_chrome(
        educational_package_id="CS1-EP001-PKG-REV-PUBLICATION-FRONT-RHO",
    )
    assert pack is not None
    assert pack.campaign_day == "CR-R1"
    text = format_tomorrow_preview_text(pack)
    assert text
    assert "2.1.2" not in text or "Revision" in text or "tomorrow" in text.lower()


def test_canonical_study_verbs() -> None:
    """PX-B-034 — one start / continue family."""
    assert canonical_start_label("Start Session") == START_TODAY
    assert canonical_start_label("Begin Session") == START_TODAY
    assert canonical_start_label("Resume Study Session") == CONTINUE
    assert canonical_start_label("Continue Session") == CONTINUE
    assert canonical_start_label("Start Today's Session") == START_TODAY
    assert canonical_start_label(None, in_progress=True) == CONTINUE


def test_duration_formatter_is_shared() -> None:
    """PX-B-035 — Home/Mission duration wording shares format_minutes."""
    assert format_minutes(45) == "45 minutes"
    assert format_minutes(60) == "1 hour"
    assert format_minutes(90) == "1 hour 30 min"


def test_ops_day_labels_are_isolated() -> None:
    """PX-B-003 — ops detector keys documented as non-student."""
    assert "expected_day" in OPS_ONLY_DAY_LABEL_KEYS
    assert "ops_expected_day" in OPS_ONLY_DAY_LABEL_KEYS


def test_session_path_declared() -> None:
    """PX-B-014 — sole-runtime authoritative path is /session."""
    assert SOLE_RUNTIME_DECLARES_SESSION_PRIMARY is True
    assert AUTHORITATIVE_SESSION_PREFIX == "/session"


def test_revision_reading_body_uses_retrieval_framing() -> None:
    """PX-B-004 — Revision checklist presentation names retrieval next steps."""
    pack = find_package_by_id("CS1-EP001-PKG-REV-PUBLICATION-FRONT-RHO")
    assert pack is not None
    assert pack.mode == "revision"
    substance = substance_from_package(
        pack, curriculum_identity="cs1-test", topic_id="t1"
    )
    bodies = " ".join(
        (a.body or "") + " " + (a.prompt or "") for a in substance.activities
    )
    assert "Retrieval" in bodies or "retrieve" in bodies.lower()
    assert "Revision focus" in bodies or "closed-book" in bodies.lower()


def test_cr_d9_successor_is_terminal_revision_without_force() -> None:
    """PX-B-005 / PX-B-007 — natural selection reaches CR-R1 after CR-D9."""
    completed = {
        "CS1-EP001-PKG-REV-SPINE-MEMORY-PI",
        "CS1-EP001-PKG-CR-1.1-AIMS-ANALYSIS",
        "CS1-EP001-PKG-CR-1.1-STAGES-TOOLS",
        "CS1-EP001-PKG-CR-1.1-DATA-SOURCES",
        "CS1-EP001-PKG-CR-1.1-REPRODUCIBLE",
        "CS1-EP001-PKG-CR-1.2-EDA-SUMMARIES",
        "CS1-EP001-PKG-CR-1.2-CORRELATION",
        "CS1-EP001-PKG-CR-1.2-PCA",
        "CS1-EP001-PKG-CR-2.1-DISCRETE",
        "CS1-EP001-PKG-CR-2.1-CONTINUOUS",
    }
    pack = resolve_active_educational_package(
        subject_id="CS1",
        syllabus_topic_code="2.1",
        completed_package_ids=completed,
        last_completed_package_id="CS1-EP001-PKG-CR-2.1-CONTINUOUS",
    )
    assert pack is not None
    assert pack.package_id == "CS1-EP001-PKG-REV-PUBLICATION-FRONT-RHO"
    assert pack.campaign_day == "CR-R1"
    assert pack.mode == "revision"


def test_topic_id_maps_campaign_revision_codes() -> None:
    """PX-B-005 — CR-R1 / CP-R1 topic codes map via tip-topic fallback."""
    from types import SimpleNamespace

    from app.application.educational_runtime_engine.service import (
        EducationalRuntimeEngineService,
    )

    artefacts = SimpleNamespace(
        topics=(
            {
                "topic_id": "topic-5-1",
                "topic_code": "5.1",
                "number": "5.1",
                "title": "5.1 Bayesian methods",
            },
        ),
        mission_templates=(),
    )
    svc = EducationalRuntimeEngineService()
    assert svc._topic_id_for_package_code(artefacts, "CR-R1") == "topic-5-1"
    assert svc._topic_id_for_package_code(artefacts, "CP-R1") == "topic-5-1"
