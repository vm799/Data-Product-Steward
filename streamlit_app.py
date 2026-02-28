import streamlit as st
from state_manager import initialize_state, get_progress, get_next_step
from components.layout import inject_custom_css, DATA_BOT_SVG
from components.sidebar import render_sidebar
from components.canvas import render_canvas
from components.helpers import PAGE_MAP, STEP_NAMES

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
# PAGE 0 — LANDING (concise value prop + deliverables)
# ═══════════════════════════════════════════════════════════════════════
def _landing():
    st.markdown(
        '<div class="landing">'
        + DATA_BOT_SVG
        + "<h1>Data Product Builder</h1>"
        '<div class="landing-tagline">'
        "7 weeks of manual work → 1 guided session"
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    # Before / After stat cards
    st.markdown(
        '<div class="landing-stat-row">'
        '<div class="landing-stat-card before">'
        '<div class="landing-stat-num">11</div>'
        '<div class="landing-stat-label">iterations across teams</div>'
        "</div>"
        '<div class="landing-arrow">→</div>'
        '<div class="landing-stat-card after">'
        '<div class="landing-stat-num">1</div>'
        '<div class="landing-stat-label">guided wizard session</div>'
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    # Deliverables grid
    st.markdown(
        '<div class="landing-deliv-title">What you walk away with</div>'
        '<div class="landing-deliv-grid">'
        '<div class="landing-deliv-chip">Snowflake DDL</div>'
        '<div class="landing-deliv-chip">Masking Policies</div>'
        '<div class="landing-deliv-chip">Secure Views</div>'
        '<div class="landing-deliv-chip">dbt Models</div>'
        '<div class="landing-deliv-chip">Collibra Metadata</div>'
        '<div class="landing-deliv-chip">Full Documentation</div>'
        "</div>",
        unsafe_allow_html=True,
    )

    _, btn_col, _ = st.columns([2, 1, 2])
    with btn_col:
        if st.button("Begin", use_container_width=True):
            st.session_state.onboard = 1
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════
# PAGE 1 — SIDEBAR GUIDE (visual mockup + annotations)
# ═══════════════════════════════════════════════════════════════════════
def _sidebar_guide():
    st.markdown(
        '<div class="guide-page">'
        '<div class="guide-step-num">1 / 2</div>'
        "<h2>The Sidebar</h2>"
        '<p class="guide-subtitle">Your command center — visible on every page</p>'
        "</div>",
        unsafe_allow_html=True,
    )

    mockup_col, explain_col = st.columns([1, 1])

    with mockup_col:
        st.markdown(
            '<div class="sidebar-mockup">'
            # 1 — Dashboard link
            '<div class="sm-section">'
            '<span class="sm-callout">1</span>'
            '<div class="sm-brand">⌂ DASHBOARD</div>'
            "</div>"
            '<div class="sm-divider"></div>'
            # 2 — Progress
            '<div class="sm-section">'
            '<span class="sm-callout">2</span>'
            '<div class="sm-label">Progress</div>'
            '<div class="sm-bar"><div class="sm-bar-fill"></div></div>'
            '<div class="sm-bar-text">28% — 2/7 steps</div>'
            "</div>"
            # 3 — Step list
            '<div class="sm-section">'
            '<span class="sm-callout">3</span>'
            '<div class="sm-step done">✅ Business Context</div>'
            '<div class="sm-step done">✅ Data Sources</div>'
            '<div class="sm-step current">⬜ ▶ Data Model ← here</div>'
            '<div class="sm-step">⬜ Governance &amp; Security</div>'
            '<div class="sm-step">⬜ Data Quality</div>'
            '<div class="sm-step">⬜ Transformations</div>'
            '<div class="sm-step">⬜ Review &amp; Export</div>'
            "</div>"
            '<div class="sm-divider"></div>'
            # 4 — Tips
            '<div class="sm-section">'
            '<span class="sm-callout">4</span>'
            '<div class="sm-label">Data Model — Why?</div>'
            '<div class="sm-tip">Tables &amp; columns define your product structure...</div>'
            "</div>"
            '<div class="sm-divider"></div>'
            # 5 — Glossary
            '<div class="sm-section">'
            '<span class="sm-callout">5</span>'
            '<div class="sm-label">Glossary</div>'
            '<div class="sm-tip">Key terms — expand to look up concepts</div>'
            "</div>"
            "</div>",
            unsafe_allow_html=True,
        )

    with explain_col:
        st.markdown(
            '<div class="guide-panel">'
            '<div class="guide-panel-label">What each section does</div>'
            '<div class="sm-explain-item">'
            '<span class="sm-explain-num">1</span>'
            "<b>Dashboard</b> — click to return to the overview at any time</div>"
            '<div class="sm-explain-item">'
            '<span class="sm-explain-num">2</span>'
            "<b>Progress bar</b> — tracks completion across all 7 steps</div>"
            '<div class="sm-explain-item">'
            '<span class="sm-explain-num">3</span>'
            "<b>Step list</b> — click any step name to navigate directly</div>"
            '<div class="sm-explain-item">'
            '<span class="sm-explain-num">4</span>'
            "<b>Step guide</b> — context-specific tips for your current step</div>"
            '<div class="sm-explain-item">'
            '<span class="sm-explain-num">5</span>'
            "<b>Glossary</b> — look up unfamiliar terms without leaving</div>"
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
# PAGE 2 — CANVAS GUIDE (visual mockup with typewriter demo)
# ═══════════════════════════════════════════════════════════════════════
def _canvas_guide():
    st.markdown(
        '<div class="guide-page">'
        '<div class="guide-step-num">2 / 2</div>'
        "<h2>The Live Canvas</h2>"
        '<p class="guide-subtitle">Your blueprint updates in real time as you build</p>'
        "</div>",
        unsafe_allow_html=True,
    )

    mockup_col, explain_col = st.columns([1, 1])

    with mockup_col:
        # Canvas mockup with typewriter demo
        st.markdown(
            '<div class="canvas-mockup">'
            '<div class="canvas-label">[ LIVE CANVAS ]</div>'
            '<div class="canvas-heading">Data Product Blueprint</div>'
            '<div class="canvas-explain">Updates as you build. Here\'s what a finished product looks like:</div>'
            '<div class="typewriter-demo">'
            '<div class="typewriter-line tw-dim tw-d1">// sample output</div>'
            '<div class="typewriter-line tw-bright tw-d2">Investor_Position_Summary</div>'
            '<div class="typewriter-line tw-dim tw-d3">Domain: Risk &middot; Region: UK</div>'
            '<div class="typewriter-line tw-d4">Entities: 3 &middot; Sources: 2 &middot; PII: 4 cols</div>'
            '<div class="typewriter-line tw-dim tw-d5">Classification: Confidential &middot; Retention: 7yr</div>'
            '<div class="typewriter-line tw-check tw-d6">&check; Snowflake DDL</div>'
            '<div class="typewriter-line tw-check tw-d7">&check; dbt Models &middot; &check; Masking Policies</div>'
            '<div class="typewriter-line tw-check tw-d8 tw-cursor">&check; Collibra Import &middot; &check; Docs</div>'
            "</div>"
            "</div>",
            unsafe_allow_html=True,
        )

    with explain_col:
        st.markdown(
            '<div class="guide-panel">'
            '<div class="guide-panel-label">What updates in real time</div>'
            '<div class="sm-explain-item">'
            '<span class="sm-explain-num">1</span>'
            "<b>Product identity</b> — name, domain, geography appear as you type</div>"
            '<div class="sm-explain-item">'
            '<span class="sm-explain-num">2</span>'
            "<b>Entities and sources</b> — tables, columns, PII tags populate live</div>"
            '<div class="sm-explain-item">'
            '<span class="sm-explain-num">3</span>'
            "<b>Governance</b> — classification, retention, compliance shown</div>"
            '<div class="sm-explain-item">'
            '<span class="sm-explain-num">4</span>'
            "<b>Deliverables checklist</b> — check marks appear as artifacts become ready</div>"
            '<div class="sm-explain-item">'
            '<span class="sm-explain-num">5</span>'
            "<b>Download anytime</b> — export artifacts even before completing all steps</div>"
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
# PAGE 3 — DASHBOARD (clickable steps + "start here" arrows)
# ═══════════════════════════════════════════════════════════════════════
def _dashboard():
    render_sidebar()

    st.markdown("# Dashboard")
    st.caption(
        "Your data product at a glance. "
        "Click a step below to start building."
    )

    # Metrics row
    if product.get("name"):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Product", product["name"])
        c2.metric("Progress", f"{progress['pct']}%")
        c3.metric("Entities", len(product.get("entities", [])))
        c4.metric("Sources", len(product.get("sources", [])))

    main_col, canvas_col = st.columns([5, 3])

    with main_col:
        st.markdown('<div class="wizard-panel">', unsafe_allow_html=True)

        st.markdown(
            "A **Data Product** in asset management is a governed dataset built "
            "for a specific business purpose — investor positions, risk exposures, "
            "regulatory reporting."
        )

        st.markdown("### The 7 Steps")
        st.caption("Click any step to navigate. Complete them in order for best results.")

        # ── Clickable journey list ──────────────────────────
        next_step = get_next_step(product)

        steps_info = [
            ("Business Context", "Name it, pick domain & geography — regulations auto-detect"),
            ("Data Sources", "Register upstream systems with owners, SLAs, criticality"),
            ("Data Model", "Design tables & columns — tag PII to auto-generate masking"),
            ("Governance", "Classify sensitivity, set retention, assign access roles"),
            ("Data Quality", "Set completeness/accuracy thresholds — become pipeline checks"),
            ("Transformations", "Document processing steps — generates runnable dbt models"),
            ("Review & Export", "Validate, fix errors, download all production artifacts"),
        ]

        for i, (name, desc) in enumerate(steps_info, 1):
            done = list(progress["steps"].values())[i - 1]
            is_next = i == next_step

            icon = "✅" if done else f"{i}"
            if is_next:
                label = f"{icon}  {name} — {desc}"
            else:
                label = f"{icon}  {name} — {desc}"

            st.page_link(PAGE_MAP[i], label=label)

            if is_next:
                st.markdown(
                    '<span class="flash-arrow">↑ START HERE</span>',
                    unsafe_allow_html=True,
                )

        st.markdown("### What Gets Generated")
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
