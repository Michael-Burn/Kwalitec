"""Twin creation coverage for Student Twin Initialization (BR-003)."""

from __future__ import annotations

from application.events.twin import DigitalTwinUpdatedApplicationEvent
from application.student_initialization import evidence_id_for_onboarding
from domain.education.digital_twin import TwinStatus
from domain.education.foundation.enums import ConfidenceLevel
from tests.education_os.application.helpers import make_events, make_uow
from tests.education_os.application.student_initialization import (
    make_completed,
    make_declarations,
    make_service,
)


def test_creates_active_student_twin() -> None:
    uow = make_uow(with_concept=None)
    events = make_events()
    service = make_service(uow=uow, events=events)

    result = service.initialize(make_completed())

    assert result.twin_id == "twin-onboarding-ob-1"
    assert result.student_id == "stu-1"
    assert result.student_twin.status is TwinStatus.ACTIVE
    assert result.student_twin.confidence.overall is ConfidenceLevel.MEDIUM
    assert result.idempotent_replay is False

    stored = uow.digital_twins.get_by_student("stu-1")
    assert stored is not None
    assert stored.twin_id.value == result.twin_id
    assert stored.has_evidence(evidence_id_for_onboarding("ob-1"))

    published = events.of_type(DigitalTwinUpdatedApplicationEvent)
    assert len(published) == 1
    assert published[0].update_kind == "initialized"


def test_confidence_band_maps_onto_twin_prior() -> None:
    service = make_service()
    result = service.initialize(
        make_completed(
            declarations=make_declarations(confidence_band="low"),
        )
    )
    assert result.student_twin.confidence.overall is ConfidenceLevel.LOW
