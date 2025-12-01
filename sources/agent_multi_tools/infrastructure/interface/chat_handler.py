import uuid

from langchain_core.messages import HumanMessage

from sources.agent_multi_tools.application.agent.agent_state_graph import AgentStateGraph
from sources.agent_multi_tools.infrastructure.chat_history.in_memory_chat_history_handler import InMemoryChatHistoryHandler
from sources.agent_multi_tools.ports.interface_handler import InterfaceHandler


class ChatHandler(InterfaceHandler):
    def __init__(self, agent_state_graph: AgentStateGraph, chat_history_handler: InMemoryChatHistoryHandler):
        self.agent_state_graph = agent_state_graph
        self.chat_history_handler = chat_history_handler
        self.sessions: dict[str, str] = {}

    def handle_message(self, message: str, session_id: str) -> str:
        """Traite un message utilisateur et retourne la réponse"""
        if session_id not in self.sessions:
            self.sessions[session_id] = str(uuid.uuid4())

        config = {"configurable": {"thread_id": self.sessions[session_id], "session_id": session_id}}

        result = self.agent_state_graph.invoke({"messages": [HumanMessage(content=message)]}, config)

        return result.get("messages")[-1].content
