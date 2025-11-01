```markdown
# Hypotheses (Pre-Registered)

This document records the hypotheses and design choices **before** running experiments.  
Each hypothesis is tested with **minimally different prompts** against the **same stats block**.

## Dataset & Scope
- Source: Anonymized IPL 2025 performance summaries (batting & bowling).
- Identifiers: Players labeled as *Player A, Player B, Player C,* etc.
- Ground Truth: Computed via Python/Pandas and saved in `analysis/ground_truth.csv`.

## Controlled Variables
- Constant stats block (same ordering, same players, same metrics).
- Same token budget and similar prompt length across conditions.
- Same models (≥2), same sampling plan (≥3 runs per model × prompt).
- No PII; anonymized identifiers only.

## Independent Variables (Conditions)
- **Framing:** positive vs negative wording (e.g., “growth potential” vs “underperforming”).
- **Demographics:** adds anonymized seniority labels (e.g., *Player A: senior*) vs no demographics.
- **Confirmation prime:** prompt includes a leading hypothesis vs neutral wording.

## Hypotheses
- **H1 (Framing):** Prompts using “underperforming” vs “developing” will produce **different coaching recommendations** for the same players.
- **H2 (Demographics):** Mentioning age/seniority will **shift which players are recommended** for coaching compared to neutral prompts.
- **H3 (Confirmation):** If the prompt primes a hypothesis (e.g., “Player A likely best”), models will **agree more often** than neutral prompts.
- **H4 (Selection Bias):** Prompt wording changes **which statistics** the model cites (e.g., cherry-picking SR vs runs).
- **H5 (Tone):** Positive vs negative framing leads to **systematically different sentiment** in the narrative.

## Prompt Sets (Minimally Different)
- `neutral` – asks for a coaching recommendation grounded in data.
- `positive` – asks who shows the most potential for improvement.
- `negative` – asks whose poor performance needs correction.
- `demographic` – repeats neutral, plus anonymized seniority labels.

All prompts reference the **exact same** stats block.

## Sampling Plan
- **Models:** ≥2 (e.g., GPT-4 and Claude).  
- **Replicates:** ≥3 runs per model × prompt condition (fresh chat each time).  
- **Logging:** `results/llm_outputs_structured.csv` with:  
  `prompt_id, hypothesis, condition, model, model_version, temperature, timestamp, prompt_text, response_text`.

## Ground Truth & Validation
- Numeric baselines (e.g., highest SR >500 runs, most overs, wickets+SR) saved in `analysis/ground_truth.csv`.
- Later (Week 3), responses will be checked for factual alignment and fabrication rates.

```