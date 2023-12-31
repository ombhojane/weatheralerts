import streamlit as st
import requests
import pandas as pd

# Define your API keys directly (replace 'YOUR_OPENWEATHERMAP_API_KEY' and 'YOUR_NEWS_API_KEY' with your actual API keys)
api_key = st.secrets.weather
news_api_key = st.secrets.news

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

# OpenWeatherMap connection
class OpenWeatherMapConnection:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self._connection = None

    def _connect(self):
        if not self._connection:
            self._connection = requests.Session()
        return self._connection

    def _disconnect(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    def get_weather_data(self, location):
        try:
            params = {"q": location, "appid": self.api_key, "units": "metric"}
            response = self._connect().get(self.base_url, params=params)
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            st.error("Error: Unable to connect to the OpenWeatherMap API.")
            return None

    def cursor(self):
        return self._connect()

# to fetch weather-related news
@st.cache_data(ttl=3600)  # Cache data for 1 hour (3600 seconds)
def fetch_weather_news(location):
    try:
        # Set the news query based on the location and weather conditions
        connection = OpenWeatherMapConnection(api_key)
        weather_data = connection.get_weather_data(location)
        weather_condition = weather_data['weather'][0]['main']

        # Use more general terms related to weather or natural disasters
        news_query = f"Weather OR Storm OR Flood OR Hurricane OR Tornado OR {location}"

        # Make API call to NewsAPI
        news_url = f"https://newsapi.org/v2/everything?q={news_query}&apiKey={news_api_key}"
        response = requests.get(news_url)
        data = response.json()

        # Extract relevant news articles from the response
        if data['status'] == 'ok' and data['totalResults'] > 0:
            articles = data['articles']
            news = []
            for article in articles[:5]:  # Display the top 5 news articles
                title = article['title']
                description = article['description']
                url = article['url']
                news.append([title, description, url])
            return news
        else:
            # If specific weather-related news is not available for the given location,
            # fall back to displaying news from the origin country of the location
            origin_country = weather_data['sys']['country']
            news_query_origin_country = f"Weather OR Storm OR Flood OR Hurricane OR Tornado OR {origin_country}"
            news_url_origin_country = f"https://newsapi.org/v2/everything?q={news_query_origin_country}&apiKey={news_api_key}"
            response_origin_country = requests.get(news_url_origin_country)
            data_origin_country = response_origin_country.json()

            if data_origin_country['status'] == 'ok' and data_origin_country['totalResults'] > 0:
                articles_origin_country = data_origin_country['articles']
                news = []
                for article in articles_origin_country[:5]:  # Display the top 5 news articles
                    title = article['title']
                    description = article['description']
                    url = article['url']
                    news.append([title, description, url])
                return news
            else:
                return None

    except requests.exceptions.RequestException as e:
        st.error("Error: Unable to fetch weather-related news.")
        return None

def main():
    st.title("Weather Forecast App with OpenWeatherMap API")

    # connection to OpenWeatherMap API
    connection = OpenWeatherMapConnection(api_key)

    location = st.text_input("Enter a location (e.g., City name, Country name):",
                             help="Example: Mumbai, India or New York, USA")

    if st.button("Get Weather Forecast"):
        if location:
            # Fetch weather data
            weather_data = connection.get_weather_data(location)
            st.write(" ")

            if weather_data:
                # Display weather information
                weather_info = {
                    "Weather Icon": weather_icons.get(weather_data['weather'][0]['main'], "🌫️"),
                    "Location": weather_data['name'],
                    "Temperature": f"{weather_data['main']['temp']}°C",
                    "Humidity": f"{weather_data['main']['humidity']}%",
                    "Wind Speed": f"{weather_data['wind']['speed']} m/s",
                    "Weather Conditions": weather_data['weather'][0]['description'],
                }
                st.table(pd.DataFrame([weather_info]))

                # Fetch weather-related news and display in a section
                weather_news = fetch_weather_news(location)
                if weather_news:
                    st.header("Your Daily Weather Updates with News API")
                    for news_item in weather_news:
                        st.write(f"**{news_item[0]}**")
                        st.write(news_item[1])
                        st.write(f"[Read More]({news_item[2]})")
                        st.markdown("---")

            else:
                st.warning("No weather data found for the given location.")

if __name__ == "__main__":
    main()
