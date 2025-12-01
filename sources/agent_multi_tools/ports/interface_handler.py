from abc import ABC, abstractmethod


class InterfaceHandler(ABC):
    @abstractmethod
    def handle_message(self, message: str, session_id: str = None) -> str:
        pass
