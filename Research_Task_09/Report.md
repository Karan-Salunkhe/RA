---
title: "From Violation to Repair: Evaluating Housing Safety Enforcement Outcomes in Syracuse"
author: ""
date: ""
output:
  html_document:
    toc: true
    toc_depth: 2
    number_sections: true
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE, message = FALSE, warning = FALSE)
```

# Project Summary

Unsafe housing conditions directly affect public health, safety, and quality of life. This project evaluates how housing code violations in Syracuse progress through enforcement and resolution. By linking housing code violations, unfit property designations, and building permit requests, the analysis examines whether unsafe conditions escalate appropriately and whether they result in timely repairs. The goal is to identify neighborhoods where enforcement or remediation delays persist and provide actionable insights for improving housing safety outcomes.

# Problem Statement

The City of Syracuse actively enforces housing codes to protect residents from unsafe living conditions. However, enforcement alone does not guarantee resolution. Some properties accumulate repeated violations, escalate to unfit status, or remain unresolved for extended periods.

This project addresses the following civic question:

> **How effectively does housing code enforcement translate into corrective action, and where do delays or breakdowns occur across Syracuse neighborhoods?**

Understanding the full enforcement-to-repair lifecycle can help city departments, housing advocates, and community organizations prioritize resources and improve outcomes for residents.

# Stakeholders and Audience

The primary stakeholders and intended audience for this project include:

- City of Syracuse Department of Neighborhood and Business Development
- Code Enforcement and Housing Inspection teams
- Public health and neighborhood planning officials
- Housing advocacy organizations
- Residents concerned about unsafe housing conditions

# Data Sources

This project uses official City of Syracuse Open Data datasets that are maintained and updated periodically. Analyses are conducted using documented data snapshots to ensure reproducibility.

- **Housing Code Violations**  
  Records of housing code violations including violation type, dates, status, and geographic location. This dataset serves as the primary indicator of unsafe housing conditions.

- **Unfit Properties**  
  Properties officially designated as unfit for human occupancy, representing severe and escalated safety risks.

- **Permit Requests**  
  Building permit issuance data indicating repair or remediation activity following housing code violations.

- **Neighborhood Boundary Dataset**  
  Official geographic boundary polygons used for spatial aggregation and neighborhood-level analysis.

# Technical Approach

The analysis follows a structured and reproducible workflow:

1. Acquire datasets from the City of Syracuse Open Data portal
2. Remove all personally identifiable information (e.g., owner names, addresses, inspector identifiers)
3. Standardize address formats and date fields
4. Perform spatial joins using latitude and longitude to assign records to official neighborhood boundaries
5. Sequence events temporally to evaluate progression from violation to unfit designation to permit issuance
6. Aggregate metrics at the neighborhood level for comparison and visualization

The project emphasizes transparent, descriptive, and comparative analysis. No black-box machine learning models are used. All claims are validated through direct calculation, and limitations are explicitly documented.

# Deliverable Description

The final deliverable will be a neighborhood-level analytical dashboard accompanied by a written report. The dashboard will present maps and timelines visualizing housing code violations, unfit properties, and repair activity over time. The report will summarize key findings, highlight disparities across neighborhoods, and document data limitations and assumptions.

# Success Criteria

The project will be considered successful if it:

- Identifies neighborhoods with the highest concentration of unresolved housing violations
- Quantifies time delays between violation, unfit designation, and permit issuance
- Clearly documents enforcement gaps and data limitations
- Produces visualizations understandable to non-technical stakeholders
- Results in a portfolio-ready project suitable for public-sector audiences

# Timeline

- **Week 1**: Dataset review, scope confirmation, stakeholder identification
- **Week 2**: Proposal finalization and preparation for exploratory data analysis

# Risks and Mitigations

- **Address inconsistencies**: Mitigated through spatial joins and neighborhood-level aggregation
- **Incomplete permit linkage**: Documented explicitly as a limitation
- **Privacy concerns**: All personally identifiable information removed prior
