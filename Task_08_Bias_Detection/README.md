# 🧠 Task 08 — Bias Detection in LLM Data Narratives

### 📘 Overview
This task investigates whether **Large Language Models (LLMs)** show systematic bias when analyzing identical datasets under different prompt framings.  
It extends prior Syracuse OPT Research work (Tasks 4–7) on the IPL 2025 Cricket Dataset.

### 🎯 Objective
To design a controlled experiment that detects framing, demographic, and confirmation biases in LLM-generated data narratives while maintaining full reproducibility and ethical transparency.

---

### ✅ Work Completed (Weeks 1–2)
| Stage | Description | Key Outputs |
|--------|--------------|-------------|
| **Data Preparation** | Anonymized IPL 2025 statistics and computed validated metrics (runs, strike rate, wickets, overs). | `analysis/ground_truth.csv` |
| **Prompt Design** | Built five framing conditions — neutral, positive, negative, demographic, confirmation — to test hypotheses H0–H3. | `prompts/prompt_variations.csv` |
| **LLM Data Collection** | Queried Gemini, ChatGPT, and Claude using each prompt; stored responses locally. | `results/raw/*.txt` *(git-ignored)* |
| **Validation Setup** | Consolidated outputs and cross-checked each response against numeric ground truth. | `analysis/claims_validation.csv` |
| **Documentation** | Created reproducible Python scripts, .gitignore, and RMarkdown report. | `scripts/*.py`, `README.Rmd` |

---

### 🧪 Repository Structure
Task_08_Bias_Detection/
├── analysis/ # ground truth + validation results
├── prompts/ # all generated prompt variations
├── results/ # structured outputs (raw folder git-ignored)
├── scripts/ # Python scripts for each workflow stage
├── docs/ # hypotheses and planning notes
└── README.Rmd # full reproducible report

yaml
Copy code

---

### 🧩 Current Focus (Weeks 3–4)
- Quantify bias patterns using sentiment and keyword analysis.  
- Compare LLM behavior across models (Gemini vs ChatGPT vs Claude).  
- Draft `REPORT.md` with visuals, findings, and mitigation strategies.  
- Submit final report and Qualtrics check-ins by **Nov 15 2025**.

---

### ⚙️ Tools & Environment
- **Python 3.12**, `pandas`, `pathlib`, `json`, `csv`  
- **R Markdown** for documentation & analysis  
- **LLMs:** ChatGPT, Claude, Gemini  
- **Git + GitHub** for version control  

---

### 🔒 Ethics & Compliance
All data are synthetic and anonymized.  
No PII is stored or published.  
Raw LLM outputs remain local (`results/raw/` excluded via `.gitignore`).

---

**Author:** [Karan C. Salunkhe](https://www.linkedin.com/in/karan-c-salunkhe/)  
**Faculty Advisor:** Jon Strome — [jrstrome@syr.edu](mailto:jrstrome@syr.edu)
