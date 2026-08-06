import streamlit as st
import requests 
from dotenv import load_dotenv
import os
import datetime
import textwrap
from collections import Counter

load_dotenv()

# Set page configuration
st.set_page_config(page_title="Skylight Weather", page_icon="⛅", layout="centered")

API_KEY = os.getenv('API_KEY')

# Initialize session states
if 'search_query' not in st.session_state:
    st.session_state['search_query'] = 'New York'

# Mapping icon_code to FontAwesome icon classes
def get_weather_icon_html(icon_code):
    icon_map = {
        '01d': '<i class="fa-solid fa-sun fa-spin-slow" style="color: #f59e0b;"></i>',
        '01n': '<i class="fa-solid fa-moon" style="color: #d97706;"></i>',
        '02d': '<i class="fa-solid fa-cloud-sun" style="color: #f59e0b;"></i>',
        '02n': '<i class="fa-solid fa-cloud-moon" style="color: #7c3aed;"></i>',
        '03d': '<i class="fa-solid fa-cloud" style="color: #94a3b8;"></i>',
        '03n': '<i class="fa-solid fa-cloud" style="color: #64748b;"></i>',
        '04d': '<i class="fa-solid fa-cloud-meatball" style="color: #64748b;"></i>',
        '04n': '<i class="fa-solid fa-cloud-meatball" style="color: #64748b;"></i>',
        '09d': '<i class="fa-solid fa-cloud-showers-heavy" style="color: #3b82f6;"></i>',
        '09n': '<i class="fa-solid fa-cloud-showers-heavy" style="color: #2563eb;"></i>',
        '10d': '<i class="fa-solid fa-cloud-sun-rain" style="color: #3b82f6;"></i>',
        '10n': '<i class="fa-solid fa-cloud-moon-rain" style="color: #2563eb;"></i>',
        '11d': '<i class="fa-solid fa-cloud-bolt" style="color: #d97706;"></i>',
        '11n': '<i class="fa-solid fa-cloud-bolt" style="color: #d97706;"></i>',
        '13d': '<i class="fa-solid fa-snowflake" style="color: #06b6d4;"></i>',
        '13n': '<i class="fa-solid fa-snowflake" style="color: #06b6d4;"></i>',
        '50d': '<i class="fa-solid fa-smog" style="color: #94a3b8;"></i>',
        '50n': '<i class="fa-solid fa-smog" style="color: #94a3b8;"></i>'
    }
    return icon_map.get(icon_code, '<i class="fa-solid fa-cloud" style="color: #64748b;"></i>')

# Fetch APIs
def get_current_weather(city, units, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None

def get_forecast(city, units, api_key):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None

# Process 5-day forecast
def process_forecast(forecast_data):
    if not forecast_data or 'list' not in forecast_data:
        return []
    
    daily_groups = {}
    for item in forecast_data.get('list', []):
        dt = datetime.datetime.fromtimestamp(item['dt'])
        date_str = dt.strftime('%Y-%m-%d')
        
        if date_str not in daily_groups:
            daily_groups[date_str] = {
                'temps': [],
                'icons': [],
                'descriptions': [],
                'weekday': dt.strftime('%A'),
                'date_formatted': dt.strftime('%b %d')
            }
        
        daily_groups[date_str]['temps'].append(item['main']['temp'])
        daily_groups[date_str]['icons'].append(item['weather'][0]['icon'])
        daily_groups[date_str]['descriptions'].append(item['weather'][0]['main'])

    daily_forecasts = []
    # Sort dates to ensure chronological order
    for d_str in sorted(daily_groups.keys()):
        group = daily_groups[d_str]
        min_temp = min(group['temps'])
        max_temp = max(group['temps'])
        
        # Determine most common weather icon/description
        most_common_icon = Counter(group['icons']).most_common(1)[0][0]
        if most_common_icon.endswith('n'):
            most_common_icon = most_common_icon[:-1] + 'd'
            
        most_common_desc = Counter(group['descriptions']).most_common(1)[0][0]
        
        daily_forecasts.append({
            'date': d_str,
            'weekday': group['weekday'],
            'date_formatted': group['date_formatted'],
            'min_temp': min_temp,
            'max_temp': max_temp,
            'icon': most_common_icon,
            'desc': most_common_desc
        })
        
    return daily_forecasts[:5]

# Load FontAwesome Icons using st.markdown to bypass DOMPurify constraints
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">', unsafe_allow_html=True)

# Inject premium fonts and custom light theme CSS styles using st.html
st.html(textwrap.dedent("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    /* Global overrides */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 800px !important;
    }

    html, body, [class*="css"], .stText, .stMarkdown {
        font-family: 'Outfit', sans-serif !important;
    }

    /* Force pure white background for the application */
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
        background-image: none !important;
    }

    /* Beautiful Custom App Header in Dark Slate */
    .app-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .app-header h1 {
        font-weight: 700;
        font-size: 2.8rem;
        margin-bottom: 0.2rem;
        color: #0f172a;
    }
    @media (max-width: 480px) {
        .app-header h1 {
            font-size: 2.2rem !important;
        }
    }
    .app-header p {
        color: #475569;
        font-size: 1.05rem;
    }

    /* Premium Light Card Style */
    .weather-card {
        background: #ffffff;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        padding: 2.2rem;
        color: #1e293b;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .weather-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }

    /* Mini Cards for stats and forecasts in Light theme */
    .mini-card {
        background: #ffffff;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        padding: 1.1rem;
        text-align: center;
        color: #334155;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -2px rgba(0, 0, 0, 0.02);
        height: 100%;
    }
    .mini-card:hover {
        background: #f8fafc;
        border-color: #cbd5e1;
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }

    /* Metrics Grid styling */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.85rem;
        margin-top: 1.8rem;
    }
    @media (max-width: 600px) {
        .metrics-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    @media (max-width: 400px) {
        .metrics-grid {
            grid-template-columns: 1fr;
        }
    }
    .metric-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .metric-icon {
        font-size: 1.7rem;
        margin-bottom: 0.4rem;
    }
    .metric-val {
        font-weight: 700;
        font-size: 1.2rem;
        color: #0f172a;
    }
    .metric-lbl {
        font-size: 0.75rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.2rem;
    }

    /* Weather icon spin animation */
    @keyframes spin-slow {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .fa-spin-slow {
        animation: spin-slow 20s linear infinite;
        display: inline-block;
    }

    /* Streamlit Widget Custom Styling for Light Theme */
    div[data-testid="stTextInput"] input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15) !important;
    }
    div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border-radius: 12px !important;
        border: none !important;
    }

    /* Make toggle labels look dark and readable */
    .stToggle label p {
        color: #334155 !important;
        font-weight: 500 !important;
    }

    /* Style Search Button */
    div.stButton > button {
        background-color: #2563eb !important;
        color: white !important;
        border: 1px solid #2563eb !important;
        border-radius: 12px !important;
        padding: 0.4rem 1.2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
    }
    div.stButton > button:hover {
        background-color: #1d4ed8 !important;
        border-color: #1d4ed8 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }

    /* Streamlit Error Override */
    div[data-testid="stNotification"] {
        background-color: #fef2f2 !important;
        border: 1px solid #fca5a5 !important;
        border-radius: 12px !important;
        color: #991b1b !important;
    }

    /* Forecast layouts */
    .forecast-container {
        margin-top: 2rem;
    }
    .forecast-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 1rem;
    }
    .forecast-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 0.75rem;
    }
    .forecast-card {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        min-height: 170px;
        padding: 1rem 0.5rem;
    }
    .forecast-day-info {
        text-align: center;
    }
    .forecast-day {
        font-weight: 600;
        font-size: 1rem;
        color: #0f172a;
    }
    .forecast-date {
        font-size: 0.75rem;
        color: #64748b;
    }
    .forecast-icon {
        font-size: 1.8rem;
        margin: 0.4rem 0;
    }
    .forecast-temps {
        font-weight: 600;
        font-size: 1rem;
        color: #0f172a;
    }
    .min-t {
        font-weight: 400;
        color: #64748b;
    }
    .forecast-desc {
        font-size: 0.75rem;
        color: #475569;
        text-transform: capitalize;
        text-align: center;
        max-width: 90px;
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
    }
    
    /* Responsive media rules for forecast on mobile */
    @media (max-width: 640px) {
        .forecast-grid {
            grid-template-columns: 1fr !important;
            gap: 0.5rem !important;
        }
        .forecast-card {
            flex-direction: row !important;
            justify-content: space-between !important;
            align-items: center !important;
            min-height: auto !important;
            padding: 0.75rem 1.25rem !important;
        }
        .forecast-day-info {
            text-align: left !important;
            flex: 1.5;
        }
        .forecast-icon {
            margin: 0 !important;
            font-size: 1.5rem !important;
            flex: 1;
            text-align: center;
        }
        .forecast-temps {
            flex: 1.5;
            text-align: right;
        }
        .forecast-desc {
            flex: 1.5;
            text-align: right !important;
            max-width: none !important;
            margin-top: 0 !important;
        }
    }
    
    /* Align checkbox/toggle container vertically */
    .stToggle {
        margin-top: 0.5rem !important;
        display: flex !important;
        align-items: center !important;
    }
    .stToggle label p {
        font-size: 0.9rem !important;
        color: #334155 !important;
        font-weight: 500 !important;
        margin-left: 0.25rem !important;
    }
    </style>
"""))

# Main App Title Layout
st.html(textwrap.dedent("""
    <div class="app-header">
        <h1>⛅ Skylight Weather</h1>
        <p style="font-size: 1.05rem; opacity: 0.85;">Discover real-time forecasts & global atmospheric metrics</p>
    </div>
"""))

# Search input row (Input field & button next to each other)
col_search_field, col_search_btn = st.columns([4, 1])

with col_search_field:
    # Text input bound to the st.session_state key
    city_val = st.text_input(
        "Search City",
        value=st.session_state['search_query'],
        key='city_input_widget',
        label_visibility="collapsed",
        placeholder="Enter City Name... (e.g. Tokyo)"
    )

with col_search_btn:
    search_btn = st.button("🔍 Search", use_container_width=True)

# Settings row below the search bar
col_toggle, col_empty = st.columns([1, 2])
with col_toggle:
    fahrenheit = st.toggle("°F Mode", value=False)
    units = 'imperial' if fahrenheit else 'metric'
    temp_unit = "°F" if fahrenheit else "°C"
    speed_unit = "mph" if fahrenheit else "m/s"

# Handle City Change & Button clicks
if search_btn:
    st.session_state['search_query'] = st.session_state['city_input_widget'].strip()
elif st.session_state['city_input_widget'] != st.session_state['search_query']:
    st.session_state['search_query'] = st.session_state['city_input_widget'].strip()

st.html("<div style='margin-bottom: 1.5rem;'></div>")

# Fetch data if a query is active
active_city = st.session_state['search_query'].strip()

if active_city:
    weather_data = get_current_weather(active_city, units, API_KEY)
    forecast_data = get_forecast(active_city, units, API_KEY)
    
    if weather_data and forecast_data:
        formatted_name = f"{weather_data['name']}, {weather_data['sys']['country']}"
        city_display_name = weather_data['name']
        icon_code = weather_data['weather'][0]['icon']
        
        # Parse Dates using timezone offset
        timezone_offset = weather_data.get('timezone', 0)
        dt_utc = weather_data.get('dt', 0)
        local_dt = datetime.datetime.fromtimestamp(dt_utc + timezone_offset, tz=datetime.timezone.utc)
        weekday = local_dt.strftime('%A')
        date_formatted = local_dt.strftime('%B %d, %Y')
        
        # Sunrise and sunset local times
        sunrise_utc = weather_data['sys']['sunrise']
        sunset_utc = weather_data['sys']['sunset']
        sunrise_local = datetime.datetime.fromtimestamp(sunrise_utc + timezone_offset, tz=datetime.timezone.utc)
        sunset_local = datetime.datetime.fromtimestamp(sunset_utc + timezone_offset, tz=datetime.timezone.utc)
        
        sunrise_time = sunrise_local.strftime('%I:%M %p')
        sunset_time = sunset_local.strftime('%I:%M %p')
        
        # Extract metrics
        temperature = round(weather_data['main']['temp'])
        feels_like = round(weather_data['main']['feels_like'])
        humidity = weather_data['main']['humidity']
        wind_speed = round(weather_data['wind']['speed'], 1)
        weather_desc = weather_data['weather'][0]['description']
        clouds = weather_data['clouds']['all']
        pressure = weather_data['main']['pressure']
        
        # Visibility conversion
        visibility_m = weather_data.get('visibility', 10000)
        if fahrenheit:
            visibility_display = f"{round((visibility_m / 1000.0) * 0.621371, 1)} mi"
        else:
            visibility_display = f"{round(visibility_m / 1000.0, 1)} km"
            
        weather_icon_lg = get_weather_icon_html(icon_code)
        
        # Render Premium Light Weather Card
        st.html(textwrap.dedent(f"""
            <div class="weather-card">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                    <div>
                        <h2 style="margin: 0; font-size: 2.2rem; font-weight: 700; color: #0f172a;">{formatted_name}</h2>
                        <div style="font-size: 1.05rem; color: #475569; margin-top: 0.3rem;">{weekday}, {date_formatted}</div>
                        <div style="margin-top: 1rem; font-size: 1.25rem; font-weight: 600; text-transform: capitalize; color: #0f172a; display: flex; align-items: center; gap: 0.5rem;">
                             {weather_desc}
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div style="font-size: 3.5rem; line-height: 1;">{weather_icon_lg}</div>
                        <div style="font-size: 4rem; font-weight: 700; line-height: 1; color: #0f172a;">{temperature}{temp_unit}</div>
                    </div>
                </div>
                
                <div class="metrics-grid">
                    <div class="mini-card">
                        <div class="metric-item">
                            <span class="metric-icon" style="color: #ef4444;"><i class="fa-solid fa-temperature-half"></i></span>
                            <span class="metric-val">{feels_like}{temp_unit}</span>
                            <span class="metric-lbl">Feels Like</span>
                        </div>
                    </div>
                    <div class="mini-card">
                        <div class="metric-item">
                            <span class="metric-icon" style="color: #3b82f6;"><i class="fa-solid fa-droplet"></i></span>
                            <span class="metric-val">{humidity}%</span>
                            <span class="metric-lbl">Humidity</span>
                        </div>
                    </div>
                    <div class="mini-card">
                        <div class="metric-item">
                            <span class="metric-icon" style="color: #10b981;"><i class="fa-solid fa-wind"></i></span>
                            <span class="metric-val">{wind_speed} {speed_unit}</span>
                            <span class="metric-lbl">Wind Speed</span>
                        </div>
                    </div>
                    <div class="mini-card">
                        <div class="metric-item">
                            <span class="metric-icon" style="color: #f59e0b;"><i class="fa-solid fa-cloud"></i></span>
                            <span class="metric-val">{clouds}%</span>
                            <span class="metric-lbl">Clouds</span>
                        </div>
                    </div>
                    <div class="mini-card">
                        <div class="metric-item">
                            <span class="metric-icon" style="color: #8b5cf6;"><i class="fa-solid fa-gauge-high"></i></span>
                            <span class="metric-val">{pressure} hPa</span>
                            <span class="metric-lbl">Pressure</span>
                        </div>
                    </div>
                    <div class="mini-card">
                        <div class="metric-item">
                            <span class="metric-icon" style="color: #ec4899;"><i class="fa-solid fa-eye"></i></span>
                            <span class="metric-val">{visibility_display}</span>
                            <span class="metric-lbl">Visibility</span>
                        </div>
                    </div>
                </div>
                
                <div style="display: flex; justify-content: space-around; margin-top: 1.5rem; border-top: 1px solid #e2e8f0; padding-top: 1.25rem; font-size: 0.95rem; color: #475569;">
                    <div style="display: flex; align-items: center; gap: 0.4rem;">
                        <i class="fa-solid fa-circle-up" style="color: #f59e0b;"></i> 
                        <span>Sunrise: <strong>{sunrise_time}</strong></span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.4rem;">
                        <i class="fa-solid fa-circle-down" style="color: #ef4444;"></i> 
                        <span>Sunset: <strong>{sunset_time}</strong></span>
                    </div>
                </div>
            </div>
        """))
        
        # 5-Day Forecast
        forecast_list = process_forecast(forecast_data)
        if forecast_list:
            cards_html = ""
            for day in forecast_list:
                day_icon_html = get_weather_icon_html(day['icon'])
                min_t = round(day['min_temp'])
                max_t = round(day['max_temp'])
                cards_html += f"""
                <div class="mini-card forecast-card">
                    <div class="forecast-day-info">
                        <div class="forecast-day">{day['weekday']}</div>
                        <div class="forecast-date">{day['date_formatted']}</div>
                    </div>
                    <div class="forecast-icon">{day_icon_html}</div>
                    <div class="forecast-temps">{max_t}° / <span class="min-t">{min_t}°</span></div>
                    <div class="forecast-desc">{day['desc']}</div>
                </div>
                """
            
            st.html(textwrap.dedent(f"""
                <div class="forecast-container">
                    <div class="forecast-title"><i class="fa-solid fa-calendar-days" style="margin-right: 0.4rem;"></i> 5-Day Forecast</div>
                    <div class="forecast-grid">
                        {cards_html}
                    </div>
                </div>
            """))
            
    else:
        st.error("⚠️ City Not Found. Please check the spelling and try again.")
