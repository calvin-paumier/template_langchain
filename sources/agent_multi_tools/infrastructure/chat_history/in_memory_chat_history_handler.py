from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)

from sources.agent_multi_tools.domain.ports.chat_history_handler import ChatHistoryHandler


class InMemoryChatHistoryHandler(ChatHistoryHandler):
    def __init__(self):
        self._session_store: dict[str, BaseChatMessageHistory] = {}

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self._session_store:
            self._session_store[session_id] = InMemoryChatMessageHistory()
        return self._session_store[session_id]

    def clear_session_history(self, session_id: str) -> bool:
        if session_id in self._session_store:
            del self._session_store[session_id]
            return True
        return False

    def clear_all_sessions(self) -> None:
        self._session_store.clear()

    def get_session_messages(self, session_id: str) -> list:
        if session_id in self._session_store:
            return self._session_store[session_id].messages
        return []

    def add_message_to_session(self, session_id: str, message) -> None:
        history = self.get_session_history(session_id)
        history.add_message(message)
