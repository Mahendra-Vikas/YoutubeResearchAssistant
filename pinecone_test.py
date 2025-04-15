from pinecone_client import upsert_data, query_data

# Example dummy vector (match your actual embedding size later)
vector = [0.12, 0.34, 0.56, 0.78]

# Upsert memory with optional metadata
upsert_data("yt-script-001", vector, metadata={"topic": "AI", "type": "research"})

# Query similar memory
results = query_data(vector)
print(results)
