# MIG-002 — Updated Migration Graph

**Repair date:** 2026-07-27  
**Prior forensic map:** `knowledge/product/mig001/MIGRATION_GRAPH.md`  
**Tooling:** `flask db heads`, `flask db history`, `flask db branches`, `alembic.script.ScriptDirectory`

---

## Heads (after repair)

```text
202607260001 (head)   # EP-008.3A recommendation_commitments
```

Exactly **one** head. `ScriptDirectory.get_current_head()` returns `202607260001`.

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
                                    └─ 202611120001  create_twin_snapshots   ★ historical BRANCHPOINT
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
                                       │                       └─ 202607240001  prd001_analytics_event_infrastructure
                                       │                          └─ 202607260001  create_recommendation_commitments  ★ HEAD
```

`flask db branches` confirms `202611120001` children are only `202607130001` and `202607190001` (commitments no longer forks from the branchpoint).

---

## Tip chain (linear)

```text
202607190002 (mergepoint)
  → 202607230001
    → 202607230002
      → 202607240001
        → 202607260001 (head)
```

---

## Diff vs MIG-001 observed graph

| Item | MIG-001 | MIG-002 |
|---|---|---|
| Heads | `202607240001`, `202607260001` | `202607260001` only |
| Parent of `202607260001` | `202611120001` | `202607240001` |
| Analytics tip | Parallel head | Intermediate revision on main line |
| New revisions | — | None |
| Schema SQL in commitments migration | — | Unchanged |

---

## Classification (post-repair)

| Revision | Role |
|---|---|
| `202611120001` | Historical branchpoint (welcome + V2 paths); **not** parent of commitments |
| `202607190002` | Historical mergepoint |
| `202607240001` | Analytics infrastructure; parent of commitments |
| `202607260001` | Unique production head |

---

## Secondary / Education OS migrations

Unchanged and still orthogonal: `src/infrastructure/persistence/migrations/versions/` is not part of the Flask `migrations/` script directory inspected by `flask db heads`.

---

## Remaining documentation / CI drift

Operational pins still name `202607230002` as the expected unique head (helpers, CI assert, alpha checklist). The **graph itself** is repaired; contract documents and test constants need a follow-up update to `202607260001`.
