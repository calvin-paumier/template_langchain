from typing import Any

from langchain_core.runnables import RunnableWithMessageHistory

from sources.agent_multi_tools.config.config_prompt import ConfigPrompts
from sources.agent_multi_tools.ports.chat_history_handler import ChatHistoryHandler
from sources.agent_multi_tools.ports.database_handler import DatabaseHandler
from sources.agent_multi_tools.ports.llm_handler import LLMHandler
from sources.agent_multi_tools.utils.prompt_formater import PromptFormater
from sources.agent_multi_tools.utils.sql_formater import SQLFormater


class ChainTextToSQL:
    def __init__(
        self,
        database_handler: DatabaseHandler,
        llm_handler: LLMHandler,
        chat_history_handler: ChatHistoryHandler,
        tables: list,
    ):
        self.database_handler = database_handler
        self.llm_handler = llm_handler
        self.chat_history_handler = chat_history_handler
        self.tables = tables

    def get_chain(self) -> RunnableWithMessageHistory:
        llm = self.llm_handler.get_llm()

        sql_schema = SQLFormater.get_schema_from_config(self.tables)
        system_message = PromptFormater.format_string(ConfigPrompts.TEXT_TO_SQL, sql_schema=sql_schema)
        text_to_sql_prompt = PromptFormater.create_chat_prompt_with_history(system_message)

        base_chain = text_to_sql_prompt | llm

        return RunnableWithMessageHistory(
            base_chain,
            self.chat_history_handler.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    def invoke(self, query: str, session_id: str) -> dict[str, Any]:
        chain = self.get_chain()
        return chain.invoke(
            {"input": query},
            config={"configurable": {"session_id": session_id}},
        )
