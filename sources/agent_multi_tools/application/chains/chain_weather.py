from typing import Any

from langchain_core.runnables import RunnableWithMessageHistory

from sources.agent_multi_tools.config.config_prompt import ConfigPrompts
from sources.agent_multi_tools.ports.chat_history_handler import ChatHistoryHandler
from sources.agent_multi_tools.ports.llm_handler import LLMHandler
from sources.agent_multi_tools.utils.prompt_formater import PromptFormater


class ChainWeather:
    def __init__(self, llm_handler: LLMHandler, chat_history_handler: ChatHistoryHandler):
        self.llm_handler = llm_handler
        self.chat_history_handler = chat_history_handler

    def get_chain(self) -> RunnableWithMessageHistory:
        llm = self.llm_handler.get_llm()

        weather_prompt = PromptFormater.create_chat_prompt_with_history(ConfigPrompts.WEATHER)

        chain = weather_prompt | llm

        return RunnableWithMessageHistory(
            chain,
            self.chat_history_handler.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    def invoke(self, weather_data: dict[str, Any], session_id: str) -> str:
        chain = self.get_chain()
        return chain.invoke({"input": str(weather_data)}, config={"configurable": {"session_id": session_id}})
