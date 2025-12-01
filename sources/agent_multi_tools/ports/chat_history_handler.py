from abc import ABC, abstractmethod
from typing import Any


class ChatHistoryHandler(ABC):
    @abstractmethod
    def get_session_history(self, session_id: str) -> Any:
        pass

    @abstractmethod
    def clear_session_history(self, session_id: str) -> bool:
        pass

    @abstractmethod
    def clear_all_sessions(self) -> None:
        pass

    @abstractmethod
    def get_session_messages(self, session_id: str) -> list:
        pass

    @abstractmethod
    def add_message_to_session(self, session_id: str, message) -> None:
        pass
