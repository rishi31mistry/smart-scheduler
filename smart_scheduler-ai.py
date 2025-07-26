import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch
import seaborn as sns

def run_scheduler(jobs_df, machines_df):
    # Preprocessing
    jobs_df['due_date'] = pd.to_datetime(jobs_df['due_date'])
    machines_df['available_at'] = pd.to_datetime(machines_df['available_at'])

    # Sort jobs by priority and due date
    jobs_df = jobs_df.sort_values(by=["priority", "due_date"])

    schedule = []

    # Scheduling Logic
    for _, job in jobs_df.iterrows():
        compatible = machines_df[machines_df['machine_type'] == job['required_machine_type']]
        
        if compatible.empty:
            continue
        
        idx = compatible['available_at'].idxmin()
        machine = machines_df.loc[idx]
        
        setup = timedelta(hours=job['setup_time'])
        start = machine['available_at'] + setup
        end = start + timedelta(hours=job['processing_time'])
        
        schedule.append({
            "job_id": job['job_id'],
            "job_type": job['job_type'],
            "machine_id": machine['machine_id'],
            "machine_type": machine['machine_type'],
            "start_time": start,
            "end_time": end,
            "due_date": job['due_date'],
            "delay_hours": max(0, (end - job['due_date']).total_seconds() / 3600)
        })
        
        machines_df.at[idx, 'available_at'] = end

    schedule_df = pd.DataFrame(schedule)
    return schedule_df

def plot_gantt_chart(schedule_df):
    plt.figure(figsize=(14, 7))
    sns.set(style="whitegrid")

    job_types = schedule_df['job_type'].unique()
    palette = sns.color_palette("tab10", len(job_types))
    color_map = dict(zip(job_types, palette))

    for _, row in schedule_df.iterrows():
        start = row['start_time']
        end = row['end_time']
        duration = (end - start).total_seconds() / 3600
        machine = row['machine_id']
        job_id = row['job_id']
        job_type = row['job_type']
        
        plt.barh(
            y=machine,
            width=duration,
            left=start,
            height=0.4,
            color=color_map[job_type],
            edgecolor='black'
        )
        
        label = f"{job_id} ({job_type})\n{start.strftime('%H:%M')} - {end.strftime('%H:%M')}"
        plt.text(
            x=start + (end - start)/2,
            y=machine,
            s=label,
            ha='center',
            va='center',
            fontsize=8,
            color='white',
            fontweight='bold'
        )

    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d\n%I:%M %p'))
    plt.xticks(rotation=45, ha='right', fontsize=8)

    legend_patches = [Patch(color=color_map[jt], label=jt) for jt in job_types]
    plt.legend(handles=legend_patches, title="Job Types", loc="upper left", bbox_to_anchor=(1, 1))

    plt.title("🔧 Detailed Machine Scheduling Gantt Chart", fontsize=14)
    plt.xlabel("Time")
    plt.ylabel("Machine ID")
    plt.grid(True, axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    return plt
