# Kwalitec

An intelligent learning platform that adapts study plans, tracks mastery, and optimizes exam preparation for demanding professional qualifications.

> Reduce decisions. Increase learning.

[![Python](https://img.shields.io/badge/python-3.11+-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.1-000000?style=flat-square&logo=flask&logoColor=white)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-157%20passed-brightgreen?style=flat-square)](https://github.com)
[![Render](https://img.shields.io/badge/deploy-Render-46E3B7?style=flat-square)](https://render.com)
[![License](https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square)](LICENSE)

---

Kwalitec is a production-ready Flask application that helps students prepare for demanding professional examinations by combining adaptive learning, intelligent study planning, mastery tracking, exam readiness analytics, and explainable recommendations into a single coherent platform.

Unlike generic study planners that leave you to decide what to work on, Kwalitec observes your performance, recalibrates your priorities daily, and generates a concrete mission for every study session. It is **more than a study planner—it is an adaptive learning platform** built on the belief that disciplined learning, backed by data, produces better outcomes than motivation alone.

## Core Features

- **Adaptive Learning Engine**—Spaced repetition scheduling and mastery scoring that adjust to your actual performance over time.
- **Intelligent Study Planning**—Exam date-driven planning that distributes topics across available study days and dynamically rebalances as progress shifts.
- **Daily Mission Optimizer**—Every day, Kwalitec generates a prioritized list of learning tasks based on urgency, readiness, and workload constraints.
- **Exam Readiness Analytics**—Track syllabus coverage, projected scores, and whether you are on pace to pass before exam day.
- **Recommendation Engine**—Deterministic, explainable suggestions for what to study next, grounded entirely in your own learning history.
- **Decision Journal**—Record which recommendations you accepted or dismissed, building an audit trail of your learning decisions.
- **Performance Analytics**—Visual dashboards showing mastery trends, time investment, and curriculum coverage.
- **Burnout Monitor**—Automated workload pacing that flags when your study load risks unsustainable intensity.
- **Secure Backup & Restore**—Export and restore your learning data so you never lose progress.
- **Production-Ready Render Deployment**—One-click blueprint deploy to Render with PostgreSQL, pre-configured for production.
- **Automatic First-Run Database Initialization**—On production startup, migrations and admin creation run automatically—no shell access or pre-deploy commands needed.
- **Automated Test Suite**—157 tests covering models, services, routes, configuration, startup initialization, and error handling with a CI pipeline on every push.

## Why Kwalitec?

Professional examinations—such as actuarial, legal, medical, and engineering qualifications—demand sustained consistency across months of preparation. The hardest part is not the material itself; it is the daily decision of **what to study next**.

Kwalitec eliminates that cognitive burden. Each recommendation is deterministic, explainable, and derived entirely from your own learning history. There is no black-box AI, no external APIs calling the shots. Every suggestion can be traced back to your performance data, your available time, and your exam deadline.

> **The philosophy:** You bring the discipline. Kwalitec provides the direction.

## Project Structure

```
kwalitec/
├── app/
│   ├── __init__.py              # Application factory + error handlers
│   ├── config.py                # Configuration classes
│   ├── extensions.py            # Flask extensions (db, migrate, login, csrf)
│   ├── analytics/               # Learning analytics blueprint
│   ├── auth/                    # Authentication blueprint
│   ├── dashboard/               # Dashboard blueprint
│   ├── mission/                 # Mission management blueprint
│   ├── models/                  # SQLAlchemy models
│   ├── services/                # Business logic layer
│   │   └── startup_service.py   # First-run DB initialization (production)
│   ├── settings/                # User settings blueprint
│   ├── study_plan/              # Study plan wizard blueprint
│   ├── static/                  # CSS, JS, images
│   ├── templates/               # Jinja2 templates
│   └── utils/                   # Utility helpers
├── migrations/                  # Alembic migration scripts
├── tests/                       # pytest test suite (157 tests)
├── .github/workflows/           # CI configuration
├── run.py                       # Development entry point
├── wsgi.py                      # Production WSGI entry point
├── requirements.txt             # Python dependencies
├── pyproject.toml               # Project metadata + tool config
├── render.yaml                  # Render deployment spec
├── .env.example                 # Environment variable template
└── .gitignore
```

## Local Setup

### Prerequisites

- Python 3.11 or later
- Git

### 1. Clone and create a virtual environment

```bash
git clone <repository-url> kwalitec
cd kwalitec
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

For development, also install test and lint tools:

```bash
pip install pytest ruff
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and set a strong `SECRET_KEY`:

```
SECRET_KEY=<generate-a-random-string>
```

### 4. Run database migrations

```bash
flask --app run.py db upgrade
```

### 5. Create the initial user

Registration is intentionally not exposed. Create the initial administrator via the bootstrap CLI:

```bash
export ADMIN_EMAIL="you@example.com"
export ADMIN_PASSWORD="change-me"
flask --app run.py create-admin
```

### 6. Start the development server

```bash
flask --app run.py run
```

Open http://127.0.0.1:5000 and sign in.

### 7. Run the test suite

```bash
python -m pytest tests/ -v
```

### 8. Lint the codebase

```bash
ruff check app/ tests/
```

## Deployment

### Render

The included `render.yaml` defines a Render web service with a PostgreSQL database. To deploy:

1. Push the repository to GitHub.
2. In Render, create a new **Blueprint** and connect your repository.
3. Render will automatically:
   - Detect the `render.yaml` configuration
   - Create a web service (`kwalitec`)
   - Provision a PostgreSQL database (`kwalitec-db`)
   - Install Python dependencies (build phase)
   - Start the app with Waitress via `wsgi:app`

On the **first application startup**, the `StartupService` automatically:

- Applies all pending Alembic migrations (equivalent to `flask db upgrade`) using the Alembic Python API
- Creates the initial administrator user from `ADMIN_EMAIL` / `ADMIN_PASSWORD`

This eliminates the need for shell access or pre-deploy commands. The
initializer is production-safe: it is idempotent, never drops tables, never
recreates existing users, never reruns migrations unnecessarily, and catches
all exceptions so the application can always start. It only runs when
`APP_ENV=production`; local development and pytest are unaffected.

#### Environment Variables (Render)

| Variable | Source | Description |
|---|---|---|
| `APP_ENV` | Static: `production` | Activates production config and automatic startup initialization |
| `FLASK_APP` | Static: `wsgi.py` | WSGI entry point |
| `SECRET_KEY` | Auto-generated | Cryptographically random key |
| `DATABASE_URL` | From database | PostgreSQL connection string |
| `ADMIN_EMAIL` | Environment variable | Administrator email (required for first-run admin creation) |
| `ADMIN_PASSWORD` | Environment variable | Administrator password (required for first-run admin creation) |

> **No shell access required.** Set `ADMIN_EMAIL` and `ADMIN_PASSWORD` in the
> Render environment variables panel before the first deploy. The database
> will be migrated and the admin user created automatically on startup. If
> either variable is missing, a warning is logged and startup continues
> without crashing—you can add them later and restart.

See **[Production Bootstrap](#production-bootstrap)** below for the manual
CLI alternative.

### Manual Deployment

Any WSGI server can serve the application:

```bash
waitress-serve --port=8000 wsgi:app
# or
gunicorn wsgi:app
```

Ensure `APP_ENV=production` and a strong `SECRET_KEY` are set. On first
startup the database will be migrated and the admin user created
automatically (see above).

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check (public) |
| GET | `/` | Redirects to dashboard |
| GET/POST | `/auth/login` | Login page |
| POST | `/auth/logout` | Log out |
| GET | `/dashboard/` | Main dashboard |
| GET | `/missions/` | Mission list |
| GET | `/missions/review/<id>` | Review a mission |
| GET | `/study-plan/` | Study plans list |
| GET | `/study-plan/wizard/<step>` | Study plan wizard |
| GET | `/analytics/` | Learning analytics |
| GET | `/settings/` | User settings |

## Development Principles

- **Small, cohesive modules.** Each blueprint and service has a single responsibility.
- **Application factory pattern.** `create_app()` enables testing and flexible configuration.
- **Blueprints for HTTP, services for logic.** Clear separation between web and business layers.
- **Deterministic calculations.** No external APIs or black-box AI are used for core features.
- **Test-driven confidence.** Tests cover models, services, routes, configuration, startup initialization, and error handling.
- **Disciplined learning first.** Every feature supports deliberate, data-informed study habits.

## Production Bootstrap

### Automatic Initialization (Recommended)

On Render Free deployments, the `StartupService` handles first-run database
initialization automatically during application startup—no shell access or
pre-deploy commands required.

When `APP_ENV=production`, the service runs once at startup and:

1. **Checks migration state** — Compares the Alembic revision stamped in the
   database against the head revision from the migration scripts.
2. **Applies migrations** — If the database is behind, runs `alembic upgrade
   head` programmatically (no subprocess). If already up to date, skips.
3. **Creates the admin user** — If no users exist and both `ADMIN_EMAIL` and
   `ADMIN_PASSWORD` are set, creates the administrator. If credentials are
   missing, logs a warning and continues.

The service is **idempotent** and **safe**:

- Never drops tables
- Never recreates existing users
- Never reruns migrations unnecessarily
- Catches all startup exceptions
- Never prevents the Flask application from starting
- No-op in development and testing

#### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `ADMIN_EMAIL` | Yes (first run) | Administrator email address |
| `ADMIN_PASSWORD` | Yes (first run) | Administrator plaintext password (hashed before storage) |

If `ADMIN_EMAIL` or `ADMIN_PASSWORD` is not set, a warning is logged and
startup continues without crashing. Set them later and restart to create the
admin user.

### Manual CLI Alternative

The `create-admin` Flask CLI command bootstraps the initial administrator
account manually. It is designed to be run once, immediately after applying
database migrations.

If any `User` records already exist in the database the command prints
`Administrator already exists.` and exits successfully (exit code 0) without
making changes. This makes it safe to run the command on every deploy—it is
idempotent by design.

```bash
flask --app wsgi.py db upgrade
flask --app wsgi.py create-admin
```

For local development, export the variables inline:

```bash
export ADMIN_EMAIL="admin@example.com"
export ADMIN_PASSWORD="super-secret-password"
flask --app run.py create-admin
```

The command exits with a non-zero status and a descriptive error if either
`ADMIN_EMAIL` or `ADMIN_PASSWORD` is missing.

## License

MIT