# Architecture Stabilisation — Failure Classification (Phase 1)

Source: `pytest` via `.venv/bin/python` — **44 failed**, 43641 passed, 7 skipped.

| # | Test | Category | Root cause (preliminary) |
|---|------|----------|--------------------------|
| 1 | `curriculum_studio/test_independence::test_application_no_forbidden_imports` | 3 Architecture | `document_upload_service` imports `app.extensions` / `app.models` |
| 2 | `curriculum_studio/test_independence::test_package_lazy_exports` | 3 Architecture | `PORT_NAMES` includes document ports; package exports drift |
| 3 | `curriculum_studio/test_port_interaction::test_health_port_availability_matrix[7]` | 3 Architecture | Health expects ready with 3 ports; document ports missing → degraded |
| 4–5 | `curriculum_studio/test_ports_edge::test_port_names[document_*]` | 3 Architecture | Document ports listed in `PORT_NAMES` but not studio facade ports |
| 6–7 | `curriculum_studio/test_services::test_health_*` | 3 Architecture | Same health/`PORT_NAMES` mismatch |
| 8 | `student_experience/test_independence::test_application_no_forbidden_imports` | 3 Architecture | Commitment/explanation/readiness import extensions/models/services/infra |
| 9 | `infrastructure/test_independence::test_application_does_not_import_infrastructure` | 3 Architecture | 9 application→infrastructure import sites |
| 10 | `authority::test_adapters_do_not_import_flask_into_application_ports` | 3 Architecture | Same application→infrastructure sites |
| 11 | `adaptive_engine::test_digital_twin_does_not_import_experience_for_t4` | 3 Architecture | `shadow_rollback.py` imports student_experience composition |
| 12–13 | `education_os/.../test_no_educational_intelligence_methods[…prioritise]` | 3 Architecture | Mission generation uses forbidden method name `prioritise` |
| 14 | `education_os/.../test_route_handlers_stay_thin[reflection]` | 3 Architecture | `submit_reflection` is 50 lines (max 45) |
| 15–20 | EOS page/token snapshot regressions (6) | 2 Snapshot | Token CSS / `color-scheme` meta drift vs golden files |
| 21–24 | Recommendation dual-run / simulation / recovery unchanged (4) | 9 App bug | `generated_at` differs across calls (non-deterministic compare) |
| 25–28 | EIP/IA mission explainability (Learning Mode / Estimated Knowledge) | 4 Template | Mission page missing student-facing explainability copy |
| 29 | EIP-003 engineering terms on settings | 4 Template | `digital twin` wording on student settings |
| 30–35 | Brand layout wiring (brand.css, Inter, meta, footer, versioned static, logo) | 5 Branding | Layouts are routers/extends; brand includes missing from scanned files; PIL missing for logo test |
| 36 | Alpha assets fonts.css reference | 5 Branding | Student layout router does not reference fonts.css |
| 37 | Sign-out order after share feedback | 5 Branding | Sidebar chrome order regression |
| 38 | Alembic head constant stale | 7 Config | Test expects `202607260001`; head is `202607270013` |
| 39–40 | Sole runtime `/` → `/student` | 7 Config / 9 Bug | Redirects to `/dashboard/` under sole runtime |
| 41 | Workflow primary action `upload` | 8 Outdated / 9 Bug | `upload` not in allowed primary keys set |
| 42 | Custom 500 page text | 4 Template | Page says "Something Went Wrong" not "Internal Server Error" |
| 43 | Login honest analytics feature copy | 4 Template | Login missing `LOGIN_ANALYTICS_FEATURE` copy |
| 44 | Founder overview "Operational pulse" | 4 Template | Header shortened away expected phrase |
| 45 | CSS budget 70362 ≥ 70000 | 6 Performance | First-party CSS 362 bytes over budget |

Categories: 1 Missing dependency · 2 Snapshot · 3 Architecture · 4 Template · 5 Branding · 6 Performance · 7 Configuration · 8 Test expectation outdated · 9 Genuine application bug
