# Production Begin Learning Investigation

**Date:** 2026-07-30  
**Scope:** Evidence-only — no application code changes, no republish, no DB writes  
**Host:** `https://kwalitec.onrender.com`  
**Subject:** `CS1`  
**Reported symptom:** Begin Learning surfaces  
`Published Curriculum must include sections, topics and objectives.`  
**Canonical exception text (code):**  
`published curriculum must include sections, topics, and objectives`  
**Local git HEAD at investigation:** `ee1101d9ef7c61201d7d1f0701223bdfdfb6fd7f`  
**Live deploy tip (Render):** `ee1101d9ef7c61201d7d1f0701223bdfdfb6fd7f` (`dep-d9lh677avr4c7394l0cg`, live)

---

## Verdict (executive)

Against the **production PostgreSQL** database bound to the live Render web service:

1. Runtime loads the expected active package: **`published_curriculum_packages.id = 1`** (`CS1` / `2026.1`).
2. That package’s `package_json.structure` has **sections=7**, **topics=117**, **`objectives=0`**.
3. Offline replay of `EducationalArtefactDeriver.derive(prod_package)` raises the exact canonical message.
4. Local SQLite’s active CS1 package is a **different publication** (certified RR-001 cutover: **5 / 15 / 73**) and is **not** what production serves.

**Root cause:** Production’s active CS1 published package has an empty `structure.objectives` list. Begin Learning fails at derive, not because Runtime pointed at the wrong DB/row, and not because migrations are missing.

---

## Evidence collected

### 1. `DATABASE_URL` currently used by production

| Item | Value |
|---|---|
| Web service | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| `APP_ENV` | `production` |
| Env source | Render service env-var `DATABASE_URL` (`fromDatabase: kwalitec-db` per `render.yaml`) |
| Internal URL (redacted) | `postgresql://kwalitec_user:***@dpg-d97bmbm8bjmc73c497e0-a/kwalitec` |
| External host (investigation connect) | `dpg-d97bmbm8bjmc73c497e0-a.oregon-postgres.render.com:5432` |
| Database name | `kwalitec` |
| Database user | `kwalitec_user` |
| Postgres instance | `kwalitec-db` (`dpg-d97bmbm8bjmc73c497e0-a`, Oregon, PostgreSQL 18.4) |
| Session identity | `current_database()=kwalitec`, `current_user=kwalitec_user` |
| Alembic head on prod | `202607300005` |

**Password values are intentionally omitted from this report.**

Confirmation: service `DATABASE_URL` internal connection string matches Render’s `kwalitec-db` internal connection string (same user, host id, database, password). Deployment is **not** pointed at the other workspace DB (`personal_books_library`).

---

### 2. Published Curriculum Package loaded for CS1

Runtime selection (unchanged from code):

```python
PublishedCurriculumPackage.query.filter_by(
    subject_code="CS1", is_active=True
).order_by(PublishedCurriculumPackage.published_at.desc()).first()
```

Production row:

| Field | Production value |
|---|---|
| Package ID | **1** |
| `subject_code` | `CS1` |
| Version label | `2026.1` |
| Foundation `version_id` (row) | **1** |
| `package_json.foundation_version_id` | **1** |
| `is_active` | `true` |
| Published timestamp | **2026-07-29T20:29:54.966711** |
| `published_by` | `1` |
| Package rows for any subject | **1** (only this CS1 row) |

**Certification status / authority**

| Source | Production value |
|---|---|
| `package_json.certification` | **Missing** (key absent; treated as empty) |
| Certification authority | **None / pre-EI package** |
| Certification status | **None** |
| Workspace `ws-cs1.certification_status` | `NULL` |
| Workspace `ws-cs1.certified_snapshot_id` | `NULL` |
| Workspace `ws-cs1.active_chain_id` | `NULL` |
| `ei_certification_records` / `ei_generation_snapshots` counts | **0 / 0** |

`PublishedCurriculumAuthority._runtime_accepts` **accepts** packages with an empty/missing certification block (pre-EI migration path). So Runtime **does** return this package to Begin Learning; it is not filtered out before derive.

---

### 3. `package_json.structure` list lengths

From production `published_curriculum_packages.id=1`:

| Path | Length |
|---|---:|
| `package_json.structure.sections` | **7** |
| `package_json.structure.topics` | **117** |
| `package_json.structure.objectives` | **0** |

Metadata mirrors the same emptiness:

| Metadata field | Value |
|---|---:|
| `section_count` | 7 |
| `topic_count` | 117 |
| `objective_count` | **0** |

Sample shapes:

- First section title: `CS1` (`section_id=ent-e7b8cfc129`)
- First topic title: `Associateship Qualification` (`topic_id=ent-4c950ed640`) — syllabus front-matter, not a numbered syllabus objective topic
- `objectives`: empty list `[]` (no nested objectives under topics either)

Same emptiness is present upstream of the package:

| Artefact | sections | topics | objectives |
|---|---:|---:|---:|
| `studio_foundation_versions.id=1` `parsed_structure_json` | 7 | 117 | **0** |
| `studio_workspace_projections` `ws-cs1` id-lists | 7 | 117 | **0** (`objective_ids`) |
| Published package structure | 7 | 117 | **0** |

This is consistent empty materialisation, not a one-off JSON corruption of the published row alone.

---

### 4. Production package vs local package

Local comparison DB (for contrast only; **not** the failure host):  
`sqlite:////Users/kwalitec/Developer/kwalitec/instance/kwalitec.sqlite3`  
Local active CS1 package id=1, `published_by=rr001`, `published_at=2026-07-29 22:21:01.531710`.

| Field | Production | Local |
|---|---|---|
| Package id | 1 | 1 |
| `version_label` | `2026.1` | `2026.1` |
| Foundation `version_id` | **1** | **5** |
| `foundation_version_id` in JSON | **1** | **5** |
| `published_by` | `1` | `rr001` |
| `published_at` | 2026-07-29 **20:29:54** | 2026-07-29 **22:21:01** |
| `certification` | **missing** | `authority=certified_snapshot`, `status=CERTIFIED_WITH_WARNINGS`, `snapshot_id=snap-ae1eaf5e82aabf58`, `chain_id=ei-chain-ws-cs1` |
| `ingestion_job_id` | `null` | `job-3b6bc53fbf32` |
| Documents | **4** (duplicate CMP×2 + Syllabus×2) | **2** (CMP + Syllabus) |
| `structure.sections` length | **7** | **5** |
| `structure.topics` length | **117** | **15** |
| `structure.objectives` length | **0** | **73** |
| `structure.section_count` | 7 | 5 |
| `structure.topic_count` | 117 | 15 |
| `structure.objective_count` | 0 | 73 |
| `structure.curriculum_authority` | missing | `certified_snapshot` |
| `structure.ei_*` certification fields | missing | present (`CERTIFIED_WITH_WARNINGS`, snap/chain ids) |
| `structure.source` | missing | `certified_snapshot` |
| Section id namespace | `ent-…` | `node-…` |
| Topic id namespace | `ent-…` | `node-…` |
| Section/topic titles | Parser/front-matter heavy (e.g. “Associateship Qualification”) | Certified syllabus chapters/topics (e.g. “1 Data analysis”) |
| Section/topic object keys | same key sets | same key sets |

**Every material difference** is that production still holds the **pre-certification Studio bridge publish** (foundation version 1, 7/117/0, no certification block), while local holds the later **RR-001 certified republish** (foundation version 5, 5/15/73).

Derive replay:

| Package | Result |
|---|---|
| Production active package | **FAIL** — `published curriculum must include sections, topics, and objectives` |
| Local active package | **OK** — `CS1:2026.1` with 5 / 15 / 73 |

---

### 5. Is Runtime loading the expected package?

**Yes — for production’s actual catalogue state.**

| Check | Result |
|---|---|
| Only active CS1 published row | id=1 |
| Authority accepts missing certification | Yes (`_runtime_accepts` returns True for empty/missing cert) |
| Enrol/derive consumes `package_json` structure lists | Yes |
| Wrong-database hypothesis | Rejected (service URL → `kwalitec-db`) |
| Stale local package hypothesis | Irrelevant to prod failure; local differs |

Call chain (unchanged):

```text
POST /study-plan/review
  → FounderStudentEnrolmentBridge.enrol
    → EducationalRuntimeEngineService.enrol_student
      → PublishedCurriculumAuthority.get_active("CS1")  → package id=1
      → EducationalArtefactDeriver.derive(package)
           raw_objectives == ()  → EducationalDerivationError
```

Gate in code:

```153:156:app/domain/educational_engine_foundation/derivation.py
        if not raw_sections or not raw_topics or not raw_objectives:
            raise EducationalDerivationError(
                "published curriculum must include sections, topics, and objectives"
            )
```

Production fails because **`raw_objectives` is empty**, even though sections and topics are non-empty.

---

### 6. Hypothesis determination

| Hypothesis | Verdict | Evidence |
|---|---|---|
| **A. Production package was never republished** (with certified dual-read / RR-001 cutover) | **Confirmed (primary)** | Single publish at 20:29:54 by `published_by=1` / “Studio publication bridge”; no certification block; foundation version still id=1 with 0 objectives; local RR-001 publish at 22:21 never applied to this DB; EI snapshot/cert tables are empty on prod |
| **B. Production package became corrupted** | **Rejected** | Empty objectives are consistent across workspace id-lists, foundation `parsed_structure_json`, and published `package_json`; not a truncated/garbled JSON decode |
| **C. Production database missed a migration** | **Rejected** | Alembic at `202607300005`; `published_curriculum_packages` exists and is readable; failure is payload content, not missing table/column |
| **D. Render deployment pointing at unexpected database** | **Rejected** | `DATABASE_URL` is `kwalitec-db` (`dpg-d97bmbm8bjmc73c497e0-a`), matching `render.yaml` |
| **E. Another root cause** | **Proximate mechanism only** | Deriver correctly rejects empty `objectives`; the environmental cause is A |

---

## Supporting production context

| Item | Value |
|---|---|
| Foundation subject | id=1, code `CS1`, title `CS1` |
| Foundation version | id=1, label `2026.1`, stage `publish`, `publication_state=published` |
| Version review notes | `Studio publication bridge` |
| Workspace | `ws-cs1`, status `published`, stage `publication` |
| Workspace facts | syllabus/CMP uploaded, validation/preview/publish flags true |
| EI generation / certification data | **Absent** (0 rows in EI chain/snapshot/cert tables) |

---

## Application / data mutations

**None.** No application code modified. No republish. No SQL writes. Investigation used read-only `SELECT` against production Postgres via the external connection string, plus offline derive against exported JSON.

---

## Exact root cause

Production Begin Learning for CS1 fails because the active published curriculum package (`published_curriculum_packages.id=1`, `CS1` / `2026.1`) materialised by the Studio publication bridge contains:

```text
structure.sections    length 7
structure.topics      length 117
structure.objectives  length 0
```

`EducationalArtefactDeriver.derive` requires all three lists to be non-empty, so enrolment raises:

`published curriculum must include sections, topics, and objectives`

That production package was **never replaced** by the certified RR-001-style republish that fixed local (5 sections / 15 topics / 73 objectives). Production also has **no** EI certified snapshot to dual-read from today.

---

## Minimum corrective action

**Do not implement in this investigation.**

Minimum fix (operations / Founder Console on production only):

1. On production for `ws-cs1` / CS1, produce a curriculum structure that includes a **non-empty flat `objectives` list** (the certified Curriculum Intelligence path used locally for RR-001 — production currently has zero EI snapshots/certs, so certification/generation must be completed on this DB first, or an equivalent certified structure must be prepared there).
2. **Then** publish to the student catalogue so `published_curriculum_packages` for active CS1 is updated.
3. Verify before student retry:

```text
len(structure.sections) > 0
len(structure.topics) > 0
len(structure.objectives) > 0
```

and that offline/derive (or Begin Learning) succeeds.

**Insufficient alone:** republishing the current foundation version 1 / current workspace structure without regenerating objectives — that would re-copy **0** objectives and the failure would persist.

**Not required for this failure:** application code change, Alembic migration, or changing `DATABASE_URL`.
