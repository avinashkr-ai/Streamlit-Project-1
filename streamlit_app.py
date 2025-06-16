import streamlit as st
import json
import os
from datetime import datetime
import google.generativeai as genai

HISTORY_FILE = "history.json"

# Load or initialize history
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_to_history(entry):
    history = load_history()
    history.insert(0, entry)  # most recent first
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# Sidebar for API key
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

st.title("🇩🇪 German Job Finder using Gemini 2.0 Flash")

if not api_key:
    st.warning("Please enter your Gemini API key in the sidebar.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)

# Gemini model setup
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

# Get job listings from Gemini
if st.button("Fetch Jobs in Germany"):
    with st.spinner("Fetching jobs from Gemini 2.0 Flash..."):
        prompt = "List 10 currently open tech jobs in Germany in JSON format with fields: title, company, location, remote, link, salary (if available)."
        try:
            response = model.generate_content(prompt)
            content = response.text

            try:
                jobs_data = json.loads(content)
            except json.JSONDecodeError:
                # Attempt to extract JSON from markdown/code blocks
                import re
                match = re.search(r"```json\n(.*?)```", content, re.DOTALL)
                if match:
                    jobs_data = json.loads(match.group(1))
                else:
                    st.error("Failed to parse JSON from Gemini output.")
                    st.text(content)
                    st.stop()

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_to_history({"timestamp": timestamp, "jobs": jobs_data})
            st.success("Jobs successfully fetched and saved.")
            st.json(jobs_data)

        except Exception as e:
            st.error(f"Error: {e}")

# Show history
st.subheader("📜 Job JSON History")
history = load_history()
if not history:
    st.info("No history yet.")
else:
    for i, entry in enumerate(history):
        with st.expander(f"{entry['timestamp']}"):
            st.json(entry['jobs'])
