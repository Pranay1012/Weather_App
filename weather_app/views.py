from django.shortcuts import render
import requests
import datetime

def fetch_weather_and_forecast(city):
    # Geocoding to get latitude and longitude
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    geocode_response = requests.get(geocode_url)
    geocode_response.raise_for_status()
    geocode_data = geocode_response.json()
    if not geocode_data.get('results'):
        return None, [], f"City not found: {city}"
        
    lat = geocode_data['results'][0].get('latitude')
    lon = geocode_data['results'][0].get('longitude')
    if not (lat and lon):
        return None, [], f"Invalid coordinates for {city}"
        
    # Fetch weather and forecast
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min,weather_code&timezone=auto&forecast_days=5"
    weather_response = requests.get(weather_url)
    weather_response.raise_for_status()
    weather_data = weather_response.json()
        
    if 'current' not in weather_data:
        return None, [], f"Error fetching weather for {city}: Invalid response"
        
    current_data = weather_data['current']
    weather_code = current_data.get('weather_code')
    if weather_code is None:
        return None, [], f"Error fetching weather for {city}: Missing weather code"
        
    try:
        weather_code = int(weather_code)
    except (TypeError, ValueError):
        return None, [], f"Error fetching weather for {city}: Invalid weather code"
        
    weather_desc = {
            0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
            45: "fog", 48: "depositing rime fog",
            51: "light drizzle", 53: "moderate drizzle", 55: "dense drizzle",
            61: "slight rain", 63: "moderate rain", 65: "heavy rain",
            71: "slight snow", 73: "moderate snow", 75: "heavy snow",
            80: "slight rain showers", 81: "moderate rain showers", 82: "heavy rain showers",
            95: "thunderstorm"
        }
        
    # Current weather data
    temperature = float(current_data.get('temperature_2m', 0))
    weather_data_dict = {
        'city': city.title(),
        'temperature': round(temperature, 2),
        'description': weather_desc.get(weather_code, "unknown"),
        'icon': str(weather_code)
    }
        
    # 5-day forecast
    daily_forecasts = []
    if 'daily' not in weather_data or not isinstance(weather_data['daily'], dict):
        return weather_data_dict, [], f"Error fetching forecast for {city}: Invalid daily data"
    
    daily_data = weather_data['daily']
    required_keys = ['time', 'temperature_2m_max', 'temperature_2m_min', 'weather_code']
    if not all(key in daily_data for key in required_keys):
        return weather_data_dict, [], f"Error fetching forecast for {city}: Missing daily keys"
    
    for idx, daily_time in enumerate(daily_data['time'][:5]):
        try:
            forecast_code = int(daily_data['weather_code'][idx])
            min_temp = float(daily_data['temperature_2m_min'][idx])
            max_temp = float(daily_data['temperature_2m_max'][idx])
        except (TypeError, ValueError, IndexError):
            return weather_data_dict, [], f"Error processing forecast for {city}"
        daily_forecasts.append({
            'day': datetime.datetime.strptime(daily_time, '%Y-%m-%d').strftime('%A'),
            'min_temp': round(min_temp, 2),
            'max_temp': round(max_temp, 2),
            'description': weather_desc.get(forecast_code, "unknown"),
            'icon': str(forecast_code)
        })
    
    return weather_data_dict, daily_forecasts, None

def index(request):
    error_message = None
    weather_data1, daily_forecasts1 = None, []
    weather_data2, daily_forecasts2 = None, []
    
    if request.method == 'POST':
        city1 = request.POST.get('city1', '').strip()
        city2 = request.POST.get('city2', '').strip()
        if city1:
            weather_data1, daily_forecasts1, error1 = fetch_weather_and_forecast(city1)
            if error1:
                error_message = error1
        else:
            error_message = "City 1 is required."
        if city2:
            weather_data2, daily_forecasts2, error2 = fetch_weather_and_forecast(city2)
            if error2:
                error_message = (error_message + " " if error_message else "") + error2
    
    context = {
        'weather_data1': weather_data1,
        'daily_forecasts1': daily_forecasts1,
        'weather_data2': weather_data2,
        'daily_forecasts2': daily_forecasts2,
        'error_message': error_message
    }
    return render(request, 'weather_app/index.html', context)