from decimal import Decimal


def temperature_classification(
    tempMin: int, tempMax: int, amTemp: int, pmTemp: int
):
    temps = [tempMin, tempMax, amTemp, pmTemp]
    valid_temps = [t for t in temps if t != "Unavailable"]

    if not valid_temps:
        return "N/A"

    avgTemp = sum(valid_temps) / len(valid_temps)

    if avgTemp < 15:
        return "Cold"
    elif avgTemp < 22:
        return "Mild"
    elif avgTemp < 30:
        return "Warm"
    else:
        return "Hot"


def rainfall_classification(rainfall: int):
    if rainfall == "Unavailable":
        return "N/A"

    if rainfall == 0.0:
        return "No rain"
    elif rainfall < 10:
        return "Light rain"
    elif rainfall < 25:
        return "Moderate rain"
    else:
        return "Heavy rain"


def sunshine_classification(sunshineHours: int):
    if sunshineHours == "Unavailable":
        return "N/A"

    sun_ratio = sunshineHours / 12
    if sun_ratio < 0.2:
        return "Cloudy"
    elif sun_ratio <= 0.7:
        return "Partly Cloudy"
    else:
        return "Sunny"


def wind_classification(windGustSpeed: int):
    if windGustSpeed == "Unavailable":
        return "N/A"

    if windGustSpeed < 20:
        return "Calm"
    elif windGustSpeed < 38:
        return "Breezy"
    elif windGustSpeed < 61:
        return "Windy"
    else:
        return "Gale"


def humidity_classification(amHumidity: int, pmHumidity: int):
    hums = [amHumidity, pmHumidity]
    valid_hums = [h for h in hums if h != "Unavailable"]

    if not valid_hums:
        return "N/A"

    avgHumidity = sum(valid_hums) / len(valid_hums)

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


def dynamodb_converter(x):
    if x == "Unavailable":
        return "Unavailable"
    return Decimal(str(x))
