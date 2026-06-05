# USGS Earthquakes Past 30 Days — Data Visualization Dashboard

**Course:** Exploratory Data Analysis  
**Instructor:** Ali Hassan Sherazi  
**Dataset:** `2_5_month.csv` (USGS Earthquake Hazards Program)

---

## Project Structure

```
dashboard_project/
├── data/
│   └── 2_5_month.csv
├── notebooks/
│   └── analysis.ipynb
├── app.py
├── charts.py
├── filters.py
├── requirements.txt
└── README.md
```

---

## Installation & Running

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the dashboard
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## Dashboard Features

**10 Chart Types:**
1. Pie Chart — Magnitude category distribution
2. Histogram — Magnitude frequency
3. Line Chart — Daily event count over time
4. Bar Chart — Top seismic networks
5. Scatter Plot — Depth vs Magnitude relationship
6. Box Plot — Depth distribution by magnitude category
7. Heatmap — Feature correlation matrix
8. Area Chart — Average daily magnitude trend
9. Count Plot — Events by magnitude type
10. Violin Plot — Magnitude distribution by category

**6 Interactive Filters (all linked to all charts):**
- Date Range Filter
- Magnitude Slider
- Event Type Multi-select
- Network Multi-select
- Location Search/Text Filter
- Reset All Filters Button

**KPI Cards:** Total Events, Avg Magnitude, Max Magnitude, Avg Depth, Max Depth, Unique Locations

---

## Key Insights

- The dataset spans ~2.5 months of global seismic activity (mag ≥ 2.5).
- Majority of earthquakes are Minor to Light in magnitude.
- Alaska and the western US are the most seismically active regions.
- Shallow earthquakes (< 70 km) dominate the dataset.
- Strong positive correlation between `nst` (station count) and data quality metrics.
