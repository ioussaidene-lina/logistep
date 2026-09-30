import streamlit as st
from core.analyzer import SystemAnalyzer
from core.translator import AWLTranslator

def render_export_section(system):
    st.subheader("Compiled Industrial Code")
    
    # 1. Extraction mathématique
    analyzer = SystemAnalyzer(system)
    equations = analyzer.extract_boolean_equations()
    
    with st.expander("View Boolean Equations (AC / DC)"):
        st.json(equations)
        
    # 2. Traduction industrielle
    translator = AWLTranslator(system)
    awl_code = translator.generate_source_code()
    
    st.code(awl_code, language="pascal")
    
    # 3. Export
    st.download_button(
        label="📥 Download .awl Source File",
        data=awl_code,
        file_name="logistep_program.awl",
        mime="text/plain"
    )