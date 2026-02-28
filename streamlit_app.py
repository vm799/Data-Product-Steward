import streamlit as st
from state_manager import initialize_state, get_progress
from components.layout import inject_custom_css
from components.sidebar import render_sidebar
from components.canvas import render_canvas

st.set_page_config(
    page_title="Data Product Builder",
    page_icon="📊",
    layout="wide",
)

initialize_state()
inject_custom_css()
render_sidebar()

product = st.session_state.product
progress = get_progress(product)

# ═══════════════════════════════════════════════════════════════════════
# HEADER — title, subtitle, helpers ribbon — no wasted vertical space
# ═══════════════════════════════════════════════════════════════════════
st.markdown("# 📊 Data Product Builder")
st.caption(
    "Define, govern, and ship a production-ready data product for asset management — "
    "this tool generates Snowflake DDL, dbt models, masking policies, and Collibra metadata."
)

# Helpers ribbon — show what tools are available
st.markdown(
    '<div class="helpers-ribbon">'
    '<span class="helper-tag">📊 Progress Tracker — sidebar</span>'
    '<span class="helper-tag">💡 Step-by-Step Tips — sidebar</span>'
    '<span class="helper-tag">📖 Glossary of Terms — sidebar</span>'
    '<span class="helper-tag">📋 Live Canvas — right panel</span>'
    "</div>",
    unsafe_allow_html=True,
)

# ═══════════════════════════════════════════════════════════════════════
# RETURNING USER — progress bar + next step
# ═══════════════════════════════════════════════════════════════════════
if product.get("name"):
    rc1, rc2, rc3, rc4 = st.columns(4)
    rc1.metric("Building", product["name"])
    rc2.metric("Progress", f"{progress['pct']}%")
    rc3.metric("Entities", len(product.get("entities", [])))
    rc4.metric("Sources", len(product.get("sources", [])))

    pending = [name for name, done in progress["steps"].items() if not done]
    if pending:
        st.info(
            f"Welcome back — next step: **{pending[0]}**. "
            f"Select it from the sidebar to continue."
        )
    else:
        st.success(
            "All steps complete. Head to **Review & Export** to download your artifacts."
        )

# ═══════════════════════════════════════════════════════════════════════
# MAIN + CANVAS SPLIT
# ═══════════════════════════════════════════════════════════════════════
main_col, canvas_col = st.columns([5, 3])

with main_col:
    # ── What is a Data Product? ─────────────────────────────────
    st.markdown(
        "In asset management, a **Data Product** is a governed dataset built "
        "for a specific business purpose — investor positions, risk exposures, "
        "regulatory reporting. This builder walks you through every decision to "
        "take one from idea to production, even if you've never done it before."
    )

    # ── Screen layout — single row, not 3 matching cards ────────
    st.markdown(
        '<div class="zone-row">'
        '<div class="zone-cell zone-nav">'
        '<div class="zone-cell-label">Left</div>'
        '<div class="zone-cell-title">Sidebar</div>'
        "Progress, tips, glossary. Navigate between steps here."
        "</div>"
        '<div class="zone-cell zone-wiz">'
        '<div class="zone-cell-label">Center</div>'
        '<div class="zone-cell-title">Wizard</div>'
        "Fill in the form for each step. Save and move forward."
        "</div>"
        '<div class="zone-cell zone-cvs">'
        '<div class="zone-cell-label">Right</div>'
        '<div class="zone-cell-title">Live Canvas</div>'
        "Your data product blueprint — updates as you build."
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    # ── 7 Steps — clean list, not bulky cards ───────────────────
    st.markdown("### The 7 steps")

    steps_info = [
        ("Business Context", "Name it, pick a domain, set geography — regulations auto-detect"),
        ("Data Sources", "Register upstream systems with owners, SLAs, and criticality"),
        ("Data Model", "Design tables and columns — tag PII to auto-generate masking"),
        ("Governance", "Classify sensitivity, set retention, assign access roles"),
        ("Data Quality", "Set completeness/accuracy thresholds — become pipeline checks"),
        ("Transformations", "Document processing steps — generates runnable dbt models"),
        ("Review & Export", "Validate, fix errors, download all production artifacts"),
    ]

    items_html = ""
    for i, (name, desc) in enumerate(steps_info, 1):
        done = list(progress["steps"].values())[i - 1]
        cls = "done" if done else ""
        icon = "✓" if done else str(i)
        items_html += (
            f'<div class="journey-item">'
            f'<span class="journey-num {cls}">{icon}</span>'
            f'<span class="journey-name">{name}</span>'
            f'<span class="journey-desc">{desc}</span>'
            f"</div>"
        )

    st.markdown(
        f'<div class="journey-list">{items_html}</div>',
        unsafe_allow_html=True,
    )

    # ── What you get ────────────────────────────────────────────
    st.markdown("### What gets generated")
    st.markdown(
        '<div class="deliv-row">'
        '<div class="deliv-item">'
        "<b>Snowflake</b>"
        "CREATE TABLE DDL, masking policies, secure views, GRANT statements"
        "</div>"
        '<div class="deliv-item">'
        "<b>dbt</b>"
        "schema.yml with tests, source definitions, transformation model SQL"
        "</div>"
        '<div class="deliv-item">'
        "<b>Governance</b>"
        "Collibra import JSON, full Markdown docs, version-controlled definition"
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    # ── CTA ─────────────────────────────────────────────────────
    st.markdown(
        '<div class="cta-line">'
        "Open the sidebar and select <b>Business Context</b> to start. "
        "The canvas on the right will build up as you go."
        "</div>",
        unsafe_allow_html=True,
    )

with canvas_col:
    render_canvas()
