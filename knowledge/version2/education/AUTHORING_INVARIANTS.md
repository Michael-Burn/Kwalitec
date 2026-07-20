# Authoring Invariants

**Document ID:** V2-SAA-006  
**Classification:** Educational Architecture — Subject Authoring Foundation  
**Status:** Binding invariants for subject authoring  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural (binding for design and governance)  
**Parent:** [`SUBJECT_AUTHORING_MODEL.md`](SUBJECT_AUTHORING_MODEL.md)  

**Related:** [`CONCEPT_DECOMPOSITION_MODEL.md`](CONCEPT_DECOMPOSITION_MODEL.md) · [`MISCONCEPTION_AUTHORING_MODEL.md`](MISCONCEPTION_AUTHORING_MODEL.md) · [`REPRESENTATION_MODEL.md`](REPRESENTATION_MODEL.md) · [`APPLICATION_AND_TRANSFER_MODEL.md`](APPLICATION_AND_TRANSFER_MODEL.md) · [`SUBJECT_INVARIANTS.md`](SUBJECT_INVARIANTS.md) · [`EDUCATIONAL_INVARIANTS.md`](EDUCATIONAL_INVARIANTS.md) · [`LEARNING_EPISODE_INVARIANTS.md`](LEARNING_EPISODE_INVARIANTS.md)

---

## 1. Purpose

This document states **authoring invariants**: rules that may never be violated when Kwalitec (or its subject experts) transforms a professional syllabus into educational knowledge for the Educational Operating Model.

These invariants specialise the Subject Authoring Model and its companions into binding obligations and prohibitions. They are educational law for *how knowledge may be authored* — not software assertions.

They sit alongside Educational Invariants (EDM), Episode Invariants (LEA), Reasoning Invariants (ERM), Strategy Invariants (TSA), and Subject Invariants (SKA). Where conflict appears, constitutional and EDM law prevail; authoring invariants refine the authoring layer. Subject Invariants (K*) remain binding for knowledge representation; authoring invariants (A*) govern the authoring process and completeness obligations.

Numbering: **A1–A20**.

---

## 2. How to Read an Invariant

Each invariant has:

- **Statement** — the binding rule  
- **Rationale** — why the rule exists  
- **Forbids** — characteristic violations  
- **Requires** — characteristic lawful behaviour  

---

## 3. Authoring Invariants

### A1 — Authoring produces educational knowledge, not software artefacts

**Statement:** Subject Authoring outputs are educational knowledge entities (concepts, dependencies, misconceptions, representations, contexts, objectives, assessment opportunities). Persistence formats, APIs, screens, and prompts are not substitutes for those entities and must not be treated as the authored truth.

**Rationale:** Collapsing education into implementation loses portability and governance.

**Forbids:** “Authored” meaning only a database row or CMS page without educational anatomy; equating UI copy with concept meaning.

**Requires:** Explicit educational artefacts (even if later stored digitally) with meaning independent of delivery mechanism.

---

### A2 — Syllabus authority bounds core authored scope

**Statement:** Core teachable knowledge for an examination pathway must remain mappable to authorised syllabus scope; enrichment outside that scope must be marked and must not be treated as examinable core without governance approval.

**Rationale:** Professional preparation is accountable to awarding-body authority.

**Forbids:** Silent scope inflation; teaching-as-core material that cannot be traced to syllabus legitimacy.

**Requires:** Traceability from learning objectives to syllabus objectives/containers.

---

### A3 — Concepts are authored before procedures as primary aims

**Statement:** Authors must not present procedures as primary teachable aims without authored governing concepts (and principles where relevant) sufficient for intelligible use — aligning with subject invariant K1 at authoring time.

**Rationale:** Ungrounded procedures produce ritual competence.

**Forbids:** Procedure-only authoring packages; answer recipes without concept anchors.

**Requires:** Concept (and principle) linkage for every primary procedure.

---

### A4 — Every concept has at least one representation

**Statement:** No teachable concept may be released as authoring-complete without at least one specified educational representation that supports its core meaning.

**Rationale:** Unrepresented concepts cannot be taught or probed consistently.

**Forbids:** Label-only concepts; decorative media counted as representation without structural content.

**Requires:** Named primary representation per concept; planned diversity where examination/professional demand requires translation.

---

### A5 — Representations support concepts; they do not replace them

**Statement:** A representation may not be treated as identical to the concept; authoring must preserve core meaning and boundaries independent of any single mode.

**Rationale:** Students otherwise lock to a picture or formula and fail under rewording.

**Forbids:** “The concept is the formula”; analogy-as-definition without limits.

**Requires:** Explicit concept meaning plus representation inventory; stated analogy limits where analogies are primary.

---

### A6 — Every misconception belongs to one or more concepts

**Statement:** Authored misconceptions must attach to concept(s) (and where relevant principles, rules, or formulae) whose meaning they distort — no free-floating confusion objects (aligns with K4).

**Rationale:** Untargeted error cannot be diagnosed or repaired explicitly.

**Forbids:** Misconception lists without concept links; treating slips as misconceptions without pattern criteria.

**Requires:** Concept linkage and observable evidence fields for operational misconceptions.

---

### A7 — Dependencies are authored before episodes

**Statement:** Learning Episodes that assume foundations may not be treated as design-ready until required educational dependencies for their target concepts/objectives are authored (typed at least for required vs helpful where the pathway uses typing).

**Rationale:** Episodes without dependency structure teach past absences and produce mimicry.

**Forbids:** Episode libraries that invent prerequisites ad hoc; “do Chapter 3 first” without named concept dependencies.

**Requires:** Dependency authorship as a precondition for episode readiness on dependent aims.

---

### A8 — Decomposition stages are not skipped

**Statement:** For a syllabus objective cluster treated as authoring-complete, the Concept Decomposition stages — Concepts → Dependencies → Misconceptions → Representations → Applications → Transfer Opportunities → Assessment Opportunities → Learning Objectives — must be addressed at least to minimal completeness; later stages may not be declared complete while earlier stages remain undefined for the same cluster.

**Rationale:** Skipping stages yields objectives without anatomy and assessment without aims.

**Forbids:** Jumping from syllabus bullet to quiz items; learning objectives authored with no concepts.

**Requires:** Ordered decomposition with iteration allowed but completeness gated.

---

### A9 — Assessment opportunities derive from learning objectives

**Statement:** Assessment opportunities must be authored relative to named learning objectives (and their knowledge targets); item-like designs without objective anchors are not lawful assessment opportunities in this architecture.

**Rationale:** Evidence without an aim cannot evaluate teaching or update understanding honestly.

**Forbids:** Orphan item banks as “assessment architecture”; assessing coverage as if it were understanding.

**Requires:** Explicit objective linkage and stated evidentiary claim (what the opportunity can and cannot show).

---

### A10 — Learning objectives are curriculum-grounded and concept-anchored

**Statement:** Every learning objective must trace to syllabus authority and name the concept(s)/skill(s) it targets; container-only aims (“finish the topic”) are not learning objectives.

**Rationale:** Teaching without a precise aim is activity theatre (aligns with episode invariant E2 at authoring source).

**Forbids:** Objectives that are only chapter titles or timeboxes.

**Requires:** Precision sufficient to guide Teaching Intention and evidence interpretation.

---

### A11 — Application follows understanding in educational design

**Statement:** Authoring must not prescribe application-primary pathways that omit conceptual meaning, boundaries, and (where relevant) misconception anticipation for the same aim; drill packages without understanding design are unlawful as complete authoring.

**Rationale:** Application without understanding produces clone competence and false readiness.

**Forbids:** Practice-only authoring for concept-bearing objectives; equating fluency drills with understanding design.

**Requires:** Understanding-supporting artefacts (meaning, boundaries, representations) alongside application contexts.

---

### A12 — Transfer requires multiple contexts

**Statement:** An authored claim that a learning objective includes transfer readiness requires more than one context (application plus at least one transfer context, or multiple differentiated application contexts with declared transfer distance); a single context cannot underwrite transfer.

**Rationale:** Transfer is flexible use under variation; one situation cannot demonstrate it.

**Forbids:** Labelling one hard clone as “transfer”; mastery language based on a single template.

**Requires:** Explicit multi-context transfer design when transfer is in scope.

---

### A13 — Application contexts precede transfer contexts for the same aim

**Statement:** Transfer contexts for an aim must reference base application context(s); authors may not introduce far transfer as the first use situation for a concept-bearing objective.

**Rationale:** Transfer presupposes something practised to transfer *from*.

**Forbids:** Novelty-first authoring that confuses shock with pedagogy.

**Requires:** Canonical application before near/far transfer ladders.

---

### A14 — Near and far transfer are distinguished

**Statement:** Authored transfer contexts must declare transfer distance (near vs far) and must not silently expand into a new learning objective without renaming the aim.

**Rationale:** Without distance and scope discipline, “transfer” becomes meaningless difficulty inflation.

**Forbids:** Undeclared recombination that adds untaught concepts under the same objective id.

**Requires:** Recorded distance judgement and concept-set check against the objective.

---

### A15 — Misconceptions include repair guidance when operational

**Statement:** Misconceptions marked operational for tutoring must include recommended teaching intentions, recommended strategy kinds, and evidence of repair — not only a description.

**Rationale:** Named errors without repair design create diagnosis theatre.

**Forbids:** Operational flags on description-only stubs; repair-by-volume as the sole recommendation.

**Requires:** Instructional completeness per Misconception Authoring Model levels.

---

### A16 — Ignorance and misconception remain distinct

**Statement:** Authoring must not encode pure absence of exposure as a misconception; gaps and wrong models require different intention classes and must be distinguishable in authored guidance.

**Rationale:** Repairing a model that was never formed wastes instructional effort; teaching as if a gap were a misconception mis-aims strategy.

**Forbids:** “Misconception: student doesn’t know X” without wrong-model content.

**Requires:** Explicit wrong-model description for misconceptions; separate handling notes for common gaps where helpful.

---

### A17 — Authenticity stays syllabus-legitimate

**Statement:** Professional, exam, and real-world application lenses must remain inside syllabus-legitimate demand for core pathways; real-world framing must not falsify subject structure.

**Rationale:** False authenticity teaches wrong models; illegitimate scope breaks professional accountability.

**Forbids:** Cartoon physics that corrupts actuarial structure; core contexts outside syllabus authority.

**Requires:** Legitimacy check per context; structural fidelity over decorative realism.

---

### A18 — Authoring does not estimate the learner

**Statement:** Subject Authoring must not assert student-specific mastery, confidence, retention, or readiness; those estimates belong to evidence-interpreting components (notably the Digital Twin), not to authored subject knowledge.

**Rationale:** Knowledge ontology and learner state are different authorities.

**Forbids:** Authored “students always know X by Chapter 4”; hard-coded readiness in concept records as if it were Twin output.

**Requires:** Separation of knowledge artefacts from learner-state artefacts.

---

### A19 — Teaching strategies consume authored knowledge; they do not invent it

**Statement:** Strategy and episode design may not introduce undocumented concepts, misconceptions, or objectives as if they were already authored; discovery of gaps must return to authoring.

**Rationale:** Otherwise the knowledge layer silently forks and Twin/diagnosis targets diverge.

**Forbids:** One-off episode concepts with no knowledge record; strategy packs that redefine meaning ad hoc.

**Requires:** Feedback loop from episode design to authoring updates.

---

### A20 — Minimal completeness gates teachability claims

**Statement:** A concept or objective cluster may not be claimed “teachable / authoring-complete” unless Concept Architecture minimal completeness (core meaning, boundaries, required prerequisites stance, canonical example, misconception stance, application context, provisional mastery indicators) and applicable authoring invariants A4–A14 are satisfied at least at stub-or-better levels defined by companion models.

**Rationale:** Premature completeness claims create false platform readiness.

**Forbids:** Shipping pathways as misconception-aware or transfer-ready without the corresponding artefacts.

**Requires:** Explicit completeness status; design debt tracked where richness is deferred.

---

## 4. Meta-Rules

1. **Amend deliberately** — Changing an invariant requires educational governance review; silent drift is unlawful.  
2. **Higher law wins** — Constitution and EDM invariants prevail over A* on conflict until aligned.  
3. **Debt is visible** — Incomplete authoring is allowed in drafts; invisible incompleteness is not.  

---

## 5. Summary Table

| ID | Short name |
|----|------------|
| A1 | Educational knowledge, not software |
| A2 | Syllabus bounds core scope |
| A3 | Concepts before procedures |
| A4 | ≥1 representation per concept |
| A5 | Representations support, not replace |
| A6 | Misconceptions attach to concepts |
| A7 | Dependencies before episodes |
| A8 | Decomposition stages not skipped |
| A9 | Assessment from objectives |
| A10 | Objectives grounded and anchored |
| A11 | Application follows understanding |
| A12 | Transfer needs multiple contexts |
| A13 | Application before transfer |
| A14 | Near/far distinguished |
| A15 | Operational misconceptions include repair |
| A16 | Ignorance ≠ misconception |
| A17 | Authenticity remains legitimate |
| A18 | Authoring ≠ learner estimation |
| A19 | Strategies consume, don’t invent |
| A20 | Minimal completeness gates claims |

---

## 6. Non-Goals

This document does not implement validators, Studio checklists, or CI rules. Future tooling may enforce subsets of these invariants; the invariants remain educational law regardless of tooling.
