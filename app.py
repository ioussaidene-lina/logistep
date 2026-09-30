import streamlit as st
import pandas as pd
from core.models import GrafcetSystem
from ui.data_input import render_input_tables
from ui.visualizer import render_graph
from ui.export_view import render_export_section

# 1. CRITIQUE : set_page_config DOIT être la première instruction Streamlit
st.set_page_config(page_title="LogiStep - GRAFCET Compiler", layout="wide", page_icon="⚙️")

# 2. Injection CSS 
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

st.title("⚙️ LogiStep : Industrial GRAFCET Compiler")
st.markdown("Mathematical system transformation to Siemens AWL/STL")

# 3. Création de la structure asymétrique (Le faux "Glider")
# La colonne de gauche prend 30% de l'écran, celle de droite 70%
col_gauche, col_droite = st.columns([0.3, 0.7])

with col_gauche:
    # 4. Récupération des données UI dans la zone restreinte
    steps_df, trans_df = render_input_tables()

# 5. Construction du modèle mathématique
system = GrafcetSystem()

for _, row in steps_df.iterrows():
    if pd.notna(row['step_id']):
        system.add_step(str(row['step_id']), bool(row['is_initial']), str(row['action']) if pd.notna(row['action']) else "")

for _, row in trans_df.iterrows():
    if pd.notna(row['transition_id']):
        system.add_transition(str(row['transition_id']), str(row['from_step']), str(row['to_step']), str(row['condition']))

# 6. Affichage structuré du Graphe et du Code
with col_droite:
    # On divise la partie droite (70%) en deux colonnes égales pour le visuel
    col_visuel, col_code = st.columns(2)
    
    with col_visuel:
        render_graph(system)
        
    with col_code:
        render_export_section(system)