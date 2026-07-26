# RC-002 — Failure Classification Matrix

**Programme:** RC-002 — Final Release Failure Classification  
**Date:** 2026-07-27  
**Mode:** Investigation only  

**Suite evidence:**

```text
.venv/bin/pytest tests/ -q --tb=no
# Stable residual set: 31 failed (MIG-003: 31 failed, 43325 passed, 7 skipped)
# This session full run: 32 failed once (intermittent
#   presentation/student/test_recommendation_commitment_contract.py::
#   test_cf_a06_reflection_binds_authored_humble_frames passed on --lf reconfirm)
.venv/bin/pytest --lf -q --tb=short
# → 31 failed, 1 passed
```

**Alembic:** single head `202607260001` (not among failures).

Every residual failure is placed in **exactly one** category.

---

## Summary counts

| Category | Count |
|----------|------:|
| A — Critical Release Blocker | 0 |
| B — High Priority Quality Issue | 4 |
| C — Technical Debt | 8 |
| D — Outdated Test | 19 |
| **Total** | **31** |

---

## Full matrix

| ID | Test | Purpose | Expected | Actual | Root cause | Cat | Deploy impact | Recommendation |
|----|------|---------|----------|--------|------------|:---:|---------------|----------------|
| A— | *(none)* | — | — | — | — | A | — | — |
| B1 | `test_eip003…::test_mission_page_explains_itself` | EIP-003 mission explainability | Contains `Learning Mode`, `Current Learning Topic`, Observed Facts, Estimates | Schema path omits Learning Mode / Current Learning Topic; keeps Why / Observed Facts / Estimates | EP-003.3 schema narration replaced legacy EIP vocabulary | **B** | Indirect (legacy `/missions/`; Stage 1 uses sole-runtime `/student`) | Restore vocabulary or update EIP-003 + cover `/student` |
| B2 | `test_eip003…::test_dashboard_and_mission_share_learning_mode_story` | Coherent Learning Mode story | Learning Mode on mission | Same omission | Same as B1 | **B** | Indirect | Same as B1 |
| B3 | `test_eip006…::test_mission_page_explains_estimated_knowledge` | EIP-006 EK labelling | `Estimated Knowledge` in body | Schema path lacks literal EK label | Schema narration omits V1 label | **B** | Indirect | Add EK label or retarget tests |
| B4 | `test_ia004…::test_mission_page_explains_learning_mode` | IA-004 terminology | Learning Mode / Current Learning Topic | Same as B1 | Same as B1 | **B** | Indirect | Same as B1 |
| C1 | `student_experience/test_independence.py::test_application_no_forbidden_imports` | Hexagonal purity | No forbidden imports | 11 offenders (commitment + explainability → models/services/infra) | EP-008.3 wiring | **C** | None | Ports + adapters |
| C2 | `eos…test_architecture_purity…[reflection/routes.py]` | Thin handlers ≤45 lines | ≤45 | `submit_reflection` = 50 | Experience context in route | **C** | None (EOS) | Extract helper |
| C3 | `eos…test_no_educational_intelligence_methods[adaptive_mission_generator.py]` | Forbid EI method names | No `prioritise` | Defines `prioritise` (ordering) | Name collision | **C** | None | Rename / allowlist |
| C4 | `…[ordering_rules.py]` | Same | No `prioritise` | Defines `prioritise` | Same | **C** | None | Same |
| C5 | `test_digital_twin_does_not_import_experience_for_t4` | T4 twin boundary | No experience import in twin | `shadow_rollback.py` imports composition | Rollback drill | **C** | None | Inject factory |
| C6 | `authority…::test_adapters_do_not_import_flask_into_application_ports` | App↛infra | No infra imports | 6 files (analytics + feedback) | Emit hooks in app layer | **C** | None | Publisher port |
| C7 | `infrastructure/test_independence.py::test_application_does_not_import_infrastructure` | Same boundary | No infra imports | Same 6 paths | Same | **C** | None | Same |
| C8 | `test_v1sp003…::test_first_party_css_js_under_budget` | CSS &lt; 70 KB | &lt; 70000 | 70362 | PX/RC CSS growth | **C** | Negligible | Trim or raise budget |
| D1 | `test_snapshot_token_style_tag` | Token CSS snapshot | Old snapshot | + motion tokens | PX-004 tokens | **D** | None | Regenerate snapshot |
| D2 | `test_page_regression_snapshots[/eos/login/…]` | EOS HTML lock | Old HTML | PX-004 shell (200 OK) | Intentional polish | **D** | None (`/eos/` not Stage 1) | Regenerate |
| D3 | `…[/eos/dashboard/…]` | Same | Old | New | Same | **D** | None | Regenerate |
| D4 | `…[/eos/mission/…]` | Same | Old | New | Same | **D** | None | Regenerate |
| D5 | `…[/eos/session/…]` | Same | Old | New | Same | **D** | None | Regenerate |
| D6 | `…[/eos/reflection/…]` | Same | Old | New | Same | **D** | None | Regenerate |
| D7 | `test_generate_recommendations_unchanged_when_dual_run_on` | Dual-run purity | Equal lists | `generated_at` only | Timestamp stamp | **D** | None | Exclude volatile fields |
| D8 | `test_recommendation_output_unchanged_with_simulation` | Simulation purity | Equal lists | `generated_at` only | Same | **D** | None | Same |
| D9 | `test_recommendation_output_unchanged_with_recovery_injection` | Recovery purity | Equal lists | `generated_at` only | Same | **D** | None | Same |
| D10 | `test_recommendation_unchanged_when_context_supplied` | Recovery + context | Equal lists | `generated_at` only | Same | **D** | None | Same |
| D11 | `test_student_templates_forbid_engineering_terms` | No eng terms | Clean scan | Jinja comment “Digital Twin” | B10 comment; label OK | **D** | None | Strip Jinja comments |
| D12 | `test_login_does_not_overclaim_exam_readiness_analytics` | Honest login | PTP constant present | PX-001 bullets; no overclaim | PX-001 redesign | **D** | None | Update assert |
| D13 | `test_custom_500_page_in_production_mode` | Custom 500 | `Internal Server Error` | `Something Went Wrong` | Student-safe copy | **D** | None | Update assert |
| D14 | `test_creates_admin_when_no_users_exist` | create-admin CLI | Old success string | Founder RBAC string | Intentional message | **D** | Ops only | Update assert |
| D15 | `test_empty_database_applies_migrations_and_creates_admin` | Startup migrate+admin | Log `Admin created.` | `Admin created with Founder RBAC.` | Intentional log | **D** | None (startup works) | Update assert |
| D16 | `test_overview_and_vision_headers_shortened` | Founder IA | `Operational pulse` | New executive summary | Console redesign | **D** | Founder only | Update assert |
| D17 | `test_templates_reference_css` | CSS referenced | String in leaf templates | Loaded via base layout | Inheritance | **D** | None | Assert base/rendered |
| D18 | `test_sign_out_follows_share_feedback` | Sidebar order | Feedback before Sign out | Sole-runtime omits Feedback | EP-007.1 nav | **D** | None | Branch on layout |
| D19 | `test_approved_logo_is_single_display_source` | Logo uniqueness + RGBA | PIL opens logo | `No module named 'PIL'` | Pillow not in deps | **D** | None (asset OK) | Add Pillow or replace check |

---

## Cross-references

| Document | Contents |
|----------|----------|
| `RELEASE_BLOCKERS.md` | Category A detail (empty) |
| `QUALITY_ISSUES.md` | Category B detail |
| `TECHNICAL_DEBT.md` | Category C detail |
| `OUTDATED_TESTS.md` | Category D detail |
| `FINAL_RELEASE_DECISION.md` | Deploy decision |
| `EXECUTIVE_SUMMARY.md` | Founder one-pager |

---

## Intermittent note (not in the 31)

`tests/presentation/student/test_recommendation_commitment_contract.py::test_cf_a06_reflection_binds_authored_humble_frames` failed once in a full-suite run and **passed** on `--lf`. Not classified as a residual failure; treat as flaky if it reappears — re-investigate before elevating to A/B.
