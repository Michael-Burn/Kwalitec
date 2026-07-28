# RP-001.4 — Experience Risk Register

**Programme:** RP-001 — Alpha Readiness Certification  
**Work Package:** RP-001.4 — Premium Experience Certification  
**Date:** 2026-07-28  
**Scope:** Risks to premium perception, calm focus, interaction trust, and accessibility presentation  
**IDs:** **XR-xx** (experience). Cross-links to R-xx / JR-xx / IR-xx where overlap exists.  
**Companion:** `PREMIUM_EXPERIENCE_AUDIT.md`

---

## Severity scale

| Level | Meaning |
|-------|---------|
| Critical | First-session premium/trust perception breaks on default Alpha path |
| High | Likely noticeable dilution of premium / calm / focus for professionals |
| Medium | Manageable with briefing or later polish; Alpha-acceptable if disclosed |
| Low | Residual; monitor |

---

## Experience risk register

| ID | Risk | Category | Severity | Surfaces | Evidence | Residual mitigation (process only — no code in RP-001.4) |
|----|------|----------|----------|----------|----------|----------------------------------------------------------|
| XR-01 | Dual design languages (EOS panels vs Bootstrap/V1 cards) feel like two products | Visual inconsistency / Brand / Trust | **High** | Onboarding, Study Plan, Help, Settings vs Home/Session | `layouts/base.html` content + Bootstrap `.card`; JR-02, R-02 | Disclose Stage-1 dual chrome; do not demo Settings as “premium showcase” |
| XR-02 | Home cognitive overload (MES + MI + secondary + tertiary) breaks calm focus | Cognitive overload / Emotional | **High** | Home | `home.html` hero + MI + readiness/journey/coach + milestones/actions; JR-05 | Brief testers: start from hero CTA; treat lower panels as optional |
| XR-03 | Presentation-only reflection options still look choice-like | Trust / Interaction / A11y | Medium | Home reflection preview | Spans `.student-reflection-option` + honesty disclaimer; RR-001.1 removed fake buttons | Disclaimer present — watch cohort for click attempts; style further in later UX |
| XR-04 | Empty Home / sparse memory surfaces look unfinished | Trust / Emotional | **High** | Home empty CTA path; early Journal/Timeline/History | JR-04, JR-19 | Provision plan+calibration; brief empty-as-honest |
| XR-05 | Navigation wraps into multi-row chrome on mobile | Navigation friction / Mobile | Medium | All EOS pages | `.student-nav-list { flex-wrap }` | Test on 375px; accept for Alpha or schedule compact nav |
| XR-06 | Two empty-state systems + sparse skeletons → uneven polish | Visual inconsistency / Perceived performance | Medium | Cross | `student-empty` vs `educational_empty`; skeleton mostly session overview | Disclose SSR nature; unify in polish programme |
| XR-07 | Bootstrap flash alerts feel generic vs EOS calm | Brand / Emotional | Medium | All flashed routes | `flash_messages.html` | Prefer calm copy; limit stack; later toast system |
| XR-08 | Error pages drop EOS topbar (auth shell) | Brand inconsistency / Navigation | Low | 403/404/500 | `errors/*.html` extend `auth_base` | Accept; recovery CTAs clear |
| XR-09 | Session focus quality not matched when returning to dense Home | Emotional / Interaction | Medium | Session → Home | Session max-width focus vs Home multi-panel | Journey briefing: Home is command centre, Session is focus room |
| XR-10 | Wizard length + V1 chrome increase onboarding friction | Interaction / Cognitive | Medium | Study Plan wizard | 7 steps; wizard.css | Prefer guided Alpha scripts; don’t skip plan |
| XR-11 | Accessibility gaps on V1 pages; no WCAG claim | Accessibility | Medium | Help, Settings, wizard, onboarding | R-15, JR-15; CAP-25 conditions | No conformance marketing; EOS path preferred for a11y demos |
| XR-12 | Profile “Reminders” implies push notifications | Trust erosion | Medium | Profile | JR-20, R-07 | Disclose student-initiated return only |
| XR-13 | History expectation (charts/analytics) unmet | Trust / Brand | Medium | History | JR-14; narrative + cards | Brief: memory + sessions, not BI |
| XR-14 | Enabling Unified Journey / Experience Feedback / QC without density redesign | Cognitive overload / Flag transition | **High** if enabled | Home, Session | Flag blocks in `home.html`; JR-18 | Keep OFF for Alpha; delta-cert if enabled |
| XR-15 | Coach / Tutor / Mission Intelligence naming competes for attention | Cognitive / Brand | Medium | Home | Coach panel + Tutor form + MI aside; IR terminology | Accept for Alpha; identity programme follow-up |
| XR-16 | CDN Bootstrap dependency vs self-hosted fonts/tokens | Brand / Perceived performance / Security posture | Low–Medium | All shells | jsDelivr Bootstrap CSS/JS | Known; CSP-sensitive; not Alpha blocker |
| XR-17 | Success feedback inconsistent (flash vs completion cards vs ack blocks) | Interaction / Visual | Medium | Session complete, commitment, forms | Mixed patterns | Accept; later unify |
| XR-18 | Help/Onboarding visual craft below learning cores | Brand / Emotional | Medium | Help, Onboarding | Utility Bootstrap layout | Don’t lead sales demos from Help |
| XR-19 | Inter-only system is professional but not distinctive typography | Brand | Low | Global | `fonts.css` Inter | Accept — restraint over novelty for Alpha |
| XR-20 | Cohort UX validation not executed — premium cert is audit-only | Operational / Trust | **High** | Cross | Same family as JR-16 / R-16 | Run Internal Alpha validation before “student-proven premium” claims |
| XR-21 | Login feature list length slightly marketing-dense | Emotional / Density | Low | Auth | Six bullets on landing | Accept; still brand-led |
| XR-22 | Finish control presentation-only on some Home guided states | Interaction honesty | Low–Medium | Home | `data-presentation-only` finish span | Honest text; ensure copy never looks like button (CSS note exists) |

---

## Highest experience risks (board view)

1. **XR-01** — Dual chrome / dual component language.  
2. **XR-02** — Home cognitive overload.  
3. **XR-04** — Empty / sparse early states mistaken for unfinished product.  
4. **XR-14** — Flag enablement without density redesign.  
5. **XR-20** — No live cohort premium validation yet.  
6. **XR-05 / XR-11** — Mobile wrap + a11y residual on V1 pages.

---

## Category summary

| Category | Critical | High | Medium | Low |
|----------|---------:|-----:|-------:|----:|
| Visual inconsistency | 0 | 1 | 2 | 0 |
| Interaction friction | 0 | 0 | 4 | 1 |
| Navigation friction | 0 | 0 | 1 | 1 |
| Cognitive overload | 0 | 2 | 2 | 0 |
| Accessibility | 0 | 0 | 1 | 0 |
| Trust erosion | 0 | 1 | 3 | 0 |
| Brand inconsistency | 0 | 1 | 2 | 2 |
| Emotional / calm | 0 | 1 | 2 | 1 |
| Operational | 0 | 1 | 0 | 0 |

(Counts overlap where a risk spans categories.)

---

## Mapping from prior programmes

| Prior ID | Experience expression |
|----------|----------------------|
| R-02 / JR-02 | XR-01 |
| R-04 / JR-04 / JR-19 | XR-04 |
| R-05 / JR-05 | XR-02 / XR-15 |
| JR-06 / IR-03 (post-RR-001.1) | XR-03 (severity, reduced severity) |
| R-15 / JR-15 | XR-11 |
| JR-14 | XR-13 |
| JR-18 / R-13 | XR-14 |
| JR-16 / R-16 | XR-20 |
| JR-20 / R-07 | XR-12 |

---

## Explicit non-risks for this package

- Implementing UI unification or Home density reduction (out of scope — identified only).  
- Enabling feature flags to “complete” the experience.  
- Changing educational algorithms, recommendations, or architecture.  
- Declaring WCAG conformance.  
- Re-scoring KSI.

---

## Failures

**No Fail-severity experience defects remain on the default Alpha path after RR-001.1** (false reflection controls and unreachable revision ack were Critical journey/trust defects; remidiated). Premium certification is therefore **Conditional Pass**, driven by High residuals above — not by open Critical UX defects.
