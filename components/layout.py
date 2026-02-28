"""
Theme — dark glassmorphism, Space Grotesk + mono accent.
Wider, heavier font for body. Mono only for labels and code.
SVG data bot icon, typewriter canvas demo.
"""

import streamlit as st

# ── SVG data bot icon (inline, teal on transparent) ─────────────────
DATA_BOT_SVG = """
<svg viewBox="0 0 200 220" xmlns="http://www.w3.org/2000/svg" class="data-bot-svg">
  <defs>
    <linearGradient id="tealGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#2DD4BF;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#22D3EE;stop-opacity:1"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <!-- Antenna -->
  <line x1="100" y1="12" x2="100" y2="38" stroke="#2DD4BF" stroke-width="2.5" opacity="0.7"/>
  <circle cx="100" cy="10" r="5" fill="#2DD4BF" filter="url(#glow)" opacity="0.9"/>

  <!-- Head -->
  <rect x="40" y="38" width="120" height="90" rx="18" ry="18"
        fill="none" stroke="url(#tealGrad)" stroke-width="2.5"/>

  <!-- Visor / screen -->
  <rect x="55" y="52" width="90" height="50" rx="8" ry="8"
        fill="rgba(45,212,191,0.08)" stroke="#2DD4BF" stroke-width="1.5"/>

  <!-- Data lines on screen -->
  <line x1="65" y1="65" x2="105" y2="65" stroke="#2DD4BF" stroke-width="2" opacity="0.8"/>
  <line x1="65" y1="75" x2="130" y2="75" stroke="#22D3EE" stroke-width="2" opacity="0.5"/>
  <line x1="65" y1="85" x2="115" y2="85" stroke="#2DD4BF" stroke-width="2" opacity="0.6"/>
  <rect x="120" y="62" width="15" height="8" rx="2" fill="#2DD4BF" opacity="0.3"/>
  <rect x="120" y="82" width="10" height="8" rx="2" fill="#22D3EE" opacity="0.3"/>

  <!-- Eyes -->
  <circle cx="78" cy="70" r="3.5" fill="#2DD4BF" filter="url(#glow)"/>
  <circle cx="122" cy="70" r="3.5" fill="#22D3EE" filter="url(#glow)"/>

  <!-- Body -->
  <rect x="55" y="138" width="90" height="55" rx="12" ry="12"
        fill="none" stroke="url(#tealGrad)" stroke-width="2"/>

  <!-- Neck connector -->
  <rect x="85" y="128" width="30" height="14" rx="4"
        fill="rgba(45,212,191,0.1)" stroke="#2DD4BF" stroke-width="1.5"/>

  <!-- Body circuit lines -->
  <line x1="75" y1="155" x2="95" y2="155" stroke="#2DD4BF" stroke-width="1.5" opacity="0.5"/>
  <line x1="105" y1="155" x2="125" y2="155" stroke="#22D3EE" stroke-width="1.5" opacity="0.5"/>
  <circle cx="100" cy="155" r="4" fill="none" stroke="#2DD4BF" stroke-width="1.5" opacity="0.7"/>
  <line x1="75" y1="168" x2="125" y2="168" stroke="#2DD4BF" stroke-width="1" opacity="0.3"/>
  <line x1="75" y1="178" x2="110" y2="178" stroke="#22D3EE" stroke-width="1" opacity="0.3"/>

  <!-- Side nodes -->
  <circle cx="32" cy="80" r="4" fill="none" stroke="#2DD4BF" stroke-width="1.5" opacity="0.5"/>
  <line x1="36" y1="80" x2="40" y2="80" stroke="#2DD4BF" stroke-width="1.5" opacity="0.5"/>
  <circle cx="168" cy="80" r="4" fill="none" stroke="#22D3EE" stroke-width="1.5" opacity="0.5"/>
  <line x1="160" y1="80" x2="164" y2="80" stroke="#22D3EE" stroke-width="1.5" opacity="0.5"/>

  <!-- Base -->
  <rect x="70" y="198" width="60" height="8" rx="4"
        fill="rgba(45,212,191,0.15)" stroke="#2DD4BF" stroke-width="1"/>
</svg>
"""


def _css() -> str:
    return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Share+Tech+Mono&display=swap');

    /* ═══════════════════════════════════════════════════
       GLOBAL — Space Grotesk body, Share Tech Mono accents
       ═══════════════════════════════════════════════════ */
    .stApp {
        background: linear-gradient(160deg, #06080D 0%, #0B1220 50%, #091018 100%) !important;
        color: #E8ECF1;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    .stApp p, .stApp span, .stApp label, .stApp input,
    .stApp textarea, .stApp select, .stApp button,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4,
    .stApp li, .stApp td, .stApp th, .stApp a, .stApp div {
        font-family: 'Space Grotesk', sans-serif !important;
    }
    /* Mono only for code and accents */
    .stApp code, .canvas-label, .step-badge,
    .sidebar-label, .typewriter-line {
        font-family: 'Share Tech Mono', monospace !important;
    }

    /* ── Kill top whitespace ────────────────────────── */
    .main .block-container {
        padding: 0.6rem 1.8rem 2rem 1.8rem !important;
        max-width: 100%;
    }
    [data-testid="stHeader"] {
        background: transparent !important;
        height: 0 !important;
        min-height: 0 !important;
        overflow: hidden;
    }

    /* ── Top progress bar (always visible) ──────────── */
    .top-progress-bar {
        width: 100%;
        height: 6px;
        background: rgba(255,255,255,0.06);
        border-radius: 3px;
        overflow: hidden;
        margin-bottom: 0.25rem;
    }
    .top-progress-fill {
        height: 100%;
        background: linear-gradient(135deg, #F97316 0%, #FB923C 50%, #2DD4BF 100%);
        border-radius: 3px;
        transition: width 0.6s ease;
        box-shadow: 0 0 8px rgba(249,115,22,0.4);
    }
    .top-progress-label {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.72rem;
        letter-spacing: 0.12em;
        color: #5A6478;
        text-align: right;
        margin-bottom: 0.6rem;
    }

    /* ═══════════════════════════════════════════════════
       TYPOGRAPHY — larger, heavier
       ═══════════════════════════════════════════════════ */
    [data-testid="stAppViewContainer"] > .main {
        font-size: 1.18rem;
        line-height: 1.75;
        color: #E8ECF1;
    }
    h1 {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        color: #2DD4BF !important;
        line-height: 1.25 !important;
        margin-bottom: 0.4rem !important;
    }
    h2 {
        font-size: 1.65rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.01em;
        color: #2DD4BF !important;
        line-height: 1.3 !important;
        margin-bottom: 0.3rem !important;
    }
    h3 {
        font-size: 1.35rem !important;
        font-weight: 600 !important;
        color: #2DD4BF !important;
        line-height: 1.35 !important;
        margin-bottom: 0.25rem !important;
    }
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: #E8ECF1;
        font-size: 1.15rem;
        line-height: 1.75;
        font-weight: 400;
    }
    [data-testid="stMarkdownContainer"] strong {
        color: #E8ECF1;
        font-weight: 600;
    }
    .stCaption, [data-testid="stCaptionContainer"] {
        color: #8B95A5 !important;
        font-size: 1rem !important;
        line-height: 1.5 !important;
    }

    /* ── Form labels ────────────────────────────────── */
    .stTextInput label p, .stSelectbox label p,
    .stMultiSelect label p, .stTextArea label p,
    .stSlider label p, .stNumberInput label p,
    .stCheckbox label p {
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        color: #E8ECF1 !important;
        line-height: 1.5 !important;
    }

    /* ── Frosted glass inputs — teal text for readability ─ */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(45,212,191,0.25) !important;
        border-radius: 0.5rem !important;
        color: #2DD4BF !important;
        font-size: 1.1rem !important;
        backdrop-filter: blur(12px);
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder,
    .stNumberInput input::placeholder {
        color: rgba(45,212,191,0.40) !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
        border-color: #2DD4BF !important;
        box-shadow: 0 0 0 2px rgba(45,212,191,0.25),
                    0 0 16px rgba(45,212,191,0.12) !important;
        background: rgba(255,255,255,0.08) !important;
    }
    .stSelectbox [data-baseweb="select"], .stMultiSelect [data-baseweb="select"] {
        background: rgba(255,255,255,0.06) !important;
        border-color: rgba(45,212,191,0.25) !important;
    }
    .stSelectbox [data-baseweb="select"] > div, .stMultiSelect [data-baseweb="select"] > div {
        background: rgba(255,255,255,0.06) !important;
        color: #2DD4BF !important;
    }
    /* Dropdown menu — dark background for contrast */
    [data-baseweb="popover"] [data-baseweb="menu"],
    [data-baseweb="popover"] ul {
        background: #1A1D23 !important;
    }
    [data-baseweb="popover"] li {
        color: #E8ECF1 !important;
    }
    [data-baseweb="popover"] li:hover {
        background: rgba(45,212,191,0.12) !important;
    }
    /* Checkbox — keep dark theme */
    .stCheckbox label span { color: #E8ECF1 !important; }

    /* ── Metrics ────────────────────────────────────── */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(16px);
        padding: 0.9rem 1rem;
        border-radius: 0.75rem;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 4px 24px rgba(0,0,0,0.15);
    }
    [data-testid="stMetric"] label {
        color: #8B95A5 !important;
        font-size: 0.92rem !important;
        line-height: 1.3 !important;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #2DD4BF !important;
        font-weight: 700 !important;
        font-size: 1.4rem !important;
        line-height: 1.3 !important;
    }

    /* ── Progress bar ───────────────────────────────── */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #2DD4BF 0%, #22D3EE 100%) !important;
    }
    .stProgress > div > div {
        background: rgba(45,212,191,0.08) !important;
    }

    /* ═══════════════════════════════════════════════════
       WIZARD PANEL — frosted glass
       ═══════════════════════════════════════════════════ */
    .wizard-panel {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 0.75rem;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.20);
    }

    /* (form glow removed — full-width layout) */

    /* ── Step complete prompt ──────────────────────────── */
    .step-complete-prompt {
        background: rgba(45,212,191,0.06);
        border: 1px solid rgba(45,212,191,0.25);
        border-radius: 0.75rem;
        padding: 1.2rem 1.5rem;
        margin-top: 1rem;
        text-align: center;
    }
    .step-complete-prompt-title {
        font-size: 1.25rem; font-weight: 700;
        color: #2DD4BF; margin-bottom: 0.3rem;
    }
    .step-complete-prompt-desc {
        font-size: 1rem; color: #8B95A5;
        margin-bottom: 0.5rem;
    }

    /* ═══════════════════════════════════════════════════
       SIDEBAR
       ═══════════════════════════════════════════════════ */
    section[data-testid="stSidebar"] {
        background: rgba(8,12,22,0.85) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255,255,255,0.06) !important;
        font-size: 1.08rem;
    }
    section[data-testid="stSidebar"] * { color: #8B95A5 !important; }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 { color: #E8ECF1 !important; }
    section[data-testid="stSidebar"] h1 {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        line-height: 1.3 !important;
    }
    section[data-testid="stSidebar"] h3 {
        font-size: 1.12rem !important;
        font-weight: 600 !important;
        line-height: 1.3 !important;
    }
    section[data-testid="stSidebar"] .stCaption *,
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
        color: #5A6478 !important;
    }
    section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.08) !important; }
    section[data-testid="stSidebar"] .stProgress > div > div > div {
        background: linear-gradient(135deg, #2DD4BF 0%, #22D3EE 100%) !important;
    }

    /* ── Dashboard link ─────────────────────────────── */
    [data-testid="stSidebarNav"] li:first-child span { font-size: 0 !important; }
    [data-testid="stSidebarNav"] li:first-child span::after {
        content: "> DASHBOARD_";
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 1.05rem;
        letter-spacing: 0.06em;
        color: #2DD4BF !important;
        text-shadow: 0 0 8px rgba(45,212,191,0.4);
    }
    [data-testid="stSidebarNav"] li:first-child:hover span::after {
        text-shadow: 0 0 14px rgba(45,212,191,0.7);
        color: #5EEAD4 !important;
    }

    /* ── Guide card ─────────────────────────────────── */
    .guide-card {
        background: rgba(45,212,191,0.06);
        border-left: 2px solid #2DD4BF;
        padding: 0.75rem 0.85rem;
        border-radius: 0 0.4rem 0.4rem 0;
        font-size: 1.02rem;
        line-height: 1.65;
        margin-bottom: 0.5rem;
    }
    .guide-card, .guide-card * { color: #8B95A5 !important; }

    /* ═══════════════════════════════════════════════════
       CANVAS — glass + pulsing teal glow
       ═══════════════════════════════════════════════════ */
    @keyframes canvasPulse {
        0%   { box-shadow: 0 0 20px rgba(45,212,191,0.06), 0 0 40px rgba(45,212,191,0.03); border-color: rgba(45,212,191,0.15); }
        50%  { box-shadow: 0 0 35px rgba(45,212,191,0.18), 0 0 70px rgba(45,212,191,0.08); border-color: rgba(45,212,191,0.35); }
        100% { box-shadow: 0 0 20px rgba(45,212,191,0.06), 0 0 40px rgba(45,212,191,0.03); border-color: rgba(45,212,191,0.15); }
    }
    .canvas-panel {
        background: rgba(45,212,191,0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(45,212,191,0.15);
        border-radius: 2px;
        padding: 1.25rem;
        min-height: 480px;
        animation: canvasPulse 3s ease-in-out infinite;
        box-shadow: inset 3px 0 0 rgba(45,212,191,0.4);
        border-left: 3px solid rgba(45,212,191,0.35);
        border-top: none;
        border-right: none;
        border-bottom: none;
        position: relative;
    }
    .canvas-panel::before {
        content: "";
        position: absolute;
        top: 0; right: 0;
        width: 0; height: 0;
        border-style: solid;
        border-width: 0 28px 28px 0;
        border-color: transparent #0D1117 transparent transparent;
    }
    .canvas-panel::after {
        content: "";
        position: absolute;
        top: 0; right: 0;
        width: 28px; height: 28px;
        border-bottom: 1px solid rgba(45,212,191,0.25);
    }
    .canvas-panel, .canvas-panel p, .canvas-panel li,
    .canvas-panel span, .canvas-panel strong, .canvas-panel b { color: #E8ECF1 !important; }
    .canvas-panel .stCaption *, .canvas-panel [data-testid="stCaptionContainer"] * { color: #8B95A5 !important; }
    .canvas-panel hr { border-color: rgba(255,255,255,0.08) !important; }
    .canvas-panel [data-testid="stMetric"] {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: none;
    }
    .canvas-panel [data-testid="stMetric"] label { color: #8B95A5 !important; }
    .canvas-panel [data-testid="stMetric"] [data-testid="stMetricValue"] { color: #2DD4BF !important; }
    .canvas-panel .stDownloadButton button {
        background: rgba(255,255,255,0.06) !important;
        color: #E8ECF1 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        font-size: 0.9rem !important;
        padding: 0.35rem 0.8rem !important;
        width: 100%;
    }
    .canvas-panel .stDownloadButton button:hover { background: rgba(255,255,255,0.10) !important; }
    .canvas-panel .stDownloadButton { margin-bottom: 0.3rem; }
    .canvas-panel .streamlit-expanderHeader,
    .canvas-panel .streamlit-expanderHeader p { background: rgba(255,255,255,0.04) !important; color: #E8ECF1 !important; }
    .canvas-panel [data-testid="stExpander"] { overflow: visible; }

    /* ── LIVE CANVAS label — mono, pulsing glow ─────── */
    @keyframes labelPulse {
        0%   { text-shadow: 0 0 8px rgba(45,212,191,0.5), 0 0 16px rgba(45,212,191,0.25); }
        50%  { text-shadow: 0 0 14px rgba(45,212,191,0.8), 0 0 28px rgba(45,212,191,0.4); }
        100% { text-shadow: 0 0 8px rgba(45,212,191,0.5), 0 0 16px rgba(45,212,191,0.25); }
    }
    .canvas-label {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #2DD4BF !important;
        margin-bottom: 0.1rem;
        animation: labelPulse 2s ease-in-out infinite;
    }
    .canvas-heading {
        font-size: 1.25rem;
        font-weight: 700;
        color: #E8ECF1 !important;
        margin-bottom: 0.5rem;
        line-height: 1.3;
    }
    .canvas-explain {
        color: #8B95A5 !important;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 0.8rem;
    }
    .canvas-body {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 0.5rem;
        padding: 0.8rem 1rem;
        font-size: 1.05rem;
        color: #E8ECF1;
        line-height: 1.6;
    }

    /* ── Canvas populated detail styles ──────────────── */
    .cv-section {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #2DD4BF !important;
        margin-top: 1rem;
        margin-bottom: 0.3rem;
        padding-bottom: 0.2rem;
        border-bottom: 1px solid rgba(45,212,191,0.15);
    }
    .cv-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        padding: 0.15rem 0;
        gap: 0.5rem;
    }
    .cv-field-label {
        font-size: 0.8rem;
        color: #8B95A5 !important;
        white-space: nowrap;
        min-width: 5rem;
        flex-shrink: 0;
    }
    .cv-field-value {
        font-size: 0.85rem;
        color: #E8ECF1 !important;
        text-align: right;
        word-break: break-word;
    }
    .cv-empty {
        font-size: 0.85rem;
        color: rgba(139,149,165,0.5) !important;
        font-style: italic;
        padding: 0.2rem 0;
    }
    .cv-divider {
        border: none !important;
        border-top: 1px solid rgba(45,212,191,0.12) !important;
        margin: 0.75rem 0 !important;
    }
    /* Sources */
    .cv-source-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.25rem 0 0 0;
    }
    .cv-source-name {
        font-size: 0.9rem;
        font-weight: 600;
        color: #E8ECF1 !important;
    }
    .cv-source-tags {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.7rem;
        color: #8B95A5 !important;
    }
    .cv-source-owner {
        font-size: 0.75rem;
        color: #8B95A5 !important;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid rgba(255,255,255,0.04);
    }
    /* Entities / attributes */
    .cv-entity-name {
        font-size: 0.9rem;
        font-weight: 600;
        color: #2DD4BF !important;
        font-family: 'Share Tech Mono', monospace !important;
        margin-top: 0.4rem;
        margin-bottom: 0.15rem;
    }
    .cv-attr-row {
        display: flex;
        align-items: center;
        padding: 0.08rem 0 0.08rem 0.8rem;
        gap: 0.4rem;
    }
    .cv-attr-name {
        font-size: 0.8rem;
        color: #E8ECF1 !important;
    }
    .cv-attr-type {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.7rem;
        color: #8B95A5 !important;
        margin-left: auto;
    }
    .cv-pii-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #F97316;
        flex-shrink: 0;
    }
    .cv-pii-tag {
        color: #F97316 !important;
        font-weight: 600;
        font-size: 0.75rem;
    }
    /* Transformations */
    .cv-transform-row {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding-top: 0.3rem;
    }
    .cv-transform-num {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.75rem;
        color: #2DD4BF !important;
        background: rgba(45,212,191,0.10);
        border-radius: 4px;
        padding: 0.1rem 0.35rem;
        flex-shrink: 0;
    }
    .cv-transform-name {
        font-size: 0.85rem;
        font-weight: 600;
        color: #E8ECF1 !important;
    }
    .cv-transform-desc {
        font-size: 0.75rem;
        color: #8B95A5 !important;
        padding: 0 0 0.25rem 2rem;
        border-bottom: 1px solid rgba(255,255,255,0.04);
    }

    /* ═══════════════════════════════════════════════════
       TYPEWRITER DEMO — canvas empty state
       ═══════════════════════════════════════════════════ */
    @keyframes blink { 50% { border-color: transparent; } }
    @keyframes fadeInLine { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }

    .typewriter-demo {
        margin-top: 0.5rem;
        padding: 1rem;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 0.5rem;
    }
    .typewriter-line {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.95rem;
        line-height: 1.8;
        color: #2DD4BF;
        opacity: 0;
        animation: fadeInLine 0.4s ease forwards;
        white-space: nowrap;
        overflow: hidden;
    }
    .typewriter-line.tw-dim { color: #5A6478; }
    .typewriter-line.tw-bright { color: #E8ECF1; }
    .typewriter-line.tw-check { color: #10B981; }
    .tw-d1 { animation-delay: 0.3s; }
    .tw-d2 { animation-delay: 0.9s; }
    .tw-d3 { animation-delay: 1.5s; }
    .tw-d4 { animation-delay: 2.1s; }
    .tw-d5 { animation-delay: 2.7s; }
    .tw-d6 { animation-delay: 3.3s; }
    .tw-d7 { animation-delay: 3.9s; }
    .tw-d8 { animation-delay: 4.5s; }
    .tw-cursor::after {
        content: "_";
        animation: blink 0.8s step-end infinite;
        color: #2DD4BF;
    }

    /* ── Step badge (mono accent) ───────────────────── */
    .step-badge {
        display: inline-block;
        font-family: 'Share Tech Mono', monospace !important;
        background: rgba(45,212,191,0.08);
        color: #2DD4BF;
        padding: 0.25rem 0.8rem;
        border-radius: 1rem;
        font-size: 0.92rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    /* ═══════════════════════════════════════════════════
       STEP INDICATOR BAR — top-of-page wizard progress
       ═══════════════════════════════════════════════════ */
    .step-bar-wrap {
        display: flex;
        align-items: flex-start;
        justify-content: center;
        padding: 0.75rem 0 0.5rem;
        gap: 0;
    }
    .step-pip {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.3rem;
        min-width: 3rem;
    }
    .pip-circle {
        width: 2.2rem;
        height: 2.2rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.9rem;
        font-weight: 700;
        background: rgba(255,255,255,0.04);
        border: 2px solid rgba(255,255,255,0.10);
        color: #555;
        transition: all 0.3s;
    }
    .pip-label {
        font-size: 0.62rem;
        color: #555;
        font-family: 'Share Tech Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        white-space: nowrap;
    }
    /* Current step — solid orange */
    .step-pip.current .pip-circle {
        background: #F97316;
        border-color: #F97316;
        color: #fff;
        box-shadow: 0 0 14px rgba(249,115,22,0.5);
    }
    .step-pip.current .pip-label {
        color: #F97316;
        font-weight: 700;
    }
    /* Completed step — teal */
    .step-pip.done .pip-circle {
        background: rgba(45,212,191,0.12);
        border-color: #2DD4BF;
        color: #2DD4BF;
    }
    .step-pip.done .pip-label {
        color: #2DD4BF;
    }
    /* Next step — orange outline + pulse */
    .step-pip.next-up .pip-circle {
        border-color: #F97316;
        color: #F97316;
        animation: pulse-next 2s ease-in-out infinite;
    }
    .step-pip.next-up .pip-label {
        color: #F97316;
    }
    /* Connector lines */
    .pip-line {
        width: 1.5rem;
        height: 2px;
        background: rgba(255,255,255,0.08);
        margin-top: 1.1rem;
        flex-shrink: 0;
    }
    .pip-line.done {
        background: #2DD4BF;
    }
    @keyframes pulse-next {
        0%, 100% { box-shadow: 0 0 0 0 rgba(249,115,22,0.35); }
        50% { box-shadow: 0 0 0 7px rgba(249,115,22,0); }
    }

    /* ── Expander / Tabs / Alerts ────────────────────── */
    .streamlit-expanderHeader { background: rgba(255,255,255,0.04) !important; border-radius: 0.5rem !important; color: #E8ECF1 !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
    .stTabs [data-baseweb="tab"] { color: #8B95A5 !important; }
    .stTabs [aria-selected="true"] { color: #2DD4BF !important; border-bottom-color: #2DD4BF !important; }
    .stCodeBlock { border-radius: 0.5rem !important; }
    .stAlert { border-radius: 0.5rem !important; }
    hr { border-color: rgba(255,255,255,0.08) !important; }

    /* ── Buttons ─────────────────────────────────────── */
    .stDownloadButton button {
        background: linear-gradient(135deg, #2DD4BF 0%, #22D3EE 100%) !important;
        color: #06080D !important; border: none !important;
        border-radius: 0.5rem !important; font-weight: 600 !important;
        font-size: 1.05rem !important;
    }
    .stFormSubmitButton button {
        background: linear-gradient(135deg, #2DD4BF 0%, #22D3EE 100%) !important;
        color: #06080D !important; border: none !important;
        border-radius: 0.5rem !important; font-weight: 600 !important;
        padding: 0.5rem 2rem !important; font-size: 1.05rem !important;
    }
    .stButton > button {
        border: 1px solid rgba(255,255,255,0.12) !important;
        color: #2DD4BF !important;
        border-radius: 0.5rem !important;
        background: transparent !important;
        font-size: 1.1rem !important;
        padding: 0.55rem 1.5rem !important;
        font-weight: 500 !important;
    }
    .stButton > button:hover {
        background: rgba(45,212,191,0.08) !important;
        border-color: #2DD4BF !important;
    }

    /* ═══════════════════════════════════════════════════
       LANDING PAGE
       ═══════════════════════════════════════════════════ */
    .landing {
        text-align: center;
        padding: 3rem 1rem 1.5rem 1rem;
    }
    .data-bot-svg {
        width: 180px;
        height: 200px;
        margin: 0 auto 1.5rem auto;
        display: block;
        filter: drop-shadow(0 0 25px rgba(45,212,191,0.3));
    }
    .landing h1 {
        font-size: 2.8rem !important;
        letter-spacing: 0.06em;
        margin-bottom: 0.8rem !important;
    }
    .landing-sub {
        font-size: 1.25rem;
        color: #8B95A5;
        max-width: 620px;
        margin: 0 auto;
        line-height: 1.75;
        font-weight: 400;
    }

    /* ═══════════════════════════════════════════════════
       GUIDE PAGES
       ═══════════════════════════════════════════════════ */
    .guide-page {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    .guide-step-num {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.9rem;
        letter-spacing: 0.15em;
        color: #5A6478;
        margin-bottom: 0.3rem;
    }
    .guide-page h2 { text-align: center; margin-bottom: 0.6rem !important; }
    .guide-panel {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 0.75rem;
        padding: 1.5rem;
        min-height: 280px;
    }
    .guide-panel p, .guide-panel li {
        font-size: 1.12rem !important;
        line-height: 1.75 !important;
        color: #C8D0DC !important;
    }
    .guide-panel b { color: #E8ECF1 !important; }
    .guide-panel-label {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.78rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #2DD4BF;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }

    /* ═══════════════════════════════════════════════════
       WIZARD AGENT — step hierarchy + orange next
       ═══════════════════════════════════════════════════ */
    .wiz-thin-rule {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.08);
        margin: 0.4rem 0 1.2rem 0;
    }

    /* ── Hero step — the next incomplete step ────────── */
    .wiz-step-hero {
        background: rgba(249,115,22,0.06);
        border: 2px solid rgba(249,115,22,0.35);
        border-radius: 0;
        clip-path: polygon(0 12px, 12px 0, 100% 0, 100% calc(100% - 12px), calc(100% - 12px) 100%, 0 100%);
        padding: 1.6rem 1.8rem;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: border-color 0.3s, box-shadow 0.3s;
        position: relative;
        box-shadow: inset 4px 0 0 #F97316;
    }
    .wiz-step-hero:hover {
        border-color: #F97316;
        box-shadow: inset 4px 0 0 #F97316, 0 0 24px rgba(249,115,22,0.18);
    }
    .wiz-step-hero-num {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.82rem; letter-spacing: 0.1em;
        color: #F97316; font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    .wiz-step-hero-name {
        font-size: 1.8rem; font-weight: 700;
        color: #E8ECF1; line-height: 1.3;
        margin-bottom: 0.3rem;
    }
    .wiz-step-hero-desc {
        font-size: 1.15rem; color: #C8D0DC;
        line-height: 1.6;
    }
    .wiz-step-hero-arrow {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 1rem; font-weight: 700;
        color: #F97316 !important;
        animation: flashArrow 1.2s ease-in-out infinite;
        margin-top: 0.6rem;
        display: inline-block;
    }

    /* ── Completed step — enlarged tick, faded text ───── */
    .wiz-step-done {
        display: flex; align-items: center; gap: 0.8rem;
        padding: 0.7rem 1rem;
        background: rgba(45,212,191,0.04);
        border: 1px solid rgba(45,212,191,0.12);
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .wiz-step-done-tick {
        font-size: 1.6rem; flex-shrink: 0;
    }
    .wiz-step-done-name {
        font-size: 1.25rem; font-weight: 600;
        color: #2DD4BF;
    }
    .wiz-step-done-desc {
        font-size: 0.95rem; color: #5A6478;
        margin-left: auto;
    }

    /* ── Pending step — small, dimmed ────────────────── */
    .wiz-step-pending {
        display: flex; align-items: center; gap: 0.7rem;
        padding: 0.5rem 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.04);
        opacity: 0.5;
    }
    .wiz-step-pending:last-child { border-bottom: none; }
    .wiz-step-pending-num {
        flex-shrink: 0;
        width: 24px; height: 24px; border-radius: 50%;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        color: #5A6478;
        font-size: 0.72rem; font-weight: 600;
        display: inline-flex; align-items: center; justify-content: center;
    }
    .wiz-step-pending-name {
        font-size: 1rem; color: #5A6478; font-weight: 500;
    }

    /* ── Deliverables row ─────────────────────────────── */
    .deliv-row { display: flex; gap: 0.75rem; margin: 0.4rem 0; }
    .deliv-item {
        flex: 1;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 0.5rem;
        padding: 0.8rem 1rem;
        font-size: 1rem; line-height: 1.55;
        color: #8B95A5;
    }
    .deliv-item b { display: block; margin-bottom: 0.15rem; color: #E8ECF1; font-size: 1.05rem; }

    /* ── Empty canvas placeholder ─────────────────────── */
    .wiz-canvas-empty {
        display: flex; align-items: center; justify-content: center;
        min-height: 400px;
        color: #3A4250;
        font-size: 1.15rem;
        font-style: italic;
    }

    /* ── Sidebar label (mono accent) ────────────────── */
    .sidebar-label {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #5A6478 !important;
        margin-bottom: 0.2rem;
    }

    /* ═══════════════════════════════════════════════════
       LANDING PAGE — value prop + deliverables grid
       ═══════════════════════════════════════════════════ */
    .landing-tagline {
        font-size: 1.6rem;
        color: #2DD4BF;
        font-weight: 600;
        max-width: 580px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.5;
    }
    .landing-stat-row {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1.5rem;
        margin: 1.5rem auto;
        max-width: 650px;
    }
    .landing-stat-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 0;
        clip-path: polygon(0 8px, 8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%);
        padding: 1.2rem 1.5rem;
        text-align: center;
        flex: 1;
        position: relative;
    }
    .landing-stat-card.before {
        border-color: rgba(239,68,68,0.3);
        background: rgba(239,68,68,0.04);
        box-shadow: inset 3px 0 0 #EF4444;
    }
    .landing-stat-card.after {
        border-color: rgba(45,212,191,0.3);
        background: rgba(45,212,191,0.04);
        box-shadow: inset 3px 0 0 #2DD4BF;
    }
    .landing-stat-num {
        font-size: 2.8rem;
        font-weight: 700;
        color: #2DD4BF;
        line-height: 1.2;
    }
    .before .landing-stat-num { color: #EF4444; }
    .landing-stat-label {
        font-size: 0.95rem;
        color: #8B95A5;
        margin-top: 0.2rem;
    }
    .landing-arrow {
        font-size: 2.5rem;
        color: #2DD4BF;
        flex-shrink: 0;
    }
    /* ── Top-of-page direction arrows (prominent) ─── */
    .arrow-prev-top {
        font-size: 2.4rem;
        font-weight: 700;
        color: #2DD4BF;
        text-align: center;
        padding: 0.3rem 0;
        background: rgba(45,212,191,0.08);
        border: 1px solid rgba(45,212,191,0.25);
        clip-path: polygon(0 6px, 6px 0, 100% 0, 100% calc(100% - 6px), calc(100% - 6px) 100%, 0 100%);
        animation: arrowBounceL 1.5s ease-in-out infinite;
    }
    .arrow-next-top {
        font-size: 2.4rem;
        font-weight: 700;
        color: #F97316;
        text-align: center;
        padding: 0.3rem 0;
        background: rgba(249,115,22,0.08);
        border: 1px solid rgba(249,115,22,0.25);
        clip-path: polygon(0 6px, 6px 0, 100% 0, 100% calc(100% - 6px), calc(100% - 6px) 100%, 0 100%);
        animation: arrowBounceR 1.5s ease-in-out infinite;
    }
    .arrow-top-label {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.78rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #5A6478;
        text-align: center;
        padding-top: 0.8rem;
    }
    @keyframes arrowBounceL {
        0%, 100% { transform: translateX(0); }
        50% { transform: translateX(-8px); }
    }
    @keyframes arrowBounceR {
        0%, 100% { transform: translateX(0); }
        50% { transform: translateX(8px); }
    }

    /* ── Deliverable panel (landing right side) ──────── */
    .deliv-panel-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #E8ECF1 !important;
        margin-bottom: 1rem;
        line-height: 1.3;
    }

    /* ── Auto-cycling deliverable carousel ──────────── */
    .deliv-carousel {
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
    }
    .deliv-card.deliv-auto {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 0;
        clip-path: polygon(0 6px, 6px 0, 100% 0, 100% calc(100% - 6px), calc(100% - 6px) 100%, 0 100%);
        padding: 0.55rem 1rem;
        opacity: 0.35;
        transform: scale(1);
        transition: none;
        animation: delivCycle 18s ease-in-out infinite;
        animation-delay: calc(var(--d) * 3s);
    }
    @keyframes delivCycle {
        0%      { opacity: 0.35; transform: scale(1); background: rgba(255,255,255,0.03);
                  border-color: rgba(255,255,255,0.06); box-shadow: none; padding: 0.55rem 1rem; }
        2%      { opacity: 1; transform: scale(1.04);
                  background: rgba(249,115,22,0.08);
                  border-color: rgba(249,115,22,0.5);
                  box-shadow: inset 3px 0 0 #F97316, 0 0 22px rgba(249,115,22,0.15);
                  padding: 1rem 1.2rem; }
        14%     { opacity: 1; transform: scale(1.04);
                  background: rgba(249,115,22,0.08);
                  border-color: rgba(249,115,22,0.5);
                  box-shadow: inset 3px 0 0 #F97316, 0 0 22px rgba(249,115,22,0.15);
                  padding: 1rem 1.2rem; }
        18%     { opacity: 0.35; transform: scale(1); background: rgba(255,255,255,0.03);
                  border-color: rgba(255,255,255,0.06); box-shadow: none; padding: 0.55rem 1rem; }
        100%    { opacity: 0.35; transform: scale(1); background: rgba(255,255,255,0.03);
                  border-color: rgba(255,255,255,0.06); box-shadow: none; padding: 0.55rem 1rem; }
    }
    .deliv-card.deliv-auto .deliv-card-name {
        font-size: 1.05rem;
        font-weight: 700;
        color: #8B95A5;
        font-family: 'Share Tech Mono', monospace !important;
        transition: color 0.3s, font-size 0.3s;
    }
    .deliv-card.deliv-auto .deliv-card-desc {
        font-size: 0;
        color: #C8D0DC;
        max-height: 0;
        overflow: hidden;
        line-height: 1.5;
        opacity: 0;
        transition: none;
        animation: delivDescCycle 18s ease-in-out infinite;
        animation-delay: calc(var(--d) * 3s);
    }
    .deliv-card.deliv-auto .deliv-card-step {
        font-size: 0;
        color: #F97316;
        max-height: 0;
        overflow: hidden;
        font-family: 'Share Tech Mono', monospace !important;
        opacity: 0;
        animation: delivDescCycle 18s ease-in-out infinite;
        animation-delay: calc(var(--d) * 3s);
    }
    @keyframes delivDescCycle {
        0%      { font-size: 0; max-height: 0; opacity: 0; margin-top: 0; }
        2%      { font-size: 0.95rem; max-height: 80px; opacity: 1; margin-top: 0.3rem; }
        14%     { font-size: 0.95rem; max-height: 80px; opacity: 1; margin-top: 0.3rem; }
        18%     { font-size: 0; max-height: 0; opacity: 0; margin-top: 0; }
        100%    { font-size: 0; max-height: 0; opacity: 0; margin-top: 0; }
    }

    /* ── Clickable deliverable card links ────────────── */
    a.deliv-link {
        display: block;
        text-decoration: none !important;
        cursor: pointer;
    }
    a.deliv-link:hover {
        opacity: 1 !important;
        border-color: #F97316 !important;
        background: rgba(249,115,22,0.12) !important;
        box-shadow: inset 3px 0 0 #F97316, 0 0 24px rgba(249,115,22,0.2) !important;
        transform: scale(1.04);
    }
    a.deliv-link:hover .deliv-card-name {
        color: #F97316 !important;
    }
    a.deliv-link:hover .deliv-card-desc {
        font-size: 0.95rem !important;
        max-height: 80px !important;
        opacity: 1 !important;
        margin-top: 0.3rem !important;
    }
    a.deliv-link:hover .deliv-card-step {
        font-size: 0.85rem !important;
        max-height: 40px !important;
        opacity: 1 !important;
        margin-top: 0.2rem !important;
    }

    /* ── Wizard step page links — full width clickable ─ */
    .wiz-link-done a {
        background: rgba(45,212,191,0.04) !important;
        border: 1px solid rgba(45,212,191,0.12) !important;
        border-radius: 0.5rem !important;
        padding: 0.7rem 1rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #2DD4BF !important;
        margin-bottom: 0.4rem !important;
        display: block !important;
    }
    .wiz-link-done a:hover {
        background: rgba(45,212,191,0.08) !important;
        border-color: #2DD4BF !important;
    }
    .wiz-link-pending a {
        background: transparent !important;
        border: 1px solid rgba(255,255,255,0.04) !important;
        border-radius: 0.4rem !important;
        padding: 0.45rem 1rem !important;
        font-size: 1rem !important;
        color: #5A6478 !important;
        opacity: 0.6;
        margin-bottom: 0.2rem !important;
        display: block !important;
    }
    .wiz-link-pending a:hover {
        opacity: 1;
        background: rgba(255,255,255,0.03) !important;
        border-color: rgba(255,255,255,0.10) !important;
    }

    /* ═══════════════════════════════════════════════════
       SIDEBAR MOCKUP — frosted white glass, full height
       ═══════════════════════════════════════════════════ */
    .sidebar-mockup {
        background: rgba(255,255,255,0.07);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 0.75rem;
        padding: 1.2rem 1.4rem 1.2rem 3rem;
        min-height: 520px;
        font-size: 1rem;
    }
    .sm-section {
        position: relative;
        padding: 0.6rem 0;
        opacity: 0.28;
        transition: opacity 0.35s ease, transform 0.35s ease;
    }
    .sm-section.active {
        opacity: 1;
        transform: scale(1.02);
    }
    .sm-callout {
        position: absolute; left: -2.2rem; top: 0.55rem;
        width: 26px; height: 26px; border-radius: 50%;
        background: rgba(255,255,255,0.12); color: #5A6478;
        font-size: 0.75rem; font-weight: 700;
        display: inline-flex; align-items: center; justify-content: center;
        transition: background 0.3s, color 0.3s;
    }
    .sm-section.active .sm-callout {
        background: #2DD4BF; color: #06080D;
        box-shadow: 0 0 10px rgba(45,212,191,0.5);
    }
    .sm-brand {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.78rem; color: #8B95A5;
        letter-spacing: 0.1em;
    }
    .sm-title { font-size: 1.1rem; font-weight: 700; color: #E8ECF1; }
    .sm-divider { border-top: 1px solid rgba(255,255,255,0.08); margin: 0.4rem 0; }
    .sm-label {
        font-size: 1rem; font-weight: 600; color: #E8ECF1;
        margin-bottom: 0.25rem;
    }
    .sm-bar {
        background: rgba(45,212,191,0.08); height: 6px;
        border-radius: 3px; margin-bottom: 0.2rem;
    }
    .sm-bar-fill {
        background: linear-gradient(135deg, #2DD4BF, #22D3EE);
        height: 100%; width: 28%; border-radius: 3px;
    }
    .sm-bar-text { font-size: 0.8rem; color: #5A6478; }
    .sm-step { padding: 0.2rem 0; color: #8B95A5; font-size: 0.95rem; }
    .sm-step.done { color: #5A6478; }
    .sm-step.current { color: #E8ECF1; font-weight: 600; }
    .sm-tip {
        background: rgba(45,212,191,0.06);
        border-left: 2px solid #2DD4BF;
        padding: 0.35rem 0.6rem;
        border-radius: 0 0.3rem 0.3rem 0;
        font-size: 0.88rem; color: #8B95A5;
    }

    /* ── Inline sidebar descriptions (beside each feature) ── */
    .sidebar-mockup.sm-inline {
        max-width: 800px;
        margin: 0 auto;
    }
    .sm-section-inline {
        display: flex;
        gap: 1.5rem;
        align-items: stretch;
        padding: 0.6rem 0;
    }
    .sm-section-content {
        flex: 0 0 240px;
        position: relative;
        padding: 0.5rem 0.6rem 0.5rem 2.2rem;
    }
    .sm-inline-desc {
        flex: 1;
        background: rgba(249,115,22,0.05);
        border-left: 3px solid #F97316;
        clip-path: polygon(0 0, 100% 0, 100% calc(100% - 6px), calc(100% - 6px) 100%, 0 100%);
        padding: 0.7rem 1rem;
        font-size: 0.95rem;
        line-height: 1.6;
        color: #C8D0DC;
    }
    .sm-inline-desc b { color: #E8ECF1 !important; }
    .sm-inline-title {
        display: block;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #F97316;
        margin-bottom: 0.25rem;
    }

    /* ── Explain annotations beside mockup (legacy) ─── */
    .sm-explain-item {
        display: flex; gap: 0.6rem; align-items: flex-start;
        margin-bottom: 0.7rem; font-size: 1.05rem; line-height: 1.6; color: #C8D0DC;
    }
    .sm-explain-item b { color: #E8ECF1 !important; }
    .sm-explain-num {
        flex-shrink: 0; width: 22px; height: 22px; border-radius: 50%;
        background: #2DD4BF; color: #06080D;
        font-size: 0.7rem; font-weight: 700;
        display: inline-flex; align-items: center; justify-content: center;
    }

    /* ═══════════════════════════════════════════════════
       CANVAS MOCKUP — for onboarding guide page
       ═══════════════════════════════════════════════════ */
    .canvas-mockup {
        background: rgba(45,212,191,0.03);
        border: 1px solid rgba(45,212,191,0.15);
        border-radius: 0.75rem;
        padding: 1.25rem;
        min-height: 380px;
        animation: canvasPulse 3s ease-in-out infinite;
    }

    /* ═══════════════════════════════════════════════════
       FLASHING ARROW — "start here" / "next step"
       ═══════════════════════════════════════════════════ */
    @keyframes flashArrow {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    .flash-arrow {
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.88rem;
        font-weight: 700;
        color: #2DD4BF !important;
        animation: flashArrow 1.2s ease-in-out infinite;
        text-shadow: 0 0 8px rgba(45,212,191,0.5);
    }

    /* ═══════════════════════════════════════════════════
       PAGE LINK STYLING — theme overrides
       ═══════════════════════════════════════════════════ */
    [data-testid="stPageLink"] a {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 0.5rem !important;
        color: #E8ECF1 !important;
        font-size: 1.05rem !important;
        padding: 0.4rem 0.8rem !important;
        text-decoration: none !important;
    }
    [data-testid="stPageLink"] a:hover {
        background: rgba(45,212,191,0.08) !important;
        border-color: #2DD4BF !important;
    }
    /* Sidebar page links — more compact */
    section[data-testid="stSidebar"] [data-testid="stPageLink"] a {
        background: transparent !important;
        border: none !important;
        padding: 0.2rem 0.4rem !important;
        font-size: 0.95rem !important;
    }
    section[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {
        background: rgba(45,212,191,0.08) !important;
        border-radius: 0.3rem;
    }

    /* ── Guide subtitle ───────────────────────────────── */
    .guide-subtitle {
        font-size: 1.1rem;
        color: #8B95A5;
        margin-bottom: 0.5rem;
    }
</style>
"""


def inject_custom_css():
    """Inject theme CSS."""
    st.markdown(_css(), unsafe_allow_html=True)


def step_header(step_num: int, title: str, subtitle: str):
    """Render a consistent step header with step badge."""
    st.markdown(
        f'<span class="step-badge">Step {step_num} of 7</span>',
        unsafe_allow_html=True,
    )
    st.header(title)
    st.caption(subtitle)
