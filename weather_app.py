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
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:zeb.innerartinteriors@gmail.com',
        'Report a bug': 'https://github.com/yourrepo/issues',
        'About': "### AI-Powered Weather App by ZebyCoder"
    }
)

# ==================== CUSTOM CSS ====================
def inject_css():
    st.markdown("""
    <style>
        /* Main Container */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Header Styling */
        .main-header {
            text-align: center;
            padding: 1rem 0;
            background: linear-gradient(to right, #6a11cb, #2575fc);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Weather Cards */
        .weather-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
            transition: transform 0.3s ease;
        }
        .weather-card:hover {
            transform: translateY(-5px);
        }
        
        /* Metrics Styling */
        [data-testid="stMetric"] {
            background: rgba(255,255,255,0.8);
            border-radius: 10px;
            padding: 1rem;
        }
        
        /* Responsive Grid */
        @media (max-width: 768px) {
            .metric-grid {
                grid-template-columns: 1fr !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# ==================== WEATHER SERVICE ====================
class WeatherService:
    @staticmethod
    @st.cache_data(ttl=3600, show_spinner="Fetching real-time weather data...")
    def get_weather_data(city: str, api_key: str) -> dict:
        """Fetch comprehensive weather data with error handling"""
        try:
            # Current Weather
            current = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric",
                timeout=10
            ).json()
            
            if current.get('cod') != 200:
                return None

            # 5-Day Forecast
            forecast = requests.get(
                f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric",
                timeout=10
            ).json()

            # Air Quality
            lat, lon = current["coord"]["lat"], current["coord"]["lon"]
            aqi = requests.get(
                f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}",
                timeout=10
            ).json()

            return {
                "current": current,
                "forecast": forecast,
                "aqi": aqi
            }
        except Exception:
            return None

# ==================== UI COMPONENTS ====================
def display_current_weather(data):
    current = data["current"]
    weather = current["weather"][0]
    timezone = pytz.timezone("Asia/Karachi")
    
    st.markdown(f"""
    <div class="main-header">
        <h1>🌤️ Weather in {current['name']}, {current['sys']['country']}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(f"https://openweathermap.org/img/wn/{weather['icon']}@4x.png", width=150)
    with col2:
        st.markdown(f"""
        <div style="font-size: 1.2rem;">
            <p><strong>Condition:</strong> {weather['main']} ({weather['description'].title()})</p>
            <p><strong>Last Updated:</strong> {datetime.fromtimestamp(current['dt'], timezone).strftime('%Y-%m-%d %H:%M')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main Weather Metrics
    st.markdown("""
    <div class="weather-card">
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;" class="metric-grid">
    """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    metrics = [
        ("🌡️ Temperature", f"{current['main']['temp']}°C", f"Feels like {current['main']['feels_like']}°C"),
        ("💧 Humidity", f"{current['main']['humidity']}%", None),
        ("🌬️ Wind", f"{current['wind']['speed']} m/s", f"Direction: {current['wind'].get('deg', 'N/A')}°"),
        ("⏱️ Pressure", f"{current['main']['pressure']} hPa", None)
    ]
    
    for i, (label, value, delta) in enumerate(metrics):
        with cols[i]:
            st.metric(label, value, delta)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Additional Weather Data
    with st.expander("Detailed Weather Information"):
        cols = st.columns(2)
        with cols[0]:
            st.metric("☁️ Cloudiness", f"{current['clouds'].get('all', 'N/A')}%")
            st.metric("👁️ Visibility", f"{current.get('visibility', 'N/A')} m")
        with cols[1]:
            st.metric("🌅 Sunrise", datetime.fromtimestamp(current['sys']['sunrise'], timezone).strftime('%H:%M'))
            st.metric("🌇 Sunset", datetime.fromtimestamp(current['sys']['sunset'], timezone).strftime('%H:%M'))

def display_forecast(data):
    st.markdown("""
    <div class="weather-card">
        <h2>📅 5-Day Forecast</h2>
    </div>
    """, unsafe_allow_html=True)
    
    forecast_items = []
    for item in data["forecast"]["list"][::8]:  # Daily forecasts
        forecast_items.append({
            "date": datetime.fromtimestamp(item["dt"]).strftime("%A, %b %d"),
            "temp": item["main"]["temp"],
            "feels_like": item["main"]["feels_like"],
            "icon": item["weather"][0]["icon"],
            "description": item["weather"][0]["main"],
            "humidity": item["main"]["humidity"],
            "wind": item["wind"]["speed"]
        })
    
    # Interactive Plotly Chart
    df = pd.DataFrame(forecast_items)
    fig = px.line(
        df, 
        x="date", 
        y="temp", 
        title="Temperature Forecast",
        labels={"temp": "Temperature (°C)", "date": "Date"},
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Daily Forecast Cards
    cols = st.columns(len(forecast_items))
    for idx, day in enumerate(forecast_items):
        with cols[idx]:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; border-radius: 10px; background: rgba(255,255,255,0.8);">
                <h4>{day['date'].split(',')[0]}</h4>
                <p><small>{day['date'].split(',')[1]}</small></p>
                <img src="https://openweathermap.org/img/wn/{day['icon']}@2x.png" width="60">
                <h3>{day['temp']}°C</h3>
                <p>{day['description']}</p>
                <p>💧 {day['humidity']}%</p>
                <p>🌬️ {day['wind']} m/s</p>
            </div>
            """, unsafe_allow_html=True)

def display_air_quality(data):
    if data["aqi"] and data["aqi"].get('list'):
        aqi = data["aqi"]['list'][0]['main']['aqi']
        components = data["aqi"]['list'][0]['components']
        
        aqi_levels = {
            1: ("Good", "🟢"),
            2: ("Fair", "🟡"),
            3: ("Moderate", "🟠"),
            4: ("Poor", "🔴"),
            5: ("Very Poor", "🟣")
        }
        level, emoji = aqi_levels.get(aqi, ("N/A", "❓"))
        
        st.markdown(f"""
        <div class="weather-card">
            <h2>💨 Air Quality: {emoji} {level} (AQI: {aqi})</h2>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
        """, unsafe_allow_html=True)
        
        cols = st.columns(4)
        pollutants = [
            ("CO", components.get('co'), "μg/m³"),
            ("NO₂", components.get('no2'), "μg/m³"),
            ("O₃", components.get('o3'), "μg/m³"),
            ("PM2.5", components.get('pm2_5'), "μg/m³")
        ]
        
        for i, (name, value, unit) in enumerate(pollutants):
            with cols[i]:
                st.metric(name, f"{value:.2f}" if value else "N/A", unit)
        
        st.markdown("</div></div>", unsafe_allow_html=True)

# ==================== MAIN APP ====================
def main():
    inject_css()
    
    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>🌍 WeatherGenius Pro</h1>
        <p>AI-Powered Weather Forecasting Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Developer Info in Sidebar
    with st.sidebar:
        st.title("ZebyCoder Solutions")
        st.write("**Developed by:** Jahanzaib Javed")
        st.write("**Specialization:** AI/ML & Full-Stack Development")
        st.write("📞 +92-300-5590321")
        st.write("✉ zeb.innerartinteriors@gmail.com")
        st.write("📧 zeb.javed1@outlook.com")
        st.write("📍 Lahore, Pakistan")
        st.markdown("---")
        st.write("**Key Features:**")
        st.write("- Real-time weather data")
        st.write("- 5-day detailed forecast")
        st.write("- Air quality monitoring")
        st.write("- Interactive visualizations")
    
    # Main Content Area
    api_key = st.secrets.get("OPENWEATHER_API_KEY", "")
    
    # City Input at Top of Main Page
    city = st.text_input("Enter City Name", "Lahore", key="city_input")
    
    if st.button("Get Weather", type="primary", use_container_width=True):
        if not api_key:
            st.error("API key missing in Streamlit Secrets!")
        else:
            with st.spinner("Fetching the latest weather data..."):
                weather_data = WeatherService.get_weather_data(city, api_key)
                if weather_data:
                    display_current_weather(weather_data)
                    display_forecast(weather_data)
                    display_air_quality(weather_data)
                    
                    # Show Map
                    st.markdown("""
                    <div class="weather-card">
                        <h2>📍 Location on Map</h2>
                    </div>
                    """, unsafe_allow_html=True)
                    map_data = pd.DataFrame({
                        'lat': [weather_data["current"]["coord"]["lat"]],
                        'lon': [weather_data["current"]["coord"]["lon"]]
                    })
                    st.map(map_data, zoom=10)
                else:
                    st.error("Failed to fetch weather data. Please check the city name and try again.")

    # Welcome Message (only shown before first search)
    if not st.session_state.get('weather_data_fetched', False):
        st.markdown("""
        <div class="weather-card">
            <h2>Welcome to WeatherGenius Pro!</h2>
            <p>Get accurate weather forecasts and air quality data for any location worldwide.</p>
            <p>Enter a city name above and click "Get Weather" to begin.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
