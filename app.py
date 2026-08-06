import streamlit as st
import requests 
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Weather App",page_icon='⛅')

st.title("😎 Weather App")

st.write('Enter The City name and click Get Weather Button to see the weather report')

city = st.text_input("Enter the City Name : ")

API_KEY = os.getenv('API_KEY')

API_URL = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'

if st.button('Get Weather Report') :
    response = requests.get(API_URL)
    if (response.status_code ==200):
        st.success("Data Fetched Successfully")
        data = response.json()
    
    #Extracting Values
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        weather = data['weather'][0]['main']
        name = data['name']
        country = data['sys']['country']

        #Display country
        st.subheader(f"{name},{country}")

        #Create 2 Rows And 2 Columns
        col1,col2 = st.columns(2)
        col3,col4 = st.columns(2)

        #display values on Screen
        col1.metric('Temprature',f'🌡️{temperature}°C')
        col2.metric('Humidity',f'💧{humidity}%')
        col3.metric('Wind Speed',f'🍃{wind_speed} m/s')
        col4.metric('Weather',f'🌤️{weather}')
    else:
        st.error('City Not Found')
