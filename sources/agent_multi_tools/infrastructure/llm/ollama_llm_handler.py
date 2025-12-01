from typing import Any

from langchain_ollama import ChatOllama

from sources.agent_multi_tools.ports.llm_handler import LLMHandler


class OllamaLLMHandler(LLMHandler):
    def __init__(
        self,
        model_name: str = "llama3.1:8b",
        temperature: float = 0.7,
        base_url: str = "http://localhost:11434",
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.base_url = base_url

        self.model = ChatOllama(model=self.model_name, temperature=self.temperature, base_url=self.base_url)

    def get_llm(self) -> Any:
        return self.model
