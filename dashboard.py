import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit Configuration
st.set_page_config(page_title="Bike Sharing Analysis", layout="wide")

# Title and Introduction
st.title("Proyek Analisis Data: Bike Sharing")
st.write("""
**Nama:** Mohammad Zulfi Rahadi Putra

**Email:** zulfi.rhp22@gmail.com

**ID Dicoding:** 

**Pertanyaan Bisnis:**
1. Bagaimana pengaruh cuaca terhadap jumlah penyewaan sepeda dalam sebulan terakhir?
2. Apakah terdapat pola tertentu dalam jumlah penyewaan sepeda berdasarkan hari dalam seminggu dalam sebulan terakhir?
""")

# Load Data
hour_data_url = "https://raw.githubusercontent.com/Zeeshuwu/Zulfi_analisisData/main/hour.csv"
day_data_url = "https://raw.githubusercontent.com/Zeeshuwu/Zulfi_analisisData/main/day.csv"

hour_data = pd.read_csv(hour_data_url)
day_data = pd.read_csv(day_data_url)

# Preprocessing
hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])

# Function to Analyze Weather Effect on Rentals
def plot_weather_effect(data):
    last_month_data = data[data['dteday'] >= (data['dteday'].max() - pd.Timedelta(days=30))]
    avg_rentals_by_weather = last_month_data.groupby('weathersit')['cnt'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    sns.barplot(data=avg_rentals_by_weather, x='weathersit', y='cnt', palette='coolwarm')
    plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Situasi Cuaca (30 Hari Terakhir)', fontsize=14)
    plt.xlabel('Situasi Cuaca', fontsize=12)
    plt.ylabel('Rata-rata Penyewaan', fontsize=12)
    plt.xticks(ticks=[0, 1, 2, 3], labels=['Cerah', 'Kabut', 'Salju/Hujan Ringan', 'Hujan Salju Berat'])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

# Function to Analyze Weekly Patterns
def plot_weekly_pattern(data):
    last_month_data = data[data['dteday'] >= (data['dteday'].max() - pd.Timedelta(days=30))]
    last_month_data['weekday'] = last_month_data['dteday'].dt.day_name()
    avg_rentals_by_weekday = last_month_data.groupby('weekday')['cnt'].mean().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']).reset_index()

    plt.figure(figsize=(10, 6))
    sns.barplot(data=avg_rentals_by_weekday, x='weekday', y='cnt', palette='viridis')
    plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Hari dalam Seminggu (30 Hari Terakhir)', fontsize=14)
    plt.xlabel('Hari', fontsize=12)
    plt.ylabel('Rata-rata Penyewaan', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

# Sidebar for EDA Options
eda_option = st.sidebar.selectbox(
    "Pilih Analisis:",
    ["Rata-rata Penyewaan Cuaca (30 Hari Terakhir)", 
     "Distribusi Penyewaan Sepeda", 
     "Pola Mingguan Penyewaan Sepeda"]
)

if eda_option == "Rata-rata Penyewaan Cuaca (30 Hari Terakhir)":
    st.header("Rata-rata Penyewaan Berdasarkan Situasi Cuaca")
    plot_weather_effect(hour_data)

elif eda_option == "Distribusi Penyewaan Sepeda":
    st.header("Distribusi Penyewaan Sepeda")
    plt.figure(figsize=(10, 5))
    sns.histplot(hour_data['cnt'], bins=30, kde=True, color='blue')
    plt.title('Distribusi Penyewaan Sepeda', fontsize=14)
    plt.xlabel('Total Penyewaan', fontsize=12)
    plt.ylabel('Frekuensi', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

elif eda_option == "Pola Mingguan Penyewaan Sepeda":
    st.header("Pola Mingguan Penyewaan Sepeda")
    plot_weekly_pattern(hour_data)

# Footer
st.write("""---
**Insight:**
- Cuaca memengaruhi jumlah penyewaan sepeda, terutama pada hari cerah.
- Pola penyewaan cenderung meningkat pada hari kerja dibandingkan akhir pekan.
""")
