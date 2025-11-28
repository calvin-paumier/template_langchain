import os

import streamlit as st
from dotenv import load_dotenv

from sources.agent_multi_tools.config.config_sql import ConfigSanrioData
from sources.agent_multi_tools.config.config_tools import ConfigTools
from sources.agent_multi_tools.domain.services.agent.agent_state import AgentState
from sources.agent_multi_tools.domain.services.agent.agent_state_graph import AgentStateGraph
from sources.agent_multi_tools.domain.services.tools.conversation import Conversation
from sources.agent_multi_tools.domain.services.tools.rag import Rag
from sources.agent_multi_tools.domain.services.tools.text_to_sql import TextToSql
from sources.agent_multi_tools.domain.services.tools.weather import Weather
from sources.agent_multi_tools.infrastructure.chat_history.in_memory_chat_history_handler import InMemoryChatHistoryHandler
from sources.agent_multi_tools.infrastructure.database.postgres_databse_handler import PostgresDatabaseHandler
from sources.agent_multi_tools.infrastructure.embeddings.ollama_embedding_handler import OllamaEmbeddingHandler
from sources.agent_multi_tools.infrastructure.interface.chat_handler import ChatHandler
from sources.agent_multi_tools.infrastructure.llm.ollama_llm_handler import OllamaLLMHandler
from sources.agent_multi_tools.infrastructure.weather_api.open_meteo_api_handler import OpenMeteoApiHandler

load_dotenv()


@st.cache_resource
def initialize_chat_handler():
    # Handlers
    chat_history_handler = InMemoryChatHistoryHandler()
    embeddings_handler = OllamaEmbeddingHandler()
    database_handler = PostgresDatabaseHandler(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        embedding_handler=embeddings_handler,
    )
    llm_handler = OllamaLLMHandler(
        base_url=os.getenv("OLLAMA_URL"),
        model=os.getenv("OLLAMA_MODEL"),
    )
    weather_api_handler = OpenMeteoApiHandler()

    # Tools
    text_to_sql_tool = TextToSql(
        database_handler=database_handler,
        llm_handler=llm_handler,
        chat_history_handler=chat_history_handler,
        tables=[ConfigSanrioData],
    )

    rag_tool = Rag(
        database_handler=database_handler,
        llm_handler=llm_handler,
        chat_history_handler=chat_history_handler,
    )

    conversation_tool = Conversation(
        database_handler=database_handler,
        llm_handler=llm_handler,
        chat_history_handler=chat_history_handler,
    )

    weather_tool = Weather(
        weather_api_handler=weather_api_handler, llm_handler=llm_handler, chat_history_handler=chat_history_handler
    )

    tools = {
        ConfigTools.conversation: conversation_tool,
        ConfigTools.rag: rag_tool,
        ConfigTools.text_to_sql: text_to_sql_tool,
        ConfigTools.weather_api: weather_tool,
    }

    # Agent
    agent_state_graph = AgentStateGraph(
        llm_handler=llm_handler, chat_history_handler=chat_history_handler, tools=tools
    ).compile_workflow(state=AgentState, memory=True)

    return ChatHandler(agent_state_graph, chat_history_handler)


def main():
    st.set_page_config(page_title="🤖 RAG Assistant", page_icon="🤖", layout="wide")

    st.title("🤖 Assistant RAG")

    chat_handler = initialize_chat_handler()

    if "session_id" not in st.session_state:
        st.session_state.session_id = "default"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Que voulez-vous savoir ?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Réflexion en cours..."):
                try:
                    response = chat_handler.handle_message(prompt, st.session_state.session_id)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Erreur: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})


if __name__ == "__main__":
    main()
