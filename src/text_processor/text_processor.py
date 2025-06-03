from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings



def split_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return text_splitter.split_text(text)



# embed all the split texts
def embed_text(text: str) -> list[str]:
    ollama_embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    return ollama_embeddings.embed_query(text)

