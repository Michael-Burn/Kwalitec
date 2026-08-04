# PX-007 — Founder Dogfood Report

**Programme:** PX-007 — Founder Dogfooding & Premium Certification  
**Workstream:** WS-11 — Founder Dogfooding (PX-B-052)  
**Status:** **COMPLETE**  
**Effective:** 2026-08-04  
**Authority:** Educational Content Freeze · EF-001 · PB-017 PASS · `PX002_WORKSTREAMS.md` · PX-003…PX-006 execution reports  

---

## 1. Purpose

Validate that Version 1 behaves like a premium study platform under structured founder usage — without expanding Version 1 scope.

## 2. Method

| Layer | What ran |
|-------|----------|
| Structured walkthrough | Login → Home → Plan → Session → Finish → Continue → Revision → History → Settings → Help → Errors (+ mobile/a11y posture) |
| Code-backed audit | Templates, microcopy, CSS/JS, presentation services on sole-runtime paths |
| Automated regression | Aggregate Phase 1–4 + PX-007 contracts — **157 passed** |
| Defect correction | PX7-001 / PX7-002 only (Major identity leaks on feedback) |

Evidence: `knowledge/evidence/releases/PX007/dogfood/` · `regression/pytest_aggregate.txt`

## 3. Coverage matrix

| Area | Covered | Verdict |
|------|---------|---------|
| Onboarding | Yes | Conditional / Pass |
| Login | Yes | Pass |
| Home | Yes | Pass |
| Study plan | Yes | Pass |
| Mission | Yes | Pass (sole-runtime → Home) |
| Session | Yes | Pass |
| Finish | Yes | Pass |
| Continue | Yes | Pass |
| Revision | Yes | Pass |
| History | Yes | Pass |
| Analytics | Yes | Pass (→ History) |
| Settings | Yes | Conditional (Minor dual chrome) |
| Help | Yes | Pass |
| Mobile | Yes | Conditional (device gallery residual) |
| Accessibility | Yes | Conditional (AT recording residual) |
| Error paths | Yes | Pass |

## 4. Findings summary

| Severity | Pre-fix | Post-fix |
|----------|---------:|----------:|
| Critical | 0 | **0** |
| Major | 2 | **0** |
| Minor | 6 | 6 (owned) |
| Cosmetic | 2 | 2 (owned) |

Ideas parked as Version 1.1 — see `PX007_RESIDUAL_REGISTER.md`.

### Closed Majors

1. **PX7-001** — Internal Alpha voice on default feedback paths → Private Beta / Kwalitec.  
2. **PX7-002** — “Closed Beta” eyebrow → Private Beta.

## 5. Chrome growth / fatigue (PX-B-052)

Established Home density, Help length, and footer chrome noted. No S1 reopen. Progressive disclosure on session complete holds. Multi-week LIVE calendar dogfood remains optional Founder follow-on; this exit closes the Foundation audit with logged observations.

## 6. Experience confidence (M10 provisional)

Mean dogfood rubric **4.4 / 5** (chrome trust, next action, tone, help, celebration honesty). Not exam-pass prediction. Not until-exam trust.

## 7. Educational honesty

Educational packages unmodified. EF-001 unchanged. Recommendation engine and Twin unchanged. No Runtime redesign.

## 8. Definition of Done — PX-B-052

| Criterion | Status |
|-----------|--------|
| Founder dogfood across primary surfaces completed | Met |
| Chrome-growth log filed | Met |
| Findings classified | Met |
| Critical = 0 · Major = 0 | Met |
| Ideas not treated as Version 1 bugs | Met |

**PX-B-052: Closed.**

## 9. Exit

Dogfood feeds WS-12 certification. See `PX007_PREMIUM_CERTIFICATION.md`.

Signed: Product Experience · PX-007 WS-11 · 2026-08-04
