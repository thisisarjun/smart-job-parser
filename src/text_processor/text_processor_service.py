from typing import List, Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore


class TextProcessor:
    def __init__(
        self,
        ollama_embeddings: Optional[OllamaEmbeddings] = None,
        vector_store: Optional[InMemoryVectorStore] = None,
    ):
        self.ollama_embeddings = ollama_embeddings or OllamaEmbeddings(
            model="mxbai-embed-large"
        )
        self.vector_store = vector_store or InMemoryVectorStore(
            embedding=self.ollama_embeddings
        )

    def split_text(
        self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200
    ) -> List[str]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        return text_splitter.split_text(text)

    def embed_text(self, text: str) -> List[float]:
        return self.ollama_embeddings.embed_query(text)

    def add_texts_to_vector_store(self, texts: List[str]) -> None:
        self.vector_store.add_texts(texts)

    def process_text(self, text: str, query: str) -> List[Document]:
        chunks = self.split_text(text=text, chunk_size=1000, chunk_overlap=200)

        # Add the chunks to the vector store
        self.add_texts_to_vector_store(chunks)

        # Search the vector store
        results = self.vector_store.similarity_search(query=query)
        return results
