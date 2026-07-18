"""OrchestrationPolicy and ValidationPolicy tests."""

from __future__ import annotations

import pytest

from app.application.education_platform.exceptions import (
    OrchestrationError,
    ValidationError,
)
from app.application.education_platform.policies.orchestration_policy import (
    ALL_WORKFLOWS,
    DEPENDENCY_CHAIN,
    WORKFLOW_BUILD_PLATFORM_SNAPSHOT,
    WORKFLOW_GENERATE_DAILY_MISSIONS,
    WORKFLOW_GENERATE_JOURNEY,
    WORKFLOW_GENERATE_LEARNING_ACTIVITIES,
    WORKFLOW_GENERATE_LEARNING_SESSIONS,
    WORKFLOW_GENERATE_SUBJECT,
    WORKFLOW_VALIDATE_PLATFORM,
    OrchestrationPolicy,
)
from app.application.education_platform.policies.validation_policy import (
    ValidationPolicy,
)


def test_known_workflows_count():
    assert len(OrchestrationPolicy.known_workflows()) == 7


def test_known_workflows_frozen():
    assert isinstance(ALL_WORKFLOWS, frozenset)


@pytest.mark.parametrize("workflow", sorted(ALL_WORKFLOWS))
def test_each_workflow_is_known(workflow):
    assert OrchestrationPolicy.is_known_workflow(workflow)


def test_unknown_workflow_not_known():
    assert OrchestrationPolicy.is_known_workflow("invent_content") is False


def test_steps_unknown_raises():
    with pytest.raises(OrchestrationError):
        OrchestrationPolicy.steps_for("nope")


def test_generate_subject_steps():
    assert OrchestrationPolicy.steps_for(WORKFLOW_GENERATE_SUBJECT) == (
        "curriculum",
    )


def test_generate_journey_steps():
    assert OrchestrationPolicy.steps_for(WORKFLOW_GENERATE_JOURNEY) == (
        "curriculum",
        "blueprint",
        "journey",
    )


def test_generate_sessions_steps():
    assert OrchestrationPolicy.steps_for(
        WORKFLOW_GENERATE_LEARNING_SESSIONS
    ) == ("curriculum", "blueprint", "journey", "session")


def test_generate_activities_steps():
    assert OrchestrationPolicy.steps_for(
        WORKFLOW_GENERATE_LEARNING_ACTIVITIES
    ) == ("curriculum", "blueprint", "journey", "session", "activity")


def test_generate_missions_steps():
    assert OrchestrationPolicy.steps_for(
        WORKFLOW_GENERATE_DAILY_MISSIONS
    ) == DEPENDENCY_CHAIN


def test_snapshot_steps():
    assert OrchestrationPolicy.steps_for(
        WORKFLOW_BUILD_PLATFORM_SNAPSHOT
    ) == DEPENDENCY_CHAIN


def test_validate_steps_empty():
    assert OrchestrationPolicy.steps_for(WORKFLOW_VALIDATE_PLATFORM) == ()


def test_dependency_chain_order():
    assert OrchestrationPolicy.dependency_chain() == (
        "curriculum",
        "blueprint",
        "journey",
        "session",
        "activity",
        "mission",
    )


@pytest.mark.parametrize(
    "workflow,required",
    [
        (WORKFLOW_GENERATE_SUBJECT, {"curriculum"}),
        (WORKFLOW_GENERATE_JOURNEY, {"curriculum", "blueprint", "journey"}),
        (WORKFLOW_VALIDATE_PLATFORM, set()),
    ],
)
def test_required_ports(workflow, required):
    assert OrchestrationPolicy.required_ports(workflow) == frozenset(required)


def test_workflow_ready_subject_with_curriculum_only():
    assert OrchestrationPolicy.workflow_ready(
        WORKFLOW_GENERATE_SUBJECT, registered={"curriculum"}
    )


def test_workflow_ready_subject_without_curriculum():
    assert not OrchestrationPolicy.workflow_ready(
        WORKFLOW_GENERATE_SUBJECT, registered=set()
    )


def test_workflow_ready_unknown():
    assert not OrchestrationPolicy.workflow_ready(
        "unknown", registered=set(DEPENDENCY_CHAIN)
    )


def test_workflow_ready_missions_needs_all():
    partial = set(DEPENDENCY_CHAIN) - {"mission"}
    assert not OrchestrationPolicy.workflow_ready(
        WORKFLOW_GENERATE_DAILY_MISSIONS, registered=partial
    )
    assert OrchestrationPolicy.workflow_ready(
        WORKFLOW_GENERATE_DAILY_MISSIONS, registered=set(DEPENDENCY_CHAIN)
    )


def test_validate_platform_always_ready():
    assert OrchestrationPolicy.workflow_ready(
        WORKFLOW_VALIDATE_PLATFORM, registered=set()
    )


# --- ValidationPolicy ---


@pytest.mark.parametrize("name", list(DEPENDENCY_CHAIN))
def test_assert_port_name_ok(name):
    ValidationPolicy.assert_port_name(name)


def test_assert_port_name_bad():
    with pytest.raises(ValidationError):
        ValidationPolicy.assert_port_name("llm")


def test_assert_no_duplicate_ok():
    ValidationPolicy.assert_no_duplicate("curriculum", registered=set())


def test_assert_no_duplicate_raises():
    with pytest.raises(ValidationError, match="Duplicate"):
        ValidationPolicy.assert_no_duplicate(
            "curriculum", registered={"curriculum"}
        )


def test_assert_no_duplicate_allow_replace():
    ValidationPolicy.assert_no_duplicate(
        "curriculum", registered={"curriculum"}, allow_replace=True
    )


def test_assert_required_ports_present_ok():
    ValidationPolicy.assert_required_ports_present(set(DEPENDENCY_CHAIN))


def test_assert_required_ports_present_raises():
    with pytest.raises(ValidationError, match="Missing"):
        ValidationPolicy.assert_required_ports_present({"curriculum"})


def test_assert_required_ports_custom():
    ValidationPolicy.assert_required_ports_present(
        {"curriculum"}, required=("curriculum",)
    )


def test_assert_workflow_known_ok():
    ValidationPolicy.assert_workflow_known(WORKFLOW_GENERATE_SUBJECT)


def test_assert_workflow_known_bad():
    with pytest.raises(ValidationError):
        ValidationPolicy.assert_workflow_known("ai_tutor")


def test_assert_workflow_ready_ok():
    ValidationPolicy.assert_workflow_ready(
        WORKFLOW_GENERATE_SUBJECT, registered={"curriculum"}
    )


def test_assert_workflow_ready_raises():
    with pytest.raises(ValidationError, match="not ready"):
        ValidationPolicy.assert_workflow_ready(
            WORKFLOW_GENERATE_SUBJECT, registered=set()
        )


def test_composition_integrity_complete():
    issues = ValidationPolicy.assert_composition_integrity(
        set(DEPENDENCY_CHAIN),
        available={n: True for n in DEPENDENCY_CHAIN},
    )
    assert issues == ()


def test_composition_integrity_missing():
    issues = ValidationPolicy.assert_composition_integrity({"curriculum"})
    assert any(i.startswith("missing_port:") for i in issues)
    assert any(i.startswith("workflow_not_ready:") for i in issues)


def test_composition_integrity_unavailable():
    issues = ValidationPolicy.assert_composition_integrity(
        set(DEPENDENCY_CHAIN),
        available={n: (n != "session") for n in DEPENDENCY_CHAIN},
    )
    assert "port_unavailable:session" in issues


def test_composition_integrity_unknown_in_available_raises():
    with pytest.raises(ValidationError):
        ValidationPolicy.assert_composition_integrity(
            set(DEPENDENCY_CHAIN),
            available={"llm": True},
        )


def test_composition_integrity_unknown_registered():
    issues = ValidationPolicy.assert_composition_integrity(
        set(DEPENDENCY_CHAIN) | {"ghost"}
    )
    assert "unknown_registered_port:ghost" in issues


def test_missing_ports_helper():
    assert ValidationPolicy.missing_ports({"curriculum", "blueprint"}) == (
        "journey",
        "session",
        "activity",
        "mission",
    )


def test_required_ports_constant_matches_chain():
    assert ValidationPolicy.REQUIRED_PORTS == DEPENDENCY_CHAIN


def test_policies_package_exports():
    from app.application.education_platform import policies as pol

    assert hasattr(pol, "OrchestrationPolicy")
    assert hasattr(pol, "ValidationPolicy")
    assert hasattr(pol, "DEPENDENCY_CHAIN")
    assert hasattr(pol, "ALL_WORKFLOWS")
