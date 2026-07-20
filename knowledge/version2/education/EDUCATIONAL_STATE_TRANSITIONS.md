# Educational State Transitions

**Document ID:** V2-EOA-003  
**Classification:** Educational Architecture — Orchestration  
**Status:** Authoritative model of educational state transitions  
**Nature:** Documentation only — no runtime behaviour  
**Authority:** Architectural  
**Parent:** [`EDUCATIONAL_ORCHESTRATION_MODEL.md`](EDUCATIONAL_ORCHESTRATION_MODEL.md)  
**Companions:** [`UNDERSTANDING_MODEL.md`](UNDERSTANDING_MODEL.md) · [`LEARNING_MODEL.md`](LEARNING_MODEL.md) · [`EDUCATIONAL_DIAGNOSIS_MODEL.md`](EDUCATIONAL_DIAGNOSIS_MODEL.md) · [`EDUCATIONAL_DECISION_POINTS.md`](EDUCATIONAL_DECISION_POINTS.md)

---

## 1. Purpose

This document describes **educational state transitions**: how a student’s educational posture relative to a learning objective may lawfully change under tutoring.

State transitions are inferred from evidence. They are not certificates, not UI statuses, and not Twin field names. They organise how existing concepts — Understanding Levels, Learning Dimensions, and Deficiency Categories — move as orchestration proceeds.

**Governing claim:** Correct answers alone do not prove a favourable transition.

---

## 2. What “Educational State” Means Here

For orchestration, **educational state** relative to an objective is the tutor’s current warranted picture of:

1. **Understanding posture** — position on the Understanding ladder (Recognition → Explanation → Application → Analysis → Teaching Others), with honest uncertainty;  
2. **Dimensional posture** — relative strength/weakness across Understanding, Application, Connection, Retention, and Transfer;  
3. **Deficiency posture** — whether a named deficiency category is active, resolving, or no longer warranted;  
4. **Calibration posture** — relationship between self-appraisal and evidential warrant (including Low Confidence and False Confidence).

These are analytic facets of one learner relative to curriculum aims — not four separate ontologies. No new educational concepts are introduced.

### 2.1 Plain-language transition labels

Orchestration may speak of transitions in plain educational language. These labels **map onto** existing models; they do not replace them:

| Plain label | Anchored in existing concepts |
|-------------|-------------------------------|
| **Confused** | Conceptual Misunderstanding and/or Incomplete Understanding; fragile or empty explanation; high uncertainty; often Recognition-only or broken Recognition |
| **Emerging Understanding** | Movement into stable Recognition and early Explanation; partial Application may begin |
| **Stable Understanding** | Durable Explanation with reliable Application on standard legitimate tasks; conditions of use largely held |
| **Transfer** | Transfer dimension advancement — success under legitimate variation after local application exists |
| **Misconception (active)** | Deficiency category Misconception warranted |
| **Misconception repaired** | Misconception no longer warranted for that model; repair evidence met |
| **Weak Retention** | Deficiency category Weak Retention; Retention dimension fragile after delay |
| **Durable Retention** | Retention dimension improved with delayed evidence — never same-day success alone |

---

## 3. Transition Record Pattern

Each transition below defines:

| Element | Meaning |
|---------|---------|
| **Entry evidence** | What typically warrants being *in* the prior state |
| **Exit evidence** | What typically warrants leaving toward the next state |
| **Permitted transitions** | Lawful next states |
| **Forbidden transitions** | Moves that should never be claimed |

---

## 4. Understanding Posture Transitions

Understanding develops through the ladder in [`UNDERSTANDING_MODEL.md`](UNDERSTANDING_MODEL.md). Favourable orchestration moves the student upward with evidence; regression under delay or pressure is real and informative.

---

### 4.1 Confused → Emerging Understanding

**Entry evidence (Confused)**  
Empty or contradictory explanations; inability to state meaning or conditions of use; collapse on “why”; confusion among near concepts without (yet) a single stable wrong model — or with high uncertainty that prevents even Recognition.

**Exit evidence (toward Emerging Understanding)**  
Minimal correct recognition of the concept/objective; own-words paraphrase that is roughly right; basic condition of validity stated; simple probes succeed without requiring full application.

**Permitted transitions**  
- Confused → Emerging Understanding (via Concept Introduction / Deepening)  
- Confused → Misconception-active (when patterned wrong model becomes clear)  
- Confused → Prerequisite-gap focus (when upstream absence is the true reading)

**Forbidden transitions**  
- Confused → Stable Understanding in one unvaried success  
- Confused → Transfer claims  
- Confused → Mastery / journey completion claims  
- Treating confidence (“I get it”) as exit evidence alone

---

### 4.2 Emerging Understanding → Stable Understanding

**Entry evidence (Emerging)**  
Recognition present; explanation beginning; application intermittent or scaffold-dependent; boundaries incomplete.

**Exit evidence (toward Stable)**  
Consistent own-words explanation; justification of method choice on standard tasks; reliable Application on legitimate standard items; boundary awareness for central cases; reduced need for heavy scaffolds.

**Permitted transitions**  
- Emerging → Stable Understanding  
- Emerging → Incomplete Understanding (specific facet missing)  
- Emerging → Misconception-active (wrong model crystallises under practice)  
- Emerging → Weak Retention (appears after delay despite same-day emergence)

**Forbidden transitions**  
- Emerging → Transfer readiness from clone success alone  
- Emerging → Teaching Others level without generative explanation evidence  
- Declaring Stable from speed or coverage

---

### 4.3 Stable Understanding → Transfer

**Entry evidence (Stable)**  
Solid Explanation and Application on practised forms; conditions of use largely held; Twin/application posture supports challenge increase.

**Exit evidence (toward Transfer)**  
Success under legitimate surface variation; structure recognised despite rewording; method selection from principle across variants; connection across related objectives when synthesis is demanded.

**Permitted transitions**  
- Stable Understanding → Transfer (near, then far as objective demands)  
- Stable Understanding → Analysis / Teaching Others elicitation (understanding ladder continuation)  
- Stable Understanding → Weak Retention (if delay erodes without retrieval)  
- Stable Understanding → Exam Technique focus (if capacity exists but timed deployment fails)

**Forbidden transitions**  
- Stable → Transfer without any varied probe  
- Jumping to far transfer as first use situation for a concept-bearing objective  
- Treating one lucky variant success as durable transfer mastery

---

### 4.4 Understanding ladder (canonical grain)

Plain labels above compress the ladder for orchestration narrative. Canonical level transitions remain:

```text
Recognition → Explanation → Application → Analysis → Teaching Others
```

**Permitted:** stepwise advance with converging indicators; regression to a lower level under time pressure or delay.  
**Forbidden:** granting Analysis from Recognition quizzes; equating Teaching Others with peer-chat activity without generative structure; irreversible “level certificates.”

---

## 5. Deficiency Resolution Transitions

---

### 5.1 Misconception → Repaired

**Entry evidence (Misconception active)**  
Patterned errors; confident wrong explanations; discrimination failures on contrastive cases; resistance to mere re-telling of the correct rule.

**Exit evidence (Repaired)**  
Correct discrimination on contrastive cases; corrected explanation of the former wrong model; success on probes that previously triggered the misconception; reflection that can name the repaired distinction when elicited.

**Permitted transitions**  
- Misconception → Repaired → re-enter Guided / Independent Practice on the objective  
- Misconception → remains active (repair incomplete) → continue repair or revise hypothesis  
- Misconception → reclassified as Prerequisite Gap or Incomplete Understanding when warrant changes

**Forbidden transitions**  
- Misconception → Repaired because the student completed a drill set without discrimination evidence  
- Misconception → Ignored while increasing practice volume on the same wrong model  
- Misconception → Mastery  
- One correct answer after repair speech as permanent closure without probe

---

### 5.2 Weak Retention → Durable Retention

**Entry evidence (Weak Retention)**  
Earlier success followed by failure after a meaningful interval; spaced probe collapse; re-learning from near-scratch on previously covered objectives.

**Exit evidence (Durable Retention)**  
Successful delayed retrieval and application after spacing; retained explanatory structure, not only steps; stability across more than one delayed probe when claims strengthen.

**Permitted transitions**  
- Weak Retention → Durable Retention via retrieval/revision episodes across sessions  
- Weak Retention → Conceptual fade discovered → Concept Deepening (not pure retrieval)  
- Durable Retention → later Weak Retention (regression is real; re-space)

**Forbidden transitions**  
- Weak Retention → Durable Retention from same-day restudy success alone  
- Claiming Durable Retention from coverage revisit without delayed evidence  
- Treating Twin retention estimates as if they were delayed observations

---

### 5.3 Incomplete Understanding → More complete understanding

**Entry evidence**  
Correct work in a subset of cases; failure on boundary or assumption-change probes; explanations omitting critical constraints.

**Exit evidence**  
The missing facet is explained and used; boundary probes succeed; “except when…” cases stabilise.

**Permitted**  
Deepening targeted at the missing facet; then return to application.  
**Forbidden**  
More identical practice of the already-known facet as if it completed understanding.

---

### 5.4 False Confidence → Calibrated confidence

**Entry evidence**  
Self-appraisal materially exceeds warrant; clone success with variant failure; readiness claims without delayed or transfer evidence.

**Exit evidence**  
Self-appraisal aligns better with performance under discriminating challenge; student can name uncertainty honestly.

**Permitted**  
Discriminating challenge, confidence calibration episodes, transfer probes.  
**Forbidden**  
Comfort content that confirms false readiness; dashboard celebration as calibration.

---

### 5.5 Low Confidence → Recovered engagement with warrant

**Entry evidence**  
Adequate performance with self-reports of unreadiness; avoidance despite success.

**Exit evidence**  
Engagement restored; self-appraisal closer to warrant; unnecessary re-teaching requests decline.

**Permitted**  
Recovery episodes when evidence contradicts felt unreadiness.  
**Forbidden**  
Skipping dangerous misconception or prerequisite work to chase comfort; empty praise without evidential anchor.

---

## 6. Dimensional Transitions (Learning Model)

Orchestration may advance dimensions asynchronously. No single session must move all five.

| Transition class | Entry signal | Exit signal | Never claim from |
|------------------|--------------|-------------|------------------|
| Understanding ↑ | Thin explanation | Richer explanation + conditions | Correct numeric answer alone |
| Application ↑ | Can’t start valid methods | Reliable task performance | Recognition quizzes |
| Connection ↑ | Siloed local success | Relating neighbouring objectives | Single-topic clone drills |
| Retention ↑ | Delay collapse | Delayed success | Same-day massed practice |
| Transfer ↑ | Clone-only success | Variant success | One novel item luck |

**Forbidden dimensional theatre:** maximising Application score while ignoring active Misconception; maximising Coverage while calling it Retention.

---

## 7. Permitted Transition Graph (Summary)

```text
Confused ──► Emerging Understanding ──► Stable Understanding ──► Transfer
                │                            │
                ├─► Misconception (active) ──► Repaired ──► (re-enter practice)
                ├─► Incomplete Understanding ──► more complete facet
                └─► Prerequisite Gap focus ──► resume dependent objective

Any acquired posture ──► Weak Retention ──► Durable Retention
                              │
                              └─► conceptual fade ──► Deepening

Calibration: False Confidence ──► Calibrated
             Low Confidence   ──► Recovered (when warrant exists)
```

Regression edges (omitted above for clarity) are permitted whenever delay, pressure, or new evidence warrants: Stable → Emerging; Durable Retention → Weak Retention; Repaired misconception may reappear if a related wrong model was incomplete.

---

## 8. Transitions That Should Never Occur

The following claims are educationally unlawful:

1. **Coverage → any understanding or mastery state** by synonym.  
2. **Single correct answer → Stable Understanding or Transfer.**  
3. **Same-day success → Durable Retention.**  
4. **Misconception active → more Independent Practice** as the sole next state.  
5. **Prerequisite gap → advanced Transfer** on the dependent objective.  
6. **Confused → Exam-ready** without intervening understanding and application evidence.  
7. **Episode or session completion → Mastery.**  
8. **Confidence self-report alone → favourable transition.**  
9. **Strategy novelty → state improvement** without evidence.  
10. **Irreversible certificates** — educational states remain revisable estimates.

---

## 9. Role of Orchestration Stages

| Orchestration stage | Role in transitions |
|---------------------|---------------------|
| Review Twin | Holds prior state estimates and uncertainty |
| Interpret Evidence / Diagnosis | Names current deficiency posture |
| Intention / Strategy / Episode | Designed to *seek* a specific favourable transition |
| Evidence / Reflection | Warrant for claiming movement or refusing it |
| Twin Update | Revises standing belief about state — never invents observations |
| Next Recommendation | Chooses the next transition-seeking move |

Teaching seeks transitions; evidence adjudicates them. Aspiration is not exit evidence.

---

## 10. Summary Propositions

1. Educational state transitions organise Understanding, Dimensions, Deficiencies, and Calibration — using existing concepts only.  
2. Plain labels (Confused, Emerging, Stable, Transfer, Repaired, Durable Retention) map onto those concepts for orchestration narrative.  
3. Every favourable transition needs entry and exit evidence; many transitions may regress.  
4. Misconception repair and retention durability have distinctive evidence — practice volume and same-day success do not suffice.  
5. Forbidden transitions protect educational honesty against completion theatre and false readiness.
