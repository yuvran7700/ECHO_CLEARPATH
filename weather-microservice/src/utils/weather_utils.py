from decimal import Decimal


def temperature_classification(
    tempMin: int, tempMax: int, amTemp: int, pmTemp: int
):
    avgTemp = (tempMin + tempMax + amTemp + pmTemp) / 4

    if avgTemp < 15:
        return "Cold"
    elif avgTemp < 22:
        return "Mild"
    elif avgTemp < 30:
        return "Warm"
    else:
        return "Hot"


def rainfall_classification(rainfall: int):
    if rainfall == 0.0:
        return "No rain"
    elif rainfall < 10:
        return "Light rain"
    elif rainfall < 25:
        return "Moderate rain"
    else:
        return "Heavy rain"


def sunshine_classification(sunshineHours: int):
    sun_ratio = sunshineHours / 24
    if sun_ratio < 0.4:
        return "Cloudy"
    elif sun_ratio <= 0.8:
        return "Partly Cloudy"
    else:
        return "Sunny"


def wind_classification(windGustSpeed: int):
    if windGustSpeed < 20:
        return "Calm"
    elif windGustSpeed < 38:
        return "Breezy"
    elif windGustSpeed < 61:
        return "Windy"
    else:
        return "Gale"


def humidity_classification(amHumidity: int, pmHumidity: int):
    avgHumidity = (amHumidity + pmHumidity) / 2

    if avgHumidity <= 30:
        return "Low Humidity"
    elif avgHumidity <= 60:
        return "Moderate Humidity"
    elif avgHumidity <= 80:
        return "High Humidity"
    else:
        return "Extreme Humidity"


def decimal_converter(x):
    if isinstance(x, Decimal):
        return float(x)
