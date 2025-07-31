Task 05: Descriptive Statistics and Large Language Models

📖 Project Overview

This research project explores how well large language models (LLMs) like ChatGPT can interpret and answer natural language questions about structured sports data. The main objective is to evaluate whether LLMs can accurately generate descriptive statistics and insights comparable to script-based validations.

🔢 Dataset Used

For this project, I selected the IPL 2025 dataset, which contains detailed performance data on batters and bowlers. It includes fields such as:

Batters: Runs, Strike Rate, Matches, Average, High Score, Balls Faced

Bowlers: Wickets, Overs, Strike Rate, Economy, Bowling Average

This dataset was chosen due to its clear structure and balanced representation of both batting and bowling performance across a complete season.

👷 Methodology

Step 1: Data Preparation

The dataset was manually reviewed for consistency and cleaned where necessary.

Non-numeric fields were verified, and missing or malformed entries were either corrected or excluded.

Step 2: Script-Based Validation (Baseline)

I used my existing custom Pandas-based statistics script from Task 4 to:

Flatten and unpack nested columns

Calculate summary statistics (mean, count, min, max, standard deviation)

Group and aggregate data (e.g., by team or player)

Step 3: Querying ChatGPT

I formulated a set of natural language questions related to player performance, team strategy, and comparative metrics. Examples include:

"Which batter had the highest strike rate among players who scored over 500 runs?"

"Who bowled the most overs in the season?"

"Which young bowler showed the highest potential based on strike rate and wickets?"

*"Who would you build a playoff team around?"

These questions were submitted to ChatGPT, and the model’s answers were saved.

Step 4: Comparison and Analysis

I compared ChatGPT's responses to the outputs of my Pandas script.

A comparison file was created (chatgpt_vs_script_comparison.csv) to show side-by-side results.

Any mismatches were noted and evaluated for possible causes (e.g., ambiguity, lack of context, or incorrect interpretation).

📊 Findings & Observations

✅ What Worked Well

ChatGPT handled well-structured, direct questions with high accuracy.

Summary-style answers (e.g., best player by stat) matched the script outputs in most cases.

ChatGPT could contextualize statistics when prompted properly (e.g., for trade suggestions).

⚠ What Was Challenging

ChatGPT occasionally made assumptions about data or inferred values from partial context.

For ambiguous queries (e.g., "most consistent under pressure"), results varied depending on how the question was framed.

Numeric precision varied slightly from Pandas calculations due to rounding or different default settings.

💡 Prompt Engineering Notes

Using "analyze the dataset and answer precisely" worked well to enforce factual responses.

Specific thresholds ("over 500 runs") and role definitions ("finisher") helped narrow down the correct logic.

Asking for rankings, summaries, or visual explanations improved the model’s interpretability.

📂 Repository Structure

Task_05_Descriptive_Stats/
├── prompts_and_responses.md         # All natural language questions + prompts used
├── chatgpt_vs_script_comparison.csv # Table comparing ChatGPT and script answers
├── README.md                        # This file

