# G1 Founder Validation Protocol

**Programme:** RC-003 — Production Cutover & G1 Launch  
**Protocol version:** 1.0  
**Release tag:** `v1.0.0-G1`  
**Environment:** Production — https://kwalitec.onrender.com  
**Authority:** RF-001 PASS · BF-001 PASS · RF-001A GO WITH ACCEPTED DEBT · SB-001A PASS · RF-002 GO FOR G1 · RC-003 cutover

---

## Purpose

G1 is **Founder Validation** of the educational system in live production after RC-003 cutover.

During G1, the Founder uses Kwalitec as a primary daily study system and collects observations about educational continuity, trust, and operational reliability.

G1 is **not** an engineering redesign window.

---

## Governing rule (mandatory)

> **During G1, observations are collected.**  
> **Engineering changes are NOT made unless a verified Category A defect is discovered.**

Accepted debt from RF-001A / RF-002 remains accepted. Do not open feature programmes, Runtime redesigns, or pytest-zero campaigns as a substitute for G1 evidence.

---

## Founder Validation duration

| Item | Value |
|------|-------|
| Start | Immediately after RC-003 production equivalence is confirmed |
| Minimum duration | **7 consecutive calendar days** of Founder use |
| Preferred duration | **14 consecutive calendar days** (two study weeks) |
| Cadence | At least one authentic study sitting per validation day |

A day counts when the Founder completes Login → educational work → Logout (or equivalent continuous session) without abandoning due to a Category A defect.

---

## Daily validation checklist

Complete once per validation day. Mark Pass / Fail / N/A.

### Access

- [ ] Login succeeds
- [ ] Home / Adaptive Workspace loads without crash
- [ ] Logout succeeds; subsequent protected routes gate to login

### Educational path (Student)

- [ ] Exam / subject selection available when needed
- [ ] Availability / scheduling step behaves as expected
- [ ] **Baseline** reachable (not Calibration theatre; not 404)
- [ ] After Baseline (or with existing Baseline), Twin / Runtime entry continues without a second intake
- [ ] Today's Mission visible when a plan is active
- [ ] Study Session starts
- [ ] Reflection / sitting completion path works
- [ ] History / Journey retained after logout and return

### Founder surfaces (as needed)

- [ ] Curriculum Studio opens
- [ ] Expand All / Collapse All behave correctly on large trees
- [ ] Publish / Archive / version assignment remain operable
- [ ] Participant Baseline inspect / reset (if used) does not annihilate learning history

### Operational

- [ ] No unexpected redirects on the primary path
- [ ] No missing static assets (CSS/JS)
- [ ] No console errors that block study
- [ ] `/health` remains `status: ok` if spot-checked

---

## Educational observations

Record in free text (or a dated log under `knowledge/evidence/releases/G1/`):

1. Does Baseline feel like a tutor intake (not a form wall)?
2. After Baseline, does Home / Mission feel continuous with what was declared?
3. After leaving mid-session and returning, does the platform still feel like it remembers?
4. Do missions feel singular (no duplicate educational state)?
5. Does Founder Baseline inspect/reset feel safe?

Do **not** redesign Runtime A, Runtime C, SCI, recommendations, Study Plans, or the Digital Twin in response to preference feedback during G1. Log preferences as observations.

---

## Operational observations

Log:

- Deploy / health incidents
- Migration or startup warnings
- Auth failures
- Asset cache issues (hard-refresh once; note fingerprint)
- Latency or blank screens on primary paths

---

## Known accepted debt (do not treat as new defects)

Carried from RF-001A / RF-002:

| Item | Status |
|------|--------|
| Thin Runtime C SCI seed (no Baseline→SCI overrides) | Accepted |
| Runtime C Twin birth may honestly skip | Disclose; monitor TwinAbsent |
| Narrow Baseline gate (Home-centric) | Accept for G1 |
| Session finish → Sitting Report test drift | RF-001A Category D |
| Full-tree pytest residual (~159) | RF-001A accepted debt |
| No dedicated per-student Twin viewer | Inspect via Baseline `twin_snapshot_id` |
| Public `/health/details` | Prior accepted ops posture |
| Legacy Founder Bootstrap islands / presentation polish | PX debt |

---

## Rules for logging issues

1. **Observe first.** Write date, path, expected vs actual, screenshot or URL if useful.
2. **Reproduce once** before elevating severity.
3. **Classify** using the severity definitions below.
4. **Do not patch** Category B/C/D or accepted debt during G1.
5. **Category A only** may interrupt G1 for a hot-fix, and only after verification that the defect is new vs accepted debt and blocks primary Founder/Student study.

Issue log path (recommended): `knowledge/evidence/releases/G1/issues/` with one file per issue (`YYYYMMDD-short-slug.md`).

---

## Severity definitions

| Severity | Definition | G1 response |
|----------|------------|-------------|
| **Category A** | Blocks primary educational path (cannot login, cannot start/continue study, data loss of learning history, Baseline unreachable in production, Runtime entry crash, Studio Expand/Collapse hard-broken when authoring is required for that day's study) | Verify → hot-fix only; document; resume G1 clock after fix |
| **Category B** | Degraded but workaround exists; educational continuity intact | Log; do not engineer during G1 |
| **Category C** | Cosmetic / polish / copy / non-blocking UI | Log; defer |
| **Category D** | Test/fixture/tooling drift not visible in Founder path | Ignore for G1 product judgment |

---

## Success criteria

G1 succeeds when **all** of the following hold:

1. Minimum duration completed (≥7 consecutive validation days; prefer 14).
2. Primary Student path remains usable each day without Category A interruption (or after Category A hot-fix, consecutive days resume to target).
3. Baseline remains reachable; Calibration does not reintroduce a second intake theatre on the primary path.
4. Twin / Runtime A entry and Runtime C bridge continue without duplicate educational state.
5. Study Plan and Mission generation remain operational for the Founder's subject.
6. History retained across sessions.
7. No unresolved Category A defects open at exit.
8. Observations and issue log filed under `knowledge/evidence/releases/G1/`.

---

## Exit criteria

| Outcome | When |
|---------|------|
| **G1 PASS** | Success criteria met; Founder judges daily study educationally coherent |
| **G1 PASS WITH OBSERVATIONS** | Success criteria met; Category B/C observations logged for later programmes |
| **G1 HOLD** | Category A verified and not yet hot-fixed; validation clock paused |
| **G1 FAIL** | Repeated Category A on primary path after cutover verification, or educational discontinuity (memory/origin) contradicts RF-002 claims in live use |

Exit does **not** require full-tree pytest zero, Runtime redesign, or SCI expansion.

---

## Relationship to product frameworks

- Educational GO authority: RF-002 recommendation (candidate equivalence post RC-003).
- Product Success / KSI and Version 1 Release Framework gates (G1–G12) remain separate; G1 Founder Validation collects evidence toward those frameworks but does not declare Version 1 production-ready by itself.

---

## Quick reference

| Do | Do not |
|----|--------|
| Study daily and log observations | Redesign Runtime A/C, SCI, Twin, Study Plans |
| Hot-fix verified Category A only | Opportunistic refactors or debt cleanups |
| Confirm production matches RF-002 candidate | Claim live Baseline continuity on pre-cutover tip |
| File evidence under `knowledge/evidence/releases/G1/` | Open engineering programmes to “improve” G1 mid-flight |
