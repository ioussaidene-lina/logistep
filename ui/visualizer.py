import streamlit as st
import graphviz

def render_graph(system):
    st.subheader("System Graph (GRAFCET)")
    
    dot = graphviz.Digraph(engine='dot')
    dot.attr(rankdir='TB', size='8,5')
    
    for step in system.steps:
        shape = 'doubleoctagon' if step.is_initial else 'box'
        dot.node(step.step_id, f"{step.step_id}\n[{step.action}]", shape=shape)
        
    for t in system.transitions:
        t_node = f"trans_{t.transition_id}"
        dot.node(t_node, t.condition, shape='plaintext', fontcolor='blue')
        dot.edge(t.from_step, t_node, arrowhead='none')
        dot.edge(t_node, t.to_step)
        
    st.graphviz_chart(dot)