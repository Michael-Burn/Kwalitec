# RC-002 — Outdated Tests (Category D)

**Programme:** RC-002  
**Date:** 2026-07-27  
**Count:** **19**

---

## Definition (charter)

Implementation is correct; expectation is stale (snapshot drift, renamed UI, updated wording, intentional redesign, test harness gap). **No application change required** — only test maintenance.

---

## Snapshots / Design System (6)

### D1 — Token style tag snapshot

| Field | Evidence |
|-------|----------|
| **Test** | `tests/education_os/adapters/flask/rendering/test_regression_snapshots.py::test_snapshot_token_style_tag` |
| **Purpose** | Lock DS token CSS markers |
| **Expected** | Snapshot without newer PX motion tokens |
| **Actual** | Adds `--transition-page` / `--transition-sidebar` / `--transition-tooltip` |
| **Root cause** | Intentional PX-004 motion tokens; snapshot not refreshed |
| **Category** | **D** |
| **Deployment impact** | None (EOS test surface) |
| **Recommendation** | Regenerate `token_style_tag_markers.html` |
| **Evidence** | Snapshot drift assertion message |

### D2–D6 — EOS page regression snapshots (×5)

| Field | Evidence |
|-------|----------|
| **Tests** | `tests/education_os/adapters/flask/test_page_snapshots.py::test_page_regression_snapshots` for `/eos/login/`, `/eos/dashboard/`, `/eos/mission/`, `/eos/session/`, `/eos/reflection/` |
| **Purpose** | Full HTML locks for Education OS pages |
| **Expected** | Pre–PX-004 HTML |
| **Actual** | `color-scheme`, Inter/shell polish, expanded CSS/JS; HTTP **200** |
| **Root cause** | Intentional PX-003/004 EOS polish |
| **Category** | **D** |
| **Deployment impact** | None — `/eos/` not registered on production Flask Stage 1 path |
| **Recommendation** | Bulk regenerate `tests/education_os/adapters/flask/snapshots/pages/*` after visual review |
| **Evidence** | Diff shows `+ <meta name="color-scheme" content="light dark">` and CSS churn |

---

## Recommendation equality (timestamps) (4)

### D7 — Dual-run unchanged recommendations

| Field | Evidence |
|-------|----------|
| **Test** | `tests/infrastructure/adapters/consumer_chain/test_study_insights_dual_run.py::test_generate_recommendations_unchanged_when_dual_run_on` |
| **Purpose** | Dual-run must not mutate recommendation payload |
| **Expected** | `again == baseline` |
| **Actual** | Only `generated_at` differs (~2 ms) |
| **Root cause** | Each call stamps `datetime.utcnow().isoformat()`; dual-run is diagnostic-only |
| **Category** | **D** |
| **Deployment impact** | None |
| **Recommendation** | Compare excluding `generated_at` or freeze clock |
| **Evidence** | Field-level diff of `generated_at` only |

### D8 — Decision simulation unchanged

| Field | Evidence |
|-------|----------|
| **Test** | `tests/services/test_decision_simulation.py::test_recommendation_output_unchanged_with_simulation` |
| **Purpose** | Simulation must not alter returned recommendations |
| **Expected** | `without == with_sim` |
| **Actual** | `generated_at` only |
| **Root cause** | Same timestamp stamp |
| **Category** | **D** |
| **Recommendation** | Semantic equality helper |
| **Evidence** | Diff of `generated_at` only |

### D9–D10 — Recovery injection unchanged (×2)

| Field | Evidence |
|-------|----------|
| **Tests** | `test_recommendation_output_unchanged_with_recovery_injection`, `test_recommendation_unchanged_when_context_supplied` |
| **Purpose** | Recovery injection must not change ranking |
| **Expected** | Full list equality |
| **Actual** | `generated_at` only; recovery remains ignored for decisions |
| **Category** | **D** |
| **Recommendation** | Same as D7 |
| **Evidence** | Diff of `generated_at` only |

---

## Copy / messaging / brand harness (9)

### D11 — Engineering term scan (Jinja comment)

| Field | Evidence |
|-------|----------|
| **Test** | `tests/test_eip003_educational_explainability.py::TestNegativeEngineeringTerminology::test_student_templates_forbid_engineering_terms` |
| **Purpose** | Forbid engineering terms on student pages |
| **Expected** | No `digital twin` in scanned template text |
| **Actual** | Hit in `{# … Digital Twin … #}` comment in `settings/index.html` |
| **Root cause** | RC-001 B10 rename documented in Jinja comment; rendered label is `Personalised recommendations`. Scan strips HTML comments only |
| **Category** | **D** |
| **Deployment impact** | Students never see the comment |
| **Recommendation** | Strip Jinja comments in scanner, or reword comment without forbidden tokens |
| **Evidence** | `app/templates/settings/index.html: digital twin` |

### D12 — Login PTP analytics constant

| Field | Evidence |
|-------|----------|
| **Test** | `tests/test_ptp003_honest_product_communication.py::…::test_login_does_not_overclaim_exam_readiness_analytics` |
| **Purpose** | Login must not say “Exam Readiness Analytics”; should use PTP honest feature line |
| **Expected** | `Estimated readiness insights` or `pcs.LOGIN_ANALYTICS_FEATURE` present |
| **Actual** | PX-001 brand-led bullets (`Always know what to study next`, `Honest progress you can trust`, …); overclaim absent |
| **Root cause** | Intentional PX-001 login redesign |
| **Category** | **D** |
| **Recommendation** | Update assertion to PX-001 honest bullets |
| **Evidence** | Assert on `LOGIN_ANALYTICS_FEATURE` fails; `Exam Readiness Analytics` not present |

### D13 — Production 500 page title

| Field | Evidence |
|-------|----------|
| **Test** | `tests/test_routes.py::TestErrorHandling::test_custom_500_page_in_production_mode` |
| **Purpose** | Production 500 returns custom page |
| **Expected** | Body contains `Internal Server Error` |
| **Actual** | `Something Went Wrong` + retry/home CTAs (`app/templates/errors/500.html`) |
| **Root cause** | Intentional student-safe copy |
| **Category** | **D** |
| **Recommendation** | Assert on current title/description |
| **Evidence** | `assert b'Internal Server Error' in response.data` fails on 500 response |

### D14 — CLI create-admin message

| Field | Evidence |
|-------|----------|
| **Test** | `tests/test_cli.py::TestCreateAdminCommand::test_creates_admin_when_no_users_exist` |
| **Purpose** | `flask create-admin` creates first admin |
| **Expected** | `Administrator created successfully.` |
| **Actual** | `Administrator created successfully (Founder RBAC granted).` (`app/cli.py`) |
| **Root cause** | Founder RBAC messaging |
| **Category** | **D** |
| **Recommendation** | Update expected string |
| **Evidence** | Output mismatch |

### D15 — Startup admin log message

| Field | Evidence |
|-------|----------|
| **Test** | `tests/test_startup_service.py::TestStartupService::test_empty_database_applies_migrations_and_creates_admin` |
| **Purpose** | Empty DB: migrate + create admin |
| **Expected** | Log contains `Admin created.` |
| **Actual** | `Admin created with Founder RBAC.` — migrations still apply |
| **Root cause** | Founder RBAC log wording (`startup_service.py`) |
| **Category** | **D** |
| **Recommendation** | Update expected log token |
| **Evidence** | MIG-002/003 already noted; pytest assert on messages list |

### D16 — Founder overview header

| Field | Evidence |
|-------|----------|
| **Test** | `tests/test_v1sp001e_information_architecture.py::TestV1sp001eFounderSimplification::test_overview_and_vision_headers_shortened` |
| **Purpose** | Founder console short headers |
| **Expected** | Overview contains `Operational pulse` |
| **Actual** | Executive summary: `What needs attention today · …` |
| **Root cause** | Founder console redesign |
| **Category** | **D** |
| **Deployment impact** | Founder-only; not Stage 1 student path |
| **Recommendation** | Update expected header strings |
| **Evidence** | Assert `'Operational pulse' in overview` fails |

### D17 — Curriculum studio CSS reference scan

| Field | Evidence |
|-------|----------|
| **Test** | `tests/operational/test_alpha_assets.py::test_templates_reference_css` |
| **Purpose** | Templates reference `founder_dashboard.css` |
| **Expected** | String present in leaf curriculum_studio templates |
| **Actual** | CSS loaded via `layouts/console_base.html` inheritance |
| **Root cause** | Inheritance-based asset loading |
| **Category** | **D** |
| **Recommendation** | Assert on base layout or rendered HTML |
| **Evidence** | Assert `'founder_dashboard.css' in html` on child template fails |

### D18 — Sidebar Sign out / Share Feedback order

| Field | Evidence |
|-------|----------|
| **Test** | `tests/test_bi001_brand_identity.py::TestSidebarBrandChrome::test_sign_out_follows_share_feedback` |
| **Purpose** | Share Feedback appears before Sign out in sidebar source |
| **Expected** | Feedback index &lt; Sign out; regex adjacency |
| **Actual** | Under `SOLE_RUNTIME` block, Share Feedback is omitted; first `Sign out` precedes legacy Feedback block |
| **Root cause** | EP-007.1 canonical nav under sole runtime |
| **Category** | **D** |
| **Recommendation** | Branch assertions on sole-runtime vs legacy layout |
| **Evidence** | `assert 5227 < 3289` (index order inverted across dual layouts) |

### D19 — Approved logo PIL check

| Field | Evidence |
|-------|----------|
| **Test** | `tests/test_bi001_brand_identity.py::TestOfficialAssetPack::test_approved_logo_is_single_display_source` |
| **Purpose** | Single approved PNG; master/legacy bytes equal; RGBA lockup |
| **Expected** | `from PIL import Image` succeeds |
| **Actual** | `ModuleNotFoundError: No module named 'PIL'` — file existence and byte-equality checks pass before import |
| **Root cause** | Pillow not in `requirements.txt` / project deps |
| **Category** | **D** |
| **Deployment impact** | None — logo asset present and served |
| **Recommendation** | Add Pillow to test deps **or** replace with PNG chunk inspection |
| **Evidence** | ModuleNotFoundError at PIL import; asset paths exist |

---

## Maintenance batch suggestion

1. Refresh EOS snapshots (D1–D6).  
2. Semantic recommendation compare helper (D7–D10).  
3. One PR for string/scan/harness updates (D11–D19).
