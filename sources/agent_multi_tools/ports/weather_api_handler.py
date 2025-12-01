from abc import ABC, abstractmethod
from typing import Any


class WeatherApiHandler(ABC):
    @abstractmethod
    def get_current_weather(self, city: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def get_forecast(self, city: str, days: int = 3) -> dict[str, Any]:
        pass
