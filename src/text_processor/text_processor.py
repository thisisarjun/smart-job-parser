from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore


class TextProcessor:
    def __init__(self):
        self.ollama_embeddings = OllamaEmbeddings(model="mxbai-embed-large")
        self.vector_store = InMemoryVectorStore(embedding=self.ollama_embeddings)

    def split_text(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        return text_splitter.split_text(text)

    def embed_text(self, text: str) -> list[str]:
        return self.ollama_embeddings.embed_query(text)

    def add_texts_to_vector_store(self, texts: list[str]) -> list[str]:
        self.vector_store.add_texts(texts)
        return self.vector_store


    def process_text(self, text: str, query: str) -> list[str]:
        chunks = self.split_text(
            text=text,
            chunk_size=1000,
            chunk_overlap=200
        )        
        
        # Add the chunks to the vector store
        vector_store = self.add_texts_to_vector_store(chunks)

        # Search the vector store
        results = vector_store.similarity_search(query=query)
        return results