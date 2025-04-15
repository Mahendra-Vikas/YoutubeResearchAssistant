from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os
import time

load_dotenv()

# Initialize Pinecone client
api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX")
cloud = os.getenv("PINECONE_CLOUD", "aws")
region = os.getenv("PINECONE_REGION", "us-east-1")

pc = Pinecone(api_key=api_key)

print("Current indexes:", pc.list_indexes().names())

# Delete the index if it exists
if index_name in pc.list_indexes().names():
    print(f"Deleting index '{index_name}'...")
    pc.delete_index(index_name)
    print("✅ Index deleted successfully")
    
    # Wait for deletion to complete
    time.sleep(5)

# Create new index with correct dimension
print(f"\nCreating new index '{index_name}' with dimension 768...")
pc.create_index(
    name=index_name,
    dimension=768,  # dimension for Gemini embeddings
    metric="cosine",
    spec=ServerlessSpec(cloud=cloud, region=region)
)

# Wait for index to be ready
time.sleep(5)

# Verify index configuration
print("\nVerifying index configuration:")
index_info = pc.describe_index(index_name)
print(f"Index name: {index_info.name}")
print(f"Dimension: {index_info.dimension}")
print(f"Metric: {index_info.metric}")
print(f"Status: {index_info.status}") 