import streamlit as st
import pandas as pd
from smart_scheduler_ai import run_scheduler, plot_gantt_chart
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Scheduler", layout="wide")

st.title("🛠️ Smart Scheduling System for Small Machine Shops")

st.markdown("This app uses job and machine data to generate an optimized production schedule.")

# File upload or default
st.sidebar.header("📂 Upload Input Files")

jobs_file = st.sidebar.file_uploader("Upload Jobs CSV", type="csv")
machines_file = st.sidebar.file_uploader("Upload Machines CSV", type="csv")

# Load default or uploaded
if jobs_file is not None and machines_file is not None:
    jobs_df = pd.read_csv(jobs_file)
    machines_df = pd.read_csv(machines_file)
    st.success("✅ Uploaded custom input files.")
else:
    jobs_df = pd.read_csv("jobs.csv")
    machines_df = pd.read_csv("machines.csv")
    st.info("ℹ️ Using default files from project.")

# Display inputs
st.subheader("📋 Jobs Data")
st.dataframe(jobs_df)

st.subheader("⚙️ Machines Data")
st.dataframe(machines_df)

# Run Scheduler
st.subheader("📅 Generated Schedule")
try:
    schedule_df = run_scheduler(jobs_df, machines_df)
    st.dataframe(schedule_df)

    # Save for export
    schedule_df.to_csv("final_schedule_ai.csv", index=False)

    # Plot chart
    st.subheader("📊 Gantt Chart")
    chart = plot_gantt_chart(schedule_df)
    st.pyplot(chart)
except Exception as e:
    st.error("❌ Failed to generate schedule.")
    st.exception(e)
