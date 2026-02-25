import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import random
import json
import os
import base64

def img_to_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

st.set_page_config(
    page_title="GreenPulse Urban Nature & Wellbeing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
CUSTOM_CSS = """
<style>
:root { 
  --gp-accent-1: #22c55e;
  --gp-accent-2: #38bdf8;
}
/* --- Background --- */
.stApp {
  background:
    radial-gradient(1200px circle at 12% 10%, rgba(34,197,94,0.18), transparent 55%),
    radial-gradient(900px circle at 88% 18%, rgba(56,189,248,0.14), transparent 52%),
    linear-gradient(180deg, #050b15 0%, #020617 100%) !important;
}

/* Hero container */
.hero {
  max-width: 1100px;
  margin: 3rem auto 2.5rem auto;
  padding: 3rem 3.5rem;
  border-radius: 26px;
  background: linear-gradient(
    135deg,
    rgba(20,60,45,0.75),
    rgba(10,20,35,0.85)
  );
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 30px 80px rgba(0,0,0,0.45);
}
/* Glass cards */
.gp-card {
  border-radius: 18px;
  padding: 16px 18px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 10px 24px rgba(0,0,0,0.22);
}
.gp-card:hover {
  transform: translateY(-2px);
  border-color: rgba(34,197,94,0.45);
  box-shadow:
    0 14px 34px rgba(0,0,0,0.28),
    0 0 22px rgba(34,197,94,0.35),
    0 0 38px rgba(56,189,248,0.22);
}


/* --- Animated full-width accent divider --- */
@keyframes gp-flow {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.gp-divider-animated {
  height: 4px;
  width: 100%;
  border-radius: 999px;

  background: linear-gradient(
    90deg,
    #22c55e,
    #38bdf8,
    #22c55e
  );
  background-size: 300% 100%;

  animation: gp-flow 8s ease-in-out infinite;

  margin: 2.4rem 0 2.8rem 0;

  box-shadow:
    0 0 14px rgba(34,197,94,0.45),
    0 0 28px rgba(56,189,248,0.25);
}
/* --- Animated glow for primary buttons --- */
@keyframes gp-button-glow {
  0% {
    box-shadow:
      0 0 0 rgba(34,197,94,0.0),
      0 0 0 rgba(56,189,248,0.0);
  }
  50% {
    box-shadow:
      0 0 18px rgba(34,197,94,0.45),
      0 0 32px rgba(56,189,248,0.30);
  }
  100% {
    box-shadow:
      0 0 0 rgba(34,197,94,0.0),
      0 0 0 rgba(56,189,248,0.0);
  }
}

/* Style + animate Streamlit buttons */
div.stButton > button {
  border-radius: 16px;
  padding: 0.75rem 1.3rem;
  font-weight: 600;
  letter-spacing: 0.01em;

  border: 1px solid rgba(34,197,94,0.45);
  background: linear-gradient(
    135deg,
    rgba(34,197,94,0.25),
    rgba(56,189,248,0.18)
  );

  animation: gp-button-glow 5.5s ease-in-out infinite;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

/* Hover = intentional emphasis */
div.stButton > button:hover {
  transform: translateY(-1px) scale(1.01);
  box-shadow:
    0 0 24px rgba(34,197,94,0.6),
    0 0 40px rgba(56,189,248,0.4);
}

/* Active (click) feedback */
div.stButton > button:active {
  transform: scale(0.98);
}
.dash-hero{
  margin: 1.2rem 0 1.2rem 0;
  padding: 1.4rem 1.6rem;
  border-radius: 22px;
  background: linear-gradient(135deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
  border: 1px solid rgba(255,255,255,0.10);
  box-shadow: 0 18px 45px rgba(0,0,0,0.35);
  position: relative;
  overflow: hidden;
}
.dash-hero:before{
  content:"";
  position:absolute;
  inset:-2px;
  background: radial-gradient(700px circle at 10% 20%, rgba(34,197,94,0.18), transparent 45%),
              radial-gradient(700px circle at 90% 10%, rgba(56,189,248,0.16), transparent 45%);
  filter: blur(8px);
  opacity: 0.9;
  pointer-events:none;
}
.dash-hero-inner{ position:relative; z-index:1; }

@keyframes gp-shimmer {
  0% { transform: translateX(-30%); opacity: 0.0; }
  20%{ opacity: 0.35; }
  50%{ opacity: 0.12; }
  100%{ transform: translateX(30%); opacity: 0.0; }
}
.dash-shimmer{
  position:absolute;
  top:-40%;
  left:0;
  width:100%;
  height:180%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.14), transparent);
  transform: translateX(-30%);
  animation: gp-shimmer 7.5s ease-in-out infinite;
  pointer-events:none;
  z-index:0;
}

/* ---------- Pills / chips ---------- */
.pill-row{ display:flex; flex-wrap:wrap; gap:10px; margin-top: 10px; }
.pill{
  display:inline-flex;
  align-items:center;
  gap:8px;
  padding: 8px 12px;
  border-radius: 999px;
  font-size: 0.92rem;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.10);
}
.pill-dot{
  width:10px; height:10px; border-radius:999px;
  background: linear-gradient(90deg, var(--gp-accent-1), var(--gp-accent-2));
  box-shadow: 0 0 14px rgba(34,197,94,0.35), 0 0 20px rgba(56,189,248,0.22);
}

/* ---------- KPI cards ---------- */
.kpi-grid{
  display:grid;
  grid-template-columns: repeat(3, minmax(0,1fr));
  gap: 14px;
  margin-top: 14px;
}
.kpi{
  border-radius: 18px;
  padding: 14px 16px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 10px 24px rgba(0,0,0,0.22);
  transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}
.kpi:hover{
  transform: translateY(-2px);
  border-color: rgba(34,197,94,0.40);
  box-shadow:
    0 14px 34px rgba(0,0,0,0.30),
    0 0 18px rgba(34,197,94,0.25),
    0 0 30px rgba(56,189,248,0.18);
}
.kpi .label{ opacity:0.8; font-size:0.95rem; }
.kpi .value{ font-size:1.55rem; font-weight:750; margin-top: 6px; }
.kpi .sub{ opacity:0.75; font-size:0.92rem; margin-top: 4px; }

@media (max-width: 1100px){
  .kpi-grid{ grid-template-columns: 1fr; }
}
/* ---------- GII Recommendation Card (dynamic + animated) ---------- */
@keyframes gp-rise-in {
  from { transform: translateY(10px); opacity: 0; }
  to   { transform: translateY(0);  opacity: 1; }
}

.gp-rec-card{
  margin-top: 18px;
  padding: 18px 22px;
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,0.10);
  box-shadow: 0 12px 30px rgba(0,0,0,0.35);
  animation: gp-rise-in 0.45s ease-out both;
}

.gp-rec-title{
  margin: 0 0 8px 0;
  font-weight: 700;
}

.gp-rec-text{
  margin: 0;
  font-size: 0.98rem;
  line-height: 1.45;
  opacity: 0.95;
}

/* severity styles */
.gp-sev-low{
  background: linear-gradient(135deg, rgba(34,197,94,0.18), rgba(2,6,23,0.55));
  border-color: rgba(34,197,94,0.40);
  box-shadow: 0 12px 30px rgba(0,0,0,0.35), 0 0 22px rgba(34,197,94,0.18);
}
.gp-sev-med{
  background: linear-gradient(135deg, rgba(234,179,8,0.18), rgba(2,6,23,0.55));
  border-color: rgba(234,179,8,0.45);
  box-shadow: 0 12px 30px rgba(0,0,0,0.35), 0 0 22px rgba(234,179,8,0.18);
}
.gp-sev-high{
  background: linear-gradient(135deg, rgba(239,68,68,0.18), rgba(2,6,23,0.55));
  border-color: rgba(239,68,68,0.45);
  box-shadow: 0 12px 30px rgba(0,0,0,0.35), 0 0 22px rgba(239,68,68,0.18);
}
@keyframes gp-logo-glow {
  0% {
    box-shadow:
      0 0 20px rgba(34,197,94,0.25),
      0 0 35px rgba(56,189,248,0.18);
  }
  50% {
    box-shadow:
      0 0 40px rgba(34,197,94,0.45),
      0 0 65px rgba(56,189,248,0.35);
  }
  100% {
    box-shadow:
      0 0 20px rgba(34,197,94,0.25),
      0 0 35px rgba(56,189,248,0.18);
  }
}

.gp-logo-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 1.5rem;
}

.gp-logo-glow {
  border-radius: 28px;
  padding: 18px;
  background: radial-gradient(
    circle at center,
    rgba(34,197,94,0.12),
    rgba(56,189,248,0.08),
    transparent 70%
  );
  animation: gp-logo-glow 6s ease-in-out infinite;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -------------------------------
# Session state
# -------------------------------
if "demo_step" not in st.session_state:
    st.session_state.demo_step = 0

if "started" not in st.session_state:
    st.session_state.started = False

# Welcome page only
if not st.session_state.started:
    st.markdown("""
    <div class="hero">
      <h1>GreenPulse</h1>
      <h3>Urban Nature, Environment & Wellbeing</h3>

      <p>
        An interactive dashboard exploring the relationships between
        <b>urban green infrastructure</b>, <b>environmental conditions</b>,
        and <b>population wellbeing</b> across London boroughs.
      </p>

      <p>
        Built using publicly available datasets, GreenPulse supports
        <b>exploratory analysis</b>, <b>education</b>, and
        <b>demonstration</b> and not predictive decision-making.
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='gp-divider-animated'></div>", unsafe_allow_html=True)

    st.markdown("### How it works")

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
        <div class="gp-card">
          <div class="title"> Choose a borough</div>
          <p class="desc">Explore London at borough level</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="gp-card">
          <div class="title"> Explore patterns</div>
          <p class="desc">Compare environment and wellbeing indicators</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="gp-card">
          <div class="title"> Test interventions</div>
          <p class="desc">Simulate green infrastructure impacts</p>
        </div>
        """, unsafe_allow_html=True)

    # Centered CTA that won't wrap weirdly
    st.markdown("<div style='max-width:420px; margin: 2.5rem auto 0 auto;'>", unsafe_allow_html=True)
    if st.button(" Enter Dashboard", use_container_width=True):
        st.session_state.started = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.stop()



# -------------------------------
# Wellbeing (ONS) loader (robust paths)
# -------------------------------
def _load_wellbeing_timeseries():
    candidate_paths = [
        "data/wellbeing-local-authority-time-series-v4.csv",
        "wellbeing-local-authority-time-series-v4.csv",
    ]
    for p in candidate_paths:
        if os.path.exists(p):
            return pd.read_csv(p)
    # Fall back to Streamlit Cloud / current working dir error message
    raise FileNotFoundError(
        "Wellbeing dataset not found. Add 'wellbeing-local-authority-time-series-v4.csv' to your repo (e.g., data/)."
    )

wellbeing_raw = _load_wellbeing_timeseries()

with open("data/london_boroughs.geojson", "r") as f:
    borough_geojson = json.load(f)

boroughs = [
    "City of London","Barking and Dagenham","Barnet","Bexley","Brent","Bromley",
    "Camden","Croydon","Ealing","Enfield","Greenwich","Hackney",
    "Hammersmith and Fulham","Haringey","Harrow","Havering","Hillingdon",
    "Hounslow","Islington","Kensington and Chelsea","Kingston upon Thames",
    "Lambeth","Lewisham","Merton","Newham","Redbridge",
    "Richmond upon Thames","Southwark","Sutton","Tower Hamlets",
    "Waltham Forest","Wandsworth","Westminster"
]

np.random.seed(7)

data = pd.DataFrame({
    "area": boroughs,
    "tree_cover_pct": np.random.randint(10, 60, len(boroughs)),
    "green_space_access_pct": np.random.randint(40, 95, len(boroughs)),
    "biodiversity_index": np.random.randint(30, 90, len(boroughs)),
})

pm25_raw = pd.read_csv("data/popwmpm252024byUKlocalauthority.csv")
pm25 = pm25_raw.rename(columns={
    "Unnamed: 1": "area",
    "population-weighted annual mean PM2.5 concentration for 2024 (ugm-3)": "pm25_ugm3"
})
pm25["area"] = pm25["area"].astype(str).str.strip()
pm25["pm25_ugm3"] = pd.to_numeric(pm25["pm25_ugm3"], errors="coerce")
pm25 = pm25.dropna(subset=["area", "pm25_ugm3"])

pm25 = pm25.replace({
    "Royal Borough of Kensington and Chelsea": "Kensington and Chelsea",
    "City of Westminster": "Westminster"
})

pm25 = pm25[pm25["area"].isin(boroughs)]
pm25 = pm25.groupby("area", as_index=False)["pm25_ugm3"].mean()

wellbeing_raw["v4_3"] = pd.to_numeric(wellbeing_raw["v4_3"], errors="coerce")
latest_year = wellbeing_raw["Time"].max()

wellbeing_df = wellbeing_raw[
    (wellbeing_raw["Time"] == latest_year) &
    (wellbeing_raw["MeasureOfWellbeing"] == "Life satisfaction") &
    # Use the official borough mean (prevents mixing mean with % breakdown rows)
    ((wellbeing_raw["Estimate"] == "Average (mean)") if "Estimate" in wellbeing_raw.columns else True) &
    (wellbeing_raw["Geography"].isin(boroughs))
][["Geography", "v4_3"]].rename(
    columns={"Geography": "area", "v4_3": "wellbeing_index"}
)

# Ensure numeric + 1 wellbeing value per borough
wellbeing_df["wellbeing_index"] = pd.to_numeric(wellbeing_df["wellbeing_index"], errors="coerce")
wellbeing_df = wellbeing_df.groupby("area", as_index=False)["wellbeing_index"].mean()

# Add a simple wellbeing band + note (similar to GII recommendations)
_london_wb_mean = float(wellbeing_df["wellbeing_index"].mean(skipna=True))

def _wellbeing_band_and_note(score: float, london_mean: float):
    if pd.isna(score):
        return ("Unknown", "Wellbeing score not available for this borough.")
    if score <= london_mean - 0.15:
        return ("Below average", "Boost wellbeing with pocket parks, safer green walking routes, and stronger links between nature and health support (e.g., social prescribing).")
    if score >= london_mean + 0.15:
        return ("Above average", "Protect existing green assets and prioritise quality upgrades (maintenance, lighting, seating and biodiversity) to sustain wellbeing.")
    return ("Average", "Maintain wellbeing by improving park quality, accessibility, and tree‑lined streets—small upgrades can have large benefits.")

wellbeing_df["wellbeing_band"], wellbeing_df["wellbeing_note"] = zip(
    *[_wellbeing_band_and_note(v, _london_wb_mean) for v in wellbeing_df["wellbeing_index"]]
)

data = data.merge(wellbeing_df, on="area", how="left")
data = data.merge(pm25, on="area", how="left")

pm25_min = data["pm25_ugm3"].min()
pm25_max = data["pm25_ugm3"].max()
pm25_range = pm25_max - pm25_min

data["air_quality_index"] = (
    50.0 if pm25_range == 0 or pd.isna(pm25_range)
    else ((data["pm25_ugm3"] - pm25_min) / pm25_range) * 100
)

data["stress_index"] = np.clip(
    75
    - 0.25 * data["green_space_access_pct"]
    - 0.20 * data["biodiversity_index"]
    + 0.10 * data["air_quality_index"],
    0, 100
)

data["respiratory_risk_index"] = np.clip(
    20
    + 0.4 * data["air_quality_index"]
    - 0.2 * data["tree_cover_pct"],
    0, 100
)


# -------------------------------------------------
# GREEN INEQUALITY INDEX (GII) – loaded from Excel
# -------------------------------------------------
def _load_gii_data():
    candidate_paths = [
        "data/GreenPulse Map.csv",
        "GreenPulse Map.csv",
        "data/Green Inequality Index.csv",
        "Green Inequality Index.csv",
    ]

    for path in candidate_paths:
        if os.path.exists(path):
            return pd.read_csv(path)

    return None


gii_df = _load_gii_data()
if gii_df is not None and "Borough" in gii_df.columns:
    gii = gii_df.copy()
    # Clean borough names
    gii["Borough"] = gii["Borough"].astype(str).str.strip()

    # Standardise column names into the dashboard
    rename_map = {
        "Borough": "area",
        "GI": "green_inequality_index",
        "PM": "gii_pm25",
        "Green": "gii_greenspace",
        "Bio": "gii_biodiversity",
        "Asthma": "gii_asthma",
    }
    gii = gii.rename(columns=rename_map)

    # Ensure numeric
    for c in ["green_inequality_index", "gii_pm25", "gii_greenspace", "gii_biodiversity", "gii_asthma"]:
        if c in gii.columns:
            gii[c] = pd.to_numeric(gii[c], errors="coerce")

    # Main driver = largest contributing factor (simple rule based on your 4 factor columns)
    driver_cols = {
        "PM2.5": "gii_pm25",
        "Low green space": "gii_greenspace",
        "Low biodiversity": "gii_biodiversity",
        "Asthma (u19)": "gii_asthma",
    }
    # Row-wise argmax across the four factors (ignoring NaNs)
    factor_frame = gii[list(driver_cols.values())].copy()
    gii["gii_main_driver"] = factor_frame.idxmax(axis=1).map({v: k for k, v in driver_cols.items()})

    # Nature-based solution recommendation per driver
    rec_map = {
        "PM2.5": "Roadside green barriers + street tree corridors to trap particulates and reduce exposure.",
        "Low green space": "Pocket parks, school greening, and converting underused land into accessible green space.",
        "Low biodiversity": "Pollinator corridors, native planting, and habitat mosaics to restore urban biodiversity.",
        "Asthma (u19)": "Greening around schools + low-allergen planting and shaded walking routes to reduce flare-up risk.",
    }
    gii["gii_recommendation"] = gii["gii_main_driver"].map(rec_map)

    # Merge into main dataset
    data = data.merge(
        gii[[
            "area",
            "green_inequality_index",
            "gii_pm25",
            "gii_greenspace",
            "gii_biodiversity",
            "gii_asthma",
            "gii_main_driver",
            "gii_recommendation",
        ]],
        on="area",
        how="left"
    )
else:
    # Keep columns present even if Excel isn't available (prevents key errors)
    data["green_inequality_index"] = np.nan
    data["gii_pm25"] = np.nan
    data["gii_greenspace"] = np.nan
    data["gii_biodiversity"] = np.nan
    data["gii_asthma"] = np.nan
    data["gii_main_driver"] = np.nan
    data["gii_recommendation"] = np.nan

# Ensure exactly 1 row per borough after merges (keeps maps + charts consistent)
numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
non_numeric_cols = [c for c in data.columns if c not in numeric_cols and c != "area"]
data = (
    data.groupby("area", as_index=False)
        .agg({**{c: "mean" for c in numeric_cols}, **{c: "first" for c in non_numeric_cols}})
)

# -------------------------------------------------
# WELLBEING (LSSC realism add-ons)
# Keep the official ONS mean (0–10) as-is, but add relative views for interpretation:
#  - wellbeing_vs_london: borough minus London mean (points)
#  - wellbeing_pct_vs_london: % difference vs London mean
#  - wellbeing_zscore: standardised deviation (z-score)
if "wellbeing_index" in data.columns:
    _wb_mean = float(data["wellbeing_index"].mean(skipna=True)) if data["wellbeing_index"].notna().any() else np.nan
    _wb_std  = float(data["wellbeing_index"].std(skipna=True)) if data["wellbeing_index"].notna().sum() > 1 else np.nan

    data["wellbeing_london_mean"] = _wb_mean

    data["wellbeing_vs_london"] = data["wellbeing_index"] - _wb_mean

    # Avoid divide-by-zero
    if pd.notna(_wb_mean) and abs(_wb_mean) > 1e-9:
        data["wellbeing_pct_vs_london"] = (data["wellbeing_vs_london"] / _wb_mean) * 100.0
    else:
        data["wellbeing_pct_vs_london"] = np.nan

    if pd.notna(_wb_std) and _wb_std > 1e-9:
        data["wellbeing_zscore"] = (data["wellbeing_index"] - _wb_mean) / _wb_std
    else:
        data["wellbeing_zscore"] = 0.0

# -------------------------------------------------
# STRATEGIC LAYERS
# -------------------------------------------------

# --- 1️⃣ Risk Classification ---
def classify_risk(gii):
    if pd.isna(gii):
        return "Unknown"
    if gii >= 0.75:
        return "Critical Ecological Stress"
    elif gii >= 0.55:
        return "High Risk"
    elif gii >= 0.35:
        return "Transitional"
    else:
        return "Resilient Zone"

data["risk_classification"] = data["green_inequality_index"].apply(classify_risk)


# --- 2️⃣ Equity (Green Access) Metric ---
# Build a smoother (less tie-prone) proxy "green access score" using multiple dimensions.
# This avoids many boroughs rounding to identical values.
data["green_access_score"] = (
    0.50 * data["green_space_access_pct"].fillna(0)
    + 0.30 * data["tree_cover_pct"].fillna(0)
    + 0.20 * data["biodiversity_index"].fillna(0)
)

# Use the median as a robust benchmark (less sensitive to outliers)
london_green_benchmark = float(data["green_access_score"].median(skipna=True))

# Deficit-only metric (0% means no deficit: borough >= benchmark)
data["equity_deficit_pct"] = np.clip(
    (london_green_benchmark - data["green_access_score"]) / london_green_benchmark * 100,
    0,
    None
)

# Percentile position (higher = better access)
data["green_access_percentile"] = data["green_access_score"].rank(pct=True) * 100


# --- 3️⃣ Policy Priority Ranking (resource allocation model) ---
# Align urgency with the risk layer:
# - GII is the main driver
# - equity_deficit increases urgency (shortfall vs benchmark)
# - stress provides additional weighting
gii_component = data["green_inequality_index"].fillna(0)
stress_component = (data["stress_index"].fillna(0) / 100)

data["intervention_urgency_score"] = (
    (gii_component * 0.60)
    + ((data["equity_deficit_pct"].fillna(0) / 100) * 0.25)
    + (stress_component * 0.15)
)

# Rank: 1 = most urgent
data["priority_rank"] = data["intervention_urgency_score"].rank(
    ascending=False, method="min"
).astype(int)

st.sidebar.title("Dashboard Navigation")

section = st.sidebar.radio(
    "Go to:",
    [
        "Overview of London",
        "Environment & Health",
        "Relationship Explorer",
        "Urban Impact Simulation",
        "Urban Sensor Integration"
    ]
)

st.sidebar.markdown("---")

demo_mode = st.sidebar.checkbox(
    "Guided Demo of GreenPulse",
    value=False
)

if demo_mode:
    demo_steps = [
        "Overview of London",
        "Environment & Health",
        "Relationship Explorer",
        "Urban Impact Simulation",
        "Urban Sensor Integration"
    ]
    section = demo_steps[st.session_state.demo_step]

st.sidebar.subheader("Controls")

if demo_mode:
    selected_area = st.sidebar.selectbox(
        "Select a borough",
        boroughs
    )
    compare_mode = True
    green_increase = st.sidebar.slider(
        "Increase green space (%)",
        0,40,20,5
    )
    tree_increase = st.sidebar.slider(
        "Increase Tree Cover (%)",
        0,30,15,5
    )
else:
    selected_area = st.sidebar.selectbox(
        "Selected borough",
        ["All areas"] + boroughs
    )

    compare_mode = False
    if selected_area != "All areas":
        compare_mode = st.sidebar.checkbox(
            "Compare with London average",
            value=True
        )

    if section == "Urban Impact Simulation":
        green_increase = st.sidebar.slider("Increase green space (%)", 0, 40, 10, 5)
        tree_increase = st.sidebar.slider("Increase tree cover (%)", 0, 30, 5, 5)
    else:
        green_increase = 0
        tree_increase = 0

df_view = data if selected_area == "All areas" else data[data["area"] == selected_area]


with st.container():

    logo_b64 = img_to_base64("GreenPulse Logo.jpeg")

    st.markdown(f"""
    <div class="gp-logo-container">
      <div class="gp-logo-glow">
        <img src="data:image/jpeg;base64,{logo_b64}" style="width:180px; height:auto; display:block;">
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.title("GreenPulse")
    SECTION_HEADERS = {
    "Overview of London": (
        "London-wide Overview",
        "Explore borough-level patterns in green infrastructure, environment, and wellbeing across London."
    ),
    "Environment & Health": (
        "Environment & Health Comparison",
        "Compare green space access and wellbeing indicators across boroughs and identify areas of concern."
    ),
    "Relationship Explorer": (
        "Relationships & Correlations",
        "Explore how environmental indicators relate to health and wellbeing outcomes across boroughs."
    ),
    "Urban Impact Simulation": (
        "Urban Impact Simulator",
        "Test how increasing green space and tree cover could influence inequality, stress, and wellbeing metrics."
    ),
    "Urban Sensor Integration": (
        "Urban Sensor Integration",
        "Demonstration of how live sensor feeds for CO₂, humidity, light and noise levels could be integrated for real-time monitoring."
    ),
}

sub, desc = SECTION_HEADERS.get(
    section,
    ("Urban Nature, Environment and Wellbeing",
     "Use the sidebar on the left to explore environmental conditions, health indicators and simulated green interventions across London boroughs.")
)

st.subheader(sub)
st.write(desc)
if demo_mode:
    st.markdown("### Guided Demo")
    #progress indicators showing how far people have gone in the demo
    total_steps = 5
    current_step = st.session_state.demo_step + 1
    st.progress(current_step / total_steps)
    col_prev, col_mid, col_next = st.columns([1, 3, 1])

    with col_prev:
        if st.button("Previous",icon=":material/arrow_back:") and st.session_state.demo_step > 0:
            st.session_state.demo_step -= 1
            st.rerun()

    with col_mid:
        st.write(
            f"Step {st.session_state.demo_step + 1} of 5 — {section}"
        )

    with col_next:
        if st.button("Next",icon=":material/arrow_forward:") and st.session_state.demo_step < 4:
            st.session_state.demo_step += 1
            st.rerun()
demo_text = {
    "Overview of London":
        "This map shows how environmental and wellbeing indicators vary across London boroughs.",
    "Environment & Health":
        "These charts compare green space access and reported wellbeing between boroughs.",
    "Relationship Explorer":
        "This scatter plot explores associations between environmental and health indicators.",
    "Urban Impact Simulation":
        "This simulation demonstrates estimated impacts of green infrastructure interventions.",
    "Urban Sensor Integration":
        "This section illustrates how live sensor data could be integrated in future."
}

if demo_mode and st.session_state.demo_step == 4:
    st.success("Demo complete! You can continue exploring the dashboard or reset the demo to start again.")


# Sections

if section == "Overview of London":
    if demo_mode:
        st.success(demo_text[section])

    map_options = {
        "Green Space Access (%)": "green_space_access_pct",

        # ONS wellbeing (raw + relative view)
        "Wellbeing (ONS Life satisfaction, 0–10)": "wellbeing_index",
        "Wellbeing (vs London avg)": "wellbeing_vs_london",

        "Respiratory Risk Index": "respiratory_risk_index",
        "Green Inequality Index (0–1)": "green_inequality_index",
    }

    map_label = st.selectbox("Colour map by:", list(map_options.keys()))
    map_metric = map_options[map_label]
    if demo_mode:
        if map_metric == "green_space_access_pct":
            demo_desc = "This map highlights differences in green space accessibility across London boroughs."
        elif map_metric == "wellbeing_index":
            demo_desc = "This map shows wellbeing based on datasets of ONS life satisfaction scores of London."
        elif map_metric == "wellbeing_vs_london":
            demo_desc = "This map shows how each borough’s wellbeing compares to the London average."
        elif map_metric == "respiratory_risk_index":
            demo_desc = "This map highlights respiratory health risk linked to environmental conditions."
        elif map_metric == "green_inequality_index":
            demo_desc = "This map visualises the Green Inequality Index, identifying boroughs facing combined environmental disadvantage."
        else:
            demo_desc = demo_text[section]
        st.success(demo_desc)

    # Colour scales
    if map_metric in ["respiratory_risk_index", "air_quality_index", "stress_index"]:
        scale = "YlOrRd"
    elif map_metric == "wellbeing_index":
        scale = "Blues"
    elif map_metric == "wellbeing_vs_london":
        # Diverging scale: negative = below London avg, positive = above London avg
        scale = "RdBu"
    elif map_metric == "green_inequality_index":
        scale = "RdYlGn_r"
    else:
        scale = "Greens"

    df_map = df_view.copy()

    # Safety: only include hover_data columns that exist (prevents Plotly ValueError on typos)
    def safe_hover_data(d, df):
        return {k: v for k, v in d.items() if k in df.columns}

    # Range handling
    if map_metric == "green_inequality_index":
        range_color = [0, 1]
        # Exclude City of London (not included in the dataset)
        df_map = df_map[df_map["area"] != "City of London"]
    elif map_metric == "wellbeing_index":
        range_color = [0, 10]
    elif map_metric == "wellbeing_vs_london":
        # Typical borough differences are modest; clip for stable colour contrast without exaggeration.
        range_color = [-0.6, 0.6]
    else:
        range_color = [0, 100]

    # Hover handling
    if map_metric == "green_inequality_index":
        if "green_inequality_index" in df_map.columns and df_map["green_inequality_index"].dropna().empty:
            st.warning(
                "Green Inequality Index data not found. Make sure 'GreenPulse Map.csv' is in your repo (e.g., data/GreenPulse Map.csv)."
            )

        hover_data = {
            "green_inequality_index": ":.3f",
            "gii_main_driver": True,
        }

    elif map_metric == "wellbeing_index":
        hover_data = {
            "wellbeing_index": ":.2f",
            "wellbeing_band": True,
            "wellbeing_pct_vs_london": ":.1f",
        }

    elif map_metric == "wellbeing_vs_london":
        hover_data = {
            "wellbeing_vs_london": ":.2f",
            "wellbeing_index": ":.2f",
            "wellbeing_pct_vs_london": ":.1f",
            "wellbeing_band": True,
        }

    else:
        hover_data = {map_metric: ":.1f"}

    hover_data = safe_hover_data(hover_data, df_map)

    fig = px.choropleth_mapbox(
        df_map,
        geojson=borough_geojson,
        locations="area",
        featureidkey="properties.name",
        color=map_metric,
        color_continuous_scale=scale,
        range_color=range_color,
        mapbox_style="carto-positron",
        zoom=8.8,
        center={"lat": 51.5074, "lon": -0.1278},
        opacity=0.75,
        hover_name="area",
        hover_data=hover_data,
        labels={
            "green_space_access_pct": "Green Space Access (%)",
            "wellbeing_index": "Wellbeing Index (0–10)",
            "wellbeing_vs_london": "Wellbeing (vs London avg)",
            "wellbeing_band": "Wellbeing Band",
            "wellbeing_pct_vs_london": "% vs London",
            "respiratory_risk_index": "Respiratory Risk Index",
            "green_inequality_index": "Green Inequality Index (0–1)",
            "gii_main_driver": "Primary Driver",
            "gii_pm25": "PM2.5 Contribution",
            "gii_greenspace": "Green Space Deficit",
            "gii_biodiversity": "Biodiversity Deficit",
            "gii_asthma": "Asthma Vulnerability (U19)",
        }
    )

    fig.update_coloraxes(colorbar_title=map_label)
    st.plotly_chart(fig, use_container_width=True)

    if map_metric in ["wellbeing_index", "wellbeing_vs_london"]:
        st.caption(
            f"Wellbeing is ONS life satisfaction (latest year: {latest_year}). "
            f"London mean: {_london_wb_mean:.2f}/10. Differences across boroughs are typically modest."
        )

    if selected_area == "All areas":
        st.caption("**Select a borough from the sidebar to see the recommendation / wellbeing note.**")

    # --- GII recommendation card (only when a borough is selected) ---
    if selected_area != "All areas" and map_metric == "green_inequality_index":
        row = data[data["area"] == selected_area]
        if not row.empty:
            r0 = row.iloc[0]
            rec = r0.get("gii_recommendation", None)
            gii_val = r0.get("green_inequality_index", None)

            sev_class = "gp-sev-med"
            sev_label = "Medium"
            try:
                if pd.notna(gii_val):
                    if gii_val < 0.33:
                        sev_class, sev_label = "gp-sev-low", "Low"
                    elif gii_val < 0.66:
                        sev_class, sev_label = "gp-sev-med", "Medium"
                    else:
                        sev_class, sev_label = "gp-sev-high", "High"
            except Exception:
                pass

            rec_txt = rec.strip() if isinstance(rec, str) else ""
            if not rec_txt:
                rec_txt = "—"

            gii_str = "—"
            try:
                if pd.notna(gii_val):
                    gii_str = f"{float(gii_val):.3f}"
            except Exception:
                pass

            st.markdown(
                f"""
                <div class="gp-rec-card {sev_class}">
                  <div class="gp-rec-title">
                    Recommendation for <b>{selected_area}</b> <span style="opacity:0.85;">(Severity: {sev_label} -> GII: {gii_str})</span>
                  </div>
                  <p class="gp-rec-text">{rec_txt}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # --- Wellbeing note card (raw + vs London view) ---
    if selected_area != "All areas" and map_metric in ["wellbeing_index", "wellbeing_vs_london"]:
        row = data[data["area"] == selected_area]
        if not row.empty:
            r0 = row.iloc[0]
            wb_val = r0.get("wellbeing_index", None)
            wb_band = r0.get("wellbeing_band", "")
            wb_note = r0.get("wellbeing_note", "")

            sev_class = "gp-sev-med"
            if isinstance(wb_band, str):
                if "Above" in wb_band:
                    sev_class = "gp-sev-low"
                elif "Below" in wb_band:
                    sev_class = "gp-sev-high"

            wb_str = "—"
            try:
                if pd.notna(wb_val):
                    wb_str = f"{float(wb_val):.2f}"
            except Exception:
                pass

            _diff = r0.get("wellbeing_vs_london", np.nan)
            _pctd = r0.get("wellbeing_pct_vs_london", np.nan)
            diff_str = "—"
            pct_str = "—"
            try:
                if pd.notna(_diff):
                    diff_str = f"{float(_diff):+.2f}"
                if pd.notna(_pctd):
                    pct_str = f"{float(_pctd):+.1f}%"
            except Exception:
                pass

            wb_note_txt = wb_note.strip() if isinstance(wb_note, str) else ""
            if not wb_note_txt:
                wb_note_txt = "—"

            st.markdown(
                f"""
                <div class="gp-rec-card {sev_class}">
                  <div class="gp-rec-title">
                    Wellbeing note for <b>{selected_area}</b>
                    <span style="opacity:0.85;">({wb_band} • Score: {wb_str}/10 • vs London: {diff_str} ({pct_str}))</span>
                  </div>
                  <p class="gp-rec-text">{wb_note_txt}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # -------------------------------------------------
    # Strategic Indicators (borough selected)
    # -------------------------------------------------
    if selected_area != "All areas":
        _row = data[data["area"] == selected_area]
        if not _row.empty:
            _r = _row.iloc[0]

            st.markdown("### Strategic Indicators")

            _risk = str(_r.get("risk_classification", "—"))
            _risk_map = {
                "Resilient Zone": ("🟢", "Low"),
                "Transitional": ("🟡", "Medium"),
                "High Risk": ("🟠", "High"),
                "Critical Ecological Stress": ("🔴", "Critical"),
                "Unknown": ("⚪", "Unknown"),
            }
            _risk_emoji, _risk_level = _risk_map.get(_risk, ("⚪", "Unknown"))

            _driver = _r.get("gii_main_driver", np.nan)
            _driver_txt = "—"
            try:
                if isinstance(_driver, str) and _driver.strip():
                    _driver_txt = _driver.strip()
                elif pd.notna(_driver):
                    _driver_txt = str(_driver)
            except Exception:
                pass

            _def = _r.get("equity_deficit_pct", np.nan)
            _pct = _r.get("green_access_percentile", np.nan)
            _rank = _r.get("priority_rank", np.nan)
            _total = int(data["area"].nunique())

            _wb = _r.get("wellbeing_index", np.nan)
            _wb_diff = _r.get("wellbeing_vs_london", np.nan)

            def _format_deficit(v: float) -> str:
                if pd.isna(v):
                    return "—"
                v = float(v)
                if v < 0.5:
                    return "No deficit"
                if v < 1.0:
                    return "<1% deficit"
                return f"{v:.1f}% deficit"

            _def_txt = _format_deficit(_def)
            _pct_txt = "—" if pd.isna(_pct) else f"{float(_pct):.0f}th"
            _alloc_txt = "—" if pd.isna(_rank) else f"{int(_rank)} / {_total}"

            _wb_txt = "—"
            _wb_diff_txt = ""
            try:
                if pd.notna(_wb):
                    _wb_txt = f"{float(_wb):.2f}/10"
                if pd.notna(_wb_diff):
                    _wb_diff_txt = f" (vs London {float(_wb_diff):+.2f})"
            except Exception:
                pass

            if pd.isna(_rank):
                _tier = "—"
            else:
                r = int(_rank)
                if r <= max(1, int(np.ceil(_total * 0.20))):
                    _tier = "Tier 1 – Immediate Allocation Focus"
                elif r <= max(1, int(np.ceil(_total * 0.50))):
                    _tier = "Tier 2 – Moderate Priority"
                else:
                    _tier = "Tier 3 – Strategic Monitoring"

            st.markdown(
                f"""
                <div class="kpi-grid">
                  <div class="kpi">
                    <div class="label">Risk classification</div>
                    <div class="value">{_risk_emoji} {_risk}</div>
                    <div class="sub">Severity: {_risk_level}</div>
                    <div class="sub">Primary driver: {_driver_txt}</div>
                  </div>

                  <div class="kpi">
                    <div class="label">Green access deficit vs London benchmark</div>
                    <div class="value">{_def_txt}</div>
                    <div class="sub">Green access percentile: {_pct_txt}</div>
                    <div class="sub">Wellbeing (ONS): <b>{_wb_txt}</b>{_wb_diff_txt}</div>
                  </div>

                  <div class="kpi">
                    <div class="label">Intervention allocation position</div>
                    <div class="value">{_alloc_txt}</div>
                    <div class="sub">{_tier}</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )
elif section == "Environment & Health":

    if demo_mode:
        st.success(demo_text[section])

    col1, col2 = st.columns(2)

    with col1:
        st.altair_chart(
            alt.Chart(df_view).mark_bar().encode(
                x=alt.X("area:N", sort="-y", title="Borough"),
                y=alt.Y("green_space_access_pct:Q", title= "Green Space Access (%)"),
                tooltip=[
                     alt.Tooltip("area:N", title="Borough"),
                     alt.Tooltip("green_space_access_pct:Q", title="Green Space Access (%)", format=".0f"),
                ]
            ),
            use_container_width=True
        )

    
    with col2:
        # Borough wellbeing (ONS) + London mean reference line
        wb_bar = alt.Chart(df_view).mark_bar().encode(
            x=alt.X("area:N", sort="-y", title="Borough"),
            y=alt.Y("wellbeing_index:Q", title="Wellbeing (ONS Life satisfaction, 0–10)"),
            tooltip=[
                alt.Tooltip("area:N", title="Borough"),
                alt.Tooltip("wellbeing_index:Q", title="Wellbeing (ONS)", format=".2f"),
                alt.Tooltip("wellbeing_pct_vs_london:Q", title="% vs London", format=".1f"),
            ]
        )

        wb_mean = alt.Chart(pd.DataFrame({"london_mean": [_london_wb_mean]})).mark_rule().encode(
            y="london_mean:Q"
        )

        st.altair_chart(wb_bar + wb_mean, use_container_width=True)
        st.caption(f"London mean (latest year: {latest_year}): {_london_wb_mean:.2f}/10")
elif section == "Relationship Explorer":
    if demo_mode:
        st.success(demo_text[section])

    env_metric_options = {
        "Green Space Accessibility (%)": "green_space_access_pct",
        "Tree Cover (%)": "tree_cover_pct",
        "Biodiversity Index": "biodiversity_index",
        "Air Quality Index (0–100)": "air_quality_index",
        "Green Inequality Index (0–1)": "green_inequality_index",
    }

    health_metric_options = {
        "Wellbeing Index (ONS Life Satisfaction)": "wellbeing_index",
        "Stress Index": "stress_index",
        "Respiratory Health Risk Index": "respiratory_risk_index",
        "Green Inequality Index (0–1)": "green_inequality_index",
    }

    selected_env_label = st.selectbox(
        "Environmental Indicator",
        list(env_metric_options.keys())
    )

    selected_health_label = st.selectbox(
        "Health & Wellbeing Indicator",
        list(health_metric_options.keys())
    )

    metric_x = env_metric_options[selected_env_label]
    metric_y = health_metric_options[selected_health_label]

    axis_labels = {
        "green_space_access_pct": "Green Space Access (%)",
        "tree_cover_pct": "Tree Cover (%)",
        "biodiversity_index": "Biodiversity Index",
        "air_quality_index": "Air Quality Index (0–100)",
        "wellbeing_index": "Wellbeing Index (0–10)",
        "stress_index": "Stress Index (0–100)",
        "respiratory_risk_index": "Respiratory Risk Index (0–100)",
        "green_inequality_index": "Green Inequality Index (0–1)",
    }

    df_plot = df_view.copy()
    x_title = axis_labels.get(metric_x, metric_x)
    y_title = axis_labels.get(metric_y, metric_y)

    base = alt.Chart(df_plot)

    glow = base.mark_circle(
        size=350,
        opacity=0.15,
        color="#38bdf8"
    ).encode(
        x=alt.X(f"{metric_x}:Q", title=x_title),
        y=alt.Y(f"{metric_y}:Q", title=y_title),
    )

    points = base.mark_circle(
        size=120,
        color="#22c55e",
        stroke="white",
        strokeWidth=1
    ).encode(
        x=alt.X(f"{metric_x}:Q", title=x_title),
        y=alt.Y(f"{metric_y}:Q", title=y_title),
        tooltip=[
            alt.Tooltip("area:N", title="Borough"),
            alt.Tooltip(f"{metric_x}:Q", title=x_title),
            alt.Tooltip(f"{metric_y}:Q", title=y_title),
        ]
    )

    st.altair_chart(glow + points, use_container_width=True)

elif section == "Urban Impact Simulation":

    london_avg = data.mean(numeric_only=True)

    base_row = df_view.iloc[0] if selected_area != "All areas" else data.mean(numeric_only=True)

    base_gii = base_row["green_inequality_index"]
    base_wellbeing = base_row["wellbeing_index"]
    base_stress = base_row["stress_index"]

    # Intervention modelling
    gii_reduction = (green_increase * 0.01 * 0.4) + (tree_increase * 0.01 * 0.3)
    projected_gii = np.clip(base_gii - gii_reduction, 0, 1)

    projected_wellbeing = np.clip(base_wellbeing + green_increase * 0.15 + tree_increase * 0.12, 0, 10)
    projected_stress = np.clip(base_stress - green_increase * 0.2, 0, 100)

    # Reclassify risk
    new_risk = classify_risk(projected_gii)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Projected Green Inequality Index",
        f"{projected_gii:.3f}",
        f"{projected_gii - base_gii:+.3f}",
        delta_color="inverse"
    )

    col2.metric(
        "Projected Wellbeing Index",
        f"{projected_wellbeing:.2f}",
        f"{projected_wellbeing - base_wellbeing:+.2f}"
    )

    col3.metric(
        "Projected Stress Index",
        f"{projected_stress:.1f}",
        f"{projected_stress - base_stress:+.1f}",
        delta_color="inverse"
    )

    st.markdown("### Risk Classification Shift")
    st.write(f"Current: **{classify_risk(base_gii)}**")
    st.write(f"Projected: **{new_risk}**")

elif section == "Urban Sensor Integration":
    if demo_mode:
        st.success(demo_text[section])

    sensor_data = {
        "CO₂ (ppm)": random.randint(380, 550),
        "Humidity (%)": random.randint(40, 75),
        "Light (lux)": random.randint(100, 1200),
        "Noise (dB)": random.randint(45, 80)
    }

    cols = st.columns(4)
    for col, (label, value) in zip(cols, sensor_data.items()):
        col.metric(label, value)

st.markdown("---")
col_reset_welcome, col_reset_demo, spacer = st.columns([3,1.5,5])
with col_reset_welcome:
    if st.button("Return to Welcome Page"):
        st.session_state.started = False
        st.session_state.demo_step = 0
        st.rerun()
with col_reset_demo:
    if demo_mode:
        if st.button("Reset Demo"):
            st.session_state.demo_step = 0
            st.rerun()
