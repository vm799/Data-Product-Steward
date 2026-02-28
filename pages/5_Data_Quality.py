import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
from state_manager import initialize_state, mark_step_complete
from components.layout import inject_custom_css, step_header
from components.sidebar import render_sidebar
from components.canvas import render_canvas
from components.helpers import render_step_nav, render_step_complete

initialize_state()
inject_custom_css()
render_sidebar(step=5)

step_header(
    5,
    "5️⃣ Data Quality",
    "Set quality thresholds that become automated checks in your data pipeline.",
)
render_step_nav(5)

product = st.session_state.product
qr = product.get("quality_rules", {})

# ── Two-panel layout ────────────────────────────────────────────────────
form_col, canvas_col = st.columns([7, 3])

with form_col:
    st.caption(
        "These thresholds define what 'good enough' means. "
        "If a metric drops below threshold, monitoring alerts fire. "
        "Adjust based on your source SLAs from Step 2."
    )

    with st.form("data_quality_form"):
        c1, c2 = st.columns(2)

        with c1:
            completeness = st.slider(
                "Completeness (%)",
                min_value=0,
                max_value=100,
                value=qr.get("completeness", 0),
                help="Percentage of non-null values expected. 95% is industry baseline.",
            )
            accuracy = st.slider(
                "Accuracy (%)",
                min_value=0,
                max_value=100,
                value=qr.get("accuracy", 0),
                help="Percentage of values that must match the source of truth.",
            )
            timeliness_hours = st.number_input(
                "Timeliness SLA (hours)",
                min_value=1,
                max_value=720,
                value=qr.get("timeliness_hours", 24),
                help="Maximum acceptable delay from source refresh to product availability.",
            )

        with c2:
            uniqueness = st.slider(
                "Uniqueness (%)",
                min_value=0,
                max_value=100,
                value=qr.get("uniqueness", 0),
                help="Percentage of records that must be unique (no duplicates). Primary keys should be 100%.",
            )
            custom_rules = st.text_area(
                "Custom Quality Rules",
                value=qr.get("custom_rules", ""),
                help="One rule per line. These become dbt tests. E.g.:\nINVESTOR_ID must not be null\nEMAIL must match regex pattern",
            )
            monitoring_channel = st.text_input(
                "Alerting Channel",
                value=qr.get("monitoring_channel", ""),
                help="Where alerts go when quality drops below threshold. E.g. #data-quality-alerts, ops@firm.com",
            )

        submitted = st.form_submit_button("Save Quality Rules")

        if submitted:
            product["quality_rules"] = {
                "completeness": completeness,
                "accuracy": accuracy,
                "timeliness_hours": timeliness_hours,
                "uniqueness": uniqueness,
                "custom_rules": custom_rules,
                "monitoring_channel": monitoring_channel,
            }
            mark_step_complete("quality")
            st.success("Data quality rules saved.")

    # ── Quality Profile ─────────────────────────────────────────────
    saved = product.get("quality_rules", {})
    if saved:
        st.divider()
        st.markdown("#### 📊 Current Quality Profile")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Completeness", f"{saved.get('completeness', 0)}%")
        m2.metric("Accuracy", f"{saved.get('accuracy', 0)}%")
        m3.metric("Timeliness", f"{saved.get('timeliness_hours', '—')}h")
        m4.metric("Uniqueness", f"{saved.get('uniqueness', 0)}%")

    # ── Step complete prompt ──────────────────────────────
    step_done = bool(product.get("quality_rules", {}).get("completeness"))
    render_step_complete(5, step_done)

with canvas_col:
    render_canvas()
