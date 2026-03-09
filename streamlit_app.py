import streamlit as st
from state_manager import initialize_state, get_progress, get_next_step
from components.layout import inject_custom_css, get_bot_svg
from components.sidebar import render_sidebar
from components.helpers import PAGE_MAP, STEP_NAMES

st.set_page_config(
    page_title="Data Product Builder",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
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
# PAGE 0 — LANDING (auto-scroll deliverables, orange focus)
# ═══════════════════════════════════════════════════════════════════════
_DELIVERABLES = [
    ("Snowflake DDL", "Production-ready CREATE TABLE, GRANT, and ALTER scripts", 3),
    ("Masking Policies", "Auto-generated from PII tags — column-level security", 4),
    ("Secure Views", "Row-level security for Restricted classification data", 4),
    ("dbt Models", "schema.yml, source defs, transformation SQL — deploy immediately", 6),
    ("Collibra Metadata", "JSON import for your data governance catalogue", 7),
    ("Full Documentation", "Markdown spec with lineage, ownership, and SLAs", 7),
]


def _landing():
    render_sidebar()

    # ── Hero — centred, full width ────────────────────────────────
    st.markdown(
        '<div class="landing-hero">'
        + get_bot_svg()
        + "<h1>Data Product Builder</h1>"
        '<div class="landing-tagline">'
        "7 weeks of manual work to 1 guided session"
        "</div>"
        '<div class="landing-value">'
        "A guided workflow that turns business requirements into production-ready "
        "Snowflake DDL, dbt models, masking policies, and governance metadata — "
        "so data teams ship compliant data products in hours, not weeks."
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Before / After stat cards — centred row ───────────────────
    st.markdown(
        '<div class="landing-stat-row">'
        '<div class="landing-stat-card before">'
        '<div class="landing-stat-num">11</div>'
        '<div class="landing-stat-label">iterations across teams</div>'
        "</div>"
        '<div class="landing-arrow">to</div>'
        '<div class="landing-stat-card after">'
        '<div class="landing-stat-num">1</div>'
        '<div class="landing-stat-label">guided workflow session</div>'
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Big CTA button ────────────────────────────────────────────
    st.markdown('<div class="hero-cta-wrap">', unsafe_allow_html=True)
    cta_col1, cta_col2, cta_col3 = st.columns([1, 1, 1])
    with cta_col1:
        if st.button("🧠 AI Agent", key="ai_agent_cta", use_container_width=True):
            st.page_link("pages/0_AI_Requirements_Agent.py", label="Start with AI Agent")
    with cta_col2:
        if st.button("⚡ Workflow", key="hero_cta", use_container_width=True):
            st.session_state.onboard = 1
            st.rerun()
    with cta_col3:
        if st.button("⚙️ Settings", key="settings_cta", use_container_width=True):
            st.page_link("pages/9_Settings.py", label="Settings")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Deliverables — full width grid below hero ─────────────────
    st.markdown(
        '<div class="landing-deliv-header">What you walk away with</div>',
        unsafe_allow_html=True,
    )

    cards_html = '<div class="deliv-carousel">'
    for i, (name, desc, step_num) in enumerate(_DELIVERABLES):
        href = PAGE_MAP[step_num]
        cards_html += (
            f'<a class="deliv-card deliv-auto deliv-link" style="--d:{i};" href="/{href}">'
            f'<div class="deliv-card-name">{name}</div>'
            f'<div class="deliv-card-desc">{desc}</div>'
            f'<div class="deliv-card-step">Step {step_num}: {STEP_NAMES[step_num - 1]}</div>'
            f"</a>"
        )
    cards_html += "</div>"

    st.markdown(cards_html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# PAGE 1 — SIDEBAR GUIDE (inline descriptions next to each feature)
# ═══════════════════════════════════════════════════════════════════════

_SB_SECTIONS = [
    (
        "1",
        "Dashboard Link",
        "Always visible at the top. Click <b>Dashboard</b> from any step "
        "to return to the overview — your progress is saved automatically.",
    ),
    (
        "2",
        "Progress Bar",
        "Tracks <b>how far you've come</b> across all 7 steps. "
        "The bar fills as you complete each section so you always "
        "know what's left.",
    ),
    (
        "3",
        "Step List",
        "Every step is a <b>clickable link</b>. Jump to any step directly — "
        "no need to go in strict order. Completed steps are marked, and the "
        "next suggested step is marked.",
    ),
    (
        "4",
        "Step Guide",
        "Context-sensitive help that <b>changes per step</b>. Shows why the "
        "current step matters, practical tips, and what downstream artifacts "
        "it feeds into.",
    ),
    (
        "5",
        "Glossary",
        "Expandable reference for <b>key terms</b> — PII, DDL, SLA, "
        "Masking Policy, and more. Look up unfamiliar concepts without "
        "leaving the page.",
    ),
]


def _sidebar_guide():
    render_sidebar()

    st.markdown(
        '<div class="guide-page">'
        '<div class="guide-step-num">1 / 2</div>'
        "<h2>The Sidebar</h2>"
        '<p class="guide-subtitle">Your command centre — visible on every page</p>'
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Build mockup HTML with INLINE descriptions ───────────────
    mockup_html = '<div class="sidebar-mockup sm-inline">'

    # 1 — Dashboard link
    mockup_html += (
        '<div class="sm-section-inline">'
        '<div class="sm-section-content">'
        '<span class="sm-callout">1</span>'
        '<div class="sm-brand">DASHBOARD</div>'
        '</div>'
        '<div class="sm-inline-desc">'
        '<span class="sm-inline-title">Dashboard Link</span>'
        f'{_SB_SECTIONS[0][2]}'
        '</div>'
        '</div>'
        '<div class="sm-divider"></div>'
    )

    # 2 — Progress
    mockup_html += (
        '<div class="sm-section-inline">'
        '<div class="sm-section-content">'
        '<span class="sm-callout">2</span>'
        '<div class="sm-label">Progress</div>'
        '<div class="sm-bar"><div class="sm-bar-fill"></div></div>'
        '<div class="sm-bar-text">28% — 2/7 steps</div>'
        '</div>'
        '<div class="sm-inline-desc">'
        '<span class="sm-inline-title">Progress Bar</span>'
        f'{_SB_SECTIONS[1][2]}'
        '</div>'
        '</div>'
        '<div class="sm-divider"></div>'
    )

    # 3 — Step list
    mockup_html += (
        '<div class="sm-section-inline">'
        '<div class="sm-section-content">'
        '<span class="sm-callout">3</span>'
        '<div class="sm-step done">1. Business Context</div>'
        '<div class="sm-step done">2. Data Sources</div>'
        '<div class="sm-step current">3. Data Model  (here)</div>'
        '<div class="sm-step">4. Governance &amp; Security</div>'
        '<div class="sm-step">5. Data Quality</div>'
        '<div class="sm-step">6. Transformations</div>'
        '<div class="sm-step">7. Review &amp; Export</div>'
        '</div>'
        '<div class="sm-inline-desc">'
        '<span class="sm-inline-title">Step List</span>'
        f'{_SB_SECTIONS[2][2]}'
        '</div>'
        '</div>'
        '<div class="sm-divider"></div>'
    )

    # 4 — Tips
    mockup_html += (
        '<div class="sm-section-inline">'
        '<div class="sm-section-content">'
        '<span class="sm-callout">4</span>'
        '<div class="sm-label">Data Model — Why?</div>'
        '<div class="sm-tip">Tables &amp; columns define your product '
        'structure. PII tagging auto-generates masking...</div>'
        '</div>'
        '<div class="sm-inline-desc">'
        '<span class="sm-inline-title">Step Guide</span>'
        f'{_SB_SECTIONS[3][2]}'
        '</div>'
        '</div>'
        '<div class="sm-divider"></div>'
    )

    # 5 — Glossary
    mockup_html += (
        '<div class="sm-section-inline">'
        '<div class="sm-section-content">'
        '<span class="sm-callout">5</span>'
        '<div class="sm-label">Glossary</div>'
        '<div class="sm-tip">PII &middot; DDL &middot; SLA &middot; dbt '
        '&middot; Lineage &middot; Masking Policy &middot; ...</div>'
        '</div>'
        '<div class="sm-inline-desc">'
        '<span class="sm-inline-title">Glossary</span>'
        f'{_SB_SECTIONS[4][2]}'
        '</div>'
        '</div>'
    )

    mockup_html += '</div>'

    st.markdown(mockup_html, unsafe_allow_html=True)

    # ── Navigation buttons ─────────────────────────────────────
    st.markdown("")
    _, back_col, _, fwd_col, _ = st.columns([1, 1, 1, 1, 1])

    with back_col:
        if st.button("Landing", use_container_width=True):
            st.session_state.onboard = 0
            st.rerun()

    with fwd_col:
        if st.button("Canvas Guide", use_container_width=True):
            st.session_state.onboard = 2
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════
# PAGE 2 — CANVAS GUIDE (visual mockup with typewriter demo)
# ═══════════════════════════════════════════════════════════════════════
def _canvas_guide():
    render_sidebar()

    st.markdown(
        '<div class="guide-page">'
        '<div class="guide-step-num">2 / 2</div>'
        "<h2>The Live Canvas</h2>"
        '<p class="guide-subtitle">Your blueprint updates in real time as you build</p>'
        "</div>",
        unsafe_allow_html=True,
    )

    mockup_col, explain_col = st.columns([3, 2])

    with mockup_col:
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
            '<div class="typewriter-line tw-check tw-d6">Snowflake DDL</div>'
            '<div class="typewriter-line tw-check tw-d7">dbt Models &middot; Masking Policies</div>'
            '<div class="typewriter-line tw-check tw-d8 tw-cursor">Collibra Import &middot; Docs</div>'
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
        if st.button("Go to Wizard Agent", use_container_width=True):
            st.session_state.onboard = 3
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════
# PAGE 3 — WIZARD AGENT (full-width step list, no canvas)
# ═══════════════════════════════════════════════════════════════════════

_STEPS_INFO = [
    ("Business Context", "Name it, pick domain & geography — regulations auto-detect"),
    ("Data Sources", "Register upstream systems with owners, SLAs, criticality"),
    ("Data Model", "Design tables & columns — tag PII to auto-generate masking"),
    ("Governance & Security", "Classify sensitivity, set retention, assign access roles"),
    ("Data Quality", "Set completeness/accuracy thresholds — become pipeline checks"),
    ("Transformations", "Document processing steps — generates runnable dbt models"),
    ("Review & Export", "Validate, fix errors, download all production artifacts"),
]


def _dashboard():
    render_sidebar()

    # ── Progress bar at the very top ──────────────────────────────
    st.markdown(
        f'<div class="top-progress-bar">'
        f'<div class="top-progress-fill" style="width:{progress["pct"]}%;"></div>'
        f'</div>'
        f'<div class="top-progress-label">{progress["pct"]}% complete — '
        f'{progress["done"]}/{progress["total"]} steps</div>',
        unsafe_allow_html=True,
    )

    st.markdown("# Wizard Agent")
    st.caption("Click a step below to start building.")
    st.markdown('<hr class="wiz-thin-rule">', unsafe_allow_html=True)

    next_step = get_next_step(product)
    step_done_list = list(progress["steps"].values())

    for i, (name, desc) in enumerate(_STEPS_INFO, 1):
        done = step_done_list[i - 1]
        is_next = i == next_step

        if done:
            st.page_link(
                PAGE_MAP[i],
                label=f"{name}  --  {desc}",
                use_container_width=True,
            )
        elif is_next:
            st.markdown(
                f'<div class="wiz-step-hero">'
                f'<div class="wiz-step-hero-num">STEP {i} OF 7</div>'
                f'<div class="wiz-step-hero-name">{name}</div>'
                f'<div class="wiz-step-hero-desc">{desc}</div>'
                f'<span class="wiz-step-hero-arrow">START HERE</span>'
                f"</div>",
                unsafe_allow_html=True,
            )
            st.page_link(
                PAGE_MAP[i],
                label=f"Open {name}",
                use_container_width=True,
            )
        else:
            st.page_link(
                PAGE_MAP[i],
                label=f"{i}.  {name}",
                use_container_width=True,
            )

    # ── Product Canvas link ─────────────────────────────────────
    st.divider()
    st.page_link(
        "pages/8_Product_Canvas.py",
        label="Product Canvas -- Live Contract View",
        use_container_width=True,
    )


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
