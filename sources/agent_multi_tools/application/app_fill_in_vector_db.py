from sources.agent_multi_tools.config.config_sql import ConfigEmbeddingWikitext
from sources.agent_multi_tools.domain.usecases.fill_in_vector_db import fill_in_vector_db
from sources.agent_multi_tools.infrastructure.database.postgres_databse_handler import (
    PostgresDatabaseHandler,
)
from sources.agent_multi_tools.infrastructure.embeddings.ollama_embedding_handler import (
    OllamaEmbeddingHandler,
)

if __name__ == "__main__":
    embedding_handler = OllamaEmbeddingHandler()
    database_handler = PostgresDatabaseHandler(embedding_handler=embedding_handler)
    fill_in_vector_db(database_handler, ConfigEmbeddingWikitext)
