# 🤖 AI Data Analyst Agent

An AI-powered data analyst that analyses CSV datasets using natural-language instructions. It generates Python code, executes the analysis, attempts to correct execution errors, creates interactive charts, and produces automated insight reports.

Built using Claude AI, Python, Streamlit, Pandas, and Plotly.

---

## What We Built

This project is an agentic AI data analysis application powered by Claude AI from Anthropic.

Unlike a traditional chatbot that only explains how to analyse data, this application generates and executes Python code to perform the requested analysis.

- Upload a CSV dataset.
- Ask questions in plain English.
- Automatically generate Python code.
- Execute the generated code on the uploaded dataset.
- Attempt automatic error correction when execution fails.
- Display analytical results and insights.

---

## What Makes It Agentic

A regular chatbot tells you what to do. This agent attempts to perform the analysis for you.

**Example question:**

"What is the survival rate by gender?"

**Agent workflow:**

1. Reads the dataset schema automatically.
2. Identifies relevant columns and data types.
3. Determines the appropriate analysis.
4. Generates Python code using Claude AI.
5. Executes the code on the full dataset.
6. Attempts to fix errors and retry execution.
7. Displays the analytical result.

The user does not need to write Python code manually.

---

## Tech Stack

- **Python** – Core programming language
- **Claude API** – AI-powered code generation and analysis
- **Anthropic SDK** – Claude API integration
- **Streamlit** – Web application interface
- **Pandas** – Data loading and manipulation
- **Plotly** – Interactive chart generation

---

## How It Works

User uploads CSV  
↓  
Dataset schema is generated automatically  
↓  
Columns, data types, missing values and statistics are identified  
↓  
User asks a question in plain English  
↓  
Dataset context and question are sent to Claude AI  
↓  
Claude generates Python code  
↓  
Generated code is extracted and executed on the dataset  
↓  
If execution fails, the error is sent back to Claude  
↓  
Claude attempts to generate corrected code  
↓  
Result is displayed to the user

---

## What We Achieved

- Natural-language data analysis
- Automatic Python code generation
- Interactive chart generation
- Automated insight reports
- Error detection and retry mechanism
- Basic handling of missing values and data-type issues
- Analysis of numerical and categorical datasets
- Deployment as a Streamlit web application

---

## Datasets Tested

The application was tested using six datasets with different sizes, structures, and data characteristics.

| Dataset | Rows | Columns | Data characteristics |
|---|---:|---:|---|
| Iris | 150 | 5 | Numerical and categorical |
| Titanic | 891 | 12 | Mixed numerical and categorical |
| Tips | 244 | 7 | Numerical and categorical |
| Boston Housing | 506 | 14 | Numerical |
| Diamonds | 53,940 | 10 | Large mixed dataset |
| Messy Customers | 25 | 8 | Missing values, inconsistent text, numerical and data-quality issues |

---

## Observed Performance

Based on practical testing:

- **Basic analytical questions:** Performs very well.
- **Intermediate analytical questions:** Performs very well across the tested datasets.
- **Estimated accuracy:** Approximately 85–90% on tested basic and intermediate analytical questions. This is an informal estimate, not a formal benchmark.
- **Complex analytical questions:** Results can be inconsistent.
- **Large datasets:** Successfully tested with the Diamonds dataset containing 53,940 rows.
- **Messy datasets:** Handles some missing values and basic data-type issues, but does not resolve every data-quality problem.

Performance depends on the dataset, question complexity, data quality, and AI-generated code.

---

## How to Use

### Tab 1 – Ask a Question

Upload a CSV file, enter a question, and click **Get Answer**.

Example: "What is the average price by category?"

### Tab 2 – Ask for a Chart

Upload a CSV file, describe the chart you want, and click **Generate Chart**.

Example: "Show sales by region as a bar chart."

### Tab 3 – Auto Insight Report

Upload a CSV file and click **Generate Report**.

The agent selects two relevant analytical questions, generates Python code, executes the analyses, and displays the results.

---

## Limitations

- Complex analytical questions may produce inconsistent results.
- Very large datasets can increase processing time and API usage.
- Messy datasets may require manual preprocessing.
- The application does not guarantee that every AI-generated result is correct.
- Generated code is executed using Python `exec()` and is not protected by a secure sandbox. Additional isolation is required before using untrusted code or sensitive datasets in a public environment.
- Results depend on the quality of the AI-generated code and the available dataset context.

---

## What I Learned

- Building agentic AI applications using LLM APIs.
- Prompt engineering for Python code generation.
- Implementing code execution and error-retry workflows.
- Working with Pandas for data analysis.
- Generating interactive visualisations using Plotly.
- Developing applications with Streamlit.
- Handling numerical, categorical, and imperfect real-world datasets.
- Deploying AI applications using Streamlit Cloud.

---

**GitHub Repository:** https://github.com/gowsik710/ai-analyst-agent
