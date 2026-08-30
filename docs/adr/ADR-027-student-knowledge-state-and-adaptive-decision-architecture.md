# ADR: Student Knowledge State and Adaptive Decision Architecture

## Status

Proposed. Not implemented. Captures a target architecture and a set of
durable principles agreed after a dedicated architecture review. No
code changes are authorized by this document alone; it is the basis
for a subsequent empirical investigation and, later, an implementation
plan.

## Context

An independent architecture review found that Kwalitec currently has
no single authoritative model of what a given student knows. At least
six distinct signals coexist, each independently writable, with no
runtime precedence rule between them: Stage A `TopicProgress.mastery_score`,
the Digital Twin's own daily-loop Estimated Knowledge (stored
separately and never synced back to Stage A), a study-plan wizard
self-declaration path that can mark a topic complete with zero
recorded mastery, a session-evidence write-through path that is
currently disabled in production, Runtime C's own event-derived
coverage state (authoritative for its own spine, independent of Stage
A), and a Runtime C API named for Estimated Knowledge that is in fact
a hardcoded stub returning a negative result for every topic. Which of
these signals actually governs what a student sees or is recommended
next depends on which code path a given surface happens to call,
rather than on any explicit rule. Drift between these signals for a
real, engaged student was found to be the default outcome, not an edge
case.

The same review found that genuine per-student adaptive selection is
not currently the operative path in production at all. The mechanism
intended to provide it, the Digital Twin's daily plan, is gated behind
a flag that is off in production, so it returns no result
unconditionally, on every call. What a real student experiences today
is linear syllabus or campaign-order progression, with one narrow,
disclosed exception for Consolidation Mission checkpoints. Describing
current production behaviour as adaptive, in the sense of a decision
that follows from what the system knows about that student, is not
accurate for the current configuration.

There are currently no real students using Kwalitec in production.
Nothing is being actively harmed by this state today, and it is worth
treating that fact as a genuine opportunity: this is a rare window to
correct the underlying architecture before real learner data and
behaviour become entrenched around a fragmented model, rather than
retrofitting correctness onto a system already carrying live student
history.

## Decision

Kwalitec's learning-decision architecture will be organised around
the following seven components and the boundaries between them.

### Knowledge Engine

The Knowledge Engine is the computation and update mechanism that
turns accepted evidence into a change in what the system believes
about a learner. It is not a separate data store. Its output is
written directly into the Learner Twin's own state; there is no
independent Estimated Knowledge store that the Twin subsequently reads
from or has to stay in sync with. Collapsing the update mechanism and
its target into a single owned state is a deliberate choice, made
specifically to avoid recreating, with better intentions, the same
synchronisation problem this ADR exists to resolve.

### Learner Twin

The Learner Twin is the single authoritative representation of what
Kwalitec currently believes about a given student. It owns Estimated
Knowledge as its core state, alongside other interpretable facts about
that student: coverage of the curriculum, when a topic was last
practised, recent and historical performance, the reliability of the
current estimate, and other validated, student-specific signals
including that student's own exam proximity.

The Twin answers questions about a learner. It does not rank, weigh,
prioritise, or recommend anything. It may expose neutral derived
values that remain directly interpretable as facts, such as the number
of days since a topic was last practised. The moment a value stops
being a fact about the learner and starts encoding a judgement about
what matters more than what, such as a computed urgency or priority
score, it has crossed into policy and no longer belongs to the Twin.
This boundary exists specifically to prevent the Twin from gradually
accumulating decision logic and becoming a second, informal decision
engine alongside the one described below.

Study Progress, meaning whether a student has covered a given piece of
content, remains a genuinely separate concept from Estimated Knowledge
inside the Twin's state, with its own writer and its own meaning. The
two may correlate for a given student, but neither should be treated
as a proxy for the other anywhere in this architecture. This
separation is not new to this ADR; it reflects a principle already
established and deliberately protected earlier in this project's
history, and nothing in this architecture is permitted to collapse it.

### Curriculum State

Curriculum State is the syllabus structure a student is working
through: sections, topics, learning objectives, any prerequisite or
sequencing relationships that exist, and other structural constraints.
It is independent of any individual learner and is not owned by the
Twin. Whether explicit prerequisite relationships currently exist
anywhere in the codebase, and whether the first decision policy
actually needs them, are open questions for the investigation that
follows this ADR, not assumptions made here.

### Context

Context is genuinely global or system-level information that is not
specific to any one learner: consolidation cadence rules, study-phase
definitions, and other constraints that apply across students rather
than describing a particular student's situation. Information that is
specific to a given student, such as that student's own exam date or
how close they are to it, belongs to that student's state in the Twin,
not to Context. This distinction exists to stop Context from becoming
an unstructured place to put anything that does not obviously belong
elsewhere.

### Adaptive Decision Engine

The Adaptive Decision Engine determines what should happen next for a
given student. It is the only component in this architecture permitted
to make that determination. It receives Learner State from the Twin,
Curriculum State, and Context as its inputs, and produces a decision.

The Decision Engine's internal policy, meaning the actual logic it
uses to turn those inputs into a decision, is explicitly expected to
start simple and to evolve over time as real learner evidence
accumulates. The architectural boundary around the Decision Engine is
what this ADR fixes with confidence now; the sophistication of the
policy running inside that boundary is treated as a separate, later,
evidence-driven question, and building a more elaborate policy now
than the available evidence can justify is explicitly out of scope for
the first implementation.

The first policy behind this boundary, referred to here as Policy V0,
is the existing linear topic-selection logic, wrapped behind the new
Decision Engine interface with no intended change in behaviour. Its
purpose is to prove that decision-making authority has moved to the
correct architectural location without simultaneously changing what
that authority decides, so that a boundary change and a behaviour
change are never validated as a single, harder-to-diagnose step.

The Decision Engine must produce one of three explicit outcomes for
every decision it is asked to make: a genuinely adaptive decision was
produced; a genuinely adaptive decision could not be produced but a
valid deterministic action exists as a safe fallback; or neither is
available and the decision is blocked. Kwalitec must never present a
safe fallback outcome to a student as though it were an adaptive one.
These three states must be recorded from the first implementation
onward, so the system can be asked, from day one, how often it is
actually adaptive, how often and why it falls back, and how often it
is blocked, rather than that question remaining unanswerable until
some later point.

Whether the Decision Engine exposes one general interface that every
selection intent, such as daily topic selection, consolidation
targeting, and revision-mode selection, routes through, or several
intent-specific interfaces, is an open question this ADR deliberately
does not resolve. It should be settled once the investigation below
has established how those three intents actually work today, not
assumed in advance.

### Learning Orchestrator

The Learning Orchestrator is a thin coordination layer that calls the
Decision Engine to determine what should happen, and then calls
Runtime C to carry that decision out. Its purpose is to keep the
dependency direction clean: Runtime C is not permitted to call the
Decision Engine directly, and should have no knowledge that it exists.
Runtime C receives a decision to execute, not a request to decide.

### Runtime C

Runtime C retains responsibility for everything it already does well:
composing a session, its partnership with the CMP, the evidence gate,
and presentation and delivery of the learning experience. It loses
responsibility for deciding what a student should study. This is
described deliberately as a demotion of Runtime C's authority over
selection, not a replacement or rework of Runtime C as a whole; the
parts of Runtime C that are not about deciding what comes next are
expected to remain largely as they are.

### The complete loop

Evidence produced by a student's activity flows into the Knowledge
Engine, which updates the Learner Twin's state. The Adaptive Decision
Engine reads that state, together with Curriculum State and Context,
and produces a decision. The Learning Orchestrator carries that
decision to Runtime C, which composes and delivers the resulting
session. That session produces new evidence, and the loop repeats.

## Principles established

- Estimated Knowledge is part of the Learner Twin's own state. It is
  never a separate store the Twin has to read from or reconcile
  against.
- The Learner Twin answers questions about a learner. It never ranks,
  prioritises, or recommends.
- Study Progress and Estimated Knowledge remain two genuinely separate
  concepts inside the Twin, each with its own writer and its own
  meaning, and neither may be used as a proxy for the other.
- The Adaptive Decision Engine is the only component that decides what
  should happen next for a student.
- Runtime C executes and composes the decision it is given. It does
  not make that decision, and does not know how it was made.
- Every decision produces one of exactly three recorded outcomes:
  genuinely adaptive, safe deterministic fallback, or blocked. A safe
  fallback outcome must never be presented to a student as an adaptive
  one.
- Establishing that Estimated Knowledge is architecturally
  trustworthy, meaning it has a single writer, no unexplained
  divergence from anything that reads it, and a working drift
  detector, is a question this project can answer before real students
  exist. Establishing that Estimated Knowledge is pedagogically valid,
  meaning it actually predicts real exam-relevant competence, requires
  real learner evidence and cannot be answered yet. These are two
  different questions, are validated at different times, and neither
  may be substituted for the other.
- A deliberately simple first decision policy is acceptable, provided
  it sits behind the correct architectural boundary described above.
  A simple policy implemented as a growing set of conditions inside
  Runtime C itself is not an acceptable substitute for this
  architecture, however small it starts.
- The complexity of the decision policy is expected to grow over time,
  and that growth should be driven by real evidence, such as a
  sufficient volume of real decisions and outcomes or a recurring,
  identifiable failure pattern in the safe-fallback or blocked
  outcomes, rather than anticipated now.

## Open questions

These are explicitly left open by this ADR and are expected to be
narrowed by the empirical investigation that follows it, not decided
here.

- Whether the Adaptive Decision Engine should eventually become the
  single authoritative source of selection decisions across every
  learning spine in Kwalitec, or whether its authority is intentionally
  scoped to a subset of them at first, and if so which.
- Whether the Decision Engine exposes one general decision interface
  or several intent-specific ones, once the actual current behaviour
  of daily selection, consolidation targeting, and revision-mode
  selection is understood in detail.
- What the existing Digital Twin daily-loop mechanism, which is
  already live in production and already writes its own state,
  actually represents today, and whether it should become the
  foundation of the Learner Twin described here, be treated as an
  upstream evidence-processing step feeding it, or be retired.
- Whether explicit prerequisite relationships between curriculum
  topics exist anywhere in the current data model, and if not, whether
  the first decision policy can operate without them or whether a
  representation for them needs to be designed.
- The precise current call sites and behaviour of both existing
  selection mechanisms, and whether there are more than the two
  identified so far.

## Consequences

This architecture requires real implementation effort before it
produces any change a student would experience; it is not a
configuration change. It also means the first working version of
adaptive selection will be deliberately unambitious in its decision
logic, favouring the certainty that the boundary is correct over the
sophistication of what happens inside it. The intended benefit is that
later improvements to the decision policy should not require
restructuring the system around them, because the structure is
expected to have been established correctly the first time, ahead of
that policy's own development. The immediate next step following this
ADR is a read-only empirical investigation into the current codebase,
grounded strictly in what is actually implemented today rather than
in what this architecture assumes or intends, so that a concrete gap
analysis and migration plan can follow from evidence rather than from
this design conversation alone.
