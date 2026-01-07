import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import random
# Configuring the dashnpard
st.set_page_config(
    page_title="GreenPulse Urban Nature & Wellbeing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Welcome Page
if "started" not in st.session_state:
    st.title("Welcome to GreenPulse")
    st.subheader("Exploring how urban nature shapes wellbeing")
    st.write("""This is an interactive dashboard that visually represents the link
    between **urban green spaces, air quality, and human health**.
    This dashboard has been designed to help **policy makers, planners, and communities**
    to identify where environmental solutions can have the biggest impact in London.
    """
    )
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
     
# Sample Data for the metrics right now which will replace wih real life datasets that will be stored in a csv file.
np.random.seed(7)

boroughs = [
    "City of London",
    "Barking and Dagenham",
    "Barnet",
    "Bexley",
    "Brent",
    "Bromley",
    "Camden",
    "Croydon",
    "Ealing",
    "Enfield",
    "Greenwich",
    "Hackney",
    "Hammersmith and Fulham",
    "Haringey",
    "Harrow",
    "Havering",
    "Hillingdon",
    "Hounslow",
    "Islington",
    "Kensington and Chelsea",
    "Kingston upon Thames",
    "Lambeth",
    "Lewisham",
    "Merton",
    "Newham",
    "Redbridge",
    "Richmond upon Thames",
    "Southwark",
    "Sutton",
    "Tower Hamlets",
    "Waltham Forest",
    "Wandsworth",
    "Westminster"
]

#adding latitude and longitude around London
base_lat = 51.5074 
base_lon = -0.1278

data = pd.DataFrame({
    "area": boroughs,
    "lat": base_lat + np.random.uniform(-0.05, 0.05, len(boroughs)),
    "lon": base_lon + np.random.uniform(-0.08, 0.08, len(boroughs)),
    # Environmental Indicators
    "tree_cover_pct": np.random.randint(10, 60, len(boroughs)),
    "green_space_access_pct": np.random.randint(40, 95, len(boroughs)),
    "biodiversity_index": np.random.randint(30, 90, len(boroughs)),   
    "air_quality_index": np.random.randint(20, 90, len(boroughs)),    
})

# Health and Wellbeing Metrics
data["stress_index"] = np.clip(
    75
    - 0.25 * data["green_space_access_pct"]
    - 0.20 * data["biodiversity_index"]
    + 0.10 * data["air_quality_index"],
    0, 100
)

data["wellbeing_index"] = np.clip(
    45
    + 0.30 * data["green_space_access_pct"]
    + 0.25 * data["biodiversity_index"]
    - 0.15 * data["air_quality_index"],
    0, 100
)

data["respiratory_risk_index"] = np.clip(
    20
    + 0.4 * data["air_quality_index"]
    - 0.2 * data["tree_cover_pct"],
    0, 100
)


# Sidebar with controls 
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
st.sidebar.markdown("**Linked SDGs**")
st.sidebar.markdown(" SDG 3 – Good Health and Wellbeing")
st.sidebar.markdown(" SDG 11 – Sustainable Cities and Communities")
st.sidebar.markdown(" SDG 15 – Life on Land")


# HEADER
st.title("GreenPulse")
st.subheader("Exploring how urban nature and biodiversity shape human wellbeing")
st.caption(
    "Prototype dashboard combining environmental indicators (air quality, tree cover, green space) "
    "with wellbeing metrics (stress, respiratory risk, overall wellbeing)."
)

# Filter data if a single area is selected
if selected_area != "All areas":
    df_view = data[data["area"] == selected_area].copy()
else:
    df_view = data.copy()


map_options = {
    "Green Space Access (%)": "green_space_access_pct",
    "Wellbeing Index": "wellbeing_index",
    "Respiratory Risk Index": "respiratory_risk_index"
}

map_label = st.selectbox(
    "Colour map by:",
    list(map_options.keys())
)

map_metric = map_options[map_label]



# Top Panel of dashboard having an overview of London
st.markdown("### Overview of London ")
st.markdown("---")
col_map, col_scores = st.columns([2, 1])

with col_map:
    st.markdown("**Where is nature and wellbeing distributed across London?**")

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
        hover_data={
            map_metric: True
        },
        color_continuous_scale="Greens",
        mapbox_style="carto-positron"
    )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    st.plotly_chart(fig, use_container_width=True)

with col_scores:
    mean_green = df_view["green_space_access_pct"].mean()
    mean_tree = df_view["tree_cover_pct"].mean()
    mean_biodiv = df_view["biodiversity_index"].mean()
    mean_wellbeing = df_view["wellbeing_index"].mean()

    st.markdown("**GreenPulse Snapshot**")
    st.metric("Avg Green Space Access (%)", f"{mean_green:.1f}")
    st.metric("Avg Tree Cover (%)", f"{mean_tree:.1f}")
    st.metric("Avg Biodiversity Index", f"{mean_biodiv:.1f}")
    st.metric("Avg Wellbeing Index", f"{mean_wellbeing:.1f}")


# Middle Panel – Environment and Health
st.markdown("### Environment & Health Indicators")

col_env, col_health = st.columns(2)

# Environment
with col_env:
    st.markdown("#### Environmental Indicators")

    chart_green = (
        alt.Chart(df_view)
        .mark_bar(color="#2E7D32")
        .encode(
            x=alt.X("area:N", sort="-y", title="Borough"),
            y=alt.Y("green_space_access_pct:Q", title="Green Space Access (%)"),
            tooltip=["area", "green_space_access_pct"]
        )
        .properties(height=280)
    )
    st.altair_chart(chart_green, use_container_width=True)

    chart_tree = (
        alt.Chart(df_view)
        .mark_bar(color="#388E3C")
        .encode(
            x=alt.X("area:N", sort="-y", title="Borough"),
            y=alt.Y("tree_cover_pct:Q", title="Tree Cover (%)"),
            tooltip=["area", "tree_cover_pct"]
        )
        .properties(height=250)
    )
    st.altair_chart(chart_tree, use_container_width=True)

# Health and Wellbeing
with col_health:
    st.markdown("#### Wellbeing & Health Indicators")

    chart_wellbeing = (
        alt.Chart(df_view)
        .mark_line(color="#1565C0", point=True)
        .encode(
            x=alt.X("area:N", title="Borough"),
            y=alt.Y("wellbeing_index:Q", title="Wellbeing Index (0–100)"),
            tooltip=["area", "wellbeing_index"]
        )
        .properties(height=280)
    )
    st.altair_chart(chart_wellbeing, use_container_width=True)

    chart_resp = (
        alt.Chart(df_view)
        .mark_bar(color="#C62828")
        .encode(
            x=alt.X("area:N", title="Borough"),
            y=alt.Y("respiratory_risk_index:Q", title="Respiratory Risk Index (0–100)"),
            tooltip=["area", "respiratory_risk_index"]
        )
        .properties(height=250)
    )
    st.altair_chart(chart_resp, use_container_width=True)


# Exploring the relationship/correlation between nature and health.
st.markdown("### Relationship Explorer: Nature vs Health")

metric_x = st.selectbox(
    "Choose environmental metric (X-axis)",
    ["green_space_access_pct", "tree_cover_pct", "biodiversity_index", "air_quality_index"],
    format_func=lambda x: {
        "green_space_access_pct": "Green Space Access (%)",
        "tree_cover_pct": "Tree Cover (%)",
        "biodiversity_index": "Biodiversity Index",
        "air_quality_index": "Air Quality Index (lower = better)"
    }[x]
)

metric_y = st.selectbox(
    "Choose health/wellbeing metric (Y-axis)",
    ["wellbeing_index", "stress_index", "respiratory_risk_index"],
    format_func=lambda x: {
        "wellbeing_index": "Wellbeing Index",
        "stress_index": "Stress Index (0–100, lower = better)",
        "respiratory_risk_index": "Respiratory Risk Index (0–100)"
    }[x]
)

scatter = (
    alt.Chart(df_view)
    .mark_circle(size=120)
    .encode(
        x=alt.X(metric_x + ":Q", title=metric_x.replace("_", " ").title()),
        y=alt.Y(metric_y + ":Q", title=metric_y.replace("_", " ").title()),
        color=alt.value("#2E7D32"),
        tooltip=["area", metric_x, metric_y]
    )
    .properties(height=350)
)
st.altair_chart(scatter, use_container_width=True)


# Simulation for adding more greenery/treesor increasing greenspace in areas of London
st.markdown("###  Simulation: What if we add more greenery?")

baseline_green = df_view["green_space_access_pct"].mean()
baseline_tree = df_view["tree_cover_pct"].mean()
baseline_wellbeing = df_view["wellbeing_index"].mean()
baseline_stress = df_view["stress_index"].mean()
baseline_resp = df_view["respiratory_risk_index"].mean()

sim_green = baseline_green + green_increase
sim_tree = baseline_tree + tree_increase

sim_wellbeing = np.clip(
    baseline_wellbeing
    + 0.25 * green_increase
    + 0.20 * tree_increase,
    0, 100
)

sim_stress = np.clip(
    baseline_stress
    - 0.20 * green_increase
    - 0.15 * tree_increase,
    0, 100
)

sim_resp = np.clip(
    baseline_resp
    - 0.20 * tree_increase,
    0, 100
)

col_base, col_sim = st.columns(2)

with col_base:
    st.markdown("Current Averages")
    st.metric("Green Space Access (%)", f"{baseline_green:.1f}")
    st.metric("Tree Cover (%)", f"{baseline_tree:.1f}")
    st.metric("Wellbeing Index", f"{baseline_wellbeing:.1f}")
    st.metric("Stress Index", f"{baseline_stress:.1f}")
    st.metric("Respiratory Risk Index", f"{baseline_resp:.1f}")

with col_sim:
    st.markdown("Simulated After Adding More Green")
    st.metric("Green Space Access (%)", f"{sim_green:.1f}", f"+{green_increase}")
    st.metric("Tree Cover (%)", f"{sim_tree:.1f}", f"+{tree_increase}")
    st.metric("Wellbeing Index", f"{sim_wellbeing:.1f}", f"{sim_wellbeing - baseline_wellbeing:+.1f}")
    st.metric("Stress Index", f"{sim_stress:.1f}", f"{sim_stress - baseline_stress:+.1f}")
    st.metric("Respiratory Risk Index", f"{sim_resp:.1f}", f"{sim_resp - baseline_resp:+.1f}")

st.info(
    f"In this simple model, adding +{green_increase}% green space and +{tree_increase}% tree cover "
    f"increases wellbeing by {sim_wellbeing - baseline_wellbeing:+.1f} points, "
    f"reduces stress by {sim_stress - baseline_stress:+.1f} points, "
    f"and lowers respiratory risk by {sim_resp - baseline_resp:+.1f} points on average."
)
# Sensor integration its a prototype so random values added for now
st.markdown("### Urban Sensor Integration (Prototype)")
st.markdown(
    "This section demonstrates how live environmental sensor data "
    "could be integrated into the GreenPulse platform in future deployments."
)
sensor_data = {
    "Co2 (ppm)": random.randint(380,550),
    "Humidity(%)": random.randint(40,75),
    "Light Intensity(lux)": random.randint(100,1200),
    "Noise Levels(dB)":  random.randint(45,80)
}

cols= st.columns(4)
for col,(label,value) in zip(cols, sesnor_data.items()):
    col.metric(label,value)
st.caption(
    "Sensor Values shown have been simulated in a few areas for demonstration purposes."
    "Future versions will integrate real-time data from low-cost urban sensors."
)
st.info(
    "Planned sensor inputs include low cost Co2,humidity,noise levels and light sensors"
    "which are connected through microcontrollers specifically an arduino uno and the results will be displayed on the dashboard"
    "through the cloud."
)
# Footer
st.markdown("---")
st.caption(
    "GreenPulse demonstrates how greener, more biodiverse neighbourhoods can support "
    "human wellbeing across London. "
    "Aligned with SDG 3 (Good Health & Wellbeing), "
    "SDG 11 (Sustainable Cities & Communities), and "
    "SDG 15 (Life on Land)."
)
st.markdown("---")
st.markdown("### Reset Dashboard")

st.write(
    "Finished exploring GreenPulse? "
    "Click below to reset the dashboard for the next user."
)

if st.button("Reset and Return to Welcome Page"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()



