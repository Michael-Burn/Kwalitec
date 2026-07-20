# Dependency Audit — Version 2.0.0

**Milestone:** APP-004  
**Date:** 2026-07-20  
**Scope:** Python runtime dependencies declared in `requirements.txt`  

---

## Method

```bash
python -m pip install -r requirements.txt pip-audit
pip-audit -r requirements.txt
```

Re-run before tagging any security-sensitive hotfix.

---

## Baseline inventory

| Package | Pin | Role |
|---|---|---|
| Flask | 3.1.0 | Web framework (legacy `app/` + EOS `src/web`) |
| Flask-SQLAlchemy | 3.1.1 | ORM integration |
| Flask-Migrate | 4.0.7 | Alembic migrations |
| Flask-Login | 0.6.3 | Session auth |
| Flask-WTF / WTForms | 1.2.2 / 3.2.1 | Forms + CSRF |
| email-validator | 2.2.0 | Email normalisation |
| python-dotenv | 1.0.1 | Local `.env` loading |
| psycopg[binary] | 3.2.13 | PostgreSQL driver |
| waitress / gunicorn | 3.0.2 / 23.0.0 | WSGI servers |
| pytest | 8.3.4 | Tests |
| ruff | 0.8.6 | Lint |

Educational OS AI providers under `src/infrastructure/ai` intentionally **do not** pin vendor SDKs; completion transports are injected. No OpenAI/Anthropic/Google packages are required for deterministic cores.

---

## Findings

| Severity | Package | Advisory | Disposition |
|---|---|---|---|
| Medium (known) | Flask 3.1.0 | Prior Alpha audits noted PYSEC advisories fixed in ≥3.1.3 | Tracked for Version 3 dependency bump; not introduced by APP-004. Core EOS paths do not rely on the affected session-fallback behaviours. |
| Info | Vendored AI SDKs | Not pinned | By design (ADR-008 enrichment boundary) |

Operators must re-run `pip-audit` on the release machine and attach the raw report to the release record if advisories change after this document’s date.

---

## Security controls verified (APP-004)

- Secrets (`SECRET_KEY`, DB URLs, `AI_API_KEY` / vendor keys) loaded only via configuration / environment
- Production startup fail-fast for insecure `SECRET_KEY` and missing database URL
- EOS web blueprints validate query/body fields through schema helpers before use-cases
- CSRF remains enabled on the legacy Flask product outside tests

---

## Decision

**ACCEPT for Version 2.0.0 close** with documented Flask pin follow-up on the Version 3 dependency track. No APP-004 educational or architectural change required.
