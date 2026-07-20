# Subject Invariants

**Document ID:** V2-SKA-005  
**Classification:** Educational Architecture — Subject Knowledge Foundation  
**Status:** Binding invariants for subject knowledge representation  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural (binding for design and governance)  
**Parent:** [`SUBJECT_KNOWLEDGE_MODEL.md`](SUBJECT_KNOWLEDGE_MODEL.md)  

**Related:** [`CONCEPT_ARCHITECTURE.md`](CONCEPT_ARCHITECTURE.md) · [`KNOWLEDGE_DEPENDENCY_MODEL.md`](KNOWLEDGE_DEPENDENCY_MODEL.md) · [`CONCEPT_NETWORK_MODEL.md`](CONCEPT_NETWORK_MODEL.md) · [`EDUCATIONAL_INVARIANTS.md`](EDUCATIONAL_INVARIANTS.md) · [`LEARNING_EPISODE_INVARIANTS.md`](LEARNING_EPISODE_INVARIANTS.md)

---

## 1. Purpose

This document states **subject knowledge invariants**: rules that may never be violated when Kwalitec represents, teaches toward, or claims progress on subject matter.

These invariants specialise the Subject Knowledge Model, Concept Architecture, Knowledge Dependency Model, and Concept Network Model into binding obligations and prohibitions. They are educational law for *what knowledge is* and *how it may be treated* — not software assertions.

They sit alongside Educational Invariants (EDM), Episode Invariants (LEA), Reasoning Invariants (ERM), and Strategy Invariants (TSA). Where conflict appears, constitutional and EDM law prevail; subject invariants refine the knowledge layer.

Numbering: **K1–K20**, plus a short meta-rule set.

---

## 2. How to Read an Invariant

Each invariant has:

- **Statement** — the binding rule  
- **Rationale** — why the rule exists  
- **Forbids** — characteristic violations  
- **Requires** — characteristic lawful behaviour  

---

## 3. Core Subject Knowledge Invariants

### K1 — Concepts precede procedures

**Statement:** A procedure may not be taught as a primary aim unless its governing concepts are introduced or verified at least to the level required for intelligible use; procedural drill must not permanently substitute for conceptual grounding.

**Rationale:** Ungrounded procedures produce ritual competence that collapses under variation.

**Forbids:** Template training with no meaning; “just plug into the formula” as the whole pedagogy for a concept-bearing method.

**Requires:** Conceptual anchoring before or with first procedure teaching; re-anchoring when evidence shows ritualisation.

---

### K2 — Definitions alone do not constitute understanding

**Statement:** Ability to state a definition never by itself warrants a claim of understanding or mastery of the defined concept.

**Rationale:** Definitions stabilise vocabulary; understanding requires relation, conditionality, and use.

**Forbids:** Marking a concept “understood” because a definition was recited or recognised.

**Requires:** Additional evidence (explanation, contrast, application, or transfer) before strong understanding claims.

---

### K3 — Every concept has prerequisites

**Statement:** Every teachable concept (except declared foundational primitives of a subject pathway) must have explicit prerequisite structure — including the possibility of an empty *required* set only when the concept is an authorised entry point, still with named helpful or parallel neighbours where relevant.

**Rationale:** “No prerequisites” is usually an unexamined assumption, not a design conclusion.

**Forbids:** Orphan concepts with no readiness analysis; treating every topic as independently startable without justification.

**Requires:** Documented prerequisite stance per concept relative to the pathway (required / helpful / entry primitive).

---

### K4 — Every misconception belongs to one or more concepts

**Statement:** A misconception must be attached to the concept(s) (and where relevant principles, rules, or formulae) whose meaning it distorts; free-floating “student is confused” is not a misconception object.

**Rationale:** Untargeted confusion cannot be taught against explicitly.

**Forbids:** Misconception catalogues disconnected from concepts; treating slips as misconceptions without pattern.

**Requires:** Concept linkage for every named misconception used in diagnosis or teaching design.

---

### K5 — Procedures require conceptual grounding

**Statement:** Every procedure in subject knowledge must be linked to the concepts and principles that justify its steps and conditions of use.

**Rationale:** Steps without justification are exam tricks, not professional knowledge.

**Forbids:** Orphan procedures; answer recipes with no validity conditions.

**Requires:** Explicit grounding links; teaching that can answer “why this step?”

---

### K6 — Formulae require interpretation

**Statement:** A formula is incomplete knowledge without interpretation of symbols, returned quantity, and assumptions of validity.

**Rationale:** Professional examinations and practice punish symbol manipulation without meaning.

**Forbids:** Formula-sheet worship; success criteria that accept numeric answers with no interpretive check when the objective requires interpretation.

**Requires:** Symbol meaning, quantity meaning, and condition-of-use knowledge alongside the expression.

---

### K7 — Dependencies are educational, not merely syllabus order

**Statement:** Educational dependency may not be equated with chapter order, PDF sequence, or navigation order; when they diverge, honest teaching follows educational dependency within syllabus scope.

**Rationale:** Publishing order is not learnability.

**Forbids:** “Chapter 5 is next” as sufficient educational justification when required prerequisites are missing; encoding only untyped “comes before” as if it were full dependency law.

**Requires:** Typed dependency reasoning (required, helpful, parallel, extension, remediation, bridge).

---

### K8 — Topics are containers, not competence

**Statement:** Completing, covering, or navigating a topic never by itself implies grasp of the concepts, skills, or objectives it contains.

**Rationale:** Containers organise; competence lives in knowledge entities and evidenced capacity.

**Forbids:** “Topic done ⇒ ready”; mastery language attached to container closure alone.

**Requires:** Separate narration of coverage and evidenced capacity on objectives/concepts.

---

### K9 — Learning objectives target knowledge entities

**Statement:** Every learning objective must target one or more named knowledge entities (concept, skill, procedure, principle, or coherent set) — not only a module title or time block.

**Rationale:** Vague aims produce vague teaching and uninterpretable evidence.

**Forbids:** Objectives that are only “study Chapter 2”; aims with no teachable object.

**Requires:** Explicit entity targets at educational grain suitable for episodes.

---

### K10 — Skills integrate concept and action

**Statement:** A skill claim requires evidence of appropriate action under legitimate demand and must not be reduced to either isolated recall or ungrounded speed drills.

**Rationale:** Professional skill is judged in use, with judgement — not in keyword recognition alone.

**Forbids:** Equating skill with click-through exposure; equating skill with stopwatch fluency on identical clones only.

**Requires:** Task-class performance with conceptual appropriateness of method choice.

---

### K11 — Examples need counterexamples for boundary-critical concepts

**Statement:** For concepts where overgeneralisation is a known educational risk, teaching design must include boundary-marking counterexamples (or equivalent contrastive instances), not only positive examples.

**Rationale:** Positive examples alone invite false generalisation — a common path to misconception.

**Forbids:** Single-clone example sets for contrast-sensitive ideas; never showing where a rule fails.

**Requires:** Example/counterexample (or contrast-pair) design for boundary-critical concepts.

---

### K12 — Analogies are subordinate to formal meaning

**Statement:** Analogies may scaffold initial grasp but must not replace definitions, principles, or validity conditions as authoritative meaning.

**Rationale:** Untethered analogies become misconceptions.

**Forbids:** Permanently substituting metaphor for theory; assessing analogy recall as if it were subject mastery.

**Requires:** Explicit qualification of analogies; return to formal meaning before strong claims.

---

### K13 — Multiple representations strengthen connection

**Statement:** Where a discipline standardly uses multiple representations of a concept, subject design must treat translation across those representations as part of conceptual command — not as optional decoration.

**Rationale:** Representation lock is a form of shallow grasp.

**Forbids:** Teaching a concept in only one representational mode when others are syllabus-standard and examinable.

**Requires:** Planned movement among standard representations for such concepts.

---

### K14 — Application contexts are not optional ornament

**Statement:** Concepts intended for examinable use must be linked to legitimate application contexts; teaching that remains forever definitional without use violates the purpose of professional subject knowledge.

**Rationale:** Professional syllabuses assess use under constraints.

**Forbids:** Endless abstract exposition with no lawful application path; application only outside syllabus legitimacy.

**Requires:** At least one syllabus-legitimate application context per use-oriented concept/objective.

---

### K15 — Transfer contexts probe structure, not tricks

**Statement:** Transfer contexts must vary surface features while preserving legitimate underlying demand aligned to the learning objective; they must not become unfair traps or out-of-syllabus puzzles.

**Rationale:** Transfer evidence is only valid inside legitimate subject demand.

**Forbids:** Gotchas outside scope; variation so compound that the objective is no longer identifiable.

**Requires:** Controlled, objective-aligned variation for transfer aims.

---

### K16 — Extension knowledge must not displace core knowledge

**Statement:** Extension material may not be taught or assessed as a substitute for core understanding of the entity it extends.

**Rationale:** Ornament without core fails combination and foundational items.

**Forbids:** Teaching only the fancy case; declaring core mastered because an extension drill succeeded.

**Requires:** Clear core vs extension distinction in design and claims.

---

### K17 — Remediation dependencies override forward coverage pressure

**Statement:** When evidence activates a remediation dependency, lawful tutoring addresses the source deficit (or explicitly revises the aim) before pressing forward coverage of dependent targets.

**Rationale:** Forward practice on a broken foundation entrenches failure.

**Forbids:** “Finish the syllabus first, fix foundations later” when required remediation is evidenced; volume-as-cure for misconceptions.

**Requires:** Foundation repair or aim revision when remediation dependency is active.

---

### K18 — Bridge concepts must be taught when regions must join

**Statement:** When a later objective requires joining two network regions, the relevant bridge concept must be taught (or verified) rather than hoping students spontaneously invent the join.

**Rationale:** Combination failure often reflects a missing bridge, not lack of effort.

**Forbids:** Jumping between disconnected clusters for combination aims without the joining structure.

**Requires:** Explicit bridge teaching for cross-region objectives.

---

### K19 — Network relationships used in teaching must be typed

**Statement:** When teaching invokes a connection between concepts, the relationship type (depends on, explains, contrasts with, etc.) must be educationally determinate — not a vague “related to.”

**Rationale:** Untyped links produce navigation theatre without instructional force.

**Forbids:** “Related topics” as a substitute for relationship-aware teaching moves.

**Requires:** Typed edge selection matched to intention (see Concept Network Model).

---

### K20 — Subject knowledge remains syllabus-grounded

**Statement:** All first-class subject knowledge entities taught as core preparation must be mappable to authoritative syllabus scope for the relevant offering and edition; the platform must not invent a private parallel canon presented as official.

**Rationale:** Kwalitec prepares candidates for external legitimacy, not for an internal mythology.

**Forbids:** Core pathways that cannot be traced to syllabus aims; silent substitution of preferred content for official scope.

**Requires:** Traceability from objectives/entities to syllabus authority (edition-aware).

---

## 4. Meta-Rules

### M1 — Invariants constrain design before implementation

Subject invariants bind educational design, product claims, and future systems. Implementation convenience does not suspend them.

### M2 — Thin evidence yields modest claims

Where prerequisite graphs, misconception libraries, or transfer batteries are incomplete, claims about mastery and readiness must remain modest — incompleteness is design debt, not permission to equate coverage with competence.

### M3 — Amendment is formal

Changing a subject invariant requires the same seriousness as amending other educational law: explicit revision of this document and reconciliation with higher authorities (Educational Constitution, EDM invariants).

---

## 5. Cross-Reference to Sibling Invariant Sets

| If the issue concerns… | Primary catalogue |
|------------------------|-------------------|
| Learning, mastery, evidence honesty | [`EDUCATIONAL_INVARIANTS.md`](EDUCATIONAL_INVARIANTS.md) |
| Episode grain / atomicity | [`LEARNING_EPISODE_INVARIANTS.md`](LEARNING_EPISODE_INVARIANTS.md) |
| Diagnosis / intention / reasoning | [`EDUCATIONAL_REASONING_INVARIANTS.md`](EDUCATIONAL_REASONING_INVARIANTS.md) |
| Instructional method choice | [`STRATEGY_INVARIANTS.md`](STRATEGY_INVARIANTS.md) |
| Structure of teachable knowledge | **This document (K1–K20)** |

---

## 6. Related Documents

- [`SUBJECT_KNOWLEDGE_MODEL.md`](SUBJECT_KNOWLEDGE_MODEL.md)  
- [`CONCEPT_ARCHITECTURE.md`](CONCEPT_ARCHITECTURE.md)  
- [`KNOWLEDGE_DEPENDENCY_MODEL.md`](KNOWLEDGE_DEPENDENCY_MODEL.md)  
- [`CONCEPT_NETWORK_MODEL.md`](CONCEPT_NETWORK_MODEL.md)  
- [`EDUCATIONAL_INVARIANTS.md`](EDUCATIONAL_INVARIANTS.md)  
