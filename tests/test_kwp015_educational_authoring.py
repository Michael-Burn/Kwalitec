"""KWP-015 — Educational Authoring & Learning Episodes tests.

Educational composition of Learning Episodes, Mission arcs, Tomorrow
Preview, Extra Study, Adaptive Workspace wiring, writing rules, and
founder metrics. Does not redesign Learning Runtime / Evidence /
Progress / EI engines / Memory / Forecast / Knowledge Architecture /
Mission Runtime.
"""

from __future__ import annotations

from pathlib import Path

from app.application.educational_authoring import (
    AuthoringContext,
    EducationalAuthoringEngine,
    EpisodeActivityKind,
    ExtraStudyKind,
    get_educational_authoring_engine,
    reset_educational_authoring_engine,
)
from app.application.educational_authoring.writing import (
    compose_educational_context,
    compose_learning_objective,
    looks_like_cmp_dump,
)
from app.application.knowledge_architecture.graph_adapter import (
    graph_from_topic_specs,
)
from app.presentation.product_language import APPROVED_TERMS
from app.presentation.student.dto.adaptive_workspace import (
    AdaptiveStudyWorkspace,
    WorkspaceLearningEpisode,
    WorkspaceMissionComposition,
    WorkspaceTomorrowPreview,
)
from app.services.educational_authoring_metrics import EducationalAuthoringMetrics

FOUNDER_ALPHA = Path(
    "app/founder/dashboard/templates/founder_dashboard/alpha_observability.html"
)
HOME_TMPL = Path("app/templates/student/home.html")

_FORBIDDEN = (
    "digital twin",
    "evidence authority",
    "pass probability",
    "guaranteed",
    "will definitely",
    "cognitive load",
    "overloaded",
    "badge",
    "leaderboard",
)


def _probability_specs() -> list[dict]:
    return [
        {
            "topic_id": "prob",
            "title": "Probability",
            "difficulty": "foundational",
            "estimated_minutes": 40,
        },
        {
            "topic_id": "cond",
            "title": "Conditional Probability",
            "difficulty": "intermediate",
            "estimated_minutes": 55,
            "prerequisite_ids": ["prob"],
            "high_dependency_on": ["prob"],
        },
        {
            "topic_id": "bayes",
            "title": "Bayes",
            "difficulty": "intermediate",
            "estimated_minutes": 60,
            "prerequisite_ids": ["cond"],
            "high_dependency_on": ["cond"],
            "foundation_of": ["cond"],
        },
    ]


def test_learning_episode_structure_complete() -> None:
    engine = EducationalAuthoringEngine(graph_from_topic_specs(_probability_specs()))
    episode = engine.author_episode(
        AuthoringContext(
            topic_id="cond",
            topic_title="Conditional Probability",
            recently_strengthened_titles=("Probability",),
        )
    )
    assert episode.has_episode
    assert episode.educational_context
    assert episode.learning_objective
    assert 2 <= len(episode.concept_focus) <= 5
    assert episode.activities
    assert episode.success_criteria
    assert episode.estimated_duration_minutes >= 15
    assert episode.connection
    assert "Study Conditional Probability" not in episode.educational_context
    for phrase in _FORBIDDEN:
        blob = " ".join(
            [
                episode.educational_context,
                episode.learning_objective,
                episode.connection,
                *episode.success_criteria,
            ]
        ).lower()
        assert phrase not in blob


def test_writing_rules_reject_cmp_and_compose_tutor_language() -> None:
    assert looks_like_cmp_dump(
        "Candidates should demonstrate learning outcome LO1; CMP extract..."
    )
    bad = compose_learning_objective(
        topic_title="Probability",
        objective_text="Study Probability.",
    )
    assert "Study Probability" not in bad
    good = compose_educational_context(
        topic_title="Conditional Probability",
        foundation_titles=("Probability",),
        successor_titles=("Bayes",),
        recently_strengthened_titles=("Probability",),
    )
    assert "foundations required" in good.lower() or "builds directly" in good.lower()
    assert "Conditional Probability" in good
    assert "Probability" in good


def test_mission_composition_arc() -> None:
    engine = EducationalAuthoringEngine(graph_from_topic_specs(_probability_specs()))
    composition = engine.author_from_topic(
        topic_id="cond",
        topic_title="Conditional Probability",
        tomorrow_topic_title="Bayes",
        tomorrow_effort_minutes=60,
        available_minutes=120,
        revision_available=True,
    )
    assert composition.has_composition
    assert composition.episodes
    assert composition.checkpoint_prompt
    assert composition.reflection_prompt
    assert composition.tomorrow_preview is not None
    assert composition.tomorrow_preview.has_preview
    assert composition.tomorrow_preview.topic_title == "Bayes"
    assert composition.tomorrow_preview.start_early_available
    assert composition.extra_study
    kinds = {o.kind for o in composition.extra_study}
    assert (
        ExtraStudyKind.CONTINUE_REVISION in kinds
        or ExtraStudyKind.START_TOMORROW in kinds
    )


def test_extra_study_only_when_spare_capacity() -> None:
    engine = get_educational_authoring_engine()
    tight = engine.author_from_topic(
        topic_title="Probability",
        estimated_effort_minutes=45,
        available_minutes=50,
        tomorrow_topic_title="Conditional Probability",
        revision_available=True,
    )
    assert tight.has_composition
    assert tight.extra_study == ()

    spare = engine.author_from_topic(
        topic_title="Probability",
        estimated_effort_minutes=45,
        available_minutes=100,
        tomorrow_topic_title="Conditional Probability",
        revision_available=True,
    )
    assert spare.extra_study
    reset_educational_authoring_engine()


def test_alignment_codes_map_to_curriculum() -> None:
    engine = EducationalAuthoringEngine(graph_from_topic_specs(_probability_specs()))
    composition = engine.author_from_topic(
        topic_id="cond",
        topic_title="Conditional Probability",
        objective_ids=("obj-1",),
        subject_code="CM1",
    )
    codes = " ".join(composition.alignment_codes)
    assert "topic:cond" in codes
    assert "subject:CM1" in codes


def test_deterministic_activities() -> None:
    engine = EducationalAuthoringEngine()
    ctx = AuthoringContext(topic_title="Interest Theory", estimated_effort_minutes=40)
    a = engine.author_episode(ctx)
    b = engine.author_episode(ctx)
    assert [x.kind for x in a.activities] == [x.kind for x in b.activities]
    assert EpisodeActivityKind.READ in {x.kind for x in a.activities}
    assert EpisodeActivityKind.PRACTICE in {x.kind for x in a.activities}
    assert EpisodeActivityKind.CHECKPOINT in {x.kind for x in a.activities}


def test_weak_topic_adds_foundation_episode() -> None:
    engine = EducationalAuthoringEngine(graph_from_topic_specs(_probability_specs()))
    composition = engine.author_mission(
        AuthoringContext(
            topic_id="cond",
            topic_title="Conditional Probability",
            weak_topic=True,
            prerequisite_titles=("Probability",),
            estimated_effort_minutes=55,
        )
    )
    assert len(composition.episodes) == 2
    assert composition.episodes[0].sequence == 1
    assert composition.episodes[1].sequence == 2


def test_workspace_dto_holds_mission_composition() -> None:
    episode = WorkspaceLearningEpisode(
        educational_context="Today's session develops foundations.",
        learning_objective="Develop Conditional Probability foundations.",
        concept_focus=("Probability", "Conditional Probability"),
        activity_labels=("Read", "Practice", "Checkpoint"),
        success_criteria=("Explain Probability within Conditional Probability.",),
        estimated_duration_label="55 minutes",
        connection="Tomorrow builds on today's work.",
        has_episode=True,
    )
    composition = WorkspaceMissionComposition(
        mission_narrative=episode.educational_context,
        episodes=(episode,),
        tomorrow_preview=WorkspaceTomorrowPreview(
            topic_title="Bayes",
            continuity_line=(
                "Building directly on today's Conditional Probability work."
            ),
            estimated_duration_label="60 minutes",
            start_early_available=True,
            has_preview=True,
        ),
        has_composition=True,
    )
    workspace = AdaptiveStudyWorkspace(
        mission_composition=composition,
        enabled=True,
    )
    assert workspace.mission_composition is not None
    assert workspace.mission_composition.episodes[0].has_episode
    assert workspace.mission_composition.tomorrow_preview.has_preview


def test_founder_metrics_from_event_counts() -> None:
    snap = EducationalAuthoringMetrics.from_event_counts(
        {
            "mission_completed": 4,
            "episode_completed": 6,
            "episode_started": 8,
            "episode_abandoned": 1,
            "tomorrow_preview_opened": 3,
            "start_tomorrow_used": 2,
            "reflection_completed": 5,
        },
        average_episode_duration_minutes=48.0,
        most_difficult_episodes=("Bayes",),
        most_successful_episodes=("Probability",),
    )
    assert snap.mission_completions == 4
    assert snap.episode_completions == 6
    assert snap.episode_abandonments == 1
    assert snap.tomorrow_preview_opens == 3
    assert snap.start_tomorrow_usage == 2
    assert snap.reflection_completions == 5
    assert snap.average_episode_duration_minutes == 48.0
    assert "Bayes" in snap.most_difficult_episodes


def test_product_language_includes_authoring_terms() -> None:
    for term in (
        "Learning Episode",
        "Educational Authoring",
        "Tomorrow Preview",
        "Extra Study",
    ):
        assert term in APPROVED_TERMS


def test_home_template_surfaces_tomorrow_not_episodes() -> None:
    text = HOME_TMPL.read_text(encoding="utf-8")
    # UX-001: Learning Episode detail moved to Session Overview.
    assert "015-learning-episode" not in text
    assert "015-tomorrow-preview" in text
    assert "015-extra-study" not in text
    assert "Learning Episode" not in text
    assert "Success looks like" not in text


def test_founder_template_has_authoring_section() -> None:
    text = FOUNDER_ALPHA.read_text(encoding="utf-8")
    assert "Educational Authoring" in text
    assert "Tomorrow Preview opens" in text
    assert "Episode completions" in text


def test_no_cmp_dump_in_authored_mission() -> None:
    engine = EducationalAuthoringEngine(graph_from_topic_specs(_probability_specs()))
    composition = engine.author_from_topic(
        topic_id="bayes",
        topic_title="Bayes",
        objective_text=(
            "Candidates should demonstrate learning outcome LO3; "
            "the aim of this unit is CMP coverage of Bayes theorem "
            "and related syllabus objective wording across many clauses; "
            "extra filler to exceed length."
        ),
    )
    primary = composition.primary_episode
    assert primary is not None
    assert "candidates should" not in primary.learning_objective.lower()
    assert "cmp" not in primary.learning_objective.lower()
    assert "Study Bayes" not in primary.educational_context
