from langchain_core.runnables import RunnableWithMessageHistory

from sources.agent_multi_tools.config.config_prompt import ConfigPrompts
from sources.agent_multi_tools.ports.chat_history_handler import ChatHistoryHandler
from sources.agent_multi_tools.ports.llm_handler import LLMHandler
from sources.agent_multi_tools.utils.prompt_formater import PromptFormater


class ChainConversation:
    def __init__(self, llm_handler: LLMHandler, chat_history_handler: ChatHistoryHandler):
        self.llm_handler = llm_handler
        self.chat_history_handler = chat_history_handler

    def get_chain(self) -> RunnableWithMessageHistory:
        llm = self.llm_handler.get_llm()

        conversation_prompt = PromptFormater.create_chat_prompt_with_history(ConfigPrompts.CONVERSATION)

        chain = conversation_prompt | llm

        return RunnableWithMessageHistory(
            chain,
            self.chat_history_handler.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    def invoke(self, query: str, session_id: str) -> dict:
        chain = self.get_chain()
        return chain.invoke({"input": query}, config={"configurable": {"session_id": session_id}})
