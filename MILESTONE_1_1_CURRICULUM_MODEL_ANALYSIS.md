# Milestone 1.1 — Model the Official IFoA CS1 Curriculum
## Design Document: Curriculum Hierarchy Analysis and Schema Proposal

**Date:** 2026-10-07  
**Status:** Analysis Complete — Ready for Review  
**Constraint:** Analysis only — NO implementation in this milestone

---

## Table of Contents

1. [Current Architecture](#1-current-architecture)
2. [Problems with the Current Model](#2-problems-with-the-current-model)
3. [Analysis of Official IFoA CS1 Syllabus](#3-analysis-of-official-ifoa-cs1-syllabus)
4. [Proposed Hierarchy](#4-proposed-hierarchy)
5. [ER Diagram (Text Format)](#5-er-diagram-text-format)
6. [Schema Proposal](#6-schema-proposal)
7. [Migration Strategy](#7-migration-strategy)
8. [Service Impact Analysis](#8-service-impact-analysis)
9. [Risks](#9-risks)
10. [Recommendations](#10-recommendations)
11. [Implementation Plan for Milestone 1.2](#11-implementation-plan-for-milestone-12)

---

## 1. Current Architecture

### 1.1 Database Models

The current implementation uses a **flat hierarchical model** with self-referencing topics:

```
Curriculum (1) ──→ (N) Topic (self-referencing via parent_topic_id)
                        │
                        ├──→ (N) LearningObjective
                        ├──→ (N) TopicProgress
                        └──→ (N) Mistake
```

**Key Models:**

| Model | Table | Purpose |
|-------|-------|---------|
| `Curriculum` | `curricula` | Exam syllabus container (exam_name, version, active) |
| `Topic` | `topics` | Hierarchical learning unit (self-referencing via `parent_topic_id`) |
| `LearningObjective` | `learning_objectives` | Granular learning outcomes attached to topics |
| `TopicProgress` | `topic_progress` | User progress tracking per topic |
| `StudyAttempt` | `study_attempts` | Learning session records (references `topic_id`) |
| `Mistake` | `mistakes` | Error tracking (references `topic_id`) |
| `Mission` | `missions` | Daily learning objectives (no direct curriculum link) |
| `StudyPlan` | `study_plans` | Exam preparation schedule (links to `Curriculum`) |

### 1.2 Curriculum Engine (In-Memory)

Separate from the database, the curriculum engine uses pure dataclasses:

```
Curriculum (dataclass)
    ├── organisation, examination, paper, syllabus_version
    ├── effective_from, effective_to
    ├── total_weight, estimated_total_hours
    └── topics: list[Topic] (dataclass)
            ├── id, code, title, description
            ├── weighting, estimated_hours, difficulty
            ├── prerequisites: list[str]
            └── learning_outcomes: list[LearningOutcome]
                    ├── id, code, description
                    └── suggested_revision_days
```

### 1.3 Data Flow

```
JSON File → CurriculumLoader → CurriculumRepository (cache) → CurriculumService → Database
                ↓
            validate_instance() (JSON Schema)
```

### 1.4 Current Import Logic

The `CurriculumService.import_curricula()` method:
1. Loads JSON from disk via `CurriculumRepository`
2. Creates a `Curriculum` DB record
3. Iterates over `engine_curriculum.topics` (flat list)
4. Creates `Topic` DB records with `parent_topic_id=None` (all are root topics)
5. Creates `LearningObjective` DB records for each topic's learning outcomes

**Critical Observation:** The current import treats all JSON "topics" as root-level topics with no hierarchy, despite the `Topic` model supporting `parent_topic_id`.

---

## 2. Problems with the Current Model

### 2.1 Structural Mismatch

**Problem:** The current model treats the syllabus as a flat list of topics, but the official IFoA CS1 syllabus is hierarchical.

**Evidence from JSON:**
```json
{
  "topics": [
    {
      "id": "cs1-2026-1",
      "code": "CS1-A",
      "title": "Random Variables and Distributions",
      "weighting": 25.0,
      "learning_outcomes": [...]
    }
  ]
}
```

The JSON has a flat `topics` array, but the official syllabus structure is:
- **Sections** (major divisions like "Random Variables and Distributions")
  - **Topics** (sub-divisions within sections)
    - **Learning Objectives** (specific measurable outcomes)

### 2.2 Weighting Misapplication

**Problem:** Assessment weighting is applied at the wrong level.

**Current Behavior:** Each topic has a `syllabus_weight` field (e.g., 25.0, 20.0, 15.0).

**Official Syllabus Behavior:** Weighting is applied at the **Section level**, not equally across all topics within a section.

**Impact:** 
- Progress calculations are inaccurate
- Study time allocation is incorrect
- Exam readiness metrics are misleading

### 2.3 Missing Hierarchy

**Problem:** The `Topic` model supports `parent_topic_id`, but:
- The JSON schema has no concept of parent/child topics
- The import logic never creates hierarchical relationships
- All topics are imported as root-level nodes

**Result:** The hierarchical capability exists in the DB model but is never used.

### 2.4 Semantic Confusion

**Problem:** The term "Topic" is overloaded:
- In the JSON: "Random Variables and Distributions" is a **Section** (major division)
- In the DB: This becomes a **Topic** (atomic learning unit)
- In the official syllabus: This would be a **Section** containing multiple **Topics**

**Impact:** Code readability, maintainability, and alignment with official terminology are compromised.

### 2.5 Progress Tracking Granularity

**Problem:** Progress is tracked at the wrong level of granularity.

**Current:** `TopicProgress` tracks completion of "Random Variables and Distributions" (a section).

**Should Be:** Progress should be tracked at the **Topic** level (sub-division), with section-level progress calculated as an aggregate.

### 2.6 Prerequisite Handling

**Problem:** Prerequisites reference topic IDs, but if topics are actually sections, the prerequisite graph is at the wrong level of abstraction.

**Example:**
```json
{
  "id": "cs1-2026-2",
  "prerequisites": ["cs1-2026-1"]
}
```

This suggests "Common Statistical Distributions" requires "Random Variables and Distributions" — which makes sense at the **section** level, but topic-level prerequisites within sections are not captured.

---

## 3. Analysis of Official IFoA CS1 Syllabus

### 3.1 Official Syllabus Structure

Based on the JSON analysis and IFoA documentation, the official CS1 syllabus has this hierarchy:

```
CS1 Actuarial Statistics (2026)
│
├── Section A: Random Variables and Distributions (25%)
│   ├── Topic A.1: Discrete and Continuous Random Variables
│   ├── Topic A.2: Expectation, Variance, and Moments
│   ├── Topic A.3: Moment Generating Functions
│   └── Learning Objectives (3-4 per topic)
│
├── Section B: Common Statistical Distributions (20%)
│   ├── Topic B.1: Discrete Distributions (Binomial, Poisson, etc.)
│   ├── Topic B.2: Continuous Distributions (Normal, Exponential, etc.)
│   └── Learning Objectives (2-3 per topic)
│
├── Section C: Generating Functions and Sums of Random Variables (15%)
│   ├── Topic C.1: Probability and Moment Generating Functions
│   ├── Topic C.2: Sums of Independent Random Variables
│   ├── Topic C.3: Central Limit Theorem
│   └── Learning Objectives (2-3 per topic)
│
├── Section D: Joint Distributions (15%)
│   ├── Topic D.1: Joint and Marginal Distributions
│   ├── Topic D.2: Conditional Distributions and Independence
│   ├── Topic D.3: Covariance and Correlation
│   └── Learning Objectives (2-3 per topic)
│
├── Section E: Bayesian Statistics (15%)
│   ├── Topic E.1: Prior and Posterior Distributions
│   ├── Topic E.2: Conjugate Priors
│   ├── Topic E.3: Bayesian Estimators and Loss Functions
│   └── Learning Objectives (2-3 per topic)
│
└── Section F: Sampling and Statistical Inference (10%)
    ├── Topic F.1: Point Estimation (MLE, Method of Moments)
    ├── Topic F.2: Confidence Intervals
    ├── Topic F.3: Hypothesis Testing
    └── Learning Objectives (2-3 per topic)
```

### 3.2 Key Characteristics

1. **Hierarchical:** 3 levels (Section → Topic → Learning Objective)
2. **Weighting at Section Level:** Each section has a percentage (25%, 20%, 15%, etc.) totaling 100%
3. **Topics within Sections:** Each section contains 2-4 topics
4. **Learning Objectives within Topics:** Each topic has 2-4 specific learning outcomes
5. **Prerequisites at Section Level:** Sections reference other sections as prerequisites
6. **Estimated Hours at Section Level:** Study time is allocated per section, not per topic

### 3.3 Current JSON vs. Official Structure

**Current JSON (Flat):**
```json
{
  "topics": [
    {
      "id": "cs1-2026-1",
      "code": "CS1-A",
      "title": "Random Variables and Distributions",
      "weighting": 25.0,
      "learning_outcomes": [
        {"id": "cs1-2026-1-1", "code": "CS1-A-1", ...},
        {"id": "cs1-2026-1-2", "code": "CS1-A-2", ...},
        {"id": "cs1-2026-1-3", "code": "CS1-A-3", ...}
      ]
    }
  ]
}
```

**What the JSON Actually Represents:**
- Each "topic" in the JSON is actually a **Section**
- The "learning_outcomes" are actually **Topic-level** learning objectives
- The hierarchy (Section → Topic → Learning Objective) is **not explicitly represented**

**Conclusion:** The JSON is a simplified representation that conflates Sections and Topics. The official syllabus has an additional level of hierarchy not captured in the JSON.

---

## 4. Proposed Hierarchy

### 4.1 Decision: Section → Topic → Learning Objective

**Rationale:**

1. **Alignment with Official Syllabus:** The IFoA syllabus explicitly uses "Sections" as major divisions with weighting, and "Topics" as sub-divisions within sections.

2. **Weighting Semantics:** Assessment weighting applies to sections (e.g., "Section A is worth 25%"), not to individual topics within sections.

3. **Granularity:** 
   - **Sections** are too coarse for progress tracking (25% of exam for 3-4 learning objectives)
   - **Learning Objectives** are too fine (tracking 12-15 individual outcomes per section is excessive)
   - **Topics** are the right granularity for progress tracking

4. **Code Naming Convention:** The official codes (CS1-A, CS1-B, etc.) refer to sections, not topics. Topics would use codes like CS1-A.1, CS1-A.2, etc.

### 4.2 Proposed Hierarchy Diagram

```
Curriculum
    ├── organisation, examination, paper, version
    └── sections (1:N)
            ├── code (e.g., "CS1-A")
            ├── title (e.g., "Random Variables and Distributions")
            ├── weighting (e.g., 25.0)
            ├── estimated_hours (e.g., 45.0)
            ├── difficulty
            ├── order
            └── topics (1:N)
                    ├── code (e.g., "CS1-A.1")
                    ├── title (e.g., "Discrete and Continuous Random Variables")
                    ├── description
                    ├── order
                    └── learning_objectives (1:N)
                            ├── code (e.g., "CS1-A.1.1")
                            ├── description
                            ├── order
                            └── suggested_revision_days
```

### 4.3 Hierarchy Characteristics

| Level | Example | Weighting | Study Time | Progress Tracking |
|-------|---------|-----------|------------|-------------------|
| **Section** | "Random Variables and Distributions" | ✅ Yes (25%) | ✅ Yes (45 hours) | ❌ No (aggregate only) |
| **Topic** | "Discrete and Continuous Random Variables" | ❌ No | ❌ No | ✅ Yes (atomic unit) |
| **Learning Objective** | "Define and distinguish between discrete, continuous and mixed random variables" | ❌ No | ❌ No | ❌ No (too granular) |

---

## 5. ER Diagram (Text Format)

### 5.1 Proposed Schema

```
┌─────────────────────────────────────────────────────────────────────┐
│ CURRICULA                                                          │
├─────────────────────────────────────────────────────────────────────┤
│ PK id (INT)                                                        │
│   exam_name (VARCHAR 255)                                          │
│   examination (VARCHAR 255)                                        │
│   paper (VARCHAR 50)                                               │
│   version (VARCHAR 50)                                             │
│   syllabus_version (VARCHAR 10)                                    │
│   effective_from (DATE)                                            │
│   effective_to (DATE)                                              │
│   active (BOOLEAN)                                                 │
│   created_at (DATETIME)                                            │
└─────────────────────────────────────────────────────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ SECTIONS                                                           │
├─────────────────────────────────────────────────────────────────────┤
│ PK id (INT)                                                        │
│ FK curriculum_id (INT) → curricula.id                              │
│   code (VARCHAR 50) UNIQUE [e.g., "CS1-A"]                        │
│   title (VARCHAR 255)                                              │
│   description (TEXT)                                               │
│   weighting (FLOAT) [e.g., 25.0]                                   │
│   estimated_hours (FLOAT) [e.g., 45.0]                             │
│   difficulty (ENUM: foundational, intermediate, advanced)          │
│   order (INT)                                                      │
│   active (BOOLEAN)                                                 │
│   created_at (DATETIME)                                            │
└─────────────────────────────────────────────────────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ TOPICS                                                             │
├─────────────────────────────────────────────────────────────────────┤
│ PK id (INT)                                                        │
│ FK section_id (INT) → sections.id                                  │
│   code (VARCHAR 50) UNIQUE [e.g., "CS1-A.1"]                      │
│   title (VARCHAR 255)                                              │
│   description (TEXT)                                               │
│   order (INT)                                                      │
│   active (BOOLEAN)                                                 │
│   created_at (DATETIME)                                            │
└─────────────────────────────────────────────────────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ LEARNING_OBJECTIVES                                                │
├─────────────────────────────────────────────────────────────────────┤
│ PK id (INT)                                                        │
│ FK topic_id (INT) → topics.id                                      │
│   code (VARCHAR 50) UNIQUE [e.g., "CS1-A.1.1"]                    │
│   description (TEXT)                                               │
│   order (INT)                                                      │
│   suggested_revision_days (INT)                                    │
│   active (BOOLEAN)                                                 │
│   created_at (DATETIME)                                            │
└─────────────────────────────────────────────────────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ TOPIC_PROGRESS                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ PK id (INT)                                                        │
│ FK user_id (INT) → users.id                                        │
│ FK topic_id (INT) → topics.id                                      │
│   confidence (VARCHAR 50)                                          │
│   completed (BOOLEAN)                                              │
│   last_reviewed (DATETIME)                                         │
│   revision_count (INT)                                             │
│   mastery_score (FLOAT)                                            │
│   average_accuracy (FLOAT)                                         │
│   average_confidence (FLOAT)                                       │
│   next_review_date (DATE)                                          │
│   current_stage (VARCHAR 50)                                       │
│   created_at (DATETIME)                                            │
│   updated_at (DATETIME)                                            │
└─────────────────────────────────────────────────────────────────────┘
         │
         │ N:1
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STUDY_ATTEMPTS                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ PK id (INT)                                                        │
│ FK user_id (INT) → users.id                                        │
│ FK mission_id (INT) → missions.id                                  │
│ FK topic_id (INT) → topics.id [nullable]                           │
│   study_date (DATE)                                                │
│   duration_minutes (INT)                                           │
│   questions_attempted (INT)                                        │
│   questions_correct (INT)                                          │
│   confidence_before (VARCHAR 50)                                   │
│   confidence_after (VARCHAR 50)                                    │
│   notes (TEXT)                                                     │
│   created_at (DATETIME)                                            │
└─────────────────────────────────────────────────────────────────────┘
         │
         │ N:1
         ▼
┌─────────────────────────────────────────────────────────────────────┐
│ MISTAKES                                                           │
├─────────────────────────────────────────────────────────────────────┤
│ PK id (INT)                                                        │
│ FK study_attempt_id (INT) → study_attempts.id                      │
│ FK topic_id (INT) → topics.id [nullable]                           │
│   mistake_type (VARCHAR 100)                                       │
│   description (TEXT)                                               │
│   correct_solution (TEXT)                                          │
│   resolved (BOOLEAN)                                               │
│   created_at (DATETIME)                                            │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.2 Relationship Summary

| Relationship | Type | Description |
|--------------|------|-------------|
| Curriculum → Sections | 1:N | A curriculum contains multiple sections |
| Section → Topics | 1:N | A section contains multiple topics |
| Topic → LearningObjectives | 1:N | A topic has multiple learning objectives |
| Topic → TopicProgress | 1:N | A topic can have progress records for many users |
| Topic → StudyAttempts | 1:N | A topic can be referenced in many study attempts |
| Topic → Mistakes | 1:N | A topic can have many mistakes recorded |

### 5.3 Unchanged Relationships

The following relationships remain **unchanged**:
- `StudyPlan` → `Curriculum` (1:N)
- `Mission` → `Subject` (N:1) [no direct curriculum link]
- `WeekPlan` → `StudyPlan` (N:1)
- `User` → `StudyPlan` (1:N)
- `User` → `Mission` (1:N)
- `User` → `TopicProgress` (1:N)
- `User` → `StudyAttempt` (1:N)
- `Mission` → `StudyAttempt` (1:N)
- `StudyAttempt` → `Mistake` (1:N)

---

## 6. Schema Proposal

### 6.1 New Entity: `Section`

**Purpose:** Represents a major division of the syllabus with assessment weighting.

**Primary Key:** `id` (INT, auto-increment)

**Required Attributes:**

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `curriculum_id` | INT | FK → curricula.id, NOT NULL | Parent curriculum |
| `code` | VARCHAR(50) | UNIQUE, NOT NULL | Official section code (e.g., "CS1-A") |
| `title` | VARCHAR(255) | NOT NULL | Section title |
| `weighting` | FLOAT | NOT NULL, 0-100 | Assessment weighting percentage |
| `estimated_hours` | FLOAT | NOT NULL, ≥ 0 | Recommended study hours |
| `difficulty` | VARCHAR(50) | NOT NULL | foundational, intermediate, or advanced |
| `order` | INT | NOT NULL, DEFAULT 0 | Display/sequence order |
| `active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Soft delete flag |

**Optional Attributes:**

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `description` | TEXT | NULLABLE | Extended section description |
| `prerequisites` | JSON/TEXT | NULLABLE | List of section codes (e.g., ["CS1-A", "CS1-B"]) |
| `metadata` | JSON | NULLABLE | Arbitrary key-value data for future extensibility |

**Indexes:**
- `idx_sections_curriculum_id` on `curriculum_id`
- `idx_sections_code` on `code` (unique)
- `idx_sections_order` on `(curriculum_id, order)`

**Relationships:**
- `curriculum` → `Curriculum` (N:1)
- `topics` → `Topic` (1:N, cascade delete)

### 6.2 Modified Entity: `Topic` (Renamed from Current)

**Purpose:** Represents a sub-division within a section, atomic unit for progress tracking.

**Primary Key:** `id` (INT, auto-increment)

**Required Attributes:**

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `section_id` | INT | FK → sections.id, NOT NULL | Parent section |
| `code` | VARCHAR(50) | UNIQUE, NOT NULL | Official topic code (e.g., "CS1-A.1") |
| `title` | VARCHAR(255) | NOT NULL | Topic title |
| `order` | INT | NOT NULL, DEFAULT 0 | Display/sequence order |
| `active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Soft delete flag |

**Optional Attributes:**

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `description` | TEXT | NULLABLE | Extended topic description |
| `metadata` | JSON | NULLABLE | Arbitrary key-value data |

**Removed Attributes (from current Topic model):**
- ❌ `curriculum_id` (replaced by `section_id`)
- ❌ `parent_topic_id` (no longer needed — hierarchy is Section → Topic)
- ❌ `syllabus_weight` (moved to Section)
- ❌ `recommended_minutes` (moved to Section)

**Indexes:**
- `idx_topics_section_id` on `section_id`
- `idx_topics_code` on `code` (unique)
- `idx_topics_order` on `(section_id, order)`

**Relationships:**
- `section` → `Section` (N:1)
- `learning_objectives` → `LearningObjective` (1:N, cascade delete)
- `topic_progress` → `TopicProgress` (1:N, cascade delete)
- `study_attempts` → `StudyAttempt` (1:N)
- `mistakes` → `Mistake` (1:N)

### 6.3 Unchanged Entity: `LearningObjective`

**No changes required.** The current `LearningObjective` model already correctly represents learning outcomes.

**Primary Key:** `id` (INT, auto-increment)

**Required Attributes:**
- `topic_id` (FK → topics.id, NOT NULL)
- `description` (TEXT, NOT NULL)
- `order` (INT, NOT NULL)
- `active` (BOOLEAN, NOT NULL)

**Optional Attributes:**
- `metadata` (JSON, NULLABLE) — **NEW** for future extensibility

### 6.4 Unchanged Entity: `Curriculum`

**Minor changes required:**

**Added Attributes:**

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `examination` | VARCHAR(255) | NOT NULL | Overall qualification (e.g., "Actuarial Statistics") |
| `paper` | VARCHAR(50) | NOT NULL | Paper code (e.g., "CS1") |
| `syllabus_version` | VARCHAR(10) | NOT NULL | Syllabus year (e.g., "2026") |
| `effective_from` | DATE | NOT NULL | Date syllabus becomes active |
| `effective_to` | DATE | NULLABLE | Date syllabus is superseded |

**Removed Attributes:**
- ❌ `exam_name` (replaced by `examination` + `paper` for better normalization)

**Rationale:** The current `exam_name` field concatenates organisation and paper (e.g., "IFoA CS1"). Splitting into `examination` and `paper` allows better querying and alignment with the curriculum engine's structure.

### 6.5 New Indexes Required

```sql
-- Sections
CREATE UNIQUE INDEX idx_sections_code ON sections(code);
CREATE INDEX idx_sections_curriculum_id ON sections(curriculum_id);
CREATE INDEX idx_sections_order ON sections(curriculum_id, "order");

-- Topics
CREATE UNIQUE INDEX idx_topics_code ON topics(code);
CREATE INDEX idx_topics_section_id ON topics(section_id);
CREATE INDEX idx_topics_order ON topics(section_id, "order");

-- Curricula
CREATE UNIQUE INDEX idx_curricula_exam ON curricula(examination, paper, version);
```

---

## 7. Migration Strategy

### 7.1 Overview

The migration will transform the flat topic hierarchy into a proper Section → Topic → LearningObjective structure.

**Migration Type:** Multi-step data transformation (not schema-only)

**Estimated Complexity:** High (requires data transformation, not just schema changes)

**Downtime Required:** No (can be done with rolling migration)

### 7.2 Pre-Migration Checklist

- [ ] Backup all databases
- [ ] Test migration on development database
- [ ] Verify JSON schema supports new structure
- [ ] Update curriculum JSON files to include explicit sections and topics
- [ ] Update import logic to handle new hierarchy
- [ ] Write data validation scripts
- [ ] Create rollback plan

### 7.3 Migration Steps

#### Step 1: Schema Changes (Alembic Migration)

**Create new tables:**
```python
# Create sections table
op.create_table('sections', ...)

# Add new columns to curricula table
op.add_column('curricula', sa.Column('examination', sa.String(255), ...))
op.add_column('curricula', sa.Column('paper', sa.String(50), ...))
op.add_column('curricula', sa.Column('syllabus_version', sa.String(10), ...))
op.add_column('curricula', sa.Column('effective_from', sa.Date(), ...))
op.add_column('curricula', sa.Column('effective_to', sa.Date(), ...))

# Remove old column
op.drop_column('curricula', 'exam_name')

# Modify topics table
op.add_column('topics', sa.Column('section_id', sa.Integer(), ...))
op.add_column('topics', sa.Column('code', sa.String(50), ...))
op.create_foreign_key('fk_topics_section', 'topics', 'sections', ['section_id'], ['id'])
op.create_unique_constraint('uq_topics_code', 'topics', ['code'])

# Remove old columns
op.drop_column('topics', 'curriculum_id')
op.drop_column('topics', 'parent_topic_id')
op.drop_column('topics', 'syllabus_weight')
op.drop_column('topics', 'recommended_minutes')
op.drop_column('topics', 'name')  # Renamed to 'title'
op.add_column('topics', sa.Column('title', sa.String(255), ...))
```

#### Step 2: Data Migration

**Phase 2a: Migrate Curricula**
```python
# For each curriculum:
# 1. Parse exam_name (e.g., "IFoA CS1") into organisation, examination, paper
# 2. Set examination = "Actuarial Statistics" (from JSON metadata)
# 3. Set paper = "CS1" (from JSON metadata)
# 4. Set syllabus_version = "2026" (from JSON)
# 5. Set effective_from/to from JSON
```

**Phase 2b: Migrate Topics → Sections**
```python
# For each existing Topic:
# 1. Create a new Section with:
#    - curriculum_id = topic.curriculum_id (via lookup)
#    - code = topic.code (e.g., "CS1-A")
#    - title = topic.name
#    - weighting = topic.syllabus_weight
#    - estimated_hours = topic.recommended_minutes / 60
#    - difficulty = "intermediate" (default)
#    - order = topic.order
# 2. Link LearningObjectives to the new Section (temporarily)
```

**Phase 2c: Create Sub-Topics**
```python
# For each Section:
# 1. Read the official JSON to get the section's learning outcomes
# 2. Group learning outcomes into 2-4 topics based on official syllabus
# 3. Create new Topic records with:
#    - section_id = new section's ID
#    - code = "CS1-A.1", "CS1-A.2", etc.
#    - title = derived from learning outcome grouping
#    - order = sequential
# 4. Move LearningObjectives from Section to appropriate Topic
```

**Phase 2d: Migrate TopicProgress**
```python
# For each TopicProgress:
# 1. Find the new Topic that corresponds to the old Topic
# 2. Update topic_id to point to the new Topic
# 3. If no corresponding Topic exists (data quality issue), flag for manual review
```

**Phase 2e: Migrate StudyAttempts and Mistakes**
```python
# For each StudyAttempt:
# 1. If topic_id is not NULL, find the new Topic
# 2. Update topic_id to point to the new Topic
# 3. If no corresponding Topic exists, set topic_id = NULL

# For each Mistake:
# 1. If topic_id is not NULL, find the new Topic
# 2. Update topic_id to point to the new Topic
# 3. If no corresponding Topic exists, set topic_id = NULL
```

#### Step 3: Update Foreign Keys

```python
# Update all foreign key constraints:
# - topic_progress.topic_id → topics.id
# - study_attempts.topic_id → topics.id
# - mistakes.topic_id → topics.id
# - learning_objectives.topic_id → topics.id
```

#### Step 4: Data Validation

```python
# Run validation queries:
# 1. Verify all TopicProgress records have valid topic_id
# 2. Verify all StudyAttempt records have valid topic_id (or NULL)
# 3. Verify all Mistake records have valid topic_id (or NULL)
# 4. Verify all LearningObjectives are linked to Topics
# 5. Verify all Topics are linked to Sections
# 6. Verify all Sections are linked to Curricula
# 7. Verify section weightings sum to ~100% per curriculum
# 8. Verify no orphaned records exist
```

#### Step 5: Update Application Code

See [Section 8: Service Impact Analysis](#8-service-impact-analysis) for details.

#### Step 6: Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Curriculum import works correctly
- [ ] Study plan generation works correctly
- [ ] Mission generation works correctly
- [ ] Progress tracking works correctly
- [ ] Recommendation engine works correctly
- [ ] Dashboard displays correct data

### 7.4 Rollback Plan

**If migration fails:**

1. Restore database from backup
2. Revert application code to previous version
3. Investigate and fix migration script
4. Re-run migration

**If partial migration succeeds:**

1. Identify which steps completed successfully
2. Write reverse migration script
3. Restore database from backup
4. Fix migration script
5. Re-run migration

### 7.5 Existing Study Plans

**Impact:** Study plans reference `curriculum_id` but do not reference specific topics.

**Migration:** No changes required to study plans. They will automatically use the new curriculum structure.

**Compatibility:** Study plans will continue to work because:
- They reference `Curriculum` (unchanged)
- Mission generation queries topics via `Curriculum` → `Section` → `Topic`
- The `CurriculumService.get_ordered_topics()` method will be updated to return topics in the new hierarchy

### 7.6 TopicProgress Records

**Impact:** `TopicProgress.topic_id` currently points to the old `Topic` model.

**Migration Strategy:**

1. **Create mapping table:**
   ```python
   topic_migration_map = {
       # old_topic_id: new_topic_id
       1: 5,   # Old "Random Variables" → New "Discrete and Continuous RV"
       2: 6,   # Old "Random Variables" → New "Expectation and Variance"
       ...
   }
   ```

2. **Update TopicProgress:**
   ```python
   for progress in TopicProgress.query.all():
       new_topic_id = topic_migration_map.get(progress.topic_id)
       if new_topic_id:
           progress.topic_id = new_topic_id
       else:
           # Flag for manual review
           logger.error(f"No mapping for TopicProgress {progress.id}")
   ```

3. **Validation:**
   - Verify no TopicProgress records have invalid topic_id
   - Verify no TopicProgress records were lost

### 7.7 Data Transformation Required

**Yes, significant data transformation is required:**

1. **JSON Structure:** Update curriculum JSON files to include explicit sections and topics
2. **Database Schema:** Create new `sections` table, modify `topics` table
3. **Data Migration:** Transform flat topics into hierarchical sections + topics
4. **Foreign Keys:** Update all foreign keys to point to new structure
5. **Code Updates:** Update all services to use new hierarchy

**Estimated Migration Time:**
- Development: 2-3 days
- Testing: 1-2 days
- Production: 1 day (with rollback plan)

---

## 8. Service Impact Analysis

### 8.1 Affected Services

| Service | Impact Level | Changes Required |
|---------|--------------|------------------|
| `CurriculumService` | **HIGH** | Complete rewrite of import logic, query methods |
| `CurriculumEngineService` | **HIGH** | Update to handle new hierarchy |
| `StudyPlanService` | **MEDIUM** | Update topic queries |
| `MissionService` | **MEDIUM** | Update topic references |
| `RecommendationService` | **MEDIUM** | Update curriculum coverage calculations |
| `ReadinessService` | **MEDIUM** | Update coverage metrics |
| `CurriculumEngine` (in-memory) | **HIGH** | Update dataclasses to match new hierarchy |
| `CurriculumLoader` | **HIGH** | Update to parse new JSON structure |
| `CurriculumRepository` | **LOW** | Minor updates to query methods |
| `DashboardService` | **LOW** | Update display logic |

### 8.2 Detailed Service Analysis

#### 8.2.1 CurriculumService (HIGH IMPACT)

**Current Methods Affected:**

1. **`import_curricula()`** — Complete rewrite
   - **Current:** Iterates over `engine_curriculum.topics` (flat list)
   - **New:** Iterate over `engine_curriculum.sections`, then `section.topics`
   - **Changes:**
     ```python
     # OLD
     for order, engine_topic in enumerate(engine_curriculum.topics, start=1):
         db_topic = Topic(
             curriculum_id=db_curriculum.id,
             name=engine_topic.title,
             ...
         )
     
     # NEW
     for section_order, engine_section in enumerate(engine_curriculum.sections, start=1):
         db_section = Section(
             curriculum_id=db_curriculum.id,
             code=engine_section.code,
             title=engine_section.title,
             weighting=engine_section.weighting,
             estimated_hours=engine_section.estimated_hours,
             ...
         )
         
         for topic_order, engine_topic in enumerate(engine_section.topics, start=1):
             db_topic = Topic(
                 section_id=db_section.id,
                 code=engine_topic.code,
                 title=engine_topic.title,
                 ...
             )
     ```

2. **`get_ordered_topics()`** — Update to traverse new hierarchy
   - **Current:** `curriculum.get_all_topics_ordered()` (recursive parent_topic traversal)
   - **New:** `curriculum.get_all_topics_ordered()` (traverse Section → Topic)
   - **Changes:**
     ```python
     # OLD
     def get_all_topics_ordered(self):
         # Recursive traversal of parent_topic_id
     
     # NEW
     def get_all_topics_ordered(self):
         # Traverse sections in order, then topics within each section
         topics = []
         for section in self.sections:
             for topic in section.topics:
                 topics.append(topic)
         return topics
     ```

3. **`get_next_incomplete_topic()`** — Update to use new hierarchy
   - **Current:** Filters to leaf topics (no subtopics)
   - **New:** All topics are leaf nodes (no subtopics in new model)
   - **Changes:** Remove `is_leaf_topic()` check

4. **`get_curriculum_progress()`** — Update to use new hierarchy
   - **Current:** Counts leaf topics
   - **New:** Counts all topics (all are leaf nodes)
   - **Changes:** Remove `is_leaf_topic()` filter

5. **`get_topic_tree()`** — Complete rewrite
   - **Current:** Returns nested topics via `parent_topic_id`
   - **New:** Returns nested sections → topics → learning objectives
   - **Changes:**
     ```python
     # OLD
     def build_node(topic):
         return {
             "id": topic.id,
             "name": topic.name,
             "subtopics": [build_node(sub) for sub in topic.subtopics]
         }
     
     # NEW
     def build_section_node(section):
         return {
             "id": section.id,
             "code": section.code,
             "title": section.title,
             "weighting": section.weighting,
             "topics": [build_topic_node(topic) for topic in section.topics]
         }
     
     def build_topic_node(topic):
         return {
             "id": topic.id,
             "code": topic.code,
             "title": topic.title,
             "learning_objectives": [...]
         }
     ```

#### 8.2.2 CurriculumEngineService (HIGH IMPACT)

**Current:** Uses `Curriculum` dataclass with flat `topics` list.

**New:** Update dataclass to include `sections` list.

**Changes:**
```python
# OLD
@dataclass(frozen=True)
class Curriculum:
    topics: list[Topic]

# NEW
@dataclass(frozen=True)
class Section:
    id: str
    code: str
    title: str
    weighting: float
    estimated_hours: float
    difficulty: str
    topics: list[Topic]

@dataclass(frozen=True)
class Curriculum:
    sections: list[Section]
```

**Impact:** All code that accesses `curriculum.topics` must be updated to `curriculum.sections[].topics`.

#### 8.2.3 CurriculumLoader (HIGH IMPACT)

**Current:** Parses flat `topics` array from JSON.

**New:** Parse hierarchical `sections` → `topics` → `learning_outcomes`.

**Changes:**
```python
# OLD
def _build_topic(raw):
    return Topic(
        id=raw["id"],
        code=raw["code"],
        title=raw["title"],
        learning_outcomes=[_build_lo(lo) for lo in raw["learning_outcomes"]]
    )

# NEW
def _build_topic(raw, section_code):
    return Topic(
        id=raw["id"],
        code=f"{section_code}.{raw['code']}",  # e.g., "CS1-A.1"
        title=raw["title"],
        ...
    )

def _build_section(raw):
    return Section(
        id=raw["id"],
        code=raw["code"],
        title=raw["title"],
        weighting=raw["weighting"],
        topics=[_build_topic(t, raw["code"]) for t in raw["topics"]]
    )
```

**JSON Schema Update Required:**
```json
{
  "sections": [
    {
      "id": "cs1-2026-1",
      "code": "CS1-A",
      "title": "Random Variables and Distributions",
      "weighting": 25.0,
      "estimated_hours": 45.0,
      "difficulty": "foundational",
      "topics": [
        {
          "id": "cs1-2026-1-1",
          "code": "1",
          "title": "Discrete and Continuous Random Variables",
          "learning_outcomes": [...]
        }
      ]
    }
  ]
}
```

#### 8.2.4 StudyPlanService (MEDIUM IMPACT)

**Current:** Queries topics via `CurriculumService.get_ordered_topics()`.

**New:** Same method, but returns topics from new hierarchy.

**Changes:** Minimal — just update to use new `CurriculumService` methods.

#### 8.2.5 MissionService (MEDIUM IMPACT)

**Current:** Generates missions based on topics from study plan.

**New:** Same logic, but topics come from new hierarchy.

**Changes:** Minimal — update topic queries to use new structure.

#### 8.2.6 RecommendationService (MEDIUM IMPACT)

**Current:** Uses `ReadinessService.get_curriculum_coverage()` which counts leaf topics.

**New:** Same logic, but leaf topics are now atomic (no subtopics).

**Changes:** Update `ReadinessService` to work with new hierarchy.

#### 8.2.7 ReadinessService (MEDIUM IMPACT)

**Current:** Calculates coverage based on leaf topics.

**New:** Same calculation, but all topics are leaf nodes.

**Changes:**
```python
# OLD
leaf_topics = [t for t in topics if t.is_leaf_topic()]

# NEW
leaf_topics = topics  # All topics are leaf nodes
```

### 8.3 Unchanged Services

The following services require **no changes**:
- `BurnoutMonitor` — operates on user data, not curriculum structure
- `ExamTimeline` — operates on dates, not curriculum structure
- `AnalyticsService` — operates on aggregated data
- `AdaptiveLearningService` — operates on TopicProgress (unchanged)
- `PlanningService` — operates on study plans (unchanged)

### 8.4 Database Model Changes Summary

| Model | Changes |
|-------|---------|
| `Curriculum` | Add `examination`, `paper`, `syllabus_version`, `effective_from`, `effective_to`; Remove `exam_name` |
| `Section` | **NEW** — replace current `Topic` as root-level entity |
| `Topic` | Change `curriculum_id` → `section_id`; Remove `parent_topic_id`, `syllabus_weight`, `recommended_minutes`, `name`; Add `code`, `title` |
| `LearningObjective` | No changes (except optional `metadata` field) |
| `TopicProgress` | No changes (foreign key still points to `topics.id`) |
| `StudyAttempt` | No changes (foreign key still points to `topics.id`) |
| `Mistake` | No changes (foreign key still points to `topics.id`) |

---

## 9. Risks

### 9.1 High-Risk Areas

#### Risk 1: Data Migration Complexity (HIGH)

**Description:** Transforming flat topics into hierarchical sections + topics requires complex data transformation.

**Impact:** Data loss or corruption if migration fails.

**Mitigation:**
- Comprehensive testing on development database
- Backup all production data before migration
- Write validation scripts to verify data integrity
- Create rollback plan
- Run migration in staging environment first

#### Risk 2: JSON Schema Changes (MEDIUM)

**Description:** Updating the JSON schema to include explicit sections and topics requires updating all curriculum JSON files.

**Impact:** Curriculum import will fail if JSON files are not updated.

**Mitigation:**
- Update all JSON files before deploying code changes
- Version control JSON files
- Write migration script to auto-convert old JSON format to new format
- Add backward compatibility check in loader

#### Risk 3: Service Dependencies (MEDIUM)

**Description:** Multiple services depend on `CurriculumService.get_ordered_topics()`.

**Impact:** Breaking changes to this method will cascade to multiple services.

**Mitigation:**
- Update all dependent services simultaneously
- Write comprehensive integration tests
- Use feature flags to gradually roll out changes
- Monitor error logs after deployment

#### Risk 4: Performance Degradation (LOW)

**Description:** Additional JOINs (Curriculum → Section → Topic) may slow down queries.

**Impact:** Slower page loads, especially on dashboard.

**Mitigation:**
- Add database indexes on foreign keys
- Use eager loading (`joinedload`) in critical queries
- Profile query performance before and after migration
- Cache frequently accessed data

#### Risk 5: User Confusion (LOW)

**Description:** Users may be confused by changes to topic names and hierarchy.

**Impact:** Reduced user satisfaction, increased support requests.

**Mitigation:**
- Display both old and new topic names during transition
- Add tooltips explaining new hierarchy
- Update user documentation
- Send notification email to active users

### 9.2 Risk Matrix

| Risk | Likelihood | Impact | Severity | Mitigation Priority |
|------|-----------|--------|----------|---------------------|
| Data migration complexity | High | High | **CRITICAL** | P0 |
| JSON schema changes | Medium | High | **HIGH** | P1 |
| Service dependencies | Medium | Medium | **MEDIUM** | P1 |
| Performance degradation | Low | Medium | **LOW** | P2 |
| User confusion | Low | Low | **LOW** | P3 |

---

## 10. Recommendations

### 10.1 Immediate Actions (Pre-Milestone 1.2)

1. **Update Curriculum JSON Files**
   - Restructure all JSON files to include explicit `sections` and `topics` arrays
   - Validate new JSON structure against updated schema
   - Version control updated JSON files

2. **Create Migration Scripts**
   - Write data migration script for existing databases
   - Write JSON migration script for old format → new format
   - Test both scripts thoroughly in development

3. **Update Curriculum Engine**
   - Update `Curriculum`, `Section`, `Topic` dataclasses
   - Update `CurriculumLoader` to parse new structure
   - Update `CurriculumRepository` query methods
   - Write unit tests for all changes

### 10.2 Design Decisions

1. **Use `Section` instead of `Topic` for root-level entities**
   - **Rationale:** Aligns with official IFoA terminology and semantics
   - **Benefit:** Clearer code, better alignment with official syllabus

2. **Keep `Topic` as atomic progress-tracking unit**
   - **Rationale:** Sections are too coarse, learning objectives are too fine
   - **Benefit:** Optimal granularity for progress tracking

3. **Store prerequisites at Section level**
   - **Rationale:** Official syllabus specifies section-level prerequisites
   - **Benefit:** Accurate prerequisite graph

4. **Add `code` field to all entities**
   - **Rationale:** Official syllabus uses codes (CS1-A, CS1-A.1, CS1-A.1.1)
   - **Benefit:** Easier mapping between JSON and database

5. **Remove `parent_topic_id` from Topic**
   - **Rationale:** Hierarchy is now Section → Topic (no nesting)
   - **Benefit:** Simpler queries, clearer semantics

### 10.3 Alternative Approaches Considered

#### Alternative 1: Keep Current Flat Structure

**Description:** Leave the current model as-is, but rename `Topic` to `Section` and add a new `Topic` model.

**Pros:**
- Less disruptive to existing code
- Easier migration

**Cons:**
- Still doesn't capture full hierarchy
- Weighting still at wrong level
- Doesn't align with official syllabus

**Decision:** ❌ Rejected — doesn't solve core problems

#### Alternative 2: Full 4-Level Hierarchy

**Description:** Curriculum → Section → SubSection → Topic → LearningObjective

**Pros:**
- Maximum flexibility
- Can represent any syllabus structure

**Cons:**
- Over-engineered for current needs
- Official syllabus only has 3 levels
- Increased complexity without clear benefit

**Decision:** ❌ Rejected — unnecessary complexity

#### Alternative 3: Keep Topic, Add SubTopic

**Description:** Keep current `Topic` model, add `SubTopic` model for sub-divisions.

**Pros:**
- Minimal changes to existing code
- Backward compatible

**Cons:**
- Semantic confusion (Topic is actually a Section)
- Weighting still at wrong level
- Doesn't align with official terminology

**Decision:** ❌ Rejected — semantic confusion outweighs benefits

### 10.4 Best Practices

1. **Database Design**
   - Use foreign keys with `ON DELETE CASCADE` for hierarchical data
   - Add unique constraints on `code` fields
   - Add indexes on foreign keys and frequently queried fields
   - Use soft deletes (`active` flag) for all entities

2. **Code Organization**
   - Keep curriculum engine separate from database models
   - Use repository pattern for data access
   - Use service layer for business logic
   - Write comprehensive unit tests

3. **Data Integrity**
   - Validate JSON before importing
   - Validate database state after migration
   - Use database transactions for multi-step operations
   - Log all data transformations

4. **Backward Compatibility**
   - Support old JSON format during transition period
   - Add deprecation warnings for old methods
   - Version API endpoints if necessary

---

## 11. Implementation Plan for Milestone 1.2

### 11.1 Overview

Milestone 1.2 will implement the proposed schema and migration strategy. This milestone is **implementation only** — the analysis and design are complete.

### 11.2 Task Breakdown

#### Phase 1: Schema Implementation (Days 1-2)

**Task 1.1: Update Database Models**
- [ ] Create `Section` model in `app/models/curriculum.py`
- [ ] Update `Curriculum` model (add fields, remove `exam_name`)
- [ ] Update `Topic` model (change `curriculum_id` → `section_id`, remove fields)
- [ ] Update `LearningObjective` model (add optional `metadata` field)
- [ ] Update relationships in all affected models

**Task 1.2: Create Alembic Migration**
- [ ] Generate migration script
- [ ] Create `sections` table
- [ ] Modify `curricula` table
- [ ] Modify `topics` table
- [ ] Add indexes and constraints
- [ ] Test migration on development database

#### Phase 2: Curriculum Engine Updates (Days 3-4)

**Task 2.1: Update Dataclasses**
- [ ] Create `Section` dataclass in `app/curriculum/models.py`
- [ ] Update `Topic` dataclass (remove `prerequisites`, add `section_code`)
- [ ] Update `Curriculum` dataclass (replace `topics` with `sections`)

**Task 2.2: Update CurriculumLoader**
- [ ] Update `_build_section()` function
- [ ] Update `_build_topic()` function
- [ ] Update `load_from_dict()` to parse `sections` array
- [ ] Update `load_from_json()` (no changes needed)

**Task 2.3: Update CurriculumRepository**
- [ ] Update `get_topics()` to return topics from all sections
- [ ] Update `get_topic()` to search across sections
- [ ] Add `get_sections()` method
- [ ] Add `get_section()` method
- [ ] Update `get_learning_outcome()` to search across sections

**Task 2.4: Update JSON Schema**
- [ ] Update `get_schema()` in `app/curriculum/schemas.py`
- [ ] Replace `topics` array with `sections` array
- [ ] Add `topics` array to section schema
- [ ] Update validation logic in `validate_instance()`

**Task 2.5: Update Curriculum Validator**
- [ ] Update `validate_curriculum()` in `app/curriculum/validator.py`
- [ ] Validate section weightings sum to ~100%
- [ ] Validate topic codes are unique within sections
- [ ] Validate learning outcome codes are unique within topics

#### Phase 3: Service Updates (Days 5-7)

**Task 3.1: Update CurriculumService**
- [ ] Rewrite `import_curricula()` to handle sections and topics
- [ ] Update `get_ordered_topics()` to traverse new hierarchy
- [ ] Update `get_next_incomplete_topic()` (remove leaf topic check)
- [ ] Update `get_curriculum_progress()` (remove leaf topic check)
- [ ] Update `get_topic_tree()` to return sections → topics → learning objectives
- [ ] Update `get_or_create_topic_progress()` (no changes needed)
- [ ] Update `update_topic_progress()` (no changes needed)

**Task 3.2: Update CurriculumEngineService**
- [ ] Update to use new `Curriculum` dataclass structure
- [ ] Update all methods that access `curriculum.topics`

**Task 3.3: Update StudyPlanService**
- [ ] Update topic queries to use new hierarchy
- [ ] Test study plan generation

**Task 3.4: Update MissionService**
- [ ] Update topic references
- [ ] Test mission generation

**Task 3.5: Update RecommendationService**
- [ ] Update `ReadinessService` integration
- [ ] Update curriculum coverage calculations
- [ ] Test recommendation generation

**Task 3.6: Update ReadinessService**
- [ ] Update `get_curriculum_coverage()` to work with new hierarchy
- [ ] Update `get_weakest_topics()` to work with new hierarchy
- [ ] Update `get_review_backlog()` (no changes needed)

#### Phase 4: Data Migration (Days 8-9)

**Task 4.1: Update Curriculum JSON Files**
- [ ] Restructure `app/curriculum/data/ifoa/cs1/2026.json`
- [ ] Add explicit `sections` array
- [ ] Add `topics` array to each section
- [ ] Move `learning_outcomes` from section to topics
- [ ] Validate new JSON structure

**Task 4.2: Write Data Migration Script**
- [ ] Create migration script in `migrations/versions/`
- [ ] Implement Phase 2a: Migrate curricula
- [ ] Implement Phase 2b: Migrate topics → sections
- [ ] Implement Phase 2c: Create sub-topics
- [ ] Implement Phase 2d: Migrate TopicProgress
- [ ] Implement Phase 2e: Migrate StudyAttempts and Mistakes
- [ ] Add data validation queries

**Task 4.3: Test Migration**
- [ ] Test on development database
- [ ] Verify data integrity
- [ ] Test rollback procedure
- [ ] Document any manual steps required

#### Phase 5: Testing (Days 10-11)

**Task 5.1: Unit Tests**
- [ ] Update `tests/test_curriculum_engine.py`
- [ ] Update `tests/test_curriculum_integration.py`
- [ ] Update `tests/test_models.py`
- [ ] Update `tests/test_services.py`
- [ ] Write new tests for Section model
- [ ] Write new tests for hierarchical queries

**Task 5.2: Integration Tests**
- [ ] Test curriculum import with new JSON structure
- [ ] Test study plan generation
- [ ] Test mission generation
- [ ] Test progress tracking
- [ ] Test recommendation engine
- [ ] Test dashboard displays

**Task 5.3: Manual Testing**
- [ ] Test on staging environment
- [ ] Verify all features work correctly
- [ ] Check for broken links or missing data
- [ ] Verify performance is acceptable

#### Phase 6: Documentation (Day 12)

**Task 6.1: Update Documentation**
- [ ] Update `app/curriculum/README.md`
- [ ] Update API documentation
- [ ] Update database schema documentation
- [ ] Write migration guide for existing databases

**Task 6.2: Update Code Comments**
- [ ] Update docstrings in all modified models
- [ ] Update docstrings in all modified services
- [ ] Add inline comments for complex logic

### 11.3 Dependencies

**External Dependencies:**
- None (all changes are internal)

**Internal Dependencies:**
- Task 1.1 (Schema) must complete before Task 1.2 (Migration)
- Task 2.1 (Dataclasses) must complete before Task 2.2 (Loader)
- Task 3.1 (CurriculumService) must complete before Task 3.2-3.6 (Other services)
- Task 4.1 (JSON files) must complete before Task 4.2 (Migration script)
- All tasks must complete before Task 5 (Testing)

### 11.4 Success Criteria

1. **Schema:**
   - [ ] All new tables created successfully
   - [ ] All foreign keys working correctly
   - [ ] All indexes created successfully
   - [ ] No data loss during migration

2. **Curriculum Engine:**
   - [ ] All curricula load correctly
   - [ ] All sections and topics parsed correctly
   - [ ] All learning objectives linked correctly
   - [ ] JSON schema validation passes

3. **Services:**
   - [ ] Curriculum import works correctly
   - [ ] Study plan generation works correctly
   - [ ] Mission generation works correctly
   - [ ] Progress tracking works correctly
   - [ ] Recommendation engine works correctly
   - [ ] Dashboard displays correct data

4. **Testing:**
   - [ ] All unit tests pass
   - [ ] All integration tests pass
   - [ ] Manual testing passes
   - [ ] Performance is acceptable

5. **Documentation:**
   - [ ] All code documented
   - [ ] Migration guide written
   - [ ] API documentation updated

### 11.5 Timeline

| Phase | Duration | Days |
|-------|----------|------|
| Phase 1: Schema Implementation | 2 days | 1-2 |
| Phase 2: Curriculum Engine Updates | 2 days | 3-4 |
| Phase 3: Service Updates | 3 days | 5-7 |
| Phase 4: Data Migration | 2 days | 8-9 |
| Phase 5: Testing | 2 days | 10-11 |
| Phase 6: Documentation | 1 day | 12 |
| **Total** | **12 days** | **1-12** |

### 11.6 Next Steps

1. **Review this document** with stakeholders
2. **Approve the proposed schema** and hierarchy
3. **Begin Phase 1** (Schema Implementation)
4. **Schedule regular check-ins** to track progress
5. **Prepare staging environment** for testing

---

## Appendix A: Example JSON Structure (Proposed)

```json
{
  "organisation": "IFoA",
  "examination": "Actuarial Statistics",
  "paper": "CS1",
  "syllabus_version": "2026",
  "effective_from": "2026-01-01",
  "effective_to": null,
  "metadata": {
    "description": "IFoA CS1 Actuarial Statistics syllabus for the 2026 examinations.",
    "source_url": "https://www.actuaries.org.uk/studying/curriculum/actuarial-statistics",
    "qualification_level": "Core Principles",
    "language": "en"
  },
  "sections": [
    {
      "id": "cs1-2026-1",
      "code": "CS1-A",
      "title": "Random Variables and Distributions",
      "description": "Understand and apply key concepts related to random variables...",
      "weighting": 25.0,
      "estimated_hours": 45.0,
      "difficulty": "foundational",
      "prerequisites": [],
      "order": 1,
      "topics": [
        {
          "id": "cs1-2026-1-1",
          "code": "1",
          "title": "Discrete and Continuous Random Variables",
          "description": "Define and distinguish between types of random variables...",
          "order": 1,
          "learning_outcomes": [
            {
              "id": "cs1-2026-1-1-1",
              "code": "CS1-A.1.1",
              "description": "Define and distinguish between discrete, continuous and mixed random variables.",
              "suggested_revision_days": 7
            }
          ]
        },
        {
          "id": "cs1-2026-1-2",
          "code": "2",
          "title": "Expectation, Variance, and Moments",
          "description": "Calculate and interpret expectation, variance, skewness and kurtosis...",
          "order": 2,
          "learning_outcomes": [
            {
              "id": "cs1-2026-1-2-1",
              "code": "CS1-A.2.1",
              "description": "Calculate and interpret expectation, variance, skewness and kurtosis.",
              "suggested_revision_days": 10
            }
          ]
        }
      ]
    }
  ]
}
```

---

## Appendix B: Code Naming Conventions

| Entity | Code Format | Example |
|--------|-------------|---------|
| Curriculum | N/A (composite key) | `IFoA/CS1/2026` |
| Section | `{PAPER}-{LETTER}` | `CS1-A`, `CS1-B` |
| Topic | `{SECTION_CODE}.{NUMBER}` | `CS1-A.1`, `CS1-A.2` |
| Learning Objective | `{SECTION_CODE}.{TOPIC_NUMBER}.{LO_NUMBER}` | `CS1-A.1.1`, `CS1-A.1.2` |

---

## Appendix C: Glossary

- **Section:** A major division of the syllabus with assessment weighting (e.g., "Random Variables and Distributions" = 25%)
- **Topic:** A sub-division within a section, atomic unit for progress tracking (e.g., "Discrete and Continuous Random Variables")
- **Learning Objective:** A specific, measurable learning outcome (e.g., "Define and distinguish between discrete, continuous and mixed random variables")
- **Leaf Topic:** A topic with no subtopics (in the new model, all topics are leaf nodes)
- **Syllabus Weighting:** The percentage contribution of a section to the overall examination
- **Curriculum Engine:** The in-memory system that loads, validates, and caches curriculum data from JSON files

---

**Document Status:** ✅ Complete  
**Next Review:** Before Milestone 1.2 implementation begins  
**Approved By:** [Pending stakeholder review]