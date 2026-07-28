# Dependency Audit — Version 2.0.0

**Milestone:** APP-004 (baseline) · **Policy update:** EI-001.2 (2026-07-28)  
**Scope:** Python runtime dependencies declared in `requirements.txt`  

**Governing policy (EI-001.2):** [`docs/security/DEPENDENCY_ASSURANCE_POLICY.md`](../security/DEPENDENCY_ASSURANCE_POLICY.md)  
**Accepted findings / Security HOLD:** [`docs/security/DEPENDENCY_ACCEPTED_FINDINGS.md`](../security/DEPENDENCY_ACCEPTED_FINDINGS.md)  
**Reproducible command:** `./scripts/dependency_audit.sh`

---

## Method

```bash
python -m pip install -r requirements.txt pip-audit
./scripts/dependency_audit.sh --output pip-audit-release.txt
```

CI hard-fails on any advisory **not** listed in `docs/security/dependency_accepted_vulns.txt`. Soft-warn gates are retired (ER-RB-07).

Re-run before tagging any security-sensitive hotfix or Version 1 / RC claim package.

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
| Medium (HOLD) | Flask 3.1.0 | PYSEC-2026-1377 / PYSEC-2026-2151 (fix ≥3.1.3) | Security HOLD — see `DEPENDENCY_ACCEPTED_FINDINGS.md`; bump tracked as ER-TD-M04 |
| Low (accepted) | python-dotenv 1.0.1 | PYSEC-2026-2270 | Accepted — `load_dotenv()` only |
| Low / non-prod | pytest 8.3.4 | PYSEC-2026-1845 | Accepted — test dependency |

Operators must re-run `./scripts/dependency_audit.sh` on the release machine and attach the raw report to the release record if unaccepted advisories appear (CI will already fail).

---

## Security controls verified (APP-004)

- Secrets (`SECRET_KEY`, DB URLs, `AI_API_KEY` / vendor keys) loaded only via configuration / environment
- Production startup fail-fast for insecure `SECRET_KEY` and missing database URL
- EOS web blueprints validate query/body fields through schema helpers before use-cases
- CSRF remains enabled on the legacy Flask product outside tests

---

## Decision

**ACCEPT for Version 2.0.0 close** with documented Flask pin follow-up (ER-TD-M04).  
**EI-001.2:** dependency assurance policy is enforceable in CI; release evidence is reproducible via `scripts/dependency_audit.sh`.
