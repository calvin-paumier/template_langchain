from typing import Any

from langchain_core.tools import BaseTool
from langchain_ollama import ChatOllama

from sources.agent_multi_tools.ports.tool_binding_llm_handler import ToolBindingLLMHandler


class OllamaToolBindingLLMHandler(ToolBindingLLMHandler):
    def __init__(
        self,
        model_name: str = "llama3.1:8b",
        base_url: str = "http://localhost:11434",
    ):
        self.model_name = model_name
        self.base_url = base_url

        self.model = ChatOllama(model=self.model_name, temperature=0., base_url=self.base_url)

    def get_tool_binding_llm(self, tools: list[BaseTool]) -> Any:
        return self.model.bind_tools(tools, tool_choice="any")
