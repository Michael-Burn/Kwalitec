# P-002.1 — Residual Register

**Programme:** P-002.1 — Version 1 Release Readiness Validation  
**Date:** 2026-08-04  
**Rule:** Residuals are Board/Founder-owned until closed. Ideas must not silently become Version 1 scope.

---

## 1. Blocking residuals (declaration)

| ID | Gate | Severity | Item | Owner | Notes |
|----|------|----------|------|-------|-------|
| P0021-B1 | G1.1 | Hard | Validated KSI ≥ 80 (current **64**) | Product | EP-008.1B board |
| P0021-B2 | G1.9 | Hard | Educational effectiveness NO-GO / PENDING EVIDENCE | Product + Educational | EP-007.3; Stage 1 ops blocked |
| P0021-B3 | G1.7 | Formality | Independent re-score ±3 | Product | Second assessor not filed |

---

## 2. Evidence / ops residuals (carry from PX-007)

| ID | Severity | Item | Owner | Prior |
|----|----------|------|-------|-------|
| P0021-R1 | S3 | Founder PNG screenshot gallery | Founder | PX7-R1 |
| P0021-R2 | S2 | Live phone + tablet gallery | Founder + PX | PX7-R2 |
| P0021-R3 | S3 | axe/Lighthouse CI | Engineering | PX7-R3 |
| P0021-R4 | S3 | VoiceOver/NVDA recording | Engineering + PX | PX7-R4 |
| P0021-R5 | S3 | LIVE Core Web Vitals | Engineering + Ops | PX7-R5 · G7 HOLD |
| P0021-R6 | S3 | LIVE Continue contention re-measure | Engineering + Ops | PX7-R6 |
| P0021-R7 | S2–S3 | Prior provisional decisions ratification | Founder | PX7-R10 |
| P0021-R8 | S3 | Optional live restore drill | Ops | G8 residual |
| P0021-R9 | S2 | Privacy Review signatures (Stage 1) | Privacy + Product | G10 · G1.9 dependency |
| P0021-R10 | S3 | G3.4 / G5.3 / G6 declaration spot-check packs | Product | Gate residuals |
| P0021-R11 | S3 | Recommendation scorecard precision sample | Product | G4.4 |
| P0021-R12 | S3 | EVF APPROVED memo for V1 claim class | Educational Gate | G2 residual |

---

## 3. Stale-test residuals (not product Critical/Major)

| ID | Severity | Item | Disposition |
|----|----------|------|-------------|
| P0021-T1 | Minor (test) | `test_finish_returns_home` expects Home; finish → session summary | Update test in follow-on hygiene — **not** Version 1 product work |
| P0021-T2 | Minor (test) | Alpha onboarding expects “Meet Study Sensei” | Update test to Private Beta copy |
| P0021-T3 | Minor (test) | Alpha telemetry allowlist vs expanded catalogue | Align test with EVENT_CATALOGUE; analytics OFF |

---

## 4. Version 1.1 backlog (Ideas — not Version 1)

- Account-durable daily study goal  
- Unified settings hub migration  
- Full icon library (`PX-B-051`)  
- Self-service password reset  
- Dual settings chrome cleanup (PX7-003)  
- Focus control hide-until-JS (PX7-007)  
- Optional bottom-nav only via Board amendment  

---

## 5. Explicitly out of programme / not claimed

- Version 1 production-ready declaration  
- Until-exam educational trust  
- Exam pass-rate proof  
- WCAG conformance level  
- High-traffic marketing under G7 HOLD  
- Live analytics KPIs while flag OFF  
- Wave 16 educational production  

---

## 6. Closed this programme

| Item | Disposition |
|------|-------------|
| G1–G12 evaluation with evidence | Closed (scored) |
| LIVE health fingerprint on tip | Closed (filed) |
| Premium / quality / curriculum regression packs | Closed (green) |
| Educational Content Freeze verification | Closed (held) |
| Founder walkthrough re-run | Closed (Critical 0 · Major 0) |

Signed: P-002.1 Residual Register · 2026-08-04
