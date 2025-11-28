from langchain_core.tools import BaseTool
from pydantic import BaseModel

from sources.agent_multi_tools.config.config_tools import LLMToolInput
from sources.agent_multi_tools.domain.ports.chat_history_handler import ChatHistoryHandler
from sources.agent_multi_tools.domain.ports.database_handler import DatabaseHandler
from sources.agent_multi_tools.domain.ports.llm_handler import LLMHandler
from sources.agent_multi_tools.domain.services.chains.chain_rag import ChainRag


class Rag(BaseTool):
    """Tool pour donner une réponse à une question basée sur la base de données sur Valkyria."""

    name: str = "get_information_from_database"
    description: str = "This tool gives an answer to a question based on the Valkyria database."
    args_schema: type[BaseModel] = LLMToolInput

    database_handler: DatabaseHandler
    llm_handler: LLMHandler
    chat_history_handler: ChatHistoryHandler

    def __init__(
        self,
        database_handler: DatabaseHandler,
        llm_handler: LLMHandler,
        chat_history_handler: ChatHistoryHandler,
        **kwargs,
    ):
        super().__init__(
            database_handler=database_handler,
            llm_handler=llm_handler,
            chat_history_handler=chat_history_handler,
            **kwargs,
        )

    def _run(self, input: str, session_id: str) -> str:
        chain = ChainRag(
            database_handler=self.database_handler,
            llm_handler=self.llm_handler,
            chat_history_handler=self.chat_history_handler,
        )
        result = chain.invoke(query=input, session_id=session_id)
        return result["answer"]
