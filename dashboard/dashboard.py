import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

sns.set_style("whitegrid")

@st.cache_data
def load_data():
    df = pd.read_csv("dashboardmain_data.csv")
    df["dteday"] = pd.to_datetime(df["dteday"])
    return df

main_df = load_data()

with st.sidebar:
    st.title("🚲 Bike Sharing Dashboard")
    st.markdown("Tentukan rentang waktu dan kategori pengguna untuk mengeksplorasi data!")
    
    min_date = main_df["dteday"].min().date()
    max_date = main_df["dteday"].max().date()
    
    date_range = st.date_input(
        label="Rentang Tanggal",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    user_type = st.selectbox(
        label="Kategori Pengguna",
        options=["Total (cnt)", "Registered (Terdaftar)", "Casual (Kasual)"]
    )
    
    st.markdown("---")
    st.caption("Dibuat\nOleh: Dewa Made Pandu Diotama\n\n Cohort ID: DS014B6Y0437")

prefix_map = {
    "Total (cnt)": "cnt",
    "Registered (Terdaftar)": "registered",
    "Casual (Kasual)": "casual"
}
base_col = prefix_map[user_type]
col_day = f"{base_col}_day"
col_hour = f"{base_col}_hour"

if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    start_date = end_date = pd.to_datetime(date_range[0])

filtered_hour = main_df[(main_df["dteday"] >= start_date) & (main_df["dteday"] <= end_date)].copy()
filtered_day = filtered_hour.groupby("dteday", as_index=False).first()

st.title("Dashboard Analisis Penyewaan Sepeda (2011–2012) ✨")
st.markdown(f"Menampilkan performa kategori **{user_type}** pada periode **{start_date.strftime('%d %b %Y')}** s.d. **{end_date.strftime('%d %b %Y')}**.")

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric("Total Penyewaan", f"{filtered_day[col_day].sum():,}")
with kpi2:
    st.metric("Rata-rata Harian", f"{filtered_day[col_day].mean():,.0f} unit/hari")
with kpi3:
    st.metric("Rata-rata Per Jam", f"{filtered_hour[col_hour].mean():,.1f} unit/jam")

st.markdown("---")

st.subheader("1. Faktor Penurunan Rata-Rata Penyewaan Sepeda")

baseline_day = filtered_day[col_day].mean()
baseline_hour = filtered_hour[col_hour].mean()

fig1, ax1 = plt.subplots(nrows=1, ncols=3, figsize=(24, 6))

season_df = filtered_day.groupby("season", observed=False)[col_day].mean().reset_index()
season_df["clean_season"] = season_df["season"].astype(int).map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})
season_df = season_df.sort_values(by=col_day, ascending=True)
season_colors = ["#72BCD4" if val < baseline_day else "#D3D3D3" for val in season_df[col_day]]

sns.barplot(x="clean_season", y=col_day, hue="clean_season", data=season_df, palette=season_colors, legend=False, ax=ax1[0])
ax1[0].axhline(baseline_day, color="red", linestyle="--", linewidth=1.5, label=f"Rata-rata Harian ({baseline_day:.0f})")
ax1[0].set_title("Rata-Rata Penyewaan per Musim", fontsize=14, pad=12)
ax1[0].set_xlabel(None)
ax1[0].set_ylabel("Rata-Rata Penyewaan (unit/hari)", fontsize=11)
ax1[0].set_ylim(0, season_df[col_day].max() * 1.18)
ax1[0].legend(loc="upper left")
ax1[0].bar_label(ax1[0].containers[0], fmt="%.0f", padding=3, fontsize=10)

weather_df = filtered_day.groupby("weathersit_day", observed=False)[col_day].mean().reset_index()
weather_df["clean_weather"] = weather_df["weathersit_day"].astype(int).map({
    1: "Cerah", 2: "Berkabut/Berawan", 3: "Hujan/Salju Ringan", 4: "Ekstrem"
})
weather_df = weather_df.sort_values(by=col_day, ascending=True)
weather_colors = ["#72BCD4" if val < baseline_day else "#D3D3D3" for val in weather_df[col_day]]

sns.barplot(x="clean_weather", y=col_day, hue="clean_weather", data=weather_df, palette=weather_colors, legend=False, ax=ax1[1])
ax1[1].axhline(baseline_day, color="red", linestyle="--", linewidth=1.5, label=f"Rata-rata Harian ({baseline_day:.0f})")
ax1[1].set_title("Rata-Rata Penyewaan per Kondisi Cuaca", fontsize=14, pad=12)
ax1[1].set_xlabel(None)
ax1[1].set_ylabel(None)
ax1[1].set_ylim(0, weather_df[col_day].max() * 1.18)
ax1[1].legend(loc="upper left")
ax1[1].bar_label(ax1[1].containers[0], fmt="%.0f", padding=3, fontsize=10)

hr_df = filtered_hour.groupby("hr", observed=False)[col_hour].mean().sort_values(ascending=True).head(8).reset_index()
hr_df["hr_label"] = hr_df["hr"].astype(str).str.zfill(2) + ":00"
hour_colors = ["#72BCD4" if hr <= 5 else "#D3D3D3" for hr in hr_df["hr"]]

sns.barplot(x="hr_label", y=col_hour, hue="hr_label", data=hr_df, palette=hour_colors, legend=False, ax=ax1[2])
ax1[2].axhline(baseline_hour, color="red", linestyle="--", linewidth=1.5, label=f"Rata-rata Jam ({baseline_hour:.0f})")
ax1[2].set_title("Top 8 Jam dengan Penyewaan Terendah", fontsize=14, pad=12)
ax1[2].set_xlabel("Jam Operasional", fontsize=11)
ax1[2].set_ylabel("Rata-Rata Penyewaan (unit/jam)", fontsize=11)
ax1[2].set_ylim(0, baseline_hour * 1.18)
ax1[2].legend(loc="upper left")
ax1[2].bar_label(ax1[2].containers[0], fmt="%.1f", padding=3, fontsize=10)

sns.despine()
plt.tight_layout()
st.pyplot(fig1)

st.info(
    "**Insight Utama:** Terdapat tiga penyebab utama yang menekan volume penyewaan sepeda di bawah rata-rata normal, "
    "yaitu datangnya musim **Spring**, kondisi cuaca **Hujan/Salju Ringan** (diikuti cuaca **Berkabut/Berawan**), "
    "serta periode waktu dini hari antara pukul **00:00 hingga 05:00** dengan titik terendah pada pukul **04:00**."
)

st.markdown("---")

st.subheader("2. Perbandingan Penyewaan Sepeda: Summer vs Winter Berdasarkan Kondisi Cuaca")

df_sw = filtered_day[filtered_day["season"].astype(int).isin([2, 4])].copy()

if df_sw["season"].nunique() < 2:
    st.warning("Pilih rentang tanggal yang mencakup musim Summer dan Winter sekaligus untuk menampilkan perbandingan ini.")
else:
    df_sw["clean_season"] = df_sw["season"].astype(int).map({2: "Summer", 4: "Winter"})
    df_sw["kondisi_cuaca"] = np.where(df_sw["weathersit_day"].astype(int) == 1, "Cerah", "Cuaca Buruk")

    fig2, ax2 = plt.subplots(nrows=1, ncols=3, figsize=(24, 6))

    sw_pivot = df_sw.pivot_table(values=col_day, index="clean_season", columns="kondisi_cuaca", aggfunc="mean").reindex(["Summer", "Winter"]).reset_index()
    max_y_sw = sw_pivot[["Cerah", "Cuaca Buruk"]].max().max() * 1.18

    sns.barplot(x="clean_season", y="Cerah", hue="clean_season", data=sw_pivot, palette=["#72BCD4", "#D3D3D3"], legend=False, ax=ax2[0])
    ax2[0].set_title("Saat Cuaca Cerah", fontsize=14, pad=12)
    ax2[0].set_xlabel(None)
    ax2[0].set_ylabel("Rata-Rata Penyewaan (unit/hari)", fontsize=11)
    ax2[0].set_ylim(0, max_y_sw)
    ax2[0].bar_label(ax2[0].containers[0], fmt="%.0f", padding=3, fontsize=11, fontweight="bold")

    sns.barplot(x="clean_season", y="Cuaca Buruk", hue="clean_season", data=sw_pivot, palette=["#D3D3D3", "#72BCD4"], legend=False, ax=ax2[1])
    ax2[1].set_title("Saat Cuaca Buruk (Berawan/Hujan)", fontsize=14, pad=12)
    ax2[1].set_xlabel(None)
    ax2[1].set_ylabel(None)
    ax2[1].set_ylim(0, max_y_sw)
    ax2[1].bar_label(ax2[1].containers[0], fmt="%.0f", padding=3, fontsize=11, fontweight="bold")

    sw_user = df_sw.groupby(["clean_season", "kondisi_cuaca"], observed=False)[["registered_day", "casual_day"]].mean().reset_index()
    sw_user["Segmen"] = sw_user["clean_season"] + "\n(" + sw_user["kondisi_cuaca"] + ")"
    order_segmen = ["Summer\n(Cerah)", "Summer\n(Cuaca Buruk)", "Winter\n(Cerah)", "Winter\n(Cuaca Buruk)"]
    
    sw_melted = sw_user.melt(id_vars=["Segmen"], value_vars=["registered_day", "casual_day"], var_name="Tipe_Pengguna", value_name="Rata_Rata")
    sw_melted["Tipe_Pengguna"] = sw_melted["Tipe_Pengguna"].replace({"registered_day": "Registered", "casual_day": "Casual"})

    sns.barplot(x="Segmen", y="Rata_Rata", hue="Tipe_Pengguna", data=sw_melted, order=order_segmen, palette=["#72BCD4", "#F4A261"], ax=ax2[2])
    ax2[2].set_title("Detail Segmen Pengguna (Registered vs Casual)", fontsize=14, pad=12)
    ax2[2].set_xlabel(None)
    ax2[2].set_ylabel("Rata-Rata Penyewaan (unit/hari)", fontsize=11)
    ax2[2].set_ylim(0, sw_melted["Rata_Rata"].max() * 1.18)
    ax2[2].legend(title="Tipe Pengguna", loc="upper right")
    for container in ax2[2].containers:
        ax2[2].bar_label(container, fmt="%.0f", padding=3, fontsize=9.5)

    sns.despine()
    plt.tight_layout()
    st.pyplot(fig2)

    st.info(
        "**Insight Utama:** Walaupun musim **Summer** mendominasi penyewaan saat **Cuaca Cerah** karena dorongan tingginya pengguna *casual*, "
        "musim **Winter** justru mencatatkan performa lebih unggul ketika **Cuaca Buruk** terjadi. Daya tahan **Winter** di tengah cuaca yang kurang bersahabat "
        "ini berasal dari konsistensi segmen pengguna *registered* yang tetap stabil dibandingkan penyusutan signifikan pada musim **Summer**."
    )