from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict


class AgentState(TypedDict):
    messages: list[BaseMessage]
    current_tool: str | None
