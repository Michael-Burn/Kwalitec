"""Custom Flask CLI commands for Kwalitec administration tasks."""

from __future__ import annotations

import logging
import os
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
    modifying the database.

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

    # Check whether any users already exist
    user_count: int = db.session.query(User).count()
    if user_count > 0:
        click.echo("Administrator already exists.")
        logger.info(
            "create-admin: %d existing user(s) found – skipping creation",
            user_count,
        )
        return

    # Read credentials from the environment
    email: str | None = os.getenv("ADMIN_EMAIL")
    password: str | None = os.getenv("ADMIN_PASSWORD")

    # Validate that both are present
    missing: list[str] = []
    if not email:
        missing.append("ADMIN_EMAIL")
    if not password:
        missing.append("ADMIN_PASSWORD")

    if missing:
        msg = (
            "Missing required environment variable(s): "
            + ", ".join(missing)
            + ". Set these variables and retry."
        )
        click.echo(f"Error: {msg}", err=True)
        logger.error("create-admin: %s", msg)
        sys.exit(1)

    # Create the administrator
    user = User(email=email, is_active_user=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    click.echo("Administrator created successfully.")
    logger.info(
        "create-admin: administrator created for email=%s", email
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
    omitted. Name is confirmed in the success message; authentication uses
    email and password only (User model has no separate name column).
    """
    logger.info("Starting create-test-user command")

    if not _users_table_exists():
        click.echo(
            "users table not found – run `flask db upgrade` first.",
            err=True,
        )
        logger.error("create-test-user: users table missing; aborting.")
        sys.exit(1)

    display_name = (name or "").strip()
    normalized_email = (email or "").strip().lower()
    if not display_name:
        click.echo("Error: Name is required.", err=True)
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

    user = User(email=normalized_email, is_active_user=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

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
                    organisation, paper, version, exc,
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
                    click.echo(
                        f"    {label}Section '{engine_section.code}' {action}."
                    )

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
