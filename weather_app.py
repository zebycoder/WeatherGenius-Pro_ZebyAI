# weather_app.py

# ==================== MAIN IMPORTS ====================
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz
import base64
# import os # Uncomment if using python-dotenv for local testing
# from dotenv import load_dotenv # Uncomment if using python-dotenv for local testing

# Uncomment this for local testing if you are using a .env file
# load_dotenv()

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
                # Provide specific error messages from the API if available
                error_message = current.get('message', 'Unknown API error')
                if current.get('cod') == '404':
                    raise ValueError(f"City not found: {city}. Please check the spelling.")
                elif current.get('cod') == '401':
                    raise ValueError("Invalid API key. Please check your OpenWeatherMap API key.")
                else:
                    raise ValueError(f"API Error: {error_message}")

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
            st.error(f"Network error: Unable to connect to OpenWeatherMap API. Please check your internet connection or try again later. Details: {str(e)}")
            return None
        except ValueError as e:
            st.error(f"Data Error: {str(e)}")
            return None
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            return None

# ==================== UI COMPONENTS ====================
class WeatherUI:
    @staticmethod
    def display_current_weather(data: dict):
        """Premium current weather display with all metrics"""
        current = data["current"]
        weather = current["weather"][0]
        # Use timezone from API if available, otherwise default to Lahore
        try:
            # OpenWeatherMap current data doesn't directly provide timezone name, but uses 'timezone' offset in seconds
            # For accurate local time, a more robust solution would be to use a separate API like Google Time Zone API
            # or pre-map common cities to their timezones.
            # For simplicity, sticking to a fixed timezone as in original code, but mentioning improvement.
            timezone = pytz.timezone("Asia/Karachi") # Defaulting to Lahore, Pakistan timezone
            
            # For truly dynamic timezone based on coordinates, you'd need a more complex lookup
            # using something like timezonefinder or a timezone API.
            # For now, sticking to the requested "Asia/Karachi"
        except pytz.UnknownTimeZoneError:
            st.warning("Could not determine local timezone. Displaying times in Asia/Karachi.")
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
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-top: 2rem;">
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
                     <div>
                        <h4 style="margin-bottom: 0.5rem;">💧 Precip. (1hr)</h4>
                        <p style="font-size: 2rem; margin: 0;">{current.get('rain', {}).get('1h', current.get('snow', {}).get('1h', 0))} mm</p>
                        <p> (Rain/Snow last hour) </p>
                    </div>
                </div>
                
                <div style="margin-top: 2rem; display: flex; justify-content: space-between; flex-wrap: wrap;">
                    <div style="margin-right: 1rem; margin-bottom: 1rem;">
                        <h4>🌅 Sunrise</h4>
                        <p>{datetime.fromtimestamp(current["sys"]["sunrise"], timezone).strftime("%H:%M")}</p>
                    </div>
                    <div style="margin-right: 1rem; margin-bottom: 1rem;">
                        <h4>🌇 Sunset</h4>
                        <p>{datetime.fromtimestamp(current["sys"]["sunset"], timezone).strftime("%H:%M")}</p>
                    </div>
                    <div style="margin-right: 1rem; margin-bottom: 1rem;">
                        <h4>👁️ Visibility</h4>
                        <p>{current.get('visibility', 'N/A')} meters</p>
                    </div>
                    <div style="margin-right: 1rem; margin-bottom: 1rem;">
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
        for item in data["forecast"]["list"]: # Process all items, then filter for daily
            forecast_items.append({
                "datetime": datetime.fromtimestamp(item["dt"]),
                "date": datetime.fromtimestamp(item["dt"]).strftime("%A, %b %d"),
                "time": datetime.fromtimestamp(item["dt"]).strftime("%H:%M"),
                "temp": item["main"]["temp"],
                "feels_like": item["main"]["feels_like"],
                "humidity": item["main"]["humidity"],
                "weather": item["weather"][0]["main"],
                "description": item["weather"][0]["description"].title(),
                "icon": item["weather"][0]["icon"],
                "wind_speed": item["wind"]["speed"],
                "pressure": item["main"]["pressure"]
            })
        
        df_forecast = pd.DataFrame(forecast_items)

        st.markdown("""
        <div class="weather-card">
            <h2>📅 5-Day Forecast</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Display forecast in a tabbed interface
        tab_daily, tab_hourly, tab_chart = st.tabs(["Daily Summary", "Detailed Hourly", "Temperature Trend"])

        with tab_daily:
            # Aggregate daily summary
            daily_summary = df_forecast.groupby(df_forecast['datetime'].dt.date).agg(
                max_temp=('temp', 'max'),
                min_temp=('temp', 'min'),
                avg_humidity=('humidity', 'mean'),
                main_weather=('weather', lambda x: x.mode()[0] if not x.empty else 'N/A'),
                icon=('icon', lambda x: x.iloc[len(x)//2]) # Get icon for a middle point of the day
            ).reset_index()
            daily_summary.rename(columns={'datetime': 'Date'}, inplace=True)
            daily_summary['Date'] = daily_summary['Date'].dt.strftime("%A, %b %d")

            st.dataframe(
                daily_summary,
                column_config={
                    "Date": "Date",
                    "max_temp": st.column_config.NumberColumn("Max Temp (°C)", format="%.1f"),
                    "min_temp": st.column_config.NumberColumn("Min Temp (°C)", format="%.1f"),
                    "avg_humidity": st.column_config.NumberColumn("Avg Humidity (%)", format="%.0f"),
                    "main_weather": "Conditions"
                },
                hide_index=True,
                use_container_width=True
            )

        with tab_hourly:
            st.dataframe(
                df_forecast[['date', 'time', 'temp', 'feels_like', 'description', 'humidity', 'wind_speed', 'pressure']],
                column_config={
                    "date": "Date",
                    "time": "Time",
                    "temp": st.column_config.NumberColumn("Temp (°C)", format="%.1f"),
                    "feels_like": st.column_config.NumberColumn("Feels Like (°C)", format="%.1f"),
                    "description": "Conditions",
                    "humidity": st.column_config.NumberColumn("Humidity (%)"),
                    "wind_speed": st.column_config.NumberColumn("Wind (m/s)", format="%.1f"),
                    "pressure": st.column_config.NumberColumn("Pressure (hPa)")
                },
                hide_index=True,
                use_container_width=True
            )
            
        with tab_chart:
            # Interactive Plot - Temperature Trend
            fig_temp = px.line(
                df_forecast,
                x="datetime",
                y="temp",
                title="5-Day Temperature Trend",
                markers=True,
                labels={"temp": "Temperature (°C)", "datetime": "Date and Time"},
                hover_data={"feels_like": True, "humidity": True, "description": True}
            )
            fig_temp.update_xaxes(
                dtick="D1",
                tickformat="%b %d\n%A",
                showgrid=True
            )
            fig_temp.update_yaxes(title_text="Temperature (°C)")
            st.plotly_chart(fig_temp, use_container_width=True)

            # Interactive Plot - Humidity Trend
            fig_humidity = px.line(
                df_forecast,
                x="datetime",
                y="humidity",
                title="5-Day Humidity Trend",
                markers=True,
                labels={"humidity": "Humidity (%)", "datetime": "Date and Time"},
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            fig_humidity.update_xaxes(
                dtick="D1",
                tickformat="%b %d\n%A",
                showgrid=True
            )
            fig_humidity.update_yaxes(title_text="Humidity (%)")
            st.plotly_chart(fig_humidity, use_container_width=True)
            
    @staticmethod
    def display_air_quality(data: dict):
        """Displays air quality index and components."""
        aqi_data = data["aqi"]
        if aqi_data and aqi_data.get('list'):
            aqi_info = aqi_data['list'][0]['main']
            components = aqi_data['list'][0]['components']

            aqi_value = aqi_info['aqi']
            
            # AQI category mapping (from OpenWeatherMap API docs)
            aqi_categories = {
                1: "Good",
                2: "Fair",
                3: "Moderate",
                4: "Poor",
                5: "Very Poor"
            }
            aqi_category = aqi_categories.get(aqi_value, "N/A")

            st.markdown(f"""
            <div class="weather-card">
                <h2>💨 Air Quality Index (AQI)</h2>
                <p style="font-size: 2rem; margin: 0;"><strong>{aqi_category}</strong> (AQI: {aqi_value})</p>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 1rem; margin-top: 1rem;">
                    <div><strong>CO:</strong> {components.get('co', 'N/A')} µg/m³</div>
                    <div><strong>NO:</strong> {components.get('no', 'N/A')} µg/m³</div>
                    <div><strong>NO2:</strong> {components.get('no2', 'N/A')} µg/m³</div>
                    <div><strong>O3:</strong> {components.get('o3', 'N/A')} µg/m³</div>
                    <div><strong>SO2:</strong> {components.get('so2', 'N/A')} µg/m³</div>
                    <div><strong>PM2.5:</strong> {components.get('pm2_5', 'N/A')} µg/m³</div>
                    <div><strong>PM10:</strong> {components.get('pm10', 'N/A')} µg/m³</div>
                    <div><strong>NH3:</strong> {components.get('nh3', 'N/A')} µg/m³</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Air Quality data not available for this location.")

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
        # Example of a local image, replace with your actual logo if you have one locally
        # st.image("path/to/your/logo.png", use_column_width=True)
        # Using a placeholder image for demonstration
        st.image("https://via.placeholder.com/200x50/6a11cb/ffffff?text=ZebyCoder", use_column_width=True)
        st.markdown("""
        <div style="margin-top: 1rem; text-align: center;">
            <p><strong>AI/ML Weather Solutions</strong></p>
            <p>📞 +92-300-5590321</p>
            <p>✉ zeb.innerartinteriors@gmail.com</p>
            <p>📍 Lahore, Pakistan</p>
            <p style="font-size: 0.8rem; color: #777;">&copy; 2024 ZebyCoder. All rights reserved.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        city = st.text_input("Enter City Name", "Lahore")
        
        # Priority for API key: Streamlit Secrets > Environment Variable (for local .env)
        api_key = st.secrets.get("OPENWEATHER_API_KEY")
        # if not api_key: # Uncomment for local testing with .env
        #     api_key = os.getenv("OPENWEATHER_API_KEY")
            
        if st.button("Get Weather", type="primary", use_container_width=True):
            if not api_key:
                st.error("OpenWeatherMap API key missing! Please add it to Streamlit Secrets or your .env file.")
            else:
                with st.spinner("Fetching premium weather data..."):
                    if weather_data := WeatherService.get_weather_data(city, api_key):
                        WeatherUI.display_current_weather(weather_data)
                        st.markdown("---")
                        WeatherUI.display_forecast(weather_data)
                        st.markdown("---")
                        WeatherUI.display_air_quality(weather_data)
                    # Error messages are handled inside WeatherService.get_weather_data,
                    # so no need for an else block here for error reporting.

if __name__ == "__main__":
    main()
