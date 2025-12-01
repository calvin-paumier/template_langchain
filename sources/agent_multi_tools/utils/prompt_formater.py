from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


class PromptFormater:
    @staticmethod
    def create_chat_prompt_with_history(system_message: str) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                MessagesPlaceholder(variable_name="chat_history"),
                ("user", "{input}"),
            ]
        )

    @staticmethod
    def format_string(template: str, **kwargs) -> str:
        return template.format(**kwargs)
