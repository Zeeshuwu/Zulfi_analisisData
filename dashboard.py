import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the dashboard
st.title("🚴 Bike Rental Dashboard")

# Load the datasets from GitHub
hour_data = pd.read_csv("https://raw.githubusercontent.com/Zeeshuwu/Zulfi_analisisData/main/hour.csv")
day_data = pd.read_csv("https://raw.githubusercontent.com/Zeeshuwu/Zulfi_analisisData/main/day.csv")

# Add a date range filter
st.sidebar.header("Filter Data")
date_range = st.sidebar.date_input("Select Date Range", [])

# Filter data by date range
if date_range:
    start_date, end_date = pd.to_datetime(date_range)
    hour_data['datetime'] = pd.to_datetime(hour_data['dteday'])
    hour_data = hour_data[(hour_data['datetime'] >= start_date) & (hour_data['datetime'] <= end_date)]

# Question 1: How does bike rental vary by season?
st.header("Bike Rental Distribution by Season 🚴‍♀️")
selected_season = st.sidebar.selectbox("Select a Season", ['Spring', 'Summer', 'Autumn', 'Winter'], index=0)
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Autumn', 4: 'Winter'}
filtered_data = hour_data[hour_data['season'] == list(season_mapping.keys())[list(season_mapping.values()).index(selected_season)]]

fig, ax = plt.subplots(figsize=(10, 6))
ax.boxplot(
    [filtered_data[filtered_data['season'] == season]['cnt'] for season in filtered_data['season'].unique()],
    labels=['Spring', 'Summer', 'Autumn', 'Winter'],
    patch_artist=True,
    boxprops=dict(facecolor="lightblue"),
)
ax.set_title('Bike Rental Distribution by Season', fontsize=16)
ax.set_xlabel('Season', fontsize=14)
ax.set_ylabel('Total Rentals 🚴', fontsize=14)
st.pyplot(fig)

# Question 2: What are the bike rental trends by day of the week?
st.header("Total Bike Rentals by Day of the Week 🚴‍♂️")
day_data['day_of_week'] = day_data['weekday'].map({0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'})
day_totals = day_data.groupby('day_of_week')['cnt'].sum().reindex(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(day_totals.index, day_totals.values, color='lightgreen')
ax.set_title('Total Bike Rentals by Day of the Week', fontsize=16)
ax.set_xlabel('Day of the Week', fontsize=14)
ax.set_ylabel('Total Rentals 🚴', fontsize=14)

# Add labels to the bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', ha='center', va='bottom', fontsize=12)

st.pyplot(fig)

# Question 3: How does weather affect bike rentals?
st.header("Bike Rentals by Weather Condition 🌦️")
weather_options = ['Clear', 'Mist', 'Light Snow/Rain', 'Heavy Rain/Snow']
selected_weather = st.sidebar.selectbox("Select Weather Condition", weather_options, index=0)
weather_mapping = {1: 'Clear', 2: 'Mist', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'}
filtered_weather_data = hour_data[hour_data['weathersit'] == list(weather_mapping.keys())[list(weather_mapping.values()).index(selected_weather)]]

fig, ax = plt.subplots(figsize=(10, 6))
ax.boxplot(
    [filtered_weather_data[filtered_weather_data['weathersit'] == weather]['cnt'] for weather in filtered_weather_data['weathersit'].unique()],
    labels=weather_options,
    patch_artist=True,
    boxprops=dict(facecolor="lightcoral"),
)
ax.set_title(f'Bike Rentals During {selected_weather}', fontsize=16)
ax.set_xlabel('Weather Condition', fontsize=14)
ax.set_ylabel('Total Rentals 🚴', fontsize=14)
st.pyplot(fig)
