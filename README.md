# Weather App

A friendly web application that lets you search any city and get up-to-date weather information. Built with Django, this app calls a geocoding API to find your location and then fetches current weather data.

## Why This Exists

Looking up weather manually is tedious. This app streamlines the process: type a city name, and instantly see the weather details you need.

## Features

- **City Search with Geocoding**  
  Uses the Open-Meteo Geocoding API to transform a city name into precise latitude/longitude coordinates.  
- **Live Weather Data**  
  Fetches current temperature, humidity, wind speed, and more from a public weather API.  
- **Responsive Design**  
  Clean, mobile-friendly interface crafted with Django templates, HTML, CSS, and JavaScript.  
- **Error Handling**  
  User-friendly messages if the city isn’t found or if the API request fails.

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/Pranay1012/Weather_App.git
   cd Weather_App
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Open your browser**
   Visit `http://127.0.0.1:8000/` and start searching for your city.

> **Tip:** Enter at least three letters of the city name for fuzzy matching by the geocoding API.

## How It Works

1. **Geocoding**  
   The app sends your city name to the Open-Meteo Geocoding API, receiving a list of matching locations with latitude and longitude.  
2. **Weather Request**  
   Using those coordinates, it fetches current weather details from a public weather API.  
3. **Display**  
   Renders the weather information (temperature, humidity, wind) neatly in the browser.

## Tech Stack

- **Backend:** Django, Python  
- **Frontend:** HTML5, CSS3, JavaScript,   
- **Geocoding API:** Open-Meteo Geocoding (https://geocoding-api.open-meteo.com)  
- **Weather API:** (e.g., OpenWeatherMap)  

## Project Structure

```
Weather_App/
├── app.py            # Main Django URLs and views (or manage.py if standard Django)
├── settings.py       # Django settings, including API URLs
├── templates/        # HTML templates (index.html, results.html)
├── static/           # CSS and JS assets
├── .env              # Environment variables (API keys)
├── requirements.txt  # Python dependencies
└── README.md         # This documentation
```

## License

This project is open source under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Happy weather watching! ☀️🌦️