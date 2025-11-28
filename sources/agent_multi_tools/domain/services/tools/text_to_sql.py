from langchain_core.tools import BaseTool
from pydantic import BaseModel

from sources.agent_multi_tools.config.config_tools import LLMToolInput
from sources.agent_multi_tools.domain.ports.chat_history_handler import ChatHistoryHandler
from sources.agent_multi_tools.domain.ports.database_handler import DatabaseHandler
from sources.agent_multi_tools.domain.ports.llm_handler import LLMHandler
from sources.agent_multi_tools.domain.services.chains.chain_text_to_sql import ChainTextToSQL


class TextToSql(BaseTool):
    """Tool pour générer des requêtes SQL"""

    name: str = "get_sql_query"
    description: str = "This tool helps to get informations from Sanrio characters by building a SQL query."
    args_schema: type[BaseModel] = LLMToolInput

    database_handler: DatabaseHandler
    llm_handler: LLMHandler
    chat_history_handler: ChatHistoryHandler
    tables: list

    def __init__(
        self,
        database_handler: DatabaseHandler,
        llm_handler: LLMHandler,
        chat_history_handler: ChatHistoryHandler,
        tables: list,
        **kwargs,
    ):
        super().__init__(
            database_handler=database_handler,
            llm_handler=llm_handler,
            chat_history_handler=chat_history_handler,
            tables=tables,
            **kwargs,
        )

    def _run(self, input: str, session_id: str) -> dict:
        chain = ChainTextToSQL(
            database_handler=self.database_handler,
            llm_handler=self.llm_handler,
            chat_history_handler=self.chat_history_handler,
            tables=self.tables,
        )
        result = chain.invoke(query=input, session_id=session_id)
        return result.content
