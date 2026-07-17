"""Authentication blueprint routes."""

from __future__ import annotations

from urllib.parse import unquote, urlsplit

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app.application.config.internal_alpha import is_internal_alpha_enabled
from app.auth.forms import LoginForm
from app.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Display and process the login form."""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = LoginForm()
    is_redirected = request.args.get("next") is not None

    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Welcome back to Kwalitec.", "success")

            # Check if user has an active study plan
            from app.services.study_plan_service import StudyPlanService
            active_plan = StudyPlanService.get_user_active_plan(user.id)

            if not active_plan:
                # Redirect to study plan wizard if no active plan
                return redirect(url_for("study_plan.wizard_step", step=1))

            return redirect(_safe_next_url() or url_for("dashboard.index"))

        flash("Invalid email or password.", "danger")

    return render_template(
        "auth/login.html",
        form=form,
        title="Sign in",
        is_redirected=is_redirected,
        internal_alpha_enabled=is_internal_alpha_enabled(),
    )


@auth_bp.post("/logout")
def logout():
    """Log out the current user.

    Intentionally not ``@login_required``: logout must remain idempotent and
    must clear a stale session even when ``load_user`` cannot resolve a user
    (for example after a local schema rebuild). CSRF still protects the POST.
    """
    logout_user()
    return redirect(url_for("auth.login"))


def _safe_next_url() -> str | None:
    """Return a same-origin relative path for post-login redirect.

    Rejects absolute URLs, protocol-relative URLs (``//…``, ``///…``),
    backslash tricks, and percent-encoded bypasses. Only path-absolute
    internal destinations are allowed (leading single ``/``).
    """
    next_url = request.args.get("next")
    if not next_url:
        return None

    raw = next_url.strip()
    if not raw:
        return None

    # Reject control characters that can smuggle headers or confuse parsers.
    if any(ch in raw for ch in ("\r", "\n", "\0", "\\")):
        return None

    # Fully decode percent-encoding so ``/%2f%2f…`` cannot bypass checks.
    candidate = raw
    for _ in range(5):
        decoded = unquote(candidate)
        if decoded == candidate:
            break
        candidate = decoded

    if any(ch in candidate for ch in ("\r", "\n", "\0", "\\")):
        return None

    # Require a single leading slash (path-absolute). Reject ``//`` / ``///``.
    if not candidate.startswith("/") or candidate.startswith("//"):
        return None

    parsed = urlsplit(candidate)
    if parsed.scheme or parsed.netloc:
        return None
    if not parsed.path.startswith("/") or parsed.path.startswith("//"):
        return None

    # Return a normalised local path (never the raw attacker string).
    safe = parsed.path
    if parsed.query:
        safe = f"{safe}?{parsed.query}"
    if parsed.fragment:
        safe = f"{safe}#{parsed.fragment}"
    return safe
