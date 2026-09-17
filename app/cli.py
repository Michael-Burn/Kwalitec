"""Custom Flask CLI commands for Kwalitec administration tasks."""

from __future__ import annotations

import logging
import sys

import click
from sqlalchemy.exc import OperationalError, ProgrammingError

from app.extensions import db
from app.models.user import User

logger = logging.getLogger(__name__)


def _sections_table_exists() -> bool:
    """Return True if the ``sections`` table exists in the current database."""
    try:
        db.session.execute(db.text("SELECT 1 FROM sections LIMIT 1"))
        return True
    except (OperationalError, ProgrammingError):
        return False


def _users_table_exists() -> bool:
    """Return True if the ``users`` table exists in the current database.

    On a fresh database (before migrations have run) the table will be
    absent.  We probe with a lightweight query and interpret any
    schema-level error as "table missing" so the caller can degrade
    gracefully instead of crashing the deploy.
    """
    try:
        db.session.execute(db.text("SELECT 1 FROM users LIMIT 1"))
        return True
    except (OperationalError, ProgrammingError) as exc:
        logger.warning(
            "create-admin: users table not available (%s); "
            "assuming migrations have not run yet",
            exc.__class__.__name__,
        )
        return False


@click.command("create-admin")
def create_admin_command() -> None:
    """Create the initial administrator user from environment variables.

    Reads ADMIN_EMAIL and ADMIN_PASSWORD from the environment. If any
    User record already exists the command exits successfully without
    modifying the database (does **not** update passwords — use
    ``flask sync-admin`` for that).

    If the ``users`` table does not yet exist (migrations have not been
    applied) the command logs a warning and exits successfully, assuming
    migrations will be applied separately. This keeps the command safe
    to run on every deploy regardless of migration ordering.

    Environment Variables:
        ADMIN_EMAIL:    Administrator email address (required on first run)
        ADMIN_PASSWORD: Administrator plaintext password (required on first run)

    Exit codes:
        0 – Administrator already exists, was created, or migrations are pending
        1 – Required environment variable is missing
    """
    from app.services.admin_bootstrap_service import (
        AdminBootstrapError,
        AdminBootstrapService,
    )

    logger.info("Starting create-admin command")

    # If the schema is not present yet, do not crash the deploy.
    # Migrations are expected to run separately (e.g. via `db upgrade`).
    if not _users_table_exists():
        click.echo(
            "users table not found – skipping create-admin "
            "(migrations may not have run yet)."
        )
        logger.warning(
            "create-admin: users table missing; skipping creation. "
            "Run `flask --app wsgi.py db upgrade` before create-admin."
        )
        return

    # Check whether any users already exist — never overwrite passwords here.
    user_count: int = db.session.query(User).count()
    if user_count > 0:
        click.echo("Administrator already exists.")
        logger.info(
            "create-admin: %d existing user(s) found – skipping creation",
            user_count,
        )
        return

    try:
        user = AdminBootstrapService.create_initial_admin_if_empty()
    except AdminBootstrapError as exc:
        click.echo(f"Error: {exc}", err=True)
        logger.error("create-admin: %s", exc)
        sys.exit(1)

    if user is None:
        # Race / concurrent create — treat as already exists.
        click.echo("Administrator already exists.")
        return

    click.echo("Administrator created successfully.")
    logger.info("create-admin: administrator created for email=%s", user.email)


@click.command("sync-admin")
def sync_admin_command() -> None:
    """Synchronise the bootstrap administrator from environment variables.

    Finds the user matching ``ADMIN_EMAIL``. When present, updates the
    password from ``ADMIN_PASSWORD`` and ensures Founder RBAC. When absent,
    creates the administrator (same as first-run ``create-admin``).

    Intended for local development when ``.env`` credentials and the local
    database diverge. Does **not** run during production startup — operators
    must invoke this command explicitly.

    Environment Variables:
        ADMIN_EMAIL:    Administrator email address (required)
        ADMIN_PASSWORD: Administrator plaintext password (required)

    Exit codes:
        0 – Administrator synchronised or created
        1 – Required environment variable missing, or schema not ready
    """
    from app.services.admin_bootstrap_service import (
        AdminBootstrapError,
        AdminBootstrapService,
    )

    logger.info("Starting sync-admin command")

    if not _users_table_exists():
        click.echo(
            "users table not found – run `flask db upgrade` first.",
            err=True,
        )
        logger.error("sync-admin: users table missing; aborting.")
        sys.exit(1)

    try:
        result = AdminBootstrapService.sync_admin()
    except AdminBootstrapError as exc:
        click.echo(f"Error: {exc}", err=True)
        logger.error("sync-admin: %s", exc)
        sys.exit(1)

    if result.created:
        click.echo("Administrator created successfully.")
        logger.info("sync-admin: administrator created for email=%s", result.email)
    else:
        click.echo("Administrator synchronised successfully.")
        click.echo("  - password updated")
        click.echo(
            "  - founder role verified"
            if result.founder_role_verified
            else "  - founder role MISSING"
        )
        click.echo(
            "  - administrator role verified"
            if result.administrator_role_verified
            else "  - administrator role MISSING"
        )
        click.echo(
            "  - student role verified"
            if result.student_role_verified
            else "  - student role MISSING"
        )
        logger.info(
            "sync-admin: synchronised email=%s password_updated=%s "
            "founder=%s administrator=%s student=%s",
            result.email,
            result.password_updated,
            result.founder_role_verified,
            result.administrator_role_verified,
            result.student_role_verified,
        )


@click.command("create-test-user")
@click.option(
    "--name",
    prompt="Name",
    help="Display name for the Internal Alpha participant.",
)
@click.option("--email", prompt="Email", help="Login email for the test user.")
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Password for the test user.",
)
def create_test_user_command(name: str, email: str, password: str) -> None:
    """Create an additional Internal Alpha test user.

    Unlike ``create-admin``, this command allows creating users when the
    database already has accounts. It is intended for operator use only and
    is not exposed through the public web UI.

    Prompts interactively for name, email, and password when options are
    omitted. Name is stored as the student display name; authentication
    still uses email and password.
    """
    logger.info("Starting create-test-user command")

    if not _users_table_exists():
        click.echo(
            "users table not found – run `flask db upgrade` first.",
            err=True,
        )
        logger.error("create-test-user: users table missing; aborting.")
        sys.exit(1)

    display_name = User.normalized_display_name(name)
    normalized_email = (email or "").strip().lower()
    if not display_name:
        click.echo(
            "Error: Name must be between "
            f"{User.DISPLAY_NAME_MIN_LENGTH} and "
            f"{User.DISPLAY_NAME_MAX_LENGTH} characters.",
            err=True,
        )
        sys.exit(1)
    if not normalized_email or "@" not in normalized_email:
        click.echo("Error: A valid email is required.", err=True)
        sys.exit(1)
    if not password or len(password) < 8:
        click.echo("Error: Password must be at least 8 characters.", err=True)
        sys.exit(1)

    existing = User.query.filter_by(email=normalized_email).first()
    if existing is not None:
        click.echo(
            f"Error: A user with email {normalized_email} already exists.",
            err=True,
        )
        sys.exit(1)

    user = User(
        email=normalized_email,
        is_active_user=True,
        display_name=display_name,
    )
    user.set_password(password)
    db.session.add(user)
    db.session.flush()
    from app.services.identity_service import IdentityService

    IdentityService.ensure_student_defaults(user)

    click.echo(
        f"Test user created successfully for {display_name} "
        f"<{normalized_email}> (id={user.id})."
    )
    logger.info(
        "create-test-user: created user id=%s email=%s name=%s",
        user.id,
        normalized_email,
        display_name,
    )


@click.command("backfill-sections")
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Preview changes without writing to the database.",
)
def backfill_sections_command(dry_run: bool) -> None:
    """Backfill Section rows and Topic.section_id for legacy V2 curricula.

    Finds every V2 curriculum in the database whose topics do not yet have
    their ``section_id`` populated (i.e. records created before the sections
    migration was applied) and:

    \b
    1. Finds the matching engine V2 curriculum by exam_name + version.
    2. Creates any missing Section rows (idempotent).
    3. Sets Topic.section_id on unlinked topics matched by title.

    This command is **idempotent**: already-linked topics are skipped.
    It is safe to run on production — no existing rows are deleted or
    modified except for setting the nullable ``section_id`` column.

    Exit codes:
        0 – Success (or nothing to do)
        1 – Schema not ready (migrations have not been applied)
    """
    if not _sections_table_exists():
        click.echo(
            "sections table not found — run `flask db upgrade` first.",
            err=True,
        )
        logger.error("backfill-sections: sections table missing; aborting.")
        sys.exit(1)

    from app.curriculum.models import CurriculumDefinition
    from app.curriculum.repository import CurriculumRepository
    from app.models.curriculum import Curriculum, Section, Topic

    repo = CurriculumRepository()
    discovered = repo.list_exams()  # [(org, paper, [versions])]

    total_sections_created = 0
    total_topics_linked = 0
    total_curricula_processed = 0

    for organisation, paper, versions in discovered:
        for version in versions:
            # Only process V2 curricula — skip V1 silently.
            try:
                engine_curriculum = repo.load_auto(organisation, paper, version)
            except Exception as exc:
                logger.warning(
                    "backfill-sections: cannot load %s/%s/%s — skipping (%s)",
                    organisation,
                    paper,
                    version,
                    exc,
                )
                continue

            if not isinstance(engine_curriculum, CurriculumDefinition):
                continue  # V1 curriculum — no sections to backfill.

            # Find the DB Curriculum row for this V2 curriculum.
            db_curriculum = Curriculum.query.filter_by(
                exam_name=engine_curriculum.exam_name,
                version=version,
            ).first()
            if db_curriculum is None:
                click.echo(
                    f"  [SKIP] No DB row for '{engine_curriculum.exam_name}'"
                    f" v{version} — run startup import first."
                )
                continue

            # Check whether any topics still have section_id = NULL.
            unlinked_count = Topic.query.filter_by(
                curriculum_id=db_curriculum.id,
                section_id=None,
                active=True,
            ).count()
            if unlinked_count == 0:
                click.echo(
                    f"  [OK]   '{engine_curriculum.exam_name}' v{version} — "
                    f"all topics already linked."
                )
                continue

            total_curricula_processed += 1
            click.echo(
                f"  [PROC] '{engine_curriculum.exam_name}' v{version} — "
                f"{unlinked_count} topic(s) need linking."
            )

            sections_created = 0
            topics_linked = 0

            for engine_section in sorted(
                engine_curriculum.sections, key=lambda s: s.display_order
            ):
                # Find or create the DB Section row.
                db_section = Section.query.filter_by(
                    curriculum_id=db_curriculum.id,
                    code=engine_section.code,
                ).first()

                if db_section is None:
                    if not dry_run:
                        db_section = Section(
                            curriculum_id=db_curriculum.id,
                            official_id=engine_section.id,
                            code=engine_section.code,
                            title=engine_section.title,
                            description=getattr(engine_section, "description", None),
                            exam_weight=getattr(engine_section, "exam_weight", None),
                            display_order=engine_section.display_order,
                            estimated_hours=getattr(
                                engine_section, "estimated_hours", None
                            ),
                            difficulty=getattr(engine_section, "difficulty", None),
                        )
                        db.session.add(db_section)
                        db.session.flush()
                    sections_created += 1
                    total_sections_created += 1
                    label = "[DRY] " if dry_run else ""
                    action = "would be created" if dry_run else "created"
                    click.echo(f"    {label}Section '{engine_section.code}' {action}.")

                if dry_run:
                    # Count how many topics would be linked for this section.
                    for engine_topic in engine_section.topics:
                        db_topic = Topic.query.filter_by(
                            curriculum_id=db_curriculum.id,
                            name=engine_topic.title,
                            section_id=None,
                        ).first()
                        if db_topic is not None:
                            topics_linked += 1
                            total_topics_linked += 1
                    continue

                # Link unlinked topics to this section.
                for engine_topic in sorted(
                    engine_section.topics, key=lambda t: t.display_order
                ):
                    db_topic = Topic.query.filter_by(
                        curriculum_id=db_curriculum.id,
                        name=engine_topic.title,
                        section_id=None,
                    ).first()
                    if db_topic is not None:
                        db_topic.section_id = db_section.id
                        topics_linked += 1
                        total_topics_linked += 1

            if not dry_run and (sections_created > 0 or topics_linked > 0):
                db.session.commit()

            prefix = "[DRY] " if dry_run else ""
            wb = "would be " if dry_run else ""
            click.echo(
                f"    {prefix}{sections_created} section(s) {wb}created, "
                f"{topics_linked} topic(s) {wb}linked."
            )

    if dry_run:
        click.echo(
            f"\nDry run complete — {total_curricula_processed} curriculum/a, "
            f"{total_sections_created} section(s) to create, "
            f"{total_topics_linked} topic(s) to link. "
            "No changes written."
        )
    else:
        click.echo(
            f"\nBackfill complete — {total_curricula_processed} curriculum/a, "
            f"{total_sections_created} section(s) created, "
            f"{total_topics_linked} topic(s) linked."
        )
    logger.info(
        "backfill-sections: done (%d curricula, %d sections, %d topics%s)",
        total_curricula_processed,
        total_sections_created,
        total_topics_linked,
        " [DRY RUN]" if dry_run else "",
    )


@click.command("internal-alpha-reset")
@click.option(
    "--yes",
    "assume_yes",
    is_flag=True,
    default=False,
    help="Skip the interactive confirmation prompt (operator automation only).",
)
def internal_alpha_reset_command(assume_yes: bool) -> None:
    """Reset generated educational state for Founder / Internal Alpha baseline.

    Removes Study Plans, Twins, progress, missions, attempts, decisions,
    research feedback, analytics, V2 aggregates, runtime enrolments, and
    related regenerable learner history. Preserves users, password hashes,
    curricula, sections, topics, learning objectives, Curriculum Studio
    configuration, published curriculum metadata, and Alembic history.

    This is NOT a database wipe. THIS CANNOT BE UNDONE.

    Exit codes:
        0 – Reset completed or cancelled by the operator
        1 – Reset failed
    """
    from app.services.internal_alpha_reset_service import InternalAlphaResetService

    logger.info("Starting internal-alpha-reset command")

    click.echo("=" * 60)
    click.echo("INTERNAL ALPHA / FOUNDER EDUCATIONAL RESET")
    click.echo("=" * 60)
    click.echo()
    click.echo("THIS CANNOT BE UNDONE")
    click.echo()
    click.echo(
        "This command removes learner-generated operational state so the "
        "environment returns to a clean Founder baseline."
    )
    click.echo("It does NOT wipe the database.")
    click.echo()

    preview = InternalAlphaResetService.preview()

    click.echo("Will delete (learner-generated operational data):")
    for item in preview.to_delete:
        click.echo(f"  - {item.table}: {item.count}")
    click.echo(f"  Total rows to delete: {preview.total_to_delete}")
    click.echo()
    click.echo("Will preserve:")
    for item in preview.preserved:
        click.echo(f"  - {item.table}: {item.count}")
    click.echo("  - Alembic migration history (alembic_version)")
    click.echo("  - Application configuration and environment settings")
    click.echo()

    if not assume_yes:
        confirmed = click.confirm(
            "Proceed with Internal Alpha reset? THIS CANNOT BE UNDONE",
            default=False,
        )
        if not confirmed:
            click.echo("Reset cancelled. No changes were made.")
            logger.info("internal-alpha-reset: cancelled by operator")
            return

    try:
        result = InternalAlphaResetService.execute()
    except Exception as exc:
        click.echo(f"Error: Internal Alpha reset failed: {exc}", err=True)
        logger.error("internal-alpha-reset: failed (%s)", exc)
        sys.exit(1)

    click.echo()
    click.echo("Reset complete. Records removed:")
    for item in result.deleted:
        click.echo(f"  - {item.table}: {item.count}")
    click.echo(f"  Total deleted: {result.total_deleted}")
    click.echo()
    click.echo("Preserved after reset:")
    for item in result.preserved:
        click.echo(f"  - {item.table}: {item.count}")
    click.echo()
    click.echo(
        "Application is ready for a clean Founder baseline. "
        "Participants may create new Study Plans, Calibration, Twins, "
        "recommendations, and missions from a shared empty history."
    )
    logger.info(
        "internal-alpha-reset: completed total_deleted=%d",
        result.total_deleted,
    )


@click.command("shadow-coverage-reconciliation")
@click.option(
    "--email",
    "emails",
    multiple=True,
    help=(
        "Learner email to reconcile (repeatable). Defaults to the founder "
        "account plus other local accounts that have Stage A or Runtime C "
        "history."
    ),
)
@click.option(
    "--output",
    type=click.Path(dir_okay=False, writable=True, path_type=str),
    default=None,
    help="Optional path to write the shadow report text.",
)
def shadow_coverage_reconciliation_command(
    emails: tuple[str, ...],
    output: str | None,
) -> None:
    """Run coverage reconciliation in shadow mode (read-only).

    Interprets Stage A TopicProgress.completed and Runtime C verified
    TOPIC_COMPLETED through the canonical identity layer. Does not change
    live coverage display or calculation.
    """
    from pathlib import Path

    from app.application.coverage_reconciliation import (
        CoverageReconciliationService,
    )
    from app.application.curriculum_identity.constants import (
        ACTIVE_CS1_CURRICULUM_VERSION,
    )
    from app.founder.dashboard.access import founder_emails
    from app.models.educational_runtime_engine import RuntimeEducationalEvent
    from app.models.topic_progress import TopicProgress

    selected = [e.strip() for e in emails if e and e.strip()]
    if not selected:
        selected = sorted({e.lower() for e in founder_emails() if e})
        # Always include known local investigation accounts when present.
        selected.extend(
            [
                "ctshumba01@gmail.com",
                "ready@ex.com",
                "demo-phase3@example.com",
                "shadow-phase3-runtime-c-verified@local.test",
            ]
        )
        # Plus any account with relevant history.
        history_ids = {
            row.user_id
            for row in TopicProgress.query.with_entities(
                TopicProgress.user_id
            ).distinct()
        } | {
            row.user_id
            for row in RuntimeEducationalEvent.query.with_entities(
                RuntimeEducationalEvent.user_id
            ).distinct()
        }
        for user in User.query.filter(User.id.in_(history_ids)).all():
            if user.email:
                selected.append(user.email)

        # De-dupe preserving order.
        seen: set[str] = set()
        ordered: list[str] = []
        for email in selected:
            key = email.strip().lower()
            if key in seen:
                continue
            seen.add(key)
            ordered.append(email.strip())
        selected = ordered

    results = CoverageReconciliationService.reconcile_accounts(
        selected,
        curriculum_version=ACTIVE_CS1_CURRICULUM_VERSION,
    )
    # Include named emails even when the user row is empty / missing history.
    present = {(r.user_email or "").lower() for r in results}
    for email in selected:
        if email.lower() in present:
            continue
        user = User.query.filter_by(email=email).first()
        if user is None:
            click.echo(f"(skip) no local user for {email}")
            continue
        results.append(
            CoverageReconciliationService.reconcile_learner(user.id)
        )

    report = CoverageReconciliationService.format_report(results)
    click.echo(report)
    if output:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report, encoding="utf-8")
        click.echo(f"Wrote shadow report to {path}")
