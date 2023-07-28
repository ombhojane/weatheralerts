import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd

# OpenWeatherMap API key (replace 'your_api_key' with your actual API key)
api_key = 'bb34b4f6362247530f4b2091d0a18a9e'

# Custom OpenWeatherMap connection class
class OpenWeatherMapConnection:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def get_weather_data(self, location):
        try:
            params = {"q": location, "appid": self.api_key, "units": "metric"}
            response = requests.get(self.base_url, params=params)
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            st.error("Error: Unable to connect to the OpenWeatherMap API.")
            return None

# Function to fetch weather data for the previous and next days
def fetch_weather_data_range(location, days):
    connection = OpenWeatherMapConnection(api_key)
    weather_data_list = []
    for i in range(days):
        date = datetime.now() + timedelta(days=(i - days // 2))
        formatted_date = date.strftime("%Y-%m-%d")
        weather_data = connection.get_weather_data(location)
        if weather_data:
            weather_data['date'] = formatted_date
            weather_data_list.append(weather_data)
    return weather_data_list

# Weather Icons mapping
weather_icons = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Drizzle": "🌧️",
    "Rain": "🌧️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Smoke": "🌫️",
    "Haze": "🌫️",
    "Dust": "🌫️",
    "Fog": "🌫️",
    "Sand": "🌫️",
    "Ash": "🌫️",
    "Squall": "🌫️",
    "Tornado": "🌪️"
}

# Function to set background image based on weather conditions
def set_background_image(weather_condition):
    # Implement your background image logic here based on weather conditions
    pass

# Main app
def main():
    st.title("Weather Forecast App with OpenWeatherMap API")
    
    # Create a connection to OpenWeatherMap API
    connection = OpenWeatherMapConnection(api_key)
    
    # Input field for location
    location = st.text_input("Enter a location (e.g., city name or latitude/longitude):")
    
    # Input field for date (optional, for future expansion)
    # date = st.date_input("Select a date:")
    
    if st.button("Get Weather Forecast"):
        if location:
            # Fetch weather data
            weather_data = connection.get_weather_data(location)
            
            if weather_data:
                # Display weather information in a table
                weather_info = {
                    "Weather Icon": weather_icons.get(weather_data['weather'][0]['description'], "🌫️"),
                    "Location": weather_data['name'],
                    "Temperature": f"{weather_data['main']['temp']}°C",
                    "Humidity": f"{weather_data['main']['humidity']}%",
                    "Wind Speed": f"{weather_data['wind']['speed']} m/s",
                    "Weather Conditions": weather_data['weather'][0]['description'],
                }
                st.table(pd.DataFrame([weather_info]))

                # Set background image based on weather conditions
                weather_condition = weather_data['weather'][0]['description']
                set_background_image(weather_condition)


            else:
                st.warning("No weather data found for the given location.")

if __name__ == "__main__":
    main()
