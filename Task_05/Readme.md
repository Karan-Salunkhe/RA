# Task 05: Descriptive Statistics and Large Language Models

## 📖 Project Overview

This research project explores how well large language models (LLMs) like ChatGPT and DeepSeek Chat can interpret and answer natural language questions about structured sports data. The main objective is to evaluate whether LLMs can accurately generate descriptive statistics and insights comparable to script-based validations.

## 🔢 Dataset Used

For this project, I selected the IPL 2025 dataset, which contains detailed performance data on batters and bowlers. It includes fields such as:

**Batters**: Runs, Strike Rate, Matches, Average, High Score, Balls Faced  
**Bowlers**: Wickets, Overs, Strike Rate, Economy, Bowling Average  

This dataset was chosen due to its clear structure and balanced representation of both batting and bowling performance across a complete season.

## 👷 Methodology

### Step 1: Data Preparation
- The dataset was manually reviewed for consistency and cleaned where necessary
- Non-numeric fields were verified, and missing/malformed entries were corrected or excluded

### Step 2: Script-Based Validation (Baseline)
Used a custom Pandas-based statistics script to:
- Flatten and unpack nested columns
- Calculate summary statistics (mean, count, min, max, standard deviation)
- Group and aggregate data (e.g., by team or player)

### Step 3: LLM Querying
Formulated natural language questions and submitted them to both ChatGPT and DeepSeek Chat:

**Example Questions**:
1. "Which batter had the highest strike rate among players who scored over 500 runs?"
2. "Who bowled the most overs in the season?"
3. "Which young bowler showed the highest potential based on strike rate and wickets?"
4. "Who would you build a playoff team around?"

**Prompt Template**:  
"Analyze the IPL 2025 dataset and answer this question precisely [specific question]"

### Step 4: Comparison and Analysis
Created three-way comparisons between:
1. ChatGPT responses
2. DeepSeek Chat responses
3. Script validation outputs

Key comparison metrics:
- Numeric accuracy (vs script)
- Contextual interpretation quality
- Handling of ambiguous queries

## 📊 Findings & Observations

### ✅ What Worked Well
- Both LLMs handled well-structured questions with high accuracy (>90% match to script)
- DeepSeek Chat showed slightly better numeric precision (exact decimal matching)
- ChatGPT provided more verbose contextual explanations
- Summary-style answers matched script outputs in most cases

### ⚠ Challenges
| Issue | ChatGPT | DeepSeek Chat |
|-------|---------|---------------|
| Numeric rounding | Occasionally rounded decimals | Matched script exactly |
| Assumption-making | More prone to inference | More conservative |
| Ambiguous queries | Varied by phrasing | Consistent but literal |

### 💡 Key Insights
- Adding "answer precisely from the dataset" improved both models' accuracy
- DeepSeek Chat performed better on direct statistical questions
- ChatGPT excelled at comparative analysis ("Player X vs Player Y")
- Both struggled equally with truly subjective questions ("most promising talent")

## 📂 Repository Structure
