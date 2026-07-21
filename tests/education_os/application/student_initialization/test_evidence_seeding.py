"""Evidence seeding coverage for Student Twin Initialization (BR-003)."""

from __future__ import annotations

from application.student_initialization import (
    EvidenceCatalogueSeeder,
    evidence_id_for_onboarding,
)
from domain.education.evidence import EvidenceItemKind, EvidenceSourceKind
from tests.education_os.application.helpers import make_uow
from tests.education_os.application.student_initialization import (
    fixed_completed_at,
    load_evidence,
    make_completed,
    make_declarations,
    make_service,
)


def test_seeds_onboarding_evidence_catalogue() -> None:
    uow = make_uow(with_concept=None)
    service = make_service(uow=uow)

    result = service.initialize(make_completed())

    assert len(result.initial_evidence.records) == 1
    assert result.initial_evidence.primary_evidence_id == (
        evidence_id_for_onboarding("ob-1")
    )
    record = result.initial_evidence.records[0]
    assert record.source.kind is EvidenceSourceKind.REFLECTION_CAPTURE
    assert record.source.channel == "onboarding"
    assert all(item.kind is EvidenceItemKind.REFLECTION for item in record.items)
    observations = {item.observation for item in record.items}
    assert "pathway=core_principles" in observations
    assert "exam_paper=CM1" in observations
    assert "confidence_band=moderate" in observations

    stored = load_evidence(uow, evidence_id_for_onboarding("ob-1"))
    assert stored is not None
    assert stored.student_id == "stu-1"


def test_evidence_seeder_is_deterministic() -> None:
    declarations = make_declarations()
    first = EvidenceCatalogueSeeder.seed(
        declarations, occurred_at=fixed_completed_at()
    )
    second = EvidenceCatalogueSeeder.seed(
        declarations, occurred_at=fixed_completed_at()
    )
    assert first.primary_evidence_id == second.primary_evidence_id
    assert len(first.records[0].items) == len(second.records[0].items)
    assert [i.observation for i in first.records[0].items] == [
        i.observation for i in second.records[0].items
    ]
