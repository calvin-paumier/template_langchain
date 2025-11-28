from langchain_core.tools import BaseTool
from pydantic import BaseModel

from sources.agent_multi_tools.config.config_tools import LLMToolInput
from sources.agent_multi_tools.domain.ports.chat_history_handler import ChatHistoryHandler
from sources.agent_multi_tools.domain.ports.llm_handler import LLMHandler
from sources.agent_multi_tools.domain.services.chains.chain_conversation import ChainConversation


class Conversation(BaseTool):
    """Tool pour répondre aux questions générales."""

    name: str = "get_general_conversation"
    description: str = "This tool gives an answer to a general question."
    args_schema: type[BaseModel] = LLMToolInput

    llm_handler: LLMHandler
    chat_history_handler: ChatHistoryHandler

    def __init__(
        self,
        llm_handler: LLMHandler,
        chat_history_handler: ChatHistoryHandler,
        **kwargs,
    ):
        super().__init__(llm_handler=llm_handler, chat_history_handler=chat_history_handler, **kwargs)

    def _run(self, input: str, session_id: str) -> str:
        chain = ChainConversation(llm_handler=self.llm_handler, chat_history_handler=self.chat_history_handler)
        result = chain.invoke(query=input, session_id=session_id)
        return result.content
