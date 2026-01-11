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


if "demo_step" not in st.session_state:
    st.session_state.demo_step = 0

if "started" not in st.session_state:
    st.session_state.started = False
if not st.session_state.started:
    st.title("Welcome to GreenPulse")
    st.subheader("Urban Nature, Environment and Wellbeing")

    st.write(
        "GreenPulse is an interactive data dashboard designed to explore relationships "
        "between urban green infrastructure, environmental conditions, and population "
        "wellbeing across London boroughs."
    )
    st.write(
        "The dashboard integrates publicly available datasets and simplified indicators "
        "to support exploratory analysis and discussion. It is intended for educational, "
        "analytical, and demonstrative use rather than predictive decision-making."
    )

    with st.expander("How to use this dashboard", expanded=True):
        st.markdown("""
        Choose a borough from the sidebar  
        Explore environmental and wellbeing patterns  
        Use the simulation sliders to test green interventions  
        """)

    st.write(
        "This dashboard explores links between urban green spaces, air quality, "
        "and human health to support evidence based urban planning in London."
    )

    if st.button("Enter Dashboard"):
        st.session_state.started = True
        st.rerun()

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
    if st.button("Reset and Return to Welcome Page"):
        st.session_state.started = False
        st.session_state.demo_step = 0
        st.rerun()
with col_reset_demo:
    if demo_mode:
        if st.button("Reset Demo"):
            st.session_state.demo_step = 0
            st.rerun()

