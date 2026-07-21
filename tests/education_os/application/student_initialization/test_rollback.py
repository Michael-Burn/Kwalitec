"""Rollback transactional coverage for Student Twin Initialization (BR-003)."""

from __future__ import annotations

import pytest

from application.student_initialization import evidence_id_for_onboarding
from tests.education_os.application.helpers import make_events
from tests.education_os.application.student_initialization import (
    load_evidence,
    load_twin,
    make_completed,
    make_service,
    make_staging_uow,
)


class BoomPipeline:
    def run(self, request):  # noqa: ANN001, ANN201
        raise RuntimeError("pipeline exploded")


def test_uncommitted_unit_rolls_back_on_pipeline_error() -> None:
    uow = make_staging_uow()
    events = make_events()
    service = make_service(uow=uow, events=events)
    object.__setattr__(service, "_pipeline", BoomPipeline())

    with pytest.raises(RuntimeError, match="pipeline exploded"):
        service.initialize(make_completed())

    assert uow.is_active is False
    assert uow.commit_count == 0
    assert uow.rollback_count >= 1
    assert load_twin(uow, "stu-1") is None
    assert load_evidence(uow, evidence_id_for_onboarding("ob-1")) is None
    assert events.events == []
