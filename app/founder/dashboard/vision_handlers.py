"""Founder Vision Journal request handlers (V1SP-001D)."""

from __future__ import annotations

from flask import (
    Response,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user

from app.founder.dashboard.vision_forms import (
    VisionConfirmForm,
    VisionEntryForm,
    VisionFilterForm,
    VisionPromoteForm,
    VisionRelationForm,
)
from app.models.vision_journal import (
    POTENTIAL_VALUE_LABELS,
    RELATION_TYPE_LABELS,
    TARGET_VERSION_LABELS,
    VISION_STATUS_LABELS,
)
from app.services.vision_journal_service import (
    SORT_NEWEST,
    VisionJournalService,
    VisionSearchFilters,
)


def _parse_tags(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]


def _filters_from_request() -> VisionSearchFilters:
    author_raw = (request.args.get("author") or "").strip()
    author_id = None
    if author_raw.isdigit():
        author_id = int(author_raw)
    return VisionSearchFilters(
        query=(request.args.get("q") or "").strip() or None,
        category=(request.args.get("category") or "").strip() or None,
        status=(request.args.get("status") or "").strip() or None,
        target_version=(request.args.get("target_version") or "").strip() or None,
        tag=(request.args.get("tag") or "").strip() or None,
        author_user_id=author_id,
    )


def _populate_entry_form(form: VisionEntryForm, entry) -> None:
    form.title.data = entry.title
    form.description.data = entry.description
    form.reason.data = entry.reason
    form.potential_value.data = entry.potential_value
    form.expected_impact.data = entry.expected_impact
    form.target_version.data = entry.target_version
    form.category.data = entry.category
    form.status.data = entry.status
    form.tags.data = entry.tags_csv
    form.future_milestone.data = entry.future_milestone or ""


def handle_vision_journal():
    """List / search / filter Vision Journal entries."""
    authors = VisionJournalService.list_authors()
    filter_form = VisionFilterForm(
        formdata=request.args if request.method == "GET" else None,
        author_choices=[(str(uid), email) for uid, email in authors],
    )
    filters = _filters_from_request()
    sort = (request.args.get("sort") or SORT_NEWEST).strip()
    entries = VisionJournalService.search(filters, sort=sort)
    return render_template(
        "founder_dashboard/vision_journal.html",
        title="Vision Journal",
        entries=entries,
        filter_form=filter_form,
        filters=filters,
        sort=sort,
        status_labels=VISION_STATUS_LABELS,
        version_labels=TARGET_VERSION_LABELS,
        value_labels=POTENTIAL_VALUE_LABELS,
    )


def handle_vision_timeline():
    """Chronological evolution timeline."""
    events = VisionJournalService.build_timeline(limit=150)
    return render_template(
        "founder_dashboard/vision_timeline.html",
        title="Vision Timeline",
        events=events,
    )


def handle_vision_new():
    """Create a new vision entry."""
    form = VisionEntryForm()
    if form.validate_on_submit():
        entry = VisionJournalService.create_entry(
            author_user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            reason=form.reason.data,
            potential_value=form.potential_value.data,
            expected_impact=form.expected_impact.data,
            target_version=form.target_version.data,
            category=form.category.data,
            status=form.status.data,
            tags=_parse_tags(form.tags.data),
            future_milestone=form.future_milestone.data,
        )
        flash("Vision entry created.", "success")
        return redirect(
            url_for("founder_dashboard.vision_entry", entry_id=entry.id)
        )
    if request.method == "GET":
        form.status.data = "vision"
        form.potential_value.data = "medium"
        form.target_version.data = "unknown"
    return render_template(
        "founder_dashboard/vision_entry_form.html",
        title="New Vision Entry",
        form=form,
        mode="create",
    )


def handle_vision_entry(entry_id: int):
    """Entry detail with relations, timeline, and promote action."""
    entry = VisionJournalService.get_entry(entry_id)
    if entry is None:
        flash("Vision entry not found.", "warning")
        return redirect(url_for("founder_dashboard.vision_journal"))

    relation_form = VisionRelationForm(prefix="rel")
    promote_form = VisionPromoteForm(prefix="promo")
    archive_form = VisionConfirmForm(prefix="archive")
    archive_form.submit.label.text = "Archive"
    delete_form = VisionConfirmForm(prefix="delete")
    delete_form.submit.label.text = "Soft-delete"

    other_entries = [
        e
        for e in VisionJournalService.search(limit=500)
        if e.id != entry.id
    ]
    relation_form.to_entry_id.choices = [
        (e.id, e.title) for e in other_entries
    ]

    if promote_form.submit.data and promote_form.validate_on_submit():
        promo = VisionJournalService.promote_to_development(
            entry.id,
            promoted_by_user_id=current_user.id,
            notes=promote_form.notes.data,
            placeholder_ref=promote_form.placeholder_ref.data,
        )
        if promo is not None:
            flash(
                f"Promoted to Development. Placeholder: {promo.placeholder_ref}",
                "success",
            )
        return redirect(
            url_for("founder_dashboard.vision_entry", entry_id=entry.id)
        )

    if (
        relation_form.submit.data
        and relation_form.validate_on_submit()
        and other_entries
    ):
        VisionJournalService.add_relation(
            from_entry_id=entry.id,
            to_entry_id=relation_form.to_entry_id.data,
            relation_type=relation_form.relation_type.data,
            created_by_user_id=current_user.id,
        )
        flash("Relationship added.", "success")
        return redirect(
            url_for("founder_dashboard.vision_entry", entry_id=entry.id)
        )

    if archive_form.submit.data and archive_form.validate_on_submit():
        VisionJournalService.archive_entry(
            entry.id, changed_by_user_id=current_user.id
        )
        flash("Entry archived.", "success")
        return redirect(url_for("founder_dashboard.vision_journal"))

    if delete_form.submit.data and delete_form.validate_on_submit():
        VisionJournalService.soft_delete_entry(
            entry.id, changed_by_user_id=current_user.id
        )
        flash("Entry soft-deleted.", "success")
        return redirect(url_for("founder_dashboard.vision_journal"))

    relations = VisionJournalService.list_related(entry.id)
    if entry.author:
        author_email = entry.author.email
    else:
        author_email = f"user:{entry.author_user_id}"
    return render_template(
        "founder_dashboard/vision_entry_detail.html",
        title=entry.title,
        entry=entry,
        author_email=author_email,
        relations=relations,
        relation_form=relation_form,
        promote_form=promote_form,
        archive_form=archive_form,
        delete_form=delete_form,
        status_labels=VISION_STATUS_LABELS,
        version_labels=TARGET_VERSION_LABELS,
        value_labels=POTENTIAL_VALUE_LABELS,
        relation_labels=RELATION_TYPE_LABELS,
    )


def handle_vision_edit(entry_id: int):
    """Edit an existing vision entry."""
    entry = VisionJournalService.get_entry(entry_id)
    if entry is None:
        flash("Vision entry not found.", "warning")
        return redirect(url_for("founder_dashboard.vision_journal"))

    form = VisionEntryForm()
    if form.validate_on_submit():
        VisionJournalService.update_entry(
            entry.id,
            changed_by_user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            reason=form.reason.data,
            potential_value=form.potential_value.data,
            expected_impact=form.expected_impact.data,
            target_version=form.target_version.data,
            category=form.category.data,
            status=form.status.data,
            tags=_parse_tags(form.tags.data),
            future_milestone=form.future_milestone.data,
        )
        flash("Vision entry updated.", "success")
        return redirect(
            url_for("founder_dashboard.vision_entry", entry_id=entry.id)
        )
    if request.method == "GET":
        _populate_entry_form(form, entry)
    return render_template(
        "founder_dashboard/vision_entry_form.html",
        title=f"Edit · {entry.title}",
        form=form,
        mode="edit",
        entry=entry,
    )


def handle_vision_export(fmt: str):
    """Export journal as markdown, json, or csv."""
    filters = _filters_from_request()
    fmt = (fmt or "markdown").strip().lower()
    if fmt == "json":
        body = VisionJournalService.export_json(filters)
        mimetype = "application/json"
        filename = "vision_journal.json"
    elif fmt == "csv":
        body = VisionJournalService.export_csv(filters)
        mimetype = "text/csv"
        filename = "vision_journal.csv"
    else:
        body = VisionJournalService.export_markdown(filters)
        mimetype = "text/markdown"
        filename = "vision_journal.md"
    return Response(
        body,
        mimetype=mimetype,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )


def handle_remove_relation(relation_id: int, entry_id: int):
    """Remove a relationship and return to the entry."""
    VisionJournalService.remove_relation(relation_id)
    flash("Relationship removed.", "success")
    return redirect(url_for("founder_dashboard.vision_entry", entry_id=entry_id))
