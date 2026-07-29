# RC-001 — Executive Summary

**Programme:** RC-001 — Release Candidate Certification  
**Status:** Complete  
**Outcome:** **CERTIFIED WITH CONDITIONS**  
**Release Candidate ID:** `RC-2026.07.29-01`

---

## Why this programme existed

EV-002 showed EV-001 and FV-001B Final were both locally correct but compared across different processes, databases, fixtures, and loaded code. RC-001 freezes one environment so every later validation cites the same Release Candidate.

This programme does **not** test product functionality.

---

## What was certified

| Layer | Binding |
|---|---|
| Source | Commit `f1705886…` on `feature/ap-002-assessment-engine` + frozen worktree digest `5e8e9225…` |
| Runtime | Fresh Flask PID `83805`, `http://127.0.0.1:5201`, debug/reload **off**, started `2026-07-28T23:04:14Z` |
| Database | New SQLite `sqlite:////tmp/rc001_RC-2026.07.29-01.sqlite3`, Alembic `202607280080`, admin-only seed |
| Fixtures | EV-001 CS1V Official CMP + Syllabus (SHA-256 recorded) |
| Application | Version `2.0.0`; empty Subjects; identity screenshots captured |

Artefacts: `knowledge/release/rc001_release_candidate/`

---

## Conditions (summary)

1. Working tree was **not** clean — code image frozen by digest instead of a clean commit.
2. Only port **5201** / DB path / fixture hashes above are in-bounds.
3. Every later report must cite `Release Candidate: RC-2026.07.29-01`.

Full text: [RELEASE_CANDIDATE_CERTIFICATE.md](RELEASE_CANDIDATE_CERTIFICATE.md)

---

## What may begin now

1. **FV-001B** — Final Founder Studio Blind Validation (on this RC)  
2. **FV-001C** — only after FV-001B GO / GO WITH CONDITIONS on this RC  
3. **CQ-007** — Internal Alpha Readiness Review  

Any source, runtime, schema, or fixture change → invalidate RC → re-run RC-001.
