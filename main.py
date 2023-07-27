import streamlit as st
import requests

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
                st.write(f"Weather Conditions: {weather_data['weather'][0]['description']}")
            else:
                st.warning("No weather data found for the given location.")
    
if __name__ == "__main__":
    main()
