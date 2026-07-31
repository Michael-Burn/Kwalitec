# RCV002_COMPLETION_REPORT.md

**Programme:** RCV-002 — Resume Production Curriculum Recovery  
**Date:** 2026-07-30  
**Prerequisite:** PGFIX-001 (PostgreSQL persistence ordering + lineage preload)  
**Prior stop:** RCV-001 STEP 2 (FK failure)  
**Evidence:** `knowledge/evidence/releases/RCV002/`  
**Harness:**  
- `knowledge/engineering/rcv002_production_curriculum_recovery/rcv002_recover.py`  
- `knowledge/engineering/rcv002_production_curriculum_recovery/rcv002_resume.py`  
**Production target:** Render Postgres `kwalitec-db` (`dpg-d97bmbm8bjmc73c497e0-a`)  
**Workspace / subject:** `ws-cs1` / `CS1` / foundation version **id=1** label `2026.1`

---

## Executive Summary

Production CS1 is now functionally equivalent to the verified local certified curriculum.

| Gate | Result |
|---|---|
| Educational Intelligence G1–G7 | **PASS** — `CERTIFIED_WITH_WARNINGS` |
| Founder Calibration (RR-001 styles) | **PASS** — gens 3–7 re-certified |
| Certified publication | **PASS** — `authority=certified_snapshot` |
| Active package counts | **5 / 15 / 73** (exact local parity) |
| Begin Learning (derive + enrol + mission) | **PASS** |
| Architectural / validation / SQL bypasses | **None** |

**Final Verdict:** `RECOVERY COMPLETE`

---

## Recovery Timeline

| Time (UTC) | Event |
|---|---|
| 11:21 | Pre-flight baseline recorded (`preflight_baseline.json`) — package 7/117/0, EI empty |
| 11:24–11:52 | First attempt stalled on remote lineage SELECTs (~200ms RTT × hundreds of nodes) |
| ~11:53 | Attempt stopped; lineage op preload added to `SqlAlchemyGenerationStore.append_snapshot` (persistence efficiency only) |
| 11:55–12:03 | STEP 1 completed in **439s** — G1–7 accepted, 7 snapshots, 2204 nodes, `CERTIFIED_WITH_WARNINGS` |
| 12:03–12:09 | First calibration attempt failed mid-flight (Postgres SSL drop); STEP 1 data preserved |
| 12:11–12:29 | Resume harness: calibration succeeded (gens 3–7, **1046s**), then publish + Begin Learning |
| 12:31 | **RECOVERY COMPLETE** (`exit=0`) |

---

## Actions Performed

### Pre-flight (read-only)

Confirmed production `DATABASE_URL` host `dpg-d97bmbm8bjmc73c497e0-a.oregon-postgres.render.com`, database `kwalitec`, workspace `ws-cs1`, foundation version 1, active package id=1 uncertified 7/117/0, EI tables empty, `runtime_enrolments=0`, PGFIX flush present, local checksum-identical syllabus PDF readable.

### STEP 1 — Educational Intelligence pipeline

`WorkspaceGenerationService.run_initial_pipeline("ws-cs1", source_documents=(syllabus,), …)`

- Accepted indices: **[1, 2, 3, 4, 5, 6, 7]**  
- Certification: **CERTIFIED_WITH_WARNINGS**  
- Snapshot: `snap-d81dc82a5b4ddb8a` (pre-calibration)  
- Metrics already showed chapters=5, topics=15, objectives=73  

### STEP 2 — Founder Calibration (RR-001)

`FounderCalibrationService.apply` balanced seed → STRICT_SYLLABUS / CONSOLIDATED / EXAM_FOCUSED  

- Generations re-run: **[3, 4, 5, 6, 7]**  
- Post-cal certification: **CERTIFIED_WITH_WARNINGS**  
- Active certified snapshot: `snap-b8a3d3ea939763d5`  

### STEP 3 — Artefact verification

Chains, snapshots (≥7), educational nodes, certification records, workspace `certified_snapshot_id` + `active_chain_id` + status — **all populated**.

### STEP 4 — Publish

`PublicationBridgeService.publish_to_catalogue("ws-cs1", actor_id="rcv002")`  
No legacy fallback. No manual SQL. No publication code changes.

### STEP 5 — Package verify

Active package: **5 sections · 15 topics · 73 objectives**, `source=certified_snapshot`, certification present.

### STEP 6 — Begin Learning

- `PublishedCurriculumAuthority.get_active("CS1")` → certified package  
- `EducationalArtefactDeriver.derive` → success  
- `EducationalRuntimeEngineService.enrol_student` → success (user_id=5)  
- `generate_daily_mission` → success (`msn_fc1413d58f8441a8b258e07549a44695`)  

### STEP 7 — Regression surfaces

Certified preview loaded; Curriculum Observatory report OK; certified mission/progress/tutor surface imports OK.

---

## Evidence

| Artefact | Path |
|---|---|
| Pre-flight baseline | `knowledge/evidence/releases/RCV002/preflight_baseline.json` |
| Package backup | `knowledge/evidence/releases/RCV002/pre_recovery_package_backup.json` |
| STEP 1 pipeline | `knowledge/evidence/releases/RCV002/step1_syllabus_pipeline.json` |
| STEP 2 calibration | `knowledge/evidence/releases/RCV002/step2_calibration_resume.json` |
| STEP 3 inventory | `knowledge/evidence/releases/RCV002/step3_certification_inventory.json` |
| STEP 4 publication | `knowledge/evidence/releases/RCV002/step4_publication.json` |
| STEP 5/6/7 | `after_active_package.json`, `step6_begin_learning.json`, `step7_regression.json` |
| Before/after | `knowledge/evidence/releases/RCV002/before_after_comparison.json` |
| Decision | `knowledge/evidence/releases/RCV002/final_decision.json` |

---

## Certification Evidence

| Field | Value |
|---|---|
| Chain | `ei-chain-ws-cs1` |
| Final certified snapshot | `snap-b8a3d3ea939763d5` |
| Status | `CERTIFIED_WITH_WARNINGS` |
| Workspace `active_chain_id` | `ei-chain-ws-cs1` |
| Certification records | 2 (initial + post-calibration) |
| Generations / snapshots / nodes (final) | 12 / 12 / 3762 |

---

## Publication Evidence

| Field | Value |
|---|---|
| Package id | 1 (upserted in place) |
| `published_by` | `rcv002` |
| Version label | `2026.1` |
| Foundation version id | **1** (unchanged PK) |
| Structure source | `certified_snapshot` |
| Certification authority | `certified_snapshot` |
| Counts | **5 / 15 / 73** |

---

## Begin Learning Evidence

| Check | Result |
|---|---|
| Authority loads certified CS1 package | ✓ |
| Deriver | ✓ |
| Student enrolment | ✓ (`enrolment_user_id=5`) |
| Daily mission generation | ✓ topic “4.2 Understand and use generalised linear models” |

---

## Before / After Comparison

| Metric | Before | After |
|---|---:|---:|
| Generation chains | 0* | 1 |
| Generation snapshots | 0 | 12 |
| Educational nodes | 0 | 3762 |
| Certification records | 0 | 2 |
| Package sections | 7 | **5** |
| Package topics | 117 | **15** |
| Package objectives | **0** | **73** |
| Package certification | absent | `certified_snapshot` / `CERTIFIED_WITH_WARNINGS` |
| Foundation structure | 7 / 117 / 0 | 5 / 15 / 73 (`certified_snapshot`) |
| Runtime enrolments | 0 | ≥1 (smoke enrolment) |

\*Pre-flight baseline. A failed early attempt briefly left an empty chain row; STEP 1 reused `ei-chain-ws-cs1`.

Local parity target **5 / 15 / 73**: **met**.

---

## Regression Results

| Surface | Result |
|---|---|
| Certified snapshot preview | PASS |
| Curriculum Observatory | PASS |
| Student certified mission/progress/tutor imports | PASS |
| Publication dual-read (`source=certified_snapshot`) | PASS |
| Begin Learning path | PASS |
| No Runtime / Deriver / Publication code changes for recovery logic | PASS |
| No validation bypass / legacy publish fallback | PASS |
| No manual SQL data writes | PASS |

**Note:** Long remote Postgres latency required a small persistence efficiency change (lineage op id preload in `append_snapshot`) so G1–7 could finish in ~7 minutes instead of stalling for 30+ minutes on per-node SELECTs. FK flush from PGFIX-001 retained. No architecture redesign.

---

## Final Verdict

**RECOVERY COMPLETE.**

Production CS1 now matches the verified local certified curriculum:

- EI pipeline complete and certified  
- Calibration re-certified under RR-001 styles  
- Active published package **5 / 15 / 73** with `certified_snapshot` authority  
- Begin Learning derive + enrolment + mission succeed  

Ready for founder smoke on `https://kwalitec.onrender.com` (Begin Learning UI).
