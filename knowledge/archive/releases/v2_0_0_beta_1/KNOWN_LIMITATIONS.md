# KNOWN LIMITATIONS — Version 2.0.0-beta.1

**Nature:** Historical record of accepted debt, deferred work, beta assumptions, and operational risks **as known at Private Beta release**.  
**Rule:** No solutions. No redesign proposals. Documentation of boundaries only.

---

## Accepted technical debt

1. **Full-tree Ruff debt** — Large pre-existing lint debt remains; RC-001 cleaned only release-touched modules. Mass auto-fix deferred under feature freeze (RC-001).
2. **Legacy student shells** — `dashboard` / `mission` / `analytics` Contained soak templates and redirects remain in tree alongside sole-runtime EOS.
3. **CMP topic over-production** — EQ-001 recorded CMP raw instructional map still ~936 topics vs syllabus-authoritative 15; residual educational extraction debt.
4. **Multiple historical mission/twin engines** — Parallel application packages (`mission_engine`, `mission_engine_v2`, twin variants, etc.) coexist; certified facade is the beta learning ingress, but older layers remain.

---

## Deferred work

1. Educational quality / mission / tutor intelligence **improvements** explicitly out of RC-001 feature freeze.
2. Full WCAG / Lighthouse lab runs on production (UX-001 residual polish).
3. Mission difficulty chip when domain projection empty (UX-001).
4. Mass Ruff remediation.
5. Persistent disk / durable instance storage proof (DP-003 residual).
6. Commercial expansion, public registration, multi-tenant billing — not part of beta.1.
7. Live cohort Private Beta validation metrics (PB-001 cohort was empty at report time).

---

## Beta assumptions

1. **Invite-only** — No public self-registration; Founder provisions accounts.
2. **Cohort size** — Designed for approximately 10–20 students (`PRIVATE_BETA_GUIDE.md`).
3. **Primary subject** — Closed-beta readiness proven on CS1 Actuarial Statistics (IFoA) certified path.
4. **Sole runtime** — Student EOS is the only student runtime under V2 flags; legacy shells are not the product path.
5. **Feature freeze** — No new educational architecture, AI systems, curriculum reasoning, UI redesign, or commercial expansion in RC-001.
6. **Operator still runs** one live publish + session loop when onboarding the first cohort (RC-001 / Private Beta Guide).

---

## Operational risks

1. **Instance storage durability (DP-003)** — Instance path present on Render; persistent disk not proven; accepted for Private Beta.
2. **Login redirect anomaly** — Login POST briefly reported `405` on `/auth/experience` during redirect chain; session still established in RC-001 smoke — monitor, not treated as deploy blocker.
3. **Deploy cutover** — Brief connection reset during Render swap observed; recovered.
4. **Empty cohort metrics** — PB-001 quality gates for adoption fail by definition until users enrol; do not interpret as platform outage.
5. **Secret / admin env** — Production depends on correctly set `SECRET_KEY`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `DATABASE_URL`; misconfiguration is operator risk outside code freeze.

---

## Items intentionally excluded from this release

1. New educational reasoning / AI agent architectures.
2. Public marketing site redesign as part of RC-001.
3. Open registration / self-serve onboarding funnels.
4. Guaranteed multi-exam catalogue beyond the certified CS1 operational path.
5. Claims of validated learning-outcome efficacy at scale (no cohort evidence yet).
6. Version 1 “production-ready” declaration gates beyond Private Beta packaging (separate frameworks remain).

---

## Future validation work (recorded, not planned here)

1. Enrol 10–20 invitees; collect PB-001 adoption / retention / feedback evidence.
2. Operator live publish → Begin Learning → session completion on production for first cohort.
3. Monitor Tutor / Knowledge Map adoption and mission completion rates against baseline documents in this archive.
4. Watch instance storage and any login redirect anomalies under real traffic.
5. Re-evaluate EQ-001 CMP coherence residuals against live reprocessed packages when educational work resumes.

---

## Source citations (original decisions)

| Limitation cluster | Source |
|---|---|
| Ruff / freeze / storage / 405 | `reports/rc001/RC001_RELEASE_REPORT.md` |
| EQ CMP residual / blocked certification claim | `reports/eq001/EQ001_EDUCATIONAL_QUALITY_REPORT.md` |
| Empty cohort | `reports/pb001/PB001_PRIVATE_BETA_REPORT.md` |
| UX residuals | `reports/ux001/UX001_PREMIUM_BETA_REPORT.md` |
| Pre-RR active catalogue noise | `reports/supporting/PL001A_LIVE_DOGFOOD_REPORT.md` |

---

*AR-001 known limitations — historical record only.*
