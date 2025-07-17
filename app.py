# app.py

import streamlit as st
import os
import sys
import json
import pandas as pd
from io import StringIO
from contextlib import redirect_stdout

# Add the src directory to the Python path to resolve module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from mission.mission_loader import load_mission_from_json
from mission.trajectory_simulator import TrajectorySimulator
from visualization.plotter import plot_results_plotly

# --- Helper Functions ---
def get_mission_details(mission_path):
    """Reads and returns the content of the mission JSON file."""
    with open(mission_path, 'r') as f:
        return json.load(f)

# --- Page Configuration ---
st.set_page_config(
    page_title="StellarLab Rocket Simulator",
    layout="wide"
)

# --- Sidebar ---
st.sidebar.title("StellarLab Controls")
st.sidebar.markdown("Configure and launch your rocket simulation.")

# --- Mission Selection ---
mission_dir = 'data/missions'
mission_files = [f for f in os.listdir(mission_dir) if f.endswith('.json')]
selected_mission = st.sidebar.selectbox(
    "Choose a Mission Profile",
    mission_files,
    index=0
)

# --- Main Page ---
st.title("StellarLab Propulsion Simulator")
st.markdown("---")

if selected_mission:
    mission_path = os.path.join(mission_dir, selected_mission)
    mission_details = get_mission_details(mission_path)
    
    # Display mission info
    st.header(f"Mission Preview: `{mission_details['name']}`")
    for i, stage in enumerate(mission_details['stages']):
        with st.expander(f"Stage {i+1}: {stage['stage_name']}"):
            col1, col2 = st.columns(2)
            col1.metric("Dry Mass (kg)", f"{stage['dry_mass']:,}")
            col1.metric("Fuel Mass (kg)", f"{stage['fuel_mass']:,}")
            col2.metric("Number of Engines", stage['num_engines'])
            col2.markdown(f"**Engine Config:** `{stage['engine_config']}`")
    
    st.markdown("---")

    if st.button("Launch Simulation", type="primary"):
        log_stream = StringIO()
        try:
            with st.spinner('Simulating trajectory... This may take a moment.'):
                with redirect_stdout(log_stream):
                    # Load mission and run simulation
                    stages = load_mission_from_json(mission_path)
                    simulator = TrajectorySimulator(stages)
                    results = simulator.simulate()
            
            st.success("Simulation Complete!")
            
            # --- Display Results ---
            st.header("Simulation Results")
            
            # Create columns for layout
            res_col1, res_col2 = st.columns([1, 2.5]) # Metrics and log on left, plot on right

            with res_col1:
                st.subheader("Key Metrics")
                max_alt = max(results['altitude'])
                max_vel = max(results['velocity'])
                total_time = results['time'][-1]
                st.metric("Max Altitude (km)", f"{max_alt:.2f}")
                st.metric("Max Velocity (m/s)", f"{max_vel:.2f}")
                st.metric("Total Mission Time (s)", f"{total_time:.2f}")
                
                # Data Export
                st.subheader("Export Data")
                df = pd.DataFrame(results)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name=f"{selected_mission.replace('.json', '')}_results.csv",
                    mime='text/csv',
                )

            with res_col2:
                # Display interactive plot
                fig = plot_results_plotly(results)
                st.plotly_chart(fig, use_container_width=True)

            # Display simulation log
            st.subheader("Simulation Log")
            st.text_area("Log Output", log_stream.getvalue(), height=250)


        except Exception as e:
            st.error(f"An error occurred during simulation: {e}")
            st.error(log_stream.getvalue())
