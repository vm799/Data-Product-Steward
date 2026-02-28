"""
Progress Tracker Component
Displays completion status across all wizard steps.
"""

import streamlit as st
from config import STEPS


def render_progress():
    """Render a progress overview for all wizard steps."""
    st.subheader("Progress")
    completed = st.session_state.get("step_completed", {})
    total = len(STEPS)
    done = sum(1 for v in completed.values() if v)
    st.progress(done / total if total > 0 else 0)
    st.caption(f"{done}/{total} steps completed")

    for step in STEPS:
        icon = "✅" if completed.get(step["key"], False) else "⬜"
        st.markdown(f"{icon} {step['label']}")
