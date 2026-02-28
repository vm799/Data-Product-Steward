import streamlit as st

def initialize_state():
    if "product" not in st.session_state:
        st.session_state.product = {
            "name": "",
            "domain": "",
            "objective": "",
            "regulatory_scope": [],
            "sources": [],
            "entities": [],
            "classification": "",
            "pii": False,
            "retention_policy": "",
            "quality_threshold": 95,
            "transformations": "",
            "access_model": "",
        }
