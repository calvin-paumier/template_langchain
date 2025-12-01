from abc import ABC, abstractmethod
from typing import Any


class LLMHandler(ABC):
    @abstractmethod
    def get_llm(self) -> Any:
        pass
