import streamlit as st
from state_manager import initialize_state
from components.glossary_panel import render_glossary
from components.progress_tracker import render_progress
from components.canvas_preview import render_canvas

st.set_page_config(
    page_title="Data Product Builder",
    layout="wide",
)

initialize_state()

st.title("🚀 Data Product Builder")
st.caption("Governed. Structured. Production-Ready.")

left, center, right = st.columns([1, 2, 1])

with left:
    render_glossary()

with right:
    render_progress()
    render_canvas()
