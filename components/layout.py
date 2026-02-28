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

    /* ── Glass inputs ───────────────────────────────── */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 0.5rem !important;
        color: #E8ECF1 !important;
        font-size: 1.1rem !important;
        backdrop-filter: blur(8px);
    }
    .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus {
        border-color: #2DD4BF !important;
        box-shadow: 0 0 0 2px rgba(45,212,191,0.25) !important;
    }
    .stSelectbox [data-baseweb="select"], .stMultiSelect [data-baseweb="select"] {
        background: rgba(255,255,255,0.04) !important;
        border-color: rgba(255,255,255,0.10) !important;
    }
    .stSelectbox [data-baseweb="select"] > div, .stMultiSelect [data-baseweb="select"] > div {
        background: rgba(255,255,255,0.04) !important;
        color: #E8ECF1 !important;
    }

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
        border-radius: 0.75rem;
        padding: 1.25rem;
        min-height: 480px;
        animation: canvasPulse 3s ease-in-out infinite;
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
    }
    .canvas-panel .stDownloadButton button:hover { background: rgba(255,255,255,0.10) !important; }
    .canvas-panel .streamlit-expanderHeader,
    .canvas-panel .streamlit-expanderHeader p { background: rgba(255,255,255,0.04) !important; color: #E8ECF1 !important; }

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
        margin-bottom: 0.25rem;
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
       DASHBOARD — journey + deliverables
       ═══════════════════════════════════════════════════ */
    .journey-list { margin: 0.4rem 0; }
    .journey-item {
        display: flex;
        align-items: baseline;
        gap: 0.7rem;
        padding: 0.55rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        font-size: 1.1rem;
        line-height: 1.5;
    }
    .journey-item:last-child { border-bottom: none; }
    .journey-num {
        flex-shrink: 0;
        width: 28px; height: 28px;
        border-radius: 50%;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        color: #8B95A5 !important;
        display: inline-flex;
        align-items: center; justify-content: center;
        font-size: 0.8rem; font-weight: 600;
    }
    .journey-num.done {
        background: rgba(45,212,191,0.10);
        border-color: #2DD4BF;
        color: #2DD4BF !important;
    }
    .journey-name { font-weight: 600; min-width: 150px; color: #E8ECF1; font-size: 1.1rem; }
    .journey-desc { color: #8B95A5; font-size: 1.02rem; }
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
        border-radius: 0.75rem;
        padding: 1.2rem 1.5rem;
        text-align: center;
        flex: 1;
    }
    .landing-stat-card.before { border-color: rgba(239,68,68,0.3); }
    .landing-stat-card.after { border-color: rgba(45,212,191,0.3); }
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
    .landing-deliv-title {
        text-align: center;
        font-size: 1.15rem;
        font-weight: 600;
        color: #E8ECF1;
        margin: 1.5rem 0 0.6rem 0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .landing-deliv-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        justify-content: center;
        margin-bottom: 1.5rem;
    }
    .landing-deliv-chip {
        background: rgba(45,212,191,0.08);
        border: 1px solid rgba(45,212,191,0.2);
        border-radius: 2rem;
        padding: 0.35rem 0.9rem;
        font-size: 0.92rem;
        color: #2DD4BF;
        font-family: 'Share Tech Mono', monospace !important;
    }

    /* ═══════════════════════════════════════════════════
       SIDEBAR MOCKUP — for onboarding guide page
       ═══════════════════════════════════════════════════ */
    .sidebar-mockup {
        background: rgba(8,12,22,0.85);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 0.75rem;
        padding: 1rem 1rem 1rem 2.4rem;
        max-width: 340px;
        font-size: 0.92rem;
    }
    .sm-section { position: relative; padding: 0.4rem 0; }
    .sm-callout {
        position: absolute; left: -1.8rem; top: 0.4rem;
        width: 22px; height: 22px; border-radius: 50%;
        background: #2DD4BF; color: #06080D;
        font-size: 0.7rem; font-weight: 700;
        display: inline-flex; align-items: center; justify-content: center;
    }
    .sm-brand { font-family: 'Share Tech Mono', monospace !important; font-size: 0.68rem; color: #5A6478; letter-spacing: 0.1em; }
    .sm-title { font-size: 1.05rem; font-weight: 700; color: #E8ECF1; }
    .sm-divider { border-top: 1px solid rgba(255,255,255,0.08); margin: 0.35rem 0; }
    .sm-label { font-size: 0.88rem; font-weight: 600; color: #E8ECF1; margin-bottom: 0.2rem; }
    .sm-bar { background: rgba(45,212,191,0.08); height: 5px; border-radius: 3px; margin-bottom: 0.15rem; }
    .sm-bar-fill { background: linear-gradient(135deg, #2DD4BF, #22D3EE); height: 100%; width: 28%; border-radius: 3px; }
    .sm-bar-text { font-size: 0.72rem; color: #5A6478; }
    .sm-step { padding: 0.15rem 0; color: #8B95A5; font-size: 0.85rem; }
    .sm-step.done { color: #5A6478; }
    .sm-step.current { color: #E8ECF1; font-weight: 600; }
    .sm-tip { background: rgba(45,212,191,0.06); border-left: 2px solid #2DD4BF; padding: 0.3rem 0.5rem; border-radius: 0 0.3rem 0.3rem 0; font-size: 0.78rem; color: #8B95A5; }

    /* ── Explain annotations beside mockup ──────────── */
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
