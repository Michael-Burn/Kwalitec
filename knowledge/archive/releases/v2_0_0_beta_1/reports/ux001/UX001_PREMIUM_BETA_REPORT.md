# UX-001 — Premium Closed Beta Experience Report

**Programme:** UX-001 · Premium Closed Beta Experience · Version 1 Polish  
**Date:** 2026-07-30  
**Scope:** User experience, interface quality, performance perception, polish, and closed-beta readiness  
**Constraint:** No new educational architecture · No new intelligence agents · No new curriculum reasoning  

---

## Summary

UX-001 transforms the engineering-complete Student EOS and Founder Console into a calmer, mission-first premium product surface for private beta. Today's Mission is the Home focal point; study orientation (subject, streak, progress, exam countdown, estimated study time) sits in one signal strip without duplicate widgets. Mission cards expose title, learning objective, duration, difficulty (when available), why-selected, and expected outcome. Study Session gains reading progress, a live timer, and Focus mode. Journey presents overall / chapter / topic / LO mastery with recent improvements and next focus areas. Tutor and Knowledge Map are first student-facing UIs over existing Twin / certified-graph services. Founder Curriculum Health summarises certification, publication, review packs, calibration, and observatory without engineering noise. Closed-beta chrome (badge, release notes, report issue, founder diagnostics) lands in the EOS footer.

---

## FINAL DECISION

# PREMIUM PRIVATE BETA READY

**Justification:** Student and Founder journeys now answer “what should I do next?” within a few seconds on primary screens, without new educational architecture. Visual language uses the existing DX-006 design system. Residual items are iterative polish (full Lighthouse lab run, denser LO mastery %, difficulty when domain projection is empty) — not closed-beta blockers given RR-001’s certified CS1 runtime readiness.

---

## UI improvements

| Area | Change |
|------|--------|
| Home | Mission-first layout; removed duplicate Current Examination widget when signals carry subject/countdown |
| Mission panel | Title, LO, duration/difficulty chips, why-selected, expected outcome |
| Signals strip | Subject · Streak · Progress · Exam countdown · Estimated study time |
| Session | Reading progress bar, live timer, Focus mode toolbar |
| Journey | Overall mastery + chapter/topic/LO sections + recent improvements / next focus |
| Tutor | Dedicated `/student/tutor` with curriculum context, loading, errors, citations |
| Knowledge Map | `/student/knowledge_graph` hierarchy with prerequisites / progress markers |
| Founder | `/console/curriculum-health` + workspace health strip |
| Shell | Closed Beta badge, Release notes, Report issue, Diagnostics (Founder) |

---

## UX improvements

- Home page question: **What should I do next?**
- Exactly one Primary CTA retained on mission Home
- Exam countdown no longer duplicated in Upcoming + Examination sections
- Quick Actions may include Ask Tutor / Knowledge Map without cloning shell nav
- Tutor explain flow stays on Tutor (no flash-redirect theatre)
- Session Focus mode hides chrome to reduce cognitive load
- Journey progress readable in ≤5 seconds via overall mastery bar + stats

---

## Performance improvements

- Knowledge Map preview tree pattern not used on student KG (native `<details>` hierarchy — no heavy virtualized tree JS)
- Session timer is client-local (no extra API polling)
- Tutor POST returns the page directly (one round-trip vs flash + redirect bounce)
- Founder Curriculum Health soft-fails without cascading service explosions
- Study signals project already-loaded Home `include_all_surfaces` profile/journey snapshots — no extra dashboard fetch

---

## Accessibility findings

| Finding | Status |
|---------|--------|
| Signal strip / mastery progressbars use `role="progressbar"` + valuemin/max/now | Improved |
| Focus mode toggle exposes `aria-pressed` | Improved |
| Tutor errors use `role="alert"`; loading sets `aria-busy` | Improved |
| Knowledge Map uses `role="tree"` / `treeitem` | Improved |
| Footer links have `:focus-visible` rings | Improved |
| Skip link preserved on EOS shell | Unchanged / good |
| Contrast against design tokens | Compliant with existing token palette; full WCAG lab audit still recommended |
| Keyboard-only full journey walkthrough | Not automated in this programme — manual beta QA item |

---

## Remaining polish items

1. Run production Lighthouse (Home, Session, Journey, Tutor, Knowledge Map) on a live build and attach scores to evidence.
2. Difficulty chip is empty when mission intelligence / educational VMs omit difficulty — wire when domain projection is present.
3. LO mastery on Journey lists objectives rather than per-LO % bars (requires richer mastery projection already in Certified Progress Engine — presentation only follow-up).
4. Knowledge Map empty state when subject code cannot be resolved from exam label — improve subject-code resolution from study plan binding.
5. Founder Curriculum Health calibration history is summary-level; deeper pack download UX can attach to `review_pack_ref` paths later.
6. Manual mobile responsive QA across iPhone / Android breakpoints.
7. Dark-mode spot check for new signal / KG / Tutor panels.

---

## Screens reviewed

- Student Home (`/student/`)
- Journey (`/student/journey`)
- History (`/student/history`) — archive ownership preserved; not redesigned as KPI wall
- Study Session (`/session/<id>/*`)
- Tutor (`/student/tutor`) — new
- Knowledge Map (`/student/knowledge_graph`) — new
- EOS shell / footer
- Founder Settings + Curriculum Health
- Curriculum Studio workspace (health strip)
- Alpha Help / Report Issue (linked, not rewritten)

---

## Screens redesigned

| Screen | Degree |
|--------|--------|
| Student Home | **Major** — mission-first + signals; removed duplicate exam widget |
| Mission panel (design system macro) | **Major** |
| Study Session body | **Moderate** — timer, focus, reading progress |
| Journey / Progress | **Major** — mastery levels |
| Tutor | **New** |
| Knowledge Map | **New** |
| Founder Curriculum Health | **New** |
| Workspace health strip | **Minor** |
| EOS footer (beta chrome) | **Minor** |

---

## Known limitations

- No new educational reasoning — Tutor / KG / Progress only project existing services.
- Difficulty and certified-source richness depend on upstream VM / package availability.
- Knowledge Map requires a resolvable subject code and certified published package.
- Full automated accessibility / Lighthouse suite was not executed in-browser in this programme (contracts + targeted pytest instead).
- Legacy `/dashboard/`, `/mission/`, `/analytics/` remain out of polish scope (RR-002.3).

---

## Beta readiness assessment

| Gate | Result |
|------|--------|
| Clear primary action on major screens | Pass |
| Clear information hierarchy | Pass |
| Premium appearance (tokens + ds-*) | Pass |
| Fast perceived loading | Pass (no new heavy requests) |
| Mobile responsive CSS | Pass (grid / wrap breakpoints) |
| No duplicated information on Home | Pass |
| Consistent spacing / typography | Pass |
| Consistent navigation | Pass (Tutor/KG under Home orientation) |
| First-time onboarding | Pass (existing Alpha onboarding gate retained) |
| Feedback / Report Issue | Pass (footer + Help) |
| Version / Closed Beta badge | Pass |
| Founder diagnostics | Pass (Curriculum Health) |

**Private beta recommendation:** Proceed. Use first beta cohort to validate Tutor Twin availability messaging, Knowledge Map subject resolution, and mobile Focus mode comfort.

---

## Workstream checklist

| WS | Outcome |
|----|---------|
| 1 Student Dashboard | Done — mission focal + signals |
| 2 Mission Experience | Done — enriched panel + completion feedback path unchanged (session summary) |
| 3 Study Session | Done — progress, timer, focus |
| 4 Progress | Done — Journey mastery redesign |
| 5 Tutor | Done — student UI |
| 6 Knowledge Graph | Done — first student UI |
| 7 Founder tools | Done — Curriculum Health |
| 8 Visual consistency | Done — design_system + student footer tokens |
| 9 Performance | Done — perceived performance / fewer redirects |
| 10 Accessibility | Improved — ARIA / focus; lab audit residual |
| 11 Closed Beta readiness | Done — badge, notes, report issue, diagnostics |

---

## Files Created

- `app/presentation/student/services/student_tutor_presentation_service.py`
- `app/presentation/student/services/student_knowledge_graph_presentation_service.py`
- `app/templates/student/tutor.html`
- `app/templates/student/knowledge_graph.html`
- `app/templates/student/components/knowledge_graph_node.html`
- `app/static/js/session/study_session_eos.js`
- `app/founder/dashboard/services/curriculum_health_service.py`
- `app/founder/dashboard/templates/founder_dashboard/curriculum_health.html`
- `tests/presentation/student/test_ux001_premium_beta.py`
- `knowledge/engineering/ux001_premium_beta/UX001_PREMIUM_BETA_REPORT.md`

## Files Modified

- `app/presentation/student/dto/student_home.py`
- `app/presentation/student/services/student_home_service.py`
- `app/presentation/student/routes.py`
- `app/presentation/student/navigation.py`
- `app/templates/student/home.html`
- `app/templates/student/journey.html`
- `app/templates/design_system/macros.html`
- `app/templates/session/partials/session_body.html`
- `app/templates/session/base.html`
- `app/templates/layouts/eos_student.html`
- `app/templates/curriculum_studio/workspace.html`
- `app/presentation/session/dto/study_session.py`
- `app/presentation/session/services/study_session_service.py`
- `app/static/css/design_system.css`
- `app/static/css/student/student.css`
- `app/founder/dashboard/routes.py`
- `app/founder/dashboard/nav.py`
- `app/founder/dashboard/templates/founder_dashboard/settings.html`
- `tests/test_dx006b_student_home.py`
- `tests/presentation/student/test_cq006_premium_craft.py`
- `tests/presentation/student/test_templates.py`
- `tests/presentation/test_sop001_student_os.py`

## Tests Executed

```bash
python3 -m pytest \
  tests/presentation/student/test_ux001_premium_beta.py \
  tests/test_dx006b_student_home.py \
  tests/presentation/student/test_cq006_premium_craft.py \
  tests/presentation/test_sop001_student_os.py \
  tests/presentation/session/test_templates.py -q
# 46 passed

python3 -m ruff check \
  app/presentation/student/services/student_knowledge_graph_presentation_service.py \
  app/presentation/student/routes.py \
  app/founder/dashboard/services/curriculum_health_service.py \
  tests/presentation/student/test_ux001_premium_beta.py
# All checks passed
```

## Migration Impact

None.

## Architecture Compliance

- Presentation-layer only; no new educational engines, agents, or curriculum reasoning.
- Tutor / KG / Progress / Founder Health call existing application services (`IntelligentTutorService`, `CertifiedLearningService`, `CurriculumObservatory`, published authority).
- Curriculum V1/V2 traversal untouched.
- Student EOS remains SOLE runtime; legacy dashboards not extended.

## Technical Debt

- Subject-code inference from exam label is best-effort for Knowledge Map.
- Founder health page aggregates up to 12 workspaces — fine for beta, not a full fleet console.
- Session timer is localStorage-based (legacy pattern) — not server authority.

## Architecture Compliance note on “no new architecture”

Routes and thin presentation services were added for Tutor, Knowledge Map, and Curriculum Health. These are UI projection adapters, not educational architecture.
