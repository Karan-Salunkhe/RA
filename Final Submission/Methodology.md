# Methodology: Syracuse Housing Safety Tracker

**Project:** From Violation to Repair: Evaluating Housing Safety Enforcement Outcomes in Syracuse
**Author:** Karan C. Salunkhe
**Date:** April 2026
**Version:** 1.3 (Comprehensive Research Release)

---

## 1. Research Objective & Scope

The primary goal of this analysis is to quantify the **Remediation Gap**: the temporal and systemic distance between a property being designated *"Unfit for Human Occupancy"* and the commencement of authorized repairs (via Building Permits).

Housing code enforcement is frequently studied from the lens of violation *issuance* — how many properties are cited, and at what rate. This study redirects analytical attention toward the *downstream* outcome of enforcement: whether designated unsafe properties receive timely, permitted intervention. The distinction is consequential. A system that aggressively identifies violations without achieving resolution does not improve housing safety; it merely documents its failure to do so.

This research operationalizes "remediation" as the issuance of a formal Building Permit at a previously designated "Unfit" address, acknowledging that this is a conservative proxy for repair activity (see Section 6 for limitations). The Remediation Gap, therefore, captures the institutional inertia between declaration and action — a metric with direct implications for tenant displacement, neighborhood disinvestment, and municipal resource allocation.

The scope of this study is bounded to the City of Syracuse, New York, using administrative records spanning the full available history of the Syracuse Open Data Portal. No private property inspections, interviews, or primary field data were collected. All findings derive exclusively from publicly available municipal records.

### 1.1 Core Research Questions

- **Temporal Persistence:** What is the median duration a property remains in a high-severity "Unfit" state before a permit is pulled?
- **Geospatial Concentration:** Do specific zip codes (`13204`, `13205`) exhibit statistically significant clusters of enforcement stagnation?
- **Process Correlation:** To what degree does formal municipal permitting track with housing code resolution, and where does the "Permit Gap" occur?

### 1.2 Theoretical Framing

This study draws on the concept of **"regulatory capture lag"** — a phenomenon documented in urban policy literature wherein enforcement agencies successfully identify non-compliance but face structural or resource-based barriers to achieving resolution. The 895-day median Remediation Gap identified in this dataset is interpreted not as the failure of individual inspectors, but as a systemic output of underfunded enforcement infrastructure, fragmented property ownership records, and legal delays inherent to tax-delinquent or estate-encumbered properties.

Furthermore, this work contributes to the growing body of civic data science literature that advocates for *outcome-based* rather than *activity-based* metrics in evaluating municipal performance. Counting violations issued is an activity metric. Measuring the time to resolution is an outcome metric — and it is the latter that bears directly on resident welfare.

---

## 2. Data Processing & Lifecycle

### 2.1 Ingestion & Source Lineage

Data was programmatically extracted from the Syracuse Open Data Portal (CKAN) using the following source endpoints:

| Dataset | Records | Role |
|---|---|---|
| Code Violations (V2) | 137,663 | Primary enforcement ledger |
| Unfit Properties | 264 | Buildings ordered to vacate |
| Building Permits | 47,902 | Legal repair and construction activity |
| Neighborhood Boundaries | GeoJSON polygons | Spatial grouping and mapping |

All datasets were retrieved via direct CSV export. No API rate limits were encountered during ingestion. Datasets were versioned by download timestamp and stored as immutable raw files prior to any transformation, ensuring full reproducibility of the pipeline.

It is worth noting the asymmetry in record volumes: 137,663 violation records versus only 264 "Unfit" designations. This reflects the rarity of the most severe enforcement action — a property must typically accumulate multiple unresolved violations, fail re-inspection, and be formally reviewed by a Code Enforcement Officer before receiving an "Unfit" designation. The 264 records therefore represent the most critical subset of the enforcement universe, and are the analytical focal point of the Remediation Gap calculation.

### 2.2 Feature Engineering: Address Normalization

The absence of a unified Property ID across legacy municipal systems — a common structural deficiency in mid-sized American cities — necessitated the development of a custom **Normalization Engine** in Python. This was a non-trivial data engineering challenge: the Violation dataset and the Permit dataset were maintained by different city departments, with different data entry conventions, and no shared foreign key.

The normalization pipeline proceeded in four stages:

**Stage 1 — Syntactic Standardization**
All address strings were converted to uppercase. Punctuation, special characters, and non-alphanumeric tokens were stripped (e.g., `O'BRIEN ST` → `OBRIEN ST`). Whitespace was collapsed and leading/trailing spaces removed.

**Stage 2 — Suffix Mapping via Regex Lookup Table**
A regex-based dictionary resolved thoroughfare suffix inconsistencies:

| Raw Variants | Normalized Form |
|---|---|
| `STREET`, `STR`, `ST.` | `ST` |
| `AVENUE`, `AVE.` | `AVE` |
| `BOULEVARD`, `BLVD.` | `BLVD` |
| `DRIVE`, `DR.` | `DR` |
| `COURT`, `CT.` | `CT` |
| `PLACE`, `PL.` | `PL` |

**Stage 3 — Composite Key Construction**
A deterministic join key was constructed as: `HouseNumber + StandardizedStreet + ZipCode`. This three-part key was chosen over address string alone to prevent false-positive matches on common street names that span multiple zip codes (e.g., `MAIN ST` exists in both `13210` and `13204`).

**Stage 4 — SBL Cross-Validation**
Where the Section-Block-Lot (SBL) tax parcel identifier was present in both datasets, it was used as a secondary verification layer. Address-matched records that disagreed on SBL were flagged for manual review rather than automatically included in the analytical join. This conservative approach prioritized precision over recall, accepting some data loss to prevent false linkages.

The final inner join yielded a match rate of approximately **61%** of "Unfit" properties to at least one Building Permit record — meaning 39% of designated "Unfit" properties show *no permitted repair activity* in the dataset whatsoever. This finding is itself analytically significant and is discussed further in Section 6.

### 2.3 Ethical Scrubbing (PII)

In compliance with Syracuse University's Ethical Data Standards and consistent with best practices in civic data analysis:

- **Owner Redaction:** All individual and corporate owner names were removed from the analytical dataset prior to any export or visualization rendering. This prevents the tool from being used as a mechanism for predatory real estate targeting or tenant harassment.
- **Privacy Buffering:** Specific apartment and unit numbers were stripped from all address fields to protect tenant anonymity in multi-family dwellings, where unit-level identification could expose individual residents.
- **Aggregation Floor:** No neighborhood-level statistics are displayed publicly if the underlying sample size is fewer than 10 matched records, to prevent de-anonymization through small-cell inference.

---

## 3. Statistical Framework & EDA

### 3.1 Distribution Analysis: Why Medians Matter

For the headline **895-day Remediation Gap**, the analytical choice to report the *median* rather than the *mean* was deliberate and methodologically significant.

Municipal enforcement data is structurally right-skewed. The distribution of remediation lag times is not normal; it contains a long right tail populated by what this study terms **"Zombie Properties"** — parcels stalled in tax foreclosure, unresolved probate proceedings, or absentee ownership disputes for periods exceeding 10 years. In a dataset with even a small number of such extreme outliers (e.g., a property with a 4,000-day lag), the arithmetic mean is disproportionately inflated.

To illustrate: in the present dataset, the *mean* remediation lag is approximately **1,340 days** — nearly 50% higher than the median. Reporting this figure as the "average" experience would misrepresent the typical enforcement cycle for the majority of properties. The median, by contrast, is robust to outliers and represents the 50th percentile of actual outcomes — the lag experienced by the "typical" unfit property in Syracuse.

For secondary analyses (e.g., neighborhood-level comparisons), we additionally report the **interquartile range (IQR)** to convey distributional spread, and flag neighborhoods where the IQR exceeds 500 days as exhibiting high enforcement *variance* — a distinct finding from high enforcement *lag*.

### 3.2 Geospatial Normalization & Density Correction

Raw violation counts are an unreliable basis for neighborhood comparison because they conflate the *prevalence* of violations with the *size* of the neighborhood. A neighborhood with 800 violations and 10,000 residential parcels has a fundamentally different enforcement profile than one with 800 violations and 1,500 parcels — yet raw counts treat them identically.

To correct for this, we applied a **Density Normalization** formula:

$$V_{density} = \left( \frac{\text{Total Neighborhood Violations}}{\text{Total Residential Parcels}} \right) \times 1000$$

This yields a **Violations per 1,000 Homes** metric that enables fair cross-neighborhood comparison. The normalization is particularly important for smaller, historically disinvested neighborhoods like Skunk City and the Near Westside, which would otherwise be obscured by the raw volume of larger administrative districts like the Northside.

Residential parcel counts were derived from the Neighborhood Boundaries GeoJSON dataset, cross-referenced against the Onondaga County property tax roll to exclude commercial, industrial, and vacant land parcels from the denominator. Using total parcel count (including non-residential) as the denominator would artificially suppress density scores in commercially mixed neighborhoods, introducing a systematic bias against residential areas.

### 3.3 Exploratory Data Analysis (EDA) Techniques

Our EDA phase, conducted prior to hypothesis formulation, identified several critical hidden variables that shaped the final analytical framework:

**Seasonality of Violations**
A statistically notable **22% spike in violation filings during winter months (December–February)** was observed, correlating directly with heating failure reports and exterior maintenance failures attributable to freeze-thaw cycles. This seasonal pattern has a methodological implication: point-in-time snapshots of "open violations" will systematically overcount if taken in Q1, and undercount if taken in Q3. All aggregate statistics in this study are therefore computed over full calendar years to neutralize seasonal bias.

**Status Attrition: The "Administrative Closure" Problem**
EDA revealed a structurally important artifact in the violation status field: a non-trivial proportion of violations are marked "Closed" not because physical repairs were verified, but because the violation record *expired* administratively — either due to inspector turnover, case age-out policies, or re-inspection scheduling failures. This "Closed Loop" phenomenon means the raw "Resolution Rate" metric is an *optimistic overestimate* of actual physical remediation. To address this, the study's Resolution Rate metric was recalculated to exclude records where the closure method was coded as administrative expiration, flagged via the `CLOSE_REASON` field in the source data.

**Permit Type Stratification**
Not all Building Permits reflect remediation activity. Permits for new construction, demolition, or cosmetic renovation were excluded from the Remediation Gap calculation. Only permits with a `WORK_TYPE` classification of *Repair*, *Rehabilitation*, or *Electrical/Plumbing Restoration* were included as valid indicators of remediation. This stratification reduced the usable permit universe from 47,902 to approximately 19,400 records.

---

## 4. AI Logic & Validation Framework

The project integrates the `gemini-2.5-flash-preview-09-2025` model to provide accessible, plain-language interpretations of complex civic data for non-technical users — including residents, community advocates, and city council members who may lack data literacy but have a direct stake in the findings. However, the deployment of a generative AI model in a civic accountability context introduces a non-trivial risk of **confabulation**: the generation of plausible but factually unsupported statements that could mislead public discourse or undermine trust in the tool.

To mitigate this risk, we implemented a **Three-Tier Validation Architecture** that treats the LLM not as a free-form narrator, but as a constrained, data-grounded reporting agent.

### 4.1 Layer 1: Contextual Grounding (The JSON "Cage")

The LLM is never given open-ended internet access or access to the full dataset. Instead, each API call is constructed to include a **"KPI Context Object"** — a structured JSON payload containing *only* the metrics relevant to the user's current view (e.g., a specific neighborhood's violation count, median lag, and resolution rate).

```json
{
  "neighborhood": "Northside",
  "total_violations": 2859,
  "median_lag_days": 912,
  "resolution_rate_pct": 43.2,
  "confidence_tier": "HIGH"
}
```

The system prompt explicitly instructs the model: *"If a number is not present in the JSON object provided, it does not exist. Do not infer, estimate, or extrapolate figures not contained in this input."* This constraint eliminates the most common failure mode of civic AI tools — the generation of authoritative-sounding but fabricated statistics.

### 4.2 Layer 2: Uncertainty Guardrails

Statistical confidence varies significantly across neighborhoods due to the uneven match rate of the address normalization join. Where the permit-to-violation match rate for a specific neighborhood falls below a **30% confidence threshold**, the application automatically injects a structured warning into the system prompt prior to generation:

> *"Warning: Statistical confidence for this neighborhood is limited by a small sample size of matched permits. You must explicitly disclose this limitation to the user in your response and refrain from drawing directional conclusions."*

This forces the model to surface data limitations rather than paper over them — a behavior that would not occur without explicit architectural enforcement, as LLMs are by default trained to produce fluent, confident-sounding text regardless of evidential basis.

### 4.3 Layer 3: Post-Generation Numerical Verification

As a final safeguard, a **JavaScript regex-based verification pass** is applied to every AI-generated response before it is rendered to the user. The verifier extracts all numerical claims (percentages, day counts, case volumes) from the generated text and cross-references them against the source KPI Context Object within a **±1% margin of error** to account for rounding.

If any numerical claim in the AI output cannot be matched to the source data within this tolerance, the response is silently discarded and the user is presented with a **"Data Mismatch Error"** notification, rather than the hallucinated content. This post-generation layer acts as a hard factual backstop independent of the model's instruction-following behavior — a critical redundancy given that prompt adherence is probabilistic, not guaranteed, in current-generation LLMs.

---

## 5. Auditability & Governance

To ensure this tool meets the evidentiary standards required for use by city officials — including the Syracuse Office of Accountability and Performance and the Common Council — every AI-generated insight is logged with the following provenance metadata:

| Field | Description |
|---|---|
| `dataset_hash` | SHA-256 fingerprint of the specific CSV version used for the analysis, enabling exact reproducibility. |
| `prompt_version` | The semantic version of the system instructions in use at generation time (e.g., `v1.2.4`), allowing regression testing if prompt logic is updated. |
| `generation_timestamp` | UTC timestamp of the API call, enabling correlation with known data portal update cycles. |
| `confidence_tier` | The confidence classification (`HIGH`, `MEDIUM`, `LOW`) assigned to the neighborhood at time of generation. |
| `numerical_verification_status` | Pass/Fail result of the Layer 3 post-generation check. |

This audit log is stored as an append-only record and is not exposed in the public UI. Its purpose is to enable retrospective validation of any insight that is cited in a policy document, news article, or public meeting — providing a chain of custody from data source to generated statement.

---

## 6. Caveats & Assumptions

### The "Permit Gap" (Primary Limitation)

The most significant structural limitation of this study is the operationalization of "remediation" as permitted construction activity. Municipal Building Permits are required for structural repairs, electrical work, plumbing replacement, and HVAC installation — but they are *not* required for a wide range of remediation activities including interior cleaning, painting, debris removal, utility reconnection by the service provider, or minor habitability repairs below a monetary threshold. Consequently, the **Remediation Gap** metric specifically captures *structural and permitted recovery*, not all forms of repair activity. Properties where a landlord remediated conditions through non-permitted means will appear in this dataset as "unresolved" even if they are physically habitable.

The practical implication is that the 895-day median lag is best interpreted as a measure of *formal, documented* remediation rather than a comprehensive measure of physical repair. It is possible — though unverifiable from this dataset — that a subset of properties were informally remediated but lack a permit record. This study takes the conservative position that undocumented remediation cannot be credited in an accountability framework.

### Reporting Delay

All municipal records reflect an estimated **30–60 day administrative lag** between the date an inspector closes or updates a case in the field and the date that change is reflected in the public Open Data Portal. This lag means that the most recently filed violations and permits are systematically underrepresented in the dataset. For the purposes of trend analysis, data from the final 60 days prior to the extraction date is treated as provisional and excluded from longitudinal calculations.

### The 39% Unmatched "Unfit" Properties

As noted in Section 2.2, approximately 39% of "Unfit" designated properties could not be matched to any Building Permit record. Three interpretations are possible: (1) the property was remediated without a permit; (2) the property remains unresolved and has received no formal repair activity; or (3) the address normalization engine failed to identify an existing permit due to data entry inconsistencies beyond the scope of the current normalization rules. Distinguishing between these cases is not possible from the available data and represents the primary avenue for future research — ideally through direct integration with the city's internal permit management system, which may contain records not yet published to the open data portal.

### Temporal Scope

This analysis is bounded by the availability of records on the Syracuse Open Data Portal. Historical enforcement records prior to the portal's launch may exist in paper or legacy digital formats that were not digitized. Properties with very long remediation histories that began before the digital record era may have their "Unfit" designation date truncated at the portal's earliest available record, artificially compressing some lag measurements.

---

> **Cross-References:**
> For development specifications, see [`TECHNICAL_DOCS.md`](./TECHNICAL_DOCS.md).
> For user instructions and feature overview, see [`README.md`](./README.md).
