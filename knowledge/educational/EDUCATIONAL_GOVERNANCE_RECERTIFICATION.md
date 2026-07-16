# Educational Governance Re-certification

**Capability ID:** EIP-004  
**Programme:** Educational Integrity Programme  
**Title:** Educational Governance Re-certification  
**Classification:** Formal Educational Governance Re-review  
**Status:** SUBMITTED — awaiting Architecture Review  
**Date:** 2026-07-15  
**Baseline:** `EDUCATIONAL_PHILOSOPHY_AUDIT_V2.md` (EPA-002)  
**Nature:** Analysis only — no application code, Constitution, Logic Registry, or other governance documents were modified  

**Governing authorities (applied as-written; not redesigned)**

| Authority | ID | Version | Path |
|-----------|-----|---------|------|
| Educational Constitution | EGI-001 | 1.0 | `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` |
| Educational Logic Registry | EGI-002 | 1.0 | `knowledge/educational/EDUCATIONAL_LOGIC_REGISTRY.md` |
| Educational Governance Review Standard | EGI-003 | 1.0 | `knowledge/educational/EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md` |

**Implementation capabilities certified against**

| Capability | Title | Primary artefacts |
|------------|-------|-------------------|
| EIP-001 | Educational State Ownership & Authority | `EDUCATIONAL_STATE_AUTHORITY_MATRIX.md`; `tests/test_eip001_educational_state_ownership.py` |
| EIP-002 | Educational Evidence Authority | `EDUCATIONAL_EVIDENCE_AUTHORITY.md`; `educational_evidence_authority.py`; `tests/test_eip002_educational_evidence_authority.py` |
| EIP-003 | Educational Narrative & Explainability | `EDUCATIONAL_EXPLAINABILITY_STANDARD.md`; `educational_explainability_service.py`; `tests/test_eip003_educational_explainability.py` |

**Method**

This is **not** a new Educational Philosophy Audit. Every EPA-002 finding is reviewed individually against current student-visible behaviour and decision authority. Categories A–H are re-scored under EGI-003. Recommendations name educational direction and future capability IDs only — not implementation design.

---

## Executive Summary

After EIP-001–EIP-003, Kwalitec’s educational cores no longer fail the automatic NON-COMPLIANT triggers that rejected EPA-002. Study Progress is no longer authored by mastery formulae; student-felt confidence and bare mission completion no longer advance Estimated Mastery; authorised Structured Question Results gate estimate writes; and student-facing Mission / Recommendation / Readiness narration now answers What / Why / Next with Learning Mode primacy and optional-coaching disclosure.

**Educational Governance Score: 88 / 100** (was **28 / 100**) — Conditional governance band.  
**Overall Governance Outcome: APPROVED WITH CONDITIONS**  
**Version 1.0 Educational Certification: NOT READY** (Release Gate still requires cleared **APPROVED**, Categories A–D **FULL**, score ≥ 90).

The understanding/ownership/evidence spine that rejected EPA-002 is restored. Residual gaps are genuine but bounded: Study Progress continuity on plan delete, thin Mastered-stage density floor, one scalar shared as Estimated Knowledge and Estimated Mastery speech, incomplete coaching Accept/Dismiss productisation, and a latent non-rendered MissionOptimizer path.

---

## Finding Review (EPA-002)

---

### FINDING-001 — Mastery formula auto-writes Study Progress

| Field | Value |
|-------|-------|
| **Previous Status** | Open — Critical (EPA-002) |
| **Current Status** | **Resolved** |
| **Educational justification** | `AdaptiveLearningService.update_mastery_after_attempt` updates Twin-owned estimate fields only and never sets `completed=True`. Regression proves high estimate scores leave Study Progress untouched. Coverage remains Mission Completion / manual Study Progress authority only (EL-001; Ownership Matrix). |
| **Related capability** | EIP-001 |

---

### FINDING-002 — Student-felt confidence can alone mint Mastered stage

| Field | Value |
|-------|-------|
| **Previous Status** | Open — Critical (EPA-002) |
| **Current Status** | **Resolved** |
| **Educational justification** | Live estimate path always passes `confidence_numeric=None`. Confidence may be retained as soft Educational Observation / display average only. Without authorised accuracy, mastery formula returns silence (0 / no write). High Mastered-stage assignment additionally requires evidence accumulation. Internal form value `"Mastered"` remains for felt confidence storage but no longer authors Estimated Mastery (see FINDING-011 residual vocabulary). |
| **Related capability** | EIP-001; EIP-002 |

---

### FINDING-003 — Mission completion still recalculates Estimated Mastery

| Field | Value |
|-------|-------|
| **Previous Status** | Open — High (EPA-002) |
| **Current Status** | **Resolved** |
| **Educational justification** | `LearningService.create_study_attempt` invokes mastery update only when Structured Question Results are present. Bare complete → attempt without accuracies leaves Estimated Knowledge / Mastery unchanged while `_apply_mission_topic_progress` updates Study Progress only. Regression proves completion-without-questions leaves prior `mastery_score` intact. |
| **Related capability** | EIP-001; EIP-002 |

---

### FINDING-004 — Study Progress co-writes `confidence="High"`

| Field | Value |
|-------|-------|
| **Previous Status** | Open — High (EPA-002) |
| **Current Status** | **Resolved** |
| **Educational justification** | Coverage writers (wizard init, sync completed topics, mission coverage path) no longer stamp system `confidence="High"` as a Study Progress side-effect. Confidence updates only when the student reports felt confidence. Coverage writes coverage. |
| **Related capability** | EIP-001 |

---

### FINDING-005 — Dual readiness meanings under “Learning Progress”

| Field | Value |
|-------|-------|
| **Previous Status** | Open — High (EPA-002) |
| **Current Status** | **Partially Resolved** |
| **Educational justification** | When a plan-backed curriculum summary exists, Dashboard “Learning Progress” narrates syllabus coverage as Learning Progress from Study Progress — explicitly not Estimated Mastery. Analytics KPI uses “Estimated readiness” with composite explanation. EIP-003 narratives separate Derived Fact (coverage) from Evidence-Based Estimate (composite). Residual: two readiness algorithms still exist in `ReadinessService`; Dashboard card title remains “Learning Progress” even on composite fallback paths, risking mild cross-surface comparison confusion if students equate the two percentages. |
| **Related capability** | EIP-001; EIP-003 |

---

### FINDING-006 — Advisory recommendation can disagree with Learning Mode without disclosure

| Field | Value |
|-------|-------|
| **Previous Status** | Open — High (EPA-002) |
| **Current Status** | **Resolved** |
| **Educational justification** | Learning Mode remains sole persisted Today’s Mission authority. Advisory cards and legacy recommendation enrichment state that coaching is optional and does not replace Learning Mode / Current Learning Topic. Weak-topic copy uses Estimated Knowledge language rather than absolute attainment theatre. CTA navigation to mission no longer silently commandeers topic authority. |
| **Related capability** | EIP-003 |

---

### FINDING-007 — Estimated Mastery lacks evidence-density gate for high stages

| Field | Value |
|-------|-------|
| **Previous Status** | Open — High (EPA-002) |
| **Current Status** | **Partially Resolved** |
| **Educational justification** | `EducationalEvidenceAuthority.may_assign_high_mastery_stage` requires at least two authorised accuracy observations before Mastered-stage assignment; a single favourable score may raise the estimate but is capped to Practising-stage language. Residual: density floor (`MIN_AUTHORISED_OBSERVATIONS_FOR_HIGH_MASTERY = 2`) is still thin relative to Constitution Article V §5 accumulation for high-stakes exam speech; spacing / Rank-A/B density not yet operational. |
| **Related capability** | EIP-002 |

---

### FINDING-008 — Educational Evidence domain not on the live student estimate path

| Field | Value |
|-------|-------|
| **Previous Status** | Open — High (EPA-002) |
| **Current Status** | **Partially Resolved** |
| **Educational justification** | Live path is governed by Educational Evidence Authority: only V1.0 authorised Structured Question Results update product estimate scalars; completion, confidence, time, and recommendations cannot. Correct silence is preferred when authorised evidence is absent. Residual: domain Evidence packages → Twin Knowledge State succession is not yet the full student-facing store (`ENABLE_EI_PROGRESS` remains False); product `TopicProgress.mastery_score` remains the interim estimate surface under Authority honesty. |
| **Related capability** | EIP-002 |

---

### FINDING-009 — Plan delete silently erases Study Progress

| Field | Value |
|-------|-------|
| **Previous Status** | Open — High (EPA-002) |
| **Current Status** | **Still Open** |
| **Educational justification** | `StudyPlanService.delete_study_plan` still hard-deletes curriculum-linked `TopicProgress` while preserving attempts/missions. Rightful coverage memory remains vulnerable to plan management. EIP-001–EIP-003 did not close this continuity debt. |
| **Related capability** | None closed — remaining backlog (see Remaining Gaps) |

---

### FINDING-010 — Shallow Why and suppressed warrant honesty

| Field | Value |
|-------|-------|
| **Previous Status** | Open — Medium (EPA-002) |
| **Current Status** | **Resolved** |
| **Educational justification** | `EducationalExplainabilityService` supplies mission, recommendation, and readiness narratives answering purpose, reason, estimates vs facts, advice, and next action. Thin-history readiness discloses that readiness cannot yet be estimated. Student-facing blocks replace family-generic silence with educationally specific Why copy. Domain EI explainability cargo may remain flag-gated; product explainability narration is live on Mission / Dashboard / Analytics paths. |
| **Related capability** | EIP-003 |

---

### FINDING-011 — Residual forbidden / borderline student language

| Field | Value |
|-------|-------|
| **Previous Status** | Open — Medium (EPA-002) |
| **Current Status** | **Partially Resolved** |
| **Educational justification** | “study evidence” replaced by “practice results” on mission/dashboard/analytics tooltips and copy; catastrophic engineering leaks remain regression-forbidden; legacy absolute “complete exam confidence” / “critically weak” fact theatre cleaned to Estimated Knowledge wording; stage “Mastered” maps to “Strong estimated knowledge” for student labels. Residual: mission review form still stores felt confidence as internal value `"Mastered"` (label “Very Confident”); Estimated Knowledge vs Estimated Mastery wording still overlaps (FINDING-012). |
| **Related capability** | EIP-003 |

---

### FINDING-012 — Estimated Knowledge and Estimated Mastery share one scalar

| Field | Value |
|-------|-------|
| **Previous Status** | Open — Medium (EPA-002) |
| **Current Status** | **Partially Resolved** |
| **Educational justification** | EIP-003 softens stage badges and prefers estimate labelling, but Version 1.0 still presents one `mastery_score` under both “Estimated Mastery” and “Estimated Knowledge” speech families. Constitutional Article IV.7 vs IV.8 distinction is narrated more carefully but not yet operationally dual-warranted. |
| **Related capability** | EIP-003 (presentation only); fuller closure deferred |

---

### FINDING-013 — Coaching agency (Accept / Dismiss) not student-productized

| Field | Value |
|-------|-------|
| **Previous Status** | Open — Medium (EPA-002) |
| **Current Status** | **Still Open** |
| **Educational justification** | Domain affordances and `RecommendationService.record_decision` remain preference-only and evidence-safe, but student HTTP Accept / Not today / Later controls for live advisory cards are not productized. CTA still primarily navigates to mission. EIP-003 improved framing of advice as optional; student coaching-consent loop remains incomplete. |
| **Related capability** | EIP-003 (partial narrative intent only) |

---

### FINDING-014 — MissionOptimizer remains a silent third advisory engine

| Field | Value |
|-------|-------|
| **Previous Status** | Open — Low (EPA-002) |
| **Current Status** | **Still Open** |
| **Educational justification** | `MissionOptimizer.generate_balanced_mission` is still computed toward dashboard context and remains unrendered. Latent dual-authority regression risk is unchanged; students do not presently rely on it. |
| **Related capability** | None closed — remaining backlog |

---

### FINDING-015 — Learning Mode mission authority itself is constitutionally aligned

| Field | Value |
|-------|-------|
| **Previous Status** | Strength (EPA-002) |
| **Current Status** | **Resolved** (strength reaffirmed) |
| **Educational justification** | Learning Mode + `CurriculumService.get_next_incomplete_topic` remains sole Version 1.0 persisted mission topic authority. EIP-001–EIP-003 preserve and reinforce this posture; advisory surfaces may advise but must not mutate Today’s Mission. |
| **Related capability** | EIP-001; EIP-003 |

---

### FINDING-016 — Digital Twin naming boundary largely intact

| Field | Value |
|-------|-------|
| **Previous Status** | Strength (EPA-002) |
| **Current Status** | **Resolved** (strength reaffirmed) |
| **Educational justification** | Students still do not see “Digital Twin” labelling; settings retain Learning profile status presence language; Progress depth remains gated. EIP-003 regression forbids engineering/Twin jargon on student templates. |
| **Related capability** | EIP-003 |

---

### Finding Resolution Summary

| Status | Count | Finding IDs |
|--------|------:|-------------|
| Resolved | 8 | 001, 002, 003, 004, 006, 010, 015, 016 |
| Partially Resolved | 5 | 005, 007, 008, 011, 012 |
| Still Open | 3 | 009, 013, 014 |
| Superseded | 0 | — |

Critical/High automatic-trigger findings from EPA-002 (001–004, 006) are **Resolved**. Remaining High-severity open residue is **FINDING-009** continuity plus partial density / Twin-store / readiness-label debts.

---

## Governance Review (Categories A–H)

Ratings use EGI-003 §4. Points use EGI-003 §5 weights. Previous scores are from EPA-002.

---

### Category A — Constitution Compliance (Weight 15)

| | |
|--|--|
| **Previous score** | NON-COMPLIANT — **0 / 15** |
| **Current score** | FULL — **15 / 15** |
| **Explanation** | Automatic Article VIII / IV triggers that rejected EPA-002 are closed: mastery is not asserted from completion, confidence, or time alone; Study Progress is not mixed into Estimated Mastery authorship; Learning Mode mission authority remains compliant. Terminology matches Article IV on the coverage and estimate spines. Residual continuity and presentation debts do not redefine constitutional meaning in live mutation behaviour. |

| Question | Answer |
|----------|--------|
| A1 Comply with Constitution? | Yes — core integrity and state-meaning rules hold on live paths |
| A2 Redefine terminology? | No material stealth redefinition; residual Knowledge/Mastery synonymy is presentation debt |
| A3 New educational concepts? | No — Authority Matrix / Evidence Authority / Explainability instantiate existing law |
| A4 Amended first? | N/A |

---

### Category B — Logic Registry Compliance (Weight 15)

| | |
|--|--|
| **Previous score** | NON-COMPLIANT — **0 / 15** |
| **Current score** | FULL — **15 / 15** |
| **Explanation** | EL-001 / EL-004 / EL-005 / EL-007 operational constraints that were violated are now enforced in write paths with regression tests. Ownership Matrix is the operational mutation gate. MissionOptimizer remains latent and **not** a student-relied decision path (EGI-003 B trigger requires student reliance). Registry residuals for Twin Progress depth remain documented debt under Evidence Authority honesty, not licence to violate registered constraints. |

| Question | Answer |
|----------|--------|
| B1 Follow registered logic? | Yes on Learning Mode, coverage, evidence-gated estimates, advisory non-mutation |
| B2 Logic changed without Registry? | No stealth meaning change; EIP artefacts subordinate to Registry |
| B3 Registry updated before approval? | Behaviour now matches declared constraints; deep Twin succession remains recorded residual |
| B4 EL-IDs identified? | Yes — EL-001–EL-012 reviewed against EIP-001–003 effects |

---

### Category C — Educational Truth (Weight 15)

| | |
|--|--|
| **Previous score** | PARTIAL — **7.5 / 15** |
| **Current score** | PARTIAL — **7.5 / 15** |
| **Explanation** | Material statements on Mission / Dashboard / Analytics / Recommendations now map to Observed Fact, Derived Fact, Evidence-Based Estimate, or Educational Advice, with estimates labelled and advice disclosed as optional. Score does not rise to FULL because one scalar still supports both Estimated Knowledge and Estimated Mastery speech (FINDING-012), which leaves a material truth-clarity defect relative to Articles III §4 and IV.6–8. |

| Question | Answer |
|----------|--------|
| C1 Four claim types only? | Yes on core narrated surfaces |
| C2 Estimates identified? | Yes for readiness composites and mastery-oriented labels |
| C3 Advice as advice? | Yes — optional coaching disclosure present |
| C4 Statements outside four types? | No material unclassified theatre found; Knowledge/Mastery synonymy remains inside estimate family but blurs two constructs |

---

### Category D — Evidence Integrity (Weight 15)

| | |
|--|--|
| **Previous score** | NON-COMPLIANT — **0 / 15** |
| **Current score** | FULL — **15 / 15** |
| **Explanation** | Automatic D triggers are closed: completion does not write Estimated Mastery; confidence alone does not author mastered language on the estimate path; duration alone does not establish understanding claims. Evidence Authority gates Twin-owned estimate writes to authorised Structured Question Results. High Mastered-stage language requires accumulation (≥2 authorised observations). Residual Twin dual-store / richer density are intentional transitional limitations that no longer fire NON-COMPLIANT triggers. |

| Question | Answer |
|----------|--------|
| D1 Claim→evidence link? | Narratives supply evidence_basis; estimates require authorised accuracies |
| D2 Completion→mastery incorrectly? | No |
| D3 Time⇒learning incorrectly? | No for estimate succession |
| D4 Confidence⇒knowledge incorrectly? | No for Twin estimate formula |
| D5 Single attempt minting? | High Mastered stage blocked; sparse estimate may update with understatement |

---

### Category E — State Ownership (Weight 10)

| | |
|--|--|
| **Previous score** | PARTIAL — **5 / 10** |
| **Current score** | FULL — **10 / 10** |
| **Explanation** | Educational State Authority Matrix establishes one Owner / Authority / Permitted Writers set for Study Progress, Educational Evidence, Estimated Knowledge, Estimated Mastery, Current Learning Topic, and Today’s Mission. Conflicting writers (estimate→coverage, completion→mastery, confidence→mastery, recommendation→mission) are regression-forbidden. Dual readiness **questions** are now lawfully distinguished in primary student labels (Learning Progress vs Estimated readiness). Continuity erasure on plan delete is a preservation defect, not a second writer of meaning (tracked under Remaining Gaps / Category G risk). |

| Question | Answer |
|----------|--------|
| E1 One owner per state? | Yes for mutation rights on Version 1.0 states |
| E2 Duplicated conflicting writers? | No on closed EIP-001 paths |
| E3 Conflicting authority for same question? | Learning Mode vs advice no longer equal-authority; readiness questions differentiated |

---

### Category F — Student Communication (Weight 10)

| | |
|--|--|
| **Previous score** | PARTIAL — **5 / 10** |
| **Current score** | FULL — **10 / 10** |
| **Explanation** | Plain educational language restored on reviewed student templates; Twin/engineering jargon forbidden by regression; What / Why / What next present for missions and recommendations; false certainty reduced via thin-history honesty and estimate labelling. Accept/Dismiss incompleteness is coaching-agency backlog (FINDING-013), not a failure of F1–F5 communication structure under current optional-advice framing. |

| Question | Answer |
|----------|--------|
| F1 Plain educational language? | Yes on reviewed surfaces |
| F2 What clear? | Yes |
| F3 Why clear? | Yes via Explainability narratives |
| F4 What next clear? | Yes — Learning Mode first; optional coaching later |
| F5 Avoid false certainty? | Yes directionally; residual form token / synonym debt acknowledged |

---

### Category G — Educational Consistency (Weight 10)

| | |
|--|--|
| **Previous score** | PARTIAL — **5 / 10** |
| **Current score** | PARTIAL — **5 / 10** |
| **Explanation** | Mission, Dashboard, and Recommendations now share one Learning Mode story with disclosed advisory divergence. Analytics separates Coverage from Estimated readiness. Category does not rise to FULL because plan delete still silently erases Study Progress (FINDING-009), breaking educational continuity across plan management, and MissionOptimizer remains a latent unrendered third generator (FINDING-014). |

| Question | Answer |
|----------|--------|
| G1 One educational story? | Mostly — continuity broken on plan delete |
| G2 Advisory divergence disclosed? | Yes |
| G3 Metric label discipline? | Improved; residual Knowledge/Mastery synonymy and Dashboard title fallback |

---

### Category H — Educational Integrity (Weight 10)

| | |
|--|--|
| **Previous score** | PARTIAL — **5 / 10** |
| **Current score** | FULL — **10 / 10** |
| **Explanation** | A reasonable educator can now defend coverage vs estimate behaviour and “completion ≠ mastery” messaging as aligned with product truth. Students can no longer manufacture Mastered-stage theatre from confidence or completion alone. Trust is preferred over optimisation on estimate succession (correct silence). Remaining risks (plan delete, thin density floor, coaching agency) are owned residuals rather than active educational dishonesty. |

| Question | Answer |
|----------|--------|
| H1 Trust rising? | Yes relative to EPA-002 / week_001 failure modes |
| H2 Educator agreement? | Yes on ownership/evidence spines |
| H3 Student misunderstanding risk? | Reduced to residual presentation / continuity issues |
| H4 Trust over optimisation? | Yes on estimate write gates |

---

## Scoring

### Educational Governance Score

| Category | Previous | Current Rating | Weight | Current Points |
|----------|----------|----------------|--------|----------------|
| A Constitution Compliance | 0 | FULL | 15 | 15 |
| B Logic Registry Compliance | 0 | FULL | 15 | 15 |
| C Educational Truth | 7.5 | PARTIAL | 15 | 7.5 |
| D Evidence Integrity | 0 | FULL | 15 | 15 |
| E State Ownership | 5 | FULL | 10 | 10 |
| F Student Communication | 5 | FULL | 10 | 10 |
| G Educational Consistency | 5 | PARTIAL | 10 | 5 |
| H Educational Integrity | 5 | FULL | 10 | 10 |
| **Total** | **28** | | **100** | **87.5 → reported 88 / 100** |

**Previous Educational Governance Score:** 28 / 100 — Failed governance  
**Current Educational Governance Score:** **88 / 100** — Conditional governance (EGI-003 §5 band 75–89)

**Delta:** **+60 points**

---

## Overall Results

| Measure | Previous (EPA-002) | Current (EIP-004) |
|---------|--------------------|-------------------|
| **Educational Governance Score** | 28 / 100 | **88 / 100** |
| **Educational Alignment** | 42 / 100 — Weak | **79 / 100** — Strong directional alignment |
| **Constitution Compliance** | NON-COMPLIANT | **COMPLIANT** (Categories A FULL; residual presentation/continuity debt owned) |
| **Logic Registry Compliance** | NON-COMPLIANT | **COMPLIANT** (Categories B FULL; residual Twin depth / latent optimizer documented) |
| **Overall Governance Outcome** | REJECTED | **APPROVED WITH CONDITIONS** |

### Outcome justification (EGI-003 §6)

- No Category A–D is NON-COMPLIANT.
- No open automatic NON-COMPLIANT rejection trigger remains on the live student path.
- Educational Governance Score ≥ 75.
- Exactly one of Categories A–D is PARTIAL (Category C — Knowledge/Mastery construct clarity).
- Written conditions below must clear before Version 1.0 Educational Release Gate.

Not **APPROVED**: score < 90 and Category C is not FULL.

---

## Automatic Trigger Check (EGI-003)

| Trigger | EPA-002 | EIP-004 |
|---------|---------|---------|
| Mastery from completion / confidence / time alone | OPEN | **Closed** |
| Adaptive interruption silently replacing Learning Mode | Closed | **Closed** |
| Student-editable mastery as verified fact checkbox | Closed | **Closed** |
| Mixing Study Progress / Learning Progress with Estimated Mastery | OPEN | **Closed** on primary labelled paths; residual synonymy tracked under Category C |
| Unregistered educational decision path students rely on | Partial (latent) | **Closed** for reliance (MissionOptimizer still unrendered / unused by students) |
| Ownership matrix violated | OPEN | **Closed** |
| Estimates as validated proof / advice as silent mission replacement | OPEN residual | **Closed** |
| Self-report alone authorizing mastered language | OPEN | **Closed** |
| Dashboard different Today’s Mission without advisory framing | OPEN residual | **Closed** |

---

## Version 1.0 Readiness

Assessed under EGI-003 §7 Educational Release Gate.

| Gate requirement | Status |
|------------------|--------|
| Educational Governance Review completed (this document) | Met |
| Outcome **APPROVED** | **Not met** — APPROVED WITH CONDITIONS |
| Categories A–D **FULL** | **Not met** — Category C PARTIAL |
| Educational Governance Score ≥ 90 | **Not met** — 88 |
| No open Educational Governance conditions | **Not met** |
| Constitution and Logic Registry versions cited | Met |
| Touched EL-xxx IDs listed | Met |

### Version 1 educational certification

**NOT READY**

Internal Alpha **educational deployment** may proceed under Architecture Office acceptance of the conditions below (EGI-003 §7 relationship note). Version 1.0 Educational Release Gate still requires cleared **APPROVED**.

---

## Remaining Gaps

Only genuine remaining educational issues. Resolved findings are not repeated.

---

### GAP-001 — Study Progress erased on plan delete

| Field | Value |
|-------|-------|
| **Source finding** | FINDING-009 |
| **Status (EIP-005)** | **CLOSED** — `StudyPlanService.delete_study_plan` preserves TopicProgress; planning artefacts and mission plan pointers only are disposed. Regression: `tests/test_eip005_educational_continuity.py`. |
| **Educational impact (pre-fix)** | Students lost rightful “completed studying” memory when deleting/managing a plan. |
| **Related Constitution Article** | Article II §1.8; Article IV.1; Article VIII.16; Article IX §4 |
| **Related Logic ID** | EL-001; EL-011 |
| **Closing capability** | **EIP-005 Educational Continuity** / `EDUCATIONAL_CONTINUITY_STANDARD.md` |

---

### GAP-002 — Estimated Knowledge vs Estimated Mastery still one scalar

| Field | Value |
|-------|-------|
| **Source finding** | FINDING-012 (also residual of FINDING-011) |
| **Educational impact** | Students cannot reliably distinguish “how well I understand now” from “how confidently I have mastered,” which weakens Category C truth clarity and analytics interpretability. |
| **Related Constitution Article** | Article III §4; Article IV.6–8; Article VIII rule 14 |
| **Related Logic ID** | EL-006; EL-007 |
| **Recommended future capability** | **EIP-V1-TRUTH**: Pick one Version 1.0 student construct (prefer Estimated Mastery with estimate framing) **or** distinguish both with separate warrant rules — stop interchangeable marketing synonyms for one score. Blocks Category C FULL. |

---

### GAP-003 — High-stage evidence density still thin

| Field | Value |
|-------|-------|
| **Source finding** | FINDING-007 |
| **Educational impact** | Two favourable practice sessions can still unlock Mastered-stage assignment language; false near-exam confidence remains more constrained than before but not fully educator-strong for Article V §5 accumulation. |
| **Related Constitution Article** | Article II §1.6–7; Article V §§3–5; Article VIII rules 10–12 |
| **Related Logic ID** | EL-005; EL-007 |
| **Recommended future capability** | **EIP-V1-DENSITY**: Raise lawful density / spacing expectations for high Estimated Mastery speech before Version 1.0 Release Gate. |

---

### GAP-004 — Coaching Accept / Not today / Later not productized

| Field | Value |
|-------|-------|
| **Source finding** | FINDING-013 |
| **Educational impact** | Advice is framed as optional, but without dismiss/defer the system cannot record preference and some students may still experience advice as non-negotiable chrome. |
| **Related Constitution Article** | Article I §4; Article II §1.9; Article VI §4 |
| **Related Logic ID** | EL-008 |
| **Recommended future capability** | **EIP-V1-AGENCY**: Productize Accept / Not today / Later as preference signals only — never as mastery or Study Progress writes. |

---

### GAP-005 — Latent MissionOptimizer path

| Field | Value |
|-------|-------|
| **Source finding** | FINDING-014 |
| **Educational impact** | No present student reliance, but a future template rewire could revive dual-authority confusion. |
| **Related Constitution Article** | Article VI; Article IX §3 |
| **Related Logic ID** | EL-003; EL-008; EL-009 |
| **Recommended future capability** | **EIP-V1-QUARANTINE**: Retire or quarantine non–Learning Mode mission-shaped generators from Version 1.0 student authority surfaces. |

---

### GAP-006 — Interim estimate store vs Twin succession depth

| Field | Value |
|-------|-------|
| **Source finding** | FINDING-008 |
| **Educational impact** | Understanding claims are now evidence-gated and honest under silence, but full Constitutional Evidence → Twin Knowledge State succession is not yet student-depth (`ENABLE_EI_PROGRESS` False). Acceptable transitional debt if strong claims remain subordinate to Authority and messaging discipline. |
| **Related Constitution Article** | Article III; Article IV.5–8; Article V; Article VIII rules 7, 10–12, 14 |
| **Related Logic ID** | EL-005; EL-006; EL-007; EL-012 |
| **Recommended future capability** | Post–Version 1.0 Twin Progress enablement under EL-012 messaging invisibility — **not** required to clear APPROVED WITH CONDITIONS if GAP-002/003 close honesty, but required before claiming full Twin-backed estimate architecture. |

---

## Conditions of Approval

Owned conditions before Version 1.0 Educational Release Gate (and before claiming outcome **APPROVED**):

1. **Close GAP-002** — eliminate interchangeable Estimated Knowledge / Estimated Mastery speech for one scalar (Category C → FULL).
2. **Close GAP-001** — preserve Study Progress across plan delete/archive unless explicit student-authorised reset (Category G material defect).
3. **Strengthen GAP-003** — raise high-stage evidence density beyond the current minimum-two floor to a Version 1.0 educator-defensible accumulation rule.
4. **Quarantine GAP-005** before any template change that could surface MissionOptimizer as mission-shaped authority.

GAP-004 (agency) and GAP-006 (Twin depth) are recommended for Version 1.0 polish and post-V1 Twin enablement respectively; Architecture Office may gate GAP-004 as a release condition if coaching consent is treated as mandatory for Internal Alpha educational trust.

---

## Certification Summary

### Improvements achieved

- Closed EPA-002 Critical/High automatic NON-COMPLIANT triggers on ownership and evidence succession (FINDING-001–004, 006).
- Established operational State Authority Matrix and Evidence Authority gate with regression protection.
- Installed student-facing explainability contract (What / Why / Next; claim-type honesty; optional coaching disclosure).
- Raised Educational Governance Score from 28 → 88 (+60).
- Restored Constitution and Logic Registry compliance on live educational cores.

### Governance categories improved

| From → To | Categories |
|-----------|------------|
| NON-COMPLIANT → FULL | A, B, D |
| PARTIAL → FULL | E, F, H |
| Unchanged PARTIAL | C, G |

### Educational strengths

- Learning Mode remains constitutionally correct sole mission topic authority.
- Coverage vs competence separation is now behavioural, not merely messaging.
- Correct silence when authorised Educational Evidence is absent.
- Twin naming invisibility and plain educational speech preserved/regressed.
- Curriculum-first deterministic cores remain free of opaque generative mission selection.

### Remaining educational risks

- Plan delete destroys rightful Study Progress.
- Knowledge/Mastery construct blur keeps Category C PARTIAL.
- Thin Mastered-stage density floor.
- Incomplete coaching Accept/Dismiss loop.
- Latent MissionOptimizer regression risk.
- Twin Progress succession still interim.

### Recommendation

**Accept EIP-004 outcome: APPROVED WITH CONDITIONS.**  
Proceed to Architecture Review. Do **not** declare Version 1.0 educational certification. Clear conditions (especially GAP-001 and GAP-002) under EIP-005 Version 1 Educational Readiness planning — without treating EIP-005 as started by this document.

---

## Method Notes

- Assessed **current implementation behaviour** after EIP-001–EIP-003, against EPA-002 finding-by-finding — not a greenfield audit.
- Student-facing paths weighted over unused domain packages.
- Internal Alpha flag contract noted: Recommendations ON; Missions / domain Explainability cargo / Progress OFF — product `EducationalExplainabilityService` narration is nonetheless live on Mission / Dashboard / Analytics routes.
- No Constitution, Registry, Governance Standard, Blueprint, or application code was modified for this deliverable.

---

## Return

**Stop after this report.**  
**Return for Architecture Review.**  
**Do not begin EIP-005.**
