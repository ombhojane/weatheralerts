import streamlit as st
import requests
import emoji
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
                # Display weather information
                st.write(f"Location: {weather_data['name']}")
                st.write(f"Temperature: {weather_data['main']['temp']}°C")
                st.write(f"Humidity: {weather_data['main']['humidity']}%")
                st.write(f"Wind Speed: {weather_data['wind']['speed']} m/s")
                weather_condition = weather_data['weather'][0]['description']
                st.write(f"Weather Conditions: {weather_condition}")
                # Weather Icons
                if 'clear' in weather_condition.lower():
                    st.write(emoji.emojize(":sunny:"))
                elif 'cloud' in weather_condition.lower():
                    st.write(emoji.emojize(":cloud:"))
                elif 'rain' in weather_condition.lower():
                    st.write(emoji.emojize(":cloud_with_rain:"))
                else:
                    st.write(emoji.emojize(":question:"))

                st.subheader("Weather Forecast for the Previous 4 Days, Today, and Next 4 Days")
                weather_data_list = fetch_weather_data_range(location, days=9)
                df = pd.DataFrame()
                for i, data in enumerate(weather_data_list):
                    date = datetime.strptime(data['date'], "%Y-%m-%d")
                    weekday = date.strftime("%A")
                    weather = data['weather'][0]['description']
                    weather_icon = get_weather_icon(weather)
                    temperature = data['main']['temp']
                    df[f"{weekday}"] = [weather_icon, temperature]

                st.dataframe(df)

            else:
                st.warning("No weather data found for the given location.")

def get_weather_icon(weather_condition):
    if 'clear' in weather_condition.lower():
        return emoji.emojize(":sunny:")
    elif 'cloud' in weather_condition.lower():
        return emoji.emojize(":cloud:")
    elif 'rain' in weather_condition.lower():
        return emoji.emojize(":cloud_with_rain:")
    else:
        return emoji.emojize(":question:")

if __name__ == "__main__":
    main()
