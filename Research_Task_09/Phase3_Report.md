# Phase 3 Report: Syracuse Housing Safety Tracker

## Dashboard Screenshot

<img width="809" height="522" alt="Dashboard" src="https://github.com/user-attachments/assets/d941218f-dcb6-4b40-a28f-a8ce4a0b659f" />




*Figure 1: Interactive dashboard visualizing housing safety violations, geospatial hotspots, and AI-generated neighborhood insights.*

---

## Project Information

- **Project Title:** *From Violation to Repair: Evaluating Housing Safety Enforcement Outcomes in Syracuse*  
- **Author:** Karan C. Salunkhe  
- **Date:** January 16, 2026  
- **Status:** Phase 3 Complete — *Functional Development, Geospatial Analysis & AI Integration*

---

## 1. Project Vision & Implementation Overview

The **Syracuse Housing Safety Tracker** has evolved from a Phase 2 data exploration exercise into a fully functional, interactive public-facing dashboard. The project directly addresses the city’s *“Remediation Gap”* by creating a transparent, data-driven view of the housing enforcement lifecycle—from initial violation to repair resolution.

This tool empowers:
- **Residents**, by improving visibility into housing safety conditions and enforcement outcomes  
- **City officials and analysts**, by identifying systemic delays and operational bottlenecks in the enforcement-to-repair pipeline  

### Interactive Dashboard Architecture

The application is implemented as a **single-page immersive dashboard**, integrating real-time filtering with high-volume geospatial rendering. The interface is optimized to handle **over 137,000 violation records** without performance degradation, ensuring responsiveness during exploratory analysis.

---

## 2. Technical Stack & Functional Specifications

### Frontend & Data Engineering

- **Framework:** React.js utilizing `useState` and `useEffect` hooks for dynamic, multi-dimensional state management  
- **Styling:** Tailwind CSS for a modern, responsive UI optimized for both desktop and mobile environments  
- **Data Visualizations:** Recharts for efficient SVG-based rendering of:
  - Violation trends over time  
  - Status distributions  
  - Neighborhood-level comparisons  
- **Geospatial Layer:** Leaflet.js with custom marker clustering to visualize concentrations of *“Unfit”* properties across Syracuse, with a focus on ZIP codes **13204** and **13205**

### Intelligence Layer (Gemini API)

- **Contextual Summarization:** Integration of the `gemini-2.5-flash-preview-09-2025` model to generate natural-language summaries describing neighborhood housing conditions  
- **Prompt Engineering:** Custom system prompts enable the AI to:
  - Interpret *Open vs. Closed* violation ratios  
  - Generate actionable, community-focused insights based on the user’s current data slice  

---

## 3. Iterative Development & Sprint Outcomes

### Sprint 1: UI Scaffolding & Component Design

- **Outcome:** Established a **Three-Pillar Layout**:
  1. KPI Header  
  2. Analytical Core  
  3. Spatial Footer  
- **Refinement:** Transitioned from a multi-page application to a single-dashboard design to minimize user friction during exploration

### Sprint 2: Address Normalization Engine

- **Challenge:** Enforcement and permit datasets used inconsistent street naming conventions (e.g., *“Ave”* vs. *“Avenue”*)  
- **Solution:** Developed a custom address normalization function that:
  - Removed punctuation  
  - Standardized suffix abbreviations  
- **Impact:** Significantly improved match rates for **Time-to-Repair** analysis

### Sprint 3: Geospatial Hotspot Mapping

- **Outcome:** Successfully mapped **264 “Unfit” properties** across Syracuse  
- **Key Discovery:** Violation hotspots are spatially correlated with **historical industrial boundaries**, particularly in the **Near Westside**, rather than being randomly distributed

### Sprint 4: AI Feature Integration

- **Outcome:** Implemented an **“Ask the Data”** feature that generates Gemini-powered explanations for:
  - Rising neighborhood backlogs  
  - Enforcement delays  
  - Spatial disparities  

---

## 4. Analytical Findings & AI Validation

| Finding | Data Evidence | AI / LLM Validation |
|------|-------------|-------------------|
| **The Remediation Gap** | Only **4%** of *Unfit* properties matched to permit records | AI identified that many resolutions occur *off-permit* (e.g., utility reconnections) |
| **Temporal Inequity** | Median lag of **895 days** to reach *Unfit* designation | AI hypothesized systemic staffing shortages and legal grace periods |
| **Seasonality Effect** | **22% spike** in violations during December–February | AI correlated trends with *Heat Supply* violations and winter infrastructure stress |

---

## 5. Success Metrics, Ethics & Future Scope

### Success Metrics

- **Efficiency:** Users can compute neighborhood-specific compliance windows in **under 10 seconds**  
- **Transparency:** The full enforcement lifecycle—from complaint to final resolution—is now visible and auditable

### Ethical Guardrails & Bias Mitigation

- **Privacy Protection:** Owner names and unit-level apartment numbers were redacted to prevent tenant targeting or predatory real estate behavior  
- **Bias Mitigation:** Violation counts were normalized by property density to prevent unfair stigmatization of high-density neighborhoods

### Future Scalability

The system architecture supports expansion to include:
- Syracuse **Lead Risk** datasets  
- **Demolition records**  
- A future **Predictive Risk Score**, leveraging machine learning to forecast which properties are most likely to become *Unfit* based on early-stage violations

### Administrative Compliance

- **OPT / Research Reporting:** All bi-monthly check-ins completed (January 1 and January 15)  
- **Open Source Commitment:** Full React source code and data processing scripts are hosted on GitHub to support transparency and community auditing
