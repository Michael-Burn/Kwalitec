"""Student Onboarding Flask routes.

Thin HTTP glue over OnboardingController. Collects declarations only; does not
diagnose, recommend, or plan missions. Autosaves each step and resumes
incomplete sessions.
"""

# HTML form markup in f-strings intentionally exceeds the line budget.
# ruff: noqa: E501

from __future__ import annotations

from typing import Any

from flask import (
    Blueprint,
    Flask,
    redirect,
    render_template_string,
    request,
    session,
)

from adapters.flask.auth.csrf import ensure_csrf_token, validate_csrf_token
from adapters.flask.auth.dependency_provider import AUTH_SESSION_KEY
from adapters.flask.dashboard.dependency_provider import STUDENT_SESSION_KEY
from adapters.flask.navigation import DASHBOARD_PATH, ONBOARDING_PATH, with_query
from adapters.flask.onboarding.controller import (
    OnboardingController,
    onboarding_error_message,
)
from adapters.flask.onboarding.dependency_provider import (
    OnboardingAdapterDependencies,
    OnboardingDependencyProvider,
    get_onboarding_dependencies,
)
from adapters.flask.page_renderer import PageRenderer
from application.onboarding.errors import OnboardingApplicationError
from presentation.onboarding import OnboardingViewModel

onboarding_bp = Blueprint(
    "eos_onboarding",
    __name__,
    url_prefix="/eos/onboarding",
)

_PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }}</title>
  <style>
    :root { color-scheme: light; }
    body { font-family: Georgia, "Times New Roman", serif; margin: 0; background:
      linear-gradient(160deg, #eef4f1 0%, #f7f3ea 55%, #e8eef8 100%); color: #1b2420; }
    main { max-width: 42rem; margin: 0 auto; padding: 1.5rem 1.25rem 3rem; }
    header h1 { font-size: clamp(1.75rem, 4vw, 2.35rem); margin: 0.25rem 0; }
    .eyebrow { letter-spacing: 0.04em; text-transform: uppercase; font-size: 0.8rem; opacity: 0.75; }
    .progress { height: 0.55rem; background: #d5ddd8; border-radius: 999px; overflow: hidden; margin: 1rem 0 1.25rem; }
    .progress > span { display: block; height: 100%; background: #2f6f5e; }
    ol.stepper { list-style: none; padding: 0; display: flex; flex-wrap: wrap; gap: 0.4rem; margin: 0 0 1.25rem; }
    ol.stepper li { font-size: 0.75rem; padding: 0.25rem 0.55rem; border-radius: 999px; background: #e4ebe7; }
    ol.stepper li[aria-current="step"] { background: #2f6f5e; color: #fff; }
    ol.stepper li.complete { background: #c7d9d2; }
    form { display: grid; gap: 0.9rem; }
    label { display: grid; gap: 0.3rem; font-size: 0.95rem; }
    input, select, textarea { font: inherit; padding: 0.55rem 0.65rem; border: 1px solid #b7c2bc; border-radius: 0.4rem; background: #fff; }
    .actions { display: flex; flex-wrap: wrap; gap: 0.6rem; margin-top: 0.5rem; }
    button { font: inherit; padding: 0.55rem 0.95rem; border-radius: 0.4rem; border: 1px solid #2f6f5e; background: #2f6f5e; color: #fff; cursor: pointer; }
    button.secondary { background: #fff; color: #1b2420; }
    button.ghost { background: transparent; border-color: transparent; color: #2f6f5e; text-decoration: underline; }
    [role="alert"] { color: #8a1f1f; }
    [role="status"] { color: #1f4d3f; }
    .review { background: rgba(255,255,255,0.7); padding: 0.9rem 1rem; border-radius: 0.5rem; }
    @media (max-width: 640px) { main { padding: 1rem; } }
  </style>
</head>
<body>
  <main>
    <header role="banner" aria-label="Student Onboarding">
      {% if eyebrow %}<p class="eyebrow">{{ eyebrow }}</p>{% endif %}
      <h1>{{ title }}</h1>
      <p>{{ description }}</p>
    </header>
    <div class="progress" role="progressbar" aria-label="Onboarding progress"
         aria-valuemin="0" aria-valuemax="100" aria-valuenow="{{ progress_now }}">
      <span style="width: {{ progress_now }}%"></span>
    </div>
    <ol class="stepper" aria-label="Onboarding progress">
      {% for step in stepper_steps %}
      <li {% if step.current %}aria-current="step"{% endif %} class="{% if step.complete %}complete{% endif %}">{{ step.label }}</li>
      {% endfor %}
    </ol>
    {% if message %}<p role="status">{{ message }}</p>{% endif %}
    {% if error %}<p role="alert">{{ error }}</p>{% endif %}
    {% if review_lines %}
    <section class="review" aria-label="Declaration review">
      <h2>Your declarations</h2>
      <ul>{% for line in review_lines %}<li>{{ line }}</li>{% endfor %}</ul>
    </section>
    {% endif %}
    {{ form_html|safe }}
  </main>
</body>
</html>
"""


def _student_id() -> str:
    auth = session.get(AUTH_SESSION_KEY) or {}
    sid = (auth.get("user_id") or session.get(STUDENT_SESSION_KEY) or "").strip()
    if sid:
        return sid
    return (request.args.get("student_id") or request.form.get("student_id") or "").strip()


def _field_html(field: Any) -> str:
    name = field.name
    value = field.value or ""
    label = field.label
    if field.input_type == "checkbox":
        checked = " checked" if value in {"true", "1", "yes", "on"} else ""
        return (
            f'<label><input type="checkbox" name="{name}" value="true"{checked}> '
            f"{label}</label>"
        )
    if field.input_type == "select":
        options = "".join(
            f'<option value="{key}"{" selected" if key == value else ""}>{text}</option>'
            for key, text in field.options
        )
        required = " required" if field.required else ""
        return (
            f'<label>{label}<select name="{name}"{required}>{options}</select></label>'
        )
    if field.input_type == "textarea":
        required = " required" if field.required else ""
        return (
            f'<label>{label}<textarea name="{name}" rows="3"{required}>'
            f"{value}</textarea></label>"
        )
    input_type = field.input_type if field.input_type in {"text", "number"} else "text"
    required = " required" if field.required else ""
    return (
        f'<label>{label}<input type="{input_type}" name="{name}" value="{value}"'
        f"{required}></label>"
    )


def _form_html(view: OnboardingViewModel, *, csrf: str, onboarding_id: str) -> str:
    fields = "".join(_field_html(field) for field in view.current_step.fields)
    actions = ['<div class="actions">']
    if view.secondary_button is not None:
        actions.append(
            f'<button class="secondary" type="submit" name="action" value="back">'
            f"{view.secondary_button.label}</button>"
        )
    if view.skip_button is not None:
        actions.append(
            f'<button class="ghost" type="submit" name="action" value="skip">'
            f"{view.skip_button.label}</button>"
        )
    if view.primary_button is not None:
        actions.append(
            f'<button type="submit" name="action" value="{view.primary_action_key}">'
            f"{view.primary_button.label}</button>"
        )
    actions.append("</div>")
    return (
        f'<form method="post" action="{ONBOARDING_PATH}" novalidate>'
        f'<input type="hidden" name="csrf_token" value="{csrf}">'
        f'<input type="hidden" name="onboarding_id" value="{onboarding_id}">'
        f'<input type="hidden" name="step" value="{view.current_step.key}">'
        f"{fields}{''.join(actions)}</form>"
    )


def _render(
    view: OnboardingViewModel,
    *,
    message: str = "",
    error: str = "",
) -> str:
    csrf = ensure_csrf_token()
    PageRenderer().for_onboarding(view)
    stepper_steps = [
        {
            "label": step.label,
            "current": step.current,
            "complete": step.complete,
        }
        for step in view.stepper.steps
    ]
    return render_template_string(
        _PAGE,
        title=view.header.title,
        eyebrow=view.header.eyebrow,
        description=view.header.description,
        progress_now=int(round(view.progress_percent)),
        stepper_steps=stepper_steps,
        review_lines=view.review_lines,
        message=message,
        error=error,
        form_html=_form_html(view, csrf=csrf, onboarding_id=view.onboarding_id),
    )


def _payload_from_form(step: str) -> dict[str, Any]:
    form = request.form
    if step == "welcome":
        return {"acknowledged": form.get("acknowledged") == "true"}
    if step == "ifoa_profile":
        return {
            "pathway": form.get("pathway", ""),
            "exam_paper": form.get("exam_paper", ""),
            "intended_sitting_label": form.get("intended_sitting_label", ""),
        }
    if step == "exam_history":
        return {
            "prior_study": form.get("prior_study", ""),
            "core_reading": form.get("core_reading", ""),
            "previous_attempts": form.get("previous_attempts", "0"),
            "sitting_intent": form.get("sitting_intent", ""),
        }
    if step == "weekly_availability":
        return {
            "weekday_minutes": form.get("weekday_minutes", "0"),
            "weekend_minutes": form.get("weekend_minutes", "0"),
            "preferred_session_minutes": form.get("preferred_session_minutes", "60"),
        }
    if step == "confidence":
        return {"band": form.get("band", ""), "notes": form.get("notes", "")}
    if step == "study_habits":
        return {
            "preference": form.get("preference", ""),
            "typical_start_time": form.get("typical_start_time", ""),
        }
    if step == "optional_diagnostic":
        return {"choice": form.get("choice", "skipped")}
    if step == "review":
        return {"confirmed": form.get("confirmed") == "true"}
    return {}


def _empty_view() -> OnboardingViewModel:
    from presentation.onboarding import OnboardingPresenter

    return OnboardingPresenter.present(None)


@onboarding_bp.get("/")
def show_onboarding() -> Any:
    """Start or resume onboarding for the current student."""
    student_id = _student_id()
    if not student_id:
        return redirect("/eos/auth/login")
    controller = OnboardingController(get_onboarding_dependencies())
    try:
        result = controller.start(student_id=student_id)
    except OnboardingApplicationError as exc:
        return _render(_empty_view(), error=onboarding_error_message(exc)), 400
    return _render(controller.present(result), message=result.message)


@onboarding_bp.post("/")
def submit_onboarding() -> Any:
    """Autosave the current step and navigate according to the submitted action."""
    if not validate_csrf_token(request.form.get("csrf_token")):
        return _render(_empty_view(), error="Invalid security token. Please try again."), 400
    student_id = _student_id()
    if not student_id:
        return redirect("/eos/auth/login")
    onboarding_id = (request.form.get("onboarding_id") or "").strip()
    step = (request.form.get("step") or "").strip()
    action = (request.form.get("action") or "advance").strip()
    controller = OnboardingController(get_onboarding_dependencies())
    try:
        if action == "back":
            result = controller.go_back(
                onboarding_id=onboarding_id, student_id=student_id
            )
        elif action == "skip":
            result = controller.skip_optional(
                onboarding_id=onboarding_id, student_id=student_id
            )
        else:
            payload = _payload_from_form(step)
            result = controller.save_step(
                onboarding_id=onboarding_id,
                student_id=student_id,
                step=step,
                payload=payload,
            )
            if action == "complete":
                result = controller.complete(
                    onboarding_id=onboarding_id, student_id=student_id
                )
            elif action == "advance" and step != "review":
                result = controller.advance(
                    onboarding_id=onboarding_id, student_id=student_id
                )
    except OnboardingApplicationError as exc:
        try:
            current = controller.start(student_id=student_id)
            view = controller.present(current)
        except OnboardingApplicationError:
            view = _empty_view()
        return _render(view, error=onboarding_error_message(exc)), 400

    if result.completed is not None:
        return redirect(
            with_query(
                result.completed.redirect_path or DASHBOARD_PATH,
                student_id=student_id,
            )
        )
    return _render(controller.present(result), message=result.message)


def register_onboarding(
    app: Flask | object,
    *,
    dependencies: OnboardingAdapterDependencies,
) -> None:
    """Register the onboarding blueprint and bind injected dependencies.

    ``dependencies`` is required. Production wiring supplies services built on
    ``SqlAlchemyProductUnitOfWork`` via ``wire_adapter_layer``; tests inject
    explicit collaborators. No in-memory fallback is constructed here.
    """
    register = getattr(app, "register_blueprint", None)
    if register is None:
        raise TypeError("app must support register_blueprint")
    if dependencies.onboarding_service is None:
        raise TypeError(
            "OnboardingAdapterDependencies.onboarding_service is required; "
            "wire production onboarding through application composition"
        )
    if isinstance(app, Flask):
        OnboardingDependencyProvider.bind(app, dependencies)
    register(onboarding_bp)


__all__ = ["onboarding_bp", "register_onboarding"]
