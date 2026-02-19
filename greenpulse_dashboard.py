import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import random
import json


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
        <b>demonstration</b> — not predictive decision-making.
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='gp-divider-animated'></div>", unsafe_allow_html=True)

    st.markdown("### How it works")

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
        <div class="gp-card">
          <div class="title">🗺️ Choose a borough</div>
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


wellbeing_raw = pd.read_csv("data/wellbeing-local-authority-time-series-v4.csv")

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
    (wellbeing_raw["Geography"].isin(boroughs))
][["Geography", "v4_3"]].rename(
    columns={"Geography": "area", "v4_3": "wellbeing_index"}
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
    st.title("GreenPulse")
    st.subheader("Urban Nature, Environment and Wellbeing")

    st.write(
        "Use the sidebar on the left to explore environmental conditions, "
        "health indicators and simulated green interventions across London boroughs."
    )
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

# -------------------------------
# Sections
# -------------------------------
if section == "Overview of London":
    if demo_mode:
        st.success(demo_text[section])

    map_options = {
        "Green Space Access (%)": "green_space_access_pct",
        "Wellbeing Index": "wellbeing_index",
        "Respiratory Risk Index": "respiratory_risk_index"
    }

    map_label = st.selectbox("Colour map by:", list(map_options.keys()))
    map_metric = map_options[map_label]

    if map_metric in ["respiratory_risk_index", "air_quality_index", "stress_index"]:
        scale = "YlOrRd"
    elif map_metric == "wellbeing_index":
        scale = "Blues"
    else:
        scale = "Greens"

    fig = px.choropleth_mapbox(
        df_view,
        geojson=borough_geojson,
        locations="area",
        featureidkey="properties.name",
        color=map_metric,
        color_continuous_scale=scale,
        range_color=[0, 100],
        mapbox_style="carto-positron",
        zoom=8.8,
        center={"lat": 51.5074, "lon": -0.1278},
        opacity=0.75,
        hover_name="area",
        hover_data={map_metric: ":.1f"},
        labels={
            "green_space_access_pct": "Green Space Access (%)",
            "wellbeing_index": "Wellbeing Index",
            "respiratory_risk_index": "Respiratory Risk Index"
        }
    )

    fig.update_coloraxes(colorbar_title=map_label)
    st.plotly_chart(fig, use_container_width=True)

elif section == "Environment & Health":
    if demo_mode:
        st.success(demo_text[section])

    col1, col2 = st.columns(2)

    with col1:
        st.altair_chart(
            alt.Chart(df_view).mark_bar().encode(
                x="area:N",
                y="green_space_access_pct:Q"
            ),
            use_container_width=True
        )

    with col2:
        st.altair_chart(
            alt.Chart(df_view).mark_line(point=True).encode(
                x="area:N",
                y="wellbeing_index:Q"
            ),
            use_container_width=True
        )

elif section == "Relationship Explorer":
    if demo_mode:
        st.success(demo_text[section])

    metric_x = st.selectbox(
        "Environmental metric",
        ["green_space_access_pct", "tree_cover_pct", "biodiversity_index", "air_quality_index"]
    )
    metric_y = st.selectbox(
        "Health metric",
        ["wellbeing_index", "stress_index", "respiratory_risk_index"]
    )

    st.altair_chart(
        alt.Chart(df_view).mark_circle(size=120).encode(
            x=f"{metric_x}:Q",
            y=f"{metric_y}:Q",
            tooltip=["area", metric_x, metric_y]
        ),
        use_container_width=True
    )

elif section == "Urban Impact Simulation":
    if demo_mode:
        st.success(demo_text[section])

    london_avg = data.mean(numeric_only=True)

    base_wellbeing = df_view["wellbeing_index"].mean()
    base_stress = df_view["stress_index"].mean()
    base_resp = df_view["respiratory_risk_index"].mean()

    sim_wellbeing = np.clip(base_wellbeing + green_increase * 0.2 + tree_increase * 0.15, 0, 100)
    sim_stress = np.clip(base_stress - green_increase * 0.16, 0, 100)
    sim_resp = np.clip(base_resp - tree_increase * 0.3, 0, 100)

    col1, col2, col3 = st.columns(3)

    if compare_mode and selected_area != "All areas":
        col1.metric(
            "Estimated Wellbeing Index",
            f"{sim_wellbeing:.1f}",
            f"{sim_wellbeing - london_avg['wellbeing_index']:+.1f} vs London"
        )
        col2.metric(
            "Estimated Stress Index",
            f"{sim_stress:.1f}",
            f"{sim_stress - london_avg['stress_index']:+.1f} vs London",
            delta_color="inverse"
        )
        col3.metric(
            "Estimated Respiratory Risk",
            f"{sim_resp:.1f}",
            f"{sim_resp - london_avg['respiratory_risk_index']:+.1f} vs London",
            delta_color="inverse"
        )
    else:
        col1.metric("Estimated Wellbeing Index", f"{sim_wellbeing:.1f}", f"{sim_wellbeing - base_wellbeing:+.1f}")
        col2.metric("Estimated Stress Index", f"{sim_stress:.1f}", f"{sim_stress - base_stress:+.1f}", delta_color="inverse")
        col3.metric("Estimated Respiratory Risk", f"{sim_resp:.1f}", f"{sim_resp - base_resp:+.1f}", delta_color="inverse")

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


