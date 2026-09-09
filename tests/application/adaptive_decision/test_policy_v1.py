"""ADR-027 Phase 3 Policy V1 dual-path and adaptive selection tests."""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

import pytest

from app.application.adaptive_decision import (
    DecisionOutcome,
    PolicyV0AdaptiveDecisionEngine,
    PolicyV1AdaptiveDecisionEngine,
    SittingDecisionOrchestrator,
)
from app.application.adaptive_decision.policy_v1 import (
    block_weakness_score,
    select_weakest_revision_package,
)
from app.application.adaptive_decision.review_cadence import (
    continuous_review_cadence,
    is_review_day,
)
from app.application.adaptive_decision.types import (
    POLICY_V1_ID,
    POLICY_V1_MIN_EVIDENCE,
    REASON_POLICY_V1_BLOCK_WEAKNESS,
    REASON_POLICY_V1_INSUFFICIENT_EVIDENCE,
    REASON_POLICY_V1_NOT_REVIEW_DAY,
    DailySittingRequest,
)
from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.educational_engine_foundation.dto import (
    EducationalArtefactSnapshot,
    ProgressModelSnapshot,
)
from app.application.educational_packages.loader import (
    packages_for_subject,
    reset_educational_package_cache,
)
from app.application.educational_runtime_engine.service import (
    EducationalRuntimeEngineService,
)
from app.application.student_twin.canonical_topic_id import CanonicalTopicId
from app.application.student_twin.query import (
    LearnerKnowledgeSnapshot,
    TopicKnowledgeFact,
)
from app.domain.educational_runtime_engine.events import EducationalEventType
from app.models.educational_runtime_engine import RuntimeEducationalEvent
from tests.application.adaptive_decision.test_dual_path import (
    _assert_same_identity,
    _legacy_identity,
    _normalize_identity,
    _policy_identity,
)
from tests.application.educational_runtime_engine.helpers import (
    make_user,
    publish_subject,
)

# Published Twin key for sampling-distributions return_targets 2.6.1–2.6.6.
_SAMPLING_TOPIC_ID = "CS1-B-T06"
_REPO_ROOT = Path(__file__).resolve().parents[3]
_CS1_SYLLABUS = (
    _REPO_ROOT / "app" / "curriculum" / "data" / "ifoa" / "cs1" / "2026.json"
)


class _FakeFoundation:
    def __init__(self, snapshot: EducationalArtefactSnapshot | None) -> None:
        self._snapshot = snapshot

    def derive_active(self, subject_code: str):
        return self._snapshot


def _cs1_syllabus_artefacts() -> EducationalArtefactSnapshot:
    """Build foundation artefacts from the live CS1 syllabus taxonomy."""
    data = json.loads(_CS1_SYLLABUS.read_text(encoding="utf-8"))
    topics: list[dict] = []
    objectives: list[dict] = []
    progress_topics: list[dict] = []
    topic_ids: list[str] = []
    for sec in data.get("sections") or ():
        for topic in sec.get("topics") or ():
            tid = str(topic.get("id") or "").strip()
            code = str(topic.get("code") or "").strip()
            if not tid:
                continue
            topic_ids.append(tid)
            topics.append(
                {
                    "topic_id": tid,
                    "code": code,
                    "title": str(topic.get("title") or "").strip(),
                }
            )
            progress_topics.append({"topic_id": tid, "topic_code": code})
            for lo in topic.get("learning_objectives") or ():
                locode = str(lo.get("code") or "").strip()
                if not locode:
                    continue
                objectives.append(
                    {
                        "objective_id": str(lo.get("id") or locode).strip(),
                        "code": locode,
                        "number": locode,
                        "topic_id": str(lo.get("topic_id") or tid).strip(),
                        "text": str(lo.get("description") or "").strip(),
                    }
                )
    return EducationalArtefactSnapshot(
        curriculum_identity="ifoa:cs1:2026",
        subject_code="CS1",
        version_label="2026",
        topics=tuple(topics),
        objectives=tuple(objectives),
        progress_model=ProgressModelSnapshot(
            curriculum_identity="ifoa:cs1:2026",
            topic_ids=tuple(topic_ids),
            topics=tuple(progress_topics),
        ),
    )


def _cs1_canonical() -> CanonicalTopicId:
    return CanonicalTopicId(foundation=_FakeFoundation(_cs1_syllabus_artefacts()))


@dataclass
class _StubTwin:
    """In-memory LearnerTwinQueryPort for Policy V1 unit tests."""

    facts: dict[str, TopicKnowledgeFact]
    covered: set[str]
    user_id: int = 1
    subject_code: str = "CS1"

    def knowledge_snapshot(
        self, *, user_id: int, subject_code: str
    ) -> LearnerKnowledgeSnapshot:
        return LearnerKnowledgeSnapshot(
            user_id=user_id,
            subject_code=subject_code,
            curriculum_identity=None,
            overall_estimated_knowledge=None,
            topics=tuple(self.facts.values()),
        )

    def topic_knowledge(
        self, *, user_id: int, subject_code: str, topic_id: str
    ) -> TopicKnowledgeFact:
        tid = (topic_id or "").strip()
        return self.facts.get(
            tid,
            TopicKnowledgeFact(
                topic_id=tid,
                has_estimated_knowledge=False,
                estimated_knowledge=None,
                estimated_mastery=None,
                evidence_count=0,
                last_practised_at=None,
            ),
        )

    def topics_with_estimated_knowledge(
        self, *, user_id: int, subject_code: str
    ) -> tuple[TopicKnowledgeFact, ...]:
        return tuple(
            f for f in self.facts.values() if f.has_estimated_knowledge
        )

    def topic_covered(
        self, *, user_id: int, subject_code: str, topic_id: str
    ) -> bool:
        return (topic_id or "").strip() in self.covered


def _fact(
    topic_id: str,
    *,
    ek: float | None,
    evidence: int,
    covered_marker: bool = True,
) -> TopicKnowledgeFact:
    del covered_marker  # coverage is separate via stub.covered
    return TopicKnowledgeFact(
        topic_id=topic_id,
        has_estimated_knowledge=ek is not None,
        estimated_knowledge=ek,
        estimated_mastery=ek,
        evidence_count=evidence,
        last_practised_at=datetime(2026, 8, 1) if evidence else None,
    )


# ---------------------------------------------------------------------------
# return_targets surface
# ---------------------------------------------------------------------------


def test_cs1_revision_packages_expose_return_targets():
    reset_educational_package_cache()
    packs = packages_for_subject("CS1", mode="revision")
    assert len(packs) == 19
    for pack in packs:
        assert pack.return_targets, f"{pack.package_id} missing return_targets"
    sampling = next(
        p
        for p in packs
        if p.package_id == "CS1-EP001-PKG-REV-SAMPLING-DISTRIBUTIONS"
    )
    assert sampling.return_targets == (
        "2.6.1",
        "2.6.2",
        "2.6.3",
        "2.6.4",
        "2.6.5",
        "2.6.6",
    )


def test_all_live_return_targets_resolve_to_published_topic_ids():
    """Every authored return_target across the 19 revision packages resolves."""
    reset_educational_package_cache()
    canonical = _cs1_canonical()
    packs = packages_for_subject("CS1", mode="revision")
    assert len(packs) == 19
    failures: list[tuple[str, str]] = []
    resolved: dict[str, str] = {}
    for pack in packs:
        for target in pack.return_targets:
            pub = canonical.resolve_from_runtime_topic_id(
                target, subject_code="CS1"
            )
            if not pub:
                failures.append((pack.package_id, target))
                continue
            resolved[target] = pub
            assert CanonicalTopicId.is_hygienic_twin_key(pub), pub
            assert pub.startswith("CS1-"), pub
    assert failures == []
    assert resolved
    assert resolved["2.6.1"] == _SAMPLING_TOPIC_ID
    assert resolved["1.1"] == "CS1-A-T01"


# ---------------------------------------------------------------------------
# Cadence (continuous interpolation)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("days", "expected"),
    [
        (90, 4.0),
        (60, 4.0),
        (45, 3.5),
        (30, 3.0),
        (21, 2.7),
        (15, 2.5),
        (0, 2.0),
        (-3, 2.0),
    ],
)
def test_continuous_review_cadence_anchors(days, expected):
    assert continuous_review_cadence(days) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("days", "topics", "review"),
    [
        (90, 3, False),
        (90, 4, True),
        (45, 3, False),  # cadence 3.5
        (45, 4, True),
        (30, 2, False),
        (30, 3, True),
        (15, 2, False),  # cadence 2.5
        (15, 3, True),
        (10, 2, False),  # cadence ≈ 2.333
        (10, 3, True),
        (0, 2, True),
        (None, 99, False),  # no exam date
    ],
)
def test_is_review_day_matrix(days, topics, review):
    assert (
        is_review_day(days_remaining=days, topics_since_last_review=topics)
        is review
    )


def test_cadence_is_strictly_tighter_as_exam_nears():
    far = continuous_review_cadence(90)
    six_weeks = continuous_review_cadence(42)
    three_weeks = continuous_review_cadence(21)
    two_weeks = continuous_review_cadence(14)
    assert far > six_weeks > three_weeks > two_weeks >= 2.0


# ---------------------------------------------------------------------------
# Block weakness score (design verification worked example)
# ---------------------------------------------------------------------------


def test_block_weakness_score_sampling_distributions_worked_example():
    """Matches ADR027_PHASE3 verification mean on the real Twin key space.

    Facts are keyed by the published Twin topic id (CS1-B-T06), not LO codes.
    Multiple LO return_targets resolve onto the same Twin fact; mean is that EK.
    """
    facts = {
        _SAMPLING_TOPIC_ID: _fact(_SAMPLING_TOPIC_ID, ek=0.252, evidence=5),
    }
    covered = {_SAMPLING_TOPIC_ID}
    canonical = _cs1_canonical()
    score = block_weakness_score(
        return_targets=(
            "2.6.1",
            "2.6.2",
            "2.6.3",
            "2.6.4",
            "2.6.5",
            "2.6.6",
        ),
        facts_by_topic=facts,
        covered=covered,
        subject_code="CS1",
        canonical=canonical,
    )
    # Three eligible LOs in the original worked example each carried distinct
    # EK; with topic-level Twin keys they share one fact. Mean is that EK.
    assert score == pytest.approx(0.252)


def test_block_weakness_score_resolves_lo_codes_to_published_twin_keys():
    """Regression: LO-shaped return_targets hit Twin facts keyed by topic id."""
    facts = {
        _SAMPLING_TOPIC_ID: _fact(_SAMPLING_TOPIC_ID, ek=0.41, evidence=5),
    }
    # Wrong key space (pre-fix bug): LO-shaped Twin keys must not be required.
    assert "2.6.1" not in facts
    score = block_weakness_score(
        return_targets=("2.6.1", "2.6.2", "2.6.3"),
        facts_by_topic=facts,
        covered={_SAMPLING_TOPIC_ID},
        subject_code="CS1",
        canonical=_cs1_canonical(),
    )
    assert score == pytest.approx(0.41)


def test_study_progress_complete_without_twin_evidence_excluded():
    """Covered + zero Twin evidence never enters the block score."""
    # Two LOs under different topics so coverage/evidence stay distinguishable.
    facts = {
        "CS1-A-T01": _fact("CS1-A-T01", ek=None, evidence=0),
        _SAMPLING_TOPIC_ID: _fact(_SAMPLING_TOPIC_ID, ek=0.5, evidence=3),
    }
    covered = {"CS1-A-T01", _SAMPLING_TOPIC_ID}
    score = block_weakness_score(
        return_targets=("1.1.1", "2.6.1"),
        facts_by_topic=facts,
        covered=covered,
        subject_code="CS1",
        canonical=_cs1_canonical(),
    )
    assert score == pytest.approx(0.5)


def test_select_weakest_revision_package_picks_sampling_over_stronger():
    reset_educational_package_cache()
    packs = packages_for_subject("CS1", mode="revision")
    sampling = next(
        p
        for p in packs
        if p.package_id == "CS1-EP001-PKG-REV-SAMPLING-DISTRIBUTIONS"
    )
    canonical = _cs1_canonical()
    # Sampling is weak on its published Twin topic; another package is strong.
    facts = {
        _SAMPLING_TOPIC_ID: _fact(_SAMPLING_TOPIC_ID, ek=0.252, evidence=5),
    }
    covered = {_SAMPLING_TOPIC_ID}
    other = next(
        p
        for p in packs
        if p.package_id != sampling.package_id and p.return_targets
    )
    other_pub = canonical.resolve_from_runtime_topic_id(
        other.return_targets[0], subject_code="CS1"
    )
    assert other_pub is not None
    if other_pub != _SAMPLING_TOPIC_ID:
        facts[other_pub] = _fact(other_pub, ek=0.90, evidence=5)
        covered.add(other_pub)

    twin = _StubTwin(facts=facts, covered=covered)
    snap = twin.knowledge_snapshot(user_id=1, subject_code="CS1")
    chosen = select_weakest_revision_package(
        packages=packs,
        snapshot=snap,
        twin=twin,
        user_id=1,
        subject_code="CS1",
        canonical=canonical,
    )
    assert chosen is not None
    pack, score, eligible = chosen
    assert pack.package_id == sampling.package_id
    assert score == pytest.approx(0.252)
    assert set(eligible) == {
        "2.6.1",
        "2.6.2",
        "2.6.3",
        "2.6.4",
        "2.6.5",
        "2.6.6",
    }


def test_insufficient_evidence_unchanged_when_twin_keys_are_correct():
    """Honest SAFE_FALLBACK: covered published topic, evidence below floor."""
    reset_educational_package_cache()
    packs = packages_for_subject("CS1", mode="revision")
    twin = _StubTwin(
        facts={
            _SAMPLING_TOPIC_ID: _fact(
                _SAMPLING_TOPIC_ID, ek=0.1, evidence=2
            ),
        },
        covered={_SAMPLING_TOPIC_ID},
    )
    snap = twin.knowledge_snapshot(user_id=1, subject_code="CS1")
    chosen = select_weakest_revision_package(
        packages=packs,
        snapshot=snap,
        twin=twin,
        user_id=1,
        subject_code="CS1",
        canonical=_cs1_canonical(),
    )
    assert chosen is None


def test_policy_v1_unit_tests_use_published_topic_id_fact_keys():
    """Guard: weakness-scoring fixtures must not plant LO-shaped Twin keys."""
    source = Path(__file__).read_text(encoding="utf-8")
    # Detect fact dict entries keyed by LO codes (digit.digit.digit) that call
    # _fact with the same LO string. That pattern masked the Twin key bug.
    lo_fact_key = re.compile(
        r'''["'](\d+\.\d+\.\d+)["']\s*:\s*_fact\(\s*["']\1["']'''
    )
    offenders = lo_fact_key.findall(source)
    assert offenders == [], (
        "Policy V1 tests still plant Twin facts under LO codes: "
        f"{offenders}"
    )


# ---------------------------------------------------------------------------
# Flag defaults / import boundaries
# ---------------------------------------------------------------------------


def test_policy_v1_flag_defaults_off_and_absent_from_render():
    bare = resolve_v2_feature_flags(environ={})
    assert bare.ADR027_POLICY_V1 is False
    loop = resolve_v2_feature_flags(environ={"KWALITEC_COMMERCIAL_LOOP": "1"})
    assert loop.ADR027_POLICY_V1 is False
    on = resolve_v2_feature_flags(environ={"KWALITEC_ADR027_POLICY_V1": "1"})
    assert on.ADR027_POLICY_V1 is True
    render = Path(__file__).resolve().parents[3] / "render.yaml"
    text = render.read_text(encoding="utf-8")
    assert "KWALITEC_ADR027_POLICY_V1" not in text
    assert "ADR027_POLICY_V1" not in text


def test_policy_v1_does_not_import_runtime_a_or_authoring_paths():
    root = Path(__file__).resolve().parents[3]
    adaptive = root / "app" / "application" / "adaptive_decision"
    forbidden_substrings = (
        "planning_service",
        "educational_campaigns",
        "app.mission",
        "app.services.planning",
        "app.infrastructure",
    )
    offenders: list[str] = []
    for path in adaptive.glob("*.py"):
        # Orchestrator may wire the Twin adapter at the composition edge.
        if path.name == "orchestrator.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                names = [node.module or ""]
            for name in names:
                for bad in forbidden_substrings:
                    if bad in name:
                        offenders.append(f"{path.name}:{name}")
    assert offenders == []


def test_policy_v1_content_imports_only_approved_package_loader():
    """AST: Policy V1 may read package metadata via educational_packages only."""
    root = Path(__file__).resolve().parents[3]
    policy = root / "app" / "application" / "adaptive_decision" / "policy_v1.py"
    tree = ast.parse(policy.read_text(encoding="utf-8"))
    edu_imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            if "educational" in node.module or "curriculum" in node.module:
                edu_imports.append(node.module)
    allowed_prefixes = (
        "app.application.educational_packages",
        "app.application.educational_runtime_engine",
        "app.domain.educational_runtime_engine",
        "app.models.educational_runtime_engine",
    )
    assert edu_imports, "expected educational imports"
    for mod in edu_imports:
        assert any(mod.startswith(p) for p in allowed_prefixes), mod
    assert not any("educational_campaigns" in m for m in edu_imports)
    assert not any("curriculum.data" in m for m in edu_imports)


# ---------------------------------------------------------------------------
# Policy V1 decide_daily_sitting paths
# ---------------------------------------------------------------------------


@pytest.fixture()
def runtime(ctx):
    return EducationalRuntimeEngineService()


def test_flag_off_policy_v0_identity_byte_identical(ctx, runtime):
    """Shipped default path: Policy V0 identity matches legacy selection."""
    assert resolve_v2_feature_flags(environ={}).ADR027_POLICY_V1 is False
    user = make_user("v1-off@example.com")
    subject = publish_subject("V1OFF")
    runtime.enrol_student(user_id=user.id, subject_code=subject)
    engine = PolicyV0AdaptiveDecisionEngine(runtime=runtime)
    day = date(2026, 8, 1)
    legacy = _legacy_identity(
        runtime, user_id=user.id, subject_code=subject, mission_date=day
    )
    policy = _policy_identity(
        engine, user_id=user.id, subject_code=subject, mission_date=day
    )
    _assert_same_identity(legacy, policy, case="flag_off_v0")


def test_zero_evidence_review_day_safe_fallback_matches_v0(ctx, runtime):
    """Real-world empty Twin: review day still SAFE_FALLBACK to Policy V0 pick."""
    user = make_user("v1-zero@example.com")
    subject = publish_subject("V1ZERO")
    journey = runtime.enrol_student(
        user_id=user.id,
        subject_code=subject,
        exam_date=date(2026, 8, 20),
    )
    enrolment = journey.enrolment
    day = date(2026, 8, 1)
    v0 = PolicyV0AdaptiveDecisionEngine(runtime=runtime)
    v1 = PolicyV1AdaptiveDecisionEngine(
        runtime=runtime,
        twin=_StubTwin(facts={}, covered=set()),
        v0=v0,
        canonical=_cs1_canonical(),
    )
    # Force review day via watermark without Twin evidence.
    v1._topics_since_last_review = lambda request: 10  # type: ignore[method-assign]
    request = DailySittingRequest(
        user_id=user.id,
        subject_code=subject,
        mission_date=day,
        curriculum_identity=enrolment.curriculum_identity,
        exam_date=enrolment.exam_date,
    )
    d0 = v0.decide_daily_sitting(request)
    d1 = v1.decide_daily_sitting(request)
    assert d1.outcome == DecisionOutcome.SAFE_FALLBACK
    assert d1.policy_id == POLICY_V1_ID
    assert REASON_POLICY_V1_INSUFFICIENT_EVIDENCE in d1.reason_codes
    assert d1.outcome != DecisionOutcome.ADAPTIVE
    assert _normalize_identity(
        {
            "topic_id": d0.topic_id,
            "educational_package_id": d0.educational_package_id,
            "certified_mission_id": d0.certified_mission_id,
            "objective_ids": tuple(d0.objective_ids),
            "blocked": False,
            "block_reason": None,
        }
    ) == _normalize_identity(
        {
            "topic_id": d1.topic_id,
            "educational_package_id": d1.educational_package_id,
            "certified_mission_id": d1.certified_mission_id,
            "objective_ids": tuple(d1.objective_ids),
            "blocked": False,
            "block_reason": None,
        }
    )


def test_not_review_day_defers_to_v0(ctx, runtime):
    user = make_user("v1-nr@example.com")
    subject = publish_subject("V1NR")
    journey = runtime.enrol_student(
        user_id=user.id,
        subject_code=subject,
        exam_date=date(2026, 12, 1),
    )
    enrolment = journey.enrolment
    day = date(2026, 8, 1)
    v0 = PolicyV0AdaptiveDecisionEngine(runtime=runtime)
    twin = _StubTwin(
        facts={
            _SAMPLING_TOPIC_ID: _fact(
                _SAMPLING_TOPIC_ID, ek=0.1, evidence=5
            )
        },
        covered={_SAMPLING_TOPIC_ID},
    )
    v1 = PolicyV1AdaptiveDecisionEngine(
        runtime=runtime,
        twin=twin,
        v0=v0,
        canonical=_cs1_canonical(),
    )
    v1._topics_since_last_review = lambda request: 0  # type: ignore[method-assign]
    request = DailySittingRequest(
        user_id=user.id,
        subject_code=subject,
        mission_date=day,
        curriculum_identity=enrolment.curriculum_identity,
        exam_date=enrolment.exam_date,
    )
    d1 = v1.decide_daily_sitting(request)
    assert d1.outcome == DecisionOutcome.SAFE_FALLBACK
    assert d1.policy_id == POLICY_V1_ID
    assert REASON_POLICY_V1_NOT_REVIEW_DAY in d1.reason_codes
    assert d1.selection_trace.get("policy_v1_review_day") is False


def test_adaptive_recorded_only_when_evidence_backed_selection(
    ctx, runtime, monkeypatch
):
    reset_educational_package_cache()
    # Test enrolment subjects have no revision inventory; use CS1 packs.
    monkeypatch.setattr(
        "app.application.adaptive_decision.policy_v1.packages_for_subject",
        lambda subject_id, mode=None: packages_for_subject("CS1", mode=mode),
    )
    user = make_user("v1-adapt@example.com")
    subject = publish_subject("V1AD")
    journey = runtime.enrol_student(
        user_id=user.id,
        subject_code=subject,
        exam_date=date(2026, 8, 20),
    )
    enrolment = journey.enrolment
    day = date(2026, 8, 1)
    facts = {
        _SAMPLING_TOPIC_ID: _fact(_SAMPLING_TOPIC_ID, ek=0.252, evidence=5),
    }
    twin = _StubTwin(facts=facts, covered={_SAMPLING_TOPIC_ID})
    v0 = PolicyV0AdaptiveDecisionEngine(runtime=runtime)
    v1 = PolicyV1AdaptiveDecisionEngine(
        runtime=runtime,
        twin=twin,
        v0=v0,
        canonical=_cs1_canonical(),
    )
    v1._topics_since_last_review = lambda request: 10  # type: ignore[method-assign]
    request = DailySittingRequest(
        user_id=user.id,
        subject_code=subject,
        mission_date=day,
        curriculum_identity=enrolment.curriculum_identity,
        exam_date=enrolment.exam_date,
    )
    decision = v1.decide_daily_sitting(request)
    assert decision.outcome == DecisionOutcome.ADAPTIVE
    assert decision.policy_id == POLICY_V1_ID
    assert decision.educational_package_id == (
        "CS1-EP001-PKG-REV-SAMPLING-DISTRIBUTIONS"
    )
    assert decision.educational_package_mode == "revision"
    assert REASON_POLICY_V1_BLOCK_WEAKNESS in decision.reason_codes
    assert decision.selection_trace.get("adaptive_selected") is True
    assert decision.selection_trace.get("weakness_score") == pytest.approx(
        0.252
    )


def test_adaptive_never_when_covered_but_below_evidence_floor(ctx, runtime):
    user = make_user("v1-floor@example.com")
    subject = publish_subject("V1FL")
    journey = runtime.enrol_student(
        user_id=user.id,
        subject_code=subject,
        exam_date=date(2026, 8, 20),
    )
    enrolment = journey.enrolment
    twin = _StubTwin(
        facts={
            _SAMPLING_TOPIC_ID: _fact(
                _SAMPLING_TOPIC_ID, ek=0.1, evidence=2
            ),
        },
        covered={_SAMPLING_TOPIC_ID},
    )
    v1 = PolicyV1AdaptiveDecisionEngine(
        runtime=runtime,
        twin=twin,
        v0=PolicyV0AdaptiveDecisionEngine(runtime=runtime),
        canonical=_cs1_canonical(),
    )
    v1._topics_since_last_review = lambda request: 10  # type: ignore[method-assign]
    decision = v1.decide_daily_sitting(
        DailySittingRequest(
            user_id=user.id,
            subject_code=subject,
            mission_date=date(2026, 8, 1),
            curriculum_identity=enrolment.curriculum_identity,
            exam_date=enrolment.exam_date,
        )
    )
    assert decision.outcome == DecisionOutcome.SAFE_FALLBACK
    assert decision.outcome != DecisionOutcome.ADAPTIVE
    assert REASON_POLICY_V1_INSUFFICIENT_EVIDENCE in decision.reason_codes


def test_exam_date_threaded_on_orchestrator_request(ctx, runtime, monkeypatch):
    user = make_user("v1-exam@example.com")
    subject = publish_subject("V1EX")
    exam = date(2026, 9, 15)
    runtime.enrol_student(
        user_id=user.id, subject_code=subject, exam_date=exam
    )
    captured: list[DailySittingRequest] = []

    class _CaptureEngine:
        def decide_daily_sitting(self, request: DailySittingRequest):
            captured.append(request)
            return PolicyV0AdaptiveDecisionEngine(
                runtime=runtime
            ).decide_daily_sitting(request)

    orch = SittingDecisionOrchestrator(
        runtime=runtime, engine=_CaptureEngine()
    )
    orch.ensure_todays_sitting(
        user_id=user.id,
        subject_code=subject,
        mission_date=date(2026, 8, 1),
    )
    assert captured
    assert captured[0].exam_date == exam


def test_orchestrator_materialises_adaptive_under_policy_v1(
    ctx, runtime, monkeypatch
):
    reset_educational_package_cache()
    monkeypatch.setattr(
        "app.application.adaptive_decision.policy_v1.packages_for_subject",
        lambda subject_id, mode=None: packages_for_subject("CS1", mode=mode),
    )
    user = make_user("v1-mat@example.com")
    subject = publish_subject("V1MAT")
    journey = runtime.enrol_student(
        user_id=user.id,
        subject_code=subject,
        exam_date=date(2026, 8, 20),
    )
    facts = {
        _SAMPLING_TOPIC_ID: _fact(_SAMPLING_TOPIC_ID, ek=0.252, evidence=5),
    }
    twin = _StubTwin(facts=facts, covered={_SAMPLING_TOPIC_ID})
    engine = PolicyV1AdaptiveDecisionEngine(
        runtime=runtime,
        twin=twin,
        v0=PolicyV0AdaptiveDecisionEngine(runtime=runtime),
        canonical=_cs1_canonical(),
    )
    engine._topics_since_last_review = lambda request: 10  # type: ignore[method-assign]
    orch = SittingDecisionOrchestrator(runtime=runtime, engine=engine)
    mission = orch.ensure_todays_sitting(
        user_id=user.id,
        subject_code=subject,
        mission_date=date(2026, 8, 1),
    )
    assert (
        mission.educational_package_id
        == "CS1-EP001-PKG-REV-SAMPLING-DISTRIBUTIONS"
    )
    rows = RuntimeEducationalEvent.query.filter_by(
        user_id=user.id,
        event_type=EducationalEventType.DECISION_RECORDED.value,
    ).all()
    assert rows
    payload = json.loads(rows[-1].payload_json or "{}")
    assert payload["outcome"] == DecisionOutcome.ADAPTIVE.value
    assert payload["policy_id"] == POLICY_V1_ID
    assert payload["educational_package_id"] == (
        "CS1-EP001-PKG-REV-SAMPLING-DISTRIBUTIONS"
    )
    assert journey.enrolment.enrolment_id


def test_min_evidence_constant_matches_design():
    assert POLICY_V1_MIN_EVIDENCE == 3


def test_daily_sitting_request_exam_date_optional_nonbreaking():
    """Existing positional construction still works; exam_date defaults None."""
    req = DailySittingRequest(
        user_id=1,
        subject_code="CS1",
        mission_date=date(2026, 8, 1),
        curriculum_identity="id",
    )
    assert req.exam_date is None
    req2 = DailySittingRequest(
        user_id=1,
        subject_code="CS1",
        mission_date=date(2026, 8, 1),
        curriculum_identity="id",
        exam_date=date(2026, 10, 1),
    )
    assert req2.exam_date == date(2026, 10, 1)
