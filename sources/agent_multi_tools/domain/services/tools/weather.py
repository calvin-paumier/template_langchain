from langchain_core.tools import BaseTool
from pydantic import BaseModel

from sources.agent_multi_tools.config.config_tools import ApiMeteoToolInput
from sources.agent_multi_tools.domain.ports.chat_history_handler import ChatHistoryHandler
from sources.agent_multi_tools.domain.ports.llm_handler import LLMHandler
from sources.agent_multi_tools.domain.ports.weather_api_handler import WeatherApiHandler
from sources.agent_multi_tools.domain.services.chains.chain_weather import ChainWeather


class Weather(BaseTool):
    """Tool météo utilisant Open-Meteo API"""

    name: str = "weather_api"
    description: str = """This tool helps to get informations about current weather and forecasts for cities around the world."""
    args_schema: type[BaseModel] = ApiMeteoToolInput

    weather_api_handler: WeatherApiHandler
    llm_handler: LLMHandler
    chat_history_handler: ChatHistoryHandler

    def __init__(
        self,
        weather_api_handler: WeatherApiHandler,
        llm_handler: LLMHandler,
        chat_history_handler: ChatHistoryHandler,
        **kwargs,
    ):
        super().__init__(
            weather_api_handler=weather_api_handler, llm_handler=llm_handler, chat_history_handler=chat_history_handler, **kwargs
        )

    def _run(self, city: str, days: int, session_id: str) -> str:
        if days == 0:
            weather_data = self.weather_api_handler.get_current_weather(city)
        else:
            weather_data = self.weather_api_handler.get_forecast(city, days)

        weather_chain = ChainWeather(
            llm_handler=self.llm_handler,
            chat_history_handler=self.chat_history_handler,
        )

        response = weather_chain.invoke(weather_data, session_id)
        return response.content
