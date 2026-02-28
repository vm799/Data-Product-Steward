import streamlit as st
from state_manager import initialize_state, get_progress
from components.layout import inject_custom_css, DATA_BOT_SVG
from components.sidebar import render_sidebar
from components.canvas import render_canvas

st.set_page_config(
    page_title="Data Product Builder",
    page_icon="📊",
    layout="wide",
)

initialize_state()
inject_custom_css()

# Onboarding step: 0=landing, 1=sidebar, 2=canvas, 3=dashboard
if "onboard" not in st.session_state:
    st.session_state.onboard = 0

product = st.session_state.product
progress = get_progress(product)

# Returning users skip straight to dashboard
if product.get("name") and st.session_state.onboard < 3:
    st.session_state.onboard = 3


# ═══════════════════════════════════════════════════════════════════════
# PAGE 0 — LANDING
# ═══════════════════════════════════════════════════════════════════════
def _landing():
    # No sidebar on landing — clean single focus
    st.markdown(
        '<div class="landing">'
        + DATA_BOT_SVG
        + "<h1>Data Product Builder</h1>"
        '<div class="landing-sub">'
        "Build production-ready, governed data products for asset management. "
        "Snowflake DDL, dbt models, masking policies, and Collibra metadata — "
        "all generated from a guided wizard."
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    # Spacer
    st.markdown("")

    _, btn_col, _ = st.columns([2, 1, 2])
    with btn_col:
        if st.button("Begin", use_container_width=True):
            st.session_state.onboard = 1
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════
# PAGE 1 — THE SIDEBAR EXPLAINED
# ═══════════════════════════════════════════════════════════════════════
def _sidebar_guide():
    st.markdown(
        '<div class="guide-page">'
        '<div class="guide-step-num">1 / 2</div>'
        "<h2>The Sidebar</h2>"
        "</div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 1])

    with left:
        st.markdown(
            '<div class="guide-panel">'
            '<div class="guide-panel-label">What it does</div>'
            "<p>The left sidebar is your <b>command center</b>. "
            "It stays visible on every page and gives you:</p>"
            "<ul>"
            "<li><b>Navigation</b> — click any step name to jump to it</li>"
            "<li><b>Progress tracker</b> — see which steps are done</li>"
            "<li><b>Tips</b> — context-specific guidance for each step</li>"
            "<li><b>Glossary</b> — look up unfamiliar terms instantly</li>"
            "</ul>"
            "</div>",
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            '<div class="guide-panel">'
            '<div class="guide-panel-label">How to use it</div>'
            "<p>The sidebar page list shows all 7 steps in order. "
            "Click any step to navigate there. Your progress is saved "
            "automatically.</p>"
            "<p>Click <b>> DASHBOARD_</b> at the top of the sidebar "
            "at any time to return to this overview and check your numbers.</p>"
            "<p>On desktop, you can <b>collapse the sidebar</b> by clicking "
            "the X at the top to get more screen space while working.</p>"
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("")

    _, back_col, _, fwd_col, _ = st.columns([1, 1, 1, 1, 1])
    with back_col:
        if st.button("Back", use_container_width=True):
            st.session_state.onboard = 0
            st.rerun()
    with fwd_col:
        if st.button("Next", use_container_width=True):
            st.session_state.onboard = 2
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════
# PAGE 2 — THE CANVAS EXPLAINED
# ═══════════════════════════════════════════════════════════════════════
def _canvas_guide():
    st.markdown(
        '<div class="guide-page">'
        '<div class="guide-step-num">2 / 2</div>'
        "<h2>The Live Canvas</h2>"
        "</div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 1])

    with left:
        st.markdown(
            '<div class="guide-panel">'
            '<div class="guide-panel-label">What it does</div>'
            "<p>The right panel is your <b>live blueprint</b>. "
            "As you fill in each wizard step, the canvas updates "
            "in real time showing:</p>"
            "<ul>"
            "<li><b>Product identity</b> — name, domain, geography</li>"
            "<li><b>Entities and sources</b> — tables, columns, PII tags</li>"
            "<li><b>Governance</b> — classification, retention, compliance</li>"
            "<li><b>Deliverables checklist</b> — which artifacts are ready</li>"
            "</ul>"
            "</div>",
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            '<div class="guide-panel">'
            '<div class="guide-panel-label">Why it matters</div>'
            "<p>The canvas shows you the <b>full picture</b> at all times — "
            "you never lose sight of what you're building.</p>"
            "<p>When a deliverable shows a check mark, it means you've "
            "provided enough data for the builder to generate that artifact "
            "automatically — DDL, masking policy, dbt model, etc.</p>"
            "<p>You can <b>download artifacts at any time</b> from the "
            "canvas, even before completing all steps.</p>"
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("")

    _, back_col, _, fwd_col, _ = st.columns([1, 1, 1, 1, 1])
    with back_col:
        if st.button("Back", use_container_width=True):
            st.session_state.onboard = 1
            st.rerun()
    with fwd_col:
        if st.button("Go to Dashboard", use_container_width=True):
            st.session_state.onboard = 3
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════
# PAGE 3 — DASHBOARD (the working view)
# ═══════════════════════════════════════════════════════════════════════
def _dashboard():
    render_sidebar()

    st.markdown("# Dashboard")
    st.caption(
        "Your data product at a glance. "
        "Select a step from the sidebar to start building."
    )

    # Metrics row
    if product.get("name"):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Product", product["name"])
        c2.metric("Progress", f"{progress['pct']}%")
        c3.metric("Entities", len(product.get("entities", [])))
        c4.metric("Sources", len(product.get("sources", [])))

        pending = [n for n, done in progress["steps"].items() if not done]
        if pending:
            st.info(f"Next step: **{pending[0]}** — select it from the sidebar.")
        else:
            st.success(
                "All steps complete. Head to **Review & Export** to download artifacts."
            )

    main_col, canvas_col = st.columns([5, 3])

    with main_col:
        st.markdown('<div class="wizard-panel">', unsafe_allow_html=True)

        st.markdown(
            "A **Data Product** in asset management is a governed dataset built "
            "for a specific business purpose — investor positions, risk exposures, "
            "regulatory reporting."
        )

        st.markdown("### The 7 steps")

        steps_info = [
            ("Business Context", "Name it, pick domain & geography — regulations auto-detect"),
            ("Data Sources", "Register upstream systems with owners, SLAs, criticality"),
            ("Data Model", "Design tables & columns — tag PII to auto-generate masking"),
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
        st.markdown(f'<div class="journey-list">{items_html}</div>', unsafe_allow_html=True)

        st.markdown("### What gets generated")
        st.markdown(
            '<div class="deliv-row">'
            '<div class="deliv-item"><b>Snowflake</b>'
            "DDL, masking policies, secure views, GRANTs</div>"
            '<div class="deliv-item"><b>dbt</b>'
            "schema.yml, source defs, transformation SQL</div>"
            '<div class="deliv-item"><b>Governance</b>'
            "Collibra JSON, Markdown docs, versioned definition</div>"
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with canvas_col:
        render_canvas()


# ═══════════════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════════════
step = st.session_state.onboard

if step == 0:
    _landing()
elif step == 1:
    _sidebar_guide()
elif step == 2:
    _canvas_guide()
else:
    _dashboard()
