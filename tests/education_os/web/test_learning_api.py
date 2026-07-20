"""Learning API endpoint tests (WEB-002)."""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest

from application.commands.complete_learning_episode import CompleteLearningEpisode
from application.commands.record_evidence import RecordEvidence
from application.commands.start_learning_session import StartLearningSession
from application.dto.evidence import EvidenceRecordDTO
from application.dto.learner import LearnerStateDTO
from application.dto.learning import LearningEpisodeDTO, LearningSessionDTO
from application.dto.trajectory import LearningTrajectoryDTO, TrajectoryPointDTO
from application.errors import ConflictError, NotFoundError
from application.queries.get_learner_state import GetLearnerState
from application.queries.get_learning_trajectory import GetLearningTrajectory
from web.blueprints.learning import schemas

LEARNING_ROUTES = {
    "/learning/session/start",
    "/learning/episode/complete",
    "/learning/evidence",
    "/learning/state/<student_id>",
    "/learning/trajectory/<student_id>",
}


@pytest.fixture
def services(client):
    """Replace request-scoped application services with mocks."""
    mock_services = MagicMock()
    mock_services.learning = MagicMock()
    mock_services.assessment = MagicMock()
    mock_services.twin = MagicMock()

    @client.application.before_request
    def _bind_mocks() -> None:
        from flask import g

        from web.lifecycle import REQUEST_SCOPE_KEY, RequestScope

        scope = getattr(g, REQUEST_SCOPE_KEY, None)
        if scope is None:
            return
        setattr(
            g,
            REQUEST_SCOPE_KEY,
            RequestScope(unit_of_work=scope.unit_of_work, services=mock_services),
        )

    return mock_services


def test_learning_endpoints_are_registered(app) -> None:
    rules = {rule.rule for rule in app.url_map.iter_rules()}
    assert LEARNING_ROUTES.issubset(rules)


def test_start_session_validates_request_body(client, services) -> None:
    response = client.post("/learning/session/start", json={})

    assert response.status_code == 400
    assert response.get_json() == {"error": "missing or invalid field: episode_id"}
    services.learning.start_learning_session.assert_not_called()


def test_start_session_invokes_service_and_serializes(client, services) -> None:
    services.learning.start_learning_session.return_value = LearningSessionDTO(
        episode_id="episode-001",
        student_id="student-ada",
        status="in_progress",
        first_active_step_id="step-001",
    )

    response = client.post(
        "/learning/session/start",
        json={"episode_id": "episode-001"},
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "episode_id": "episode-001",
        "student_id": "student-ada",
        "status": "in_progress",
        "first_active_step_id": "step-001",
    }
    command = services.learning.start_learning_session.call_args.args[0]
    assert isinstance(command, StartLearningSession)
    assert command.episode_id == "episode-001"


def test_complete_episode_validation_and_status(client, services) -> None:
    response = client.post("/learning/episode/complete", json={"episode_id": "e1"})
    assert response.status_code == 400
    assert "reflection_id" in response.get_json()["error"]

    services.learning.complete_learning_episode.return_value = LearningEpisodeDTO(
        episode_id="episode-001",
        student_id="student-ada",
        status="completed",
        teaching_goal_statement="Goal",
        teaching_strategy_id="strategy-1",
        primary_dimension="understanding",
        step_count=2,
        evidence_count=1,
        has_reflection=True,
        outcome_kind="goal_achieved",
    )
    payload = {
        "episode_id": "episode-001",
        "reflection_id": "reflection-001",
        "reflection_type": "post_episode",
        "reflection_content": "I understand the distinction.",
        "outcome_id": "outcome-001",
        "outcome_kind": "goal_achieved",
        "outcome_summary": "Goal advanced",
    }
    response = client.post("/learning/episode/complete", json=payload)

    assert response.status_code == 200
    body = response.get_json()
    assert body["status"] == "completed"
    assert body["outcome_kind"] == "goal_achieved"
    command = services.learning.complete_learning_episode.call_args.args[0]
    assert isinstance(command, CompleteLearningEpisode)
    assert command.episode_id == "episode-001"


def test_record_evidence_creates_and_serializes(client, services) -> None:
    services.assessment.record_evidence.return_value = EvidenceRecordDTO(
        evidence_id="evidence-001",
        student_id="student-ada",
        status="active",
        strength_level="strong",
        confidence_level="high",
        item_count=1,
        concept_ids=("concept-001",),
        learning_episode_ids=(),
        occurred_at="2026-07-20T10:00:00+00:00",
    )
    payload = {
        "evidence_id": "evidence-001",
        "student_id": "student-ada",
        "source_id": "source-001",
        "source_kind": "assessment",
        "source_label": "Quiz probe",
        "context_id": "ctx-001",
        "context_dimension": "understanding",
        "context_summary": "Post-explanation probe",
        "confidence_level": "high",
        "strength_level": "strong",
        "occurred_at": "2026-07-20T10:00:00Z",
        "items": [
            {
                "item_id": "item-001",
                "kind": "question_response",
                "summary": "Correct discrimination",
                "concept_id": "concept-001",
            }
        ],
        "concept_ids": ["concept-001"],
    }

    response = client.post("/learning/evidence", json=payload)

    assert response.status_code == 201
    body = response.get_json()
    assert body["evidence_id"] == "evidence-001"
    assert body["item_count"] == 1
    assert body["concept_ids"] == ["concept-001"]
    command = services.assessment.record_evidence.call_args.args[0]
    assert isinstance(command, RecordEvidence)
    assert command.occurred_at == datetime(2026, 7, 20, 10, 0, tzinfo=UTC)
    assert len(command.items) == 1


def test_record_evidence_rejects_empty_items(client, services) -> None:
    response = client.post(
        "/learning/evidence",
        json={
            "evidence_id": "evidence-001",
            "student_id": "student-ada",
            "source_id": "source-001",
            "source_kind": "assessment",
            "source_label": "Quiz",
            "context_id": "ctx-001",
            "context_dimension": "understanding",
            "context_summary": "Probe",
            "confidence_level": "high",
            "strength_level": "strong",
            "occurred_at": "2026-07-20T10:00:00Z",
            "items": [],
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "items must be a non-empty list"}
    services.assessment.record_evidence.assert_not_called()


def test_get_state_invokes_twin_service(client, services) -> None:
    services.twin.get_learner_state.return_value = LearnerStateDTO(
        twin_id="twin-001",
        student_id="student-ada",
        learner_state_id="state-001",
        activity_status="engaged",
        twin_status="active",
        concept_count=2,
        evidence_count=3,
        intervention_count=0,
    )

    response = client.get("/learning/state/student-ada")

    assert response.status_code == 200
    assert response.get_json() == {
        "twin_id": "twin-001",
        "student_id": "student-ada",
        "learner_state_id": "state-001",
        "activity_status": "engaged",
        "twin_status": "active",
        "concept_count": 2,
        "evidence_count": 3,
        "intervention_count": 0,
    }
    query = services.twin.get_learner_state.call_args.args[0]
    assert isinstance(query, GetLearnerState)
    assert query.student_id == "student-ada"


def test_get_trajectory_serializes_points(client, services) -> None:
    services.twin.get_learning_trajectory.return_value = LearningTrajectoryDTO(
        twin_id="twin-001",
        student_id="student-ada",
        points=(
            TrajectoryPointDTO(sequence=0, kind="created", label="Twin created"),
            TrajectoryPointDTO(sequence=1, kind="evidence", label="Evidence recorded"),
        ),
    )

    response = client.get("/learning/trajectory/student-ada")

    assert response.status_code == 200
    body = response.get_json()
    assert body["student_id"] == "student-ada"
    assert body["points"] == [
        {"sequence": 0, "kind": "created", "label": "Twin created"},
        {"sequence": 1, "kind": "evidence", "label": "Evidence recorded"},
    ]
    query = services.twin.get_learning_trajectory.call_args.args[0]
    assert isinstance(query, GetLearningTrajectory)
    assert query.student_id == "student-ada"


def test_not_found_maps_to_404(client, services) -> None:
    services.learning.start_learning_session.side_effect = NotFoundError(
        "LearningEpisode",
        "missing",
    )

    response = client.post("/learning/session/start", json={"episode_id": "missing"})

    assert response.status_code == 404
    assert response.get_json() == {
        "error": "LearningEpisode not found: missing",
    }


def test_conflict_maps_to_409(client, services) -> None:
    services.learning.complete_learning_episode.side_effect = ConflictError(
        "episode is not in progress"
    )

    response = client.post(
        "/learning/episode/complete",
        json={
            "episode_id": "episode-001",
            "reflection_id": "reflection-001",
            "reflection_type": "post_episode",
            "reflection_content": "Not ready.",
            "outcome_id": "outcome-001",
            "outcome_kind": "goal_achieved",
            "outcome_summary": "Should conflict",
        },
    )

    assert response.status_code == 409
    assert response.get_json() == {"error": "episode is not in progress"}


def test_schema_rejects_non_object_body() -> None:
    with pytest.raises(Exception, match="JSON object"):
        schemas.parse_start_learning_session([])


def test_schema_parses_complete_optional_fields() -> None:
    command = schemas.parse_complete_learning_episode(
        {
            "episode_id": "episode-001",
            "reflection_id": "reflection-001",
            "reflection_type": "post_episode",
            "reflection_content": "Content",
            "outcome_id": "outcome-001",
            "outcome_kind": "goal_achieved",
            "outcome_summary": "Summary",
            "perceived_difficulty": "medium",
            "perceived_understanding": "high",
        }
    )
    assert command.perceived_difficulty == "medium"
    assert command.perceived_understanding == "high"
