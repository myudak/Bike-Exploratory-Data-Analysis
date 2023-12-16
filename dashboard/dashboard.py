import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

#SETUP
link = lambda x : f"https://raw.githubusercontent.com/myudak/Bike-Exploratory-Data-Analysis/main/data/{x}.csv"
sns.set(style='dark')

day_df = pd.read_csv(link("day"))
hour_df = pd.read_csv(link("hour"))


bike_df = hour_df.merge(day_df, on='dteday', how='inner', suffixes=('_hour', '_day'))
weather_labels = {
    1: 'Jernih',
    2: 'Kabut',
    3: 'Curah Hujan Ringan',
    4: 'Curah Hujan Lebat'
}

bike_df['weather_label'] = bike_df['weathersit_day'].map(weather_labels)
#SETUP

datetime_columns = ["dteday"]

for column in datetime_columns:
    bike_df[column] = pd.to_datetime(bike_df[column])

min_date = bike_df["dteday"].min()
max_date = bike_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://storage.googleapis.com/kaggle-datasets-images/3556223/6194875/c51f57d9f027c00fc8d573060eef197b/dataset-card.jpeg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = bike_df[(bike_df["dteday"] >= str(start_date)) & 
                (bike_df["dteday"] <= str(end_date))]

st.header('Bike-Exploratory-Data-Analysis :sparkles:')

st.subheader('Daily User Registered vs Casual')
col1, col2 = st.columns(2)
with col1 :
    total_registered = main_df.registered_hour.sum()
    st.metric("Total registered", value=total_registered)
with col2 :
    total_casual = main_df.casual_hour.sum()
    st.metric("Total Casual User ", value=total_casual )

# GRAPHIC 1
col1, col2 = st.columns(2)
 
with col1 :
    total_rentals_hour = bike_df.groupby('hr')[['registered_hour', 'casual_hour']].sum()
    plt.figure(figsize=(8, 8))
    plt.pie(total_rentals_hour.sum(), labels=['Registered', 'Casual'], autopct='%1.1f%%', colors=plt.cm.Paired.colors, startangle=90)
    
    st.pyplot(plt)
with col2 :
    daily_user_counts = main_df.groupby('dteday')[['registered_day', 'casual_day']].sum().reset_index()
    plt.figure(figsize=(14, 8))
    sns.lineplot(x='dteday', y='registered_day', data=daily_user_counts, label='Registered', marker='o', markersize=6)
    sns.lineplot(x='dteday', y='casual_day', data=daily_user_counts, label='Casual', marker='o', markersize=6)


    plt.xlabel('Date')
    plt.ylabel('Daily User Count')
    plt.legend()
    plt.xticks(rotation=45, ha='right')

    st.pyplot(plt)
# GRAPHIC 1

# GRAPHIC 2
st.subheader("Rata-Rata sewa dalam jam")
rental_jam = main_df.groupby('hr')['cnt_hour'].mean()

plt.figure(figsize=(10,6))
plt.bar(rental_jam.index, rental_jam.values, color='#1f77b4')

plt.xlabel('Jam')
plt.ylabel('Rata - Rata Penyewaan')

st.pyplot(plt)
# GRAPHIC 2

#GRAPHIC 3
st.subheader("Rata - Rata Penyewaan Sepeda berdasarkan Kondisi Cuaca")
avg_weather = main_df.groupby('weather_label')['cnt_day'].mean().reset_index().sort_values("cnt_day")

plt.figure(figsize=(10, 6))
sns.barplot(x='cnt_day', y='weather_label', data=avg_weather, palette='viridis')


plt.xlabel('Rata - Rata Penyewaan')
plt.ylabel('Kondisi Cuaca')

st.pyplot(plt)
#GRAPHIC 3

#GRAPHIC 4
st.subheader("Rata-rata Penyewaan Sepeda pada Hari Libur")
avg_holiday = main_df.groupby('holiday_day')['cnt_day'].mean().reset_index().sort_values("cnt_day")

plt.figure(figsize=(8, 5))
sns.barplot(x='holiday_day', y='cnt_day', data=avg_holiday, palette='Set2')

plt.xlabel('Hari Libur')
plt.ylabel('Rata-rata Penyewaan')
plt.xticks([0, 1], ['Tidak Libur', 'Libur'])

st.pyplot(plt)
#GRAPHIC 4