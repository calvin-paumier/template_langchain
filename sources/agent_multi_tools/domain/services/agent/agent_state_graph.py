from typing import Any

from langchain_core.runnables import Runnable
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from sources.agent_multi_tools.config.config_agent import ConfigAgent, ConfigAgentState
from sources.agent_multi_tools.domain.ports.chat_history_handler import ChatHistoryHandler
from sources.agent_multi_tools.domain.ports.llm_handler import LLMHandler
from sources.agent_multi_tools.domain.services.agent.agent_state import AgentState
from sources.agent_multi_tools.domain.services.agent.agent_tool_router import ToolRouter


class AgentStateGraph:
    def __init__(
        self,
        llm_handler: LLMHandler,
        chat_history_handler: ChatHistoryHandler,
        tools: dict[str, Runnable[Any, Any]],
        session_id: str = "default",
    ):
        self.llm_handler = llm_handler
        self.chat_history_handler = chat_history_handler
        self.tools = tools
        self.session_id = session_id

    def compile_workflow(self, state: AgentState, memory: bool = False) -> Runnable:
        workflow = StateGraph(state)

        # Router
        workflow.add_node(
            ConfigAgent.NODE_ROUTER_AGENT,
            ToolRouter(self.llm_handler, self.chat_history_handler, self.tools).route_to_tool,
        )
        workflow.add_edge(START, ConfigAgent.NODE_ROUTER_AGENT)

        # Tools
        for name, function in self.tools.items():
            workflow.add_node(
                name,
                ToolNode([function]),
            )
            workflow.add_edge(name, END)

        workflow.add_conditional_edges(
            ConfigAgent.NODE_ROUTER_AGENT,
            lambda state: state.get(ConfigAgentState.CURRENT_TOOL),
            list(self.tools.keys()),
        )

        if memory:
            return workflow.compile(checkpointer=MemorySaver())
        else:
            return workflow.compile()
