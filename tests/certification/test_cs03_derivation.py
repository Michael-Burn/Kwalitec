"""CS-03: Educational derivation certification."""

from __future__ import annotations

from app.application.educational_engine_foundation.service import (
    EducationalEngineFoundationService,
)
from tests.certification.pi001d_helpers import publish_certified_subject


class TestEducationalDerivation:
    """Certify artefact derivation from published packages."""

    def test_cs03_1_all_artefacts_derived(self, ctx):
        publish_certified_subject("DER1")
        service = EducationalEngineFoundationService()
        snapshot = service.derive_active("DER1")

        assert snapshot is not None
        assert len(snapshot.sections) >= 1
        assert len(snapshot.topics) >= 1
        assert len(snapshot.objectives) >= 1
        assert snapshot.graph is not None
        assert len(snapshot.graph.topic_ids) >= 1
        assert snapshot.study_plan_template is not None
        assert len(snapshot.study_plan_template.topic_templates) >= 1
        assert len(snapshot.mission_templates) >= 1
        assert snapshot.journey is not None
        assert snapshot.progress_model is not None

    def test_cs03_2_topic_ordering_respects_prerequisites(self, ctx):
        publish_certified_subject("DER2")
        service = EducationalEngineFoundationService()
        snapshot = service.derive_active("DER2")

        topo_order = list(snapshot.graph.topological_order)

        for edge_src, edge_tgt in snapshot.graph.prerequisite_edges:
            if edge_src in topo_order and edge_tgt in topo_order:
                assert topo_order.index(edge_tgt) < topo_order.index(edge_src)

    def test_cs03_4_mission_template_per_topic(self, ctx):
        publish_certified_subject("DER4")
        service = EducationalEngineFoundationService()
        snapshot = service.derive_active("DER4")

        template_topic_ids = {t.topic_id for t in snapshot.mission_templates}
        artefact_topic_ids = {t["topic_id"] for t in snapshot.topics}
        assert template_topic_ids == artefact_topic_ids

    def test_cs03_5_progress_model_completeness(self, ctx):
        publish_certified_subject("DER5")
        service = EducationalEngineFoundationService()
        snapshot = service.derive_active("DER5")

        artefact_topic_ids = {t["topic_id"] for t in snapshot.topics}
        model_topic_ids = set(snapshot.progress_model.topic_ids)
        assert model_topic_ids == artefact_topic_ids

        artefact_obj_ids = {o["objective_id"] for o in snapshot.objectives}
        model_obj_ids = set(snapshot.progress_model.objective_ids)
        assert model_obj_ids == artefact_obj_ids
