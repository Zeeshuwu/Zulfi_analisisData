import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the dashboard
st.title("🚴 Bike Rental Dashboard")

# Load the datasets from GitHub
hour_data_url = "https://raw.githubusercontent.com/Zeeshuwu/Zulfi_analisisData/main/hour.csv"
day_data_url = "https://raw.githubusercontent.com/Zeeshuwu/Zulfi_analisisData/main/day.csv"

try:
    hour_data = pd.read_csv(hour_data_url)
    day_data = pd.read_csv(day_data_url)
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

required_columns = {'hour': ['season', 'cnt'], 'day': ['weekday', 'cnt']}
if not all(col in hour_data.columns for col in required_columns['hour']):
    st.error("The hour dataset does not have the required columns!")
    st.stop()
if not all(col in day_data.columns for col in required_columns['day']):
    st.error("The day dataset does not have the required columns!")
    st.stop()

# Question 1: How does bike rental vary by season?
st.header("Bike Rental Distribution by Season 🚴‍♀️")

season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Autumn', 4: 'Winter'}

# Prepare the data for each season
grouped_data = [hour_data[hour_data['season'] == season]['cnt'] for season in season_mapping.keys()]

# Create the boxplot
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.boxplot(
    grouped_data,
    labels=list(season_mapping.values()),  # Ensure labels match the number of data groups
    patch_artist=True,
    boxprops=dict(facecolor='lightblue', color='blue')
)
ax1.set_title('Bike Rental Distribution by Season 🚴‍♀️', fontsize=16)
ax1.set_xlabel('Season', fontsize=14)
ax1.set_ylabel('Total Rentals 🚴', fontsize=14)

# Render the plot in Streamlit
st.pyplot(fig1)

# Question 2: What are the bike rental trends by day of the week?
st.header("Total Bike Rentals by Day of the Week 🚴‍♂️")

# Mapping weekdays to names
weekday_mapping = {0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'}
day_data['day_of_week'] = day_data['weekday'].map(weekday_mapping)

# Aggregate rentals by day of the week
weekly_rentals = day_data.groupby('day_of_week')['cnt'].sum().reindex(
    ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
)

# Create the bar chart
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.bar(weekly_rentals.index, weekly_rentals.values, color='skyblue', edgecolor='black')
ax2.set_title('Total Bike Rentals by Day of the Week', fontsize=16)
ax2.set_xlabel('Day of the Week', fontsize=14)
ax2.set_ylabel('Total Rentals 🚴', fontsize=14)

# Add data labels to the bars
for i, v in enumerate(weekly_rentals.values):
    ax2.text(i, v + 50, str(v), ha='center', fontsize=10)

# Render the plot in Streamlit
st.pyplot(fig2)
