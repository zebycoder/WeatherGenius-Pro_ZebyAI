# weather_app.py

# REMOVE THESE LINES:
# subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
# subprocess.run([sys.executable, "-m", "pip", "install", "--no-cache-dir", "-r", "requirements.txt"], check=True)

# ==================== MAIN IMPORTS ====================
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz
import base64

# ==================== APP CONFIGURATION ====================
st.set_page_config(
    page_title="WeatherGenius Pro ☀️",
    page_icon="⛅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ENTERPRISE-GRADE CSS ====================
def inject_css():
    st.markdown(f"""
    <style>
        /* Professional Gradient Background */
        .stApp {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        /* Premium Card Styling */
        .weather-card {{
            background: rgba(255, 255, 255, 0.97);
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            margin-bottom: 2rem;
        }}
        
        /* Animated Button */
        .stButton>button {{
            background: linear-gradient(45deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            padding: 0.75rem 1.5rem;
            transition: all 0.4s ease;
        }}
        
        .stButton>button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(37, 117, 252, 0.3);
        }}
        
        /* Responsive Grid */
        @media (max-width: 768px) {{
            .weather-grid {{
                grid-template-columns: 1fr !important;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

# ==================== WEATHER API SERVICE ====================
class WeatherService:
    @staticmethod
    @st.cache_data(ttl=3600, show_spinner="Fetching weather data...")
    def get_weather_data(city: str, api_key: str) -> dict:
        """Enterprise-grade weather data fetcher with full error handling"""
        try:
            # Current Weather
            current = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric",
                timeout=15
            ).json()
            
            if current.get('cod') != 200:
                raise ValueError(current.get('message', 'Unknown API error'))

            # 5-Day Forecast
            forecast = requests.get(
                f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric",
                timeout=15
            ).json()

            # Air Quality Data
            lat, lon = current["coord"]["lat"], current["coord"]["lon"]
            aqi = requests.get(
                f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}",
                timeout=15
            ).json()

            return {
                "current": current,
                "forecast": forecast,
                "aqi": aqi
            }
            
        except requests.exceptions.RequestException as e:
            st.error(f"Network error: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Processing error: {str(e)}")
            return None

# ==================== UI COMPONENTS ====================
class WeatherUI:
    @staticmethod
    def display_current_weather(data: dict):
        """Premium current weather display with all metrics"""
        current = data["current"]
        weather = current["weather"][0]
        timezone = pytz.timezone("Asia/Karachi")
        
        with st.container():
            st.markdown(f"""
            <div class="weather-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h1 style="margin-bottom: 0.2rem;">{current['name']}, {current['sys']['country']}</h1>
                        <h3 style="margin-top: 0; color: #555;">{weather['main']} ({weather['description'].title()})</h3>
                    </div>
                    <img src="https://openweathermap.org/img/wn/{weather['icon']}@4x.png" width="120">
                </div>
                
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; margin-top: 2rem;">
                    <div>
                        <h4 style="margin-bottom: 0.5rem;">🌡️ Temperature</h4>
                        <p style="font-size: 2rem; margin: 0;">{current['main']['temp']}°C</p>
                        <p>Feels like: {current['main']['feels_like']}°C</p>
                    </div>
                    
                    <div>
                        <h4 style="margin-bottom: 0.5rem;">💧 Humidity</h4>
                        <p style="font-size: 2rem; margin: 0;">{current['main']['humidity']}%</p>
                    </div>
                    
                    <div>
                        <h4 style="margin-bottom: 0.5rem;">🌬️ Wind</h4>
                        <p style="font-size: 2rem; margin: 0;">{current['wind']['speed']} m/s</p>
                        <p>Direction: {current['wind'].get('deg', 'N/A')}°</p>
                    </div>
                    
                    <div>
                        <h4 style="margin-bottom: 0.5rem;">⏱️ Pressure</h4>
                        <p style="font-size: 2rem; margin: 0;">{current['main']['pressure']} hPa</p>
                    </div>
                </div>
                
                <div style="margin-top: 2rem; display: flex; justify-content: space-between;">
                    <div>
                        <h4>🌅 Sunrise</h4>
                        <p>{datetime.fromtimestamp(current["sys"]["sunrise"], timezone).strftime("%H:%M")}</p>
                    </div>
                    <div>
                        <h4>🌇 Sunset</h4>
                        <p>{datetime.fromtimestamp(current["sys"]["sunset"], timezone).strftime("%H:%M")}</p>
                    </div>
                    <div>
                        <h4>👁️ Visibility</h4>
                        <p>{current.get('visibility', 'N/A')} meters</p>
                    </div>
                    <div>
                        <h4>☁️ Clouds</h4>
                        <p>{current['clouds'].get('all', 'N/A')}%</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    @staticmethod
    def display_forecast(data: dict):
        """Interactive 5-day forecast with Plotly visualization"""
        forecast_items = []
        for item in data["forecast"]["list"][::8]:  # Daily forecasts
            forecast_items.append({
                "date": datetime.fromtimestamp(item["dt"]).strftime("%A, %b %d"),
                "temp": item["main"]["temp"],
                "feels_like": item["main"]["feels_like"],
                "humidity": item["main"]["humidity"],
                "weather": item["weather"][0]["main"],
                "icon": item["weather"][0]["icon"],
                "wind_speed": item["wind"]["speed"]
            })
        
        st.markdown("""
        <div class="weather-card">
            <h2>📅 5-Day Forecast</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabular Data
        df = pd.DataFrame(forecast_items)
        st.dataframe(
            df[["date", "temp", "weather", "humidity"]],
            column_config={
                "date": "Date",
                "temp": st.column_config.NumberColumn("Temp (°C)", format="%.1f"),
                "weather": "Conditions",
                "humidity": st.column_config.NumberColumn("Humidity (%)")
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Interactive Plot
        fig = px.line(
            df,
            x="date",
            y="temp",
            title="Temperature Trend",
            markers=True,
            labels={"temp": "Temperature (°C)", "date": "Date"}
        )
        st.plotly_chart(fig, use_container_width=True)

# ==================== MAIN APP ====================
def main():
    inject_css()
    
    # Premium Header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="margin: 0; font-size: 3rem;">WeatherGenius Pro ☀️</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; color: #555;">
            Developed by <strong>Jahanzaib Javed</strong> | <strong>ZebyCoder</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x50/6a11cb/ffffff?text=ZebyCoder", use_column_width=True)
        st.markdown("""
        <div style="margin-top: 1rem; text-align: center;">
            <p><strong>AI/ML Weather Solutions</strong></p>
            <p>📞 +92-300-5590321</p>
            <p>✉ zeb.innerartinteriors@gmail.com</p>
            <p>📍 Lahore, Pakistan</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        city = st.text_input("Enter City Name", "Lahore")
        api_key = st.secrets.get("OPENWEATHER_API_KEY", "")
        
        if st.button("Get Weather", type="primary", use_container_width=True):
            if not api_key:
                st.error("API key missing in Streamlit Secrets!")
            else:
                with st.spinner("Fetching premium weather data..."):
                    if weather_data := WeatherService.get_weather_data(city, api_key):
                        WeatherUI.display_current_weather(weather_data)
                        WeatherUI.display_forecast(weather_data)
                    else:
                        st.error("Failed to fetch weather data. Please check inputs.")

if __name__ == "__main__":
    main()
