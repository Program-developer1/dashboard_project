import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import pandas as pd
import numpy as np


# ── INFOGRAPHIC LIGHT PALETTE ──────────────────────────────────────────
BG = "#FFFFFF"
BG_CARD = "#FFFFFF"
GRID = "#DDE3EA"
TEXT = "#4B5563"
TEXT_BRIGHT = "#222222"

INFO = ["#00A6ED","#FF6B00","#E53935","#FFC107","#00C853","#8E24AA","#EC407A","#26C6DA","#3949AB","#795548"]

SEQ_LOW="#FFC107"
SEQ_MID="#FF6B00"
SEQ_HIGH="#E53935"
SEQ_MAP=mcolors.LinearSegmentedColormap.from_list("info_seq",[SEQ_LOW,SEQ_MID,SEQ_HIGH])

DIV_SHALLOW="#26C6DA"
DIV_MID="#00A6ED"
DIV_DEEP="#3949AB"
DIV_MAP=mcolors.LinearSegmentedColormap.from_list("depth",[DIV_SHALLOW,DIV_MID,DIV_DEEP])

CAT_PALETTE=INFO
plt.rcParams.update({
    "figure.facecolor":  BG_CARD,
    "axes.facecolor":    BG_CARD,
    "axes.edgecolor":    GRID,
    "axes.labelcolor":   TEXT,
    "axes.titlecolor":   TEXT_BRIGHT,
    "axes.grid":         True,
    "grid.color":        GRID,
    "grid.linewidth":    0.5,
    "grid.linestyle":    "--",
    "xtick.color":       TEXT,
    "ytick.color":       TEXT,
    "text.color":        TEXT,
    "legend.facecolor":  BG_CARD,
    "legend.edgecolor":  GRID,
    "legend.labelcolor": TEXT,
    "figure.dpi":        120,
})


def _new(w=9, h=4.5):
    plt.close("all")
    fig, ax = plt.subplots(figsize=(w, h), facecolor=BG_CARD)
    ax.set_facecolor(BG_CARD)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)
    return fig, ax


def _title(ax, text):
    ax.set_title(text, fontsize=12, fontweight="bold", color=TEXT_BRIGHT, pad=14)


def _xlabel(ax, text):
    ax.set_xlabel(text, fontsize=10, color=TEXT, labelpad=6)


def _ylabel(ax, text):
    ax.set_ylabel(text, fontsize=10, color=TEXT, labelpad=6)


# ── 1. PIE CHART — categorical (regions by mag category) ────────────────────
def pie_chart(df):
    counts = df["mag_category"].value_counts().dropna()
    # use sequential ember for magnitude categories — low to high
    pie_colors = [SEQ_LOW, "#FBB040", SEQ_MID, "#C0392B", SEQ_HIGH][:len(counts)]
    plt.close("all")
    fig, ax = plt.subplots(figsize=(7, 5), facecolor=BG_CARD)
    wedges, texts, autotexts = ax.pie(
        counts, labels=counts.index, autopct="%1.1f%%",
        colors=pie_colors, startangle=140,
        pctdistance=0.78,
        wedgeprops={"linewidth": 1.8, "edgecolor": BG_CARD}
    )
    for t in texts:
        t.set_color(TEXT)
        t.set_fontsize(9)
    for at in autotexts:
        at.set_color(TEXT_BRIGHT)
        at.set_fontsize(9)
        at.set_fontweight("bold")
    _title(ax, "Earthquake Distribution by Magnitude Category")
    plt.tight_layout()
    return fig


# ── 2. HISTOGRAM — sequential ember (magnitude = intensity data) ─────────────
def histogram(df):
    mags = df["mag"].dropna()
    fig, ax = _new()
    n, bins, patches = ax.hist(mags, bins=30, edgecolor=BG_CARD, linewidth=0.4)
    norm = mcolors.Normalize(vmin=bins[0], vmax=bins[-1])
    for patch, left_edge in zip(patches, bins[:-1]):
        patch.set_facecolor(SEQ_MAP(norm(left_edge)))
        patch.set_alpha(0.9)
    sm = plt.cm.ScalarMappable(cmap=SEQ_MAP, norm=norm)
    sm.set_array([])
    cb = plt.colorbar(sm, ax=ax, pad=0.02)
    cb.set_label("Magnitude", color=TEXT, fontsize=9)
    cb.ax.yaxis.set_tick_params(color=TEXT)
    plt.setp(cb.ax.yaxis.get_ticklabels(), color=TEXT)
    cb.outline.set_edgecolor(GRID)
    _xlabel(ax, "Magnitude")
    _ylabel(ax, "Frequency")
    _title(ax, "Magnitude Frequency Distribution")
    plt.tight_layout()
    return fig


# ── 3. LINE CHART — single accent (temporal trend) ──────────────────────────
def line_chart(df):
    daily = df.groupby("date").size().reset_index(name="count")
    daily["date"] = pd.to_datetime(daily["date"])
    daily = daily.sort_values("date")
    fig, ax = _new(10, 4.5)
    ax.plot(daily["date"], daily["count"], color=SEQ_MID, linewidth=2,
            marker="o", markersize=3.5, markerfacecolor=SEQ_LOW, markeredgewidth=0)
    ax.fill_between(daily["date"], daily["count"], alpha=0.15, color=SEQ_MID)
    _xlabel(ax, "Date")
    _ylabel(ax, "Number of Events")
    _title(ax, "Daily Earthquake Count Over Time")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    return fig


# ── 4. BAR CHART — categorical palette (region comparisons) ─────────────────
def bar_chart(df):
    top_nets = df["net"].value_counts().head(10)
    fig, ax = _new()
    colors = [CAT_PALETTE[i % len(CAT_PALETTE)] for i in range(len(top_nets))]
    bars = ax.bar(top_nets.index, top_nets.values, color=colors,
                  edgecolor=BG_CARD, linewidth=0.6)
    for bar in bars:
        ax.annotate(
            int(bar.get_height()),
            (bar.get_x() + bar.get_width() / 2, bar.get_height() + 2),
            ha="center", fontsize=8, color=TEXT
        )
    _xlabel(ax, "Network")
    _ylabel(ax, "Count")
    _title(ax, "Top Seismic Networks by Event Count")
    plt.tight_layout()
    return fig


# ── 5. SCATTER PLOT — sequential ember (magnitude intensity) ─────────────────
def scatter_plot(df):
    sample = df.sample(min(len(df), 800), random_state=42)
    fig, ax = _new(9, 5)
    sc = ax.scatter(
        sample["depth"], sample["mag"],
        c=sample["mag"], cmap=SEQ_MAP,
        alpha=0.7, edgecolors="none", s=20,
        vmin=df["mag"].min(), vmax=df["mag"].max()
    )
    cb = plt.colorbar(sc, ax=ax, pad=0.02)
    cb.set_label("Magnitude", color=TEXT, fontsize=9)
    cb.ax.yaxis.set_tick_params(color=TEXT)
    plt.setp(cb.ax.yaxis.get_ticklabels(), color=TEXT)
    cb.outline.set_edgecolor(GRID)
    _xlabel(ax, "Depth (km)")
    _ylabel(ax, "Magnitude")
    _title(ax, "Earthquake Depth vs Magnitude")
    plt.tight_layout()
    return fig


# ── 6. BOX PLOT — sequential ember (magnitude ordered categories) ────────────
def box_plot(df):
    order = ["Minor (<3)", "Light (3-4)", "Moderate (4-5)", "Strong (5-6)", "Major (6+)"]
    data  = df[df["mag_category"].notna()]
    valid = [o for o in order if o in data["mag_category"].unique()]
    box_colors = [SEQ_LOW, "#FBB040", SEQ_MID, "#C0392B", SEQ_HIGH][:len(valid)]
    fig, ax = _new(9, 5)
    sns.boxplot(
        data=data, x="mag_category", y="depth",
        hue="mag_category", order=valid,
        palette=box_colors, legend=False, ax=ax,
        linewidth=1.2,
        boxprops={"edgecolor": GRID},
        whiskerprops={"color": TEXT, "linewidth": 1},
        capprops={"color": TEXT, "linewidth": 1.5},
        medianprops={"color": SEQ_LOW, "linewidth": 2.5},
        flierprops={"markerfacecolor": SEQ_HIGH, "markersize": 3, "alpha": 0.5, "markeredgewidth": 0}
    )
    _xlabel(ax, "Magnitude Category")
    _ylabel(ax, "Depth (km)")
    _title(ax, "Depth Distribution by Magnitude Category")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    return fig


# ── 7. HEATMAP — diverging teal→brown (correlation = diverging data) ─────────
def heatmap(df):
    cols = ["mag", "depth", "latitude", "longitude", "gap", "rms", "nst", "dmin"]
    available = [c for c in cols if c in df.columns]
    corr = df[available].dropna().corr()
    plt.close("all")
    fig, ax = plt.subplots(figsize=(9, 6), facecolor=BG_CARD)
    ax.set_facecolor(BG_CARD)
    div_cmap = mcolors.LinearSegmentedColormap.from_list("div", ["#67E8F9", "#1E293B", "#92400E"])
    sns.heatmap(
        corr, annot=True, fmt=".2f", cmap=div_cmap,
        center=0, linewidths=0.5, linecolor=BG,
        ax=ax, annot_kws={"size": 9, "color": TEXT_BRIGHT},
        cbar_kws={"shrink": 0.8}
    )
    ax.tick_params(colors=TEXT)
    _title(ax, "Feature Correlation Heatmap")
    plt.tight_layout()
    return fig


# ── 8. AREA CHART — diverging depth color (earth structure) ──────────────────
def area_chart(df):
    daily = df.groupby("date")["mag"].mean().reset_index()
    daily["date"] = pd.to_datetime(daily["date"])
    daily = daily.sort_values("date")
    fig, ax = _new(10, 4.5)
    ax.fill_between(daily["date"], daily["mag"], alpha=0.22, color=DIV_SHALLOW)
    ax.plot(daily["date"], daily["mag"], color=DIV_SHALLOW, linewidth=2)
    # add a reference mean line
    mean_mag = daily["mag"].mean()
    ax.axhline(mean_mag, color=SEQ_MID, linewidth=1, linestyle="--", alpha=0.6)
    ax.text(daily["date"].iloc[-1], mean_mag + 0.03, f" avg {mean_mag:.2f}",
            color=SEQ_MID, fontsize=8, va="bottom")
    _xlabel(ax, "Date")
    _ylabel(ax, "Average Magnitude")
    _title(ax, "Average Daily Magnitude (Area Chart)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    return fig


# ── 9. COUNT PLOT — categorical palette (type comparisons) ───────────────────
def count_plot(df):
    top_types = df["magType"].value_counts().head(8).index
    data = df[df["magType"].isin(top_types)]
    fig, ax = _new()
    sns.countplot(
        data=data, x="magType", order=top_types,
        hue="magType", palette=CAT_PALETTE[:len(top_types)],
        legend=False, ax=ax
    )
    for p in ax.patches:
        ax.annotate(
            int(p.get_height()),
            (p.get_x() + p.get_width() / 2, p.get_height() + 2),
            ha="center", fontsize=8, color=TEXT
        )
    _xlabel(ax, "Magnitude Type")
    _ylabel(ax, "Count")
    _title(ax, "Count of Events by Magnitude Type")
    plt.tight_layout()
    return fig


# ── 10. VIOLIN PLOT — sequential ember (magnitude distribution) ──────────────
def violin_plot(df):
    order = ["Minor (<3)", "Light (3-4)", "Moderate (4-5)", "Strong (5-6)", "Major (6+)"]
    data  = df[df["mag_category"].notna()]
    valid = [o for o in order if o in data["mag_category"].unique()]
    vio_colors = [SEQ_LOW, "#FBB040", SEQ_MID, "#C0392B", SEQ_HIGH][:len(valid)]
    fig, ax = _new(10, 5)
    sns.violinplot(
        data=data, x="mag_category", y="mag",
        hue="mag_category", order=valid,
        palette=vio_colors, inner="quartile",
        legend=False, ax=ax, linewidth=1
    )
    _xlabel(ax, "Magnitude Category")
    _ylabel(ax, "Magnitude")
    _title(ax, "Magnitude Distribution by Category (Violin)")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    return fig
