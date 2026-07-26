# MS-001 — UI Inventory (Navigation-Related)

**Milestone:** MS-001 — Foundational Trust  
**Status:** Architecture Investigation (read-only)

Inventory of every navigation-related UI surface involved in finding, starting, resuming, or completing study. Templates, partials, JS, and presentation components.

---

## 1. Canonical Student Experience

| Location | Responsibility | Dependencies | Reusable? | Removal candidate? |
|---|---|---|---|---|
| `app/templates/student/base.html` | Student chrome / layout | student nav, shared assets | Layout only | **Keep** |
| `app/templates/student/home.html` | Primary “what next” + Start Session form | `StartSessionForm`, page VM, CTA | Page | **Keep** — primary entry |
| `app/templates/student/journey.html` | Journey progress surface | page VM | Page | **Keep** |
| `app/templates/student/revision.html` | Revision options + begin form | `BeginRevisionForm` | Page | **Keep** |
| `app/templates/student/history.html` | History / analytics replacement | page VM | Page | **Keep** |
| `app/templates/student/profile.html` | Profile / settings-ish surface | page VM | Page | **Keep** |
| `app/templates/student/components/navigation.html` | In-page student nav | endpoints | Partial | **Keep** |
| `…/recommendation_card.html` | Renders recommendation block | home VM | Partial | **Keep** |
| `…/explanation_card.html` | Why this recommendation | explanation VM | Partial | **Keep** |
| `…/readiness_card.html` | Readiness display | home VM | Partial | **Keep** |
| `…/countdown_card.html` | Exam countdown | home VM | Partial | **Keep** |
| `…/progress_card.html` | Progress snippet | home VM | Partial | **Keep** |
| `…/journey_card.html` | Journey snippet on Home | journey VM | Partial | **Keep** |
| `…/history_card.html` | History snippet on Home | history VM | Partial | **Keep** |
| `app/presentation/student/view_models.py` | Page VM assembly | snapshots | Python | **Keep** |
| `app/presentation/student/navigation.py` | Nav tree definition | ExperienceSurface | Python | **Keep** |
| `app/static/js/student.js` | CTA dedupe, optimistic nav, telemetry | `/alpha/telemetry` | Script | **Keep** |

---

## 2. Canonical Session Experience

| Location | Responsibility | Dependencies | Reusable? | Removal candidate? |
|---|---|---|---|---|
| `app/templates/session/base.html` | Session chrome | session components | Layout | **Keep** |
| `session/overview.html` | Objective + Begin Session | `BeginSessionForm` | Page | **Keep** |
| `session/activity.html` | Question / answer / advance | answer + advance forms | Page | **Keep** |
| `session/reflection.html` | Reflection checkpoint | continue form | Page | **Keep** |
| `session/summary.html` | Outcomes + next | complete form | Page | **Keep** |
| `session/complete.html` | Return home CTA | complete form | Page | **Keep** |
| `session/components/navigation.html` | Linear step chrome | SURFACE_ENDPOINTS | Partial | **Keep** |
| `…/progress_bar.html` | Step progress | flow position | Partial | **Keep** |
| `…/activity_card.html` | Activity shell | activity VM | Partial | **Keep** |
| `…/question_card.html` | Prompt display | activity VM | Partial | **Keep** |
| `…/explanation_card.html` | In-session explanation | VM | Partial | **Keep** |
| `…/reflection_card.html` | Reflection content | VM | Partial | **Keep** |
| `…/completion_card.html` | Completion content | VM | Partial | **Keep** |
| `…/timer_card.html` | Timer display (server/VM driven) | VM | Partial | **Keep** (no legacy JS hooks) |
| `app/presentation/session/navigation.py` | Step ↔ endpoint map | SessionSurface | Python | **Keep** |
| `app/presentation/session/view_models.py` | Session page VM | flow snapshots | Python | **Keep** |

**Gap:** No `study_session.js`-equivalent for canonical timer/duration capture. Timer card exists; legacy localStorage timer is not shared.

---

## 3. Legacy Dashboard / Mission

| Location | Responsibility | Dependencies | Reusable? | Removal candidate? |
|---|---|---|---|---|
| `app/templates/dashboard/index.html` | Legacy home; Start/Resume CTA → missions | Planning, Mission, Recommendation, readiness | Page | **Yes** under sole runtime (superseded by student home) |
| `app/templates/mission/index.html` | Today’s Study Session hub | Mission status CTAs | Page | **Yes** under sole runtime |
| `app/templates/mission/session.html` | In-progress study UI | `study_session.js` data hooks | Page | **Yes** when legacy session retired |
| `app/templates/mission/session_practice_outcome.html` | Practice outcome capture | StudySessionService forms | Page | **Yes** with legacy closure path |
| `app/templates/mission/session_recorded.html` | Post-session feedback | session_feedback VM | Page | **Yes** with legacy path |
| `app/static/js/study_session.js` | Timer, checklist, duration prefill | localStorage / sessionStorage | Script | **Yes** when mission session UI removed |

**Retain until:** bridging ships **or** legacy dual-run remains required for evidence-gated practice outcome capture.

---

## 4. Shared chrome and ancillary navigation

| Location | Responsibility | Dependencies | Reusable? | Removal candidate? |
|---|---|---|---|---|
| `app/templates/partials/sidebar.html` | Dual nav trees by `SOLE_RUNTIME` | `v2_flags` | Partial | **Keep** structure; **remove legacy branch** after cutover |
| `app/templates/partials/topnav.html` | Top navigation | shared | Partial | **Keep** |
| `app/templates/partials/welcome_modal.html` | First-run; links `mission.missions` | dashboard dismiss | Partial | **Retarget or remove** (legacy-coupled) |
| Study Plan templates (`study_plan/*`) | Plan CRUD/wizard | wizard session | Pages | **Keep** (shared workflow) |
| Calibration templates | Post-plan Twin birth | coordinator | Pages | **Keep** |
| `alpha` onboarding / help | Onboarding + help centre | Alpha services | Pages | **Keep**; onboarding redirect target may need student.home |
| `app/static/js/app.js`, `theme.js` | Global UI | Bootstrap/theme | Scripts | **Keep** |

---

## 5. Forms (navigation-critical)

| Form | Module | Used by |
|---|---|---|
| `StartSessionForm` | `presentation/student/forms.py` | Home CTA |
| `BeginRevisionForm` | same | Revision CTA |
| `BeginSessionForm` | `presentation/session/forms.py` | Overview begin |
| `SubmitAnswerForm` / `AdvanceActivityForm` | same | Activity |
| `ContinueReflectionForm` / `CompleteSessionForm` | same | Reflection / complete |
| Legacy mission start / finish / outcome forms | `mission` templates + routes | Legacy session |

---

## 6. Reusability summary

| Category | Reusability | Notes |
|---|---|---|
| Student component cards | High within Student OS | Do not reuse on legacy dashboard without VM adapters |
| Session components | High within session flow | Linear only; not for legacy mission checklist |
| Legacy mission templates | Low | Tightly coupled to Mission.status + StudySessionService |
| Sidebar dual tree | Medium | Temporary coexistence pattern |

---

## 7. Candidates for removal (priority order after bridge)

1. Legacy branch of `sidebar.html`  
2. `dashboard/index.html` study CTA + eventually full page if unused  
3. `mission/index.html` + session/outcome/recorded templates  
4. `study_session.js`  
5. Welcome modal mission links (or retarget first)  
6. Unwired MissionEngine UI (none student-facing today — code archival, not template)

**Do not remove yet:** Study Plan, Calibration, Help, Auth, Evidence-bearing legacy finish path until canonical path writes equivalent `TopicProgress` / Evidence.

---

## 8. Components that should remain (Foundational Trust)

- Student Home + Start Session CTA  
- Session linear flow (overview → … → complete)  
- Resume-by-`active_surface` behaviour  
- Canonical sidebar tree  
- Study Plan wizard (onboarding to curriculum binding)  
- Telemetry hooks that measure real entry (`PresentationTelemetryService` events)

Anything that presents **demo “Core methods”** as if it were the student’s real mission should be treated as a **trust defect** until bridged — not as a permanent UI product.
