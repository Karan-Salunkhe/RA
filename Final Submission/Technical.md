# Technical Documentation: Syracuse Housing Safety Tracker

**Project Version:** 1.0.0 (Phase 4 Release)
**Target Audience:** Developers, Data Engineers, System Maintainers

---

## 1. System Architecture

The Syracuse Housing Safety Tracker is architected as a **Decoupled Data-Driven Web Application**. It follows a *"Static Data, Dynamic Intelligence"* pattern, ensuring high performance by processing ~137,000 records server-side (or via script) while using the browser for interactive visualization and AI-driven synthesis.

### High-Level Data Flow

```
Ingestion Layer (Python)
        ↓
  Raw CSVs fetched from the Syracuse Open Data Portal

Transformation Layer (Python/Pandas)
        ↓
  • Normalization: Street addresses standardized to resolve join-key inconsistencies
  • Aggregation: Data grouped by SBL (Tax ID) and Neighborhood
  • PII Scrubbing: All owner names and contact details removed

Visualization Layer (React/Vite)
        ↓
  SPA consumes processed JSON objects to render Map and Charts

AI Service Layer (Gemini API)
        ↓
  Async hook triggers Gemini 2.5 Flash to generate "Contextual Insights"
  when a user selects a specific neighborhood or data slice
```

---

## 2. Development Setup & Environment

### Prerequisites

| Tool | Version |
|---|---|
| Node.js | v18.0.0+ (LTS recommended) |
| Python | v3.9.0+ |
| Browser | Modern Evergreen (Chrome, Firefox, Safari) |

### Environment Variables (`.env`)

The project requires the following keys to function:

| Variable | Description |
|---|---|
| `VITE_GEMINI_API_KEY` | Google AI Studio key for the Smart Auditor features. |
| `VITE_APP_ID` | Internal identifier used for Firestore-based logging (if enabled). |

### Installation Procedure

```bash
# 1. Install Node dependencies
npm install

# 2. Setup Python Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 3. Data Pipeline & Logic (The "Remediation Gap")

The project's primary analytical contribution is the measurement of the **Remediation Gap**.

### Address Normalization Algorithm

To link `Unfit_Properties.csv` (Enforcement) with `Permit_Requests.csv` (Resolution), we use a custom Regex engine:

1. **Lowercase & Strip:** Removes all punctuation and special characters.
2. **Standardization Dictionary:**
   - `STREET` / `STR` → `ST`
   - `AVENUE` / `AVE.` → `AVE`
   - `BOULEVARD` / `BLVD.` → `BLVD`
3. **Join Logic:** Inner join on `Normalized_Address` + `ZipCode`.

### Quantitative Formulae

**Remediation Lag (Days):**
$$T_{remediation} = Date_{PermitIssue} - Date_{UnfitDesignation}$$

**Enforcement Escalation (Days):**
$$T_{escalation} = Date_{UnfitDesignation} - Date_{InitialViolation}$$

**Backlog Density:**
$$\frac{\sum \text{Open Violations}}{\text{Total Neighborhood Properties}} \times 1000$$

---

## 4. AI Integration (Gemini 2.5 Flash)

The dashboard utilizes the `gemini-2.5-flash-preview-09-2025` model as a **deterministic reporting agent**.

### System-Constrained Grounding

To prevent hallucinations, the model is initialized with a **"Strict Persona"** that prohibits speculation:

- **Input Schema:** Instead of raw text, the API receives a JSON summary of the currently filtered view.
- **Temperature (`0.2`):** Set extremely low to prioritize factual accuracy over creative variance.
- **Safety Settings:** `"Harassment"` and `"Hate Speech"` filters are set to `BLOCK_NONE` (as we are dealing with public municipal records), but `"Dangerous Content"` is strictly monitored.

---

## 5. UI Component Architecture

The frontend is built using **React 18** with functional components and hooks.

### Core Component Tree

```
App.jsx
├── MetricGrid.jsx
├── SpatialEngine.jsx
└── AuditorPanel.jsx
```

| Component | Responsibility |
|---|---|
| `App.jsx` | Main entry point managing global state (selected neighborhood, date range). |
| `MetricGrid.jsx` | Uses Recharts to render the "895-day lag" distribution curve. |
| `SpatialEngine.jsx` | Wraps Leaflet.js. Uses `L.markerClusterGroup` for high-density violation markers in zip codes `13204` and `13205`. |
| `AuditorPanel.jsx` | Manages the fetch lifecycle for the Gemini API, including a custom `useBackoff` hook for rate limiting. |

---

## 6. Testing & Quality Assurance

### Data Validation

The `scripts/test_pipeline.py` suite includes:

- **Join Verification:** Ensures the normalization logic doesn't create "false positive" matches on common street names (e.g., `"Main St"` vs `"N Main St"`).
- **Null Handling:** Validates that 0-day compliance windows are excluded from median calculations as data entry errors.

### UI Testing

- **Responsive Breakpoints:** Verified for Mobile (iPhone SE), Tablet (iPad Air), and Desktop (1920×1080).
- **Accessibility:** WCAG 2.1 compliance for color contrast on the violation heatmaps.

---

## 7. Deployment & Maintenance

| Task | Detail |
|---|---|
| **Build Command** | `npm run build` |
| **CI/CD** | Automated via GitHub Actions — every push to `main` triggers a build check. |
| **Static Assets** | Processed data stored in `/public/data/` as immutable JSON files to reduce runtime API dependency. |

---

## 8. API Reference (Internal)

| Service | Method | Input | Responsibility |
|---|---|---|---|
| Geocoding | `GET` | Address String | Resolves property location for Leaflet markers. |
| Gemini LLM | `POST` | KPI JSON | Generates the "Smart Summary" narrative. |
| Data Service | `GET` | NeighborhoodID | Fetches pre-computed metrics for the Scoreboard. |

---

> **Note:** This documentation is maintained by **Karan C. Salunkhe** as part of the Syracuse Open Data Civic Project — Phase 4.
