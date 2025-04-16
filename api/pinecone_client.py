import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

load_dotenv()

# Load from .env
api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX")
cloud = os.getenv("PINECONE_CLOUD", "aws")
region = os.getenv("PINECONE_REGION", "us-east-1")

# Create Pinecone client
pc = Pinecone(api_key=api_key)

# Create index if it doesn't exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=768,  # dimension for Gemini embeddings
        metric="cosine",
        spec=ServerlessSpec(cloud=cloud, region=region)
    )

# Connect to index
index = pc.Index(index_name)

def upsert_data(id: str, vector: List[float], metadata: Optional[Dict[str, Any]] = None) -> None:
    """
    Upsert a vector with metadata into the Pinecone index.
    
    Args:
        id: Unique identifier for the vector
        vector: The vector to store
        metadata: Optional metadata dictionary
    """
    index.upsert(vectors=[(id, vector, metadata or {})])

def query_data(vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Query the index for similar vectors.
    
    Args:
        vector: Query vector
        top_k: Number of results to return
        
    Returns:
        List of matches with their scores and metadata
    """
    results = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True
    )
    return results.matches

def delete_data(id: str) -> None:
    """
    Delete a vector from the index.
    
    Args:
        id: ID of the vector to delete
    """
    index.delete(ids=[id])

def list_indexes() -> List[str]:
    """
    List all available indexes.
    
    Returns:
        List of index names
    """
    return pc.list_indexes().names()
