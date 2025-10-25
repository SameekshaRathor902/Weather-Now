import streamlit as st
import requests
from datetime import datetime
import base64
import os

# ====================================================================
# CONFIGURATION AND TRANSLATIONS
# ====================================================================

# 🔑 API KEYS - Load securely using st.secrets or environment variables
# NOTE: You MUST create a .streamlit/secrets.toml file or set environment variables 
#       for 'WEATHERAPI_KEY' and 'UNSPLASH_ACCESS_KEY'.
try:
    WEATHERAPI_KEY = st.secrets["WEATHERAPI_KEY"]
except KeyError:
    WEATHERAPI_KEY = os.environ.get("WEATHERAPI_KEY")

try:
    UNSPLASH_ACCESS_KEY = st.secrets["UNSPLASH_ACCESS_KEY"]
except KeyError:
    UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")


WEATHERAPI_CURRENT_URL = "http://api.weatherapi.com/v1/current.json"
WEATHERAPI_FORECAST_URL = "http://api.weatherapi.com/v1/forecast.json"
UNSPLASH_API_URL = "https://api.unsplash.com/search/photos"

# --- Dynamic Background Image URLs ---
BACKGROUND_IMAGES = {
    "clear": "https://images.pexels.com/photos/281260/pexels-photo-281260.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=2000",
    "clouds": "https://images.pexels.com/photos/531767/pexels-photo-531767.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=2000",
    "rain": "https://images.unsplash.com/photo-1610741083757-1ae88e1a17f7?q=80&w=2000&auto=format&fit=crop",
    "drizzle": "https://images.unsplash.com/photo-1610741083757-1ae88e1a17f7?q=80&w=2000&auto=format&fit=crop",
    "thunderstorm": "https://images.pexels.com/photos/1118873/pexels-photo-1118873.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=2000",
    "snow": "https://images.pexels.com/photos/1144211/pexels-photo-1144211.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=2000",
    "mist": "https://images.unsplash.com/photo-1544321045-8664165d5686?q=80&w=2000&auto=format&fit=crop",
    "haze": "https://images.unsplash.com/photo-1544321045-8664165d5686?q=80&w=2000&auto=format&fit=crop",
    "fog": "https://images.unsplash.com/photo-1544321045-8664165d5686?q=80&w=2000&auto=format&fit=crop",
    "default": "https://images.pexels.com/photos/531767/pexels-photo-531767.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=2000"
}

# --- TRANSLATIONS DICTIONARY ---
TRANSLATIONS = {
    "english": {
        "title": "Weather Now - Smart Forecasting",
        "tagline": "Get real-time weather and a **3-day outlook** for any city on the globe.",
        "input_label": "📍 Enter City Name (e.g., Dehradun, Delhi, London)",
        "input_placeholder": "Enter City Name and press Enter",
        "press_enter": "Press Enter to search for the city's weather!",
        "welcome": "Welcome! Start by entering a city name above.",
        "welcome_detail": "Enter a city to see its aesthetic weather forecast and a glimpse of its famous landmark.",
        "weather": "Weather",
        "landmark_unavailable": "Landmark image not available.",
        "feels_like": "Feels Like",
        "humidity": "Humidity",
        "wind_speed": "Wind Speed",
        "pressure": "Pressure",
        "severe_alert": "🚨 Severe Weather Alert! Take precautions.",
        "forecast_header": "📅 3-Day Forecast",
        "forecast_error": "Error: Could not fetch 3-day forecast. Check API configuration or city name.",
        "city_not_found": "City '{}' not found! Please try again.",
        "error_fetching": "Error fetching weather data: {}",
        "theme_selector": "Interface Theme",
        "language_selector": "Select Language",
        "light_mode": "🌞 Light Mode",
        "dark_mode": "🌙 Dark Mode",
        "max_temp": "Max Temp",
        "min_temp": "Min Temp",
    },
    "hindi": {
        "title": "मौसम अब - स्मार्ट पूर्वानुमान",
        "tagline": "दुनिया के किसी भी शहर के लिए वास्तविक समय का मौसम और **3-दिन का पूर्वानुमान** प्राप्त करें।",
        "input_label": "📍 शहर का नाम दर्ज करें (उदाहरण: देहरादून, दिल्ली, लंदन)",
        "input_placeholder": "शहर का नाम दर्ज करें और Enter दबाएँ",
        "press_enter": "शहर के मौसम की खोज के लिए Enter दबाएँ!",
        "welcome": "स्वागत है! ऊपर शहर का नाम दर्ज करके शुरुआत करें।",
        "welcome_detail": "इसके सौंदर्यपूर्ण मौसम पूर्वानुमान और प्रसिद्ध स्थल की झलक देखने के लिए एक शहर दर्ज करें।",
        "weather": "मौसम",
        "landmark_unavailable": "पहचान चिह्न की तस्वीर उपलब्ध नहीं है।",
        "feels_like": "महसूस होता है",
        "humidity": "आर्द्रता",
        "wind_speed": "हवा की गति",
        "pressure": "दबाव",
        "severe_alert": "🚨 गंभीर मौसम चेतावनी! सावधानी बरतें।",
        "forecast_header": "📅 3-दिन का पूर्वानुमान",
        "forecast_error": "त्रुटि: 3-दिन का पूर्वानुमान प्राप्त नहीं किया जा सका। एपीआई कॉन्फ़िगरेशन या शहर का नाम जाँच करें।",
        "city_not_found": "शहर '{}' नहीं मिला! कृपया पुनः प्रयास करें।",
        "error_fetching": "मौसम डेटा प्राप्त करने में त्रुटि: {}",
        "theme_selector": "इंटरफ़ेस थीम",
        "language_selector": "भाषा चुनें",
        "light_mode": "🌞 हल्का मोड",
        "dark_mode": "🌙 गहरा मोड",
        "max_temp": "अधिकतम तापमान",
        "min_temp": "न्यूनतम तापमान",
    }
}

# ---- INITIAL STATE SETUP ----
if 'theme' not in st.session_state:
    st.session_state['theme'] = 'light'
if 'language' not in st.session_state:
    st.session_state['language'] = 'english'
if 'search_triggered' not in st.session_state:
    st.session_state['search_triggered'] = False
if 'background_url' not in st.session_state:
    st.session_state['background_url'] = None
if 'current_weather_data' not in st.session_state:
    st.session_state['current_weather_data'] = None
if 'city_image_url' not in st.session_state:
    st.session_state['city_image_url'] = None


# --- UTILITY FUNCTIONS ---

def get_base64_image(image_path):
    """Encodes a local image file into a Base64 string for CSS background injection."""
    try:
        if not os.path.exists(image_path):
            return None
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return None

def get_weather_background_url(condition_text):
    """Maps WeatherAPI condition text to a background image URL by checking keywords."""
    condition_text = condition_text.lower()
    
    if "clear" in condition_text or "sunny" in condition_text:
        return BACKGROUND_IMAGES.get("clear")
    elif "cloud" in condition_text or "overcast" in condition_text:
        return BACKGROUND_IMAGES.get("clouds")
    elif "rain" in condition_text or "shower" in condition_text:
        return BACKGROUND_IMAGES.get("rain")
    elif "drizzle" in condition_text:
        return BACKGROUND_IMAGES.get("drizzle")
    elif "thunder" in condition_text or "storm" in condition_text:
        return BACKGROUND_IMAGES.get("thunderstorm")
    elif "snow" in condition_text or "sleet" in condition_text or "ice" in condition_text:
        return BACKGROUND_IMAGES.get("snow")
    elif "mist" in condition_text or "fog" in condition_text or "haze" in condition_text:
        return BACKGROUND_IMAGES.get("mist")
    
    return BACKGROUND_IMAGES.get("default") # Default fallback

# --- ADDED ST.CACHE_DATA FOR PERFORMANCE ---
@st.cache_data(ttl=3600)
def fetch_unsplash_image_url(city_name):
    """Fetches a city landmark image from Unsplash or uses a fallback."""
    KNOWN_CITIES = {
        "amritsar": "https://images.pexels.com/photos/17798305/pexels-photo-17798305/free-photo-of-golden-temple-at-night.jpeg?auto=compress&cs=tinysrgb&w=800",
        "delhi": "https://images.pexels.com/photos/3476472/pexels-photo-3476472.jpeg?auto=compress&cs=tinysrgb&w=800",
        "mumbai": "https://images.pexels.com/photos/10203531/pexels-photo-10203531.jpeg?auto=compress&cs=tinysrgb&w=800",
        "london": "https://images.pexels.com/photos/460672/pexels-photo-460672.jpeg?auto=compress&cs=tinysrgb&w=800",
    }
    
    # Check if a key is available (securely loaded or otherwise)
    if not UNSPLASH_ACCESS_KEY:
        return KNOWN_CITIES.get(city_name.lower(), None)
        
    try:
        query = f"famous landmark in {city_name}"
        params = {"query": query, "per_page": 1, "client_id": UNSPLASH_ACCESS_KEY}
        response = requests.get(UNSPLASH_API_URL, params=params)
        response.raise_for_status() 
        data = response.json()
        if data['results']:
            # Use 'small' or 'regular' depending on quality preference, 'regular' is typical for full display
            return data['results'][0]['urls']['regular'] 
        else:
            return KNOWN_CITIES.get(city_name.lower(), None)
            
    except requests.exceptions.RequestException:
        # Fallback to local image if Unsplash fails or key is invalid
        return KNOWN_CITIES.get(city_name.lower(), None)


def get_translation(key):
    """Retrieves the translated text for a given key."""
    lang = st.session_state.get('language', 'english')
    return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS['english'][key])

def update_theme(theme_choice):
    """Callback to update the internal theme state."""
    st.session_state['theme'] = 'dark' if 'Dark' in theme_choice or 'गहरा' in theme_choice else 'light'


# ---- CRITICAL FIX: CONSOLIDATED FETCH FUNCTION ----

def fetch_and_render_weather_data():
    """
    Handles all API calls and updates session state with weather data, background, 
    and landmark image URL.
    """
    T = get_translation
    city = st.session_state.city_input
    
    # Clear previous error and data on new search attempt
    st.session_state['error_message'] = None
    st.session_state['current_weather_data'] = None
    st.session_state['background_url'] = None
    st.session_state['search_triggered'] = False
    
    if not city:
        return

    # Check for API key availability before starting heavy network I/O
    if not WEATHERAPI_KEY:
        st.session_state['error_message'] = "Weather API Key is missing. Please check your secrets configuration."
        return

    try:
        # 1. Fetch Current Weather
        current_url = f"{WEATHERAPI_CURRENT_URL}?key={WEATHERAPI_KEY}&q={city}&aqi=no"
        current_res = requests.get(current_url)
        current_res.raise_for_status() 
        current_data = current_res.json()

        if 'error' in current_data:
            st.session_state['error_message'] = T("city_not_found").format(city.title())
            return
        
        # 2. Update Dynamic Background URL in state
        main_condition_text = current_data['current']['condition']['text']
        bg_url = get_weather_background_url(main_condition_text)
        st.session_state['background_url'] = bg_url
        
        # 3. Fetch Forecast Data
        forecast_url = f"{WEATHERAPI_FORECAST_URL}?key={WEATHERAPI_KEY}&q={city}&days=3"
        forecast_res = requests.get(forecast_url)
        forecast_res.raise_for_status() 
        forecast_data = forecast_res.json()
        
        # 4. Fetch City Landmark Image (using cached function)
        city_image_url = fetch_unsplash_image_url(city)
        st.session_state['city_image_url'] = city_image_url
        
        # 5. Save ALL data to state
        st.session_state['current_weather_data'] = current_data
        st.session_state['forecast_data'] = forecast_data
        st.session_state['search_triggered'] = True
        
    except requests.exceptions.HTTPError as e:
        # Handles 400 (Bad Request), 401 (Unauthorized - usually bad key), 404, etc.
        error_msg = f"API Request Failed ({e.response.status_code}). Check city name or API Key."
        st.session_state['error_message'] = error_msg
    except requests.exceptions.RequestException as e:
        # Handles Network issues (connection refused, timeouts)
        st.session_state['error_message'] = T("error_fetching").format(f"Network error: {e}")
    except Exception as e:
        # General catch for unexpected errors
        st.session_state['error_message'] = T("error_fetching").format(f"An unexpected error occurred: {e}")


# ---- PAGE CONFIG ----
st.set_page_config(page_title="Weather Now", page_icon="☁️", layout="wide")


# ---- DYNAMIC CSS FUNCTION ----

def apply_dynamic_css(dynamic_bg_style):
    
    is_dark = st.session_state.theme == 'dark'
    
    # Define colors based on theme
    bg_color_main = "#1e1e1e" if is_dark else "#333333"
    text_color = "#f0f2f6" if is_dark else "#333333"
    accent_color = "#4CAF50" if is_dark else "#6A5ACD"
    card_bg = "rgba(0, 0, 0, 0.4)" if is_dark else "rgba(255, 255, 255, 0.7)"
    input_bg = "rgba(50, 50, 50, 0.7)" if is_dark else "rgba(255, 255, 255, 0.4)"
    border_color = "rgba(255, 255, 255, 0.2)" if is_dark else "rgba(255, 255, 255, 0.8)"
    metric_bg = "rgba(50, 50, 50, 0.7)" if is_dark else "rgba(255, 255, 255, 0.4)"
    
    css = f"""
    <style>
    /* 1. App background: Dynamic injection of image or gradient */
    .stApp {{
        background: none !important;
        color: {bg_color_main};
        backdrop-filter: blur(0px); 
        -webkit-backdrop-filter: blur(0px);
        transition: color 0.5s;
    }}

    /* New CSS rule for the blurred background image (pseudo-element) */
    .stApp::before {{
        content: "";
        position: fixed; 
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: {dynamic_bg_style} !important;
        background-size: cover !important;
        z-index: -1; 
        transition: background-image 1s ease-in-out, filter 0.5s;
        /* Darken and blur the background image */
        filter: blur(8px) brightness({0.6 if is_dark else 1.0}); 
        -webkit-filter: blur(8px) brightness({0.6 if is_dark else 1.0});
    }}

    /* 2. Text color for general elements (dynamic based on theme) */
    .stText, .stMarkdown, .stSubheader, .stTitle, h1, h2, h3, h4, p, label {{
        color: {text_color} !important;
    }}
    
    /* FIX: Sidebar Headers and Radio Labels MUST be white (Light & Dark Mode) */
    [data-testid="stSidebarContent"] h2,
    [data-testid="stSidebarContent"] label,
    [data-testid="stSidebarContent"] div p {{ 
        color: white !important;
    }}

    /* Title Color */
    .centered-title h1 {{
        text-align: center; !important;
        font-weight: 900;
        letter-spacing: 2px;
        color: {accent_color};
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }}
    
    /* Input Styling */
    .stTextInput input {{
        color: {text_color} !important;
        background-color: {input_bg} !important;
        border: 1px solid {border_color} !important;
        padding: 10px;
        border-radius: 10px;
    }}
    
    /* 3. Floating 'Glassmorphism' card effect for all components */
    .card {{
        background: {card_bg};
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
        border: 1px solid {border_color};
        transition: transform 0.3s, box-shadow 0.3s;
    }}
    
    /* 5. Metric component styling */
    div[data-testid="stMetric"] > div {{
        background: {metric_bg};
        border: 1px solid {border_color};
        border-radius: 15px;
        padding: 8px 10px;
        text-align: center;
        transition: transform 0.3s, box-shadow 0.3s;
    }}
    div[data-testid="stMetric"] label {{
        color: {accent_color} !important;
        font-weight: bold;
        font-size: 0.9rem;
        margin-bottom: -5px;
    }}
    div[data-testid="stMetric"] div:nth-child(2) {{
        color: {text_color} !important;
        font-size: 1.5rem;
    }}
    
    /* H1 (Temperature) margin */
    .main-weather-card h1 {{
        font-size: 5rem;
        color: {text_color};
        margin-bottom: -15px !important;
        margin-top: 0px !important;
    }}
    /* H3 (Condition) margin */
    .main-weather-card h3 {{
        color: {accent_color};
        margin-top: 5px !important;
        margin-bottom: 5px !important;
    }}
    
    /* Style for the date in forecast cards */
    .forecast-card .date-text {{
        font-size: 0.85rem;
        color: {accent_color} !important;
        margin: -5px 0 5px 0 !important;
    }}
    
    /* Hide the default Streamlit footer elements */
    .stDeployButton, .st-emotion-cache-1r6r8q0 {{ 
        display: none !important; 
    }}
    
    /* Hover effects */
    .forecast-card:hover, div[data-testid="stMetric"] > div:hover {{
        transform: translateY(-8px);
        box-shadow: 0 20px 40px 0 rgba(0, 0, 0, 0.2);
    }}
    div[data-testid="stMetric"] > div:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 20px 0 rgba(0, 0, 0, 0.15);
    }}
    .main-weather-card {{
        transition: none !important;
        transform: none !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1) !important;
    }}
    .stTextInput label {{
        display: none;
    }}

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ---- DYNAMIC BACKGROUND LOGIC (Run Before Content) ----

# 1. Determine the default background
local_image_path = "bright_day_light.jpg"
base64_image = get_base64_image(local_image_path)

if base64_image:
    default_bg = f"url('data:image/jpeg;base64,{base64_image}') no-repeat center center fixed"
else:
    if st.session_state.theme == 'dark':
        default_bg = 'linear-gradient(135deg, #1C2833 0%, #2C3E50 50%, #4A637A 100%)'
    else:
        default_bg = 'linear-gradient(135deg, #CFD8DC 0%, #B0BEC5 50%, #78909C 100%)' 

# 2. Use the fetched background URL if available, otherwise use default/theme-based
dynamic_bg_style = default_bg
if st.session_state.get('background_url'):
    dynamic_bg_style = f"url('{st.session_state.background_url}') no-repeat center center fixed"
        
# --- Apply CSS after background is determined ---
apply_dynamic_css(dynamic_bg_style)


# ---- SIDEBAR FOR THEME AND LANGUAGE ----

def format_language_display(lang_key):
    if lang_key == 'english':
        return 'English'
    return 'हिंदी (Hindi)'

st.sidebar.markdown(f"## {get_translation('language_selector')}")
st.sidebar.radio(
    " ",
    ['english', 'hindi'], 
    key='language',
    index=0 if st.session_state.language == 'english' else 1,
    format_func=format_language_display
)

st.sidebar.markdown("---")

st.sidebar.markdown(f"## {get_translation('theme_selector')}")
st.sidebar.radio(
    " ",
    [get_translation('light_mode'), get_translation('dark_mode')],
    key='theme_choice',
    index=0 if st.session_state.theme == 'light' else 1,
    on_change=lambda: update_theme(st.session_state.theme_choice)
)


# ---- RENDER FUNCTIONS ----

def render_weather_results():
    """Renders the main weather content using data from session state."""
    
    T = get_translation
    
    # Check if data is available
    if not st.session_state.get('current_weather_data') or not st.session_state.get('forecast_data'):
        # If search was triggered but data is missing (due to an error), we exit render.
        return 
    
    city = st.session_state.city_input
    current_res = st.session_state.current_weather_data
    forecast_res = st.session_state.forecast_data
    image_url = st.session_state.city_image_url # Use the URL fetched and cached in the state
    
    # Get dynamic colors for inlined HTML
    accent = "#4CAF50" if st.session_state.theme == 'dark' else "#6A5ACD"
    text = "#f0f2f6" if st.session_state.theme == 'dark' else "#333333"

    
    # --- Columns and Content ---
    left_col_main, right_col_main = st.columns([1.5, 3]) 

    # --- LEFT COLUMN: IMAGE ---
    with left_col_main:
        if image_url:
            # Using st.image for better Streamlit compatibility, although custom CSS is applied to the HTML element
            st.markdown(f'<img class="card city-image" style="width:100%; height:auto;" src="{image_url}" alt="{city} landmark">', unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='card' style='text-align: center;'><h2 style='color: {accent};'>🏙️ {city.title()} {T('weather')}</h2><p style='color: {text};'>{T('landmark_unavailable')}</p></div>", unsafe_allow_html=True)

    # --- RIGHT COLUMN: MAIN WEATHER DATA (WeatherAPI Parsing) ---
    current = current_res['current']
    
    temp = current['temp_c']
    feels_like = current['feelslike_c']
    humidity = current['humidity']
    wind_speed = current['wind_kph'] * 1000 / 3600 # Convert kph to m/s
    pressure = current['pressure_mb'] * 1.0 # Convert mb to hPa (1mb = 1hPa)
    condition_description = current['condition']['text'].title()
    main_condition_text = current['condition']['text'].lower()
    
    with right_col_main:
        st.markdown('<div class="card main-weather-card">', unsafe_allow_html=True)
        
        # 1. City Heading (only if image is present on the left)
        if image_url: 
             st.markdown(f"<h2 style='color: {accent}; margin-top: 0px;'>🏙️ {city.title()} {T('weather')}</h2>", unsafe_allow_html=True)
        
        # 2. Temperature and Condition
        st.markdown(f"""
            <h1 class="main-temp">
                {temp:.0f} °C
            </h1>
            <h3 class="main-condition">
                {condition_description}
            </h3>
        """, unsafe_allow_html=True)
        
        # 3. Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(T("feels_like"), f"{feels_like:.0f} °C")
        col2.metric(T("humidity"), f"{humidity} %")
        col3.metric(T("wind_speed"), f"{wind_speed:.1f} m/s")
        col4.metric(T("pressure"), f"{pressure:.0f} hPa")
        
        st.markdown('</div>', unsafe_allow_html=True) # End of Main Card

    # Severe alert
    if any(keyword in main_condition_text for keyword in ["thunder", "rain", "heavy", "snow", "sleet"]):
        st.error(T("severe_alert"))
        
    st.markdown("---") 

    # ---- 3-DAY FORECAST ----
    st.markdown(f"<h2 style='color: {accent};'>{T('forecast_header')}</h2>", unsafe_allow_html=True)
    
    if 'forecast' in forecast_res and 'forecastday' in forecast_res['forecast']:
        
        forecast_days = forecast_res['forecast']['forecastday']
        forecast_cols = st.columns(min(len(forecast_days), 3)) 
        
        icon_map = {
             "clear": "☀️", "sunny": "☀️","cloud": "☁️", "rain": "🌧️", 
             "drizzle": "☔", "thunder": "⛈️", "snow": "❄️", 
             "mist": "🌫️", "fog": "🌫️", "haze": "🌫️",
        }
        
        for i, daily_info in enumerate(forecast_days):
            
            date = daily_info["date"]
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            date_formatted_day = date_obj.strftime("%a")
            date_formatted_date = date_obj.strftime("%b %d") 
            
            day_data = daily_info["day"]
            condition_text = day_data["condition"]["text"].lower()
            temp_max = day_data["maxtemp_c"]
            temp_min = day_data["mintemp_c"]
            
            icon = "❓"
            for keyword, emoji in icon_map.items():
                if keyword in condition_text:
                    icon = emoji
                    break

            with forecast_cols[i]:
                translated_condition = day_data["condition"]["text"].title()
                
                st.markdown(
                    f"""
                    <div class="card forecast-card" style="padding: 15px; text-align: center;">
                        <h4 style='margin-bottom: 0px; color: {accent};'>{date_formatted_day}</h4>
                        <p class="date-text">{date_formatted_date}</p> <p style='font-size: 2rem; margin-top: 0; margin-bottom: 10px;'>{icon}</p>
                        <p style='font-size: 1.5rem; font-weight: bold; margin: 0; color: {text};'>{temp_max:.0f}°C / {temp_min:.0f}°C</p>
                        <p style='font-size: 0.8rem; opacity: 0.8; margin-top: 5px; color: {text};'>{translated_condition}</p>
                    </div>
                    """, unsafe_allow_html=True
                )
    else:
        st.warning(T("forecast_error"))


def display_app_content():
    
    T = get_translation
    
    accent = "#4CAF50" if st.session_state.theme == 'dark' else "#6A5ACD"
    text = "#f0f2f6" if st.session_state.theme == 'dark' else "#333333"

    col_left_pad, col_center_content, col_right_pad = st.columns([1, 5, 1]) 
    
    with col_center_content:
        
        # --- App Header (Title and Tagline) ---
        st.markdown('<div class="centered-title">', unsafe_allow_html=True)
        st.title(T("title"))
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(
            f"""
            <div style="text-align: center; color: {text}; margin-top: -10px;">
                {T('tagline')}
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        
        # 2. City Input (CRITICAL: on_change calls the fetch function)
        st.text_input(
            T("input_label"), 
            key="city_input", 
            on_change=fetch_and_render_weather_data, # Calls the consolidated fetch function
            placeholder=T("input_placeholder")
        )
        
        # 3. Display Errors or Info/Results
        if st.session_state.get('error_message'):
            # Display any error message generated during fetch
            st.error(st.session_state.error_message)
            st.session_state['error_message'] = None # Clear after display
        
        elif st.session_state.get('city_input') and not st.session_state.get('search_triggered'):
            # The search hasn't executed yet (user has typed, but not pressed Enter)
            st.info(T("press_enter"))
        
        elif not st.session_state.get('search_triggered'):
            # Initial Welcome Card 
            st.markdown(f'''
                <div class="card" style="text-align: center; padding: 50px;">
                    <h2 style="color: {accent};">{T('welcome')}</h2>
                    <p style="color: {text};">{T('welcome_detail')}</p>
                </div>
            ''', unsafe_allow_html=True)
        
# ---- App Execution Flow ----
display_app_content()

# RENDER content using data already stored in session state
if st.session_state.get('search_triggered'):
    # The render function will use the full width and check if data exists
    render_weather_results()