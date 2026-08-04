# KSI-002 — Risk and Bias Register

**Programme:** KSI-002 — Educational Effectiveness Validation Protocol  
**Version:** 1.0  
**Status:** PROTOCOL COMPLETE — AWAITING FOUNDER REVIEW  
**Effective:** 2026-08-04  
**Authority:** `KSI002_VALIDATION_PROTOCOL.md` · `KSI002_STUDY_DESIGN.md` · `KSI002_PARTICIPANT_PROTOCOL.md` · `KSI002_EVIDENCE_ACCEPTANCE_CRITERIA.md`  

**Registers biases and controls for future validation ops.** Does not measure a live cohort.

---

## 1. Purpose

Name the biases that historically threaten Kwalitec educational claims, and bind **minimum controls** before Gate G1 language is used.

---

## 2. Bias register

### B1 — Selection bias

| Field | Content |
|-------|---------|
| **Risk** | Inviting only highly motivated acquaintances → overstated consistency / usefulness |
| **Control** | Inclusion criteria published; report refusal / non-accept rates; ITT-Accepted denominators; no silent exclusion of inactive |
| **Residual** | Invite-only beta remains selected vs full market — label limitation; no population inference |

### B2 — Confirmation bias

| Field | Content |
|-------|---------|
| **Risk** | Scoring categories to reach KSI 80 after seeing favourable quotes |
| **Control** | Score after locked analysis sets; prefer-lower; Q10 honesty question mandatory; estimated ΔKSI banned from inputs |
| **Residual** | Judgemental KSI scoring always carries subjectivity — G1.7 mitigates |

### B3 — Observer bias

| Field | Content |
|-------|---------|
| **Risk** | Interviewer hears what they hope; codes generously |
| **Control** | Fixed question order; forbidden leading probes; dual coding; interviewer separation from recent implementers |
| **Residual** | Single-Founder ops capacity concentration — document when unavoidable |

### B4 — Survivorship bias

| Field | Content |
|-------|---------|
| **Risk** | Reporting only students who stayed active / completed interviews |
| **Control** | N-flow diagram; drop-off / never-activated / dormant rates; sensitivity with missing interview = not-Yes when claiming GO |
| **Residual** | Interview self-selection among activated — disclose |

### B5 — Novelty bias

| Field | Content |
|-------|---------|
| **Risk** | Week-1 enthusiasm mistaken for effectiveness |
| **Control** | Minimum 4 weeks for Stage 1 advance; 6–8 weeks recommended; 2-week snapshots forbidden for G1.9 PASS; re-invite disclosure |
| **Residual** | First professional-tool exposure may still inflate early weeks — interpret M6 trajectories |

### B6 — Hawthorne effect

| Field | Content |
|-------|---------|
| **Risk** | Students study more because they are observed / interviewed |
| **Control** | Emphasise honest reporting over performance; avoid evaluative tone in check-ins; do not tie continued access to metric greenness |
| **Residual** | Cannot fully eliminate in invite-only pilots — label in limitations |

### B7 — Founder bias

| Field | Content |
|-------|---------|
| **Risk** | Founder walkthrough / dogfood treated as external usefulness; Founder sole Strong-band scorer |
| **Control** | Stage 0 ≠ external N; Founder interviews require second coder for GO; G1.7 independent re-score; constitutional C2/C3/C4 |
| **Residual** | GP-001 capacity concentration — each capacity still needs its own review record |

### B8 — Developer bias

| Field | Content |
|-------|---------|
| **Risk** | Engineers redefine metrics, tune windows, or ship mid-study changes to “help” scores |
| **Control** | Metric definitions frozen to Educational Metrics + this protocol; educational behaviour freeze during claim window; SAP amendment log; no ranking changes under KSI-002 |
| **Residual** | Emergency defect fixes allowed with honesty note |

---

## 3. Additional protocol risks (non-bias)

| ID | Risk | Severity | Control |
|----|------|----------|---------|
| R1 | Privacy Review unsigned → illegal/unethical external measurement | **S1** | No invites until signed |
| R2 | Declaring G1 PASS from protocol publication alone | **S1** | KSI-002 exit = STOP; no G1 claim |
| R3 | Starting KSI-003 ops without Founder accept of protocol | **S2** | Explicit Founder decision record |
| R4 | PII committed to git | **S1** | Pseudonymous IDs only; rejection class R-PII |
| R5 | Marketing freeze breach using observational rates | **S1** | Rates for K2 scoring only; O8 freeze held |
| R6 | Pass-rate claim creep in interview write-ups | **S1** | Non-claims section mandatory |
| R7 | Underpowered Stage 1 over-interpreted | **S2** | SAP power posture; waiver rules |
| R8 | Combining W-GATED lifts into W-PROD board | **S1** | Separate claim windows |
| R9 | EF-001 unfreeze proposed to “fix” effectiveness gap | **S1** | Effectiveness gaps ≠ framework failure; ops first |
| R10 | Treating Content Freeze completion as G1 | **S1** | Claim taxonomy separation |

---

## 4. Severity scale (aligned with EF-001 ops review)

| Level | Meaning |
|-------|---------|
| S1 | Can produce false Version 1 / G1 claims or privacy harm |
| S2 | Can distort scores without immediate declaration fraud |
| S3 | Local noise; document and monitor |

---

## 5. Pre-ops go checklist (bias controls)

Before any future external wave:

- [ ] Privacy Review signed  
- [ ] Protocol + SAP version pinned  
- [ ] Inclusion/exclusion/dropout rules briefed to ops  
- [ ] Interviewer assigned under §B3 controls  
- [ ] Dual-coding plan confirmed if GO path intended  
- [ ] Claim window / flag matrix frozen and written  
- [ ] Non-claims language in participant welcome  

---

## 6. Exit

**STOP.** Register accepted for Founder review. No live bias audit executed in KSI-002.
