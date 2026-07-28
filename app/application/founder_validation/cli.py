"""Flask CLI for Founder Validation metrics (FV-001)."""

from __future__ import annotations

import json

import click

from app.application.founder_validation.metrics_service import (
    FounderValidationMetricsService,
)


@click.command("fv-metrics")
@click.option(
    "--pretty/--compact",
    default=True,
    show_default=True,
    help="Pretty-print JSON output.",
)
def fv_metrics_command(pretty: bool) -> None:
    """Print FV-001 product metrics + Version 1 workflow catalogue.

    Consumes RI-002 adoption telemetry, LP-001 operation rows, mission
    completion counts, and process-scoped founder validation telemetry.
    Does not mutate educational state.
    """
    payload = FounderValidationMetricsService().build_operator_payload()
    if pretty:
        click.echo(json.dumps(payload, indent=2, sort_keys=True))
    else:
        click.echo(json.dumps(payload, sort_keys=True))
