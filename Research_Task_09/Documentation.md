---
title: "AI Integration & Validation Documentation"
subtitle: "Syracuse Housing Safety Tracker — Phase 3."
author: "Karan C. Salunkhe."
date: "January 2026."
output:
  html_document:
    toc: true
    toc_depth: 3
    number_sections: true
---

# Project Overview

**Project:** From Violation to Repair: Syracuse Housing Safety Tracker  
**Phase:** Phase 3 — AI Integration, Validation & Governance  
**LLM:** `gemini-2.5-flash-preview-09-2025`

This document describes the technical design, prompt engineering strategy, validation pipeline, and quality assurance controls implemented to integrate Large Language Model (LLM)–based narratives into the Syracuse Housing Safety Tracker.

The objective of the AI layer is to generate *civically responsible, plain-English summaries* of housing enforcement metrics while ensuring statistical fidelity, uncertainty transparency, and zero hallucination risk.

---

# 1. AI Design Objectives

The AI component is designed to meet the following non-negotiable constraints:

- **Deterministic grounding:** All numerical outputs must originate from computed metrics.
- **Explainability:** Narratives must clearly separate observed facts from inferred hypotheses.
- **Uncertainty disclosure:** The model must explicitly state when data is incomplete or insufficient.
- **Fail-safe behavior:** When inputs are invalid, the system must return structured refusal responses rather than speculative text.

---

# 2. Prompt Engineering Strategy

## 2.1 System-Constrained Grounding

A **System Instruction–first architecture** is used to tightly constrain model behavior. The system role establishes both *domain expertise* and *epistemic limits*.

### System Instruction (Authoritative Persona)

```text
You are a Housing Policy Auditor for the City of Syracuse.

You are provided with computed, verified metrics related to housing code violations,
Unfit properties, and remediation timelines.

Rules:
1. You must only reference statistics explicitly provided in the prompt context.
2. You must not estimate, extrapolate, or invent values.
3. If the user asks a question that cannot be answered using the provided data,
   you must explicitly state that the information is unavailable.
4. Any explanation of causes must be grounded in observed fields
   (e.g., corrective_action, permit_status).
5. When data quality is limited, you must disclose uncertainty.
This instruction is injected before all user content and overrides any conversational tendencies of the model.

2.2 Prompt Context Structure
All prompts follow a fixed schema to minimize variance:

{
  "city_kpis": {
    "total_open_violations": 2859,
    "remediation_gap_pct": 19.5,
    "median_unfit_days": 895
  },
  "neighborhood_metrics": {
    "name": "Northside",
    "open_violations": 2859,
    "matched_permits_pct": 41.2
  },
  "data_quality_flags": {
    "small_sample_warning": false,
    "date_inconsistencies_present": true
  }
}
The model is explicitly instructed that this JSON block represents ground truth and must be treated as immutable.

3. Prompt Iteration Log
Iteration	Prompt Focus	Observed Issue	Mitigation Implemented
V1	Generic neighborhood summary	Hallucinated 2024 statistics	Introduced strict system instruction
V2	Neighborhood-level summary	Ignored remediation duration	Injected "Critical Metrics" block
V3	Causal explanation	Political speculation	Added hypothesis restriction rules
V4	Final	Stable, accurate, cautious	Locked schema + unit tests
4. Data-to-Prompt Validation Pipeline
4.1 Metric Computation Layer
All metrics are computed prior to LLM invocation using Python and Pandas.

median_days = (
    unfit_df["resolution_date"] - unfit_df["designation_date"]
).dt.days.median()

backlog_pct = (
    open_violations / total_violations
) * 100
No raw records are passed directly to the LLM.

4.2 Prompt Injection Mechanism
Computed KPIs are serialized to JSON and injected verbatim into the prompt context.

prompt_context = json.dumps(kpis, ensure_ascii=False)
This ensures:

Numerical determinism

Reproducibility

Full traceability from source data to narrative output

4.3 Output Verification (Unit Testing)
A post-generation validation step enforces numeric fidelity.

def test_llm_percentages(llm_output, source_df):
    extracted = extract_percentages(llm_output)
    for value in extracted:
        assert abs(value - source_df["expected"]) < 1.0
If validation fails, the response is discarded and replaced with a system error message.

5. Uncertainty & Data Quality Guardrails
5.1 Small Sample Size Detection
If the match rate between Unfit properties and issued permits falls below a defined threshold:

if match_rate < 0.30:
    data_quality_flags["small_sample_warning"] = True
The model is instructed to prepend a warning disclaimer in its response.

5.2 Hypothesis Constraints
The AI may only reference causal explanations that are directly observable in the dataset:

Allowed:

Missing permits

Repeated inspection failures

Administrative lag indicators

Disallowed:

Political decisions

Budget allocations

Owner financial status (unless explicitly present)

6. Example AI Narrative Output
User Query:

What is the status of the Northside neighborhood?

AI Response:

Based on current city records, the Northside neighborhood contains 2,859 unresolved housing code violations, representing the largest concentration of open cases city-wide.

Properties designated as Unfit remain in that status for a median duration of 895 days, contributing significantly to the overall Remediation Gap of 19.5%.

While permit activity exists, only 41.2% of Unfit properties show a corresponding repair permit. Data on owner financial capacity or external constraints is not available in this dataset; therefore, observed delays can only be attributed to documented administrative and permitting timelines.

7. Edge Case Handling
7.1 Invalid Geographic Queries
If a user queries a neighborhood outside the GIS boundary set:

if neighborhood not in valid_shapes:
    return "Data Unavailable: Neighborhood not found in city records."
No inference or fallback guessing is permitted.

7.2 Temporal Inconsistencies
If permit dates precede violation dates:

if permit_date < violation_date:
    record.flag = "Inconsistent Entry"
Flagged records are excluded from duration metrics and explicitly referenced as data quality issues.

8. Governance & Auditability
Every AI-generated narrative can be traced back to:

Source dataset version hash

KPI computation timestamp

Prompt JSON payload

Validation test results

This design ensures the AI layer functions as an interpretable reporting interface, not a decision-making authority.

9. Summary
The Phase 3 AI integration prioritizes statistical accuracy, civic responsibility, and explainability. By combining deterministic metric computation with constrained language generation and automated validation, the system delivers accessible narratives without compromising analytical integrity.

This approach establishes a scalable blueprint for responsible AI use in municipal analytics.
