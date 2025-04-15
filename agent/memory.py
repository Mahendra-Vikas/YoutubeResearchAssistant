# memory.py

from langchain_community.vectorstores import Pinecone
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from pinecone_client import index, upsert_data, query_data
import uuid

def store_memory(text: str, metadata: dict, embedding_model: GoogleGenerativeAIEmbeddings) -> None:
    """
    Stores the given text and metadata into the Pinecone vector store.

    Args:
        text (str): The text to store.
        metadata (dict): Additional metadata for the document.
        embedding_model: The embedding model to use.
    """
    # Generate embedding for the text
    embedding = embedding_model.embed_query(text)
    
    # Generate a unique ID for this memory
    memory_id = str(uuid.uuid4())
    
    # Store in Pinecone
    upsert_data(
        id=memory_id,
        vector=embedding,
        metadata={"text": text, **metadata}
    )

def retrieve_memory(query: str, embedding_model: GoogleGenerativeAIEmbeddings, top_k: int = 5) -> list[Document]:
    """
    Retrieves similar memories from the Pinecone vector store based on the query.

    Args:
        query (str): The input query text.
        embedding_model: The embedding model used for similarity search.
        top_k (int): Number of results to return.

    Returns:
        list: A list of retrieved Document objects.
    """
    # Generate embedding for the query
    query_embedding = embedding_model.embed_query(query)
    
    # Query Pinecone
    results = query_data(vector=query_embedding, top_k=top_k)
    
    # Convert results to Document objects
    documents = []
    for match in results:
        if match.metadata and "text" in match.metadata:
            doc = Document(
                page_content=match.metadata["text"],
                metadata={k: v for k, v in match.metadata.items() if k != "text"}
            )
            documents.append(doc)
    
    return documents
