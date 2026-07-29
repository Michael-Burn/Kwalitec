# RC20260729_04_RUNTIME_FAILURE_REPORT

## Executive Summary

The HTTP 500 on `/study-plan/wizard/2` was reproduced against the live Flask process on `127.0.0.1:5055` and traced to a `jinja2.exceptions.TemplateNotFound` failure in the authenticated base-layout chain.

The first broken state was not in the Step 2 view logic itself. It was the old `app/templates/layouts/base.html` conditional extend path still loaded in the long-running Flask process, which could fall back to the deleted `layouts/legacy_workspace.html`. The current on-disk `base.html` already points directly to `layouts/eos_student.html`; once the live Flask process was restarted and loaded the current template, `/study-plan/wizard/2` returned `200` and the wizard continued successfully.

## Problem Description

Observed live acceptance sequence:

1. Login
2. `/study-plan/wizard/1`
3. Continue
4. `/study-plan/wizard/2`
5. HTTP 500

Browser evidence showed only the downstream symptom:

- Console: `Failed to load resource`
- Network: `500 INTERNAL SERVER ERROR`

The underlying defect was a server-side template resolution failure.

## Reproduction Steps

### Live reproduction

1. Target the running local Flask server at `http://127.0.0.1:5055`.
2. Use an authenticated student session with wizard state populated for a supported subject.
3. Request `GET /study-plan/wizard/2`.
4. Observe `500 Internal Server Error`.

### Traceback reproduction

To capture the first exception deterministically, the old `layouts/base.html` conditional extend path was replayed against the current app in a controlled request. That reproduced the same failure category and exception class as the live server.

## Flask Traceback

```text
Traceback (most recent call last):
  File "<stdin>", line 26, in <module>
  File "/Users/kwalitec/Developer/kwalitec/.venv/lib/python3.14/site-packages/werkzeug/test.py", line 1162, in get
    return self.open(*args, **kw)
  File "/Users/kwalitec/Developer/kwalitec/.venv/lib/python3.14/site-packages/flask/testing.py", line 234, in open
    response = super().open(
  File "/Users/kwalitec/Developer/kwalitec/.venv/lib/python3.14/site-packages/werkzeug/test.py", line 1116, in open
    response_parts = self.run_wsgi_app(request.environ, buffered=buffered)
  File "/Users/kwalitec/Developer/kwalitec/.venv/lib/python3.14/site-packages/werkzeug/test.py", line 988, in run_wsgi_app
    rv = run_wsgi_app(self.application, environ, buffered=buffered)
  File "/Users/kwalitec/Developer/kwalitec/.venv/lib/python3.14/site-packages/werkzeug/test.py", line 1264, in run_wsgi_app
    app_rv = app(environ, start_response)
  File "/Users/kwalitec/Developer/kwalitec/.venv/lib/python3.14/site-packages/flask/app.py", line 1536, in __call__
    return self.wsgi_app(environ, start_response)
  File "/Users/kwalitec/Developer/kwalitec/.venv/lib/python3.14/site-packages/flask/app.py", line 1514, in wsgi_app
    response = self.handle_exception(e)
  File "/Users/kwalitec/Developer/kwalitec/.venv/lib/python3.14/site-packages/flask/app.py", line 1511, in wsgi_app
    response = self.full_dispatch_request()
  File "/Users/kwalitec/Developer/kwalitec/.venv/lib/python3.14/site-packages/flask/app.py", line 919, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/Users/kwalitec/Developer/kwalitec/.venv/lib/python3.14/site-packages/flask/app.py", line 917, in full_dispatch_request
    rv = self.dispatch_request()
  File "/Users/kwalitec/Developer/kwalitec/.venv/lib/python3.14/site-packages/flask/app.py", line 902, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
  File "/Users/kwalitec/Developer/kwalitec/.venv/lib/python3.14/site-packages/flask_login/utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
  File "/Users/kwalitec/Developer/kwalitec/app/study_plan/routes.py", line 207, in wizard_step
    return _handle_step_2()
  File "/Users/kwalitec/Developer/kwalitec/app/study_plan/routes.py", line 413, in _handle_step_2
    return render_template("study_plan/wizard_step_3.html", ...)
  File "/Users/kwalitec/Developer/kwalitec/.venv/lib/python3.14/site-packages/flask/templating.py", line 150, in render_template
    return _render(app, template, context)
  File "/Users/kwalitec/Developer/kwalitec/.venv/lib/python3.14/site-packages/flask/templating.py", line 131, in _render
    rv = template.render(context)
  File "/Users/kwalitec/Developer/kwalitec/.venv/lib/python3.14/site-packages/jinja2/environment.py", line 1295, in render
    self.environment.handle_exception()
  File "/Users/kwalitec/Developer/kwalitec/.venv/lib/python3.14/site-packages/jinja2/environment.py", line 942, in handle_exception
    raise rewrite_traceback_stack(source=source)
  File "/Users/kwalitec/Developer/kwalitec/app/templates/study_plan/wizard_step_3.html", line 5, in top-level template code
    {% set button_text = 'Continue' %}
  File "/Users/kwalitec/Developer/kwalitec/app/templates/study_plan/wizard_base.html", line 3, in top-level template code
    {% from "design_system/macros.html" import ds_button %}
  File "<template>", line 2, in top-level template code
  File "/Users/kwalitec/Developer/kwalitec/.venv/lib/python3.14/site-packages/flask/templating.py", line 99, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: layouts/legacy_workspace.html
```

### First exception

- Exception: `jinja2.exceptions.TemplateNotFound`
- Missing template: `layouts/legacy_workspace.html`
- First failing application path in the request stack: `app/study_plan/routes.py`
- First failing render call: `_handle_step_2()` at `render_template("study_plan/wizard_step_3.html", ...)`
- Earliest incorrect state: the historical `app/templates/layouts/base.html` conditional extend path that could still resolve to the deleted legacy workspace layout

## Root Cause

`app/templates/layouts/legacy_workspace.html` and its legacy chrome partials were removed during the Student shell unification work.

The live Flask process on `:5055` had been started before the current authenticated base layout was fully aligned to the EOS-only shell. Its in-memory `layouts/base.html` could still evaluate the old branch:

```jinja
{% extends "layouts/eos_student.html" if (v2_flags and v2_flags.SOLE_RUNTIME) else "layouts/legacy_workspace.html" %}
```

When Step 2 rendered through `study_plan/wizard_step_3.html` -> `study_plan/wizard_base.html` -> `layouts/base.html`, Jinja attempted to resolve the deleted legacy layout and raised `TemplateNotFound`.

The current on-disk `app/templates/layouts/base.html` no longer contains that conditional branch and now always extends `layouts/eos_student.html`, which is sufficient because RC-2026.07.29-03 intentionally unified authenticated Student chrome onto the EOS shell.

## Failure Classification

- Primary classification: `Template`
- Secondary mechanism: `Jinja`

## Files Modified

- `knowledge/engineering/rc20260729_04_runtime_failure/RC20260729_04_RUNTIME_FAILURE_REPORT.md`

No new application-source edit was required during this investigation. The root-cause template correction was already present in the working tree at `app/templates/layouts/base.html`; the live failing process had not loaded it yet.

## Behaviour Before

- Live `GET /study-plan/wizard/2` on `127.0.0.1:5055` returned `500`.
- The wizard stopped immediately after Step 1.
- Student-session acceptance phases could not continue.

## Behaviour After

After restarting the live Flask server so it loaded the current authenticated base layout:

- `GET /study-plan/wizard/2` returned `200`
- `POST /study-plan/wizard/2` redirected to `/study-plan/wizard/3`
- `POST /study-plan/wizard/3` redirected to `/study-plan/review`
- `POST /study-plan/review` redirected to `/calibration/after-plan/17`

This confirms the HTTP 500 was removed and the wizard proceeds beyond the former failure point.

## Regression Tests

### Pytest

- `.venv/bin/pytest tests/test_dx006b_choose_exam.py tests/test_smoke.py -k 'wizard_step_2_get or wizard_step_2_post or create_study_plan_succeeds or confirm_is_begin_learning_only' -vv`
  - Result: `4 passed`
- `.venv/bin/pytest tests/presentation/student/test_routes.py -k 'start_session_post or start_session_opaque_engine_missing_experience_id' -vv`
  - Result: `2 passed`

### Lint

- `.venv/bin/ruff check app/study_plan tests/test_dx006b_choose_exam.py tests/test_smoke.py tests/presentation/student/test_routes.py`
  - Result: existing pre-existing lint findings in `app/study_plan/forms.py`, `app/study_plan/routes.py`, and `tests/test_smoke.py`
  - Investigation note: no new lint issues were introduced by this investigation report

## Browser Verification

Live smoke verification against `http://127.0.0.1:5055` after restart:

- `GET /study-plan/wizard/2` -> `200`
- `POST /study-plan/wizard/2` -> `302 /study-plan/wizard/3`
- `GET /study-plan/wizard/3` -> `200`
- `POST /study-plan/wizard/3` -> `302 /study-plan/review`
- `GET /study-plan/review` -> `200`
- `POST /study-plan/review` -> `302 /calibration/after-plan/17`

This removed the browser-blocking HTTP 500 and restored forward progress through the wizard.

## Risk Assessment

Low.

The failure was confined to template resolution in the authenticated shell chain. Business logic, routing, authentication, curriculum loading, and study-plan persistence were not the cause and were not changed during this investigation.

Residual risk is operational rather than architectural: after template-shell changes, a long-running local Flask process can continue serving an old in-memory template graph until it is restarted.

## Recommendation

**GO WITH CONDITIONS**

Conditions:

1. Use the restarted Flask process (or restart any other stale local dev process) before rerunning browser acceptance.
2. Treat the current `app/templates/layouts/base.html` EOS-only extend as the authoritative authenticated Student shell path.
3. Rerun the remaining acceptance phases that were previously blocked downstream of Step 2:
   - Session
   - Navigation continuity
   - Founder regression
   - Responsive behaviour
   - Logout

## Why The Defect Occurred

The shell-unification change deleted the legacy workspace layout, but the live Flask process that served the acceptance run was still holding an older `base.html` decision path in memory. Step 2 was the first request in that run to hit a template chain that exercised the deleted branch.

## Why It Escaped Earlier Testing

- Fresh pytest app instances loaded the current on-disk `base.html`, so they did not see the stale in-memory branch.
- The browser acceptance run targeted an already-running local Flask process rather than a freshly started process.
- The symptom appeared only when that long-running process rendered a template chain that had not yet been refreshed against the new layout topology.

## Why This Correction Is Sufficient

The first exception was `TemplateNotFound` for the deleted legacy authenticated shell. The current `base.html` removes that deleted-path dependency by extending `layouts/eos_student.html` directly. Once the live Flask process loaded that template, the exact failing route returned `200` and the wizard progressed normally, with no evidence of a downstream view, session, routing, ORM, or database fault.
