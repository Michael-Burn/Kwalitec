# RC-001 — Screenshot Index

**Location:** all files below are under `knowledge/product/rc001/screens/`.
**Total files:** 162.
**Capture pipeline:** `knowledge/product/rc001/_evidence/capture_rc001.py` (static screens, 9 breakpoints, live routes), `capture_session_flow.py` (session flow, 9 breakpoints, real service stack via Flask test client), `capture_dark_mode.py` (dark/light theme pairs), plus three one-off captures (404 error page, live B4/B5 keyboard checks).

Breakpoint naming convention: `{tier}-{width}px-{screen}.png`, where tier is `mobile` (320/375/390/414), `tablet` (768/820), or `desktop` (1024/1280/1440).

---

## Success-state screens — full 9-breakpoint coverage

Each row below has a screenshot at all 9 required breakpoints (320, 375, 390, 414, 768, 820, 1024, 1280, 1440px). Filenames follow `{tier}-{width}px-{screen}.png`.

| Screen | Route | 320 | 375 | 390 | 414 | 768 | 820 | 1024 | 1280 | 1440 |
|---|---|---|---|---|---|---|---|---|---|---|
| Home | `/student/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Journey | `/student/journey` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Revision | `/student/revision` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| History | `/student/history` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Profile | `/student/profile` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Study Plan | `/study-plan/` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Settings → Profile | `/settings/profile` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Settings → Preferences | `/settings/preferences` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Settings → Data | `/settings/data` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Settings → Account Status | `/settings/internal-alpha` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Help | `/alpha/help` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Session Overview | `/session/<id>/overview` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Session Activity | `/session/<id>/activity` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Session Activity (explained, post-answer) | `/session/<id>/activity/answer` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Session Reflection | `/session/<id>/reflection` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Session Summary | `/session/<id>/summary` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

16 screens × 9 breakpoints = 144 files. Example filenames: `mobile-320px-home.png`, `tablet-768px-session-reflection.png`, `desktop-1440px-settings-account-status.png`.

## Empty-state screens (1440px, representative)

Captured against a seeded student account with no active study plan, so widgets render their genuine "no data yet" copy rather than fabricated content:

- `desktop-1440px-empty-home.png`
- `desktop-1440px-empty-journey.png`
- `desktop-1440px-empty-revision.png`
- `desktop-1440px-empty-history.png`
- `desktop-1440px-empty-profile.png`

## Error state

- `desktop-1440px-error-404.png` — unauthenticated-safe 404 page (`/student/does-not-exist-rc001`), confirming the product's error surface is honest ("Page Not Found," reference ID for support) rather than a stack trace or blank page.

## Onboarding

- `onboarding-1440px-onboarding.png` — the guaranteed first-time onboarding screen (B8).

## Dark mode / Light mode (1440px, representative screens)

Captured via Playwright's `color_scheme` context option, which drives the same `prefers-color-scheme` media query `app/static/js/theme.js` resolves `data-theme` from:

| Screen | Light | Dark |
|---|---|---|
| Home | `light-1440px-home.png` | `dark-1440px-home.png` |
| Session Reflection | `light-1440px-reflection.png` | `dark-1440px-reflection.png` |
| Settings → Account Status | `light-1440px-settings-account-status.png` | `dark-1440px-settings-account-status.png` |
| Study Plan | `light-1440px-study-plan.png` | `dark-1440px-study-plan.png` |

## Accessibility live-check captures

- `a11y-b4-after-escape.png` — Welcome modal immediately after Escape dismissal (B4).
- `a11y-b5-drawer-open.png` — Navigation drawer open at mobile width, focus inside it (B5).
- `b10-settings-account-status.png` — Settings → Account Status page confirming "Learning profile status" no longer appears (B10).

---

## Coverage accounting

- 144 success-state screens (16 screens × 9 breakpoints)
- 5 empty-state screens (1440px)
- 1 error-state screen (1440px)
- 1 onboarding screen (1440px)
- 8 dark/light theme pairs (4 screens × 2 themes)
- 3 accessibility live-check captures

**Total: 162 screenshots**, matching the file count under `knowledge/product/rc001/screens/`.

All required screen categories from the programme brief are represented: Loading (see Known Limitation below), Empty, Success, Error, Settings, Help, Mission (Session flow — the canonical Mission/session experience under `SOLE_RUNTIME`), Study Plan, History, Journey, Revision, Reflection, Profile, Home.

**Known limitation — Loading state:** this application is server-rendered (Flask + Jinja2); there is no client-side loading spinner or skeleton state between navigation and content paint to capture as a distinct screenshot — the server returns a fully-rendered page in one response. A literal "Loading" screenshot would show either a blank white frame (mid-navigation) or the fully-loaded page, neither of which is a meaningful, reproducible design artifact. This is stated as an honest architectural fact, not an omission.
