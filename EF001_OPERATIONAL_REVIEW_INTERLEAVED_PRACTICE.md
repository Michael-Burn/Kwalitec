# EF-001 Operational Review: Interleaved Practice (F2b)

**Programme:** Educational Framework Freeze EF-001  
**Instrument:** Operational Review (completed from `EF001_OPERATIONAL_REVIEW_TEMPLATE.md`)  
**Observation ID:** F2b, Interleaved practice  
**Status:** Complete (documentation only; no application redesign)  
**Authority:** `EF001_EDUCATIONAL_FRAMEWORK_FREEZE.md`  
**Evidentiary basis:** Read-only investigation of 2026-09-09 ([interleaving investigation](5fc4fe77-bd1b-4c48-9eac-d749e5f9a409)), grounded in Domain F deferral ([Domain F scope](c464e925-d1ee-4174-b112-3868dc5d1386))  
**Effective review date:** 2026-09-09  

---

For every future educational observation, use the following review structure **before proposing any solution**.

## 1. Observation

Describe the observed behaviour factually.

The educational-science / Domain F audit deferred **F2b (Interleaved practice)** as Architecture / policy with the instruction: do not build for Private Beta; Constitutional conflict cited as Educational Atomicity plus the intentional Study Progress vs understanding split; **EF-001 review before redesign**. That formal Operational Review had never been filed in committed EF-001 artefacts before tonight.

Tonight’s read-only investigation established the following facts about the live product and law:

1. **Missing review artefact.** No completed Observation → Classification → Severity → Evidence → Smallest Effective Intervention → EF-001 Check for F2b exists under `EF001_*`, volume plans, or PB reports. Rubric scores from the science audits are not committed in git. The deferral text lives in the Domain F transcript, not in frozen EF-001 files.

2. **Arbitration explicitly forbids session-split mixing.** Same-day sitting precedence is locked in `app/application/adaptive_decision/arbitration.py` (module docstring, lines 1–10): overdue > due > adaptive > sequential; protected spaced reviews cannot be preempted; **“No session-split mixing.”** Granularity is which **one package** wins the whole day’s sitting. Classic educational-science interleaving (inject related old-topic items alongside new-topic practice **inside one sitting**) is a composition shape orthogonal to that precedence chain and is currently forbidden by that lock.

3. **Educational Atomicity.** Canonical law in `knowledge/version2/education/EDUCATIONAL_ATOMICITY.md`: every Learning Episode improves **one** educational capability relative to a curriculum-grounded learning objective. Session assembly may compose multiple episodes but must not fuse purposes. Kitchen-sink episodes that pack interleaving with other co-equal aims are forbidden under strategy invariant S6.

4. **Study Progress vs understanding split.** Canonical Version 1 story in `knowledge/educational/VERSION1_EDUCATIONAL_STATE_REFINEMENT.md` §4: Study Progress is syllabus coverage (completing study ≠ understanding); Estimated Knowledge is practice-backed provisional understanding; Educational Guidance does not replace Today’s Mission. Constitution integrity forbids mixing Study Plan coverage with Digital Twin understanding. Article VI Learning Mode follows **Current Learning Topic**; consolidation is a disclosed whole-day topic swap, not a silent mixed sitting. Live write-through attributes scored practice to **one** practiced topic (`app/application/student_runtime/evidence_write_through.py`).

5. **Package posture: stay within one topic / LO.** Learning sittings bind one package; practice items come from that package’s `knowledge_checks`; packages instruct students to stay on today’s LO (investigation example: “Stay inside 2.1.3.” in package JSON, reported as ~54 packages with that posture).

6. **No topic-relatedness model for mix candidacy.** Catalog/runtime can group by syllabus section, official order, or revision `return_targets` (19 revision packages; 0 learning packages). Those are **not** a discrimination / “related enough to interleave” graph. CS1 2026 has 14 topics and 72 LOs with **0** populated prerequisites. Learning Graph can hold edges but does not supply a populated CS1 interleave-relatedness model. Zero `interleav` / `INTERLEAVING` matches under live `app/` session composition (`INTERLEAVING` appears only in Version 2 `src/domain/education/` strategy catalogues, not EOS composition).

7. **Pedagogy catalogues already allow interleaving after floors; live EOS does not execute classic within-session mix.** P10 and `TEACHING_STRATEGY_CATALOGUE.md` §3.14 treat interleaving as a transfer strategy after single-node competence floors. The collision is not “interleaving is unknown to the books.” The collision is that **live EOS packages are atomic single-LO sittings**, and classic within-session multi-topic mix would make “today is topic X” partially false, risk Study Progress contamination, muddy per-capability evidence, and require multi-topic attribution the single-topic path does not own.

8. **Day-level revisit ≠ interleaved practice.** Spacing due/overdue and adaptive / consolidation whole-day swaps remain single-package sittings. They are not substitutes for within-session interleaved practice as Domain F scoped F2b.

---

## 2. Classification

Choose exactly one:

| Code | Meaning |
|------|---------|
| **EC** | Educational Content |
| **AW** | Author Workflow |
| **RB** | Runtime Behaviour |
| **PI** | Product Implementation |
| **EF** | Educational Framework (requires evidence that EF-001 is insufficient) |

**Chosen classification: EF**

**Reasoning (not a default):**

- This is **not EC**: the issue is not a missing Continuity Front LO package or authorable content gap on the first-pass spine.
- This is **not AW**: author tooling / EW-001 is not the limiting surface.
- This is **not RB**: arbitration and single-package composition are behaving as designed; there is no defect to patch that would unlock classic within-session mix.
- This is **not merely PI**: shipping classic within-session interleaving is not a contained product feature under existing sitting law. The hard stop is Educational Atomicity as applied to episode/sitting purpose, the intentional Study Progress vs understanding split (including Current Learning Topic honesty), and composition policy that encodes those meanings (“No session-split mixing”). Domain F correctly labelled F2b **Constitutional**.

**Stewardship honesty (template note):** Classification **EF** is exceptional. Freeze §2 still requires Founder Validation or Private Beta evidence of a genuine educational failure that existing law cannot explain or correct, plus evidence of **framework** deficiency. Tonight’s investigation documents a **law collision for classic within-session interleaving**, not a validated student-harm package meeting §2. This EF classification therefore means: resolving F2b **as classic within-session interleaving** would require changing frozen educational meanings / their application to sittings. It does **not** by itself authorize an EF-001 unfreeze programme.

---

## 3. Severity

| Code | Meaning |
|------|---------|
| **S1** | Educationally blocking |
| **S2** | Educational quality reduced |
| **S3** | Cosmetic / polish |

**Chosen severity: S2**

**Reasoning:** Domain F explicitly deferred F2b for Private Beta (not S1 educationally blocking for Stage 1 / first-pass volume). Absence of classic post-floor interleaved discrimination practice is still a substantive educational-quality gap relative to the educational-science and Version 2 strategy catalogue posture for transfer, not cosmetic polish (not S3). Severity is **literature- and architecture-informed**, not Founder-Validated student harm: N_external remains 0 and no FV session evidence of transfer failure from missing within-session mix was part of tonight’s basis.

---

## 4. Evidence

Summarise the evidence supporting the observation.

| Finding | Reference |
|---------|-----------|
| Mandatory pre-solution gate (six sections) | `EF001_OPERATIONAL_REVIEW_TEMPLATE.md` |
| Freeze law; §2 unfreeze higher bar; operational review mandatory | `EF001_EDUCATIONAL_FRAMEWORK_FREEZE.md` §§2, 5; `.cursor/rules/11-educational-framework-freeze.mdc` |
| F2b deferral: Architecture / policy; Defer; Constitutional; Atomicity + Study Progress vs understanding; EF-001 review before redesign | Domain F scope transcript [Domain F scope](c464e925-d1ee-4174-b112-3868dc5d1386) |
| Formal F2b Operational Review previously absent from committed artefacts | Tonight’s investigation [interleaving investigation](5fc4fe77-bd1b-4c48-9eac-d749e5f9a409) §1 |
| “No session-split mixing”; overdue > due > adaptive > sequential | `app/application/adaptive_decision/arbitration.py` lines 1–10 |
| Composer selection reasons (spaced / adaptive / sequential / student_selected) | `app/application/educational_runtime_engine/selection_reasons.py` |
| Educational Atomicity definition and one-capability rule | `knowledge/version2/education/EDUCATIONAL_ATOMICITY.md` |
| Study Progress ≠ Estimated Knowledge; forbidden mixing | `knowledge/educational/VERSION1_EDUCATIONAL_STATE_REFINEMENT.md` §4; `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` integrity / Article VI |
| Single-topic practice attribution | `app/application/student_runtime/evidence_write_through.py` |
| Stay-on-today’s-LO package instruction (example “Stay inside 2.1.3.”; ~54 packages reported) | CS1 educational package JSON (e.g. `app/curriculum/data/educational_packages/cs1/cp-2.1.3-prob-quantiles-cs1016.json`); investigation §2 table |
| No discrimination relatedness model; sections / order / `return_targets` insufficient; 0 CS1 prerequisites populated | `app/curriculum/data/ifoa/cs1/2026.json`; revision package `return_targets`; `app/application/learning_graph/graph_builder_service.py`; investigation §3 |
| Interleaving named as post-floor strategy (not live EOS composition) | `knowledge/version2/education/INSTRUCTIONAL_PRINCIPLES.md` P10; `knowledge/version2/education/TEACHING_STRATEGY_CATALOGUE.md` §3.14; `INTERLEAVING` in `src/domain/education/` only |
| Objective evidence can record objective grain but not mix condition today | `app/application/objective_evidence/records.py`; investigation §5 |
| Spacing / adaptive day-level revisit ≠ within-session interleaving | Investigation §4 |

---

## 5. Smallest Effective Intervention

Recommend the minimum change necessary to resolve the issue.

**Primary recommendation: (a) build nothing for classic within-session interleaved practice, and formally document the boundary.**

1. Treat this completed Operational Review as the missing F2b gate artefact Domain F required before redesign.
2. Do **not** redesign arbitration, session composition, package atomicity, Study Progress semantics, or Educational Atomicity in response to F2b.
3. Record explicitly: **classic within-session interleaving** (mixed related problem types / topics inside one sitting while Current Learning advances) requires a **future architectural / educational-law change** if ever pursued, plus freeze §2 evidence (genuine FV/PB failure, insufficiency of existing law, framework-level deficiency). Preference, educational-science fashion, or roadmap completeness are not §2 evidence.
4. Do not weaken the definition of interleaved practice by claiming that spacing due/overdue, adaptive review, or consolidation whole-day swaps “already are interleaving.” Those are lawful single-package revisit mechanisms; they are not F2b.

**Secondary, explicitly separate track: (b) distributed cross-session sequencing may be investigated later as its own question.**

- That idea (ordering related topics across days without within-session mix) is **not** the F2b mechanism Domain F deferred.
- It must not be smuggled in as “solving interleaving” or as a silent redefinition of F2b.
- If product change is ever proposed for that track, it needs its **own** EF-001 Operational Review, with its own classification against existing spacing / adaptive / campaign sequencing law, and must not invent relatedness capability the catalog still lacks.

**Rejected under tonight’s discipline:**

- Building classic within-session mix now (mechanism-now without lawful composition or evidence condition tags).
- Inventing mix candidacy from section co-membership or `return_targets` alone.
- Treating arbitration as a place to add a fifth “interleave” winner as if that were classic interleaving.
- Solving a roadmap item by weakening Atomicity, Study Progress honesty, or the meaning of interleaved practice.

---

## 6. EF-001 Check

Answer:

> Can this be resolved without modifying the frozen Educational Framework?

| Answer | Action |
|--------|--------|
| **YES** | Proceed under existing Educational Law. |
| **NO** | Document why all existing mechanisms are insufficient and prepare evidence for a potential EF-001 unfreeze review (freeze §2 conditions). |

**Answer for classic within-session interleaved practice (F2b as Domain F scoped it): NO**

**Why existing mechanisms are insufficient for that form:**

- Live sitting law and composition already implement Educational Atomicity and Current Learning Topic honesty as **one package / one primary purpose per sitting**, with an explicit **no session-split mixing** lock.
- Study Progress vs Estimated Knowledge integrity forbids treating mixed revisit practice as coverage theatre or as silent Current Learning advance.
- Day-level spacing and adaptive revisit are available under existing law and do **not** produce classic within-session interleaving; they cannot be stretched to satisfy F2b without redefinition.
- Relatedness data required to choose honest interleave candidates does not exist in the live catalog; inventing mixes without it would be capability theatre.

Therefore classic within-session interleaving **cannot** be introduced while leaving frozen Educational Framework meanings (and their sitting-level application) unchanged.

**What does *not* require framework modification:** accepting the intentional absence for Private Beta; continuing volume, Founder study, and evidence collection; optionally opening a **separate** review later for distributed cross-session sequencing that does not claim to be F2b.

**Freeze §2 posture:** This NO documents insufficiency of existing mechanisms **for the classic F2b form**. It does **not** open an unfreeze programme. Unfreeze remains blocked until Founder Validation or Private Beta shows a genuine educational failure that existing law cannot correct, with evidence the deficiency is in the framework itself.

---

## Stewardship note

This review template is mandatory for all future educational observations and ensures every improvement remains evidence-driven, proportionate, and consistent with EF-001.

Classification **EF** is exceptional. Prefer EC / AW / RB / PI unless Founder Validation or Private Beta evidence shows the failure cannot be explained or corrected under existing Educational Law.

**Application of that note here:** EF is chosen because resolving classic within-session interleaving collides with frozen educational meanings (Atomicity, Study Progress vs understanding, Current Learning Topic honesty), not because §2 unfreeze evidence already exists. No application code, architecture, or arbitration change accompanies this review.
