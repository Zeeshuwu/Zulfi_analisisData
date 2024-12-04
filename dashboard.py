import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


sns.set_theme(style="whitegrid")

st.title("🚴 Bike Rental Dashboard")


hour_data = pd.read_csv("https://raw.githubusercontent.com/Zeeshuwu/Zulfi_analisisData/main/hour.csv")
day_data = pd.read_csv("https://raw.githubusercontent.com/Zeeshuwu/Zulfi_analisisData/main/day.csv")


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
season_fig, season_ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='season', y='cnt', data=filtered_data, ax=season_ax, palette='Set2')
season_ax.set_title('Bike Rental Distribution by Season', fontsize=16)
season_ax.set_xlabel('Season', fontsize=14)
season_ax.set_ylabel('Total Rentals 🚴', fontsize=14)
season_ax.set_xticklabels(['Spring', 'Summer', 'Autumn', 'Winter'])
season_ax.tick_params(axis='both', which='major', labelsize=12)
st.pyplot(season_fig)

# Question 2: What are the bike rental trends by day of the week?
st.header("Total Bike Rentals by Day of the Week 🚴‍♂️")
day_data['day_of_week'] = day_data['weekday'].map({0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'})
day_fig, day_ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='day_of_week', y='cnt', data=day_data, ax=day_ax, palette='pastel', order=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
day_ax.set_title('Total Bike Rentals by Day of the Week', fontsize=16)
day_ax.set_xlabel('Day of the Week', fontsize=14)
day_ax.set_ylabel('Total Rentals 🚴', fontsize=14)
day_ax.tick_params(axis='both', which='major', labelsize=12)

# Adding data labels to the bars
for p in day_ax.patches:
    day_ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=12)

st.pyplot(day_fig)

# Question 3: How does weather affect bike rentals?
st.header("Bike Rentals by Weather Condition 🌦️")
weather_options = ['Clear', 'Mist', 'Light Snow/Rain', 'Heavy Rain/Snow']
selected_weather = st.sidebar.selectbox("Select Weather Condition", weather_options, index=0)
weather_mapping = {1: 'Clear', 2: 'Mist', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Snow'}
filtered_weather_data = hour_data[hour_data['weathersit'] == list(weather_mapping.keys())[list(weather_mapping.values()).index(selected_weather)]]
weather_fig, weather_ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='weathersit', y='cnt', data=filtered_weather_data, ax=weather_ax, palette='coolwarm')
weather_ax.set_title(f'Bike Rentals During {selected_weather}', fontsize=16)
weather_ax.set_xlabel('Weather Condition', fontsize=14)
weather_ax.set_ylabel('Total Rentals 🚴', fontsize=14)
weather_ax.tick_params(axis='both', which='major', labelsize=12)
st.pyplot(weather_fig)
