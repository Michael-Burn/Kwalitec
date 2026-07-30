"""EI-002A migration tooling — bind legacy workspaces to Generation Chains."""

from __future__ import annotations

import logging

import click

from app.application.curriculum_intelligence.in_memory_generation_store import (
    InMemoryGenerationStore,
)
from app.application.curriculum_intelligence.workspace_generation_service import (
    WorkspaceGenerationService,
)
from app.application.curriculum_studio.fact_updates import copy_publication_facts
from app.domain.curriculum_intelligence.workspace_binding import (
    META_CHAIN_ID,
    chain_id_for_workspace,
)
from app.extensions import db
from app.infrastructure.adapters.curriculum_studio_workspace_persistence import (
    load_all_workspaces,
    persist_workspace,
)
from app.models.curriculum_studio_foundation import StudioWorkspaceProjection

logger = logging.getLogger(__name__)


def migrate_legacy_workspaces(
    *,
    mark_legacy_fallback: bool = True,
    run_engine: bool = False,
) -> dict[str, int]:
    """Bind existing Studio workspaces to Generation Chains.

    Default mode marks workspaces without a certified chain for legacy CIP
    publish fallback. Optional ``run_engine`` attempts a full G1–G7 run when
    source documents are available (best-effort).
    """
    from app.infrastructure.adapters.curriculum_intelligence.generation_store import (
        SqlAlchemyGenerationStore,
    )
    from app.presentation.curriculum_studio.factory import get_studio_service

    studio = get_studio_service()
    try:
        store = SqlAlchemyGenerationStore()
    except Exception:  # noqa: BLE001
        store = InMemoryGenerationStore()

    service = WorkspaceGenerationService(store, registry=studio.registry)
    stats = {
        "scanned": 0,
        "bound": 0,
        "legacy_marked": 0,
        "engine_ran": 0,
        "errors": 0,
    }

    workspaces = list(studio.registry.list_workspaces())
    if not workspaces:
        workspaces = list(load_all_workspaces())
        for ws in workspaces:
            studio.registry.put_workspace(ws)

    for workspace in workspaces:
        stats["scanned"] += 1
        wid = workspace.workspace_id
        try:
            meta = dict(workspace.metadata)
            existing_chain = meta.get(META_CHAIN_ID) or (
                store.get_chain_id_for_workspace(wid)
            )
            if not existing_chain:
                binding = service.ensure_binding(wid)
                stats["bound"] += 1
                existing_chain = binding.chain_id
            else:
                store.ensure_chain(existing_chain, wid)
                stats["bound"] += 1

            certified = workspace.facts.intelligence_certified
            if not certified and mark_legacy_fallback:
                service.mark_legacy_fallback(wid)
                stats["legacy_marked"] += 1

            if run_engine and not certified:
                try:
                    result = service.run_initial_pipeline(
                        wid,
                        subject_code=workspace.subject_code,
                        version_label=workspace.version_label or "default",
                    )
                    if result.intelligence_certified:
                        stats["engine_ran"] += 1
                        ws = studio.registry.get_workspace(wid)
                        if ws is not None:
                            facts = copy_publication_facts(
                                ws.facts,
                                intelligence_certified=True,
                                legacy_publish_fallback=False,
                            )
                            studio.registry.put_workspace(ws.with_facts(facts))
                except Exception:  # noqa: BLE001
                    logger.exception("Engine run failed for %s", wid)

            row = db.session.get(StudioWorkspaceProjection, wid)
            if row is not None:
                row.active_chain_id = existing_chain or chain_id_for_workspace(wid)
                ws = studio.registry.get_workspace(wid)
                if ws is not None:
                    m = dict(ws.metadata)
                    row.certified_snapshot_id = m.get("ei_certified_snapshot_id")
                    row.calibration_profile_id = m.get("ei_calibration_profile_id")
                    row.certification_status = m.get("ei_certification_status")
                    row.review_pack_ref = m.get("ei_review_pack_ref")
                    persist_workspace(ws)
            db.session.commit()
        except Exception:  # noqa: BLE001
            stats["errors"] += 1
            logger.exception("Migration failed for workspace %s", wid)
            try:
                db.session.rollback()
            except Exception:  # noqa: BLE001
                pass

    return stats


@click.command("ei-migrate-workspaces")
@click.option(
    "--legacy-fallback/--no-legacy-fallback",
    default=True,
    help="Mark unbound workspaces for legacy CIP publish fallback.",
)
@click.option(
    "--run-engine/--no-run-engine",
    default=False,
    help="Attempt full EI pipeline for uncertified workspaces.",
)
def ei_migrate_workspaces_command(
    legacy_fallback: bool,
    run_engine: bool,
) -> None:
    """Bind Curriculum Studio workspaces to Generation Chains (EI-002A)."""
    stats = migrate_legacy_workspaces(
        mark_legacy_fallback=legacy_fallback,
        run_engine=run_engine,
    )
    click.echo(
        "EI-002A workspace migration: "
        f"scanned={stats['scanned']} bound={stats['bound']} "
        f"legacy_marked={stats['legacy_marked']} "
        f"engine_ran={stats['engine_ran']} errors={stats['errors']}"
    )
