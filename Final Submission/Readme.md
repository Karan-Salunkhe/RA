Syracuse Housing Safety Tracker

Quantifying the "Remediation Gap" in Municipal Enforcement

📌 Project Description & Motivation

In Syracuse, New York, thousands of properties are cited for code violations annually. The most severe cases are designated as "Unfit for Human Occupancy." However, identifying a safety hazard is only the first step; the true measure of urban health is the speed of resolution.

The Motivation: This project addresses a critical transparency void: How long does a dangerous property actually stay dangerous? By cross-referencing violation records with building permit data, this tracker identifies the Remediation Gap—the systemic delay between a city's "Unfit" designation and the issuance of a formal permit to begin repairs. Our analysis uncovered a median lag of 895 days, providing a quantitative foundation for policy reform, budget allocation, and community advocacy.

🚀 Core Features & Functionality

1. Neighborhood Health Scoreboard

An interactive leaderboard that ranks Syracuse’s 30+ neighborhoods. Users can filter by:

Violation Density: Violations per 1,000 residents.

Resolution Rate: Percentage of "Closed" vs. "Open" cases.

Median Backlog: The average age of unresolved violations in that specific area.

2. Geospatial "Unfit" Hotspots

Utilizing Leaflet.js, the dashboard renders a spatial heat map of high-priority enforcement actions.

Clustering: View property density in zip codes 13204 and 13205.

Detail Overlays: Click markers to view the specific "Corrective Action" required (e.g., "Supply Power" or "Structural Repair").

3. AI-Powered "Smart Auditor"

Integrated with the Gemini 2.5 Flash API, this feature provides:

Automated Narratives: Translates complex data tables into plain-English summaries.

Uncertainty Disclosures: The AI is constrained by a strict JSON schema to ensure it only reports verified metrics, preventing hallucinations regarding sensitive city data.

4. The Remediation Timeline

A longitudinal visualization showing the typical path from a minor "Interior Maintenance" report to a major "Unfit" designation, highlighting the 2.4-year average escalation period.

🛠 Technical Architecture & Stack

Layer

Technology

Purpose

Frontend

React (Vite)

Component-based UI for high-performance data rendering.

Styling

Tailwind CSS

Responsive, mobile-first design for civic accessibility.

Analysis

Python (Pandas)

Normalization of 137k+ records and address-matching logic.

Mapping

Leaflet.js

Interactive geographic visualization of property clusters.

Intelligence

Gemini API

Natural language generation and data-driven storytelling.

Charts

Recharts

Dynamic SVG charting for violation trends.

📦 Installation & Developer Setup

To run the dashboard locally or contribute to the codebase:

1. Prerequisites

Node.js (v18+)

Python 3.9+

A Google AI Studio API Key

2. Deployment Steps

# Clone the repository
git clone [https://github.com/your-username/syracuse-housing-tracker.git](https://github.com/your-username/syracuse-housing-tracker.git)
cd syracuse-housing-tracker

# Install Frontend Dependencies
npm install

# Setup Python Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure Environment Variables
echo "VITE_GEMINI_API_KEY=your_key_here" > .env


3. Execution

# Start the development server
npm run dev


📊 Data Governance & Citations

Source Data

All data is retrieved from the Syracuse Open Data Portal:

Housing Code Violations: Primary dataset for volume and status analysis.

Unfit Properties: Secondary dataset for high-severity cases.

Building Permits: Proxy dataset for remediation activity.

Ethical Standards

PII Redaction: All owner names, phone numbers, and specific apartment identifiers have been stripped to protect resident privacy.

Bias Mitigation: Violation counts are normalized against neighborhood property density to ensure fair representation of smaller neighborhoods.

⚠️ Known Limitations & Assumptions

The "Permit Gap": Many repairs (e.g., cleaning, simple painting) do not require a permit. Therefore, the "Remediation Gap" specifically measures structural and permitted recovery, not all forms of repair.

Data Entry Lags: Municipal records may have a 30-60 day reporting delay from the time an inspector closes a case to the portal update.

👤 Project Leadership

Karan C. Salunkhe Data & Business Intelligence Analyst Syracuse University | School of Information Studies (iSchool)

Status: Phase 4 Submission (April 2026)

This project was developed as part of the Syracuse Open Data Civic Challenge to promote transparency in municipal housing enforcement.
