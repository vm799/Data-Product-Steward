import streamlit as st


def initialize_state():
    """Initialize the unified product session state."""
    if "product" not in st.session_state:
        st.session_state.product = {
            # Business Context
            "name": "",
            "domain": "",
            "objective": "",
            "regulatory_scope": [],
            "geo_scope": "",
            "consumers": "",
            # Data Sources
            "sources": [],
            # Data Model
            "entities": [],
            # Governance & Security
            "classification": "",
            "pii": False,
            "retention_policy": "",
            "compliance_frameworks": [],
            "access_roles": "",
            "lineage_notes": "",
            # Data Quality
            "quality_rules": {},
            # Transformations
            "transformations": [],
        }
    if "steps_completed" not in st.session_state:
        st.session_state.steps_completed = set()
    if "theme" not in st.session_state:
        st.session_state.theme = "terminal"


def mark_step_complete(step_key):
    """Mark a wizard step as completed."""
    st.session_state.steps_completed.add(step_key)


def get_progress(product):
    """Compute wizard progress from actual product state."""
    completed = st.session_state.get("steps_completed", set())

    steps = {
        "Business Context": bool(
            product.get("name") and product.get("domain") and product.get("objective")
        ),
        "Data Sources": len(product.get("sources", [])) > 0,
        "Data Model": any(
            len(e.get("attributes", [])) > 0 for e in product.get("entities", [])
        ),
        "Governance & Security": "governance" in completed,
        "Data Quality": "quality" in completed,
        "Transformations": len(product.get("transformations", [])) > 0,
    }

    all_prior = all(steps.values())
    steps["Review & Export"] = all_prior and "review" in completed

    done = sum(1 for v in steps.values() if v)
    total = len(steps)
    pct = int(done / total * 100) if total > 0 else 0

    return {"steps": steps, "done": done, "total": total, "pct": pct}


def get_next_step(product):
    """Return 1-indexed number of the first incomplete step, or None if all done."""
    progress = get_progress(product)
    for i, done in enumerate(progress["steps"].values()):
        if not done:
            return i + 1
    return None
