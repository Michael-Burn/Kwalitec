"""Persistence for Educational Reasoning Engine metadata (SDT-002).

Append-only. Does not store Twin mastery/gap/recommendation rows — those remain
in SDT-001 tables via TwinPersistenceService.
"""

from __future__ import annotations

import json
import uuid
from typing import Any

from app.domain.educational_reasoning.decision import EducationalDecision
from app.domain.educational_reasoning.explanation import Explanation
from app.domain.educational_reasoning.reasoning_result import ReasoningResult
from app.domain.educational_reasoning.reasoning_rule import RuleExecution
from app.extensions import db
from app.models.educational_reasoning import (
    DecisionRecord,
    EducationalReasoningRun,
    EducationalRuleExecution,
    ReasoningExplanation,
)


def _dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)


def _loads(raw: str | None, default: Any) -> Any:
    if not raw:
        return default
    return json.loads(raw)


class ReasoningPersistenceService:
    """Append-only persistence for reasoning runs, executions, explanations,
    and decisions.
    """

    def persist_result(self, result: ReasoningResult) -> EducationalReasoningRun:
        """Persist a complete reasoning cycle. Raises if run_id already exists."""
        existing = EducationalReasoningRun.query.filter_by(run_id=result.run_id).first()
        if existing is not None:
            raise ValueError(
                f"reasoning run {result.run_id!r} already persisted (immutable)"
            )

        run = EducationalReasoningRun(
            run_id=result.run_id,
            twin_id=result.twin_id,
            triggered_by=result.triggered_by,
            observation_ids_json=_dumps(list(result.observation_ids)),
            curriculum_evidence_ids_json=_dumps(
                list(result.curriculum_evidence.all_evidence_ids)
            ),
            retrieval_log_ids_json=_dumps(
                list(result.curriculum_evidence.retrieval_log_ids)
            ),
            summary=result.summary,
            engine_version=result.engine_version,
            rule_count=len(result.executions),
            decision_count=len(result.decisions),
            created_at=result.created_at,
        )
        db.session.add(run)
        # Flush parent before children: DecisionRecord / EducationalRuleExecution /
        # ReasoningExplanation FK to educational_reasoning_runs.run_id (unique,
        # non-PK). Without an explicit flush, query-triggered autoflush can INSERT
        # decision_records before the run row exists under PRAGMA foreign_keys=ON.
        db.session.flush()

        for seq, execution in enumerate(result.executions):
            self._persist_execution(result, execution, sequence=seq)

        for decision in result.decisions:
            self._persist_decision(result, decision)

        # Cycle-level explanations (one per rule) plus decision-level if distinct.
        seen_summaries: set[str] = set()
        for execution in result.executions:
            expl = execution.explanation
            key = f"{expl.rule_code}:{expl.summary}"
            if key in seen_summaries:
                continue
            seen_summaries.add(key)
            self._persist_explanation(
                result,
                expl,
                decision_id=None,
                explanation_id=f"expl-{result.run_id}-{execution.rule_code}",
            )

        for decision in result.decisions:
            key = f"dec:{decision.decision_id}"
            if key in seen_summaries:
                continue
            seen_summaries.add(key)
            self._persist_explanation(
                result,
                decision.explanation,
                decision_id=decision.decision_id,
                explanation_id=f"expl-{decision.decision_id}",
            )

        return run

    def get_run(self, run_id: str) -> EducationalReasoningRun | None:
        return EducationalReasoningRun.query.filter_by(run_id=run_id).first()

    def list_runs_for_twin(
        self, twin_id: str, *, limit: int = 50
    ) -> list[EducationalReasoningRun]:
        return (
            EducationalReasoningRun.query.filter_by(twin_id=twin_id)
            .order_by(EducationalReasoningRun.created_at.desc())
            .limit(limit)
            .all()
        )

    def list_executions(self, run_id: str) -> list[EducationalRuleExecution]:
        return (
            EducationalRuleExecution.query.filter_by(run_id=run_id)
            .order_by(EducationalRuleExecution.sequence.asc())
            .all()
        )

    def list_explanations(
        self,
        *,
        twin_id: str | None = None,
        run_id: str | None = None,
        limit: int = 100,
    ) -> list[ReasoningExplanation]:
        q = ReasoningExplanation.query
        if twin_id:
            q = q.filter_by(twin_id=twin_id)
        if run_id:
            q = q.filter_by(run_id=run_id)
        return q.order_by(ReasoningExplanation.created_at.desc()).limit(limit).all()

    def get_decision(self, decision_id: str) -> DecisionRecord | None:
        return DecisionRecord.query.filter_by(decision_id=decision_id).first()

    def list_decisions_for_run(self, run_id: str) -> list[DecisionRecord]:
        return (
            DecisionRecord.query.filter_by(run_id=run_id)
            .order_by(DecisionRecord.created_at.asc())
            .all()
        )

    def run_as_dict(self, run: EducationalReasoningRun) -> dict[str, Any]:
        return {
            "run_id": run.run_id,
            "twin_id": run.twin_id,
            "triggered_by": run.triggered_by,
            "observation_ids": _loads(run.observation_ids_json, []),
            "curriculum_evidence_ids": _loads(run.curriculum_evidence_ids_json, []),
            "retrieval_log_ids": _loads(run.retrieval_log_ids_json, []),
            "summary": run.summary,
            "engine_version": run.engine_version,
            "rule_count": run.rule_count,
            "decision_count": run.decision_count,
            "created_at": run.created_at.isoformat() if run.created_at else None,
            "executions": [
                {
                    "execution_id": e.execution_id,
                    "rule_code": e.rule_code,
                    "rule_name": e.rule_name,
                    "sequence": e.sequence,
                    "inputs": _loads(e.inputs_json, {}),
                    "outputs": _loads(e.outputs_json, {}),
                    "explanation_summary": e.explanation_summary,
                }
                for e in self.list_executions(run.run_id)
            ],
        }

    def decision_as_dict(self, row: DecisionRecord) -> dict[str, Any]:
        return {
            "decision_id": row.decision_id,
            "run_id": row.run_id,
            "twin_id": row.twin_id,
            "kind": row.kind,
            "rule_code": row.rule_code,
            "subject_ref": row.subject_ref,
            "value": row.value,
            "explanation_summary": row.explanation_summary,
            "observation_ids": _loads(row.observation_ids_json, []),
            "curriculum_evidence_ids": _loads(row.curriculum_evidence_ids_json, []),
            "payload": _loads(row.payload_json, {}),
            "created_at": row.created_at.isoformat() if row.created_at else None,
        }

    def explanation_as_dict(self, row: ReasoningExplanation) -> dict[str, Any]:
        return {
            "explanation_id": row.explanation_id,
            "run_id": row.run_id,
            "twin_id": row.twin_id,
            "rule_code": row.rule_code,
            "decision_id": row.decision_id,
            "summary": row.summary,
            "detail": row.detail,
            "observation_ids": _loads(row.observation_ids_json, []),
            "curriculum_evidence_ids": _loads(row.curriculum_evidence_ids_json, []),
            "metadata": _loads(row.metadata_json, {}),
            "created_at": row.created_at.isoformat() if row.created_at else None,
        }

    def _persist_execution(
        self,
        result: ReasoningResult,
        execution: RuleExecution,
        *,
        sequence: int,
    ) -> EducationalRuleExecution:
        row = EducationalRuleExecution(
            execution_id=f"exe-{result.run_id}-{sequence:02d}",
            run_id=result.run_id,
            twin_id=result.twin_id,
            rule_code=execution.rule_code,
            rule_name=execution.rule_name,
            sequence=sequence,
            inputs_json=_dumps(dict(execution.inputs)),
            outputs_json=_dumps(dict(execution.outputs)),
            explanation_summary=execution.explanation.summary,
            created_at=result.created_at,
        )
        db.session.add(row)
        return row

    def _persist_decision(
        self, result: ReasoningResult, decision: EducationalDecision
    ) -> DecisionRecord:
        row = DecisionRecord(
            decision_id=decision.decision_id,
            run_id=result.run_id,
            twin_id=result.twin_id,
            kind=decision.kind.value,
            rule_code=decision.rule_code,
            subject_ref=decision.subject_ref,
            value=decision.value,
            explanation_summary=decision.explanation.summary,
            observation_ids_json=_dumps(list(decision.observation_ids)),
            curriculum_evidence_ids_json=_dumps(
                list(decision.curriculum_evidence_ids)
            ),
            payload_json=_dumps(dict(decision.payload)),
            created_at=decision.created_at,
        )
        db.session.add(row)
        return row

    def _persist_explanation(
        self,
        result: ReasoningResult,
        explanation: Explanation,
        *,
        decision_id: str | None,
        explanation_id: str,
    ) -> ReasoningExplanation:
        # Ensure uniqueness if collision (e.g. re-run edge cases).
        if ReasoningExplanation.query.filter_by(explanation_id=explanation_id).first():
            explanation_id = f"{explanation_id}-{uuid.uuid4().hex[:8]}"
        row = ReasoningExplanation(
            explanation_id=explanation_id,
            run_id=result.run_id,
            twin_id=result.twin_id,
            rule_code=explanation.rule_code,
            decision_id=decision_id,
            summary=explanation.summary,
            detail=explanation.detail,
            observation_ids_json=_dumps(list(explanation.observation_ids)),
            curriculum_evidence_ids_json=_dumps(
                list(explanation.curriculum_evidence_ids)
            ),
            metadata_json=_dumps(dict(explanation.metadata)),
            created_at=result.created_at,
        )
        db.session.add(row)
        return row
