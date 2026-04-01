---
Title: "Phase 2 Report: Housing Safety Enforcement Data Exploration"
Author: "Karan C. Salunkhe"
Date: "January 1, 2026"
---

# Project Title  
**From Violation to Repair: Evaluating Housing Safety Enforcement Outcomes in Syracuse**

**Status:** Phase 2 Complete — *Data Acquisition & Validation*

---

## 1. Data Acquisition and Validation

### Dataset Overview

This report analyzes four primary datasets characterizing the municipal housing safety lifecycle:

- **Housing Code Violations (V2):** 137,663 records of documented safety and maintenance issues  
- **Unfit Properties:** 264 high-priority records of buildings designated unfit for human occupancy  
- **Building Permit Requests:** 47,902 records indicating remediation and repair activity  
- **Neighborhood Boundaries:** Geographic polygons for spatial aggregation and comparative analysis  

**Acquisition Date:** January 1, 2026  
**Lineage:** Raw CSV files are preserved. All transformations were performed using **Python (Pandas)**.  
All personally identifiable information (Owner names, Inspector IDs) was removed to maintain ethical data standards.

---

### Data Quality Assessment

**Completeness**

- Over **99% coverage** for **SBL (Tax ID)** and **Neighborhood** fields in the violations dataset.

**Logical Consistency**

- Identified **11 properties** where building permits were successfully matched to "Unfit" designations using normalized address matching.
- This provides a small but valid sample for **time-to-repair** analysis.

**Integration Challenges**

- Street naming conventions varied (e.g., `"Street"` vs `"ST"`).
- A normalization algorithm stripped punctuation and standardized suffixes to improve join accuracy between **Unfit** and **Permit** datasets.

---

## 2. Key Statistical Summaries

### Housing Enforcement Health *(N = 137,663)*

| Metric | Value |
|--------|-------|
| Median Time to Unfit Designation | **895 days** from initial violation |
| Median Time to Repair Permit | **1,153 days** from "Unfit" status |
| Primary Backlog Area | **Northside** (2,859 unresolved violations) |
| System Status | **80.5% Closed**, **19.5% Open** |

---

## 3. Exploratory Data Analysis (Visualizations)

### 3.1 Top 10 Violation Types
<img width="1000" height="600" alt="Top 10 Violation types in SYR" src="https://github.com/user-attachments/assets/21853b8c-7d2f-43a9-899c-75c7bdf07e0a" />

**Interpretation:**  
Property Maintenance (Internal) and Heat Supply issues dominate the enforcement docket, highlighting critical public health concerns.

### 3.2 Seasonal Distribution of Violations 
<img width="1000" height="600" alt="Monthly Distribution of code violations" src="https://github.com/user-attachments/assets/8a8dff0e-f729-47ba-94c7-dfda07a61cff" />

**Interpretation:**  
Violation reports spike in winter months, likely driven by heating failures and emergency interior inspections.

### 3.3 Proportion of Open vs. Closed Violations
<img width="800" height="800" alt="Pie chart open vs closed violations" src="https://github.com/user-attachments/assets/882bf2aa-7d2b-4a60-8693-9d6f991d5a4e" />

**Interpretation:**  
Although most cases are resolved, nearly **1 in 5 violations remains Open**, representing a substantial backlog.

### 3.4 Unfit Properties by Zip Code 
<img width="1000" height="600" alt="Unfit prop count by zip code" src="https://github.com/user-attachments/assets/e14e3103-d9ab-4304-bcd9-0eb19cba8d3c" />

**Interpretation:**  
High-severity enforcement is concentrated in specific zip codes (**13204, 13205**), identifying priority zones for Phase 3 resource allocation.

### 3.5 Top 10 Building Permit Types  
<img width="1000" height="600" alt="Top 10 building permit types" src="https://github.com/user-attachments/assets/8c7a6e18-a877-432b-8b6f-2cf3d2b3e259" />

**Interpretation:**  
"Res. Remodel" and "Sidewalk Replace" dominate, suggesting remediation is primarily focused on structural and exterior maintenance.

### 3.6 Neighborhood Violation Volume (Top 15) 
<img width="1200" height="600" alt="Top 15 neighbourhoods by violation volume" src="https://github.com/user-attachments/assets/8a6e764a-57f4-46da-b498-a636f8c4d4b6" />

**Interpretation:**  
**Northside** and **Near Westside** exhibit the highest enforcement volumes, warranting deeper analysis of owner occupancy patterns.

### 3.7 Violation Status Heatmap by Top Neighborhoods  
<img width="1200" height="600" alt="Heatmap Violation status of hood" src="https://github.com/user-attachments/assets/8c1f6e9e-559a-48e4-ae52-2a7594ab11f9" />

**Interpretation:**  
Northside not only has the most violations, but also the highest absolute number of **Open** cases.

### 3.8 Yearly Building Permit Trends  
<img width="1000" height="600" alt="Yearly building permit issuance (2011- 2025)" src="https://github.com/user-attachments/assets/1333892e-65c5-4135-86cf-fe522711376f" />

**Interpretation:**  
Permit activity remained stable with slight post-2020 recovery, reflecting consistent citywide maintenance investment.

### 3.9 Distribution of Required Compliance Windows  
<img width="1000" height="600" alt="Distibution of required complaince windows (Days)" src="https://github.com/user-attachments/assets/52998320-ad07-412e-ae7c-ef39939e2b99" />

**Interpretation:**  
Most owners receive **30–60 days** to comply, yet the **895-day median** to Unfit designation indicates major enforcement delay.

### 3.10 Common Required Corrective Actions  
<img width="1000" height="600" alt="Most common required corrective actions for unifit props" src="https://github.com/user-attachments/assets/8345628f-58ca-4219-9c98-beae93d11baf" />

**Interpretation:**  
"Remove Unfit Violation" and "Supply Power" are the most frequent orders, revealing utility loss as a leading driver of uninhabitable conditions.

---

## 4. Findings & Hypotheses

### **Finding: The Remediation Gap**

Only **11 properties** in the Unfit dataset matched to repair permits.  
This suggests a systemic breakdown where severe safety violations fail to translate into permitted repairs, increasing risk of property abandonment.

### **Hypothesis 1: Arterial Backlog**

Neighborhoods with high **Open violation** counts (e.g., Northside) likely experience lower permit pull rates due to owner financial constraints.

### **Hypothesis 2: Temporal Inequity**

The **895-day delay** before Unfit designation indicates properties remain trapped in minor-violation cycles for years before serious enforcement occurs.

---

## 5. LLM-Assisted Analysis & Validation

**LLM Insight**

An LLM was used to explore reasons for the low permit match rate.  
It suggested:
- Off-permit minor repairs
- Entry into tax foreclosure

**Validation**

Review of the **Corrective Action** field confirmed that many requirements involve cleaning or basic utility restoration — activities often not requiring permits — validating the "Permit Gap" explanation.

**Bias Mitigation**

To prevent neighborhood bias, all violation volumes were normalized against total property counts per neighborhood, ensuring analysis reflects **relative density**, not raw population size.
