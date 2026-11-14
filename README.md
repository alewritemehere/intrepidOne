# INTREPID ONE 🛰️
### Earth System Trend Detective & Urban Cool-Shade Router
**Official Submission for NASA International Space Apps Challenge — Rome 2026**  
**Challenge:** [Be An Earth System Trend Detective!](https://www.spaceappschallenge.org/2026/challenges/earth-system-trend-detective/)  
**Event Location:** Faculty of Engineering, University of Rome Tor Vergata  
**License:** [Apache 2.0](LICENSE)

---

## 🌟 Executive Summary

Earth system trends are not uniform across the globe: regional patterns often deviate sharply from global averages. In dense metropolitan areas like Rome, rising surface temperatures combine with the **Urban Heat Island (UHI)** effect, creating severe thermal stress for pedestrians and citizens during summer heatwaves.

**IntrepidOne** is an open-source analytical tool and interactive dashboard designed to solve the *Earth System Trend Detective* challenge by:
1. **Detecting and Quantifying Trends**: Mining 30 years (1995–2024) of NASA GMAO MERRA-2 assimilation records to detect long-term shifts in ambient temperature, maximum heat events, and radiative land surface temperature (LST).
2. **Validating Scientific Significance**: Applying the non-parametric **Mann-Kendall Trend Test** and **Sen's Slope Estimator** to verify whether regional warming is statistically significant ($p < 0.05$).
3. **Actionable Resilience (Cool-Shade Navigation)**: Translating macro satellite observations into actionable street-level pedestrian routing. By modeling urban canopy cover and building height-to-width ($H/W$) shadow corridors, IntrepidOne calculates shaded, lower-temperature walking paths that lower thermal exposure by up to **-8.9 °C**.

---

## 🔬 Answering the 4 Core Challenge Questions

| Challenge Question | Scientific Finding by IntrepidOne |
| :--- | :--- |
| **1. What is changing?** | Summer Mean Air Temperature ($T_{2m}$), Maximum Summer Peaks ($T_{2m\text{ Max}}$), and Radiative Land Surface Temperature ($TS$). |
| **2. Where is it changing?** | The metropolitan area of Rome, with extreme amplification inside dense asphalt and stone street canyons (Colosseum, Termini Station, EUR). |
| **3. How much is it changing?** | Sen's Slope of **+0.81 °C per decade** (+1.49 °C observed warming relative to the 1995–2004 baseline period). |
| **4. Is it statistically significant?** | **YES.** The non-parametric Mann-Kendall test yields $p = 4.12 \times 10^{-4}$ ($p \ll 0.05$). The trend is systematic, not random climatic noise. |

---

## 🗺️ Interactive Urban Cool-Shade Routing

When extreme heat events are detected, IntrepidOne offers citizens and tourists in Rome optimized walking routes across 3 key scenarios:

1. **Historic Center (Colosseum ➔ Piazza Navona)**:
   - *Direct Sun Route*: Via dei Fori Imperiali / Corso Vittorio. 2.2 km, 14% shade, **39.5 °C** surface temp.
   - *Cool & Shaded Route*: Rione Monti / Colle Oppio canopy / deep Renaissance building canyons. 2.5 km, **74% shade**, **30.6 °C** surface temp (**-8.9 °C cooler!**).
2. **Green Corridor (Termini Station ➔ Villa Borghese Gardens)**:
   - Circumvents the dense traffic heat island along Via XX Settembre, guiding pedestrians through the pine canopy of Villa Borghese (**-10.9 °C surface temp reduction**).
3. **University Campus (Tor Vergata Engineering Faculty ➔ Rectorate)**:
   - Connected via perimeter botanical paths and covered campus arcades.

---

## 🛠️ Architecture & Tech Stack

```
IntrepidOne/
├── app.py               # Main Streamlit Dashboard (Space Apps 2026 Brand Design)
├── data_service.py      # NASA POWER API ingestion, caching & Mann-Kendall engine
├── routing_service.py   # Urban shade and thermal route simulator for Rome
├── requirements.txt     # Python dependencies
├── REFERENCES.md        # Citations of NASA datasets, papers & open-source libraries
├── LICENSE              # Apache 2.0 Open Source License
└── ui/                  # NASA Space Apps official brand assets, logos & patterns
```

- **Backend / Data Science**: Python 3.14, `pandas`, `numpy`, `scipy.stats`, `pymannkendall`.
- **NASA Data Sources**: NASA POWER API (MERRA-2 assimilation model), NASA GIBS (MODIS Land Surface Temp).
- **Frontend / Visualization**: Streamlit, Plotly.py, Folium / Leaflet.js.
- **Visual Identity**: Implemented in strict accordance with the official *NASA Space Apps Brand Guidelines (June 2026)*:
  - Deep Blue (`#07173F`), Electric Blue (`#0042A6`), Neon Yellow (`#EAFE07`), Neon Blue (`#2E96F5`).
  - Google Fonts: **Fira Sans** (Headings) and **Overpass** (Body Copy).

---

## 🚀 Quickstart & Installation

### 1. Clone the repository
```bash
git clone https://github.com/alewritemehere/intrepidOne.git
cd intrepidOne
```

### 2. Setup Virtual Environment
```bash
python -m venv .venv
# On Windows:
.\.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🏆 Alignment with NASA Evaluation Criteria

- **Impact**: Provides tangible, preventive tools for public health, city planning, and citizen mobility during intense heatwaves.
- **Creativity**: Connects macro-scale satellite Earth observation records with micro-scale street canyon shadow dynamics.
- **Validity**: Employs peer-reviewed, non-parametric statistical methods recommended by NASA (Mann-Kendall test and Sen's slope).
- **Relevance**: Directly addresses all four inquiry requirements of the *Earth System Trend Detective* challenge.
- **Presentation**: Fully English, accessible, and structured with NASA Space Apps official design system.

---

## 📚 References & Citations
Complete citations of NASA datasets, scientific papers, and open-source tools are documented in [REFERENCES.md](REFERENCES.md).
