from typing import Any

import pandas as pd
from langchain_postgres import PGVector
from sqlalchemy import Engine, create_engine, text

from sources.agent_multi_tools.ports.database_handler import DatabaseHandler
from sources.agent_multi_tools.ports.embedding_handler import EmbeddingHandler


class PostgresDatabaseHandler(DatabaseHandler):
    def __init__(
        self,
        host: str = "localhost",
        port: str = "5432",
        database: str = "my_db",
        username: str = "my_user",
        password: str = "my_password",
        embedding_handler: EmbeddingHandler | None = None,
    ):
        self.connection_string = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
        self.embedding_handler = embedding_handler
        self.engine = create_engine(self.connection_string)

        self._initialize_database()

    def get_engine(self) -> Engine:
        return self.engine

    def load_table(self, table_name: str, columns: list[str] | None = None) -> pd.DataFrame:
        cols = "*" if columns is None else ", ".join(columns)
        query = f"SELECT {cols} FROM {table_name};"
        with self.engine.connect() as conn:
            df = pd.read_sql(query, conn)
        return df

    def embed_documents(self, df: pd.DataFrame, text_column: str, collection_name: str) -> None:
        texts = df[text_column].tolist()
        ids = df["id"].tolist() if "id" in df.columns else None

        PGVector.from_texts(
            texts=texts,
            embedding=self.embedding_handler.get_embeddings(),
            connection=self.connection_string,
            collection_name=collection_name,
            ids=ids,
        )

    def get_vector_store(self, collection_name: str) -> Any:
        return PGVector(
            embeddings=self.embedding_handler.get_embeddings(),
            connection=self.connection_string,
            collection_name=collection_name,
            use_jsonb=True,
        )

    def _initialize_database(self):
        engine = self.get_engine()
        with engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
