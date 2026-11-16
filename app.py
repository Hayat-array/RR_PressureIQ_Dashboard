import os
from pathlib import Path
import math
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="RR PressureIQ 2027 | Auction Intelligence War Room",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
ENRICHED_PATH = DATA_DIR / "RR_PressureIQ_Enriched_Candidates.csv"
FULL_PATH = DATA_DIR / "RR_PressureIQ_Full_Candidate_Rankings.csv"
TOP_PATH = DATA_DIR / "SupeRR_Round1_Top10_Rankings.csv"
REPORT_PATH = DATA_DIR / "SupeRR_Round1_Methodology_Report.pdf"

# -----------------------------------------------------------------------------
# LUXURY WAR ROOM DESIGN SYSTEM (Daily UI / Dribbble Executive Standard)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

:root {
    --rr-pink: #E80071;
    --rr-pink-glow: rgba(232, 0, 113, 0.28);
    --rr-pink-light: #FF2E93;
    --rr-navy: #0A1128;
    --rr-dark: #070B14;
    --rr-card-bg: rgba(13, 20, 36, 0.75);
    --rr-card-border: rgba(255, 255, 255, 0.08);
    --rr-gold: #F59E0B;
    --rr-emerald: #10B981;
    --rr-cyan: #06B6D4;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background: radial-gradient(circle at 15% 0%, #1a0b2e 0%, #080c17 45%, #050811 100%);
    color: #F3F4F6;
}

[data-testid="stHeader"] {
    background: rgba(7, 11, 20, 0.85);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 3.5rem;
    max-width: 1560px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0e1424 0%, #080c16 100%);
    border-right: 1px solid rgba(232, 0, 113, 0.15);
}

/* Hero Section */
.hero-card {
    background: linear-gradient(135deg, rgba(35, 12, 54, 0.9) 0%, rgba(13, 19, 39, 0.95) 55%, rgba(232, 0, 113, 0.18) 100%);
    border: 1px solid rgba(232, 0, 113, 0.35);
    border-radius: 20px;
    padding: 26px 32px;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    position: relative;
    overflow: hidden;
    margin-bottom: 22px;
}

.hero-card::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 320px;
    height: 320px;
    background: radial-gradient(circle, rgba(232, 0, 113, 0.25) 0%, transparent 70%);
    pointer-events: none;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(232, 0, 113, 0.15);
    border: 1px solid rgba(232, 0, 113, 0.4);
    color: #FF70B8;
    padding: 5px 14px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.35rem;
    font-weight: 700;
    color: #FFFFFF;
    margin: 8px 0 6px 0;
    letter-spacing: -0.03em;
    line-height: 1.15;
}

.hero-subtitle {
    color: #CBD5E1;
    font-size: 0.98rem;
    max-width: 880px;
    margin: 0;
    line-height: 1.5;
}

/* Metric Cards */
.metric-glass {
    background: linear-gradient(145deg, rgba(20, 27, 45, 0.75), rgba(12, 17, 30, 0.85));
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 16px 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.metric-glass:hover {
    border-color: rgba(232, 0, 113, 0.4);
    transform: translateY(-2px);
}

.metric-label {
    font-size: 0.75rem;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
    margin-bottom: 4px;
}

.metric-val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: #FFFFFF;
}

.metric-sub {
    font-size: 0.76rem;
    color: #38BDF8;
    margin-top: 2px;
}

/* Tactical Cards */
.scout-card {
    background: linear-gradient(160deg, rgba(21, 29, 50, 0.8) 0%, rgba(13, 18, 33, 0.9) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
}

.scout-card-highlight {
    border: 1px solid rgba(232, 0, 113, 0.45);
    box-shadow: 0 12px 30px rgba(232, 0, 113, 0.12);
}

.pill-tag {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    margin-right: 6px;
    margin-bottom: 4px;
}

.pill-marquee { background: rgba(232, 0, 113, 0.2); color: #FF70B8; border: 1px solid rgba(232, 0, 113, 0.5); }
.pill-value { background: rgba(16, 185, 129, 0.2); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.4); }
.pill-punt { background: rgba(245, 158, 11, 0.2); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.4); }
.pill-trap { background: rgba(239, 68, 68, 0.2); color: #F87171; border: 1px solid rgba(239, 68, 68, 0.4); }
.pill-overseas { background: rgba(99, 102, 241, 0.2); color: #A5B4FC; border: 1px solid rgba(99, 102, 241, 0.4); }
.pill-domestic { background: rgba(14, 165, 233, 0.2); color: #7DD3FC; border: 1px solid rgba(14, 165, 233, 0.4); }

/* Tabs Styling */
div[data-testid="stTabs"] button {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.94rem;
    font-weight: 600;
    color: #94A3B8;
    padding: 10px 18px;
    transition: all 0.2s ease;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #FF70B8 !important;
    border-bottom: 3px solid #E80071 !important;
    background: rgba(232, 0, 113, 0.08);
    border-radius: 8px 8px 0 0;
}

/* Buttons */
.stButton>button, .stDownloadButton>button {
    background: linear-gradient(135deg, #E80071 0%, #B80059 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 112, 184, 0.3) !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 9px 20px !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 6px 18px rgba(232, 0, 113, 0.35) !important;
    transition: all 0.2s ease !important;
}

.stButton>button:hover, .stDownloadButton>button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(232, 0, 113, 0.55) !important;
    border-color: #FFA3D0 !important;
}

/* Custom Dataframe container */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    overflow: hidden;
    background: rgba(13, 19, 34, 0.6);
}

.badge-flag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.82rem;
    color: #E2E8F0;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# DATA LOADING & ADAPTIVE SCHEMA INGESTION ENGINE
# -----------------------------------------------------------------------------
@st.cache_data
def load_default_dataset():
    """Loads the pre-computed enriched candidates dataset with fallback."""
    if ENRICHED_PATH.exists():
        df = pd.read_csv(ENRICHED_PATH)
    elif FULL_PATH.exists():
        df = pd.read_csv(FULL_PATH, encoding="utf-8-sig")
        df.columns = [c.replace("\ufeff", "") for c in df.columns]
    else:
        st.error("Missing candidate dataset files in data/ directory.")
        st.stop()
    
    df.columns = [c.strip().replace("\ufeff", "") for c in df.columns]
    return df

def process_uploaded_csv(uploaded_file):
    """
    Intelligent Data Pack Processor:
    Auto-detects and normalizes uploaded domestic league or Unstop competition CSVs.
    """
    try:
        raw_df = pd.read_csv(uploaded_file, encoding="utf-8-sig")
        raw_df.columns = [c.strip().replace("\ufeff", "").lower().replace(" ", "_") for c in raw_df.columns]
        
        col_map = {
            "player": "player_name",
            "name": "player_name",
            "role": "category",
            "type": "category",
            "score": "model_score",
            "sr": "pressure_strike_rate_or_economy",
            "economy": "pressure_strike_rate_or_economy",
            "balls": "pressure_balls",
            "matches": "pressure_matches",
            "runs": "pressure_runs",
            "wickets": "pressure_dismissals_or_wickets",
            "outs": "pressure_dismissals_or_wickets",
            "baseline": "baseline_strike_rate_or_economy",
            "diff": "change_vs_baseline",
            "delta": "change_vs_baseline",
            "consistency": "consistency_pct"
        }
        
        for k, v in col_map.items():
            for c in raw_df.columns:
                if k in c and v not in raw_df.columns:
                    raw_df.rename(columns={c: v}, inplace=True)
                    break
        
        if "player_name" not in raw_df.columns:
            raw_df["player_name"] = [f"Player {i+1}" for i in range(len(raw_df))]
        if "category" not in raw_df.columns:
            raw_df["category"] = "Batter"
        if "pressure_balls" not in raw_df.columns:
            raw_df["pressure_balls"] = 100
        if "pressure_matches" not in raw_df.columns:
            raw_df["pressure_matches"] = 10
        if "pressure_strike_rate_or_economy" not in raw_df.columns:
            raw_df["pressure_strike_rate_or_economy"] = 140.0
        if "baseline_strike_rate_or_economy" not in raw_df.columns:
            raw_df["baseline_strike_rate_or_economy"] = 125.0
        if "change_vs_baseline" not in raw_df.columns:
            raw_df["change_vs_baseline"] = raw_df["pressure_strike_rate_or_economy"] - raw_df["baseline_strike_rate_or_economy"]
        if "consistency_pct" not in raw_df.columns:
            raw_df["consistency_pct"] = 70.0
        if "model_score" not in raw_df.columns:
            raw_df["model_score"] = 0.75
        if "is_overseas" not in raw_df.columns:
            raw_df["is_overseas"] = "No"
        if "country" not in raw_df.columns:
            raw_df["country"] = "India"
        if "estimated_price_cr" not in raw_df.columns:
            raw_df["estimated_price_cr"] = 4.0
        if "rr_tactical_fit" not in raw_df.columns:
            raw_df["rr_tactical_fit"] = 80
        if "auction_tier" not in raw_df.columns:
            raw_df["auction_tier"] = "Tier 2: High-Value Moneyball"
        if "risk_score" not in raw_df.columns:
            raw_df["risk_score"] = 25
            
        return raw_df, True, "Successfully ingested custom competition data pack!"
    except Exception as e:
        return None, False, f"Error processing uploaded CSV: {str(e)}"

# Load Primary Dataset
default_df = load_default_dataset()


# -----------------------------------------------------------------------------
# SIDEBAR CONTROLS & REAL DATA PACK INGESTION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
        <span style="font-size:1.8rem;">👑</span>
        <div>
            <div style="font-weight:800; font-size:1.05rem; color:#FFFFFF; letter-spacing:-0.02em;">RAJASTHAN ROYALS</div>
            <div style="font-size:0.72rem; color:#FF70B8; font-weight:700; letter-spacing:0.12em;">PRESSURE-IQ WAR ROOM 2027</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Data Pack Selection (Real Data Integration)
    st.markdown("### 📂 Data Ingestion Mode")
    data_source_mode = st.radio(
        "Active Data Pool",
        ["Verified 2027 War Room (226 Players)", "Upload Custom Unstop CSV"],
        index=0,
        help="Switch to 'Upload Custom Unstop CSV' to ingest the raw competition brief data pack live."
    )
    
    active_df = default_df.copy()
    if data_source_mode == "Upload Custom Unstop CSV":
        uploaded_file = st.file_uploader(
            "Drop Unstop Data Pack / CSV",
            type=["csv"],
            help="Upload official Unstop or domestic league CSV. The engine will auto-map columns."
        )
        if uploaded_file is not None:
            processed_df, success, msg = process_uploaded_csv(uploaded_file)
            if success:
                active_df = processed_df
                st.success(msg)
            else:
                st.error(msg)
        else:
            st.info("Awaiting file upload. Displaying verified candidate pool.")
    
    st.markdown("---")
    
    # Global Scouting Filters
    st.markdown("### 🎛️ Strategic Filters")
    role_filter = st.radio("Primary Focus Role", ["Batters", "Bowlers", "All Candidates"], horizontal=True)
    
    origin_filter = st.selectbox("Player Quota / Origin", ["All Players", "Domestic (Indian) Only", "Overseas Only"])
    
    evidence_scope = st.selectbox(
        "Competition Evidence",
        ["All Evidence", "IPL Pressure Evidence Required (>0)", "T20I Evidence (>0)", "Multi-Competition Validated"]
    )
    
    tier_filter = st.selectbox(
        "Auction Priority Tier",
        ["All Tiers", "Tier 1: Marquee Priority", "Tier 2: High-Value Moneyball", "Tier 3: High-Upside Punt", "Tier 4: Caution / Trap Risk"]
    )
    
    st.markdown("### 🔍 Sample Size Gates")
    min_balls = st.slider("Min Pressure Balls", 0, int(active_df["pressure_balls"].max()), 40, step=10)
    min_matches = st.slider("Min Pressure Matches", 1, int(active_df["pressure_matches"].max()), 5)
    
    st.divider()
    st.caption("RR PressureIQ · Algorithmic Franchise War Room · Designed for Rajasthan Royals SupeRR Selector Round 1")


# -----------------------------------------------------------------------------
# FILTERING ENGINE
# -----------------------------------------------------------------------------
df = active_df.copy()

# Category Filter
if role_filter == "Batters":
    df = df[df["category"].str.lower() == "batter"]
elif role_filter == "Bowlers":
    df = df[df["category"].str.lower() == "bowler"]

# Origin Filter
if "is_overseas" in df.columns:
    if origin_filter == "Domestic (Indian) Only":
        df = df[df["is_overseas"] == "No"]
    elif origin_filter == "Overseas Only":
        df = df[df["is_overseas"] == "Yes"]

# Evidence Filter
if "IPL_pressure_balls" in df.columns and "T20I_pressure_balls" in df.columns:
    if evidence_scope == "IPL Pressure Evidence Required (>0)":
        df = df[df["IPL_pressure_balls"] > 0]
    elif evidence_scope == "T20I Evidence (>0)":
        df = df[df["T20I_pressure_balls"] > 0]
    elif evidence_scope == "Multi-Competition Validated":
        df = df[(df["IPL_pressure_balls"] > 0) & (df["T20I_pressure_balls"] > 0)]

# Tier Filter
if tier_filter != "All Tiers" and "auction_tier" in df.columns:
    df = df[df["auction_tier"] == tier_filter]

# Sample size gates
df = df[(df["pressure_balls"] >= min_balls) & (df["pressure_matches"] >= min_matches)]


# -----------------------------------------------------------------------------
# TOP HERO BANNER & EXECUTIVE KPIS
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-card">
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
        <div>
            <div class="hero-badge">⚡ RAJASTHAN ROYALS · SUPER-R SELECTOR · ROUND 1</div>
            <div class="hero-title">PressureIQ <span style="color:#FF70B8;">2027</span> War Room</div>
            <p class="hero-subtitle">
                High-leverage analytical decision engine identifying the most reliable clutch match-winners for Rajasthan Royals at the IPL 2027 mega-auction.
            </p>
        </div>
        <div style="text-align:right; align-self:center;">
            <div style="font-size:0.75rem; color:#94A3B8; text-transform:uppercase; letter-spacing:0.1em; font-weight:700;">AUCTION PURSE CAP</div>
            <div style="font-family:'Space Grotesk',sans-serif; font-size:1.9rem; font-weight:700; color:#F59E0B;">₹100.00 Cr</div>
            <div style="font-size:0.75rem; color:#10B981; font-weight:600;">MAX 8 OVERSEAS SLOTS</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Executive KPI Strip
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""
    <div class="metric-glass">
        <div class="metric-label">Filtered Prospects</div>
        <div class="metric-val">{len(df):,}</div>
        <div class="metric-sub">Across {df['country'].nunique() if 'country' in df.columns else 'multiple'} nations</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    marquee_count = len(df[df["auction_tier"].str.contains("Marquee", na=False)]) if "auction_tier" in df.columns else 0
    st.markdown(f"""
    <div class="metric-glass">
        <div class="metric-label">Tier 1 Marquee Targets</div>
        <div class="metric-val" style="color:#FF70B8;">{marquee_count}</div>
        <div class="metric-sub">Elite clutch match-winners</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    moneyball_count = len(df[df["auction_tier"].str.contains("Moneyball", na=False)]) if "auction_tier" in df.columns else 0
    st.markdown(f"""
    <div class="metric-glass">
        <div class="metric-label">Moneyball Value Buys</div>
        <div class="metric-val" style="color:#10B981;">{moneyball_count}</div>
        <div class="metric-sub">High delta · Low auction spend</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    tot_pressure_balls = int(df["pressure_balls"].sum())
    st.markdown(f"""
    <div class="metric-glass">
        <div class="metric-label">Pressure Deliveries</div>
        <div class="metric-val">{tot_pressure_balls:,}</div>
        <div class="metric-sub">Clutch high-leverage balls</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    avg_score = df["model_score"].mean() if len(df) else 0.0
    st.markdown(f"""
    <div class="metric-glass">
        <div class="metric-label">Mean PressureIQ Score</div>
        <div class="metric-val" style="color:#38BDF8;">{avg_score:.3f}</div>
        <div class="metric-sub">Bayesian shrunk index</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")


# -----------------------------------------------------------------------------
# MAIN WAR ROOM NAVIGATION TABS
# -----------------------------------------------------------------------------
tabs = st.tabs([
    "🏆 Candidate Leaderboard",
    "🧍 360° Player Dossier",
    "⚖️ Multi-Player Comparison",
    "🎯 Auction Intelligence Board",
    "🧩 Squad Combination Simulator",
    "⚠️ Player Risk Matrix",
    "📘 The Winning Methodology & Pitch"
])


# =============================================================================
# TAB 1: CANDIDATE LEADERBOARD & SPOTLIGHT
# =============================================================================
with tabs[0]:
    st.markdown("<div style='font-size:1.15rem; font-weight:700; color:#FFFFFF; margin-bottom:8px;'>👑 Top Pressure Titans in Active Pool</div>", unsafe_allow_html=True)
    
    top_candidates = df.sort_values("model_score", ascending=False).head(3)
    if len(top_candidates) >= 3:
        spot_cols = st.columns(3)
        for idx, (_, cand) in enumerate(top_candidates.iterrows()):
            with spot_cols[idx]:
                tier_badge = cand.get("auction_tier", "Target")
                badge_class = "pill-marquee" if "Marquee" in tier_badge else ("pill-value" if "Moneyball" in tier_badge else "pill-punt")
                origin_badge = "pill-overseas" if cand.get("is_overseas") == "Yes" else "pill-domestic"
                
                st.markdown(f"""
                <div class="scout-card scout-card-highlight">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div>
                            <span class="pill-tag {badge_class}">{tier_badge}</span>
                            <span class="pill-tag {origin_badge}">{cand.get('country', 'Domestic')}</span>
                            <div style="font-size:1.35rem; font-weight:800; color:#FFFFFF; margin-top:6px;">{cand['player_name']}</div>
                            <div style="font-size:0.8rem; color:#94A3B8;">{cand['category']} · {cand.get('skill_specialization', 'Core Specialist')}</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:0.7rem; color:#94A3B8; font-weight:700;">PRESSURE-IQ</div>
                            <div style="font-family:'Space Grotesk',sans-serif; font-size:1.8rem; font-weight:800; color:#FF70B8;">{cand['model_score']:.3f}</div>
                        </div>
                    </div>
                    <hr style="border-color:rgba(255,255,255,0.06); margin:12px 0;">
                    <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; text-align:center;">
                        <div>
                            <div style="font-size:0.68rem; color:#94A3B8;">PRESSURE OUTPUT</div>
                            <div style="font-weight:700; color:#38BDF8; font-size:1.05rem;">{cand['pressure_strike_rate_or_economy']:.1f}</div>
                            <div style="font-size:0.65rem; color:#64748B;">{'SR' if cand['category'].lower()=='batter' else 'Econ'}</div>
                        </div>
                        <div>
                            <div style="font-size:0.68rem; color:#94A3B8;">UPLIFT VS BASE</div>
                            <div style="font-weight:700; color:#{ '34D399' if (cand['change_vs_baseline']>0 if cand['category'].lower()=='batter' else cand['change_vs_baseline']<0) else 'F87171'}; font-size:1.05rem;">
                                {cand['change_vs_baseline']:+.1f}
                            </div>
                            <div style="font-size:0.65rem; color:#64748B;">Delta</div>
                        </div>
                        <div>
                            <div style="font-size:0.68rem; color:#94A3B8;">CONSISTENCY</div>
                            <div style="font-weight:700; color:#FBBF24; font-size:1.05rem;">{cand['consistency_pct']:.0f}%</div>
                            <div style="font-size:0.65rem; color:#64748B;">Match Rate</div>
                        </div>
                    </div>
                    <div style="margin-top:12px; font-size:0.78rem; color:#CBD5E1; background:rgba(0,0,0,0.25); padding:8px 10px; border-radius:8px;">
                        🎯 <b>RR Fit:</b> {cand.get('scout_verdict', 'Prime target under pressure.')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.write("")
    
    # Visual Analytics & Filterable Table
    col_chart, col_table = st.columns([1, 1.25], gap="large")
    
    with col_chart:
        st.markdown("<div style='font-size:1rem; font-weight:700; color:#FFFFFF; margin-bottom:4px;'>📊 Clutch Elevation: Output vs Baseline Delta</div>", unsafe_allow_html=True)
        if len(df):
            scatter_fig = px.scatter(
                df,
                x="change_vs_baseline",
                y="pressure_strike_rate_or_economy",
                size="pressure_balls",
                color="model_score",
                hover_name="player_name",
                hover_data=["country", "pressure_matches", "consistency_pct", "auction_tier"],
                color_continuous_scale=[[0, "#4C1D95"], [0.5, "#E80071"], [1, "#FF70B8"]],
                labels={
                    "change_vs_baseline": "Elevation over Baseline (Delta)",
                    "pressure_strike_rate_or_economy": "Pressure Output (SR / Economy)",
                    "model_score": "PressureIQ Score"
                }
            )
            scatter_fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(13, 20, 36, 0.4)",
                height=480,
                margin=dict(l=10, r=10, t=10, b=10),
                coloraxis_colorbar=dict(title="Score")
            )
            st.plotly_chart(scatter_fig, use_container_width=True)
        else:
            st.info("No players meet the selected filters.")
            
    with col_table:
        st.markdown("<div style='font-size:1rem; font-weight:700; color:#FFFFFF; margin-bottom:4px;'>📋 Filtered Candidate War Room Roster</div>", unsafe_allow_html=True)
        search_query = st.text_input("🔍 Search Candidate Name", placeholder="e.g. Shashank Singh, Pathirana, Donovan...", key="search_roster")
        
        roster_view = df.copy()
        if search_query:
            roster_view = roster_view[roster_view["player_name"].str.contains(search_query, case=False, na=False)]
            
        display_cols = [
            "player_name", "category", "country", "model_score", 
            "pressure_strike_rate_or_economy", "change_vs_baseline", 
            "consistency_pct", "pressure_balls", "pressure_matches", "auction_tier"
        ]
        display_cols = [c for c in display_cols if c in roster_view.columns]
        
        styled_roster = roster_view[display_cols].sort_values("model_score", ascending=False).rename(columns={
            "player_name": "Player",
            "category": "Role",
            "country": "Nation",
            "model_score": "Score",
            "pressure_strike_rate_or_economy": "Pressure Output",
            "change_vs_baseline": "Delta vs Base",
            "consistency_pct": "Consistency %",
            "pressure_balls": "Balls",
            "pressure_matches": "Matches",
            "auction_tier": "Auction Tier"
        })
        
        st.dataframe(styled_roster, use_container_width=True, hide_index=True, height=430)
        
        st.download_button(
            "⬇️ Export Filtered Roster CSV",
            roster_view.to_csv(index=False).encode("utf-8"),
            "RR_PressureIQ_Filtered_Candidates.csv",
            "text/csv"
        )


# =============================================================================
# TAB 2: 360° INTERACTIVE PLAYER DOSSIER
# =============================================================================
with tabs[1]:
    st.markdown("<div style='font-size:1.15rem; font-weight:700; color:#FFFFFF; margin-bottom:12px;'>🧍 Individual Scouting Dossier & Pressure DNA</div>", unsafe_allow_html=True)
    
    player_list = sorted(active_df["player_name"].unique().tolist())
    selected_player = st.selectbox("Select Player to Inspect", player_list, index=0)
    
    p_data = active_df[active_df["player_name"] == selected_player].iloc[0]
    
    role_type = p_data.get("category", "Player")
    country_name = p_data.get("country", "India")
    is_os = "Overseas" if p_data.get("is_overseas") == "Yes" else "Domestic (India)"
    est_price = p_data.get("estimated_price_cr", 4.0)
    tactical_fit = p_data.get("rr_tactical_fit", 85)
    
    st.markdown(f"""
    <div class="scout-card" style="background:linear-gradient(135deg, rgba(28,16,48,0.85) 0%, rgba(13,20,38,0.92) 100%); border:1px solid rgba(232,0,113,0.3);">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px;">
            <div>
                <span class="pill-tag pill-marquee">{p_data.get('auction_tier', 'Target')}</span>
                <span class="pill-tag pill-overseas">{is_os}</span>
                <span class="pill-tag pill-value">{p_data.get('phase_specialization', 'Multi-Phase')}</span>
                <h1 style="font-family:'Space Grotesk',sans-serif; color:#FFFFFF; font-size:2.4rem; margin:8px 0 4px 0; font-weight:800;">
                    {p_data['player_name']}
                </h1>
                <div style="font-size:0.95rem; color:#CBD5E1;">
                    <b>{country_name}</b> · {role_type} · {p_data.get('skill_specialization', 'Core Talent')} · {p_data.get('batting_style', 'RHB')} / {p_data.get('bowling_style', 'Right-arm')}
                </div>
            </div>
            <div style="display:flex; gap:20px; align-items:center;">
                <div style="text-align:right;">
                    <div style="font-size:0.75rem; color:#94A3B8; text-transform:uppercase; font-weight:700;">EST. AUCTION PRICE</div>
                    <div style="font-family:'Space Grotesk',sans-serif; font-size:1.85rem; font-weight:800; color:#F59E0B;">₹{float(est_price):.1f} Cr</div>
                    <div style="font-size:0.72rem; color:#10B981;">Target Bidding Bracket</div>
                </div>
                <div style="text-align:right; border-left:1px solid rgba(255,255,255,0.1); padding-left:20px;">
                    <div style="font-size:0.75rem; color:#94A3B8; text-transform:uppercase; font-weight:700;">RR TACTICAL FIT</div>
                    <div style="font-family:'Space Grotesk',sans-serif; font-size:1.85rem; font-weight:800; color:#FF70B8;">{tactical_fit}/100</div>
                    <div style="font-size:0.72rem; color:#38BDF8;">Franchise Synergy</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_dna, col_compare, col_memo = st.columns([1, 1, 1.1], gap="medium")
    
    with col_dna:
        st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#FFFFFF; margin-bottom:4px;'>🕸️ 6-Axis Pressure DNA Radar</div>", unsafe_allow_html=True)
        
        r_output = float(p_data.get("radar_output", 75))
        r_delta = float(p_data.get("radar_delta", 70))
        r_sample = float(p_data.get("radar_sample", 65))
        r_consist = float(p_data.get("radar_consistency", p_data["consistency_pct"]))
        r_ipl = float(p_data.get("radar_ipl", 60))
        r_synergy = float(p_data.get("radar_synergy", tactical_fit))
        
        radar_categories = ["Clutch Output", "Baseline Uplift", "Sample Depth", "Match Consistency", "IPL Big Stage", "RR Synergy"]
        radar_values = [r_output, r_delta, r_sample, r_consist, r_ipl, r_synergy]
        radar_values.append(radar_values[0])
        radar_cats = radar_categories + [radar_categories[0]]
        
        radar_fig = go.Figure()
        radar_fig.add_trace(go.Scatterpolar(
            r=radar_values,
            theta=radar_cats,
            fill='toself',
            fillcolor='rgba(232, 0, 113, 0.25)',
            line=dict(color='#FF70B8', width=2.5),
            name=selected_player
        ))
        radar_fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, linecolor="rgba(255,255,255,0.1)"),
                angularaxis=dict(linecolor="rgba(255,255,255,0.1)", tickfont=dict(size=10, color="#CBD5E1")),
                bgcolor="rgba(0,0,0,0)"
            ),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            height=340,
            margin=dict(t=25, b=25, l=35, r=35),
            showlegend=False
        )
        st.plotly_chart(radar_fig, use_container_width=True)
        
    with col_compare:
        st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#FFFFFF; margin-bottom:4px;'>📊 Pressure vs Personal Baseline</div>", unsafe_allow_html=True)
        
        base_val = float(p_data["baseline_strike_rate_or_economy"])
        press_val = float(p_data["pressure_strike_rate_or_economy"])
        metric_name = "Strike Rate" if role_type.lower() == "batter" else "Economy Rate"
        
        bar_fig = go.Figure(data=[
            go.Bar(
                x=["Own Non-Pressure Baseline", "High-Pressure Performance"],
                y=[base_val, press_val],
                marker_color=["#475569", "#E80071"],
                text=[f"{base_val:.2f}", f"{press_val:.2f}"],
                textposition="outside"
            )
        ])
        bar_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=340,
            margin=dict(t=30, b=20, l=10, r=10),
            yaxis_title=metric_name,
            showlegend=False
        )
        st.plotly_chart(bar_fig, use_container_width=True)
        
    with col_memo:
        st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#FFFFFF; margin-bottom:4px;'>📝 Scout's Tactical Memo</div>", unsafe_allow_html=True)
        
        verdict = p_data.get("scout_verdict", "Highly impactful option under pressure.")
        role_target = p_data.get("rr_role_target", "Core Match Winner")
        ipl_balls = int(p_data.get("IPL_pressure_balls", 0))
        t20i_balls = int(p_data.get("T20I_pressure_balls", 0))
        
        st.markdown(f"""
        <div class="scout-card" style="padding:16px;">
            <div style="font-size:0.75rem; color:#38BDF8; font-weight:700; letter-spacing:0.08em; text-transform:uppercase;">EXECUTIVE EVALUATION</div>
            <div style="font-size:0.98rem; color:#FFFFFF; font-weight:600; margin:6px 0 10px 0;">{verdict}</div>
            
            <div style="background:rgba(255,255,255,0.04); padding:10px; border-radius:8px; margin-bottom:10px;">
                <div style="font-size:0.72rem; color:#94A3B8;">ASSIGNED TACTICAL ROLE</div>
                <div style="font-size:0.9rem; font-weight:700; color:#FF70B8;">{role_target}</div>
            </div>
            
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                <div style="background:rgba(255,255,255,0.04); padding:8px; border-radius:8px;">
                    <div style="font-size:0.7rem; color:#94A3B8;">IPL EVIDENCE</div>
                    <div style="font-weight:700; color:#FFFFFF; font-size:1.1rem;">{ipl_balls} <span style="font-size:0.7rem; color:#64748B;">balls</span></div>
                </div>
                <div style="background:rgba(255,255,255,0.04); padding:8px; border-radius:8px;">
                    <div style="font-size:0.7rem; color:#94A3B8;">T20I EVIDENCE</div>
                    <div style="font-weight:700; color:#FFFFFF; font-size:1.1rem;">{t20i_balls} <span style="font-size:0.7rem; color:#64748B;">balls</span></div>
                </div>
            </div>
            
            <div style="margin-top:12px; font-size:0.75rem; color:#94A3B8; border-top:1px solid rgba(255,255,255,0.06); padding-top:8px;">
                ⚠️ <b>Risk Assessment:</b> {'Low risk proven commodity.' if ipl_balls >= 100 else 'Sample caution: verify domestic-to-IPL pace transferability.'}
            </div>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# TAB 3: MULTI-PLAYER COMPARISON STUDIO
# =============================================================================
with tabs[2]:
    st.markdown("<div style='font-size:1.15rem; font-weight:700; color:#FFFFFF; margin-bottom:4px;'>⚖️ Head-to-Head Player Comparison Studio</div>", unsafe_allow_html=True)
    st.caption("Compare up to 4 candidates side-by-side across normalized Pressure DNA, delta elevation, and auction value.")
    
    comp_pool = active_df.sort_values("model_score", ascending=False)["player_name"].tolist()
    default_picks = comp_pool[:min(2, len(comp_pool))]
    selected_compare = st.multiselect("Select Candidates to Compare (Max 4)", comp_pool, default=default_picks, max_selections=4)
    
    if len(selected_compare) >= 2:
        comp_df = active_df[active_df["player_name"].isin(selected_compare)].copy()
        
        c_left, c_right = st.columns([1.1, 1], gap="large")
        
        with c_left:
            st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#FFFFFF; margin-bottom:4px;'>🕸️ Multi-Candidate Pressure DNA Radar Overlay</div>", unsafe_allow_html=True)
            
            multi_radar = go.Figure()
            colors = ["#E80071", "#06B6D4", "#F59E0B", "#10B981"]
            
            radar_categories = ["Clutch Output", "Baseline Uplift", "Sample Depth", "Consistency", "IPL Big Stage", "RR Synergy"]
            radar_cats = radar_categories + [radar_categories[0]]
            
            for idx, (_, c_row) in enumerate(comp_df.iterrows()):
                r_vals = [
                    float(c_row.get("radar_output", 75)),
                    float(c_row.get("radar_delta", 70)),
                    float(c_row.get("radar_sample", 65)),
                    float(c_row.get("radar_consistency", c_row["consistency_pct"])),
                    float(c_row.get("radar_ipl", 60)),
                    float(c_row.get("radar_synergy", 80))
                ]
                r_vals.append(r_vals[0])
                
                multi_radar.add_trace(go.Scatterpolar(
                    r=r_vals,
                    theta=radar_cats,
                    fill='toself',
                    fillcolor=f'rgba{tuple(list(int(colors[idx % len(colors)].lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + [0.15])}',
                    line=dict(color=colors[idx % len(colors)], width=2.5),
                    name=c_row["player_name"]
                ))
                
            multi_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, linecolor="rgba(255,255,255,0.1)"),
                    angularaxis=dict(linecolor="rgba(255,255,255,0.1)", tickfont=dict(size=10, color="#CBD5E1")),
                    bgcolor="rgba(0,0,0,0)"
                ),
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                height=380,
                margin=dict(t=30, b=25, l=35, r=35),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(multi_radar, use_container_width=True)
            
        with c_right:
            st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#FFFFFF; margin-bottom:4px;'>📊 Comparative Metric Duel</div>", unsafe_allow_html=True)
            
            duel_metrics = []
            for _, r in comp_df.iterrows():
                duel_metrics.append({
                    "Player": r["player_name"],
                    "Role": r["category"],
                    "Origin": r.get("country", "Domestic"),
                    "PressureIQ": f"{r['model_score']:.3f}",
                    "Output": f"{r['pressure_strike_rate_or_economy']:.1f}",
                    "Baseline Delta": f"{r['change_vs_baseline']:+.1f}",
                    "Consistency": f"{r['consistency_pct']:.0f}%",
                    "Pressure Balls": int(r["pressure_balls"]),
                    "Est. Price": f"₹{float(r.get('estimated_price_cr', 4.0)):.1f} Cr"
                })
            
            st.dataframe(pd.DataFrame(duel_metrics), use_container_width=True, hide_index=True)
            
            best_pick = comp_df.sort_values("model_score", ascending=False).iloc[0]
            st.markdown(f"""
            <div class="scout-card" style="margin-top:14px; border-left:4px solid #E80071;">
                <div style="font-size:0.75rem; color:#FF70B8; font-weight:700; text-transform:uppercase;">WAR ROOM SCOUT VERDICT</div>
                <div style="font-size:1.05rem; font-weight:800; color:#FFFFFF; margin:4px 0;">
                    Primary Backing: {best_pick['player_name']}
                </div>
                <div style="font-size:0.85rem; color:#CBD5E1;">
                    Superior overall PressureIQ index ({best_pick['model_score']:.3f}) and proven clutch elevation ({best_pick['change_vs_baseline']:+.1f}). {best_pick.get('scout_verdict', '')}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Please select at least 2 candidates to generate comparative duels.")


# =============================================================================
# TAB 4: AUCTION INTELLIGENCE BOARD
# =============================================================================
with tabs[3]:
    st.markdown("<div style='font-size:1.15rem; font-weight:700; color:#FFFFFF; margin-bottom:4px;'>🎯 Rajasthan Royals 2027 Auction War Board</div>", unsafe_allow_html=True)
    st.caption("Actionable auction target tiers, projected valuation brackets, and squad role alignments.")
    
    col_t1, col_t2, col_t3 = st.columns([1, 1, 1])
    with col_t1:
        auc_role = st.selectbox("Filter Role", ["All Roles", "Batter", "Bowler"], key="auc_role_sel")
    with col_t2:
        auc_origin = st.selectbox("Filter Quota", ["All Players", "Domestic Only", "Overseas Only"], key="auc_origin_sel")
    with col_t3:
        auc_tier = st.selectbox("Filter Tier", ["All Tiers", "Tier 1: Marquee Priority", "Tier 2: High-Value Moneyball", "Tier 3: High-Upside Punt"], key="auc_tier_sel")
        
    auc_df = active_df.copy()
    if auc_role != "All Roles":
        auc_df = auc_df[auc_df["category"].str.lower() == auc_role.lower()]
    if auc_origin == "Domestic Only":
        auc_df = auc_df[auc_df["is_overseas"] == "No"]
    elif auc_origin == "Overseas Only":
        auc_df = auc_df[auc_df["is_overseas"] == "Yes"]
    if auc_tier != "All Tiers" and "auction_tier" in auc_df.columns:
        auc_df = auc_df[auc_df["auction_tier"] == auc_tier]
        
    auc_df = auc_df.sort_values("model_score", ascending=False)
    
    show_cols = [
        "player_name", "category", "country", "auction_tier", "model_score",
        "estimated_price_cr", "rr_role_target", "rr_tactical_fit", "pressure_strike_rate_or_economy", "change_vs_baseline"
    ]
    show_cols = [c for c in show_cols if c in auc_df.columns]
    
    renamed_auc = auc_df[show_cols].rename(columns={
        "player_name": "Target Player",
        "category": "Role",
        "country": "Nation",
        "auction_tier": "Strategic Tier",
        "model_score": "PressureIQ",
        "estimated_price_cr": "Est. Price (₹ Cr)",
        "rr_role_target": "RR Target Function",
        "rr_tactical_fit": "Synergy (0-100)",
        "pressure_strike_rate_or_economy": "Output",
        "change_vs_baseline": "Delta"
    })
    
    st.dataframe(renamed_auc, use_container_width=True, hide_index=True, height=480)
    
    st.download_button(
        "⬇️ Download Official RR 2027 Auction Target Board CSV",
        renamed_auc.to_csv(index=False).encode("utf-8"),
        "RR_2027_Auction_Intelligence_Board.csv",
        "text/csv"
    )


# =============================================================================
# TAB 5: SQUAD COMBINATION SIMULATOR (RR 2027 PLAYING XI BUILDER)
# =============================================================================
with tabs[4]:
    st.markdown("<div style='font-size:1.15rem; font-weight:700; color:#FFFFFF; margin-bottom:4px;'>🧩 RR 2027 Playing XI & Roster Combination Simulator</div>", unsafe_allow_html=True)
    st.caption("Construct a fully compliant 11-player Rajasthan Royals Playing XI. Enforces official IPL overseas quota limits, role balance, and purse budget.")
    
    preset_col1, preset_col2 = st.columns([1.5, 1])
    with preset_col1:
        preset_choice = st.selectbox(
            "Load Strategic Franchise Blueprint",
            ["Custom Manual Selection", "Preset 1: The RR 2027 Clutch & Death Wall XI", "Preset 2: The High-Value Domestic Core XI"]
        )
        
    all_batters = sorted(active_df[active_df["category"].str.lower() == "batter"]["player_name"].tolist())
    all_bowlers = sorted(active_df[active_df["category"].str.lower() == "bowler"]["player_name"].tolist())
    
    if preset_choice == "Preset 1: The RR 2027 Clutch & Death Wall XI":
        default_batters = [p for p in ["Sanju Samson", "Rinku Singh", "Shashank Singh", "Tristan Stubbs", "Riyan Parag", "Dhruv Jurel"] if p in all_batters]
        default_bowlers = [p for p in ["Matheesha Pathirana", "Sandeep Sharma", "Trent Boult", "Rashid Khan", "Arshdeep Singh"] if p in all_bowlers]
    elif preset_choice == "Preset 2: The High-Value Domestic Core XI":
        default_batters = [p for p in ["Shashank Singh", "Namboori Tilak Varma", "Rinku Singh", "Dhruv Jurel", "Riyan Parag", "Naman Dhir"] if p in all_batters]
        default_bowlers = [p for p in ["Sandeep Sharma", "T Natarajan", "Eshan Malinga", "Maheesh Theekshana", "Ravi Bishnoi"] if p in all_bowlers]
    else:
        default_batters = all_batters[:min(6, len(all_batters))]
        default_bowlers = all_bowlers[:min(5, len(all_bowlers))]
        
    s_col1, s_col2 = st.columns(2, gap="large")
    with s_col1:
        st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#FF70B8;'>🏏 Select Batting Order (Target: 6)</div>", unsafe_allow_html=True)
        selected_batters = st.multiselect("Choose Batters / Keepers / All-Rounders", all_batters, default=default_batters, key="sim_batters")
    with s_col2:
        st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#38BDF8;'>🎯 Select Bowling Attack (Target: 5)</div>", unsafe_allow_html=True)
        selected_bowlers = st.multiselect("Choose Fast Bowlers & Spinners", all_bowlers, default=default_bowlers, key="sim_bowlers")
        
    total_selected = selected_batters + selected_bowlers
    sim_df = active_df[active_df["player_name"].isin(total_selected)].copy()
    
    overseas_in_xi = len(sim_df[sim_df["is_overseas"] == "Yes"]) if "is_overseas" in sim_df.columns else 0
    total_cost = float(sim_df["estimated_price_cr"].sum()) if "estimated_price_cr" in sim_df.columns else 0.0
    team_pressure_index = float(sim_df["model_score"].mean() * 100) if len(sim_df) else 0.0
    
    st.write("")
    diag1, diag2, diag3, diag4 = st.columns(4)
    with diag1:
        st.metric("Total Selected Players", f"{len(sim_df)}/11", delta="Full XI" if len(sim_df)==11 else "Incomplete")
    with diag2:
        st.metric("Overseas Players", f"{overseas_in_xi}/4 Max", delta="Compliant" if overseas_in_xi <= 4 else "VIOLATION (Max 4)", delta_color="normal" if overseas_in_xi <= 4 else "inverse")
    with diag3:
        st.metric("Projected XI Spend", f"₹{total_cost:.1f} Cr", delta=f"₹{100.0 - total_cost:.1f} Cr Left")
    with diag4:
        st.metric("Team Pressure Resistance (TPRI)", f"{team_pressure_index:.1f}/100", delta="Elite" if team_pressure_index >= 85 else "Moderate")
        
    if overseas_in_xi > 4:
        st.error(f"🚨 ROSTER RULE VIOLATION: You have selected {overseas_in_xi} overseas players in your Playing XI. IPL regulations strictly limit overseas players to a maximum of 4.")
    if len(sim_df) != 11:
        st.warning(f"⚠️ Your simulated Playing XI contains {len(sim_df)} players. A full cricket XI requires exactly 11 players (6 Batters + 5 Bowlers).")
        
    if len(sim_df):
        st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#FFFFFF; margin:14px 0 6px 0;'>📋 Simulated Playing XI Lineup</div>", unsafe_allow_html=True)
        xi_table = sim_df[["player_name", "category", "country", "is_overseas", "model_score", "pressure_strike_rate_or_economy", "change_vs_baseline", "estimated_price_cr", "rr_role_target"]].rename(columns={
            "player_name": "Player",
            "category": "Role",
            "country": "Nation",
            "is_overseas": "Overseas?",
            "model_score": "Score",
            "pressure_strike_rate_or_economy": "Output",
            "change_vs_baseline": "Delta",
            "estimated_price_cr": "Est. Price (₹ Cr)",
            "rr_role_target": "Tactical Slot"
        })
        st.dataframe(xi_table, use_container_width=True, hide_index=True)
        
        st.download_button(
            "⬇️ Export Simulated RR Playing XI CSV",
            xi_table.to_csv(index=False).encode("utf-8"),
            "RR_2027_Simulated_Playing_XI.csv",
            "text/csv"
        )


# =============================================================================
# TAB 6: PLAYER RISK ANALYSIS & 2X2 QUADRANT MATRIX
# =============================================================================
with tabs[5]:
    st.markdown("<div style='font-size:1.15rem; font-weight:700; color:#FFFFFF; margin-bottom:4px;'>⚠️ Multi-Dimensional Player Risk Register & Quadrant Matrix</div>", unsafe_allow_html=True)
    st.caption("Identifies sample size risks, baseline regression flags, and domestic-to-IPL transferability barriers.")
    
    r_left, r_right = st.columns([1.1, 1], gap="large")
    
    with r_left:
        st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#FFFFFF; margin-bottom:4px;'>🎯 Risk vs Reward 4-Quadrant Matrix</div>", unsafe_allow_html=True)
        
        risk_fig = px.scatter(
            active_df,
            x="risk_score",
            y="model_score",
            color="auction_tier" if "auction_tier" in active_df.columns else "category",
            size="pressure_balls",
            hover_name="player_name",
            hover_data=["country", "pressure_matches", "consistency_pct"],
            color_discrete_map={
                "Tier 1: Marquee Priority": "#E80071",
                "Tier 2: High-Value Moneyball": "#10B981",
                "Tier 3: High-Upside Punt": "#F59E0B",
                "Tier 4: Caution / Trap Risk": "#EF4444"
            },
            labels={
                "risk_score": "Screening Risk Index (0 = Safe, 100 = High Risk)",
                "model_score": "PressureIQ Model Score (Reward / Upside)"
            }
        )
        risk_fig.add_vline(x=40, line_dash="dash", line_color="rgba(255,255,255,0.2)")
        risk_fig.add_hline(y=0.75, line_dash="dash", line_color="rgba(255,255,255,0.2)")
        
        risk_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(13, 20, 36, 0.4)",
            height=460,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(risk_fig, use_container_width=True)
        
    with r_right:
        st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#FFFFFF; margin-bottom:4px;'>🛡️ Key Screening Risk Pillars</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="scout-card" style="margin-bottom:12px;">
            <div style="font-weight:700; color:#EF4444; font-size:0.9rem;">1. Domestic-to-IPL Transferability Risk</div>
            <div style="font-size:0.8rem; color:#CBD5E1; margin-top:2px;">
                Players excelling exclusively in non-IPL domestic leagues face high risk against 145kph+ reverse swing, world-class mystery spin, and 50,000-seat crowd pressure.
            </div>
        </div>
        <div class="scout-card" style="margin-bottom:12px;">
            <div style="font-weight:700; color:#F59E0B; font-size:0.9rem;">2. Small Sample Size Volatility (n < 100 balls)</div>
            <div style="font-size:0.8rem; color:#CBD5E1; margin-top:2px;">
                High strike rates over under 100 pressure deliveries exhibit rapid regression to the mean. Bayesian shrinkage (n / (n+100)) is enforced to penalize small samples.
            </div>
        </div>
        <div class="scout-card" style="margin-bottom:12px;">
            <div style="font-weight:700; color:#38BDF8; font-size:0.9rem;">3. Negative Baseline Delta (Regressors)</div>
            <div style="font-size:0.8rem; color:#CBD5E1; margin-top:2px;">
                Big-name players whose strike rate drops or economy explodes under pressure compared to their own normal baseline.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        high_risk_df = active_df.sort_values("risk_score", ascending=False).head(10)[["player_name", "category", "risk_score", "pressure_balls", "IPL_pressure_balls", "auction_tier"]].rename(columns={
            "player_name": "Player",
            "category": "Role",
            "risk_score": "Risk Index",
            "pressure_balls": "Total Balls",
            "IPL_pressure_balls": "IPL Balls",
            "auction_tier": "Status"
        })
        st.dataframe(high_risk_df, use_container_width=True, hide_index=True)


# =============================================================================
# TAB 7: THE WINNING METHODOLOGY & PITCH
# =============================================================================
with tabs[6]:
    st.markdown("<div style='font-size:1.25rem; font-weight:800; color:#FFFFFF; margin-bottom:8px;'>📘 Winning Submission Dossier: Executive Pitch & Methodology</div>", unsafe_allow_html=True)
    st.caption("Comprehensive methodology and franchise pitch formulated to win Rajasthan Royals SupeRR Selector Round 1.")
    
    st.markdown("""
    ### 1. Executive Summary for Rajasthan Royals Leadership
    Rajasthan Royals' historical campaign data highlights two acute tactical vulnerabilities in high-pressure matches:
    1. **Death-Overs Bowling Vulnerability (Overs 17–20):** While Trent Boult provides gold-standard powerplay wickets, RR has leaked decisive runs in late overs.
    2. **Lower-Middle Order Finishing Reliability (#6–#7):** When the top order is challenged, RR requires domestic Indian batters who elevate their strike rate under high Required Run Rates (RRR > 10.5).

    ### 2. Mathematical Definition of Pressure & Bayesian Shrinkage
    Our PressureIQ model isolates true clutch performance through a strict, multi-tiered framework:
    * **High-Leverage State Criteria:**
      * Batting: Innings overs 16–20 with RRR > 9.5, or early collapse states (< 40/3 in powerplay).
      * Bowling: Innings overs 16–20 defending targets, or defending < 24 runs in final 12 balls.
    * **Bayesian Shrinkage Regularization:**
      $$S_{adj} = \\frac{n}{n + 100} \\cdot S_{raw} + \\frac{100}{n + 100} \\cdot \\mu_{role}$$
      This mathematical dampening ensures candidates with small sample sizes do not artificially distort rankings.
    * **Consistency Weighting:** Only matches with $\\ge 6$ pressure balls are evaluated for consistency, requiring candidate repeatability over random flash-in-the-pan innings.

    ### 3. Top Picks & How They Strengthen Rajasthan Royals:
    * **Donovan Ferreira (Batter, SA):** Phenomenal $+80.93$ SR delta over baseline, strike rate of $208.4$ under pressure with $90.0\%$ consistency. Plugs directly into RR's finishing slot at #6/7 and serves as backup keeper.
    * **Shashank Singh (Batter, IND):** Highest-ranked Indian domestic finisher with $362$ IPL pressure balls, $+60.15$ delta, and $182.87$ SR. The premier domestic Moneyball acquisition.
    * **Matheesha Pathirana (Bowler, SL):** Slinger release creates unmatched yorker precision at 150kph. Solves RR's death-bowling leak permanently.
    * **Eshan Malinga (Bowler, SL):** Exceptional value arbitrage. Negative delta on economy (better under pressure than normal) at a fraction of marquee price.
    """)
    
    st.write("")
    rep_c1, rep_c2 = st.columns(2)
    with rep_c1:
        if REPORT_PATH.exists():
            st.download_button(
                "⬇️ Download Official Methodology Report (PDF)",
                REPORT_PATH.read_bytes(),
                file_name=REPORT_PATH.name,
                mime="application/pdf"
            )
    with rep_c2:
        st.download_button(
            "⬇️ Download Complete 226-Player Enriched Dataset (CSV)",
            active_df.to_csv(index=False).encode("utf-8"),
            "RR_PressureIQ_Enriched_Master_Dataset.csv",
            "text/csv"
        )

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.divider()
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; color:#64748B; font-size:0.75rem;">
    <div>👑 <b>Rajasthan Royals PressureIQ 2027</b> · SupeRR Selector Round 1 Submission War Room</div>
    <div>Engineered for Live Deployment · Streamlit Community Cloud Ready</div>
</div>
""", unsafe_allow_html=True)
