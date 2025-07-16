# 🧠 Task_04_Descriptive_Stats

A cross-strategy data summarization toolkit built to explore and describe real-world datasets — with and without third-party libraries — as part of an applied research challenge on 2024 U.S. presidential election social media data.

---

## 📌 Project Overview

This project delivers a flexible and extensible framework for descriptive statistics. It was designed to support researchers in quickly generating insights from datasets that may include nested JSON structures, inconsistent formatting, or categorical and numeric diversity.

To ensure full transparency and reproducibility, the system was developed in **three separate flavors**:

1. **Pure Python** (no third-party libraries)  
2. **Pandas-based** implementation  
3. **Polars-based** implementation

Each version is capable of:
- Unpacking nested JSON-like fields
- Computing count, mean, min, max, standard deviation (for numeric fields)
- Identifying unique values and the most frequent value (for non-numeric fields)
- Optionally performing aggregation/grouping

---

## 🚀 How to Run

### Requirements

- Python 3.10+
- For `pandas_stats.py`:
  ```bash
  pip install pandas
For polars_stats.py:

bash
Copy
Edit
pip install polars
(Optional for visualization)matplotlib, seaborn, or plotly

Running Each Script
⚠️ IMPORTANT: DO NOT upload or include any dataset in the repository!

Each script prompts the user to select a .csv file from their system. No file path hardcoding is necessary.

bash
Copy
Edit
# Pure Python
python pure_python_stats.py

# Pandas
python pandas_stats.py

# Polars
python polars_stats.py
📊 What Each Script Does
Dynamically detects improperly formatted or nested columns

Unpacks JSON strings into analyzable columns

Performs summary statistics for:

Numeric fields: count, mean, min, max, std

Non-numeric: count, unique, most frequent

Offers grouping options by 1 or 2 columns

Cleanly displays side-by-side tabular results

📁 Folder Structure
.
├── pure_python_stats.py
├── pandas_stats.py
├── polars_stats.py
├── README.md
└── (No datasets included)
🔍 Key Insights & Learnings
Polars showed significant performance gains with large datasets and JSON unpacking, especially when schema inference was optimized.

Pandas was the easiest to use and most familiar, making it perfect for quick iteration.

Pure Python reinforces core concepts of iteration, parsing, and aggregation, making it ideal for learning, although less efficient for scaling.

ChatGPT-style LLMs were very helpful in prototyping template logic, but human judgment was crucial for:

Handling edge cases in nested structures

Designing clean CLI prompts

Ensuring script flexibility across multiple datasets
