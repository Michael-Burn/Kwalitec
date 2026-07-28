# Governance Compliance Scorecard

**Programme:** EGC-001 — Educational Governance Compliance  
**Version:** 1.0  
**Status:** Active — Board compliance baseline  
**Score date:** 2026-07-28  
**Authority:** `EDUCATIONAL_GOVERNANCE_COMPLIANCE_AUDIT.md`  
**Constraint:** Scoring only — no product changes.

---

## 1. Overall product certification

| Field | Value |
|-------|-------|
| **Overall classification** | **NON-COMPLIANT** |
| **Meaning** | Alpha does not yet satisfy DG-001 as a coherent student-facing educational system. Compliant pockets exist. |
| **Programme EGC-001** | **Complete** — baseline measurable; remediation traceable |
| **Unqualified “educationally governed Alpha” claim** | **Forbidden** until P0 NCR items close with implementation evidence |

---

## 2. Compliance statistics

### 2.1 By capability (primary status)

Primary status = overall row for that capability in the Audit.

| Classification | Count | Share |
|----------------|------:|------:|
| Fully Compliant (FC) | 5 | 18% |
| Partially Compliant (PC) | 12 | 43% |
| Non-Compliant (NC) | 10 | 36% |
| Not Applicable (NA) | 1 | 4% |
| **Total capabilities scored** | **28** | 100% |

Capabilities counted: Authentication, Onboarding, Home, Mission Intelligence, Mission Commitment, Study Session, Decision Journal, Educational Timeline, Feedback Loop, Revision, History, Calibration, Help, Notifications, Settings, Success states, Empty states, Error states, Feature flag messaging, Educational copy, Educational explanations, Reflection flows, Narrator transitions, Authority ownership, Educational terminology, Educational memory, Product Check-in — and Notifications treated as NA/watch (counted NA).

*Note:* Notifications = NA; Feature flag = PC (contained). Educational memory = PC.

### 2.2 Non-Compliance Register

| Class in register | Count |
|-------------------|------:|
| NC findings | 12 |
| PC findings (material) | 10 |
| Contained / watch (subset) | 1+ (NCR-014) |
| **Total NCR rows** | **22** |

### 2.3 By priority (open remediation)

| Priority | NCR count (approx) | Intent |
|----------|-------------------:|--------|
| P0 | 12 | Must precede “governed Alpha” claims |
| P1 | 8 | Next remediation wave |
| P2 | 2 | Disclosure / polish |
| P3 | Preventive (EGC-R11) | When notifications educationalise |

### 2.4 Constitutional principles (CP-01–CP-10)

| Status | Count |
|--------|------:|
| FC | 1 (CP-02 process for EGC-001) |
| PC | 5 |
| NC | 4 |

### 2.5 Supporting invariants (CI-01–CI-06)

| Status | Count |
|--------|------:|
| FC | 2 (CI-02 host; CI-04 audited paths) |
| PC | 2 |
| NC | 2 (CI-01; CI-05) |

---

## 3. Compliance by governance package

| Package | Instrument | Product posture | Headline |
|---------|------------|-----------------|----------|
| **DG-001.1** Lexicon | Canonical lexicon + DEP + map + style | **Non-Compliant application** | Law complete; tip/Session/Mission storm live |
| **DG-001.2** Authority | Authority model + transitions + matrix + AC register | **Non-Compliant application** | Three authorities in law; dual narrator + missing handoff live |
| **DG-001.3** Reflection | Architecture + lifecycle + relationships + RG rules | **Non-Compliant as student system** | Hosts/optionality partially good; map missing; Check-in misnamed |
| **DG-001.4** Constitution | CP/CI, hierarchy, amendment, checklist | **Process Compliant for EGC-001** | Product fails CP-03/04/05/10; checklist usable |

### Package score bars (qualitative)

```
DG-001.1 application   ████░░░░░░  ~35%  (Journal/Timeline terms partial; tip fails)
DG-001.2 application   ███░░░░░░░  ~30%  (memory SS good; orientation KW fails)
DG-001.3 application   ████░░░░░░  ~40%  (optionality/honesty; map/Check-in fail)
DG-001.4 process (EGC) ██████████  100%  (audit precedes remediation)
```

Percentages are **illustrative Board scorecard signals**, not KSI substitutes.

---

## 4. Fully Compliant pockets (preserve)

Do not break these while remediating:

| Pocket | Why FC |
|--------|--------|
| Authentication as Kwalitec product speech | D02 |
| Settings / About as product | D02 |
| Calibration as declaration not reflection | D05 |
| Error / mechanical unavailable as System/product | D03 |
| Decision Journal as sole durable Sensei memory **host** | D02 / CI-02 |
| Decision Journal Sensei eyebrow + non-shame honesty | D01; CP-07 |
| Guided Reflection preview honesty disclaimer | RG-01; ED-09 mitigated |
| Session reflection optional note | RG-02 |
| Sensei reflection optional / no re-rank (architecture) | D06; CI-04 |
| Revision ack not sold as Revision Reflection capture | D05 companion |

---

## 5. Critical findings (Board attention)

1. **Missing Study Sensei handoff** (NCR-001 / NCR-018) — CI-05 / D04  
2. **Tip / Mission / Session noun storm** (NCR-015 / NCR-020) — CI-01 / D02  
3. **Help omits Sensei memory surfaces** (NCR-011 / NCR-021) — D04 / ED-04  
4. **Reflection not one student system** (NCR-017) — CP-05 / ED-03  
5. **Product Check-in titled Reflection** (NCR-022) — D05 / §11.5  
6. **Runtime C System-as-mentor if enabled** (NCR-014) — D07 / DEP-04  

---

## 6. Dimension heat map (capabilities × dimensions)

Legend: F = FC · P = PC · N = NC · — = NA

| Capability | Lex | Auth | Refl | Const | Expl | Honest | Judge | Trust | Narr | Evid |
|------------|:---:|:----:|:----:|:-----:|:----:|:------:|:-----:|:-----:|:----:|:----:|
| Authentication | F | F | — | F | — | F | — | F | F | F |
| Onboarding | N | N | N | N | N | N | P | N | N | F |
| Home | P | P | P | P | P | P | P | P | P | F |
| Mission Intelligence | P | P | — | P | P | P | P | P | P | F |
| Mission Commitment | P | P | P | P | P | P | P | P | P | F |
| Study Session | P | P | F | P | P | P | P | P | P | F |
| Decision Journal | P | F | F | P | F | P | F | F | F | F |
| Educational Timeline | P | P | P | P | P | P | P | P | F | F |
| Feedback Loop | P | F | F | P | F | F | F | F | F | F |
| Revision | P | P | F | P | P | P | P | P | P | P |
| History | P | N | — | N | P | N | P | P | N | F |
| Calibration | F | F | F | F | F | F | — | F | F | F |
| Help | N | N | N | N | P | N | N | N | N | F |
| Notifications | — | — | — | — | — | — | — | — | — | P |
| Settings | F | F | — | F | — | F | — | F | F | F |
| Success states | P | P | — | P | P | P | P | P | P | F |
| Empty states | P | P | P | P | P | P | P | P | P | F |
| Error states | F | F | — | F | — | F | — | F | F | F |
| Feature flags | P | P | P | P | P | P | — | P | P | F |
| Educational copy | N | N | — | N | N | N | P | N | N | F |
| Explanations | N | P | — | N | P | P | P | P | N | F |
| Reflection flows | N | P | N | N | P | P | P | P | P | F |
| Narrator transitions | N | N | — | N | — | N | — | N | N | F |
| Authority ownership | N | N | P | N | P | N | P | N | N | F |
| Terminology | N | N | — | N | N | N | P | N | N | F |
| Educational memory | P | P | F | P | P | P | F | P | P | F |
| Product Check-in | N | F | N | N | P | N | — | N | P | F |

---

## 7. Remediation sequencing (recommended)

```
Wave 0 (governance already done)     DG-001.1–4  ✓
Wave 1 (P0 trust + vocabulary)       EGC-R01 → R02 → R03 → R04 → R05
Wave 2 (epistemology + honesty)      EGC-R06 → R08 → R12 → R10
Wave 3 (containment / thin surfaces) EGC-R07 (before flags) → R09 → R11
```

No wave may invent a fourth narrator or second durable Sensei memory.

---

## 8. Scorecard decision

| Claim | Allowed after EGC-001? |
|-------|------------------------|
| “DG-001 law exists” | Yes |
| “Product compliance baseline certified” | Yes — **NON-COMPLIANT** |
| “Alpha complies with educational governance” | **No** |
| “ED-01–ED-04 closed” | **No** |
| “Remediation can start with clause traceability” | **Yes** |

---

**End of GOVERNANCE_COMPLIANCE_SCORECARD**
