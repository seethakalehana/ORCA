
import requests


def get_inland_conditions(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
            "wind_direction_10m"
        ],
        "timezone": "auto"
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()

    return {
        "data_source": "Open-Meteo",
        "latitude": latitude,
        "longitude": longitude,
        "current_conditions": data.get("current", {})
    }
