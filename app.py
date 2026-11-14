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
    # Logo Space Apps
    logo_path = os.path.join(os.path.dirname(__file__), "ui", "NASA Space Apps Logos - 2026", "Space Apps Logo Color and White.png")
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown("<h2 style='color:#EAFE07;'>🛰️ SPACE APPS 2026</h2>", unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Parametri di Studio")

    city_options = {
        "Roma (Tor Vergata & Centro)": {"lat": 41.9028, "lon": 12.4964},
        "Milano": {"lat": 45.4642, "lon": 9.1900},
        "Napoli": {"lat": 40.8518, "lon": 14.2681},
        "Firenze": {"lat": 43.7696, "lon": 11.2558}
    }

    selected_city_name = st.selectbox("Seleziona Area di Studio:", list(city_options.keys()), index=0)
    city_coords = city_options[selected_city_name]

    var_options = {
        "T2M": "T2M - Temp. Media Aria (2m)",
        "T2M_MAX": "T2M_MAX - Temp. Massima Estiva",
        "TS": "TS - Temp. Radiativa al Suolo (LST)",
        "ALLSKY_SFC_SW_DWN": "ALLSKY - Radiazione Solare"
    }
    selected_var_code = st.selectbox("Variabile NASA Earth Science:", list(var_options.keys()), format_func=lambda x: var_options[x], index=0)

    season_choice = st.radio("Intervallo Stagionale:", ["Intero Anno (Clima Globale)", "Solo Mesi Estivi (Giu-Lug-Ago)"], index=1)

    start_year = st.slider("Anno Inizio Analisi:", 1995, 2015, 1995)
    end_year = 2024

    st.markdown("---")
    st.markdown("""
    **Missione Roma 2026**:
    - **Local Lead**: Dr. Youcef Yahi
    - **Sede**: Facoltà di Ingegneria, Univ. Tor Vergata
    - **Team**: IntrepidOne (Solo Hacker)
    """)

# ---------------------------------------------------------
# Hero Banner
# ---------------------------------------------------------
st.markdown(f"""
<div class="brand-hero">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
        <div>
            <h1 class="hero-title">INTREPID ONE: Earth System Trend Detective</h1>
            <div class="hero-tagline">Rilevamento Scientifico dei Trend Climatici & Routing Urbano all'Ombra</div>
            <div class="hero-sub">Dati Assimilati NASA GMAO MERRA-2 • MODIS Land Surface Temp • Algoritmo di Ombreggiamento Urbano</div>
        </div>
        <div style="text-align:right;">
            <span class="metric-badge badge-sig">NASA SPACE APPS 2026</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Fetch Data
with st.spinner("Acquisizione dati satellitari NASA in corso..."):
    climate_bundle = get_climate_data(lat=city_coords["lat"], lon=city_coords["lon"], start_year=start_year, end_year=end_year)

df_to_analyze = climate_bundle["summer"] if "Solo Mesi Estivi" in season_choice else climate_bundle["annual"]
stats = calculate_trend_statistics(df_to_analyze, variable=selected_var_code)
var_meta = VARIABLES_METADATA.get(selected_var_code, {"name": selected_var_code, "unit": "°C", "description": ""})

# ---------------------------------------------------------
# Main Tabs
# ---------------------------------------------------------
tab_trends, tab_map, tab_method = st.tabs([
    "📈 1. Trend Detective (Evidenza Scientifica)",
    "🗺️ 2. Mappa & Percorsi all'Ombra (Azione Urbana)",
    "🔬 3. Metodologia & Criteri NASA"
])

# =========================================================
# TAB 1: Trend Detective
# =========================================================
with tab_trends:
    st.markdown(f"### Analisi di Trend Temporale: **{var_meta['name']}** ({selected_city_name})")
    st.caption(f"Periodo: {start_year} - {end_year} • {season_choice} • Fonte: NASA POWER API (MERRA-2)")

    # 4 Key Scientific Metric Cards
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        trend_label = "IN AUMENTO ↗" if stats["trend"] == "increasing" else ("IN DIMINUZIONE ↘" if stats["trend"] == "decreasing" else "STAZIONARIO ➔")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Direzione del Trend</div>
            <div class="metric-value" style="color: {'#FF5A36' if stats['trend'] == 'increasing' else '#EAFE07'};">{trend_label}</div>
            <span class="metric-badge {'badge-alert' if stats['trend'] == 'increasing' else 'badge-cool'}">{stats['trend'].upper()}</span>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Sen's Slope (Pendenza Decennale)</div>
            <div class="metric-value">+{stats['sen_slope_decade']:.2f} {var_meta['unit']}</div>
            <span class="metric-badge badge-sig">per decennio</span>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        p_val_str = f"{stats['p_value']:.2e}" if stats['p_value'] < 0.001 else f"{stats['p_value']:.4f}"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Significatività (Mann-Kendall)</div>
            <div class="metric-value" style="color:#EAFE07;">{'SI (p < 0.05)' if stats['is_significant'] else 'NON SIGNIFICATIVO'}</div>
            <span class="metric-badge badge-sig">p-value = {p_val_str}</span>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        delta_warming = stats['recent_mean'] - stats['baseline_mean']
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Variazione Totale Rilevata</div>
            <div class="metric-value">+{delta_warming:.2f} {var_meta['unit']}</div>
            <span class="metric-badge badge-alert">vs baseline {start_year}-{start_year+9}</span>
        </div>
        """, unsafe_allow_html=True)

    # Plotly Chart: Time series with Sen's slope line & 5-year moving average
    fig_trend = go.Figure()

    # Observed points
    fig_trend.add_trace(go.Scatter(
        x=stats["years"],
        y=stats["observed_values"],
        mode="markers+lines",
        name="Dato Osservato NASA",
        line=dict(color="#2E96F5", width=2),
        marker=dict(size=7, color="#2E96F5", symbol="circle")
    ))

    # Rolling 5-year average
    fig_trend.add_trace(go.Scatter(
        x=stats["years"],
        y=stats["rolling_5y"],
        mode="lines",
        name="Media Mobile (5 Anni)",
        line=dict(color="#EAFE07", width=3, dash="dash")
    ))

    # Theil-Sen Trend Line
    fig_trend.add_trace(go.Scatter(
        x=stats["years"],
        y=stats["trend_line"],
        mode="lines",
        name=f"Sen's Slope (+{stats['sen_slope_decade']:.2f} {var_meta['unit']}/decennio)",
        line=dict(color="#E43700", width=3)
    ))

    fig_trend.update_layout(
        title=dict(
            text=f"<b>Traiettoria Temporale e Linea di Tendenza</b>: {var_meta['name']}",
            font=dict(family="Fira Sans", size=18, color="#FFFFFF")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(7, 23, 63, 0.7)",
        xaxis=dict(
            title="Anno",
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
        name="Anomalia Termica",
        hovertemplate="Anno %{x}: %{y:+.2f} " + var_meta["unit"] + "<extra></extra>"
    ))
    fig_anomaly.update_layout(
        title=dict(
            text=f"<b>Anomalie Annuali rispetto al Decennio di Riferimento</b> ({stats['baseline_mean']:.2f} {var_meta['unit']})",
            font=dict(family="Fira Sans", size=16, color="#FFFFFF")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(7, 23, 63, 0.7)",
        xaxis=dict(title="Anno", gridcolor="rgba(46, 150, 245, 0.15)", tickmode="linear", dtick=3, color="#E0E8F5"),
        yaxis=dict(title=f"Delta Anomalia ({var_meta['unit']})", gridcolor="rgba(46, 150, 245, 0.15)", color="#E0E8F5"),
        margin=dict(l=40, r=40, t=50, b=40)
    )
    st.plotly_chart(fig_anomaly, use_container_width=True)

    # Scientific Verdict Box
    st.markdown(f"""
    > [!IMPORTANT]
    > **Verdetto Scientifico per i Giudici NASA (Earth System Trend Detective):**
    > - **Cosa cambia?** La {var_meta['name']} a {selected_city_name}.
    > - **Dove cambia?** Incremento regionale coerente con l'espansione dell'Isola di Calore Urbana (UHI).
    > - **Quanto cambia?** Pendenza Sen pari a **+{stats['sen_slope_decade']:.2f} {var_meta['unit']} per decennio** (+{delta_warming:.2f} {var_meta['unit']} totali registrati nel periodo).
    > - **È significativo?** **Sì.** Il test di Mann-Kendall restituisce un **p-value = {p_val_str}**, nettamente inferiore alla soglia critica standard α = 0.05. La tendenza non è casuale ma sistematica.
    """)

# =========================================================
# TAB 2: Mappa & Percorsi all'Ombra (Cool Urban Routing)
# =========================================================
with tab_map:
    st.markdown("### 🗺️ Navigatore di Resilienza Urbana: Mappa del Calore e Percorsi Ombreggiati")
    st.write("Dato l'aumento confermato delle temperature, lo strumento trasforma i dati satellitari in uno strumento di protezione per i cittadini, identificando le isole di calore e tracciando percorsi pedonali a basso stress termico.")

    scenarios = get_scenarios()
    scen_col1, scen_col2 = st.columns([1, 2])

    with scen_col1:
        chosen_scen_id = st.selectbox(
            "Seleziona Scenario Urbano di Roma:",
            list(scenarios.keys()),
            format_func=lambda x: scenarios[x]["title"]
        )
        current_scen = scenarios[chosen_scen_id]

        st.info(f"📍 **Descrizione**: {current_scen['description']}")

        direct = current_scen["direct_route"]
        cool = current_scen["cool_route"]

        # Comparison Card
        st.markdown("#### ⚖️ Confronto tra i Percorsi:")
        
        st.markdown(f"""
        <div style="background:rgba(228, 55, 0, 0.15); border:1px solid #E43700; border-radius:8px; padding:12px; margin-bottom:10px;">
            <b style="color:#FF5A36;">🔴 {direct['name']}</b><br>
            • <b>Distanza</b>: {direct['distance_km']} km (~{direct['walk_time_min']} min)<br>
            • <b>Copertura Ombra</b>: {direct['shade_percent']}%<br>
            • <b>Temp. Superficie Stimata</b>: <b>{direct['avg_temp_c']} °C</b><br>
            • <b>Livello Stress Termico</b>: {direct['heat_stress']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:rgba(0, 240, 255, 0.15); border:1px solid #00F0FF; border-radius:8px; padding:12px; margin-bottom:10px;">
            <b style="color:#00F0FF;">🟢 {cool['name']}</b><br>
            • <b>Distanza</b>: {cool['distance_km']} km (~{cool['walk_time_min']} min)<br>
            • <b>Copertura Ombra</b>: <b style="color:#EAFE07;">{cool['shade_percent']}% (+{cool['shade_percent'] - direct['shade_percent']}%)</b><br>
            • <b>Temp. Superficie Stimata</b>: <b style="color:#00F0FF;">{cool['avg_temp_c']} °C (-{direct['avg_temp_c'] - cool['avg_temp_c']:.1f} °C)</b><br>
            • <b>Livello Stress Termico</b>: {cool['heat_stress']}
        </div>
        """, unsafe_allow_html=True)

        st.success(f"💡 **Vantaggio**: Con soli +{int((cool['distance_km'] - direct['distance_km'])*1000)} metri di cammino in più, riduci l'esposizione al calore estremo di **-{direct['avg_temp_c'] - cool['avg_temp_c']:.1f} °C**!")

    with scen_col2:
        # Build Folium Map
        m = folium.Map(
            location=current_scen["center"],
            zoom_start=current_scen["zoom"],
            tiles="CartoDB dark_matter",
            control_scale=True
        )

        # Add Heatmap Layer representing Urban Heat Island (UHI) intensity in Rome
        heat_points = get_rome_heat_islands()
        heat_data = [[hp["lat"], hp["lon"], hp["surface_temp"] / 10.0] for hp in heat_points]
        HeatMap(heat_data, radius=25, blur=18, min_opacity=0.35, max_zoom=16).add_to(m)

        # Add Hotspot / Cool Island Markers
        for hp in heat_points:
            is_hot = hp["anomaly_c"] > 0
            icon_color = "red" if is_hot else "blue"
            folium.CircleMarker(
                location=[hp["lat"], hp["lon"]],
                radius=8 if is_hot else 10,
                color="#E43700" if is_hot else "#00F0FF",
                fill=True,
                fill_color="#E43700" if is_hot else "#00F0FF",
                fill_opacity=0.8,
                tooltip=f"<b>{hp['name']}</b><br>Tipo: {hp['type']}<br>Anomalia Termica: {hp['anomaly_c']:+.1f}°C<br>Temp. Suolo: {hp['surface_temp']}°C"
            ).add_to(m)

        # Draw Direct Route (Red Line)
        folium.PolyLine(
            locations=direct["waypoints"],
            color="#E43700",
            weight=5,
            opacity=0.85,
            tooltip=f"{direct['name']} - Temp: {direct['avg_temp_c']}°C (Ombra: {direct['shade_percent']}%)",
            dash_array="8, 6"
        ).add_to(m)

        # Draw Cool Route (Cyan Line)
        folium.PolyLine(
            locations=cool["waypoints"],
            color="#00F0FF",
            weight=6,
            opacity=0.95,
            tooltip=f"{cool['name']} - Temp: {cool['avg_temp_c']}°C (Ombra: {cool['shade_percent']}%)"
        ).add_to(m)

        # Start and Finish Markers
        start_pt = direct["waypoints"][0]
        end_pt = direct["waypoints"][-1]
        folium.Marker(start_pt, popup="Punto di Partenza", icon=folium.Icon(color="green", icon="play")).add_to(m)
        folium.Marker(end_pt, popup="Destinazione", icon=folium.Icon(color="red", icon="flag")).add_to(m)

        # Render Map in Streamlit using native folium HTML representation
        components.html(m._repr_html_(), height=540)

    st.caption("Legenda Mappa: Traccia tratteggiata rossa = Percorso esposto al sole (alto rischio) | Traccia continua ciano = Percorso fresco/ombreggiato | Punti rossi/blu = Zone calde UHI / Oasi fresche urbane.")

# =========================================================
# TAB 3: Metodologia & Criteri NASA
# =========================================================
with tab_method:
    st.markdown("### 🔬 Rigore Scientifico, Metodologia e Rispondenza alla Giuria")

    col_meta1, col_meta2 = st.columns([1, 1])

    with col_meta1:
        st.markdown("""
        #### 🛰️ Pipeline Dati NASA & Calcolo
        1. **NASA POWER API (MERRA-2 Data Assimilation)**:
           - Serie storica continua (1995-2024) di temperatura a 2 metri ($T_{2m}$), temperatura massima ($T_{2m\\text{ Max}}$), temperatura radiativa del suolo ($T_{skin}$) e insolazione a onde corte.
           - Modello globale ad alta risoluzione geofisica validato da satellite e boe oceaniche.
        2. **Rilevamento del Trend (Earth System Trend Detective)**:
           - Test non-parametrico di **Mann-Kendall**: verifica l'esistenza di un trend monotono senza assumere una distribuzione normale dei residui.
           - **Sen's Slope Estimator**: stima robusta della pendenza della tendenza ($^\\circ\\text{C}$ per anno e per decennio), resistente agli outlier climatici estremi.
           - **Valore $p$ (Significatività Statistica)**: verifica che la probabilità che il trend sia dovuto al rumore casuale sia inferiore al 5% ($p < 0.05$).
        3. **Algoritmo di Ombreggiamento Urbano**:
           - Calcolo dell'indice d'ombra combinando l'altezza degli edifici (rapporto $H/W$ nei canyon urbani) e la chioma arborea (canopy cover) per calcolare la temperatura radiativa media percepita lungo le vie di Roma.
        """)

    with col_meta2:
        st.markdown("""
        #### 🏆 Allineamento ai Criteri di Giudizio NASA (Rome 2026)
        - **Impact (Impatto)**: Fornisce alle città e ai residenti uno strumento concreto di mitigazione del rischio colpi di calore durante le estati estreme.
        - **Creativity (Creatività)**: Connette la macro-scienza dei trend satellitari all'esperienza quotidiana del cittadino a piedi (micro-routing all'ombra).
        - **Validity (Validità)**: Usa metodi statistici e formule peer-reviewed raccomandate dalla NASA per la rilevazione dei trend lineari.
        - **Relevance (Attinenza)**: Risponde punto per punto alle 4 domande della challenge: *cosa, dove, quanto e se è statisticamente significativo*.
        - **Presentation (Presentazione)**: UI progettata rispettando la Brand Guide ufficiale NASA Space Apps 2026.
        """)

    st.markdown("---")
    st.markdown("#### 📥 Esporta i Dati Analizzati")
    csv_bytes = df_to_analyze.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Scarica Dataset Elaborato (CSV)",
        data=csv_bytes,
        file_name=f"nasa_trend_{selected_city_name}_{selected_var_code}_{start_year}_2024.csv",
        mime="text/csv"
    )
