# RELEASE_CANDIDATE_CERTIFICATE.md

**Programme:** RC-001 — Release Candidate Certification  
**Release Candidate ID:** `RC-2026.07.29-01`  
**Issued (UTC):** `2026-07-28T23:10:00Z`

---

## Outcome

# CERTIFIED WITH CONDITIONS

The Release Candidate is reproducible under the recorded bindings.

Subsequent validation programmes **may begin**, provided every condition below is observed.

---

## Certification checklist

| Item | Result |
|---|---|
| Clean repository | **FAIL** → waived via frozen worktree digest (Condition 1) |
| Correct commit | **PASS** — `f17058862baf9aa8c6f416c6fa7bd26739812fb8` checked out |
| Correct branch | **PASS** — `feature/ap-002-assessment-engine` |
| Fresh runtime | **PASS** — PID `83805`, port `5201`, start after source mtimes, `--no-reload` |
| Fresh database | **PASS** — `/tmp/rc001_RC-2026.07.29-01.sqlite3`, empty Studio/publication tables |
| Current migration | **PASS** — `202607280080` (head) |
| Approved fixtures | **PASS** — EV-001 CS1V CMP/Syllabus SHA-256 frozen |
| Matching application identity | **PASS** — version `2.0.0` on Console / Settings / `/health` |
| Release Candidate ID assigned | **PASS** — `RC-2026.07.29-01` |

---

## Conditions

1. **Dirty working tree.** Repository is not clean. The certified code image is HEAD plus the frozen application worktree digest  
   `5e8e92256cbd1e728e5ddb8f8ec40b1f9f26ccf1ac84ddb0addd36d02593915e`.  
   Any file change under the freeze set invalidates this RC. A clean-tree re-certification (commit + new RC ID) is recommended before commercial gate programmes if governance requires a clean tree.

2. **Bound runtime.** Validation must use `http://127.0.0.1:5201` (PID `83805` as certified). Do not use orphan listeners on `:5130`, `:5128`, `:5001`, or `:5055`. Process restart requires a new RC.

3. **Bound database.** Validation must use `DATABASE_URL=sqlite:////tmp/rc001_RC-2026.07.29-01.sqlite3` (or an exact pre-programme copy). Do not use `instance/kwalitec.sqlite3`.

4. **Bound fixtures.** Upload only the approved CMP/Syllabus hashes in [FIXTURE_CERTIFICATION.md](FIXTURE_CERTIFICATION.md). Subject code prescription: `CS1V`.

5. **Mandatory citation.** Every subsequent report must include:

   ```text
   Release Candidate: RC-2026.07.29-01
   ```

---

## Authorised next programmes

With this certificate, the project may proceed to:

1. FV-001B — Final Founder Studio Blind Validation (re-run on this RC)
2. FV-001C — Student Blind Validation (only after FV-001B GO / GO WITH CONDITIONS on this RC)
3. CQ-007 — Internal Alpha Readiness Review

---

## Invalidation

Any change to source code, runtime configuration, database schema, or validation fixtures invalidates `RC-2026.07.29-01` and requires a new RC certification.

---

## Certificate references

| Document |
|---|
| [SOURCE_CERTIFICATION.md](SOURCE_CERTIFICATION.md) |
| [RUNTIME_CERTIFICATION.md](RUNTIME_CERTIFICATION.md) |
| [DATABASE_CERTIFICATION.md](DATABASE_CERTIFICATION.md) |
| [FIXTURE_CERTIFICATION.md](FIXTURE_CERTIFICATION.md) |
| [APPLICATION_IDENTITY.md](APPLICATION_IDENTITY.md) |
| [ENVIRONMENT_INTEGRITY.md](ENVIRONMENT_INTEGRITY.md) |
| [RC001_EXECUTIVE_SUMMARY.md](RC001_EXECUTIVE_SUMMARY.md) |
| Evidence tree `_evidence/` |
