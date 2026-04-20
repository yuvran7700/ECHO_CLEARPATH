# transport-microservice/src/utils/classifiers.py
def classify_temperature(max_temp_c: float, min_temp_c: float) -> str:
    avg = (max_temp_c + min_temp_c) / 2
    if avg < 15:
        return "Cold"
    elif avg < 22:
        return "Mild"
    elif avg < 30:
        return "Warm"
    else:
        return "Hot"


def classify_rainfall(rainfall_mm: float) -> str:
    if rainfall_mm == 0.0:
        return "No rain"
    elif rainfall_mm < 10:
        return "Light rain"
    elif rainfall_mm < 25:
        return "Moderate rain"
    else:
        return "Heavy rain"


def classify_wind(max_wind_speed_kmh: float) -> str:
    if max_wind_speed_kmh < 20:
        return "Calm"
    elif max_wind_speed_kmh < 38:
        return "Breezy"
    elif max_wind_speed_kmh < 61:
        return "Windy"
    else:
        return "Gale"


def classify_humidity(humidity_percent: float) -> str:
    if humidity_percent <= 30:
        return "Low Humidity"
    elif humidity_percent <= 60:
        return "Moderate Humidity"
    elif humidity_percent <= 80:
        return "High Humidity"
    else:
        return "Extreme Humidity"


def classify_sun_from_condition(weather_condition_text: str) -> str:
    condition = weather_condition_text.lower()
    if "partly" in condition:
        return "Partly Cloudy"
    elif "cloud" in condition or "rain" in condition or "drizzle" in condition:
        return "Cloudy"
    else:
        return "Sunny"
