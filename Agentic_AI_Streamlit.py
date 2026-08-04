# Generated from: Agentic_AI_Streamlit.ipynb
# Converted at: 2026-07-11T11:05:32.773Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

# Cell 1 - Imports and Setup
import streamlit as st
import anthropic
import pandas as pd
import plotly.express as px
import re, sys, io, ast

st.set_page_config(page_title="AI Data Analyst Agent", page_icon="🤖", layout="wide")
st.title("🤖 AI Data Analyst Agent")
st.caption("Upload any CSV and ask me anything!")

# Cell 2 - Connect Claude and Define Functions
client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

def extract_code(text):
    matches = re.findall(r'```python(.*?)```', text, re.DOTALL)
    return matches[0].strip() if matches else None

def execute_code(code, df):
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        local_vars = {"df": df, "pd": pd}
        exec(code, local_vars)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        if not output and 'result' in local_vars:
            output = str(local_vars['result'])
        return output.strip(), True
    except Exception as e:
        sys.stdout = old_stdout
        return f"Error: {str(e)}", False

# Cell 3 - File Upload and Schema
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Auto clean messy columns
    for col in df.columns:
        if df[col].dtype == object:
            cleaned = df[col].str.extract(r'(\d+\.?\d*)')
            if cleaned.notna().sum()[0] > len(df) * 0.5:
                try:
                    df[col] = cleaned.astype(float)
                except:
                    pass
    
    st.success(f"✅ Loaded: {df.shape[0]} rows x {df.shape[1]} columns")
    st.dataframe(df.head(3))

    schema = f"""
Dataset has {df.shape[0]} rows and {df.shape[1]} columns.
Column names and data types:
{df.dtypes.to_string()}
Missing values in each column:
{df.isnull().sum().to_string()}
Sample data (3 rows):
{df.head(3).to_string()}
Basic statistics:
{df.describe().to_string()}
"""

# cell 4 (Ask a Question)
if uploaded_file:
    st.subheader("💬 Ask Anything About Your Data")
    question = st.text_input("Type your question here:")

    if st.button("Get Answer"):
        with st.spinner(""):
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=300,
                messages=[{"role": "user", "content": f"""Dataset:
{schema}

Question: {question}

YOU MUST respond in this exact format only:
```python
# code here
print(result)
```
Use df as dataframe.
Check data types before calculating.
Clean messy columns if needed."""}]
            )
            code = extract_code(response.content[0].text)
            if code:
                output, success = execute_code(code, df)
                if not success:
                    fix = client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=300,
                        messages=[
                            {"role": "user", "content": f"Dataset:\n{schema}\n\nQuestion: {question}"},
                            {"role": "assistant", "content": response.content[0].text},
                            {"role": "user", "content": f"Error: {output}\nFix it. Return ONLY code in ```python ``` blocks."}
                        ]
                    )
                    code = extract_code(fix.content[0].text)
                    if code:
                        output, success = execute_code(code, df)
            st.write(output if success else "Please try again.")

# Cell 5 ( Ask For a Chart )
if uploaded_file:
    st.subheader("📊 Ask for a Chart")
    chart_question = st.text_input("What chart do you want?")

    if st.button("Generate Chart"):
        with st.spinner(""):

            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=500,
                messages=[{"role": "user", "content": f"""Dataset:
{schema}

Question: {chart_question}

YOU MUST respond in this exact format only:
```python
# code here
fig = px.something(...)
```
Use df as dataframe.
Use plotly.express as px.
Do NOT include fig.show().
Clean messy columns if needed."""}]
            )

            code = extract_code(response.content[0].text)

            if code:
                try:
                    local_vars = {"df": df, "pd": pd, "px": px}
                    exec(code, local_vars)
                    fig = local_vars.get('fig')
                    if fig:
                        st.plotly_chart(fig)
                except:
                    fix = client.messages.create(
                        model="claude-sonnet-4-6",
                        max_tokens=500,
                        messages=[
                            {"role": "user", "content": f"Dataset:\n{schema}\n\nQuestion: {chart_question}"},
                            {"role": "assistant", "content": response.content[0].text},
                            {"role": "user", "content": f"Fix the error. Return ONLY code in ```python ``` blocks."}
                        ]
                    )
                    code = extract_code(fix.content[0].text)
                    if code:
                        try:
                            local_vars = {"df": df, "pd": pd, "px": px}
                            exec(code, local_vars)
                            fig = local_vars.get('fig')
                            if fig:
                                st.plotly_chart(fig)
                        except:
                            st.write("Please try again.")

# Cell - 6 ( Auto Insight Generator )
if uploaded_file:
    st.subheader("🤖 Auto Insight Report")

    if st.button("Generate Report"):
        with st.spinner(""):

            # Step 1 - Claude decides 2 questions
            decision = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=200,
                messages=[{"role": "user", "content": f"""Dataset:
{schema}

Decide 2 most important questions to analyse.
Return ONLY this, nothing else:
analyses = ["question1", "question2"]"""}]
            )

            # Step 2 - Parse safely
            try:
                text = decision.content[0].text.strip()
                list_start = text.index('[')
                list_end = text.index(']') + 1
                analyses = ast.literal_eval(text[list_start:list_end])
            except:
                analyses = [
                    "What are the key statistics?",
                    "What are the top values in main column?"
                ]

            # Step 3 - Run each analysis
            for i, question in enumerate(analyses):
                st.write(f"📊 Analysis {i+1}: {question}")

                res = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=500,
                    messages=[{"role": "user", "content": f"""Dataset:
{schema}

Question: {question}

YOU MUST respond in this exact format only:
```python
# code here
result = df.something()
print(result.to_string())
```
Use df as dataframe.
Keep output short and simple.
Max 5 lines of output.
Clean messy columns if needed."""}]
                )

                code = extract_code(res.content[0].text)

                if code:
                    output, success = execute_code(code, df)

                    if not success:
                        fix = client.messages.create(
                            model="claude-sonnet-4-6",
                            max_tokens=500,
                            messages=[
                                {"role": "user", "content": f"Dataset:\n{schema}\n\nQuestion: {question}"},
                                {"role": "assistant", "content": res.content[0].text},
                                {"role": "user", "content": f"Error: {output}\nFix it. Return ONLY code in ```python ``` blocks."}
                            ]
                        )
                        code = extract_code(fix.content[0].text)
                        if code:
                            output, success = execute_code(code, df)
                            if success:
                                st.code(output)
                    else:
                        st.code(output)

            st.success("✅ Report Complete!")