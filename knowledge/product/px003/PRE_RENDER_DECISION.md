# PX-003 — Pre-Render Decision

**Reviewer role:** Head of Product Design / Principal UX Researcher / Accessibility Specialist / Release Approval Reviewer, combined, independent of prior programme authorship.
**Mandate:** Reject if warranted. Do not redesign. Do not invent features. Judge only against usability, consistency, trust, accessibility, cognitive load, craftsmanship, and educational focus.

---

## 1. Screen-by-screen verdict

Verdict key: **Ready** — no blocking issue found on this screen. **Blocked** — at least one item in `RELEASE_BLOCKERS.md` lives on this screen. **Ready with notes** — no blocker, but see `NON_BLOCKING_IMPROVEMENTS.md`. **Not independently verified** — reachable, but this review did not sample it in enough depth to render an independent verdict (inherited from a prior audit's same gap, or newly identified as unsampled).

| Screen / state | Verdict | Why |
|---|---|---|
| **Authentication** — Sign in | Ready with notes | Clean, honest, correct CSRF/error handling. "Education Operating System" and "Internal Alpha" framing carried over unresolved (N7, N8) but not independently blocking. |
| Authentication — invalid credentials | Ready | Generic, non-leaking error message; field errors rendered accessibly. |
| Authentication — after logout | Ready | Returns cleanly to Sign in. |
| Authentication — account recovery | Ready with notes | No self-service reset exists by design (invite-only); no rate-limit messaging (N9). Acceptable for an invite-only model, flagged for operational sign-off. |
| **Onboarding** | Blocked | Content itself is strong, but B8: not reliably triggered on the actual production login path. |
| **Home** (`/student/`) | Blocked | B2 (Profile contradiction is visible from Home's own plan-coherence framing), B3 (duration trust), B8-adjacent (may be the very first screen if onboarding is skipped). Cognitive load also elevated (N2). |
| **Home — empty (new account)** | Ready with notes | Calm, explains why it's empty; denser than strictly necessary (inherited PX-001 note), not blocking. |
| **Mission / Today's Study Session** | Blocked | B3 (duration trust) originates partly here; otherwise the single strongest, clearest screen in the product (confirmed again in this review). |
| **Active Study Session** | Ready with notes | Real timer, real pause/finish controls; N14 (finish has no confirmation), N17 (timer not `aria-live`). |
| **Practice Outcome Capture** | Ready | Honest framing, explicit "I didn't practise today" opt-out, no false precision demanded. |
| **Study Session Feedback** (`session_recorded.html`) | Ready with notes | Best-written screen in the product; diluted slightly by visible internal-alpha feedback instrumentation (N18), not blocking. |
| **Session Overview** | Ready | Clean structure; skeleton loading state present and correctly built. |
| **Session Activity** | Ready | No new issues found. |
| **Session Reflection** | Blocked | B1 — the note a student writes is discarded despite an explicit on-screen promise that it is kept. |
| **Session Summary** | Ready with notes | Functions correctly; N16 (step indicator advertises a "Complete" step the happy path never shows). |
| **Session Complete** | Ready with notes | Well-written but effectively dead code on the default path (N16). |
| **Journey** | Ready with notes | Empty state genuinely improved since PX-001; populated state still thin (N5), not blocking. |
| **Revision** | Ready with notes | Same assessment as Journey; both empty-state tiers are calm and explanatory. |
| **History** | Ready with notes | Empty and populated states both reasonable; no alarming zero-state framing found. |
| **Analytics (legacy)** | Ready with notes | KPI-per-row rule now respected (4+2, not 6); zero-history framing improved; false precision remains on hour figures (N3, N4). |
| **Dashboard (legacy)** | Not independently verified beyond confirming it correctly redirects under production flags (B9's sibling routes) — see Settings for the one legacy surface that does *not* redirect. |
| **Study Plan — Wizard (all steps)** | Ready with notes | Honest "Not Supported"/"Partially Supported" badging preserved; step 1's unsupported-option density is a pre-existing, non-blocking finding carried from PX-001. |
| **Study Plan — Roadmap view** | Ready with notes | False-precision fix (PX-002B) verified still in place; duration semantics (topic time vs. session time) still contribute to B3. |
| **Study Plan — List / Edit / Archive / Delete** | Ready | Native `confirm()` dialogs confirmed fully replaced by the styled confirmation modal in this surface. |
| **Settings — General** | Blocked | B9 — this entire surface is a second, un-redirected, reachable settings experience running the legacy shell alongside the canonical Profile the current nav actually points to. |
| **Settings — Internal Alpha** | Blocked | B10 — "Learning profile status" internal-engine label exposed to any logged-in student, not gated to alpha participants; also inherits B9 and B6 (contrast). |
| **Settings — Data (export/backup/restore)** | Ready | Confirmed styled confirmation modal in place for the single most destructive action on this screen; no native dialogs found. |
| **Profile (canonical, `/student/profile`)** | Blocked | B2 — "Current Examination: Not set" contradiction with the rest of the product for the same account. |
| **Help & Support** | Ready with notes | Substantively rebuilt since PX-001 — real FAQ content, working search, accessible empty-state announcement. Minor gap: non-empty filtered results are not announced (folded into Accessibility Review §2), not blocking. |
| **Errors — 404** | Ready | On-brand, calm, correct routing by auth state, reference ID now on-palette and explained. |
| **Errors — 403** | Ready | Same pattern and quality as 404. |
| **Errors — 500** | Ready with notes | Styled path confirmed to exist; "Try again" link uses `javascript:location.reload()` rather than a semantic button (cosmetic, not blocking). Whether a raw, unbranded Flask error can still occur for some failure classes was not independently re-verified in this pass beyond confirming the registered handler exists in `app/__init__.py`. |
| **Confirmation dialogs (destructive actions)** | Ready with notes | Native `confirm()`/`alert()` confirmed fully removed from all in-scope student templates; the one remaining native `confirm()` in the codebase is in the founder/admin console, out of this review's student-facing scope. Modal's dependency on Bootstrap loading successfully (N6) is a minor, non-blocking robustness gap. |
| **Welcome modal** (first-session dialog) | Blocked | B4 — declares `aria-modal="true"` with no supporting focus management, on the first modal a new student sees. |
| **Loading states** | Ready with notes | Skeleton primitives are well-built and correctly used (Session Overview); real-world timing/visibility was not independently re-verified (inherited PX-001 evidence gap, non-blocking on its own). |
| **Navigation chrome — Sidebar / mobile drawer** | Blocked | B5 (no focus trap / ARIA-expanded state) and B6 (contrast failure on section labels), both on a surface reachable from Settings, Help, Study Plan, and Onboarding. |
| **Navigation chrome — Canonical student top nav** | Ready with notes | Functions correctly; does not collapse to a drawer on mobile, instead wraps (N12) — a deliberate-looking but unconfirmed choice. |
| **Desktop (general)** | Ready with notes | The strongest-evidenced surface across all three prior programmes and this review; the majority of blockers above are trust/data/accessibility defects that reproduce on desktop just as much as any other size — desktop rendering itself is not the concern. |
| **Tablet (general)** | Blocked (evidence gap) | B7 — no tablet viewport has ever been rendered and looked at. Verdict is "blocked" on the *absence of verification*, not a confirmed visual defect. |
| **Mobile (general)** | Blocked | B7 (same evidence gap) plus concrete, code-derived candidate defects this review could locate without rendering anything (mission grid `minmax(320px)` overflow risk, appearance-switcher touch targets, B5's drawer accessibility gap, which is mobile-only in practice). |

---

## 2. Release-blocking questions — direct answers

**Can a student immediately understand where they are?**
Mostly yes, with one concrete exception: a student who reaches `/settings/` (still fully reachable, B9) is in a visually and structurally different place than the canonical Settings/Profile the current navigation actually points to, with no signal that this is a different surface.

**Can a student immediately understand what they should do next?**
On the product's best screens (Mission, Study Session Feedback, error pages) — yes, clearly, in under two seconds. On Home, in its richest conditional state, no — the primary action can be preceded by up to a dozen stacked explanatory blocks (N2). This is a cognitive-load finding, not treated as independently blocking, but it is adjacent to two things that are blocking: if onboarding is skipped (B8), a first-time student's very first exposure to "what do I do next" may be Home in a state this review cannot guarantee is its simplest one.

**Can a student understand why something is important?**
The explainability pattern (Mission's "Why you are studying this," Study Session Feedback's four-question honesty structure) is genuinely one of the product's strengths and holds up under this review's independent inspection. The one place this answer is actively false rather than merely absent is Reflection (B1) — it tells the student why the note matters and then discards it.

**Would any screen reduce trust?**
Yes: Reflection (B1), Profile (B2), and the Home/Mission/Study-Plan duration question (B3) are all specific, verifiable, factual contradictions or false promises — not tone issues. This is the most serious category of finding in this review, and it is the same category every prior programme identified as the product's central risk.

**Would any screen increase anxiety?**
No new anxiety-inducing pattern was found on the screens sampled (Analytics' zero-state framing, previously flagged, is verified fixed). The closest candidate is Settings exposing "Learning profile status" (B10) and other diagnostic language to a non-technical student, which reads as unfinished/internal rather than alarming per se.

**Would any wording confuse a first-time user?**
"Education Operating System" (N7) and "Internal Alpha" framing for what should be an external cohort (N8) are the two candidates; neither is confusing so much as tonally mismatched, which is why both are non-blocking rather than blocking.

**Would any workflow feel inconsistent?**
Yes: two settings experiences (B9), two full study-session flows with different completion semantics (N15), and a phantom fifth "Complete" step most students will never see (N16) are all real, verifiable inconsistencies.

**Would any interaction surprise the user?**
"Finish Study Session" ending an active session with a single, unconfirmed click (N14) is the closest candidate; not severe enough to block alone, but inconsistent with the product's own confirm-modal standard elsewhere.

**Would any screen feel unfinished?**
Settings → Internal Alpha's exposed engine-status label (B10) and the visible internal-feedback instrumentation on Study Session Feedback (N18) are the two candidates; the latter is likely intentional pilot instrumentation rather than an oversight.

**Would any screen feel over-designed?**
No. This review found no evidence of decorative complexity exceeding the product's own stated restraint standard.

**Would any screen feel under-designed?**
No screen was found to be under-designed in the visual sense (the previously-flagged "sparse canonical shell" issue on Journey/Revision is verified improved). The closer analogue is Home's cognitive-load ceiling (N2) — over-stacked, not under-designed.

---

## 3. What would change this decision

The ten items in `RELEASE_BLOCKERS.md` are individually narrow and, based on this review's reading of the code, individually fast to fix — none requires new architecture, new copy voice, or a redesign of any screen. Resolving B1 (wire the reflection note through), B2 (make Profile's exam label fall back to the same source Dashboard/Study Plan already use correctly), B9 (add the same `redirect_if_sole_runtime` guard already present on Dashboard/Analytics/Mission to Settings), and B10 (move or remove the "Learning profile status" field, or gate the route to actual alpha participants) closes four of the ten with a pattern the codebase already demonstrates it knows how to apply correctly elsewhere. B4 and B5 are focus-management additions to existing modal/drawer JS, not new components. B6 is a single CSS color-token change. B3 and B8 require a genuine decision (which service is the single source of truth for duration; whether onboarding gates on `student.home` as well as `dashboard.index`) but not a new design. B7 requires an action this review cannot itself perform: rendering the product on a real or emulated phone and tablet and looking at it.

None of the above is a reason to approve now on the promise of a fast follow-up. This review's mandate is conservative: an item that is fast to fix is still unfixed until it is fixed.

---

## 4. Decision

**REQUIRES ADDITIONAL WORK**

Ten specific, code-verified defects (`RELEASE_BLOCKERS.md`, B1–B10) each independently answer at least one of this review's release-blocking questions in the negative, on a screen a real Stage 1 external pilot student will reach through the product's own normal navigation — not an edge case, not a hypothetical, and not a matter of design taste. Three of the ten (B1, B2, B3) are specific, factual trust violations of exactly the kind the product's own prior review programmes identified as its most damaging failure mode, and this review found them to be still present in the current code, not resolved as previously reported. Two more (B4, B5) are accessibility failures on the two screens where failure matters most (the first modal a new student sees; the only way to reach navigation on a phone for half the product). One (B7) is a missing-evidence blocker: no mobile or tablet screen has ever actually been looked at, for a product explicitly preparing for a population that will use phones. Per this review's own instruction to be conservative and to reject when uncertain, the correct decision is to require this work before render, not to approve on the strength of everything else this product does well — and this review found genuine strengths (Mission, Study Session Feedback, Help, error pages, the confirm-modal replacement of native dialogs) that are not in question here.
