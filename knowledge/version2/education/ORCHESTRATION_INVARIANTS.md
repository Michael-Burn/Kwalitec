# Orchestration Invariants

**Document ID:** V2-EOA-005  
**Classification:** Educational Architecture — Orchestration  
**Status:** Binding educational orchestration invariants  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`EDUCATIONAL_ORCHESTRATION_MODEL.md`](EDUCATIONAL_ORCHESTRATION_MODEL.md)  
**Companions:** [`EDUCATIONAL_REASONING_INVARIANTS.md`](EDUCATIONAL_REASONING_INVARIANTS.md) · [`LEARNING_EPISODE_INVARIANTS.md`](LEARNING_EPISODE_INVARIANTS.md) · [`STRATEGY_INVARIANTS.md`](STRATEGY_INVARIANTS.md) · [`EDUCATIONAL_INVARIANTS.md`](EDUCATIONAL_INVARIANTS.md) · [`SESSION_ASSEMBLY_MODEL.md`](SESSION_ASSEMBLY_MODEL.md)

---

## 1. Purpose

This document states **Orchestration Invariants**: permanent constraints on how Kwalitec may coordinate the Educational Operating Model into a tutoring experience.

These invariants specialise Domain, Reasoning, Strategy, and Episode invariants at the **orchestration grain** — the collaboration among Twin review, diagnosis, priority, intention, strategy, episodes, evidence, reflection, Twin update, and recommendation.

Approximate catalogue size: **twenty** orchestration invariants (O1–O20), plus short meta-rules.

Where conflict appears with higher constitutional law, higher law prevails until formal amendment aligns them.

---

## 2. How to Read an Invariant

Each invariant has:

- **Statement** — the binding rule  
- **Rationale** — why the rule exists  
- **Forbids** — characteristic violations  
- **Requires** — characteristic lawful behaviour  

---

## 3. Core Orchestration Invariants

---

### O1 — The Digital Twin is consulted before teaching

**Statement:** Targeted teaching in an orchestration turn may not begin without Review of the Student Digital Twin as standing educational belief and uncertainty (including the lawful thin-Twin cold-start case).

**Rationale:** Tutoring without learner-state context repeats amnesia and invents need from the calendar.

**Forbids:** Teaching assignments that ignore Twin context; treating Twin review as optional decoration.

**Requires:** Explicit Twin consultation before Intention locks into Delivery.

---

### O2 — Every episode originates from an educational justification

**Statement:** Every Learning Episode enacted under orchestration must be traceable to Educational Diagnosis and Teaching Intention (including lawful cold-start introduction diagnosis under curriculum sequencing).

**Rationale:** Episodes without justification are activity theatre.

**Forbids:** Content pushed because it was next in a file; UI templates spawning episodes without need.

**Requires:** Diagnosis → Intention → Strategy → Episode Selection chain for each teaching episode.

---

### O3 — Every session contains coherent Learning Episodes

**Statement:** A Learning Session may only assemble episodes that share educational coherence (objective arc, justified prerequisite bridge, or lawful contrastive repair) — not an arbitrary bundle.

**Rationale:** Incoherent sittings break concept continuity and explainability.

**Forbids:** Topic thrash playlists; packing unrelated deficiency classes for engagement.

**Requires:** Session Assembly principles: ordering, atomicity, concept continuity.

---

### O4 — Teaching never bypasses diagnosis

**Statement:** Orchestration may not move from arrival or Twin review to episode delivery without Educational Diagnosis (brief cold-start diagnosis included).

**Rationale:** Teaching without diagnosis is broadcasting.

**Forbids:** “Start practice” as the first reasoning act; strategy-first teaching that reverse-fits a diagnosis.

**Requires:** Named educational problem before Intention and Strategy.

---

### O5 — Recommendations are explainable

**Statement:** Every material Next Recommendation must answer what should happen next, why (diagnosis + intention at minimum), and what follows — in educational language.

**Rationale:** Opaque next-buttons destroy tutor trust and educational accountability.

**Forbids:** Recommendations justified only by engagement, streaks, or inventory pressure.

**Requires:** Traceable Adaptation after Twin Update.

---

### O6 — Evidence is collected after every episode

**Statement:** Every Learning Episode that claims educational work must produce evidence attributable to its purpose (including honest empty/failure evidence).

**Rationale:** Without evidence, Twin Update and next diagnosis are fiction.

**Forbids:** Closing episodes as complete with no observational spine; inventing evidence from scores alone.

**Requires:** Evidence Collection as a non-optional orchestration stage per episode.

---

### O7 — Reflection changes future teaching

**Statement:** Reflection artefacts captured under orchestration must be capable of influencing subsequent Diagnosis, Hypothesis, Intention, Strategy, or Twin interpretation; decorative reflection is unlawful.

**Rationale:** Reflection without consequence is ritual, not tutoring.

**Forbids:** Surveys that cannot affect the next move; discarding reflection before Twin Update.

**Requires:** Consequence-bearing reflection or lawful deferral with preserved consequence.

---

### O8 — Priority precedes intention when needs compete

**Statement:** When multiple material diagnoses exist, Educational Priority must select the governing problem before Teaching Intention locks.

**Rationale:** Unprioritised intention becomes opportunistic content pushing.

**Forbids:** Teaching the most convenient objective while a blocking prerequisite or active misconception is ignored.

**Requires:** Application of Priority principles (see Priority Model).

---

### O9 — Hypothesis remains orchestration-visible and revisable

**Statement:** The working Educational Hypothesis (or competitor set) must remain available to strategy selection and must be revised when evidence contradicts.

**Rationale:** Hidden or frozen hypotheses produce wrong long commitments.

**Forbids:** Teaching as if a refuted hypothesis still governed; omitting hypothesis posture when evidence already underdetermines the move.

**Requires:** Explicit demotion, revision, or replacement when warrant changes.

---

### O10 — Strategy never replaces diagnosis or intention

**Statement:** Selecting a Teaching Strategy does not constitute diagnosis or intention and may not skip those stages.

**Rationale:** *How* is not *what is wrong* and not *what change to seek*.

**Forbids:** Method-first orchestration; diagnosis statements that are merely method labels.

**Requires:** Intention → Strategy order inside the flow.

---

### O11 — Episode selection preserves atomicity

**Statement:** Orchestration may select only episode types and goals that obey Educational Atomicity — one primary purpose per episode.

**Rationale:** Multi-purpose episodes destroy evaluability and Twin honesty.

**Forbids:** Fusing repair + transfer + exam technique into one atom; session blobs without episode identity.

**Requires:** Atomic Teaching Goals at episode grain.

---

### O12 — Dependencies constrain assembly and demand

**Statement:** Session assembly and challenge increases must respect Knowledge Dependencies and Concept Network constraints; transfer and advanced demand may not precede required introduction or prerequisite repair when those block honesty.

**Rationale:** Premature demand produces noise and false diagnosis.

**Forbids:** Far transfer as first use; advanced struggle that is really upstream absence left unaddressed.

**Requires:** Prerequisite-before-extension discipline in ordering and Decision D8.

---

### O13 — Misconception and prerequisite interrupts outrank planned volume

**Statement:** When evidence warrants Misconception or blocking Prerequisite Gap, orchestration must interrupt undifferentiated practice volume on the affected objective.

**Rationale:** Practice strengthens wrong models; advanced theatre on missing foundations harms learning.

**Forbids:** “Finish the plan first”; burying error in more clones.

**Requires:** Repair / Prerequisite Repair episodes (or equivalent lawful types) as priority overrides.

---

### O14 — Twin Update follows evidence and reflection

**Statement:** Twin Update in an orchestration turn follows Evidence Collection and Reflection (or lawful deferred reflection with preserved consequence); it may not precede them as if belief revision needed no inputs.

**Rationale:** Twin belief must track lawful inputs.

**Forbids:** Updating Twin from completion flags alone; skipping update while claiming tutoring closed.

**Requires:** Evidence (+ reflection) → Twin Update → Next Recommendation order.

---

### O15 — Twin estimates are never treated as new observations

**Statement:** Orchestration may use Twin estimates as interpretive context only; it may not treat them as fresh Evidence items.

**Rationale:** Collapsing belief and observation destroys evidential honesty.

**Forbids:** “Twin says mastered, therefore evidence of mastery today”; silent double-counting.

**Requires:** Clear separation of Review Twin / Interpret Evidence / Evidence Collection.

---

### O16 — Session completion never implies mastery

**Statement:** Closing a Learning Session must never be presented or reasoned as mastery, understanding completion, or journey success by synonym.

**Rationale:** Completion is sitting closure; mastery requires dimensional evidence over time.

**Forbids:** “Topic complete” celebrations from session end alone; wiping deficiency memory because the sitting finished.

**Requires:** Honest completion language and preserved deferred educational memory.

---

### O17 — Stopping conditions protect educational honesty

**Statement:** Orchestration must stop a sitting when capacity, evidence integrity, or Priority spacing requires — rather than filling time with unjustified episodes.

**Rationale:** Exhausted theatre and unfinished unevidenced episodes corrupt Twin and trust.

**Forbids:** Starting transfer/exam episodes that cannot be evidenced; pushing volume after identified but unaddressed misconception.

**Requires:** Lawful stopping conditions per Session Assembly Model.

---

### O18 — Adaptation requires interpretation

**Statement:** Changes to intention, strategy, focus, or recommendation mid-flow or across turns must follow interpretation of evidence (and reflection when present); novelty and engagement are not lawful drivers.

**Rationale:** Adaptation without interpretation is thrash (Domain invariant spirit).

**Forbids:** Random topic switching; strategy fashion; ignoring contradicting evidence to protect a plan.

**Requires:** Decision discipline (especially D11, D15) grounded in Interpret Evidence.

---

### O19 — Cold start remains honest

**Statement:** When evidence is thin, orchestration may use curriculum sequencing as a lawful temporary guide for introduction need, and must not fabricate educational history, mastery, or false confidence.

**Rationale:** Empty Twin is not licence for fiction.

**Forbids:** Fake prior mastery; overconfident Twin updates from first exposure alone.

**Requires:** Modest claims, introduction-class diagnosis, high uncertainty preserved.

---

### O20 — Orchestration stages may be brief but not absent

**Statement:** When tutoring is claimed, each stage of the Educational Orchestration flow may be brief under thin evidence, but none may be silently skipped.

**Rationale:** Absent stages recreate feature islands and break explainability.

**Forbids:** Jumping from login to questions with no Twin/diagnosis/intention path; skipping reflection and Twin Update at sitting close.

**Requires:** Complete flow integrity per Orchestration Model §7.

---

## 4. Meta-Rules

1. **Specialisation, not contradiction** — O-invariants refine I/R/S/E invariants; they do not authorise violations of higher educational law.  
2. **No new concepts via invariant** — invariants constrain collaboration among existing concepts only.  
3. **Technology independence** — invariants bind educational design and future implementation alike; they are not test assertions for a particular stack.  
4. **Amend deliberately** — changing an orchestration invariant is an architectural act, not a product tweak.

---

## 5. Catalogue Index

| ID | Statement (short) |
|----|-------------------|
| O1 | Twin consulted before teaching |
| O2 | Every episode has educational justification |
| O3 | Sessions contain coherent episodes |
| O4 | Teaching never bypasses diagnosis |
| O5 | Recommendations are explainable |
| O6 | Evidence after every episode |
| O7 | Reflection changes future teaching |
| O8 | Priority before intention when needs compete |
| O9 | Hypothesis visible and revisable |
| O10 | Strategy replaces neither diagnosis nor intention |
| O11 | Episode selection preserves atomicity |
| O12 | Dependencies constrain assembly and demand |
| O13 | Repair/prerequisite interrupts outrank volume |
| O14 | Twin Update follows evidence and reflection |
| O15 | Twin estimates ≠ new observations |
| O16 | Session completion ≠ mastery |
| O17 | Stopping protects honesty |
| O18 | Adaptation requires interpretation |
| O19 | Cold start remains honest |
| O20 | Stages may be brief, never absent |

---

## 6. Summary Propositions

1. Orchestration invariants bind how existing educational concepts collaborate into tutoring.  
2. Twin-before-teaching, diagnosis-before-teaching, justification-before-episode, and evidence/reflection-before-update form the non-negotiable spine.  
3. Sessions must be coherent; completion and stopping must remain honest.  
4. Explainable recommendations and consequence-bearing reflection keep Adaptation educational.  
5. Twenty invariants (O1–O20) are sufficient to govern orchestration design without prescribing implementation.
