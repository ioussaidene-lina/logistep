import streamlit as st
import pandas as pd

def render_input_tables():
    st.sidebar.header("System Configuration")
    
    st.sidebar.subheader("1. Steps Definition")
    default_steps = pd.DataFrame([
        {"step_id": "S1", "is_initial": True, "action": "Motor_ON"},
        {"step_id": "S2", "is_initial": False, "action": "Valve_Open"},
        {"step_id": "S3", "is_initial": False, "action": "Idle"}
    ])
    steps_df = st.sidebar.data_editor(default_steps, num_rows="dynamic", key="steps_table")
    
    st.sidebar.subheader("2. Transitions Definition")
    default_transitions = pd.DataFrame([
        {"transition_id": "T1", "from_step": "S1", "to_step": "S2", "condition": "Start_Button"},
        {"transition_id": "T2", "from_step": "S2", "to_step": "S3", "condition": "Sensor_Level"},
        {"transition_id": "T3", "from_step": "S3", "to_step": "S1", "condition": "Timer_5s"}
    ])
    trans_df = st.sidebar.data_editor(default_transitions, num_rows="dynamic", key="trans_table")
    
    return steps_df, trans_df