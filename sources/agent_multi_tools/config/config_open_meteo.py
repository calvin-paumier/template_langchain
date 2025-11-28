class ConfigOpenMeteo:
    BASE_URL = "https://api.open-meteo.com/v1"
    DEFAULT_CITY = "Paris"
    DEFAULT_COORDINATES = {"latitude": 48.8566, "longitude": 2.3522}
    TIMEOUT_SECONDS = 10

    CURRENT_PARAMS = ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "weather_code", "wind_speed_10m"]

    FORECAST_PARAMS = ["temperature_2m_max", "temperature_2m_min", "weather_code", "precipitation_probability_max"]

    WEATHER_CODES = {
        0: "Ciel dégagé",
        1: "Principalement dégagé",
        2: "Partiellement nuageux",
        3: "Nuageux",
        45: "Brouillard",
        48: "Brouillard givrant",
        51: "Bruine légère",
        53: "Bruine modérée",
        55: "Bruine forte",
        61: "Pluie légère",
        63: "Pluie modérée",
        65: "Pluie forte",
        71: "Neige légère",
        73: "Neige modérée",
        75: "Neige forte",
        80: "Averses légères",
        81: "Averses modérées",
        82: "Averses fortes",
        95: "Orage",
    }
