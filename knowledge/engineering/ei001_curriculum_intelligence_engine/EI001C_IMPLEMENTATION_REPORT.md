# EI-001C — Implementation Report

**Programme:** Curriculum Intelligence Engine · Phase C  
**Status:** PHASE C COMPLETE  
**Date:** 2026-07-30  
**Authority:** `EI001_CURRICULUM_INTELLIGENCE_ENGINE.md` §12 Phase C  
**Scope:** Generations 4–6 + Educational Policies + Evidence grading  

---

## Summary

EI-001C delivers the first true educational reasoning capabilities of the
Curriculum Intelligence Engine. Generation 4 is renamed internally to
**Concept Formation** and discovers coherent learning units (merge / split /
retain) via `ConceptFormationPolicy`. Generation 5 (**Objective Intelligence**)
associates learning objectives, competencies, knowledge statements, and exam
expectations via `ObjectivePolicy`. Generation 6 (**Educational Reconciliation**)
builds a syllabus coverage matrix via `CoveragePolicy`. Every educational
decision carries reason, evidence, confidence, policy id, and Evidence Grade
(A–D). `RegressionGuard` now hard-gates coverage, hierarchy, granularity,
evidence quality, and confidence. The existing CIP pipeline remains functional.

---

## Educational Policies

Policies define deterministic educational decision rules. Agents execute them.

| Policy | ID | Gen | Decisions |
|---|---|---:|---|
| `EducationalPolicy` (base) | — | — | Common descriptor contract |
| `ConceptFormationPolicy` | `concept_formation_policy` | 4 | merge · split · retain |
| `ObjectivePolicy` | `objective_policy` | 5 | attach LO / competency / knowledge / exam |
| `CoveragePolicy` | `coverage_policy` | 6 | covered · missing · unexpected · hierarchy |

Every `EducationalDecision` includes:

- Reason  
- Evidence refs  
- Confidence  
- Policy used  
- Highest supporting Evidence Grade  
- Optional syllabus reference  

Laws: same inputs → same decisions; no LLM in educational decisions.

---

## Evidence grading

| Grade | Meaning |
|---|---|
| **A** | Official syllabus / official learning objectives |
| **B** | CMP headings / definitions / worked examples |
| **C** | Paragraph inference / examples |
| **D** | Heuristic inference / AI-supported reasoning (presentation-only) |

`QualitySnapshot.evidence_quality` is the mean grade weight on active educational
nodes (A=1.0 … D=0.25). Pre-grading generations infer A for syllabus-ref nodes
and B for provenance-backed nodes so RegressionGuard has a comparable vector
from Gen 1 onward.

---

## Concept Formation results

Internally renamed from Topic Consolidation → Concept Formation
(`GenerationIndex.CONCEPT_FORMATION`; `TOPIC_CONSOLIDATION` retained as alias).

Fixture run (mini CS1 syllabus, `fixed_created_at_iso=2026-07-30T12:00:00Z`):

| Outcome | Behaviour |
|---|---|
| Retain | Coherent syllabus topics kept as `kind=concept` with Grade A |
| Merge | Near-duplicate siblings / fragments → survivor absorbs; lineage `MERGED`; children `REPARENTED` |
| Split | Compound multi-numbered titles → new concept nodes; source soft-inactive |

On the mini fixture all three topics were **retained** (already coherent).
Synthetic sibling fixtures exercise merge + reassignment lineage in tests.
Optimisation target is educational coherence — not topic-count targets.

---

## Coverage improvements

| Metric | Gen 3 | Gen 4 | Gen 5 | Gen 6 |
|---|---:|---:|---:|---:|
| coverage | 0.6780 | 0.6780 | 0.6780 | **1.0000** |
| hierarchy | 0.6900 | 0.6900 | 0.6900 | 0.6900 |
| granularity | 0.8500 | 0.8500 | 0.8500 | 0.8500 |
| evidence_quality | 0.9750 | 0.9750 | 0.9750 | 0.9750 |
| confidence | 0.9240 | 0.9360 | 0.9480 | 0.9480 |
| noise | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

Gen 6 coverage matrix (fixture):

- covered = 4 · missing = 0 · unexpected = 0  
- hierarchy_consistent = True · completeness = 1.0000  

Coverage rises because Gen 6 blends syllabus completeness into the quality
vector (`coverage_override`), elevating reconciliation to a first-class
generation metric.

---

## Reasoning examples

**Concept Formation (retain):**

> Topic `1.1 Describe the purpose and function of data analysis`  
> Action: retain · Policy: `concept_formation_policy` · Grade: A  
> Reason: “Topic already forms a coherent learning unit”  
> Confidence: 0.92 · Syllabus ref: from lineage  

**Concept Formation (merge — synthetic):**

> Sibling topics sharing syllabus number `1.1` with near-duplicate wording  
> Action: merge · Survivor keeps identity · Absorbed soft-inactive  
> Reason: “Sibling topics form one coherent learning unit; an IFoA student
> would naturally study them together”  
> Children of absorbed topics reassigned (`REPARENTED`) under survivor  

**Objective Intelligence:**

> LO `1.1.1 …` receives attachments:  
> `obj:learning_objective` · `obj:knowledge_statement` · `obj:competency`
> (when verb present) · `obj:exam_expectation`  
> Each with Evidence Grade A (syllabus ref) + policy id + decision id  

**Educational Reconciliation:**

> Coverage matrix summary node `kind=coverage_report`  
> Findings: covered / missing_concept / unexpected_concept /
> hierarchy_inconsistent / educationally_complete  
> Policy: `coverage_policy` · Grade: A for syllabus authority rows  

---

## Architecture updates

```
EducationalPolicy (base)
  ConceptFormationPolicy · ObjectivePolicy · CoveragePolicy
        ↓ executed by
ConceptFormationAgent (G4)
ObjectiveIntelligenceAgent (G5)
EducationalReconciliationAgent (G6)
        ↓
GenerationOrchestrator + RegressionGuard
  hard gates: coverage · noise · hierarchy · granularity
              · evidence_quality · confidence
        ↓
Immutable snapshots + Curriculum Memory lineage
  MERGED / SPLIT / REPARENTED recorded append-only
```

| Change | Detail |
|---|---|
| Gen 4 rename | `concept_formation` purpose; enum `CONCEPT_FORMATION` |
| Evidence on nodes | `EducationalNode.evidence_grade` + `policy_id` |
| Quality vector | `evidence_quality` metric |
| RegressionPolicy | ε + reject flags for granularity / evidence / confidence |
| Runners | `default_phase_c_runners()` wires G1–G6 Agents |
| Persistence | Grade/policy folded into node `attributes_json` (no migration) |

Laws preserved: snapshots write-once; rejected ≠ deleted; no LLM; CIP ingress /
Studio egress / Student Runtime untouched.

---

## Files Created

- `app/domain/curriculum_intelligence/evidence.py`
- `app/domain/curriculum_intelligence/policy.py`
- `app/application/curriculum_intelligence/policies/__init__.py`
- `app/application/curriculum_intelligence/policies/base.py`
- `app/application/curriculum_intelligence/policies/concept_formation_policy.py`
- `app/application/curriculum_intelligence/policies/objective_policy.py`
- `app/application/curriculum_intelligence/policies/coverage_policy.py`
- `app/application/curriculum_intelligence/agents/concept_formation_agent.py`
- `app/application/curriculum_intelligence/agents/objective_intelligence_agent.py`
- `app/application/curriculum_intelligence/agents/educational_reconciliation_agent.py`
- `tests/application/curriculum_intelligence/test_ei001c_educational_reasoning.py`
- `knowledge/engineering/ei001_curriculum_intelligence_engine/EI001C_IMPLEMENTATION_REPORT.md`

## Files Modified

- `app/domain/curriculum_intelligence/generation.py` — Concept Formation rename; evidence fields; RegressionPolicy; merge/split lineage
- `app/domain/curriculum_intelligence/agent.py` — `evidence_quality` in standard metrics
- `app/domain/curriculum_intelligence/__init__.py` — Evidence / Policy exports
- `app/application/curriculum_intelligence/agents/__init__.py` — Phase C agents + `default_phase_c_runners`
- `app/application/curriculum_intelligence/generation_quality.py` — evidence quality + concept-aware granularity
- `app/application/curriculum_intelligence/regression_guard.py` — extended hard gates
- `app/application/curriculum_intelligence/generation_hash.py` — fingerprint includes grade/policy
- `app/application/curriculum_intelligence/generation_orchestrator.py` — Phase C docstring
- `app/application/curriculum_intelligence/ports/calibration_router_port.py` — `CONCEPT_FORMATION`
- `app/infrastructure/adapters/curriculum_intelligence/generation_store.py` — hydrate evidence fields

---

## Tests Executed

```bash
python3 -m pytest tests/application/curriculum_intelligence/test_ei001c_educational_reasoning.py \
  tests/application/curriculum_intelligence/test_ei001b_generation_agents.py \
  tests/application/curriculum_intelligence/test_ei001a_generation_engine.py -q
# 30 passed

python3 -m pytest tests/application/curriculum_intelligence/test_educational_quality.py \
  tests/application/curriculum_intelligence/test_pipeline.py -q
# 21 passed (CIP + EQ-001 regression)

ruff check <EI-001C modules>
# All checks passed
```

Coverage exercised:

- Concept formation (merge / split / retain + lineage)  
- Objective attachment  
- Coverage matrix  
- Evidence grading  
- Regression (evidence / granularity / confidence rejection)  
- Policy execution / descriptors  
- Phase C reproducibility  
- Phase B compatibility  

---

## Migration Impact

**None.** Evidence grade and policy id persist via existing
`attributes_json` keys (`_evidence_grade`, `_policy_id`). No Alembic revision.
V1/V2 curriculum engine schema untouched.

---

## Architecture Compliance

- Layering Presentation → Application → Domain → Infra preserved.  
- Policies + Agents in application; EvidenceGrade / PolicyDescriptor /
  EducationalDecision in domain.  
- Curriculum V1/V2 traversal/import compatibility: **preserved (untouched)**.  
- CIP pipeline remains the document spine; EI Agents additive (not yet wired
  into `PipelineCoordinator` — Phase D+ shim).  
- No LLM in educational decisions.  

---

## Technical Debt

- Mini syllabus fixture yields retain-only Concept Formation; merge/split
  proven via synthetic nodes — full CMP ~936 coalescing awaits live CMP input.  
- Gen 6 unexpected-concept detection skips nodes with syllabus refs; CMP-only
  teaching assets need richer CmpInstructionPort binding (Phase D/F).  
- Competency verb lexicon is English heuristic; actuarial review of Review Packs
  should extend denylists/merge dictionaries (architecture limitation §16).  
- CIP dual-read / coordinator adapter period (EI-001 §10.3) not started.  

---

## Known Limitations

- No Certification Engine (Gen 7) — Phase D.  
- No Founder Calibration UI — Phase E.  
- No Student Runtime or publication changes.  
- Cross-diet 2019 CMP vs 2026 syllabus semantic gaps remain
  CERTIFIED_WITH_WARNINGS territory (Gen 7).  

---

## Remaining work

| Item | Phase |
|---|---|
| CertificationEngine + Review Pack | D |
| Studio structure prep reads certified snapshot | D |
| Calibration partial regen + Founder controls | E |
| Live CS1 republish dogfood (5/15/73 + CMP coherence) | F |

---

## FINAL DECISION

# PHASE C COMPLETE

Educational Policies are operational. Evidence grading (A–D) is operational.
Generations 4–6 are implemented (Concept Formation, Objective Intelligence,
Educational Reconciliation). Educational reasoning is demonstrated with
explainable decisions (reason · evidence · confidence · policy · grade).
RegressionGuard evaluates coverage, hierarchy, granularity, evidence quality,
and confidence and rejects regressions automatically. Curriculum Memory records
merge / split / reassignment. Existing CIP and Phase A/B tests remain green.
Certification, Founder calibration, and live republish remain deferred to
Phases D–F as designed.
