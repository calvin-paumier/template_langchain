import inspect
from typing import Any

from langchain_core.runnables import RunnableConfig, RunnableWithMessageHistory
from langchain_core.tools import BaseTool

from sources.agent_multi_tools.config.config_agent import ConfigAgentState
from sources.agent_multi_tools.config.config_prompt import ConfigPrompts
from sources.agent_multi_tools.config.config_tools import ConfigTools
from sources.agent_multi_tools.ports.chat_history_handler import ChatHistoryHandler
from sources.agent_multi_tools.ports.llm_handler import LLMHandler
from sources.agent_multi_tools.utils.prompt_formater import PromptFormater


class ToolRouter:
    def __init__(self, llm_handler: LLMHandler, chat_history_handler: ChatHistoryHandler, tools: dict[str, BaseTool]):
        self.llm = llm_handler.get_llm().bind_tools(list(tools.values()), tool_choice="any")
        self.chat_history_handler = chat_history_handler
        self.tools_descriptions = self._get_tool_descriptions(tools)
        self.tool_mapping = self._get_tool_mapping(tools)

    def _get_tool_descriptions(self, tools: dict[str, BaseTool]) -> dict[str, str]:
        tools_descriptions = {}
        for name, function in tools.items():
            first_line = inspect.getdoc(function).split("\n")[0]
            tools_descriptions[name] = first_line
        return tools_descriptions

    def _get_tool_mapping(self, tools: dict[str, BaseTool]) -> dict[str, str]:
        tool_mapping = {}
        for name, tool in tools.items():
            tool_mapping[tool.name] = name
        return tool_mapping

    def _get_routing_chain(self) -> RunnableWithMessageHistory:
        tools_list = "\n".join([f"- {name}: {description}" for name, description in self.tools_descriptions.items()])

        routing_prompt = PromptFormater.create_chat_prompt_with_history(ConfigPrompts.ROUTING.format(tools_list))

        chain = routing_prompt | self.llm

        return RunnableWithMessageHistory(
            chain,
            self.chat_history_handler.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    def route_to_tool(self, state: dict[str, Any], config: RunnableConfig) -> str:
        messages = state.get(ConfigAgentState.MESSAGES)
        last_message = messages[-1]
        question = last_message.content

        routing_chain = self._get_routing_chain()

        response = routing_chain.invoke(
            {"input": question}, config={"configurable": {"session_id": config["configurable"]["session_id"]}}
        )

        tool_choice = self.tool_mapping.get(response.tool_calls[0].get("name"))

        response.tool_calls[0]["args"]["session_id"] = config["configurable"]["session_id"]

        available_tools = list(self.tools_descriptions.keys())

        if tool_choice not in available_tools:
            tool_choice = ConfigTools.conversation

        state[ConfigAgentState.CURRENT_TOOL] = tool_choice
        state[ConfigAgentState.MESSAGES] = messages + [response]

        return state
