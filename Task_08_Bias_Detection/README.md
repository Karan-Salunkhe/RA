# Task_08_Bias_Detection

Bias detection in LLM-generated data narratives using an anonymized sports dataset (IPL 2025).  
This project tests whether the **same data** produces **different narratives** when prompts are framed differently (e.g., positive vs negative wording, demographic mentions, hypothesis priming).

---

## Objectives
- Design a **controlled experiment** to detect framing, demographic, confirmation, and selection biases in LLM outputs.
- Use a **constant stats block** and **minimally different prompts** to isolate each bias.
- Collect responses from **multiple LLMs**, sample each prompt **3–5 times**, and **log** model, version, timestamp, prompt, and response.
- Validate claims against a **ground-truth** baseline computed from the dataset.
- Keep the repo **privacy-safe** (no PII, no source data committed).

---

## Ethics & Data Handling
- **No PII** or real names; use *Player A/B/C* only.
- **Do not commit datasets**. Source files live locally in `data/` (gitignored).
- Commit only derived artifacts that are safe (e.g., `analysis/ground_truth.csv`, charts, structured logs without sensitive content).

---

## Repository Structure

```bash
Task_08_Bias_Detection/
├─ scripts/
│ ├─ sanitize_players.py # anonymize names → data/*_anon.csv (local)
│ ├─ ground_truth.py # compute objective baselines → analysis/ground_truth.csv
│ ├─ experiment_design.py # build prompt_variations.csv from Jinja templates
│ ├─ run_experiment.py # consolidate raw responses → results/llm_outputs_structured.csv
│ ├─ analyze_bias.py # quick sentiment + simple pivots (Weeks 1–2 sanity checks)
│ └─ validate_claims.py # starter numeric checks vs ground truth
├─ prompts/
│ ├─ base_stats.txt
│ ├─ neutral.j2
│ ├─ positive.j2
│ ├─ negative.j2
│ ├─ demographic.j2
│ └─ prompt_variations.csv # generated
├─ results/
│ ├─ raw/ # raw LLM outputs (txt), not committed
│ └─ llm_outputs_structured.csv # consolidated, safe to commit
├─ analysis/
│ ├─ ground_truth.csv
│ ├─ sentiment_summary.csv
│ └─ charts/
├─ docs/
│ └─ hypotheses.md
├─ data/ # local only, not committed
├─ .env # API keys if used (not committed)
├─ .gitignore
├─ requirements.txt
├─ REPORT.md
└─ README.md
```

## How to Reproduce (Weeks 1–2)

> **Pre-req:** Python 3.10+, `pip`, and a virtual environment (recommended).

1. **Create & activate venv, install requirements**
   ```bash
   python -m venv .venv
   # Windows: .\.venv\Scripts\activate
   # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt

2. **Place source CSVs locally (not in git)**

Put ipl_batting.csv and ipl_bowling.csv in data/.

3. **Anonymize data (local only)**

```bash
python scripts/sanitize_players.py
```
```bash
```
4. **Compute ground truth baseline**

```bash
python scripts/ground_truth.py
```
5. **Generate prompt variations**
```bash
python scripts/experiment_design.py
```
Output: prompts/prompt_variations.csv

6. **Collect LLM responses**
    
Easiest path (manual UI): for each prompt condition, copy/paste into 2+ models (e.g., GPT-4, Claude), 3–5 runs each. Save texts under:

```bash
results/raw/gpt4_neutral_run1.txt
results/raw/gpt4_neutral_run2.txt
...
results/raw/claude_positive_run1.txt
``` 

Consolidate to structured CSV:
```bash
python scripts/run_experiment.py
```
Output: results/llm_outputs_structured.csv


