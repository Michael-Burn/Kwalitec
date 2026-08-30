"""Architectural drift detector for the canonical Learner Twin (ADR-027).

Phase 2 Stage 4 implements D1-D5 as callable checks. D2 permanently enforces
that Stack A contains no assignments to the retired Estimated Knowledge
columns. Stack C mastery references remain inventory-only for sandbox retention.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from app.application.student_twin.canonical_topic_id import CanonicalTopicId
from app.application.student_twin.daily_loop_codec import (
    decode_daily_loop_twin,
    encode_daily_loop_twin,
)
from app.application.student_twin.query import TopicKnowledgeFact
from app.application.student_twin.twin_engine import StudentTwinEngine
from app.domain.student_twin.digital_twin import DigitalTwin
from app.domain.student_twin.evidence_event import EvidenceEvent
from app.domain.student_twin.learner import Learner

CODEC_DECIMAL_PLACES = 6

# Paths relative to repo ``app/`` that Stack C sandbox inventory expects.
KNOWN_BASELINE_C_WRITER_FRAGMENTS = (
    "student_digital_twin/persistence.py",
    "student_reasoning_service.py",
)


@dataclass(frozen=True)
class ReplayDriftFinding:
    """One mismatched field from D1 replay comparison."""

    field: str
    persisted: Any
    recalculated: Any


@dataclass(frozen=True)
class ReplayDriftReport:
    """Result of D1 replay determinism check."""

    ok: bool
    findings: tuple[ReplayDriftFinding, ...] = ()

    @property
    def drifted(self) -> bool:
        return not self.ok


@dataclass(frozen=True)
class WriterHit:
    """One detected EK writer reference for D2."""

    path: str
    kind: str
    detail: str


@dataclass(frozen=True)
class WriterInventory:
    """D2 single-writer sentry inventory."""

    hits: tuple[WriterHit, ...] = ()

    @property
    def stack_a_hits(self) -> tuple[WriterHit, ...]:
        return tuple(h for h in self.hits if h.kind.startswith("A:"))

    @property
    def stack_c_hits(self) -> tuple[WriterHit, ...]:
        return tuple(h for h in self.hits if h.kind.startswith("C:"))

    def baseline_writers_present(self) -> bool:
        """True when known retained Stack C sandbox modules appear in hits."""
        paths = " ".join(h.path for h in self.hits)
        return any(frag in paths for frag in KNOWN_BASELINE_C_WRITER_FRAGMENTS)


@dataclass(frozen=True)
class SingleWriterSentryReport:
    """D2 permanent retired-column enforcement result."""

    ok: bool
    cutover_active: bool
    inventory: WriterInventory
    retired_writes: tuple[str, ...] = ()
    mode: str = "enforce"

    @property
    def missing_guards(self) -> tuple[str, ...]:
        """Compatibility alias for pre-cutover sentry consumers."""
        return self.retired_writes


@dataclass(frozen=True)
class IdentityHygieneReport:
    """D3 identity hygiene result."""

    ok: bool
    violations: tuple[str, ...] = ()


@dataclass(frozen=True)
class ScaleReport:
    """D5 unit-interval scale result."""

    ok: bool
    violations: tuple[str, ...] = ()


@dataclass
class DriftDetector:
    """Callable D1-D5 checks for the canonical Learner Twin."""

    engine: StudentTwinEngine = field(default_factory=StudentTwinEngine)
    app_root: Path | None = None

    # --- D1 ------------------------------------------------------------------

    def check_replay_determinism(
        self, document: dict[str, Any]
    ) -> ReplayDriftReport:
        """Reload Twin evidence, recalculate, compare to persisted maps."""
        persisted_knowledge = _float_map(document.get("estimated_knowledge"))
        persisted_mastery = _float_map(document.get("estimated_mastery"))
        persisted_overall_k = _round_opt(document.get("overall_knowledge"))
        persisted_overall_m = _round_opt(document.get("overall_mastery"))

        events = _events_from_document(document)
        twin_id = str(document.get("twin_id") or "").strip() or "twin-replay"
        learner_id = str(document.get("learner_id") or "").strip() or "learner"
        subject = document.get("subject_code")
        subject_code = str(subject).strip() if subject else None

        twin = self.engine.create_twin(
            Learner.create(learner_id),
            twin_id=twin_id,
            subject_code=subject_code,
        )
        if events:
            twin = self.engine.ingest_many(twin, events)
        twin = self.engine.recalculate(twin)

        recalc_knowledge = {
            record.topic_id: round(record.knowledge_score, CODEC_DECIMAL_PLACES)
            for record in twin.knowledge.topic_records
        }
        recalc_mastery = {
            record.topic_id: round(record.mastery_score, CODEC_DECIMAL_PLACES)
            for record in twin.mastery.topic_records
        }
        recalc_overall_k = round(twin.knowledge.overall_score, CODEC_DECIMAL_PLACES)
        recalc_overall_m = round(twin.mastery.overall_score, CODEC_DECIMAL_PLACES)

        findings: list[ReplayDriftFinding] = []
        findings.extend(
            _map_diffs("estimated_knowledge", persisted_knowledge, recalc_knowledge)
        )
        findings.extend(
            _map_diffs("estimated_mastery", persisted_mastery, recalc_mastery)
        )
        if persisted_overall_k != recalc_overall_k:
            findings.append(
                ReplayDriftFinding(
                    "overall_knowledge", persisted_overall_k, recalc_overall_k
                )
            )
        if persisted_overall_m != recalc_overall_m:
            findings.append(
                ReplayDriftFinding(
                    "overall_mastery", persisted_overall_m, recalc_overall_m
                )
            )
        return ReplayDriftReport(ok=not findings, findings=tuple(findings))

    def check_replay_from_twin(self, twin: DigitalTwin) -> ReplayDriftReport:
        """Encode a Twin then run D1 against the opaque document."""
        document = encode_daily_loop_twin(twin)
        return self.check_replay_determinism(document)

    # --- D2 ------------------------------------------------------------------

    def scan_ek_writers(self, *, root: Path | None = None) -> WriterInventory:
        """Scan application code for Stack A/C EK write paths."""
        app_root = root or self.app_root or _default_app_root()
        hits: list[WriterHit] = []
        scan_dirs = (app_root / "services", app_root / "application")
        for directory in scan_dirs:
            if not directory.is_dir():
                continue
            for path in directory.rglob("*.py"):
                # Stage 1/2 twin modules themselves are not writers; skip noise.
                rel = str(path.relative_to(app_root))
                if rel.startswith("application/student_twin/drift_detector"):
                    continue
                if rel.startswith("application/student_twin/query"):
                    continue
                if rel.startswith("application/student_twin/canonical_topic_id"):
                    continue
                if rel.startswith("application/student_twin/cutover"):
                    continue
                text = path.read_text(encoding="utf-8")
                hits.extend(_scan_file_for_writers(rel, text))
        return WriterInventory(hits=tuple(hits))

    def check_single_writer_sentry(
        self,
        *,
        root: Path | None = None,
    ) -> SingleWriterSentryReport:
        """D2: enforce zero Stack A retired EK attribute assignments."""
        inventory = self.scan_ek_writers(root=root)
        retired_writes = tuple(
            f"{hit.path}:{hit.detail}:{hit.kind}"
            for hit in inventory.stack_a_hits
            if hit.kind in {
                "A:attr.mastery_score",
                "A:attr.average_accuracy",
            }
        )
        return SingleWriterSentryReport(
            ok=not retired_writes,
            cutover_active=True,
            inventory=inventory,
            retired_writes=retired_writes,
            mode="enforce",
        )

    # --- D3 ------------------------------------------------------------------

    def check_identity_hygiene(
        self, topic_ids: list[str] | tuple[str, ...] | set[str]
    ) -> IdentityHygieneReport:
        """Reject blank, pure-int, and node- style Twin topic keys."""
        violations = tuple(
            tid
            for tid in topic_ids
            if not CanonicalTopicId.is_hygienic_twin_key(str(tid))
        )
        return IdentityHygieneReport(ok=not violations, violations=violations)

    def check_identity_hygiene_in_document(
        self, document: dict[str, Any]
    ) -> IdentityHygieneReport:
        keys = set(_float_map(document.get("estimated_knowledge")))
        keys |= set(_float_map(document.get("estimated_mastery")))
        return self.check_identity_hygiene(keys)

    # --- D4 ------------------------------------------------------------------

    @staticmethod
    def check_study_progress_not_ek(
        *,
        topic_covered: bool,
        fact: TopicKnowledgeFact,
        twin_has_topic_evidence: bool,
    ) -> bool:
        """Invariant: coverage alone must not mint Estimated Knowledge.

        Returns True when the invariant holds.
        """
        if topic_covered and not twin_has_topic_evidence:
            return fact.has_estimated_knowledge is False
        return True

    # --- D5 ------------------------------------------------------------------

    def check_scale(self, document: dict[str, Any]) -> ScaleReport:
        """All Twin EK/mastery values must lie in [0, 1]."""
        violations: list[str] = []
        for label, raw in (
            ("estimated_knowledge", document.get("estimated_knowledge")),
            ("estimated_mastery", document.get("estimated_mastery")),
        ):
            for topic_id, value in _float_map(raw).items():
                if value < 0.0 or value > 1.0:
                    violations.append(f"{label}[{topic_id}]={value}")
        for label in ("overall_knowledge", "overall_mastery"):
            value = document.get(label)
            if value is None:
                continue
            try:
                numeric = float(value)
            except (TypeError, ValueError):
                violations.append(f"{label}=non-numeric")
                continue
            if numeric < 0.0 or numeric > 1.0:
                violations.append(f"{label}={numeric}")
        return ScaleReport(ok=not violations, violations=tuple(violations))

    def check_scale_from_twin(self, twin: DigitalTwin) -> ScaleReport:
        return self.check_scale(encode_daily_loop_twin(twin))


def _default_app_root() -> Path:
    # app/application/student_twin/drift_detector.py -> app/
    return Path(__file__).resolve().parents[2]


def _round_opt(value: Any) -> float | None:
    if value is None:
        return None
    return round(float(value), CODEC_DECIMAL_PLACES)


def _float_map(raw: Any) -> dict[str, float]:
    if not isinstance(raw, dict):
        return {}
    out: dict[str, float] = {}
    for key, value in raw.items():
        try:
            out[str(key)] = round(float(value), CODEC_DECIMAL_PLACES)
        except (TypeError, ValueError):
            continue
    return out


def _map_diffs(
    label: str,
    persisted: dict[str, float],
    recalculated: dict[str, float],
) -> list[ReplayDriftFinding]:
    findings: list[ReplayDriftFinding] = []
    keys = set(persisted) | set(recalculated)
    for key in sorted(keys):
        left = persisted.get(key)
        right = recalculated.get(key)
        if left != right:
            findings.append(
                ReplayDriftFinding(f"{label}[{key}]", left, right)
            )
    return findings


def _events_from_document(document: dict[str, Any]) -> list[EvidenceEvent]:
    decoded = decode_daily_loop_twin(document)
    if decoded is None:
        return []
    twin, _status = decoded
    return list(twin.history.events)


_A_CALL_PATTERNS = (
    (
        "A:update_mastery_after_attempt",
        re.compile(r"update_mastery_after_attempt\s*\("),
    ),
    ("A:copy_estimate_fields", re.compile(r"_copy_estimate_fields\s*\(")),
    ("A:copy_continuity_fields", re.compile(r"_copy_continuity_fields\s*\(")),
)
_C_CALL_PATTERNS = (
    ("C:replace_inferences", re.compile(r"replace_inferences\s*\(")),
    ("C:SdtMasteryRecord", re.compile(r"\bSdtMasteryRecord\s*\(")),
)
_ASSIGN_ATTRS = frozenset({"mastery_score", "average_accuracy"})


def _scan_file_for_writers(rel: str, text: str) -> list[WriterHit]:
    hits: list[WriterHit] = []
    for kind, pattern in _A_CALL_PATTERNS + _C_CALL_PATTERNS:
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            hits.append(
                WriterHit(path=rel, kind=kind, detail=f"line {line}: {match.group(0)}")
            )

    # Attribute assignments in Stack A services are retired EK column writes.
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return hits

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Attribute) and target.attr in _ASSIGN_ATTRS:
                if "services/" not in rel:
                    continue
                hits.append(
                    WriterHit(
                        path=rel,
                        kind=f"A:attr.{target.attr}",
                        detail=f"line {getattr(node, 'lineno', '?')}",
                    )
                )
    return hits

