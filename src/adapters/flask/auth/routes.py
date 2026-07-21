"""Production authentication Flask routes.

Thin HTTP glue over AuthController. CSRF-protected state-changing forms.
Establishes trusted student identities; does not create Student Twins or
run onboarding.
"""

# HTML form markup in f-strings intentionally exceeds the line budget.
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import Any

from flask import (
    Blueprint,
    Flask,
    redirect,
    render_template_string,
    request,
    session,
    url_for,
)

from adapters.flask.auth.controller import AuthController, auth_error_message
from adapters.flask.auth.csrf import ensure_csrf_token, validate_csrf_token
from adapters.flask.auth.dependency_provider import (
    AUTH_SESSION_KEY,
    AuthAdapterDependencies,
    AuthDependencyProvider,
    get_auth_dependencies,
)
from adapters.flask.auth.factory import build_authentication_service
from adapters.flask.auth.secure_cookies import apply_secure_cookie_config
from adapters.flask.dashboard.dependency_provider import STUDENT_SESSION_KEY
from adapters.flask.navigation import DASHBOARD_PATH, with_query
from application.auth.errors import AuthenticationError
from application.auth.results import AuthSessionClaims

auth_bp = Blueprint(
    "eos_auth",
    __name__,
    url_prefix="/eos/auth",
)

_BASE_FORM = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{{ title }}</title>
</head>
<body>
  <main>
    <h1>{{ title }}</h1>
    {% if message %}<p role="status">{{ message }}</p>{% endif %}
    {% if error %}<p role="alert">{{ error }}</p>{% endif %}
    {{ form_html|safe }}
  </main>
</body>
</html>
"""


def _client_key() -> str:
    forwarded = (request.headers.get("X-Forwarded-For") or "").split(",")[0].strip()
    return forwarded or (request.remote_addr or "anonymous")


def _store_session(claims: AuthSessionClaims) -> None:
    session[AUTH_SESSION_KEY] = {
        "user_id": claims.user_id,
        "email": claims.email,
        "remember_me": claims.remember_me,
        "created_at": claims.created_at.isoformat(),
        "last_activity_at": claims.last_activity_at.isoformat(),
        "email_verified": claims.email_verified,
    }
    session[STUDENT_SESSION_KEY] = claims.user_id
    session.permanent = bool(claims.remember_me)


def _clear_session() -> None:
    session.pop(AUTH_SESSION_KEY, None)
    session.pop(STUDENT_SESSION_KEY, None)


def _load_claims() -> AuthSessionClaims | None:
    raw = session.get(AUTH_SESSION_KEY)
    if not isinstance(raw, dict):
        return None
    try:
        return AuthSessionClaims(
            user_id=str(raw["user_id"]),
            email=str(raw["email"]),
            remember_me=bool(raw.get("remember_me")),
            created_at=datetime.fromisoformat(str(raw["created_at"])),
            last_activity_at=datetime.fromisoformat(str(raw["last_activity_at"])),
            email_verified=bool(raw.get("email_verified")),
        )
    except (KeyError, TypeError, ValueError):
        return None


def _require_csrf() -> str | None:
    if not validate_csrf_token(request.form.get("csrf_token")):
        return "Invalid CSRF token."
    return None


def _page(title: str, form_html: str, *, error: str = "", message: str = "") -> str:
    return render_template_string(
        _BASE_FORM,
        title=title,
        form_html=form_html,
        error=error,
        message=message,
    )


@auth_bp.get("/register")
def show_register() -> Any:
    csrf = ensure_csrf_token()
    form = f"""
    <form method="post" action="{url_for("eos_auth.submit_register")}" aria-label="Register">
      <input type="hidden" name="csrf_token" value="{csrf}">
      <label for="email">Email</label>
      <input id="email" name="email" type="email" required autocomplete="email">
      <label for="password">Password</label>
      <input id="password" name="password" type="password" required autocomplete="new-password">
      <button type="submit">Create account</button>
    </form>
    """
    return _page("Register", form)


@auth_bp.post("/register")
def submit_register() -> Any:
    csrf_error = _require_csrf()
    if csrf_error:
        return _page("Register", "", error=csrf_error), 400
    controller = AuthController(get_auth_dependencies())
    try:
        result = controller.register(
            email=request.form.get("email") or "",
            password=request.form.get("password") or "",
            client_key=_client_key(),
        )
    except AuthenticationError as exc:
        csrf = ensure_csrf_token()
        form = f"""
        <form method="post" action="{url_for("eos_auth.submit_register")}" aria-label="Register">
          <input type="hidden" name="csrf_token" value="{csrf}">
          <label for="email">Email</label>
          <input id="email" name="email" type="email" required>
          <label for="password">Password</label>
          <input id="password" name="password" type="password" required>
          <button type="submit">Create account</button>
        </form>
        """
        return _page("Register", form, error=auth_error_message(exc)), 400
    return _page(
        "Register",
        f'<p><a href="{url_for("eos_auth.show_login")}">Sign in</a></p>',
        message=result.message,
    )


@auth_bp.get("/login")
def show_login() -> Any:
    csrf = ensure_csrf_token()
    form = f"""
    <form method="post" action="{url_for("eos_auth.submit_login")}" aria-label="Login">
      <input type="hidden" name="csrf_token" value="{csrf}">
      <label for="email">Email</label>
      <input id="email" name="email" type="email" required autocomplete="username">
      <label for="password">Password</label>
      <input id="password" name="password" type="password" required autocomplete="current-password">
      <label><input type="checkbox" name="remember_me" value="1"> Remember me</label>
      <button type="submit">Sign in</button>
    </form>
    """
    return _page("Sign in", form)


@auth_bp.post("/login")
def submit_login() -> Any:
    csrf_error = _require_csrf()
    if csrf_error:
        return _page("Sign in", "", error=csrf_error), 400
    controller = AuthController(get_auth_dependencies())
    try:
        result = controller.login(
            email=request.form.get("email") or "",
            password=request.form.get("password") or "",
            remember_me=bool(request.form.get("remember_me")),
            client_key=_client_key(),
        )
    except AuthenticationError as exc:
        csrf = ensure_csrf_token()
        form = f"""
        <form method="post" action="{url_for("eos_auth.submit_login")}" aria-label="Login">
          <input type="hidden" name="csrf_token" value="{csrf}">
          <label for="email">Email</label>
          <input id="email" name="email" type="email" required>
          <label for="password">Password</label>
          <input id="password" name="password" type="password" required>
          <label><input type="checkbox" name="remember_me" value="1"> Remember me</label>
          <button type="submit">Sign in</button>
        </form>
        """
        return _page("Sign in", form, error=auth_error_message(exc)), 401
    assert result.session is not None
    _store_session(result.session)
    return redirect(with_query(DASHBOARD_PATH, student_id=result.session.user_id))


@auth_bp.post("/logout")
def logout() -> Any:
    csrf_error = _require_csrf()
    if csrf_error:
        return _page("Sign out", "", error=csrf_error), 400
    claims = _load_claims()
    AuthController(get_auth_dependencies()).logout(
        claims.user_id if claims else None
    )
    _clear_session()
    return redirect(url_for("eos_auth.show_login"))


@auth_bp.get("/verify-email")
def show_verify_email() -> Any:
    csrf = ensure_csrf_token()
    token = (request.args.get("token") or "").strip()
    form = f"""
    <form method="post" action="{url_for("eos_auth.submit_verify_email")}" aria-label="Verify email">
      <input type="hidden" name="csrf_token" value="{csrf}">
      <label for="token">Verification token</label>
      <input id="token" name="token" value="{token}" required>
      <button type="submit">Verify email</button>
    </form>
    """
    return _page("Verify email", form)


@auth_bp.post("/verify-email")
def submit_verify_email() -> Any:
    csrf_error = _require_csrf()
    if csrf_error:
        return _page("Verify email", "", error=csrf_error), 400
    controller = AuthController(get_auth_dependencies())
    try:
        result = controller.verify_email(
            token=request.form.get("token") or "",
            client_key=_client_key(),
        )
    except AuthenticationError as exc:
        return _page("Verify email", "", error=auth_error_message(exc)), 400
    return _page(
        "Verify email",
        f'<p><a href="{url_for("eos_auth.show_login")}">Sign in</a></p>',
        message=result.message,
    )


@auth_bp.get("/forgot-password")
def show_forgot_password() -> Any:
    csrf = ensure_csrf_token()
    form = f"""
    <form method="post" action="{url_for("eos_auth.submit_forgot_password")}" aria-label="Forgot password">
      <input type="hidden" name="csrf_token" value="{csrf}">
      <label for="email">Email</label>
      <input id="email" name="email" type="email" required>
      <button type="submit">Send reset link</button>
    </form>
    """
    return _page("Forgot password", form)


@auth_bp.post("/forgot-password")
def submit_forgot_password() -> Any:
    csrf_error = _require_csrf()
    if csrf_error:
        return _page("Forgot password", "", error=csrf_error), 400
    result = AuthController(get_auth_dependencies()).request_password_reset(
        email=request.form.get("email") or "",
        client_key=_client_key(),
    )
    return _page("Forgot password", "", message=result.message)


@auth_bp.get("/reset-password")
def show_reset_password() -> Any:
    csrf = ensure_csrf_token()
    token = (request.args.get("token") or "").strip()
    form = f"""
    <form method="post" action="{url_for("eos_auth.submit_reset_password")}" aria-label="Reset password">
      <input type="hidden" name="csrf_token" value="{csrf}">
      <label for="token">Reset token</label>
      <input id="token" name="token" value="{token}" required>
      <label for="new_password">New password</label>
      <input id="new_password" name="new_password" type="password" required>
      <button type="submit">Reset password</button>
    </form>
    """
    return _page("Reset password", form)


@auth_bp.post("/reset-password")
def submit_reset_password() -> Any:
    csrf_error = _require_csrf()
    if csrf_error:
        return _page("Reset password", "", error=csrf_error), 400
    controller = AuthController(get_auth_dependencies())
    try:
        result = controller.reset_password(
            token=request.form.get("token") or "",
            new_password=request.form.get("new_password") or "",
            client_key=_client_key(),
        )
    except AuthenticationError as exc:
        return _page("Reset password", "", error=auth_error_message(exc)), 400
    return _page(
        "Reset password",
        f'<p><a href="{url_for("eos_auth.show_login")}">Sign in</a></p>',
        message=result.message,
    )


@auth_bp.get("/change-password")
def show_change_password() -> Any:
    csrf = ensure_csrf_token()
    form = f"""
    <form method="post" action="{url_for("eos_auth.submit_change_password")}" aria-label="Change password">
      <input type="hidden" name="csrf_token" value="{csrf}">
      <label for="current_password">Current password</label>
      <input id="current_password" name="current_password" type="password" required>
      <label for="new_password">New password</label>
      <input id="new_password" name="new_password" type="password" required>
      <button type="submit">Change password</button>
    </form>
    """
    return _page("Change password", form)


@auth_bp.post("/change-password")
def submit_change_password() -> Any:
    csrf_error = _require_csrf()
    if csrf_error:
        return _page("Change password", "", error=csrf_error), 400
    claims = _load_claims()
    if claims is None:
        return redirect(url_for("eos_auth.show_login"))
    controller = AuthController(get_auth_dependencies())
    try:
        result = controller.change_password(
            user_id=claims.user_id,
            current_password=request.form.get("current_password") or "",
            new_password=request.form.get("new_password") or "",
            client_key=_client_key(),
        )
    except AuthenticationError as exc:
        return _page("Change password", "", error=auth_error_message(exc)), 400
    return _page("Change password", "", message=result.message)


@auth_bp.before_app_request
def enforce_session_timeout() -> None:
    """Invalidate expired authenticated sessions on each request."""
    if not request.path.startswith("/eos/"):
        return
    # Avoid recursion into auth pages that must remain reachable after expiry.
    if request.path.startswith("/eos/auth/"):
        return
    claims = _load_claims()
    if claims is None:
        return
    deps = get_auth_dependencies()
    if deps.auth_service is None:
        return
    controller = AuthController(deps)
    try:
        result = controller.validate_session(claims)
    except AuthenticationError:
        _clear_session()
        return
    if result.session is not None:
        touched = controller.touch_session(result.session)
        _store_session(touched)


def register_auth(
    app: Flask | object,
    *,
    dependencies: AuthAdapterDependencies | None = None,
    secure_cookies: bool = True,
) -> None:
    """Register the authentication blueprint and bind dependencies."""
    register = getattr(app, "register_blueprint", None)
    if register is None:
        raise TypeError("app must support register_blueprint")
    deps = dependencies or AuthAdapterDependencies(
        auth_service=build_authentication_service(expose_tokens=False)
    )
    if isinstance(app, Flask):
        AuthDependencyProvider.bind(app, deps)
        if secure_cookies and not app.config.get("TESTING"):
            apply_secure_cookie_config(app.config, secure=True)
        elif app.config.get("TESTING"):
            apply_secure_cookie_config(app.config, secure=False)
    register(auth_bp)
