# REFERENCES & DATA SOURCES
**Project:** IntrepidOne - Earth System Trend Detective & Urban Cool-Shade Router  
**Event:** NASA International Space Apps Challenge - Rome 2026  
**Challenge:** Be An Earth System Trend Detective!  
**License:** Apache 2.0 (Open Source)

---

## 1. NASA Earth Science Data & APIs
1. **NASA POWER Project (Prediction Of Worldwide Energy Resources)**
   - **Provider:** NASA Langley Research Center (LaRC)
   - **Model & Source:** NASA GMAO MERRA-2 (Modern-Era Retrospective analysis for Research and Applications, Version 2) and GEOS FP assimilation models.
   - **Parameters used:**
     - `T2M`: Temperature at 2 Meters (°C)
     - `T2M_MAX`: Maximum Temperature at 2 Meters (°C)
     - `TS`: Earth Skin / Surface Temperature (°C)
     - `ALLSKY_SFC_SW_DWN`: All Sky Surface Shortwave Downward Irradiance (kW-hr/m²/day)
   - **API Endpoint:** `https://power.larc.nasa.gov/api/temporal/monthly/point`
   - **Temporal Range:** 1995 – 2024 (30-year historical climate series)

2. **NASA GIBS (Global Imagery Browse Services)**
   - **Provider:** NASA Earth Science Data and Information System (ESDIS) Project
   - **Products:** MODIS Terra & Aqua Land Surface Temperature (Day/Night) 1km (MOD11A1 / MYD11A1)
   - **Portal:** `https://worldview.earthdata.nasa.gov`

## 2. Statistical & Scientific Methodology
1. **Mann-Kendall Trend Test:**
   - Mann, H. B. (1945). *Nonparametric tests against trend.* Econometrica, 13(3), 245-259.
   - Kendall, M. G. (1975). *Rank Correlation Methods.* Charles Griffin, London.
2. **Sen's Slope Estimator:**
   - Sen, P. K. (1968). *Estimates of the regression coefficient based on Kendall's tau.* Journal of the American Statistical Association, 63(324), 1379-1389.
3. **Urban Heat Island & Shaded Pedestrian Comfort:**
   - Oke, T. R. (1982). *The energetic basis of the urban heat island.* Quarterly Journal of the Royal Meteorological Society, 108(455), 1-24.

## 3. Open Source Software & Libraries
- **Python 3.14**: Python Software Foundation License
- **Streamlit**: Apache License 2.0
- **Folium & Branca**: MIT License
- **Plotly.py**: MIT License
- **pandas & NumPy**: BSD 3-Clause License
- **SciPy**: BSD 3-Clause License
- **pymannkendall**: MIT License
- **Requests**: Apache License 2.0
- **OpenStreetMap & CartoDB Dark Matter**: Open Data Commons Open Database License (ODbL) / CartoDB terms.

## 4. Visual Identity & Brand Assets
- NASA Space Apps Brand Guidelines (Version: June 25, 2026)
- Fonts: `Fira Sans` (SIL Open Font License), `Overpass` (SIL OFL), `Fira Code` (SIL OFL) via Google Fonts.
- Official NASA Space Apps Rome 2026 logos and geometric patterns from the official Participant Pack.
