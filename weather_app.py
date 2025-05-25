# ==================== MAIN IMPORTS ====================
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# ==================== APP CONFIGURATION ====================
st.set_page_config(
    page_title="WeatherGenius Pro ☀️",
    page_icon="⛅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== WEATHER SERVICE ====================
class WeatherService:
    @staticmethod
    @st.cache_data(ttl=3600)
    def get_weather_data(city: str, api_key: str) -> dict:
        """Fetch weather data with robust error handling"""
        try:
            # Current Weather
            current = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric",
                timeout=10
            ).json()
            
            if current.get('cod') != 200:
                return None

            # Forecast
            forecast = requests.get(
                f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric",
                timeout=10
            ).json()

            return {
                "current": current,
                "forecast": forecast
            }
        except Exception:
            return None

# ==================== UI COMPONENTS ====================
def display_current_weather(data):
    current = data["current"]
    weather = current["weather"][0]
    timezone = pytz.timezone("Asia/Karachi")
    
    st.subheader(f"Weather in {current['name']}, {current['sys']['country']}")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(f"https://openweathermap.org/img/wn/{weather['icon']}@4x.png", width=150)
    with col2:
        st.metric("Temperature", f"{current['main']['temp']}°C", f"Feels like {current['main']['feels_like']}°C")
        st.write(f"**Condition:** {weather['main']} ({weather['description'].title()})")
    
    cols = st.columns(4)
    with cols[0]:
        st.metric("Humidity", f"{current['main']['humidity']}%")
    with cols[1]:
        st.metric("Wind Speed", f"{current['wind']['speed']} m/s")
    with cols[2]:
        st.metric("Pressure", f"{current['main']['pressure']} hPa")
    with cols[3]:
        st.metric("Visibility", f"{current.get('visibility', 'N/A')} m")
    
    st.write(f"**Sunrise:** {datetime.fromtimestamp(current['sys']['sunrise'], timezone).strftime('%H:%M')} | "
             f"**Sunset:** {datetime.fromtimestamp(current['sys']['sunset'], timezone).strftime('%H:%M')}")

def display_forecast(data):
    st.subheader("5-Day Forecast")
    
    forecast_days = []
    for item in data["forecast"]["list"][::8]:  # Daily forecasts
        forecast_days.append({
            "date": datetime.fromtimestamp(item["dt"]).strftime("%A"),
            "temp": item["main"]["temp"],
            "icon": item["weather"][0]["icon"],
            "description": item["weather"][0]["main"]
        })
    
    cols = st.columns(len(forecast_days))
    for idx, day in enumerate(forecast_days):
        with cols[idx]:
            st.image(f"https://openweathermap.org/img/wn/{day['icon']}@2x.png", width=50)
            st.write(f"**{day['date']}**")
            st.write(f"{day['temp']}°C")
            st.write(day['description'])

# ==================== MAIN APP ====================
def main():
    # Sidebar Configuration
    with st.sidebar:
        st.title("ZebyCoder Solutions")
        st.write("**Developed by:** Jahanzaib Javed")
        st.write("**Specialization:** AI/ML & Full-Stack Development")
        st.write("📞 +92-300-5590321")
        st.write("✉ zeb.innerartinteriors@gmail.com")
        st.write("📧 zeb.javed1@outlook.com")
        st.write("📍 Lahore, Pakistan")
        st.markdown("---")
        
        city = st.text_input("Enter City Name", "Lahore")
        api_key = st.secrets.get("OPENWEATHER_API_KEY", "")
        
        if st.button("Get Weather", type="primary"):
            if not api_key:
                st.error("API key missing in Streamlit Secrets!")
            else:
                with st.spinner("Fetching weather data..."):
                    if weather_data := WeatherService.get_weather_data(city, api_key):
                        display_current_weather(weather_data)
                        display_forecast(weather_data)
                    else:
                        st.error("Failed to fetch weather data")

    # Main Content Area
    st.title("🌍 WeatherGenius Pro")
    st.write("Discover real-time weather conditions and forecasts for any city worldwide")
    st.markdown("---")
    
    if not st.session_state.get('weather_data_fetched', False):
        st.write("""
        ### Welcome to WeatherGenius Pro!
        
        **Key Features:**
        - ⚡ Instant weather updates
        - 🗓️ 5-day forecasts
        - 📊 Interactive charts
        - 📱 Mobile-friendly
        
        Enter a city name in the sidebar and click 'Get Weather' to begin!
        """)

if __name__ == "__main__":
    main()
