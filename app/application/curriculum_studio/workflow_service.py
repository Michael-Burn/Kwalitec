"""WorkflowService — Founder workflow stage transitions with readiness gates."""

from __future__ import annotations

from app.application.curriculum_studio._registry import StudioRegistry
from app.application.curriculum_studio._snapshots import workflow_snapshot
from app.application.curriculum_studio.dto.workflow_snapshot import WorkflowSnapshot
from app.application.curriculum_studio.exceptions import (
    WorkflowError,
    WorkflowGateBlocked,
    WorkspaceNotFound,
)
from app.domain.curriculum_studio.publication_checklist import ChecklistItemCode
from app.domain.curriculum_studio.studio_workflow import (
    WorkflowTransitionEvent,
    next_workflow_state,
)
from app.domain.curriculum_studio.workflow_stage import (
    WorkflowStage,
    next_stage,
    previous_stage,
)

# Required checklist facts before ADVANCING into each target stage.
_ADVANCE_GATES: dict[WorkflowStage, tuple[ChecklistItemCode, ...]] = {
    WorkflowStage.CONTENT_SOURCES: (),
    WorkflowStage.VALIDATION: (
        ChecklistItemCode.CMP_UPLOADED,
        ChecklistItemCode.OFFICIAL_SYLLABUS_UPLOADED,
    ),
    WorkflowStage.PREVIEW: (ChecklistItemCode.VALIDATION_PASSED,),
    WorkflowStage.APPROVAL: (ChecklistItemCode.PREVIEW_APPROVED,),
    WorkflowStage.PUBLICATION: (
        ChecklistItemCode.PREVIEW_APPROVED,
        ChecklistItemCode.VERSION_ASSIGNED,
    ),
}


class WorkflowService:
    """Drive Founder workflow stages for Curriculum Studio workspaces."""

    def __init__(self, registry: StudioRegistry) -> None:
        self._registry = registry

    def get_workflow(self, workspace_id: str) -> WorkflowSnapshot:
        """Return the workflow snapshot for a workspace."""
        workspace = self._require_workspace(workspace_id)
        assert workspace.workflow is not None
        return workflow_snapshot(
            workspace.workflow,
            can_advance=self._can_advance(workspace),
            can_retreat=previous_stage(workspace.current_stage) is not None,
        )

    def advance(
        self,
        workspace_id: str,
        *,
        actor_id: str | None = None,
        occurred_at: str = "",
        reason: str = "",
    ) -> WorkflowSnapshot:
        """Advance to the next stage when readiness gates pass."""
        workspace = self._require_workspace(workspace_id)
        assert workspace.workflow is not None
        target = next_stage(workspace.current_stage)
        if target is None:
            raise WorkflowError("Already at terminal publication stage")
        self._assert_advance_gates(workspace, target)
        updated_wf = workspace.workflow.with_transition(
            WorkflowTransitionEvent.ADVANCE,
            occurred_at=occurred_at,
            actor_id=actor_id,
            reason=reason or f"advance_to_{target.value}",
        )
        self._registry.put_workspace(workspace.with_workflow(updated_wf))
        return self.get_workflow(workspace_id)

    def retreat(
        self,
        workspace_id: str,
        *,
        actor_id: str | None = None,
        occurred_at: str = "",
        reason: str = "",
    ) -> WorkflowSnapshot:
        """Retreat to the previous stage."""
        workspace = self._require_workspace(workspace_id)
        assert workspace.workflow is not None
        if previous_stage(workspace.current_stage) is None:
            raise WorkflowError("Already at subject stage")
        updated_wf = workspace.workflow.with_transition(
            WorkflowTransitionEvent.RETREAT,
            occurred_at=occurred_at,
            actor_id=actor_id,
            reason=reason or "retreat",
        )
        self._registry.put_workspace(workspace.with_workflow(updated_wf))
        return self.get_workflow(workspace_id)

    def transition(
        self,
        workspace_id: str,
        event: WorkflowTransitionEvent | str,
        *,
        actor_id: str | None = None,
        occurred_at: str = "",
        reason: str = "",
        enforce_gates: bool = True,
    ) -> WorkflowSnapshot:
        """Apply an explicit workflow transition event."""
        workspace = self._require_workspace(workspace_id)
        assert workspace.workflow is not None
        try:
            target = next_workflow_state(workspace.current_stage, event)
        except ValueError as exc:
            raise WorkflowError(str(exc)) from exc
        if enforce_gates and stage_is_forward(
            workspace.current_stage, target
        ):
            self._assert_advance_gates(workspace, target)
        updated_wf = workspace.workflow.with_transition(
            event,
            occurred_at=occurred_at,
            actor_id=actor_id,
            reason=reason,
        )
        self._registry.put_workspace(workspace.with_workflow(updated_wf))
        return self.get_workflow(workspace_id)

    def reset(
        self,
        workspace_id: str,
        *,
        actor_id: str | None = None,
        occurred_at: str = "",
    ) -> WorkflowSnapshot:
        """Reset workflow to SUBJECT."""
        return self.transition(
            workspace_id,
            WorkflowTransitionEvent.RESET,
            actor_id=actor_id,
            occurred_at=occurred_at,
            reason="reset",
            enforce_gates=False,
        )

    def _can_advance(self, workspace) -> bool:  # noqa: ANN001
        target = next_stage(workspace.current_stage)
        if target is None:
            return False
        try:
            self._assert_advance_gates(workspace, target)
            return True
        except WorkflowGateBlocked:
            return False

    def _assert_advance_gates(self, workspace, target: WorkflowStage) -> None:  # noqa: ANN001
        required = _ADVANCE_GATES.get(target, ())
        missing = [
            code.value
            for code in required
            if not workspace.facts.fact_for(code)
        ]
        if missing:
            raise WorkflowGateBlocked(
                f"Cannot advance to {target.value}; missing: {', '.join(missing)}"
            )

    def _require_workspace(self, workspace_id: str):
        workspace = self._registry.get_workspace(workspace_id)
        if workspace is None:
            raise WorkspaceNotFound(f"Workspace not found: {workspace_id!r}")
        return workspace


def stage_is_forward(current: WorkflowStage, target: WorkflowStage) -> bool:
    """True when ``target`` is strictly after ``current`` in the workflow."""
    from app.domain.curriculum_studio.workflow_stage import stage_index

    return stage_index(target) > stage_index(current)
