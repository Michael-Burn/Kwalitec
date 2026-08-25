"""MISSION-002 / SR-001A P0 — Mission briefing & selection coherence.

Covers unit, integration, regression, and acceptance gates:
- Mission topic ≡ progress current topic ≡ Home why-now topic
- Zero ``node-`` substrings on student-facing mission chrome
- Rationale claims syllabus-order only when selection is syllabus-order
"""

from __future__ import annotations

import json
from datetime import date

import pytest

from app.application.curriculum_intelligence.certified_mission_engine import (
    CertifiedMissionEngine,
)
from app.application.educational_experience.service import EducationalExperienceService
from app.application.educational_runtime_engine.service import (
    EducationalRuntimeEngineService,
)
from app.domain.curriculum_intelligence.certified_learning import (
    MissionSelectionReason,
)
from app.domain.educational_engine_foundation.derivation import (
    EducationalArtefactDeriver,
)
from app.domain.educational_quality.rules import (
    build_mission_educational_rationale,
    build_mission_explanation,
)
from app.domain.educational_runtime_engine.progress import (
    ProgressModelSpec,
    ProgressTopicSpec,
    derive_progress,
)
from app.domain.educational_runtime_engine.student_facing_identity import (
    contains_internal_node_identifier,
    sanitize_student_text,
    student_mission_title,
    student_syllabus_code,
)
from app.extensions import db
from app.models.curriculum_studio_foundation import PublishedCurriculumPackage
from app.presentation.student.educational_view_models import (
    educational_vm,
    page_from_educational_experience,
)
from app.presentation.student.services.student_home_service import StudentHomeService
from app.presentation.student.view_models import (
    ExplanationViewModel,
    HomePageViewModel,
    RecommendationCardViewModel,
)
from tests.certification.pi001d_helpers import make_certified_user

# ── Fixtures: MISSION-001 reproduction shape (uneven LO density) ───────────


def _mission001_package() -> dict:
    """CS1-shaped package: topic 1.1 has 5 LOs; topic 4.2 has 10 LOs.

    Pre-MISSION-002 LO-density scoring selected 4.2 while progress stayed on 1.1.
    """
    topics = []
    objectives = []
    # 1.1 — five objectives (syllabus head)
    t1 = "node-f6efa6549c1cb033"
    topics.append(
        {
            "topic_id": t1,
            "code": t1,
            "title": "1.1 Data Analysis",
            "section_ref": "sec-1",
            "number": "1",
            "order_index": 1,
            "estimated_minutes": 90,
            "difficulty": "foundational",
            "prerequisite_ids": [],
        }
    )
    for i in range(1, 6):
        oid = f"node-lo11{i:02d}aaaaaaaa"
        objectives.append(
            {
                "objective_id": oid,
                "code": oid,
                "text": f"Data analysis objective {i}",
                "topic_ref": t1,
                "number": str(i),
                "order_index": i,
                "estimated_minutes": 20,
            }
        )
    # Intermediate topics with one LO each (display order 2–3)
    for order, (tid, title) in enumerate(
        (
            ("node-bbbbbbbbbbbbbb02", "1.2 Summarising data"),
            ("node-bbbbbbbbbbbbbb03", "2.1 Probability"),
        ),
        start=2,
    ):
        topics.append(
            {
                "topic_id": tid,
                "code": tid,
                "title": title,
                "section_ref": "sec-1",
                "number": str(order),
                "order_index": order,
                "estimated_minutes": 60,
                "difficulty": "intermediate",
                "prerequisite_ids": [],
            }
        )
        oid = f"node-lo{order:02d}aaaaaaaaaa"
        objectives.append(
            {
                "objective_id": oid,
                "code": oid,
                "text": f"{title} objective",
                "topic_ref": tid,
                "number": "1",
                "order_index": 1,
                "estimated_minutes": 20,
            }
        )
    # 4.2 — ten objectives (would win LO-density scoring)
    t42 = "node-8185f5267169ea7d"
    topics.append(
        {
            "topic_id": t42,
            "code": t42,
            "title": "4.2 Understand and use generalised linear models",
            "section_ref": "sec-4",
            "number": "4",
            "order_index": 4,
            "estimated_minutes": 250,
            "difficulty": "advanced",
            "prerequisite_ids": [],
        }
    )
    for i in range(1, 11):
        oid = f"node-lo42{i:02d}aaaaaaaa"
        objectives.append(
            {
                "objective_id": oid,
                "code": oid,
                "text": f"GLM objective {i}",
                "topic_ref": t42,
                "number": str(i),
                "order_index": i,
                "estimated_minutes": 25,
            }
        )
    return {
        "subject_code": "CS1",
        "version_label": "2026.7-mission002",
        "certification": {
            "chain_id": "ei-chain-mission002",
            "snapshot_id": "snap-mission002",
            "status": "certified_with_warnings",
            "authority": "certified_snapshot",
        },
        "structure": {
            "sections": [
                {
                    "section_id": "sec-1",
                    "code": "1",
                    "title": "Section 1",
                    "number": "1",
                    "order_index": 1,
                },
                {
                    "section_id": "sec-4",
                    "code": "4",
                    "title": "Section 4",
                    "number": "4",
                    "order_index": 4,
                },
            ],
            "topics": topics,
            "objectives": objectives,
            "prerequisite_edges": [],
        },
    }


_VERSION_SEQ = 900_002


def _seed_package(package: dict) -> PublishedCurriculumPackage:
    global _VERSION_SEQ
    _VERSION_SEQ += 1
    PublishedCurriculumPackage.query.filter_by(
        subject_code=package["subject_code"], is_active=True
    ).update({"is_active": False})
    row = PublishedCurriculumPackage(
        subject_code=package["subject_code"],
        version_id=_VERSION_SEQ,
        version_label=package["version_label"],
        package_json=json.dumps(package),
        is_active=True,
        published_by="mission002",
    )
    db.session.add(row)
    db.session.commit()
    return row


# ── Unit: student-facing identity ───────────────────────────────────────────


def test_unit_student_syllabus_code_never_returns_node_id():
    assert (
        student_syllabus_code(
            code="node-8185f5267169ea7d",
            title="4.2 Understand and use generalised linear models",
        )
        == "4.2"
    )
    assert student_syllabus_code(code="1.1", title="Data Analysis") == "1.1"
    assert not contains_internal_node_identifier(
        student_mission_title(
            code="node-abc",
            title="1.1 Data Analysis",
        )
    )


def test_unit_sanitize_strips_node_identifiers():
    dirty = (
        "Study node-8185f5267169ea7d — 4.2 GLM. "
        "Published topic node-8185f5267169ea7d (node-8185f5267169ea7d). "
        "Learning objective ids: node-lo4201aaaaaaaa"
    )
    clean = sanitize_student_text(dirty)
    assert "node-" not in clean.lower()
    assert "4.2" in clean or "GLM" in clean


# ── Unit: CertifiedMissionEngine syllabus-order selection ───────────────────


def test_unit_certified_mission_selects_syllabus_head_not_lo_density():
    package = _mission001_package()
    mission = CertifiedMissionEngine().generate(package, mission_id="msn-p0-1")
    assert mission.topic_id == "node-f6efa6549c1cb033"
    assert "1.1" in mission.topic_title
    assert MissionSelectionReason.PROGRESS_ADVANCE in mission.selection_reasons


def test_unit_certified_mission_respects_preferred_topic_id():
    package = _mission001_package()
    mid = "node-bbbbbbbbbbbbbb02"
    mission = CertifiedMissionEngine().generate(
        package,
        preferred_topic_id=mid,
        mission_id="msn-p0-pref",
    )
    assert mission.topic_id == mid


def test_unit_certified_mission_advances_after_completion():
    package = _mission001_package()
    first = "node-f6efa6549c1cb033"
    mission = CertifiedMissionEngine().generate(
        package,
        completed_node_ids=(first,),
        mastered_objective_ids=tuple(
            o["objective_id"]
            for o in package["structure"]["objectives"]
            if o["topic_ref"] == first
        ),
    )
    assert mission.topic_id == "node-bbbbbbbbbbbbbb02"


def test_unit_derivation_humanises_node_codes_in_mission_title():
    package = _mission001_package()
    bundle = EducationalArtefactDeriver().derive(package)
    template = next(
        t
        for t in bundle.mission_templates
        if t.topic_id == "node-f6efa6549c1cb033"
    )
    assert not contains_internal_node_identifier(template.title)
    assert not contains_internal_node_identifier(template.topic_code)
    assert "1.1" in template.title or "Data Analysis" in template.title
    assert "next incomplete topic in syllabus order" in template.educational_rationale
    assert not contains_internal_node_identifier(template.educational_rationale)


def test_unit_mission_explanation_excludes_internal_ids():
    payload = build_mission_explanation(
        topic_id="node-8185f5267169ea7d",
        topic_code="node-8185f5267169ea7d",
        topic_title="4.2 Understand and use generalised linear models",
        objective_ids=("node-lo4201aaaaaaaa",),
        objective_codes=("node-lo4201aaaaaaaa",),
        estimated_duration_minutes=60,
        educational_rationale=build_mission_educational_rationale(
            topic_code="node-8185f5267169ea7d",
            topic_title="4.2 Understand and use generalised linear models",
            objective_codes=("node-lo4201aaaaaaaa",),
            prerequisite_ids=(),
        ),
        prerequisites_satisfied=True,
    )
    blob = " ".join(
        [
            payload["judgement"],
            payload["why_this_mission"],
            *payload["supporting_evidence"],
            payload["expected_benefit"],
            payload["suggested_next_action"],
        ]
    )
    assert "node-" not in blob.lower()
    assert "4.2" in blob


# ── Integration: enrol → generate → experience → Home VM ────────────────────


@pytest.fixture()
def mission002_user(ctx):
    return make_certified_user("mission002@example.com")


def test_integration_mission_matches_progress_and_home_why(
    ctx, mission002_user
):
    package = _mission001_package()
    package["version_label"] = "2026.7-mission002-a"
    _seed_package(package)
    runtime = EducationalRuntimeEngineService()
    runtime.enrol_student(
        user_id=mission002_user.id,
        subject_code="CS1",
        exam_date=date(2026, 12, 1),
    )
    mission = runtime.generate_daily_mission(
        user_id=mission002_user.id,
        subject_code="CS1",
        mission_date=date(2026, 7, 30),
    )
    progress = runtime.get_progress(
        user_id=mission002_user.id,
        subject_code="CS1",
    )
    assert mission.topic_id == progress.current_topic_id
    assert mission.topic_id == "node-f6efa6549c1cb033"
    assert not contains_internal_node_identifier(mission.title)
    # Titles may be package display titles (LO-style) rather than "1.1 — Data Analysis".
    title_l = (mission.title or "").lower()
    assert (
        "1.1" in (mission.title or "")
        or "data analysis" in title_l
    ), mission.title

    experience = EducationalExperienceService().load_for_user(
        mission002_user.id,
        subject_code="CS1",
        mission_date=date(2026, 7, 30),
        ensure_mission=True,
    )
    assert experience is not None
    assert experience.mission is not None
    assert experience.curriculum_position.topic_id == mission.topic_id
    assert "1.1" in experience.journey.why_today or "Data Analysis" in (
        experience.journey.why_today
    )
    assert "4.2" not in experience.journey.why_today
    assert "4.2" not in (experience.mission.title or "")

    student_strings = [
        experience.mission.title,
        experience.mission.why_this_mission,
        experience.mission.educational_rationale,
        *experience.mission.supporting_evidence,
        *experience.mission.learning_objectives,
        experience.curriculum_position.topic_code,
        experience.journey.why_today,
    ]
    for text in student_strings:
        assert not contains_internal_node_identifier(text), text

    page = page_from_educational_experience(experience, surface="home")
    home = page.home
    assert home is not None
    why_now = StudentHomeService._why_now(home)
    assert "1.1" in why_now or "Data Analysis" in why_now
    assert "4.2" not in why_now
    assert not contains_internal_node_identifier(why_now)
    assert not contains_internal_node_identifier(home.primary_mission_title or "")


def test_integration_mid_progress_coherence(ctx, mission002_user):
    package = _mission001_package()
    package["version_label"] = "2026.7-mission002-b"
    _seed_package(package)
    runtime = EducationalRuntimeEngineService()
    runtime.enrol_student(
        user_id=mission002_user.id,
        subject_code="CS1",
        exam_date=date(2026, 12, 1),
    )
    # Topic 1.1 has multiple LOs; one mission may not fully cover it. Keep
    # completing day-missions until progress advances, asserting coherence each step.
    from datetime import timedelta

    day = date(2026, 7, 28)
    first = runtime.generate_daily_mission(
        user_id=mission002_user.id,
        subject_code="CS1",
        mission_date=day,
    )
    assert first.topic_id == "node-f6efa6549c1cb033"
    current = first
    second = None
    for offset in range(1, 8):
        runtime.complete_mission(
            user_id=mission002_user.id,
            mission_instance_id=current.mission_instance_id,
        )
        day = date(2026, 7, 28) + timedelta(days=offset)
        nxt = runtime.generate_daily_mission(
            user_id=mission002_user.id,
            subject_code="CS1",
            mission_date=day,
        )
        progress = runtime.get_progress(
            user_id=mission002_user.id,
            subject_code="CS1",
        )
        assert nxt.topic_id == progress.current_topic_id
        assert not contains_internal_node_identifier(nxt.title)
        if nxt.topic_id != first.topic_id:
            second = nxt
            break
        current = nxt
    assert second is not None, "expected syllabus advance off topic 1.1 within a week"
    assert second.topic_id == "node-bbbbbbbbbbbbbb02"


# ── Unit: Home why_now prefers mission rationale ────────────────────────────


def test_unit_why_now_prefers_mission_rationale_over_timeliness():
    home = HomePageViewModel(
        greeting="Today",
        recommendation=RecommendationCardViewModel(
            title="Study 1.1 — Data Analysis",
            summary="Mission rationale about 1.1",
            has_recommendation=True,
        ),
        explanation=ExplanationViewModel(
            why_recommended=(
                "Today focuses on 1.1 — Data Analysis because it is the next "
                "incomplete topic in syllabus order."
            ),
            timeliness_line=(
                "Today's topic is 4.2 — GLM because it is the next incomplete topic."
            ),
            has_content=True,
        ),
    )
    why = StudentHomeService._why_now(home)
    assert "1.1" in why
    assert "4.2" not in why


# ── Regression: progress derive unchanged for empty stream ──────────────────


def test_regression_empty_progress_current_is_first_incomplete():
    model = ProgressModelSpec(
        curriculum_identity="CS1:test",
        topic_ids=("t1", "t2", "t3"),
        topics=(
            ProgressTopicSpec(topic_id="t1", topic_code="1.1"),
            ProgressTopicSpec(topic_id="t2", topic_code="1.2"),
            ProgressTopicSpec(topic_id="t3", topic_code="4.2"),
        ),
    )
    derived = derive_progress(model, events=())
    assert derived.current_topic_id == "t1"
    assert derived.coverage_ratio == 0.0
    assert derived.completed_topic_ids == ()


def test_regression_ei002b_human_code_fixture_still_selects_first():
    """Existing EI-002B human-code package still picks syllabus head."""
    from tests.application.curriculum_intelligence import (
        test_ei002b_student_intelligence as ei002b,
    )

    mission = CertifiedMissionEngine().generate(ei002b._certified_package())
    assert mission.topic_id == "cs1-t1"


# ── Acceptance: educational_vm single artefact ──────────────────────────────


def test_acceptance_educational_vm_single_topic_story(ctx, mission002_user):
    package = _mission001_package()
    package["version_label"] = "2026.7-mission002-c"
    _seed_package(package)
    runtime = EducationalRuntimeEngineService()
    runtime.enrol_student(
        user_id=mission002_user.id,
        subject_code="CS1",
    )
    snap = EducationalExperienceService().load_for_user(
        mission002_user.id,
        subject_code="CS1",
        mission_date=date(2026, 7, 30),
    )
    assert snap is not None
    edu = educational_vm(snap)
    assert edu is not None
    assert edu.mission_title
    topic_markers = ("1.1", "Data Analysis")
    assert any(m in edu.mission_title for m in topic_markers)
    assert any(m in (edu.today_topic_title or "") for m in topic_markers)
    assert any(m in (edu.why_today or "") for m in topic_markers)
    assert any(
        m in (edu.why_this_mission or edu.mission_rationale or "")
        for m in topic_markers
    )
    for field in (
        edu.mission_title,
        edu.today_topic_code,
        edu.why_today,
        edu.why_this_mission,
        edu.mission_rationale,
        *edu.supporting_evidence,
        *edu.learning_objectives,
    ):
        assert not contains_internal_node_identifier(field or "")
