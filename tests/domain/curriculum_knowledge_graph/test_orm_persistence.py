"""ORM smoke tests for Curriculum Knowledge Graph persistence."""

from __future__ import annotations

from app.extensions import db
from app.models.curriculum_knowledge_graph import (
    CkgDefinition,
    CkgEdge,
    CkgGraphEdition,
    CkgLearningObjective,
    CkgLoLink,
    CkgSection,
    CkgSubject,
    CkgSubsection,
    CkgTopic,
)


def test_orm_hierarchy_and_links(ctx) -> None:
    edition = CkgGraphEdition(
        edition_id="ckg-cs1-2026",
        subject_code="CS1",
        edition_label="2026",
        provider="IFoA",
        title="Actuarial Statistics",
    )
    subject = CkgSubject(
        stable_id="CS1",
        graph_edition_id="ckg-cs1-2026",
        code="CS1",
        title="Actuarial Statistics",
        provider="IFoA",
        edition_label="2026",
    )
    topic = CkgTopic(
        stable_id="CS1.T04",
        subject_stable_id="CS1",
        code="T04",
        title="Conditional probability",
        display_order=4,
    )
    section = CkgSection(
        stable_id="CS1.T04.S04.02",
        topic_stable_id="CS1.T04",
        code="S04.02",
        title="Bayes theorem",
        display_order=2,
    )
    subsection = CkgSubsection(
        stable_id="CS1.T04.S04.02.SS01",
        section_stable_id="CS1.T04.S04.02",
        code="SS01",
        title="Statement of Bayes",
        display_order=1,
    )
    lo1 = CkgLearningObjective(
        stable_id="CS1.T04.S04.02.SS01.LO01",
        subsection_stable_id="CS1.T04.S04.02.SS01",
        code="LO01",
        statement="State Bayes theorem",
        display_order=1,
    )
    lo3 = CkgLearningObjective(
        stable_id="CS1.T04.S04.02.SS01.LO03",
        subsection_stable_id="CS1.T04.S04.02.SS01",
        code="LO03",
        statement="Apply Bayes theorem",
        display_order=3,
        estimated_study_minutes=45,
    )
    definition = CkgDefinition(
        stable_id="CS1.T04.S04.02.SS01.DEF01",
        owner_stable_id="CS1.T04.S04.02.SS01",
        title="Prior probability",
        body="Operational definition label",
    )
    link = CkgLoLink(
        link_id="link-lo3-def01",
        lo_stable_id="CS1.T04.S04.02.SS01.LO03",
        target_kind="definition",
        target_stable_id="CS1.T04.S04.02.SS01.DEF01",
        relationship_type="references",
    )
    edge = CkgEdge(
        edge_id="edge-lo3-requires-lo1",
        from_stable_id="CS1.T04.S04.02.SS01.LO03",
        to_stable_id="CS1.T04.S04.02.SS01.LO01",
        relationship_type="requires",
    )

    db.session.add_all(
        [
            edition,
            subject,
            topic,
            section,
            subsection,
            lo1,
            lo3,
            definition,
            link,
            edge,
        ]
    )
    db.session.commit()

    loaded = CkgLearningObjective.query.filter_by(
        stable_id="CS1.T04.S04.02.SS01.LO03"
    ).one()
    assert loaded.statement == "Apply Bayes theorem"
    assert loaded.subsection.stable_id == "CS1.T04.S04.02.SS01"
    assert len(loaded.links) == 1
    assert loaded.links[0].target_stable_id == "CS1.T04.S04.02.SS01.DEF01"

    requires = CkgEdge.query.filter_by(relationship_type="requires").one()
    assert requires.from_stable_id == "CS1.T04.S04.02.SS01.LO03"
    assert requires.to_stable_id == "CS1.T04.S04.02.SS01.LO01"

    # Contained topics via relationship
    assert CkgSubject.query.filter_by(stable_id="CS1").one().topics[0].stable_id == (
        "CS1.T04"
    )
