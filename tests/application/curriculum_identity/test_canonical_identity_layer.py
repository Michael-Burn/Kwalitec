"""Tests for the canonical curriculum identity layer (first step)."""

from __future__ import annotations

import json

import pytest

from app.application.curriculum_identity import (
    UNKNOWN_CURRICULUM_IDENTITY,
    CurriculumIdentityService,
)
from app.application.curriculum_identity.constants import (
    ACTIVE_CS1_CURRICULUM_VERSION,
    ACTIVE_CS1_STAGE_A_SOURCE_VERSION,
    MAPPING_EXACT,
    MAPPING_OBSOLETE_NO_EQUIVALENT,
    SOURCE_PUBLISHED_CONTENT,
    SOURCE_STAGE_A_DATABASE,
    SOURCE_STUDY_EVENT,
)
from app.application.curriculum_identity.seed_cs1_active import load_cs1_active_seed
from app.application.educational_runtime_engine.service import (
    EducationalRuntimeEngineService,
)
from app.domain.educational_runtime_engine.events import EducationalEventType
from app.extensions import db
from app.models.curriculum import Curriculum, Section, Topic
from app.models.curriculum_identity import CurriculumTopicIdentityMap
from app.models.user import User


def _populate_stage_a_cs1(include_orphans: bool = True) -> Curriculum:
    """Create active IFoA CS1 2026 with 14 sectioned topics matching the seed."""
    seed = load_cs1_active_seed()
    curriculum = Curriculum(exam_name="IFoA CS1", version="2026", active=True)
    db.session.add(curriculum)
    db.session.flush()

    section = Section(
        curriculum_id=curriculum.id,
        official_id="CS1-A",
        code="1",
        title="Data analysis",
        exam_weight=1.0,
        display_order=1,
    )
    db.session.add(section)
    db.session.flush()

    if include_orphans:
        for i, name in enumerate(["T0", "T1", "T2"], start=1):
            db.session.add(
                Topic(
                    curriculum_id=curriculum.id,
                    name=name,
                    order=i,
                    syllabus_weight=1.0,
                    recommended_minutes=30,
                    active=True,
                    section_id=None,
                )
            )

    for index, entry in enumerate(seed["topics"], start=1):
        db.session.add(
            Topic(
                curriculum_id=curriculum.id,
                name=str(entry["title"]),
                order=index,
                syllabus_weight=1.0,
                recommended_minutes=60,
                active=True,
                section_id=section.id,
            )
        )
    db.session.commit()
    return curriculum


@pytest.fixture
def cs1_identity_populated(app, db):
    """Stage A CS1 topics + identity registry/maps ready for assertions."""
    with app.app_context():
        _populate_stage_a_cs1(include_orphans=True)
        counts = CurriculumIdentityService.ensure_active_cs1_populated(
            require_stage_a=True
        )
        assert counts["canonical_inserted"] == 14
        yield


class TestIdentityPopulation:
    def test_registry_and_maps_for_active_syllabus(
        self, app, db, cs1_identity_populated
    ):
        with app.app_context():
            seed = load_cs1_active_seed()
            assert CurriculumIdentityService.active_registry_count() == 14
            assert (
                CurriculumIdentityService.exact_map_count(
                    source_system=SOURCE_PUBLISHED_CONTENT,
                    source_version=ACTIVE_CS1_CURRICULUM_VERSION,
                )
                == 14
            )
            assert (
                CurriculumIdentityService.exact_map_count(
                    source_system=SOURCE_STUDY_EVENT,
                    source_version=ACTIVE_CS1_CURRICULUM_VERSION,
                )
                == 14
            )
            assert (
                CurriculumIdentityService.exact_map_count(
                    source_system=SOURCE_STAGE_A_DATABASE,
                    source_version=ACTIVE_CS1_STAGE_A_SOURCE_VERSION,
                )
                == 14
            )

            orphans = CurriculumTopicIdentityMap.query.filter_by(
                mapping_status=MAPPING_OBSOLETE_NO_EQUIVALENT,
                source_system=SOURCE_STAGE_A_DATABASE,
            ).all()
            assert len(orphans) == 3
            assert all(row.canonical_id is None for row in orphans)

            for entry in seed["topics"]:
                published = CurriculumIdentityService.resolve(
                    source_system=SOURCE_PUBLISHED_CONTENT,
                    source_id=str(entry["published_source_id"]),
                    source_version=ACTIVE_CS1_CURRICULUM_VERSION,
                )
                assert published is not None
                assert published.canonical_id == entry["canonical_id"]
                assert published.mapping_status == MAPPING_EXACT
                assert published.title == entry["title"]

            # Idempotent re-seed inserts nothing new.
            again = CurriculumIdentityService.ensure_active_cs1_populated(
                require_stage_a=True
            )
            assert again["canonical_inserted"] == 0
            assert again["maps_inserted"] == 0


class TestFiveTopicValidationChain:
    """Part 3: show the real resolve chain for five live syllabus topics."""

    SAMPLE_CODES = ("1.1", "2.3", "3.2", "4.1", "5.1")

    def test_five_topic_chain_shown_directly(
        self, app, db, cs1_identity_populated, capsys
    ):
        with app.app_context():
            seed = load_cs1_active_seed()
            by_code = {str(t["syllabus_code"]): t for t in seed["topics"]}
            chains = []
            for code in self.SAMPLE_CODES:
                entry = by_code[code]
                chain = CurriculumIdentityService.chain_for_published(
                    str(entry["published_source_id"])
                )
                stage_topic = db.session.get(Topic, int(chain["stage_a_source_id"]))
                assert stage_topic is not None
                assert stage_topic.name == entry["title"]
                assert chain["canonical_id"] == entry["canonical_id"]
                assert chain["curriculum_version"] == ACTIVE_CS1_CURRICULUM_VERSION
                assert chain["mapping_status"] == MAPPING_EXACT
                chains.append(chain)
                print(
                    f"CHAIN {code}: published={chain['published_source_id']} "
                    f"stage_a_orm={chain['stage_a_source_id']} "
                    f"study_event={chain['study_event_source_id']} "
                    f"canonical={chain['canonical_id']} "
                    f"version={chain['curriculum_version']} "
                    f"status={chain['mapping_status']} "
                    f"title={chain['title']!r}"
                )

            captured = capsys.readouterr().out
            assert "CHAIN 1.1:" in captured
            assert "CHAIN 5.1:" in captured
            assert len(chains) == 5


class TestNewEvidenceFirewall:
    def test_unresolvable_marked_unknown_resolvable_unchanged(
        self, app, db, cs1_identity_populated
    ):
        with app.app_context():
            user = User(email="identity-fw@example.com", is_active_user=True)
            user.set_password("password123")
            db.session.add(user)
            db.session.commit()

            engine = EducationalRuntimeEngineService()

            ok = engine._append_event(
                event_type=EducationalEventType.TOPIC_COMPLETED,
                user_id=user.id,
                curriculum_identity=ACTIVE_CS1_CURRICULUM_VERSION,
                topic_id="topic-t1-1",
                payload={"probe": "ok"},
            )
            assert ok.topic_id == "topic-t1-1"
            assert json.loads(ok.payload_json)["probe"] == "ok"
            assert "unresolved_topic_id" not in json.loads(ok.payload_json)

            bad = engine._append_event(
                event_type=EducationalEventType.TOPIC_COMPLETED,
                user_id=user.id,
                curriculum_identity=ACTIVE_CS1_CURRICULUM_VERSION,
                topic_id="topic-nope-not-real",
                payload={"probe": "bad"},
            )
            assert bad.topic_id == UNKNOWN_CURRICULUM_IDENTITY
            bad_payload = json.loads(bad.payload_json)
            assert bad_payload["probe"] == "bad"
            assert bad_payload["unresolved_topic_id"] == "topic-nope-not-real"

            none_row = engine._append_event(
                event_type=EducationalEventType.STUDENT_ENROLLED,
                user_id=user.id,
                curriculum_identity=ACTIVE_CS1_CURRICULUM_VERSION,
                topic_id=None,
                payload={},
            )
            assert none_row.topic_id is None

            # Unmapped curriculum version: pass through (soft enable).
            other = engine._append_event(
                event_type=EducationalEventType.STUDY_PLAN_INSTANTIATED,
                user_id=user.id,
                curriculum_identity="CS1:2027.1",
                topic_id="topic-t1",
                payload={},
            )
            assert other.topic_id == "topic-t1"

            db.session.commit()

    def test_firewall_helper_direct(self, app, db, cs1_identity_populated):
        with app.app_context():
            tid, payload = CurriculumIdentityService.apply_event_topic_firewall(
                "topic-t3-2",
                ACTIVE_CS1_CURRICULUM_VERSION,
                payload={"x": 1},
            )
            assert tid == "topic-t3-2"
            assert payload == {"x": 1}

            tid2, payload2 = CurriculumIdentityService.apply_event_topic_firewall(
                "ghost-topic",
                ACTIVE_CS1_CURRICULUM_VERSION,
            )
            assert tid2 == UNKNOWN_CURRICULUM_IDENTITY
            assert payload2["unresolved_topic_id"] == "ghost-topic"
