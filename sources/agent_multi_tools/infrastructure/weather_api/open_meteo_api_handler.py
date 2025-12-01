from typing import Any

import requests
from geopy.geocoders import Nominatim

from sources.agent_multi_tools.config.config_open_meteo import ConfigOpenMeteo
from sources.agent_multi_tools.ports.weather_api_handler import WeatherApiHandler


class OpenMeteoApiHandler(WeatherApiHandler):
    def __init__(self):
        self.base_url = ConfigOpenMeteo.BASE_URL
        self.geocoder = Nominatim(user_agent="template_langchain_weather")

    def _get_coordinates(self, city: str) -> dict[str, float] | None:
        if city.lower() == "default":
            return ConfigOpenMeteo.DEFAULT_COORDINATES
        try:
            location = self.geocoder.geocode(city)
            if location:
                return {"latitude": location.latitude, "longitude": location.longitude}
        except Exception:
            return None
        return None

    def get_current_weather(self, city: str) -> dict[str, Any]:
        try:
            coords = self._get_coordinates(city)
            if not coords:
                return {"status": "error", "message": f"Ville '{city}' non trouvée"}

            url = f"{self.base_url}/forecast"
            params = {
                "latitude": coords["latitude"],
                "longitude": coords["longitude"],
                "current": ",".join(ConfigOpenMeteo.CURRENT_PARAMS),
                "timezone": "Europe/Paris",
            }

            response = requests.get(url, params=params, timeout=ConfigOpenMeteo.TIMEOUT_SECONDS)
            response.raise_for_status()

            data = response.json()
            current = data["current"]

            weather_code = current.get("weather_code", 0)
            description = ConfigOpenMeteo.WEATHER_CODES.get(weather_code, "Inconnu")

            return {
                "city": city,
                "coordinates": coords,
                "temperature": current["temperature_2m"],
                "apparent_temperature": current["apparent_temperature"],
                "humidity": current["relative_humidity_2m"],
                "wind_speed": current["wind_speed_10m"],
                "description": description,
                "weather_code": weather_code,
                "timestamp": current["time"],
                "status": "success",
            }

        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Erreur réseau: {str(e)}"}
        except Exception as e:
            return {"status": "error", "message": f"Erreur: {str(e)}"}

    def get_forecast(self, city: str, days: int) -> dict[str, Any]:
        try:
            coords = self._get_coordinates(city)
            if not coords:
                return {"status": "error", "message": f"Ville '{city}' non trouvée"}

            url = f"{self.base_url}/forecast"
            params = {
                "latitude": coords["latitude"],
                "longitude": coords["longitude"],
                "daily": ",".join(ConfigOpenMeteo.FORECAST_PARAMS),
                "forecast_days": min(days, 7),
                "timezone": "Europe/Paris",
            }

            response = requests.get(url, params=params, timeout=ConfigOpenMeteo.TIMEOUT_SECONDS)
            response.raise_for_status()

            data = response.json()
            daily = data["daily"]

            forecasts = []
            for i in range(len(daily["time"])):
                weather_code = daily["weather_code"][i]
                description = ConfigOpenMeteo.WEATHER_CODES.get(weather_code, "Inconnu")

                forecasts.append(
                    {
                        "date": daily["time"][i],
                        "temperature_max": daily["temperature_2m_max"][i],
                        "temperature_min": daily["temperature_2m_min"][i],
                        "precipitation_probability": daily["precipitation_probability_max"][i],
                        "description": description,
                        "weather_code": weather_code,
                    }
                )

            return {"city": city, "coordinates": coords, "forecasts": forecasts, "status": "success"}

        except Exception as e:
            return {"status": "error", "message": str(e)}
