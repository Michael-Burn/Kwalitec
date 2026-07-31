"""V1S-008 — Educational Integrity & Learning Experience Validation tests.

Architecture frozen (A9). Defect-only fixes for educational quality:
DF-013 xp scrub, DF-016 title/duration continuity, circular success criteria.
"""

from __future__ import annotations

from pathlib import Path

from app.application.educational_authoring import EducationalAuthoringEngine
from app.application.educational_authoring.guidance import scrub
from app.application.educational_authoring.writing import compose_success_criteria
from app.domain.educational_runtime_engine.student_facing_identity import (
    student_mission_title,
    student_syllabus_code,
)
from app.presentation.student.adaptive_workspace import _session_plan
from app.presentation.student.dto.adaptive_workspace import (
    WorkspaceLearningEpisode,
    WorkspaceMissionComposition,
)
from app.presentation.student.dto.student_home import HomeMission
from app.services.dogfood_validation import (
    LEARNING_FRICTION_REGISTER,
    VALIDATION_ISSUES,
    assert_dogfood_registry_integrity,
    open_friction_issues,
)
from app.services.v1_readiness_dashboard import build_v1_readiness_snapshot

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_df013_scrub_preserves_educational_verbs() -> None:
    """xp must never destroy Explain / exploratory / experience / Examples."""
    assert scrub("Explain the purpose and function of data analysis") == (
        "Explain the purpose and function of data analysis"
    )
    assert scrub("Complete exploratory data analysis") == (
        "Complete exploratory data analysis"
    )
    assert scrub("Experience the method") == "Experience the method"
    assert scrub("Examples of variance") == "Examples of variance"
    assert scrub("Earn 50 XP today") == "Earn 50 today"
    assert "streak" not in scrub("Your streak is strong").lower()
    assert scrub("digital twin says hello") == "says hello"
    assert "guaranteed" not in scrub("Results are guaranteed tomorrow").lower()


def test_df013_authored_episode_preserves_explain() -> None:
    engine = EducationalAuthoringEngine()
    composition = engine.author_from_topic(
        topic_id="cs1-1-1",
        topic_title="1.1 Describe the purpose and function of data analysis",
        objective_text="Explain the purpose and function of data analysis.",
        estimated_effort_minutes=45,
        tomorrow_topic_title="1.2 Complete exploratory data analysis",
        tomorrow_effort_minutes=45,
    )
    assert composition.has_composition
    episode = composition.episodes[0]
    blob = " ".join(
        [
            episode.learning_objective,
            episode.educational_context,
            *episode.success_criteria,
            composition.checkpoint_prompt or "",
            composition.reflection_prompt or "",
            (
                composition.tomorrow_preview.topic_title
                if composition.tomorrow_preview
                else ""
            ),
            (
                composition.tomorrow_preview.continuity_line
                if composition.tomorrow_preview
                else ""
            ),
        ]
    )
    assert "Elain" not in blob
    assert "eloratory" not in blob
    assert "eerience" not in blob
    assert "Explain" in blob or "explain" in blob.lower()
    assert "exploratory" in blob.lower()


def test_df016_mission_title_preserves_syllabus_digits() -> None:
    assert student_syllabus_code(code="1", title="1.1 Describe the purpose") == "1.1"
    assert student_mission_title(
        code="1",
        title="1.1 Describe the purpose and function of data analysis",
    ) == (
        "Study 1.1 — Describe the purpose and function of data analysis"
    )
    assert student_mission_title(
        code="1.1",
        title="1.1 Describe the purpose",
    ) == "Study 1.1 — Describe the purpose"
    assert ".1 Describe" not in student_mission_title(
        code="1",
        title="1.1 Describe the purpose",
    )


def test_df016_session_plan_prefers_mission_duration() -> None:
    mission = HomeMission(
        subject_name="CS1",
        objective="Explain the purpose of data analysis.",
        status_label="Ready",
        why_now="Next in syllabus",
        after_completion="Continue tomorrow",
        primary_label="Start Today's Session",
        primary_kind="start_form",
        title="Study 1.1 — Describe the purpose",
        duration_label="45 minutes",
        learning_objective="Explain the purpose of data analysis.",
    )
    composition = WorkspaceMissionComposition(
        has_composition=True,
        total_duration_label="125 minutes",
        episodes=(
            WorkspaceLearningEpisode(
                learning_objective="Explain the purpose of data analysis.",
                estimated_duration_label="125 minutes",
            ),
        ),
    )
    plan = _session_plan(mission, composition=composition)
    assert plan is not None
    assert plan.duration_label == "45 minutes"


def test_no_circular_success_criteria() -> None:
    criteria = compose_success_criteria(
        topic_title="1.1 Describe the purpose and function of data analysis",
        concept_titles=(
            "1.1 Describe the purpose and function of data analysis",
        ),
        objective_text="Explain the purpose and function of data analysis.",
    )
    joined = " ".join(criteria).lower()
    assert "within 1.1 describe the purpose" not in joined
    assert "explain the core ideas" in joined or "complete:" in joined


def test_core_methods_fallback_removed_from_runtime_adapter() -> None:
    source = (
        REPO_ROOT / "app/infrastructure/session/runtime_adapter.py"
    ).read_text(encoding="utf-8")
    assert 'return "Core methods"' not in source
    assert '"Core methods"' not in source


def test_df013_df016_resolved_in_registry() -> None:
    assert_dogfood_registry_integrity()
    by_id = {i.issue_id: i for i in VALIDATION_ISSUES}
    assert by_id["DF-013"].status == "RESOLVED"
    assert by_id["DF-016"].status == "RESOLVED"
    open_p0 = {i.issue_id for i in open_friction_issues() if i.priority == "P0"}
    assert open_p0 == set()
    friction_ids = {r.issue_id for r in LEARNING_FRICTION_REGISTER}
    assert "DF-013" in friction_ids
    assert "DF-016" in friction_ids


def test_v1_readiness_programme_v1s008() -> None:
    snapshot = build_v1_readiness_snapshot()
    assert snapshot.programme == "V1S-008"
    assert (
        "V1S008_EDUCATIONAL_INTEGRITY_VALIDATION_REPORT.md"
        in snapshot.evidence_paths
    )
    open_p0 = [
        i for i in snapshot.learning_friction_open if i.priority == "P0"
    ]
    assert open_p0 == []


def test_release_criteria_mentions_v1s008() -> None:
    text = (REPO_ROOT / "V1_RELEASE_CRITERIA.md").read_text(encoding="utf-8")
    assert "V1S-008" in text or "V1S008" in text
    assert "DF-013" in text
