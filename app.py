import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from filters import load_data, apply_filters, get_kpis
from charts import (
    pie_chart, histogram, line_chart, bar_chart, scatter_plot,
    box_plot, heatmap, area_chart, count_plot, violin_plot
)

st.set_page_config(
    page_title="USGS Earthquakes Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');

/* ── FORCE DARK MODE ─────────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], .main, .block-container {
    background-color: #FFFFFF !important;
    color: #222222 !important;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
* { font-family: 'DM Sans', sans-serif; letter-spacing: 0.3px; }

/* ── SIDEBAR — deep slate monochromatic ─────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #F5F7FA !important;
    border-right: 1px solid #DDE3EA !important;
}
[data-testid="stSidebar"] * { color: #4B5563 !important; }

[data-testid="stSidebar"] .stMarkdown h2 {
    font-family: 'Syne', sans-serif !important;
    font-size: 16px !important;
    font-weight: 800 !important;
    color: #222222 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase;
}

[data-testid="stSidebar"] label {
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 1.2px !important;
    text-transform: uppercase !important;
    color: #475569 !important;
}

[data-testid="stSidebar"] input {
    background: #FFFFFF !important;
    border: 1px solid #DDE3EA !important;
    border-radius: 6px !important;
    color: #222222 !important;
    font-size: 13px !important;
}
[data-testid="stSidebar"] input:focus {
    border-color: #F97316 !important;
}

/* multiselect tags */
[data-testid="stSidebar"] span[data-baseweb="tag"] {
    background: rgba(249,115,22,0.15) !important;
    border: 1px solid rgba(249,115,22,0.35) !important;
    border-radius: 4px !important;
    color: #FB923C !important;
}
/* hide the square indicator icons on multiselect */
[data-testid="stSidebar"] [data-baseweb="select"] svg,
[data-testid="stSidebar"] [data-baseweb="select"] [data-testid="stMarkdownContainer"] ~ div svg {
    display: none !important;
}
[data-testid="stSidebar"] [role="combobox"] ~ div {
    display: none !important;
}

/* slider thumb */
[data-testid="stSidebar"] [role="slider"] {
    background: #F97316 !important;
    border: 2px solid #FDE047 !important;
}

/* selectbox */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1px solid #DDE3EA !important;
    border-radius: 6px !important;
}

/* reset button */
[data-testid="stSidebar"] .stButton button {
    background: transparent !important;
    border: 1px solid #DDE3EA !important;
    border-radius: 8px !important;
    color: #4B5563 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    border-color: #F97316 !important;
    color: #F97316 !important;
}

/* sidebar divider */
[data-testid="stSidebar"] hr {
    border-color: #DDE3EA !important;
    margin: 12px 0 !important;
}

/* active nav indicator — orange left border on selectbox */
[data-testid="stSidebar"] [data-baseweb="select"]:focus-within > div {
    border-color: #F97316 !important;
    border-left: 3px solid #F97316 !important;
}

/* ── KPI CARDS — slate with orange accent ───────────────────────────────── */
.kpi-card {
    background: #F5F7FA;
    border: 1px solid #DDE3EA;
    border-radius: 12px;
    padding: 18px 14px 14px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.35);
    transition: border-color 0.2s ease;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #FDE047, #F97316, #DC2626);
}
.kpi-card:hover {
    border-color: #F97316;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 40px;
    font-weight: 800;
    color: #222222;
    line-height: 1.1;
    margin-bottom: 5px;
}
.kpi-label {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #475569;
}
.kpi-icon { font-size: 18px; margin-bottom: 6px; display: block; }

/* ── SECTION TITLES ──────────────────────────────────────────────────────── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #475569;
    padding: 0 0 8px 0;
    margin: 36px 0 14px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.section-title::before {
    content: '';
    width: 3px;
    height: 14px;
    background: linear-gradient(180deg, #FDE047, #F97316);
    border-radius: 2px;
    flex-shrink: 0;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #F5F7FA;
}

/* ── CHART CONTAINERS ────────────────────────────────────────────────────── */
.chart-wrap {
    background: #F5F7FA;
    border: 1px solid #DDE3EA;
    border-radius: 12px;
    padding: 4px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
}
[data-testid="stImage"] img { border-radius: 10px; }

/* ── PAGE HEADER ─────────────────────────────────────────────────────────── */
.dash-header { padding: 4px 0 24px; }
.dash-title {
    font-family: 'Syne', sans-serif;
    font-size: 42px;
    font-weight: 800;
    color: #222222;
    letter-spacing: 1px;
    line-height: 1.1;
}
.dash-title span {
    background: linear-gradient(90deg, #FDE047, #F97316, #DC2626);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.dash-sub {
    font-size: 18px;
    color: #475569;
    margin-top: 5px;
    letter-spacing: 0.5px;
}

/* ── LEGEND STRIP ────────────────────────────────────────────────────────── */
.legend-strip {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 10px 16px;
    background: #F5F7FA;
    border: 1px solid #DDE3EA;
    border-radius: 8px;
    margin-bottom: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}
.legend-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 5px;
}

/* ── LOCATION BADGE ──────────────────────────────────────────────────────── */
.loc-badge {
    display: inline-block;
    background: rgba(249,115,22,0.12);
    border: 1px solid rgba(249,115,22,0.4);
    border-radius: 4px;
    padding: 2px 10px;
    font-size: 11px;
    font-weight: 700;
    color: #FB923C;
    letter-spacing: 1px;
    margin-left: 12px;
    vertical-align: middle;
    text-transform: uppercase;
}

/* ── FOOTER ──────────────────────────────────────────────────────────────── */
.dash-footer {
    text-align: center;
    font-size: 11px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #DDE3EA;
    padding: 16px 0 8px;
}
.block-container { padding-top: 2rem !important; padding-bottom: 2rem !important; }
</style>
""", unsafe_allow_html=True)



# Theme toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode=False
colt1,colt2=st.columns([8,1])
with colt2:
    st.toggle("🌙 Dark", key="dark_mode")

@st.cache_data
def get_data():
    return load_data()



# Dynamic theme
if st.session_state.dark_mode:
    st.markdown("""<style>html, body, [data-testid="stAppViewContainer"], .main, .block-container{background:#121212 !important;color:#f3f4f6 !important}.kpi-card,.chart-wrap,.legend-strip{background:#1e1e1e !important;border-color:#333 !important}.dash-title,.kpi-value{color:#f3f4f6 !important}.dash-sub,.kpi-label{color:#cbd5e1 !important}</style>""",unsafe_allow_html=True)

df = get_data()
df["_region"] = df["place"].str.extract(r",\s*(.+)$")[0].str.strip()

min_date = df["time"].dt.date.min()
max_date = df["time"].dt.date.max()
mag_min  = float(df["mag"].min())
mag_max  = float(df["mag"].max())

TOP_LOCATIONS = [
    "Alaska", "CA", "Papua New Guinea", "Indonesia", "Puerto Rico",
    "Japan", "Chile", "Nevada", "Hawaii", "Tonga",
    "Philippines", "Russia", "Vanuatu", "New Zealand", "China",
    "Argentina", "Greece", "Iran", "Fiji", "Peru", "Mexico",
]
ALL_LOCATIONS  = sorted(df["_region"].dropna().unique().tolist())
OTHER_LOCATIONS = sorted([l for l in ALL_LOCATIONS if l not in TOP_LOCATIONS])

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌋 USGS Dashboard")
    st.markdown("---")

    if st.button("↺  Reset All Filters", use_container_width=True):
        for k in ["date_start","date_end","mag_range","event_types","networks","location_select","other_location"]:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()

    st.markdown("**📅 Date Range**")
    ca, cb = st.columns(2)
    with ca:
        date_start = st.date_input("From", value=min_date, min_value=min_date, max_value=max_date, key="date_start")
    with cb:
        date_end = st.date_input("To", value=max_date, min_value=min_date, max_value=max_date, key="date_end")
    if date_start > date_end:
        date_start, date_end = date_end, date_start

    mag_range = st.slider("📊 Magnitude Range", min_value=mag_min, max_value=mag_max,
                          value=(mag_min, mag_max), step=0.1, key="mag_range")

    all_types  = sorted(df["type"].dropna().unique().tolist())
    event_types = st.multiselect("🏷️ Event Type", options=all_types, default=[], placeholder="All types selected", key="event_types")

    all_nets  = sorted(df["net"].dropna().unique().tolist())
    networks  = st.multiselect("🌐 Network", options=all_nets, default=[], placeholder="All networks selected", key="networks")

    st.markdown("---")
    st.markdown("**📍 Location**")
    loc_options = ["🌍 All Locations"] + TOP_LOCATIONS + ["— Other Locations —"]
    selected_loc = st.selectbox("", loc_options, index=0, key="location_select", label_visibility="collapsed")

    if selected_loc == "— Other Locations —":
        other_loc = st.selectbox("Choose location", OTHER_LOCATIONS, key="other_location")
        active_location = other_loc
    elif selected_loc == "🌍 All Locations":
        active_location = None
    else:
        active_location = selected_loc

    st.markdown("---")
    # color legend in sidebar
    st.markdown("""
    <div style='font-size:10px;color:#475569;letter-spacing:0.8px;line-height:2'>
    <b style='color:#64748B;letter-spacing:1px'>COLOR GUIDE</b><br>
    <span style='color:#FDE047'>●</span> Low Magnitude<br>
    <span style='color:#F97316'>●</span> Medium Magnitude<br>
    <span style='color:#DC2626'>●</span> High / Severe<br>
    <span style='color:#67E8F9'>●</span> Shallow Depth<br>
    <span style='color:#92400E'>●</span> Deep Focus
    </div>
    """, unsafe_allow_html=True)

# ── APPLY FILTERS ─────────────────────────────────────────────────────────────
filtered_df = apply_filters(df, (date_start, date_end), mag_range, event_types, networks, "")
if active_location:
    filtered_df = filtered_df[filtered_df["_region"] == active_location].reset_index(drop=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
loc_badge = f'<span class="loc-badge">📍 {active_location}</span>' if active_location else ""
st.markdown(f"""
<div class="dash-header">
    <div class="dash-title">🌍 USGS <span>Earthquake</span> Dashboard {loc_badge}</div>
    <div class="dash-sub">Past 2.5 Months &nbsp;·&nbsp; Global Seismic Activity &nbsp;·&nbsp; Exploratory Data Analysis</div>
</div>
""", unsafe_allow_html=True)

# color legend strip
st.markdown("""
<div class="legend-strip">
    <span style='color:#64748B'>Magnitude Scale:</span>
    <span><span class="legend-dot" style="background:#FDE047"></span><span style="color:#4B5563">Low</span></span>
    <span><span class="legend-dot" style="background:#F97316"></span><span style="color:#4B5563">Medium</span></span>
    <span><span class="legend-dot" style="background:#DC2626"></span><span style="color:#4B5563">High</span></span>
    &nbsp;&nbsp;
    <span style='color:#64748B'>Depth Scale:</span>
    <span><span class="legend-dot" style="background:#67E8F9"></span><span style="color:#4B5563">Shallow</span></span>
    <span><span class="legend-dot" style="background:#4B5563"></span><span style="color:#4B5563">Mid</span></span>
    <span><span class="legend-dot" style="background:#92400E"></span><span style="color:#4B5563">Deep</span></span>
</div>
""", unsafe_allow_html=True)

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
kpis = get_kpis(filtered_df)
k1, k2, k3, k4, k5, k6 = st.columns(6)
cards = [
    (k1, "🔢", kpis["total"],               "Total Events"),
    (k2, "📈", kpis["avg_mag"],             "Avg Magnitude"),
    (k3, "⚡", kpis["max_mag"],             "Max Magnitude"),
    (k4, "🕳️", f"{kpis['avg_depth']} km",  "Avg Depth"),
    (k5, "📍", f"{kpis['max_depth']} km",  "Max Depth"),
    (k6, "🗺️", kpis["unique_locations"],   "Locations"),
]
for col, icon, val, label in cards:
    col.markdown(
        f'<div class="kpi-card">'
        f'<span class="kpi-icon">{icon}</span>'
        f'<div class="kpi-value">{val}</div>'
        f'<div class="kpi-label">{label}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.markdown("<div style='margin-top:6px'></div>", unsafe_allow_html=True)

if len(filtered_df) == 0:
    st.warning("⚠️ No data matches the selected filters. Try adjusting the filters.")
    st.stop()

# ── CHARTS ────────────────────────────────────────────────────────────────────
def chart_card(fig):
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)
    plt.close(fig)

st.markdown('<div class="section-title">Temporal Analysis</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1: chart_card(line_chart(filtered_df))
with c2: chart_card(area_chart(filtered_df))

st.markdown('<div class="section-title">Distribution Analysis</div>', unsafe_allow_html=True)
c3, c4, c5 = st.columns(3)
with c3: chart_card(pie_chart(filtered_df))
with c4: chart_card(histogram(filtered_df))
with c5: chart_card(count_plot(filtered_df))

st.markdown('<div class="section-title">Statistical Depth Analysis</div>', unsafe_allow_html=True)
c6, c7 = st.columns(2)
with c6: chart_card(box_plot(filtered_df))
with c7: chart_card(violin_plot(filtered_df))

st.markdown('<div class="section-title">Relational & Categorical</div>', unsafe_allow_html=True)
c8, c9 = st.columns(2)
with c8: chart_card(scatter_plot(filtered_df))
with c9: chart_card(bar_chart(filtered_df))

st.markdown('<div class="section-title">Correlation Heatmap</div>', unsafe_allow_html=True)
chart_card(heatmap(filtered_df))

st.markdown("""
<div class="dash-footer">
    USGS Earthquakes Dashboard &nbsp;·&nbsp; Exploratory Data Analysis &nbsp;·&nbsp; Ali Hassan Sherazi
</div>
""", unsafe_allow_html=True)
