# Beta Readiness Checklist

**Status:** Permanent Cursor governance  
**Companion:** [`knowledge/version2/INTERNAL_ALPHA_CHECKLIST.md`](../knowledge/version2/INTERNAL_ALPHA_CHECKLIST.md), [`knowledge/version2/ALPHA_READINESS_FOUNDER_UX.md`](../knowledge/version2/ALPHA_READINESS_FOUNDER_UX.md)

Permanent checklist for progressing from development through Closed Beta to Launch Candidate. Items are cumulative — LC requires all prior stages.

---

## Foundation

| Area | Requirement | Status marker |
|---|---|---|
| **Authentication** | Argon2 hashing, CSRF, secure cookies, session timeout, account lockout, invite-only registration | ☐ |
| **Onboarding** | Full wizard (exam target, history, availability, confidence); twin initialization | ☐ |
| **Student Twin** | Durable twin persistence; evidence-linked state; no bypass paths | ☐ |
| **Educational Pipeline** | End-to-end orchestration; recommendations from pipeline only; architecture tests green | ☐ |
| **Persistence** | PostgreSQL in production; Alembic migrations; backup strategy | ☐ |

---

## Operations

| Area | Requirement | Status marker |
|---|---|---|
| **Monitoring** | Health endpoint; deploy fingerprint; error rate visibility | ☐ |
| **Logging** | Structured logging at INFO; no credential leakage; pipeline observability | ☐ |
| **Backups** | Pre-migrate snapshots; documented restore procedure | ☐ |
| **CI/CD** | GitHub Actions green (pytest + ruff); automated deploy to staging/production | ☐ |

---

## Quality

| Area | Requirement | Status marker |
|---|---|---|
| **Accessibility** | WCAG contrast via design tokens; keyboard navigation; form labels | ☐ |
| **Architecture** | `tests/architecture/` mandatory gates green | ☐ |
| **Curriculum** | V1 flat + V2 hierarchical both loadable and traversable | ☐ |
| **Security** | Secrets in env; rate limiting on auth; least-privilege DB user | ☐ |

---

## Closed Beta

Prerequisites: all Foundation + Operations + Quality items complete.

| Area | Requirement | Status marker |
|---|---|---|
| **Dual-run stable** | V1 home at `/`; V2 student at `/student`; no sole-runtime flag | ☐ |
| **Durable store** | `KWALITEC_V2_DURABLE_STORE=1` with evidence events persisted | ☐ |
| **Cohort onboarding** | Invited learners complete onboarding → twin → first session | ☐ |
| **Founder visibility** | Evidence gates, operational health, feedback intake | ☐ |
| **Rollback plan** | Documented flag rollback without data loss | ☐ |

---

## Launch Candidate

Prerequisites: Closed Beta exercised with real cohort; no P0/P1 blockers open.

| Area | Requirement | Status marker |
|---|---|---|
| **Sole runtime decision** | Explicit go/no-go on `KWALITEC_V2_SOLE_RUNTIME` | ☐ |
| **Performance** | Session and dashboard load within acceptable bounds under cohort load | ☐ |
| **Data compatibility** | Migration path for existing alpha users documented | ☐ |
| **Release protocol** | Full [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) passed on candidate tag | ☐ |
| **Support runbook** | Known limitations, escalation path, and reset procedures documented | ☐ |

---

## Environment reference (Internal Alpha)

```bash
KWALITEC_V2_STUDENT_EXPERIENCE=1
KWALITEC_V2_DURABLE_STORE=1
KWALITEC_V2_INJECT_ENGINES=1
KWALITEC_V2_SEED_DEMO=0
KWALITEC_V2_FOUNDER_INTELLIGENCE=1
# Do NOT set KWALITEC_V2_SOLE_RUNTIME until Launch Candidate
```

See [`.env.example`](../.env.example) and [`render.yaml`](../render.yaml) for production defaults.

---

## How to use this checklist

1. Mark items complete only with evidence (test output, deploy log, or operator sign-off).
2. Do not advance stage with open P0 blockers.
3. Update this file only when readiness criteria change via ADR or release protocol — not per-milestone.
