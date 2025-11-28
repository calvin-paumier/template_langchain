from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables import RunnableWithMessageHistory

from sources.agent_multi_tools.config.config_prompt import ConfigPrompts
from sources.agent_multi_tools.config.config_sql import ConfigEmbeddingWikitext
from sources.agent_multi_tools.domain.ports.chat_history_handler import ChatHistoryHandler
from sources.agent_multi_tools.domain.ports.database_handler import DatabaseHandler
from sources.agent_multi_tools.domain.ports.llm_handler import LLMHandler
from sources.agent_multi_tools.domain.services.utils.prompt_formater import PromptFormater


class ChainRag:
    def __init__(
        self,
        database_handler: DatabaseHandler,
        llm_handler: LLMHandler,
        chat_history_handler: ChatHistoryHandler,
    ):
        self.database_handler = database_handler
        self.llm_handler = llm_handler
        self.chat_history_handler = chat_history_handler

    def get_chain(self) -> RunnableWithMessageHistory:
        vector_store = self.database_handler.get_vector_store(ConfigEmbeddingWikitext.COLLECTION_NAME)
        llm = self.llm_handler.get_llm()

        retriever_prompt = PromptFormater.create_chat_prompt_with_history(ConfigPrompts.REFORMAT_FOR_RETRIEVER)
        history_aware_retriever = create_history_aware_retriever(llm, vector_store.as_retriever(), retriever_prompt)

        generation_prompt = PromptFormater.create_chat_prompt_with_history(ConfigPrompts.GENERATION)
        chain_documents = create_stuff_documents_chain(llm, generation_prompt)

        chain_with_retriever = create_retrieval_chain(history_aware_retriever, chain_documents)

        return RunnableWithMessageHistory(
            chain_with_retriever,
            self.chat_history_handler.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

    def invoke(self, query: str, session_id: str) -> dict:
        chain = self.get_chain()
        return chain.invoke({"input": query}, config={"configurable": {"session_id": session_id}})
