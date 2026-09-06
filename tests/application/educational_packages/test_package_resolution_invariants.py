"""Invariants for educational package resolution (title-match override fix).

Guards the class of defect where a session rebuild with a known
educational_package_id silently binds a different package via fragile
substring keyword matching against a placeholder title like "Today's topic".
"""

from __future__ import annotations

from app.application.educational_packages.loader import (
    find_educational_package,
    find_package_by_id,
    reset_educational_package_cache,
)
from app.application.learning_session.educational_flow import EducationalStage
from app.application.learning_session.runtime import LearningSessionRuntime
from app.application.learning_session.substance_planner import (
    EducationalSubstancePlanner,
)
from app.infrastructure.adapters.learning_session.package_activity_engine import (
    PackageActivityEngine,
)
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.session.store import SessionDocumentStore
from tests.application.learning_session.helpers import make_journey, make_objective

_T_STATISTIC = "CS1-EP001-PKG-2.6-T-STATISTIC"
_GLM_PKG = "CS1-EP001-PKG-4.2-EXPONENTIAL-FAMILY"
_PLACEHOLDER_TITLE = "Today's topic"


def setup_function() -> None:
    reset_educational_package_cache()


def test_todays_topic_does_not_resolve_to_t_statistic_via_keyword_t() -> None:
    """Regression: bare keyword ``t`` must not match inside ``Today's topic``."""
    pack = find_educational_package(
        topic_title=_PLACEHOLDER_TITLE,
        subject_id="CS1",
    )
    assert pack is None or pack.package_id != _T_STATISTIC
    # Stronger: no approved package should claim this generic placeholder.
    assert pack is None


def test_t_statistic_still_resolves_from_real_title_keywords() -> None:
    """Whole-word ``t-statistic`` / distinctive keywords still resolve without an id."""
    from app.application.educational_packages.loader import (
        _title_matches_keywords,
        _whole_word_in_title,
    )

    real_title = (
        "Describe the distribution of the t-statistic for Normal samples"
    )
    assert _whole_word_in_title("t-statistic", real_title.lower())
    assert _title_matches_keywords(
        real_title.lower(),
        ("t-statistic", "statistic", "Student", "Normal", "sample", "sigma"),
    )
    # Bare single-char ``t`` is ignored even if still present in a keyword list.
    assert not _title_matches_keywords("today's topic", ("t",))

    # ``sigma`` uniquely identifies this package among live CS1 inventory.
    pack = find_educational_package(
        topic_title="unknown sigma",
        subject_id="CS1",
    )
    assert pack is not None
    assert pack.package_id == _T_STATISTIC


def test_known_package_id_wins_over_ambiguous_placeholder_title() -> None:
    """Known educational_package_id must never be overridden by title matching."""
    glm = find_package_by_id(_GLM_PKG)
    assert glm is not None

    substance = EducationalSubstancePlanner().plan_for_topic(
        curriculum_identity="CS1:test",
        topic_id="node-other",
        topic_title=_PLACEHOLDER_TITLE,
        educational_package_id=_GLM_PKG,
        use_campaign_resolution=True,
    )
    assert substance is not None
    package_ids = {
        dict(act.metadata or ()).get("package_id")
        for act in substance.activities
        if dict(act.metadata or ()).get("package_id")
    }
    assert package_ids == {_GLM_PKG}
    assert _T_STATISTIC not in package_ids


def test_known_but_missing_package_id_does_not_fall_through_to_title() -> None:
    """A known id that cannot be loaded must not silently title-match elsewhere."""
    substance = EducationalSubstancePlanner().plan_for_topic(
        curriculum_identity="CS1:test",
        topic_id="node-x",
        topic_title=_PLACEHOLDER_TITLE,
        educational_package_id="CS1-EP001-PKG-DOES-NOT-EXIST",
        use_campaign_resolution=True,
    )
    assert substance is None


def test_session_rebuild_uses_stored_educational_package_id() -> None:
    """_ensure_sequence rebuild must honour the session binding package id."""
    store = SessionDocumentStore()
    persistence = LearningSessionPersistenceAdapter(store=store)
    lsr = LearningSessionRuntime()
    journey = make_journey(
        topic_id="topic-glm",
        objectives=[make_objective("obj-glm", topic_id="topic-glm")],
    )
    handle = lsr.create_session(journey, session_id="sess-pkg-bind-1")
    handle = lsr.prepare_session(handle)
    handle = lsr.start_session(handle)
    persistence.save_binding(
        student_id="stu-pkg-bind",
        mission_instance_id="m-pkg-bind",
        handle=handle,
        topic_title=_PLACEHOLDER_TITLE,
        topic_id="topic-glm",
        curriculum_identity="CS1:test",
        educational_package_id=_GLM_PKG,
    )

    engine = PackageActivityEngine(store=store, persistence=persistence)
    seq = engine._ensure_sequence(
        "stu-pkg-bind",
        session_id="sess-pkg-bind-1",
        topic_title=_PLACEHOLDER_TITLE,
    )
    assert seq is not None
    assert seq.get("educational_package_id") == _GLM_PKG
    assert seq.get("educational_package_id") != _T_STATISTIC


def test_cross_stage_same_topic_and_package_id_invariant() -> None:
    """Reading, Worked Example, and Practice must share topic_id and package id."""
    store = SessionDocumentStore()
    persistence = LearningSessionPersistenceAdapter(store=store)
    lsr = LearningSessionRuntime()
    journey = make_journey(
        topic_id="topic-cross-stage",
        objectives=[make_objective("obj-cross", topic_id="topic-cross-stage")],
    )
    handle = lsr.create_session(journey, session_id="sess-cross-1")
    handle = lsr.prepare_session(handle)
    handle = lsr.start_session(handle)
    persistence.save_binding(
        student_id="stu-cross",
        mission_instance_id="m-cross",
        handle=handle,
        topic_title=_PLACEHOLDER_TITLE,
        topic_id="topic-cross-stage",
        curriculum_identity="CS1:test",
        educational_package_id=_GLM_PKG,
    )

    engine = PackageActivityEngine(store=store, persistence=persistence)
    # Force rebuild path (no prior sequence).
    seq = engine._ensure_sequence(
        "stu-cross",
        session_id="sess-cross-1",
        topic_title=_PLACEHOLDER_TITLE,
    )
    assert seq is not None
    activities = list(seq.get("activities") or ())
    assert activities

    stages_seen: set[str] = set()
    package_ids: set[str] = set()
    topic_ids: set[str] = {str(seq.get("topic_id") or "")}
    for item in activities:
        stage = str(item.get("stage") or "")
        stages_seen.add(stage)
        meta = item.get("metadata") or {}
        if isinstance(meta, dict):
            pid = str(meta.get("package_id") or "").strip()
        else:
            pid = ""
        # Opaque sequence items may carry package_id at top level too.
        pid = pid or str(item.get("package_id") or "").strip()
        if pid:
            package_ids.add(pid)
        tid = str(item.get("topic_id") or seq.get("topic_id") or "").strip()
        if tid:
            topic_ids.add(tid)

    assert EducationalStage.READ.value in stages_seen
    assert EducationalStage.WORKED_EXAMPLE.value in stages_seen
    assert EducationalStage.PRACTICE.value in stages_seen
    assert package_ids == {_GLM_PKG}
    assert topic_ids == {"topic-cross-stage"}
    assert str(seq.get("educational_package_id") or "") == _GLM_PKG


def test_t_statistic_keywords_no_longer_contain_bare_t() -> None:
    """Catalogue defense: T-STATISTIC must not advertise a single-char keyword."""
    pack = find_package_by_id(_T_STATISTIC)
    assert pack is not None
    lowered = {k.strip().lower() for k in pack.topic_title_keywords}
    assert "t" not in lowered
    assert "t-statistic" in lowered
