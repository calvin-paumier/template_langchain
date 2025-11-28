from abc import ABC, abstractmethod
from typing import Any

import pandas as pd


class DatabaseHandler(ABC):
    @abstractmethod
    def get_engine(self) -> Any:
        pass

    @abstractmethod
    def load_table(self, table_name: str, columns: list[str] | None = None) -> pd.DataFrame:
        pass

    @abstractmethod
    def embed_documents(self, df: pd.DataFrame, text_column: str, collection_name: str) -> None:
        pass

    @abstractmethod
    def get_vector_store(self) -> Any:
        pass
