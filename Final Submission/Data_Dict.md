# Data Dictionary: Syracuse Housing Safety Tracker

This document defines the fields and metadata for the three primary datasets used to quantify the **"Remediation Gap"** in Syracuse, NY.

---

## 1. Housing Code Violations (V2)

**Source:** [Syracuse Open Data Portal](https://data.syrgov.net)
**Description:** The primary ledger of all reported maintenance and safety issues.

| Field Name | Data Type | Description | Example |
|---|---|---|---|
| `violation_id` | Integer | Unique identifier for the violation record. | `137663` |
| `violation_date` | Date | The date the violation was officially cited by an inspector. | `2023-11-15` |
| `complaint_type` | String | Categorization of the issue (e.g., Heat, Interior, Exterior). | `HEAT SUPPLY` |
| `address` | String | Physical location of the property (Raw). | `123 MAIN ST` |
| `norm_addr` | String | ⚙ **Engineered Field:** Standardized address for dataset joining. | `123 MAIN ST` |
| `status_type_name` | String | Current enforcement state (`Open` or `Closed`). | `Open` |
| `Neighborhood` | String | The Syracuse neighborhood boundary the property falls within. | `Northside` |
| `comply_by_date` | Date | The legal deadline for the owner to resolve the issue. | `2023-12-15` |

---

## 2. Unfit Properties

**Source:** [Syracuse Open Data Portal](https://data.syrgov.net)
**Description:** A high-priority subset of properties ordered to be vacated due to extreme safety risks.

| Field Name | Data Type | Description | Example |
|---|---|---|---|
| `unfit_id` | Integer | Unique identifier for the "Order to Vacate." | `264` |
| `violation_date` | Date | The date the property was designated "Unfit." | `2022-05-10` |
| `corrective_action` | String | Specific legal requirement to lift the unfit status. | `SUPPLY POWER` |
| `zip` | Integer | Five-digit postal code. | `13204` |
| `SBL` | String | Section-Block-Lot identifier (Tax ID). | `094.-04-05.0` |

---

## 3. Building Permit Requests

**Source:** [Syracuse Open Data Portal](https://data.syrgov.net)
**Description:** Proxy dataset used to track authorized remediation activity.

| Field Name | Data Type | Description | Example |
|---|---|---|---|
| `Application_ID` | String | Unique tracking number for the permit request. | `PL-23-089` |
| `Issue_Date` | Date | The date the permit was legally issued. | `2024-02-01` |
| `Permit_Type` | String | Classification of work (e.g., Residential Remodel). | `RES REMODEL` |
| `Valuation` | Decimal | Estimated cost of the proposed repairs. | `4500.00` |
| `remediation_gap` | Integer | 🔢 **Calculated Field:** Days between Unfit status and Permit issue. | `895` |

---

## Field Type Reference

| Type | Description |
|---|---|
| `Integer` | Whole number, no decimals. |
| `String` | Free-text or categorical value. |
| `Date` | ISO 8601 format — `YYYY-MM-DD`. |
| `Decimal` | Floating-point numeric value (2 decimal places). |

---

> **Privacy Note:** All PII (owner names, phone numbers) has been excluded from this dictionary as it was redacted during the ingestion phase. See [`METHODOLOGY.md`](./METHODOLOGY.md) §2.3 for full ethical scrubbing details.
