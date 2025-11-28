from pydantic import BaseModel, Field


class LLMToolInput(BaseModel):
    """Input for LLM tools."""

    input: str = Field(description="Question to search for information")
    session_id: str = Field(default="default", description="Session hash for chat history")


class ApiMeteoToolInput(BaseModel):
    """Input for ApiMeteoTool."""

    city: str = Field(default="default", description="City to get weather information for")
    days: int = Field(default=0, description="Number of days for the weather forecast, 0 for current weather")
    session_id: str = Field(default="default", description="Session hash for chat history")


class ConfigTools:
    rag: str = "rag_tool"
    text_to_sql: str = "text_to_sql_tool"
    conversation: str = "conversation_tool"
    weather_api: str = "weather_api_tool"
