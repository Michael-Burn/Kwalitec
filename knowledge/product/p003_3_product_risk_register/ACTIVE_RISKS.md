# Active Risks

**Programme:** P-003.3 — Product Risk Register  
**Date:** 2026-07-26  
**Status:** ACTIVE index  
**Canonical cards:** [`PRODUCT_RISK_REGISTER.md`](PRODUCT_RISK_REGISTER.md)

This index lists every product risk that remains material to Version 1 release success. Posture: freeze at 2026-07-26 evidence (aligned with P-003.1 / P-003.2).

**Board question answered here:** *What risks remain, how serious are they, and what must happen before they close?*

---

## Board reading order (15 minutes)

1. **PR-001 → PR-002 → PR-003 → PR-006** (why Version 1 cannot be declared)  
2. **PR-004 → PR-019** (declaration pressure + incomplete gate package)  
3. **PR-012 → PR-016** (flags / claim honesty)  
4. **PR-007 → PR-017** (ops chain: privacy → recruitment → onboarding)  
5. Skim **WATCH / ACCEPTED** only if proposing flag ON or public launch  

---

## By Overall Rating

### Red (must clear or explicitly HOLD before Version 1 declaration)

| ID | Title | Category | Status | Likelihood | Impact | Owner |
|---|---|---|---|---|---|---|
| [PR-001](PRODUCT_RISK_REGISTER.md#pr-001--educational-effectiveness-unproven-while-product-may-be-described-as-ready) | Educational effectiveness unproven | Educational · Evidence | ACTIVE | High | Critical | Product Board |
| [PR-002](PRODUCT_RISK_REGISTER.md#pr-002--validated-ksi-below-version-1-bar-62--80) | Validated KSI 62 &lt; 80 | Release · Evidence | ACTIVE | Very High | Critical | Product |
| [PR-003](PRODUCT_RISK_REGISTER.md#pr-003--privacy-review-unsigned-blocks-stage-1-expansion) | Privacy Review unsigned | Privacy · Release | ACTIVE | High | High | Product + Privacy |
| [PR-006](PRODUCT_RISK_REGISTER.md#pr-006--external-cohort-unavailable-evidence-floors-unmet) | External cohort unavailable / floors unmet | Evidence · Adoption | ACTIVE | High | High | Product (beta ops) |
| [PR-007](PRODUCT_RISK_REGISTER.md#pr-007--stage-1--stage-2-recruitment-blocked-on-privacy-not-a-recruitment-failure) | Stage 1/2 recruitment blocked on privacy | Adoption · Privacy | ACTIVE | High | High | Product (beta ops) |
| [PR-008](PRODUCT_RISK_REGISTER.md#pr-008--confidence-medium-ceiling-without-external-corroboration) | Confidence Medium ceiling | Evidence | ACTIVE | High | Medium | Product (Validation) |
| [PR-009](PRODUCT_RISK_REGISTER.md#pr-009--independent-ksi-re-score-g17-unfinished) | Independent KSI re-score (G1.7) HOLD | Evidence · Governance | ACTIVE | Very High | Medium | Product Board |
| [PR-019](PRODUCT_RISK_REGISTER.md#pr-019--release-gate-package-incompleteness-g2g12-residuals) | Release gate package incompleteness | Release · Governance | ACTIVE | High | High | Product Board |
| [PR-020](PRODUCT_RISK_REGISTER.md#pr-020--constitutional--evf-compliance-not-approved-for-v1-claim-class-g2) | G2 EVF/constitutional not APPROVED | Governance · Release | ACTIVE | Medium | High | Product Board |

### Amber (material; controlled or residual)

| ID | Title | Category | Status | Likelihood | Impact | Owner |
|---|---|---|---|---|---|---|
| [PR-004](PRODUCT_RISK_REGISTER.md#pr-004--premature-version-1-production-ready-declaration) | Premature V1 declaration pressure | Release · Governance | ACTIVE (controlled) | Medium→Low* | Critical | Product Board |
| [PR-005](PRODUCT_RISK_REGISTER.md#pr-005--cold-start--sparse-evidence-overconfidence) | Cold-start / sparse-evidence overconfidence | Educational · Product | ACTIVE | Medium | Medium | Product |
| [PR-010](PRODUCT_RISK_REGISTER.md#pr-010--production-load--performance-claims-unverified) | Production load test not started | Operational · Technical | ACTIVE | Medium | Medium | Engineering |
| [PR-011](PRODUCT_RISK_REGISTER.md#pr-011--telemetry--journey-emit-overclaim-while-gated-off) | Telemetry overclaim while gated OFF | Operational · Governance | ACTIVE (controlled) | Medium | Medium | Product + Analytics |
| [PR-012](PRODUCT_RISK_REGISTER.md#pr-012--feature-flag-matrix--rollback-unreadiness-for-on-defaults-g12) | Feature-flag / rollback unreadiness (G12) | Deployment · Release | ACTIVE | Medium | Medium | Engineering + Product |
| [PR-013](PRODUCT_RISK_REGISTER.md#pr-013--rollback-drill--reliability-packaging-incomplete-g8) | Rollback drill / G8 packaging incomplete | Deployment · Operational | ACTIVE | Medium | Medium | Engineering |
| [PR-014](PRODUCT_RISK_REGISTER.md#pr-014--deployment--release-execution-vs-declaration-confusion) | Ship ≠ declare confusion | Release · Governance | ACTIVE (controlled) | Medium | Medium | Product Board |
| [PR-015](PRODUCT_RISK_REGISTER.md#pr-015--support--commercial-unreadiness-for-public-launch) | Support / commercial unreadiness | Operational · Adoption | ACCEPTED | High if public | Medium | Product + Founder |
| [PR-016](PRODUCT_RISK_REGISTER.md#pr-016--personalisation--twin-capabilities-marketed-while-flags-off) | Personalisation/Twin marketed while OFF | Governance · Product | ACTIVE (controlled) | Medium | High | Product |
| [PR-017](PRODUCT_RISK_REGISTER.md#pr-017--sparse-onboarding--orientation-content) | Sparse onboarding / orientation | Adoption · Educational | ACTIVE | Medium | Medium | Product |
| [PR-018](PRODUCT_RISK_REGISTER.md#pr-018--coach--session-naming-and-twin-trust-perception) | Coach/Session naming & Twin trust | Educational · Adoption | WATCH | Medium | Medium | Product |
| [PR-021](PRODUCT_RISK_REGISTER.md#pr-021--documentation-drift-between-companion-release-artefacts) | Documentation drift | Governance · Evidence | ACTIVE | Medium | Low–Medium | Product (docs) |
| [PR-022](PRODUCT_RISK_REGISTER.md#pr-022--shadow-constitution--constitutional-bypass-pressure-governance-drift) | Shadow constitution / bypass pressure | Governance | WATCH | Low–Medium | High | Product Board |
| [PR-023](PRODUCT_RISK_REGISTER.md#pr-023--security-csp--dependency-residuals-g10) | Security CSP / G10 residuals | Technical · Privacy | ACTIVE | Low–Medium | Medium | Engineering |
| [PR-024](PRODUCT_RISK_REGISTER.md#pr-024--pass-rate-vision-north-star-measurement-methodology-undefined) | Pass-rate methodology undefined | Evidence · Educational | ACTIVE | High for Vision claims | High / Medium† | Product |
| [PR-025](PRODUCT_RISK_REGISTER.md#pr-025--second--opaque-educational-brain-creep) | Second educational brain creep | Educational · Technical | WATCH | Low–Medium | Critical | Architecture + Product |
| [PR-026](PRODUCT_RISK_REGISTER.md#pr-026--process-local-state-loss-on-restart-profile--metrics) | Process-local state loss | Technical · Operational | ACCEPTED | High | Low | Engineering |
| [PR-027](PRODUCT_RISK_REGISTER.md#pr-027--concentration-of-duties-under-founder-operation) | Founder capacity concentration | Governance · Operational | ACCEPTED | Very High | Medium | Founder (Chair) |

\* Likelihood reduced while NO GO held.  
† Impact High for Vision pass-rate claims; Medium for KSI-only V1 declaration scope.

---

## By category

| Category | Risk IDs |
|---|---|
| Educational | PR-001, PR-005, PR-017, PR-018, PR-024, PR-025 |
| Operational | PR-010, PR-011, PR-013, PR-015, PR-026, PR-027 |
| Release | PR-002, PR-003, PR-004, PR-012, PR-014, PR-019, PR-020 |
| Governance | PR-004, PR-009, PR-011, PR-014, PR-016, PR-019, PR-021, PR-022, PR-027 |
| Evidence | PR-001, PR-002, PR-006, PR-008, PR-009, PR-021, PR-024 |
| Privacy | PR-003, PR-007, PR-023 |
| Technical | PR-010, PR-023, PR-025, PR-026 |
| Product | PR-005, PR-016 |
| Adoption | PR-006, PR-007, PR-015, PR-017, PR-018 |
| Deployment | PR-012, PR-013 |

---

## Closure checklist (declaration-critical)

Before Version 1 production-ready declaration, at minimum clear or HOLD under P-002.1:

| Must address | Risk IDs |
|---|---|
| Effectiveness not NO-GO (G1.9) | PR-001, PR-006, PR-007 (via PR-003) |
| Validated KSI ≥ 80 (G1.1) | PR-002 |
| Privacy signatures for Stage 1 | PR-003 |
| G1.7 second score | PR-009 |
| Gate package G2–G12 | PR-019, PR-012, PR-013, PR-020, PR-010, PR-023 |
| Claim honesty (OFF flags) | PR-016, PR-011 |
| No premature declare | PR-004, PR-014 |

Closed / fixed items: [`CLOSED_RISKS.md`](CLOSED_RISKS.md).

---

## Counts

| Set | Count |
|---|---:|
| Total registered (PR-001…PR-027) | 27 |
| Red Overall | 9 |
| Amber Overall (incl. controlled / watch / accepted) | 18 |
| Green Overall as current operating posture | 0 as primary rating (PR-015/PR-026 note Green *under invite-only / OFF flags*) |
