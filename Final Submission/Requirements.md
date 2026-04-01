# ─────────────────────────────────────────────────────────────
# Syracuse Housing Safety Tracker — Python Requirements
# Author : Karan C. Salunkhe
# Version: 1.0.0 (Phase 4 Release)
# Install: pip install -r requirements.txt
# Python : 3.9+
# ─────────────────────────────────────────────────────────────

# ── Core Data Processing ──────────────────────────────────────
pandas==2.2.2
numpy==1.26.4

# ── Address Normalization & String Matching ───────────────────
regex==2024.4.16
fuzzywuzzy==0.18.0
python-Levenshtein==0.25.1        # speeds up fuzzywuzzy

# ── Geospatial & Mapping ──────────────────────────────────────
geopandas==0.14.4
shapely==2.0.4
pyproj==3.6.1
fiona==1.9.6

# ── Data Ingestion (Syracuse Open Data Portal / CKAN) ─────────
requests==2.31.0
urllib3==2.2.1

# ── Statistical Analysis ──────────────────────────────────────
scipy==1.13.0
statsmodels==0.14.2

# ── EDA & Visualization (Python side) ────────────────────────
matplotlib==3.8.4
seaborn==0.13.2
plotly==5.22.0

# ── Jupyter / Notebook Support ───────────────────────────────
jupyter==1.0.0
notebook==7.1.3
ipykernel==6.29.4
nbformat==5.10.4
nbconvert==7.16.6

# ── Data Export & Serialization ──────────────────────────────
openpyxl==3.1.2                   # Excel export
pyarrow==16.0.0                   # Parquet support
ujson==5.9.0                      # Fast JSON serialization

# ── Hashing & Auditability ────────────────────────────────────
hashlib-compat==1.0.0             # SHA-256 dataset fingerprinting

# ── Environment & Config ──────────────────────────────────────
python-dotenv==1.0.1
pyyaml==6.0.1

# ── Testing ───────────────────────────────────────────────────
pytest==8.2.0
pytest-cov==5.0.0
