# Product Experience Guidelines

**Status:** Permanent constitution  
**Authority:** PX-001 Product Experience Elevation  
**Audience:** Anyone who changes student- or Founder-facing presentation

These guidelines define *how Kwalitec must feel*. They do not define features, algorithms, curriculum, or architecture.

Future development must follow this document. When uncertain, ask:

> Does this help the user complete their next action?

If the answer is no — remove it.

---

## 1. Every screen has one purpose

- One primary question per screen.
- One primary action per screen.
- Secondary information must support that purpose or leave.

| Role | Screen purpose example |
|------|------------------------|
| Student Home | What should I do now? |
| Session Overview | Am I ready to begin? |
| Session Activity | Complete this practice. |
| Founder Home | What needs attention today? |
| Subjects | Find or create a subject. |
| Curriculum Studio workspace | Advance this publication. |

If a screen answers multiple questions, split the experience.

---

## 2. Guide before explaining

Kwalitec is a mentor, not documentation.

**Remove**

- Platform philosophy
- Educational philosophy essays
- Implementation explanations
- System behaviour narration
- Internal terminology
- Engineering language
- Framework descriptions

**Prefer**

- Short guidance that enables the next decision
- Progressive detail only when the user asks for it

Help may teach product vocabulary. Primary study and manage surfaces must not.

---

## 3. One piece of information, once

- No repeated titles, objectives, durations, subject names, or guidance on the same view.
- If Home shows the subject, Progress must not repeat it.
- If Overview shows the objective in context, do not restack the same sentence as a wall of briefing above the primary action.

---

## 4. Progressive disclosure

- Start with what is immediately actionable.
- Educational detail appears when the student opens it.
- Operational detail appears when the Founder needs it.
- Default open = only the next action and its essential context.

---

## 5. Empty states guide

Maximum structure:

1. Heading
2. One sentence
3. One action

Nothing else. No “why this is empty.” No philosophy. No second CTA.

---

## 6. Remove before adding

- Prefer deletion over decoration.
- Prefer quieter copy over clever copy.
- Prefer one clear CTA over a row of alternatives.
- Do not add features, workflows, configuration, AI, or educational-logic changes under the guise of “experience.”

---

## 7. Navigation describes workflows

| Audience | Navigation should reflect |
|----------|---------------------------|
| Student | Studying |
| Founder | Managing |

Labels must match page titles. Nav items belong to logical groups. Navigation must not expose implementation names.

---

## 8. Product language

Every sentence must help a decision.

| Do | Don’t |
|----|--------|
| Short | Verbose |
| Confident | Academic |
| Helpful | Technical |
| Specific | Repetitive |

Banned on primary surfaces: explaining the product to itself, milestone IDs, runtime names, dual-run language, “operator,” “epistemology,” “feedback loop” as a student label.

---

## 9. Interactions feel finished

Audit and complete:

- Modal dismissal
- Toast behaviour
- Alignment and spacing
- Hover and focus states
- Loading states
- Button hierarchy
- Animations (presence, not noise)
- Keyboard navigation
- Scrolling

Unfinished interactions are defects.

---

## 10. Visual rhythm

Pages must feel calm.

- Clear typography hierarchy
- Consistent spacing scale
- No visual crowding
- No oversized paragraphs
- No oversized cards for passive content
- Cards only when they contain interaction

---

## Change control

- Experience work may change templates, presentation DTOs, copy constants, and design-system macros.
- Experience work must **not** change Runtime C, SCI lifecycle, recommendation algorithms, curriculum truth, or Founder capability scope.
- New programmes that touch UI must cite compliance with this constitution in their completion report.
