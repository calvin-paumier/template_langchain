from langchain_ollama import OllamaEmbeddings

from sources.agent_multi_tools.domain.ports.embedding_handler import EmbeddingHandler


class OllamaEmbeddingHandler(EmbeddingHandler):
    def __init__(
        self,
        model: str = "nomic-embed-text:latest",
        base_url: str = "http://localhost:11434",
    ):
        self.model = model
        self.embeddings = OllamaEmbeddings(model=model, base_url=base_url)

    def get_embeddings(self):
        return self.embeddings

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.embeddings.embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        return self.embeddings.embed_query(text)
