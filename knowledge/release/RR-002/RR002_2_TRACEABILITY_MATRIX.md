# RR-002.2 — Traceability Matrix

**Programme:** RR-002 — Governance Convergence  
**Work Package:** RR-002.2 — Educational Chrome & Presentation Convergence  
**Date:** 2026-07-28  
**Rule:** Every remediation references RP-002 finding → governance clause → modified file → student impact.  
**Companion:** `RR002_2_COMPLETION_REPORT.md` · `RP002_NON_COMPLIANCE_REGISTER.md`

---

## 1. Finding → evidence

| Finding | RP-002 NCR | Governance clause(s) | Modified file(s) | Student impact | Closure |
|---------|------------|----------------------|------------------|----------------|---------|
| **NCR-005** | RP002-NCR-005 | DG-001.1-D02; CI-01; DEP-03; RP002-AC-08 | `student/components/recommendation_card.html` | Reusable card no longer teaches Recommendation-as-Mission-hero; **Guidance** matches Home | **Closed** |
| **NCR-006** | RP002-NCR-006 | DG-001.2-D01/D02/D03; CP-10; RP002-AC-06 | `mission/session_recorded.html` | Observation = System; educational conclusion = Study Sensei — product brand not mentor | **Closed** |
| **NCR-007** | RP002-NCR-007 | DG-001.1-D02; CP-03; RP002-AC-07 | `dashboard/index.html` | Dashboard recommendation slot uses **Guidance** + Sensei attribution; no competing “Today's Recommendation” focus noun | **Closed** |

### RP-002 evidence paths (pre-remediation)

| NCR | RP-002 evidence cite |
|-----|----------------------|
| RP002-NCR-005 | `recommendation_card.html` L4 eyebrow; not included on sole-runtime `home.html` |
| RP002-NCR-006 | `session_recorded.html` L29 / L38 Kwalitec observe/conclude; mission route sole-runtime redirect |
| RP002-NCR-007 | `dashboard/index.html` L294 Today's Recommendation; `dashboard/routes.py` redirect_if_sole_runtime |

---

## 2. RP-002 audit surface → remediations

| RP-002 audit surface | Pre-status | RR-002.2 action |
|----------------------|------------|-----------------|
| Latent recommendation_card macro | Contained | Guidance eyebrow + Mission/Session empty copy |
| Legacy session feedback narrator | Contained | System / Study Sensei reattribution |
| Legacy dashboard lexicon | Contained | Guidance section + Sensei chrome; empty/attention aligned |
| Open PC-001–004 (RR-002.1) | Closed | Unchanged (regression verified) |
| AR-001–007 | Accepted Residual | **Unchanged** |

---

## 3. Constitutional principles exercised

| Principle | Result |
|-----------|--------|
| **CP-03** One concept → one definition | Guidance chrome unified; Recommendation no longer daily-focus synonym on remediations |
| **CP-04** One primary authority per interaction | Session feedback splits System observation vs Sensei conclusion |
| **CP-10** Sole Study Sensei mentor | Dashboard + session conclusions no longer teach KW-as-mentor |
| **CI-01** Mission ≠ Session ≠ Recommendation | Card/dashboard stop using Today's Recommendation as focus hero |
| **DG-001.1-D02** Mission-led focus | Presentation reinforces Mission/Guidance hierarchy |

---

## 4. Authority conflicts advanced

| RP-002 AC | Pre-status | Post RR-002.2 |
|-----------|------------|---------------|
| RP002-AC-06 Legacy session feedback Kwalitec observer | Contained | **Closed** (System + Sensei labels) |
| RP002-AC-07 Legacy dashboard Recommendation-as-focus | Contained | **Closed** (Guidance chrome) |
| RP002-AC-08 Latent recommendation_card eyebrow | Contained | **Closed** (Guidance eyebrow) |

---

## 5. Explicit non-claims

| Item | Why not claimed |
|------|-----------------|
| Full RP-002 Pass | Accepted Residuals AR-001–007 remain |
| Dual-runtime retirement | Redirect discipline unchanged; chrome safe if dual-run retained |
| Algorithm / ranking / MI behaviour change | Presentation-only WP |
| New educational concepts | Forbidden; lexicon alignment only |

---

**End of RR002_2_TRACEABILITY_MATRIX**
