# RCV001_IMPLEMENTATION_REPORT.md

**Programme:** RCV-001 — Production Curriculum Recovery  
**Date:** 2026-07-30  
**Operator harness:** `knowledge/engineering/rcv001_production_curriculum_recovery/rcv001_recover.py`  
**Evidence:** `knowledge/evidence/releases/RCV001/`  
**Pre-recovery rollback commit:** `7b1137a`  
**Live deploy tip (unchanged):** `ee1101d9ef7c61201d7d1f0701223bdfdfb6fd7f`

---

## Executive Summary

RCV-001 **did not complete**. Production remains at the pre-recovery published state (**7 sections · 117 topics · 0 objectives**, uncertified).

STEP 1 prerequisites **passed**. Source PDFs, active CMP/Syllabus, workspace `ws-cs1`, and foundation version `1` are present.

STEP 2 **stopped** when `SqlAlchemyGenerationStore.append_snapshot` attempted to persist Generation 1 on production Postgres. PostgreSQL enforced a foreign-key constraint that local SQLite does not (`PRAGMA foreign_keys = 0` locally). Educational nodes were flushed **before** their parent snapshot row existed:

```text
ForeignKeyViolation: ei_educational_nodes.snapshot_id_fkey
Key (snapshot_id)=(snap-081e04ecdb0472e1) is not present in ei_generation_snapshots
```

No architectural redesign was performed. No validation was bypassed. No manual SQL writes were applied. The failed transaction rolled back; production EI tables remain **0 rows** and the active package is unchanged.

**Final Verdict:** `RECOVERY BLOCKED` — minimal application persistence fix required before recovery can continue.

---

## Actions Performed

| Step | Action | Result |
|---:|---|---|
| 0 | Git rollback point `7b1137a` | Done (prior turn) |
| 0b | Read-only backup of active package + foundation structure | Done → `pre_recovery_*_backup.json` |
| 1 | Verify production prerequisites against Render `kwalitec-db` | **PASS** |
| 2 | Extract/normalize local checksum-identical PDFs | **PASS** (syllabus 8 pages; CMP window 30–180) |
| 2a | Optional CMP+syllabus G1–G7 probe (`rcv001-cmp-syllabus`) | **FAIL** — FK violation in `append_snapshot` |
| 2b | Syllabus-authoritative `WorkspaceGenerationService.run_initial_pipeline(ws-cs1)` | **FAIL** — session left in `PendingRollbackError` after 2a; same underlying store defect would block a clean retry |
| 3 | Founder Calibration | **Not reached** |
| 4 | Publication bridge cutover | **Not reached** |
| 5 | Package verify 5/15/73 | **Not reached** |
| 6 | Begin Learning / `EducationalArtefactDeriver` | **Not reached** |
| 7 | Regression surfaces | **Not reached** |

Services invoked (existing only):

- `PyPdfExtractionAdapter`
- `DocumentNormalizationService`
- `WorkspaceGenerationService` / `build_default_orchestrator`
- `GenerationOrchestrator.run_chain`
- `SqlAlchemyGenerationStore.append_snapshot` ← **failure site**

Services **not** reached: `FounderCalibrationService`, `PublicationBridgeService`, `EducationalArtefactDeriver` (post-publish).

---

## Evidence

| Artefact | Path |
|---|---|
| Timeline | `knowledge/evidence/releases/RCV001/timeline.json` |
| Issues (FK + PendingRollback) | `knowledge/evidence/releases/RCV001/issues.json` |
| STEP 1 prerequisites | `knowledge/evidence/releases/RCV001/step1_prerequisites.json` |
| Extraction metrics | `knowledge/evidence/releases/RCV001/extraction_metrics.json` |
| CMP probe meta | `knowledge/evidence/releases/RCV001/cmp_syllabus_g1_g7.json` |
| Syllabus pipeline meta | `knowledge/evidence/releases/RCV001/syllabus_pipeline.json` |
| Before package | `knowledge/evidence/releases/RCV001/before_active_package.json` |
| Pre-recovery package backup | `knowledge/evidence/releases/RCV001/pre_recovery_package_backup.json` |
| Pre-recovery foundation backup | `knowledge/evidence/releases/RCV001/pre_recovery_foundation_structure_backup.json` |
| Operational harness | `knowledge/engineering/rcv001_production_curriculum_recovery/rcv001_recover.py` |

---

## Before / After Comparison

| Field | Before | After attempt |
|---|---|---|
| Active package sections | 7 | **7** (unchanged) |
| Active package topics | 117 | **117** (unchanged) |
| Active package objectives | 0 | **0** (unchanged) |
| Certification block | absent | **absent** |
| `ei_generation_chains` | 0 | **0** |
| `ei_generation_snapshots` | 0 | **0** |
| `ei_educational_nodes` | 0 | **0** |
| `ei_certification_records` | 0 | **0** |
| Workspace `certified_snapshot_id` | NULL | **NULL** |
| `runtime_enrolments` | 0 | **0** |

Production catalogue was **not** mutated. Safe to retry after the persistence fix.

---

## Production Counts

### STEP 1 confirmed inventory

| Prerequisite | Status |
|---|---|
| Active CMP (`checksum 6cb786c59ea43960…`, `ready_for_embeddings`) | ✓ |
| Active Syllabus (`checksum adad4b0985279dfc…`, `ready_for_embeddings`) | ✓ |
| Local PDF bytes readable (identical checksum prefixes) | ✓ |
| Workspace `ws-cs1` | ✓ (`status=published`) |
| Foundation version | ✓ (`id=1`, label `2026.1`, `published`) |
| Active published package | ✓ (`id=1`, uncertified 7/117/0) |

### Target (not achieved)

| Metric | Local certified | Production now | Required |
|---|---:|---:|---|
| Sections | 5 | 7 | > 0 (prefer 5) |
| Topics | 15 | 117 | > 0 (prefer 15) |
| Objectives | 73 | 0 | > 0 (prefer 73) |

---

## Certification Evidence

**None persisted.** Gen 1 never completed a successful `append_snapshot` on production Postgres.

Local SQLite (where RR-001 previously succeeded) runs with foreign keys **disabled**:

```text
PRAGMA foreign_keys = 0
```

That masks the insert-order bug that Postgres enforces.

---

## Publication Evidence

**Not executed.** Publish was correctly gated behind successful certification. No legacy fallback was enabled.

---

## Begin Learning Evidence

**Not re-tested on a new package** (no new package). Pre-recovery derive failure condition remains: empty `structure.objectives`.

---

## Regression Results

Not executed (blocked at STEP 2). No Founder Console / Studio / Runtime surface changes were deployed. Application code under `app/` was **not** modified during this attempt.

---

## STOP — Missing / Defective Capability

### What failed

**Capability:** Persistent Educational Intelligence generation store on PostgreSQL  
**Class:** `SqlAlchemyGenerationStore.append_snapshot`  
**File:** `app/infrastructure/adapters/curriculum_intelligence/generation_store.py`

### Why it cannot complete safely today

1. Snapshot row is `session.add`’d.
2. Node rows are `session.add`’d referencing `snapshot_id`.
3. `_ensure_lineage_op` issues a **SELECT** (`.first()`), which triggers SQLAlchemy **autoflush**.
4. Autoflush INSERTs nodes **before** the snapshot INSERT is visible to Postgres FK checks.
5. Postgres raises `ForeignKeyViolation` on `ei_educational_nodes_snapshot_id_fkey`.
6. Session enters rollback-needed state; further pipeline work cannot proceed without `Session.rollback()`.

This is **not** a missing curriculum algorithm, validation gate, Runtime, Deriver, or publication rule. It is a **persistence ordering defect** that makes the existing EI pipeline non-operable against production Postgres while remaining operable against local SQLite (FKs off).

### Why continuation without a fix would be unsafe

- Retrying the same harness will fail again at Gen 1.
- Bypassing the store / writing SQL manually would violate RCV-001 constraints.
- Enabling `legacy_publish_fallback` would republish 0 objectives and keep Begin Learning broken.
- Weakening FK constraints on production is not an acceptable recovery path.

### Minimal application enhancement required (before re-running RCV-001)

**Do not redesign architecture.** Apply a small persistence-order fix in `SqlAlchemyGenerationStore.append_snapshot`:

1. After adding `EiGenerationSnapshot` (and chain/generation rows), call `db.session.flush()` **before** inserting educational nodes / lineage queries; **or**
2. Wrap the lineage existence query in `with db.session.no_autoflush:` so node INSERTs are not flushed before the snapshot row; **and**
3. Ensure STEP harnesses call `db.session.rollback()` after a failed probe so a subsequent syllabus-authoritative run starts clean.

Optional hardening (still small): enable SQLite `PRAGMA foreign_keys=ON` in tests so this class of bug cannot regress locally.

After that fix is deployed (or applied in the ops checkout used against production), re-run:

```bash
DATABASE_URL=<production postgres> \
APP_ENV=development \
PYTHONPATH=. python knowledge/engineering/rcv001_production_curriculum_recovery/rcv001_recover.py
```

Expected then: STEP 2–7 complete to certified package with non-empty objectives (local parity target **5 / 15 / 73**).

---

## Final Verdict

**RECOVERY BLOCKED at STEP 2.**

| Criterion | Status |
|---|---|
| No architectural redesign | Met |
| No validation bypass | Met |
| No manual SQL fixes | Met |
| No data fabrication | Met |
| Use existing production services only | Attempted — store cannot persist on Postgres |
| Production functionally equivalent to local certified curriculum | **Not met** |
| Begin Learning succeeds on production | **Not met** |

Production is still safe (no partial EI residue; package unchanged). Recovery must pause until the minimal `SqlAlchemyGenerationStore` PostgreSQL flush/ordering fix is applied, then RCV-001 STEPs 2–7 can be resumed.
