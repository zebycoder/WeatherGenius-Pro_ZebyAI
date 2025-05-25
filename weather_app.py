# weather_app.py

# ==================== MAIN IMPORTS ====================
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz
# import os # Uncomment if using python-dotenv for local testing
# from dotenv import load_dotenv # Uncomment if using python-dotenv for local testing

# Uncomment this for local testing if you are using a .env file
# load_dotenv()

# ==================== APP CONFIGURATION ====================
st.set_page_config(
    page_title="WeatherGenius Pro ☀️",
    page_icon="⛅",
    layout="wide", # Use wide layout for more space
    initial_sidebar_state="expanded"
)

# ==================== ENTERPRISE-GRADE CSS FOR SUPER ATTRACTIVE UI ====================
def inject_css():
    st.markdown("""
    <style>
        /* General App Styling */
        .stApp {
            background: linear-gradient(135deg, #e0f2f7 0%, #c1e4f2 100%); /* Light blue gradient */
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333;
        }

        /* Header Styling */
        .stApp > header {
            background-color: transparent;
            padding: 0;
        }
        .stApp > header .st-emotion-cache-1gh2thc {
            padding-top: 0;
        }

        /* Custom Header for App Title */
        .app-header {
            text-align: center;
            padding: 2rem 0 1rem;
            background: linear-gradient(to right, #6a11cb, #2575fc); /* Purple to blue gradient */
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        }
        .app-tagline {
            text-align: center;
            font-size: 1.3rem;
            color: #4a4a4a;
            margin-bottom: 2rem;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }

        /* Premium Card Styling */
        .weather-card {
            background: rgba(255, 255, 255, 0.98);
            border-radius: 20px; /* More rounded corners */
            padding: 2.5rem;
            box-shadow: 0 12px 40px rgba(31, 38, 135, 0.1); /* Softer, larger shadow */
            backdrop-filter: blur(8px); /* Stronger blur effect */
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            margin-bottom: 2.5rem;
            transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        }
        .weather-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 18px 50px rgba(31, 38, 135, 0.15);
        }

        /* Animated Button */
        .stButton>button {
            background: linear-gradient(45deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            border: none;
            border-radius: 10px; /* More rounded buttons */
            font-weight: bold;
            padding: 0.9rem 2rem; /* Larger padding */
            transition: all 0.4s ease;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }
        .stButton>button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(37, 117, 252, 0.4);
            filter: brightness(1.1);
        }

        /* Input Field Styling */
        .stTextInput > div > div > input {
            border-radius: 10px;
            border: 1px solid #a0c4ff;
            padding: 0.75rem 1rem;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.08);
            transition: border-color 0.3s, box-shadow 0.3s;
        }
        .stTextInput > div > div > input:focus {
            border-color: #2575fc;
            box-shadow: 0 0 0 0.2rem rgba(37, 117, 252, 0.25);
        }

        /* Metric Styling */
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.8);
            border-radius: 15px;
            padding: 1rem 1.5rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border: 1px solid rgba(255, 255, 255, 0.5);
        }
        [data-testid="stMetric"] label {
            font-size: 1.1em;
            color: #555;
            font-weight: 600;
        }
        [data-testid="stMetric"] .st-emotion-cache-1wivf6q { /* Value */
            font-size: 2.2em;
            font-weight: bold;
            color: #2575fc;
        }
        [data-testid="stMetric"] .st-emotion-cache-121p57u { /* Delta */
            color: #666;
            font-size: 0.9em;
        }

        /* Responsive Grid for Weather Details */
        .weather-details-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
        }

        /* Forecast Cards */
        .forecast-card {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 6px 20px rgba(0,0,0,0.08);
            text-align: center;
            transition: transform 0.2s ease-in-out;
        }
        .forecast-card:hover {
            transform: translateY(-3px);
        }
        .forecast-card h4 {
            color: #6a11cb;
            margin-bottom: 0.5rem;
        }
        .forecast-card p {
            margin: 0.2rem 0;
            font-size: 0.95rem;
            color: #444;
        }
        .forecast-card img {
            margin-bottom: 0.5rem;
        }

        /* Sidebar Styling */
        .st-emotion-cache-1l02z8d { /* Sidebar background */
            background: linear-gradient(180deg, #6a11cb 0%, #2575fc 100%);
            color: white;
        }
        .st-emotion-cache-1l02z8d h1, .st-emotion-cache-1l02z8d h2, .st-emotion-cache-1l02z8d h3, .st-emotion-cache-1l02z8d h4, .st-emotion-cache-1l02z8d p, .st-emotion-cache-1l02z8d a {
            color: white !important;
        }
        .sidebar-info p {
            font-size: 0.95rem;
            margin-bottom: 0.5rem;
        }
        .sidebar-info strong {
            color: #e0f2f7;
        }

        /* Plotly Chart Styling */
        .stPlotlyChart {
            border-radius: 15px;
            overflow: hidden; /* Ensures borders are respected */
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            margin-top: 1.5rem;
        }

        /* Responsive Adjustments */
        @media (max-width: 768px) {
            .app-header {
                font-size: 2.5rem;
            }
            .app-tagline {
                font-size: 1rem;
            }
            .weather-card {
                padding: 1.5rem;
            }
            .weather-details-grid {
                grid-template-columns: 1fr; /* Stack on small screens */
            }
            .stButton>button {
                padding: 0.7rem 1.2rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# ==================== WEATHER API SERVICE ====================
class WeatherService:
    @staticmethod
    @st.cache_data(ttl=3600, show_spinner="Fetching premium weather data...")
    def get_weather_data(city: str, api_key: str) -> dict:
        """Enterprise-grade weather data fetcher with full error handling"""
        try:
            # Current Weather
            current = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric",
                timeout=15
            ).json()
            
            if current.get('cod') != 200:
                error_message = current.get('message', 'Unknown API error')
                if current.get('cod') == '404':
                    raise ValueError(f"City not found: '{city}'. Please check the spelling.")
                elif current.get('cod') == '401':
                    raise ValueError("Invalid OpenWeatherMap API key. Please check your Streamlit Secrets.")
                else:
                    raise ValueError(f"OpenWeatherMap API Error: {error_message}")

            # 5-Day Forecast (3-hour step, ~40 items for 5 days)
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
            
        except requests.exceptions.ConnectionError:
            st.error("Network connection failed. Please check your internet connection.")
            return None
        except requests.exceptions.Timeout:
            st.error("The request to OpenWeatherMap timed out. Please try again later.")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"A network error occurred: {str(e)}")
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
        
        # Default to Asia/Karachi if timezone info is not reliable or available from API
        # OpenWeatherMap provides 'timezone' as offset in seconds, not a timezone name.
        # For precise local time, a more advanced solution would involve a timezone lookup service.
        timezone = pytz.timezone("Asia/Karachi")
        
        st.markdown(f"""
        <div class="weather-card">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <h1 style="margin-bottom: 0.2rem; font-size: 2.5rem; color: #333;">{current['name']}, {current['sys']['country']}</h1>
                    <h3 style="margin-top: 0; color: #555; font-weight: normal;">{weather['main']} ({weather['description'].title()})</h3>
                </div>
                <img src="https://openweathermap.org/img/wn/{weather['icon']}@4x.png" width="120" alt="{weather['description']}">
            </div>
            
            <div style="text-align: center; margin: 1.5rem 0;">
                <p style="font-size: 4rem; font-weight: bold; color: #2575fc; margin: 0;">{current['main']['temp']}°C</p>
                <p style="font-size: 1.2rem; color: #666;">Feels like: {current['main']['feels_like']}°C</p>
            </div>

            <div class="weather-details-grid">
                <div data-testid="stMetric">
                    <label>💧 Humidity</label>
                    <div class="st-emotion-cache-1wivf6q">{current['main']['humidity']}%</div>
                </div>
                <div data-testid="stMetric">
                    <label>🌬️ Wind Speed</label>
                    <div class="st-emotion-cache-1wivf6q">{current['wind']['speed']} m/s</div>
                    <div class="st-emotion-cache-121p57u">Direction: {current['wind'].get('deg', 'N/A')}°</div>
                </div>
                <div data-testid="stMetric">
                    <label>⏱️ Pressure</label>
                    <div class="st-emotion-cache-1wivf6q">{current['main']['pressure']} hPa</div>
                </div>
                <div data-testid="stMetric">
                    <label>☁️ Cloudiness</label>
                    <div class="st-emotion-cache-1wivf6q">{current['clouds'].get('all', 'N/A')}%</div>
                </div>
                <div data-testid="stMetric">
                    <label>👁️ Visibility</label>
                    <div class="st-emotion-cache-1wivf6q">{current.get('visibility', 'N/A')} m</div>
                </div>
                <div data-testid="stMetric">
                    <label>☀️ UV Index</label>
                    <div class="st-emotion-cache-1wivf6q">N/A</div> <div class="st-emotion-cache-121p57u">(Requires separate API call)</div>
                </div>
            </div>
            
            <div style="display: flex; justify-content: space-around; margin-top: 2rem; flex-wrap: wrap; text-align: center;">
                <div style="margin: 0.5rem;">
                    <h4>🌅 Sunrise</h4>
                    <p>{datetime.fromtimestamp(current["sys"]["sunrise"], timezone).strftime("%H:%M")}</p>
                </div>
                <div style="margin: 0.5rem;">
                    <h4>🌇 Sunset</h4>
                    <p>{datetime.fromtimestamp(current["sys"]["sunset"], timezone).strftime("%H:%M")}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def display_forecast(data: dict):
        """Interactive 5-day forecast with Plotly visualization and daily cards"""
        forecast_items = []
        for item in data["forecast"]["list"]:
            forecast_items.append({
                "dt": item["dt"], # Keep original timestamp for Plotly
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
        
        # Tabbed interface for forecast
        tab_daily_cards, tab_hourly_table, tab_charts = st.tabs(["Daily Summary", "Detailed Hourly", "Temperature & Humidity Trends"])

        with tab_daily_cards:
            st.markdown("### Daily Overview")
            # Group by day and get key stats for daily cards
            daily_summary = df_forecast.groupby(df_forecast['datetime'].dt.date).agg(
                max_temp=('temp', 'max'),
                min_temp=('temp', 'min'),
                avg_humidity=('humidity', 'mean'),
                main_weather=('weather', lambda x: x.mode()[0] if not x.empty else 'N/A'),
                description=('description', lambda x: x.mode()[0] if not x.empty else 'N/A'),
                icon=('icon', lambda x: x.iloc[len(x)//2]) # Get icon for a middle point of the day
            ).reset_index()
            
            # Fix for AttributeError: 'datetime.date' object has no attribute '.dt'
            daily_summary['Date'] = daily_summary['datetime'].apply(lambda x: x.strftime("%A, %b %d"))

            # Display daily cards in a responsive grid
            cols = st.columns(len(daily_summary))
            for i, row in daily_summary.iterrows():
                with cols[i]:
                    st.markdown(f"""
                    <div class="forecast-card">
                        <h4>{row['Date']}</h4>
                        <img src="https://openweathermap.org/img/wn/{row['icon']}@2x.png" width="60" alt="{row['description']}">
                        <p><strong>{row['main_weather']}</strong></p>
                        <p>Max: {row['max_temp']:.1f}°C</p>
                        <p>Min: {row['min_temp']:.1f}°C</p>
                        <p>Avg Hum: {row['avg_humidity']:.0f}%</p>
                    </div>
                    """, unsafe_allow_html=True)

        with tab_hourly_table:
            st.markdown("### Hourly Details")
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
            
        with tab_charts:
            st.markdown("### Visual Trends")
            # Interactive Plot - Temperature Trend
            fig_temp = px.line(
                df_forecast,
                x="datetime",
                y="temp",
                title="Temperature Trend Over 5 Days",
                markers=True,
                labels={"temp": "Temperature (°C)", "datetime": "Date and Time"},
                hover_data={"feels_like": True, "humidity": True, "description": True},
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
            fig_temp.update_xaxes(
                dtick="D1",
                tickformat="%b %d\n%A",
                showgrid=True,
                title_text="Date"
            )
            fig_temp.update_yaxes(title_text="Temperature (°C)")
            fig_temp.update_layout(hovermode="x unified") # Enhanced hover
            st.plotly_chart(fig_temp, use_container_width=True)

            # Interactive Plot - Humidity Trend
            fig_humidity = px.line(
                df_forecast,
                x="datetime",
                y="humidity",
                title="Humidity Trend Over 5 Days",
                markers=True,
                labels={"humidity": "Humidity (%)", "datetime": "Date and Time"},
                color_discrete_sequence=px.colors.qualitative.Dark24 # Different color palette
            )
            fig_humidity.update_xaxes(
                dtick="D1",
                tickformat="%b %d\n%A",
                showgrid=True,
                title_text="Date"
            )
            fig_humidity.update_yaxes(title_text="Humidity (%)")
            fig_humidity.update_layout(hovermode="x unified")
            st.plotly_chart(fig_humidity, use_container_width=True)
            
    @staticmethod
    def display_air_quality(data: dict):
        """Displays air quality index and components."""
        aqi_data = data["aqi"]
        if aqi_data and aqi_data.get('list'):
            aqi_info = aqi_data['list'][0]['main']
            components = aqi_data['list'][0]['components']

            aqi_value = aqi_info['aqi']
            
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
                <p style="font-size: 2.5rem; font-weight: bold; color: #6a11cb; margin: 0.5rem 0;">
                    {aqi_category} (AQI: {aqi_value})
                </p>
                <p style="font-size: 0.9rem; color: #777; margin-bottom: 1.5rem;">
                    (AQI scale: 1=Good, 2=Fair, 3=Moderate, 4=Poor, 5=Very Poor)
                </p>
                <div class="weather-details-grid">
                    <div data-testid="stMetric">
                        <label>CO</label>
                        <div class="st-emotion-cache-1wivf6q">{components.get('co', 'N/A')}</div>
                        <div class="st-emotion-cache-121p57u">µg/m³</div>
                    </div>
                    <div data-testid="stMetric">
                        <label>NO</label>
                        <div class="st-emotion-cache-1wivf6q">{components.get('no', 'N/A')}</div>
                        <div class="st-emotion-cache-121p57u">µg/m³</div>
                    </div>
                    <div data-testid="stMetric">
                        <label>NO2</label>
                        <div class="st-emotion-cache-1wivf6q">{components.get('no2', 'N/A')}</div>
                        <div class="st-emotion-cache-121p57u">µg/m³</div>
                    </div>
                    <div data-testid="stMetric">
                        <label>O3</label>
                        <div class="st-emotion-cache-1wivf6q">{components.get('o3', 'N/A')}</div>
                        <div class="st-emotion-cache-121p57u">µg/m³</div>
                    </div>
                    <div data-testid="stMetric">
                        <label>SO2</label>
                        <div class="st-emotion-cache-1wivf6q">{components.get('so2', 'N/A')}</div>
                        <div class="st-emotion-cache-121p57u">µg/m³</div>
                    </div>
                    <div data-testid="stMetric">
                        <label>PM2.5</label>
                        <div class="st-emotion-cache-1wivf6q">{components.get('pm2_5', 'N/A')}</div>
                        <div class="st-emotion-cache-121p57u">µg/m³</div>
                    </div>
                    <div data-testid="stMetric">
                        <label>PM10</label>
                        <div class="st-emotion-cache-1wivf6q">{components.get('pm10', 'N/A')}</div>
                        <div class="st-emotion-cache-121p57u">µg/m³</div>
                    </div>
                    <div data-testid="stMetric">
                        <label>NH3</label>
                        <div class="st-emotion-cache-1wivf6q">{components.get('nh3', 'N/A')}</div>
                        <div class="st-emotion-cache-121p57u">µg/m³</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Air Quality data not available for this location.")

# ==================== MAIN APP LOGIC ====================
def main():
    inject_css() # Inject custom CSS for styling

    # --- Hero Section: Title, Tagline, City Input, Get Weather Button ---
    st.markdown('<h1 class="app-header">WeatherGenius Pro ☀️</h1>', unsafe_allow_html=True)
    st.markdown('<p class="app-tagline">Your ultimate AI-powered companion for precise global weather forecasting and air quality analysis.</p>', unsafe_allow_html=True)

    # City input and button moved to main content area for prominence
    col_city_input, col_button_go = st.columns([3, 1])
    with col_city_input:
        city = st.text_input("Enter City Name (e.g., London, Tokyo, Lahore)", "Lahore", key="main_city_input", help="Type any city name from around the world.")
    with col_button_go:
        st.markdown("<br>", unsafe_allow_html=True) # Align button with text input
        get_weather_button = st.button("Get Weather", type="primary", use_container_width=True)

    st.markdown("---") # Visual separator

    # --- Sidebar: Developer Info ---
    with st.sidebar:
        st.image("https://via.placeholder.com/200x50/6a11cb/ffffff?text=ZebyCoder", use_column_width=True, caption="Powered by ZebyCoder")
        st.markdown("""
        <div class="sidebar-info" style="margin-top: 1.5rem; text-align: center;">
            <p><strong>Developed by:</strong> Jahanzaib Javed</p>
            <p><strong>Brand:</strong> ZebyCoder</p>
            <p>📞 +92-300-5590321</p>
            <p>✉ zeb.innerartinteriors@gmail.com</p>
            <p>📍 Lahore, Pakistan</p>
            <p style="font-size: 0.8rem; color: #e0f2f7; margin-top: 1rem;">&copy; 2024 ZebyCoder. All rights reserved.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.info("💡 **Tip:** This app fetches real-time data from OpenWeatherMap APIs. Data is cached for 1 hour to optimize performance.")


    # --- Main Content Area: Display Weather Data or Welcome Message ---
    api_key = st.secrets.get("OPENWEATHER_API_KEY")
    # For local testing with .env, uncomment the next two lines:
    # if not api_key:
    #     api_key = os.getenv("OPENWEATHER_API_KEY")
            
    if not api_key:
        st.error("OpenWeatherMap API key missing! Please add it to Streamlit Secrets for deployment, or create a `.env` file for local testing.")
        # Display a friendly welcome message even if API key is missing
        st.info("Please enter your API key in Streamlit Secrets to unlock full functionality.")
    elif get_weather_button: # Only fetch and display data if button is clicked AND API key exists
        with st.status("Fetching premium weather data...", expanded=True) as status_box:
            weather_data = WeatherService.get_weather_data(city, api_key)
            if weather_data:
                status_box.update(label="Weather data fetched successfully!", state="complete", expanded=False)
                st.markdown("### Current City: " + city.title())
                WeatherUI.display_current_weather(weather_data)
                st.markdown("---")
                WeatherUI.display_forecast(weather_data)
                st.markdown("---")
                WeatherUI.display_air_quality(weather_data)
            else:
                status_box.update(label="Failed to fetch weather data.", state="error", expanded=True)
                # Error messages are handled inside WeatherService.get_weather_data,
                # so no need for an additional st.error here.
    else: # Initial state or after refresh without button click
        st.info("🌍 **Welcome to WeatherGenius Pro!** Enter a city name above and click 'Get Weather' to see real-time forecasts and air quality data for any location in the world.")
        st.image("https://placehold.co/800x400/ADD8E6/000000?text=Global+Weather+Map+Placeholder", use_column_width=True, caption="Explore weather worldwide!")


if __name__ == "__main__":
    main()
