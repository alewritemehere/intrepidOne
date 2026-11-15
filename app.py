"""
IntrepidOne - Earth System Trend Detective & Urban Cool-Shade Router
NASA Space Apps Challenge Rome 2026
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import folium
from folium.plugins import HeatMap
import streamlit.components.v1 as components

from data_service import get_climate_data, calculate_trend_statistics, get_rome_heat_islands, VARIABLES_METADATA
from routing_service import get_scenarios

# ---------------------------------------------------------
# Page Configuration & Space Apps Brand Identity
# ---------------------------------------------------------
st.set_page_config(
    page_title="IntrepidOne | NASA Trend Detective & Cool Routes",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS adhering strictly to Space_Apps_Brand_Guide_VUGpVJm.md
# Primary Palette: Deep Blue (#07173F), Electric Blue (#0042A6), Neon Yellow (#EAFE07), Neon Blue (#2E96F5)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Fira+Sans:wght@700;900&family=Overpass:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Overpass', sans-serif;
        color: #FFFFFF;
    }

    .stApp {
        background-color: #07173F;
        background-image: radial-gradient(circle at 10% 20%, rgba(0, 66, 166, 0.4) 0%, rgba(7, 23, 63, 0.95) 90%);
    }

    h1, h2, h3 {
        font-family: 'Fira Sans', sans-serif;
        font-weight: 900;
        letter-spacing: -0.5px;
    }

    /* Brand Header Card with 45° Gradient */
    .brand-hero {
        background: linear-gradient(135deg, #0042A6 0%, #07173F 100%);
        border: 1px solid rgba(46, 150, 245, 0.3);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    }

    .hero-title {
        font-size: 2.2rem;
        color: #FFFFFF;
        margin: 0;
        font-family: 'Fira Sans', sans-serif;
    }

    .hero-tagline {
        color: #EAFE07;
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 6px;
    }

    .hero-sub {
        color: #E0E8F5;
        font-size: 0.95rem;
        margin-top: 8px;
    }

    /* Stat Cards */
    .metric-card {
        background: rgba(0, 66, 166, 0.25);
        border-left: 4px solid #EAFE07;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
        backdrop-filter: blur(4px);
    }

    .metric-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        color: #2E96F5;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 900;
        color: #FFFFFF;
        font-family: 'Fira Sans', sans-serif;
        margin: 4px 0;
    }

    .metric-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 700;
        font-family: 'Fira Code', monospace;
    }

    .badge-sig {
        background-color: rgba(234, 254, 7, 0.2);
        color: #EAFE07;
        border: 1px solid #EAFE07;
    }

    .badge-alert {
        background-color: rgba(228, 55, 0, 0.2);
        color: #FF5A36;
        border: 1px solid #E43700;
    }

    .badge-cool {
        background-color: rgba(0, 240, 255, 0.2);
        color: #00F0FF;
        border: 1px solid #00F0FF;
    }

    /* Custom Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(7, 23, 63, 0.6);
        padding: 8px;
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        color: #E0E8F5;
        font-family: 'Overpass', sans-serif;
        font-weight: 600;
        border-radius: 6px;
        padding: 10px 18px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #0042A6 !important;
        color: #EAFE07 !important;
        border-bottom: 2px solid #EAFE07 !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #05102B;
        border-right: 1px solid rgba(46, 150, 245, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar Controls & City Selector
# ---------------------------------------------------------
with st.sidebar:
    # Space Apps Official Logo
    logo_path = os.path.join(os.path.dirname(__file__), "ui", "NASA Space Apps Logos - 2026", "Space Apps Logo Color and White.png")
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown("<h2 style='color:#EAFE07;'>🛰️ SPACE APPS 2026</h2>", unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Study Configuration")

    city_options = {
        "Rome (Tor Vergata & Historic Center)": {"lat": 41.9028, "lon": 12.4964},
        "Milan": {"lat": 45.4642, "lon": 9.1900},
        "Naples": {"lat": 40.8518, "lon": 14.2681},
        "Florence": {"lat": 43.7696, "lon": 11.2558}
    }

    selected_city_name = st.selectbox("Select Study Region:", list(city_options.keys()), index=0)
    city_coords = city_options[selected_city_name]

    var_options = {
        "T2M": "T2M - Mean Air Temp (2m)",
        "T2M_MAX": "T2M_MAX - Daily Max Summer Temp",
        "TS": "TS - Land Surface Temp (LST)",
        "ALLSKY_SFC_SW_DWN": "ALLSKY - Downward Solar Irradiance"
    }
    selected_var_code = st.selectbox("NASA Earth Science Variable:", list(var_options.keys()), format_func=lambda x: var_options[x], index=0)

    season_choice = st.radio("Seasonal Scope:", ["Full Year (Global Climatology)", "Summer Months Only (Jun-Jul-Aug)"], index=1)

    start_year = st.slider("Analysis Start Year:", 1995, 2015, 1995)
    end_year = 2024

    st.markdown("---")
    st.markdown("""
    **Rome 2026 Mission Event:**
    - **Local Lead**: Dr. Youcef Yahi
    - **Host Venue**: University of Rome Tor Vergata
    - **Team**: IntrepidOne
    - **Team Owner**: Alessandro Intropido *(Solo Participant)*
    """)

# ---------------------------------------------------------
# Hero Banner
# ---------------------------------------------------------
st.markdown(f"""
<div class="brand-hero">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
        <div>
            <h1 class="hero-title">INTREPID ONE: Earth System Trend Detective</h1>
            <div class="hero-tagline">Scientific Climate Trend Detection & Urban Cool-Shade Navigation</div>
            <div class="hero-sub">NASA GMAO MERRA-2 Assimilation • MODIS Land Surface Temperature • Urban Shadow & Canopy Model</div>
        </div>
        <div style="text-align:right;">
            <span class="metric-badge badge-sig">NASA SPACE APPS 2026</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Fetch Data
with st.spinner("Retrieving NASA Earth Science records..."):
    climate_bundle = get_climate_data(lat=city_coords["lat"], lon=city_coords["lon"], start_year=start_year, end_year=end_year)

df_to_analyze = climate_bundle["summer"] if "Summer Months" in season_choice else climate_bundle["annual"]
stats = calculate_trend_statistics(df_to_analyze, variable=selected_var_code)
var_meta = VARIABLES_METADATA.get(selected_var_code, {"name": selected_var_code, "unit": "°C", "description": ""})

# ---------------------------------------------------------
# Main Tabs
# ---------------------------------------------------------
tab_trends, tab_map, tab_method = st.tabs([
    "📈 1. Trend Detective (Scientific Evidence)",
    "🗺️ 2. Thermal Map & Cool Routes (Urban Action)",
    "🔬 3. Methodology & NASA Judging Criteria"
])

# =========================================================
# TAB 1: Trend Detective
# =========================================================
with tab_trends:
    st.markdown(f"### Temporal Trend Analysis: **{var_meta['name']}** ({selected_city_name})")
    st.caption(f"Timeframe: {start_year} - {end_year} • {season_choice} • Source: NASA POWER API (MERRA-2 Model)")

    # 4 Key Scientific Metric Cards
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        trend_label = "INCREASING ↗" if stats["trend"] == "increasing" else ("DECREASING ↘" if stats["trend"] == "decreasing" else "STABLE ➔")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Trend Direction</div>
            <div class="metric-value" style="color: {'#FF5A36' if stats['trend'] == 'increasing' else '#EAFE07'};">{trend_label}</div>
            <span class="metric-badge {'badge-alert' if stats['trend'] == 'increasing' else 'badge-cool'}">{stats['trend'].upper()}</span>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Sen's Slope (Decadal Rate)</div>
            <div class="metric-value">+{stats['sen_slope_decade']:.2f} {var_meta['unit']}</div>
            <span class="metric-badge badge-sig">per decade</span>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        p_val_str = f"{stats['p_value']:.2e}" if stats['p_value'] < 0.001 else f"{stats['p_value']:.4f}"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Significance (Mann-Kendall)</div>
            <div class="metric-value" style="color:#EAFE07;">{'YES (p < 0.05)' if stats['is_significant'] else 'NOT SIGNIFICANT'}</div>
            <span class="metric-badge badge-sig">p-value = {p_val_str}</span>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        delta_warming = stats['recent_mean'] - stats['baseline_mean']
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Observed Change</div>
            <div class="metric-value">+{delta_warming:.2f} {var_meta['unit']}</div>
            <span class="metric-badge badge-alert">vs {start_year}-{start_year+9} baseline</span>
        </div>
        """, unsafe_allow_html=True)

    # Plotly Chart: Time series with Sen's slope line & 5-year moving average
    fig_trend = go.Figure()

    # Observed points
    fig_trend.add_trace(go.Scatter(
        x=stats["years"],
        y=stats["observed_values"],
        mode="markers+lines",
        name="NASA Observed Value",
        line=dict(color="#2E96F5", width=2),
        marker=dict(size=7, color="#2E96F5", symbol="circle")
    ))

    # Rolling 5-year average
    fig_trend.add_trace(go.Scatter(
        x=stats["years"],
        y=stats["rolling_5y"],
        mode="lines",
        name="5-Year Moving Average",
        line=dict(color="#EAFE07", width=3, dash="dash")
    ))

    # Theil-Sen Trend Line
    fig_trend.add_trace(go.Scatter(
        x=stats["years"],
        y=stats["trend_line"],
        mode="lines",
        name=f"Sen's Slope (+{stats['sen_slope_decade']:.2f} {var_meta['unit']}/decade)",
        line=dict(color="#E43700", width=3)
    ))

    fig_trend.update_layout(
        title=dict(
            text=f"<b>Temporal Trajectory & Sen's Slope Trendline</b>: {var_meta['name']}",
            font=dict(family="Fira Sans", size=18, color="#FFFFFF")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(7, 23, 63, 0.7)",
        xaxis=dict(
            title="Year",
            gridcolor="rgba(46, 150, 245, 0.15)",
            tickmode="linear",
            dtick=3,
            color="#E0E8F5"
        ),
        yaxis=dict(
            title=f"{var_meta['name']} ({var_meta['unit']})",
            gridcolor="rgba(46, 150, 245, 0.15)",
            color="#E0E8F5"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#FFFFFF")
        ),
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode="x unified"
    )

    st.plotly_chart(fig_trend, use_container_width=True)

    # Anomaly Bars Plotly Chart
    fig_anomaly = go.Figure()
    bar_colors = ["#E43700" if a >= 0 else "#2E96F5" for a in stats["anomalies"]]
    fig_anomaly.add_trace(go.Bar(
        x=stats["years"],
        y=stats["anomalies"],
        marker_color=bar_colors,
        name="Thermal Anomaly",
        hovertemplate="Year %{x}: %{y:+.2f} " + var_meta["unit"] + "<extra></extra>"
    ))
    fig_anomaly.update_layout(
        title=dict(
            text=f"<b>Annual Anomalies Relative to Baseline Decade</b> ({stats['baseline_mean']:.2f} {var_meta['unit']})",
            font=dict(family="Fira Sans", size=16, color="#FFFFFF")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(7, 23, 63, 0.7)",
        xaxis=dict(title="Year", gridcolor="rgba(46, 150, 245, 0.15)", tickmode="linear", dtick=3, color="#E0E8F5"),
        yaxis=dict(title=f"Anomaly Delta ({var_meta['unit']})", gridcolor="rgba(46, 150, 245, 0.15)", color="#E0E8F5"),
        margin=dict(l=40, r=40, t=50, b=40)
    )
    st.plotly_chart(fig_anomaly, use_container_width=True)

    # Scientific Verdict Callout Box
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #2E96F5; margin-top: 16px;">
        <div class="metric-label" style="font-size: 0.95rem; margin-bottom: 8px;">🔬 Earth System Trend Summary</div>
        <ul style="margin: 0; padding-left: 20px; color: #FFFFFF; line-height: 1.6;">
            <li><b>What is changing?</b> {var_meta['name']} across {selected_city_name}.</li>
            <li><b>Where is it changing?</b> Regional urban warming concentrated inside expanding Urban Heat Islands (UHI).</li>
            <li><b>How much is it changing?</b> Robust Sen's slope of <b>{stats['sen_slope_decade']:+.2f} {var_meta['unit']} per decade</b> ({delta_warming:+.2f} {var_meta['unit']} total change over the study period).</li>
            <li><b>Is it statistically significant?</b> <b>{'Yes' if stats['is_significant'] else 'No'}.</b> The non-parametric Mann-Kendall test yields <b>p-value = {p_val_str}</b> ({'below' if stats['is_significant'] else 'above'} the canonical significance threshold &alpha; = 0.05).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# TAB 2: Thermal Map & Cool Routes (Urban Action)
# =========================================================
with tab_map:
    st.markdown("### 🗺️ Urban Resilience Navigator: Thermal Surface Heat & Cool Shaded Paths")
    st.write("Given the verified warming trend, this tool transforms satellite climate data into pedestrian protection, identifying heat islands and calculating shade-optimized walking routes.")

    scenarios = get_scenarios()
    scen_col1, scen_col2 = st.columns([1, 2])

    with scen_col1:
        chosen_scen_id = st.selectbox(
            "Select Rome Urban Scenario:",
            list(scenarios.keys()),
            format_func=lambda x: scenarios[x]["title"]
        )
        current_scen = scenarios[chosen_scen_id]

        st.info(f"📍 **Scenario**: {current_scen['description']}")

        direct = current_scen["direct_route"]
        cool = current_scen["cool_route"]

        # Comparison Card
        st.markdown("#### ⚖️ Route Comparison:")
        
        st.markdown(f"""
        <div style="background:rgba(228, 55, 0, 0.15); border:1px solid #E43700; border-radius:8px; padding:12px; margin-bottom:10px;">
            <b style="color:#FF5A36;">🔴 {direct['name']}</b><br>
            • <b>Distance</b>: {direct['distance_km']} km (~{direct['walk_time_min']} min)<br>
            • <b>Shade Coverage</b>: {direct['shade_percent']}%<br>
            • <b>Estimated Surface Temp</b>: <b>{direct['avg_temp_c']} °C</b><br>
            • <b>Heat Stress Level</b>: {direct['heat_stress']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:rgba(0, 240, 255, 0.15); border:1px solid #00F0FF; border-radius:8px; padding:12px; margin-bottom:10px;">
            <b style="color:#00F0FF;">🟢 {cool['name']}</b><br>
            • <b>Distance</b>: {cool['distance_km']} km (~{cool['walk_time_min']} min)<br>
            • <b>Shade Coverage</b>: <b style="color:#EAFE07;">{cool['shade_percent']}% (+{cool['shade_percent'] - direct['shade_percent']}%)</b><br>
            • <b>Estimated Surface Temp</b>: <b style="color:#00F0FF;">{cool['avg_temp_c']} °C (-{direct['avg_temp_c'] - cool['avg_temp_c']:.1f} °C)</b><br>
            • <b>Heat Stress Level</b>: {cool['heat_stress']}
        </div>
        """, unsafe_allow_html=True)

        st.success(f"💡 **Takeaway**: By walking only +{int((cool['distance_km'] - direct['distance_km'])*1000)} extra meters, you avoid extreme solar exposure and reduce heat stress by **-{direct['avg_temp_c'] - cool['avg_temp_c']:.1f} °C**!")

    with scen_col2:
        # Build Folium Map with clean OpenStreetMap tiles (no watermarks)
        m = folium.Map(
            location=current_scen["center"],
            zoom_start=current_scen["zoom"],
            tiles="OpenStreetMap",
            control_scale=True
        )

        # Add Heatmap Layer representing Urban Heat Island (UHI) intensity in Rome
        heat_points = get_rome_heat_islands()
        heat_data = [[hp["lat"], hp["lon"], hp["surface_temp"] / 10.0] for hp in heat_points]
        HeatMap(heat_data, radius=25, blur=18, min_opacity=0.35, max_zoom=16).add_to(m)

        # Add Hotspot / Cool Island Markers
        for hp in heat_points:
            is_hot = hp["anomaly_c"] > 0
            folium.CircleMarker(
                location=[hp["lat"], hp["lon"]],
                radius=8 if is_hot else 10,
                color="#E43700" if is_hot else "#00F0FF",
                fill=True,
                fill_color="#E43700" if is_hot else "#00F0FF",
                fill_opacity=0.8,
                tooltip=f"<b>{hp['name']}</b><br>Type: {hp['type']}<br>Thermal Anomaly: {hp['anomaly_c']:+.1f}°C<br>Surface Temp: {hp['surface_temp']}°C"
            ).add_to(m)

        # Draw Direct Route (Red Line)
        folium.PolyLine(
            locations=direct["waypoints"],
            color="#E43700",
            weight=5,
            opacity=0.85,
            tooltip=f"{direct['name']} - Temp: {direct['avg_temp_c']}°C (Shade: {direct['shade_percent']}%)",
            dash_array="8, 6"
        ).add_to(m)

        # Draw Cool Route (Cyan Line)
        folium.PolyLine(
            locations=cool["waypoints"],
            color="#00F0FF",
            weight=6,
            opacity=0.95,
            tooltip=f"{cool['name']} - Temp: {cool['avg_temp_c']}°C (Shade: {cool['shade_percent']}%)"
        ).add_to(m)

        # Start and Finish Markers
        start_pt = direct["waypoints"][0]
        end_pt = direct["waypoints"][-1]
        folium.Marker(start_pt, popup="Starting Point", icon=folium.Icon(color="green", icon="play")).add_to(m)
        folium.Marker(end_pt, popup="Destination", icon=folium.Icon(color="red", icon="flag")).add_to(m)

        # Render Map in Streamlit using native folium HTML representation
        components.html(m._repr_html_(), height=540)

    st.caption("Map Legend: Red dashed line = Direct sun-exposed route (High heat stress) | Solid cyan line = Shaded & cool route | Red/Blue circles = Urban Heat Islands / Cool green oases.")

# =========================================================
# TAB 3: Methodology & NASA Criteria
# =========================================================
with tab_method:
    st.markdown("### 🔬 Scientific Methodology & Civic Impact Framework")

    col_meta1, col_meta2 = st.columns([1, 1])

    with col_meta1:
        st.markdown("""
        #### 🛰️ NASA Data & Computation Pipeline
        1. **NASA POWER API (MERRA-2 Data Assimilation)**:
           - Continuous 30-year climate records (1995-2024) of 2-meter air temperature ($T_{2m}$), maximum temperature ($T_{2m\\text{ Max}}$), radiative surface skin temperature ($T_{skin}$), and shortwave downward insolation.
           - Global geophysical reanalysis and assimilation model rigorously validated against satellite radiometry and surface observations.
        2. **Earth System Trend Detective (Statistical Engine)**:
           - **Mann-Kendall Non-Parametric Test**: evaluates monotonic trends over time without assuming normally distributed residuals.
           - **Sen's Slope Estimator**: median slope across all sample point pairs, highly resilient against extreme climatic outliers and noise.
           - **P-Value (Statistical Significance)**: verifies whether the probability of the trend occurring purely by random chance is strictly below the 5% alpha threshold ($p < 0.05$).
        3. **Urban Shadow & Microclimate Routing (Prototype)**:
           - Combines building height-to-width ($H/W$) aspect ratios in urban canyons with tree canopy coverage to estimate mean radiant temperature and shaded pedestrian corridors across Rome.
        """)

        st.info(
            "**Prototype Scope & Transparency:** While the 30-year climate trend analysis is computed directly from real NASA POWER (MERRA-2) records, the street-level routing module currently uses a parametric microclimate simulation for Rome as a proof-of-concept—designed to integrate high-resolution NASA ECOSTRESS/Landsat Land Surface Temperature layers and OpenStreetMap 3D building/tree data in production."
        )

    with col_meta2:
        st.markdown("""
        #### 🌍 Operational Value & Design Principles (Rome 2026)
        - **Civic & Urban Impact**: Protects daily commuters, tourists, and vulnerable citizens from summer heat stress while offering urban planners clear evidence for green corridors.
        - **Translational Innovation**: Bridges macro Earth science satellite observations directly with street-level pedestrian micro-routing.
        - **Scientific Validity**: Built on peer-reviewed non-parametric statistical methods (Mann-Kendall + Sen's Slope) and verified NASA open datasets.
        - **Challenge Relevance**: Directly answers the four core Earth system questions: *what is changing, where it is changing, how much, and whether it is statistically significant*.
        - **Accessible Presentation**: Designed in accordance with NASA Space Apps 2026 Brand Guidelines and WCAG visual contrast standards.
        """)

    st.markdown("---")
    st.markdown("#### 📥 Export Analyzed Climate Data")
    csv_bytes = df_to_analyze.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Processed Dataset (CSV)",
        data=csv_bytes,
        file_name=f"nasa_trend_{selected_city_name}_{selected_var_code}_{start_year}_2024.csv",
        mime="text/csv"
    )
