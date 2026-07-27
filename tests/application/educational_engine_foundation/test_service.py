from __future__ import annotations

from app.application.curriculum_studio_foundation.service import (
    CurriculumStudioFoundationService,
)
from app.application.educational_engine_foundation.service import (
    EducationalEngineFoundationService,
)


def test_service_derives_artefacts_from_active_published_subject(ctx):
    foundation = CurriculumStudioFoundationService()
    engine = EducationalEngineFoundationService()

    foundation.create_subject("LAW1", title="Contract Law", actor_id="founder")
    version = foundation.create_version("LAW1", "2027.1", actor_id="founder")
    structure = {
        "entries": [
            {
                "entry_id": "s1",
                "entry_type": "section",
                "text": "Foundations",
                "number": "1",
            },
            {
                "entry_id": "t1",
                "entry_type": "topic",
                "text": "Offer and acceptance",
                "number": "1.1",
                "parent_ref": "s1",
            },
            {
                "entry_id": "o1",
                "entry_type": "objective",
                "text": "Explain formation basics",
                "number": "1.1.1",
                "parent_ref": "t1",
            },
            {
                "entry_id": "s2",
                "entry_type": "section",
                "text": "Remedies",
                "number": "2",
            },
            {
                "entry_id": "t2",
                "entry_type": "topic",
                "text": "Damages",
                "number": "2.1",
                "parent_ref": "s2",
                "attributes": {"prerequisites": "t1"},
            },
            {
                "entry_id": "o2",
                "entry_type": "objective",
                "text": "Apply damages principles",
                "number": "2.1.1",
                "parent_ref": "t2",
            },
        ]
    }
    foundation.upload_document(
        version.version_id,
        kind="cmp",
        reference="ref://cmp/law1",
        structure=structure,
        actor_id="founder",
    )
    foundation.upload_document(
        version.version_id,
        kind="syllabus",
        reference="ref://syllabus/law1",
        structure=structure,
        actor_id="founder",
    )
    foundation.process_curriculum(version.version_id, actor_id="founder")
    foundation.validate_curriculum(version.version_id, actor_id="founder")
    foundation.founder_review(version.version_id, actor_id="founder")
    foundation.publish_curriculum(version.version_id, actor_id="founder")

    snapshot = engine.derive_active("LAW1")

    assert snapshot is not None
    assert snapshot.curriculum_identity == "LAW1:2027.1"
    assert len(snapshot.sections) == 2
    assert len(snapshot.topics) == 2
    assert len(snapshot.objectives) == 2
    assert snapshot.graph.prerequisite_edges == (("topic-t2", "topic-t1"),)
    assert len(snapshot.study_plan_template.topic_templates) == 2
    assert len(snapshot.mission_templates) == 2
    assert len(snapshot.journey.sections) == 2
    assert len(snapshot.progress_model.topic_ids) == 2
