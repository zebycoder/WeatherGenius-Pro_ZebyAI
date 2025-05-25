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
            display: none; /* Hide Streamlit's default header */
        }
        .stApp > header .st-emotion-cache-1gh2thc {
            padding-top: 0;
        }

        /* Custom Header for App Title */
        .app-header {
            text-align: center;
            padding: 2rem 0 0.5rem; /* Reduced bottom padding */
            background: linear-gradient(to right, #6a11cb, #2575fc); /* Purple to blue gradient */
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3.8rem; /* Slightly larger */
            font-weight: bold;
            margin-bottom: 0.2rem;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.15); /* Stronger shadow */
        }
        .app-tagline {
            text-align: center;
            font-size: 1.4rem; /* Slightly larger */
            color: #4a4a4a;
            margin-bottom: 2.5rem; /* More space */
            max-width: 850px; /* Wider tagline */
            margin-left: auto;
            margin-right: auto;
            line-height: 1.5;
        }
        .welcome-section {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            padding: 3rem 2rem; /* Larger padding */
            box-shadow: 0 15px 50px rgba(31, 38, 135, 0.1);
            margin-top: 2rem;
            text-align: center;
        }
        .welcome-section h3 {
            color: #6a11cb;
            font-size: 2rem;
            margin-bottom: 1.5rem;
        }
        .welcome-section p {
            font-size: 1.15rem;
            line-height: 1.8;
            color: #555;
            max-width: 700px;
            margin: 0 auto;
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
            border-radius: 12px; /* More rounded buttons */
            font-weight: bold;
            padding: 1.2rem 2.5rem; /* Larger padding */
            transition: all 0.4s ease;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            font-size: 1.1rem;
        }
        .stButton>button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(37, 117, 252, 0.5); /* Stronger shadow on hover */
            filter: brightness(1.1);
        }

        /* Input Field Styling */
        .stTextInput > div > div > input {
            border-radius: 12px; /* Rounded input */
            border: 1px solid #a0c4ff;
            padding: 1rem 1.2rem; /* Larger padding */
            box-shadow: inset 0 1px 5px rgba(0,0,0,0.08);
            transition: border-color 0.3s, box-shadow 0.3s;
            font-size: 1.1rem;
        }
        .stTextInput > div > div > input:focus {
            border-color: #2575fc;
            box-shadow: 0 0 0 0.3rem rgba(37, 117, 252, 0.3); /* Larger focus glow */
        }
        .stTextInput label {
            font-size: 1.1em;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #333;
        }


        /* Metric Styling */
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.8);
            border-radius: 15px;
            padding: 1.5rem 2rem; /* Larger padding */
            box-shadow: 0 4px 20px rgba(0,0,0,0.07); /* Stronger shadow */
            border: 1px solid rgba(255, 255, 255, 0.5);
            text-align: center; /* Center align metrics */
        }
        [data-testid="stMetric"] label {
            font-size: 1.2em;
            color: #555;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        [data-testid="stMetric"] .st-emotion-cache-1wivf6q { /* Value */
            font-size: 2.8em; /* Larger value */
            font-weight: bold;
            color: #2575fc;
            margin-top: 0.2rem;
        }
        [data-testid="stMetric"] .st-emotion-cache-121p57u { /* Delta */
            color: #666;
            font-size: 1em; /* Larger delta */
        }

        /* Responsive Grid for Weather Details */
        .weather-details-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); /* Larger min width */
            gap: 1.8rem; /* Larger gap */
            margin-top: 2.5rem;
        }

        /* Forecast Cards */
        .forecast-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 18px; /* More rounded */
            padding: 1.8rem; /* Larger padding */
            box-shadow: 0 8px 25px rgba(0,0,0,0.1); /* Stronger shadow */
            text-align: center;
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            border: 1px solid rgba(255, 255, 255, 0.6);
        }
        .forecast-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.15);
        }
        .forecast-card h4 {
            color: #6a11cb;
            margin-bottom: 0.6rem;
            font-size: 1.3rem;
        }
        .forecast-card p {
            margin: 0.3rem 0;
            font-size: 1rem;
            color: #444;
        }
        .forecast-card img {
            margin-bottom: 0.6rem;
            width: 70px; /* Slightly larger icons */
            height: 70px;
        }

        /* Sidebar Styling */
        .st-emotion-cache-1l02z8d { /* Sidebar background */
            background: linear-gradient(180deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            padding: 2.5rem 1.5rem; /* More padding */
            border-radius: 0 20px 20px 0; /* Rounded right edge */
        }
        .st-emotion-cache-1l02z8d h1, .st-emotion-cache-1l02z8d h2, .st-emotion-cache-1l02z8d h3, .st-emotion-cache-1l02z8d h4, .st-emotion-cache-1l02z8d p, .st-emotion-cache-1l02z8d a, .st-emotion-cache-1l02z8d span {
            color: white !important;
        }
        .sidebar-info {
            text-align: center;
            margin-top: 1.5rem;
        }
        .sidebar-info p {
            font-size: 1rem;
            margin-bottom: 0.6rem;
            line-height: 1.4;
        }
        .sidebar-info strong {
            color: #e0f2f7;
            font-weight: 700;
            font-size: 1.1rem;
        }
        .sidebar-info a {
            color: #e0f2f7 !important;
            text-decoration: none;
        }
        .sidebar-info a:hover {
            text-decoration: underline;
        }
        .sidebar-info .contact-icon {
            margin-right: 8px;
            vertical-align: middle;
        }
        .sidebar-brand {
            font-size: 1.8rem;
            font-weight: bold;
            margin-bottom: 1.5rem;
            text-shadow: 1px 1px 5px rgba(0,0,0,0.2);
        }

        /* Plotly Chart Styling */
        .stPlotlyChart {
            border-radius: 15px;
            overflow: hidden; /* Ensures borders are respected */
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            margin-top: 1.5rem;
            background: rgba(255,255,255,0.9);
        }

        /* Footer */
        .app-footer {
            text-align: center;
            padding: 2rem 0 1rem;
            color: #666;
            font-size: 0.9rem;
            margin-top: 3rem;
            border-top: 1px solid #ccc;
        }
        .app-footer a {
            color: #2575fc;
            text-decoration: none;
            font-weight: bold;
        }
        .app-footer a:hover {
            text-decoration: underline;
        }

        /* Mobile Responsiveness */
        @media (max-width: 768px) {
            .app-header {
                font-size: 2.8rem;
                padding: 1.5rem 0 0.5rem;
            }
            .app-tagline {
                font-size: 1.1rem;
                margin-bottom: 1.5rem;
            }
            .welcome-section {
                padding: 2rem 1rem;
            }
            .welcome-section h3 {
                font-size: 1.6rem;
            }
            .welcome-section p {
                font-size: 1rem;
            }
            .weather-card {
                padding: 1.5rem;
                margin-bottom: 1.5rem;
            }
            .stButton>button {
                padding: 0.9rem 1.5rem;
                font-size: 1rem;
            }
            .stTextInput > div > div > input {
                padding: 0.8rem 1rem;
                font-size: 1rem;
            }
            [data-testid="stMetric"] {
                padding: 1rem;
            }
            [data-testid="stMetric"] .st-emotion-cache-1wivf6q {
                font-size: 2.2em;
            }
            .weather-details-grid {
                grid-template-columns: 1fr; /* Stack on small screens */
                gap: 1.2rem;
            }
            .forecast-card {
                padding: 1.2rem;
            }
            .forecast-card h4 {
                font-size: 1.1rem;
            }
            .forecast-card p {
                font-size: 0.9rem;
            }
            .sidebar-info {
                padding: 1rem 0;
            }
            .sidebar-info p {
                font-size: 0.85rem;
            }
            .sidebar-brand {
                font-size: 1.5rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# ==================== WEATHER API SERVICE ====================
class WeatherService:
    @staticmethod
    @st.cache_data(ttl=3600) # Cache data for 1 hour to optimize API calls
    def get_weather_data(city: str, api_key: str) -> dict:
        """Enterprise-grade weather data fetcher with full error handling"""
        try:
            # Current Weather
            current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            current_response = requests.get(current_url, timeout=10)
            current_response.raise_for_status() # Raise an exception for HTTP errors
            current = current_response.json()
            
            if current.get('cod') == '404':
                raise ValueError(f"City '{city}' not found. Please check the spelling.")
            elif current.get('cod') == '401':
                raise ValueError("Invalid OpenWeatherMap API key. Please check your Streamlit Secrets.")

            # 5-Day Forecast (3-hour step, ~40 items for 5 days)
            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
            forecast_response = requests.get(forecast_url, timeout=10)
            forecast_response.raise_for_status()
            forecast = forecast_response.json()

            # Air Quality Data
            lat, lon = current["coord"]["lat"], current["coord"]["lon"]
            aqi_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
            aqi_response = requests.get(aqi_url, timeout=10)
            aqi_response.raise_for_status()
            aqi = aqi_response.json()

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
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                st.error(f"City '{city}' not found. Please check the spelling.")
            elif e.response.status_code == 401:
                st.error("Invalid OpenWeatherMap API key. Please check your Streamlit Secrets.")
            else:
                st.error(f"OpenWeatherMap API Error: {e.response.status_code} - {e.response.reason}")
            return None
        except ValueError as e: # Custom value errors
            st.error(f"Data Error: {str(e)}")
            return None
        except Exception as e:
            st.error(f"An unexpected error occurred during data fetching: {str(e)}")
            return None

# ==================== UI COMPONENTS ====================
class WeatherUI:
    @staticmethod
    def display_current_weather(data: dict):
        """Premium current weather display with all metrics"""
        current = data["current"]
        weather = current["weather"][0]
        
        # Default to Asia/Karachi for time display
        timezone = pytz.timezone("Asia/Karachi") # Default to Pakistan time

        st.markdown(f"""
        <div class="weather-card">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; margin-bottom: 1.5rem;">
                <div>
                    <h1 style="margin-bottom: 0.2rem; font-size: 2.8rem; color: #333;">{current['name']}, {current['sys']['country']}</h1>
                    <h3 style="margin-top: 0; color: #555; font-weight: normal; font-size: 1.5rem;">
                        {weather['main']} ({weather['description'].title()})
                    </h3>
                </div>
                <img src="https://openweathermap.org/img/wn/{weather['icon']}@4x.png" width="120" alt="{weather['description']}" style="vertical-align: middle;">
            </div>
            
            <div style="text-align: center; margin: 2rem 0;">
                <p style="font-size: 5rem; font-weight: bold; color: #2575fc; margin: 0; line-height: 1;">{current['main']['temp']:.1f}°C</p>
                <p style="font-size: 1.5rem; color: #666; margin-top: 0.5rem;">Feels like: {current['main']['feels_like']:.1f}°C</p>
            </div>

            <div class="weather-details-grid">
                <div data-testid="stMetric">
                    <label>💧 Humidity</label>
                    <div class="st-emotion-cache-1wivf6q">{current['main']['humidity']}%</div>
                </div>
                <div data-testid="stMetric">
                    <label>🌬️ Wind Speed</label>
                    <div class="st-emotion-cache-1wivf6q">{current['wind']['speed']:.1f} m/s</div>
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
                    <div class="st-emotion-cache-1wivf6q">N/A</div> <div class="st-emotion-cache-121p57u">(Data not available in this API)</div>
                </div>
            </div>
            
            <div style="display: flex; justify-content: space-around; margin-top: 2.5rem; flex-wrap: wrap; text-align: center;">
                <div style="margin: 0.5rem 1rem; flex-basis: 45%;">
                    <h4>🌅 Sunrise</h4>
                    <p style="font-size: 1.1rem;">{datetime.fromtimestamp(current["sys"]["sunrise"], timezone).strftime("%I:%M %p")}</p>
                </div>
                <div style="margin: 0.5rem 1rem; flex-basis: 45%;">
                    <h4>🌇 Sunset</h4>
                    <p style="font-size: 1.1rem;">{datetime.fromtimestamp(current["sys"]["sunset"], timezone).strftime("%I:%M %p")}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Display map of the city - simple Streamlit map
        st.subheader("📍 Location on Map")
        st.map(pd.DataFrame([[current["coord"]["lat"], current["coord"]["lon"]]], columns=['lat', 'lon']), zoom=10)
        st.markdown("---")

    @staticmethod
    def display_forecast(data: dict):
        """Interactive 5-day forecast with Plotly visualization and daily cards"""
        forecast_items = []
        for item in data["forecast"]["list"]:
            forecast_items.append({
                "dt": item["dt"], # Keep original timestamp for Plotly
                "datetime": datetime.fromtimestamp(item["dt"]),
                "date": datetime.fromtimestamp(item["dt"]).strftime("%A, %b %d"),
                "time": datetime.fromtimestamp(item["dt"]).strftime("%I:%M %p"),
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

        st.markdown(f"""
        <div class="weather-card">
            <h2>📅 5-Day Forecast for {data['current']['name']}</h2>
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
            
            # Convert 'datetime' column (which is date object after groupby) back to datetime object for formatting
            daily_summary['Date'] = daily_summary['datetime'].apply(lambda x: x.strftime("%A, %b %d"))

            # Display daily cards in a responsive grid
            daily_cols = st.columns(len(daily_summary))
            for i, row in daily_summary.iterrows():
                with daily_cols[i]:
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
            st.markdown("### Detailed Hourly Forecast")
            # Select relevant columns for display
            display_df = df_forecast[['date', 'time', 'temp', 'feels_like', 'description', 'humidity', 'wind_speed', 'pressure']].copy()
            # Rename columns for better readability
            display_df.columns = ["Date", "Time", "Temperature (°C)", "Feels Like (°C)", "Conditions", "Humidity (%)", "Wind Speed (m/s)", "Pressure (hPa)"]
            
            st.dataframe(
                display_df,
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
                dtick="D1", # Show daily ticks
                tickformat="%b %d\n%A", # Format as Month Day, Day of Week
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
                        <div class="st-emotion-cache-1wivf6q">{components.get('co', 'N/A'):.2f}</div>
                        <div class="st-emotion-cache-121p57u">μg/m³</div>
                    </div>
                    <div data-testid="stMetric">
                        <label>NO</label>
                        <div class="st-emotion-cache-1wivf6q">{components.get('no', 'N/A'):.2f}</div>
                        <div class="st-emotion-cache-121p57u">μg/m³</div>
                    </div>
                    <div data-testid="stMetric">
                        <label>NO2</label>
                        <div class="st-emotion-cache-1wivf6q">{components.get('no2', 'N/A'):.2f}</div>
                        <div class="st-emotion-cache-121p57u">μg/m³</div>
                    </div>
                    <div data-testid="stMetric">
                        <label>O3</label>
                        <div class="st-emotion-cache-1wivf6q">{components.get('o3', 'N/A'):.2f}</div>
                        <div class="st-emotion-cache-121p57u">μg/m³</div>
                    </div>
                    <div data-testid="stMetric">
                        <label>SO2</label>
                        <div class="st-emotion-cache-1wivf6q">{components.get('so2', 'N/A'):.2f}</div>
                        <div class="st-emotion-cache-121p57u">μg/m³</div>
                    </div>
                    <div data-testid="stMetric">
                        <label>PM2.5</label>
                        <div class="st-emotion-cache-1wivf6q">{components.get('pm2_5', 'N/A'):.2f}</div>
                        <div class="st-emotion-cache-121p57u">μg/m³</div>
                    </div>
                    <div data-testid="stMetric">
                        <label>PM10</label>
                        <div class="st-emotion-cache-1wivf6q">{components.get('pm10', 'N/A'):.2f}</div>
                        <div class="st-emotion-cache-121p57u">μg/m³</div>
                    </div>
                    <div data-testid="stMetric">
                        <label>NH3</label>
                        <div class="st-emotion-cache-1wivf6q">{components.get('nh3', 'N/A'):.2f}</div>
                        <div class="st-emotion-cache-121p57u">μg/m³</div>
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
    st.markdown('<p class="app-tagline">Your ultimate AI-powered companion for precise global weather forecasting and air quality analysis. Designed for accuracy, speed, and a delightful user experience.</p>', unsafe_allow_html=True)

    # City input and button moved to main content area for prominence
    col_city_input, col_button_go = st.columns([3, 1])
    with col_city_input:
        city = st.text_input("Enter City Name (e.g., London, Tokyo, Lahore)", "Lahore", key="main_city_input", help="Type any city name from around the world to get instant weather updates.")
    with col_button_go:
        st.markdown("<br>", unsafe_allow_html=True) # Align button with text input
        get_weather_button = st.button("Get Weather", type="primary", use_container_width=True)

    st.markdown("---") # Visual separator

    # --- Sidebar: Developer Info ---
    with st.sidebar:
        st.markdown("""<div class="sidebar-brand">ZebyCoder Solutions</div>""", unsafe_allow_html=True)
        st.markdown("""
        <div class="sidebar-info">
            <p><strong>Developed by:</strong> Jahanzaib Javed</p>
            <p><strong>Specialization:</strong> AI/ML & Full-Stack Development</p>
            <p><span class="contact-icon">📞</span> +92-300-5590321</p>
            <p><span class="contact-icon">✉</span> <a href="mailto:zeb.innerartinteriors@gmail.com">zeb.innerartinteriors@gmail.com</a></p>
            <p><span class="contact-icon">📍</span> Lahore, Pakistan</p>
            <p style="font-size: 0.8rem; color: #e0f2f7; margin-top: 1.5rem; line-height: 1.3;">
                <br>
                WeatherGenius Pro is a testament to cutting-edge AI/ML integration for real-time data processing and intuitive user interfaces.
                <br><br>
                For custom AI/ML development, web applications, or scalable software solutions, feel free to reach out!
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.info("💡 **Tip:** This app fetches real-time data from OpenWeatherMap APIs. Data is cached for 1 hour to optimize performance and reduce API calls.")


    # --- Main Content Area: Display Weather Data or Welcome Message ---
    api_key = st.secrets.get("OPENWEATHER_API_KEY")
    # For local testing with .env, uncomment the next two lines:
    # if not api_key:
    #     api_key = os.getenv("OPENWEATHER_API_KEY")
            
    if not api_key:
        st.error("OpenWeatherMap API key missing! Please add it to Streamlit Secrets for deployment, or create a `.env` file for local testing.")
        # Display a friendly welcome message even if API key is missing
        st.markdown("""
        <div class="welcome-section">
            <h3>🌍 Welcome to WeatherGenius Pro!</h3>
            <p>This application provides precise global weather forecasting and air quality analysis using real-time data from OpenWeatherMap.</p>
            <p>To get started, simply enter a city name in the input field above and click 'Get Weather'.</p>
            <p><strong>Please note:</strong> The OpenWeatherMap API key is required for data fetching. Ensure it's correctly configured in your Streamlit Secrets.</p>
        </div>
        """, unsafe_allow_html=True)
    elif get_weather_button: # Only fetch and display data if button is clicked AND API key exists
        with st.status("Fetching premium weather data...", expanded=False) as status_box: # Default to not expanded
            weather_data = WeatherService.get_weather_data(city, api_key)
            if weather_data:
                status_box.update(label="Weather data fetched successfully!", state="complete", expanded=False)
                # The main weather details are now displayed directly below the input
                # No need for a hidden expander, as per user's request.
                st.markdown(f"## Weather for {city.title()}") # Prominent city name heading
                WeatherUI.display_current_weather(weather_data)
                st.markdown("---") # Separator after current weather
                WeatherUI.display_forecast(weather_data)
                st.markdown("---") # Separator after forecast
                WeatherUI.display_air_quality(weather_data)
            else:
                status_box.update(label="Failed to fetch weather data. Please check error messages above.", state="error", expanded=True)
                # Error messages are handled inside WeatherService.get_weather_data,
                # so no need for an additional st.error here.
    else: # Initial state or after refresh without button click
        st.markdown("""
        <div class="welcome-section">
            <h3>🌍 Welcome to WeatherGenius Pro!</h3>
            <p>Discover real-time weather conditions, 5-day forecasts, and detailed air quality information for **any city in the world**.</p>
            <p>Our intuitive interface provides comprehensive insights at a glance, making weather analysis effortless and enjoyable.</p>
            <p>Simply enter a city name in the search bar above and click 'Get Weather' to explore!</p>
            <br>
            <p><strong>Key Features:</strong></p>
            <ul>
                <li>⚡ Instant Current Weather Updates</li>
                <li>🗓️ Detailed 5-Day Hourly & Daily Forecasts</li>
                <li>📊 Interactive Temperature & Humidity Charts</li>
                <li>🌬️ Comprehensive Air Quality Index (AQI)</li>
                <li>📍 Map Visualization of Searched City</li>
                <li>📱 Fully Responsive Design (Desktop & Mobile)</li>
                <li>🚀 Blazing Fast Performance with Data Caching</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        # Placeholder for a world map/globe.
        # Streamlit's st.map is for displaying data points, not for interactive city selection.
        # A full interactive globe for city selection is beyond st.map's current capabilities
        # and would require complex integration with other JS libraries.
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.subheader("Explore Global Weather")
        st.image("https://placehold.co/1000x500/A0D1F8/000000?text=Interactive+World+Map+Coming+Soon+%F0%9F%8C%8D", use_column_width=True, caption="Pinpoint any location on the globe!")


    # --- Footer ---
    st.markdown("---")
    st.markdown("""
    <div class="app-footer">
        <p>&copy; 2024 WeatherGenius Pro. Developed with passion by <a href="mailto:zeb.innerartinteriors@gmail.com">Jahanzaib Javed (ZebyCoder)</a>. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
