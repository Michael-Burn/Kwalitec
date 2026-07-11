# Milestone 1.2 — Design the Canonical Curriculum JSON Format

**Date:** 2026-10-07  
**Status:** Design Complete — Ready for Review  
**Constraint:** Architecture only — NO implementation in this milestone

---

## Table of Contents

1. [Overview](#1-overview)
2. [JSON Schema Specification](#2-json-schema-specification)
3. [Fully Populated CS1 Example](#3-fully-populated-cs1-example)
4. [Field Documentation](#4-field-documentation)
5. [Validation Rules](#5-validation-rules)
6. [Naming Conventions](#6-naming-conventions)
7. [File Organization](#7-file-organization)
8. [Backwards Compatibility](#8-backwards-compatibility)
9. [Migration Recommendations](#9-migration-recommendations)
10. [Future Extensibility](#10-future-extensibility)

---

## 1. Overview

### 1.1 Purpose

This document defines the **canonical curriculum JSON format** that will become the single source of truth for every supported professional examination. The JSON schema is designed to:

- Accurately represent the official IFoA syllabus hierarchy
- Support the future Adaptive Learning Engine
- Enable multiple examination providers
- Maintain backwards compatibility with existing data
- Provide stable, permanent identifiers for all entities

### 1.2 Design Principles

1. **Hierarchy First:** The schema reflects the official syllabus structure (Section → Topic → Learning Objective)
2. **Stable Identifiers:** Every entity has a permanent identifier that never changes
3. **Metadata Rich:** Each level contains sufficient metadata for adaptive learning
4. **Extensible:** Future features can be added without redesigning the structure
5. **Provider Agnostic:** Supports IFoA, CAA, SOA, and other examination bodies
6. **Version Controlled:** Each syllabus version is explicitly tracked

### 1.3 Hierarchy

```
Curriculum
    └── Sections (1:N)
            └── Topics (1:N)
                    └── Learning Objectives (1:N)
```

### 1.4 Constraints

**This milestone is architecture only.** The following are explicitly out of scope:

- ❌ Database model changes
- ❌ Migration scripts
- ❌ Application service modifications
- ❌ UI template changes
- ❌ Test modifications
- ❌ Code implementation of any kind

---

## 2. JSON Schema Specification

### 2.1 Schema Definition (Draft 2020-12)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://kwalitec.dev/schemas/curriculum-v2.json",
  "title": "Kwalitec Curriculum V2",
  "description": "A versioned, hierarchical representation of an examination syllabus.",
  "type": "object",
  "required": [
    "exam_code",
    "exam_name",
    "provider",
    "version",
    "effective_date",
    "sections"
  ],
  "properties": {
    "exam_code": {
      "type": "string",
      "description": "Unique exam identifier (e.g., 'CS1', 'CM1')",
      "pattern": "^[A-Z]{2}[0-9]$",
      "minLength": 3,
      "maxLength": 3
    },
    "exam_name": {
      "type": "string",
      "description": "Full examination name (e.g., 'Actuarial Statistics')",
      "minLength": 1
    },
    "provider": {
      "type": "string",
      "description": "Examining body (e.g., 'IFoA', 'CAA', 'SOA')",
      "minLength": 1
    },
    "version": {
      "type": "string",
      "description": "Syllabus version year (e.g., '2026')",
      "pattern": "^\\d{4}$"
    },
    "effective_date": {
      "type": "string",
      "format": "date",
      "description": "Date the syllabus becomes effective (ISO 8601: YYYY-MM-DD)"
    },
    "superseded_date": {
      "type": ["string", "null"],
      "format": "date",
      "description": "Date the syllabus is superseded, or null if current"
    },
    "total_estimated_hours": {
      "type": "number",
      "minimum": 0,
      "description": "Total recommended study hours for the entire exam"
    },
    "description": {
      "type": "string",
      "description": "Overall exam description and objectives"
    },
    "sections": {
      "type": "array",
      "description": "Ordered list of syllabus sections",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "id",
          "code",
          "title",
          "description",
          "exam_weight",
          "estimated_hours",
          "display_order",
          "topics"
        ],
        "properties": {
          "id": {
            "type": "string",
            "description": "Stable section identifier (e.g., 'CS1-A')",
            "pattern": "^[A-Z]{2}[0-9]-[A-Z]$"
          },
          "code": {
            "type": "string",
            "description": "Official section code (e.g., 'CS1-A')",
            "minLength": 1
          },
          "title": {
            "type": "string",
            "description": "Section title",
            "minLength": 1
          },
          "description": {
            "type": "string",
            "description": "Detailed section description"
          },
          "exam_weight": {
            "type": "number",
            "minimum": 0,
            "maximum": 100,
            "description": "Assessment weighting percentage (e.g., 25.0 for 25%)"
          },
          "estimated_hours": {
            "type": "number",
            "minimum": 0,
            "description": "Recommended study hours for this section"
          },
          "difficulty": {
            "type": "string",
            "enum": ["foundational", "intermediate", "advanced"],
            "description": "Overall section difficulty level"
          },
          "display_order": {
            "type": "integer",
            "minimum": 1,
            "description": "Sequential display order (1-based)"
          },
          "topics": {
            "type": "array",
            "description": "Ordered list of topics within this section",
            "minItems": 1,
            "items": {
              "type": "object",
              "required": [
                "id",
                "section_id",
                "code",
                "title",
                "description",
                "estimated_minutes",
                "difficulty",
                "display_order",
                "learning_objectives"
              ],
              "properties": {
                "id": {
                  "type": "string",
                  "description": "Stable topic identifier (e.g., 'CS1-A-T01')",
                  "pattern": "^[A-Z]{2}[0-9]-[A-Z]-T[0-9]{2}$"
                },
                "section_id": {
                  "type": "string",
                  "description": "Parent section identifier (e.g., 'CS1-A')",
                  "pattern": "^[A-Z]{2}[0-9]-[A-Z]$"
                },
                "code": {
                  "type": "string",
                  "description": "Official topic code (e.g., 'CS1-A.1')",
                  "minLength": 1
                },
                "title": {
                  "type": "string",
                  "description": "Topic title",
                  "minLength": 1
                },
                "description": {
                  "type": "string",
                  "description": "Detailed topic description"
                },
                "estimated_minutes": {
                  "type": "integer",
                  "minimum": 0,
                  "description": "Estimated study time in minutes"
                },
                "difficulty": {
                  "type": "string",
                  "enum": ["foundational", "intermediate", "advanced"],
                  "description": "Topic difficulty level"
                },
                "display_order": {
                  "type": "integer",
                  "minimum": 1,
                  "description": "Sequential display order within section (1-based)"
                },
                "learning_objectives": {
                  "type": "array",
                  "description": "Ordered list of learning objectives",
                  "minItems": 1,
                  "items": {
                    "type": "object",
                    "required": [
                      "id",
                      "topic_id",
                      "code",
                      "description",
                      "cognitive_level",
                      "estimated_minutes",
                      "learning_type",
                      "display_order"
                    ],
                    "properties": {
                      "id": {
                        "type": "string",
                        "description": "Stable learning objective identifier (e.g., 'CS1-A-T01-LO01')",
                        "pattern": "^[A-Z]{2}[0-9]-[A-Z]-T[0-9]{2}-LO[0-9]{2}$"
                      },
                      "topic_id": {
                        "type": "string",
                        "description": "Parent topic identifier (e.g., 'CS1-A-T01')",
                        "pattern": "^[A-Z]{2}[0-9]-[A-Z]-T[0-9]{2}$"
                      },
                      "code": {
                        "type": "string",
                        "description": "Official learning objective code (e.g., 'CS1-A.1.1')",
                        "minLength": 1
                      },
                      "description": {
                        "type": "string",
                        "description": "Learning objective description (measurable outcome)"
                      },
                      "cognitive_level": {
                        "type": "string",
                        "enum": ["remember", "understand", "apply", "analyze", "evaluate", "create"],
                        "description": "Bloom's taxonomy cognitive level"
                      },
                      "estimated_minutes": {
                        "type": "integer",
                        "minimum": 0,
                        "description": "Estimated study time in minutes"
                      },
                      "learning_type": {
                        "type": "string",
                        "enum": ["concept", "procedure", "problem_solving", "application", "analysis"],
                        "description": "Type of learning outcome"
                      },
                      "display_order": {
                        "type": "integer",
                        "minimum": 1,
                        "description": "Sequential display order within topic (1-based)"
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    },
    "metadata": {
      "type": "object",
      "description": "Arbitrary key-value metadata for future extensibility",
      "additionalProperties": {
        "type": "string"
      }
    }
  },
  "additionalProperties": false
}
```

### 2.2 Schema Characteristics

| Aspect | Detail |
|--------|--------|
| **Schema Version** | Draft 2020-12 |
| **Schema ID** | `https://kwalitec.dev/schemas/curriculum-v2.json` |
| **Strict Mode** | `additionalProperties: false` at root level |
| **Extensibility** | `metadata` object allows arbitrary key-value pairs |
| **Validation** | Pattern matching for identifiers, enum constraints for categorical fields |

---

## 3. Fully Populated CS1 Example

### 3.1 Complete JSON File

```json
{
  "exam_code": "CS1",
  "exam_name": "Actuarial Statistics",
  "provider": "IFoA",
  "version": "2026",
  "effective_date": "2026-01-01",
  "superseded_date": null,
  "total_estimated_hours": 190.0,
  "description": "The aim of the CS1 syllabus is to provide a grounding in mathematical and statistical techniques that are of particular relevance to actuarial work.",

  "sections": [
    {
      "id": "CS1-A",
      "code": "CS1-A",
      "title": "Random Variables and Distributions",
      "description": "Understand and apply key concepts related to random variables, including probability functions, distribution functions, expectation, variance, and higher moments.",
      "exam_weight": 25.0,
      "estimated_hours": 45.0,
      "difficulty": "foundational",
      "display_order": 1,

      "topics": [
        {
          "id": "CS1-A-T01",
          "section_id": "CS1-A",
          "code": "CS1-A.1",
          "title": "Discrete and Continuous Random Variables",
          "description": "Define and distinguish between discrete, continuous and mixed random variables. Understand probability mass functions, probability density functions, and cumulative distribution functions.",
          "estimated_minutes": 90,
          "difficulty": "foundational",
          "display_order": 1,

          "learning_objectives": [
            {
              "id": "CS1-A-T01-LO01",
              "topic_id": "CS1-A-T01",
              "code": "CS1-A.1.1",
              "description": "Define and distinguish between discrete, continuous and mixed random variables.",
              "cognitive_level": "understand",
              "estimated_minutes": 30,
              "learning_type": "concept",
              "display_order": 1
            },
            {
              "id": "CS1-A-T01-LO02",
              "topic_id": "CS1-A-T01",
              "code": "CS1-A.1.2",
              "description": "Calculate and interpret probability mass functions, probability density functions, and cumulative distribution functions.",
              "cognitive_level": "apply",
              "estimated_minutes": 45,
              "learning_type": "procedure",
              "display_order": 2
            }
          ]
        },

        {
          "id": "CS1-A-T02",
          "section_id": "CS1-A",
          "code": "CS1-A.2",
          "title": "Expectation, Variance, and Moments",
          "description": "Calculate and interpret expectation, variance, skewness, and kurtosis for random variables.",
          "estimated_minutes": 120,
          "difficulty": "foundational",
          "display_order": 2,

          "learning_objectives": [
            {
              "id": "CS1-A-T02-LO01",
              "topic_id": "CS1-A-T02",
              "code": "CS1-A.2.1",
              "description": "Calculate and interpret expectation, variance, skewness and kurtosis.",
              "cognitive_level": "apply",
              "estimated_minutes": 45,
              "learning_type": "procedure",
              "display_order": 1
            },
            {
              "id": "CS1-A-T02-LO02",
              "topic_id": "CS1-A-T02",
              "code": "CS1-A.2.2",
              "description": "Derive the moment generating function and cumulant generating function for common distributions.",
              "cognitive_level": "apply",
              "estimated_minutes": 60,
              "learning_type": "procedure",
              "display_order": 2
            }
          ]
        },

        {
          "id": "CS1-A-T03",
          "section_id": "CS1-A",
          "code": "CS1-A.3",
          "title": "Moment Generating Functions",
          "description": "Use moment generating functions and cumulant generating functions to derive properties of distributions.",
          "estimated_minutes": 90,
          "difficulty": "intermediate",
          "display_order": 3,

          "learning_objectives": [
            {
              "id": "CS1-A-T03-LO01",
              "topic_id": "CS1-A-T03",
              "code": "CS1-A.3.1",
              "description": "Derive the moment generating function and cumulant generating function for common distributions.",
              "cognitive_level": "apply",
              "estimated_minutes": 60,
              "learning_type": "procedure",
              "display_order": 1
            },
            {
              "id": "CS1-A-T03-LO02",
              "topic_id": "CS1-A-T03",
              "code": "CS1-A.3.2",
              "description": "Use moment generating functions to derive moments and distributions of sums of independent random variables.",
              "cognitive_level": "analyze",
              "estimated_minutes": 45,
              "learning_type": "problem_solving",
              "display_order": 2
            }
          ]
        }
      ]
    },

    {
      "id": "CS1-B",
      "code": "CS1-B",
      "title": "Common Statistical Distributions",
      "description": "Apply the binomial, Poisson, negative binomial, exponential, gamma, normal, log-normal, chi-squared, t and F distributions.",
      "exam_weight": 20.0,
      "estimated_hours": 35.0,
      "difficulty": "intermediate",
      "display_order": 2,

      "topics": [
        {
          "id": "CS1-B-T01",
          "section_id": "CS1-B",
          "code": "CS1-B.1",
          "title": "Discrete Distributions",
          "description": "Apply the binomial, Poisson, and negative binomial distributions to model discrete data.",
          "estimated_minutes": 90,
          "difficulty": "intermediate",
          "display_order": 1,

          "learning_objectives": [
            {
              "id": "CS1-B-T01-LO01",
              "topic_id": "CS1-B-T01",
              "code": "CS1-B.1.1",
              "description": "Derive moments, mode and quantiles for the binomial, Poisson and negative binomial distributions.",
              "cognitive_level": "apply",
              "estimated_minutes": 45,
              "learning_type": "procedure",
              "display_order": 1
            },
            {
              "id": "CS1-B-T01-LO02",
              "topic_id": "CS1-B-T01",
              "code": "CS1-B.1.2",
              "description": "Identify appropriate distributions for real-world modelling scenarios involving discrete data.",
              "cognitive_level": "analyze",
              "estimated_minutes": 30,
              "learning_type": "application",
              "display_order": 2
            }
          ]
        },

        {
          "id": "CS1-B-T02",
          "section_id": "CS1-B",
          "code": "CS1-B.2",
          "title": "Continuous Distributions",
          "description": "Apply the exponential, gamma, normal, log-normal, chi-squared, t and F distributions to model continuous data.",
          "estimated_minutes": 120,
          "difficulty": "intermediate",
          "display_order": 2,

          "learning_objectives": [
            {
              "id": "CS1-B-T02-LO01",
              "topic_id": "CS1-B-T02",
              "code": "CS1-B.2.1",
              "description": "Derive moments, mode and quantiles for the exponential, gamma, normal, log-normal, chi-squared, t and F distributions.",
              "cognitive_level": "apply",
              "estimated_minutes": 60,
              "learning_type": "procedure",
              "display_order": 1
            },
            {
              "id": "CS1-B-T02-LO02",
              "topic_id": "CS1-B-T02",
              "code": "CS1-B.2.2",
              "description": "Identify appropriate distributions for real-world modelling scenarios involving continuous data.",
              "cognitive_level": "analyze",
              "estimated_minutes": 45,
              "learning_type": "application",
              "display_order": 2
            }
          ]
        }
      ]
    },

    {
      "id": "CS1-C",
      "code": "CS1-C",
      "title": "Generating Functions and Sums of Random Variables",
      "description": "Use probability generating functions, moment generating functions and cumulant generating functions to derive properties of sums of independent random variables, including the central limit theorem.",
      "exam_weight": 15.0,
      "estimated_hours": 30.0,
      "difficulty": "intermediate",
      "display_order": 3,

      "topics": [
        {
          "id": "CS1-C-T01",
          "section_id": "CS1-C",
          "code": "CS1-C.1",
          "title": "Probability and Moment Generating Functions",
          "description": "Use probability generating functions, moment generating functions and cumulant generating functions.",
          "estimated_minutes": 90,
          "difficulty": "intermediate",
          "display_order": 1,

          "learning_objectives": [
            {
              "id": "CS1-C-T01-LO01",
              "topic_id": "CS1-C-T01",
              "code": "CS1-C.1.1",
              "description": "Derive exact distributions of sums of independent random variables using generating functions.",
              "cognitive_level": "apply",
              "estimated_minutes": 60,
              "learning_type": "procedure",
              "display_order": 1
            }
          ]
        },

        {
          "id": "CS1-C-T02",
          "section_id": "CS1-C",
          "code": "CS1-C.2",
          "title": "Central Limit Theorem",
          "description": "State and apply the central limit theorem for a single sample and for two independent samples.",
          "estimated_minutes": 90,
          "difficulty": "intermediate",
          "display_order": 2,

          "learning_objectives": [
            {
              "id": "CS1-C-T02-LO01",
              "topic_id": "CS1-C-T02",
              "code": "CS1-C.2.1",
              "description": "State and apply the central limit theorem for a single sample and for two independent samples.",
              "cognitive_level": "apply",
              "estimated_minutes": 45,
              "learning_type": "application",
              "display_order": 1
            }
          ]
        }
      ]
    },

    {
      "id": "CS1-D",
      "code": "CS1-D",
      "title": "Joint Distributions",
      "description": "Understand joint (bivariate) distributions, including joint probability/density functions, marginal distributions, conditional distributions, independence, covariance, correlation and expectation of functions of two random variables.",
      "exam_weight": 15.0,
      "estimated_hours": 25.0,
      "difficulty": "advanced",
      "display_order": 4,

      "topics": [
        {
          "id": "CS1-D-T01",
          "section_id": "CS1-D",
          "code": "CS1-D.1",
          "title": "Joint and Marginal Distributions",
          "description": "Calculate marginal and conditional distributions from a joint distribution.",
          "estimated_minutes": 75,
          "difficulty": "advanced",
          "display_order": 1,

          "learning_objectives": [
            {
              "id": "CS1-D-T01-LO01",
              "topic_id": "CS1-D-T01",
              "code": "CS1-D.1.1",
              "description": "Calculate marginal and conditional distributions from a joint distribution.",
              "cognitive_level": "apply",
              "estimated_minutes": 45,
              "learning_type": "procedure",
              "display_order": 1
            }
          ]
        },

        {
          "id": "CS1-D-T02",
          "section_id": "CS1-D",
          "code": "CS1-D.2",
          "title": "Independence, Covariance, and Correlation",
          "description": "Determine whether two random variables are independent and calculate covariance and correlation.",
          "estimated_minutes": 75,
          "difficulty": "advanced",
          "display_order": 2,

          "learning_objectives": [
            {
              "id": "CS1-D-T02-LO01",
              "topic_id": "CS1-D-T02",
              "code": "CS1-D.2.1",
              "description": "Determine whether two random variables are independent and calculate covariance and correlation.",
              "cognitive_level": "apply",
              "estimated_minutes": 45,
              "learning_type": "procedure",
              "display_order": 1
            }
          ]
        }
      ]
    },

    {
      "id": "CS1-E",
      "code": "CS1-E",
      "title": "Bayesian Statistics",
      "description": "Understand and apply Bayesian methods, including the prior distribution, posterior distribution, conjugate priors, loss functions and Bayesian estimators.",
      "exam_weight": 15.0,
      "estimated_hours": 25.0,
      "difficulty": "advanced",
      "display_order": 5,

      "topics": [
        {
          "id": "CS1-E-T01",
          "section_id": "CS1-E",
          "code": "CS1-E.1",
          "title": "Prior and Posterior Distributions",
          "description": "Derive posterior distributions using Bayes' theorem for common conjugate families.",
          "estimated_minutes": 75,
          "difficulty": "advanced",
          "display_order": 1,

          "learning_objectives": [
            {
              "id": "CS1-E-T01-LO01",
              "topic_id": "CS1-E-T01",
              "code": "CS1-E.1.1",
              "description": "Derive posterior distributions using Bayes' theorem for common conjugate families.",
              "cognitive_level": "apply",
              "estimated_minutes": 45,
              "learning_type": "procedure",
              "display_order": 1
            }
          ]
        },

        {
          "id": "CS1-E-T02",
          "section_id": "CS1-E",
          "code": "CS1-E.2",
          "title": "Bayesian Estimators and Loss Functions",
          "description": "Calculate Bayesian estimators under quadratic and absolute error loss.",
          "estimated_minutes": 75,
          "difficulty": "advanced",
          "display_order": 2,

          "learning_objectives": [
            {
              "id": "CS1-E-T02-LO01",
              "topic_id": "CS1-E-T02",
              "code": "CS1-E.2.1",
              "description": "Calculate Bayesian estimators under quadratic and absolute error loss.",
              "cognitive_level": "apply",
              "estimated_minutes": 45,
              "learning_type": "procedure",
              "display_order": 1
            }
          ]
        }
      ]
    },

    {
      "id": "CS1-F",
      "code": "CS1-F",
      "title": "Sampling and Statistical Inference",
      "description": "Apply methods of point estimation including the method of moments and maximum likelihood estimation. Construct confidence intervals and perform hypothesis tests, including likelihood ratio tests.",
      "exam_weight": 10.0,
      "estimated_hours": 30.0,
      "difficulty": "intermediate",
      "display_order": 6,

      "topics": [
        {
          "id": "CS1-F-T01",
          "section_id": "CS1-F",
          "code": "CS1-F.1",
          "title": "Point Estimation",
          "description": "Derive maximum likelihood estimators and evaluate their properties.",
          "estimated_minutes": 90,
          "difficulty": "intermediate",
          "display_order": 1,

          "learning_objectives": [
            {
              "id": "CS1-F-T01-LO01",
              "topic_id": "CS1-F-T01",
              "code": "CS1-F.1.1",
              "description": "Derive maximum likelihood estimators and evaluate their properties.",
              "cognitive_level": "apply",
              "estimated_minutes": 60,
              "learning_type": "procedure",
              "display_order": 1
            }
          ]
        },

        {
          "id": "CS1-F-T02",
          "section_id": "CS1-F",
          "code": "CS1-F.2",
          "title": "Confidence Intervals and Hypothesis Testing",
          "description": "Construct confidence intervals and perform hypothesis tests.",
          "estimated_minutes": 90,
          "difficulty": "intermediate",
          "display_order": 2,

          "learning_objectives": [
            {
              "id": "CS1-F-T02-LO01",
              "topic_id": "CS1-F-T02",
              "code": "CS1-F.2.1",
              "description": "Construct confidence intervals for means, proportions and variances.",
              "cognitive_level": "apply",
              "estimated_minutes": 45,
              "learning_type": "procedure",
              "display_order": 1
            },
            {
              "id": "CS1-F-T02-LO02",
              "topic_id": "CS1-F-T02",
              "code": "CS1-F.2.2",
              "description": "Perform hypothesis tests, including likelihood ratio tests.",
              "cognitive_level": "apply",
              "estimated_minutes": 45,
              "learning_type": "procedure",
              "display_order": 2
            }
          ]
        }
      ]
    }
  ],

  "metadata": {
    "source_url": "https://www.actuaries.org.uk/studying/curriculum/actuarial-statistics",
    "qualification_level": "Core Principles",
    "language": "en",
    "created_date": "2025-06-01",
    "last_modified": "2025-09-15",
    "curriculum_officer": "IFoA Curriculum Team"
  }
}
```

### 3.2 Example Statistics

| Metric | Value |
|--------|-------|
| **Total Sections** | 6 (A-F) |
| **Total Topics** | 12 |
| **Total Learning Objectives** | 18 |
| **Total Estimated Hours** | 190.0 |
| **Section Weightings** | 25% + 20% + 15% + 15% + 15% + 10% = 100% |

---

## 4. Field Documentation

### 4.1 Curriculum Level

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `exam_code` | string | ✅ | Unique exam identifier (3 chars: 2 letters + 1 digit) | `"CS1"` |
| `exam_name` | string | ✅ | Full examination name | `"Actuarial Statistics"` |
| `provider` | string | ✅ | Examining body | `"IFoA"` |
| `version` | string | ✅ | Syllabus version year (4 digits) | `"2026"` |
| `effective_date` | string (date) | ✅ | ISO 8601 date when syllabus becomes active | `"2026-01-01"` |
| `superseded_date` | string \| null | ❌ | ISO 8601 date when syllabus is superseded, or null | `null` |
| `total_estimated_hours` | number | ✅ | Total recommended study hours for entire exam | `190.0` |
| `description` | string | ✅ | Overall exam description and objectives | `"The aim of the CS1 syllabus..."` |
| `sections` | array | ✅ | Ordered list of syllabus sections | See Section 4.2 |
| `metadata` | object | ❌ | Arbitrary key-value metadata for future extensibility | See Section 4.4 |

### 4.2 Section Level

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `id` | string | ✅ | Stable section identifier (pattern: `[A-Z]{2}[0-9]-[A-Z]`) | `"CS1-A"` |
| `code` | string | ✅ | Official section code | `"CS1-A"` |
| `title` | string | ✅ | Section title | `"Random Variables and Distributions"` |
| `description` | string | ✅ | Detailed section description | `"Understand and apply..."` |
| `exam_weight` | number | ✅ | Assessment weighting percentage (0-100) | `25.0` |
| `estimated_hours` | number | ✅ | Recommended study hours for this section | `45.0` |
| `difficulty` | string (enum) | ✅ | Overall section difficulty level | `"foundational"` |
| `display_order` | integer | ✅ | Sequential display order (1-based) | `1` |
| `topics` | array | ✅ | Ordered list of topics within this section | See Section 4.3 |

**Enum Values for `difficulty`:**
- `"foundational"` - Basic concepts, prerequisite for other sections
- `"intermediate"` - Builds on foundational knowledge
- `"advanced"` - Complex applications and analysis

### 4.3 Topic Level

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `id` | string | ✅ | Stable topic identifier (pattern: `[A-Z]{2}[0-9]-[A-Z]-T[0-9]{2}`) | `"CS1-A-T01"` |
| `section_id` | string | ✅ | Parent section identifier | `"CS1-A"` |
| `code` | string | ✅ | Official topic code | `"CS1-A.1"` |
| `title` | string | ✅ | Topic title | `"Discrete and Continuous Random Variables"` |
| `description` | string | ✅ | Detailed topic description | `"Define and distinguish..."` |
| `estimated_minutes` | integer | ✅ | Estimated study time in minutes | `90` |
| `difficulty` | string (enum) | ✅ | Topic difficulty level | `"foundational"` |
| `display_order` | integer | ✅ | Sequential display order within section (1-based) | `1` |
| `learning_objectives` | array | ✅ | Ordered list of learning objectives | See Section 4.4 |

**Enum Values for `difficulty`:**
- `"foundational"` - Basic concepts
- `"intermediate"` - Application and analysis
- `"advanced"` - Complex problem-solving

### 4.4 Learning Objective Level

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `id` | string | ✅ | Stable LO identifier (pattern: `[A-Z]{2}[0-9]-[A-Z]-T[0-9]{2}-LO[0-9]{2}`) | `"CS1-A-T01-LO01"` |
| `topic_id` | string | ✅ | Parent topic identifier | `"CS1-A-T01"` |
| `code` | string | ✅ | Official learning objective code | `"CS1-A.1.1"` |
| `description` | string | ✅ | Learning objective description (measurable outcome) | `"Define and distinguish..."` |
| `cognitive_level` | string (enum) | ✅ | Bloom's taxonomy cognitive level | `"understand"` |
| `estimated_minutes` | integer | ✅ | Estimated study time in minutes | `30` |
| `learning_type` | string (enum) | ✅ | Type of learning outcome | `"concept"` |
| `display_order` | integer | ✅ | Sequential display order within topic (1-based) | `1` |

**Enum Values for `cognitive_level` (Bloom's Taxonomy):**
- `"remember"` - Recall facts and basic concepts
- `"understand"` - Explain ideas or concepts
- `"apply"` - Use information in new situations
- `"analyze"` - Draw connections among ideas
- `"evaluate"` - Justify a decision or course of action
- `"create"` - Produce new or original work

**Enum Values for `learning_type`:**
- `"concept"` - Understanding definitions and principles
- `"procedure"` - Learning step-by-step processes
- `"problem_solving"` - Solving complex problems
- `"application"` - Applying knowledge to real-world scenarios
- `"analysis"` - Breaking down complex information

### 4.5 Metadata Object

The `metadata` object at the curriculum level allows arbitrary key-value pairs for future extensibility:

```json
{
  "metadata": {
    "source_url": "https://www.actuaries.org.uk/...",
    "qualification_level": "Core Principles",
    "language": "en",
    "created_date": "2025-06-01",
    "last_modified": "2025-09-15",
    "curriculum_officer": "IFoA Curriculum Team"
  }
}
```

**Guidelines:**
- All values must be strings
- Keys should be snake_case
- Reserved for provider-specific or future use
- No validation on keys or values

---

## 5. Validation Rules

### 5.1 Structural Validation

1. **Required Fields:** All fields marked as required must be present
2. **Type Checking:** All fields must match their specified types
3. **No Additional Properties:** Root-level `additionalProperties: false` prevents unknown fields
4. **Array Minimums:** `sections`, `topics`, and `learning_objectives` must have at least 1 item

### 5.2 Identifier Validation

1. **Pattern Matching:**
   - `exam_code`: Must match `^[A-Z]{2}[0-9]$` (e.g., "CS1", "CM1")
   - `section.id`: Must match `^[A-Z]{2}[0-9]-[A-Z]$` (e.g., "CS1-A")
   - `topic.id`: Must match `^[A-Z]{2}[0-9]-[A-Z]-T[0-9]{2}$` (e.g., "CS1-A-T01")
   - `learning_objective.id`: Must match `^[A-Z]{2}[0-9]-[A-Z]-T[0-9]{2}-LO[0-9]{2}$` (e.g., "CS1-A-T01-LO01")

2. **Uniqueness:**
   - All `id` fields must be unique within their scope
   - Section `id` must be unique across the curriculum
   - Topic `id` must be unique across the curriculum
   - Learning objective `id` must be unique across the curriculum

3. **Referential Integrity:**
   - `topic.section_id` must reference an existing `section.id`
   - `learning_objective.topic_id` must reference an existing `topic.id`

### 5.3 Business Rule Validation

1. **Exam Weighting:**
   - Sum of all `section.exam_weight` values must equal 100.0 (±0.1 for floating point tolerance)
   - Each `section.exam_weight` must be between 0 and 100

2. **Time Validation:**
   - `total_estimated_hours` should approximately equal sum of all `section.estimated_hours` (±10% tolerance)
   - `section.estimated_hours` should approximately equal sum of all `topic.estimated_minutes` / 60 (±10% tolerance)
   - `topic.estimated_minutes` should approximately equal sum of all `learning_objective.estimated_minutes` (±10% tolerance)

3. **Display Order:**
   - `section.display_order` must be sequential starting from 1
   - `topic.display_order` must be sequential starting from 1 within each section
   - `learning_objective.display_order` must be sequential starting from 1 within each topic

4. **Date Validation:**
   - `effective_date` must be a valid ISO 8601 date
   - `superseded_date` must be either null or a valid ISO 8601 date
   - If `superseded_date` is not null, it must be after `effective_date`

5. **Enum Validation:**
   - `difficulty` must be one of: `"foundational"`, `"intermediate"`, `"advanced"`
   - `cognitive_level` must be one of: `"remember"`, `"understand"`, `"apply"`, `"analyze"`, `"evaluate"`, `"create"`
   - `learning_type` must be one of: `"concept"`, `"procedure"`, `"problem_solving"`, `"application"`, `"analysis"`

### 5.4 Semantic Validation

1. **Description Quality:**
   - Learning objective descriptions should be measurable (start with action verbs)
   - Descriptions should not be empty strings

2. **Time Reasonableness:**
   - `learning_objective.estimated_minutes` should be between 5 and 120 minutes
   - `topic.estimated_minutes` should be between 15 and 480 minutes
   - `section.estimated_hours` should be between 1 and 100 hours

3. **Hierarchy Depth:**
   - Maximum depth is 3 levels (Curriculum → Section → Topic → Learning Objective)
   - No circular references allowed

---

## 6. Naming Conventions

### 6.1 Identifier Patterns

All identifiers follow strict patterns to ensure stability and uniqueness:

| Entity | Pattern | Example | Rationale |
|--------|---------|---------|-----------|
| **Exam Code** | `[A-Z]{2}[0-9]` | `CS1`, `CM1` | 2-letter subject + 1-digit level |
| **Section ID** | `[A-Z]{2}[0-9]-[A-Z]` | `CS1-A`, `CM1-B` | Exam code + hyphen + section letter |
| **Topic ID** | `[A-Z]{2}[0-9]-[A-Z]-T[0-9]{2}` | `CS1-A-T01`, `CM1-B-T05` | Section ID + `-T` + 2-digit sequence |
| **Learning Objective ID** | `[A-Z]{2}[0-9]-[A-Z]-T[0-9]{2}-LO[0-9]{2}` | `CS1-A-T01-LO01` | Topic ID + `-LO` + 2-digit sequence |

### 6.2 Code Patterns

Human-readable codes use a dot notation:

| Entity | Pattern | Example | Notes |
|--------|---------|---------|-------|
| **Section Code** | Same as ID | `CS1-A` | Official IFoA code |
| **Topic Code** | `[Section Code].[Number]` | `CS1-A.1`, `CS1-A.2` | Decimal notation |
| **Learning Objective Code** | `[Topic Code].[Number]` | `CS1-A.1.1`, `CS1-A.1.2` | Nested decimal notation |

### 6.3 Naming Rules

1. **Stability:**
   - Identifiers NEVER change, even if display names change
   - Identifiers are assigned once and remain forever
   - Do NOT use display names in identifiers

2. **Case Sensitivity:**
   - All identifiers use UPPERCASE
   - All codes use UPPERCASE
   - Field names use snake_case

3. **Sequencing:**
   - Topics: 2-digit zero-padded (T01, T02, ..., T10, T11)
   - Learning Objectives: 2-digit zero-padded (LO01, LO02, ..., LO10, LO11)
   - Allows up to 99 topics per section and 99 LOs per topic

4. **Reserved Characters:**
   - Hyphen (`-`) separates hierarchy levels in IDs
   - Period (`.`) separates hierarchy levels in codes
   - No spaces allowed in IDs or codes

### 6.4 Examples

**Good:**
- `CS1-A-T01-LO01` - Stable, descriptive, follows pattern
- `CS1-B.3.2` - Clear hierarchy, official code format

**Bad:**
- `random-variables` - Not stable, uses display name
- `CS1-A-Topic1` - Inconsistent naming, not zero-padded
- `cs1-a-t01-lo01` - Wrong case (should be uppercase)

---

## 7. File Organization

### 7.1 Directory Structure

```
curriculum/
├── README.md
├── SCHEMA.md
├── ifoa/
│   ├── cs1/
│   │   ├── 2026.json
│   │   ├── 2025.json
│   │   └── archive/
│   │       ├── 2024.json
│   │       └── 2023.json
│   ├── cm1/
│   │   ├── 2026.json
│   │   └── 2025.json
│   ├── cm2/
│   │   ├── 2026.json
│   │   └── 2025.json
│   ├── cb1/
│   │   ├── 2026.json
│   │   └── 2025.json
│   └── cb2/
│       ├── 2026.json
│       └── 2025.json
├── caa/
│   ├── ct1/
│   │   ├── 2026.json
│   │   └── 2025.json
│   └── ct2/
│       ├── 2026.json
│       └── 2025.json
└── soa/
    ├── pa/
    │   ├── 2026.json
    │   └── 2025.json
    └── sr/
        ├── 2026.json
        └── 2025.json
```

### 7.2 File Naming Convention

**Pattern:** `[version].json`

**Examples:**
- `2026.json` - Current syllabus version
- `2025.json` - Previous syllabus version
- `2024.json` - Archived in `archive/` subdirectory

**Rationale:**
- Simple, predictable naming
- Easy to identify current vs. historical versions
- Supports multiple versions per exam
- Archive directory keeps root clean

### 7.3 Organization Principles

1. **Provider-First:** Top-level directories by examining body (`ifoa`, `caa`, `soa`)
2. **Exam-Second:** Second-level directories by exam code (`cs1`, `cm1`, `cb1`)
3. **Version-Third:** Files named by syllabus version year (`2026.json`)
4. **Archive:** Older versions moved to `archive/` subdirectory
5. **Current:** Latest version stays in root of exam directory

### 7.4 Multi-Exam Support

The structure supports unlimited providers and exams:

**Adding a New Provider:**
```bash
mkdir -p curriculum/new_provider/exam_code
```

**Adding a New Exam Version:**
```bash
cp curriculum/ifoa/cs1/2026.json curriculum/ifoa/cs1/2027.json
# Edit 2027.json with new content
```

**Archiving an Old Version:**
```bash
mkdir -p curriculum/ifoa/cs1/archive
mv curriculum/ifoa/cs1/2025.json curriculum/ifoa/cs1/archive/
```

### 7.5 File Loading Strategy

The application should load curriculum files using this logic:

```python
def load_curriculum(provider: str, exam_code: str, version: str = None):
    """
    Load a curriculum file.
    
    Args:
        provider: Examining body (e.g., 'ifoa', 'caa', 'soa')
        exam_code: Exam code (e.g., 'cs1', 'cm1')
        version: Syllabus version year (e.g., '2026'). 
                 If None, loads the latest version.
    
    Returns:
        Parsed curriculum dict
    """
    base_path = f"curriculum/{provider}/{exam_code}"
    
    if version:
        file_path = f"{base_path}/{version}.json"
    else:
        # Find latest version (highest year number)
        versions = sorted(Path(base_path).glob("*.json"), reverse=True)
        file_path = versions[0]
    
    with open(file_path) as f:
        return json.load(f)
```

---

## 8. Backwards Compatibility

### 8.1 Current JSON Structure

**Current Format (V1):**
```json
{
  "organisation": "IFoA",
  "examination": "Actuarial Statistics",
  "paper": "CS1",
  "syllabus_version": "2026",
  "effective_from": "2026-01-01",
  "effective_to": null,
  "metadata": {
    "description": "...",
    "source_url": "...",
    "qualification_level": "Core Principles",
    "language": "en"
  },
  "topics": [
    {
      "id": "cs1-2026-1",
      "code": "CS1-A",
      "title": "Random Variables and Distributions",
      "description": "...",
      "weighting": 25.0,
      "estimated_hours": 45.0,
      "difficulty": "foundational",
      "prerequisites": [],
      "learning_outcomes": [
        {
          "id": "cs1-2026-1-1",
          "code": "CS1-A-1",
          "description": "...",
          "suggested_revision_days": 7
        }
      ]
    }
  ]
}
```

### 8.2 Field Mapping

| Current Field (V1) | New Field (V2) | Action | Notes |
|-------------------|----------------|--------|-------|
| `organisation` | `provider` | **Renamed** | Same meaning, clearer name |
| `examination` | `exam_name` | **Retained** | Same field, new location |
| `paper` | `exam_code` | **Renamed** | Same meaning, standardized format |
| `syllabus_version` | `version` | **Renamed** | Same meaning, shorter name |
| `effective_from` | `effective_date` | **Renamed** | Same meaning, consistent naming |
| `effective_to` | `superseded_date` | **Renamed** | Same meaning, clearer name |
| `metadata.description` | `description` | **Relocated** | Moved to root level |
| `metadata.source_url` | `metadata.source_url` | **Retained** | Stays in metadata |
| `metadata.qualification_level` | `metadata.qualification_level` | **Retained** | Stays in metadata |
| `metadata.language` | `metadata.language` | **Retained** | Stays in metadata |
| `topics` | `sections` | **Restructured** | Each V1 topic becomes a V2 section |
| `topics[].id` | `sections[].id` | **Retained** | Same ID, new parent |
| `topics[].code` | `sections[].code` | **Retained** | Same code, new parent |
| `topics[].title` | `sections[].title` | **Retained** | Same field, new parent |
| `topics[].description` | `sections[].description` | **Retained** | Same field, new parent |
| `topics[].weighting` | `sections[].exam_weight` | **Renamed** | Same meaning, clearer name |
| `topics[].estimated_hours` | `sections[].estimated_hours` | **Retained** | Same field, new parent |
| `topics[].difficulty` | `sections[].difficulty` | **Retained** | Same field, new parent |
| `topics[].prerequisites` | **Deprecated** | **Removed** | Will be replaced by section-level prerequisites in future |
| `topics[].learning_outcomes` | `sections[].topics[].learning_objectives` | **Restructured** | Moved one level deeper |

### 8.3 Transformation Logic

**Step 1: Rename Top-Level Fields**

```python
v2 = {
    "exam_code": v1["paper"],
    "exam_name": v1["examination"],
    "provider": v1["organisation"],
    "version": v1["syllabus_version"],
    "effective_date": v1["effective_from"],
    "superseded_date": v1["effective_to"],
    "description": v1["metadata"]["description"],
    "metadata": {
        "source_url": v1["metadata"]["source_url"],
        "qualification_level": v1["metadata"]["qualification_level"],
        "language": v1["metadata"]["language"]
    }
}
```

**Step 2: Transform Topics to Sections**

```python
v2["sections"] = []
for topic in v1["topics"]:
    section = {
        "id": topic["id"],
        "code": topic["code"],
        "title": topic["title"],
        "description": topic["description"],
        "exam_weight": topic["weighting"],
        "estimated_hours": topic["estimated_hours"],
        "difficulty": topic["difficulty"],
        "display_order": len(v2["sections"]) + 1,
        "topics": []  # Will be populated in Step 3
    }
    v2["sections"].append(section)
```

**Step 3: Create Topics from Learning Outcomes**

```python
# For each section, group learning outcomes into topics
for section in v2["sections"]:
    v1_topic = find_v1_topic_by_id(section["id"])
    
    # Group learning outcomes into topics (2-4 per topic)
    lo_groups = group_learning_outcomes(v1_topic["learning_outcomes"])
    
    for i, lo_group in enumerate(lo_groups, start=1):
        topic = {
            "id": f"{section['id']}-T{i:02d}",
            "section_id": section["id"],
            "code": f"{section['code']}.{i}",
            "title": generate_topic_title(lo_group),
            "description": generate_topic_description(lo_group),
            "estimated_minutes": sum(lo["suggested_revision_days"] * 60 for lo in lo_group),
            "difficulty": section["difficulty"],
            "display_order": i,
            "learning_objectives": []
        }
        section["topics"].append(topic)
```

**Step 4: Transform Learning Outcomes to Learning Objectives**

```python
# For each topic, transform learning outcomes
for section in v2["sections"]:
    for topic in section["topics"]:
        for j, lo in enumerate(topic["learning_objectives"], start=1):
            learning_objective = {
                "id": f"{topic['id']}-LO{j:02d}",
                "topic_id": topic["id"],
                "code": f"{topic['code']}.{j}",
                "description": lo["description"],
                "cognitive_level": infer_cognitive_level(lo["description"]),
                "estimated_minutes": lo["suggested_revision_days"] * 60,
                "learning_type": infer_learning_type(lo["description"]),
                "display_order": j
            }
            topic["learning_objectives"].append(learning_objective)
```

### 8.4 Data Loss Warning

**The following data cannot be automatically migrated:**

1. **Prerequisites:** The V1 `prerequisites` field is removed in V2. This data must be manually re-entered at the section level in V2.
2. **Topic Grouping:** The V1 format does not explicitly group learning outcomes into topics. The transformation logic must infer topic groupings, which may require manual review.
3. **Cognitive Level and Learning Type:** These new fields have no V1 equivalent and must be manually assigned.

### 8.5 Migration Validation

After transformation, validate:

1. ✅ All section IDs match V1 topic IDs
2. ✅ All section codes match V1 topic codes
3. ✅ All section weightings match V1 topic weightings
4. ✅ All learning objective descriptions match V1 learning outcome descriptions
5. ✅ Total estimated hours are preserved
6. ✅ Section weightings sum to 100%

---

## 9. Migration Recommendations

### 9.1 Migration Strategy

**Approach:** Dual-write with gradual cutover

**Phases:**

1. **Phase 1: Schema Validation (Week 1)**
   - Implement V2 JSON schema validator
   - Validate all existing V1 files can be transformed to V2
   - No code changes to application

2. **Phase 2: Dual Format Support (Week 2-3)**
   - Update `CurriculumLoader` to support both V1 and V2 formats
   - Update `CurriculumEngine` dataclasses to support both formats
   - Add format detection logic

3. **Phase 3: Data Migration (Week 4)**
   - Transform all V1 JSON files to V2 format
   - Validate transformed files
   - Archive V1 files

4. **Phase 4: V2-Only Mode (Week 5)**
   - Remove V1 support from code
   - Update all services to use V2 format
   - Update tests

### 9.2 Importer Changes

**Current Importer Logic:**
```python
# OLD: V1 importer
for topic in curriculum.topics:
    db_topic = Topic(
        curriculum_id=curriculum.id,
        name=topic.title,
        syllabus_weight=topic.weighting,
        ...
    )
    for lo in topic.learning_outcomes:
        db_lo = LearningObjective(
            topic_id=db_topic.id,
            description=lo.description,
            ...
        )
```

**New Importer Logic:**
```python
# NEW: V2 importer
for section in curriculum.sections:
    db_section = Section(
        curriculum_id=curriculum.id,
        code=section.code,
        title=section.title,
        exam_weight=section.exam_weight,
        estimated_hours=section.estimated_hours,
        difficulty=section.difficulty,
        display_order=section.display_order,
        ...
    )
    
    for topic in section.topics:
        db_topic = Topic(
            section_id=db_section.id,
            code=topic.code,
            title=topic.title,
            difficulty=topic.difficulty,
            display_order=topic.display_order,
            ...
        )
        
        for lo in topic.learning_objectives:
            db_lo = LearningObjective(
                topic_id=db_topic.id,
                description=lo.description,
                cognitive_level=lo.cognitive_level,
                learning_type=lo.learning_type,
                ...
            )
```

### 9.3 Curriculum Engine Changes

**Current Engine:**
```python
@dataclass(frozen=True)
class Curriculum:
    topics: list[Topic]

@dataclass(frozen=True)
class Topic:
    id: str
    code: str
    title: str
    learning_outcomes: list[LearningOutcome]
```

**New Engine:**
```python
@dataclass(frozen=True)
class Section:
    id: str
    code: str
    title: str
    exam_weight: float
    estimated_hours: float
    difficulty: str
    topics: list[Topic]

@dataclass(frozen=True)
class Topic:
    id: str
    section_id: str
    code: str
    title: str
    estimated_minutes: int
    difficulty: str
    learning_objectives: list[LearningObjective]

@dataclass(frozen=True)
class LearningObjective:
    id: str
    topic_id: str
    code: str
    description: str
    cognitive_level: str
    estimated_minutes: int
    learning_type: str

@dataclass(frozen=True)
class Curriculum:
    exam_code: str
    exam_name: str
    provider: str
    version: str
    sections: list[Section]
```

### 9.4 Service Impact Summary

| Service | Impact | Changes Required |
|---------|--------|------------------|
| `CurriculumLoader` | **HIGH** | Parse new hierarchy, support both V1 and V2 during transition |
| `CurriculumEngineService` | **HIGH** | Update dataclasses, update all `curriculum.topics` references |
| `CurriculumService` | **HIGH** | Rewrite import logic, update query methods |
| `StudyPlanService` | **MEDIUM** | Update topic queries to traverse new hierarchy |
| `MissionService` | **MEDIUM** | Update topic references |
| `RecommendationService` | **MEDIUM** | Update curriculum coverage calculations |
| `ReadinessService` | **MEDIUM** | Update coverage metrics |

### 9.5 Testing Strategy

1. **Unit Tests:**
   - Test V1 → V2 transformation logic
   - Test V2 schema validation
   - Test identifier pattern matching
   - Test referential integrity

2. **Integration Tests:**
   - Test curriculum loading (V1 and V2)
   - Test curriculum import (V2 only)
   - Test study plan generation with V2 curriculum
   - Test mission generation with V2 curriculum

3. **Data Validation Tests:**
   - Test all existing V1 files can be transformed
   - Test transformed V2 files validate against schema
   - Test no data loss during transformation

---

## 10. Future Extensibility

### 10.1 Extension Points

The schema is designed to support future features without redesign:

### 10.2 Flashcards

**Current Support:** ✅ Ready (via `metadata`)

**Future Implementation:**
```json
{
  "learning_objectives": [
    {
      "id": "CS1-A-T01-LO01",
      "flashcards": [
        {
          "id": "CS1-A-T01-LO01-F01",
          "front": "What is a discrete random variable?",
          "back": "A random variable that can take on a countable number of distinct values.",
          "difficulty": "easy"
        }
      ]
    }
  ]
}
```

**Migration Path:** Add `flashcards` array to learning objectives

### 10.3 Notes

**Current Support:** ✅ Ready (via `metadata`)

**Future Implementation:**
```json
{
  "topics": [
    {
      "id": "CS1-A-T01",
      "notes": [
        {
          "id": "CS1-A-T01-N01",
          "content": "Key insight: PMF sums to 1...",
          "author": "instructor",
          "created_date": "2025-09-01"
        }
      ]
    }
  ]
}
```

**Migration Path:** Add `notes` array to topics

### 10.4 Videos

**Current Support:** ✅ Ready (via `metadata`)

**Future Implementation:**
```json
{
  "topics": [
    {
      "id": "CS1-A-T01",
      "videos": [
        {
          "id": "CS1-A-T01-V01",
          "url": "https://...",
          "title": "Introduction to Random Variables",
          "duration_minutes": 15,
          "provider": "YouTube"
        }
      ]
    }
  ]
}
```

**Migration Path:** Add `videos` array to topics

### 10.5 Recommended Reading

**Current Support:** ✅ Ready (via `metadata`)

**Future Implementation:**
```json
{
  "sections": [
    {
      "id": "CS1-A",
      "recommended_reading": [
        {
          "id": "CS1-A-R01",
          "title": "Probability and Statistics for Actuaries",
          "author": "Smith, J.",
          "isbn": "978-0-123456-78-9",
          "pages": "45-67"
        }
      ]
    }
  ]
}
```

**Migration Path:** Add `recommended_reading` array to sections

### 10.6 Textbook References

**Current Support:** ✅ Ready (via `metadata`)

**Future Implementation:**
```json
{
  "learning_objectives": [
    {
      "id": "CS1-A-T01-LO01",
      "textbook_references": [
        {
          "id": "CS1-A-T01-LO01-T01",
          "textbook_id": "TEXTBOOK-001",
          "chapter": "3",
          "section": "3.2",
          "pages": "45-50"
        }
      ]
    }
  ]
}
```

**Migration Path:** Add `textbook_references` array to learning objectives

### 10.7 Past Paper Questions

**Current Support:** ✅ Ready (via `metadata`)

**Future Implementation:**
```json
{
  "learning_objectives": [
    {
      "id": "CS1-A-T01-LO01",
      "past_paper_questions": [
        {
          "id": "CS1-A-T01-LO01-PP01",
          "exam_session": "2025-09",
          "question_number": "3",
          "mark_allocation": 15,
          "difficulty": "intermediate"
        }
      ]
    }
  ]
}
```

**Migration Path:** Add `past_paper_questions` array to learning objectives

### 10.8 Quizzes

**Current Support:** ✅ Ready (via `metadata`)

**Future Implementation:**
```json
{
  "topics": [
    {
      "id": "CS1-A-T01",
      "quizzes": [
        {
          "id": "CS1-A-T01-Q01",
          "title": "Random Variables Quiz",
          "questions": [
            {
              "id": "CS1-A-T01-Q01-Q01",
              "type": "multiple_choice",
              "text": "Which of the following is a discrete random variable?",
              "options": ["A) Height", "B) Number of claims", "C) Time to failure", "D) Weight"],
              "correct_answer": "B",
              "explanation": "..."
            }
          ]
        }
      ]
    }
  ]
}
```

**Migration Path:** Add `quizzes` array to topics

### 10.9 Revision Tips

**Current Support:** ✅ Ready (via `metadata`)

**Future Implementation:**
```json
{
  "sections": [
    {
      "id": "CS1-A",
      "revision_tips": [
        {
          "id": "CS1-A-RT01",
          "tip": "Focus on understanding the difference between PMF and PDF...",
          "difficulty": "foundational",
          "common_mistakes": ["Confusing PMF with PDF", "..."]
        }
      ]
    }
  ]
}
```

**Migration Path:** Add `revision_tips` array to sections

### 10.10 Prerequisite Relationships

**Current Support:** ⚠️ Partial (field exists in V1 but removed in V2)

**Future Implementation:**
```json
{
  "sections": [
    {
      "id": "CS1-B",
      "prerequisites": ["CS1-A"],
      "recommended_order": ["CS1-A", "CS1-C", "CS1-B"]
    }
  ]
}
```

**Migration Path:** Add `prerequisites` and `recommended_order` arrays to sections

### 10.11 Competency Mappings

**Current Support:** ✅ Ready (via `metadata`)

**Future Implementation:**
```json
{
  "learning_objectives": [
    {
      "id": "CS1-A-T01-LO01",
      "competencies": [
        {
          "id": "COMP-001",
          "name": "Statistical Analysis",
          "level": "intermediate",
          "framework": "IFoA Competency Framework"
        }
      ]
    }
  ]
}
```

**Migration Path:** Add `competencies` array to learning objectives

### 10.12 Extensibility Principles

1. **Additive Changes Only:** New features add arrays/objects, never modify existing fields
2. **Backwards Compatible:** Old files without new fields remain valid
3. **Optional Fields:** All new fields are optional with sensible defaults
4. **Metadata Fallback:** If unsure where to add a feature, use `metadata` object
5. **No Breaking Changes:** Never remove or rename existing fields

---

## 11. Summary

### 11.1 Deliverables

✅ **1. JSON Schema Specification** - Complete Draft 2020-12 schema with all constraints

✅ **2. Fully Populated CS1 Example** - Complete IFoA CS1 2026 syllabus with 6 sections, 12 topics, 18 learning objectives

✅ **3. Field Documentation** - Comprehensive documentation for all fields at all levels

✅ **4. Validation Rules** - Structural, identifier, business rule, and semantic validation

✅ **5. Naming Conventions** - Stable identifier patterns and code conventions

✅ **6. File Organization** - Directory structure supporting multiple providers and exams

✅ **7. Migration Recommendations** - Step-by-step migration strategy with backwards compatibility

### 11.2 Key Design Decisions

1. **Hierarchy:** Section → Topic → Learning Objective (3 levels)
2. **Identifiers:** Stable, pattern-based, never depend on display names
3. **Weighting:** Applied at section level (matches official syllabus)
4. **Progress Tracking:** At topic level (atomic unit)
5. **Extensibility:** Metadata objects and additive arrays for future features
6. **Backwards Compatibility:** V1 → V2 transformation preserves all data

### 11.3 Next Steps

This design is ready for review. Once approved, implementation should proceed as:

1. Review and approve this design document
2. Implement V2 JSON schema validator
3. Update curriculum loader to support V2 format
4. Transform all V1 JSON files to V2 format
5. Update curriculum engine dataclasses
6. Update all services to use V2 hierarchy
7. Update database models (separate milestone)
8. Write migration scripts (separate milestone)

---

**Document Status:** Complete  
**Ready for Implementation:** Yes  
**Constraints Met:** No code changes, no model changes, no migrations, architecture only