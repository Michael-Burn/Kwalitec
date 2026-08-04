# KSI-002 — Participant Protocol

**Programme:** KSI-002 — Educational Effectiveness Validation Protocol  
**Version:** 1.0  
**Status:** PROTOCOL COMPLETE — AWAITING FOUNDER REVIEW  
**Effective:** 2026-08-04  
**Authority:** `KSI002_VALIDATION_PROTOCOL.md` · `KSI002_STUDY_DESIGN.md` · `PRIVATE_BETA_PROTOCOL.md` · EP-007.3 `COHORT_DESIGN.md`  

**Defines participant and interview rules only.** Does not recruit or interview anyone.

---

## 1. Sample size parameters

| Parameter | Value |
|-----------|------:|
| **Minimum sample** (Stage 1 accepted external) | **5** |
| **Target sample** (Stage 1) | **5–10** |
| **Product-decision floor** (Stage 2 active, ≥4 weeks) | **20** |
| **Maximum sample** (accepted concurrent under this protocol) | **50** |
| Interview minimum (GO path) | **≥8** or **≥25%** of active (see Study Design) |

---

## 2. Inclusion criteria

A person may count toward **external** N only if **all** hold:

1. Preparing for an **in-scope** professional exam subject loadable on V1/V2 curricula (priority subjects per ops plan; historically CM2/CS2 in EP-007.3).  
2. **Invite-only** account; no public self-registration.  
3. **Signed / recorded** privacy notice acknowledgement and **measurement consent** before KPI inclusion.  
4. Not acting solely as staff dogfood (see §4).  
5. Agrees to closed-beta expectations (bugs possible; no pass guarantee in welcome copy).  
6. Privacy Review for the study wave is **signed** before invite send.

---

## 3. Exclusion criteria

Exclude from external N (may still receive support access at Founder discretion):

1. Cannot consent to privacy / measurement terms.  
2. Recommendation A/B or other interventional ranking-trial assignment (out of protocol).  
3. Accounts created for automated tests / personas only.  
4. Duplicate accounts (see §7).  
5. Failed registrations that never reached invite-accepted state (see §6).  

---

## 4. Repeat participants and staff

| Case | Rule |
|------|------|
| **Staff / Founder dogfood** | Stage 0 only; **never** in external denominators unless explicitly dual-marked — still labelled **internal** for G1.9 |
| **Repeat external** (re-invited after prior wave) | Allowed if prior wave ended; personal start resets; disclose prior exposure (novelty bias control) |
| **Concurrent Tier B + Stage 1** | Same person may contribute perception and behavioural evidence; label dual-role; do not double-count N without disclosure |

---

## 5. Inactive students

| Definition | Spec |
|------------|------|
| **Inactive (week)** | Accepted participant with **zero** productive Session completions in the ISO week |
| **Never-activated** | Accepted but no productive Session within **7 days** of acceptance (onboarding fail) |
| **Dormant** | Activated earlier but **≥14 days** with no productive Session |

**Reporting:** Always report inactive / never-activated / dormant counts in ITT-Accepted. Do not drop them silently to inflate M6.

**Dropout vs inactive:** Inactivity alone ≠ dropout until dropout rules trigger.

---

## 6. Failed registrations

| State | Definition | Counts toward external N? |
|-------|------------|---------------------------|
| Invite sent, not accepted | No acceptance timestamp | **No** |
| Acceptance incomplete (account provision failed) | Ops failure | **No** — log as ops defect |
| Accepted then immediate withdrawal of consent | Accepted then excluded from KPIs | **No** for numerators; footnote in flow diagram |

---

## 7. Duplicate accounts

| Rule | Spec |
|------|------|
| Detection | Same email (normalised), or ops-confirmed same person with multiple user_ids |
| Action | Keep earliest accepted ID unless Founder designates otherwise; merge behavioural events under retained ID for analysis; mark others `duplicate_excluded` |
| Evidence | Pseudonymous note in exclusions log — **no** raw emails in git |

---

## 8. Dropout rules

A participant is **dropped** from Active-Evaluable when **any** hold:

1. Measurement consent withdrawn.  
2. Account closed / banned for ToS.  
3. Explicit study withdrawal.  
4. Ops-confirmed duplicate (non-retained ID).  

**Do not** drop solely for low activity — classify as inactive / dormant and retain in ITT honesty metrics.

**Censoring:** For longitudinal means, censor at dropout date; do not impute post-dropout completions.

---

## 9. Consent layers

| Layer | Required for |
|-------|----------------|
| Privacy notice ack | Any external invite acceptance |
| Measurement consent | Inclusion in M1–M9 and effectiveness board |
| Interview consent | Structured interview participation |
| Quote consent | Publishable anonymous quotes |

Decline of interview/quote **must not** remove study access.

---

## 10. ID scheme

Use pseudonymous IDs only in knowledge artefacts (e.g. `BETA-PIL-###` or wave-specific prefix). PII stays in approved ops stores outside git.

---

## 11. Structured interview protocol

### 11.1 Timing and length

- Schedule from **week 4** of personal start (earlier only for exit interviews on withdrawal).  
- Duration: **~30 minutes**.  
- Mode: call or equivalent; record only with explicit consent (recording optional).

### 11.2 Question order (fixed)

Ask in this order. Do not reorder to chase favourable themes.

| # | Neutral stem | Maps to |
|---|--------------|---------|
| Q1 | “Walk me through how you decided what to study in your last few sessions.” | K1 |
| Q2 | “When the product suggested a next action, what did you do, and why?” | K2 |
| Q3 | “How do you tell whether you are prepared enough in a topic? What do you look at?” | K3 |
| Q4 | “Does the plan feel like it fits *your* situation? What would make it more or less so?” | K4 |
| Q5 | “After a missed study day, what happened next?” | K5 |
| Q6 | “Can you explain your progress in one sentence? What helped you see that?” | K6 |
| Q7 | “If you revised, did that change what you practised afterwards?” | K7 |
| Q8 | “Did you understand *why* the product guided you that way? What was unclear?” | K8 |
| Q9 | “Over these weeks, has Kwalitec helped you study like a professional preparing for an exam?” (Final Test) | Effectiveness / usefulness |
| Q10 | “What should we **not** claim about the product based on your experience?” | Honesty / G1.8 |

### 11.3 Approved probes (only)

- “Can you give a concrete example from a specific day?”  
- “What did you see on screen when that happened?”  
- “Was that helpful, unhelpful, or unclear — and what makes you say that?”  
- “Anything else on this question before we move on?”  

### 11.4 Forbidden interviewer behaviours

- Leading: “So you’d say it’s really useful, right?”  
- Selling Premium / pass-rate / marketing claims  
- Defending engineering decisions mid-interview  
- Coaching the “correct” educational framework answer  
- Skipping Q10  
- Offering incentives contingent on positive answers  

### 11.5 Interviewer restrictions

- Prefer interviewer who did **not** implement the primary surface under test in the last 30 days.  
- If Founder interviews, second coder mandatory for theme extraction when claiming GO.  
- No live score changes to validated KSI during the call.

### 11.6 Coding methodology

1. Use codebook axes: K1–K8 valence (Positive / Mixed / Negative / Unclear), M-linked behaviour mentions, Final Test (Yes / Partial / No), Honesty caution flags.  
2. Primary coder codes within 5 business days.  
3. Second coder independently codes ≥20% (all if N_interviews ≤10).  
4. Resolve disagreements by discussion; if unresolved, code **Mixed/Unclear** and apply prefer-lower in scoring.  

### 11.7 Theme extraction

- Themes require ≥2 independent interviews **or** 1 interview + corroborating behavioural metric.  
- Single vivid quote ≠ portfolio theme.  
- Negative themes cannot be dropped from the Evidence Register.

### 11.8 Inter-rater agreement

| Metric | Rule |
|--------|------|
| Report | % agreement on Final Test + Cohen’s κ on K-category valence when second coding exists |
| Threshold | κ &lt; 0.40 → do not claim High confidence on qualitative lifts; remediate codebook |
| Archive | Coded sheets under evidence programme folder (pseudonymous) |

---

## 12. Participant communications

Welcome and check-ins follow Private Beta Protocol tone: companion for learning; **no** pass guarantees; bugs expected; educational honesty preferred.

---

## 13. Exit

**STOP.** No recruitment under KSI-002. Await Founder review + Privacy sign-off before any future ops programme invites.
