# weather_app.py
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz
import base64

# =============================================
# APP CONFIGURATION
# =============================================
st.set_page_config(
    page_title="WeatherGenius Pro ☀️",
    page_icon="⛅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# CUSTOM CSS (Embedded - no separate file needed)
# =============================================
def inject_css():
    st.markdown(f"""
    <style>
        /* Main Background */
        .stApp {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        /* Header Styling */
        .header {{
            background: linear-gradient(45deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 0 0 15px 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        /* Card Styling */
        .weather-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }}
        
        /* Button Styling */
        .stButton>button {{
            background: linear-gradient(45deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }}
        
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .weather-card {{
                padding: 1rem;
            }}
            .header h1 {{
                font-size: 1.5rem !important;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

# =============================================
# WEATHER DATA FUNCTIONS
# =============================================
@st.cache_data(ttl=3600)
def get_weather_data(city, api_key):
    try:
        # Current Weather
        current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        current_data = requests.get(current_url).json()

        if current_data.get('cod') != 200:
            return None

        # Forecast
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        forecast_data = requests.get(forecast_url).json()

        # Air Quality
        lat, lon = current_data["coord"]["lat"], current_data["coord"]["lon"]
        aqi_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        aqi_data = requests.get(aqi_url).json()

        return {
            "current": current_data,
            "forecast": forecast_data,
            "aqi": aqi_data
        }
    except Exception:
        return None

# =============================================
# UI COMPONENTS
# =============================================
def show_current_weather(data):
    current = data["current"]
    weather = current["weather"][0]
    timezone = pytz.timezone("Asia/Karachi")
    
    st.markdown(f"""
    <div class="weather-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2 style="margin-bottom: 0;">{current['name']}, {current['sys']['country']}</h2>
                <h3 style="margin-top: 0; color: #666;">{weather['main']} ({weather['description'].title()})</h3>
            </div>
            <img src="https://openweathermap.org/img/wn/{weather['icon']}@4x.png" width="120">
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-top: 1.5rem;">
            <div>
                <h4 style="margin-bottom: 0.5rem;">🌡️ Temperature</h4>
                <p style="font-size: 1.5rem; margin-top: 0;">{current['main']['temp']}°C</p>
                <p>Feels like: {current['main']['feels_like']}°C</p>
            </div>
            
            <div>
                <h4 style="margin-bottom: 0.5rem;">💧 Humidity</h4>
                <p style="font-size: 1.5rem; margin-top: 0;">{current['main']['humidity']}%</p>
            </div>
            
            <div>
                <h4 style="margin-bottom: 0.5rem;">🌬️ Wind</h4>
                <p style="font-size: 1.5rem; margin-top: 0;">{current['wind']['speed']} m/s</p>
            </div>
            
            <div>
                <h4 style="margin-bottom: 0.5rem;">⏱️ Pressure</h4>
                <p style="font-size: 1.5rem; margin-top: 0;">{current['main']['pressure']} hPa</p>
            </div>
        </div>
        
        <div style="margin-top: 1.5rem;">
            <p>🌅 Sunrise: {datetime.fromtimestamp(current["sys"]["sunrise"], timezone).strftime("%H:%M")} 
            | 🌇 Sunset: {datetime.fromtimestamp(current["sys"]["sunset"], timezone).strftime("%H:%M")}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_forecast(data):
    forecast_items = []
    for item in data["forecast"]["list"][::8]:  # Get one forecast per day
        date = datetime.fromtimestamp(item["dt"]).strftime("%A, %b %d")
        forecast_items.append({
            "Date": date,
            "Temperature": f"{item['main']['temp']}°C",
            "Weather": item["weather"][0]["main"],
            "Icon": f"https://openweathermap.org/img/wn/{item['weather'][0]['icon']}@2x.png",
            "Humidity": f"{item['main']['humidity']}%",
            "Wind": f"{item['wind']['speed']} m/s"
        })
    
    st.markdown("""
    <div class="weather-card">
        <h2>📅 5-Day Forecast</h2>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(len(forecast_items))
    for idx, forecast in enumerate(forecast_items):
        with cols[idx]:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; border-radius: 10px; background: rgba(255,255,255,0.7);">
                <h4>{forecast['Date'].split(',')[0]}</h4>
                <p><small>{forecast['Date'].split(',')[1]}</small></p>
                <img src="{forecast['Icon']}" width="60">
                <h3>{forecast['Temperature']}</h3>
                <p>{forecast['Weather']}</p>
                <p>💧 {forecast['Humidity']}</p>
                <p>🌬️ {forecast['Wind']}</p>
            </div>
            """, unsafe_allow_html=True)

# =============================================
# MAIN APP
# =============================================
def main():
    inject_css()  # Inject our custom CSS
    
    # Header with branding
    st.markdown(f"""
    <div class="header">
        <h1 style="margin: 0; text-align: center;">WeatherGenius Pro ☀️</h1>
        <p style="text-align: center; margin: 0.5rem 0 0 0; font-size: 1.1rem;">
            Developed by <strong>Jahanzaib Javed</strong> | <strong>ZebyCoder</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    st.sidebar.image("https://via.placeholder.com/150x50/6a11cb/ffffff?text=ZebyCoder", use_column_width=True)
    st.sidebar.markdown("""
    <div style="text-align: center;">
        <p><strong>AI/ML Weather Solutions</strong></p>
        <p>📞 +92-300-5590321</p>
        <p>✉ zeb.innerartinteriors@gmail.com</p>
        <p>📍 Lahore, Pakistan</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Get user input
    city = st.sidebar.text_input("Enter City Name", "Lahore")
    api_key = st.secrets.get("OPENWEATHER_API_KEY", "")
    
    if st.sidebar.button("Get Weather", type="primary"):
        if not api_key:
            st.error("Please configure your OpenWeatherMap API key in Streamlit secrets")
            return
            
        with st.spinner("Fetching weather data..."):
            weather_data = get_weather_data(city, api_key)
            
            if weather_data:
                show_current_weather(weather_data)
                show_forecast(weather_data)
            else:
                st.error("Could not fetch weather data. Please check the city name or try again later.")

if __name__ == "__main__":
    main()
