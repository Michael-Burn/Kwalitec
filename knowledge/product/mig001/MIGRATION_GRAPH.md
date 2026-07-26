# MIG-001 — Migration Graph

**Investigation date:** 2026-07-27  
**Repo HEAD at investigation:** `65cb380` (Release Candidate 1)  
**Tooling:** `flask db heads`, `flask db history`, `flask db branches`, `alembic.script.ScriptDirectory`

---

## Observed heads

```text
202607240001 (head)   # PRD-001 analytics event infrastructure
202607260001 (head)   # EP-008.3A recommendation_commitments
```

Evidence: `flask db heads` and `ScriptDirectory.get_heads()` both return exactly these two revisions. `get_current_head()` raises `CommandError: multiple heads`.

---

## Exact tree (Flask Alembic script directory)

Root: `202607080001` (`create_user_model`).

```text
<base>
└─ 202607080001  create_user_model
   └─ 202607080002  create_mission_models
      └─ 202607080003  create_study_plan_models
         └─ 202607080004  create_curriculum_learning_models
            └─ 202607080005  add_adaptive_learning_fields
               └─ 0a272936a47b  add_decision_model
                  └─ 202609070001  add_preferred_session_minutes
                     └─ 202609070002  add_curriculum_version_to_study_plans
                        └─ 202609070003  add_curriculum_topic_code_to_study_plans
                           └─ 202609070004  add_archived_to_study_plans
                              └─ 202610070001  create_sections_table
                                 └─ 202610070002  add_topic_section_relationship
                                    └─ 202611120001  create_twin_snapshots   ★ BRANCHPOINT
                                       ├─ 202607130001  add_user_welcome_flags
                                       │  └─ 202607130002  widen_learning_objective_description
                                       │     └─ 202607150001  add_study_plan_id_to_missions
                                       │        └─ 202607160001  create_research_feedback_tables
                                       │           └─ 202607160002  create_contributor_recognition_tables
                                       │              └─ 202607160003  create_founder_research_command_centre
                                       │                 └─ 202607170001  add_revision_lifecycle_fields
                                       │                    └─ 202607170002  create_vision_journal_tables
                                       │                       └─ 202607170003  add_v1sp003_performance_indexes
                                       │                          ↘
                                       ├─ 202607190001  create_v2_aggregate_tables
                                       │                          ↘
                                       │              202607190002  merge_v2_aggregate_heads  (mergepoint)
                                       │                 └─ 202607230001  alpha_001_infrastructure
                                       │                    └─ 202607230002  pr001_rbac_identity
                                       │                       └─ 202607240001  prd001_analytics_event_infrastructure  ★ HEAD A
                                       │
                                       └─ 202607260001  create_recommendation_commitments  ★ HEAD B
```

`flask db branches` confirms `202611120001` is the branchpoint with three children: `202607130001`, `202607190001`, and `202607260001`.

---

## Classification

| Revision | Role | Evidence |
|---|---|---|
| `202607080001` | Root | `down_revision = None` |
| `202611120001` | Historical branchpoint (legitimate past fork) | Children include welcome-flags path and V2 aggregates path; later merged by `202607190002` |
| `202607190002` | Historical mergepoint | `down_revision = ("202607170003", "202607190001")` |
| `202607230002` | Prior single-head (CI still asserts this) | `.github/workflows/ci.yml` L177; `tests/operational/helpers.py` `ALEMBIC_HEAD` |
| `202607240001` | **Current main-chain tip (Head A)** | Parent = `202607230002`; no children |
| `202607260001` | **Parallel tip (Head B) — misparented** | Parent = `202611120001` (ancestor), not the current main tip |

---

## Orphans / dead branches

### Is `202607240001` an orphan?

**No.**

Definition used: a revision is orphaned only if it is unreachable from the intended production upgrade path, or disconnected from the root, or superseded with zero remaining dependents.

Evidence against orphanhood:

1. Parent is the previous production head `202607230002` (migration header + `down_revision`).
2. It is reachable from root via the post-merge main line (`… → 202607190002 → 202607230001 → 202607230002 → 202607240001`).
3. Local primary SQLite DB `instance/kwalitec.sqlite3` is stamped at `202607240001` and contains `analytics_events`, `analytics_outbox`, `analytics_audit_log`.
4. No later migration references it **because it is a head** — absence of children is normal for a tip, not proof of orphanhood.

### Is `202607260001` an orphan?

**No — but it is a dead/incorrect side branch relative to the production tip.**

Evidence:

1. It is connected to root via `202611120001`.
2. Its parent is an **ancestor already behind the merged main line**, not the current tip.
3. Applying it alone from a DB already at `202607240001` is impossible without a merge or reparent (Alembic will not walk “sideways” onto that branch).
4. Local primary DB at `202607240001` does **not** contain `recommendation_commitments` (table missing while stamp is analytics head).

### Dead branch verdict

The **problem branch** is `202611120001 → 202607260001`, not the analytics head. Dual heads exist because EP-008.3A revision was parented onto a historical branchpoint instead of `202607240001` (or at least `202607230002`).

---

## Secondary / Education OS migrations

A separate Alembic tree exists under `src/infrastructure/persistence/migrations/versions/` (`202607200001`, `202607200002`). It is **not** part of the Flask `migrations/` script directory that `flask db heads` inspects. Out of scope for this dual-head condition except to note it does not explain the two heads above.

---

## Stale single-head contract

CI and operational helpers still expect a **single** head of `202607230002`:

- `.github/workflows/ci.yml` — `assert head == "202607230002"`
- `tests/operational/helpers.py` — `ALEMBIC_HEAD = "202607230002"`
- `knowledge/version2/INTERNAL_ALPHA_CHECKLIST.md` — expect `202607230002`

That contract was already stale after analytics (`202607240001`) landed in commit `0cf8541` (2026-07-24), before the recommendation-commitments head appeared. Dual heads make `get_current_head()` fail entirely.
