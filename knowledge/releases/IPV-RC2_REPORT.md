# IPV-RC2 — Independent Product Validation Report

**Programme:** Independent Product Validation (IPV)  
**Build:** VERSION 1.0.0 — RC2 (`APP_VERSION` / health `version` = `1.0.0`; chrome **Build RC2**)  
**Status:** INDEPENDENT VALIDATION — COMPLETE  
**Evaluator posture:** External Internal Alpha participant / product reviewer  
**Method:** Fresh local install (venv, `.env`, `flask db upgrade`, `flask create-admin`, `flask create-test-user`), then black-box HTTP journeys against a clean SQLite database. Judgement based only on observable product behaviour.  
**Date:** 2026-07-17  
**Mandatory references reviewed after evaluation:** `PRODUCT_BLUEPRINT.md`, `docs/release/RELEASE_NOTES_v1.0.0-RC2.md`  
**Manifest:** `knowledge/releases/RC2_RELEASE_MANIFEST.md`

---

## Executive Summary

RC2 is a coherent invite-only Internal Alpha product. A new student can sign in with provisioned credentials, create a Study Plan, complete a Study Session with practice capture, see Dashboard recommendations and Analytics, and — after syllabus completion — continue in a clearly labelled Revision Workspace with revision-specific sessions. The Founder Command Centre is operable when the runtime administrator email allowlist matches the signed-in account.

No Critical defects were observed that break the primary learning loop or Founder governance surfaces under correct configuration. Remaining issues are operator friction, documentation gaps, and Alpha-honest limitations already aligned with the release notes (no public registration, deferred Twin-first cutover, Founder post-login landing).

**Release decision: APPROVE** — VERSION1-RC2 may proceed as the Internal Alpha operational baseline.

---

## Product Scorecard

| Area | Rating (/10) |
|-------|--------------|
| Student Experience | 8 |
| Founder Experience | 7 |
| Educational Workflow | 8 |
| Performance | 9 |
| Security Confidence | 8 |
| Documentation | 6 |
| Branding | 8 |
| Usability | 7 |
| Operational Readiness | 8 |

---

## Strengths

1. **Install path works.** README Getting Started (`venv` → `.env` → `flask db upgrade` → `flask create-admin` → `flask run`) produced a healthy app. `/health` returned `status=ok`, `database=connected`, `version=1.0.0`. Curriculum import on first app start loaded supported IFoA papers without operator intervention.

2. **Invite-only Alpha is honest.** Login shows Internal Alpha / Build RC2 identity, explains there is no public sign-up, and points participants to a coordinator. No registration link was observed.

3. **First-time student path is directed.** A new account without a plan is sent to Study Plan wizard step 1. Empty states push “Create your study plan” rather than a blank dashboard.

4. **Study Plan wizard is clear.** Seven steps with Supported / Coming Soon labelling. Selecting Coming Soon paper **CS2** correctly stayed on step 2 (did not advance). Supported **CS1** created a real curriculum-backed plan.

5. **End-to-end Learning loop works.** Plan creation → today’s Study Session → start → finish with practice outcome → recorded confirmation → Dashboard recommendations (with why/explain language) → Analytics with topic/readiness language. Session completion persisted.

6. **Revision feels like a continuation.** After full syllabus topic completion, Dashboard switched to **Revision Workspace**, announced **Revision Mode**, and Study Session became **Today’s Revision Session** with consolidate framing. A regenerated revision mission (`Revision: Timed Practice Session`) completed successfully; syllabus `completed` topic counts remained intact (14/14).

7. **Founder Command Centre is a real operator home.** With matching `ADMIN_EMAIL`, all primary/secondary Founder GET routes returned HTTP 200 (Overview, Operational Health, Feedback, Vision Journal, Releases, Internal Alpha, Research, Participants, Settings, Attention, Findings, Operations, Vision Timeline/New). Vision Journal accepted a new entry. Operational Health showed Needs Attention / Healthy Activity / Trends with revision, session, feedback, and participant signals. Releases and Internal Alpha reflected **1.0.0 / Build RC2**. Students receive **403** on `/founder/`.

8. **Security basics held under abuse probes.** External `next=` open redirect rejected; CSRF rejected tokenless POSTs; GET `/auth/logout` returned 405 (POST-only); cross-user Study Session access denied; invalid practice (`correct > attempted`) refused completion with validation messaging; duplicate finish on completed session did not 500; concurrent dual sessions for one user both loaded Dashboard.

9. **Branding and chrome are consistent.** Login hero (“Disciplined Exam Preparation”), Internal Alpha badge, Build RC2, student sidebar (Dashboard / Study Plan / Study Session / Analytics), `lang` on HTML, and `<main>` landmarks present. Student Mission terminology on Study Session pages was largely cleaned up (Study Session-dominant copy).

10. **Performance felt snappy locally.** Primary student and Founder pages typically rendered in tens of milliseconds in the evaluation harness (well under 1.5s).

11. **Product Check-in works when completed.** Full radio set + free text submitted to `/research/thank-you`; Founder Feedback inbox reflected submission attributes (e.g. experience rating / classification). Contributor recognition fired on submit.

---

## Issues

### Critical

None observed.

---

### High

#### H-1 — Founder access depends on runtime email allowlist, not the admin account itself

**Description:** Founder Command Centre access is granted when the signed-in user’s email is in `ADMIN_EMAIL` ∪ `FOUNDER_EMAILS` **as currently set in the process environment**. Creating an admin via `flask create-admin` does not encode Founder capability on the user record. If `ADMIN_EMAIL` later differs from that user’s email (common when reusing a shared `.env` or rotating env vars), the “administrator” receives opaque **403** on every `/founder/*` route.

**Impact:** A coordinator following README create-admin can believe they have an operator account while being locked out of Founder Overview, Operational Health, Feedback, and Vision Journal — the surfaces Internal Alpha depends on.

**Steps to reproduce:**
1. `ADMIN_EMAIL=ipv-admin@…` → `flask create-admin`.
2. Restart / run app with a different `ADMIN_EMAIL` (e.g. from another `.env`).
3. Sign in as `ipv-admin@…` and open `/founder/`.
4. Observe HTTP 403.

**Recommendation:** Document the allowlist rule next to `create-admin` in README and `.env.example` (`ADMIN_EMAIL` / `FOUNDER_EMAILS`). Prefer a durable Founder flag or “first admin is Founder” invariant that does not silently diverge from env drift. Surface a student-safe explanation on 403 (“not authorised for Founder”) instead of a bare forbidden page when authenticated.

---

### Medium

#### M-1 — README does not document participant provisioning

**Description:** Getting Started covers `create-admin` but not `flask create-test-user`, which is the observable path to create Internal Alpha student accounts (no public registration).

**Impact:** A new developer/operator can stand up the app but cannot onboard student participants from README alone.

**Steps to reproduce:** Follow README Getting Started only; attempt to create a second login for a student without reading CLI help.

**Recommendation:** Add an Internal Alpha operator subsection: `flask create-test-user`, credential handoff, and note that Founder emails must remain aligned with `ADMIN_EMAIL` / `FOUNDER_EMAILS`.

#### M-2 — Administrator without a Study Plan is diverted into the student wizard on login

**Description:** Signing in as the Founder/admin account with no active Study Plan lands on `/study-plan/wizard/1`. Founder routes remain reachable by URL once the allowlist matches, but first landing is student onboarding.

**Impact:** Operator efficiency suffers; Founder must know to navigate away from the wizard. (Also listed as a deferred limitation in RC2 release notes — confirmed live.)

**Steps to reproduce:** Create admin only; sign in; observe redirect to wizard step 1 rather than `/founder/`.

**Recommendation:** Post-login routing: Founder emails → Founder Overview (or Dashboard with Founder CTA); students without plans → wizard.

#### M-3 — Skipping Calibration without beginner-skip can leave TwinAbsent and weaken first-run welcome

**Description:** After plan creation the product routes to Calibration (“Educational history”). Completing beginner skip / confirmation marks welcome eligibility. Abandoning without that path, or never finishing Calibration, leaves Dashboard operating with TwinAbsent fallback (observed repeatedly in server logs) while Stage A recommendations still appear. Welcome modal did not appear until welcome eligibility was marked (e.g. via Calibration completion path).

**Impact:** First-time guidance (welcome modal) and Twin-backed intelligence may never appear for students who dismiss Calibration casually; operators see TwinAbsent noise; educational honesty is preserved but the “personalised journey” promise is softer.

**Steps to reproduce:** Create plan → open `/calibration/after-plan/<id>` → leave without beginner skip/confirm → use Dashboard/Study Session.

**Recommendation:** On abandon, still mark welcome eligibility and show an explicit “starting from scratch” confirmation; keep TwinAbsent invisible to students (already largely true) but ensure next-step CTA remains obvious.

#### M-4 — Product Check-in form is heavy; incomplete submits are easy

**Description:** Share Feedback requires many mandatory radio groups (experience, feature helped, friction, confidence, return intent, classification, etc.). Incomplete POSTs remain on the form. Errors are present but the form is long enough that Alpha participants may abandon.

**Impact:** Lower feedback volume into Founder inbox — weakens the continuous improvement loop even though the pipeline works when completed.

**Steps to reproduce:** Open `/research/checkin?source=settings`; submit with only free text; observe return to check-in without thank-you.

**Recommendation:** Progressive disclosure or a shorter Alpha default check-in; stronger top-of-form “complete all required ratings” summary.

#### M-5 — Founder Overview logs weekly brief validation failure

**Description:** Opening Founder Overview logged `BriefingValidationError: missing_week` while the Overview page still rendered successfully.

**Impact:** Operator log noise; possible missing weekly brief panel content for Alpha weeks without brief artefacts. Page remained usable.

**Steps to reproduce:** Sign in as Founder; GET `/founder/`; inspect application logs.

**Recommendation:** Soft-empty state in UI (“No weekly brief for this week”) without ERROR stack traces in normal Alpha operation.

---

### Low

#### L-1 — Duplicate Study Session options on Product Check-in

**Description:** `feature_helped_most` offers both “Study Session” and “Today’s Study Session”.

**Impact:** Minor terminology confusion in feedback taxonomy.

**Steps to reproduce:** Open Product Check-in; inspect feature radios.

**Recommendation:** Collapse to a single canonical label matching nav (“Study Session”).

#### L-2 — Analytics less clearly Revision-branded than Dashboard / Study Session

**Description:** In Revision Mode, Dashboard and Missions strongly say Revision Workspace; Analytics emphasised Completed / Readiness / Topic language without equally clear Revision Workspace framing.

**Impact:** Slight workspace identity break across Analysis nav.

**Steps to reproduce:** Enter Revision Mode; open Analytics.

**Recommendation:** Mirror Revision Workspace eyebrow/description on Analytics when `is_revision`.

#### L-3 — Settings profile “save” honesty not deeply validated

**Description:** Settings shows Internal Alpha / Build RC2 usefully. Deeper profile persistence behaviours were not fully exercised beyond surface load; prior readiness notes flagged flash-only saves — treat as residual Alpha polish risk.

**Impact:** Low for invite-only Alpha if operators communicate limitations.

**Steps to reproduce:** Open Settings; attempt profile edits if offered.

**Recommendation:** Either persist promised fields or remove save affordances that no-op.

---

### Observation

#### O-1 — No public self-serve account creation

Expected for Internal Alpha; participants need coordinator + CLI provisioning. Login copy explains this when Internal Alpha enablement is on.

#### O-2 — Twin-first Educational Intelligence not the live student authority

Dashboard continued to serve recommendations while logging TwinAbsent for a student without Calibration Twin. Matches Version 1 coexistence described in release notes — not a regression against RC2 claims, but students should not be told Twin is “live” as sole authority.

#### O-3 — Password reset is coordinator-mediated

Acceptable for invite-only Alpha; not suitable for public launch.

#### O-4 — `RC2_RELEASE_MANIFEST.md` missing

Release notes and operational readiness report exist; a single manifest file named in the IPV brief was not found.

---

## Recommendations

### Immediate (before or with RC2 operator handoff)

1. Document `FOUNDER_EMAILS` / `ADMIN_EMAIL` allowlist behaviour and `flask create-test-user` in README + `.env.example`.
2. Confirm production/staging `ADMIN_EMAIL` matches the Founder login used for Alpha ops (fingerprint checklist item in release notes).
3. Smoke: login → wizard/plan → Study Session → Analytics; Founder Overview + Operational Health; one Product Check-in.

### Post-RC2

1. Founder post-login landing (avoid student wizard diversion) — already deferred in release notes; prioritise.
2. Durable Founder authorisation (role flag) to eliminate env-drift 403s.
3. Shorten Alpha Product Check-in; improve incomplete-submit summary.
4. Calibration abandon → welcome eligibility + clear fresh-start messaging.
5. Quiet weekly-brief empty state on Founder Overview.

### Version 2

1. Twin-first product cutover and persistence (retire TwinAbsent fallback as primary path).
2. Exam Ready lifecycle beyond Learning → Revision.
3. Public registration / password reset only after explicit release gates.
4. Broader subject support beyond current Supported IFoA set.

---

## Release Decision

**APPROVE**

VERSION 1.0.0 Build RC2 is suitable to proceed as the invite-only Internal Alpha operational baseline. The observable student Learning and Revision workflows, Founder Command Centre (when correctly allowlisted), branding fingerprint, and baseline security behaviours support continued Alpha use. Issues above should be tracked; none observed in this validation were Critical blockers for Internal Alpha.

---

## Evaluation Evidence (summary)

| Area | Result |
|------|--------|
| Installation & Startup | Pass — migrate, admin, health, login chrome |
| First-time student | Pass — wizard redirect, Supported/Coming Soon gate, plan create, Calibration entry |
| Learning workflow | Pass — session start/finish/practice, dashboard recommendations, analytics |
| Revision workflow | Pass — workspace switch, revision session, progress preserved |
| Founder platform | Pass (with H-1 config caveat) — Overview, OH, Feedback, Vision, Releases, IA |
| Reliability | Pass — CSRF, open redirect, ownership, invalid practice, logout, multi-session |
| Educational integrity | Pass for Stage A Alpha — recommendations + revision consolidation language; Twin deferred |
| Founder governance | Pass — Vision entry create; feedback inbox; OH signals; release identity |

---

## Overall Product Experience

**Would you continue using this product?**  
Yes — as an Internal Alpha actuarial student with a Supported paper (e.g. CS1), the daily loop (plan → session → feedback → analytics) is understandable and low-friction.

**Would you recommend it to another actuarial student?**  
Yes, with coordinator onboarding (invite credentials, Supported-paper expectation). Not yet as a public self-serve product.

**Would you trust this platform for Internal Alpha?**  
Yes. Identity, educational workflow, Revision continuation, and Founder oversight are real and usable. Trust for wider release would require closing High/Medium operator and Twin/auth gaps above.

---

## Acceptance Criteria Checklist

- [x] Entire student workflow evaluated  
- [x] Revision workflow completed  
- [x] Founder platform reviewed  
- [x] Reliability assessed  
- [x] Product strengths documented  
- [x] Defects classified  
- [x] Overall recommendation issued  
- [x] Release decision recorded (**APPROVE**)
