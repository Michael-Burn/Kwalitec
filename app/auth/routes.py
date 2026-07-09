"""Authentication blueprint routes."""

from urllib.parse import urlsplit

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

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

    return render_template("auth/login.html", form=form, title="Sign in", is_redirected=is_redirected)


@auth_bp.post("/logout")
@login_required
def logout():
    """Log out the current user."""
    logout_user()
    flash("You have been signed out.", "info")
    return redirect(url_for("auth.login"))


def _safe_next_url() -> str | None:
    """Return a local next URL, rejecting external redirects."""
    next_url = request.args.get("next")
    if not next_url:
        return None

    parsed = urlsplit(next_url)
    if parsed.netloc or parsed.scheme:
        return None

    return next_url
