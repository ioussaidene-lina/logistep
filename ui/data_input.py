import streamlit as st
import pandas as pd

def render_input_tables():
    st.header("System Configuration")
    
    st.subheader("1. Steps Definition")
    default_steps = pd.DataFrame([
        {"step_id": "S1", "is_initial": True, "action": "Motor_ON"},
        {"step_id": "S2", "is_initial": False, "action": "Valve_Open"},
        {"step_id": "S3", "is_initial": False, "action": "Idle"}
    ])
    # Ajout de use_container_width et height pour stabiliser l'UI
    steps_df = st.data_editor(
        default_steps, 
        num_rows="dynamic", 
        key="steps_table",
        use_container_width=True,
        height=250 
    )
    
    st.subheader("2. Transitions Definition")
    default_transitions = pd.DataFrame([
        {"transition_id": "T1", "from_step": "S1", "to_step": "S2", "condition": "Start_Button"},
        {"transition_id": "T2", "from_step": "S2", "to_step": "S3", "condition": "Sensor_Level"},
        {"transition_id": "T3", "from_step": "S3", "to_step": "S1", "condition": "Timer_5s"}
    ])
    # Ajout de use_container_width et height pour stabiliser l'UI
    trans_df = st.data_editor(
        default_transitions, 
        num_rows="dynamic", 
        key="trans_table",
        use_container_width=True,
        height=250
    )
    
    return steps_df, trans_df