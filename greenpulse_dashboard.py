import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import random

wellbeing_raw = pd.read_csv("data/wellbeing-local-authority-time-series-v4.csv")

st.set_page_config(
    page_title="GreenPulse Urban Nature & Wellbeing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "started" not in st.session_state:
    st.title("Welcome to GreenPulse")
    st.subheader("Exploring how urban nature shapes wellbeing")
    st.write("""This is an interactive dashboard that visually represents the link
    between **urban green spaces, air quality, and human health**.
    This dashboard has been designed to help **policy makers, planners, and communities**
    to identify where environmental solutions can have the biggest impact in London.
    """)
    st.markdown(
        """
    **What can be explored:**
    - Greenery and tree cover across London
    - Linking the relationship between nature and health
    - Simulation of nature-related interventions
    """
    )
    if st.button("Enter Dashboard"):
        st.session_state.started = True
        st.rerun()
    st.stop()

np.random.seed(7)

boroughs = [
    "City of London","Barking and Dagenham","Barnet","Bexley","Brent","Bromley",
    "Camden","Croydon","Ealing","Enfield","Greenwich","Hackney",
    "Hammersmith and Fulham","Haringey","Harrow","Havering","Hillingdon",
    "Hounslow","Islington","Kensington and Chelsea","Kingston upon Thames",
    "Lambeth","Lewisham","Merton","Newham","Redbridge",
    "Richmond upon Thames","Southwark","Sutton","Tower Hamlets",
    "Waltham Forest","Wandsworth","Westminster"
]

base_lat = 51.5074
base_lon = -0.1278

data = pd.DataFrame({
    "area": boroughs,
    "lat": base_lat + np.random.uniform(-0.05, 0.05, len(boroughs)),
    "lon": base_lon + np.random.uniform(-0.08, 0.08, len(boroughs)),
    "tree_cover_pct": np.random.randint(10, 60, len(boroughs)),
    "green_space_access_pct": np.random.randint(40, 95, len(boroughs)),
    "biodiversity_index": np.random.randint(30, 90, len(boroughs)),
    "air_quality_index": np.random.randint(20, 90, len(boroughs)),
})

wellbeing_raw["v4_3"] = pd.to_numeric(wellbeing_raw["v4_3"], errors="coerce")
latest_year = wellbeing_raw["Time"].max()

wellbeing_filtered = wellbeing_raw[
    (wellbeing_raw["Time"] == latest_year) &
    (wellbeing_raw["MeasureOfWellbeing"] == "Life satisfaction") &
    (wellbeing_raw["Geography"].isin(boroughs))
][["Geography", "v4_3"]]

wellbeing_df = (
    wellbeing_filtered
    .dropna(subset=["v4_3"])
    .groupby("Geography", as_index=False)
    .first()
    .rename(columns={"Geography": "area", "v4_3": "wellbeing_index"})
)

data = data.merge(wellbeing_df, on="area", how="left")

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

st.sidebar.title("Controls")

selected_area = st.sidebar.selectbox(
    "Focus area",
    ["All areas"] + boroughs
)

green_increase = st.sidebar.slider(
    "Simulate increase in green space (%)",
    min_value=0, max_value=40, value=10, step=5
)

tree_increase = st.sidebar.slider(
    "Simulate increase in tree cover (%)",
    min_value=0, max_value=30, value=5, step=5
)

st.sidebar.markdown("---")
st.sidebar.markdown("SDG 3 – Good Health and Wellbeing")
st.sidebar.markdown("SDG 11 – Sustainable Cities and Communities")
st.sidebar.markdown("SDG 15 – Life on Land")

st.title("GreenPulse")
st.subheader("Exploring how urban nature and biodiversity shape human wellbeing")
st.caption(
    "Wellbeing index derived from Office for National Statistics (ONS) Life Satisfaction "
    "values and rescaled to a 0–100 index for comparability."
)

df_view = data if selected_area == "All areas" else data[data["area"] == selected_area].copy()

map_options = {
    "Green Space Access (%)": "green_space_access_pct",
    "Wellbeing Index (ONS, 0–100)": "wellbeing_index",
    "Respiratory Risk Index": "respiratory_risk_index"
}

map_label = st.selectbox("Colour map by:", list(map_options.keys()))
map_metric = map_options[map_label]

st.markdown("### Overview of London")
st.markdown("---")
col_map, col_scores = st.columns([2, 1])

with col_map:
    fig = px.scatter_mapbox(
        df_view,
        lat="lat",
        lon="lon",
        color=map_metric,
        size=map_metric,
        size_max=22,
        zoom=9,
        center={"lat": 51.5074, "lon": -0.1278},
        hover_name="area",
        color_continuous_scale="Greens",
        mapbox_style="carto-positron"
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig, use_container_width=True)

with col_scores:
    st.metric("Avg Green Space Access (%)", f"{df_view['green_space_access_pct'].mean():.1f}")
    st.metric("Avg Tree Cover (%)", f"{df_view['tree_cover_pct'].mean():.1f}")
    st.metric("Avg Biodiversity Index", f"{df_view['biodiversity_index'].mean():.1f}")
    st.metric("Avg Wellbeing Index (ONS, 0–100)", f"{df_view['wellbeing_index'].mean():.1f}")

st.markdown("### Environment & Health Indicators")
col_env, col_health = st.columns(2)

with col_env:
    st.altair_chart(
        alt.Chart(df_view).mark_bar(color="#2E7D32").encode(
            x=alt.X("area:N", sort="-y"),
            y="green_space_access_pct:Q",
            tooltip=["area", "green_space_access_pct"]
        ).properties(height=280),
        use_container_width=True
    )
    st.altair_chart(
        alt.Chart(df_view).mark_bar(color="#388E3C").encode(
            x=alt.X("area:N", sort="-y"),
            y="tree_cover_pct:Q",
            tooltip=["area", "tree_cover_pct"]
        ).properties(height=250),
        use_container_width=True
    )

with col_health:
    st.altair_chart(
        alt.Chart(df_view).mark_line(color="#1565C0", point=True).encode(
            x="area:N",
            y=alt.Y("wellbeing_index:Q", title="Wellbeing Index (0–100)"),
            tooltip=["area", "wellbeing_index"]
        ).properties(height=280),
        use_container_width=True
    )
    st.altair_chart(
        alt.Chart(df_view).mark_bar(color="#C62828").encode(
            x="area:N",
            y="respiratory_risk_index:Q",
            tooltip=["area", "respiratory_risk_index"]
        ).properties(height=250),
        use_container_width=True
    )

st.markdown("### Relationship Explorer: Nature vs Health")

metric_x = st.selectbox(
    "Choose environmental metric (X-axis)",
    ["green_space_access_pct", "tree_cover_pct", "biodiversity_index", "air_quality_index"]
)

metric_y = st.selectbox(
    "Choose health/wellbeing metric (Y-axis)",
    ["wellbeing_index", "stress_index", "respiratory_risk_index"]
)

st.altair_chart(
    alt.Chart(df_view).mark_circle(size=120).encode(
        x=f"{metric_x}:Q",
        y=f"{metric_y}:Q",
        tooltip=["area", metric_x, metric_y]
    ).properties(height=350),
    use_container_width=True
)

st.markdown("### Simulation: What if we add more greenery?")

baseline_wellbeing = df_view["wellbeing_index"].mean()

sim_wellbeing = np.clip(
    baseline_wellbeing
    + 0.25 * green_increase
    + 0.20 * tree_increase,
    0, 100
)

col_base, col_sim = st.columns(2)

with col_base:
    st.metric("Current Wellbeing Index (0–100)", f"{baseline_wellbeing:.1f}")

with col_sim:
    st.metric(
        "Simulated Wellbeing Index (0–100)",
        f"{sim_wellbeing:.1f}",
        f"{sim_wellbeing - baseline_wellbeing:+.1f}"
    )

st.markdown("### Urban Sensor Integration (Prototype)")

sensor_data = {
    "CO₂ (ppm)": random.randint(380, 550),
    "Humidity (%)": random.randint(40, 75),
    "Light Intensity (lux)": random.randint(100, 1200),
    "Noise Levels (dB)": random.randint(45, 80)
}

cols = st.columns(4)
for col, (label, value) in zip(cols, sensor_data.items()):
    col.metric(label, value)

st.markdown("---")

if st.button("Reset and Return to Welcome Page"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
