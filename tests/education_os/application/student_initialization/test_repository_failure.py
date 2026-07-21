"""Repository failure and rollback coverage (BR-003)."""

from __future__ import annotations

import pytest

from application.events.twin import DigitalTwinUpdatedApplicationEvent
from application.student_initialization import evidence_id_for_onboarding
from tests.education_os.application.helpers import make_events
from tests.education_os.application.student_initialization import (
    FailingTwinRepository,
    load_evidence,
    load_twin,
    make_completed,
    make_service,
    make_staging_uow,
    make_uow_with_failing_twins,
)


class BoomPipeline:
    """Pipeline stub that fails after Twin/evidence have been staged."""

    def run(self, request):  # noqa: ANN001, ANN201
        raise RuntimeError("pipeline exploded")


def test_repository_failure_rolls_back_and_raises() -> None:
    uow = make_uow_with_failing_twins()
    events = make_events()
    service = make_service(uow=uow, events=events)

    with pytest.raises(RuntimeError, match="repository save failed"):
        service.initialize(make_completed())

    assert uow.commit_count == 0
    assert uow.rollback_count >= 1
    failing = uow.digital_twins
    assert isinstance(failing, FailingTwinRepository)
    assert failing.save_attempts == 1
    assert load_twin(uow, "stu-1") is None
    assert load_evidence(uow, evidence_id_for_onboarding("ob-1")) is None
    assert len(events.of_type(DigitalTwinUpdatedApplicationEvent)) == 0


def test_pipeline_failure_rolls_back_persisted_work() -> None:
    uow = make_staging_uow()
    events = make_events()
    service = make_service(uow=uow, events=events)
    object.__setattr__(service, "_pipeline", BoomPipeline())

    with pytest.raises(RuntimeError, match="pipeline exploded"):
        service.initialize(make_completed())

    assert uow.commit_count == 0
    assert uow.rollback_count >= 1
    assert load_twin(uow, "stu-1") is None
    assert load_evidence(uow, evidence_id_for_onboarding("ob-1")) is None
    assert len(events.of_type(DigitalTwinUpdatedApplicationEvent)) == 0
