import streamlit as st
import pandas as pd
from core.models import GrafcetSystem
from ui.data_input import render_input_tables
from ui.visualizer import render_graph
from ui.export_view import render_export_section

# Injection CSS pour masquer le menu, le footer et le bouton de déploiement
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden; display: none;}
    .stDeployButton {display:none;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.set_page_config(page_title="LogiStep - GRAFCET Compiler", layout="wide", page_icon="⚙️")
st.title("⚙️ LogiStep : Industrial GRAFCET Compiler")
st.markdown("Mathematical system transformation to Siemens AWL/STL")

# 1. Récupération des données UI
steps_df, trans_df = render_input_tables()

# 2. Construction du modèle mathématique
system = GrafcetSystem()

for _, row in steps_df.iterrows():
    if pd.notna(row['step_id']):
        system.add_step(str(row['step_id']), bool(row['is_initial']), str(row['action']) if pd.notna(row['action']) else "")

for _, row in trans_df.iterrows():
    if pd.notna(row['transition_id']):
        system.add_transition(str(row['transition_id']), str(row['from_step']), str(row['to_step']), str(row['condition']))

# 3. Affichage structuré
col1, col2 = st.columns(2)

with col1:
    render_graph(system)

with col2:
    render_export_section(system)