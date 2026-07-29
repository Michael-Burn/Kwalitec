# ENVIRONMENT_INTEGRITY.md

**Programme:** RC-001  
**Release Candidate ID:** `RC-2026.07.29-01`

---

## Integrity chain

```text
Source Code  →  Runtime  →  Database  →  Fixtures  →  Application
     ✓*            ✓            ✓            ✓             ✓
```

\* Source passes via **frozen worktree digest** (tree not clean — see conditions).

| Layer | Binding value | Matches RC? |
|---|---|---|
| Source | Commit `f1705886…` + build id `5e8e9225…` | Yes (frozen) |
| Runtime | PID `83805` @ `127.0.0.1:5201`, start `2026-07-28T23:04:14Z`, no-reload | Yes |
| Database | `sqlite:////tmp/rc001_RC-2026.07.29-01.sqlite3`, alembic `202607280080` | Yes |
| Fixtures | CMP/Syllabus SHA-256 as in [FIXTURE_CERTIFICATION.md](FIXTURE_CERTIFICATION.md) | Yes |
| Application | `/health` version `2.0.0`, Console `V2.0.0`, empty Subjects | Yes |

---

## Cross-checks performed

| Check | Result |
|---|---|
| Runtime `DATABASE_URL` equals certified DB path | **PASS** (log: external DATABASE_URL set; seed file present) |
| Runtime migrations == DB `alembic_version` == head | **PASS** (`202607280080`) |
| Runtime start ≥ latest PI-002R source mtimes | **PASS** |
| Application Subjects empty ↔ DB studio subjects 0 | **PASS** |
| Fixtures hashed and stored under RC evidence tree | **PASS** |
| Health `/health` served by RC port only | **PASS** (`http://127.0.0.1:5201/health`) |
| Stale `:5130` / other orphans not bound to RC | **PASS** (documented; excluded) |

---

## Mismatch policy

Any of the following **immediately invalidates** `RC-2026.07.29-01`:

1. Worktree digest ≠ `5e8e92256cbd1e728e5ddb8f8ec40b1f9f26ccf1ac84ddb0addd36d02593915e`
2. Different Flask PID / port / start without re-certification
3. Different `DATABASE_URL` or polluted subject/publication rows not created by the current programme under this RC
4. Different CMP/Syllabus SHA-256
5. Application version / migration head drift

No assumptions. Re-measure; if mismatch → new RC certification.

---

## Single environment declaration

All subsequent programmes (FV-001B Final re-run, FV-001C, CQ-007, …) that cite this Release Candidate declare they executed against **this exact chain**. Cross-programme comparison is valid only when each report includes:

```text
Release Candidate: RC-2026.07.29-01
```
