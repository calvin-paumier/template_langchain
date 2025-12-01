from abc import ABC, abstractmethod
from typing import Any

from langchain_core.tools import BaseTool


class ToolBindingLLMHandler(ABC):
    @abstractmethod
    def get_tool_binding_llm(self, tools: dict[str, BaseTool]) -> Any:
        pass
