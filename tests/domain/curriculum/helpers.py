"""Shared fixtures / builders for Curriculum Graph domain tests."""

from __future__ import annotations

from app.domain.curriculum import (
    Curriculum,
    CurriculumVersion,
    Dependency,
    DependencyType,
    GraphBuilder,
    LearningPath,
    Module,
    Prerequisite,
    RevisionLink,
    Subject,
    Topic,
    TopicDifficulty,
)


def make_topic(
    topic_id: str,
    name: str | None = None,
    *,
    difficulty: TopicDifficulty = TopicDifficulty.FOUNDATIONAL,
    estimated_effort_minutes: int = 30,
    module_id: str | None = None,
    sequence_index: int = 0,
    learning_objective_refs: list[str] | None = None,
) -> Topic:
    return Topic.create(
        topic_id,
        name or topic_id.replace("-", " ").title(),
        difficulty=difficulty,
        estimated_effort_minutes=estimated_effort_minutes,
        module_id=module_id,
        sequence_index=sequence_index,
        learning_objective_refs=learning_objective_refs,
    )


def make_module(
    module_id: str,
    topics: list[Topic],
    *,
    name: str | None = None,
    sequence_index: int = 0,
    subject_id: str | None = None,
) -> Module:
    return Module.create(
        module_id,
        name or module_id,
        topics=topics,
        sequence_index=sequence_index,
        subject_id=subject_id,
    )


def make_subject(
    subject_id: str,
    modules: list[Module],
    *,
    name: str | None = None,
    sequence_index: int = 0,
    curriculum_id: str | None = None,
) -> Subject:
    return Subject.create(
        subject_id,
        name or subject_id,
        modules=modules,
        sequence_index=sequence_index,
        curriculum_id=curriculum_id,
    )


def make_curriculum(
    curriculum_id: str = "demo-curr",
    *,
    subjects: list[Subject] | None = None,
    prerequisites: list[Prerequisite] | None = None,
    dependencies: list[Dependency] | None = None,
    revision_links: list[RevisionLink] | None = None,
    learning_paths: list[LearningPath] | None = None,
    version_label: str = "2026",
) -> Curriculum:
    version = CurriculumVersion.create(curriculum_id, version_label)
    return Curriculum.create(
        curriculum_id,
        f"Programme {curriculum_id}",
        version,
        subjects=subjects or [],
        prerequisites=prerequisites or [],
        dependencies=dependencies or [],
        revision_links=revision_links or [],
        learning_paths=learning_paths or [],
    )


def linear_curriculum() -> Curriculum:
    """A → B → C REQUIRES chain under one subject/module."""
    topics = [
        make_topic("a", "Probability", module_id="m1", sequence_index=0),
        make_topic(
            "b",
            "Random Variables",
            module_id="m1",
            sequence_index=1,
            difficulty=TopicDifficulty.INTERMEDIATE,
        ),
        make_topic(
            "c",
            "Expectation",
            module_id="m1",
            sequence_index=2,
            difficulty=TopicDifficulty.INTERMEDIATE,
        ),
    ]
    module = make_module("m1", topics, subject_id="s1")
    subject = make_subject("s1", [module], curriculum_id="demo-curr")
    prereqs = [
        Prerequisite.create("p1", "b", "a"),
        Prerequisite.create("p2", "c", "b"),
    ]
    path = LearningPath.create(
        "path-prob",
        "Probability path",
        ["a", "b", "c"],
        curriculum_id="demo-curr",
    )
    return make_curriculum(
        "demo-curr",
        subjects=[subject],
        prerequisites=prereqs,
        learning_paths=[path],
    )


def diamond_curriculum() -> Curriculum:
    """Diamond: A→B, A→C, B→D, C→D via REQUIRES."""
    topics = [
        make_topic("a", module_id="m1", sequence_index=0),
        make_topic("b", module_id="m1", sequence_index=1),
        make_topic("c", module_id="m1", sequence_index=2),
        make_topic("d", module_id="m1", sequence_index=3),
    ]
    module = make_module("m1", topics, subject_id="s1")
    subject = make_subject("s1", [module], curriculum_id="diamond")
    deps = [
        Dependency.create("d1", "b", "a", DependencyType.REQUIRES),
        Dependency.create("d2", "c", "a", DependencyType.REQUIRES),
        Dependency.create("d3", "d", "b", DependencyType.REQUIRES),
        Dependency.create("d4", "d", "c", DependencyType.REQUIRES),
    ]
    return make_curriculum("diamond", subjects=[subject], dependencies=deps)


def revision_pair_curriculum() -> Curriculum:
    """Expectation ⇄ Variance revision link plus a third related topic."""
    topics = [
        make_topic("expectation", module_id="m1", sequence_index=0),
        make_topic("variance", module_id="m1", sequence_index=1),
        make_topic("mgf", module_id="m1", sequence_index=2),
    ]
    module = make_module("m1", topics, subject_id="s1")
    subject = make_subject("s1", [module], curriculum_id="rev-curr")
    links = [
        RevisionLink.create("r1", "expectation", "variance"),
    ]
    deps = [
        Dependency.create(
            "rel1", "mgf", "expectation", DependencyType.RELATED
        ),
    ]
    return make_curriculum(
        "rev-curr",
        subjects=[subject],
        revision_links=links,
        dependencies=deps,
    )


def build_graph(curriculum: Curriculum):
    return GraphBuilder().build_from_curriculum(curriculum)
